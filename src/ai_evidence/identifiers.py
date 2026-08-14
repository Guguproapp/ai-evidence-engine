import re
import uuid


SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
URN_RE = re.compile(r"^urn:aee:(passport|event|auth|device):v1:([A-Za-z0-9._:-]+)$")


def _uuid_text(value):
    return str(uuid.UUID(str(value)))


def passport_identifier(value):
    return f"urn:aee:passport:v1:{_uuid_text(value)}"


def event_identifier(value):
    return f"urn:aee:event:v1:{_uuid_text(value)}"


def authorization_identifier(value):
    return f"urn:aee:auth:v1:{_uuid_text(value)}"


def device_identifier(value):
    opaque = str(value).strip()
    try:
        opaque = _uuid_text(opaque)
    except ValueError:
        fingerprint = opaque.lower().replace(":", "")
        if not re.fullmatch(r"[0-9a-f]{32,128}", fingerprint):
            raise ValueError("device identifier must be a UUID or public-key fingerprint")
    return f"urn:aee:device:v1:{opaque}"


def issuer_identifier(value):
    opaque = str(value).strip()
    if not re.fullmatch(r"[A-Za-z0-9._-]+", opaque):
        raise ValueError("issuer identifier must be a non-empty opaque token")
    return f"urn:aee:issuer:v1:{opaque}"


def digest_identifier(hex_digest):
    value = f"sha256:{str(hex_digest).lower()}"
    if not SHA256_RE.fullmatch(value):
        raise ValueError("digest must contain exactly 64 hexadecimal characters")
    return value


def is_canonical_digest(value):
    return bool(SHA256_RE.fullmatch(str(value)))


def is_canonical_aee_identifier(value):
    text = str(value)
    return bool(URN_RE.fullmatch(text) or text.startswith("urn:aee:issuer:v1:"))
