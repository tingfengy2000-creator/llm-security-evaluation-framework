import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from codeguarder.attacks.matrix_loader import (
    ATTACK_CATEGORIES,
    load_attack_matrix,
    load_benign_requests,
)


class MatrixLoaderTests(unittest.TestCase):
    def test_smoke_matrix_has_two_per_category_and_unique_ids(self):
        samples = load_attack_matrix(ROOT / "data" / "stage5", per_category=2)
        self.assertEqual(12, len(samples))
        self.assertEqual(12, len({sample.id for sample in samples}))
        for category in ATTACK_CATEGORIES:
            self.assertEqual(
                2,
                len([sample for sample in samples if sample.category == category]),
            )

    def test_benign_has_at_least_ten(self):
        samples = load_benign_requests(ROOT / "data" / "stage5")
        self.assertGreaterEqual(len(samples), 10)
        self.assertTrue(all(sample.benign for sample in samples))

