# Build with Gemini XPRIZE — Final Qualification Audit

Audit date: 2026-08-18. Overall status: **FAIL — NOT SUBMISSION READY**.

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
| Video <3 minutes | Final narrated candidate is 148.000 seconds, 1920×1080, 30fps, 16:9, with a 48 kHz mono AAC track and embedded English subtitles | PASS local technical review | Video evidence |
| Video shows functioning Product | Real Production and Development/Test recordings show provenance verification, First-Seen, V1 → V2, measured change, Gemini boundary, retention, HTTP 403 delete rejection, HTTP 412 overwrite rejection, retrieval, SHA-256 Match, and Evidence Continuity | PASS local technical review | Video URL |
| Video Judge-accessible | Final 2026-08-18 candidate has not been uploaded/published; the older public video is superseded | BLOCKED owner video approval and publication | Video URL |
| English Materials | English submission draft, testing instructions, narration, and subtitles exist | PASS | Submission text / video |
| Revenue Disclosure | Owner confirmed total revenue USD 0 | PASS | Revenue evidence / P&L |
| Monthly Revenue | Owner confirmed May, June, July, and August at USD 0 each | PASS | Revenue evidence / P&L |
| Expenses | Google Cloud shows USD 0.45 gross August usage fully offset by credits; owner confirmed total actual cash expense USD 0 | PASS | P&L / private billing evidence |
| Marketing/CAC Spend | Owner confirmed USD 0 / USD 0 | PASS | P&L |
| Related-Party Revenue | Owner confirmed USD 0 | PASS | Revenue evidence / P&L |
| Real User Evidence | 0 external users disclosed truthfully; FAQ states no minimum customer threshold, though this weakens Business Viability | PASS disclosure / no traction | User evidence |
| Production Evidence | Public verifier screenshots, Cloud Run revision, Vertex AI request logs, and Gemini response evidence exist | PASS | Production Evidence |
| Google Cloud Billing Evidence | Signed-in Billing overview shows USD 0.45 gross August usage, USD 0.45 savings/credits, USD 0.00 total cost, and active free trial | PASS private evidence; invoice optional unless live form asks | Private local archive |
| Gemini Dashboard Evidence | Sanitized two-day dashboard screenshot shows `gemini-2.5-flash` model invocations and token usage | PASS | `docs/evidence/2026-08-15-gemini-observability.jpg` |
| Testing Instructions | Anonymous, no-payment test procedure exists in English | PASS | Testing Instructions |
| IP Ownership / Licensing | Owner confirmed GUGUPRO/AEE materials and license-compliant third-party use; legal checkbox remains owner-only | PASS evidence / OWNER ACTION for legal checkbox | IP / License Audit |
| No Secrets | Working tree and Git-history signature scan found no key/token/private-key patterns at this checkpoint | PASS | Repository evidence |
| Demo available through Judging Period | Demo, Cloud Run, repository, and video are publicly accessible now; owner maintenance commitment through 2026-09-15 is not recorded | BLOCKED owner commitment | Testing Availability statement |

## Testing availability statement

- Public verifier: `https://ai-evidence-engine-gugupro.artistuncle.chatgpt.site` — no login or payment.
- Cloud Run explainer: `https://ai-evidence-explainer-856572888721.asia-east1.run.app` — public Production endpoint used by the verifier.
- Repository: `https://github.com/Guguproapp/ai-evidence-engine` — public, Apache-2.0.
- Video: final 2026-08-18 candidate is complete locally but not judge-accessible. The older `pqRNOvyE3_c` and `HDG1qYo5hUg` videos are superseded.
- Official judging period shown on Devpost: 2026-08-20 09:00 PDT through 2026-09-15 17:00 PDT; winners announced 2026-09-25.

The Entrant must commit not to disable or place a paywall/login restriction on judge-required services before judging and verification are complete. If any endpoint becomes private, direct judge credentials and instructions must be supplied before the deadline.

## Blocking owner actions

1. Attest legal eligibility, project start date, and completeness of pre-existing-work disclosure while accepting the official Rules personally.
2. Reconcile and confirm revenue, monthly revenue, expenses, Marketing/CAC spend, and related-party revenue against real records; attach redacted billing/Cost Table support if available.
3. Review the exact 2026-08-18 final candidate, confirm IP/brand/video rights, and approve judge-accessible publication.
4. Keep the demo, Cloud Run, repository, and video available through judging; personally perform Join/Rules/Final Submission steps.

Optional before deadline: complete an informed real external-user test. Do not delay Final Submission if the truthful count remains zero.
