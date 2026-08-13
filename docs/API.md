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

`POST /register` accepts `content` plus provider, model, model_version, action_type, involvement_level, modification_scope, operator_type, human_approval, blackbox_available, parent_event, passport_id, and content_id.

`POST /verify` with `event` returns `hash_valid`, `signature_valid`, `parent_valid`, and `verified`. With `source` and `candidate`, it returns provenance similarity evidence, not a legal verdict.

This checkpoint has no authentication or authorization layer. Bind to localhost only; do not expose it to the internet.

