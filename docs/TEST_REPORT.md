# Test Report

This file records executed results only. Planned work is never `PASS`.

## Local automated tests — 2026-08-15

| Suite | Command | Result |
|---|---|---|
| Python core/integration | `PYTHONPATH=src /tmp/ai-evidence-explainer-venv/bin/python -m unittest discover -s tests -v` | PASS — 34/34 |
| Web classification/render/security | `npm test` in `apps/web` | PASS — 11/11 |
| Lint | `npm run lint` in `apps/web` | PASS |
| Production build | `npm run build` in `apps/web` | PASS |

Python coverage includes v1 Identifier/digest formats, canonical JSON stability, Event Schema validation, profile status enforcement, deterministic decisions, legacy Event signature/history/parent compatibility, Wallet commitments, Authorization scope/expiry/revocation/single-use rules, hierarchical Text DNA, RSA signatures, C2PA creation/read/verify, real tampered data-hash mismatch, RGB Modification Masks, and the Gemini decision boundary.

The final eligibility-document audit reran the same suites after adding the project timeline, Google Cloud evidence index, IP/license audit, financial/user evidence boundaries, and final qualification gate: Python 34/34, Web 11/11 including Production build, and Lint all remained PASS. No product source or Production deployment changed in that audit.

The Individual-entrant and owner-closeout document update reran the suites on 2026-08-15: Python 34/34, Web 11/11 including Production build, and Lint all PASS. The public verifier returned HTTP 200 and the Cloud Run `/health` endpoint returned HTTP 200 with `gemini-2.5-flash` on Vertex AI. The Cloud Run service root returned HTTP 404 by design because the health resource is `/health`; this is not a failed service check. No product source or Production deployment changed.

## Required provenance classification matrix

| Input evidence | Expected | Result |
|---|---|---|
| Valid C2PA + no Registry match | `Unverified` | PASS |
| Valid Registry + invalid C2PA | `Invalid Evidence` | PASS |
| No C2PA + no Registry | `Unverified` | PASS |
| Valid C2PA + valid matching Registry + no parent | `Verified Original` | PASS |
| Valid C2PA + valid matching Registry + parent | `Verified Modified` | PASS |
| Matching Registry + invalid signature | `Invalid Evidence` | PASS |
| Matching Registry + hash mismatch | `Invalid Evidence` | PASS |

The state machine keeps C2PA integrity, Registry match, identity trust, and provenance outcome as separate signals. A single evidence source cannot imply `Verified Original`.

## Rebuilt image Evidence

Command: `PYTHONPATH=src /tmp/ai-evidence-explainer-venv/bin/python scripts/build_image_demo.py`

Result: PASS. Official `c2patool 0.27.12` produced three embedded manifests and a three-version parent ingredient chain. All three rebuilt Registry signatures verify. Version 3 measured 16,500 changed pixels of 345,600, ratio `0.047743`, bounding box `{x:250,y:245,width:220,height:75}`.

The prepared tampered Version 3 was read by the official tool and returned `assertion.dataHash.mismatch`; the previous signed Version 3 remains C2PA-valid but has no match in the rebuilt Registry and is the real browser fixture for `Valid C2PA + no Registry → Unverified`.

## Cloud Run / Gemini — rebuilt four-state contract

| Check | Result | Evidence |
|---|---|---|
| Cloud Run deploy | PASS | Revision `ai-evidence-explainer-00003-m75`, 100% traffic |
| Health | PASS | Production HTTPS returned HTTP 200 |
| Gemini Production call | PASS | Vertex AI `gemini-2.5-flash`, HTTP 200 |
| State preservation | PASS | Request and response both `Verified Modified` |
| Allowlisted facts | PASS | Service rejects unsupported states and removes non-allowlisted facts in tests |
| Failure fallback | PASS locally | Web retains deterministic verification and presents an explicit explanation failure |

