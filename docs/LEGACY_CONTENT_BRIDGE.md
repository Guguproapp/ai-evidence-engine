# AEE Legacy Content Bridge

Status: **Development / Test MVP**

## Purpose

The bridge gives an asset with no trustworthy AEE or C2PA history a truthful starting point:

1. The upload remains `Provenance State = UNVERIFIED`.
2. The owner explicitly chooses **Start a verified history from now**.
3. AEE hashes the exact bytes, creates a Passport and signed `aee.event.v1` First-Seen Event, seals the same bytes in the Development / Test Evidence Black Box, retrieves them, and re-verifies SHA-256.
4. Later recorded versions become child Events of that First-Seen Event.

First-Seen proves only that AEE received, fingerprinted, signed, and sealed those bytes at a recorded time. It does not prove originality, authorship, copyright, truth, or history before AEE received the asset.

## State model

The canonical `Provenance State` enum is unchanged. A First-Seen Event remains `UNVERIFIED` because prior provenance is unknown. `FIRST_SEEN_SEALED` is a derived `registration_status` shown only after the real remote seal, retrieval, and hash continuity checks pass.

- `VERIFIED PROVENANCE`: existing verified source/version history.
- `RECOVERED PROVENANCE`: reserved for future soft-binding recovery; not implemented.
- `FIRST-SEEN SEALED`: derived registration status; prior provenance remains unknown.
- `UNVERIFIED`: no verified history and no completed First-Seen seal.

## Signed fields and runtime fields

The signed Event uses the existing `source_assets` field to preserve:

- `relationship: first_seen`
- `prior_provenance: unknown`
- `aee_first_seen_time`
- `server_received_time`
- `soft_binding_type`
- `soft_binding_value`
- `manifest_repository_reference`
- `recovery_status`

Google object generation, metageneration, object path, retention expiration, and seal time remain in the separate remote Seal Result. They are never written back into the already-signed Event.

## Implemented MVP

- `aee.image.firstseen.v1` Evidence Profile.
- Exact SHA-256 fingerprint and signed Event.
- IAM-protected AEE backend to Remote Black Box call.
- Google Cloud Development / Test seal with generation precondition.
- Retention metadata, retrieval, and SHA-256 reverification.
- V1 to V2 parent Event and known-version RGB pixel comparison.
- Explicit opt-in UI and truthful bilingual boundary language.

## Reserved, not implemented

- C2PA Soft Binding federation.
- Invisible watermark recovery.
- Manifest repository lookup.
- Perceptual image, video, audio, text, or 3D recovery.
- Single-asset forensic modification detection.
- Production Black Box and durable cross-instance user ledger.

The Development / Test bridge currently uses ephemeral Cloud Run local state to retain the signing key, local Registry, and V1 comparison bytes between requests. This is sufficient for a bounded test flow but is not a Production durability design.
