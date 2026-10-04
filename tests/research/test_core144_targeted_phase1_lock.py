"""Synthetic contracts only; tests do not annotate actual Candidates."""

import copy
import json
import os
import tempfile
import unittest
from pathlib import Path
from typing import Any

from scripts.research.lock_core144_d2_d3_phase1_returns import digest, save_new
from scripts.research.lock_core144_targeted_phase1_returns import (
    compare_targeted,
    merge_evidence_view,
    validate_targeted,
    verify_index,
)


class TargetedPhase1ContractTest(unittest.TestCase):
    def setUp(self) -> None:
        self.packet = [
            {"blind_review_id": f"ID-{i}", "candidate_text": "虚构文本"}
            for i in range(25)
        ]
        self.rows: list[dict[str, Any]] = [
            {
                "blind_review_id": row["blind_review_id"],
                "text_naturalness": "NATURAL",
                "local_internal_conflict": "NO",
                "self_containment": "PASS",
                "ambiguous_referent": "NO",
                "meta_or_template_language": "NO",
                "issue_note": "",
            }
            for row in self.packet
        ]
        self.schema = {
            "record_count": 25,
            "keys": list(self.rows[0]),
            "enums": {
                "text_naturalness": ["NATURAL", "MINOR_ISSUE", "UNNATURAL"],
                "local_internal_conflict": ["YES", "NO", "UNCERTAIN"],
                "self_containment": ["PASS", "FLAG", "UNCERTAIN"],
                "ambiguous_referent": ["YES", "NO", "UNCERTAIN"],
                "meta_or_template_language": ["YES", "NO", "UNCERTAIN"],
            },
        }

    def check(self) -> dict:
        return validate_targeted(
            json.dumps(self.rows).encode(), self.packet, self.schema
        )[0]

    def test_frozen_25_and_32_counts(self) -> None:
        self.assertTrue(self.check()["validation_pass"])
        for i in range(25, 32):
            self.packet.append(dict(self.packet[0], blind_review_id=f"ID-{i}"))
            self.rows.append(dict(self.rows[0], blind_review_id=f"ID-{i}"))
        self.schema["record_count"] = 32
        self.assertTrue(self.check()["validation_pass"])

    def test_not_hardcoded_144(self) -> None:
        self.rows.pop()
        self.assertFalse(self.check()["validation_pass"])

    def test_order_and_duplicates(self) -> None:
        self.rows.reverse()
        self.assertFalse(self.check()["validation_pass"])
        self.rows.reverse()
        self.rows[1] = self.rows[0].copy()
        self.assertFalse(self.check()["validation_pass"])

    def test_extra_key_and_key_order(self) -> None:
        self.rows[0]["confidence"] = "HIGH"
        self.assertFalse(self.check()["validation_pass"])
        del self.rows[0]["confidence"]
        self.rows[0] = dict(reversed(list(self.rows[0].items())))
        self.assertFalse(self.check()["validation_pass"])

    def test_enum_types_and_required_note(self) -> None:
        self.rows[0]["self_containment"] = "FLAG"
        self.assertFalse(self.check()["validation_pass"])
        self.rows[0]["issue_note"] = "虚构对象缺失"
        self.assertTrue(self.check()["validation_pass"])
        self.rows[0]["self_containment"] = "缺失"
        self.assertFalse(self.check()["validation_pass"])
        self.rows[0]["self_containment"] = None
        self.assertFalse(self.check()["validation_pass"])

    def test_duplicate_json_keys_bom_nan(self) -> None:
        raw = json.dumps(self.rows).encode()
        for invalid in (b"\xef\xbb\xbf" + raw, b'[{"x":1,"x":2}]', b"[NaN]"):
            self.assertFalse(
                validate_targeted(invalid, self.packet, self.schema)[0][
                    "validation_pass"
                ]
            )

    def test_different_reviewer_order_joined_by_id(self) -> None:
        right = copy.deepcopy(self.rows[::-1])
        right[0]["local_internal_conflict"] = "YES"
        right[0]["issue_note"] = "虚构冲突"
        result = compare_targeted(self.packet, self.rows, right)
        self.assertEqual(
            result["categorical_agreement"]["local_internal_conflict"]["agree"], 24
        )
        self.assertEqual(result["disagreement_rows"][0]["blind_review_id"], "ID-24")
        self.assertTrue(result["agreement_is_not_acceptance"])

    def test_notes_do_not_require_literal_agreement(self) -> None:
        right = copy.deepcopy(self.rows)
        right[0]["issue_note"] = "可选文字"
        result = compare_targeted(self.packet, self.rows, right)
        self.assertEqual(result["disagreement_cell_count"], 0)
        self.assertEqual(result["issue_note_raw_identical_rows"], 24)

    def test_merge_raw_values_preserved_and_lineage_attributed(self) -> None:
        targeted = [
            dict(
                self.rows[0],
                blind_review_id="NEW-0",
                text_naturalness="MINOR_ISSUE",
                issue_note="虚构偏好",
            )
        ]
        original = copy.deepcopy(self.rows)
        merged = merge_evidence_view(
            self.rows, targeted, [{"old_id": "ID-0", "new_id": "NEW-0"}]
        )
        self.assertEqual(merged[0]["answer"], targeted[0])
        self.assertEqual(merged[0]["source"], "TARGETED_V1")
        self.assertEqual(merged[1]["answer"], self.rows[1])
        self.assertEqual(self.rows, original)

    def test_merge_rejects_missing_target_or_ancestor(self) -> None:
        for lineage in (
            [{"old_id": "ID-0", "new_id": "NEW-0"}],
            [{"old_id": "ABSENT", "new_id": "ID-0"}],
        ):
            with self.assertRaises(ValueError):
                merge_evidence_view(self.rows, [self.rows[0]], lineage)

    def test_index_supports_both_historical_shapes_and_detects_change(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            file = root / "input.json"
            save_new(file, {"synthetic": True})
            item = {"sha256": digest(file.read_bytes()), "bytes": file.stat().st_size}
            for entries in ({file.name: item}, [dict(item, path=file.name)]):
                index = root / "FINAL_EVIDENCE_INDEX_V1.json"
                if index.exists():
                    os.chmod(index, 0o666)
                    index.unlink()
                save_new(index, {"files": entries})
                self.assertTrue(verify_index(root, digest(index.read_bytes()))["pass"])
            with self.assertRaises(ValueError):
                verify_index(root, "not-the-sha")
            os.chmod(file, 0o666)
            file.write_bytes(b"changed synthetic input")
            with self.assertRaises(ValueError):
                verify_index(root, digest(index.read_bytes()))


if __name__ == "__main__":
    unittest.main()
