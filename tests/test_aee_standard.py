import copy
import json
import tempfile
import unittest
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

from ai_evidence.authorization import sign_authorization, validate_authorization
from ai_evidence.canonical import canonical_json, sha256_bytes
from ai_evidence.crypto import sign_bytes
from ai_evidence.decision import decide_evidence
from ai_evidence.identifiers import (
    authorization_identifier, digest_identifier, event_identifier,
    is_canonical_aee_identifier, is_canonical_digest, passport_identifier,
    device_identifier, issuer_identifier,
)
from ai_evidence.profiles import IMPLEMENTED, SPECIFIED_NOT_IMPLEMENTED, resolve_profile
from ai_evidence.registry import LEGACY_PUBLIC_EVENT_FIELDS, Registry, normalize_legacy_event
from ai_evidence.schema import validate_event_v1
from ai_evidence.wallet import verify_wallet_commitment, wallet_commitment


class IdentifierAndCanonicalTests(unittest.TestCase):
    def test_identifier_formats(self):
        value = uuid.uuid4()
        self.assertTrue(is_canonical_aee_identifier(passport_identifier(value)))
        self.assertTrue(is_canonical_aee_identifier(event_identifier(value)))
        self.assertTrue(is_canonical_aee_identifier(authorization_identifier(value)))
        self.assertTrue(is_canonical_aee_identifier(device_identifier(value)))
        self.assertEqual(issuer_identifier("gugupro-demo"), "urn:aee:issuer:v1:gugupro-demo")
        with self.assertRaises(ValueError):
            device_identifier("personal-device-serial")
        with self.assertRaises(ValueError):
            issuer_identifier("person@example.com")

    def test_digest_format(self):
        value = digest_identifier("ab" * 32)
        self.assertEqual(value, "sha256:" + "ab" * 32)
        self.assertTrue(is_canonical_digest(value))
        with self.assertRaises(ValueError):
            digest_identifier("not-a-digest")

    def test_canonical_json_and_hash_are_stable(self):
        left = {"b": 2, "a": {"y": "證據", "x": 1}}
        right = {"a": {"x": 1, "y": "證據"}, "b": 2}
        self.assertEqual(canonical_json(left), canonical_json(right))
        self.assertEqual(sha256_bytes(canonical_json(left)), sha256_bytes(canonical_json(right)))


class ProfileAndDecisionTests(unittest.TestCase):
    def test_implemented_profiles_resolve(self):
        self.assertEqual(resolve_profile("aee.text.v1", True).implementation_status, IMPLEMENTED)
        self.assertEqual(resolve_profile("aee.image.c2pa.v1", True).implementation_status, IMPLEMENTED)
        self.assertEqual(resolve_profile("aee.image.firstseen.v1", True).implementation_status, IMPLEMENTED)

    def test_reserved_profiles_cannot_verify(self):
        self.assertEqual(resolve_profile("aee.video.v1").implementation_status, SPECIFIED_NOT_IMPLEMENTED)
        with self.assertRaises(NotImplementedError):
            resolve_profile("aee.video.v1", True)

    def test_original_and_modified_decisions(self):
        base = dict(registry_match=True, signature_valid=True, content_hash_valid=True,
                    parent_chain_valid=True, required_profile_evidence_valid=True,
                    c2pa_present=True, c2pa_integrity_valid=True, identity_trust="DEVELOPMENT")
        self.assertEqual(decide_evidence(**base, has_parent=False)["provenance_state"], "VERIFIED_ORIGINAL")
        self.assertEqual(decide_evidence(**base, has_parent=True)["provenance_state"], "VERIFIED_MODIFIED")

    def test_valid_c2pa_without_registry_is_unverified(self):
        result = decide_evidence(registry_match=False, signature_valid=False, content_hash_valid=False,
                                 parent_chain_valid=False, required_profile_evidence_valid=False,
                                 c2pa_present=True, c2pa_integrity_valid=True)
        self.assertEqual(result["integrity_state"], "UNVERIFIED")
        self.assertEqual(result["provenance_state"], "UNVERIFIED")

    def test_invalid_required_evidence_is_invalid(self):
        result = decide_evidence(registry_match=True, signature_valid=True, content_hash_valid=True,
                                 parent_chain_valid=True, required_profile_evidence_valid=False)
        self.assertEqual(result["integrity_state"], "INVALID")
        self.assertEqual(result["provenance_state"], "INVALID_EVIDENCE")

    def test_signature_hash_and_parent_tampering_are_invalid(self):
        for field in ("signature_valid", "content_hash_valid", "parent_chain_valid"):
            values = dict(registry_match=True, signature_valid=True, content_hash_valid=True,
                          parent_chain_valid=True, required_profile_evidence_valid=True)
            values[field] = False
            self.assertEqual(decide_evidence(**values)["provenance_state"], "INVALID_EVIDENCE")


