# Android Closed Test Plan

## Applicability

UNKNOWN until the owner confirms Play Console account type and creation date. If Personal and created after 2023-11-13, the minimum is 12 opted-in testers continuously for at least 14 days. Plan for 15–20 invited testers to keep a safety margin.

## Setup

- Testers need Google accounts.
- Use a Play Console closed-testing track after the AAB, listing, privacy, Data Safety, and App Content setup are complete.
- Record opt-in start/end dates; do not remove the track or testers before the continuous period completes.
- Tell testers that this is an Android product test. Separate consent is required before reusing feedback as XPRIZE user evidence.

## Test matrix

1. Install, update, launch, and cold start.
2. Default Traditional Chinese, switch to English, reload, and confirm saved choice.
3. Select PNG, JPEG, and WebP with the system picker.
4. Verify registered original, registered modified, unsigned/unregistered, and tampered evidence.
5. View modification mask, overlay, measured pixel change, Evidence Passport, History, C2PA, signature, Registry, and identity trust.
6. Request Gemini explanation and confirm it cannot change deterministic status.
7. Disconnect network and confirm local UI/failure messages remain understandable.
8. Simulate Cloud Run failure and confirm cryptographic result remains usable.
9. Test back button, rotation, common phone viewports, memory pressure, and Android 16.
10. Record crashes, performance issues, task completion, and exact feedback.

## Evidence template

| Date | Anonymous tester ID | Device / Android | Functions completed | Result | Original feedback | Permission to quote |
|---|---|---|---|---|---|---|

Do not fabricate testers, dates, opt-ins, feedback, or Production access.
