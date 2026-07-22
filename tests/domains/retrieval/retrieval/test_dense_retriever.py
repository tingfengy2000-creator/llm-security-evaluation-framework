from __future__ import annotations

import hashlib
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
from llmguard.domains.retrieval.embedding import EmbeddingModelSpec, StaticEmbeddingProvider
from llmguard.domains.retrieval.retrieval.dense_retriever import DenseRetriever
from llmguard.domains.retrieval.vectorstore import (
    CollectionFingerprint,
    InMemoryVectorStore,
    VectorCollectionSpec,
    VectorCollectionInfo,
    VectorDocument,
    VectorSearchHit,
    VectorStore,
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
) -> RetrievalRequest:
    query = RetrieverQueryRecord(
        query_id="Q-0001",
        retrieval_query="sensitive query",
        public_metadata={"delivery_layer": "retrieval"},
    )
    return RetrievalRequest.from_query(
        query,
        request_schema_version="1.0",
        top_k=3,
        collection_fingerprint=collection_fingerprint or collection.fingerprint,
        query_embedding_spec_hash=(
            query_embedding_spec_hash or provider.model_spec.fingerprint(scope="query")
        ),
        retrieval_config_hash=retrieval_config_hash,
    )


def _retriever(
    provider: StaticEmbeddingProvider,
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
            _request(provider, collection, **request_kwargs)
        )


class _FakeVectorStore:
    def __init__(self, hits: tuple[VectorSearchHit, ...], *, count: int) -> None:
        self._hits = hits
        self._count = count

    def count(self, collection: VectorCollectionSpec) -> int:
        return self._count

    def get_collection_info(self, collection: VectorCollectionSpec) -> VectorCollectionInfo:
        return VectorCollectionInfo(
            collection_name=collection.collection_name,
            fingerprint=collection.fingerprint,
            dimension=collection.dimension,
            distance_metric=collection.distance_metric,
            count=self._count,
            vector_schema_version=collection.vector_schema_version,
            public_metadata_schema_version=collection.public_metadata_schema_version,
        )

    def query(self, collection: VectorCollectionSpec, query: object) -> tuple[VectorSearchHit, ...]:
        return self._hits


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
        cast(VectorStore, _FakeVectorStore((second, duplicate, third, first), count=4)),
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
