from .canonical import canonical_json, sha256_bytes
from .identifiers import digest_identifier


def wallet_commitment(private_bundle):
    return digest_identifier(sha256_bytes(canonical_json(private_bundle)))


def verify_wallet_commitment(private_bundle, commitment):
    return wallet_commitment(private_bundle) == commitment
