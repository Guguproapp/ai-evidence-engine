export const INTEGRITY_STATES = Object.freeze({ VALID: "VALID", INVALID: "INVALID", UNVERIFIED: "UNVERIFIED" });
export const PROVENANCE_STATES = Object.freeze({
  VERIFIED_ORIGINAL: "VERIFIED_ORIGINAL",
  VERIFIED_MODIFIED: "VERIFIED_MODIFIED",
  UNVERIFIED: "UNVERIFIED",
  INVALID_EVIDENCE: "INVALID_EVIDENCE",
});
export const PROVENANCE_LABELS = Object.freeze({
  VERIFIED_ORIGINAL: "Verified Original",
  VERIFIED_MODIFIED: "Verified Modified",
  UNVERIFIED: "Unverified",
  INVALID_EVIDENCE: "Invalid Evidence",
});
export const IDENTITY_TRUST = Object.freeze({ TRUSTED: "TRUSTED", DEVELOPMENT: "DEVELOPMENT", UNKNOWN: "UNKNOWN", REVOKED: "REVOKED" });

/**
 * Classify provenance without turning any single signal into a truth claim.
 * C2PA integrity, Registry matching, Registry signature/chain validity, and
 * parentage are evaluated separately before a provenance state is returned.
 */
export function classifyEvidence({
  hasC2pa, c2paValid, registryMatched, registryValid,
  signatureValid = registryValid, contentHashValid = registryValid,
  parentChainValid = registryValid, requiredProfileEvidenceValid = registryValid,
  hasParent, identityTrust = "UNKNOWN",
}) {
  const normalizedIdentity = String(identityTrust).toUpperCase();
  const reasons = [];
  if (normalizedIdentity === IDENTITY_TRUST.REVOKED) reasons.push("signer_identity_revoked");
  if (hasC2pa && !c2paValid) reasons.push("c2pa_integrity_invalid");
  if (registryMatched) {
    if (!signatureValid) reasons.push("signature_invalid");
    if (!contentHashValid) reasons.push("content_hash_mismatch");
    if (!parentChainValid) reasons.push("parent_chain_invalid");
    if (!requiredProfileEvidenceValid) reasons.push("required_profile_evidence_invalid");
  }

  let integrityState = INTEGRITY_STATES.UNVERIFIED;
  let provenanceStateCode = PROVENANCE_STATES.UNVERIFIED;
  if (reasons.length) {
    integrityState = INTEGRITY_STATES.INVALID;
    provenanceStateCode = PROVENANCE_STATES.INVALID_EVIDENCE;
  } else if (registryMatched) {
    integrityState = INTEGRITY_STATES.VALID;
    provenanceStateCode = hasParent ? PROVENANCE_STATES.VERIFIED_MODIFIED : PROVENANCE_STATES.VERIFIED_ORIGINAL;
    reasons.push("registry_and_required_evidence_valid");
  } else {
    reasons.push(hasC2pa && c2paValid ? "c2pa_integrity_valid_but_registry_no_match" : "no_verifiable_registry_source");
  }

  return {
    integrityState,
    provenanceStateCode,
    provenanceState: PROVENANCE_LABELS[provenanceStateCode],
    c2paIntegrity: !hasC2pa ? "Not Present" : c2paValid ? "Valid" : "Invalid",
    registryStatus: registryMatched ? (registryValid ? "Matched" : "Invalid") : "No Match",
    identityTrust: normalizedIdentity,
    reasons,
  };
}
