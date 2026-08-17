# Legacy Bridge restart recovery evidence

Captured: 2026-08-17 (Asia/Taipei)

Environment: Development / Test only

- Google Cloud project: `ai-evidence-engine-gugupro`
- Evidence bucket: `aee-blackbox-test-856572888721`
- Remote Black Box revision: `aee-blackbox-test-00003-nxw`
- Continuity revision before forced restart: `aee-continuity-demo-00006-dtv`
- Continuity revision after forced restart: `aee-continuity-demo-00007-hgm`

## V1 First-Seen

- Input: `apps/web/public/demo/version-1.png` (synthetic public demo asset)
- Registration: `FIRST_SEEN_SEALED`
- Prior provenance: `unknown`
- Passport ID: `c8ed52a2-8702-4464-85f7-76a5faf8fb5e`
- Event ID: `f6c30202-0586-4b62-afcf-3a2a65781fd3`
- Content SHA-256: `082cc812bb1720f7335e41da823706dc022aae1ded0daa1dfbc20b93717e0fee`
- Object generation: `1786972746892094`
- Retention expiration: `2026-08-17T13:29:06.897000+00:00`
- Retrieval hash match: `true`

## Forced state loss and recovery

The Continuity service was forced onto a new Cloud Run revision after V1. The
new revision had no access to the prior revision's `/tmp` bridge cache. Recovery
used only the Passport ID and anchor Event ID to list the deterministic GCS
Passport prefix, validate the stored Signed Event and public key, download V1,
and reverify its SHA-256.

- Recovery result: `PASS`
- Recovered from persistent evidence: `true`
- Recovered history count: `1`
- Recovered V1 Signature: `valid`
- Recovered V1 Event Hash: `valid`
- Recovered V1 provenance: `UNVERIFIED` (prior history remains unknown)

## V2 after restart

- Input: `apps/web/public/demo/version-2.png` (synthetic public demo asset)
- Passport ID: `c8ed52a2-8702-4464-85f7-76a5faf8fb5e`
- Event ID: `8c4fda36-1ddb-4a72-935b-4dddac0cde74`
- Parent Event: `f6c30202-0586-4b62-afcf-3a2a65781fd3`
- Content SHA-256: `02cb6fa502538e12a6f7dec66db75638d32efefe5a60ac2ed5848abc56783954`
- Object generation: `1786972782253862`
- Retention expiration: `2026-08-17T13:29:42.258000+00:00`
- Retrieval hash match: `true`
- Persistent history count: `2`
- Spatial change ratio: `0.574832`
- Bounding box: `x=0, y=0, width=720, height=400`
- Evidence Continuity: `PASS`

No credential, access token, private key, private source asset, or private user
data is included in this record.
