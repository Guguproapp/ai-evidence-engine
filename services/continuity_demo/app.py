import base64
import copy
import hashlib
import json
import logging
import os
import tempfile
import time
import uuid
from collections import defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path

import requests
from flask import Flask, jsonify, request, send_from_directory
from PIL import Image, UnidentifiedImageError

from ai_evidence.canonical import canonical_json
from ai_evidence.crypto import public_key_pem, verify_bytes
from ai_evidence.image_diff import diff_mask
from ai_evidence.identifiers import digest_identifier
from ai_evidence.registry import EVENT_V1_FIELDS, Registry
from ai_evidence.schema import validate_event_v1


APP_ROOT = Path(__file__).resolve().parent
CONTAINER_DEMO_ASSET = APP_ROOT / "static" / "version-3.png"
DEFAULT_DEMO_ASSET = CONTAINER_DEMO_ASSET if CONTAINER_DEMO_ASSET.is_file() else APP_ROOT.parents[1] / "apps" / "web" / "public" / "demo" / "version-3.png"
DEMO_ASSET = Path(os.getenv("DEMO_EVIDENCE_PATH", str(DEFAULT_DEMO_ASSET)))
DEMO_MANIFEST_ID = "urn:c2pa:cd1f092b-94fe-4623-9e51-a8eacd50a762"
MAX_RUNS_PER_MINUTE = 5
MAX_FILE_BYTES = 10 * 1024 * 1024
ALLOWED_CONTENT_TYPES = {"image/png", "image/jpeg", "image/webp"}
CONTENT_SUFFIX = {"image/png": ".png", "image/jpeg": ".jpg", "image/webp": ".webp"}
BRIDGE_ROOT = Path(os.getenv("LEGACY_BRIDGE_ROOT", Path(tempfile.gettempdir()) / "aee-legacy-bridge"))
ALLOWED_ORIGINS = {
    value.strip()
    for value in os.getenv(
        "LEGACY_BRIDGE_ALLOWED_ORIGINS",
        "https://ai-evidence-engine-gugupro.artistuncle.chatgpt.site,http://localhost:3000,http://127.0.0.1:3000",
    ).split(",")
    if value.strip()
}

app = Flask(__name__, static_folder=str(APP_ROOT / "static"), static_url_path="/static")
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_BYTES + (1024 * 1024)
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

    def seal(self, event, evidence_path, content_type="image/png", issuer_public_key=None):
        data = evidence_path.read_bytes()
        fields = {
            "schema_version": event["schema_version"],
            "passport_id": event["passport_id"],
            "event_id": event["event_id"],
            "content_sha256": event["exact_hash"],
            "content_type": content_type,
            "signed_event": canonical_json(event).decode("utf-8"),
            "issuer_public_key": str(issuer_public_key or ""),
        }
        return self._post(
            "/v1/evidence/seal",
            data=fields,
            files={"evidence_file": (evidence_path.name, data, content_type)},
        )

    def retrieve(self, passport_id, event_id):
        return self._post(
            "/v1/evidence/retrieve",
            json={"passport_id": passport_id, "event_id": event_id},
        )

    def history(self, passport_id, anchor_event_id):
        return self._post(
            "/v1/evidence/history",
            json={"passport_id": passport_id, "event_id": anchor_event_id},
        )

    def download(self, passport_id, event_id):
        return self._post(
            "/v1/evidence/download",
            json={"passport_id": passport_id, "event_id": event_id},
        )


def _stage(name, status, detail):
    return {"name": name, "status": status, "detail": detail}


def _now():
    return datetime.now(timezone.utc).isoformat()


def _validate_image(data, content_type):
    if content_type not in ALLOWED_CONTENT_TYPES:
        raise ValueError("unsupported_image_type")
    if not data:
        raise ValueError("empty_image")
    if len(data) > MAX_FILE_BYTES:
        raise ValueError("image_exceeds_10_mb")
    signatures = {
        "image/png": data.startswith(b"\x89PNG\r\n\x1a\n"),
        "image/jpeg": data.startswith(b"\xff\xd8\xff"),
        "image/webp": len(data) >= 12 and data[:4] == b"RIFF" and data[8:12] == b"WEBP",
    }
    if not signatures[content_type]:
        raise ValueError("image_bytes_do_not_match_content_type")
    try:
        from io import BytesIO
        with Image.open(BytesIO(data)) as image:
            image.verify()
    except (UnidentifiedImageError, OSError, ValueError):
        raise ValueError("invalid_image") from None


