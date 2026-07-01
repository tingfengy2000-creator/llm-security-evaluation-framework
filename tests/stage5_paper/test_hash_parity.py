import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from codeguarder.stage5_paper.evaluation.validators import (
    validate_output_only,
    validate_prompt_hash_parity,
)


class HashParityTests(unittest.TestCase):
    def test_matching_p_i_o_f_pass(self):
        records = [
            {"sample_id": "s1", "guard_code": code, "prompt_hash": "same"}
            for code in ("P", "I", "O", "F")
        ]
        self.assertEqual([], validate_prompt_hash_parity(records))

    def test_output_only_requires_upstream_and_raw_hash(self):
        records = [
            {
                "sample_id": "s1",
                "guard_code": "O",
                "input_guard_enabled": False,
                "output_guard_enabled": True,
                "input_blocked": False,
                "upstream_called": False,
                "raw_model_output_hash": None,
            }
        ]
        codes = {issue.code for issue in validate_output_only(records)}
        self.assertIn("output_only_upstream", codes)
        self.assertIn("output_only_raw_hash", codes)


if __name__ == "__main__":
    unittest.main()
