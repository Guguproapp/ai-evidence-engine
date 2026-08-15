# Production Evidence Index

Only artifacts actually captured for the rebuilt release may be marked `PASS`. Historical Version 3 screenshots and the old YouTube video use superseded labels/IDs and are not final-submission evidence.

| Evidence | Status | Current evidence |
|---|---|---|
| Google Cloud project | PASS | Dedicated project `ai-evidence-engine-gugupro` |
| Cloud Run deployment | PASS | Revision `ai-evidence-explainer-00003-m75` in `asia-east1`, 100% traffic |
| Cloud Run health | PASS | Public HTTPS HTTP 200 |
| Gemini Production call | PASS | Vertex AI `gemini-2.5-flash` returned HTTP 200 and preserved `Verified Modified` |
| Gemini Cloud Logging | PASS | Request ID `3da55316-9616-46af-9ab2-39e34a1bdb49`; upstream Vertex AI HTTP 200; no prompt/secret logged |
| Gemini Observability screenshot | PASS | Sanitized two-day dashboard shows `gemini-2.5-flash` model invocations and token count in `docs/evidence/2026-08-15-gemini-observability.jpg` |
| Cloud Run Console screenshot | PASS | Sanitized service/region/URL and request metrics in `docs/evidence/2026-08-15-cloud-run-observability.jpg` |
| Rebuilt public verifier deployment | PASS | Sites Version 5, commit `2e8ef3cea3945f8db830ff76fd97e4d45e5cc3c8` |
| Rebuilt public browser regression | PASS | All four states, valid-C2PA Registry miss, no-C2PA miss, History, Mask, ProofCart, Gemini, adapters, and Next Stage rerun on public HTTPS |
| Final public demo video | PASS — judge-accessible | Replacement `HDG1qYo5hUg`: 2:43, 1920×1080, real Production operation and English captions; YouTube Studio reports Public and signed-out oEmbed returned HTTP 200 on 2026-08-15. Old `Fwu7yGUTVwo` remains rejected |
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

## Sites Version 5 public regression

Public URL: `https://ai-evidence-engine-gugupro.artistuncle.chatgpt.site`

- Signed Version 1: `Verified Original`, one C2PA manifest, Registry match, L0, no parent.
- Signed Version 3: `Verified Modified`, three C2PA manifests, Registry match, L4, parent Event present.
- Previous valid signed Version 3: `Unverified`, C2PA Valid, Registry No Match.
- Unsigned Modification Mask: `Unverified`, C2PA Not Present, Registry No Match.
- Tampered current Version 3: `Invalid Evidence`, `assertion.dataHash.mismatch`.
- History: all three rebuilt Event IDs rendered and changed state when selected.
- Modification Mask: `/demo/version-3-mask.png`, `4.8% measured pixel change`.
- ProofCart: `Verify Evidence` returned to current signed Version 3.
- Gemini: real Production response displayed `gemini-2.5-flash on Vertex AI` and `Status remains Verified Modified`; no fallback message.
- Universal architecture: Text, Image, Video, Audio, Documents, 2D, 3D, and Manufacturing adapters rendered with the shared foundation.
- Next Stage: Private Black Box + Mobile Authorization visibly labelled `NEXT — NOT YET IMPLEMENTED`.
- Evidence language: `aee.image.c2pa.v1`, Integrity, Provenance, Identity Trust, signed AI Involvement, Change Metrics, and Private Evidence are displayed as independent fields.
- Deterministic policy: `Valid C2PA + Registry No Match` remained `Unverified` and never displayed `Verified Original`.
