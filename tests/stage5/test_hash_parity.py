import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from codeguarder.evaluation.validators import (
    validate_prompt_hash_parity,
    validate_raw_output_hash_parity,
)


class HashParityTests(unittest.TestCase):
    def test_four_matching_modes_pass(self):
        records = [
            {"sample_id": "s1", "guard_mode": mode, "prompt_hash": "same"}
            for mode in (
                "passthrough",
                "input-only",
                "output-only",
                "full-guard",
            )
        ]
        self.assertEqual([], validate_prompt_hash_parity(records))

    def test_hash_mismatch_fails(self):
        records = [
            {"sample_id": "s1", "guard_mode": "passthrough", "prompt_hash": "a"},
            {"sample_id": "s1", "guard_mode": "input-only", "prompt_hash": "a"},
            {"sample_id": "s1", "guard_mode": "output-only", "prompt_hash": "b"},
            {"sample_id": "s1", "guard_mode": "full-guard", "prompt_hash": "a"},
        ]
        issues = validate_prompt_hash_parity(records)
        self.assertIn("prompt_hash_parity", {issue.code for issue in issues})

    def test_raw_hash_compares_only_upstream_called_modes(self):
        records = [
            {
                "sample_id": "s1",
                "guard_mode": "passthrough",
                "upstream_called": True,
                "raw_model_output_hash": "same",
            },
            {
                "sample_id": "s1",
                "guard_mode": "input-only",
                "upstream_called": False,
                "raw_model_output_hash": None,
            },
            {
                "sample_id": "s1",
                "guard_mode": "output-only",
                "upstream_called": True,
                "raw_model_output_hash": "same",
            },
        ]
        self.assertEqual([], validate_raw_output_hash_parity(records))
