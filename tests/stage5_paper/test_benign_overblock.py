import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from codeguarder.stage5_paper.metrics.suite import compute_metrics


class BenignOverblockTests(unittest.TestCase):
    def test_overblock_uses_benign_denominator(self):
        records = [
            {
                "benign_sample": True,
                "input_blocked": True,
                "output_blocked": False,
                "failure_types": ["T5"],
                "latency_ms": 1,
            }
        ]
        self.assertEqual(100.0, compute_metrics(records)["overblock"]["rate_percent"])


if __name__ == "__main__":
    unittest.main()
