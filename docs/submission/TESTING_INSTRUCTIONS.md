# Testing Instructions

Status: **READY**

No login or payment is required.

1. Open https://ai-evidence-engine-gugupro.artistuncle.chatgpt.site.
2. Select `EN` in the header.
3. Use the built-in demo or upload the provided signed Version 3 image.
4. Review the provenance result, signed version history, and 4.8% measured pixel change.
5. Switch between the current image, change overlay, and modification mask.
6. Open the version history and inspect the parent/child sequence.
7. Upload an image without trusted provenance. Confirm that AEE returns `Unverified` and does not guess whether it is real, fake, edited, or AI-generated.
8. Select `Start a verified history from now`. Confirm that the UI says prior history is unknown and creates a First-Seen point rather than claiming originality.
9. Add the provided recorded V2 example. Confirm the same Passport, new child Event, parent link, measured known-version change, and V1 → V2 history.
10. Select `Explain with Gemini`. Gemini explains allowlisted facts but does not alter the deterministic result.

Development/Test Evidence Black Box prototype: https://aee-continuity-demo-856572888721.asia-east1.run.app

This second URL uses short test retention and synthetic/public test evidence. It is not a permanent or court-certified production vault. It demonstrates sealing, object generation, retention metadata, retrieval, SHA-256 reverification, and Evidence Continuity.
