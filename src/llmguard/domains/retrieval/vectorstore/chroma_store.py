"""Persistent ChromaDB adapter behind the stable LLMGuard VectorStore contract."""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, cast

try:
    import chromadb
except ModuleNotFoundError:  # pragma: no cover - exercised only in missing-dependency environments.
    chromadb = None  # type: ignore[assignment]

from .models import (
    CollectionFingerprintMismatchError,
    VectorCollectionInfo,
    VectorCollectionSpec,
    VectorDimensionError,
    VectorDocument,
    VectorSearchHit,
    VectorSearchQuery,
    VectorStoreConfigurationError,
    VectorStorePersistenceError,
    VectorStoreQueryError,
    validate_public_metadata,
)


_DEFAULT_PERSIST_DIRECTORY = Path("runtime") / "stage6_rag_security" / "chroma"
_COLLECTION_METADATA_PREFIX = "llmguard_"


class ChromaVectorStore:
    """Persistent cosine store that never exposes raw Chroma return structures."""

    def __init__(self, persist_directory: Path | str = _DEFAULT_PERSIST_DIRECTORY) -> None:
        if chromadb is None:
            raise VectorStoreConfigurationError("chromadb dependency is unavailable")
        self._persist_directory = Path(persist_directory)
        self._collections: dict[str, tuple[VectorCollectionSpec, Any]] = {}
        self._closed = False
        try:
            self._client: Any = chromadb.PersistentClient(path=str(self._persist_directory))
        except Exception as error:
            raise VectorStorePersistenceError(
                "unable to initialize persistent Chroma vector store"
            ) from error

    def create_or_open_collection(
        self,
        collection: VectorCollectionSpec,
    ) -> VectorCollectionInfo:
        self._require_open()
        cached = self._collections.get(collection.fingerprint)
        if cached is not None:
            cached_spec, cached_collection = cached
            if cached_spec != collection:
                raise CollectionFingerprintMismatchError(
                    "cached collection fingerprint has incompatible configuration"
                )
            return self._collection_info(cached_spec, cached_collection)

        try:
            chroma_collection = self._client.get_or_create_collection(
                name=collection.collection_name,
                metadata=self._collection_metadata(collection),
                configuration={"hnsw": {"space": "cosine"}},
                embedding_function=None,
            )
        except Exception as error:
            raise VectorStorePersistenceError(
                "unable to create or open persistent vector collection"
            ) from error
        self._validate_collection_metadata(chroma_collection, collection)
        self._collections[collection.fingerprint] = (collection, chroma_collection)
        return self._collection_info(collection, chroma_collection)

    def upsert(
        self,
        collection: VectorCollectionSpec,
        documents: Sequence[VectorDocument],
    ) -> None:
        chroma_collection = self._open_existing(collection)
        for document in documents:
            self._validate_dimension(document.vector, collection.dimension, document.doc_id)
            self._require_nonzero(document.vector, "document vector")
        if not documents:
            return
        try:
            chroma_collection.upsert(
                ids=[document.doc_id for document in documents],
                embeddings=[list(document.vector) for document in documents],
                metadatas=[dict(document.metadata) for document in documents],
                # Chroma requires a documents field for some backends. This is a controlled
                # reference only; full source text remains outside the vector store.
                documents=[document.content_ref for document in documents],
            )
        except Exception as error:
            raise VectorStorePersistenceError(
                "unable to upsert public vectors into Chroma"
            ) from error

    def query(
        self,
        collection: VectorCollectionSpec,
        query: VectorSearchQuery,
    ) -> tuple[VectorSearchHit, ...]:
        chroma_collection = self._open_existing(collection)
        self._validate_dimension(query.vector, collection.dimension, "query")
        self._require_nonzero(query.vector, "query vector")
        count = self.count(collection)
        if count == 0:
            return ()
        try:
            raw_result = chroma_collection.query(
                query_embeddings=[list(query.vector)],
                n_results=min(query.top_k, count),
                include=["metadatas", "distances"],
            )
        except Exception as error:
            raise VectorStoreQueryError("Chroma vector query failed") from error
        return self._to_stable_hits(raw_result)

    def count(self, collection: VectorCollectionSpec) -> int:
        chroma_collection = self._open_existing(collection)
        try:
            return int(chroma_collection.count())
        except Exception as error:
            raise VectorStorePersistenceError("unable to count Chroma vector rows") from error

    def get_collection_info(
        self,
        collection: VectorCollectionSpec,
    ) -> VectorCollectionInfo:
        return self._collection_info(collection, self._open_existing(collection))

    def close(self) -> None:
        if self._closed:
            return
        try:
            self._client.close()
        except Exception as error:
            raise VectorStorePersistenceError("unable to close persistent Chroma store") from error
        self._collections.clear()
        self._closed = True

    def _open_existing(self, collection: VectorCollectionSpec) -> Any:
        self._require_open()
        cached = self._collections.get(collection.fingerprint)
        if cached is None:
            raise VectorStoreConfigurationError("collection has not been created or opened")
        cached_spec, chroma_collection = cached
        if cached_spec != collection:
            raise CollectionFingerprintMismatchError(
                "cached collection fingerprint has incompatible configuration"
            )
        return chroma_collection

    def _collection_info(
        self,
        collection: VectorCollectionSpec,
        chroma_collection: Any,
    ) -> VectorCollectionInfo:
        try:
            count = int(chroma_collection.count())
        except Exception as error:
            raise VectorStorePersistenceError("unable to inspect Chroma collection") from error
        return VectorCollectionInfo(
            collection_name=collection.collection_name,
            fingerprint=collection.fingerprint,
            dimension=collection.dimension,
            distance_metric=collection.distance_metric,
            count=count,
            vector_schema_version=collection.vector_schema_version,
            public_metadata_schema_version=collection.public_metadata_schema_version,
        )

    @staticmethod
    def _collection_metadata(collection: VectorCollectionSpec) -> dict[str, str | int]:
        return {
            f"{_COLLECTION_METADATA_PREFIX}fingerprint": collection.fingerprint,
            f"{_COLLECTION_METADATA_PREFIX}dimension": collection.dimension,
            f"{_COLLECTION_METADATA_PREFIX}distance_metric": collection.distance_metric,
            f"{_COLLECTION_METADATA_PREFIX}vector_schema_version": collection.vector_schema_version,
            f"{_COLLECTION_METADATA_PREFIX}public_metadata_schema_version": collection.public_metadata_schema_version,
        }

    def _validate_collection_metadata(
        self,
        chroma_collection: Any,
        collection: VectorCollectionSpec,
    ) -> None:
        metadata = getattr(chroma_collection, "metadata", None)
        if not isinstance(metadata, Mapping):
            raise CollectionFingerprintMismatchError(
                "existing Chroma collection does not expose LLMGuard provenance"
            )
        expected = self._collection_metadata(collection)
        for key, expected_value in expected.items():
            if metadata.get(key) != expected_value:
                raise CollectionFingerprintMismatchError(
                    "existing Chroma collection has incompatible provenance"
                )

    @staticmethod
    def _to_stable_hits(raw_result: Mapping[str, object]) -> tuple[VectorSearchHit, ...]:
        ids_outer = raw_result.get("ids")
        metadatas_outer = raw_result.get("metadatas")
        distances_outer = raw_result.get("distances")
        if not all(isinstance(value, list) and value for value in (ids_outer, metadatas_outer, distances_outer)):
            raise VectorStoreQueryError("Chroma query response is incomplete")
        ids_group = cast(list[object], ids_outer)[0]
        metadatas_group = cast(list[object], metadatas_outer)[0]
        distances_group = cast(list[object], distances_outer)[0]
        if not all(
            isinstance(value, list)
            for value in (ids_group, metadatas_group, distances_group)
        ):
            raise VectorStoreQueryError("Chroma query response has invalid result groups")
        ids = cast(list[object], ids_group)
        metadatas = cast(list[object], metadatas_group)
        distances = cast(list[object], distances_group)
        if not (len(ids) == len(metadatas) == len(distances)):
            raise VectorStoreQueryError("Chroma query response has inconsistent result counts")

        candidates: list[tuple[float, str, Mapping[str, object]]] = []
        for doc_id, metadata, distance in zip(ids, metadatas, distances, strict=True):
            if not isinstance(doc_id, str) or not isinstance(metadata, Mapping):
                raise VectorStoreQueryError("Chroma query response contains invalid metadata")
            if isinstance(distance, bool) or not isinstance(distance, (int, float)):
                raise VectorStoreQueryError("Chroma query response contains invalid distance")
            distance_value = float(distance)
            if not math.isfinite(distance_value) or distance_value < 0:
                raise VectorStoreQueryError("Chroma query response contains invalid distance")
            candidates.append(
                (
                    distance_value,
                    doc_id,
                    validate_public_metadata(metadata, doc_id=doc_id),
                )
            )
        candidates.sort(key=lambda item: (item[0], item[1]))
        return tuple(
            VectorSearchHit(
                doc_id=doc_id,
                distance=distance,
                similarity=max(-1.0, min(1.0, 1.0 - distance)),
                metadata=metadata,
                rank=rank,
            )
            for rank, (distance, doc_id, metadata) in enumerate(candidates, start=1)
        )

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
