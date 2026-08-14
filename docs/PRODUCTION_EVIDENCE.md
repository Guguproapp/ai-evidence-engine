# Production Evidence Index

Only artifacts that were actually captured may be marked `PASS`. Screenshots and logs must not contain API keys, OAuth codes, access tokens, private keys, customer contact details, or unrelated project data.

| Evidence | Status | Required capture |
|---|---|---|
| Public verifier | PASS | Public HTTPS URL and anonymous HTTP/browser result |
| Try Demo | PASS | Screenshot showing verification result, mask, signature, and version count |
| ProofCart | PASS | Screenshot showing the buyer-facing Verify Evidence flow |
| Google Cloud project | PASS | Dedicated project `ai-evidence-engine-gugupro`; OAuth account active; billing currently disabled |
| Cloud Run deployment | BLOCKED | Billing prerequisite failed before API activation; capture service dashboard with project, region, revision, and URL after enrollment |
| Cloud Run production request | NOT RUN | Sanitized Cloud Logging request/response execution record |
| Gemini API production call | NOT RUN | Sanitized log with model, request ID, success, and latency plus Vertex AI usage view |
| Evidence verification logs | PASS locally | Automated tests and public browser acceptance report |

Artifacts captured later should be placed under `docs/evidence/` with a date and short description. Binary screenshots should not be committed until checked for account emails, project numbers, billing details, and tokens.
