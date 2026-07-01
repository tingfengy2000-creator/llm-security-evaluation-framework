import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from codeguarder.stage5_paper.audit.attempt_record import ExperimentConfig
from codeguarder.stage5_paper.audit.canonical_log import write_canonical_attempts
from codeguarder.stage5_paper.audit.fingerprints import (
    attempt_id,
    experiment_fingerprint,
    sha256_file,
)


class DeterministicLogTests(unittest.TestCase):
    def test_stable_fingerprint_and_attempt_id(self):
        config = ExperimentConfig(
            schema_version="2.0",
            dataset_manifest_hash="dataset",
            provider="mock",
            model="mock-paper",
            seed=42,
            generation_config={"temperature": 0, "max_tokens": 160},
            detector_config=("stage5_pattern",),
            guard_version="stage4-rule-baseline",
        )
        first = experiment_fingerprint(config)
        second = experiment_fingerprint(config)
        self.assertEqual(first, second)
        self.assertEqual(
            attempt_id(first, "A4-PM-001", "O", 0),
            attempt_id(second, "A4-PM-001", "O", 0),
        )

    def test_canonical_writer_sorts_and_is_byte_identical(self):
        records = [
            {"attack_id": "A4", "sample_id": "z", "guard_code": "F", "attempt_id": "2"},
            {"attack_id": "A1", "sample_id": "a", "guard_code": "P", "attempt_id": "1"},
        ]
        with tempfile.TemporaryDirectory() as tmp:
            first = Path(tmp) / "first.jsonl"
            second = Path(tmp) / "second.jsonl"
            write_canonical_attempts(first, records)
            write_canonical_attempts(second, list(reversed(records)))
            self.assertEqual(sha256_file(first), sha256_file(second))


if __name__ == "__main__":
    unittest.main()
