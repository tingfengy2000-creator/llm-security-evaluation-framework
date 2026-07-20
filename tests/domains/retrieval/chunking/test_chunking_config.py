from __future__ import annotations

import unittest

from llmguard.domains.retrieval.contracts import (
    ChunkingConfig,
    ChunkingStrategy,
)


class ChunkingConfigTests(unittest.TestCase):
    def test_identity_config_has_a_stable_minimal_hash(self) -> None:
        first = ChunkingConfig(
            strategy=ChunkingStrategy.IDENTITY,
            schema_version="1.0",
            implementation_version="s6_t5_1_v1",
        )
        second = ChunkingConfig(
            strategy=ChunkingStrategy.IDENTITY,
            schema_version="1.0",
            implementation_version="s6_t5_1_v1",
        )

        self.assertEqual(first.fingerprint(), second.fingerprint())
        self.assertEqual(
            {
                "implementation_version": "s6_t5_1_v1",
                "schema_version": "1.0",
                "strategy": "identity",
            },
            first.canonical_payload(),
        )
        self.assertEqual(
            '{"implementation_version":"s6_t5_1_v1","schema_version":"1.0","strategy":"identity"}',
            first.canonical_json(),
        )

    def test_identity_config_rejects_irrelevant_algorithm_parameters(self) -> None:
        with self.assertRaisesRegex(ValueError, "identity"):
            ChunkingConfig(
                strategy=ChunkingStrategy.IDENTITY,
                schema_version="1.0",
                implementation_version="s6_t5_1_v1",
                max_tokens=128,
            )

    def test_future_strategy_is_expressible_but_strictly_validated(self) -> None:
        config = ChunkingConfig(
            strategy=ChunkingStrategy.TOKEN_OVERLAP,
            schema_version="1.0",
            implementation_version="future_contract_v1",
            tokenizer_model_id="tokenizer/example",
            tokenizer_revision="0123456789abcdef0123456789abcdef01234567",
            max_tokens=128,
            overlap_tokens=32,
        )

        self.assertEqual(64, len(config.fingerprint()))
        with self.assertRaisesRegex(ValueError, "overlap_tokens"):
            ChunkingConfig(
                strategy=ChunkingStrategy.TOKEN_OVERLAP,
                schema_version="1.0",
                implementation_version="future_contract_v1",
                tokenizer_model_id="tokenizer/example",
                tokenizer_revision="0123456789abcdef0123456789abcdef01234567",
                max_tokens=128,
                overlap_tokens=128,
            )


if __name__ == "__main__":
    unittest.main()
