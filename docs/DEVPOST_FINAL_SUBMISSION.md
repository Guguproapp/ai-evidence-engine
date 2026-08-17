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

AI Evidence Engine helps creators and small businesses preserve a verifiable evidence history around valuable digital work—from the first recorded point onward.

## What it does

Small creators and small businesses often have files, but not dedicated provenance and evidence-preservation infrastructure. AI Evidence Engine helps preserve provenance, signed version history, measured changes, and tamper-resistant evidence records around their work.

When trusted provenance exists, AEE verifies it. When prior provenance is unavailable, AEE does not invent historical truth: the public First-Seen flow records and seals the exact content from a clearly identified first recorded point. Later versions create new signed child Events, preserving V1 → V2 history without overwriting the past.

AEE combines content hashes, digital signatures, C2PA manifests, an append-only parent-child event chain, known-version change metrics, and evidence continuity. The public verifier presents `Verified Original`, `Verified Modified`, `Unverified`, or `Invalid Evidence` without claiming world truth, authorship, copyright ownership, or a legal verdict.

Capability boundary: Level 1 Provenance Verification is implemented. Level 2 Known-Version Modification Comparison is implemented when trusted recorded versions exist. Level 3 Single-Asset Forensic Modification Detection is not implemented. An unfamiliar image without trusted provenance returns `Unverified`; AEE does not infer whether it is real, fake, edited, or AI-generated from appearance.

ProofCart is the first Small Business Services use case. For a listing photo with recorded provenance, a buyer can inspect its recorded versions, edit history, changed region, C2PA provenance, and signed evidence before deciding how to use the media.

## How we built it

- Official `c2patool 0.27.12` creates, embeds, reads, and verifies C2PA manifests.
- Official `@contentauth/c2pa-web 0.13.4` verifies image provenance in the browser.
- RSA-2048/SHA-256 signs canonical evidence events.
- An append-only event chain preserves version and parent-hash relationships.
- A deterministic RGB image-diff algorithm compares trusted recorded versions and generates the Modification Mask, ratio, and bounding box.
- AEE Evidence Identification & Coding Standard v1.0 separates integrity, provenance, identity trust, signed AI involvement, and change scope; `aee.event.v1` and legacy compatibility are covered by automated tests.
- The verifier processes uploaded images locally in the browser and has no image-upload endpoint.
- A bounded Cloud Run Evidence Explainer calls Gemini on Vertex AI only after cryptographic verification; Gemini cannot assign or change the deterministic provenance state.
- The public Legacy Content Bridge establishes a First-Seen evidence point for content whose earlier provenance is unknown, then persists and reconstructs its signed V1 → V2 history from sealed evidence rather than Cloud Run memory.
- A Development/Test Evidence Black Box prototype uses Google Cloud Storage generation preconditions and short test retention to seal, retrieve, and reverify evidence continuity.

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

## Creator Rights Evidence Use Case

AEE is not a copyright registry and does not prove authorship. It helps photographers, designers, illustrators, writers, content creators, agencies, and brand teams preserve creation and version records that may form one part of the evidence they later choose to present when protecting their interests.

## Business Model

Potential model: a free creator entry tier, paid evidence storage/export plans, and usage-based verification APIs for small businesses, agencies, marketplaces, and platforms. No paid customer or enterprise partnership is currently claimed.

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
- Public First-Seen registration with explicit `Prior History Unknown`, signed Passport/Event creation, persistent V1 → V2 history, and measured known-version changes.
- Development/Test Google Cloud evidence sealing, short retention, retrieval, SHA-256 reverification, delete rejection, overwrite rejection, and evidence continuity.
- Implemented `aee.text.v1` and `aee.image.c2pa.v1` Evidence Profiles, with audio/video/document/2D/3D/manufacturing explicitly marked `SPECIFIED_NOT_IMPLEMENTED`.
- Formal L0–L5 AI involvement, multimodal adapter metrics, and owner-controlled Private Black Box / Mobile Authorization architecture without representing the next-stage features as complete.

## What we learned

Provenance should report evidence rather than make legal verdicts. Recorded version events can support contribution and modification history; an AI detector probability cannot reconstruct missing provenance with certainty.

