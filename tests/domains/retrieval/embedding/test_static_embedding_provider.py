from __future__ import annotations

import math
import unittest

from llmguard.domains.retrieval.embedding.model_spec import EmbeddingModelSpec
from llmguard.domains.retrieval.embedding.static_provider import (
    EmbeddingInputError,
    StaticEmbeddingProvider,
)


FIXED_REVISION = "16e5344fbfc7dfbbbe0019d30cec21e2940cb4e1"


def make_spec(**overrides: object) -> EmbeddingModelSpec:
    values: dict[str, object] = {
        "provider": "static",
        "model_id": "llmguard/static-fixture",
        "revision": FIXED_REVISION,
        "dimension": 8,
        "normalize_embeddings": True,
        "device": "cpu",
        "batch_size": 4,
        "trust_remote_code": False,
        "local_files_only": True,
        "implementation_version": "s6_t4_static_v1",
    }
    values.update(overrides)
    return EmbeddingModelSpec(**values)  # type: ignore[arg-type]


class StaticEmbeddingProviderTests(unittest.TestCase):
    def test_same_input_produces_identical_read_only_finite_vectors(self) -> None:
        provider = StaticEmbeddingProvider(make_spec())

        first = provider.embed_documents(("alpha", "beta"))
        second = provider.embed_documents(("alpha", "beta"))

        self.assertEqual(first, second)
        self.assertIsInstance(first, tuple)
        self.assertEqual((8, 8), tuple(len(vector) for vector in first))
        self.assertTrue(all(math.isfinite(value) for vector in first for value in vector))
        with self.assertRaises(TypeError):
            first[0][0] = 0.0  # type: ignore[index]

    def test_explicit_fixture_vectors_support_known_similarity_cases(self) -> None:
        provider = StaticEmbeddingProvider(
            make_spec(dimension=3),
            fixture_vectors={
                "north": (1.0, 0.0, 0.0),
                "south": (-1.0, 0.0, 0.0),
            },
        )

        self.assertEqual((1.0, 0.0, 0.0), provider.embed_query("north"))
        self.assertEqual((-1.0, 0.0, 0.0), provider.embed_query("south"))

    def test_empty_batch_is_empty_and_blank_text_is_rejected_without_echoing_text(self) -> None:
        provider = StaticEmbeddingProvider(make_spec())

        self.assertEqual((), provider.embed_documents(()))
        with self.assertRaisesRegex(EmbeddingInputError, "index 0") as raised:
            provider.embed_documents(("   ",))
        self.assertNotIn("   ", str(raised.exception))


if __name__ == "__main__":
    unittest.main()
