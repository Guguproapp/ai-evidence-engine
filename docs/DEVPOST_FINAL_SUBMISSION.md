# Devpost Final Submission — AI Evidence Engine

Status: **DRAFT — NOT SUBMISSION READY**

## Entrant

Entrant Type: `INDIVIDUAL`.

Entrant: `Tsing-YI Chen / 陳宗億`.

Product/brand: `AI Evidence Engine by GUGUPRO`. GUGUPRO is not the Organization Entrant.

Representative: `NOT REQUIRED`.

Corporate ID: `NOT REQUIRED`, unless the actual Individual submission form explicitly asks for an available identifier.

## Project Name

AI Evidence Engine

## Category

Small Business Services

## Elevator Pitch

AI Evidence Engine is a Universal Evidence Passport for Digital & Physical Creation: it preserves and verifies recorded provenance and signed version history, measures changes between trusted recorded versions, and detects tampering with the evidence chain.

## What it does

AI Evidence Engine helps merchants, platforms, and consumers verify recorded provenance without guessing whether AI made something. It combines content hashes, digital signatures, C2PA manifests, an append-only parent-child event chain, and modality-specific change metrics. Image is the first working adapter; text, video, audio, documents, 2D design, 3D models, and manufacturing share the Passport, Registry, and Private Wallet architecture. The public verifier presents `Verified Original`, `Verified Modified`, `Unverified`, or `Invalid Evidence` without claiming world truth or a legal verdict.

Capability boundary: Level 1 Provenance Verification is implemented. Level 2 Known-Version Modification Comparison is implemented when trusted recorded versions exist. Level 3 Single-Asset Forensic Modification Detection is not implemented. An unfamiliar image without trusted provenance returns `Unverified`; AEE does not infer whether it is real, fake, edited, or AI-generated from appearance.

ProofCart is the first Small Business Services use case. For a listing photo with recorded provenance, a buyer can inspect its registered original version, edit history, changed region, C2PA provenance, and signed Registry evidence before deciding whether to trust the media.

## How we built it

- Official `c2patool 0.27.12` creates, embeds, reads, and verifies C2PA manifests.
- Official `@contentauth/c2pa-web 0.13.4` verifies image provenance in the browser.
- RSA-2048/SHA-256 signs canonical evidence events.
- An append-only event chain preserves version and parent-hash relationships.
- A deterministic RGB image-diff algorithm compares trusted recorded versions and generates the Modification Mask, ratio, and bounding box.
- AEE Evidence Identification & Coding Standard v1.0 separates integrity, provenance, identity trust, signed AI involvement, and change scope; `aee.event.v1` and legacy compatibility are covered by automated tests.
- The verifier processes uploaded images locally in the browser and has no image-upload endpoint.
- A bounded Cloud Run Evidence Explainer calls Gemini on Vertex AI only after cryptographic verification; Gemini cannot assign or change the deterministic provenance state.

The AI Evidence Engine business and repository were created during the Submission Period. The first Git commit is dated 2026-08-14. Generic language/runtime facilities, React/vinext tooling, open-source packages, C2PA tooling, generic starter assets, and standard cryptographic primitives are pre-existing building blocks and are not claimed as newly created project IP. See `docs/PROJECT_ELIGIBILITY_TIMELINE.md`.

## AI-Native Operations

The evidence decision pipeline is deterministic. Hash, signature, C2PA, registry, and parent-chain validation determine the verification state. Gemini is restricted to explaining the supplied structured facts to a non-technical buyer; it cannot replace or reinterpret the verification state.

Current qualification status: the deployed Cloud Run service made a logged Vertex AI Gemini production call while preserving the deterministic verification result.

## Google Cloud Usage

Production product: Google Cloud Run, hosting the Evidence Explainer API in the dedicated project `ai-evidence-engine-gugupro`.

Authentication design: Cloud Run service-account Application Default Credentials. No Gemini API key is shipped to the browser or repository.

Current status: PASS. Revision `ai-evidence-explainer-00003-m75` is ready in `asia-east1` and serves 100% of traffic at the public Cloud Run URL.

## Gemini Usage

Planned API: Gemini API on Vertex AI using the official Google Gen AI SDK.

Input: allowlisted structured verification facts after the deterministic verifier has completed.

Output: a two-sentence buyer-facing explanation. The deterministic status is returned unchanged alongside the explanation.

Current status: PASS. Cloud Run revision `ai-evidence-explainer-00003-m75` made a real `gemini-2.5-flash` Vertex AI call for rebuilt Evidence ID `1c3d4a0f-9e2a-4a18-a83f-0c982db4ef33`, returned HTTP 200, and preserved `Verified Modified`. Sites Version 5 then reproduced the same result from the public verifier. Sanitized evidence is preserved under `docs/evidence/`.

## C2PA

The three-version ProofCart image chain contains real embedded C2PA manifests and parent ingredients. Original C2PA reports are preserved. The bytes and claims validate, while the current demo signing certificate is a development identity and is not represented as a production-trusted C2PA Trust List identity.

## ProofCart Use Case

ProofCart demonstrates how a small merchant can attach evidence to a product image and how a buyer can verify its recorded provenance, two registered edits, changed region, signatures, C2PA chain, and Registry record.

## Business Model

Potential model: verification and provenance infrastructure sold to merchants and platforms through usage-based API plans and ProofCart verification features. No paid customer or enterprise partnership is currently claimed.

## Users

