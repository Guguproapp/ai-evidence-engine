# Google Play Asset Checklist

Official reference: https://support.google.com/googleplay/android-developer/answer/9866151

| Asset | Requirement | Current artifact / status |
|---|---|---|
| App icon | 512×512, 32-bit PNG, max 1 MB | PASS — `apps/web/public/app-icon-512.png`, 512×512 RGBA, about 12 KB |
| PWA icon | 192×192 PNG | PASS — `apps/web/public/app-icon-192.png` |
| Feature graphic | 1024×500 JPEG or 24-bit PNG without alpha | PASS — `apps/web/public/google-play-feature-graphic-1024x500.jpg`, uses a real Version 3 comparison asset |
| Phone screenshots | Real Android UI only | NOT RUN — Android build/device test not yet available; no fake screenshots created |
| Promo video | Optional | Existing product video is not automatically approved as Play Store media |

## Required real screenshot shot list

Capture these from a built Android app on a representative phone viewport after Digital Asset Links and device testing pass:

1. Traditional Chinese home.
2. Android system file picker returning to the app.
3. 已驗證修改版本 / Verified Modified result.
4. Modification Mask and measured pixel change.
5. Evidence Passport.
6. Version History.
7. Trust section with C2PA, signature, Registry, and development identity boundary.
8. Gemini Evidence Explanation.

Do not use browser mockups, fabricated status, or screenshots that differ from the submitted AAB.
