# Security Notes

- Localhost-only is the safe default. The prototype API has no authentication, rate limiting, or TLS.
- Development signing keys are generated locally and excluded from Git. They are not production certificates and are not on the C2PA Trust List.
- Private Wallet text is stored locally with `0600` permissions. Disk encryption and OS account security remain external requirements.
- Registry events are append-only by application behavior, not by filesystem enforcement. A production registry needs write-once controls, audit replication, and authenticated administrators.
- Revocation records are prototypes and are not yet bound into a signed transparency log.
- Prompt, input, output, and tool calls must stay in the private Wallet unless the owner explicitly authorizes disclosure.
- Text similarity can produce false positives and false negatives. It must not be used as a legal plagiarism or copyright verdict.
- Secrets, passwords, OAuth tokens, API keys, tax, banking, and identity data must never be committed.
- Browser verification accepts only PNG, JPEG, or WebP and rejects files over 10 MB before C2PA parsing.
- File names are displayed as text only; no name is used as a filesystem path and no uploaded content is executed.
- Upload verification is client-only and has a basic eight-attempts-per-minute browser rate limit to reduce accidental local resource exhaustion. There is no server upload endpoint to attack.
- The deployed demo must contain no private signing key. Production signing requires a remote signer/HSM and a certificate issued under an appropriate trust policy; the built-in development certificate is never labelled trusted.
- Direct `<img>` delivery is intentional for signed assets because an optimizing image proxy could transform bytes and invalidate/remove C2PA credentials.

Report vulnerabilities privately to the project owner. Do not include exploit details in public issues until a fix is available.
