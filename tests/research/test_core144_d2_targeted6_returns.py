"""Synthetic targeted-return checks; no benchmark answers."""
from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path

from scripts.research.lock_core144_d2_targeted6_phase2_returns import lock_pair, validate_targeted
from tests.research.test_core144_d2_phase2_returns import fixture


class TargetedReturnTests(unittest.TestCase):
    def test_six_own_ids_order_schema(self) -> None:
        rows, schema, packet = fixture()
        rows = rows[:6]
        packet["records"] = packet["records"][:6]
        schema["record_count"] = 6
        self.assertTrue(validate_targeted(rows, packet, schema)["structural_pass"])
        rows.reverse()
        self.assertFalse(validate_targeted(rows, packet, schema)["structural_pass"])

    def test_extra_key_bad_enum_duplicate_missing_and_reason(self) -> None:
        rows, schema, packet = fixture()
        rows = rows[:6]
        packet["records"] = packet["records"][:6]
        schema["record_count"] = 6
        rows[0]["unexpected"] = "x"
        rows[1]["overall_fact_status"] = "INVALID"
        rows[2]["phase2_reason"] = " "
        rows[3]["blind_review_id"] = rows[4]["blind_review_id"]
        self.assertFalse(validate_targeted(rows, packet, schema)["structural_pass"])

    def test_consistency_flags_do_not_rewrite(self) -> None:
        rows, schema, packet = fixture()
        rows = rows[:6]
        packet["records"] = packet["records"][:6]
        schema["record_count"] = 6
        rows[0]["minimum_external_evidence_needed"] = "ONE_OFFICIAL_EVIDENCE"
        before = copy.deepcopy(rows)
        result = validate_targeted(rows, packet, schema)
        self.assertTrue(result["structural_pass"])
        self.assertEqual(result["consistency_flags"][0]["code"], "NONCONFLICT_MINIMUM")
        self.assertEqual(rows, before)

    def test_lock_bytes_even_before_bad_JSON_is_parsed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            paths = {}
            for who, content in (("R3_GPT", b"not JSON\r\n"), ("R4_CODEX", b"[]\n")):
                paths[who] = root / (who + ".json")
                paths[who].write_bytes(content)
            out = root / "locked"
            manifest = lock_pair(paths, out)
            self.assertEqual(len(manifest), 2)
            self.assertEqual((out / "raw/R3_GPT.json").read_bytes(), b"not JSON\r\n")
            with self.assertRaises(ValueError):
                lock_pair(paths, out)


if __name__ == "__main__":
    unittest.main()
