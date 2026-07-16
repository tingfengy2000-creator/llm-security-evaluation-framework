"""Provider-neutral embedding contracts and validation helpers."""

from __future__ import annotations

import math
from collections.abc import Sequence
from typing import TYPE_CHECKING, Protocol, TypeAlias, runtime_checkable


if TYPE_CHECKING:
    from .model_spec import EmbeddingModelSpec


EmbeddingVector: TypeAlias = tuple[float, ...]
EmbeddingBatch: TypeAlias = tuple[EmbeddingVector, ...]


class EmbeddingError(RuntimeError):
    """Base error for provider-neutral embedding failures."""


class EmbeddingConfigurationError(EmbeddingError):
    """Raised when an embedding configuration violates the frozen contract."""


class EmbeddingModelLoadError(EmbeddingError):
    """Raised when a configured embedding model cannot be loaded."""


class EmbeddingDimensionError(EmbeddingError):
    """Raised when a provider output does not match its declared dimension."""


class EmbeddingInputError(EmbeddingError):
    """Raised for invalid text input without echoing user-provided content."""


class EmbeddingRuntimeError(EmbeddingError):
    """Raised for provider execution failures that are not configuration errors."""


@runtime_checkable
class EmbeddingProvider(Protocol):
    """Stable provider interface used by later VectorStore infrastructure."""

    @property
    def model_spec(self) -> EmbeddingModelSpec:
        """Return the immutable configuration that defines provider behaviour."""

    @property
    def dimension(self) -> int:
        """Return the fixed output dimension declared by ``model_spec``."""

    def embed_documents(self, texts: Sequence[str]) -> EmbeddingBatch:
        """Embed a document batch without mutating or logging its text."""

    def embed_query(self, text: str) -> EmbeddingVector:
        """Embed one query without mutating or logging its text."""


def validate_text_batch(texts: Sequence[str]) -> tuple[str, ...]:
    """Validate text inputs while keeping errors free of the original text."""

    if isinstance(texts, (str, bytes, bytearray)):
        raise EmbeddingInputError("texts must be a sequence of strings")

    validated: list[str] = []
    for index, text in enumerate(texts):
        if not isinstance(text, str) or not text.strip():
            raise EmbeddingInputError(f"text at index {index} must be nonblank")
        validated.append(text)
    return tuple(validated)


def validate_embedding_vector(
    vector: Sequence[float],
    *,
    expected_dimension: int,
    output_index: int | None = None,
) -> EmbeddingVector:
    """Return a finite immutable vector with exactly ``expected_dimension`` values."""

    if isinstance(vector, (str, bytes, bytearray)):
        raise EmbeddingDimensionError("embedding output must be a numeric sequence")
    if len(vector) != expected_dimension:
        label = "embedding output" if output_index is None else f"embedding output {output_index}"
        raise EmbeddingDimensionError(
            f"{label} dimension {len(vector)} does not match {expected_dimension}"
        )

    validated: list[float] = []
    for component_index, value in enumerate(vector):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise EmbeddingRuntimeError(
                f"embedding component {component_index} must be a finite number"
            )
        number = float(value)
        if not math.isfinite(number):
            raise EmbeddingRuntimeError(
                f"embedding component {component_index} must be finite"
            )
        validated.append(number)
    return tuple(validated)


def validate_embedding_batch(
    vectors: Sequence[Sequence[float]],
    *,
    expected_count: int,
    expected_dimension: int,
) -> EmbeddingBatch:
    """Validate provider batch cardinality, dimensions and numeric finiteness."""

    if len(vectors) != expected_count:
        raise EmbeddingRuntimeError(
            "embedding output count does not match input text count"
        )
    return tuple(
        validate_embedding_vector(
            vector,
            expected_dimension=expected_dimension,
            output_index=index,
        )
        for index, vector in enumerate(vectors)
    )
