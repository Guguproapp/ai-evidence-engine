# Mobile Authorization Specification

Status: next-stage architecture. No mobile app or authorization service is represented as implemented.

## Purpose

Let an evidence owner disclose selected Private Black Box fields without permanently opening the Wallet or publishing private source material.

## Flow

1. A third-party Verifier creates an Evidence Disclosure Request.
2. The owner phone receives the request through an authenticated channel.
3. The phone displays requester identity, requested fields, purpose, expiry, Passport/Event IDs, and risk.
4. The owner chooses `Approve`, `Deny`, or edits the requested scope.
5. The phone signs a single-use Authorization Token with the owner device identity.
6. The Black Box validates request ID, nonce, scope, audience, expiry, signature, and revocation state.
7. Only authorized fields are returned in a signed disclosure package.
8. Request, decision, disclosed fields, and result are appended to an Audit Log.

Example approval:

- Allow: version history, tool/model, timestamp.
- Deny: full prompt and original private source.

## Authorization token

Required claims:

- authorization ID and request ID
- passport/event ID
- issuer/owner signing identity
- requester/audience
- exact field scopes
- purpose
- issued-at and expiry
- single-use nonce
- revocation reference
- signature algorithm and signature

## Security requirements

- Single-use by default.
- Short expiry.
- Explicit field-level scope; no wildcard default.
- Audience-bound and purpose-disclosed.
- Owner can revoke before use or during a longer approved session.
- Replays, scope escalation, requester mismatch, and expired tokens fail closed.
- Permanent full-Wallet authorization is prohibited by default.

## Device evidence strength

- Direct SDK/tool integration: strongest event evidence.
- Share extension or OS document provider: medium evidence with a clear capture boundary.
- User after-the-fact upload: weaker provenance evidence.
- Screen/accessibility monitoring: privacy-heavy and unsuitable as the default evidence source.

## Public/private boundary

The public Passport exposes minimum proof only. The phone never releases prompt, original source, personal data, or sensitive parameters merely because a public verifier asks. Selective Disclosure requires a fresh valid authorization.
