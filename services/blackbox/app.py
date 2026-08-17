import base64
import hashlib
import json
import logging
import os
import re
import uuid
from datetime import datetime, timezone

from flask import Flask, jsonify, request


ALLOWED_SCHEMA_VERSIONS = {"aee.event.v1"}
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}
FORBIDDEN_STORAGE_FIELDS = {
    "acl",
    "bucket",
    "change_retention",
    "generation",
    "object_path",
    "path",
    "retention",
    "service_account",
}
MAX_FILE_BYTES = 10 * 1024 * 1024
MAX_PUBLIC_KEY_BYTES = 8 * 1024
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
EVENT_HASH_RE = re.compile(r"^sha256:[0-9a-f]{64}$")

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_BYTES + (1024 * 1024)
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("aee-blackbox-test")

# Tests replace this with an in-memory implementation. Production uses ADC and
# the Cloud Run service account; no service-account key is accepted or stored.
storage_client_factory = None


def _now():
    return datetime.now(timezone.utc).isoformat()


def _iso(value):
    return value.isoformat() if value else None


def _storage_client():
    if storage_client_factory is not None:
        return storage_client_factory()
    from google.cloud import storage

    return storage.Client(project=os.environ["GOOGLE_CLOUD_PROJECT"])


def _bucket_name():
    value = os.getenv("EVIDENCE_BUCKET", "").strip()
    if not value:
        raise RuntimeError("EVIDENCE_BUCKET is not configured")
    return value


def _normalize_identifier(value, kind):
    text = str(value or "").strip()
    prefix = f"urn:aee:{kind}:v1:"
    if text.startswith("urn:"):
        if not text.startswith(prefix):
            raise ValueError(f"invalid {kind}_id")
        text = text[len(prefix) :]
    try:
        return str(uuid.UUID(text))
    except (ValueError, AttributeError, TypeError):
        raise ValueError(f"invalid {kind}_id") from None


def _normalize_sha256(value):
    digest = str(value or "").strip().lower()
    if digest.startswith("sha256:"):
        digest = digest[7:]
    if not SHA256_RE.fullmatch(digest):
        raise ValueError("content_sha256 must contain exactly 64 hexadecimal characters")
    return digest


def _object_path(passport_id, event_id):
    return f"evidence/v1/passports/{passport_id}/events/{event_id}/evidence"


def _validate_content_type(content_type, data):
    if content_type not in ALLOWED_CONTENT_TYPES:
        raise ValueError("unsupported content_type")
    signatures = {
        "image/png": data.startswith(b"\x89PNG\r\n\x1a\n"),
        "image/jpeg": data.startswith(b"\xff\xd8\xff"),
        "image/webp": len(data) >= 12 and data[:4] == b"RIFF" and data[8:12] == b"WEBP",
    }
    if not signatures[content_type]:
        raise ValueError("evidence_file bytes do not match content_type")


def _parse_signed_event(value):
    try:
        event = json.loads(str(value or ""))
    except json.JSONDecodeError:
        raise ValueError("signed_event must be valid JSON") from None
    if not isinstance(event, dict):
        raise ValueError("signed_event must be a JSON object")
    if event.get("schema_version") not in ALLOWED_SCHEMA_VERSIONS:
        raise ValueError("signed_event has an unsupported schema_version")
    event_hash = str(event.get("event_hash") or "").lower()
    if not EVENT_HASH_RE.fullmatch(event_hash):
        raise ValueError("signed_event event_hash is invalid")
    if not str(event.get("signature") or "").strip():
        raise ValueError("signed_event signature is required")
    if not str(event.get("signature_algorithm") or "").strip():
        raise ValueError("signed_event signature_algorithm is required")
    return event


def _parse_public_key(value):
    public_key = str(value or "").strip()
    if not public_key:
        raise ValueError("issuer_public_key is required")
    if len(public_key.encode("utf-8")) > MAX_PUBLIC_KEY_BYTES:
        raise ValueError("issuer_public_key is too large")
    if not public_key.startswith("-----BEGIN PUBLIC KEY-----") or not public_key.endswith("-----END PUBLIC KEY-----"):
        raise ValueError("issuer_public_key must be a PEM public key")
    return public_key + "\n"


def _event_content_sha256(event):
    content_digest = event.get("content_digest")
    exact_hash = event.get("exact_hash")
    digest = _normalize_sha256(content_digest if content_digest is not None else exact_hash)
    if content_digest is not None and exact_hash is not None and digest != _normalize_sha256(exact_hash):
        raise ValueError("signed_event content_digest and exact_hash do not match")
    return digest


