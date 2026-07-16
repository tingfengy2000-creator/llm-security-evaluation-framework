from __future__ import annotations

import ast
import inspect
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class SingleCanonicalImplementationTests(unittest.TestCase):
    def test_stage6_contract_classes_are_defined_only_in_llmguard(self) -> None:
        from codeguarder.stage6_rag.contracts import DocumentRecord as old_document
        from llmguard.domains.retrieval.contracts import DocumentRecord
        from llmguard.domains.retrieval.contracts import QueryRecord

        self.assertIs(old_document, DocumentRecord)
        self.assertEqual(
            "llmguard.domains.retrieval.contracts.models",
            inspect.getmodule(DocumentRecord).__name__,
        )
        self.assertEqual(
            "llmguard.domains.retrieval.contracts.models",
            inspect.getmodule(QueryRecord).__name__,
        )

    def test_legacy_modules_contain_no_class_definitions(self) -> None:
        legacy_root = ROOT / "src" / "codeguarder" / "stage6_rag"
        for source_path in legacy_root.rglob("*.py"):
            with self.subTest(source_path=source_path.relative_to(ROOT)):
                module = ast.parse(source_path.read_text(encoding="utf-8"))
                self.assertFalse(
                    any(isinstance(node, ast.ClassDef) for node in module.body)
                )


if __name__ == "__main__":
    unittest.main()
