# Android Permission Audit

Principle: request only what V1 needs.

| Permission / capability | Reason | Required | Play declaration | Risk |
|---|---|---:|---|---|
| `INTERNET` | Open production TWA and optional Cloud Run Gemini explanation | Yes | Normal permission; no sensitive-permission form expected | Network metadata and structured facts must match privacy disclosure |
| System file/photo picker | User explicitly chooses PNG/JPEG/WebP | Yes | No broad storage permission | Selected file is handled locally by the webpage |
| Camera | Not used | No | None | Must not be added without a real feature and disclosure |
| Microphone | Not used | No | None | Must not be added |
| Location | Not used | No | None | Must not enable Android Browser Helper location delegation |
| Contacts | Not used | No | None | Must not be added |
| SMS / Call Log | Not used | No | High-risk form avoided | Must not be added |
| `READ_MEDIA_IMAGES` | Not needed with system picker | No | None | Do not add |
| `MANAGE_EXTERNAL_STORAGE` | Not needed | No | Restricted permission avoided | Prohibited for V1 |
| Advertising ID | No ads/analytics SDK | No | Ads declaration = No | Re-audit if any SDK changes |

Manifest audit: only `android.permission.INTERNET` is declared in project source. Final merged-manifest audit remains NOT RUN until dependencies are built.
