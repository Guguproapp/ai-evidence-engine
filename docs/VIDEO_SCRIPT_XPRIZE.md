# Build with Gemini XPRIZE — Demo Video Script

Target duration: **2:35**. Hard limit: **under 3:00**. Language: English narration or complete English subtitles. No unlicensed music.

## 00:00–00:18 — Problem

> AI-edited product media is everywhere. But a buyer usually cannot tell where an image came from, who changed it, what changed, or whether its history was tampered with.

Show the public AI Evidence Engine homepage.

## 00:18–00:42 — Try Demo

Click `Try the 60-second demo`.

> AI Evidence Engine does not guess an AI percentage. It verifies recorded evidence: the content hash, digital signature, C2PA manifests, registry record, and parent-child version chain.

## 00:42–01:05 — Modification Mask

Click `Change overlay` and `Mask`.

> The mask is calculated from the real pixel differences between versions. Here, 4.8 percent of the image changed around the product label. This measures the changed region; it is not a copyright percentage.

## 01:05–01:30 — Version History and C2PA

Click Versions 1, 2, and 3. Open Advanced details.

> Each substantive edit creates a child version instead of overwriting history. Every version has its own event ID, parent, hash, signature, and embedded C2PA provenance.

## 01:30–01:48 — Tamper Detection

Upload the prepared tampered image.

> When the signed image bytes are changed, the verifier reports Invalid Signature and a C2PA data-hash mismatch.

## 01:48–02:08 — Gemini Evidence Explainer

Show the deployed Evidence Explainer after Cloud Run integration is complete.

> Gemini turns the structured verification facts into a short explanation for a buyer. Gemini never decides Authentic, Modified, Unknown, or Invalid. Cryptographic evidence remains the source of truth.

Do not record this section until the Cloud Run endpoint has made a real Gemini production call.

## 02:08–02:28 — ProofCart

Click ProofCart `Verify Evidence`.

> ProofCart is the Small Business Services use case. Merchants can attach verifiable media history, while buyers can inspect the source and edits before trusting a listing.

## 02:28–02:35 — Close

> AI Evidence Engine records what happened. It does not make copyright or legal verdicts. Evidence, not guesswork.

## Publication checklist

- Final runtime is less than 3:00.
- Actual product operation is visible.
- English audio or complete English subtitles are present.
- No copyrighted music or unauthorized third-party material.
- Uploaded to public YouTube, Vimeo, or Youku.
- Public URL tested while signed out.

