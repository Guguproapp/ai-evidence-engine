# AEE Evidence Identification & Coding Standard v1.0

Status: **Normative v1.0**  
Schema: `aee.event.v1`  
Compatibility: legacy signed events remain byte-for-byte verifiable.

## 1. Scope and truth boundary

AI Evidence Engine (AEE) records verifiable provenance, integrity, identity signals, AI involvement evidence, and modality-specific change measurements. It does not decide world truth, copyright ownership, infringement, plagiarism, legality, or an "AI probability".

The five dimensions below are independent. Implementations MUST NOT collapse them into one authenticity score.

## 2. Canonical states

### 2.1 Integrity State

| Enum | Meaning |
|---|---|
| `VALID` | Required evidence bytes, hashes, signatures, and chains verified under the selected profile. |
| `INVALID` | At least one required integrity check failed or evidence was revoked. |
| `UNVERIFIED` | Evidence is absent or insufficient to complete the required checks. |

Integrity never means that the depicted claim is true.

### 2.2 Provenance State

| Enum | Public label | Meaning |
|---|---|---|
| `VERIFIED_ORIGINAL` | Verified Original | A matching Registry event and required profile evidence verify, with no parent event. |
| `VERIFIED_MODIFIED` | Verified Modified | A matching Registry event and required profile evidence verify, with a valid parent relationship. |
| `UNVERIFIED` | Unverified | No matching, complete verifiable provenance was established. |
| `INVALID_EVIDENCE` | Invalid Evidence | Present evidence failed a required hash, signature, C2PA, profile, revocation, or parent-chain check. |

The word `Authentic` MUST NOT be used to mean world truth.

### 2.3 Identity Trust

| Enum | Meaning |
|---|---|
| `TRUSTED` | The signer identity passed the applicable production trust policy. |
| `DEVELOPMENT` | A valid development/self-issued identity; not production trust. |
| `UNKNOWN` | Identity assurance is unavailable or not evaluated. |
| `REVOKED` | The identity or credential is revoked. |

`Signature Valid` is not equivalent to `Signer Trusted`. Current demo C2PA certificates MUST display `DEVELOPMENT`.

### 2.4 AI Involvement

AI involvement MUST come from signed Event evidence or another verifiable source, never visual guessing.

| Level | Definition | Required evidence | Example | UI wording |
|---|---|---|---|---|
| `L0` | No recorded AI content involvement; transport or retrieval only. | Signed action showing no content modification. | copy, transfer, storage, plain retrieval | No recorded AI content involvement |
| `L1` | Technical transformation only. | Signed technical action and parameters. | conversion, resize, compression, transcoding | Technical transformation |
| `L2` | AI-assisted mechanical correction. | Signed AI/tool correction event. | spelling, noise reduction, mechanical cleanup | AI-assisted correction |
| `L3` | AI-assisted partial creative modification. | Signed event plus affected scope where available. | local generation, local rewrite, object edit | AI-assisted partial modification |
| `L4` | AI-major transformation derived from a source. | Signed event, source/parent, model/tool identity. | major rewrite or major generative edit | AI-major transformation |
| `L5` | Primarily AI-generated or synthetic creation. | Signed generation event and model/tool evidence. | generated article or image | AI-generated content |
| `UNKNOWN` | Insufficient signed evidence. | None sufficient. | unregistered uploaded file | AI involvement unknown |

### 2.5 Change Scope

Change Scope describes how much and where content changed under a modality-specific metric. It is not AI probability, fake probability, copyright percentage, or truth score.

## 3. Identifiers and digests

Legacy UUID values remain valid. Canonical public forms are:

| Object | Format |
|---|---|
| Passport | `urn:aee:passport:v1:<uuid>` |
| Event | `urn:aee:event:v1:<uuid>` |
| Authorization | `urn:aee:auth:v1:<uuid>` |
| Device | `urn:aee:device:v1:<public-key-fingerprint-or-uuid>` |
| Issuer | `urn:aee:issuer:v1:<issuer-id>` |
| Evidence Profile | `aee.<asset-type>.v1` |
| Content digest | `sha256:<64-lowercase-hex>` |
| Event hash | `sha256:<64-lowercase-hex>` |

