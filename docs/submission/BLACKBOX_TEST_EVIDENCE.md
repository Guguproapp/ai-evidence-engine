# Development/Test Evidence Black Box — Sanitized Evidence

Environment: **Development/Test prototype**, not a permanent production evidence vault.

## Retention, deletion, overwrite, and retrieval run

- Recorded at: 2026-08-17T13:00:00.544Z
- Bucket: `aee-blackbox-test-856572888721`
- Object key: `evidence/v1/passports/84808f17-e82d-4b2c-931f-d9a127c8bcef/events/3d3e0c3f-5337-468b-a447-473a8bf3bea1/evidence`
- Passport ID: `84808f17-e82d-4b2c-931f-d9a127c8bcef`
- Event ID: `3d3e0c3f-5337-468b-a447-473a8bf3bea1`
- Object generation: `1786971545428744`
- Retention expiration: `2026-08-17T13:09:05.432000+00:00`
- Original SHA-256: `7e4bb29731e36aebad5907ce749bad3f0f542df155e39af713d30ed606bba37c`
- Retrieved SHA-256: `7e4bb29731e36aebad5907ce749bad3f0f542df155e39af713d30ed606bba37c`
- Hash match: `YES`
- Delete attempt: Google Cloud returned HTTP 403 while retention was active.
- Overwrite attempt: Google Cloud returned HTTP 412 because the generation precondition failed.
- Object existence after attempts: `YES`
- Evidence Continuity: `PASS`

Credentials, access tokens, account identifiers, and private keys are excluded.

## First-Seen V1 → V2 run

- Recorded at: 2026-08-17T16:57:34.728Z
- Passport ID: `9fb63dff-53f2-4d80-8c18-4c7a7bd152cf`
- V2 Event ID: `f5cac8a4-b821-4a89-ac11-201609d76aff`
- Parent V1 Event ID: `f6b423e4-0541-4dac-b8a9-7079c76f5820`
- V1 SHA-256: `80ce890c25b61b55dc680dde1b2960a2f14a4d9e35ddcc53b0d7a11b2920fa88`
- V2 SHA-256: `e4935b1524169bb6353e993c4660524393c1cd430dd201e7bf63e2a9fcdd5da3`
- Retrieved SHA-256: `e4935b1524169bb6353e993c4660524393c1cd430dd201e7bf63e2a9fcdd5da3`
- Object generation: `1786985811149278`
- Retention expiration: `2026-08-17T17:06:51.153000+00:00`
- Measured pixel change: `7.01%`
- Retrieved matches V2: `YES`
- Evidence Continuity: `PASS`

First-Seen states only that AEE recorded and sealed the exact version from that time. It is not proof of originality, authorship, copyright ownership, or earlier history.
