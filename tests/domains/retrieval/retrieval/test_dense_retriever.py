from __future__ import annotations

import hashlib
from collections.abc import Sequence
from dataclasses import replace
from typing import cast

import pytest

from llmguard.domains.retrieval.contracts import (
    RetrievalConfigurationError,
    RetrievalIntegrityError,
    RetrievalRequest,
    RetrieverQueryRecord,
    ChunkRecord,
    derive_chunk_id,
    format_corpus_content_ref,
)
from llmguard.domains.retrieval.embedding import (
    EmbeddingModelSpec,
    EmbeddingProvider,
    StaticEmbeddingProvider,
)
from llmguard.domains.retrieval.embedding.base import EmbeddingRuntimeError
from llmguard.domains.retrieval.retrieval.dense_retriever import DenseRetriever
from llmguard.domains.retrieval.vectorstore import (
    CollectionFingerprint,
    InMemoryVectorStore,
    VectorCollectionSpec,
    VectorCollectionInfo,
    VectorDocument,
    VectorSearchHit,
    VectorStore,
    VectorStoreQueryError,
)


CONFIG_HASH = "e" * 64
SNAPSHOT_ID = "stage6-v1"


def _chunk(suffix: str) -> str:
    return "CH-" + suffix * 64


def _provider() -> StaticEmbeddingProvider:
    spec = EmbeddingModelSpec(
        provider="static",
        model_id="llmguard/static-retrieval",
        revision="16e5344fbfc7dfbbbe0019d30cec21e2940cb4e1",
        dimension=3,
        normalize_embeddings=True,
        device="cpu",
        batch_size=1,
        trust_remote_code=False,
        local_files_only=True,
        implementation_version="s6_t5_3_v1",
    )
    return StaticEmbeddingProvider(
        spec,
        fixture_vectors={"sensitive query": (1.0, 0.0, 0.0)},
    )


def _collection(provider: StaticEmbeddingProvider, schema_version: str = "1.1") -> VectorCollectionSpec:
    fingerprint = CollectionFingerprint.from_document_embedding_spec(
        corpus_hash="a" * 64,
        corpus_manifest_version="1.0.1",
        chunking_config_hash="b" * 64,
        document_embedding_spec=provider.model_spec,
        distance_metric="cosine",
        vector_schema_version="1.0",
        public_metadata_schema_version=schema_version,
    )
    return VectorCollectionSpec(
        fingerprint=fingerprint.value,
        dimension=provider.dimension,
        public_metadata_schema_version=schema_version,
    )


def _metadata(chunk_id: str, parent_doc_id: str) -> dict[str, object]:
    return {
        "doc_id": chunk_id,
        "parent_doc_id": parent_doc_id,
        "source_id": "handbook",
        "source_type": "policy",
        "timestamp": "2026-07-01T00:00:00Z",
        "version": "1.0",
        "content_hash": "c" * 64,
        "corpus_snapshot_id": SNAPSHOT_ID,
    }


def _document(chunk_id: str, parent_doc_id: str, vector: tuple[float, ...]) -> VectorDocument:
    return VectorDocument(
        doc_id=chunk_id,
        vector=vector,
        metadata=_metadata(chunk_id, parent_doc_id),
        content_hash="c" * 64,
        content_ref=f"corpus:{SNAPSHOT_ID}:{chunk_id}",
    )


def _request(
    provider: StaticEmbeddingProvider,
    collection: VectorCollectionSpec,
    *,
    retrieval_config_hash: str = CONFIG_HASH,
    collection_fingerprint: str | None = None,
    query_embedding_spec_hash: str | None = None,
    top_k: int = 3,
) -> RetrievalRequest:
    query = RetrieverQueryRecord(
        query_id="Q-0001",
        retrieval_query="sensitive query",
        public_metadata={"delivery_layer": "retrieval"},
    )
    return RetrievalRequest.from_query(
        query,
        request_schema_version="1.0",
        top_k=top_k,
        collection_fingerprint=collection_fingerprint or collection.fingerprint,
        query_embedding_spec_hash=(
            query_embedding_spec_hash or provider.model_spec.fingerprint(scope="query")
        ),
        retrieval_config_hash=retrieval_config_hash,
    )


