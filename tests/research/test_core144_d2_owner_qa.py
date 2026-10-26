"""Synthetic guards for semantic-first QA and bounded additive HN repair."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.research.audit_core144_d2_owner_semantics import (
    RAW_SHA, seal_semantics, sha, validate_review_inventory, witness, write_new,
)
from scripts.research.repair_core144_d2_owner_two_hn import (
    check_semantic_lock, phase1_prompt, require_two_hn_roles, surface,
)


class SemanticContractTests(unittest.TestCase):
    def test_independent_disposition_inventory(self) -> None:
        rows = [{"blind_review_id": f"invented-{n}"} for n in range(37)]
        authored = {r["blind_review_id"]: ["finding", "independent reason"] for r in rows}
        validate_review_inventory(authored, rows)
        with self.assertRaises(ValueError):
            validate_review_inventory(authored, rows[:-1])

    def test_two_authorized_repairs_only(self) -> None:
        rows = [{"construction_role": "HARD_NEGATIVE"}] * 2
        require_two_hn_roles(rows)
        with self.assertRaises(ValueError):
            require_two_hn_roles(rows + rows)

    def test_no_repairing_controlled_poison_as_hn(self) -> None:
        with self.assertRaises(ValueError):
            require_two_hn_roles([{"construction_role": "HARD_NEGATIVE"}, {"construction_role": "POISON"}])

    def test_empty_independent_reason_rejected(self) -> None:
        rows = [{"blind_review_id": f"invented-{n}"} for n in range(37)]
        authored = {r["blind_review_id"]: ["finding", ""] for r in rows}
        with self.assertRaises(ValueError):
            validate_review_inventory(authored, rows)

    def test_process_difference_not_disposition_inventory(self) -> None:
        self.assertNotIn("evidence_selection", phase1_prompt("R3_GPT", "a.json", "b.json", "return.json"))

    def test_historical_raw_hashes(self) -> None:
        self.assertEqual(set(RAW_SHA), {"R3_GPT", "R4_CODEX"})
        self.assertTrue(all(len(value) == 64 for value in RAW_SHA.values()))

    def test_witness_literal_and_offsets(self) -> None:
        doc = {"evidence_id": "EV-TEST", "title": "Invented", "official_url": "https://example.gov/",
               "snapshot_sha256": "x", "source_text_sha256": "y", "frozen_excerpt_sha256": "z",
               "source_character_ranges": [[0, 8]], "frozen_excerpt": "序言。第一条原文"}
        result = witness(doc, "第一条", 3)
        self.assertEqual(result["literal_quote"], "第一条")
        self.assertEqual(result["excerpt_char_start"], 3)
        self.assertEqual(result["quote_sha256"], sha("第一条".encode()))

    def test_witness_absence_is_error(self) -> None:
        with self.assertRaises(ValueError):
            witness({"frozen_excerpt": "甲", "evidence_id": "test"}, "乙")

    def test_new_file_never_overwrites(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "raw.json"
            write_new(path, {"a": 1})
            before = path.read_bytes()
            with self.assertRaises(FileExistsError):
                write_new(path, {"a": 2})
            self.assertEqual(path.read_bytes(), before)

    def test_semantic_lock_explicitly_precedes_control(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            write_new(output / "judgement.json", {"hidden_role_used": False})
            result = seal_semantics(output)
            self.assertEqual(result["files_locked"], 1)
            lock = (output / "CANDIDATE_VISIBLE_SEMANTIC_LOCK_V1.json").read_text("utf-8")
            self.assertIn('"construction_control_plane_loaded": false', lock)
            for p in output.iterdir():
                p.chmod(0o666)

    def test_wrong_lock_identity_blocks_construction(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_new(root / "semantic_lock_v1/CANDIDATE_VISIBLE_SEMANTIC_LOCK_V1.json", {})
            with self.assertRaises(ValueError):
                check_semantic_lock(root)

    def test_synthetic_surface_no_extra_history_cues(self) -> None:
        self.assertEqual(surface("虚构规程规定两项材料。")["historical_cues"], 0)

    def test_synthetic_surface_keeps_dates_separate(self) -> None:
        self.assertEqual(surface("虚构2031年规程。")["dates"], 1)

    def test_surface_metrics_not_false_model_tokens(self) -> None:
        result = surface("甲13%。乙9%。")
        self.assertEqual(result["sentences"], 2)
        self.assertEqual(result["numbers"], 2)
        self.assertNotIn("tokens", result)

    def test_phase1_prompt_exact_file_list(self) -> None:
        prompt = phase1_prompt("R3_GPT", "a.json", "b.json", "return.json")
        self.assertIn("仅三件授权输入", prompt)
        self.assertIn("`a.json`", prompt)
        self.assertIn("`b.json`", prompt)
        self.assertIn("`return.json`", prompt)

    def test_r4_provider_identity_truthful(self) -> None:
        prompt = phase1_prompt("R4_CODEX", "a.json", "b.json", "return.json")
        self.assertIn("豆包 Doubao", prompt)
        self.assertIn("并非Codex模型", prompt)

    def test_no_targeted_phase2_release_or_new_session_default(self) -> None:
        prompt = phase1_prompt("R3_GPT", "a.json", "b.json", "return.json")
        self.assertIn("原 D2 独立会话", prompt)
        self.assertIn("不进入Phase2", prompt)
        self.assertIn("原 D2 会话已不可用", prompt)


if __name__ == "__main__":
    unittest.main()
