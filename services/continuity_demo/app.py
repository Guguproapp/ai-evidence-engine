import copy
import hashlib
import json
import logging
import os
import tempfile
import time
import uuid
from collections import defaultdict, deque
from pathlib import Path

import requests
from flask import Flask, jsonify, request, send_from_directory

from ai_evidence.canonical import canonical_json
from ai_evidence.registry import Registry


APP_ROOT = Path(__file__).resolve().parent
CONTAINER_DEMO_ASSET = APP_ROOT / "static" / "version-3.png"
DEFAULT_DEMO_ASSET = CONTAINER_DEMO_ASSET if CONTAINER_DEMO_ASSET.is_file() else APP_ROOT.parents[1] / "apps" / "web" / "public" / "demo" / "version-3.png"
DEMO_ASSET = Path(os.getenv("DEMO_EVIDENCE_PATH", str(DEFAULT_DEMO_ASSET)))
DEMO_MANIFEST_ID = "urn:c2pa:cd1f092b-94fe-4623-9e51-a8eacd50a762"
MAX_RUNS_PER_MINUTE = 5

app = Flask(__name__, static_folder=str(APP_ROOT / "static"), static_url_path="/static")
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("aee-continuity-demo")
attempts = defaultdict(deque)
remote_client_factory = None


def _rate_limited(client):
    now = time.monotonic()
    queue = attempts[client]
    while queue and now - queue[0] > 60:
        queue.popleft()
    if len(queue) >= MAX_RUNS_PER_MINUTE:
        return True
    queue.append(now)
    return False


def _remote_client():
    if remote_client_factory is not None:
        return remote_client_factory()
    return RemoteBlackBoxClient(
        os.environ["REMOTE_BLACKBOX_URL"].rstrip("/"),
        os.getenv("REMOTE_BLACKBOX_AUDIENCE", os.environ["REMOTE_BLACKBOX_URL"]).rstrip("/"),
    )


class RemoteBlackBoxClient:
    def __init__(self, service_url, audience):
        self.service_url = service_url
        self.audience = audience

    def _token(self):
        from google.auth.transport.requests import Request
        from google.oauth2 import id_token

        return id_token.fetch_id_token(Request(), self.audience)

    def _post(self, path, **kwargs):
        headers = dict(kwargs.pop("headers", {}))
        headers["Authorization"] = "Bearer " + self._token()
        response = requests.post(self.service_url + path, headers=headers, timeout=90, **kwargs)
        try:
            payload = response.json()
        except ValueError:
            payload = {"error": "invalid_remote_response"}
        if response.status_code >= 400:
            raise RuntimeError(f"Remote Black Box HTTP {response.status_code}: {payload.get('error', 'unknown_error')}")
        return payload

    def seal(self, event, evidence_path):
        data = evidence_path.read_bytes()
        fields = {
            "schema_version": event["schema_version"],
            "passport_id": event["passport_id"],
            "event_id": event["event_id"],
            "content_sha256": event["exact_hash"],
            "content_type": "image/png",
            "signed_event": canonical_json(event).decode("utf-8"),
        }
        return self._post(
            "/v1/evidence/seal",
            data=fields,
            files={"evidence_file": (evidence_path.name, data, "image/png")},
        )

    def retrieve(self, passport_id, event_id):
        return self._post(
            "/v1/evidence/retrieve",
            json={"passport_id": passport_id, "event_id": event_id},
        )


def _stage(name, status, detail):
    return {"name": name, "status": status, "detail": detail}


