# AI Evidence Engine

Local-first **Universal Evidence Passport for Digital & Physical Creation** by **GUGUPRO**.

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
- **AEE Evidence Identification & Coding Standard v1.0** with versioned identifiers, `aee.event.v1`, implemented Text/Image profiles, deterministic verification policy, legacy signature compatibility, Wallet commitments, and authorization signing/validation foundations.
- Traditional Chinese default UI with a persistent English switch and a bilingual Privacy Policy.
- Android API 36 TWA source foundation, PWA manifest, Google Play listings, Data Safety draft, permission audit, signing plan, and closed-test plan.
- An IAM-protected **Development/Test** Remote Black Box API that binds an existing local `aee.event.v1` Signed Event one-to-one to synthetic evidence, seals it to the isolated Test Bucket with `ifGenerationMatch=0`, returns real retention metadata, retrieves it, deterministically reverifies SHA-256, and leaves the original Signed Event unchanged. This is not the Production Black Box.
- A public, rate-limited **Development/Test Evidence Continuity Demo** that accepts only the bundled synthetic ProofCart asset. Its AEE Backend creates and verifies a real Signed Event, calls the IAM-protected Remote Black Box with a dedicated service identity, displays Google Object generation and retention metadata, retrieves the Object, reverifies SHA-256, and verifies the unchanged Event again. Demo: https://aee-continuity-demo-856572888721.asia-east1.run.app

Not yet complete: Production Remote Black Box integration, remote Event Ledger, encrypted local queue/sync, production PKI/C2PA Trust List identity, Black Box authorization UI, desktop agent, persistent cloud registry, real external-user evidence, and production security hardening.

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

Previous public operation recording: https://www.youtube.com/watch?v=pqRNOvyE3_c —
1920×1080, 2:43, real image-verifier Production interaction. It predates the
Remote Black Box Test API and is **not the final submission video**. Board gate:
`VIDEO READY = NO` until Public Demo integration, local-to-remote continuity,
and a complete recordable rehearsal pass. The older `Fwu7yGUTVwo` and silent
`HDG1qYo5hUg` uploads are also superseded.

- Current ProofCart Version 3 evidence event: `1c3d4a0f-9e2a-4a18-a83f-0c982db4ef33`
- Current Version 3 SHA-256: `7e4bb29731e36aebad5907ce749bad3f0f542df155e39af713d30ed606bba37c`

See [AEE Coding Standard v1.0](docs/EVIDENCE_IDENTIFICATION_AND_CODING_STANDARD.md), [architecture](docs/ARCHITECTURE.md), [Android audit](docs/ANDROID_APP_AUDIT.md), [Google Play account checklist](docs/GOOGLE_PLAY_ACCOUNT_REQUIREMENTS.md), [evidence classification](docs/EVIDENCE_CLASSIFICATION_SPEC.md), [multimodal adapters](docs/MULTIMODAL_EVIDENCE_SPEC.md), [Private Black Box](docs/BLACK_BOX_ARCHITECTURE.md), [Mobile Authorization](docs/MOBILE_AUTHORIZATION_SPEC.md), [API](docs/API.md), [qualification audit](docs/QUALIFICATION_AUDIT.md), [final submission draft](docs/DEVPOST_FINAL_SUBMISSION.md), and [test report](docs/TEST_REPORT.md).