def _stored_event(blob):
    metadata = blob.metadata or {}
    try:
        event = json.loads(metadata.get("signed_event") or "")
        public_key = base64.b64decode(metadata.get("issuer_public_key_b64") or "", validate=True).decode("utf-8")
    except (ValueError, UnicodeDecodeError, json.JSONDecodeError):
        raise ValueError("stored Signed Event recovery metadata is invalid") from None
    event = _parse_signed_event(json.dumps(event, separators=(",", ":"), sort_keys=True))
    public_key = _parse_public_key(public_key)
    passport_id = _normalize_identifier(event.get("passport_id"), "passport")
    event_id = _normalize_identifier(event.get("event_id"), "event")
    if passport_id != _normalize_identifier(metadata.get("passport_id"), "passport"):
        raise ValueError("stored Signed Event passport_id does not match object metadata")
    if event_id != _normalize_identifier(metadata.get("event_id"), "event"):
        raise ValueError("stored Signed Event event_id does not match object metadata")
    if _event_content_sha256(event) != _normalize_sha256(metadata.get("content_sha256")):
        raise ValueError("stored Signed Event content SHA-256 does not match object metadata")
    if event["event_hash"].lower() != str(metadata.get("signed_event_hash") or "").lower():
        raise ValueError("stored Signed Event hash does not match object metadata")
    return event, public_key


def _forbidden_fields(values):
    return sorted(FORBIDDEN_STORAGE_FIELDS.intersection(values.keys()))


def _is_error(error, status_code, class_name):
    code = getattr(error, "code", None)
    return code == status_code or error.__class__.__name__ == class_name


def _audit(request_id, operation, result, passport_id=None, event_id=None, generation=None, hash_match=None):
    record = {
        "request_id": request_id,
        "operation": operation,
        "passport_id": passport_id,
        "event_id": event_id,
        "object_generation": str(generation) if generation is not None else None,
        "timestamp": _now(),
        "result": result,
        "hash_match": hash_match,
    }
    logger.info("blackbox_audit %s", json.dumps(record, ensure_ascii=True, sort_keys=True))


@app.after_request
def _security_headers(response):
    response.headers["Cache-Control"] = "no-store"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


@app.get("/health")
def health():
    return jsonify(
        {
            "service": "aee-remote-blackbox-test",
            "status": "ok",
            "environment": "Development / Test",
            "bucket_configured": bool(os.getenv("EVIDENCE_BUCKET")),
            "operations": ["sealEvidence", "retrieveEvidence", "history", "downloadEvidence"],
        }
    )


@app.post("/v1/evidence/seal")
def seal_evidence():
    request_id = str(uuid.uuid4())
    passport_id = None
    event_id = None
    try:
        forbidden = _forbidden_fields(request.form)
        if forbidden:
            raise ValueError("client-controlled storage fields are not allowed: " + ", ".join(forbidden))
        if request.form.get("schema_version") not in ALLOWED_SCHEMA_VERSIONS:
            raise ValueError("unsupported schema_version")
        passport_id = _normalize_identifier(request.form.get("passport_id"), "passport")
        event_id = _normalize_identifier(request.form.get("event_id"), "event")
        expected_sha256 = _normalize_sha256(request.form.get("content_sha256"))
        signed_event = _parse_signed_event(request.form.get("signed_event"))
        issuer_public_key = _parse_public_key(request.form.get("issuer_public_key"))
        signed_passport_id = _normalize_identifier(signed_event.get("passport_id"), "passport")
        signed_event_id = _normalize_identifier(signed_event.get("event_id"), "event")
        signed_content_sha256 = _event_content_sha256(signed_event)
        if passport_id != signed_passport_id:
            raise ValueError("passport_id does not match signed_event")
        if event_id != signed_event_id:
            raise ValueError("event_id does not match signed_event")
        if expected_sha256 != signed_content_sha256:
            raise ValueError("content_sha256 does not match signed_event")
        content_type = str(request.form.get("content_type") or "").strip().lower()
        uploaded = request.files.get("evidence_file")
        if uploaded is None:
            raise ValueError("evidence_file is required")
        data = uploaded.read(MAX_FILE_BYTES + 1)
        if not data:
            raise ValueError("evidence_file must not be empty")
        if len(data) > MAX_FILE_BYTES:
            raise ValueError("evidence_file exceeds 10 MB")
        _validate_content_type(content_type, data)
        actual_sha256 = hashlib.sha256(data).hexdigest()
        if actual_sha256 != signed_content_sha256:
            raise ValueError("evidence_file SHA-256 does not match signed_event")

        object_path = _object_path(passport_id, event_id)
        blob = _storage_client().bucket(_bucket_name()).blob(object_path)
        blob.metadata = {
            "aee_environment": "development_test",
            "schema_version": request.form["schema_version"],
            "passport_id": passport_id,
            "event_id": event_id,
            "content_sha256": expected_sha256,
            "signed_event_hash": signed_event["event_hash"].lower(),
            "signed_event": json.dumps(signed_event, ensure_ascii=True, separators=(",", ":"), sort_keys=True),
            "issuer_public_key_b64": base64.b64encode(issuer_public_key.encode("utf-8")).decode("ascii"),
        }
        if signed_event.get("parent_event"):
            blob.metadata["parent_event_id"] = _normalize_identifier(signed_event["parent_event"], "event")
        if signed_event.get("action_type"):
            blob.metadata["event_type"] = str(signed_event["action_type"])[:128]
        blob.upload_from_string(data, content_type=content_type, if_generation_match=0)
        blob.reload()
        _audit(request_id, "sealEvidence", "PASS", passport_id, event_id, blob.generation, True)
        return (
            jsonify(
                {
                    "ok": True,
                    "request_id": request_id,
                    "environment": "Development / Test",
                    "passport_id": passport_id,
                    "event_id": event_id,
                    "object_path": object_path,
                    "generation": str(blob.generation),
                    "metageneration": int(blob.metageneration),
                    "content_sha256": expected_sha256,
                    "signed_event_hash": signed_event["event_hash"].lower(),
                    "size": int(blob.size),
                    "content_type": blob.content_type or content_type,
                    "created_at": _iso(blob.time_created),
                    "retention_expiration": _iso(blob.retention_expiration_time),
                    "storage_location": os.getenv("STORAGE_LOCATION", "ASIA-EAST1"),
                }
            ),
            201,
        )
    except ValueError as error:
        _audit(request_id, "sealEvidence", "REJECTED", passport_id, event_id)
        return jsonify({"ok": False, "request_id": request_id, "error": "invalid_request", "message": str(error)}), 400
    except Exception as error:
        if _is_error(error, 412, "PreconditionFailed"):
            _audit(request_id, "sealEvidence", "ALREADY_SEALED", passport_id, event_id)
            return jsonify({"ok": False, "request_id": request_id, "error": "evidence_already_sealed"}), 409
        logger.exception("sealEvidence failed request_id=%s", request_id)
        _audit(request_id, "sealEvidence", "ERROR", passport_id, event_id)
        return jsonify({"ok": False, "request_id": request_id, "error": "storage_unavailable"}), 503