Production request ID: `3da55316-9616-46af-9ab2-39e34a1bdb49`. Cloud Logging records the corresponding Vertex AI upstream HTTP 200 and Version 3 Evidence ID `1c3d4a0f-9e2a-4a18-a83f-0c982db4ef33`.

## Public Production regression for rebuilt release

| Flow | Status |
|---|---|
| Universal Evidence Passport homepage | PASS |
| Signed Version 1 upload → Verified Original | PASS |
| Signed Version 3 upload → Verified Modified | PASS |
| Valid old C2PA + rebuilt Registry miss → Unverified | PASS |
| No C2PA + no Registry → Unverified | PASS |
| Tampered Version 3 → Invalid Evidence + dataHash mismatch | PASS |
| Version History 1/2/3 | PASS |
| 4.8% Modification Mask | PASS |
| Evidence Passport / Change Metrics / Trust / Private Evidence | PASS |
| ProofCart | PASS |
| Missing Evidence ID | PASS |
| Gemini Production integration | PASS |
| Universal adapters / Next Stage architecture | PASS |

The checks above were rerun against Sites Version 5 at the public HTTPS URL after deployment, using actual project-generated files through the page file chooser. Version 5 displays the v1 Evidence Profile, Integrity, Provenance, Identity Trust, signed AI Involvement, measured Change Scope, and Private Evidence boundary. The old valid C2PA fixture displayed `C2PA integrity: Valid`, `Registry: No Match`, and `Unverified`. The tampered fixture displayed `Invalid Evidence`, `assertion.dataHash.mismatch`, and `c2pa_integrity_invalid`. Gemini returned `gemini-2.5-flash on Vertex AI` while preserving `Verified Modified`.

## Video

Final operation recording: **PASS** — ID `pqRNOvyE3_c`; visibility is
**PUBLIC — judge-accessible**.

- Duration: 2:42.733 (YouTube display 2:43), below the three-minute limit.
- Video: H.264, 1920×1080, 30 fps, 16:9, burned-in English captions.
- Audio: AAC, 48 kHz, mono English narration; measured mean volume -15.6 dB and peak -1.3 dB.
- Actual Production operations: signed Version 3 upload, `Verified Modified`,
  Current Image, Change Overlay, 4.8% Mask, History 1/2/3, tampered upload,
  `Invalid Evidence`, `assertion.dataHash.mismatch`, Gemini explanation,
  ProofCart, universal adapters, and labelled Next Stage.
- Visual QA: complete browser viewport, visible operation cursor, no giant black
  borders, and no cropped website column. Automated crop detection found only
  a four-pixel encoder edge, not the large framing failure in the rejected video.
- YouTube copyright check: completed with no issue reported during processing.
- External visibility check after the owner's publication instruction: signed-out
  YouTube oEmbed returned HTTP 200 with the correct title and video ID.

The previous 2:24 `Fwu7yGUTVwo` video remains rejected and must not be submitted.
The public but silent `HDG1qYo5hUg` upload is also superseded and must not be submitted.

## Bilingual web and Android preparation — 2026-08-16

| Check | Result |
|---|---|
| Traditional Chinese SSR default | PASS |
| Visible Traditional Chinese / English switch | PASS in source/render tests; live browser deployment pending |
| `aee_locale` localStorage persistence | PASS in source contract test; interactive reload pending deployment |
| Canonical Evidence enums unchanged | PASS |
| Bilingual `/privacy` page | PASS in server-render test |
| Web tests | PASS — 13/13 |
| Web lint | PASS |
| Web production build | PASS |
| Android API / package | PASS — compile/target 36, min 23, `com.gugupro.aievidence` |
| Android build | PASS — Gradle 8.11.1, AGP 8.9.1, Android Browser Helper 2.7.2 |
| Debug APK signature | PASS — Android debug certificate, APK v1/v2 signatures verify |
| Android 16 install | PASS — installed on API 36 emulator |
| Android launch regression | PASS after adding required `ManageDataLauncherActivity`; no AEE fatal exception |
| Android full verifier flow | BLOCKED — clean emulator shows Chrome first-run Terms; owner action required |
| Release AAB | PASS build, intentionally unsigned; NOT READY for Play upload |
| Digital Asset Links / fullscreen TWA | BLOCKED — final Play App Signing public fingerprint not yet available |
| Real Android screenshots | NOT RUN — no store screenshots fabricated before full runtime test |

