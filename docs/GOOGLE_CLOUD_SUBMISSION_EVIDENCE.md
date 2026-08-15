# Google Cloud Submission Evidence Package

Audit date: 2026-08-15. This index separates evidence already preserved from account-owner evidence that must remain private and redacted.

## Production inventory

| Item | Current evidence | Status |
|---|---|---|
| Google Cloud project | `ai-evidence-engine-gugupro`; live Billing API reports billing enabled | PASS |
| Cloud Run deployment | Service `ai-evidence-explainer`, region `asia-east1`, ready revision `ai-evidence-explainer-00003-m75`, 100% traffic | PASS |
| Cloud Run HTTPS | `https://ai-evidence-explainer-856572888721.asia-east1.run.app`; health check HTTP 200 on 2026-08-15 | PASS |
| Gemini on Vertex AI | `gemini-2.5-flash`; real HTTP 200 Production calls and request IDs preserved in `docs/evidence/` | PASS |
| Production execution logs | Sanitized Cloud Run and Vertex AI request facts preserved in `docs/evidence/2026-08-14-cloud-run-gemini.md` and `docs/evidence/2026-08-15-four-state-cloud-run-gemini.md` | PASS |
| Public verifier integration | Public Sites verifier called the Cloud Run explainer and preserved the deterministic `Verified Modified` state | PASS |
| Monthly billing invoice / zero-dollar cost table | No redacted invoice or Cost Table export is present in the submission evidence package | BLOCKED — owner account action |
| Gemini Observability dashboard screenshot | `docs/evidence/2026-08-15-gemini-observability.jpg`; two-day dashboard shows `gemini-2.5-flash` model invocations and token count | PASS |
| Cloud Run Console deployment screenshot | `docs/evidence/2026-08-15-cloud-run-observability.jpg`; service, region, public URL, request metrics, and latency views are visible | PASS |

## Evidence already safe to submit

- Google Cloud project ID, service name, region, revision, public URL, model name, non-sensitive request ID, timestamp, HTTP result, and deterministic verification state.
- Product screenshots under `docs/evidence/` that show the public verifier, C2PA result, History, Mask, ProofCart, and Gemini explanation.
- Sanitized text evidence that excludes prompts, credentials, keys, tokens, private Evidence Wallet content, billing identifiers, and payment information.

## Owner capture procedure

These files must be downloaded or captured while signed into the Google Cloud account. They must not be committed to the public repository unless fully redacted.

1. Billing: Google Cloud Console → Billing → Documents/Invoices or Cost table. Export each available monthly invoice for the competition period. If credits or Free Trial make the invoice zero, export the zero-dollar invoice or monthly Cost Table.
2. Gemini: Vertex AI → Monitoring/Observability → select the production Gemini model and competition date range. Capture a screenshot showing actual request usage and timestamps.
3. Cloud Run: open `ai-evidence-explainer` in `asia-east1`. Capture service name, ready revision, traffic, and URL.
4. Logs Explorer: capture a filtered production request showing timestamp, Cloud Run revision, Vertex AI method/model, and successful response.

## Mandatory redaction

Remove or cover all of the following before uploading evidence to Devpost:

- Billing account number, payment method, card/bank details, address, tax data, and unrelated project costs.
- OAuth tokens, access tokens, API keys, service-account credentials, private keys, cookies, and authorization headers.
- Unrelated project names, personal data, prompts, source assets, and Private Evidence Wallet contents.

Keep unredacted financial originals outside Git. Devpost submission evidence should contain only the minimum information needed to establish monthly Google Cloud usage and cost.

## Official minimum evidence boundary

The official FAQ requests monthly Google Cloud billing invoices for the competition or a zero-dollar invoice/Cost Table when using credits, plus screenshots of observability dashboards for Gemini models and supporting execution/API logs. The observability and supporting-log requirements now have evidence. The monthly invoice/Cost Table export is still missing and cannot be replaced by a dashboard screenshot.
