import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from codeguarder.stage5_paper.metrics.suite import compute_metrics


class MetricsTests(unittest.TestCase):
    def test_rates_include_numerator_denominator_and_rate(self):
        records = [
            {
                "benign_sample": False,
                "final_risk": True,
                "raw_model_risk": True,
                "garak_covered": True,
                "failure_types": ["T1", "T2"],
                "input_guard_enabled": False,
                "output_guard_enabled": False,
                "input_blocked": False,
                "output_blocked": False,
                "upstream_called": True,
                "latency_ms": 100,
            },
            {
                "benign_sample": False,
                "final_risk": False,
                "raw_model_risk": False,
                "garak_covered": False,
                "failure_types": [],
                "input_guard_enabled": True,
                "output_guard_enabled": False,
                "input_blocked": True,
                "output_blocked": False,
                "upstream_called": False,
                "latency_ms": 20,
            },
        ]
        metrics = compute_metrics(records)
        self.assertEqual(
            {"numerator": 1, "denominator": 2, "rate_percent": 50.0},
            metrics["asr"],
        )
        self.assertEqual(100.0, metrics["dmr"]["rate_percent"])
        self.assertIn("latency", metrics)


if __name__ == "__main__":
    unittest.main()