The first launch exposed and fixed a real Android Browser Helper integration failure: `ManageDataLauncherActivity` was missing from the app manifest. The repaired APK launched and bound to the Android Chrome TWA provider. Testing stopped at Chrome's first-run Terms screen; Codex did not accept it on behalf of the owner.

## Remote Black Box Development/Test API — 2026-08-16

| Check | Result |
|---|---|
| Python core/integration including 5 new Black Box tests | PASS — 39/39 |
| Dedicated runtime identity | PASS — `aee-blackbox-test@ai-evidence-engine-gugupro.iam.gserviceaccount.com` |
| Project-level roles for runtime identity | PASS — none |
| Test-Bucket permissions | PASS — Object Creator + Object Viewer only |
| Anonymous Cloud Run request | PASS — HTTP 403 |
| New synthetic Passport/Event seal through API | PASS |
| Server-side pre-upload SHA-256 | PASS |
| Google Object generation and retention metadata | PASS |
| API retrieval and server-side SHA-256 recheck | PASS — `hash_match=true` |
| Wrong SHA-256 creates no Object | PASS — HTTP 400 then retrieve HTTP 404 |
| Duplicate Event seal | PASS — HTTP 409; original generation unchanged |
| Invalid Passport/Event identifiers | PASS — HTTP 400 |
| Client-controlled Object path | PASS — rejected HTTP 400 |
| Cloud Run audit log allowlist | PASS — request, operation, IDs, generation, timestamp, result, hash match only |

Real E2E Test Event: `f562e4d8-f633-4e4c-883a-3092a1f2e133`; Passport:
`ff23831f-4950-44ab-ac90-82847e96d464`; Object generation:
`1786895306215137`; SHA-256:
`7e4bb29731e36aebad5907ce749bad3f0f542df155e39af713d30ed606bba37c`.
The retrieved digest matched exactly. This is a Development/Test service, not a
Production Black Box or remote Event Ledger. `VIDEO READY = NO` pending Public
Demo integration and a complete rehearsal.

## Signed Event to Remote Evidence Continuity — 2026-08-17

| Check | Result |
|---|---|
| Existing Registry signing flow | PASS — `Registry.register_file` created a new `aee.event.v1` Signed Event |
| Pre-seal local Event verification | PASS — Event Hash and RSA signature valid |
| Passport ID continuity | PASS — client, Signed Event, Object metadata, and retrieval matched |
| Event ID continuity | PASS — client, Signed Event, Object metadata, and retrieval matched |
| Content SHA-256 continuity | PASS — Signed Event, server upload calculation, stored metadata, and retrieval matched |
| Remote Object creation | PASS — Cloud Run revision `aee-blackbox-test-00002-9d5` |
| Generation precondition | PASS — duplicate seal HTTP 409; original generation unchanged |
| Retention metadata | PASS — real Google Object retention expiration returned and independently read |
| Signed Event mutation check | PASS — canonical Event bytes unchanged after seal/retrieval |
| Post-seal local Event verification | PASS — Event Hash and RSA signature remained valid |
| Passport mismatch | PASS — HTTP 400; no Object created at mismatched path |
| Event mismatch | PASS — HTTP 400; no Object created at mismatched path |
| Signed Event/file SHA mismatch | PASS — HTTP 400; no Object created |
| Client/Signed Event SHA mismatch | PASS — HTTP 400 |
| Tampered signed field | PASS — existing Registry verification rejected modified `action_type` |

