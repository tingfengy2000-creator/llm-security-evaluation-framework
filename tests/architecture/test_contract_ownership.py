from __future__ import annotations

import inspect
import unittest


class ChunkingContractOwnershipTests(unittest.TestCase):
    def test_chunking_stable_dtos_are_owned_by_contracts(self) -> None:
        from llmguard.domains.retrieval.contracts import (
            ChunkRecord,
            ChunkingConfig,
            ChunkingStrategy,
        )

        for contract in (ChunkRecord, ChunkingConfig, ChunkingStrategy):
            with self.subTest(contract=contract.__name__):
                self.assertEqual(
                    "llmguard.domains.retrieval.contracts.chunking",
                    inspect.getmodule(contract).__name__,
                )

    def test_chunking_package_exposes_behavior_not_duplicate_models(self) -> None:
        from llmguard.domains.retrieval.chunking import IdentityChunker

        self.assertEqual(
            "llmguard.domains.retrieval.chunking.identity_chunker",
            inspect.getmodule(IdentityChunker).__name__,
        )

    def test_chunking_errors_are_owned_by_contracts_and_reexported_by_behavior(self) -> None:
        from llmguard.domains.retrieval.chunking import ChunkingIntegrityError as legacy
        from llmguard.domains.retrieval.contracts import ChunkingIntegrityError

        self.assertIs(ChunkingIntegrityError, legacy)
        self.assertEqual(
            "llmguard.domains.retrieval.contracts.errors",
            inspect.getmodule(ChunkingIntegrityError).__name__,
        )


if __name__ == "__main__":
    unittest.main()
