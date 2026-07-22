"""Transparent dense retrieval that stops at canonical evidence and trace records."""

from __future__ import annotations

import time
from collections.abc import Mapping
from typing import cast

from llmguard.domains.retrieval.contracts import (
    ContentRef,
    RetrievalConfigurationError,
    RetrievalEvidence,
    RetrievalEvidenceSummary,
    RetrievalInputError,
    RetrievalIntegrityError,
    RetrievalRequest,
    RetrievalTrace,
    derive_evidence_uid,
)
from llmguard.domains.retrieval.contracts.identifiers import require_sha256
from llmguard.domains.retrieval.embedding import EmbeddingProvider
from llmguard.domains.retrieval.embedding.base import (
    EmbeddingError,
    validate_embedding_vector,
)
from llmguard.domains.retrieval.vectorstore import (
    MetadataIsolationError,
    VectorCollectionInfo,
    VectorCollectionSpec,
    VectorSearchHit,
    VectorSearchQuery,
    VectorStore,
    VectorStoreError,
    validate_retrieval_ready_metadata,
)


_RETRIEVAL_READY_SCHEMA_VERSION = "1.1"
_EVIDENCE_SCHEMA_VERSION = "1.0"
_TRACE_SCHEMA_VERSION = "1.0"


class DenseRetriever:
    """Run a provider-neutral dense query without reading document content."""

    def __init__(
        self,
        *,
        embedding_provider: EmbeddingProvider,
        vector_store: VectorStore,
        collection: VectorCollectionSpec,
        retrieval_config_hash: str,
    ) -> None:
        if collection.public_metadata_schema_version != _RETRIEVAL_READY_SCHEMA_VERSION:
            raise RetrievalConfigurationError(
                "dense retrieval requires retrieval-ready metadata schema",
                error_code="RETRIEVAL_METADATA_SCHEMA_MISMATCH",
            )
        if embedding_provider.dimension != collection.dimension:
            raise RetrievalConfigurationError(
                "embedding provider dimension does not match collection",
                error_code="RETRIEVAL_DIMENSION_MISMATCH",
            )
        try:
            require_sha256(retrieval_config_hash, "retrieval_config_hash")
        except RetrievalInputError as error:
            raise RetrievalConfigurationError(
                "retrieval configuration hash is invalid",
                error_code="RETRIEVAL_CONFIG_HASH_MISMATCH",
            ) from error
        self._embedding_provider = embedding_provider
        self._vector_store = vector_store
        self._collection = collection
        self._retrieval_config_hash = retrieval_config_hash
        self._query_embedding_spec_hash = embedding_provider.model_spec.fingerprint(
            scope="query"
        )

    def retrieve(
        self,
        request: RetrievalRequest,
    ) -> tuple[tuple[RetrievalEvidence, ...], RetrievalTrace]:
        """Return canonical evidence and trace, never plaintext document content."""

        if not isinstance(request, RetrievalRequest):
            raise RetrievalInputError("dense retrieval requires a retrieval request")
        self._validate_request(request)
        self._validate_store_state()

        started = time.perf_counter()
        query_vector = self._embed_query(request)
        try:
            raw_hits: object = self._vector_store.query(
                self._collection,
                VectorSearchQuery(vector=query_vector, top_k=request.top_k),
            )
        except VectorStoreError as error:
            raise RetrievalIntegrityError(
                "vector store query failed",
                error_code="RETRIEVAL_QUERY_FAILURE",
            ) from error
        except Exception as error:
            raise RetrievalIntegrityError(
                "vector store query failed",
                error_code="RETRIEVAL_QUERY_FAILURE",
            ) from error
        if not isinstance(raw_hits, tuple):
            raise RetrievalIntegrityError(
                "vector store returned invalid hit collection",
                error_code="INVALID_RETRIEVAL_HIT_PROVENANCE",
            )
        candidate_count = len(raw_hits)
        normalized_hits = self._normalize_hits(raw_hits)
        evidence = self._to_evidence(request, normalized_hits)
        latency_ms = (time.perf_counter() - started) * 1000.0
        trace = RetrievalTrace.create(
            trace_schema_version=_TRACE_SCHEMA_VERSION,
            request_id=request.request_id,
            query_id=request.query_id,
            retrieval_query_hash=request.retrieval_query_hash,
            query_embedding_spec_hash=request.query_embedding_spec_hash,
            collection_fingerprint=request.collection_fingerprint,
            top_k=request.top_k,
            candidate_count=candidate_count,
            evidence_summaries=tuple(
                cast(RetrievalEvidenceSummary, item.to_summary()) for item in evidence
            ),
            retrieval_latency_ms=latency_ms,
        )
        return evidence, trace

    def _embed_query(self, request: RetrievalRequest) -> tuple[float, ...]:
        """Embed the projected query without exposing provider details outside this layer."""

        try:
            return validate_embedding_vector(
                self._embedding_provider.embed_query(request.retrieval_query),
                expected_dimension=self._collection.dimension,
            )
        except EmbeddingError as error:
            raise RetrievalIntegrityError(
                "query embedding failed",
                error_code="RETRIEVAL_EMBEDDING_FAILURE",
            ) from error
        except Exception as error:
            raise RetrievalIntegrityError(
                "query embedding failed",
                error_code="RETRIEVAL_EMBEDDING_FAILURE",
            ) from error

    def _validate_request(self, request: RetrievalRequest) -> None:
        if request.collection_fingerprint != self._collection.fingerprint:
            raise RetrievalConfigurationError(
                "request collection provenance does not match retriever",
                error_code="RETRIEVAL_COLLECTION_FINGERPRINT_MISMATCH",
            )
        if request.query_embedding_spec_hash != self._query_embedding_spec_hash:
            raise RetrievalConfigurationError(
                "request embedding provenance does not match retriever",
                error_code="RETRIEVAL_EMBEDDING_SPEC_MISMATCH",
            )
        if request.retrieval_config_hash != self._retrieval_config_hash:
            raise RetrievalConfigurationError(
                "request retrieval configuration does not match retriever",
                error_code="RETRIEVAL_CONFIG_HASH_MISMATCH",
            )

    def _validate_store_state(self) -> None:
        try:
            info = self._vector_store.get_collection_info(self._collection)
        except VectorStoreError as error:
            raise RetrievalConfigurationError(
                "vector store state is unavailable",
                error_code="RETRIEVAL_STORE_STATE_FAILURE",
            ) from error
        except Exception as error:
            raise RetrievalConfigurationError(
                "vector store state is unavailable",
                error_code="RETRIEVAL_STORE_STATE_FAILURE",
            ) from error
        if not isinstance(info, VectorCollectionInfo):
            raise RetrievalConfigurationError(
                "vector store state is invalid",
                error_code="RETRIEVAL_STORE_STATE_FAILURE",
            )
        if info.fingerprint != self._collection.fingerprint:
            raise RetrievalConfigurationError(
                "vector store fingerprint does not match retriever",
                error_code="RETRIEVAL_COLLECTION_FINGERPRINT_MISMATCH",
            )
        if info.dimension != self._collection.dimension:
            raise RetrievalConfigurationError(
                "vector store dimension does not match retriever",
                error_code="RETRIEVAL_DIMENSION_MISMATCH",
            )
        if info.distance_metric != self._collection.distance_metric:
            raise RetrievalConfigurationError(
                "vector store distance metric does not match retriever",
                error_code="RETRIEVAL_DISTANCE_METRIC_MISMATCH",
            )
        if info.vector_schema_version != self._collection.vector_schema_version:
            raise RetrievalConfigurationError(
                "vector store vector schema does not match retriever",
                error_code="RETRIEVAL_VECTOR_SCHEMA_MISMATCH",
            )
        if info.public_metadata_schema_version != _RETRIEVAL_READY_SCHEMA_VERSION:
            raise RetrievalConfigurationError(
                "vector store metadata schema does not support dense retrieval",
                error_code="RETRIEVAL_METADATA_SCHEMA_MISMATCH",
            )
        # collection_name is a fingerprint-derived display value, not separate provenance.

    def _normalize_hits(
        self,
        raw_hits: object,
    ) -> tuple[tuple[VectorSearchHit, Mapping[str, str | int]], ...]:
        if not isinstance(raw_hits, tuple):
            raise RetrievalIntegrityError(
                "vector store returned invalid hit collection",
                error_code="INVALID_RETRIEVAL_HIT_PROVENANCE",
            )
        candidates: list[tuple[VectorSearchHit, Mapping[str, str | int]]] = []
        for hit in raw_hits:
            if not isinstance(hit, VectorSearchHit):
                raise RetrievalIntegrityError(
                    "vector store returned invalid retrieval hit",
                    error_code="INVALID_RETRIEVAL_HIT_PROVENANCE",
                )
            if "parent_doc_id" not in hit.metadata:
                raise RetrievalIntegrityError(
                    "retrieval hit is missing parent-document identity",
                    error_code="MISSING_PARENT_DOCUMENT_ID",
                )
            try:
                metadata = validate_retrieval_ready_metadata(
                    hit.metadata,
                    doc_id=hit.doc_id,
                )
            except MetadataIsolationError as error:
                raise RetrievalIntegrityError(
                    "retrieval hit provenance is invalid",
                    error_code="INVALID_RETRIEVAL_HIT_PROVENANCE",
                ) from error
            candidates.append((hit, metadata))

        candidates.sort(key=lambda item: (-item[0].similarity, item[0].distance, item[0].doc_id))
        deduplicated: list[tuple[VectorSearchHit, Mapping[str, str | int]]] = []
        seen_identity: dict[str, tuple[str | int, ...]] = {}
        identity_fields = (
            "parent_doc_id",
            "corpus_snapshot_id",
            "content_hash",
            "source_id",
            "source_type",
            "version",
            "timestamp",
        )
        for hit, metadata in candidates:
            identity = tuple(metadata[field] for field in identity_fields)
            previous_identity = seen_identity.get(hit.doc_id)
            if previous_identity is not None:
                if previous_identity != identity:
                    raise RetrievalIntegrityError(
                        "duplicate retrieval chunk has conflicting provenance",
                        error_code="INVALID_RETRIEVAL_HIT_PROVENANCE",
                    )
                continue
            seen_identity[hit.doc_id] = identity
            deduplicated.append((hit, metadata))
        return tuple(deduplicated)

    def _to_evidence(
        self,
        request: RetrievalRequest,
        hits: tuple[tuple[VectorSearchHit, Mapping[str, str | int]], ...],
    ) -> tuple[RetrievalEvidence, ...]:
        evidence: list[RetrievalEvidence] = []
        for rank, (hit, metadata) in enumerate(hits, start=1):
            chunk_id = hit.doc_id
            corpus_snapshot_id = str(metadata["corpus_snapshot_id"])
            content_hash = str(metadata["content_hash"])
            evidence.append(
                RetrievalEvidence(
                    evidence_schema_version=_EVIDENCE_SCHEMA_VERSION,
                    evidence_uid=derive_evidence_uid(
                        evidence_schema_version=_EVIDENCE_SCHEMA_VERSION,
                        corpus_snapshot_id=corpus_snapshot_id,
                        chunk_id=chunk_id,
                        content_hash=content_hash,
                    ),
                    query_id=request.query_id,
                    retrieval_request_id=request.request_id,
                    corpus_snapshot_id=corpus_snapshot_id,
                    doc_id=chunk_id,
                    chunk_id=chunk_id,
                    parent_doc_id=str(metadata["parent_doc_id"]),
                    content_ref=ContentRef.corpus(corpus_snapshot_id, chunk_id),
                    content_hash=content_hash,
                    source_id=str(metadata["source_id"]),
                    source_type=str(metadata["source_type"]),
                    version=str(metadata["version"]),
                    timestamp=str(metadata["timestamp"]),
                    rank=rank,
                    distance=hit.distance,
                    similarity=hit.similarity,
                    collection_fingerprint=request.collection_fingerprint,
                    public_metadata={},
                )
            )
        return tuple(evidence)