@app.post("/v1/evidence/retrieve")
def retrieve_evidence():
    request_id = str(uuid.uuid4())
    passport_id = None
    event_id = None
    try:
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            raise ValueError("a JSON object is required")
        forbidden = _forbidden_fields(payload)
        if forbidden:
            raise ValueError("client-controlled storage fields are not allowed: " + ", ".join(forbidden))
        passport_id = _normalize_identifier(payload.get("passport_id"), "passport")
        event_id = _normalize_identifier(payload.get("event_id"), "event")
        blob = _storage_client().bucket(_bucket_name()).blob(_object_path(passport_id, event_id))
        blob.reload()
        metadata = blob.metadata or {}
        stored_schema_version = str(metadata.get("schema_version") or "")
        stored_passport_id = _normalize_identifier(metadata.get("passport_id"), "passport")
        stored_event_id = _normalize_identifier(metadata.get("event_id"), "event")
        if stored_schema_version not in ALLOWED_SCHEMA_VERSIONS:
            raise ValueError("stored schema_version is invalid")
        if stored_passport_id != passport_id or stored_event_id != event_id:
            raise ValueError("stored continuity identifiers do not match request")
        data = blob.download_as_bytes()
        stored_sha256 = _normalize_sha256(metadata.get("content_sha256"))
        signed_event_hash = str(metadata.get("signed_event_hash") or "").lower()
        if not EVENT_HASH_RE.fullmatch(signed_event_hash):
            raise ValueError("stored signed_event_hash is invalid")
        retrieved_sha256 = hashlib.sha256(data).hexdigest()
        hash_match = stored_sha256 == retrieved_sha256
        _audit(request_id, "retrieveEvidence", "PASS" if hash_match else "HASH_MISMATCH", passport_id, event_id, blob.generation, hash_match)
        return jsonify(
            {
                "ok": hash_match,
                "request_id": request_id,
                "environment": "Development / Test",
                "passport_id": passport_id,
                "event_id": event_id,
                "schema_version": stored_schema_version,
                "generation": str(blob.generation),
                "stored_sha256": stored_sha256,
                "retrieved_sha256": retrieved_sha256,
                "signed_event_hash": signed_event_hash,
                "hash_match": hash_match,
                "size": int(blob.size),
                "content_type": blob.content_type,
                "retention_expiration": _iso(blob.retention_expiration_time),
            }
        )
    except ValueError as error:
        _audit(request_id, "retrieveEvidence", "REJECTED", passport_id, event_id)
        return jsonify({"ok": False, "request_id": request_id, "error": "invalid_request", "message": str(error)}), 400
    except Exception as error:
        if _is_error(error, 404, "NotFound"):
            _audit(request_id, "retrieveEvidence", "NOT_FOUND", passport_id, event_id)
            return jsonify({"ok": False, "request_id": request_id, "error": "evidence_not_found"}), 404
        logger.exception("retrieveEvidence failed request_id=%s", request_id)
        _audit(request_id, "retrieveEvidence", "ERROR", passport_id, event_id)
        return jsonify({"ok": False, "request_id": request_id, "error": "storage_unavailable"}), 503


