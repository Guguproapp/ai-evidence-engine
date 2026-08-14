# Architecture

## Boundary

```text
Device Passport Agent
  ├─ exact hash + hierarchical fingerprint
  ├─ event + parent hash
  └─ RSA-2048/SHA-256 signature
          │
          ├─ Private Evidence Wallet (content, prompt, input/output, tools)
          │
          └─ Verification Registry (minimum passport proof only)
                         │
                         └─ Verifier (signature, chain, fingerprint evidence)
```

The current prototype runs these parts on one machine while preserving the public/private data boundary. Splitting them into processes later must not cause private Wallet content to be uploaded by default.

## Event semantics

L0 copy/transfer/storage and L1 formatting must not be treated as AI creation. L2 mechanical correction records AI involvement without calling it creative authorship. L3–L5 create a new event and preserve parent-child history whenever content changes materially.

The verifier reports evidence and provenance similarity. It never returns copyright ownership, infringement, plagiarism, legality, or world-truth decisions. Its four provenance outcomes are `Verified Original`, `Verified Modified`, `Unverified`, and `Invalid Evidence`; C2PA integrity, Registry match, and identity trust remain separate signals.

## Cryptography

The development issuer is self-issued and uses RSA-2048 with SHA-256 because this Mac's system OpenSSL lacks Ed25519 support. Its private key remains local with file mode `0600`; the registry publishes the corresponding public key. This proves tamper evidence in the prototype but is not production identity assurance. Production requires protected key storage, certificate policy, rotation, revocation, trust-list governance, and a deliberate algorithm upgrade.

## C2PA alignment

C2PA is the standards adapter for embedded manifests, ingredients, actions, signatures, trust lists, and hard bindings. `scripts/build_image_demo.py` creates true embedded C2PA manifests with `c2patool`, carries the parent asset as an ingredient, and preserves the complete raw read report. The custom C2PA assertion stores the matching AI Evidence Event ID; the Registry separately signs that event and verifies the parent hash.

The public verifier uses `@contentauth/c2pa-web` in a Web Worker/WASM entirely inside the visitor's browser. Selected images are never posted to an application endpoint. The website displays both integrity and identity trust separately: a valid asset hash/signature is not the same as a signer trusted by the official C2PA Trust List.

## Image difference masks

The deterministic demo retains RGB buffers before and after each edit. For every pixel, the maximum channel difference is compared with threshold 12. Changed pixels become white in the mask and red in the comparison overlay; unchanged pixels are black or averaged. The output includes changed pixel count, ratio, and bounding box. This is a visual modification statistic, never a copyright percentage.

## Public demo boundary

The deployed website contains signed public demo images, raw public C2PA reports, registry public evidence, and public keys only. It does not contain the Evidence Wallet source directory, development Registry private key, prompt data, credentials, or API secrets.

## Evidence Explainer submission integration

The optional Evidence Explainer is isolated under `services/explainer/` and targets Google Cloud Run plus the Gemini API on Vertex AI. It receives only an allowlisted structured verification result after the hash, signature, C2PA, Registry, and evidence-chain checks have completed.

Gemini is not in the trust path. The service validates one of four deterministic states (`Verified Original`, `Verified Modified`, `Unverified`, or `Invalid Evidence`), sends the state and facts for plain-language explanation, and returns the original state unchanged. Gemini failures return an explicit service error; no generated fallback is presented as a real model result.

## Universal adapter model

Image is the first implemented adapter, not the product boundary. Text, video, audio, documents, 2D design, 3D models, and digital manufacturing use modality-specific fingerprints and change metrics while sharing the Passport, Event Chain, Hash, Signature, Registry, and Private Wallet foundation. See `EVIDENCE_CLASSIFICATION_SPEC.md` and `MULTIMODAL_EVIDENCE_SPEC.md`.

Private evidence remains encrypted and owner-controlled. The future Mobile Authorization path is explicitly architecture-only: a verifier requests selected fields, the owner approves or denies on a phone, a scoped single-use token is signed, and only authorized evidence is released. It is not represented as implemented in the current demo.
