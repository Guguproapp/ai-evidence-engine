import re
from collections import Counter
from difflib import SequenceMatcher

from .canonical import exact_text_hash, normalize_text, sha256_bytes


def _sentences(text):
    return [part.strip() for part in re.split(r"(?<=[。！？.!?])\s*|\n+", text) if part.strip()]


def _paragraphs(text):
    return [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()]


def _tokens(text):
    normalized = normalize_text(text)
    return re.findall(r"[A-Za-z0-9_]+|[\u3400-\u9fff]", normalized, re.UNICODE)


def _ngrams(tokens, size=5):
    return [" ".join(tokens[index:index + size]) for index in range(max(0, len(tokens) - size + 1))]


def fingerprint_text(text, ngram_size=5):
    sentences = _sentences(text)
    paragraphs = _paragraphs(text)
    tokens = _tokens(text)
    ngrams = _ngrams(tokens, ngram_size)
    return {
        "exact_hash": exact_text_hash(text),
        "sentence_hashes": [exact_text_hash(value) for value in sentences],
        "paragraph_hashes": [exact_text_hash(value) for value in paragraphs],
        "ngram_size": ngram_size,
        "ngram_hashes": [sha256_bytes(value.encode("utf-8")) for value in ngrams],
        "token_count": len(tokens),
        "sentence_count": len(sentences),
        "paragraph_count": len(paragraphs),
    }


def compare_text(source, candidate, ngram_size=5):
    source_normalized = normalize_text(source)
    candidate_normalized = normalize_text(candidate)
    if source_normalized == candidate_normalized:
        return _result("exact_match", 1.0, 1.0, 1.0, "strong")

    source_tokens = _tokens(source)
    candidate_tokens = _tokens(candidate)
    source_ngrams = Counter(_ngrams(source_tokens, ngram_size))
    candidate_ngrams = Counter(_ngrams(candidate_tokens, ngram_size))
    overlap = sum((source_ngrams & candidate_ngrams).values())
    source_total = max(1, sum(source_ngrams.values()))
    candidate_total = max(1, sum(candidate_ngrams.values()))
    source_coverage = overlap / source_total
    candidate_coverage = overlap / candidate_total
    sequence = SequenceMatcher(None, source_normalized, candidate_normalized).ratio()

    blocks = SequenceMatcher(None, source_tokens, candidate_tokens).get_matching_blocks()
    longest = max((block.size for block in blocks), default=0)
    continuous = longest / max(1, len(source_tokens))

    if continuous >= 0.60 and source_coverage >= 0.70:
        tier, strength = "large_continuous_match", "strong"
    elif source_coverage >= 0.40 and candidate_coverage >= 0.40:
        tier, strength = "partial_match", "medium"
    elif sequence >= 0.55 or source_coverage >= 0.20:
        tier, strength = "approximate_rewrite", "possible"
    else:
        tier, strength = "semantic_similarity_only", "weak"

    confidence = round(0.50 * source_coverage + 0.30 * sequence + 0.20 * continuous, 4)
    return _result(tier, confidence, source_coverage, continuous, strength, candidate_coverage, sequence)


def _result(tier, confidence, source_coverage, continuous, strength, candidate_coverage=1.0, sequence=1.0):
    return {
        "evidence_tier": tier,
        "evidence_strength": strength,
        "confidence": round(confidence, 4),
        "source_ngram_coverage": round(source_coverage, 4),
        "candidate_ngram_coverage": round(candidate_coverage, 4),
        "longest_continuous_ratio": round(continuous, 4),
        "character_similarity": round(sequence, 4),
        "legal_plagiarism_verdict": None,
        "notice": "Provenance similarity only; this is not a copyright, infringement, or plagiarism judgment.",
    }
