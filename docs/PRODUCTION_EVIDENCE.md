# Production Evidence Index

Only artifacts that were actually captured may be marked `PASS`. Screenshots and logs must not contain API keys, OAuth codes, access tokens, private keys, customer contact details, or unrelated project data.

| Evidence | Status | Required capture |
|---|---|---|
| Public verifier | PASS | Public HTTPS URL and anonymous HTTP/browser result |
| Try Demo | PASS | Version 3 Production screenshots show `Modified`, 4.8% mask, valid signature, and three-version history |
| ProofCart | PASS | Version 3 screenshot shows the buyer-facing Verify Evidence flow and current Evidence ID |
| Google Cloud project | PASS | Dedicated billing-enabled project `ai-evidence-engine-gugupro` |
| Cloud Run deployment | PASS | Ready revision `ai-evidence-explainer-00002-z76` in `asia-east1`, serving 100% of traffic |
| Cloud Run production request | PASS | Public health and explanation requests returned HTTP 200; sanitized Cloud Logging record preserved |
| Gemini API production call | PASS | Vertex AI `gemini-2.5-flash` request returned HTTP 200 and preserved deterministic `Modified` status |
| Public Verifier Gemini integration | PASS | Anonymous production browser invoked Cloud Run and displayed the Gemini explanation while preserving `Modified` |
| Evidence verification logs | PASS | Automated tests plus fresh public-browser `Authentic`, `Modified`, `Unknown`, and `Invalid Signature` results |
| Brand correction | PASS | All newly captured public screenshots and image bytes show `GUGUPRO`; old `GUGUPROO` material is excluded from the official video |
| Version 3 data consistency | PASS | Public image bytes match repository SHA-256 values; Event IDs, parents, C2PA manifest IDs, signatures, and Registry records belong to the rebuilt Version 3 chain |

Artifacts captured later should be placed under `docs/evidence/` with a date and short description. Binary screenshots should not be committed until checked for account emails, project numbers, billing details, and tokens.

Current text evidence: `docs/evidence/2026-08-14-cloud-run-gemini.md`.

Current Version 3 Production captures:

- `docs/evidence/2026-08-15-production-v3-home.png`
- `docs/evidence/2026-08-15-production-v3-modified.png`
- `docs/evidence/2026-08-15-production-v3-mask.png`
- `docs/evidence/2026-08-15-production-v3-history.png`
- `docs/evidence/2026-08-15-production-v3-c2pa.png`
- `docs/evidence/2026-08-15-production-v3-invalid-signature.png`
- `docs/evidence/2026-08-15-production-v3-unknown.png`
- `docs/evidence/2026-08-15-production-v3-proofcart.png`
- `docs/evidence/2026-08-15-production-v3-gemini.png`

Version 3 identifiers:

- Evidence Event: `b56445dd-1530-4c69-93d1-6977120a9f40`
- Parent Event: `ae10e9fb-ad94-403b-a150-c3883aa32ef6`
- SHA-256: `3b00f3ac87e58c5bf5ddb5e2dd021a0236bc3e3c5a02c082c1735867ea81bba9`
- Active C2PA Manifest: `urn:c2pa:da19b9d8-4115-4708-95d1-de5763364a6d`
- Event Hash: `e545c90fcd342fb753e3301509cdc5e048e5645d58e302144a99516b19bdee0d`
