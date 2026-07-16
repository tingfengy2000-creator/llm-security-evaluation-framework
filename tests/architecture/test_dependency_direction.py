from __future__ import annotations

import ast
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CANONICAL_ROOT = ROOT / "src" / "llmguard"
LEGACY_STAGE6_ROOT = ROOT / "src" / "codeguarder" / "stage6_rag"


class DependencyDirectionTests(unittest.TestCase):
    def test_canonical_llmguard_code_never_imports_codeguarder(self) -> None:
        for source_path in CANONICAL_ROOT.rglob("*.py"):
            with self.subTest(source_path=source_path.relative_to(ROOT)):
                source = source_path.read_text(encoding="utf-8")
                self.assertNotIn("codeguarder", source)

    def test_legacy_stage6_modules_are_reexport_only_facades(self) -> None:
        for source_path in LEGACY_STAGE6_ROOT.rglob("*.py"):
            with self.subTest(source_path=source_path.relative_to(ROOT)):
                module = ast.parse(source_path.read_text(encoding="utf-8"))
                self.assertFalse(
                    any(
                        isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))
                        for node in module.body
                    ),
                    "legacy facades must not define business logic",
                )
                self.assertIn("llmguard", source_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
