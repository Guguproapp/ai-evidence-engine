# Build with Gemini XPRIZE — Final Qualification Audit

Audit date: 2026-08-15. Overall status: **FAIL — NOT SUBMISSION READY**.

Official references checked: Devpost Overview, FAQ, Schedule, and the XPRIZE launch announcement. The Rules page itself requires interactive browser verification; no rule acceptance or legal attestation was performed by this audit.

## Entrant type gate

Entrant Type: **INDIVIDUAL**.

- Entrant: **Tsing-YI Chen / 陳宗億**.
- Product/brand: **AI Evidence Engine by GUGUPRO**.
- GUGUPRO is a product/brand identifier and is not the Organization Entrant.
- Representative: **NOT REQUIRED** for an Individual.
- Corporate ID: **NOT REQUIRED** for an Individual unless the actual Devpost form explicitly requests an available identifier.

## Final qualification gate

| Requirement | Evidence | Status | Submission location |
|---|---|---|---|
| Entrant Eligibility | Legal age, legal residence, prohibited-country, sponsor/affiliate, sanctions, and other Rule exclusions require Entrant attestation | BLOCKED | Eligibility / Rules acceptance |
| Correct Entrant Type | Owner decision: `INDIVIDUAL`; Tsing-YI Chen / 陳宗億 | PASS | Entrant information |
| Representative if required | Not required for an Individual | N/A | Entrant information |
| Corporate ID if required | Not required for an Individual unless the actual form explicitly asks for an available identifier | N/A | Revenue/entity evidence |
| Project Created After 2026-05-19 | Earliest Git commit 2026-08-14; complete timeline in `PROJECT_ELIGIBILITY_TIMELINE.md` | PASS pending owner attestation | Build story / repository history |
| Pre-existing Work Disclosed | Generic frameworks, dependencies, C2PA tooling, templates, and primitives are separately disclosed | PASS | Build story / project description |
| Category Selected | Small Business Services | PASS | Category field |
| Google Cloud Product | Production Evidence Explainer on Cloud Run in `ai-evidence-engine-gugupro`; billing enabled | PASS | Google Cloud Usage |
| Gemini Production Call | Vertex AI `gemini-2.5-flash`, real HTTP 200 requests and logs | PASS | Gemini Usage / Production Evidence |
| Third-party SDK Authorization | C2PA/JS and other dependencies audited; applicable terms and license obligations identified | PASS with notices follow-up | IP / License Audit |
| Repository Complete | Public repository contains core, verifier, C2PA adapter, tests, explainer, and submission docs | PASS | Repository URL |
| Relevant License | Public repository reports Apache-2.0 | PASS | Repository / `LICENSE` |
| Public / Judge-accessible Demo | Anonymous HTTPS verifier and Cloud Run health both returned HTTP 200 on 2026-08-15 | PASS | Public Demo URL |
| Video <3 minutes | Final local review candidate is 162.733 seconds, 1920×1080, 30fps, 16:9 | PASS for duration / BLOCKED owner acceptance | Video evidence |
| Video shows functioning Product | 2:42.733 Production recording and sampled timeline show signed upload, verification, Mask, History, tamper failure, Gemini, ProofCart, and next-stage boundary | PASS technical review | Video URL |
| English Materials | English submission draft, testing instructions, narration, and subtitles exist | PASS | Submission text / video |
| Revenue Disclosure | Draft total revenue is $0.00; no bank/revenue evidence or owner confirmation supplied | BLOCKED | Revenue evidence / P&L |
| Monthly Revenue | May, June, July, August each drafted as $0.00; owner confirmation required | BLOCKED | Revenue evidence / P&L |
| Expenses | Draft total expenses is $0.00; Google Cloud and all other billing records not yet reconciled | BLOCKED | P&L |
| Marketing/CAC Spend | Draft $0.00 / $0.00; owner confirmation required | BLOCKED | P&L |
| Related-Party Revenue | Draft $0.00; owner confirmation required | BLOCKED | Revenue evidence / P&L |
| Real User Evidence | 0 verified external users; no informed external-user record or testimonial | FAIL | User evidence |
| Production Evidence | Public verifier screenshots, Cloud Run revision, Vertex AI request logs, and Gemini response evidence exist | PASS | Production Evidence |
| Google Cloud Billing Evidence | Current official FAQ says the minimum evidence includes monthly billing PDFs, or a zero-dollar invoice/Cost Table when using credits; no export has been supplied | BLOCKED — required submission evidence, not Entrant-type eligibility | Private/redacted evidence upload |
| Gemini Dashboard Evidence | Sanitized two-day dashboard screenshot shows `gemini-2.5-flash` model invocations and token usage | PASS | `docs/evidence/2026-08-15-gemini-observability.jpg` |
| Testing Instructions | Anonymous, no-payment test procedure exists in English | PASS | Testing Instructions |
| IP Ownership / Licensing | Source/dependencies audited; GUGUPRO and final-video rights attestations remain owner-controlled | BLOCKED | IP / License Audit |
| No Secrets | Working tree and Git-history signature scan found no key/token/private-key patterns at this checkpoint | PASS | Repository evidence |
| Demo available through Judging Period | Demo, Cloud Run, repository, and video are publicly accessible now; owner maintenance commitment through 2026-09-15 is not recorded | BLOCKED owner commitment | Testing Availability statement |

## Testing availability statement

- Public verifier: `https://ai-evidence-engine-gugupro.artistuncle.chatgpt.site` — no login or payment.
- Cloud Run explainer: `https://ai-evidence-explainer-856572888721.asia-east1.run.app` — public Production endpoint used by the verifier.
- Repository: `https://github.com/Guguproapp/ai-evidence-engine` — public, Apache-2.0.
- Video: public at `https://www.youtube.com/watch?v=HDG1qYo5hUg`; signed-out oEmbed returned HTTP 200.
- Official judging period shown on Devpost: 2026-08-20 09:00 PDT through 2026-09-15 17:00 PDT; winners announced 2026-09-25.

The Entrant must commit not to disable or place a paywall/login restriction on judge-required services before judging and verification are complete. If any endpoint becomes private, direct judge credentials and instructions must be supplied before the deadline.

## Blocking owner actions

1. Attest legal eligibility, project start date, and completeness of pre-existing-work disclosure while accepting the official Rules personally.
2. Export and redact Google Cloud monthly billing PDF, zero-dollar invoice, or Cost Table evidence required by the current FAQ.
3. Reconcile and confirm revenue, monthly revenue, expenses, Marketing/CAC spend, and related-party revenue against real records.
4. Complete at least one informed real external-user test and retain consent/evidence privately.
5. Confirm IP/brand/video rights and the final submission facts for the now-public YouTube video.
6. Keep the demo, Cloud Run, repository, and video available through judging; personally perform Join/Rules/Final Submission steps.