def _bridge_path(bridge_id):
    try:
        normalized = str(uuid.UUID(str(bridge_id)))
    except (ValueError, AttributeError, TypeError):
        raise ValueError("invalid_bridge_id") from None
    path = BRIDGE_ROOT / normalized
    if not path.is_dir():
        raise ValueError("bridge_not_found")
    return path


def _write_private_file(path, data):
    path.write_bytes(data)
    path.chmod(0o600)


def _event_summary(event, verification):
    return {
        "schema_version": event["schema_version"],
        "passport_id": event["passport_id"],
        "event_id": event["event_id"],
        "event_hash": event["event_hash"],
        "content_id": event["content_id"],
        "content_sha256": event["exact_hash"],
        "version_id": event["version_id"],
        "parent_event": event.get("parent_event"),
        "action_type": event["action_type"],
        "timestamp": event["timestamp"],
        "integrity_state": verification["integrity_state"],
        "provenance_state": verification["provenance_state"],
        "signature_valid": verification["signature_valid"],
        "hash_valid": verification["hash_valid"],
    }


def _seal_and_retrieve(registry, event, evidence_path, content_type):
    snapshot = copy.deepcopy(event)
    canonical_before = canonical_json(event)
    before = registry.verify_event(event)
    if not (before["signature_valid"] and before["hash_valid"] and before["parent_valid"]):
        raise RuntimeError("Local Signed Event verification failed before seal")
    remote = _remote_client()
    sealed = remote.seal(event, evidence_path, content_type, public_key_pem(registry.public_key))
    retrieved = remote.retrieve(event["passport_id"], event["event_id"])
    after = registry.verify_event(event)
    event_unchanged = event == snapshot and canonical_json(event) == canonical_before
    digest = event["exact_hash"]
    continuity = all([
        sealed.get("passport_id") == event["passport_id"],
        sealed.get("event_id") == event["event_id"],
        sealed.get("content_sha256") == digest,
        sealed.get("signed_event_hash") == event["event_hash"],
        bool(sealed.get("generation")),
        bool(sealed.get("retention_expiration")),
        retrieved.get("passport_id") == event["passport_id"],
        retrieved.get("event_id") == event["event_id"],
        retrieved.get("stored_sha256") == digest,
        retrieved.get("retrieved_sha256") == digest,
        retrieved.get("signed_event_hash") == event["event_hash"],
        retrieved.get("hash_match") is True,
        after["signature_valid"],
        after["hash_valid"],
        after["parent_valid"],
        event_unchanged,
    ])
    if not continuity:
        raise RuntimeError("Evidence continuity verification failed")
    return before, after, sealed, retrieved, event_unchanged


def _history(registry, content_id):
    return [
        _event_summary(event, registry.verify_event(event))
        for event in registry.history(content_id)
    ]


def _verify_persistent_history(records, passport_id, anchor_event_id):
    if not records:
        raise RuntimeError("Persistent Evidence history is empty")
    events_by_id = {}
    verified_records = []
    for record in records:
        event = record.get("signed_event")
        public_key = str(record.get("issuer_public_key") or "")
        if not isinstance(event, dict):
            raise RuntimeError("Persistent Evidence contains an invalid Signed Event")
        validate_event_v1(event)
        if event.get("passport_id") != passport_id:
            raise RuntimeError("Persistent Evidence passport continuity failed")
        unsigned = {key: event[key] for key in EVENT_V1_FIELDS if key in event}
        payload = canonical_json(unsigned)
        calculated_hash = digest_identifier(hashlib.sha256(payload).hexdigest())
        hash_valid = calculated_hash == event.get("event_hash")
        with tempfile.NamedTemporaryFile(mode="w", suffix=".pem", encoding="utf-8") as key_file:
            key_file.write(public_key)
            key_file.flush()
            signature_valid = verify_bytes(Path(key_file.name), payload, event.get("signature", ""))
        parent_valid = True
        if event.get("parent_event"):
            parent = events_by_id.get(event["parent_event"])
            parent_valid = parent is not None and parent.get("event_hash") == event.get("parent_hash")
        if not (hash_valid and signature_valid and parent_valid):
            raise RuntimeError("Persistent Signed Event verification failed")
        events_by_id[event["event_id"]] = event
        verification = {
            "integrity_state": "VALID",
            "provenance_state": "UNVERIFIED" if event.get("action_type") == "first_seen_registration" else "VERIFIED_MODIFIED",
            "signature_valid": True,
            "hash_valid": True,
        }
        verified_records.append({**record, "summary": _event_summary(event, verification)})
    if anchor_event_id not in events_by_id:
        raise RuntimeError("Persistent Evidence anchor Event was not found")
    return verified_records


