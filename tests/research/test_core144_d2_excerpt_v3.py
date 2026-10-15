"""Synthetic-only invariants for an additive evidence-presentation repair."""
from __future__ import annotations

import copy
import unittest

from scripts.research.repair_core144_d2_phase2_excerpts_v3 import (
    JOINER,
    add_complete_article,
    projection,
    targeted_packet,
    validate_repair,
)


class ExcerptRepairTests(unittest.TestCase):
    def test_whole_article_including_conditions_and_old_spans(self) -> None:
        text = "虚构标题\n第一条 说明。\n第二条 主规则。\n例外和条件。\n第三条 后续。\n"
        old = [[0, 5], [text.index("第三条"), len(text)]]
        ranges, article = add_complete_article(text, old, "第二条")
        self.assertEqual(article, "第二条 主规则。\n例外和条件。\n")
        new = projection(text, ranges)
        self.assertIn(article, new)
        self.assertIn(text[:5], new)
        self.assertIn("第三条 后续。", new)
        self.assertIn(JOINER, new)

    def test_missing_or_duplicate_heading_fails_closed(self) -> None:
        for text in ("第一条 A。\n第三条 C。", "第二条 A。\n第二条 B。\n第三条 C。"):
            with self.assertRaises(ValueError):
                add_complete_article(text, [[0, 1]], "第二条")

    def test_invalid_ranges_fail_closed(self) -> None:
        for ranges in ([[0, 50]], [[5, 2]], [[3, 5], [0, 4]]):
            with self.assertRaises(ValueError):
                projection("123456789", ranges)

    def test_targets_keep_own_order_and_only_used_documents(self) -> None:
        packet = {"format": "test", "reviewer_code": "R3_GPT", "actual_provider": "GPT",
                  "records": [{"blind_review_id": x, "candidate_text": "虚构文本", "evidence": {"E1": d}}
                              for x, d in (("c", "d2"), ("a", "d1"), ("b", "d3"))],
                  "evidence_documents": [{"evidence_id": x} for x in ("d1", "d2", "d3")]}
        before = copy.deepcopy(packet)
        result = targeted_packet(packet, {"b", "c"})
        self.assertEqual([r["blind_review_id"] for r in result["records"]], ["c", "b"])
        self.assertEqual([r["evidence_id"] for r in result["evidence_documents"]], ["d2", "d3"])
        self.assertEqual(packet, before)
        with self.assertRaises(ValueError):
            targeted_packet(packet, {"absent"})

    def test_only_authorized_documents_and_no_record_changes(self) -> None:
        old = {"records": [{"candidate_text": "虚构"}],
               "evidence_documents": [{"evidence_id": "a", "frozen_excerpt": "old"},
                                      {"evidence_id": "b", "frozen_excerpt": "same"}]}
        new = copy.deepcopy(old)
        new["evidence_documents"][0]["frozen_excerpt"] = "new"
        self.assertTrue(validate_repair(old, new, {"a"})["records_exact"])
        with self.assertRaises(ValueError):
            validate_repair(old, new, {"a", "b"})
        new["records"][0]["candidate_text"] = "changed"
        with self.assertRaises(ValueError):
            validate_repair(old, new, {"a"})


if __name__ == "__main__":
    unittest.main()
