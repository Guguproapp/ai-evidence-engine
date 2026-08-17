# Final Production Snapshot

Snapshot time: 2026-08-18 (before deadline)

| Item | Value | Status |
|---|---|---|
| Public Production | https://ai-evidence-engine-gugupro.artistuncle.chatgpt.site | HTTP 200 READY |
| English UI | Header EN switch and English dictionary in deployed bundle | READY |
| Login / paywall | None | READY |
| Public GitHub | https://github.com/Guguproapp/ai-evidence-engine | HTTP 200 READY |
| GitHub HEAD at audit | `27d73634ea61982cdd33eb5dca608ab870b8d106` | READY |
| Production source baseline | `27d73634ea61982cdd33eb5dca608ab870b8d106` per Engineering Freeze checkpoint | READY, hosting Git SHA not public |
| Cloud Run explainer | `ai-evidence-explainer-00003-m75` | READY, 100% traffic |
| Gemini model | `gemini-2.5-flash` on Vertex AI | READY |
| Cloud project | `ai-evidence-engine-gugupro` | READY |
| Development/Test continuity | https://aee-continuity-demo-856572888721.asia-east1.run.app | HTTP 200 READY AS PROTOTYPE |
| Final YouTube | https://youtu.be/LJh42-gYD4U | PRIVATE / MISSING for submission |

The public site response exposes a deployment artifact identifier, not a Git commit. The source baseline above is taken from the accepted deployment checkpoint and must not be described as independently proven by the public hosting response.
