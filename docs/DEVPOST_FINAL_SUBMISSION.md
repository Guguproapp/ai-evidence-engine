# Devpost Final Submission — AI Evidence Engine

Status: **DRAFT — NOT SUBMISSION READY**

## Project Name

AI Evidence Engine

## Category

Small Business Services

## Elevator Pitch

AI Evidence Engine is a Universal Evidence Passport for Digital & Physical Creation: it records where a creation came from, who or what changed it, how much changed, and whether the evidence history was tampered with.

## What it does

AI Evidence Engine helps merchants, platforms, and consumers verify provenance without guessing whether AI made something. It combines content hashes, digital signatures, C2PA manifests, an append-only parent-child event chain, and modality-specific change metrics. Image is the first working adapter; text, video, audio, documents, 2D design, 3D models, and manufacturing share the Passport, Registry, and Private Wallet architecture. The public verifier presents `Verified Original`, `Verified Modified`, `Unverified`, or `Invalid Evidence` without claiming world truth or a legal verdict.

ProofCart is the first Small Business Services use case. A buyer can inspect a listing photo's original version, edit history, changed region, C2PA provenance, and signed registry evidence before deciding whether to trust the media.

## How we built it

- Official `c2patool 0.27.12` creates, embeds, reads, and verifies C2PA manifests.
- Official `@contentauth/c2pa-web 0.13.4` verifies image provenance in the browser.
- RSA-2048/SHA-256 signs canonical evidence events.
- An append-only event chain preserves version and parent-hash relationships.
- A deterministic RGB image-diff algorithm generates the Modification Mask, ratio, and bounding box.
- The verifier processes uploaded images locally in the browser and has no image-upload endpoint.
- A bounded Cloud Run Evidence Explainer calls Gemini on Vertex AI only after cryptographic verification; Gemini cannot assign or change the deterministic provenance state.

## AI-Native Operations

The evidence decision pipeline is deterministic. Hash, signature, C2PA, registry, and parent-chain validation determine the verification state. Gemini is restricted to explaining the supplied structured facts to a non-technical buyer; it cannot replace or reinterpret the verification state.

Current qualification status: the deployed Cloud Run service made a logged Vertex AI Gemini production call while preserving the deterministic verification result.

## Google Cloud Usage

Production product: Google Cloud Run, hosting the Evidence Explainer API in the dedicated project `ai-evidence-engine-gugupro`.

Authentication design: Cloud Run service-account Application Default Credentials. No Gemini API key is shipped to the browser or repository.

Current status: PASS. Revision `ai-evidence-explainer-00002-z76` is ready in `asia-east1` and serves 100% of traffic at the public Cloud Run URL.

## Gemini Usage

Planned API: Gemini API on Vertex AI using the official Google Gen AI SDK.

Input: allowlisted structured verification facts after the deterministic verifier has completed.

Output: a two-sentence buyer-facing explanation. The deterministic status is returned unchanged alongside the explanation.

Current status: PASS. Cloud Run revision `ai-evidence-explainer-00003-m75` made a real `gemini-2.5-flash` Vertex AI call for rebuilt Evidence ID `1c3d4a0f-9e2a-4a18-a83f-0c982db4ef33`, returned HTTP 200, and preserved `Verified Modified`. Sites Version 4 then reproduced the same result from the public verifier. Sanitized evidence is preserved under `docs/evidence/`.

## C2PA

The three-version ProofCart image chain contains real embedded C2PA manifests and parent ingredients. Original C2PA reports are preserved. The bytes and claims validate, while the current demo signing certificate is a development identity and is not represented as a production-trusted C2PA Trust List identity.

## ProofCart Use Case

ProofCart demonstrates how a small merchant can attach evidence to a product image and how a buyer can verify the image's origin, two edits, changed region, signatures, C2PA chain, and registry record.

## Business Model

Potential model: verification and provenance infrastructure sold to merchants and platforms through usage-based API plans and ProofCart verification features. No paid customer or enterprise partnership is currently claimed.

## Users

Verified external users: 0. Internal developer and automated browser tests are not counted. Real external testing remains required.

## Revenue

Total Revenue: $0.00 USD.

Monthly revenue: May $0.00; June $0.00; July $0.00; August $0.00 as of 2026-08-14.

Related-Party Revenue: $0.00.

## Expenses

Total documented expenses: $0.00 pending Entrant confirmation against all billing records.

Marketing Spend: $0.00. Customer Acquisition Spend: $0.00.

## Challenges

The central technical challenge was separating content integrity from issuer trust. A C2PA claim can be cryptographically intact while the development certificate is not on the official Trust List. The interface therefore states `Integrity verified; development identity` instead of overstating production trust.

The Gemini boundary presents a second challenge: a helpful explanation must never become an ungrounded provenance verdict. The service validates a deterministic status, forwards only allowlisted facts, and returns that status unchanged.

## Accomplishments

- Three signed image versions with nested C2PA parent ingredients.
- Shared Event IDs between C2PA assertions and the signed Registry.
- Actual pixel-derived Modification Masks.
- Working local `Verified Original`, `Verified Modified`, `Unverified`, and `Invalid Evidence` classification flows.
- Public one-click ProofCart demo.
- 20/20 Python tests and 9/9 website tests at the current local checkpoint.
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

## Public Demo URL

https://ai-evidence-engine-gugupro.artistuncle.chatgpt.site

## Cloud Production URL

https://ai-evidence-explainer-856572888721.asia-east1.run.app

## Repository URL

https://github.com/Guguproapp/ai-evidence-engine

## Video URL

https://youtu.be/HDG1qYo5hUg

The accepted replacement is 2:43, 1920×1080, and uses real Production
interaction with burned-in English captions. It shows signed Version 3 upload,
all three image views, version history, a real tampered upload,
`assertion.dataHash.mismatch`, Gemini explanation, ProofCart, the universal
adapter architecture, and the explicitly labelled next stage. The superseded
`Fwu7yGUTVwo` video must not be submitted.

## Production Evidence

See `docs/PRODUCTION_EVIDENCE.md`. Sanitized Cloud Run, Vertex AI, and public
verifier request evidence has been preserved without credentials.

## Known Limitations

- Development C2PA certificate, not an official production Trust List identity.
- No persistent cloud registry yet.
- No external users or revenue yet.
- Real-user evidence and owner-confirmed financial disclosures remain mandatory blockers.
