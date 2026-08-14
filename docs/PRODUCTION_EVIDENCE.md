# Production Evidence Index

Only artifacts actually captured for the rebuilt release may be marked `PASS`. Historical Version 3 screenshots and the old YouTube video use superseded labels/IDs and are not final-submission evidence.

| Evidence | Status | Current evidence |
|---|---|---|
| Google Cloud project | PASS | Dedicated project `ai-evidence-engine-gugupro` |
| Cloud Run deployment | PASS | Revision `ai-evidence-explainer-00003-m75` in `asia-east1`, 100% traffic |
| Cloud Run health | PASS | Public HTTPS HTTP 200 |
| Gemini Production call | PASS | Vertex AI `gemini-2.5-flash` returned HTTP 200 and preserved `Verified Modified` |
| Gemini Cloud Logging | PASS | Request ID `3da55316-9616-46af-9ab2-39e34a1bdb49`; upstream Vertex AI HTTP 200; no prompt/secret logged |
| Rebuilt public verifier deployment | NOT RUN | Awaiting Sites publish |
| Rebuilt public browser regression | NOT RUN | Must rerun all four states, History, Mask, ProofCart, Gemini, architecture |
| Final public demo video | NOT RUN | Old `Fwu7yGUTVwo` video rejected; replacement required |
| Real external user evidence | FAIL | 0 verified external users |

## Rebuilt Version 3 identifiers

- Passport ID: `18b270f8-9937-4d07-b059-010e15fa9264`
- Version 1 Event: `7fcbfc61-fcdd-482e-98a8-047769747f32`
- Version 2 Event: `51b90c7b-8bcb-4df9-8e76-8f25f5c6539c`
- Version 3 Event: `1c3d4a0f-9e2a-4a18-a83f-0c982db4ef33`
- Version 3 Parent Event: `51b90c7b-8bcb-4df9-8e76-8f25f5c6539c`
- Version 3 SHA-256: `7e4bb29731e36aebad5907ce749bad3f0f542df155e39af713d30ed606bba37c`
- Version 3 C2PA Manifest: `urn:c2pa:cd1f092b-94fe-4623-9e51-a8eacd50a762`
- Version 3 Event Hash: `262c794b7fa3077a52c0166617e6f2cbfedf47e335102fa02fdf8c39a8333ce6`
- Version 3 Spatial Change: `0.047743` (`4.8%` display)

## Sanitization boundary

Screenshots and logs must not contain API keys, OAuth codes, access tokens, private keys, customer contact details, billing details, or unrelated project data. Public evidence may include service URL, revision, model, request ID, deterministic state, Evidence ID, latency, and non-sensitive validation results.

Historical evidence remains under `docs/evidence/` for audit history. It must not be described as the current rebuilt release unless a fresh Production check reproduces the result with the identifiers above.
