from .identifiers import is_canonical_digest
from .profiles import resolve_profile


EVENT_SCHEMA_VERSION = "aee.event.v1"
AI_INVOLVEMENT_LEVELS = {"L0", "L1", "L2", "L3", "L4", "L5", "UNKNOWN"}
INTEGRITY_STATES = {"VALID", "INVALID", "UNVERIFIED"}
PROVENANCE_STATES = {"VERIFIED_ORIGINAL", "VERIFIED_MODIFIED", "UNVERIFIED", "INVALID_EVIDENCE"}
IDENTITY_TRUST_STATES = {"TRUSTED", "DEVELOPMENT", "UNKNOWN", "REVOKED"}
PUBLIC_DISCLOSURE_LEVELS = {"PUBLIC_MINIMUM", "PUBLIC_EXTENDED", "PRIVATE", "SELECTIVE"}

EVENT_V1_REQUIRED_FIELDS = {
    "schema_version", "event_id", "passport_id", "content_id", "content_digest",
    "event_hash", "asset_type", "media_type", "evidence_profile", "version_id",
    "source_assets", "issuer", "timestamp", "involvement_level", "identity_trust",
    "integrity_state", "provenance_state", "change_metrics", "wallet_commitment",
    "public_disclosure_level", "signature_algorithm", "signature",
}


def validate_event_v1(event, require_signature=True):
    if event.get("schema_version") != EVENT_SCHEMA_VERSION:
        raise ValueError("unsupported event schema_version")
    required = EVENT_V1_REQUIRED_FIELDS if require_signature else EVENT_V1_REQUIRED_FIELDS - {"event_hash", "signature_algorithm", "signature"}
    missing = sorted(field for field in required if field not in event)
    if missing:
        raise ValueError("missing Event v1 fields: " + ", ".join(missing))
    resolve_profile(event["evidence_profile"], require_implemented=True)
    if event.get("involvement_level") not in AI_INVOLVEMENT_LEVELS:
        raise ValueError("invalid AI involvement level")
    if event.get("identity_trust") not in IDENTITY_TRUST_STATES:
        raise ValueError("invalid identity trust")
    if event.get("integrity_state") not in INTEGRITY_STATES:
        raise ValueError("invalid integrity state")
    if event.get("provenance_state") not in PROVENANCE_STATES:
        raise ValueError("invalid provenance state")
    if event.get("public_disclosure_level") not in PUBLIC_DISCLOSURE_LEVELS:
        raise ValueError("invalid public disclosure level")
    if not is_canonical_digest(event.get("content_digest")):
        raise ValueError("invalid content digest")
    if not is_canonical_digest(event.get("wallet_commitment")):
        raise ValueError("invalid wallet commitment")
    if require_signature and not is_canonical_digest(event.get("event_hash")):
        raise ValueError("invalid event hash")
    return True