def _retriever(
    provider: EmbeddingProvider,
    store: VectorStore,
    collection: VectorCollectionSpec,
) -> DenseRetriever:
    return DenseRetriever(
        embedding_provider=provider,
        vector_store=store,
        collection=collection,
        retrieval_config_hash=CONFIG_HASH,
    )


def test_dense_retriever_builds_evidence_and_trace_without_query_or_plaintext() -> None:
    provider = _provider()
    collection = _collection(provider)
    store = InMemoryVectorStore()
    store.create_or_open_collection(collection)
    first_chunk = _chunk("a")
    second_chunk = _chunk("b")
    store.upsert(
        collection,
        (
            _document(first_chunk, "D-001", (1.0, 0.0, 0.0)),
            _document(second_chunk, "D-001", (0.8, 0.2, 0.0)),
        ),
    )

    evidence, trace = _retriever(provider, store, collection).retrieve(_request(provider, collection))

    assert tuple(item.chunk_id for item in evidence) == (first_chunk, second_chunk)
    assert tuple(item.parent_doc_id for item in evidence) == ("D-001", "D-001")
    assert all(item.doc_id == item.chunk_id for item in evidence)
    assert all(item.content_ref == f"corpus:{SNAPSHOT_ID}:{item.chunk_id}" for item in evidence)
    assert trace.request_id == _request(provider, collection).request_id
    assert "sensitive query" not in repr(trace)
    assert "sensitive query" not in str(trace.to_audit_dict())
    assert "content_ref" not in evidence[0].to_audit_dict()


def test_dense_retriever_rejects_legacy_schema_1_0_before_querying() -> None:
    provider = _provider()
    legacy_collection = _collection(provider, "1.0")

    with pytest.raises(RetrievalConfigurationError, match="RETRIEVAL_METADATA_SCHEMA_MISMATCH"):
        _retriever(provider, cast(VectorStore, object()), legacy_collection)


def test_dense_retriever_rejects_request_provenance_mismatch_without_echoing_query() -> None:
    provider = _provider()
    collection = _collection(provider)
    store = InMemoryVectorStore()
    store.create_or_open_collection(collection)
    request = _request(provider, collection, retrieval_config_hash="f" * 64)

    with pytest.raises(RetrievalConfigurationError, match="RETRIEVAL_CONFIG_HASH_MISMATCH") as error:
        _retriever(provider, store, collection).retrieve(request)

    assert "sensitive query" not in str(error.value)


@pytest.mark.parametrize(
    ("request_kwargs", "error_code"),
    (
        ({"collection_fingerprint": "f" * 64}, "RETRIEVAL_COLLECTION_FINGERPRINT_MISMATCH"),
        ({"query_embedding_spec_hash": "f" * 64}, "RETRIEVAL_EMBEDDING_SPEC_MISMATCH"),
    ),
)
def test_dense_retriever_rejects_collection_and_embedding_provenance_mismatches(
    request_kwargs: dict[str, str],
    error_code: str,
) -> None:
    provider = _provider()
    collection = _collection(provider)
    store = InMemoryVectorStore()
    store.create_or_open_collection(collection)

    with pytest.raises(RetrievalConfigurationError, match=error_code):
        _retriever(provider, store, collection).retrieve(
            _request(
                provider,
                collection,
                collection_fingerprint=request_kwargs.get("collection_fingerprint"),
                query_embedding_spec_hash=request_kwargs.get("query_embedding_spec_hash"),
            )
        )


class _FakeVectorStore:
    def __init__(
        self,
        hits: object,
        *,
        count: int,
        info: VectorCollectionInfo | None = None,
        info_error: Exception | None = None,
        query_error: Exception | None = None,
    ) -> None:
        self._hits = hits
        self._count = count
        self._info = info
        self._info_error = info_error
        self._query_error = query_error

    def count(self, collection: VectorCollectionSpec) -> int:
        raise AssertionError("DenseRetriever must not use collection count for a query trace")

    def get_collection_info(self, collection: VectorCollectionSpec) -> VectorCollectionInfo:
        if self._info_error is not None:
            raise self._info_error
        if self._info is not None:
            return self._info
        return VectorCollectionInfo(
            collection_name=collection.collection_name,
            fingerprint=collection.fingerprint,
            dimension=collection.dimension,
            distance_metric=collection.distance_metric,
            count=self._count,
            vector_schema_version=collection.vector_schema_version,
            public_metadata_schema_version=collection.public_metadata_schema_version,
        )

    def query(self, collection: VectorCollectionSpec, query: object) -> object:
        if self._query_error is not None:
            raise self._query_error
        return self._hits


