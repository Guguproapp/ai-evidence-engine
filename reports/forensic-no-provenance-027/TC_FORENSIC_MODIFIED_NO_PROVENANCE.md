# TC-FORENSIC-MODIFIED-NO-PROVENANCE

Test date: 2026-08-17

Production URL: https://ai-evidence-engine-gugupro.artistuncle.chatgpt.site

Production interaction: real Chrome file selection and visible UI result; only image B was selected.

## Test material and provenance exclusion

Source photograph: [Wikimedia Commons — Photo of building.jpg](https://commons.wikimedia.org/wiki/File:Photo_of_building.jpg), author Mrshaxas, CC0 1.0.

The deterministic fixture script makes both images the same 1500×2000 RGB PNG, then changes only a known local region in B by adding a red rounded rectangle and white X. The purpose is to retain exact A/B Ground Truth, not to simulate an AEE Event.

| Asset | Role | SHA-256 | Size |
|---|---|---|---:|
| `ground-truth-A-original.png` | Original A | `2fc36dd07038add110cf4aba3b9db4bae46499e975d49c85419bca8b1ffc03ca` | 5,279,166 bytes |
| `ground-truth-B-modified.png` | Modified B; only Production input | `2a0ccc1496d42e6e749f2c9432899f9bc28e5b88e9da882e7f7c6fa8522736bd` | 5,198,530 bytes |
| `ground-truth-mask.png` | Offline Ground Truth mask | `8316aa8aabc4d95adc3e526f11ce21d8b31857fe29c6908bb6e974cbec506df6` | 9,627 bytes |

Exclusion checks:

- no AEE Passport was created for A or B
- no AEE Signed Event was created for A or B
- no AEE Registry record matches either fixture hash
- `c2patool 0.27.12` returned `No claim found` for both A and B
- A was never selected in the Production verifier; only B was selected

## Ground Truth, not Production detection

The offline A/B comparator uses the current image-profile threshold:

```text
delta = max(abs(R1-R2), abs(G1-G2), abs(B1-B2))
changed = delta >= 12
```

Result:

- changed pixels: 51,920
- total pixels: 3,000,000
- spatial change ratio: 1.7307%
- bounding box: `x=1094, y=1419, width=272, height=192`

This is an offline A/B Ground Truth measurement. It is not an AEE Production single-image forensic result.

## Actual Production result for B only

General UI displayed:

- `尚未驗證`
- `無法確認來源`
- AEE source history: not found
- C2PA provenance credential: not found
- signer identity: no verifiable data
- AI involvement: cannot determine
- content fingerprint: created

Developer Details displayed:

- full SHA-256: `2a0ccc1496d42e6e749f2c9432899f9bc28e5b88e9da882e7f7c6fa8522736bd`
- Manifest count: `0`
- Registry state: `No Match`
- Identity trust: `Unknown`
- AI involvement evidence: `UNKNOWN`
- validation detail: `no_c2pa_validation_record`
- reason code: `no_verifiable_registry_source`

Production did not display a modification mask, changed region, bounding box, or change percentage for B.

## Required answers

| Question | Evidence-based answer |
|---|---|
| A. Can AEE determine that B was modified without original history? | **No.** Current Production returns `UNVERIFIED`; it does not perform single-image forensic modification detection. |
| B. Can AEE locate the modified region? | **No.** Not from B alone. The test mask/bounding box exists only because the offline test retains A and B. |
| C. Can AEE calculate a modification ratio? | **No.** Not from B alone. The offline 1.7307% is an A/B Ground Truth measurement, not Production output. |
| D. Can AEE determine the original source? | **No.** There is no matching provenance record, embedded claim, or reverse-image index. |
| E. What does it actually output? | `UNVERIFIED` / `無法確認來源`, no Registry match, no C2PA, signer unknown, and AI involvement unknown. |
| F. Which functions are provenance verification rather than forensic detection? | Hash/Registry matching, C2PA/signature validation, Event/parent history, and A/B mask/ratio for recorded versions are Provenance Verification. Inferring edits from one unfamiliar image is Forensic Modification Detection and is not implemented. |

## Capability classification

**IMPLEMENTED — Provenance Verification:** verification and deterministic version comparison when trusted source/version evidence exists.

**NOT IMPLEMENTED — Forensic Modification Detection:** detecting, localizing, or measuring unknown edits from a single unfamiliar image without trusted provenance.

## Evidence files

- `ground-truth-A-original.png`
- `ground-truth-B-modified.png`
- `ground-truth-mask.png`
- `ground-truth-metrics.json`
- `make_ground_truth.mjs`
- `production-B-unverified.png`
- `production-B-developer-details.png`
