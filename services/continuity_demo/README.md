# AEE Evidence Continuity Demo — Development/Test

This service is a controlled UI and backend orchestrator for the single built-in
synthetic ProofCart Version 3 asset. It creates a real `aee.event.v1` through the
existing AEE Registry, verifies its signature, invokes the IAM-protected Remote
Black Box service-to-service, retrieves the Google Cloud Object, reverifies
SHA-256, and verifies the unchanged local Signed Event again.

It does not accept user uploads, arbitrary object paths, bucket selection,
retention controls, credentials, or private evidence. It is not the Production
Black Box and does not expose Google identity tokens to the browser.

Environment variables:

- `REMOTE_BLACKBOX_URL`
- `REMOTE_BLACKBOX_AUDIENCE`
- optional `DEMO_EVIDENCE_PATH`