Real continuity evidence used only the public synthetic Version 3 demo image.
Passport `e234b162-6ad7-460f-9795-089f5bf4d807`, Event
`6064588b-b2f6-4119-bd74-8a531977f607`, Event Hash
`sha256:3fa0419494892c28f2ab2984b8d8b8ba24bd63318ce07742c7b95e566be49f77`,
content SHA-256
`7e4bb29731e36aebad5907ce749bad3f0f542df155e39af713d30ed606bba37c`,
and Google Object generation `1786898417902863` matched across the full flow.
Cloud Run audit logs recorded seal, retrieval, rejected mismatches, and duplicate
seal without recording evidence bytes, credentials, tokens, or private keys.
This remains Development/Test; `VIDEO READY = NO` pending a controlled
user-operable Demo path and complete no-edit rehearsal.

## Development Evidence Continuity Demo UI — 2026-08-17

| Check | Result |
|---|---|
| Public Development Demo UI | PASS — `https://aee-continuity-demo-856572888721.asia-east1.run.app` |
| Built-in evidence selection | PASS — only bundled synthetic ProofCart Version 3 accepted |
| Existing AEE Registry signing | PASS — real `aee.event.v1`, RSA signature valid before seal |
| Browser credential boundary | PASS — no Google token or credential exposed to browser |
| Backend service identity | PASS — dedicated `aee-continuity-demo` identity |
| Black Box IAM boundary | PASS — demo identity has only service-level Cloud Run Invoker |
| Project/Test-Bucket role for demo identity | PASS — none |
| Google Cloud seal | PASS — real Object created in existing Development/Test Bucket |
| Generation and retention display | PASS — real Google values rendered in UI |
| Retrieval and SHA-256 reverification | PASS — `hash_match=true` |
| Post-seal Signed Event verification | PASS — signature/Event Hash valid and Event unchanged |
| Evidence Continuity | PASS — UI and API both returned PASS |
| Desktop browser interaction | PASS — real button click and complete result inspected |
| Mobile 390 px layout | PASS — no horizontal overflow; evidence image and action visible |

Browser-operated evidence: Passport `a91dc2a0-36df-4a58-bb12-97aa4e94bba4`,
Event `1532be92-f70a-4c3f-a3fc-42226a524ceb`, Object generation
`1786904222644809`, and content SHA-256
`7e4bb29731e36aebad5907ce749bad3f0f542df155e39af713d30ed606bba37c`.
An independent Google Storage metadata read confirmed the same identifiers,
digest, Signed Event Hash reference, generation, and retention expiration.
This remains Development/Test and does not change `VIDEO READY = NO`.

## No-provenance modified image boundary — 2026-08-17

Test Case: `TC-FORENSIC-MODIFIED-NO-PROVENANCE`

| Check | Result |
|---|---|
| Public CC0 source A and deterministic local edit B retained | PASS |
| A/B have no AEE Passport, Signed Event, Registry match, or C2PA claim | PASS |
| Only modified B selected in public Production | PASS — real Chrome interaction |
| Production provenance result | PASS — `UNVERIFIED` / `無法確認來源` |
| Production avoids AI/real/fake guessing | PASS — AI involvement `UNKNOWN` |
| Production single-image edit localization | NOT IMPLEMENTED — no mask/region shown |
| Production single-image edit ratio | NOT IMPLEMENTED — no change percentage shown |
| Production original-source recovery | NOT IMPLEMENTED |
| Offline A/B Ground Truth | PASS — 51,920/3,000,000 pixels, 1.7307%, bbox `1094,1419,272,192` |

The offline A/B number is not a Production forensic result. It is retained only
to prove that B was genuinely modified before the single-image test. Full input,
screenshots, hashes, and required A–F answers are in
`reports/forensic-no-provenance-027/TC_FORENSIC_MODIFIED_NO_PROVENANCE.md`.
