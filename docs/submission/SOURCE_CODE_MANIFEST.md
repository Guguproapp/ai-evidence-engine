# Source Code Manifest

Status: **READY**

- Repository: https://github.com/Guguproapp/ai-evidence-engine
- Visibility: Public
- License: Apache-2.0
- Default branch: `main`
- Final audited remote SHA before this evidence-pack commit: `27d73634ea61982cdd33eb5dca608ab870b8d106`

## Source layout

| Path | Purpose |
|---|---|
| `apps/web` | Bilingual public verifier, First-Seen UI, ProofCart demo, local C2PA/SHA-256 verification, tests, and Sites build configuration |
| `src/ai_evidence` | Canonical identifiers, event schema, signatures, decision policy, Registry, Evidence Profiles, Text DNA, image diff, wallet commitments, and authorization foundation |
| `services/explainer` | Cloud Run Gemini Evidence Explainer with allowlisted facts and deterministic-status boundary |
| `services/blackbox` | IAM-protected Development/Test Remote Black Box API |
| `services/continuity_demo` | Public Development/Test continuity and Legacy Content Bridge demo |
| `tests` | Python unit/integration tests for core, C2PA, First-Seen, persistence, continuity, Black Box, and Gemini boundary |
| `apps/android-twa` | Non-blocking Android API 36 TWA source foundation; not part of the submitted production path |
| `scripts` | Reproducible demo/evidence generation and validation utilities |
| `docs` | Architecture, standards, threat boundaries, test evidence, and submission materials |

## Build and test

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
cd apps/web
npm ci
npm test
npm run lint
npm run build
```

Service-specific dependencies are pinned in each `services/*/requirements.txt`. Public configuration examples are provided without credentials. Production secrets, service-account credentials, and signing private keys are intentionally excluded.

## Judge usability conclusion

Judges have the necessary source code to understand and test the submitted production verifier, deterministic evidence core, Cloud Run explainer, Development/Test Black Box, continuity demo, and tests. Cloud credentials are not required to inspect the code or use the public deployment. Re-deploying the exact Google Cloud resources requires the judge's own project and credentials, as expected.

P0 missing source: **NONE FOUND**.
