"""Synthetic bounded repair checks; never create real reviewer answers."""

import copy
import unittest
from typing import Any

from scripts.research.repair_core144_bounded_phase1 import (
    repair_row,
    targeted_packet,
    verify_scope,
)


class BoundedRepairTests(unittest.TestCase):
    def test_v3_to_v4_identity_is_deterministic_without_mutation(self) -> None:
        old = {
            "sample_id": "g-P-V3",
            "blind_review_id": "old",
            "candidate_text": "旧句。",
            "normalized_text": "旧句。",
            "group_id": "g",
            "family_cluster_id": "f",
            "created_utc": "old",
        }
        before = copy.deepcopy(old)
        new = repair_row(old, "新句。", "stamp")
        self.assertEqual(new["sample_id"], "g-P-V4")
        self.assertEqual(old, before)
        self.assertNotEqual(new["blind_review_id"], "old")
        self.assertEqual(new, repair_row(old, "新句。", "stamp"))
        self.assertEqual(new["family_cluster_id"], "f")

    def test_no_change_and_empty_text_rejected(self) -> None:
        for text in ("旧句", " "):
            with self.assertRaises(ValueError):
                repair_row({"candidate_text": "旧句"}, text, "stamp")

    def test_only_exact_three_one_scope(self) -> None:
        scope: dict[str, Any] = {"D2": {str(i): {} for i in range(3)}, "D3": {"a": {}}}
        verify_scope(scope, {d: set(v) for d, v in scope.items()})
        with self.assertRaises(ValueError):
            verify_scope(scope, {"D2": {"0", "1", "other"}, "D3": {"a"}})
        scope["D3"]["extra"] = {}
        with self.assertRaises(ValueError):
            verify_scope(scope, {d: set(v) for d, v in scope.items()})

    def test_packet_preserves_reviewer_subset_order_and_hides_control(self) -> None:
        rows = [{"blind_review_id": x, "candidate_text": x} for x in ("b", "c", "a")]
        replacements = {
            x: {
                "blind_review_id": x + "new",
                "candidate_text": "正文",
                "construction_role": "PRIVATE",
            }
            for x in ("a", "b")
        }
        result = targeted_packet(rows, replacements)
        self.assertEqual([r["blind_review_id"] for r in result], ["bnew", "anew"])
        self.assertTrue(
            all(set(r) == {"blind_review_id", "candidate_text"} for r in result)
        )
        with self.assertRaises(ValueError):
            targeted_packet(rows[:1], replacements)


if __name__ == "__main__":
    unittest.main()