class _FailingEmbeddingProvider:
    def __init__(self, provider: StaticEmbeddingProvider, outcome: object) -> None:
        self._provider = provider
        self._outcome = outcome

    @property
    def model_spec(self) -> EmbeddingModelSpec:
        return self._provider.model_spec

    @property
    def dimension(self) -> int:
        return self._provider.dimension

    def embed_query(self, text: str) -> tuple[float, ...]:
        if isinstance(self._outcome, Exception):
            raise self._outcome
        return cast(tuple[float, ...], self._outcome)

    def embed_documents(self, texts: Sequence[str]) -> tuple[tuple[float, ...], ...]:
        return self._provider.embed_documents(texts)


def test_dense_retriever_fails_closed_for_missing_or_conflicting_parent_identity() -> None:
    provider = _provider()
    collection = _collection(provider)
    chunk_id = _chunk("a")
    missing_parent = VectorSearchHit(
        doc_id=chunk_id,
        distance=0.0,
        similarity=1.0,
        metadata={key: value for key, value in _metadata(chunk_id, "D-001").items() if key != "parent_doc_id"},
        rank=1,
    )
    with pytest.raises(RetrievalIntegrityError, match="MISSING_PARENT_DOCUMENT_ID"):
        _retriever(provider, cast(VectorStore, _FakeVectorStore((missing_parent,), count=1)), collection).retrieve(
            _request(provider, collection)
        )

    first = VectorSearchHit(
        doc_id=chunk_id,
        distance=0.0,
        similarity=1.0,
        metadata=_metadata(chunk_id, "D-001"),
        rank=1,
    )
    conflicting = replace(first, metadata=_metadata(chunk_id, "D-999"), rank=2)
    with pytest.raises(RetrievalIntegrityError, match="INVALID_RETRIEVAL_HIT_PROVENANCE"):
        _retriever(provider, cast(VectorStore, _FakeVectorStore((first, conflicting), count=2)), collection).retrieve(
            _request(provider, collection)
        )


def test_dense_retriever_uses_similarity_distance_and_doc_id_sorting_and_deduplicates_chunks() -> None:
    provider = _provider()
    collection = _collection(provider)
    first_chunk = _chunk("a")
    second_chunk = _chunk("b")
    first = VectorSearchHit(
        doc_id=first_chunk,
        distance=0.1,
        similarity=0.8,
        metadata=_metadata(first_chunk, "D-001"),
        rank=2,
    )
    duplicate = replace(first, rank=3)
    second = VectorSearchHit(
        doc_id=second_chunk,
        distance=0.2,
        similarity=0.8,
        metadata=_metadata(second_chunk, "D-002"),
        rank=1,
    )
    third_chunk = _chunk("c")
    third = VectorSearchHit(
        doc_id=third_chunk,
        distance=0.1,
        similarity=0.8,
        metadata=_metadata(third_chunk, "D-003"),
        rank=4,
    )

    evidence, trace = _retriever(
        provider,
        cast(VectorStore, _FakeVectorStore((second, duplicate, third, first), count=100)),
        collection,
    ).retrieve(_request(provider, collection))

    assert tuple(item.chunk_id for item in evidence) == (first_chunk, third_chunk, second_chunk)
    assert tuple(item.rank for item in evidence) == (1, 2, 3)
    assert trace.candidate_count == 4
    assert trace.returned_count == 3


