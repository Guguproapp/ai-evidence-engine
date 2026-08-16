#!/usr/bin/env python3
import argparse
import hashlib
import json
import mimetypes
import os
import subprocess
import sys
import uuid
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen


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


def seal(service_url, token, path, passport_id, event_id, digest, extra_fields=None):
    data = path.read_bytes()
    content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    fields = {
        "schema_version": "aee.event.v1",
        "passport_id": passport_id,
        "event_id": event_id,
        "content_sha256": digest,
        "content_type": content_type,
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


def main():
    parser = argparse.ArgumentParser(description="AEE Remote Black Box real Development/Test E2E")
    parser.add_argument("--service-url", required=True)
    parser.add_argument("--file", required=True, type=Path)
    args = parser.parse_args()
    service_url = args.service_url.rstrip("/")
    data = args.file.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    token = identity_token()

    passport_id = str(uuid.uuid4())
    event_id = str(uuid.uuid4())
    status, sealed = seal(service_url, token, args.file, passport_id, event_id, digest)
    require(status == 201 and sealed.get("ok"), f"sealEvidence failed: {status} {sealed}")
    require(sealed.get("content_sha256") == digest, "sealEvidence returned a different SHA-256")
    require(sealed.get("generation"), "sealEvidence did not return generation")
    require(sealed.get("retention_expiration"), "sealEvidence did not return retention metadata")

    status, retrieved = retrieve(service_url, token, passport_id, event_id)
    require(status == 200 and retrieved.get("ok"), f"retrieveEvidence failed: {status} {retrieved}")
    require(retrieved.get("hash_match") is True, "retrieved hash did not match")
    require(retrieved.get("stored_sha256") == digest, "stored SHA-256 did not match")
    require(retrieved.get("retrieved_sha256") == digest, "retrieved SHA-256 did not match")

    bad_event_id = str(uuid.uuid4())
    wrong_digest = "0" * 64 if digest != "0" * 64 else "1" * 64
    status, bad_hash = seal(service_url, token, args.file, passport_id, bad_event_id, wrong_digest)
    require(status == 400 and bad_hash.get("error") == "invalid_request", "wrong SHA-256 was not rejected")
    status, absent = retrieve(service_url, token, passport_id, bad_event_id)
    require(status == 404 and absent.get("error") == "evidence_not_found", "wrong-hash request created an object")

    status, duplicate = seal(service_url, token, args.file, passport_id, event_id, digest)
    require(status == 409 and duplicate.get("error") == "evidence_already_sealed", "duplicate seal was not rejected")
    status, after_duplicate = retrieve(service_url, token, passport_id, event_id)
    require(after_duplicate.get("generation") == sealed.get("generation"), "duplicate seal changed the generation")

    status, invalid_passport = seal(service_url, token, args.file, "../invalid", str(uuid.uuid4()), digest)
    require(status == 400 and invalid_passport.get("error") == "invalid_request", "invalid passport_id was not rejected")
    status, invalid_event = seal(service_url, token, args.file, str(uuid.uuid4()), "not-a-uuid", digest)
    require(status == 400 and invalid_event.get("error") == "invalid_request", "invalid event_id was not rejected")
    status, path_injection = seal(
        service_url,
        token,
        args.file,
        str(uuid.uuid4()),
        str(uuid.uuid4()),
        digest,
        {"object_path": "../../arbitrary"},
    )
    require(status == 400 and path_injection.get("error") == "invalid_request", "object_path injection was not rejected")

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
        "negative_tests": {
            "wrong_sha256": "PASS",
            "duplicate_seal": "PASS",
            "generation_unchanged": "PASS",
            "invalid_passport_id": "PASS",
            "invalid_event_id": "PASS",
            "object_path_injection": "PASS",
        },
        "e2e": "PASS",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(json.dumps({"e2e": "FAIL", "error": str(error)}, ensure_ascii=False), file=sys.stderr)
        raise
