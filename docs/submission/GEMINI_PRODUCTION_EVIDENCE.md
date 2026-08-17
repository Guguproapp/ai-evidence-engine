# Gemini Production Evidence

Status: **READY**

- Model: `gemini-2.5-flash`
- Platform: Gemini API on Vertex AI
- Deployed service: `ai-evidence-explainer`
- Ready revision: `ai-evidence-explainer-00003-m75`
- Region: `asia-east1`
- Production health URL: https://ai-evidence-explainer-856572888721.asia-east1.run.app/health
- Relevant source: `services/explainer/app.py`
- Public caller: `apps/web/app/verifier.tsx`

Live Cloud Run logs on 2026-08-17 recorded repeated `evidence_explained` calls with `model=gemini-2.5-flash`, `status=Verified Modified`, and measured latency. Example timestamp: `2026-08-17T16:56:07.096922Z`; revision `ai-evidence-explainer-00003-m75`; latency 862 ms.

Evidence assets:

- `docs/evidence/2026-08-15-gemini-observability.jpg`
- `docs/evidence/2026-08-15-cloud-run-observability.jpg`
- `docs/evidence/2026-08-15-production-v3-gemini.png`
- `docs/evidence/2026-08-14-cloud-run-gemini.md`

## Safety boundary

Gemini receives allowlisted structured verification facts and generates a short explanation. It does not decide or modify Integrity, Provenance, Signature validity, Hash match, C2PA status, Retention state, or Evidence validity. No API key is shipped to the browser or repository; Cloud Run uses its service identity.