def test_parent_document_identity_matches_original_chunk_across_vector_store_and_evidence() -> None:
    provider = _provider()
    collection = _collection(provider)
    content = "synthetic chunk body"
    content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
    chunk_id = derive_chunk_id(
        chunk_schema_version="1.0",
        corpus_snapshot_id=SNAPSHOT_ID,
        parent_doc_id="D-041",
        chunk_index=0,
        content_hash=content_hash,
        chunking_config_hash="d" * 64,
    )
    chunk = ChunkRecord(
        chunk_schema_version="1.0",
        chunk_id=chunk_id,
        parent_doc_id="D-041",
        corpus_snapshot_id=SNAPSHOT_ID,
        chunk_index=0,
        content=content,
        content_hash=content_hash,
        content_ref=format_corpus_content_ref(SNAPSHOT_ID, chunk_id),
        chunking_strategy="identity",
        chunking_config_hash="d" * 64,
        source_id="handbook",
        source_type="policy",
        version="1.0",
        timestamp="2026-07-01T00:00:00Z",
        public_metadata={},
    )
    store = InMemoryVectorStore()
    store.create_or_open_collection(collection)
    store.upsert(
        collection,
        (VectorDocument.from_chunk_record(chunk, vector=(1.0, 0.0, 0.0)),),
    )

    evidence, _ = _retriever(provider, store, collection).retrieve(_request(provider, collection))

    assert evidence[0].parent_doc_id == chunk.parent_doc_id
    assert content not in str(evidence[0].to_audit_dict())


def test_dense_retriever_trace_counts_query_hits_not_collection_rows() -> None:
    provider = _provider()
    collection = _collection(provider)
    store = InMemoryVectorStore()
    store.create_or_open_collection(collection)
    store.upsert(
        collection,
        tuple(
            _document(_chunk(suffix), f"D-00{index}", vector)
            for index, (suffix, vector) in enumerate(
                (
                    ("a", (1.0, 0.0, 0.0)),
                    ("b", (0.9, 0.1, 0.0)),
                    ("c", (0.8, 0.2, 0.0)),
                    ("d", (0.7, 0.3, 0.0)),
                ),
                start=1,
            )
        ),
    )

    evidence, trace = _retriever(provider, store, collection).retrieve(
        _request(provider, collection, top_k=3)
    )

    assert len(evidence) == 3
    assert trace.candidate_count == 3
    assert trace.returned_count == 3
    assert trace.candidate_count != store.count(collection)


def test_dense_retriever_empty_and_short_collections_report_actual_raw_hits() -> None:
    provider = _provider()
    collection = _collection(provider)
    empty_store = InMemoryVectorStore()
    empty_store.create_or_open_collection(collection)

    evidence, trace = _retriever(provider, empty_store, collection).retrieve(
        _request(provider, collection, top_k=3)
    )
    assert evidence == ()
    assert trace.candidate_count == 0
    assert trace.returned_count == 0

    short_store = InMemoryVectorStore()
    short_store.create_or_open_collection(collection)
    short_store.upsert(
        collection,
        (_document(_chunk("a"), "D-001", (1.0, 0.0, 0.0)),),
    )
    evidence, trace = _retriever(provider, short_store, collection).retrieve(
        _request(provider, collection, top_k=9)
    )
    assert tuple(item.chunk_id for item in evidence) == (_chunk("a"),)
    assert trace.candidate_count == 1
    assert trace.returned_count == 1


@pytest.mark.parametrize(
    ("field", "value", "error_code"),
    (
        ("fingerprint", "f" * 64, "RETRIEVAL_COLLECTION_FINGERPRINT_MISMATCH"),
        ("dimension", 99, "RETRIEVAL_DIMENSION_MISMATCH"),
        ("distance_metric", "l2", "RETRIEVAL_DISTANCE_METRIC_MISMATCH"),
        ("vector_schema_version", "2.0", "RETRIEVAL_VECTOR_SCHEMA_MISMATCH"),
        ("public_metadata_schema_version", "1.0", "RETRIEVAL_METADATA_SCHEMA_MISMATCH"),
    ),
)
def test_dense_retriever_rejects_store_provenance_mismatch(
    field: str,
    value: str | int,
    error_code: str,
) -> None:
    provider = _provider()
    collection = _collection(provider)
    expected = VectorCollectionInfo(
        collection_name=collection.collection_name,
        fingerprint=collection.fingerprint,
        dimension=collection.dimension,
        distance_metric=collection.distance_metric,
        count=0,
        vector_schema_version=collection.vector_schema_version,
        public_metadata_schema_version=collection.public_metadata_schema_version,
    )
    if field == "fingerprint":
        mismatched_info = replace(expected, fingerprint=cast(str, value))
    elif field == "dimension":
        mismatched_info = replace(expected, dimension=cast(int, value))
    elif field == "distance_metric":
        mismatched_info = replace(expected, distance_metric=cast(str, value))
    elif field == "vector_schema_version":
        mismatched_info = replace(expected, vector_schema_version=cast(str, value))
    else:
        mismatched_info = replace(
            expected,
            public_metadata_schema_version=cast(str, value),
        )
    store = _FakeVectorStore((), count=0, info=mismatched_info)

    with pytest.raises(RetrievalConfigurationError, match=error_code) as error:
        _retriever(provider, cast(VectorStore, store), collection).retrieve(
            _request(provider, collection)
        )

    assert "sensitive query" not in str(error.value)


