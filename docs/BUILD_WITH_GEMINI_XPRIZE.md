# Build with Gemini XPRIZE — Official Compliance Checkpoint

Checked against the official Devpost Rules on 2026-08-14.

Official sources:

- Rules: https://xprize.devpost.com/rules
- Event: https://xprize.devpost.com/
- Schedule: https://xprize.devpost.com/details/dates
- FAQ: https://xprize.devpost.com/details/faq
- Resources: https://xprize.devpost.com/resources

## Fixed entry direction

- Category: **Small Business Services**
- Core product: **AI Evidence Engine**
- Commercial use case: **ProofCart**
- Relevance: provenance, edit history, signatures, C2PA evidence, evidence chains, and modification regions help everyday merchants and platforms establish trust in product media.

This event does not require a sponsor challenge selection. The project must instead satisfy the general Project and Submission Requirements in the Official Rules.

## Official mandatory requirements

- Submission period: May 19, 2026 at 10:00 AM PDT through August 17, 2026 at 1:00 PM PDT.
- Category selection is required.
- The project must use at least one Google Cloud product.
- If the project includes LLM functionality, the deployed application must make at least one Gemini API call.
- The repository must contain all necessary source and be public with a relevant license, or private and shared with `testing@devpost.com` and `judging@hacker.fund`.
- The public demonstration video must be under three minutes and show the working product.
- Submission and testing materials must be in English or include complete English translations.
- Revenue, monthly revenue, total expenses, marketing/customer-acquisition spend, related-party revenue, real-user evidence, and evidence of production operation must be disclosed.
- A working project must remain available free of charge and without restriction through the judging period.

## Current truth boundary

- The public verifier is deployed through Sites and calls a production Evidence Explainer hosted on Google Cloud Run.
- The dedicated billing-enabled project is `ai-evidence-engine-gugupro`; the ready Cloud Run revision is in `asia-east1`.
- A real Vertex AI `gemini-2.5-flash` request returned HTTP 200, produced a buyer-facing explanation, and preserved the deterministic verification status.
- Cloud Run, Vertex AI, and public-browser logs are preserved under `docs/evidence/` without secrets.
- Current status is **not Submission Ready** because real external-user evidence, a public URL for the completed under-three-minute video, and final entrant acceptance/submission remain incomplete.
