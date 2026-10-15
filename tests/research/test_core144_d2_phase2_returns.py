"""Synthetic tests; no construction labels, Expected or Human answers."""
from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path
from typing import Any

from scripts.research.lock_core144_d2_phase2_returns import (
    compare_rows,
    lock_sources,
    strict_parse,
    validate_rows,
)


def fixture() -> tuple[list[dict[str, str]], dict, dict]:
    rows = [{"blind_review_id": f"opaque-{i}", "overall_fact_status": "CURRENTLY_CONSISTENT",
             "version_claim_status": "NOT_PRESENT", "authority_claim_status": "NOT_PRESENT",
             "minimum_external_evidence_needed": "NOT_APPLICABLE", "evidence_selection": "E1",
             "phase2_issue": "NONE", "phase2_reason": "Fictional E1 supports the claim.",
             "possible_accidental_secondary_error": "NO", "evidence_sufficiency": "SUFFICIENT",
             "reviewer_note": ""} for i in range(144)]
    schema: dict[str, Any] = {"keys": list(rows[0]), "enums": {k: [v] for k, v in rows[0].items()
              if k not in {"blind_review_id", "phase2_reason", "reviewer_note"}}}
    schema["enums"]["evidence_selection"] += ["NONE", "E2", "E1+E2"]
    schema["enums"]["minimum_external_evidence_needed"] += ["ZERO_EXTERNAL_EVIDENCE_REQUIRED", "ONE_OFFICIAL_EVIDENCE"]
    schema["enums"]["overall_fact_status"].append("FACTUAL_CONFLICT")
    schema["enums"]["version_claim_status"].append("PRESENT_CORRECT")
    package = {"records": [{"blind_review_id": r["blind_review_id"], "candidate_text": "Fictional text.",
                           "locked_phase1_local_internal_conflict": "NO", "evidence": {"E1": "doc"}}
                          for r in rows]}
    return rows, schema, package


class ReturnTests(unittest.TestCase):
    def test_valid_and_exact_order(self) -> None:
        rows, schema, packet = fixture()
        self.assertTrue(validate_rows(rows, packet, schema)["structural_pass"])
        rows.reverse()
        self.assertFalse(validate_rows(rows, packet, schema)["structural_pass"])

    def test_strict_parser_rejects_duplicate_keys_BOM_and_NaN(self) -> None:
        for raw in (b'{"x":1,"x":2}', b'\xef\xbb\xbf[]', b'[NaN]'):
            with self.assertRaises(ValueError):
                strict_parse(raw)

    def test_extra_keys_duplicate_ids_and_blank_reason(self) -> None:
        rows, schema, packet = fixture()
        rows[0]["unapproved"] = "value"
        rows[1]["blind_review_id"] = rows[2]["blind_review_id"]
        rows[3]["phase2_reason"] = " "
        result = validate_rows(rows, packet, schema)
        self.assertFalse(result["structural_pass"])
        self.assertGreaterEqual(len(result["structural_errors"]), 3)

    def test_locked_phase1_zero_condition_is_checked_not_corrected(self) -> None:
        rows, schema, packet = fixture()
        rows[0].update(overall_fact_status="FACTUAL_CONFLICT", minimum_external_evidence_needed="ONE_OFFICIAL_EVIDENCE")
        packet["records"][0]["locked_phase1_local_internal_conflict"] = "YES"
        before = copy.deepcopy(rows)
        result = validate_rows(rows, packet, schema)
        self.assertTrue(result["structural_pass"])
        self.assertEqual(result["consistency_flags"][0]["code"], "LOCKED_LOCAL_YES_REQUIRES_ZERO")
        self.assertEqual(rows, before)

    def test_unoffered_evidence_is_flagged(self) -> None:
        rows, schema, packet = fixture()
        rows[0]["evidence_selection"] = "E2"
        self.assertEqual(validate_rows(rows, packet, schema)["consistency_flags"][0]["code"], "UNSUPPLIED_EVIDENCE_SELECTED")

    def test_process_difference_not_semantic_vote(self) -> None:
        rows, _, packet = fixture()
        other = copy.deepcopy(rows)
        other[0]["evidence_selection"] = "NONE"
        result = compare_rows(rows, other, packet)
        self.assertEqual(result["process_only_disagreement_rows"], 1)
        self.assertEqual(result["semantic_disagreement_rows"], 0)
        self.assertFalse(result["GT_created"])

    def test_semantic_difference_and_reason_wording_preserved(self) -> None:
        rows, _, packet = fixture()
        other = copy.deepcopy(rows)
        other[0]["version_claim_status"] = "PRESENT_CORRECT"
        other[1]["phase2_reason"] = "Different wording is not categorical disagreement."
        result = compare_rows(rows, other, packet)
        self.assertEqual(result["semantic_disagreement_rows"], 1)
        self.assertEqual(result["reason_exact_byte_equal_rows"], 143)

    def test_lock_precedes_parse_and_no_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            sources = []
            for reviewer in ("R3_GPT", "R4_CODEX"):
                path = root / f"{reviewer}.json"
                path.write_bytes(b"not valid JSON")
                sources.append({"reviewer": reviewer, "source": str(path)})
            output = root / "locked"
            result = lock_sources(sources, output)
            self.assertEqual(len(result), 2)
            for item in result:
                self.assertEqual(Path(item["locked_path"]).read_bytes(), b"not valid JSON")
            with self.assertRaises(ValueError):
                lock_sources(sources, output)
            for item in result:
                Path(item["locked_path"]).chmod(0o666)
