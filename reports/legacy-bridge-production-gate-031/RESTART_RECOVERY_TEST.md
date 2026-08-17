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

## Physical iPhone Production validation

Device/UI path: physical iPhone 15, Mobile Safari, native iOS file picker, and
the public Production website at
`https://ai-evidence-engine-gugupro.artistuncle.chatgpt.site`.

The input is a public synthetic test screenshot and contains no private user
content. Its history before the First-Seen record remains unknown; neither the
UI nor the Signed Event identifies it as an original work, authorship proof, or
copyright proof.

### Measurable V1 First-Seen

- Input: `02-unknown-source.jpg`
- Registration: `FIRST_SEEN_SEALED`
- Prior provenance: `unknown`
- Passport ID: `bb05ef66-cc40-426c-bd97-38ce5835861f`
- Event ID: `ae1ab53e-d7ca-4be2-a939-d75ad39b51d0`
- Content SHA-256: `80ce890c25b61b55dc680dde1b2960a2f14a4d9e35ddcc53b0d7a11b2920fa88`
- Object generation: `1786973948953645`
- Retention expiration: `2026-08-17T13:49:08+0000`
- Retrieved SHA-256: `80ce890c25b61b55dc680dde1b2960a2f14a4d9e35ddcc53b0d7a11b2920fa88`
- Retrieval hash match: `true`

### Measurable V2

- Input: `08-unknown-source-modified-same-size.png`
- Passport ID: `bb05ef66-cc40-426c-bd97-38ce5835861f`
- Event ID: `5a98155a-fdb9-4413-a951-7f2a23060f38`
- Parent Event: `ae1ab53e-d7ca-4be2-a939-d75ad39b51d0`
- Parent Hash: `sha256:9af1b9ced51c13fbf1020bb6ee1bbad9836100cf264200b5567f7b5cda66544f`
- Content SHA-256: `e4935b1524169bb6353e993c4660524393c1cd430dd201e7bf63e2a9fcdd5da3`
- Object generation: `1786973992972372`
- Retention expiration: `2026-08-17T13:49:52+0000`
- Retrieved SHA-256: `e4935b1524169bb6353e993c4660524393c1cd430dd201e7bf63e2a9fcdd5da3`
- Retrieval hash match: `true`
- Persistent history count: `2`
- Spatial change ratio: `0.070073` (`7.01%`)
- Changed pixels: `82047 / 1170879`
- Bounding box: `x=0, y=1, width=1409, height=768`
- Evidence Continuity: `PASS`

### Physical-device screenshots

- `iphone/01-first-seen-sealed.png`
- `iphone/02-v1-storage-history.png`
- `iphone/03-v2-sealed-history.png`
- `iphone/04-passport-continuity.png`
- `iphone/05-v2-generation-event.png`
- `iphone/06-measurable-v1-first-seen.png`
- `iphone/07-measurable-v1-v2-history.png`
- `iphone/08-v2-measured-change-storage.png`
- `iphone/09-v2-bounding-box-technical-details.png`

An earlier physical-device V2 test used a different-size derivative. AEE
correctly returned `comparison_status=different_dimensions` and did not invent
a change percentage. The measurable chain above is the conforming same-size
V1/V2 acceptance case.
