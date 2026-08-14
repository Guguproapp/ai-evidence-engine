# Test Report

This file records executed results only. Planned work is never `PASS`.

## Local automated tests — 2026-08-15

| Suite | Command | Result |
|---|---|---|
| Python core/integration | `PYTHONPATH=src /tmp/ai-evidence-explainer-venv/bin/python -m unittest discover -s tests -v` | PASS — 20/20 |
| Web classification/render/security | `npm test` in `apps/web` | PASS — 9/9 |
| Lint | `npm run lint` in `apps/web` | PASS |
| Production build | `npm run build` in `apps/web` | PASS |

Python coverage includes hierarchical Text DNA, common-phrase guard, RSA signatures, parent chains, backward-compatible expanded Registry schema, C2PA creation/read/verify, real tampered data-hash mismatch, RGB Modification Masks, and the Gemini decision boundary.

## Required provenance classification matrix

| Input evidence | Expected | Result |
|---|---|---|
| Valid C2PA + no Registry match | `Unverified` | PASS |
| Valid Registry + invalid C2PA | `Invalid Evidence` | PASS |
| No C2PA + no Registry | `Unverified` | PASS |
| Valid C2PA + valid matching Registry + no parent | `Verified Original` | PASS |
| Valid C2PA + valid matching Registry + parent | `Verified Modified` | PASS |

The state machine keeps C2PA integrity, Registry match, identity trust, and provenance outcome as separate signals. A single evidence source cannot imply `Verified Original`.

## Rebuilt image Evidence

Command: `PYTHONPATH=src /tmp/ai-evidence-explainer-venv/bin/python scripts/build_image_demo.py`

Result: PASS. Official `c2patool 0.27.12` produced three embedded manifests and a three-version parent ingredient chain. All three rebuilt Registry signatures verify. Version 3 measured 16,500 changed pixels of 345,600, ratio `0.047743`, bounding box `{x:250,y:245,width:220,height:75}`.

The prepared tampered Version 3 was read by the official tool and returned `assertion.dataHash.mismatch`; the previous signed Version 3 remains C2PA-valid but has no match in the rebuilt Registry and is the real browser fixture for `Valid C2PA + no Registry → Unverified`.

## Cloud Run / Gemini — rebuilt four-state contract

| Check | Result | Evidence |
|---|---|---|
| Cloud Run deploy | PASS | Revision `ai-evidence-explainer-00003-m75`, 100% traffic |
| Health | PASS | Production HTTPS returned HTTP 200 |
| Gemini Production call | PASS | Vertex AI `gemini-2.5-flash`, HTTP 200 |
| State preservation | PASS | Request and response both `Verified Modified` |
| Allowlisted facts | PASS | Service rejects unsupported states and removes non-allowlisted facts in tests |
| Failure fallback | PASS locally | Web retains deterministic verification and presents an explicit explanation failure |

Production request ID: `3da55316-9616-46af-9ab2-39e34a1bdb49`. Cloud Logging records the corresponding Vertex AI upstream HTTP 200 and Version 3 Evidence ID `1c3d4a0f-9e2a-4a18-a83f-0c982db4ef33`.

## Public Production regression for rebuilt release

| Flow | Status |
|---|---|
| Universal Evidence Passport homepage | NOT RUN |
| Signed Version 1 upload → Verified Original | NOT RUN |
| Signed Version 3 upload → Verified Modified | NOT RUN |
| Valid old C2PA + rebuilt Registry miss → Unverified | NOT RUN |
| Tampered Version 3 → Invalid Evidence + dataHash mismatch | NOT RUN |
| Version History 1/2/3 | NOT RUN |
| 4.8% Modification Mask | NOT RUN |
| Evidence Passport / Change Metrics / Trust / Private Evidence | NOT RUN |
| ProofCart | NOT RUN |
| Gemini Production integration | NOT RUN |
| Universal adapters / Next Stage architecture | NOT RUN |

The prior Production browser results use superseded labels and Evidence IDs. They are retained as historical evidence but are not counted for this rebuilt release.

## Video

Final operation video: `NOT RUN`. The previous 2:24 YouTube video is rejected because its framing and interaction do not satisfy the new acceptance gate. It must not be submitted as the final video.
