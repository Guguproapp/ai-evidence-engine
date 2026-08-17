# Google Cloud Evidence

Status: **READY**

- Project ID: `ai-evidence-engine-gugupro`
- Project number: `856572888721`
- Project created: `2026-08-14T11:14:53.481Z`
- Region: `asia-east1`

## Cloud Run

| Service | Created | Ready revision | Traffic | Purpose |
|---|---|---|---:|---|
| `ai-evidence-explainer` | 2026-08-14T14:11:14Z | `ai-evidence-explainer-00003-m75` | 100% | Production Gemini explanation |
| `aee-blackbox-test` | 2026-08-16T15:43:57Z | `aee-blackbox-test-00003-nxw` | 100% | IAM-protected Development/Test sealing/retrieval API |
| `aee-continuity-demo` | 2026-08-16T18:14:31Z | `aee-continuity-demo-00007-hgm` | 100% | Public Development/Test continuity and First-Seen demo |

## Cloud Storage

- Bucket: `aee-blackbox-test-856572888721`
- Created: `2026-08-16T15:04:30Z`
- Region: `ASIA-EAST1`
- Public access prevention: enforced
- Uniform bucket-level access: enabled
- Test retention: 600 seconds
- Retention policy lock: not locked

Recorded final-demo evidence:

- Object generation: `1786985811149278`
- Retention until: `2026-08-17T17:06:51.153000Z`
- Original/Retrieved SHA-256: `e4935b1524169bb6353e993c4660524393c1cd430dd201e7bf63e2a9fcdd5da3`
- Hash match: YES
- Evidence Continuity: PASS

Independent uncut retention test:

- Object generation: `1786971545428744`
- Delete attempt: real Google Cloud HTTP 403 while retention was active
- Overwrite attempt: real generation-precondition HTTP 412
- Object still existed after both attempts: YES

Sanitized screenshots and logs are indexed in `PRODUCT_EVIDENCE_INDEX.md`. No credentials or private signing keys are included.
