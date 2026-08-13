import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from ai_evidence.c2pa_adapter import C2paTool


ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "demo-output" / "image-demo"


class C2paIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tool = C2paTool()
        cls.demo = json.loads((DEMO / "demo-case.json").read_text(encoding="utf-8"))

    def test_official_tool_and_three_manifest_chain(self):
        self.assertEqual(self.tool.version(), "c2patool 0.27.12")
        report = self.tool.read(DEMO / "signed" / "version-3.png")
        self.assertEqual(len(report["manifests"]), 3)
        self.assertEqual(report["active_manifest"], self.demo["versions"][2]["c2pa"]["active_manifest"])

    def test_c2pa_custom_assertion_links_registry_event(self):
        report = self.tool.read(DEMO / "signed" / "version-3.png")
        active = report["manifests"][report["active_manifest"]]
        assertion = next(item for item in active["assertions"] if item["label"].startswith("org.gugupro.ai-evidence"))
        self.assertEqual(assertion["data"]["event_id"], self.demo["versions"][2]["event_id"])
        self.assertTrue(self.demo["registry_verification"][2]["verified"])

    def test_tampered_asset_reports_hash_mismatch(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "tampered.png"
            subprocess.run(
                ["python3", str(ROOT / "scripts" / "tamper_png_for_test.py"), str(DEMO / "signed" / "version-3.png"), str(output)],
                check=True,
            )
            report = self.tool.read(output)
            codes = {item["code"] for item in report.get("validation_status", [])}
            self.assertIn("assertion.dataHash.mismatch", codes)


if __name__ == "__main__":
    unittest.main()