def _persistent_history(remote, passport_id, anchor_event_id):
    response = remote.history(passport_id, anchor_event_id)
    return _verify_persistent_history(response.get("events", []), passport_id, anchor_event_id)


def _recover_bridge(passport_id, anchor_event_id):
    try:
        passport_id = str(uuid.UUID(str(passport_id)))
        anchor_event_id = str(uuid.UUID(str(anchor_event_id)))
    except (ValueError, AttributeError, TypeError):
        raise ValueError("invalid_persistent_history_locator") from None
    remote = _remote_client()
    records = _persistent_history(remote, passport_id, anchor_event_id)
    first = records[0]
    first_event = first["signed_event"]
    downloaded = remote.download(passport_id, first_event["event_id"])
    try:
        data = base64.b64decode(downloaded.get("evidence_base64") or "", validate=True)
    except ValueError:
        raise RuntimeError("Persistent Evidence download is invalid") from None
    if hashlib.sha256(data).hexdigest() != first_event["exact_hash"]:
        raise RuntimeError("Persistent Evidence recovery SHA-256 mismatch")
    content_type = str(downloaded.get("content_type") or first.get("content_type") or "")
    _validate_image(data, content_type)
    bridge_id = str(uuid.uuid4())
    bridge_dir = BRIDGE_ROOT / bridge_id
    bridge_dir.mkdir(parents=True, mode=0o700)
    original_path = bridge_dir / ("version-1" + CONTENT_SUFFIX[content_type])
    _write_private_file(original_path, data)
    registry = Registry(bridge_dir / "registry", bridge_dir / "keys", issuer_id=f"gugupro-legacy-bridge-recovered-{bridge_id}")
    registry.events_path.write_text(
        "".join(json.dumps(record["signed_event"], ensure_ascii=False, sort_keys=True) + "\n" for record in records),
        encoding="utf-8",
    )
    state = {
        "bridge_id": bridge_id,
        "content_type": content_type,
        "original_path": original_path.name,
        "passport_id": passport_id,
        "content_id": first_event["content_id"],
        "first_event_id": first_event["event_id"],
        "latest_event_id": records[-1]["signed_event"]["event_id"],
        "first_seen_time": first_event["timestamp"],
        "recovered_from_persistent_evidence": True,
    }
    state_path = bridge_dir / "state.json"
    state_path.write_text(json.dumps(state, sort_keys=True), encoding="utf-8")
    state_path.chmod(0o600)
    return bridge_id, bridge_dir, state, registry, records


def start_first_seen(data, content_type):
    _validate_image(data, content_type)
    server_received_time = _now()
    bridge_id = str(uuid.uuid4())
    bridge_dir = BRIDGE_ROOT / bridge_id
    bridge_dir.mkdir(parents=True, mode=0o700)
    evidence_path = bridge_dir / ("version-1" + CONTENT_SUFFIX[content_type])
    _write_private_file(evidence_path, data)
    digest = hashlib.sha256(data).hexdigest()
    registry = Registry(bridge_dir / "registry", bridge_dir / "keys", issuer_id="gugupro-legacy-bridge-dev")
    event = registry.register_file(
        evidence_path,
        fingerprint={"kind": "sha256", "value": digest},
        asset_type="image",
        media_type=content_type,
        evidence_profile="aee.image.firstseen.v1",
        provider="gugupro",
        model="aee-legacy-content-bridge",
        model_version="1",
        action_type="first_seen_registration",
        involvement_level="UNKNOWN",
        operator_type="human_upload",
        human_approval=True,
        blackbox_available=True,
        provenance_state="UNVERIFIED",
        source_assets=[{
            "relationship": "first_seen",
            "prior_provenance": "unknown",
            "aee_first_seen_time": server_received_time,
            "server_received_time": server_received_time,
            "soft_binding_type": "sha256",
            "soft_binding_value": "sha256:" + digest,
            "manifest_repository_reference": None,
            "recovery_status": "not_attempted",
        }],
    )
    before, after, sealed, retrieved, unchanged = _seal_and_retrieve(registry, event, evidence_path, content_type)
    state = {
        "bridge_id": bridge_id,
        "content_type": content_type,
        "original_path": evidence_path.name,
        "passport_id": event["passport_id"],
        "content_id": event["content_id"],
        "first_event_id": event["event_id"],
        "latest_event_id": event["event_id"],
        "first_seen_time": server_received_time,
    }
    state_path = bridge_dir / "state.json"
    state_path.write_text(json.dumps(state, sort_keys=True), encoding="utf-8")
    state_path.chmod(0o600)
    persistent_records = _persistent_history(_remote_client(), event["passport_id"], event["event_id"])
    return {
        "ok": True,
        "environment": "Development / Test",
        "bridge_id": bridge_id,
        "registration_status": "FIRST_SEEN_SEALED",
        "prior_provenance": "unknown",
        "message": "Provenance before this AEE record is unknown. AEE preserves a verifiable evidence history from this point forward.",
        "first_seen_time": server_received_time,
        "server_received_time": server_received_time,
        "seal_time": sealed.get("created_at") or _now(),
        "signed_event": _event_summary(event, after),
        "remote_seal": sealed,
        "retrieval": retrieved,
        "event_unchanged": unchanged,
        "evidence_continuity": "PASS",
        "history": [record["summary"] for record in persistent_records],
        "soft_binding": {
            "type": "sha256",
            "value": "sha256:" + digest,
            "manifest_repository_reference": None,
            "recovery_status": "not_attempted",
            "full_recovery_implemented": False,
        },
    }


