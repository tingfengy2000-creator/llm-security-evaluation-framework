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


if __name__ == "__main__":
    unittest.main()
