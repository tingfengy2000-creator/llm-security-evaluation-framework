import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class DependencyContractTests(unittest.TestCase):
    def test_stage6_rag_dependency_and_runtime_contract(self):
        requirements = (ROOT / "requirements-stage6-rag.txt").read_text(
            encoding="utf-8"
        )
        gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")

        self.assertIn("chromadb==1.5.9", requirements)
        self.assertIn("sentence-transformers==5.6.0", requirements)
        self.assertIn("Pillow==12.2.0", requirements)
        self.assertIn("runtime/stage6_rag/", gitignore)
        self.assertIn("stage6-rag", pyproject)


if __name__ == "__main__":
    unittest.main()
