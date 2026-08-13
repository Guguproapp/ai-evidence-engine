# C2PA Adapter Status

Status: **PASS — integrated and tested locally**.

Official components used:

- C2PA specification 2.4.
- CAI-maintained `c2patool 0.27.12`, installed through the official Homebrew formula.
- CAI-maintained `@contentauth/c2pa-web 0.13.4` for private browser-side upload verification.

The image demo creates three PNG versions, embeds one C2PA manifest per version, preserves each parent as a C2PA ingredient, stores the raw C2PA JSON, and links the custom `org.gugupro.ai-evidence` assertion to the existing Registry event ID. The third image contains and validates a three-manifest provenance chain.

The signing credential is the official tool's built-in development signer. Integrity validation passes, but official trust evaluation correctly reports `signingCredential.untrusted`. It is clearly labelled as a development identity and is not represented as production-trusted. No private key is included in the deployed web bundle.
