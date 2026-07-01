import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from codeguarder.metrics.overblock import overblock_rate
from codeguarder.taxonomy.failure_taxonomy import classify_failure_types


class BenignOverblockTests(unittest.TestCase):
    def test_t5_and_rate(self):
        record = {
            "benign_sample": True,
            "input_blocked": True,
            "output_blocked": False,
            "raw_model_risk": False,
            "final_risk": False,
            "garak_pass": True,
            "input_guard_enabled": True,
            "output_guard_enabled": False,
            "final_risk_matches": [],
            "category": "benign",
            "turn_count": 1,
            "confidentiality_breach": False,
            "tool_call_intent": False,
            "would_execute_side_effect": False,
        }
        self.assertIn("T5", classify_failure_types(record))
        self.assertEqual(100.0, overblock_rate([record]))

