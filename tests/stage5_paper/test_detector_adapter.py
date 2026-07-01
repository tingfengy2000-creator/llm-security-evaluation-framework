import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from codeguarder.stage5_paper.detectors.garak_adapter import GarakDetectorAdapter
from codeguarder.stage5_paper.detectors.pattern_detector import Stage5PatternDetector


class DetectorAdapterTests(unittest.TestCase):
    def test_pattern_source_is_exact(self):
        verdict = Stage5PatternDetector().evaluate(
            "SYNTHETIC_MARKER", ("SYNTHETIC_MARKER",), target="raw"
        )
        self.assertEqual("stage5_pattern", verdict.detector_source)
        self.assertTrue(verdict.risk)

    def test_official_garak_detector_runs_without_scheduler(self):
        verdicts = GarakDetectorAdapter(
            ("promptinject.AttackRogueString",)
        ).evaluate(
            prompt="test",
            output="I hate humans",
            notes={"triggers": ["I hate humans"]},
            target="raw",
        )
        self.assertEqual(1, len(verdicts))
        self.assertEqual("garak", verdicts[0].detector_source)
        self.assertEqual(1.0, verdicts[0].score)
        self.assertTrue(verdicts[0].risk)

    def test_no_official_detector_is_not_applicable(self):
        verdict = GarakDetectorAdapter(()).not_applicable("raw")
        self.assertEqual("not_applicable", verdict.coverage)
        self.assertIsNone(verdict.risk)


if __name__ == "__main__":
    unittest.main()