@app.post("/v1/evidence/history")
def evidence_history():
    request_id = str(uuid.uuid4())
    passport_id = None
    anchor_event_id = None
    try:
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            raise ValueError("a JSON object is required")
        forbidden = _forbidden_fields(payload)
        if forbidden:
            raise ValueError("client-controlled storage fields are not allowed: " + ", ".join(forbidden))
        passport_id = _normalize_identifier(payload.get("passport_id"), "passport")
        anchor_event_id = _normalize_identifier(payload.get("event_id"), "event")
        prefix = f"evidence/v1/passports/{passport_id}/events/"
        records = []
        for blob in _storage_client().list_blobs(_bucket_name(), prefix=prefix):
            blob.reload()
            event, public_key = _stored_event(blob)
            records.append(
                {
                    "signed_event": event,
                    "issuer_public_key": public_key,
                    "object_path": blob.name,
                    "generation": str(blob.generation),
                    "metageneration": int(blob.metageneration),
                    "created_at": _iso(blob.time_created),
                    "retention_expiration": _iso(blob.retention_expiration_time),
                    "content_type": blob.content_type,
                    "size": int(blob.size),
                }
            )
        records.sort(key=lambda record: (record["signed_event"].get("timestamp", ""), record["signed_event"]["event_id"]))
        if not any(record["signed_event"]["event_id"] == anchor_event_id for record in records):
            return jsonify({"ok": False, "request_id": request_id, "error": "evidence_not_found"}), 404
        _audit(request_id, "history", "PASS", passport_id, hash_match=True)
        return jsonify({"ok": True, "request_id": request_id, "passport_id": passport_id, "events": records})
    except ValueError as error:
        _audit(request_id, "history", "REJECTED", passport_id)
        return jsonify({"ok": False, "request_id": request_id, "error": "invalid_request", "message": str(error)}), 400
    except Exception:
        logger.exception("history failed request_id=%s", request_id)
        _audit(request_id, "history", "ERROR", passport_id)
        return jsonify({"ok": False, "request_id": request_id, "error": "storage_unavailable"}), 503


@app.post("/v1/evidence/download")
def download_evidence():
    request_id = str(uuid.uuid4())
    passport_id = None
    event_id = None
    try:
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            raise ValueError("a JSON object is required")
        forbidden = _forbidden_fields(payload)
        if forbidden:
            raise ValueError("client-controlled storage fields are not allowed: " + ", ".join(forbidden))
        passport_id = _normalize_identifier(payload.get("passport_id"), "passport")
        event_id = _normalize_identifier(payload.get("event_id"), "event")
        blob = _storage_client().bucket(_bucket_name()).blob(_object_path(passport_id, event_id))
        blob.reload()
        event, _public_key = _stored_event(blob)
        data = blob.download_as_bytes()
        digest = hashlib.sha256(data).hexdigest()
        expected = _event_content_sha256(event)
        if digest != expected:
            _audit(request_id, "downloadEvidence", "HASH_MISMATCH", passport_id, event_id, blob.generation, False)
            return jsonify({"ok": False, "request_id": request_id, "error": "evidence_hash_mismatch"}), 409
        _audit(request_id, "downloadEvidence", "PASS", passport_id, event_id, blob.generation, True)
        return jsonify(
            {
                "ok": True,
                "request_id": request_id,
                "passport_id": passport_id,
                "event_id": event_id,
                "generation": str(blob.generation),
                "content_type": blob.content_type,
                "content_sha256": digest,
                "evidence_base64": base64.b64encode(data).decode("ascii"),
            }
        )
    except ValueError as error:
        _audit(request_id, "downloadEvidence", "REJECTED", passport_id, event_id)
        return jsonify({"ok": False, "request_id": request_id, "error": "invalid_request", "message": str(error)}), 400
    except Exception as error:
        if _is_error(error, 404, "NotFound"):
            _audit(request_id, "downloadEvidence", "NOT_FOUND", passport_id, event_id)
            return jsonify({"ok": False, "request_id": request_id, "error": "evidence_not_found"}), 404
        logger.exception("downloadEvidence failed request_id=%s", request_id)
        _audit(request_id, "downloadEvidence", "ERROR", passport_id, event_id)
        return jsonify({"ok": False, "request_id": request_id, "error": "storage_unavailable"}), 503


@app.errorhandler(413)
def request_too_large(_error):
    return jsonify({"ok": False, "error": "request_too_large"}), 413


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
