# AI Evidence Engine — Project Eligibility Timeline

Audit date: 2026-08-15. Official Submission Period: 2026-05-19 10:00 PDT through 2026-08-17 13:00 PDT.

## Conclusion

Repository evidence places every identifiable AI Evidence Engine product milestone inside the eligible period. The earliest commit is 2026-08-14, 87 days after the period opened. Git history can prove when recorded work first appeared; it cannot by itself prove that no unrecorded business existed earlier. The Entrant must therefore attest that the AI Evidence Engine business and project did not begin before 2026-05-19.

## Timeline

| Milestone | Earliest verified time | Evidence | Status |
|---|---|---|---|
| AI Evidence Engine business start | 2026-08-14, subject to Entrant attestation | Earliest repository commit and no supplied earlier business, customer, revenue, product, or production record | PASS pending owner attestation |
| First Git commit | 2026-08-14 00:46:34 +08:00 | `f63318236bc5e80b8fd1ee7238c3275ce3140f42` — `Build judge-ready AI Evidence Engine verifier` | PASS |
| First Product Build | 2026-08-14 | The first commit contains the verifier, registry/evidence implementation, tests, and reproducible web build; later `docs/TEST_REPORT.md` records successful automated builds | PASS |
| First public Production | 2026-08-14 | Production verifier integration was recorded in commit `f8112c8f55746f02330f4dac019d8d67b8144519`; current public endpoint returns HTTP 200 | PASS |
| First Google Cloud Production | 2026-08-14 | Cloud Run deployment recorded in commit `362b324ce117ccf53efb1c3db84d31c3608a89f8`; live service reports revision `ai-evidence-explainer-00003-m75` with 100% traffic | PASS |
| First Gemini Production Call | 2026-08-14 14:14:07 UTC | `docs/evidence/2026-08-14-cloud-run-gemini.md`; Vertex AI `gemini-2.5-flash`, HTTP 200, request ID preserved | PASS |
| Public GitHub repository created | 2026-08-14 11:24:21 UTC | GitHub repository metadata for `Guguproapp/ai-evidence-engine` | PASS |

## Pre-existing work disclosure

The AI Evidence Engine business logic listed below is represented by the supplied repository history as new work created during the Submission Period:

- Evidence Passport, signed Event Chain, Registry, and Evidence Wallet.
- C2PA image signing/reading adapter and the three-version ProofCart evidence chain.
- Deterministic Modification Mask and change metrics.
- Public verifier and deterministic provenance decision states.
- Cloud Run Evidence Explainer and bounded Gemini integration.
- AEE Evidence Identification & Coding Standard v1.0 and implemented text/image profiles.

The project reuses the following pre-existing or third-party generic building blocks and does not claim them as newly invented project code:

- Python and JavaScript language/runtime facilities.
- React, vinext/Vite, Cloudflare build tooling, ESLint, Tailwind-related build dependencies, and other packages pinned in `apps/web/package-lock.json`.
- Flask, Gunicorn, and the Google Gen AI SDK listed in `services/explainer/requirements.txt`.
- Official `c2patool` and `@contentauth/c2pa-web` C2PA tooling.
- Generic SVG starter icons and system font fallbacks.
- Generic cryptographic primitives and formats such as SHA-256, RSA, canonical JSON, UUID, PNG, and HTTPS.

No pre-existing product is being described as a newly created AI Evidence Engine feature. If any owner, contractor, employee, template, private source, or earlier prototype contributed material not visible in this repository, it must be disclosed before submission, together with associated hackathon-period expenses where required.

## Entrant attestation required

Before Final Submission, Tsing-YI Chen must confirm all three statements:

1. The AI Evidence Engine business/project began on or after 2026-05-19.
2. No product or business with substantially the same AI Evidence Engine operations existed before that date.
3. The pre-existing-work disclosure above is complete, or has been amended to include every omitted source.
