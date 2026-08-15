# Build with Gemini XPRIZE — Final Qualification Audit

Audit date: 2026-08-15. Overall status: **FAIL — NOT SUBMISSION READY**.

Official references checked: Devpost Overview, FAQ, Schedule, and the XPRIZE launch announcement. The Rules page itself requires interactive browser verification; no rule acceptance or legal attestation was performed by this audit.

## Entrant type gate

The Entrant type is **BLOCKED — owner selection required**. Do not infer it from the GitHub organization, project brand, or number of contributors.

| Owner choice | Representative | Corporate ID |
|---|---|---|
| `INDIVIDUAL` | Tsing-YI Chen is the Entrant; no separate team representative | Not required unless the form explicitly requests an available business ID |
| `TEAM` | Team must appoint and authorize one representative; proposed representative must be confirmed by all eligible members | Not required for an unincorporated team unless the form/rules request an available ID |
| `ORGANIZATION` | Organization must appoint and authorize one representative | Required under the supplied decision; also verify the organization has fewer than 25 employees and is eligible |

## Final qualification gate

| Requirement | Evidence | Status | Submission location |
|---|---|---|---|
| Entrant Eligibility | Legal age, legal residence, prohibited-country, sponsor/affiliate, sanctions, and other Rule exclusions require Entrant attestation | BLOCKED | Eligibility / Rules acceptance |
| Correct Entrant Type | No explicit Individual, Team, or Organization selection has been received | BLOCKED | Entrant information |
| Representative if required | Tsing-YI Chen is proposed only; Team/Organization authorization has not been established | BLOCKED / N/A for Individual | Entrant information |
| Corporate ID if required | Conditional on Entrant type and whether a business ID is available | BLOCKED / N/A for Individual | Revenue/entity evidence |
| Project Created After 2026-05-19 | Earliest Git commit 2026-08-14; complete timeline in `PROJECT_ELIGIBILITY_TIMELINE.md` | PASS pending owner attestation | Build story / repository history |
| Pre-existing Work Disclosed | Generic frameworks, dependencies, C2PA tooling, templates, and primitives are separately disclosed | PASS | Build story / project description |
| Category Selected | Small Business Services | PASS | Category field |
| Google Cloud Product | Production Evidence Explainer on Cloud Run in `ai-evidence-engine-gugupro`; billing enabled | PASS | Google Cloud Usage |
| Gemini Production Call | Vertex AI `gemini-2.5-flash`, real HTTP 200 requests and logs | PASS | Gemini Usage / Production Evidence |
| Third-party SDK Authorization | C2PA/JS and other dependencies audited; applicable terms and license obligations identified | PASS with notices follow-up | IP / License Audit |
| Repository Complete | Public repository contains core, verifier, C2PA adapter, tests, explainer, and submission docs | PASS | Repository URL |
| Relevant License | Public repository reports Apache-2.0 | PASS | Repository / `LICENSE` |
| Public / Judge-accessible Demo | Anonymous HTTPS verifier and Cloud Run health both returned HTTP 200 on 2026-08-15 | PASS | Public Demo URL |
| Video <3 minutes | Local tracked evidence is 144 seconds; prior private-upload record says 2:43. Both are under 3 minutes, but file identity must be confirmed | PASS for duration / BLOCKED identity check | Video evidence |
| Video shows functioning Product | Prior record describes real Production operation; actual private upload requires final owner review | BLOCKED | Video URL |
| English Materials | English submission draft, testing instructions, narration, and subtitles exist | PASS | Submission text / video |
| Revenue Disclosure | Draft total revenue is $0.00; no bank/revenue evidence or owner confirmation supplied | BLOCKED | Revenue evidence / P&L |
| Monthly Revenue | May, June, July, August each drafted as $0.00; owner confirmation required | BLOCKED | Revenue evidence / P&L |
| Expenses | Draft total expenses is $0.00; Google Cloud and all other billing records not yet reconciled | BLOCKED | P&L |
| Marketing/CAC Spend | Draft $0.00 / $0.00; owner confirmation required | BLOCKED | P&L |
| Related-Party Revenue | Draft $0.00; owner confirmation required | BLOCKED | Revenue evidence / P&L |
| Real User Evidence | 0 verified external users; no informed external-user record or testimonial | FAIL | User evidence |
| Production Evidence | Public verifier screenshots, Cloud Run revision, Vertex AI request logs, and Gemini response evidence exist | PASS | Production Evidence |
| Google Cloud Billing Evidence | No monthly invoice or zero-dollar Cost Table export has been supplied | BLOCKED | Private/redacted evidence upload |
| Gemini Dashboard Evidence | Sanitized two-day dashboard screenshot shows `gemini-2.5-flash` model invocations and token usage | PASS | `docs/evidence/2026-08-15-gemini-observability.jpg` |
| Testing Instructions | Anonymous, no-payment test procedure exists in English | PASS | Testing Instructions |
| IP Ownership / Licensing | Source/dependencies audited; GUGUPRO, narration/audio, private upload, and no-unlicensed-music attestations remain | BLOCKED | IP / License Audit |
| No Secrets | Working tree and Git-history signature scan found no key/token/private-key patterns at this checkpoint | PASS | Repository evidence |
| Demo available through Judging Period | Demo, Cloud Run, and repository work now; video is private and owner maintenance commitment through 2026-09-15 is not recorded | BLOCKED | Testing Availability statement |

## Testing availability statement

- Public verifier: `https://ai-evidence-engine-gugupro.artistuncle.chatgpt.site` — no login or payment.
- Cloud Run explainer: `https://ai-evidence-explainer-856572888721.asia-east1.run.app` — public Production endpoint used by the verifier.
- Repository: `https://github.com/Guguproapp/ai-evidence-engine` — public, Apache-2.0.
- Video: private pending review; judges cannot rely on it until visibility is changed and externally verified.
- Official judging period shown on Devpost: 2026-08-20 09:00 PDT through 2026-09-15 17:00 PDT; winners announced 2026-09-25.

The Entrant must commit not to disable or place a paywall/login restriction on judge-required services before judging and verification are complete. If any endpoint becomes private, direct judge credentials and instructions must be supplied before the deadline.

## Blocking owner actions

1. Select `INDIVIDUAL`, `TEAM`, or `ORGANIZATION`; confirm representative and Corporate ID applicability.
2. Attest legal eligibility, project start date, and completeness of pre-existing-work disclosure while accepting the official Rules personally.
3. Export and redact Google Cloud monthly billing/Cost Table evidence.
4. Reconcile and confirm revenue, monthly revenue, expenses, Marketing/CAC spend, and related-party revenue against real records.
5. Complete at least one informed real external-user test and retain consent/evidence privately.
6. Confirm IP/brand/audio/music rights; review the actual private YouTube upload, then make the accepted video judge-accessible.
7. Keep the demo, Cloud Run, repository, and video available through judging; personally perform Final Submission.
