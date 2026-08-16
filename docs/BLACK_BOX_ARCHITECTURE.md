# Private Black Box Architecture

Status: partial Development/Test implementation. The repository has a local Evidence Wallet and an isolated IAM-protected Remote Black Box Test API for synthetic public demo evidence. A complete encrypted Production Black Box, automatic local-to-remote sync, remote Event Ledger, authorization service, and disclosure UI are not implemented.

## Principles

- Private by default.
- Local or owner-controlled storage.
- Encrypted at rest and in transit.
- Public Registry stores only minimum proof and commitments.
- No default upload of prompts, original private files, input data, private media, sensitive parameters, or personal identity data.
- Disclosure is explicit, scoped, expiring, revocable, and auditable.

## Private record

The Black Box may preserve:

- prompt and system prompt
- source assets and private originals
- model input/output
- tool calls and tool results
- provider, model, model version, seed, and parameters
- device, software, operator, and human approval
- full modification history and modality-specific masks/ranges
- production, slicer, printer, material, and manufacturing details

## Public commitment

For every private record, the public event may store a `wallet_commitment`, disclosure policy identifier, availability state, and encrypted-record locator that reveals no private content. The Registry must not receive plaintext private fields.

## Encryption and keys

- Generate a per-record content-encryption key.
- Encrypt private fields with authenticated encryption.
- Wrap the key to the owner device/account key.
- Protect device keys with Secure Enclave, Android Keystore, enterprise HSM, or equivalent.
- Separate evidence signing keys from data-encryption keys.
- Support rotation, recovery policy, revocation, and cryptographic deletion.

## Selective disclosure

The disclosure service verifies a signed authorization token, reads only the approved field paths, decrypts only the required record, returns a signed disclosure package, and writes an immutable audit event. It must fail closed on expired, replayed, revoked, mismatched, or over-broad requests.

## Current truth boundary

- Implemented: local Wallet asset bytes, `0600` permissions, public/private architecture boundary, event field for a Wallet commitment, and a Development/Test `sealEvidence` / `retrieveEvidence` Cloud Run service. The Test API validates identifiers, MIME signatures, size, and server-side SHA-256; derives a fixed Object path; uploads with `ifGenerationMatch=0`; returns Google retention metadata; retrieves the Object; and recomputes SHA-256. Its dedicated service account has Test-Bucket-level Object Creator and Object Viewer only.
- Test-only boundary: `aee-blackbox-test-856572888721` in `ASIA-EAST1`, 600-second unlocked bucket retention, Public Access Prevention enforced, Cloud Run IAM authentication required. No private user data is authorized for this environment.
- Not implemented: Production Evidence Bucket/API, automatic encrypted local-to-remote queue/sync, remote Event Ledger, complete encrypted schema, prompt/tool-call capture, mobile approval, selective disclosure service, enterprise recovery, and disclosure UI.
- Demo events must set `blackbox_available=false` until a complete corresponding private record is actually available.
