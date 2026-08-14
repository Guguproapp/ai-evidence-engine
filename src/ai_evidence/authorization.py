from datetime import datetime, timezone

from .canonical import canonical_json
from .crypto import sign_bytes, verify_bytes


AUTHORIZATION_FIELDS = (
    "authorization_id", "request_id", "issuer", "requester", "scope",
    "allowed_fields", "denied_fields", "created_at", "expires_at",
    "single_use", "revoked",
)


def authorization_payload(authorization):
    return {field: authorization[field] for field in AUTHORIZATION_FIELDS}


def sign_authorization(authorization, private_key):
    signed = dict(authorization_payload(authorization))
    signed["signature"] = sign_bytes(private_key, canonical_json(signed))
    return signed


def validate_authorization(authorization, public_key, requested_fields=(), used_authorizations=None, now=None):
    reasons = []
    try:
        payload = authorization_payload(authorization)
    except KeyError as error:
        return {"valid": False, "reasons": [f"missing_field:{error.args[0]}"]}
    if not verify_bytes(public_key, canonical_json(payload), authorization.get("signature", "")):
        reasons.append("signature_invalid")
    current = now or datetime.now(timezone.utc)
    expires = datetime.fromisoformat(payload["expires_at"].replace("Z", "+00:00"))
    if current >= expires:
        reasons.append("authorization_expired")
    if payload["revoked"]:
        reasons.append("authorization_revoked")
    used = used_authorizations or set()
    if payload["single_use"] and payload["authorization_id"] in used:
        reasons.append("authorization_already_used")
    allowed = set(payload["allowed_fields"])
    denied = set(payload["denied_fields"])
    for field in requested_fields:
        if field not in allowed or field in denied:
            reasons.append(f"field_not_allowed:{field}")
    return {"valid": not reasons, "reasons": reasons}
