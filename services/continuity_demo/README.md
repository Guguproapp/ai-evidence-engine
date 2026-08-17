# AEE Evidence Continuity Demo — Development/Test

This service is a controlled UI and backend orchestrator. The original
continuity path uses the single built-in synthetic ProofCart Version 3 asset.
The explicit opt-in Legacy Content Bridge accepts PNG/JPEG/WebP test images
under 10 MB and creates a First-Seen history start whose prior provenance
remains unknown. Both paths create a real `aee.event.v1` through the existing
AEE Registry, verify its signature, invoke the IAM-protected Remote Black Box
service-to-service, retrieve the Google Cloud Object, reverify SHA-256, and
verify the unchanged local Signed Event again.

It never accepts arbitrary object paths, bucket selection, retention controls,
credentials, or browser-provided Signed Events. The Legacy Bridge accepts an
image only after an explicit user action and creates the Signed Event on the
AEE backend. It is not the Production Black Box and does not expose Google
identity tokens to the browser.

Environment variables:

- `REMOTE_BLACKBOX_URL`
- `REMOTE_BLACKBOX_AUDIENCE`
- optional `DEMO_EVIDENCE_PATH`
- optional `LEGACY_BRIDGE_ROOT`
- optional comma-separated `LEGACY_BRIDGE_ALLOWED_ORIGINS`

Endpoints:

- `POST /v1/demo/continuity` — bundled synthetic asset only.
- `POST /v1/demo/first-seen` — explicit multipart image First-Seen seal.
- `POST /v1/demo/first-seen/version` — child version for an existing bridge;
  when the local cache is gone, Passport and anchor Event locators trigger
  reconstruction from persistent Evidence.
- `POST /v1/demo/first-seen/recover` — reconstruct a local cache from the
  sealed Signed Events and evidence stored in the Development/Test bucket.

Cloud Run local storage is only a temporary cache. The persistent source for
the bounded V1-to-V2 history is the sealed Google Cloud Storage Evidence Object:
its unchanged Signed Event, public verification key, Passport/Event/Parent
identifiers, and content SHA-256 are used to rebuild and verify the chain after
a restart. This remains a Development/Test Black Box, not a claim of permanent
or judicial storage.
