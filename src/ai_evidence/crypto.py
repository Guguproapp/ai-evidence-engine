import base64
import os
import subprocess
import tempfile
from pathlib import Path


class SigningError(RuntimeError):
    pass


def _run(args, input_bytes=None):
    result = subprocess.run(args, input=input_bytes, capture_output=True)
    if result.returncode != 0:
        raise SigningError(result.stderr.decode("utf-8", errors="replace").strip())
    return result.stdout


def ensure_issuer_keys(key_dir, issuer_id):
    key_dir = Path(key_dir)
    key_dir.mkdir(parents=True, exist_ok=True)
    private_key = key_dir / (issuer_id + "-private.pem")
    public_key = key_dir / (issuer_id + "-public.pem")
    if not private_key.exists():
        _run(["openssl", "genrsa", "-out", str(private_key), "2048"])
        os.chmod(private_key, 0o600)
    if not public_key.exists():
        _run(["openssl", "pkey", "-in", str(private_key), "-pubout", "-out", str(public_key)])
    return private_key, public_key


def sign_bytes(private_key, payload):
    signature = _run(["openssl", "dgst", "-sha256", "-sign", str(private_key)], payload)
    return base64.b64encode(signature).decode("ascii")


def verify_bytes(public_key, payload, signature_b64):
    try:
        signature = base64.b64decode(signature_b64, validate=True)
    except Exception:
        return False
    with tempfile.NamedTemporaryFile() as signature_file:
        signature_file.write(signature)
        signature_file.flush()
        result = subprocess.run(
            ["openssl", "dgst", "-sha256", "-verify", str(public_key), "-signature", signature_file.name],
            input=payload,
            capture_output=True,
        )
    return result.returncode == 0


def public_key_pem(public_key):
    return Path(public_key).read_text(encoding="utf-8")
