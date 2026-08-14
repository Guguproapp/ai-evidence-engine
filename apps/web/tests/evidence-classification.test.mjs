import assert from "node:assert/strict";
import test from "node:test";

import { classifyEvidence } from "../app/evidence-classification.mjs";

test("valid C2PA without a Registry match is Unverified", () => {
  const result = classifyEvidence({ hasC2pa: true, c2paValid: true, registryMatched: false, registryValid: false, hasParent: false });
  assert.equal(result.provenanceState, "Unverified");
  assert.equal(result.integrityState, "UNVERIFIED");
  assert.equal(result.c2paIntegrity, "Valid");
  assert.equal(result.registryStatus, "No Match");
});

test("valid Registry with invalid C2PA is Invalid Evidence", () => {
  const result = classifyEvidence({ hasC2pa: true, c2paValid: false, registryMatched: true, registryValid: true, hasParent: false });
  assert.equal(result.provenanceState, "Invalid Evidence");
  assert.equal(result.integrityState, "INVALID");
});

test("no C2PA and no Registry is Unverified", () => {
  const result = classifyEvidence({ hasC2pa: false, c2paValid: false, registryMatched: false, registryValid: false, hasParent: false });
  assert.equal(result.provenanceState, "Unverified");
});

test("matching valid original evidence is Verified Original", () => {
  const result = classifyEvidence({ hasC2pa: true, c2paValid: true, registryMatched: true, registryValid: true, hasParent: false });
  assert.equal(result.provenanceState, "Verified Original");
  assert.equal(result.provenanceStateCode, "VERIFIED_ORIGINAL");
  assert.equal(result.integrityState, "VALID");
});

test("matching valid child evidence is Verified Modified", () => {
  const result = classifyEvidence({ hasC2pa: true, c2paValid: true, registryMatched: true, registryValid: true, hasParent: true });
  assert.equal(result.provenanceState, "Verified Modified");
});

test("matching Registry with invalid signature is Invalid Evidence", () => {
  const result = classifyEvidence({ hasC2pa: true, c2paValid: true, registryMatched: true, registryValid: false, signatureValid: false, contentHashValid: true, parentChainValid: true, requiredProfileEvidenceValid: true, hasParent: false });
  assert.equal(result.provenanceStateCode, "INVALID_EVIDENCE");
  assert.ok(result.reasons.includes("signature_invalid"));
});

test("matching Registry with hash mismatch is Invalid Evidence", () => {
  const result = classifyEvidence({ hasC2pa: true, c2paValid: true, registryMatched: true, registryValid: false, signatureValid: true, contentHashValid: false, parentChainValid: true, requiredProfileEvidenceValid: true, hasParent: false });
  assert.equal(result.provenanceStateCode, "INVALID_EVIDENCE");
  assert.ok(result.reasons.includes("content_hash_mismatch"));
});
