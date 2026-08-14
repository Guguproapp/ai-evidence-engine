# Production Evidence Index

Only artifacts that were actually captured may be marked `PASS`. Screenshots and logs must not contain API keys, OAuth codes, access tokens, private keys, customer contact details, or unrelated project data.

| Evidence | Status | Required capture |
|---|---|---|
| Public verifier | PASS | Public HTTPS URL and anonymous HTTP/browser result |
| Try Demo | PASS | Screenshot showing verification result, mask, signature, and version count |
| ProofCart | PASS | Screenshot showing the buyer-facing Verify Evidence flow |
| Google Cloud project | PASS | Dedicated billing-enabled project `ai-evidence-engine-gugupro` |
| Cloud Run deployment | PASS | Ready revision `ai-evidence-explainer-00002-z76` in `asia-east1`, serving 100% of traffic |
| Cloud Run production request | PASS | Public health and explanation requests returned HTTP 200; sanitized Cloud Logging record preserved |
| Gemini API production call | PASS | Vertex AI `gemini-2.5-flash` request returned HTTP 200 and preserved deterministic `Modified` status |
| Evidence verification logs | PASS locally | Automated tests and public browser acceptance report |

Artifacts captured later should be placed under `docs/evidence/` with a date and short description. Binary screenshots should not be committed until checked for account emails, project numbers, billing details, and tokens.

Current text evidence: `docs/evidence/2026-08-14-cloud-run-gemini.md`.
