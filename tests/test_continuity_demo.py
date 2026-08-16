import hashlib
import importlib.util
import os
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
APP_PATH = ROOT / "services" / "continuity_demo" / "app.py"
SPEC = importlib.util.spec_from_file_location("aee_continuity_demo", APP_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class FakeRemoteClient:
    def __init__(self):
        self.event = None

    def seal(self, event, evidence_path):
        digest = hashlib.sha256(evidence_path.read_bytes()).hexdigest()
        if event["exact_hash"] != digest:
            raise AssertionError("event and file digest differ")
        self.event = event
        return {
            "passport_id": event["passport_id"],
            "event_id": event["event_id"],
            "content_sha256": digest,
            "signed_event_hash": event["event_hash"],
            "object_path": f"evidence/{event['passport_id']}/{event['event_id']}",
            "generation": "123456",
            "metageneration": 1,
            "retention_expiration": "2026-08-17T01:00:00+00:00",
            "storage_location": "ASIA-EAST1",
        }

    def retrieve(self, passport_id, event_id):
        return {
            "passport_id": passport_id,
            "event_id": event_id,
            "generation": "123456",
            "stored_sha256": self.event["exact_hash"],
            "retrieved_sha256": self.event["exact_hash"],
            "signed_event_hash": self.event["event_hash"],
            "hash_match": True,
        }


class ContinuityDemoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.asset = ROOT / "apps" / "web" / "public" / "demo" / "version-3.png"

    def setUp(self):
        MODULE.remote_client_factory = FakeRemoteClient
        MODULE.attempts.clear()
        MODULE.app.config.update(TESTING=True)
        self.client = MODULE.app.test_client()

    def test_real_registry_event_survives_continuity_flow(self):
        result = MODULE.run_continuity(self.asset)
        self.assertEqual(result["evidence_continuity"], "PASS")
        self.assertEqual(result["signed_event"]["schema_version"], "aee.event.v1")
        self.assertTrue(result["signed_event"]["pre_seal_signature_valid"])
        self.assertTrue(result["signed_event"]["post_seal_signature_valid"])
        self.assertTrue(result["signed_event"]["event_unchanged"])
        self.assertTrue(result["retrieval"]["hash_match"])
        self.assertEqual(result["retrieval"]["stored_sha256"], result["retrieval"]["retrieved_sha256"])

    def test_api_only_accepts_built_in_asset(self):
        invalid = self.client.post("/v1/demo/continuity", json={"asset_id": "arbitrary-file"})
        self.assertEqual(invalid.status_code, 400)
        valid = self.client.post("/v1/demo/continuity", json={"asset_id": "proofcart-version-3"})
        self.assertEqual(valid.status_code, 200)
        self.assertEqual(valid.json["evidence_continuity"], "PASS")

    def test_ui_and_health_declare_development_boundary(self):
        page = self.client.get("/")
        self.assertEqual(page.status_code, 200)
        page_data = page.data
        page.close()
        self.assertIn(b"DEVELOPMENT / TEST", page_data)
        self.assertIn(b'<select id="asset">', page_data)
        self.assertIn("不接受或上傳使用者檔案".encode("utf-8"), page_data)
        health = self.client.get("/health")
        self.assertEqual(health.json["environment"], "Development / Test")
        self.assertEqual(health.json["remote_blackbox"], "IAM protected")


if __name__ == "__main__":
    unittest.main()
