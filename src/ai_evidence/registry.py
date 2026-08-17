import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

from .canonical import canonical_json, sha256_bytes
from .crypto import ensure_issuer_keys, public_key_pem, sign_bytes, verify_bytes
from .decision import IdentityTrust, decide_evidence
from .identifiers import digest_identifier
from .profiles import IMPLEMENTED, resolve_profile
from .schema import validate_event_v1
from .text_dna import fingerprint_text
from .wallet import wallet_commitment, verify_wallet_commitment


LEGACY_PUBLIC_EVENT_FIELDS = {
    "event_id", "passport_id", "parent_event", "parent_hash", "content_id", "exact_hash",
    "fingerprint", "timestamp", "issuer", "provider", "model", "model_version", "action_type",
    "involvement_level", "modification_scope", "operator_type", "human_approval", "blackbox_available",
    "asset_type", "media_type", "device_id", "software", "software_version", "model_provider",
    "model_id", "source_assets", "authorization_id", "wallet_commitment", "c2pa_manifest_id",
    "trust_status", "change_metrics", "public_disclosure_level",
}

EVENT_V1_FIELDS = LEGACY_PUBLIC_EVENT_FIELDS | {
    "schema_version", "evidence_profile", "version_id", "model_version",
    "identity_trust", "integrity_state", "provenance_state", "content_digest",
}

# Public import retained for integrations that used the original constant.
PUBLIC_EVENT_FIELDS = EVENT_V1_FIELDS


def normalize_legacy_event(event):
    """Return a read-time view without changing the legacy signed payload."""
    normalized = dict(event)
    if not event.get("schema_version"):
        normalized["schema_version"] = "legacy"
        media_type = event.get("media_type", "application/octet-stream")
        normalized.setdefault("evidence_profile", "aee.text.v1" if media_type.startswith("text/") else "aee.image.c2pa.v1" if media_type.startswith("image/") else None)
        normalized.setdefault("version_id", event.get("content_id"))
        trust = str(event.get("trust_status", "unknown")).upper()
        normalized.setdefault("identity_trust", trust if trust in {item.value for item in IdentityTrust} else "UNKNOWN")
        normalized.setdefault("integrity_state", "UNVERIFIED")
        normalized.setdefault("provenance_state", "UNVERIFIED")
    return normalized


def _signed_fields(event):
    return EVENT_V1_FIELDS if event.get("schema_version") == "aee.event.v1" else LEGACY_PUBLIC_EVENT_FIELDS


