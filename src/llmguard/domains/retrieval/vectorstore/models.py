"""Stable VectorStore domain objects and public metadata validation."""

from __future__ import annotations

import math
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime, timedelta
from types import MappingProxyType

from llmguard.domains.retrieval.contracts.content_ref import ContentRef


PUBLIC_METADATA_FIELDS = frozenset(
    {
        "doc_id",
        "source_id",
        "source_type",
        "timestamp",
        "version",
        "content_hash",
        "corpus_snapshot_id",
        "chunk_index",
        "language",
    }
)
FORBIDDEN_METADATA_FIELDS = frozenset(
    {
        "poisoned",
        "poison_label",
        "label",
        "attack_id",
        "attack_goal",
        "attack_category",
        "expected_answer",
        "expected_behavior",
        "failure_type",
        "ground_truth",
        "oracle",
        "risk_goal",
        "stealth_level",
    }
)
_SHA256 = re.compile(r"\A[0-9a-f]{64}\Z")
_UTC_ISO8601 = re.compile(r"\A\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|\+00:00)\Z")


class VectorStoreError(RuntimeError):
    """Base error for vector storage infrastructure."""


class VectorDimensionError(VectorStoreError):
    """Raised when a vector dimension does not fit its collection."""


class VectorStoreConfigurationError(VectorStoreError):
    """Raised for incompatible collection or store configuration."""


class VectorStorePersistenceError(VectorStoreError):
    """Raised for persistent vector store open or write failures."""


class VectorStoreQueryError(VectorStoreError):
    """Raised for invalid query execution without exposing query content."""


class CollectionFingerprintMismatchError(VectorStoreConfigurationError):
    """Raised when an existing collection has different immutable provenance."""


class MetadataIsolationError(VectorStoreError):
    """Raised when metadata is not part of the public retrieval schema."""


