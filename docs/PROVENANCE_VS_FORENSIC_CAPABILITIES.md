# AEE Provenance Verification vs. Forensic Modification Detection

Status: product capability boundary and Phase 2 research specification

Last verified: 2026-08-17

## Official capability statement

> AEE目前可驗證有來源履歷之內容變更；對沒有可信原始履歷的陌生內容，目前只能提供有限來源／完整性資訊，不能保證判斷是否曾被修改。

AI Evidence Engine is currently a provenance and integrity system. It is not a general-purpose single-image forensic detector.

## Two separate capabilities

### 1. Provenance Verification — IMPLEMENTED

When verifiable evidence exists, AEE can deterministically evaluate:

- exact content SHA-256
- AEE Registry match
- signed `aee.event.v1` Event evidence
- Event/parent chain continuity
- C2PA presence and integrity
- signature validity and separate signer trust status
- recorded AI involvement without visual guessing
- version history
- image A/B pixel comparison, Modification Mask, spatial change ratio, and bounding box when both bound versions are available

These results answer whether the supplied bytes match a recorded Evidence Event and how recorded versions relate. They do not prove that the depicted scene is true, identify an unrecorded author, or decide copyright and legality.

### 2. Forensic Modification Detection — NOT IMPLEMENTED

Given only one unfamiliar image with no trusted original, no matching AEE Registry Event, no Signed Event, and no C2PA provenance, AEE does not currently:

- prove that the image was modified
- locate an unknown edit
- calculate the edit percentage
- recover or identify the original source
- classify the asset as AI-generated or non-AI from appearance
- decide that the image is true, false, fake, or authentic

The correct current result is `UNVERIFIED`, together with the evidence that was or was not found. Missing provenance is not evidence of manipulation.

## Empirical boundary test

`TC-FORENSIC-MODIFIED-NO-PROVENANCE` uses a public CC0 photograph as A and a deterministic local edit as B. Neither fixture contains AEE/C2PA provenance. Only B was selected in the public Production verifier.

Ground truth from an offline A/B comparison:

- changed pixels: 51,920 of 3,000,000
- spatial change ratio: 1.7307%
- bounding box: `x=1094, y=1419, width=272, height=192`

Public Production returned `UNVERIFIED`, no Registry match, no C2PA manifest, `AI involvement = UNKNOWN`, and did not display a modification mask, changed region, or change percentage. That is the correct evidence-bounded behavior. The 1.7307% value is available only because the test harness deliberately retains both A and B; it is not a single-image Production forensic result.

Full evidence: `reports/forensic-no-provenance-027/TC_FORENSIC_MODIFIED_NO_PROVENANCE.md`.

## Phase 2 research: optional no-provenance forensic layer

This layer is a research proposal only. It must remain separate from the deterministic provenance Decision Engine and must never override signed evidence.

| Signal | Research purpose | Important limitation |
|---|---|---|
| Compression/recompression artifacts | Find inconsistent JPEG block/quantization histories | Normal exports and social platforms create similar artifacts |
| Error Level Analysis (ELA) | Visualize regions with different recompression behavior | Highly format- and quality-dependent; weak alone |
| Noise inconsistency | Compare sensor/noise residuals across regions | Denoising, resizing, low light, and synthetic imagery confound it |
| Resampling artifacts | Detect interpolation, scale, rotation, or pasted-region traces | Ordinary editing and platform processing can trigger it |
| Lighting/shadow inconsistency | Compare geometry, illumination, reflections, and shadows | Scene reconstruction is uncertain and domain-specific |
| Metadata contradictions | Compare EXIF, encoder, timestamp, dimensions, and container claims | Metadata may be missing, stripped, copied, or legitimately rewritten |
| Clone/copy-move detection | Search for duplicated regions within the same image | Repetition, textures, and compression produce false positives |
| Generative-AI forensic models | Estimate model-specific synthetic traces | Model/version drift, post-processing, dataset bias, and adversarial edits reduce reliability |
| Reverse image/source similarity search | Locate possible earlier public sources or near-duplicates | Requires an external index; similarity is not authorship or legal proof |

## Proposed Phase 2 architecture

```text
Input asset
  ├─ Deterministic Provenance Verification (existing trust path)
  └─ Optional Forensic Analysis (future, never in the trust path)
       ├─ independent signal extractors
       ├─ calibrated per-format/per-domain models
       ├─ anomaly fusion with source attribution
       └─ bounded forensic report
```

Each signal must preserve its detector name/version, input preprocessing, anomaly location, confidence calibration, benchmark scope, and limitations. Cross-domain and cross-format claims require held-out calibration datasets and published false-positive/false-negative measurements.

## Allowed future forensic wording

Allowed:

- `suspicious`
- `likely modified`
- `confidence`
- `detected anomaly`

Forbidden:

- `100% fake`
- `proven modified`
- `legally verified`
- any equivalent claim that turns probabilistic forensic signals into legal or cryptographic proof

Forensic confidence must be displayed separately from `Integrity State`, `Provenance State`, `Identity Trust`, `AI Involvement`, and recorded `Change Scope`.