Identifiers MUST be opaque, stable, versioned, and machine-readable. They MUST NOT contain names, email addresses, phone numbers, postal addresses, Apple/Google/GitHub account identifiers, MAC addresses, IMEI values, or real device serial numbers.

## 4. Canonicalization, hashing, and signing

Event JSON uses UTF-8, recursively sorted object keys, compact separators, and deterministic JSON serialization. The unsigned Event payload is canonicalized before SHA-256 and signature generation. Different dictionary insertion orders MUST produce identical bytes and hashes.

Text canonicalization is Unicode NFKC, lowercase, whitespace collapse, and trim. Existing Text DNA behavior is normative for `aee.text.v1`.

Every material content modification creates a new Event. The child stores `parent_event` and `parent_hash`; no prior Event is overwritten.

## 5. Event schema `aee.event.v1`

New Events include the legacy fields and:

`schema_version`, `asset_type`, `media_type`, `evidence_profile`, `version_id`, `source_assets`, `device_id`, `software`, `software_version`, `model_provider`, `model_id`, `model_version`, `authorization_id`, `wallet_commitment`, `c2pa_manifest_id`, `identity_trust`, `integrity_state`, `provenance_state`, `change_metrics`, and `public_disclosure_level`.

All fields inside the v1 signed-field set are canonicalized and signed. Implementations MUST NOT add inferred v1 fields to a legacy signed payload and then claim that the original signature covers them.

## 6. Evidence Profiles

Every profile declares: profile ID, asset/media type, canonicalization, required and optional fingerprints, required evidence, verification rules, change metrics, C2PA applicability, external-manifest policy, and implementation status.

| Profile | Status | Key metrics/evidence |
|---|---|---|
| `aee.text.v1` | `IMPLEMENTED` | exact/normalized hash, paragraph/sentence/5-gram fingerprints, source/candidate coverage, continuous ratio, character similarity |
| `aee.image.c2pa.v1` | `IMPLEMENTED` | exact SHA-256, C2PA, Registry Event, parent chain, signature, mask, spatial change |
| `aee.audio.v1` | `SPECIFIED_NOT_IMPLEMENTED` | modified-time ratio, source coverage |
| `aee.video.v1` | `SPECIFIED_NOT_IMPLEMENTED` | temporal/spatial/audio change ratios, source coverage |
| `aee.document.v1` | `SPECIFIED_NOT_IMPLEMENTED` | Text DNA, embedded media passports, document version chain, C2PA where applicable |
| `aee.design2d.v1` | `SPECIFIED_NOT_IMPLEMENTED` | object, layer, geometry, text change |
| `aee.model3d.v1` | `SPECIFIED_NOT_IMPLEMENTED` | geometry, mesh, topology, dimension, material change |
| `aee.manufacturing.v1` | `SPECIFIED_NOT_IMPLEMENTED` | source/derived hashes, slicer, G-code, printer identity, material, job, operator, authorization, manufacturing signature |

Reserved profiles MUST NOT enter the Decision Engine as successfully verified until an implementation and its conformance tests exist. Formats that cannot embed C2PA use an external Evidence Passport/manifest and disclose that binding policy.

## 7. Text Profile v1

Implemented fingerprints: exact SHA-256, normalized exact hash, paragraph hashes, sentence hashes, and 5-gram hashes.

Evidence tiers are `exact_match`, `large_continuous_match`, `partial_match`, `approximate_rewrite`, and `semantic_similarity_only`.

Relationship confidence is:

```text
0.50 × source_ngram_coverage
+ 0.30 × character_similarity
+ 0.20 × longest_continuous_ratio
```

Outputs include `evidence_tier`, `evidence_strength`, `relationship_confidence`, `source_coverage`, `candidate_coverage`, `longest_continuous_ratio`, and `character_similarity`. Legacy `confidence`, `source_ngram_coverage`, and `candidate_ngram_coverage` remain aliases.

