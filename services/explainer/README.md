# Evidence Explainer — Cloud Run + Gemini

This bounded service explains an already-computed verification result. It does not determine `Verified Original`, `Verified Modified`, `Unverified`, or `Invalid Evidence`.

Production target:

- Google Cloud Run
- Gemini API on Vertex AI
- Cloud Run service-account Application Default Credentials
- No API key in source or frontend

Required APIs: Cloud Run, Cloud Build, Artifact Registry, Vertex AI.

The service accepts only an allowlisted set of structured verification facts, enforces a 16 KB request limit and a basic per-instance rate limit, and logs request ID, evidence ID, deterministic status, model, and latency without logging prompts or secrets.

Deployment is intentionally not claimed until a real Cloud Run URL, successful Gemini response, Cloud Logging record, and Vertex AI usage record are captured.
