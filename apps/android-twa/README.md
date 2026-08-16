# AI Evidence Engine Android TWA

This is a minimal Android wrapper around the production Progressive Web App. It reuses the tested web UI and device-side C2PA/SHA-256 verification instead of duplicating the Evidence Engine.

Status: source foundation created; APK/AAB build requires JDK 17, Android SDK Platform 36, Build Tools 36.x, Gradle 8.11.1, and acceptance of the applicable Android SDK licenses by the account owner.

The package `com.gugupro.aievidence` is provisional until it is reserved in Play Console. Do not upload an AAB before owner confirmation because a published package identifier cannot be reused or casually changed.

Digital Asset Links are intentionally not published yet. The final SHA-256 fingerprint depends on the Google Play App Signing certificate selected by the owner.
