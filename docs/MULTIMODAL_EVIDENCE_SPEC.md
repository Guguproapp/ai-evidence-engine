# AI Evidence Engine — Multimodal Evidence Adapter Specification

Status: architecture specification. `Image` has a working provenance demo and `Text` has a local fingerprint prototype. Video, audio, document containers, 2D design, 3D, and manufacturing adapters are next-stage work unless explicitly marked otherwise.

## Shared Universal Evidence Passport

Every adapter emits the same minimum event envelope:

- passport, event, content, and parent identifiers
- exact content hash and modality fingerprint
- timestamp, issuer, operator, device, software, model, and action
- AI involvement level and modality-specific change metrics
- source assets and parent hashes
- evidence signature, trust status, revocation status, and public disclosure level
- wallet commitment and optional external/C2PA manifest identifier

The adapter supplies modality-specific fingerprints and change metrics. The Passport, Event Chain, Signature, Registry, Private Wallet, and authorization model remain shared.

## Text / Article adapter

Store:

- exact hash
- paragraph and sentence hashes
- token and n-gram fingerprints
- source and candidate coverage
- longest continuous ratio
- character similarity
- optional semantic evidence explicitly labelled weak

Display `Source Coverage %` and `Relationship Confidence`. Never display an AI probability unless a separately validated model is added and clearly identified.

Current status: exact, paragraph, sentence, five-token n-gram, coverage, continuous match, and character similarity are implemented locally. Global corpus search is not implemented.

## Image adapter

Store exact hash, perceptual fingerprint, C2PA manifest, pixel diff, region mask, bounding box, and version chain. Display `Spatial Change %` with a warning that it is not an AI, ownership, copyright, or truth percentage.

Current status: exact hash, C2PA, signed chain, and Registry match are implemented. Pixel diff, mask, and bounding box are implemented only when AEE has the two bound image versions needed for deterministic comparison. Broad perceptual-source lookup and single unfamiliar-image forensic modification detection are not implemented.

## Video adapter

Store:

- file and segment hashes
- sampled frame fingerprints and keyframe fingerprints
- audio fingerprints
- C2PA/external manifests
- timeline parent-child history
- region masks attached to time ranges

Change Scope:

- Temporal Change %
- Spatial Change % per segment
- Audio Change %
- Source Coverage %

The verifier must support statements such as `00:12–00:18 modified` and `01:45–01:52 AI-generated segment` only when backed by recorded events or matched evidence.

Current status: `SPECIFIED_NOT_IMPLEMENTED`.

## Audio adapter

Store file hash, segment fingerprints, waveform/spectral/acoustic fingerprints, timeline events, source coverage, and modified-time ratio. Preserve channel, sampling, codec, model/tool, and operator evidence.

Current status: `SPECIFIED_NOT_IMPLEMENTED`.

## Document adapter

Supported design targets: PDF, HTML, EPUB, Office, and structured text. Combine C2PA or external manifests, Text DNA, embedded-media Passports, page/object structure, and document version chains. A document result must expose which pages, paragraphs, objects, or embedded assets changed.

Current status: `SPECIFIED_NOT_IMPLEMENTED` for document containers; `aee.text.v1` is implemented separately.

## 2D Design adapter

Design targets: SVG, PDF, DXF, and compatible structured design formats. Store file hash, object/layer tree, geometry, text, transforms, export history, linked assets, and print-job lineage. Raster exports become child assets rather than silently replacing the structured source.

Current status: `SPECIFIED_NOT_IMPLEMENTED`.

## 3D adapter

Design targets: STL, OBJ, STEP, 3MF, and other CAD/mesh formats. Store geometry, mesh, topology, dimension, texture/material, coordinate-system, unit, and parent-model fingerprints. Change metrics must distinguish geometry, topology, dimension, texture, and material changes.

Current status: `SPECIFIED_NOT_IMPLEMENTED`.

## 3D Printing / Digital Manufacturing adapter

Required lineage:

`Original CAD → Derived Model → STL/3MF → Slicer → G-code → Printer → Material → Print Job → Physical Output Passport`

Store at minimum:

- source design and derived-file hashes
- slicer/software and version
- G-code/toolpath hash
- printer/device identity
- material/batch when available
- job timestamp and production parameters
- operator and authorization
- manufacturing job signature
- output serial/QR/NFC identifier

When a format cannot embed C2PA, use a signed External Manifest / Evidence Passport. A physical-object Passport proves recorded lineage and device/job evidence; it does not guarantee that every physical property is true without trusted sensors or inspection evidence.

Current status: `SPECIFIED_NOT_IMPLEMENTED`.

## Adapter conformance

An adapter is `Integrated` only after create, sign, read, verify, tamper, parent-chain, and disclosure tests run against real assets. Interface-only adapters must be labelled `Specification` or `Prototype`, never `Integrated`.
