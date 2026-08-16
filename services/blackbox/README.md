# AEE Remote Black Box API — Development/Test

This isolated Cloud Run service seals and retrieves non-private synthetic test
evidence in `aee-blackbox-test-856572888721`. It is not a Production Black Box,
Event Ledger, deletion service, or retention administrator.

## Security boundary

- Cloud Run IAM authentication is required; anonymous invocation is disabled.
- The runtime service account has bucket-level Object Creator and Object Viewer
  only. It has no delete, overwrite, bucket-admin, IAM, or retention permission.
- Clients cannot select a bucket, object path, ACL, generation, service account,
  or retention setting.
- Every seal uses `ifGenerationMatch=0`.
- Every seal carries an existing `aee.event.v1` Signed Event. The server requires
  its Passport ID, Event ID, and content SHA-256 to match the client request and
  the uploaded bytes before creating an object.
- The server stores only the Signed Event Hash reference in object metadata. It
  does not store a private key, modify the event, or create a second event.
- The server recalculates SHA-256 before upload and after retrieval. The
  controlled client verifies the original event with the existing AEE Registry
  before and after remote storage operations.
- Only PNG, JPEG, and WebP evidence up to 10 MB is accepted.
- Audit logs contain identifiers, generation, result, and hash-match state; they
  never contain evidence bytes, credentials, access tokens, or private keys.

## Routes

- `POST /v1/evidence/seal` — multipart fields `schema_version`, `passport_id`,
  `event_id`, `content_sha256`, `content_type`, `signed_event`, and
  `evidence_file`.
- `POST /v1/evidence/retrieve` — JSON fields `passport_id` and `event_id`.

Run the controlled end-to-end client after deploying:

```bash
PYTHONPATH=src python3 scripts/blackbox_e2e.py \
  --service-url "https://SERVICE_URL" \
  --file apps/web/public/demo/version-3.png
```

The client obtains a Cloud Run identity token through the already-authenticated
Google Cloud CLI unless `AEE_ID_TOKEN` is present. It never prints the token.
