"""Contract checks for strict JSON, immutable locks, and reviewer-specific ordering."""

import json
import os
import tempfile
import unittest
from pathlib import Path

from scripts.research.lock_core144_d2_d3_phase1_returns import (
    FIELDS,
    compare,
    lock_original,
    parse,
    validate,
)


class Phase1LockContractTest(unittest.TestCase):
    def setUp(self) -> None:
        self.packet = [
            {"blind_review_id": f"ID-{index:03d}", "candidate_text": "虚构文字"}
            for index in range(144)
        ]
        self.rows = [
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
            "keys": list(self.rows[0]),
            "enums": {
                "text_naturalness": ["NATURAL", "MINOR_ISSUE", "UNNATURAL"],
                "local_internal_conflict": ["YES", "NO", "UNCERTAIN"],
                "self_containment": ["PASS", "FLAG", "UNCERTAIN"],
                "ambiguous_referent": ["YES", "NO", "UNCERTAIN"],
                "meta_or_template_language": ["YES", "NO", "UNCERTAIN"],
            },
        }

    def check_return(self) -> dict:
        report, _ = validate(json.dumps(self.rows).encode(), self.packet, self.schema)
        return report

    def test_valid_array_and_optional_default_note(self) -> None:
        self.rows[0]["issue_note"] = "默认值的可选说明"
        self.assertTrue(self.check_return()["validation_pass"])

    def test_exact_id_order(self) -> None:
        self.rows[0], self.rows[1] = self.rows[1], self.rows[0]
        self.assertFalse(self.check_return()["validation_pass"])

    def test_duplicate_id(self) -> None:
        self.rows[1]["blind_review_id"] = self.rows[0]["blind_review_id"]
        self.assertFalse(self.check_return()["validation_pass"])

    def test_extra_key(self) -> None:
        self.rows[0]["confidence"] = "HIGH"
        self.assertFalse(self.check_return()["validation_pass"])

    def test_missing_row(self) -> None:
        self.rows.pop()
        self.assertFalse(self.check_return()["validation_pass"])

    def test_illegal_enum(self) -> None:
        self.rows[0]["text_naturalness"] = "自然"
        self.assertFalse(self.check_return()["validation_pass"])

    def test_abnormal_requires_note(self) -> None:
        self.rows[0]["local_internal_conflict"] = "YES"
        self.assertFalse(self.check_return()["validation_pass"])

    def test_comparison_aligns_by_id_not_reviewer_order(self) -> None:
        reversed_rows = list(reversed(self.rows))
        result = compare(self.packet, self.rows, reversed_rows)
        self.assertEqual(result["disagreement_row_count"], 0)
        for field in FIELDS:
            self.assertEqual(result["categorical_agreement"][field]["agree"], 144)

    def test_json_duplicates_and_constants_rejected(self) -> None:
        for raw in (b'{"x":1,"x":2}', b"[NaN]", b"[Infinity]", b"\xef\xbb\xbf[]"):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                parse(raw)

    def test_raw_byte_preservation_before_parse_and_no_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source.json"
            target = Path(directory) / "raw.json"
            original = b"bad JSON is still process evidence\r\n"
            source.write_bytes(original)
            lock_original(source, target)
            self.assertEqual(target.read_bytes(), original)
            with self.assertRaises(FileExistsError):
                lock_original(source, target)
            os.chmod(target, 0o666)


if __name__ == "__main__":
    unittest.main()
