# AI Evidence Engine Final Device & Evidence Gate 029

Test date: 2026-08-17 (Asia/Taipei)

## Source consistency

- Branch: `main`
- Local HEAD: `a5f69e494a13be6e0b57ac68023b8c048fbb903b`
- Remote `origin/main`: `a5f69e494a13be6e0b57ac68023b8c048fbb903b`
- Production Sites Version: `10`
- Production source commit: `a5f69e494a13be6e0b57ac68023b8c048fbb903b`
- Public URL: `https://ai-evidence-engine-gugupro.artistuncle.chatgpt.site`
- Result: `PASS`

## Physical device

- Device: physical iPhone 15 (`physical` confirmed by Apple device tooling)
- OS: iOS 26.6 Beta
- Browser: Mobile Safari bundled with iOS 26.6 Beta
- Connection: wired physical device plus iPhone Mirroring
- Simulator used as acceptance evidence: `NO`

## Summary table

| Test Case | Input | Expected | Actual | Status | Evidence |
|---|---|---|---|---|---|
| TC-SIGNED-MODIFIED | `01-aee-signed-version-3.png` | Verified Modified, C2PA, signature, mask, history | Verified Modified; 4.8% measured pixel change; C2PA/signature/history shown | PASS | `../app-user-test-024/iphone/04-signed-upload-result.png`, `07-modification-mask.png`, `08-signature-c2pa.png`, `10-version-history.png` |
| TC-UNKNOWN | `02-unknown-source.jpg` | UNVERIFIED; do not guess AI, human, true or false | “無法確認來源”; explicitly states this does not mean fake or AI-generated | PASS | `iphone/03-unknown-uploaded.png`, `iphone/04-unknown-unverified.png` |
| TC-AI-NO-SOURCE | `03-ai-no-source.jpg` | AI Involvement UNKNOWN without signed evidence | “無法確認來源”; “AI 參與：無法確認”; no L4/L5 guess | PASS | `iphone/05-ai-no-source-uploaded.png`, `iphone/06-ai-no-source-unverified.png`, `iphone/07-ai-no-source-ai-unknown.png` |
| TC-CORRUPT | `04-corrupt.png` | Reject; no stale Verified result | Clear invalid-image message; result area says no verification result is displayed | PASS | `iphone/08-corrupt-error.png`, `iphone/09-corrupt-no-stale-result.png` |
| TC-UNSUPPORTED | `05-unsupported.txt` | Reject; no false evidence result | iOS native picker disables the TXT file, so it cannot be sent to AEE and no result is created | PASS | `iphone/10-unsupported-txt-disabled-in-picker.png` |
| TC-BLACKBOX | Built-in `ProofCart Version 3` synthetic evidence | Seal, retention metadata, retrieve, SHA match, signed-event post-seal verification, continuity | Physical iPhone UI completed all steps against real Development/Test Google Cloud service | PASS | `iphone/12-blackbox-entry.png` through `iphone/18-blackbox-generation-content-sha.png` |

## Input facts

| File | Size | SHA-256 | Source |
|---|---:|---|---|
| `01-aee-signed-version-3.png` | 239714 bytes | `7e4bb29731e36aebad5907ce749bad3f0f542df155e39af713d30ed606bba37c` | Project synthetic signed demo |
| `02-unknown-source.jpg` | 76443 bytes | `80ce890c25b61b55dc680dde1b2960a2f14a4d9e35ddcc53b0d7a11b2920fa88` | Public/non-private test asset without AEE provenance |
| `03-ai-no-source.jpg` | 720x480 JPEG, approximately 26 KB | `9f578b3eff8a13d89526fa1116180e19e87d259b989b0af20ea49f120ae9d418` | Synthetic AI test image without signed AEE event |
| `04-corrupt.png` | 15 bytes | `1bb5eeb95c53aa415e4222efa146a385f5210ab42d0122aa949e98ef41c0675d` | Deliberately corrupt non-private test input |
| `05-unsupported.txt` | approximately 1.7 KB | `1f2a4094b9c7230241baee001382ccbccbcb8cbb0c5050a1867142d0b6ad9be3` | Non-private unsupported test input |

## Known-version comparison evidence

- Original Version 1 SHA-256: `082cc812bb1720f7335e41da823706dc022aae1ded0daa1dfbc20b93717e0fee`
- Modified Version 3 SHA-256: `7e4bb29731e36aebad5907ce749bad3f0f542df155e39af713d30ed606bba37c`
- `spatial_change_ratio`: `0.047743` (UI: 4.8% measured pixel change)
- Bounding box: `{"x":250,"y":245,"width":220,"height":75}`
- Capability boundary: this is a comparison between trusted recorded versions, not single-image forensic detection.

## Physical iPhone Black Box evidence

