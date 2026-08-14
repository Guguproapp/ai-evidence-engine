# AI Evidence Engine

Local-first **Universal Evidence Passport for Digital & Physical Creation** by **gugupro**.

This is not an AI detector and does not produce legal conclusions. It records where a creation came from, which tools or agents changed it, how much changed, and whether its signed history was tampered with. Image is the first working adapter; text, video, audio, documents, 2D design, 3D models, and digital manufacturing share the same Passport, Event Chain, Registry, and Private Wallet architecture.

## Working checkpoint

- Real RSA-2048/SHA-256 issuer keys and signatures through the system OpenSSL executable.
- Append-only JSONL registry with parent-event and parent-hash chains.
- Local private Evidence Wallet files with `0600` permissions.
- Exact, paragraph, sentence, and word n-gram text fingerprints.
- Evidence tiers: exact, large continuous, partial, approximate rewrite, semantic-only.
- HTTP endpoints for register, verify, passport, history, issuer, revoke, and fingerprint lookup.
- Deterministic tests for retyping, small edits, heavy rewrites, common short phrases, signatures, tampering, and chains.
- Three-version image provenance chain using official C2PA tooling.
- Explainable RGB image-diff masks with measured change ratios and bounding boxes.
- Judge-facing Verifier website with Try Demo, upload verification, Evidence ID lookup, version history, and ProofCart vertical demo.
- A production Cloud Run Evidence Explainer using Vertex AI `gemini-2.5-flash`, while keeping Gemini outside the deterministic verification decision.
- Public Production Version 3 with the corrected `GUGUPRO` brand, rebuilt image hashes, C2PA parent ingredients, signed events, Registry records, and Modification Mask.
- Four independent provenance outcomes: `Verified Original`, `Verified Modified`, `Unverified`, and `Invalid Evidence`; identity trust and C2PA integrity are displayed separately.
- Formal L0–L5 AI involvement, multimodal change metrics, Private Black Box, and Mobile Authorization specifications.

Not yet complete: production PKI/C2PA Trust List identity, Black Box authorization UI, desktop agent, persistent cloud registry, real external-user evidence, and production security hardening.

## Run

Requires Python 3.9+ and OpenSSL.

```bash
cd ai-provenance
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 scripts/demo.py
PYTHONPATH=src python3 scripts/build_image_demo.py
PYTHONPATH=src python3 -m ai_evidence.api
```

Health check:

```bash
curl http://127.0.0.1:8787/health
```

Register text:

```bash
curl -X POST http://127.0.0.1:8787/register \
  -H 'Content-Type: application/json' \
  -d '{"content":"需要登錄的文字","provider":"gugupro","action_type":"generate","involvement_level":"L5"}'
```

## Truth boundary

Every adapter has a `STATUS.md`. `NOT RUN` and `not integrated` are intentional; no mock response is represented as official support.

Web verifier:

```bash
cd apps/web
npm install
npm run dev
```

Public verifier: https://ai-evidence-engine-gugupro.artistuncle.chatgpt.site

Final demo recording: `HDG1qYo5hUg` — **PASS**, 1920×1080, 2:43, real
Production interaction with burned-in English captions. Visibility is
**PRIVATE — pending owner review**; do not place it in the final submission
until the owner re-enables public access. The superseded `Fwu7yGUTVwo` video
remains rejected and must not be submitted.

- Current ProofCart Version 3 evidence event: `1c3d4a0f-9e2a-4a18-a83f-0c982db4ef33`
- Current Version 3 SHA-256: `7e4bb29731e36aebad5907ce749bad3f0f542df155e39af713d30ed606bba37c`

See [architecture](docs/ARCHITECTURE.md), [evidence classification](docs/EVIDENCE_CLASSIFICATION_SPEC.md), [multimodal adapters](docs/MULTIMODAL_EVIDENCE_SPEC.md), [Private Black Box](docs/BLACK_BOX_ARCHITECTURE.md), [Mobile Authorization](docs/MOBILE_AUTHORIZATION_SPEC.md), [API](docs/API.md), [qualification audit](docs/QUALIFICATION_AUDIT.md), [final submission draft](docs/DEVPOST_FINAL_SUBMISSION.md), and [test report](docs/TEST_REPORT.md).