def _disclosure_level(value):
    aliases = {"MINIMUM": "PUBLIC_MINIMUM", "EXTENDED": "PUBLIC_EXTENDED"}
    normalized = str(value or "PUBLIC_MINIMUM").upper()
    normalized = aliases.get(normalized, normalized)
    if normalized not in {"PUBLIC_MINIMUM", "PUBLIC_EXTENDED", "PRIVATE", "SELECTIVE"}:
        raise ValueError("invalid public_disclosure_level")
    return normalized


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

    def normalized_events(self):
        return [normalize_legacy_event(event) for event in self.all_events()]

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
        media_type = metadata.get("media_type", "text/plain" if wallet_suffix == ".txt" else "application/octet-stream")
        asset_type = metadata.get("asset_type", "text" if media_type.startswith("text/") else "image" if media_type.startswith("image/") else "digital_content")
        profile_id = metadata.get("evidence_profile") or ("aee.text.v1" if media_type.startswith("text/") else "aee.image.c2pa.v1" if media_type.startswith("image/") else None)
        if profile_id:
            resolve_profile(profile_id, require_implemented=True)
        private_bundle = metadata.get("private_evidence") or {
            "event_id": event_id,
            "content_digest": "sha256:" + exact_hash,
            "media_type": media_type,
        }
        commitment = metadata.get("wallet_commitment") or wallet_commitment(private_bundle)
        event = {
            "schema_version": "aee.event.v1",
            "event_id": event_id,
            "passport_id": metadata.get("passport_id") or str(uuid.uuid4()),
            "parent_event": parent_event,
            "parent_hash": parent.get("event_hash") if parent else None,
            "content_id": metadata.get("content_id") or str(uuid.uuid4()),
            "exact_hash": exact_hash,
            "content_digest": digest_identifier(exact_hash),
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
            "asset_type": asset_type,
            "media_type": media_type,
            "evidence_profile": profile_id,
            "version_id": metadata.get("version_id") or str(uuid.uuid4()),
            "device_id": metadata.get("device_id"),
            "software": metadata.get("software"),
            "software_version": metadata.get("software_version"),
            "model_provider": metadata.get("model_provider", metadata.get("provider", "unknown")),
            "model_id": metadata.get("model_id", metadata.get("model")),
            "source_assets": metadata.get("source_assets", []),
            "authorization_id": metadata.get("authorization_id"),
            "wallet_commitment": commitment,
            "c2pa_manifest_id": metadata.get("c2pa_manifest_id"),
            "trust_status": metadata.get("trust_status", "development"),
            "identity_trust": str(metadata.get("identity_trust", "DEVELOPMENT")).upper(),
            "integrity_state": "VALID",
            "provenance_state": metadata.get("provenance_state", "VERIFIED_MODIFIED" if parent else "VERIFIED_ORIGINAL"),
            "change_metrics": metadata.get("change_metrics", metadata.get("modification_scope") if isinstance(metadata.get("modification_scope"), dict) else {}),
            "public_disclosure_level": _disclosure_level(metadata.get("public_disclosure_level")),
        }
        payload = canonical_json(event)
        validate_event_v1(event, require_signature=False)
        event["event_hash"] = digest_identifier(sha256_bytes(payload))
        event["signature_algorithm"] = "RSA-2048/SHA-256"
        event["signature"] = sign_bytes(self.private_key, payload)
        validate_event_v1(event)
        with self.events_path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
        wallet = self.data_dir / "wallet"
        wallet.mkdir(parents=True, exist_ok=True)
        wallet_file = wallet / (event["event_id"] + wallet_suffix)
        wallet_file.write_bytes(wallet_content)
        wallet_file.chmod(0o600)
        bundle_file = wallet / (event["event_id"] + ".bundle.json")
        bundle_file.write_text(json.dumps(private_bundle, ensure_ascii=False, sort_keys=True), encoding="utf-8")
        bundle_file.chmod(0o600)
        return event

    def get_passport(self, passport_id):
        matches = [event for event in self.all_events() if event["passport_id"] == passport_id]
        return normalize_legacy_event(matches[-1]) if matches else None

    def history(self, content_id):
        return [normalize_legacy_event(event) for event in self.all_events() if event["content_id"] == content_id]

    def issuer(self, issuer_id):
        return self._read_json(self.issuers_path, {}).get(issuer_id)

    def verify_event(self, event):
        unsigned = {key: event[key] for key in _signed_fields(event) if key in event}
        payload = canonical_json(unsigned)
        calculated_hash = sha256_bytes(payload)
        expected_hash = event.get("event_hash")
        hash_valid = expected_hash in {calculated_hash, digest_identifier(calculated_hash)}
        signature_valid = verify_bytes(self.public_key, payload, event.get("signature", ""))
        parent_valid = True
        if event.get("parent_event"):
            parent = next((candidate for candidate in self.all_events() if candidate["event_id"] == event["parent_event"]), None)
            parent_valid = parent is not None and parent.get("event_hash") == event.get("parent_hash")
        revocations = self._read_json(self.data_dir / "revocations.json", {})
        revocation = revocations.get(event.get("passport_id"))
        profile_valid = True
        if event.get("schema_version") == "aee.event.v1":
            try:
                profile = resolve_profile(event.get("evidence_profile"), require_implemented=True)
                profile_valid = profile.implementation_status == IMPLEMENTED
                if profile.profile_id == "aee.image.c2pa.v1":
                    profile_valid = profile_valid and bool(event.get("c2pa_manifest_id"))
            except (ValueError, NotImplementedError):
                profile_valid = False
        identity = "REVOKED" if revocation else event.get("identity_trust", "DEVELOPMENT" if event.get("trust_status") == "development" else "UNKNOWN")
        decision = decide_evidence(
            registry_match=True,
            signature_valid=signature_valid,
            content_hash_valid=hash_valid,
            parent_chain_valid=parent_valid,
            required_profile_evidence_valid=profile_valid,
            c2pa_present=bool(event.get("c2pa_manifest_id")),
            c2pa_integrity_valid=None,
            identity_trust=identity,
            has_parent=bool(event.get("parent_event")),
        )
        # A signed first-seen event proves integrity from the registration time
        # forward. It must never be promoted to VERIFIED_ORIGINAL because the
        # asset history before AEE first saw it is explicitly unknown.
        provenance_state = decision["provenance_state"]
        reasons = list(decision["reasons"])
        if event.get("action_type") == "first_seen_registration" and decision["integrity_state"] == "VALID":
            provenance_state = "UNVERIFIED"
            reasons.append("prior_provenance_unknown")
        verified = decision["integrity_state"] == "VALID" and revocation is None
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
            "required_profile_evidence_valid": profile_valid,
            "integrity_state": decision["integrity_state"],
            "provenance_state": provenance_state,
            "identity_trust": decision["identity_trust"],
            "reasons": reasons,
            "verified": verified,
        }

    def verify_private_bundle(self, event_id, private_bundle):
        event = next((candidate for candidate in self.all_events() if candidate.get("event_id") == event_id), None)
        if not event:
            raise ValueError("event does not exist")
        return verify_wallet_commitment(private_bundle, event.get("wallet_commitment", ""))

    def revoke(self, passport_id, reason):
        path = self.data_dir / "revocations.json"
        revocations = self._read_json(path, {})
        revocations[passport_id] = {"reason": reason, "timestamp": datetime.now(timezone.utc).isoformat()}
        path.write_text(json.dumps(revocations, ensure_ascii=False, indent=2), encoding="utf-8")
        return revocations[passport_id]
