# Production Evidence — Cloud Run and Gemini

Captured: 2026-08-14 UTC. This record contains no API key, OAuth token, service-account key, private key, or billing identifier.

## Cloud Run

- Google Cloud project: `ai-evidence-engine-gugupro`
- Service: `ai-evidence-explainer`
- Region: `asia-east1`
- Public URL: `https://ai-evidence-explainer-856572888721.asia-east1.run.app`
- Ready revision: `ai-evidence-explainer-00002-z76`
- Traffic: 100% to the ready revision
- Runtime identity: keyless dedicated service account
- Limits: 1 CPU, 512 MiB, maximum 3 instances, 60-second timeout

The public health request returned HTTP 200 and declared Cloud Run, Vertex AI, and `gemini-2.5-flash`.

## Real Gemini API production call

Timestamp: `2026-08-14T14:14:07Z`

Request facts were allowlisted and contained a deterministic `Modified` result. The response returned HTTP 200:

- Request ID: `0b64459c-ff15-4e49-91b4-e0dbc2073ddd`
- Provider: Gemini API on Vertex AI
- Model: `gemini-2.5-flash`
- Returned verification status: `Modified`
- Decision source: AI Evidence Engine cryptographic verification
- Explanation: `This image has been modified, with an object added and a label edited. The changes were signed by "gugupro development issuer" and the signature is valid.`

Cloud Logging independently recorded:

- a POST to `aiplatform.googleapis.com/v1/projects/ai-evidence-engine-gugupro/locations/global/publishers/google/models/gemini-2.5-flash:generateContent`
- upstream response `HTTP/1.1 200 OK`
- the same request ID, evidence ID `event-3`, deterministic status `Modified`, model, and 4522 ms latency

Gemini explained an already-computed result. It did not determine or overwrite `Authentic`, `Modified`, `Unknown`, or `Invalid Signature`.

## Public Verifier production integration — Version 3 refresh

Sites Version 3 deployed commit `c0a407a160c3bf90a03f76a75c69ce6f577f5976` to the public verifier. A fresh browser test opened the anonymous HTTPS site, selected the rebuilt ProofCart Version 3 evidence, clicked `Explain with Gemini`, and received:

- Explanation: `This image has been modified. Specifically, the product label area was changed.`
- Model: `gemini-2.5-flash` on Vertex AI
- Preserved status: `Modified`

Cloud Logging recorded the browser-triggered request at `2026-08-14T17:07:58Z` with request ID `79039afc-d8e9-4ae1-8569-0d7a780e387d`, ProofCart evidence ID `b56445dd-1530-4c69-93d1-6977120a9f40`, revision `ai-evidence-explainer-00002-z76`, and 3460 ms latency. The Vertex AI upstream request returned HTTP 200.

Version 3 Production browser regression passed `Modified`, `Authentic`, `Unknown`, `Invalid Signature`, Modification Mask, three-version history, ProofCart, Advanced C2PA evidence, and Gemini Explanation. A local cross-origin failure simulation displayed the fallback message and left the cryptographic status unchanged.
