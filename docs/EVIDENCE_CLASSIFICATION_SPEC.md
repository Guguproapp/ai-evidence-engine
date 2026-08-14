# AI Evidence Engine — Evidence Classification Specification

Status: v1.0 normative product specification. The image adapter is the first working modality. This document does not claim that every listed adapter is implemented.

## Purpose

AI Evidence Engine verifies recorded provenance evidence. It does not decide whether content is factually true, legal, non-infringing, or human-authored. Results are expressed on three independent axes so that no single signal is promoted into a universal truth claim.

## Axis A — Provenance State

| State | Required conditions | Meaning | Required display wording |
|---|---|---|---|
| Verified Original | C2PA integrity valid where required; exact Registry match; Registry event signature and chain valid; no parent event | This asset matches a signed recorded first version | `Verified Original — recorded first version; not a claim that the depicted facts are true.` |
| Verified Modified | C2PA integrity valid where required; exact Registry match; Registry signature and chain valid; parent exists | This asset matches a signed child version | `Verified Modified — signed history and parent relationship verified.` |
| Unverified | Evidence absent, incomplete, or valid C2PA has no matching Registry record | Provenance cannot be established from available evidence | `Unverified — absence of matched evidence does not prove the asset is fake.` |
| Invalid Evidence | C2PA data/hash invalid, Registry signature/chain invalid, revoked record, or required evidence conflicts | Evidence exists but fails integrity or consistency checks | `Invalid Evidence — one or more evidence checks failed.` |

Decision rules:

1. Valid C2PA without a Registry match is `Unverified`.
2. Valid Registry evidence with invalid C2PA is `Invalid Evidence` for an adapter that requires C2PA.
3. No C2PA and no Registry match is `Unverified`.
4. Valid C2PA plus a valid matching Registry record with no parent is `Verified Original`.
5. Valid C2PA plus a valid matching Registry record with a parent is `Verified Modified`.
6. Identity trust is displayed separately as `Trusted`, `Development`, or `Unknown`.

## Axis B — AI Involvement

AI involvement describes recorded process evidence. It is not inferred from style and is not an AI probability.

| Level | Criteria | Examples | Required evidence | Display wording |
|---|---|---|---|---|
| L0 | No AI content involvement; transport, copy, storage, or direct capture only | Copy, transfer, storage, camera capture | Event type, operator/device, time, content hash | `L0 — no recorded AI content involvement` |
| L1 | Technical transformation without intended semantic or creative change | File conversion, font/layout change, export, compression | Parent/child hashes, software, action, deterministic settings | `L1 — technical transformation only` |
| L2 | AI-assisted mechanical correction with meaning intended to remain unchanged | Spelling, punctuation, typo correction, mechanical formatting | Parent/child, tool/model, corrected ranges, approval | `L2 — AI-assisted mechanical correction` |
| L3 | AI-assisted partial creative modification; original remains materially recognizable | Crop, color grade, denoise, sentence polish, local retouch | Parent/child, tool/model, affected regions/ranges, change metrics | `L3 — AI-assisted partial creative modification` |
| L4 | AI performs a major transformation or substantial creative edit | Semantic rewrite, object removal/addition, generative fill, background generation | Parent/child, model/tool, prompt commitment, masks/ranges, approval | `L4 — AI-major transformation` |
| L5 | Asset or major component is generated as synthetic content | Full article, image, audio, video, code, or 3D generation | Generation event, model/provider/version, input commitments, output hash | `L5 — AI-generated or synthetic content` |

Rules:

- L0 and L1 must never be displayed as AI creation.
- L2 records AI assistance but must not be displayed as creative authorship by default.
- L3–L5 require a new child event; the parent must not be overwritten.
- A level may be shown only from recorded evidence. A detector estimate must be labelled separately and cannot populate this axis.

## Axis C — Change Scope

Change Scope measures how much of the asset changed. It is independent of AI involvement and must never be labelled as copyright percentage, ownership percentage, truth score, or AI probability.

| Modality | Metrics |
|---|---|
| Text | source coverage, candidate coverage, longest continuous ratio, character similarity, changed ranges |
| Image | spatial changed-pixel ratio, region masks, bounding boxes, perceptual distance |
| Video | temporal change, spatial change by segment, audio change, source coverage |
| Audio | modified-time ratio, segment coverage, spectral/acoustic distance |
| Document | text change, page/object change, embedded-media changes |
| 2D design | object/layer/geometry/text change and export lineage |
| 3D | geometry, mesh, topology, dimension, texture, and material change |
| Manufacturing | design-to-toolpath lineage, parameter changes, job completion evidence |

## Trust signals shown independently

- Content integrity: exact hash and C2PA hard binding.
- Evidence signature: event signature validation.
- Chain integrity: parent event and parent hash validation.
- Registry match: exact registered record found or not found.
- Issuer identity: trusted production identity, development identity, or unknown.
- Revocation: active or revoked.
- Private evidence: unavailable, available to owner, or selectively disclosed.

## Legal boundary

The system must never output a legal plagiarism, infringement, copyright ownership, or legality verdict. Semantic similarity alone is weak evidence and cannot establish provenance.
