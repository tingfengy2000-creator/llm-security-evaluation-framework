from __future__ import annotations

import hashlib
from dataclasses import replace

import pytest

from llmguard.domains.retrieval.embedding.model_spec import EmbeddingModelSpec
from llmguard.domains.retrieval.contracts import ChunkRecord, derive_chunk_id, format_corpus_content_ref
from llmguard.domains.retrieval.vectorstore.chroma_store import ChromaVectorStore
from llmguard.domains.retrieval.vectorstore.fingerprint import CollectionFingerprint
from llmguard.domains.retrieval.vectorstore.in_memory_store import InMemoryVectorStore
from llmguard.domains.retrieval.vectorstore.models import (
    PUBLIC_METADATA_FIELDS,
    RETRIEVAL_READY_METADATA_FIELDS,
    MetadataIsolationError,
    VectorCollectionSpec,
    VectorDocument,
    VectorSearchQuery,
    validate_retrieval_ready_metadata,
)


CONTENT_HASH = "a" * 64


def _fingerprint(schema_version: str) -> CollectionFingerprint:
    embedding_spec = EmbeddingModelSpec(
        provider="llmguard_static",
        model_id="llmguard/static-fixture",
        revision="16e5344fbfc7dfbbbe0019d30cec21e2940cb4e1",
        dimension=3,
        normalize_embeddings=True,
        device="cpu",
        batch_size=16,
        trust_remote_code=False,
        local_files_only=True,
        implementation_version="s6_t5_3_p1",
    )
    return CollectionFingerprint.from_document_embedding_spec(
        corpus_hash="b" * 64,
        corpus_manifest_version="1.0.1",
        chunking_config_hash="c" * 64,
        document_embedding_spec=embedding_spec,
        distance_metric="cosine",
        vector_schema_version="1.0",
        public_metadata_schema_version=schema_version,
    )


def _collection(schema_version: str) -> VectorCollectionSpec:
    return VectorCollectionSpec(
        fingerprint=_fingerprint(schema_version).value,
        dimension=3,
        public_metadata_schema_version=schema_version,
    )


def _metadata(*, parent_doc_id: str | None = "D-001") -> dict[str, object]:
    values: dict[str, object] = {
        "doc_id": "CH-" + "d" * 64,
        "source_id": "handbook",
        "source_type": "policy",
        "timestamp": "2026-07-01T00:00:00Z",
        "version": "1.0",
        "content_hash": CONTENT_HASH,
        "corpus_snapshot_id": "stage6-v1",
        "chunk_index": 0,
        "language": "zh",
    }
    if parent_doc_id is not None:
        values["parent_doc_id"] = parent_doc_id
    return values


def _document(*, parent_doc_id: str | None = "D-001") -> VectorDocument:
    return VectorDocument(
        doc_id="CH-" + "d" * 64,
        vector=(1.0, 0.0, 0.0),
        metadata=_metadata(parent_doc_id=parent_doc_id),
        content_hash=CONTENT_HASH,
        content_ref="corpus:stage6-v1:CH-" + "d" * 64,
    )


def test_parent_document_identity_is_public_and_frozen() -> None:
    document = _document()

    assert "parent_doc_id" in PUBLIC_METADATA_FIELDS
    assert "parent_doc_id" in RETRIEVAL_READY_METADATA_FIELDS
    assert document.metadata["parent_doc_id"] == "D-001"
    with pytest.raises(TypeError):
        document.metadata["parent_doc_id"] = "D-002"  # type: ignore[index]


def test_chunk_record_projects_its_exact_parent_identity_without_plaintext_metadata() -> None:
    content = "synthetic retrieval fixture"
    chunk_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
    chunk_id = derive_chunk_id(
        chunk_schema_version="1.0",
        corpus_snapshot_id="stage6-v1",
        parent_doc_id="D-041",
        chunk_index=0,
        content_hash=chunk_hash,
        chunking_config_hash="e" * 64,
    )
    chunk = ChunkRecord(
        chunk_schema_version="1.0",
        chunk_id=chunk_id,
        parent_doc_id="D-041",
        corpus_snapshot_id="stage6-v1",
        chunk_index=0,
        content=content,
        content_hash=chunk_hash,
        content_ref=format_corpus_content_ref("stage6-v1", chunk_id),
        chunking_strategy="identity",
        chunking_config_hash="e" * 64,
        source_id="handbook",
        source_type="policy",
        version="1.0",
        timestamp="2026-07-01T00:00:00Z",
        public_metadata={},
    )

    document = VectorDocument.from_chunk_record(chunk, vector=(1.0, 0.0, 0.0))

    assert document.doc_id == chunk.chunk_id
    assert document.metadata["parent_doc_id"] == chunk.parent_doc_id
    assert content not in document.metadata.values()


