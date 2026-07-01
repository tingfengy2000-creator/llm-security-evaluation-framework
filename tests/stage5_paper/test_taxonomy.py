import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from codeguarder.stage5_paper.taxonomy.engine import classify_failure_types


def record(**updates):
    value = {
        "benign_sample": False,
        "raw_model_risk": False,
        "final_risk": False,
        "garak_covered": False,
        "garak_pass": None,
        "input_guard_enabled": False,
        "output_guard_enabled": False,
        "input_blocked": False,
        "output_blocked": False,
        "threat_layer": "Runtime",
        "turn_count": 1,
        "confidentiality_breach": False,
        "tool_call_intent": False,
        "would_execute_side_effect": False,
    }
    value.update(updates)
    return value


class TaxonomyTests(unittest.TestCase):
    def test_t1_to_t5(self):
        self.assertEqual(["T1"], classify_failure_types(record(raw_model_risk=True)))
        self.assertIn(
            "T2",
            classify_failure_types(
                record(raw_model_risk=True, garak_covered=True, garak_pass=True)
            ),
        )
        self.assertIn(
            "T3",
            classify_failure_types(record(input_guard_enabled=True, final_risk=True)),
        )
        self.assertIn(
            "T4",
            classify_failure_types(record(output_blocked=True, final_risk=True)),
        )
        self.assertIn(
            "T5",
            classify_failure_types(record(benign_sample=True, input_blocked=True)),
        )

    def test_t6_to_t9(self):
        failures = classify_failure_types(
            record(
                threat_layer="Retrieval",
                turn_count=3,
                raw_model_risk=True,
                confidentiality_breach=True,
                tool_call_intent=True,
                would_execute_side_effect=True,
            )
        )
        self.assertTrue({"T6", "T7", "T8", "T9"}.issubset(failures))

    def test_uncovered_garak_is_not_t2(self):
        failures = classify_failure_types(
            record(raw_model_risk=True, garak_covered=False, garak_pass=True)
        )
        self.assertNotIn("T2", failures)


if __name__ == "__main__":
    unittest.main()
