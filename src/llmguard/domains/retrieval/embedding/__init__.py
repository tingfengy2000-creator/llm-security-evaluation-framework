"""Embedding configuration and provider contracts for S6-T4."""

from .base import (
    EmbeddingConfigurationError,
    EmbeddingDimensionError,
    EmbeddingInputError,
    EmbeddingModelLoadError,
    EmbeddingProvider,
    EmbeddingRuntimeError,
    EmbeddingVector,
)
from .model_spec import EmbeddingModelSpec
from .sentence_transformer_provider import SentenceTransformerEmbeddingProvider
from .static_provider import StaticEmbeddingProvider

__all__ = [
    "EmbeddingConfigurationError",
    "EmbeddingDimensionError",
    "EmbeddingInputError",
    "EmbeddingModelLoadError",
    "EmbeddingModelSpec",
    "EmbeddingProvider",
    "EmbeddingRuntimeError",
    "EmbeddingVector",
    "SentenceTransformerEmbeddingProvider",
    "StaticEmbeddingProvider",
]
