import copy
import tempfile
import unittest
from pathlib import Path

from ai_evidence.registry import Registry
from ai_evidence.text_dna import compare_text, fingerprint_text


ARTICLE = """人工智慧可以協助整理大量資訊，但來源紀錄仍然重要。每一次實質修改都應建立新的事件。\n\n系統只記錄發生過什麼，不判斷著作權或侵權。可靠的驗證需要雜湊、簽章、時間與版本關係。"""


class TextDnaTests(unittest.TestCase):
    def test_metadata_free_retyping_is_exact(self):
        self.assertEqual(compare_text(ARTICLE, ARTICLE)["evidence_tier"], "exact_match")

    def test_small_edit_remains_related(self):
        candidate = ARTICLE.replace("大量資訊", "許多資料").replace("仍然重要", "非常重要")
        result = compare_text(ARTICLE, candidate)
        self.assertIn(result["evidence_tier"], {"large_continuous_match", "partial_match", "approximate_rewrite"})
        self.assertGreater(result["confidence"], 0.55)

    def test_heavy_rewrite_lowers_confidence(self):
        result = compare_text(ARTICLE, "科技工具能提高效率。法律責任應由具權限的機構判定。")
        self.assertLess(result["confidence"], 0.35)
        self.assertIn(result["evidence_strength"], {"weak", "possible"})

    def test_common_short_phrase_is_not_strong_evidence(self):
        result = compare_text(ARTICLE, "人工智慧")
        self.assertNotEqual(result["evidence_strength"], "strong")
        self.assertIsNone(result["legal_plagiarism_verdict"])

    def test_hierarchical_fingerprints_exist(self):
        value = fingerprint_text(ARTICLE)
        self.assertTrue(value["exact_hash"])
        self.assertGreaterEqual(len(value["sentence_hashes"]), 2)
        self.assertEqual(len(value["paragraph_hashes"]), 2)
        self.assertGreater(len(value["ngram_hashes"]), 1)


class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.registry = Registry(root / "data", root / "keys")

    def tearDown(self):
        self.temp.cleanup()

    def test_sign_verify_and_tamper_detection(self):
        event = self.registry.register_text(ARTICLE, provider="gugupro", model="demo", involvement_level="L5", action_type="generate")
        self.assertTrue(self.registry.verify_event(event)["verified"])
        tampered = copy.deepcopy(event)
        tampered["action_type"] = "copy"
        self.assertFalse(self.registry.verify_event(tampered)["verified"])

    def test_parent_chain(self):
        first = self.registry.register_text(ARTICLE, content_id="article-1", action_type="generate", involvement_level="L5")
        second = self.registry.register_text(ARTICLE + " 新增一段。", content_id="article-1", parent_event=first["event_id"], action_type="rewrite", involvement_level="L4")
        self.assertEqual(second["parent_hash"], first["event_hash"])
        self.assertTrue(self.registry.verify_event(second)["parent_valid"])
        self.assertEqual(len(self.registry.history("article-1")), 2)

    def test_private_wallet_permissions(self):
        event = self.registry.register_text(ARTICLE)
        wallet = Path(self.temp.name) / "data" / "wallet" / (event["event_id"] + ".txt")
        self.assertTrue(wallet.exists())
        self.assertEqual(wallet.stat().st_mode & 0o777, 0o600)

    def test_revocation_changes_verification_status(self):
        event = self.registry.register_text(ARTICLE, involvement_level="L5", action_type="generate")
        self.registry.revoke(event["passport_id"], "test revocation")
        result = self.registry.verify_event(event)
        self.assertEqual(result["revocation_status"], "revoked")
        self.assertFalse(result["verified"])
        self.assertEqual(result["signature_status"], "valid")


if __name__ == "__main__":
    unittest.main()
