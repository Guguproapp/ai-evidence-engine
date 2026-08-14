# Four-state Cloud Run and Gemini production evidence

Date: 2026-08-15 Asia/Taipei (`2026-08-14T20:47:32Z` in Cloud Logging)

Cloud Run service: `ai-evidence-explainer`

Revision: `ai-evidence-explainer-00003-m75`, `asia-east1`, 100% traffic.

Public endpoint: `https://ai-evidence-explainer-856572888721.asia-east1.run.app`

## Executed request

The rebuilt service received an allowlisted structured result for Evidence ID `1c3d4a0f-9e2a-4a18-a83f-0c982db4ef33` with deterministic status `Verified Modified`, parent `proofcart-v2`, three C2PA manifests, a matched Registry record, a valid evidence signature, and measured change ratio `0.047743`.

The Production response returned HTTP 200 with:

- model: `gemini-2.5-flash`
- provider: `Gemini API on Vertex AI`
- preserved status: `Verified Modified`
- decision source: `AI Evidence Engine cryptographic verification`
- request ID: `3da55316-9616-46af-9ab2-39e34a1bdb49`

Cloud Logging independently recorded the same request ID and Evidence ID, `status=Verified Modified`, model, and 3590 ms latency. The upstream Vertex AI `generateContent` request returned HTTP 200.

Gemini explained an already-computed result. It did not assign or change `Verified Original`, `Verified Modified`, `Unverified`, or `Invalid Evidence`.

No API key, OAuth token, credential, private key, prompt, or private Evidence Wallet content is included in this evidence record.