def test_retrieval_ready_metadata_rejects_path_label_and_plaintext_shaped_parent_id() -> None:
    windows_absolute = "C:" + chr(92) + "sensitive" + chr(92) + "document"
    unix_absolute = "/" + "srv/private/document"
    for value in (windows_absolute, unix_absolute, "line one\nline two"):
        with pytest.raises(MetadataIsolationError):
            validate_retrieval_ready_metadata(_metadata(parent_doc_id=value), doc_id="CH-" + "d" * 64)

    metadata = _metadata()
    metadata["attack_goal"] = "unsafe"
    with pytest.raises(MetadataIsolationError):
        validate_retrieval_ready_metadata(metadata, doc_id="CH-" + "d" * 64)


def test_schema_1_0_keeps_legacy_metadata_compatible_but_schema_1_1_fails_closed() -> None:
    legacy_document = _document(parent_doc_id=None)
    legacy_store = InMemoryVectorStore()
    legacy_collection = _collection("1.0")
    legacy_store.create_or_open_collection(legacy_collection)
    legacy_store.upsert(legacy_collection, (legacy_document,))

    retrieval_ready_store = InMemoryVectorStore()
    retrieval_ready_collection = _collection("1.1")
    retrieval_ready_store.create_or_open_collection(retrieval_ready_collection)
    with pytest.raises(MetadataIsolationError):
        retrieval_ready_store.upsert(retrieval_ready_collection, (legacy_document,))


@pytest.mark.parametrize(
    "field_name",
    tuple(RETRIEVAL_READY_METADATA_FIELDS - {"doc_id"}),
)
def test_schema_1_1_rejects_each_missing_retrieval_provenance_field(field_name: str) -> None:
    metadata = _metadata()
    metadata.pop(field_name)
    document = VectorDocument(
        doc_id="CH-" + "d" * 64,
        vector=(1.0, 0.0, 0.0),
        metadata=metadata,
        content_hash=CONTENT_HASH,
        content_ref="corpus:stage6-v1:CH-" + "d" * 64,
    )
    store = InMemoryVectorStore()
    collection = _collection("1.1")
    store.create_or_open_collection(collection)

    with pytest.raises(MetadataIsolationError):
        store.upsert(collection, (document,))


def test_schema_1_1_rejects_doc_id_mismatch() -> None:
    metadata = _metadata()
    metadata["doc_id"] = "CH-" + "e" * 64
    with pytest.raises(MetadataIsolationError):
        _document(parent_doc_id="D-001").__class__(
            doc_id="CH-" + "d" * 64,
            vector=(1.0, 0.0, 0.0),
            metadata=metadata,
            content_hash=CONTENT_HASH,
            content_ref="corpus:stage6-v1:CH-" + "d" * 64,
        )


def test_in_memory_query_preserves_parent_document_identity_for_schema_1_1() -> None:
    store = InMemoryVectorStore()
    collection = _collection("1.1")
    store.create_or_open_collection(collection)
    store.upsert(collection, (_document(parent_doc_id="D-041"),))

    hit = store.query(collection, VectorSearchQuery(vector=(1.0, 0.0, 0.0), top_k=1))[0]

    assert hit.metadata["parent_doc_id"] == "D-041"


def test_chroma_stable_hit_conversion_preserves_or_fails_closed_for_parent_id() -> None:
    collection = _collection("1.1")
    raw = {
        "ids": [["CH-" + "d" * 64]],
        "metadatas": [[_metadata(parent_doc_id="D-041")]],
        "distances": [[0.0]],
    }
    hits = ChromaVectorStore._to_stable_hits(raw, collection=collection)
    assert hits[0].metadata["parent_doc_id"] == "D-041"

    missing_parent = {**raw, "metadatas": [[_metadata(parent_doc_id=None)]]}
    with pytest.raises(MetadataIsolationError):
        ChromaVectorStore._to_stable_hits(missing_parent, collection=collection)

    tampered_parent = {**raw, "metadatas": [[_metadata(parent_doc_id="D-tampered")]]}
    tampered_hits = ChromaVectorStore._to_stable_hits(tampered_parent, collection=collection)
    assert tampered_hits[0].metadata["parent_doc_id"] == "D-tampered"


def test_schema_versions_create_distinct_collection_identity_and_are_not_interchangeable() -> None:
    legacy = _collection("1.0")
    retrieval_ready = _collection("1.1")

    assert legacy.fingerprint != retrieval_ready.fingerprint
    assert legacy.collection_name != retrieval_ready.collection_name
    assert replace(legacy, public_metadata_schema_version="1.1") != retrieval_ready
