from enum import Enum


class IntegrityState(str, Enum):
    VALID = "VALID"
    INVALID = "INVALID"
    UNVERIFIED = "UNVERIFIED"


class ProvenanceState(str, Enum):
    VERIFIED_ORIGINAL = "VERIFIED_ORIGINAL"
    VERIFIED_MODIFIED = "VERIFIED_MODIFIED"
    UNVERIFIED = "UNVERIFIED"
    INVALID_EVIDENCE = "INVALID_EVIDENCE"


class IdentityTrust(str, Enum):
    TRUSTED = "TRUSTED"
    DEVELOPMENT = "DEVELOPMENT"
    UNKNOWN = "UNKNOWN"
    REVOKED = "REVOKED"


def decide_evidence(*, registry_match, signature_valid, content_hash_valid,
                    parent_chain_valid, required_profile_evidence_valid,
                    c2pa_present=False, c2pa_integrity_valid=None,
                    identity_trust=IdentityTrust.UNKNOWN, has_parent=False):
    identity = IdentityTrust(identity_trust)
    reasons = []

    if identity is IdentityTrust.REVOKED:
        reasons.append("signer_identity_revoked")
    if c2pa_present and c2pa_integrity_valid is False:
        reasons.append("c2pa_integrity_invalid")
    if registry_match:
        if not signature_valid:
            reasons.append("signature_invalid")
        if not content_hash_valid:
            reasons.append("content_hash_mismatch")
        if not parent_chain_valid:
            reasons.append("parent_chain_invalid")
        if not required_profile_evidence_valid:
            reasons.append("required_profile_evidence_invalid")

    if reasons:
        return {
            "integrity_state": IntegrityState.INVALID.value,
            "provenance_state": ProvenanceState.INVALID_EVIDENCE.value,
            "identity_trust": identity.value,
            "reasons": reasons,
        }

    if registry_match:
        return {
            "integrity_state": IntegrityState.VALID.value,
            "provenance_state": (ProvenanceState.VERIFIED_MODIFIED if has_parent else ProvenanceState.VERIFIED_ORIGINAL).value,
            "identity_trust": identity.value,
            "reasons": ["registry_and_required_evidence_valid"],
        }

    if c2pa_present and c2pa_integrity_valid:
        reasons.append("c2pa_integrity_valid_but_registry_no_match")
    else:
        reasons.append("no_verifiable_registry_source")
    return {
        "integrity_state": IntegrityState.UNVERIFIED.value,
        "provenance_state": ProvenanceState.UNVERIFIED.value,
        "identity_trust": identity.value,
        "reasons": reasons,
    }
