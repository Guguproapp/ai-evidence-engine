# Registry API

Default base URL: `http://127.0.0.1:8787`

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Service status |
| POST | `/register` | Register a text event and local private wallet record |
| POST | `/verify` | Verify a signed event, or compare `source` and `candidate` text |
| POST | `/fingerprint/lookup` | Compare candidate text against locally available Wallet sources |
| GET | `/passport/{id}` | Latest event for passport ID |
| GET | `/history/{content_id}` | Ordered recorded events for one content ID |
| GET | `/issuer/{id}` | Issuer public key and development trust status |
| POST | `/revoke` | Record a passport revocation reason and time |

`POST /register` accepts `content` plus provider, model, model_version, action_type, involvement_level, modification_scope, operator_type, human_approval, blackbox_available, parent_event, passport_id, and content_id. The signed public event schema is backward-compatible and can additionally carry `asset_type`, `media_type`, `device_id`, `software`, `software_version`, `model_provider`, `model_id`, `source_assets`, `authorization_id`, `wallet_commitment`, `c2pa_manifest_id`, `trust_status`, `change_metrics`, and `public_disclosure_level`.

`POST /verify` with `event` returns `hash_valid`, `signature_valid`, `parent_valid`, and `verified`. With `source` and `candidate`, it returns provenance similarity evidence, not a legal verdict.

This checkpoint has no authentication or authorization layer. Bind to localhost only; do not expose it to the internet.

## Development / Test Legacy Content Bridge

Base URL: `https://aee-continuity-demo-856572888721.asia-east1.run.app`

| Method | Path | Purpose |
|---|---|---|
| POST | `/v1/demo/first-seen` | Multipart image upload; create signed First-Seen Event, seal, retrieve, and reverify |
| POST | `/v1/demo/first-seen/version` | Multipart child image plus server-issued `bridge_id`; create V2 parent link, compare known versions, seal, and reverify |

The browser may provide only `evidence_file` and, for V2, the opaque server-issued `bridge_id`. It cannot provide a bucket, object path, generation, retention setting, credential, Passport ID, Event ID, content hash, or Signed Event. The backend validates image bytes, computes SHA-256, creates the existing `aee.event.v1`, and calls the IAM-protected Remote Black Box.

This is Development / Test only. First-Seen returns canonical `provenance_state=UNVERIFIED` and derived `registration_status=FIRST_SEEN_SEALED`; it never returns `VERIFIED_ORIGINAL`. Local V1/V2 state is ephemeral and full C2PA Soft Binding recovery is not implemented.
