# AI Evidence Engine

Local-first AI content provenance prototype by **gugupro**.

This is not an AI detector and does not produce legal conclusions. It records verifiable events, keeps private source content in a local Evidence Wallet, publishes only minimum passport evidence, and compares text using hierarchical fingerprints.

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

Not yet complete: production PKI/C2PA Trust List identity, Black Box authorization UI, desktop agent, persistent cloud registry, public YouTube/Vimeo video hosting, real external-user evidence, and production security hardening.

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

- Current ProofCart Version 3 evidence event: `b56445dd-1530-4c69-93d1-6977120a9f40`
- Current Version 3 SHA-256: `3b00f3ac87e58c5bf5ddb5e2dd021a0236bc3e3c5a02c082c1735867ea81bba9`

See [architecture](docs/ARCHITECTURE.md), [API](docs/API.md), [Build with Gemini XPRIZE compliance](docs/BUILD_WITH_GEMINI_XPRIZE.md), [qualification audit](docs/QUALIFICATION_AUDIT.md), [final submission draft](docs/DEVPOST_FINAL_SUBMISSION.md), [video script](docs/VIDEO_SCRIPT_XPRIZE.md), and [test report](docs/TEST_REPORT.md).
