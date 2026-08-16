# Google Play Data Safety Draft

Status: code/network/SDK audit completed for current source; final answers must be re-audited against the built AAB, merged manifest, production logging settings, and current Play Console wording.

Official reference: https://support.google.com/googleplay/android-developer/answer/10787469

## Audited behavior

- Selected images are read by browser APIs for local SHA-256 and C2PA processing. No file upload, `FormData`, or server image endpoint exists.
- `aee_locale` is stored locally for language preference.
- Optional Gemini explanation sends an allowlisted JSON object of verification facts to Cloud Run.
- Cloud Run logs request ID, Evidence ID, deterministic status, Gemini model, and latency. It does not intentionally log original image bytes or the generated prompt body.
- Android Browser Helper shares the launched URL with the user's browser. Its current disclosure says the library itself does not transfer data over the network; browser/service behavior still requires final AAB/SDK review.
- No account, ads SDK, analytics SDK, crash SDK, location delegation, billing SDK, or push-notification SDK is configured.

## Draft classification

| Play data type | Status | Collected / shared | Required / optional | Processing / purpose |
|---|---|---|---|---|
| Photos and videos | NOT COLLECTED off device | Not shared by AEE; selected locally | Optional user action | Local app functionality only |
| Files and docs | NOT COLLECTED off device | Not shared | Optional | Local verification only |
| Personal info | NOT COLLECTED | Not shared | N/A | No account/contact form |
| Device or other IDs | NOT COLLECTED by app source | Browser/cloud request metadata requires final platform review | N/A | No advertising ID SDK |
| App activity / interactions | COLLECTED when Gemini explanation is requested | NOT SHARED for advertising; sent to service provider Google Cloud | Optional | App functionality, security, diagnostics |
| Other user-generated content / structured verification facts | COLLECTED | NOT SHARED beyond service-provider processing | Optional | Gemini explanation |
| Crash logs | NOT COLLECTED by dedicated SDK | Cloud service errors may be logged | N/A | Diagnostics |
| Diagnostics | COLLECTED server-side | NOT SHARED for advertising | Required for Cloud request | Security, reliability, debugging |
| Approximate location | NOT COLLECTED intentionally | IP address may exist in standard infrastructure metadata | N/A | Rate limiting/security; verify final Console interpretation |

## Security and deletion

- HTTPS is used in transit.
- No app account exists, so account-deletion requirements are not triggered by current functionality.
- Users can clear local language data through Android/browser site settings.
- A support channel and final retention/deletion process require owner confirmation before submission.

Final Play answers remain **OWNER CONFIRMATION REQUIRED** because Google makes the developer responsible for declarations, and the form wording can change.
