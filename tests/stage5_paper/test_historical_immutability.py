import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from codeguarder.stage5_paper.audit.fingerprints import (
    load_sha256_manifest,
    verify_sha256_manifest,
)


class HistoricalImmutabilityTests(unittest.TestCase):
    def test_historical_files_match_frozen_baseline(self):
        manifest = load_sha256_manifest(
            ROOT / "provenance" / "historical_baseline.sha256"
        )
        self.assertTrue(manifest)
        self.assertEqual([], verify_sha256_manifest(ROOT, manifest))


if __name__ == "__main__":
    unittest.main()