def run_continuity(asset_path=DEMO_ASSET):
    if not asset_path.is_file():
        raise RuntimeError("Built-in synthetic evidence is unavailable")
    evidence_bytes = asset_path.read_bytes()
    content_sha256 = hashlib.sha256(evidence_bytes).hexdigest()

    with tempfile.TemporaryDirectory(prefix="aee-continuity-demo-") as temp_dir:
        temp = Path(temp_dir)
        registry = Registry(temp / "registry", temp / "keys", issuer_id="gugupro-continuity-demo")
        event = registry.register_file(
            asset_path,
            asset_type="image",
            media_type="image/png",
            evidence_profile="aee.image.c2pa.v1",
            c2pa_manifest_id=DEMO_MANIFEST_ID,
            provider="gugupro",
            model="aee-continuity-demo",
            model_version="1",
            action_type="development_remote_seal",
            involvement_level="L0",
            operator_type="program",
            human_approval=True,
            blackbox_available=False,
        )
        event_snapshot = copy.deepcopy(event)
        event_bytes_before = canonical_json(event)
        pre_verify = registry.verify_event(event)
        if not (pre_verify["verified"] and pre_verify["signature_valid"] and pre_verify["hash_valid"]):
            raise RuntimeError("Local Signed Event pre-seal verification failed")
        if event["exact_hash"] != content_sha256:
            raise RuntimeError("Local Signed Event content SHA-256 mismatch")

        remote = _remote_client()
        sealed = remote.seal(event, asset_path)
        retrieved = remote.retrieve(event["passport_id"], event["event_id"])
        post_verify = registry.verify_event(event)
        event_unchanged = event == event_snapshot and canonical_json(event) == event_bytes_before

        continuity = all(
            [
                sealed.get("passport_id") == event["passport_id"],
                sealed.get("event_id") == event["event_id"],
                sealed.get("content_sha256") == content_sha256,
                sealed.get("signed_event_hash") == event["event_hash"],
                bool(sealed.get("generation")),
                bool(sealed.get("retention_expiration")),
                retrieved.get("passport_id") == event["passport_id"],
                retrieved.get("event_id") == event["event_id"],
                retrieved.get("stored_sha256") == content_sha256,
                retrieved.get("retrieved_sha256") == content_sha256,
                retrieved.get("signed_event_hash") == event["event_hash"],
                retrieved.get("hash_match") is True,
                post_verify["verified"],
                post_verify["signature_valid"],
                post_verify["hash_valid"],
                event_unchanged,
            ]
        )
        if not continuity:
            raise RuntimeError("Evidence continuity verification failed")

        stages = [
            _stage("Built-in synthetic evidence", "PASS", f"proofcart-version-3.png · {len(evidence_bytes)} bytes"),
            _stage("Signed aee.event.v1", "PASS", event["event_id"]),
            _stage("Signature verification before seal", "PASS", "RSA-2048/SHA-256 valid"),
            _stage("IAM-protected Remote Black Box", "PASS", "AEE Backend service-to-service call"),
            _stage("Google Cloud seal", "PASS", sealed["object_path"]),
            _stage("Object generation", "PASS", str(sealed["generation"])),
            _stage("Retention expiration", "PASS", sealed["retention_expiration"]),
            _stage("Evidence retrieval", "PASS", f"generation {retrieved['generation']}"),
            _stage("SHA-256 reverification", "PASS", retrieved["retrieved_sha256"]),
            _stage("Signed Event verification after seal", "PASS", "Signature and Event Hash remain valid"),
            _stage("Evidence Continuity", "PASS", "IDs, hashes, Event reference, and original Signed Event all match"),
        ]
        logger.info(
            "continuity_demo request_id=%s passport_id=%s event_id=%s generation=%s result=PASS",
            str(uuid.uuid4()),
            event["passport_id"],
            event["event_id"],
            sealed["generation"],
        )
        return {
            "ok": True,
            "environment": "Development / Test",
            "asset": {"id": "proofcart-version-3", "label": "AEE built-in synthetic ProofCart Version 3"},
            "signed_event": {
                "schema_version": event["schema_version"],
                "passport_id": event["passport_id"],
                "event_id": event["event_id"],
                "event_hash": event["event_hash"],
                "content_sha256": event["exact_hash"],
                "signature_algorithm": event["signature_algorithm"],
                "pre_seal_signature_valid": pre_verify["signature_valid"],
                "post_seal_signature_valid": post_verify["signature_valid"],
                "event_unchanged": event_unchanged,
            },
            "remote_seal": {
                "object_path": sealed["object_path"],
                "generation": sealed["generation"],
                "metageneration": sealed["metageneration"],
                "retention_expiration": sealed["retention_expiration"],
                "storage_location": sealed["storage_location"],
            },
            "retrieval": {
                "generation": retrieved["generation"],
                "stored_sha256": retrieved["stored_sha256"],
                "retrieved_sha256": retrieved["retrieved_sha256"],
                "hash_match": retrieved["hash_match"],
            },
            "stages": stages,
            "evidence_continuity": "PASS",
        }


@app.after_request
def _security_headers(response):
    response.headers["Cache-Control"] = "no-store"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "default-src 'self'; style-src 'self'; script-src 'self'; img-src 'self'; connect-src 'self'"
    return response


@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.get("/health")
def health():
    return jsonify(
        {
            "service": "aee-continuity-demo",
            "status": "ok",
            "environment": "Development / Test",
            "asset_available": DEMO_ASSET.is_file(),
            "remote_blackbox": "IAM protected",
        }
    )


@app.get("/v1/demo/assets")
def assets():
    return jsonify(
        {
            "assets": [
                {
                    "id": "proofcart-version-3",
                    "label": "AEE built-in synthetic ProofCart Version 3",
                    "content_type": "image/png",
                    "preview": "/static/version-3.png",
                }
            ]
        }
    )


@app.post("/v1/demo/continuity")
def continuity():
    client = request.headers.get("X-Forwarded-For", request.remote_addr or "unknown").split(",")[0].strip()
    if _rate_limited(client):
        return jsonify({"ok": False, "error": "rate_limit_exceeded"}), 429
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict) or payload.get("asset_id") != "proofcart-version-3":
        return jsonify({"ok": False, "error": "invalid_asset"}), 400
    try:
        return jsonify(run_continuity())
    except Exception:
        request_id = str(uuid.uuid4())
        logger.exception("continuity_demo failed request_id=%s", request_id)
        return jsonify({"ok": False, "error": "continuity_failed", "request_id": request_id}), 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
