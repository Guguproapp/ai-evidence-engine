from dataclasses import dataclass


IMPLEMENTED = "IMPLEMENTED"
SPECIFIED_NOT_IMPLEMENTED = "SPECIFIED_NOT_IMPLEMENTED"


@dataclass(frozen=True)
class EvidenceProfile:
    profile_id: str
    asset_type: str
    media_type: str
    canonicalization: tuple
    required_fingerprints: tuple
    optional_fingerprints: tuple
    required_evidence: tuple
    verification_rules: tuple
    change_metrics: tuple
    c2pa_applicability: str
    external_manifest_policy: str
    implementation_status: str


PROFILES = {
    "aee.text.v1": EvidenceProfile(
        "aee.text.v1", "text", "text/plain",
        ("unicode_nfkc", "lowercase", "whitespace_normalization", "strip"),
        ("exact_sha256", "normalized_exact_hash", "paragraph_hashes", "sentence_hashes", "5gram_hashes"),
        ("semantic_evidence",),
        ("signed_registry_event", "content_hash", "event_hash", "signature"),
        ("exact", "partial", "approximate", "semantic_only_is_weak"),
        ("source_coverage", "candidate_coverage", "longest_continuous_ratio", "character_similarity", "relationship_confidence"),
        "OPTIONAL", "External manifest allowed when the text container cannot embed C2PA.", IMPLEMENTED,
    ),
    "aee.image.c2pa.v1": EvidenceProfile(
        "aee.image.c2pa.v1", "image", "image/*",
        ("exact_asset_bytes",),
        ("exact_sha256", "c2pa_hard_binding"),
        ("perceptual_fingerprint", "region_mask"),
        ("signed_registry_event", "content_hash", "event_hash", "signature", "c2pa_manifest"),
        ("registry_match", "signature_valid", "parent_chain_valid", "c2pa_integrity_valid"),
        ("changed_pixels", "total_pixels", "spatial_change_ratio", "changed_region", "bounding_box", "pixel_threshold"),
        "REQUIRED", "External manifest allowed only where embedding is unsupported; policy must be disclosed.", IMPLEMENTED,
    ),
    "aee.image.firstseen.v1": EvidenceProfile(
        "aee.image.firstseen.v1", "image", "image/*",
        ("exact_asset_bytes",),
        ("exact_sha256", "signed_first_seen_event"),
        ("perceptual_fingerprint", "soft_binding", "region_mask"),
        ("signed_registry_event", "content_hash", "event_hash", "signature", "remote_seal_result"),
        ("signature_valid", "content_hash_valid", "remote_retrieval_hash_match", "prior_provenance_remains_unknown"),
        ("first_seen_time", "server_received_time", "seal_time", "spatial_change_ratio", "changed_region"),
        "OPTIONAL", "External Evidence Passport is the primary manifest; future soft-binding recovery may link a C2PA manifest repository.", IMPLEMENTED,
    ),
}


def _reserved(profile_id, asset_type, media_type, metrics, c2pa="WHERE_APPLICABLE"):
    return EvidenceProfile(
        profile_id, asset_type, media_type, ("profile_specific_not_implemented",),
        (), (), ("implementation_required_before_verification",),
        ("MUST_NOT_RETURN_VERIFIED_UNTIL_IMPLEMENTED",), tuple(metrics), c2pa,
        "External Evidence Passport required when the format cannot embed C2PA.", SPECIFIED_NOT_IMPLEMENTED,
    )


PROFILES.update({
    "aee.audio.v1": _reserved("aee.audio.v1", "audio", "audio/*", ("modified_time_ratio", "source_coverage")),
    "aee.video.v1": _reserved("aee.video.v1", "video", "video/*", ("temporal_change_ratio", "spatial_change_ratio", "audio_change_ratio", "source_coverage")),
    "aee.document.v1": _reserved("aee.document.v1", "document", "application/*", ("text_dna", "embedded_media_passports", "document_version_chain")),
    "aee.design2d.v1": _reserved("aee.design2d.v1", "design2d", "application/*", ("object_change", "layer_change", "geometry_change", "text_change")),
    "aee.model3d.v1": _reserved("aee.model3d.v1", "model3d", "model/*", ("geometry_change", "mesh_change", "topology_change", "dimension_change", "material_change")),
    "aee.manufacturing.v1": _reserved("aee.manufacturing.v1", "manufacturing", "application/octet-stream", ("source_design_hash", "derived_model_hash", "slicer_version", "gcode_hash", "printer_device_id", "material", "job_timestamp", "operator", "authorization_id", "manufacturing_signature"), "EXTERNAL_MANIFEST"),
})


def resolve_profile(profile_id, require_implemented=False):
    try:
        profile = PROFILES[profile_id]
    except KeyError as error:
        raise ValueError(f"unknown evidence profile: {profile_id}") from error
    if require_implemented and profile.implementation_status != IMPLEMENTED:
        raise NotImplementedError(f"{profile_id} is SPECIFIED — NOT IMPLEMENTED")
    return profile


def profiles_manifest():
    return {profile_id: profile.__dict__.copy() for profile_id, profile in PROFILES.items()}
