"""Preflight tests; no answers, source URLs, body text or hidden dataset labels."""

from __future__ import annotations

import copy
import unittest

from scripts.research.prepare_core144_d2_d3_phase2 import (
    KEYS,
    excerpt_ranges,
    official_title,
    project_record,
    prompt,
    reconstruct,
)


class Phase2PreflightTests(unittest.TestCase):
    def test_projection_is_allowlisted(self) -> None:
        row = {"blind_review_id": "opaque", "candidate_text": "fictional",
               "construction_role": "private", "group_id": "private", "repair_reason": "private"}
        answer = {"local_internal_conflict": "YES", "text_naturalness": "MINOR_ISSUE"}
        result = project_record(row, answer, ["doc-a", "doc-b"])
        self.assertEqual(set(result), {"blind_review_id", "candidate_text",
                                     "locked_phase1_local_internal_conflict", "evidence"})
        self.assertEqual(result["evidence"], {"E1": "doc-a", "E2": "doc-b"})
        self.assertEqual(result["locked_phase1_local_internal_conflict"], "YES")

    def test_title_is_official_not_annotated_alias(self) -> None:
        raw = b'<html><meta name="ArticleTitle" content="Actual title"></html>'
        self.assertEqual(official_title(raw, "Actual title", "Correct old source")[0], "Actual title")

    def test_pdf_title_requires_witness(self) -> None:
        with self.assertRaisesRegex(ValueError, "witness"):
            official_title(b"%PDF", "Unrelated text", "Unsupported alias")

    def test_ordered_lineage_replay_detects_latest_text_drift(self) -> None:
        original = [{"blind_review_id": f"x{i}", "sample_id": f"s{i}-V1",
                     "group_id": f"g{i // 3}", "construction_role": "private",
                     "candidate_text": "original", "normalized_text": "original"} for i in range(144)]
        prior = [{"old_id": "x0", "new_id": "p0", "old_text": "original",
                  "new_text": "prior", "new_sample_id": "s0-V3"}]
        bounded = [{"old_id": "p0", "new_id": "n0", "old_text": "prior",
                    "new_text": "latest", "new_sample_id": "s0-V4"}]
        final = copy.deepcopy(original)
        final[0].update(blind_review_id="n0", candidate_text="latest", sample_id="s0-V4")
        rows = reconstruct(original, prior, bounded, final)
        self.assertEqual(rows[0]["superseded_blind_ids"], ["x0", "p0"])
        final[0]["candidate_text"] = "unapproved"
        with self.assertRaisesRegex(ValueError, "semantic identity"):
            reconstruct(original, prior, bounded, final)

    def test_schema_has_exact_eleven_keys(self) -> None:
        self.assertEqual(len(KEYS), 11)
        self.assertEqual(len(set(KEYS)), 11)

    def test_excerpt_retains_full_article_all_occurrences_and_identity(self) -> None:
        text = "Fictional issuer and identity\n第一条 总则。\n第二条 " + "context" * 1000
        text += " witness exception-and-condition。\n第三条 unrelated。\n第四条 witness other-condition。\n第五条 ending。"
        ranges = excerpt_ranges(text, ["witness"])
        excerpt = "".join(text[a:b] for a, b in ranges)
        self.assertIn("Fictional issuer and identity", excerpt)
        self.assertIn("context" * 1000 + " witness exception-and-condition。", excerpt)
        self.assertIn("第四条 witness other-condition。", excerpt)
        self.assertNotIn("第三条 unrelated", excerpt)

    def test_excerpt_missing_witness_fails_even_on_short_source(self) -> None:
        with self.assertRaisesRegex(ValueError, "witness absent"):
            excerpt_ranges("fictional text", ["absent"])

    def test_prompt_same_session_provider_no_guessing(self) -> None:
        text = prompt("D2", "R4_CODEX").decode("utf-8")
        for expected in ("Doubao", "同一个隔离会话", "十二个", "144 objects", "可下载文件",
                         "不得网页搜索", "ZERO_EXTERNAL_EVIDENCE_REQUIRED", "单独交付 incident"):
            self.assertIn(expected, text)


if __name__ == "__main__":
    unittest.main()
