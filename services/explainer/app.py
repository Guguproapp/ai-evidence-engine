import json
import logging
import os
import time
import uuid
from collections import defaultdict, deque

from flask import Flask, jsonify, request


ALLOWED_STATUSES = {"Authentic", "Modified", "Unknown", "Invalid Signature"}
MAX_REQUEST_BYTES = 16 * 1024
RATE_LIMIT_PER_MINUTE = 10
DEFAULT_MODEL = "gemini-2.5-flash"

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_REQUEST_BYTES
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("evidence-explainer")
attempts = defaultdict(deque)


def _allowed_origins():
    configured = os.getenv(
        "ALLOWED_ORIGINS",
        "https://ai-evidence-engine-gugupro.artistuncle.chatgpt.site",
    )
    return {origin.strip() for origin in configured.split(",") if origin.strip()}


def _cors(response):
    origin = request.headers.get("Origin")
    if origin and origin in _allowed_origins():
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Vary"] = "Origin"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    return response


@app.after_request
def add_security_headers(response):
    response.headers["Cache-Control"] = "no-store"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return _cors(response)


def _rate_limited(client):
    now = time.monotonic()
    queue = attempts[client]
    while queue and now - queue[0] > 60:
        queue.popleft()
    if len(queue) >= RATE_LIMIT_PER_MINUTE:
        return True
    queue.append(now)
    return False


def _validate_payload(payload):
    if not isinstance(payload, dict):
        raise ValueError("A JSON object is required.")
    status = payload.get("status")
    if status not in ALLOWED_STATUSES:
        raise ValueError("status must be a supported deterministic verification result.")
    facts = payload.get("facts")
    if not isinstance(facts, dict):
        raise ValueError("facts must be an object.")

    allowed_fact_keys = {
        "action",
        "changed_ratio",
        "c2pa_manifest_count",
        "c2pa_status",
        "evidence_id",
        "parent_version_id",
        "registry_status",
        "signature_status",
        "signer",
        "version_id",
    }
    sanitized = {}
    for key in allowed_fact_keys:
        value = facts.get(key)
        if isinstance(value, (str, int, float, bool)) or value is None:
            sanitized[key] = value
    if not sanitized.get("version_id"):
        raise ValueError("facts.version_id is required.")
    return status, sanitized


def _generate_explanation(status, facts):
    from google import genai
    from google.genai.types import GenerateContentConfig, HttpOptions

    model = os.getenv("GEMINI_MODEL", DEFAULT_MODEL)
    client = genai.Client(http_options=HttpOptions(api_version="v1"))
    prompt = (
        "Explain the following already-determined image verification result to a "
        "non-technical small-business buyer in two short sentences. Use only the "
        "provided facts. Never change, reinterpret, or independently decide the "
        "verification status. Do not give a copyright, infringement, plagiarism, "
        "or legal verdict. If evidence is unknown, say that absence of evidence does "
        "not prove the image is fake.\n\n"
        + json.dumps({"deterministic_status": status, "facts": facts}, ensure_ascii=False)
    )
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=GenerateContentConfig(
            temperature=0.1,
            max_output_tokens=180,
            system_instruction=(
                "You are the Evidence Explainer. Cryptographic verification is the "
                "source of truth; you only explain its supplied result."
            ),
        ),
    )
    explanation = (response.text or "").strip()
    if not explanation:
        raise RuntimeError("Gemini returned an empty explanation.")
    return explanation, model


@app.get("/health")
def health():
    return jsonify(
        {
            "service": "ai-evidence-explainer",
            "status": "ok",
            "google_cloud": "Cloud Run",
            "gemini_backend": "Vertex AI",
            "model": os.getenv("GEMINI_MODEL", DEFAULT_MODEL),
        }
    )


@app.route("/v1/explain", methods=["POST", "OPTIONS"])
def explain():
    if request.method == "OPTIONS":
        return ("", 204)
    client = request.headers.get("X-Forwarded-For", request.remote_addr or "unknown").split(",")[0].strip()
    if _rate_limited(client):
        return jsonify({"error": "rate_limit_exceeded"}), 429

    request_id = str(uuid.uuid4())
    started = time.monotonic()
    try:
        status, facts = _validate_payload(request.get_json(silent=True))
        explanation, model = _generate_explanation(status, facts)
    except ValueError as error:
        return jsonify({"error": "invalid_request", "message": str(error)}), 400
    except Exception:
        logger.exception("Gemini explanation failed request_id=%s", request_id)
        return jsonify({"error": "gemini_unavailable", "request_id": request_id}), 503

    elapsed_ms = round((time.monotonic() - started) * 1000)
    logger.info(
        "evidence_explained request_id=%s evidence_id=%s status=%s model=%s latency_ms=%s",
        request_id,
        facts.get("evidence_id", "none"),
        status,
        model,
        elapsed_ms,
    )
    return jsonify(
        {
            "request_id": request_id,
            "verification_status": status,
            "explanation": explanation,
            "model": model,
            "provider": "Gemini API on Vertex AI",
            "decision_source": "AI Evidence Engine cryptographic verification",
        }
    )


@app.errorhandler(413)
def request_too_large(_error):
    return jsonify({"error": "request_too_large"}), 413


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
