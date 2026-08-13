import unittest

from ai_evidence.image_diff import diff_mask, fill_rect, solid_canvas


class ImageDiffTests(unittest.TestCase):
    def test_local_object_mask_matches_changed_box(self):
        width, height = 100, 80
        before = solid_canvas(width, height, (20, 20, 20))
        after = bytearray(before)
        fill_rect(after, width, height, 30, 20, 50, 45, (240, 30, 30))
        _, stats = diff_mask(before, after, width, height)
        self.assertEqual(stats["bounding_box"], {"x": 30, "y": 20, "width": 20, "height": 25})
        self.assertAlmostEqual(stats["changed_ratio"], 0.0625)

    def test_background_mask_covers_full_frame(self):
        width, height = 40, 30
        before = solid_canvas(width, height, (10, 20, 30))
        after = solid_canvas(width, height, (60, 70, 80))
        _, stats = diff_mask(before, after, width, height)
        self.assertEqual(stats["changed_ratio"], 1.0)
        self.assertEqual(stats["bounding_box"], {"x": 0, "y": 0, "width": width, "height": height})

    def test_below_threshold_noise_is_ignored(self):
        width, height = 20, 20
        before = solid_canvas(width, height, (100, 100, 100))
        after = solid_canvas(width, height, (106, 106, 106))
        _, stats = diff_mask(before, after, width, height, threshold=12)
        self.assertEqual(stats["changed_pixels"], 0)