Verified external users: 0 at this checkpoint. Internal developer and automated browser tests are not counted. Use `docs/REAL_USER_TEST_PACKET.md` and replace this sentence only after a consenting external user actually completes the flow.

## Revenue

Total Revenue: $0.00 USD.

Monthly revenue: May $0.00; June $0.00; July $0.00; August $0.00 as of 2026-08-15.

Related-Party Revenue: $0.00.

Status: draft pending owner reconciliation against bank, payment, and customer records.

## Expenses

Total documented expenses: $0.00 pending Entrant confirmation against all billing records.

Marketing Spend: $0.00. Customer Acquisition Spend: $0.00.

Status: draft pending owner reconciliation against Google Cloud, API, hosting, labor, contractor, marketing, and acquisition records.

## Challenges

The central technical challenge was separating content integrity from issuer trust. A C2PA claim can be cryptographically intact while the development certificate is not on the official Trust List. The interface therefore states `Integrity verified; development identity` instead of overstating production trust.

The Gemini boundary presents a second challenge: a helpful explanation must never become an ungrounded provenance verdict. The service validates a deterministic status, forwards only allowlisted facts, and returns that status unchanged.

## Accomplishments

- Three signed image versions with nested C2PA parent ingredients.
- Shared Event IDs between C2PA assertions and the signed Registry.
- Actual pixel-derived Modification Masks between trusted recorded versions.
- Working local `Verified Original`, `Verified Modified`, `Unverified`, and `Invalid Evidence` classification flows.
- Public one-click ProofCart demo.
- 47/47 Python tests and 14/14 website tests at the current local checkpoint.
- Implemented `aee.text.v1` and `aee.image.c2pa.v1` Evidence Profiles, with audio/video/document/2D/3D/manufacturing explicitly marked `SPECIFIED_NOT_IMPLEMENTED`.
- Formal L0–L5 AI involvement, multimodal adapter metrics, and owner-controlled Private Black Box / Mobile Authorization architecture without representing the next-stage features as complete.

## What we learned

Provenance should report evidence rather than make legal verdicts. Recorded version events can support contribution and modification history; an AI detector probability cannot reconstruct missing provenance with certainty.

## What's next

- Obtain external user feedback with informed disclosure.
- Replace the demo registry bundle with a persistent production registry.
- Obtain a production C2PA signing certificate and protect the key with KMS/HSM after submission readiness.
- Implement the owner-controlled Private Black Box and single-use Mobile Authorization design after the hackathon submission.

## Testing Instructions

1. Open the public demo without signing in.
2. Use `Upload an image` with the signed Version 3 fixture, or click `Try the 60-second demo`.
3. Confirm `Verified Modified`, valid evidence signature, three C2PA versions, and Registry match.
4. Click `Change overlay` and `Mask` to inspect the 4.8% changed region.
5. Select Versions 1, 2, and 3 to inspect parent-child history.
6. Open Advanced details to inspect Manifest ID, Event ID, parent, and event hash.
7. Click ProofCart `Verify Evidence`.
8. Click `Explain with Gemini` and confirm the plain-language explanation appears while the deterministic status remains unchanged.
9. Review `One evidence foundation. Many creation formats.` and the explicitly labelled `NEXT — NOT YET IMPLEMENTED` Mobile Authorization architecture.

No login or payment is required for the public verifier.

The Entrant must keep the public verifier, Cloud Run explainer, repository, and judge-accessible video operational without payment through the official judging period ending 2026-09-15 17:00 PDT and any announced verification window.

## Public Demo URL

https://ai-evidence-engine-gugupro.artistuncle.chatgpt.site

## Cloud Production URL

https://ai-evidence-explainer-856572888721.asia-east1.run.app

## Repository URL

https://github.com/Guguproapp/ai-evidence-engine

## Video URL

https://www.youtube.com/watch?v=pqRNOvyE3_c

Visibility: `PUBLIC`. A signed-out YouTube oEmbed request returned HTTP 200 on 2026-08-15, confirming judge-accessible playback metadata.

The matching local final candidate measures 2:42.734, 1920×1080, 30fps, 16:9, and contains a 48 kHz mono AAC English narration track. Its visuals use real Production
interaction with burned-in English captions. It shows signed Version 3 upload,
all three image views, version history, a real tampered upload,
`assertion.dataHash.mismatch`, Gemini explanation, ProofCart, the universal
adapter architecture, and the explicitly labelled next stage. The superseded
`Fwu7yGUTVwo` and silent `HDG1qYo5hUg` videos must not be submitted.

Frame sampling found no giant black borders or cropped browser column. The Entrant must still confirm the IP declarations and final submission facts personally.

## Production Evidence

See `docs/PRODUCTION_EVIDENCE.md`. Sanitized Cloud Run, Vertex AI, and public
verifier request evidence has been preserved without credentials.

Sanitized Gemini Observability and Cloud Run screenshots are preserved. Google Cloud monthly invoice/zero-dollar Cost Table evidence remains blocked on owner account access. See `docs/GOOGLE_CLOUD_SUBMISSION_EVIDENCE.md`.

## Known Limitations

- Development C2PA certificate, not an official production Trust List identity.
- Single-asset forensic modification detection without trusted provenance is not implemented.
- No persistent cloud registry yet.
- No external users or revenue yet.
- Real-user evidence and owner-confirmed financial disclosures remain mandatory blockers.
- Eligibility attestation, Google billing evidence, IP/video attestations, real-user evidence, financial confirmation, and Final Submission remain owner-controlled blockers.
