# Test Report

This file records commands and results. It must be updated from actual execution; planned work is never `PASS`.

## Automated core tests

Command: `PYTHONPATH=src python3 -m unittest discover -s tests -v`

Latest result: **PASS — 15/15 Python tests and 3/3 web tests**.

The generated demo report recorded exact retyping at 1.0000 confidence, the approximately 10% edit at 0.8603 (strong), the approximately 30% edit at 0.6218 (medium), and the heavy rewrite at 0.0503 (weak). These are test-fixture measurements, not universal accuracy claims.

Live HTTP run on localhost port 8877 returned: `/register` 201; `/passport`, `/history`, `/issuer`, `/fingerprint/lookup`, `/verify`, and `/revoke` 200. Event verification returned `verified=true`. The temporary server was stopped after testing. Port 8787 was already occupied by an unrelated local application and was not modified.

## Integration status

| Capability | Status | Evidence |
|---|---|---|
| Text DNA exact/retyping | PASS | Automated test + demo report |
| Approximate text relationship | PASS | 10%, 30%, heavy-rewrite fixture results descend |
| Common phrase guard | PASS | Short common phrase is not strong evidence |
| RSA-2048/SHA-256 sign/verify | PASS | Real OpenSSL signing and verification |
| Tamper detection | PASS | Modified event fails verification |
| Parent chain | PASS | Parent event/hash verified |
| Registry HTTP API | PASS | Seven requested route families returned expected HTTP status |
| C2PA create/sign/embed/read/verify | PASS | `c2patool 0.27.12`; third image contains 3 manifests |
| C2PA to Registry event link | PASS | Custom assertion event ID equals signed Registry event ID |
| Modified asset rejection | PASS | Tampered PNG returns `assertion.dataHash.mismatch`; browser shows Invalid Signature |
| Image modification mask | PASS | Local object, full background, and noise threshold tests |
| Verifier website build | PASS | vinext production build and rendered HTML tests |
| Browser Try Demo | PASS | Modified result, 3-version history, 4.8% mask, C2PA and Registry shown |
| Browser signed upload | PASS | Signed v3 parsed as 3 manifests and matched `proofcart-v3` |
| Browser unsigned upload | PASS | Shows Unknown and 0 manifests |
| Upload security boundary | PASS | Types, 10 MB limit, local SHA-256/C2PA, no upload endpoint, rate limiter |
| Google SynthID | NOT INTEGRATED | No official unrestricted general verification API confirmed |
| OpenAI provenance API | NOT INTEGRATED | No public third-party Verify API confirmed |
| Image history/masks | PASS | Three real signed versions and two generated diff masks |
| Video prototype | NOT IMPLEMENTED | Deferred behind image/text/black-box core |
