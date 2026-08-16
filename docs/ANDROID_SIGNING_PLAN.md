# Android Signing Plan

1. Use Google Play App Signing for the Play-distributed app, enabled by the owner in Play Console.
2. Create a separate upload key in an owner-controlled secure location. Never store the keystore, passwords, private key, or recovery material in Git, chat, screenshots, CI logs, or public cloud storage.
3. Keep debug signing local and separate from release/upload signing.
4. After Play App Signing is enabled, copy only the public SHA-256 signing certificate fingerprint into `/.well-known/assetlinks.json` with package `com.gugupro.aievidence`.
5. Verify Digital Asset Links before claiming fullscreen TWA. A mismatch produces a Custom Tab, not a verified TWA.
6. Record key ownership/recovery instructions privately. Do not publish them in this repository.

Current status: no release key created; no signing secret exists in the repository; Play App Signing owner confirmation is BLOCKED by design.