def test_dense_retriever_redacts_provider_and_store_failures() -> None:
    provider = _provider()
    collection = _collection(provider)
    sensitive_provider_error = EmbeddingRuntimeError("provider saw sensitive query")
    failing_provider = _FailingEmbeddingProvider(provider, sensitive_provider_error)
    store = _FakeVectorStore((), count=0)

    with pytest.raises(RetrievalIntegrityError, match="RETRIEVAL_EMBEDDING_FAILURE") as error:
        _retriever(failing_provider, cast(VectorStore, store), collection).retrieve(
            _request(provider, collection)
        )

    assert "sensitive query" not in str(error.value)

    sensitive_path = f"{'C'}:\\sensitive\\path"
    query_error = VectorStoreQueryError(f"query sensitive query failed at {sensitive_path}")
    failing_store = _FakeVectorStore((), count=0, query_error=query_error)
    with pytest.raises(RetrievalIntegrityError, match="RETRIEVAL_QUERY_FAILURE") as error:
        _retriever(provider, cast(VectorStore, failing_store), collection).retrieve(
            _request(provider, collection)
        )

    assert "sensitive query" not in str(error.value)
    assert sensitive_path not in str(error.value)

    wrong_dimension_provider = _FailingEmbeddingProvider(provider, (1.0, 0.0))
    with pytest.raises(RetrievalIntegrityError, match="RETRIEVAL_EMBEDDING_FAILURE") as error:
        _retriever(wrong_dimension_provider, cast(VectorStore, store), collection).retrieve(
            _request(provider, collection)
        )
    assert "sensitive query" not in str(error.value)

    state_error = VectorStoreQueryError(f"state failure at {sensitive_path}")
    state_store = _FakeVectorStore((), count=0, info_error=state_error)
    with pytest.raises(
        RetrievalConfigurationError,
        match="RETRIEVAL_STORE_STATE_FAILURE",
    ) as state_failure:
        _retriever(provider, cast(VectorStore, state_store), collection).retrieve(
            _request(provider, collection)
        )
    assert sensitive_path not in str(state_failure.value)


def test_dense_retriever_maps_closed_store_and_invalid_store_outputs_to_stable_errors() -> None:
    provider = _provider()
    collection = _collection(provider)
    closed_store = InMemoryVectorStore()
    closed_store.close()

    with pytest.raises(RetrievalConfigurationError, match="RETRIEVAL_STORE_STATE_FAILURE") as error:
        _retriever(provider, closed_store, collection).retrieve(_request(provider, collection))
    assert "sensitive query" not in str(error.value)

    for raw_hits in (("not-a-hit",), ["not-a-tuple"]):
        with pytest.raises(RetrievalIntegrityError, match="INVALID_RETRIEVAL_HIT_PROVENANCE"):
            _retriever(
                provider,
                cast(VectorStore, _FakeVectorStore(raw_hits, count=1)),
                collection,
            ).retrieve(_request(provider, collection))


def test_dense_retriever_trace_hash_is_stable_when_latency_changes() -> None:
    provider = _provider()
    collection = _collection(provider)
    hit = VectorSearchHit(
        doc_id=_chunk("a"),
        distance=0.0,
        similarity=1.0,
        metadata=_metadata(_chunk("a"), "D-001"),
        rank=1,
    )
    retriever = _retriever(
        provider,
        cast(VectorStore, _FakeVectorStore((hit,), count=1)),
        collection,
    )

    first_evidence, first_trace = retriever.retrieve(_request(provider, collection))
    second_evidence, second_trace = retriever.retrieve(_request(provider, collection))

    assert first_evidence == second_evidence
    assert first_trace.trace_hash == second_trace.trace_hash
    assert first_trace.retrieval_latency_ms >= 0
    assert second_trace.retrieval_latency_ms >= 0
