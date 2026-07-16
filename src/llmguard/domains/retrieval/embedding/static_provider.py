"""Deterministic, offline-only embedding provider for fast infrastructure tests."""

from __future__ import annotations

import hashlib
import math
from collections.abc import Mapping, Sequence
from types import MappingProxyType

from .base import (
    EmbeddingBatch,
    EmbeddingConfigurationError,
    EmbeddingInputError,
    EmbeddingVector,
    validate_embedding_vector,
    validate_text_batch,
)
from .model_spec import EmbeddingModelSpec


class StaticEmbeddingProvider:
    """Generate stable vectors from SHA-256 or explicit non-sensitive fixtures."""

    def __init__(
        self,
        model_spec: EmbeddingModelSpec,
        *,
        fixture_vectors: Mapping[str, Sequence[float]] | None = None,
    ) -> None:
        if model_spec.provider != "static":
            raise EmbeddingConfigurationError(
                "StaticEmbeddingProvider requires model_spec.provider='static'"
            )
        self._model_spec = model_spec
        vectors = fixture_vectors or {}
        self._fixture_vectors = MappingProxyType(
            {
                text: validate_embedding_vector(
                    vector,
                    expected_dimension=model_spec.dimension,
                )
                for text, vector in vectors.items()
            }
        )

    @property
    def model_spec(self) -> EmbeddingModelSpec:
        return self._model_spec

    @property
    def dimension(self) -> int:
        return self._model_spec.dimension

    def embed_documents(self, texts: Sequence[str]) -> EmbeddingBatch:
        validated_texts = validate_text_batch(texts)
        return tuple(self._embed_one(text) for text in validated_texts)

    def embed_query(self, text: str) -> EmbeddingVector:
        if not isinstance(text, str) or not text.strip():
            raise EmbeddingInputError("query text must be nonblank")
        return self._embed_one(text)

    def _embed_one(self, text: str) -> EmbeddingVector:
        fixture = self._fixture_vectors.get(text)
        if fixture is not None:
            return self._normalize_if_configured(fixture)

        values: list[float] = []
        counter = 0
        text_bytes = text.encode("utf-8")
        while len(values) < self.dimension:
            digest = hashlib.sha256(
                b"llmguard-static-embedding-v1\x00"
                + counter.to_bytes(8, "big")
                + b"\x00"
                + text_bytes
            ).digest()
            for offset in range(0, len(digest), 8):
                value = int.from_bytes(digest[offset : offset + 8], "big")
                values.append((value / ((1 << 64) - 1)) * 2.0 - 1.0)
                if len(values) == self.dimension:
                    break
            counter += 1
        return self._normalize_if_configured(tuple(values))

    def _normalize_if_configured(self, vector: EmbeddingVector) -> EmbeddingVector:
        if not self.model_spec.normalize_embeddings:
            return vector
        norm = math.sqrt(sum(value * value for value in vector))
        if norm == 0.0:
            raise EmbeddingConfigurationError("static embedding fixture must be nonzero")
        return tuple(value / norm for value in vector)


__all__ = ["EmbeddingInputError", "StaticEmbeddingProvider"]
