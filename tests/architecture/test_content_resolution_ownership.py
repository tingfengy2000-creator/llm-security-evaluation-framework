from __future__ import annotations

import ast
import inspect
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RETRIEVAL_ROOT = ROOT / "src" / "llmguard" / "domains" / "retrieval"
CONTEXT_ROOT = RETRIEVAL_ROOT / "context"


class ContentResolutionOwnershipTests(unittest.TestCase):
    def test_resolved_content_has_one_canonical_contract_owner(self) -> None:
        from llmguard.domains.retrieval.contracts import ResolvedContent

        self.assertEqual(
            "llmguard.domains.retrieval.contracts.content_resolution",
            inspect.getmodule(ResolvedContent).__name__,
        )
        definitions = []
        for path in RETRIEVAL_ROOT.rglob("*.py"):
            module = ast.parse(path.read_text(encoding="utf-8"))
            definitions.extend(
                path
                for node in module.body
                if isinstance(node, ast.ClassDef) and node.name == "ResolvedContent"
            )
        self.assertEqual(
            [RETRIEVAL_ROOT / "contracts" / "content_resolution.py"], definitions
        )

    def test_context_is_behavior_only_and_has_no_forbidden_dependencies(self) -> None:
        self.assertFalse((CONTEXT_ROOT / "models.py").exists())
        for path in CONTEXT_ROOT.rglob("*.py"):
            source = path.read_text(encoding="utf-8")
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertNotIn("chromadb", source.casefold())
                self.assertNotIn("groundtruth", source.casefold())
                self.assertNotIn("codeguarder", source)

    def test_only_resolver_constructs_resolved_content_in_production_code(self) -> None:
        constructors = []
        for path in RETRIEVAL_ROOT.rglob("*.py"):
            module = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(module):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    if node.func.id == "ResolvedContent":
                        constructors.append(path)
        self.assertEqual([CONTEXT_ROOT / "resolver.py"], constructors)

    def test_context_errors_reexport_contract_errors_without_duplicate_classes(self) -> None:
        errors = CONTEXT_ROOT / "errors.py"
        module = ast.parse(errors.read_text(encoding="utf-8"))
        self.assertFalse(any(isinstance(node, ast.ClassDef) for node in module.body))


if __name__ == "__main__":
    unittest.main()
