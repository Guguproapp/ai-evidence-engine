#!/usr/bin/env python3
import argparse
import copy
import hashlib
import json
import mimetypes
import os
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from ai_evidence.canonical import canonical_json
from ai_evidence.registry import Registry


def identity_token():
    configured = os.getenv("AEE_ID_TOKEN", "").strip()
    if configured:
        return configured
    completed = subprocess.run(
        ["gcloud", "auth", "print-identity-token"],
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def request_json(url, token, body, content_type="application/json"):
    request = Request(
        url,
        data=body,
        headers={"Authorization": f"Bearer {token}", "Content-Type": content_type},
        method="POST",
    )
    try:
        with urlopen(request, timeout=60) as response:
            return response.status, json.loads(response.read())
    except HTTPError as error:
        return error.code, json.loads(error.read())


def multipart(fields, file_field, filename, content_type, data):
    boundary = "----aee-" + uuid.uuid4().hex
    chunks = []
    for name, value in fields.items():
        chunks.extend(
            [
                f"--{boundary}\r\n".encode(),
                f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode(),
                str(value).encode(),
                b"\r\n",
            ]
        )
    chunks.extend(
        [
            f"--{boundary}\r\n".encode(),
            f'Content-Disposition: form-data; name="{file_field}"; filename="{filename}"\r\n'.encode(),
            f"Content-Type: {content_type}\r\n\r\n".encode(),
            data,
            b"\r\n",
            f"--{boundary}--\r\n".encode(),
        ]
    )
    return b"".join(chunks), f"multipart/form-data; boundary={boundary}"


def seal(service_url, token, path, signed_event, passport_id=None, event_id=None, digest=None, extra_fields=None):
    data = path.read_bytes()
    content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    fields = {
        "schema_version": "aee.event.v1",
        "passport_id": passport_id or signed_event["passport_id"],
        "event_id": event_id or signed_event["event_id"],
        "content_sha256": digest or signed_event["exact_hash"],
        "content_type": content_type,
        "signed_event": canonical_json(signed_event).decode("utf-8"),
    }
    fields.update(extra_fields or {})
    body, multipart_type = multipart(fields, "evidence_file", path.name, content_type, data)
    return request_json(service_url + "/v1/evidence/seal", token, body, multipart_type)


def retrieve(service_url, token, passport_id, event_id, extra=None):
    payload = {"passport_id": passport_id, "event_id": event_id}
    payload.update(extra or {})
    return request_json(service_url + "/v1/evidence/retrieve", token, json.dumps(payload).encode())


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def create_signed_event(registry, path, *, action_type="remote_seal_test"):
    content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return registry.register_file(
        path,
        asset_type="image",
        media_type=content_type,
        evidence_profile="aee.image.c2pa.v1",
        c2pa_manifest_id="urn:aee:c2pa:test:" + str(uuid.uuid4()),
        provider="gugupro",
        model="aee-continuity-test-client",
        model_version="1",
        action_type=action_type,
        involvement_level="L0",
        operator_type="program",
        human_approval=True,
        blackbox_available=False,
    )


def main():
    parser = argparse.ArgumentParser(description="AEE Remote Black Box real Development/Test E2E")
    parser.add_argument("--service-url", required=True)
    parser.add_argument("--file", required=True, type=Path)
    args = parser.parse_args()
    service_url = args.service_url.rstrip("/")
    data = args.file.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    token = identity_token()

    with tempfile.TemporaryDirectory(prefix="aee-continuity-") as temp_dir:
        temp = Path(temp_dir)
        registry = Registry(temp / "registry", temp / "keys", issuer_id="gugupro-continuity-test")
        event = create_signed_event(registry, args.file)
        event_snapshot = copy.deepcopy(event)
        event_bytes_before = canonical_json(event)
        pre_verify = registry.verify_event(event)
        require(pre_verify["verified"] and pre_verify["signature_valid"] and pre_verify["hash_valid"], "local Signed Event failed pre-seal verification")
        require(event["schema_version"] == "aee.event.v1", "Registry did not create aee.event.v1")
        require(event["exact_hash"] == digest, "Signed Event content SHA-256 does not match evidence")

        passport_id = event["passport_id"]
        event_id = event["event_id"]
        status, sealed = seal(service_url, token, args.file, event)
        require(status == 201 and sealed.get("ok"), f"sealEvidence failed: {status} {sealed}")
        require(sealed.get("passport_id") == passport_id, "sealed Passport ID changed")
        require(sealed.get("event_id") == event_id, "sealed Event ID changed")
        require(sealed.get("content_sha256") == digest, "sealEvidence returned a different SHA-256")
        require(sealed.get("signed_event_hash") == event["event_hash"], "sealEvidence returned a different Event Hash")
        require(sealed.get("generation"), "sealEvidence did not return generation")
        require(sealed.get("retention_expiration"), "sealEvidence did not return retention metadata")

        status, retrieved = retrieve(service_url, token, passport_id, event_id)
        require(status == 200 and retrieved.get("ok"), f"retrieveEvidence failed: {status} {retrieved}")
        require(retrieved.get("hash_match") is True, "retrieved hash did not match")
        require(retrieved.get("stored_sha256") == digest, "stored SHA-256 did not match")
        require(retrieved.get("retrieved_sha256") == digest, "retrieved SHA-256 did not match")
        require(retrieved.get("schema_version") == event["schema_version"], "retrieved Schema Version did not match")
        require(retrieved.get("passport_id") == passport_id, "retrieved Passport ID changed")
        require(retrieved.get("event_id") == event_id, "retrieved Event ID changed")
        require(retrieved.get("signed_event_hash") == event["event_hash"], "retrieved Event Hash reference did not match")

        mismatched_passport = str(uuid.uuid4())
        status, bad_passport = seal(service_url, token, args.file, event, passport_id=mismatched_passport)
        require(status == 400 and bad_passport.get("error") == "invalid_request", "Signed Event Passport mismatch was not rejected")
        status, absent_passport = retrieve(service_url, token, mismatched_passport, event_id)
        require(status == 404 and absent_passport.get("error") == "evidence_not_found", "Passport mismatch created an object")

        mismatched_event = str(uuid.uuid4())
        status, bad_event = seal(service_url, token, args.file, event, event_id=mismatched_event)
        require(status == 400 and bad_event.get("error") == "invalid_request", "Signed Event Event ID mismatch was not rejected")
        status, absent_event = retrieve(service_url, token, passport_id, mismatched_event)
        require(status == 404 and absent_event.get("error") == "evidence_not_found", "Event ID mismatch created an object")

        alternate_path = temp / "alternate.png"
        alternate_path.write_bytes(data + b"alternate")
        alternate_event = create_signed_event(registry, alternate_path, action_type="negative_file_hash_test")
        status, bad_file_hash = seal(service_url, token, args.file, alternate_event)
        require(status == 400 and bad_file_hash.get("error") == "invalid_request", "Signed Event/file SHA mismatch was not rejected")
        status, absent_file_hash = retrieve(service_url, token, alternate_event["passport_id"], alternate_event["event_id"])
        require(status == 404 and absent_file_hash.get("error") == "evidence_not_found", "file SHA mismatch created an object")

        wrong_digest = "0" * 64 if digest != "0" * 64 else "1" * 64
        status, bad_claim = seal(service_url, token, args.file, event, digest=wrong_digest)
        require(status == 400 and bad_claim.get("error") == "invalid_request", "Client/Signed Event SHA mismatch was not rejected")

        tampered_event = copy.deepcopy(event)
        tampered_event["action_type"] = "tampered_action"
        tampered_verify = registry.verify_event(tampered_event)
        require(not tampered_verify["signature_valid"] and not tampered_verify["verified"], "tampered Signed Event was not rejected by Registry verification")

        status, duplicate = seal(service_url, token, args.file, event)
        require(status == 409 and duplicate.get("error") == "evidence_already_sealed", "duplicate seal was not rejected")
        status, after_duplicate = retrieve(service_url, token, passport_id, event_id)
        require(status == 200 and after_duplicate.get("generation") == sealed.get("generation"), "duplicate seal changed the generation")

        post_verify = registry.verify_event(event)
        require(post_verify["verified"] and post_verify["signature_valid"] and post_verify["hash_valid"], "local Signed Event failed post-seal verification")
        require(event == event_snapshot and canonical_json(event) == event_bytes_before, "Remote operations modified the local Signed Event")

        result = {
            "environment": "Development / Test",
            "passport_id": passport_id,
            "event_id": event_id,
            "object_path": sealed["object_path"],
            "generation": sealed["generation"],
            "retention_expiration": sealed["retention_expiration"],
            "content_sha256": digest,
            "retrieved_sha256": retrieved["retrieved_sha256"],
            "hash_match": retrieved["hash_match"],
            "signed_event_hash": event["event_hash"],
            "local_signed_event": {
                "schema_version": event["schema_version"],
                "pre_seal_signature_valid": pre_verify["signature_valid"],
                "pre_seal_hash_valid": pre_verify["hash_valid"],
                "post_seal_signature_valid": post_verify["signature_valid"],
                "post_seal_hash_valid": post_verify["hash_valid"],
                "event_unchanged": event == event_snapshot,
            },
            "negative_tests": {
                "passport_id_mismatch": "PASS",
                "event_id_mismatch": "PASS",
                "signed_event_file_sha256_mismatch": "PASS",
                "client_signed_event_sha256_mismatch": "PASS",
                "tampered_signed_event_verification": "PASS",
                "duplicate_seal": "PASS",
                "generation_unchanged": "PASS",
            },
            "continuity": "PASS",
            "e2e": "PASS",
        }
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(json.dumps({"e2e": "FAIL", "error": str(error)}, ensure_ascii=False), file=sys.stderr)
        raise
