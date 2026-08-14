# Devpost Submission Draft｜AI Evidence Engine

> Superseded for the current competition. Use [DEVPOST_FINAL_SUBMISSION.md](DEVPOST_FINAL_SUBMISSION.md) for Build with Gemini XPRIZE.

這是可編輯草稿，不代表已接受 Devpost 規則，也沒有執行最終 Submission。

## Project name

AI Evidence Engine

## Team

gugupro

## Elevator pitch

AI Evidence Engine gives digital content a verifiable history: where it came from, who or what changed it, exactly what changed, and whether the evidence was tampered with.

## What it does

AI Evidence Engine is a local-first provenance and evidence platform. It embeds official C2PA manifests in image versions, links each version to a signed append-only evidence event, calculates explainable modification masks, and presents the result in a verifier that non-technical users can understand.

The verifier answers five practical questions:

1. Is verifiable evidence present?
2. Where did this image come from?
3. Which agent or tool changed it?
4. Which pixels changed?
5. Do the image, signature, C2PA manifest, and registry record still agree?

ProofCart is the first vertical demo. A buyer can inspect a seller's product photo and verify its original version, edit history, changed region, C2PA chain, and signed registry evidence.

## How we built it

- Official `c2patool 0.27.12` creates, embeds, reads, and verifies the C2PA manifests.
- Official `@contentauth/c2pa-web 0.13.4` verifies uploaded images in the browser.
- Each substantive edit creates a child version with a parent relationship; previous versions are not overwritten.
- The existing AI Evidence Engine Registry signs canonical event records with RSA-2048/SHA-256.
- A deterministic RGB image-diff algorithm generates the Modification Mask, changed-pixel ratio, and bounding box.
- The public verifier runs on an HTTPS Sites deployment. Image verification is local to the browser and has no server upload endpoint.

## Challenges we ran into

The hardest boundary was separating content integrity from issuer trust. A C2PA manifest can be cryptographically intact while its development certificate is not on the official Trust List. The verifier therefore says `Integrity verified; development identity` instead of presenting a development signer as a production-trusted identity.

We also had to preserve exact signed image bytes. Image optimization or transcoding can remove or invalidate embedded provenance, so the verifier serves signed demo assets directly and validates their hashes.

## Accomplishments

- Three real signed image versions with nested C2PA parent ingredients.
- Shared Event IDs between C2PA assertions and the signed Registry.
- Modification Masks generated from actual pixel changes.
- Browser results for `Modified`, `Unknown`, and `Invalid Signature`.
- Tampered-image test that produces `assertion.dataHash.mismatch`.
- One-click ProofCart demo that a judge can understand in under three minutes.
- 15/15 Python tests and 3/3 website tests passing.

## What we learned

Provenance should report evidence, not make legal or authorship verdicts. It is also important to distinguish an AI content detector's probability from a recorded version history. Recorded events can show contribution and modification; a detector cannot recreate missing provenance with certainty.

## What's next

- Obtain a production C2PA signing certificate and protect its private key with KMS/HSM.
- Add minimal authorization for sensitive Evidence Wallet records.
- Replace the demo registry bundle with a persistent production registry.
- Package the same verifier capability for ecommerce platforms through ProofCart.

## Public demo

https://ai-evidence-engine-gugupro.artistuncle.chatgpt.site

## Truth boundary before submission

- Do not claim that the development signer is on the official C2PA Trust List.
- Do not claim Google SynthID or an OpenAI Verify API is integrated.
- Do not claim a sponsor API challenge until that API is actually integrated and tested.
- Do not describe `Unknown` as proof that content is fake.
- Repository: https://github.com/Guguproapp/ai-evidence-engine
- Final public video: https://youtu.be/HDG1qYo5hUg