Thresholds are **Prototype Calibration**, not cross-language or cross-domain universal accuracy. Outputs are not plagiarism, copyright infringement, or AI-generation percentages.

## 8. Image C2PA Profile v1

For equal-size RGB buffers, each pixel uses:

```text
delta = max(abs(R1-R2), abs(G1-G2), abs(B1-B2))
changed = delta >= 12
spatial_change_ratio = changed_pixels / total_pixels
```

Outputs: `changed_pixels`, `total_pixels`, `spatial_change_ratio`, `changed_region`, `bounding_box`, and `pixel_threshold`. Legacy `changed_ratio` and `threshold` remain aliases. UI wording is `<value>% measured pixel change`.

These outputs require a bound source/candidate pair. They MUST NOT be produced as if they were measured facts when only one unfamiliar image is available and no trusted source version can be resolved. In that case the current v1 profile performs provenance/integrity verification only and returns `UNVERIFIED` when required evidence is absent; single-image forensic modification detection is `NOT IMPLEMENTED`.

## 9. Deterministic Decision Matrix

| Case | Required result |
|---|---|
| Registry match + valid signature/hash/parent/profile evidence + no parent | `VALID`, `VERIFIED_ORIGINAL` |
| Same, with parent | `VALID`, `VERIFIED_MODIFIED` |
| Valid C2PA + no Registry match | overall `UNVERIFIED`, provenance `UNVERIFIED`; C2PA Integrity separately `Valid` |
| Registry exists + required evidence fails | `INVALID`, `INVALID_EVIDENCE` |
| C2PA/signature/hash/parent tampered | `INVALID`, `INVALID_EVIDENCE` |
| No C2PA + no Registry | `UNVERIFIED`, `UNVERIFIED` |

The Decision Engine returns `integrity_state`, `provenance_state`, `identity_trust`, and machine-readable `reasons[]`.

## 10. Legacy compatibility

Events without `schema_version` are read as `legacy`. Read-time normalization may derive display fields but MUST NOT alter stored JSON, event hash input, or signature input. Legacy Event reads, signatures, histories, passport lookup, and parent-chain checks remain supported.

## 11. Private Wallet commitment

A private evidence bundle is canonicalized and hashed:

```text
wallet_commitment = sha256:<SHA-256(canonical private bundle)>
```

Only the commitment is public. Prompts, system prompts, source assets, input/output, tool calls, model parameters, seed, device/operator details, full history, and manufacturing details remain private by default. Recomputing the bundle hash verifies disclosure against the public commitment.

## 12. Mobile Authorization foundation

Authorization fields are `authorization_id`, `request_id`, `issuer`, `requester`, `scope`, `allowed_fields`, `denied_fields`, `created_at`, `expires_at`, `single_use`, `revoked`, and `signature`.

Policy is default-deny, scope-limited, expiring, revocable, signed, and capable of single-use enforcement. The schema, signature, and validator are implemented; a mobile application is **NOT IMPLEMENTED**.

## 13. Public disclosure levels

Canonical enum: `PUBLIC_MINIMUM`, `PUBLIC_EXTENDED`, `PRIVATE`, `SELECTIVE`. Default is `PUBLIC_MINIMUM`; sensitive Black Box fields are `PRIVATE`; authorized disclosure is `SELECTIVE`.

## 14. Implementation boundary

- **IMPLEMENTED:** v1 identifiers/helpers, canonical JSON, v1 Event fields/signing, legacy compatibility, Text Profile, Image C2PA Profile, deterministic Decision Engine, Wallet commitments, authorization schema/signing/validation foundation, and public Verifier state presentation.
- **SPECIFIED — NOT IMPLEMENTED:** audio, video, document, 2D design, 3D model, and manufacturing verification adapters.
- **NOT IMPLEMENTED:** single unfamiliar-image forensic modification detection without a trusted source/history, complete encrypted Black Box product, mobile application, production IAM, and production C2PA Trust List identity.
