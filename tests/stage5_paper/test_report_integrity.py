import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from PIL import Image

from codeguarder.stage5_paper.audit.fingerprints import sha256_file
from codeguarder.stage5_paper.evaluation.stage5_runner import run_experiment


class ReportIntegrityTests(unittest.TestCase):
    def test_mock_runs_are_complete_and_canonical_logs_match(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            first = run_experiment(
                provider_name="mock",
                data_root=ROOT / "data" / "stage5_paper",
                output_root=output,
                include_benign=True,
                seed=42,
            )
            second = run_experiment(
                provider_name="mock",
                data_root=ROOT / "data" / "stage5_paper",
                output_root=output,
                include_benign=True,
                seed=42,
            )
            self.assertEqual("completed", first["run_status"])
            self.assertEqual(22, first["sample_count"])
            self.assertEqual(88, first["attempt_count"])
            self.assertEqual(
                first["experiment_fingerprint"],
                second["experiment_fingerprint"],
            )
            self.assertEqual(
                sha256_file(Path(first["run_dir"]) / "canonical_attempts.jsonl"),
                sha256_file(Path(second["run_dir"]) / "canonical_attempts.jsonl"),
            )
            required = {
                "experiment_result.json",
                "taxonomy_result.json",
                "metrics_summary.csv",
                "attack_heatmap.csv",
                "threat_layer_heatmap.csv",
                "canonical_attempts.jsonl",
                "measurements.jsonl",
                "run_manifest.json",
                "run_summary.md",
            }
            self.assertTrue(
                required
                <= {path.name for path in Path(first["run_dir"]).iterdir()}
            )

    def test_architecture_figure_is_figure_ready(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run_experiment(
                provider_name="mock",
                data_root=ROOT / "data" / "stage5_paper",
                output_root=Path(tmp),
                include_benign=False,
                seed=42,
            )
            figures = Path(result["output_root"]) / "figures"
            self.assertTrue((figures / "stage5_architecture.mmd").is_file())
            self.assertTrue((figures / "stage5_architecture.svg").is_file())
            png = figures / "stage5_architecture.png"
            self.assertTrue(png.is_file())
            with Image.open(png) as image:
                self.assertGreaterEqual(image.width, 2400)
                self.assertGreaterEqual(image.height, 1350)


if __name__ == "__main__":
    unittest.main()