- Environment: Development / Test
- Input: built-in `ProofCart Version 3` synthetic evidence
- Passport ID: `dc0fc62d-6c67-4dc9-b463-4c25141aa36b`
- Event ID: `8516ad68-21ee-4695-9885-f49e2d90ec50`
- Object key: `evidence/v1/passports/dc0fc62d-6c67-4dc9-b463-4c25141aa36b/events/8516ad68-21ee-4695-9885-f49e2d90ec50/evidence`
- Object generation: `1786957767206882`
- Sealed time: `2026-08-17T09:09:27+00:00`
- Retention until: `2026-08-17T09:19:27+00:00`
- Retention state during test: protected by active approximately 10-minute Development/Test retention window
- Original SHA-256: `7e4bb29731e36aebad5907ce749bad3f0f542df155e39af713d30ed606bba37c`
- Retrieved SHA-256: `7e4bb29731e36aebad5907ce749bad3f0f542df155e39af713d30ed606bba37c`
- Match: `YES`
- Signature verification before seal: `PASS`
- Signed Event verification after seal: `PASS`
- Evidence Continuity: `PASS`

This is a real Development/Test Google Cloud flow. It is not described as a Production Black Box or permanent retention.

## Historical iPhone gate audit

| Gate | Earlier status | Actual completion | Evidence |
|---|---|---|---|
| Unknown source | NOT RUN in 024-028 | Completed in 029 | `iphone/03-unknown-uploaded.png`, `iphone/04-unknown-unverified.png` |
| AI image without trusted provenance | NOT RUN in 024-028 | Completed in 029 | `iphone/05-ai-no-source-uploaded.png` to `07-ai-no-source-ai-unknown.png` |
| Corrupt PNG | NOT RUN in 024-028 | Completed in 029 | `iphone/08-corrupt-error.png`, `iphone/09-corrupt-no-stale-result.png` |
| Unsupported TXT | NOT RUN in 024-028 | Completed in 029 by native picker rejection | `iphone/10-unsupported-txt-disabled-in-picker.png` |

## Final Gate A-U

| Gate | Status | Evidence |
|---|---|---|
| A. Production | PASS | Public Site Version 10 is live |
| B. GitHub Source一致 | PASS | Local, remote and Production source all `a5f69e...` |
| C. Signed Image | PASS | `../app-user-test-024/iphone/04-signed-upload-result.png` |
| D. Known Version Modification Comparison | PASS | `../app-user-test-024/iphone/06-verified-modified-status.png` |
| E. Modification Mask | PASS | `../app-user-test-024/iphone/07-modification-mask.png` |
| F. C2PA | PASS | `../app-user-test-024/iphone/08-signature-c2pa.png` |
| G. Signature | PASS | `../app-user-test-024/iphone/08-signature-c2pa.png` |
| H. History | PASS | `../app-user-test-024/iphone/10-version-history.png` |
| I. Unknown Source | PASS | `iphone/04-unknown-unverified.png` |
| J. AI-no-source | PASS | `iphone/06-ai-no-source-unverified.png`, `07-ai-no-source-ai-unknown.png` |
| K. Corrupt Image | PASS | `iphone/08-corrupt-error.png`, `09-corrupt-no-stale-result.png` |
| L. Unsupported File | PASS | `iphone/10-unsupported-txt-disabled-in-picker.png` |
| M. Mac Evidence Black Box | PASS | `../app-user-test-024/desktop/11-blackbox-complete-pass.png`, `12-blackbox-final-state.png` |
| N. iPhone Evidence Black Box | PASS | `iphone/14-blackbox-continuity-pass.png` through `18-blackbox-generation-content-sha.png` |
| O. Google Cloud Seal | PASS | `iphone/15-blackbox-google-seal.png` |
| P. Retention Metadata | PASS | `iphone/16-blackbox-retention-retrieval-sha.png` |
| Q. Retrieval | PASS | `iphone/16-blackbox-retention-retrieval-sha.png` |
| R. SHA-256 Reverification | PASS | `iphone/16-blackbox-retention-retrieval-sha.png` |
| S. Signed Event Post-Seal Verification | PASS | `iphone/17-blackbox-signed-event-ids.png` |
| T. Evidence Continuity | PASS | `iphone/14-blackbox-continuity-pass.png`, `17-blackbox-signed-event-ids.png` |
| U. Gemini Explanation | PASS | `../app-user-test-024/iphone/09-gemini-explanation.png` |

## Issues and evidence integrity

- P0 bugs: `NONE` in the final completed flows.
- `iphone/ERROR_01-ai-no-source-verification-timeout.png` is retained because failed/ambiguous evidence must not be deleted. Investigation showed the earlier action targeted the Evidence ID control instead of the image flow; the same physical iPhone later completed the correct image upload and produced UNVERIFIED / AI Unknown evidence. It is an operator-control artifact, not a product verification PASS.
- iPhone Mirroring disconnected once while opening Files. The physical device remained paired; macOS showed the correct selected iPhone. Restarting the mirroring app restored the same physical iPhone session. No simulator replaced this test.
- The public UI does not automatically scroll to the uploaded-image result on iPhone. Keyboard focus had to be moved before scrolling. This is a P1 usability issue, not an evidence-integrity failure.

## Recording and VIDEO READY

- Formal edited competition video: `NOT RUN` by instruction.
- Full unedited acceptance recording: `NOT RUN`; this is the next gate after this report.
- Screenshot evidence: 18 physical-iPhone files in `reports/app-user-test-029/iphone/`, plus historical 024 evidence.
- VIDEO READY: `YES` for beginning the required unedited acceptance recording. This does not authorize or claim completion of the final edited competition video.
