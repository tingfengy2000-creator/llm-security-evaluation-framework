from __future__ import annotations

import unittest
from collections.abc import Sequence

from llmguard.domains.retrieval.embedding.base import (
    EmbeddingDimensionError,
    EmbeddingModelLoadError,
    EmbeddingRuntimeError,
)
from llmguard.domains.retrieval.embedding.model_spec import EmbeddingModelSpec
from llmguard.domains.retrieval.embedding.sentence_transformer_provider import (
    SentenceTransformerEmbeddingProvider,
)


FIXED_REVISION = "16e5344fbfc7dfbbbe0019d30cec21e2940cb4e1"


def make_spec(**overrides: object) -> EmbeddingModelSpec:
    values: dict[str, object] = {
        "provider": "sentence_transformers",
        "model_id": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        "revision": FIXED_REVISION,
        "dimension": 384,
        "normalize_embeddings": True,
        "device": "cpu",
        "batch_size": 2,
        "trust_remote_code": False,
        "local_files_only": True,
        "implementation_version": "s6_t4_sentence_transformers_v1",
        "document_prefix": "document: ",
        "query_prefix": "query: ",
    }
    values.update(overrides)
    return EmbeddingModelSpec(**values)  # type: ignore[arg-type]


class FakeSentenceTransformer:
    def __init__(self, output_dimension: int = 384) -> None:
        self.output_dimension = output_dimension
        self.calls: list[tuple[tuple[str, ...], dict[str, object]]] = []

    def encode(self, texts: Sequence[str], **kwargs: object) -> list[list[float]]:
        self.calls.append((tuple(texts), kwargs))
        return [[1.0] + [0.0] * (self.output_dimension - 1) for _ in texts]


class SentenceTransformerProviderContractTests(unittest.TestCase):
    def test_loading_is_lazy_and_forwards_frozen_model_settings(self) -> None:
        loaded: list[dict[str, object]] = []
        fake_model = FakeSentenceTransformer()

        def loader(**kwargs: object) -> FakeSentenceTransformer:
            loaded.append(kwargs)
            return fake_model

        source_texts = ("第一条文档", "second document")
        provider = SentenceTransformerEmbeddingProvider(make_spec(), model_loader=loader)
        self.assertEqual([], loaded)

        vectors = provider.embed_documents(source_texts)
        query_vector = provider.embed_query("查询")

        self.assertEqual(source_texts, ("第一条文档", "second document"))
        self.assertEqual(1, len(loaded))
        self.assertEqual(FIXED_REVISION, loaded[0]["revision"])
        self.assertIs(False, loaded[0]["trust_remote_code"])
        self.assertIs(True, loaded[0]["local_files_only"])
        self.assertEqual("cpu", loaded[0]["device"])
        self.assertEqual((384, 384), tuple(len(vector) for vector in vectors))
        self.assertEqual(384, len(query_vector))
        self.assertEqual(("document: 第一条文档", "document: second document"), fake_model.calls[0][0])
        self.assertEqual(("query: 查询",), fake_model.calls[1][0])
        self.assertEqual(2, fake_model.calls[0][1]["batch_size"])
        self.assertIs(True, fake_model.calls[0][1]["normalize_embeddings"])
        self.assertEqual(FIXED_REVISION, provider.runtime_metadata()["revision"])

    def test_bad_provider_output_and_load_failure_are_classified_without_fallback(self) -> None:
        provider = SentenceTransformerEmbeddingProvider(
            make_spec(),
            model_loader=lambda **_: FakeSentenceTransformer(output_dimension=383),
        )
        with self.assertRaises(EmbeddingDimensionError):
            provider.embed_query("query")

        def failing_loader(**_: object) -> FakeSentenceTransformer:
            raise OSError("model cannot be resolved")

        unavailable = SentenceTransformerEmbeddingProvider(make_spec(), model_loader=failing_loader)
        with self.assertRaises(EmbeddingModelLoadError):
            unavailable.embed_query("query")

    def test_runtime_failure_is_classified(self) -> None:
        class FailingModel(FakeSentenceTransformer):
            def encode(self, texts: Sequence[str], **kwargs: object) -> list[list[float]]:
                raise RuntimeError("backend failure")

        provider = SentenceTransformerEmbeddingProvider(
            make_spec(),
            model_loader=lambda **_: FailingModel(),
        )
        with self.assertRaises(EmbeddingRuntimeError):
            provider.embed_documents(("document",))


if __name__ == "__main__":
    unittest.main()
