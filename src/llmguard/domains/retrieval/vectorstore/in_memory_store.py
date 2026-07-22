"""Deterministic in-memory VectorStore used only by fast tests."""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass, field

from .models import (
    VectorCollectionInfo,
    VectorCollectionSpec,
    VectorDimensionError,
    VectorDocument,
    VectorSearchHit,
    VectorSearchQuery,
    VectorStoreConfigurationError,
    VectorStoreQueryError,
    validate_metadata_for_schema,
)


@dataclass(slots=True)
class _MemoryCollection:
    spec: VectorCollectionSpec
    documents: dict[str, VectorDocument] = field(default_factory=dict)


class InMemoryVectorStore:
    """Cosine VectorStore with deterministic tie-breaking and no persistence."""

    def __init__(self) -> None:
        self._collections: dict[str, _MemoryCollection] = {}
        self._closed = False

    def create_or_open_collection(
        self,
        collection: VectorCollectionSpec,
    ) -> VectorCollectionInfo:
        self._require_open()
        existing = self._collections.get(collection.fingerprint)
        if existing is None:
            existing = _MemoryCollection(spec=collection)
            self._collections[collection.fingerprint] = existing
        elif existing.spec != collection:
            raise VectorStoreConfigurationError(
                "existing collection fingerprint has incompatible configuration"
            )
        return self._collection_info(existing)

    def upsert(
        self,
        collection: VectorCollectionSpec,
        documents: Sequence[VectorDocument],
    ) -> None:
        memory_collection = self._open_existing(collection)
        for document in documents:
            self._validate_dimension(document.vector, collection.dimension, document.doc_id)
            self._require_nonzero(document.vector, "document vector")
            validate_metadata_for_schema(
                document.metadata,
                doc_id=document.doc_id,
                public_metadata_schema_version=collection.public_metadata_schema_version,
            )
        for document in documents:
            memory_collection.documents[document.doc_id] = document

    def query(
        self,
        collection: VectorCollectionSpec,
        query: VectorSearchQuery,
    ) -> tuple[VectorSearchHit, ...]:
        memory_collection = self._open_existing(collection)
        self._validate_dimension(query.vector, collection.dimension, "query")
        self._require_nonzero(query.vector, "query vector")
        scored = [
            (
                1.0 - self._cosine_similarity(query.vector, document.vector),
                document.doc_id,
                document,
            )
            for document in memory_collection.documents.values()
        ]
        scored.sort(key=lambda item: (item[0], item[1]))
        return tuple(
            VectorSearchHit(
                doc_id=document.doc_id,
                distance=distance,
                similarity=1.0 - distance,
                metadata=validate_metadata_for_schema(
                    document.metadata,
                    doc_id=document.doc_id,
                    public_metadata_schema_version=collection.public_metadata_schema_version,
                ),
                rank=rank,
            )
            for rank, (distance, _, document) in enumerate(
                scored[: query.top_k],
                start=1,
            )
        )

    def count(self, collection: VectorCollectionSpec) -> int:
        return len(self._open_existing(collection).documents)

    def get_collection_info(
        self,
        collection: VectorCollectionSpec,
    ) -> VectorCollectionInfo:
        return self._collection_info(self._open_existing(collection))

    def close(self) -> None:
        self._closed = True
        self._collections.clear()

    def _open_existing(self, collection: VectorCollectionSpec) -> _MemoryCollection:
        self._require_open()
        existing = self._collections.get(collection.fingerprint)
        if existing is None:
            raise VectorStoreConfigurationError("collection has not been created")
        if existing.spec != collection:
            raise VectorStoreConfigurationError(
                "existing collection fingerprint has incompatible configuration"
            )
        return existing

    def _require_open(self) -> None:
        if self._closed:
            raise VectorStoreConfigurationError("vector store is closed")

    @staticmethod
    def _validate_dimension(
        vector: Sequence[float],
        dimension: int,
        subject: str,
    ) -> None:
        if len(vector) != dimension:
            raise VectorDimensionError(
                f"{subject} vector dimension {len(vector)} does not match {dimension}"
            )

    @staticmethod
    def _require_nonzero(vector: Sequence[float], subject: str) -> None:
        if math.sqrt(sum(value * value for value in vector)) == 0.0:
            raise VectorStoreQueryError(f"{subject} must not be a zero vector")

    @staticmethod
    def _cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
        denominator = math.sqrt(sum(value * value for value in left)) * math.sqrt(
            sum(value * value for value in right)
        )
        if denominator == 0.0:
            raise VectorStoreQueryError("cosine similarity requires nonzero vectors")
        similarity = sum(a * b for a, b in zip(left, right, strict=True)) / denominator
        return max(-1.0, min(1.0, similarity))

    @staticmethod
    def _collection_info(collection: _MemoryCollection) -> VectorCollectionInfo:
        spec = collection.spec
        return VectorCollectionInfo(
            collection_name=spec.collection_name,
            fingerprint=spec.fingerprint,
            dimension=spec.dimension,
            distance_metric=spec.distance_metric,
            count=len(collection.documents),
            vector_schema_version=spec.vector_schema_version,
            public_metadata_schema_version=spec.public_metadata_schema_version,
        )
