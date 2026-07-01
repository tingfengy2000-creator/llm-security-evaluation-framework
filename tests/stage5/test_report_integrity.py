import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from codeguarder.evaluation.validators import validate_report_integrity
from codeguarder.evaluation.stage5_runner import run_experiment


class ReportIntegrityTests(unittest.TestCase):
    def test_complete_four_mode_record_set(self):
        records = [
            {
                "sample_id": "s1",
                "guard_mode": mode,
                "failure_types": [],
                "prompt_hash": "same",
            }
            for mode in (
                "passthrough",
                "input-only",
                "output-only",
                "full-guard",
            )
        ]
        self.assertEqual(
            [],
            validate_report_integrity(records, expected_sample_ids={"s1"}),
        )

    def test_missing_mode_invalid(self):
        records = [
            {
                "sample_id": "s1",
                "guard_mode": "passthrough",
                "failure_types": [],
                "prompt_hash": "same",
            }
        ]
        issues = validate_report_integrity(records, expected_sample_ids={"s1"})
        self.assertIn("report_integrity", {issue.code for issue in issues})

    def test_mock_end_to_end_writes_complete_88_attempt_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run_experiment(
                provider="mock",
                data_root=ROOT / "data" / "stage5",
                output_root=Path(tmp),
                per_category=2,
                include_benign=True,
                delay_seconds=0,
            )
            self.assertEqual("completed", result["run_status"])
            self.assertEqual(88, len(result["attempts"]))
            for filename in (
                "attack_matrix_result.json",
                "failure_taxonomy_result.json",
                "metrics_summary.csv",
                "attack_coverage_heatmap.csv",
            ):
                self.assertTrue((Path(tmp) / filename).is_file(), filename)
                self.assertTrue(
                    (Path(tmp) / "logs" / result["run_id"] / filename).is_file(),
                    f"run-scoped {filename}",
                )

    def test_stage5_script_sample_sizes_are_explicit(self):
        smoke = (ROOT / "scripts" / "run_stage5_smoke.ps1").read_text(
            encoding="utf-8"
        )
        full = (ROOT / "scripts" / "run_stage5_full.ps1").read_text(
            encoding="utf-8"
        )
        self.assertIn("--per-category 2", smoke)
        self.assertIn("--per-category 10", full)
