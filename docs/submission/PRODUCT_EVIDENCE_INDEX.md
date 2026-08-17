# Product Evidence Index

Status: **READY**

| Evidence | Path | Date | Environment | What it proves |
|---|---|---|---|---|
| Production home | `docs/evidence/2026-08-15-production-v3-home.png` | 2026-08-15 | Public Production | Anonymous HTTPS verifier is available |
| Verified Modified | `docs/evidence/2026-08-15-production-v3-modified.png` | 2026-08-15 | Public Production | Recorded child version classification |
| Modification Mask | `docs/evidence/2026-08-15-production-v3-mask.png` | 2026-08-15 | Public Production | Known-version measured change and region mask |
| C2PA | `docs/evidence/2026-08-15-production-v3-c2pa.png` | 2026-08-15 | Public Production | Embedded manifest and development-identity boundary |
| Version History | `docs/evidence/2026-08-15-production-v3-history.png` | 2026-08-15 | Public Production | Parent/child recorded history |
| Invalid Evidence | `docs/evidence/2026-08-15-production-v3-invalid-signature.png` | 2026-08-15 | Public Production | Tamper/invalid path |
| Unknown source | `docs/evidence/2026-08-15-production-v3-unknown.png` | 2026-08-15 | Public Production | Unknown content is not guessed |
| Gemini explanation | `docs/evidence/2026-08-15-production-v3-gemini.png` | 2026-08-15 | Public Production | Gemini explains deterministic facts |
| Mac end-to-end sequence | `reports/app-user-test-023/desktop/` | 2026-08-17 | Physical Mac / public site | Actual browser workflow, seal, retrieve, and continuity |
| iPhone unknown/AI/corrupt tests | `reports/app-user-test-029/iphone/` | 2026-08-17 | Physical iPhone 15 / Safari | Real-device unknown-source safety and error handling |
| iPhone First-Seen V1 → V2 | `reports/legacy-bridge-production-gate-031/iphone/` | 2026-08-17 | Physical iPhone 15 / Production | First-Seen, same Passport, child Event, persistence, measured change |
| Restart recovery | `reports/legacy-bridge-production-gate-031/RESTART_RECOVERY_TEST.md` | 2026-08-17 | Development/Test | History reconstructs after loss of in-memory state |
| Cloud Run dashboard | `docs/evidence/2026-08-15-cloud-run-observability.jpg` | 2026-08-15 | Google Cloud | Deployed service operations |
| Gemini dashboard | `docs/evidence/2026-08-15-gemini-observability.jpg` | 2026-08-15 | Vertex AI | Model invocation/usage evidence |
| Retention/delete/overwrite/retrieval | `docs/submission/BLACKBOX_TEST_EVIDENCE.md` | 2026-08-17 | Development/Test Google Cloud | Sanitized HTTP 403 delete rejection, HTTP 412 overwrite rejection, object existence, retrieval, and hash evidence |
| Final First-Seen run | `docs/submission/BLACKBOX_TEST_EVIDENCE.md` | 2026-08-17 | Production + Development/Test | Sanitized First-Seen, V1 → V2, generation, retention, SHA-256 Match, and continuity evidence |
| Final video | `docs/evidence/AI-Evidence-Engine-XPRIZE-Final-2026-08-18.mp4` | 2026-08-18 | Submission artifact | Working project under 3 minutes |

No PASS is inferred merely from a filename; the referenced reports include actual inputs, outputs, identifiers, hashes, or screenshots.
