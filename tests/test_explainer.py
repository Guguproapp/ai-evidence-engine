import importlib.util
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


APP_PATH = Path(__file__).parents[1] / "services" / "explainer" / "app.py"
SPEC = importlib.util.spec_from_file_location("evidence_explainer_app", APP_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class EvidenceExplainerTests(unittest.TestCase):
    def setUp(self):
        MODULE.attempts.clear()
        MODULE.app.config.update(TESTING=True)
        self.client = MODULE.app.test_client()

    def payload(self, status="Modified"):
        return {
            "status": status,
            "facts": {
                "version_id": "proofcart-v3",
                "evidence_id": "event-3",
                "action": "Product label area changed",
                "changed_ratio": 0.0477,
                "signature_status": "valid",
                "c2pa_manifest_count": 3,
                "secret": "must-not-be-forwarded",
            },
        }

    def test_health_declares_real_production_target(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["google_cloud"], "Cloud Run")
        self.assertEqual(response.json["gemini_backend"], "Vertex AI")

    def test_gemini_explains_but_cannot_replace_status(self):
        with patch.object(MODULE, "_generate_explanation", return_value=("The signed record is valid and the label area changed.", "gemini-test")) as mocked:
            response = self.client.post("/v1/explain", json=self.payload())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["verification_status"], "Modified")
        self.assertEqual(response.json["decision_source"], "AI Evidence Engine cryptographic verification")
        forwarded_facts = mocked.call_args.args[1]
        self.assertNotIn("secret", forwarded_facts)

    def test_rejects_model_invented_or_unsupported_status(self):
        response = self.client.post("/v1/explain", json=self.payload("Probably Authentic"))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"], "invalid_request")

    def test_cors_is_limited_to_production_verifier(self):
        allowed = self.client.options(
            "/v1/explain",
            headers={"Origin": "https://ai-evidence-engine-gugupro.artistuncle.chatgpt.site"},
        )
        denied = self.client.options("/v1/explain", headers={"Origin": "https://evil.example"})
        self.assertEqual(allowed.headers.get("Access-Control-Allow-Origin"), "https://ai-evidence-engine-gugupro.artistuncle.chatgpt.site")
        self.assertIsNone(denied.headers.get("Access-Control-Allow-Origin"))


if __name__ == "__main__":
    unittest.main()
