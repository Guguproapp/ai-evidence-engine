# Google Play Store Listing — English

## App name

AI Evidence Engine

## Short description (within 80 characters)

Verify image provenance, history, C2PA and signed evidence.

## Full description (within 4,000 characters)

Verify recorded provenance and changes between trusted versions.

AI Evidence Engine is an evidence verifier for digital-content provenance and modification history. Version 1 supports images. It combines content hashes, digital signatures, C2PA, Registry records, and version chains to show whether a file matches a registered original or modified version and whether its evidence has been altered.

Current features:

• Image verification for PNG, JPEG, and WebP, with on-device SHA-256 hashing and C2PA parsing.
• Evidence Passport details including Passport ID, version, issuer, tool, model, recorded AI involvement level, and Evidence Event.
• Version History showing parent relationships and the recorded changes across Version 1, Version 2, and Version 3.
• Modification Mask, Change Overlay, and measured pixel-change percentage between trusted recorded versions.
• Separate trust signals for C2PA, integrity, digital signature, Registry matching, and identity trust.
• Four provenance states: Verified Original, Verified Modified, Unverified, and Invalid Evidence.
• Gemini Evidence Explanation, which explains already-verified structured facts in plain language. Gemini cannot determine or change the verification state.
• Traditional Chinese and English interfaces.

Important boundary:

The product verifies recorded provenance, evidence integrity, signatures, C2PA, and Registry records. It measures changes only when trusted recorded versions are available. An unfamiliar image without trusted provenance returns Unverified; the app does not infer whether it is real, fake, edited, or AI-generated from appearance. A change percentage is measured pixel change, not AI probability, a fake score, or a copyright percentage. The product does not establish real-world truth or issue legal conclusions about copyright, infringement, plagiarism, or legality.

Image handling:

The current public Verifier processes selected images on device and does not send the original image to Gemini. Only when you request a Gemini explanation are allowlisted structured verification facts sent to the explanation service.

Not currently supported: video, audio, documents, 2D design, 3D models, manufacturing history, a complete Private Black Box, or mobile authorization. These are future plans, not Version 1 features.

AI Evidence Engine by GUGUPRO

## Suggested category

Tools or Productivity; owner confirmation required in the current Play Console options.

## Owner input required

- Developer name: GUGUPRO (OWNER CONFIRMATION REQUIRED)
- Support email: OWNER INPUT REQUIRED
- Developer email: OWNER INPUT REQUIRED
- Support URL: OWNER INPUT REQUIRED
- Privacy policy URL: `https://ai-evidence-engine-gugupro.artistuncle.chatgpt.site/privacy`
- Website: `https://ai-evidence-engine-gugupro.artistuncle.chatgpt.site`
- Default language: Traditional Chinese (zh-TW), with English localization
- Country/region availability: OWNER INPUT REQUIRED
