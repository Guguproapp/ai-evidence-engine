# Android App Audit

Date: 2026-08-16

## Decision

Selected architecture: **Trusted Web Activity (TWA) over the production PWA**, using Google's Android Browser Helper 2.7.2.

Why: the verified product already runs in the browser, its C2PA SDK is browser/WASM based, and its SHA-256 verification uses Web Crypto. TWA reuses the tested UI and Evidence Decision Engine and avoids maintaining a second security-sensitive verifier. Capacitor would introduce a WebView-specific runtime and plugin surface; a native shell would duplicate the product and is not proportionate for V1.

This is not a WebView. A verified TWA runs in a supported Android browser. Until Digital Asset Links matches the final Play signing certificate, it falls back to a Custom Tab with browser UI.

## Existing-state audit

| Item | Before this task | Current status |
|---|---|---|
| Android project | None | TWA API 36 project created and built in `apps/android-twa` |
| Capacitor | Not installed | Not selected |
| Native Android shell | None | Not selected |
| PWA manifest | None | Implemented at `/manifest.webmanifest` |
| Digital Asset Links | None | BLOCKED until final Play App Signing SHA-256 fingerprint |
| JDK / Android SDK | Initial shell check missed existing tools | PASS: Android Studio JBR 17, SDK 36, Build Tools 36.0.0 |
| APK | None | PASS: Debug APK built, signature verified, installed on Android 16 emulator |
| AAB | None | PASS build / BLOCKED submission: release AAB built but intentionally unsigned until owner-controlled upload key and Play App Signing |

## Runtime capability assessment

| Capability | Expected TWA behavior | Evidence / remaining test |
|---|---|---|
| C2PA WASM | Uses Chrome-compatible WebAssembly and existing dynamic import | Web production passes; Android runtime BLOCKED by first-run Chrome Terms screen |
| File picker | HTML file input invokes Android system picker; no broad storage permission | Android runtime BLOCKED by first-run Chrome Terms screen |
| `crypto.subtle` | Available in the secure HTTPS browser context | Web source/build verified; Android physical-device test NOT RUN |
| Cloud Run | HTTPS request to production explainer | Existing production endpoint; Android runtime BLOCKED by Chrome onboarding |
| Gemini | Only allowlisted structured facts are sent on user action | Existing web integration; Android runtime BLOCKED by Chrome onboarding |
| Local verification | SHA-256 and C2PA parsing remain on device in the browser process | Source audit PASS; Android runtime BLOCKED by Chrome onboarding |
| Original image upload | No `FormData` or file upload path exists | Code audit PASS |

## Options evaluated

1. **TWA / PWA — selected.** Lowest rework, Chrome-secure-context compatibility, shared web UI and core.
2. **Capacitor — not selected.** Would require WebView-specific C2PA/WASM/file-picker regression work and additional native dependency maintenance.
3. **Native shell — not selected.** Highest duplication and would risk diverging from the proven verifier.

Official references:

- https://developer.chrome.com/docs/android/trusted-web-activity/
- https://github.com/GoogleChrome/android-browser-helper
- https://developer.android.com/about/versions/16/setup-sdk

## Gate before Play upload

The debug package builds and launches without an AEE crash after adding the required `ManageDataLauncherActivity`. The clean Android 16 emulator then stops at Chrome's first-run Terms screen. Codex did not click through or accept those terms. The owner must complete Chrome onboarding before the web runtime, file picker, C2PA, Gemini, rotation, and back-button matrix can be executed.

After runtime testing, create an owner-controlled upload key, enable Play App Signing, obtain the Play signing SHA-256 certificate fingerprint, publish `/.well-known/assetlinks.json`, and verify fullscreen TWA. No release upload is authorized by this document.

Local artifacts (ignored by Git):

- Debug APK: `apps/android-twa/app/build/outputs/apk/debug/app-debug.apk`, SHA-256 `5431081dd8f8418718923346ca3184c275b0c13a7f8eadcd40b0ac22f7cd0873`
- Unsigned release AAB: `apps/android-twa/app/build/outputs/bundle/release/app-release.aab`, SHA-256 `5f68b21797cbfc866a4ab9003b6acd4f1a2a5c3af19013d5cd126f201d984800`
