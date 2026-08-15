# Test Report

This file records executed results only. Planned work is never `PASS`.

## Local automated tests — 2026-08-15

| Suite | Command | Result |
|---|---|---|
| Python core/integration | `PYTHONPATH=src /tmp/ai-evidence-explainer-venv/bin/python -m unittest discover -s tests -v` | PASS — 34/34 |
| Web classification/render/security | `npm test` in `apps/web` | PASS — 11/11 |
| Lint | `npm run lint` in `apps/web` | PASS |
| Production build | `npm run build` in `apps/web` | PASS |

Python coverage includes v1 Identifier/digest formats, canonical JSON stability, Event Schema validation, profile status enforcement, deterministic decisions, legacy Event signature/history/parent compatibility, Wallet commitments, Authorization scope/expiry/revocation/single-use rules, hierarchical Text DNA, RSA signatures, C2PA creation/read/verify, real tampered data-hash mismatch, RGB Modification Masks, and the Gemini decision boundary.

The final eligibility-document audit reran the same suites after adding the project timeline, Google Cloud evidence index, IP/license audit, financial/user evidence boundaries, and final qualification gate: Python 34/34, Web 11/11 including Production build, and Lint all remained PASS. No product source or Production deployment changed in that audit.

## Required provenance classification matrix

| Input evidence | Expected | Result |
|---|---|---|
| Valid C2PA + no Registry match | `Unverified` | PASS |
| Valid Registry + invalid C2PA | `Invalid Evidence` | PASS |
| No C2PA + no Registry | `Unverified` | PASS |
| Valid C2PA + valid matching Registry + no parent | `Verified Original` | PASS |
| Valid C2PA + valid matching Registry + parent | `Verified Modified` | PASS |
| Matching Registry + invalid signature | `Invalid Evidence` | PASS |
| Matching Registry + hash mismatch | `Invalid Evidence` | PASS |

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
| Universal Evidence Passport homepage | PASS |
| Signed Version 1 upload → Verified Original | PASS |
| Signed Version 3 upload → Verified Modified | PASS |
| Valid old C2PA + rebuilt Registry miss → Unverified | PASS |
| No C2PA + no Registry → Unverified | PASS |
| Tampered Version 3 → Invalid Evidence + dataHash mismatch | PASS |
| Version History 1/2/3 | PASS |
| 4.8% Modification Mask | PASS |
| Evidence Passport / Change Metrics / Trust / Private Evidence | PASS |
| ProofCart | PASS |
| Missing Evidence ID | PASS |
| Gemini Production integration | PASS |
| Universal adapters / Next Stage architecture | PASS |

The checks above were rerun against Sites Version 5 at the public HTTPS URL after deployment, using actual project-generated files through the page file chooser. Version 5 displays the v1 Evidence Profile, Integrity, Provenance, Identity Trust, signed AI Involvement, measured Change Scope, and Private Evidence boundary. The old valid C2PA fixture displayed `C2PA integrity: Valid`, `Registry: No Match`, and `Unverified`. The tampered fixture displayed `Invalid Evidence`, `assertion.dataHash.mismatch`, and `c2pa_integrity_invalid`. Gemini returned `gemini-2.5-flash on Vertex AI` while preserving `Verified Modified`.

## Video

Final operation recording: **PASS** — ID `HDG1qYo5hUg`; visibility is
**PRIVATE — pending owner review**.

- Duration: 2:42.733 (YouTube display 2:43), below the three-minute limit.
- Video: H.264, 1920×1080, 30 fps, 16:9, burned-in English captions.
- Actual Production operations: signed Version 3 upload, `Verified Modified`,
  Current Image, Change Overlay, 4.8% Mask, History 1/2/3, tampered upload,
  `Invalid Evidence`, `assertion.dataHash.mismatch`, Gemini explanation,
  ProofCart, universal adapters, and labelled Next Stage.
- Visual QA: complete browser viewport, visible operation cursor, no giant black
  borders, and no cropped website column. Automated crop detection found only
  a four-pixel encoder edge, not the large framing failure in the rejected video.
- YouTube copyright check: completed with no issue reported during processing.
- External visibility check after the owner's privacy change: `LOGIN_REQUIRED`
  with the message `This is a private video`.

The previous 2:24 `Fwu7yGUTVwo` video remains rejected and must not be submitted.