class RegistryV1AndLegacyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.registry = Registry(root / "data", root / "keys")

    def tearDown(self):
        self.temp.cleanup()

    def test_new_event_has_v1_schema_and_profile(self):
        event = self.registry.register_text("Evidence text", involvement_level="L2")
        self.assertEqual(event["schema_version"], "aee.event.v1")
        self.assertEqual(event["evidence_profile"], "aee.text.v1")
        self.assertEqual(event["public_disclosure_level"], "PUBLIC_MINIMUM")
        self.assertTrue(event["wallet_commitment"].startswith("sha256:"))
        self.assertTrue(event["content_digest"].startswith("sha256:"))
        self.assertTrue(event["event_hash"].startswith("sha256:"))
        self.assertTrue(validate_event_v1(event))
        self.assertTrue(self.registry.verify_event(event)["verified"])

    def test_first_seen_event_preserves_unknown_prior_provenance(self):
        source = Path(self.temp.name) / "first-seen.png"
        source.write_bytes(b"\x89PNG\r\n\x1a\nsynthetic-test")
        event = self.registry.register_file(
            source,
            media_type="image/png",
            evidence_profile="aee.image.firstseen.v1",
            action_type="first_seen_registration",
            provenance_state="UNVERIFIED",
            source_assets=[{"relationship": "first_seen", "prior_provenance": "unknown"}],
        )
        verification = self.registry.verify_event(event)
        self.assertTrue(verification["signature_valid"])
        self.assertTrue(verification["hash_valid"])
        self.assertEqual(verification["integrity_state"], "VALID")
        self.assertEqual(verification["provenance_state"], "UNVERIFIED")
        self.assertIn("prior_provenance_unknown", verification["reasons"])
        self.assertEqual(event["source_assets"][0]["prior_provenance"], "unknown")

    def _legacy(self, event):
        legacy = {key: event[key] for key in LEGACY_PUBLIC_EVENT_FIELDS if key in event}
        payload = canonical_json(legacy)
        legacy["event_hash"] = sha256_bytes(payload)
        legacy["signature_algorithm"] = "RSA-2048/SHA-256"
        legacy["signature"] = sign_bytes(self.registry.private_key, payload)
        return legacy

    def test_legacy_event_read_signature_and_history(self):
        first = self._legacy(self.registry.register_text("legacy one", content_id="legacy-content"))
        second_source = self.registry.register_text("legacy two", content_id="legacy-content")
        second_source["parent_event"] = first["event_id"]
        second_source["parent_hash"] = first["event_hash"]
        second = self._legacy(second_source)
        self.registry.events_path.write_text("\n".join(json.dumps(item) for item in (first, second)) + "\n", encoding="utf-8")
        self.assertEqual(normalize_legacy_event(first)["schema_version"], "legacy")
        self.assertTrue(self.registry.verify_event(first)["signature_valid"])
        self.assertTrue(self.registry.verify_event(second)["parent_valid"])
        self.assertEqual(len(self.registry.history("legacy-content")), 2)


class WalletAndAuthorizationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.registry = Registry(root / "data", root / "keys")

    def tearDown(self):
        self.temp.cleanup()

    def test_wallet_commitment_detects_modified_bundle(self):
        bundle = {"prompt": "private", "seed": 7}
        commitment = wallet_commitment(bundle)
        self.assertTrue(verify_wallet_commitment(bundle, commitment))
        changed = copy.deepcopy(bundle)
        changed["seed"] = 8
        self.assertFalse(verify_wallet_commitment(changed, commitment))

    def _authorization(self):
        now = datetime.now(timezone.utc)
        return sign_authorization({
            "authorization_id": authorization_identifier(uuid.uuid4()),
            "request_id": str(uuid.uuid4()),
            "issuer": "urn:aee:issuer:v1:gugupro-local-dev",
            "requester": "verifier.example",
            "scope": "private-evidence.read",
            "allowed_fields": ["version_history"],
            "denied_fields": ["prompt", "private_source"],
            "created_at": now.isoformat(),
            "expires_at": (now + timedelta(minutes=5)).isoformat(),
            "single_use": True,
            "revoked": False,
        }, self.registry.private_key)

    def test_authorization_valid_and_default_deny(self):
        auth = self._authorization()
        self.assertTrue(validate_authorization(auth, self.registry.public_key, ["version_history"])["valid"])
        denied = validate_authorization(auth, self.registry.public_key, ["prompt"])
        self.assertFalse(denied["valid"])
        self.assertIn("field_not_allowed:prompt", denied["reasons"])

    def test_authorization_expired_revoked_and_single_use(self):
        auth = self._authorization()
        future = datetime.now(timezone.utc) + timedelta(hours=1)
        self.assertIn("authorization_expired", validate_authorization(auth, self.registry.public_key, now=future)["reasons"])
        revoked = dict(auth)
        revoked["revoked"] = True
        self.assertFalse(validate_authorization(revoked, self.registry.public_key)["valid"])
        used = {auth["authorization_id"]}
        self.assertIn("authorization_already_used", validate_authorization(auth, self.registry.public_key, used_authorizations=used)["reasons"])


if __name__ == "__main__":
    unittest.main()
