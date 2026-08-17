import base64
import hashlib
import importlib.util
import io
import json
import os
import sys
import unittest
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path


APP_PATH = Path(__file__).parents[1] / "services" / "blackbox" / "app.py"
SPEC = importlib.util.spec_from_file_location("aee_blackbox_app", APP_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class PreconditionFailed(Exception):
    code = 412


class NotFound(Exception):
    code = 404


class FakeRecord:
    def __init__(self, data, content_type, metadata, generation):
        now = datetime.now(timezone.utc)
        self.data = data
        self.content_type = content_type
        self.metadata = dict(metadata or {})
        self.generation = generation
        self.metageneration = 1
        self.size = len(data)
        self.time_created = now
        self.retention_expiration_time = now + timedelta(minutes=10)


class FakeBlob:
    def __init__(self, records, name):
        self.records = records
        self.name = name
        self.metadata = None

    def upload_from_string(self, data, content_type, if_generation_match):
        if if_generation_match != 0:
            raise AssertionError("seal must use ifGenerationMatch=0")
        if self.name in self.records:
            raise PreconditionFailed()
        self.records[self.name] = FakeRecord(data, content_type, self.metadata, len(self.records) + 100)
        self._load()

    def reload(self):
        if self.name not in self.records:
            raise NotFound()
        self._load()

    def download_as_bytes(self):
        if self.name not in self.records:
            raise NotFound()
        return self.records[self.name].data

    def _load(self):
        record = self.records[self.name]
        self.metadata = dict(record.metadata)
        self.content_type = record.content_type
        self.generation = record.generation
        self.metageneration = record.metageneration
        self.size = record.size
        self.time_created = record.time_created
        self.retention_expiration_time = record.retention_expiration_time


class FakeBucket:
    def __init__(self, records):
        self.records = records

    def blob(self, name):
        return FakeBlob(self.records, name)


class FakeStorageClient:
    def __init__(self):
        self.records = {}

    def bucket(self, _name):
        return FakeBucket(self.records)

    def list_blobs(self, _name, prefix):
        return [FakeBlob(self.records, name) for name in sorted(self.records) if name.startswith(prefix)]


class BlackBoxApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.png = b"\x89PNG\r\n\x1a\n" + b"synthetic-aee-test"
        cls.digest = hashlib.sha256(cls.png).hexdigest()

    def setUp(self):
        self.storage = FakeStorageClient()
        MODULE.storage_client_factory = lambda: self.storage
        os.environ["EVIDENCE_BUCKET"] = "aee-blackbox-unit-test"
        MODULE.app.config.update(TESTING=True)
        self.client = MODULE.app.test_client()
        self.passport_id = str(uuid.uuid4())
        self.event_id = str(uuid.uuid4())
        self.signed_event = {
            "schema_version": "aee.event.v1",
            "passport_id": self.passport_id,
            "event_id": self.event_id,
            "exact_hash": self.digest,
            "content_digest": "sha256:" + self.digest,
            "event_hash": "sha256:" + "a" * 64,
            "signature_algorithm": "RSA-2048/SHA-256",
            "signature": "unit-test-signature",
            "parent_event": None,
            "action_type": "remote_seal_test",
        }
        self.public_key = "-----BEGIN PUBLIC KEY-----\ndW5pdC10ZXN0\n-----END PUBLIC KEY-----\n"

    def seal(self, **overrides):
        fields = {
            "schema_version": "aee.event.v1",
            "passport_id": self.passport_id,
            "event_id": self.event_id,
            "content_sha256": self.digest,
            "content_type": "image/png",
            "signed_event": json.dumps(self.signed_event),
            "issuer_public_key": self.public_key,
            "evidence_file": (io.BytesIO(self.png), "evidence.png"),
        }
        fields.update(overrides)
        return self.client.post("/v1/evidence/seal", data=fields, content_type="multipart/form-data")

    def retrieve(self, **overrides):
        payload = {"passport_id": self.passport_id, "event_id": self.event_id}
        payload.update(overrides)
        return self.client.post("/v1/evidence/retrieve", json=payload)

    def test_seal_and_retrieve_reverify_sha256(self):
        sealed = self.seal()
        self.assertEqual(sealed.status_code, 201)
        self.assertTrue(sealed.json["ok"])
        self.assertTrue(sealed.json["generation"])
        self.assertTrue(sealed.json["retention_expiration"])
        self.assertNotIn("credential", sealed.json)
        retrieved = self.retrieve()
        self.assertEqual(retrieved.status_code, 200)
        self.assertTrue(retrieved.json["hash_match"])
        self.assertEqual(retrieved.json["stored_sha256"], self.digest)
        self.assertEqual(retrieved.json["retrieved_sha256"], self.digest)
        self.assertEqual(retrieved.json["signed_event_hash"], self.signed_event["event_hash"])
        record = next(iter(self.storage.records.values()))
        self.assertEqual(record.metadata["passport_id"], self.passport_id)
        self.assertEqual(record.metadata["event_id"], self.event_id)
        self.assertEqual(record.metadata["content_sha256"], self.digest)
        self.assertEqual(record.metadata["signed_event_hash"], self.signed_event["event_hash"])
        self.assertEqual(json.loads(record.metadata["signed_event"])["event_id"], self.event_id)

    def test_history_and_download_reconstruct_persistent_record(self):
        self.assertEqual(self.seal().status_code, 201)
        history = self.client.post(
            "/v1/evidence/history",
            json={"passport_id": self.passport_id, "event_id": self.event_id},
        )
        self.assertEqual(history.status_code, 200)
        self.assertEqual(history.json["events"][0]["signed_event"]["event_id"], self.event_id)
        self.assertEqual(history.json["events"][0]["issuer_public_key"], self.public_key)
        downloaded = self.client.post(
            "/v1/evidence/download",
            json={"passport_id": self.passport_id, "event_id": self.event_id},
        )
        self.assertEqual(downloaded.status_code, 200)
        self.assertEqual(base64.b64decode(downloaded.json["evidence_base64"]), self.png)
        self.assertEqual(downloaded.json["content_sha256"], self.digest)

    def test_wrong_sha256_is_rejected_without_object(self):
        response = self.seal(content_sha256="0" * 64)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.storage.records, {})

    def test_client_passport_must_match_signed_event(self):
        response = self.seal(passport_id=str(uuid.uuid4()))
        self.assertEqual(response.status_code, 400)
        self.assertIn("passport_id does not match", response.json["message"])
        self.assertEqual(self.storage.records, {})

    def test_client_event_must_match_signed_event(self):
        response = self.seal(event_id=str(uuid.uuid4()))
        self.assertEqual(response.status_code, 400)
        self.assertIn("event_id does not match", response.json["message"])
        self.assertEqual(self.storage.records, {})

    def test_signed_event_hash_must_match_file(self):
        event = dict(self.signed_event)
        event["exact_hash"] = "0" * 64
        event["content_digest"] = "sha256:" + "0" * 64
        response = self.seal(content_sha256="0" * 64, signed_event=json.dumps(event))
        self.assertEqual(response.status_code, 400)
        self.assertIn("evidence_file SHA-256", response.json["message"])
        self.assertEqual(self.storage.records, {})

    def test_client_hash_must_match_signed_event(self):
        response = self.seal(content_sha256="0" * 64)
        self.assertEqual(response.status_code, 400)
        self.assertIn("content_sha256 does not match signed_event", response.json["message"])
        self.assertEqual(self.storage.records, {})

    def test_signed_event_is_required(self):
        response = self.seal(signed_event="")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.storage.records, {})

    def test_duplicate_seal_is_rejected_and_generation_is_unchanged(self):
        original = self.seal().json
        duplicate = self.seal()
        self.assertEqual(duplicate.status_code, 409)
        self.assertEqual(duplicate.json["error"], "evidence_already_sealed")
        self.assertEqual(self.retrieve().json["generation"], original["generation"])

    def test_invalid_identifiers_are_rejected(self):
        self.assertEqual(self.seal(passport_id="../bad").status_code, 400)
        self.assertEqual(self.seal(event_id="not-a-uuid").status_code, 400)

    def test_client_cannot_inject_storage_controls(self):
        response = self.seal(object_path="../../arbitrary", bucket="other-bucket")
        self.assertEqual(response.status_code, 400)
        self.assertIn("client-controlled storage fields", response.json["message"])
        self.assertEqual(self.storage.records, {})


if __name__ == "__main__":
    unittest.main()
