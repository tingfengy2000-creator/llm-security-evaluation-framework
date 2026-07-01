import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from codeguarder.evaluation.validators import validate_no_secret_leak


class NoKeyLeakTests(unittest.TestCase):
    def test_clean_file_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "report.md"
            path.write_text("Only hashes and aggregate metrics.", encoding="utf-8")
            self.assertEqual([], validate_no_secret_leak([path]))

    def test_credential_markers_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "report.json"
            path.write_text('{"header":"Bearer example"}', encoding="utf-8")
            issues = validate_no_secret_leak([path])
            self.assertIn("secret_leak", {issue.code for issue in issues})

