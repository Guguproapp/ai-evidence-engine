import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

from .canonical import canonical_json, sha256_bytes
from .crypto import ensure_issuer_keys, public_key_pem, sign_bytes, verify_bytes
from .text_dna import fingerprint_text


PUBLIC_EVENT_FIELDS = {
    "event_id", "passport_id", "parent_event", "parent_hash", "content_id", "exact_hash",
    "fingerprint", "timestamp", "issuer", "provider", "model", "model_version", "action_type",
    "involvement_level", "modification_scope", "operator_type", "human_approval", "blackbox_available",
    "asset_type", "media_type", "device_id", "software", "software_version", "model_provider",
    "model_id", "source_assets", "authorization_id", "wallet_commitment", "c2pa_manifest_id",
    "trust_status", "change_metrics", "public_disclosure_level",
}


class Registry:
    def __init__(self, data_dir, key_dir, issuer_id="gugupro-local-dev"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.events_path = self.data_dir / "events.jsonl"
        self.issuers_path = self.data_dir / "issuers.json"
        self.private_key, self.public_key = ensure_issuer_keys(key_dir, issuer_id)
        self.issuer_id = issuer_id
        self._save_issuer()

    def _save_issuer(self):
        issuers = self._read_json(self.issuers_path, {})
        issuers[self.issuer_id] = {
            "issuer_id": self.issuer_id,
            "algorithm": "RSA-2048/SHA-256",
            "public_key_pem": public_key_pem(self.public_key),
            "status": "development-self-issued",
        }
        self.issuers_path.write_text(json.dumps(issuers, ensure_ascii=False, indent=2), encoding="utf-8")

    @staticmethod
    def _read_json(path, default):
        if not path.exists():
            return default
        return json.loads(path.read_text(encoding="utf-8"))

    def all_events(self):
        if not self.events_path.exists():
            return []
        return [json.loads(line) for line in self.events_path.read_text(encoding="utf-8").splitlines() if line.strip()]

    def register_text(self, content, **metadata):
        return self._register_content(
            content.encode("utf-8"),
            fingerprint_text(content),
            ".txt",
            content.encode("utf-8"),
            **metadata,
        )

    def register_file(self, path, fingerprint=None, **metadata):
        path = Path(path)
        content = path.read_bytes()
        return self._register_content(
            content,
            fingerprint or {"kind": "sha256", "value": sha256_bytes(content)},
            path.suffix.lower() or ".bin",
            content,
            **metadata,
        )

    def _register_content(self, content_bytes, fingerprint, wallet_suffix, wallet_content, **metadata):
        events = self.all_events()
        parent_event = metadata.get("parent_event")
        parent = next((event for event in events if event["event_id"] == parent_event), None) if parent_event else None
        if parent_event and parent is None:
            raise ValueError("parent_event does not exist")

        event_id = metadata.get("event_id") or str(uuid.uuid4())
        exact_hash = sha256_bytes(content_bytes)
        event = {
            "event_id": event_id,
            "passport_id": metadata.get("passport_id") or str(uuid.uuid4()),
            "parent_event": parent_event,
            "parent_hash": parent.get("event_hash") if parent else None,
            "content_id": metadata.get("content_id") or str(uuid.uuid4()),
            "exact_hash": exact_hash,
            "fingerprint": fingerprint,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "issuer": self.issuer_id,
            "provider": metadata.get("provider", "unknown"),
            "model": metadata.get("model"),
            "model_version": metadata.get("model_version"),
            "action_type": metadata.get("action_type", "unknown"),
            "involvement_level": metadata.get("involvement_level", "L0"),
            "modification_scope": metadata.get("modification_scope", "unknown"),
            "operator_type": metadata.get("operator_type", "AI"),
            "human_approval": bool(metadata.get("human_approval", False)),
            "blackbox_available": bool(metadata.get("blackbox_available", False)),
            "asset_type": metadata.get("asset_type", "digital_content"),
            "media_type": metadata.get("media_type", "text/plain" if wallet_suffix == ".txt" else "application/octet-stream"),
            "device_id": metadata.get("device_id"),
            "software": metadata.get("software"),
            "software_version": metadata.get("software_version"),
            "model_provider": metadata.get("model_provider", metadata.get("provider", "unknown")),
            "model_id": metadata.get("model_id", metadata.get("model")),
            "source_assets": metadata.get("source_assets", []),
            "authorization_id": metadata.get("authorization_id"),
            "wallet_commitment": metadata.get("wallet_commitment") or sha256_bytes(("wallet:" + event_id + ":" + exact_hash).encode("utf-8")),
            "c2pa_manifest_id": metadata.get("c2pa_manifest_id"),
            "trust_status": metadata.get("trust_status", "development"),
            "change_metrics": metadata.get("change_metrics", metadata.get("modification_scope") if isinstance(metadata.get("modification_scope"), dict) else {}),
            "public_disclosure_level": metadata.get("public_disclosure_level", "minimum"),
        }
        payload = canonical_json(event)
        event["event_hash"] = sha256_bytes(payload)
        event["signature_algorithm"] = "RSA-2048/SHA-256"
        event["signature"] = sign_bytes(self.private_key, payload)
        with self.events_path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
        wallet = self.data_dir / "wallet"
        wallet.mkdir(parents=True, exist_ok=True)
        wallet_file = wallet / (event["event_id"] + wallet_suffix)
        wallet_file.write_bytes(wallet_content)
        wallet_file.chmod(0o600)
        return event

    def get_passport(self, passport_id):
        matches = [event for event in self.all_events() if event["passport_id"] == passport_id]
        return matches[-1] if matches else None

    def history(self, content_id):
        return [event for event in self.all_events() if event["content_id"] == content_id]

    def issuer(self, issuer_id):
        return self._read_json(self.issuers_path, {}).get(issuer_id)

    def verify_event(self, event):
        unsigned = {key: event[key] for key in PUBLIC_EVENT_FIELDS if key in event}
        payload = canonical_json(unsigned)
        hash_valid = sha256_bytes(payload) == event.get("event_hash")
        signature_valid = verify_bytes(self.public_key, payload, event.get("signature", ""))
        parent_valid = True
        if event.get("parent_event"):
            parent = next((candidate for candidate in self.all_events() if candidate["event_id"] == event["parent_event"]), None)
            parent_valid = parent is not None and parent.get("event_hash") == event.get("parent_hash")
        revocations = self._read_json(self.data_dir / "revocations.json", {})
        revocation = revocations.get(event.get("passport_id"))
        verified = all([hash_valid, signature_valid, parent_valid]) and revocation is None
        return {
            "ai_involvement": event.get("involvement_level") not in {None, "L0"},
            "issuer": event.get("issuer"),
            "creation_time": event.get("timestamp"),
            "modification_status": event.get("action_type"),
            "parent": event.get("parent_event"),
            "signature_status": "valid" if signature_valid else "invalid",
            "blackbox_available": bool(event.get("blackbox_available")),
            "confidence_level": "cryptographic" if verified else "unverified",
            "revocation_status": "revoked" if revocation else "active",
            "hash_valid": hash_valid,
            "signature_valid": signature_valid,
            "parent_valid": parent_valid,
            "verified": verified,
        }

    def revoke(self, passport_id, reason):
        path = self.data_dir / "revocations.json"
        revocations = self._read_json(path, {})
        revocations[passport_id] = {"reason": reason, "timestamp": datetime.now(timezone.utc).isoformat()}
        path.write_text(json.dumps(revocations, ensure_ascii=False, indent=2), encoding="utf-8")
        return revocations[passport_id]