## What's next

- Obtain external user feedback with informed disclosure.
- Replace the demo registry bundle with a persistent production registry.
- Obtain a production C2PA signing certificate and protect the key with KMS/HSM after submission readiness.
- Evolve the Development/Test Evidence Black Box prototype into an owner-controlled production service with reviewed retention, privacy, authorization, and cost policies after the hackathon submission.
- Research Soft Binding recovery, invisible watermarking, and additional audio/video/CAD/3D evidence profiles without representing them as current capabilities.

## Testing Instructions

1. Open the public demo without signing in.
2. Upload the signed Version 3 fixture or use the built-in demo; confirm `Verified Modified`, the signed version history, and the 4.8% measured change mask.
3. Upload an image without trusted provenance; confirm `Unverified` and that AEE does not guess whether it is real, fake, edited, or AI-generated.
4. Choose `Start a verified history from now`; confirm the First-Seen notice says prior history remains unknown.
5. Add the recorded V2 fixture; confirm the same Passport, a new child Event, parent linkage, history, and measured known-version change.
6. Click `Explain with Gemini`; confirm that Gemini explains allowlisted facts while the deterministic status remains unchanged.
7. Open the clearly labelled `Development / Test Evidence Black Box Prototype`; run Seal and Retrieve, then inspect retention metadata, SHA-256 Match, and Evidence Continuity.

No login or payment is required for the public verifier.

The Entrant must keep the public verifier, Cloud Run explainer, repository, and judge-accessible video operational without payment through the official judging period ending 2026-09-15 17:00 PDT and any announced verification window.

## Public Demo URL

https://ai-evidence-engine-gugupro.artistuncle.chatgpt.site

## Cloud Production URL

https://ai-evidence-explainer-856572888721.asia-east1.run.app

## Repository URL

https://github.com/Guguproapp/ai-evidence-engine

## Video URL

Private review URL: https://youtu.be/LJh42-gYD4U

Public judge-accessible URL: `PENDING OWNER REVIEW AND PUBLICATION`

Final local candidate: `docs/evidence/AI-Evidence-Engine-XPRIZE-Final-2026-08-18.mp4`.

Duration: 2:28.000. Resolution: 1920×1080 at 30fps. Audio: English 48 kHz mono AAC narration. Subtitles: embedded English subtitle track. No music or cloned human voice.

The visuals show real Production interaction and the real Development/Test prototype. They include signed provenance, measured known-version change, an unknown image returning `Unverified`, First-Seen with prior history unknown, V1 → V2, Gemini's bounded explanation, Google Cloud retention metadata, real delete rejection (HTTP 403), real overwrite rejection (HTTP 412), retrieval, SHA-256 Match, and Evidence Continuity. The older `pqRNOvyE3_c`, `Fwu7yGUTVwo`, and `HDG1qYo5hUg` videos are superseded and must not be submitted.

The final candidate is uploaded as a private YouTube video pending Entrant review. It must not be made judge-accessible until Tsing-YI Chen approves the exact video and confirms the IP declarations.

## Production Evidence

See `docs/PRODUCTION_EVIDENCE.md`. Sanitized Cloud Run, Vertex AI, and public
verifier request evidence has been preserved without credentials.

Sanitized Gemini Observability and Cloud Run screenshots are preserved. Google Cloud monthly invoice/zero-dollar Cost Table evidence remains blocked on owner account access. See `docs/GOOGLE_CLOUD_SUBMISSION_EVIDENCE.md`.

## Known Limitations

- Development C2PA certificate, not an official production Trust List identity.
- Single-asset forensic modification detection without trusted provenance is not implemented.
- First-Seen proves only that AEE received, fingerprinted, signed, and sealed that exact version at the recorded time. It does not prove originality, authorship, copyright ownership, or history before that point.
- The Google Cloud Evidence Black Box is a Development/Test prototype with short test retention, not a permanent or court-certified production vault.
- No external users or revenue yet.
- Real-user evidence and owner-confirmed financial disclosures remain mandatory blockers.
- Eligibility attestation, Google billing evidence, IP/video attestations, real-user evidence, financial confirmation, and Final Submission remain owner-controlled blockers.
