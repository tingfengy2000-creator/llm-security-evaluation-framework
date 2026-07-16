import subprocess
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EXPECTED_PINS = frozenset(
    {
        "chromadb==1.5.9",
        "sentence-transformers==5.6.0",
        "Pillow==12.2.0",
    }
)


def parse_effective_requirements(requirements):
    return frozenset(
        line
        for raw_line in requirements.splitlines()
        if (line := raw_line.strip()) and not line.startswith("#")
    )


class RequirementParsingTests(unittest.TestCase):
    def test_rejects_commented_near_miss_and_drifted_dependencies(self):
        invalid_requirements = (
            (
                "# chromadb==1.5.9\n"
                "sentence-transformers==5.6.0\n"
                "Pillow==12.2.0\n"
            ),
            (
                "chromadb==1.5.90\n"
                "sentence-transformers==5.6.0\n"
                "Pillow==12.2.0\n"
            ),
            (
                "chromadb==1.5.9 ; python_version >= '3.12'\n"
                "sentence-transformers==5.6.0\n"
                "Pillow==12.2.0\n"
            ),
        )

        for requirements in invalid_requirements:
            with self.subTest(requirements=requirements):
                self.assertNotEqual(
                    EXPECTED_PINS,
                    parse_effective_requirements(requirements),
                )


class DependencyContractTests(unittest.TestCase):
    def test_stage6_rag_dependency_and_runtime_contract(self):
        requirements = parse_effective_requirements(
            (ROOT / "requirements_stage6_rag_security.txt").read_text(encoding="utf-8")
        )
        with (ROOT / "pyproject.toml").open("rb") as pyproject_file:
            pyproject = tomllib.load(pyproject_file)

        project = pyproject["project"]
        optional_dependencies = frozenset(
            project["optional-dependencies"]["stage6_rag_security"]
        )
        ignored_runtime_paths = (
            "runtime/stage6_rag_security/.contract-probe",
            "runtime/stage6_rag_security/chroma/chroma.sqlite3",
        )

        self.assertEqual(EXPECTED_PINS, requirements)
        self.assertEqual(EXPECTED_PINS, optional_dependencies)
        self.assertEqual(requirements, optional_dependencies)
        self.assertEqual(">=3.12", project["requires-python"])
        for ignored_path in ignored_runtime_paths:
            with self.subTest(ignored_path=ignored_path):
                ignore_check = subprocess.run(
                    ["git", "check-ignore", "-v", "--", ignored_path],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(
                    0,
                    ignore_check.returncode,
                    msg=ignore_check.stderr or ignore_check.stdout,
                )


if __name__ == "__main__":
    unittest.main()