def add_recorded_version(bridge_id, data, content_type, passport_id=None, anchor_event_id=None):
    _validate_image(data, content_type)
    recovered = False
    try:
        bridge_dir = _bridge_path(bridge_id)
        state = json.loads((bridge_dir / "state.json").read_text(encoding="utf-8"))
        registry = Registry(bridge_dir / "registry", bridge_dir / "keys", issuer_id="gugupro-legacy-bridge-dev")
    except ValueError as error:
        if str(error) != "bridge_not_found" or not passport_id or not anchor_event_id:
            raise
        bridge_id, bridge_dir, state, registry, _records = _recover_bridge(passport_id, anchor_event_id)
        recovered = True
    parent = registry.all_events()[-1]
    evidence_path = bridge_dir / (f"version-{len(registry.all_events()) + 1}" + CONTENT_SUFFIX[content_type])
    _write_private_file(evidence_path, data)
    original_path = bridge_dir / state["original_path"]
    change_metrics = {}
    try:
        with Image.open(original_path) as original_image, Image.open(evidence_path) as modified_image:
            original_rgb = original_image.convert("RGB")
            modified_rgb = modified_image.convert("RGB")
            if original_rgb.size == modified_rgb.size:
                _, change_metrics = diff_mask(
                    original_rgb.tobytes(), modified_rgb.tobytes(),
                    original_rgb.width, original_rgb.height,
                )
            else:
                change_metrics = {"comparison_status": "different_dimensions", "spatial_change_ratio": None, "changed_region": None}
    except (UnidentifiedImageError, OSError):
        change_metrics = {"comparison_status": "decode_failed", "spatial_change_ratio": None, "changed_region": None}
    event = registry.register_file(
        evidence_path,
        fingerprint={"kind": "sha256", "value": hashlib.sha256(data).hexdigest()},
        passport_id=state["passport_id"],
        content_id=state["content_id"],
        parent_event=parent["event_id"],
        asset_type="image",
        media_type=content_type,
        evidence_profile="aee.image.firstseen.v1",
        provider="gugupro",
        model="aee-legacy-content-bridge",
        model_version="1",
        action_type="recorded_version_update",
        involvement_level="UNKNOWN",
        operator_type="human_upload",
        human_approval=True,
        blackbox_available=True,
        change_metrics=change_metrics,
        modification_scope=change_metrics,
        source_assets=[{
            "relationship": "derived_from_first_seen",
            "source_event_id": parent["event_id"],
            "prior_provenance": "unknown_before_first_seen",
            "soft_binding_type": "sha256",
            "soft_binding_value": "sha256:" + hashlib.sha256(data).hexdigest(),
            "manifest_repository_reference": None,
            "recovery_status": "not_attempted",
        }],
    )
    _, after, sealed, retrieved, unchanged = _seal_and_retrieve(registry, event, evidence_path, content_type)
    state["latest_event_id"] = event["event_id"]
    (bridge_dir / "state.json").write_text(json.dumps(state, sort_keys=True), encoding="utf-8")
    persistent_records = _persistent_history(_remote_client(), event["passport_id"], event["event_id"])
    return {
        "ok": True,
        "environment": "Development / Test",
        "bridge_id": bridge_id,
        "recovered_from_persistent_evidence": recovered,
        "registration_status": "FIRST_SEEN_SEALED",
        "prior_provenance": "unknown",
        "message": "This version is verifiably linked to the AEE first-seen record; history before that first record remains unknown.",
        "signed_event": _event_summary(event, after),
        "remote_seal": sealed,
        "retrieval": retrieved,
        "event_unchanged": unchanged,
        "evidence_continuity": "PASS",
        "change_metrics": change_metrics,
        "history": [record["summary"] for record in persistent_records],
    }


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
        sealed = remote.seal(event, asset_path, "image/png", public_key_pem(registry.public_key))
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
    origin = request.headers.get("Origin")
    if origin in ALLOWED_ORIGINS:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Vary"] = "Origin"
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
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
            "legacy_content_bridge": "Development / Test",
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


