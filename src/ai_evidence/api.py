import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

from .registry import Registry
from .text_dna import compare_text


class ApiHandler(BaseHTTPRequestHandler):
    registry = None

    def _json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _body(self):
        length = int(self.headers.get("Content-Length", "0"))
        return json.loads(self.rfile.read(length) or b"{}")

    def do_GET(self):
        parts = urlparse(self.path).path.strip("/").split("/")
        if parts == ["health"]:
            return self._json(200, {"status": "ok", "service": "ai-evidence-registry"})
        if len(parts) == 2 and parts[0] == "passport":
            value = self.registry.get_passport(parts[1])
            return self._json(200 if value else 404, value or {"error": "not_found"})
        if len(parts) == 2 and parts[0] == "history":
            return self._json(200, self.registry.history(parts[1]))
        if len(parts) == 2 and parts[0] == "issuer":
            value = self.registry.issuer(parts[1])
            return self._json(200 if value else 404, value or {"error": "not_found"})
        return self._json(404, {"error": "not_found"})

    def do_POST(self):
        path = urlparse(self.path).path
        try:
            body = self._body()
            if path == "/register":
                content = body.pop("content")
                return self._json(201, self.registry.register_text(content, **body))
            if path == "/verify":
                if "event" in body:
                    return self._json(200, self.registry.verify_event(body["event"]))
                if "source" in body and "candidate" in body:
                    return self._json(200, compare_text(body["source"], body["candidate"]))
                return self._json(400, {"error": "event or source+candidate required"})
            if path == "/fingerprint/lookup":
                candidate = body["content"]
                results = []
                for event in self.registry.all_events():
                    private_path = self.registry.data_dir / "wallet" / (event["event_id"] + ".txt")
                    if private_path.exists():
                        results.append({"passport_id": event["passport_id"], **compare_text(private_path.read_text(encoding="utf-8"), candidate)})
                return self._json(200, sorted(results, key=lambda item: item["confidence"], reverse=True))
            if path == "/revoke":
                return self._json(200, self.registry.revoke(body["passport_id"], body["reason"]))
        except (KeyError, ValueError, json.JSONDecodeError) as error:
            return self._json(400, {"error": str(error)})
        return self._json(404, {"error": "not_found"})

    def log_message(self, format, *args):
        return


def main():
    data_dir = os.environ.get("AI_EVIDENCE_DATA_DIR", "./data")
    key_dir = os.environ.get("AI_EVIDENCE_KEY_DIR", "./keys")
    ApiHandler.registry = Registry(data_dir, key_dir)
    address = (os.environ.get("AI_EVIDENCE_HOST", "127.0.0.1"), int(os.environ.get("AI_EVIDENCE_PORT", "8787")))
    print("AI Evidence Registry listening on http://%s:%d" % address)
    ThreadingHTTPServer(address, ApiHandler).serve_forever()


if __name__ == "__main__":
    main()

