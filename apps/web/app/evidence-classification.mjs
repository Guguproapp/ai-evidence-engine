export const PROVENANCE_STATES = Object.freeze({
  VERIFIED_ORIGINAL: "Verified Original",
  VERIFIED_MODIFIED: "Verified Modified",
  UNVERIFIED: "Unverified",
  INVALID: "Invalid Evidence",
});

/**
 * Classify provenance without turning any single signal into a truth claim.
 * C2PA integrity, Registry matching, Registry signature/chain validity, and
 * parentage are evaluated separately before a provenance state is returned.
 */
export function classifyEvidence({
  hasC2pa,
  c2paValid,
  registryMatched,
  registryValid,
  hasParent,
  identityTrust = "Unknown",
}) {
  const c2paIntegrity = !hasC2pa ? "Not Present" : c2paValid ? "Valid" : "Invalid";
  const registryStatus = registryMatched ? (registryValid ? "Matched" : "Invalid") : "No Match";

  let provenanceState = PROVENANCE_STATES.UNVERIFIED;
  if ((hasC2pa && !c2paValid) || (registryMatched && !registryValid) || (registryMatched && !hasC2pa)) {
    provenanceState = PROVENANCE_STATES.INVALID;
  } else if (hasC2pa && c2paValid && registryMatched && registryValid) {
    provenanceState = hasParent ? PROVENANCE_STATES.VERIFIED_MODIFIED : PROVENANCE_STATES.VERIFIED_ORIGINAL;
  }

  return {
    provenanceState,
    c2paIntegrity,
    registryStatus,
    identityTrust,
  };
}