def _uploaded_image():
    uploaded = request.files.get("evidence_file")
    if uploaded is None:
        raise ValueError("evidence_file_required")
    content_type = str(uploaded.mimetype or "").lower().strip()
    data = uploaded.read(MAX_FILE_BYTES + 1)
    _validate_image(data, content_type)
    return data, content_type


@app.route("/v1/demo/first-seen", methods=["POST", "OPTIONS"])
def first_seen():
    if request.method == "OPTIONS":
        return ("", 204)
    client = request.headers.get("X-Forwarded-For", request.remote_addr or "unknown").split(",")[0].strip()
    if _rate_limited(client):
        return jsonify({"ok": False, "error": "rate_limit_exceeded"}), 429
    try:
        data, content_type = _uploaded_image()
        return jsonify(start_first_seen(data, content_type)), 201
    except ValueError as error:
        return jsonify({"ok": False, "error": str(error)}), 400
    except Exception:
        request_id = str(uuid.uuid4())
        logger.exception("first_seen failed request_id=%s", request_id)
        return jsonify({"ok": False, "error": "first_seen_failed", "request_id": request_id}), 503


@app.route("/v1/demo/first-seen/version", methods=["POST", "OPTIONS"])
def first_seen_version():
    if request.method == "OPTIONS":
        return ("", 204)
    client = request.headers.get("X-Forwarded-For", request.remote_addr or "unknown").split(",")[0].strip()
    if _rate_limited(client):
        return jsonify({"ok": False, "error": "rate_limit_exceeded"}), 429
    try:
        data, content_type = _uploaded_image()
        return jsonify(
            add_recorded_version(
                request.form.get("bridge_id"),
                data,
                content_type,
                request.form.get("passport_id"),
                request.form.get("event_id"),
            )
        ), 201
    except ValueError as error:
        return jsonify({"ok": False, "error": str(error)}), 400
    except Exception:
        request_id = str(uuid.uuid4())
        logger.exception("first_seen version failed request_id=%s", request_id)
        return jsonify({"ok": False, "error": "recorded_version_failed", "request_id": request_id}), 503


@app.route("/v1/demo/first-seen/recover", methods=["POST", "OPTIONS"])
def first_seen_recover():
    if request.method == "OPTIONS":
        return ("", 204)
    client = request.headers.get("X-Forwarded-For", request.remote_addr or "unknown").split(",")[0].strip()
    if _rate_limited(client):
        return jsonify({"ok": False, "error": "rate_limit_exceeded"}), 429
    try:
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            raise ValueError("json_object_required")
        bridge_id, _bridge_dir, state, _registry, records = _recover_bridge(
            payload.get("passport_id"), payload.get("event_id")
        )
        return jsonify(
            {
                "ok": True,
                "environment": "Development / Test",
                "bridge_id": bridge_id,
                "registration_status": "FIRST_SEEN_SEALED",
                "prior_provenance": "unknown",
                "recovered_from_persistent_evidence": True,
                "passport_id": state["passport_id"],
                "latest_event_id": state["latest_event_id"],
                "history": [record["summary"] for record in records],
            }
        )
    except ValueError as error:
        return jsonify({"ok": False, "error": str(error)}), 400
    except Exception:
        request_id = str(uuid.uuid4())
        logger.exception("first_seen recovery failed request_id=%s", request_id)
        return jsonify({"ok": False, "error": "persistent_history_recovery_failed", "request_id": request_id}), 503


@app.errorhandler(413)
def request_too_large(_error):
    return jsonify({"ok": False, "error": "image_exceeds_10_mb"}), 413


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
