from __future__ import annotations

import unittest


class NamespaceCompatibilityTests(unittest.TestCase):
    def test_legacy_stage6_types_are_canonical_llmguard_types(self) -> None:
        from codeguarder.stage6_rag.contracts import DocumentRecord as old_document
        from codeguarder.stage6_rag.contracts import QueryRecord as old_query
        from codeguarder.stage6_rag.contracts import validate_document as old_validate
        from codeguarder.stage6_rag.contracts.models import DocumentRecord as old_module_document
        from llmguard.domains.retrieval.contracts import DocumentRecord as new_document
        from llmguard.domains.retrieval.contracts import QueryRecord as new_query
        from llmguard.domains.retrieval.contracts import validate_document as new_validate

        self.assertIs(old_document, new_document)
        self.assertIs(old_module_document, new_document)
        self.assertIs(old_query, new_query)
        self.assertIs(old_validate, new_validate)

    def test_legacy_attack_loader_is_the_canonical_llmguard_loader(self) -> None:
        from codeguarder.stage6_rag.attacks import load_public_dataset as old_loader
        from llmguard.domains.retrieval.attacks import load_public_dataset as new_loader

        self.assertIs(old_loader, new_loader)


if __name__ == "__main__":
    unittest.main()
