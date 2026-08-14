import assert from "node:assert/strict";
import test from "node:test";

import { classifyEvidence } from "../app/evidence-classification.mjs";

test("valid C2PA without a Registry match is Unverified", () => {
  const result = classifyEvidence({ hasC2pa: true, c2paValid: true, registryMatched: false, registryValid: false, hasParent: false });
  assert.equal(result.provenanceState, "Unverified");
  assert.equal(result.c2paIntegrity, "Valid");
  assert.equal(result.registryStatus, "No Match");
});

test("valid Registry with invalid C2PA is Invalid Evidence", () => {
  const result = classifyEvidence({ hasC2pa: true, c2paValid: false, registryMatched: true, registryValid: true, hasParent: false });
  assert.equal(result.provenanceState, "Invalid Evidence");
});

test("no C2PA and no Registry is Unverified", () => {
  const result = classifyEvidence({ hasC2pa: false, c2paValid: false, registryMatched: false, registryValid: false, hasParent: false });
  assert.equal(result.provenanceState, "Unverified");
});

test("matching valid original evidence is Verified Original", () => {
  const result = classifyEvidence({ hasC2pa: true, c2paValid: true, registryMatched: true, registryValid: true, hasParent: false });
  assert.equal(result.provenanceState, "Verified Original");
});

test("matching valid child evidence is Verified Modified", () => {
  const result = classifyEvidence({ hasC2pa: true, c2paValid: true, registryMatched: true, registryValid: true, hasParent: true });
  assert.equal(result.provenanceState, "Verified Modified");
});