def _require_nonblank(value: object, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a nonblank string")
    return value


def _require_sha256(value: object, field_name: str) -> str:
    if not isinstance(value, str) or _SHA256.fullmatch(value) is None:
        raise ValueError(f"{field_name} must be a lowercase SHA-256 digest")
    return value


def _freeze_vector(vector: Sequence[float], field_name: str) -> tuple[float, ...]:
    if isinstance(vector, (str, bytes, bytearray)) or not isinstance(vector, Sequence):
        raise ValueError(f"{field_name} must be a numeric sequence")
    values: list[float] = []
    for index, value in enumerate(vector):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{field_name}[{index}] must be a finite number")
        number = float(value)
        if not math.isfinite(number):
            raise ValueError(f"{field_name}[{index}] must be a finite number")
        values.append(number)
    if not values:
        raise ValueError(f"{field_name} must not be empty")
    return tuple(values)


def _validate_timestamp(value: object, field_name: str) -> str:
    timestamp = _require_nonblank(value, field_name)
    if _UTC_ISO8601.fullmatch(timestamp) is None:
        raise MetadataIsolationError(f"{field_name} must use UTC ISO-8601 syntax")
    try:
        parsed = datetime.fromisoformat(timestamp)
    except ValueError as error:
        raise MetadataIsolationError(f"{field_name} must be a valid UTC timestamp") from error
    if parsed.tzinfo is None or parsed.utcoffset() != timedelta(0):
        raise MetadataIsolationError(f"{field_name} must include a UTC offset")
    return timestamp


def validate_public_metadata(
    metadata: Mapping[str, object],
    *,
    doc_id: str | None = None,
) -> Mapping[str, str | int]:
    """Freeze only schema-approved public metadata for vector persistence."""

    if not isinstance(metadata, Mapping):
        raise MetadataIsolationError("metadata must be a mapping")
    values: dict[str, str | int] = {}
    for key, value in metadata.items():
        if not isinstance(key, str):
            raise MetadataIsolationError("metadata keys must be strings")
        if key in FORBIDDEN_METADATA_FIELDS or key not in PUBLIC_METADATA_FIELDS:
            raise MetadataIsolationError(f"metadata field '{key}' is not approved")
        if isinstance(value, Mapping) or isinstance(value, (list, tuple, set, frozenset)):
            raise MetadataIsolationError(f"metadata field '{key}' must be a scalar")
        if key in {"doc_id", "source_id", "source_type", "version", "corpus_snapshot_id", "language"}:
            values[key] = _require_nonblank(value, f"metadata.{key}")
        elif key == "timestamp":
            values[key] = _validate_timestamp(value, "metadata.timestamp")
        elif key == "content_hash":
            values[key] = _require_sha256(value, "metadata.content_hash")
        elif key == "chunk_index":
            if type(value) is not int or value < 0:
                raise MetadataIsolationError("metadata.chunk_index must be a nonnegative integer")
            values[key] = value
        else:  # pragma: no cover - maintained for defensive future schema edits.
            raise MetadataIsolationError(f"metadata field '{key}' is not supported")
    if doc_id is not None and "doc_id" in values and values["doc_id"] != doc_id:
        raise MetadataIsolationError("metadata.doc_id must match the vector document id")
    return MappingProxyType({key: values[key] for key in sorted(values)})


@dataclass(frozen=True, slots=True)
class VectorDocument:
    """A content-independent vector row for a public retrieval collection."""

    doc_id: str
    vector: Sequence[float]
    metadata: Mapping[str, object]
    content_hash: str
    content_ref: str

    def __post_init__(self) -> None:
        doc_id = _require_nonblank(self.doc_id, "doc_id")
        vector = _freeze_vector(self.vector, "vector")
        content_hash = _require_sha256(self.content_hash, "content_hash")
        content_ref = ContentRef(self.content_ref)
        if content_ref.scheme != "chroma":
            raise ValueError("VectorDocument supports legacy chroma content references only")
        metadata = validate_public_metadata(self.metadata, doc_id=doc_id)
        if "content_hash" in metadata and metadata["content_hash"] != content_hash:
            raise MetadataIsolationError("metadata.content_hash must match content_hash")
        object.__setattr__(self, "doc_id", doc_id)
        object.__setattr__(self, "vector", vector)
        object.__setattr__(self, "content_hash", content_hash)
        object.__setattr__(self, "content_ref", content_ref)
        object.__setattr__(self, "metadata", metadata)


@dataclass(frozen=True, slots=True)
class VectorSearchQuery:
    """A numeric search request that deliberately carries no query text."""

    vector: Sequence[float]
    top_k: int

    def __post_init__(self) -> None:
        if type(self.top_k) is not int or self.top_k <= 0:
            raise ValueError("top_k must be a positive integer")
        object.__setattr__(self, "vector", _freeze_vector(self.vector, "vector"))


@dataclass(frozen=True, slots=True)
class VectorSearchHit:
    """Stable, Chroma-independent hit returned to a future Retriever layer."""

    doc_id: str
    distance: float
    similarity: float
    metadata: Mapping[str, object]
    rank: int

    def __post_init__(self) -> None:
        doc_id = _require_nonblank(self.doc_id, "doc_id")
        if type(self.rank) is not int or self.rank <= 0:
            raise ValueError("rank must be a positive integer")
        for name, value in (("distance", self.distance), ("similarity", self.similarity)):
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
                raise ValueError(f"{name} must be finite")
        if self.distance < 0:
            raise ValueError("distance must be nonnegative")
        if not -1.0 <= self.similarity <= 1.0:
            raise ValueError("similarity must be between -1 and 1")
        object.__setattr__(self, "doc_id", doc_id)
        object.__setattr__(self, "distance", float(self.distance))
        object.__setattr__(self, "similarity", float(self.similarity))
        object.__setattr__(self, "metadata", validate_public_metadata(self.metadata, doc_id=doc_id))


@dataclass(frozen=True, slots=True)
class VectorCollectionSpec:
    """Immutable collection identity used by in-memory and Chroma adapters."""

    fingerprint: str
    dimension: int
    distance_metric: str = "cosine"
    vector_schema_version: str = "1.0"
    public_metadata_schema_version: str = "1.0"

    def __post_init__(self) -> None:
        _require_sha256(self.fingerprint, "fingerprint")
        if type(self.dimension) is not int or self.dimension <= 0:
            raise VectorStoreConfigurationError("dimension must be a positive integer")
        if self.distance_metric != "cosine":
            raise VectorStoreConfigurationError(
                "S6-T4 VectorStore supports only cosine distance"
            )
        _require_nonblank(self.vector_schema_version, "vector_schema_version")
        _require_nonblank(
            self.public_metadata_schema_version,
            "public_metadata_schema_version",
        )

    @property
    def collection_name(self) -> str:
        return f"llmguard_s6_{self.fingerprint[:24]}"


@dataclass(frozen=True, slots=True)
class VectorCollectionInfo:
    """Public collection provenance without database-specific internal objects."""

    collection_name: str
    fingerprint: str
    dimension: int
    distance_metric: str
    count: int
    vector_schema_version: str
    public_metadata_schema_version: str
