import hashlib
import json
import re
import unicodedata


def canonical_json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_bytes(value):
    return hashlib.sha256(value).hexdigest()


def normalize_text(text):
    text = unicodedata.normalize("NFKC", text).lower()
    return re.sub(r"\s+", " ", text).strip()


def exact_text_hash(text):
    return sha256_bytes(normalize_text(text).encode("utf-8"))

