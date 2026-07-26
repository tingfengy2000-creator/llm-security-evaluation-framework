"""Opt-in S6-T5.7 MiniLM and temporary Chroma controlled-pipeline validation."""

from __future__ import annotations

import hashlib
import math
import os
import tempfile
from pathlib import Path

import pytest


RUN_REAL_RAG_INTEGRATION = os.getenv("RUN_REAL_RAG_INTEGRATION") == "1"
MODEL_ID = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
FIXED_REVISION = "16e5344fbfc7dfbbbe0019d30cec21e2940cb4e1"


def _sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


@pytest.mark.skipif(
    not RUN_REAL_RAG_INTEGRATION,
    reason="set RUN_REAL_RAG_INTEGRATION=1 to run the pinned MiniLM + temporary Chroma integration test",
)
def test_real_minilm_chroma_dense_retrieval_to_controlled_context_package() -> None:
    """Exercise only accepted infrastructure with synthetic temporary documents."""

    from llmguard.domains.retrieval.context import (
        CanonicalEvidenceEnvelopeFactory,
        CorpusContentResolver,
        DeterministicContextBuilder,
        InMemoryCorpusSnapshotReader,
        StaticApprovedCorpusSnapshotRegistry,
    )
    from llmguard.domains.retrieval.contracts import (
        CitationMode,
        ContextBuildConfig,
        QueryRecord,
        RetrievalRequest,
        project_retriever_query,
    )
    from llmguard.domains.retrieval.embedding import (
        EmbeddingModelSpec,
        SentenceTransformerEmbeddingProvider,
    )
    from llmguard.domains.retrieval.retrieval import DenseRetriever
    from llmguard.domains.retrieval.vectorstore import (
        ChromaVectorStore,
        CollectionFingerprint,
        VectorCollectionSpec,
        VectorDocument,
    )

    model_spec = EmbeddingModelSpec(
        provider="sentence_transformers",
        model_id=MODEL_ID,
        revision=FIXED_REVISION,
        dimension=384,
        normalize_embeddings=True,
        device="cpu",
        batch_size=2,
        trust_remote_code=False,
        local_files_only=False,
        implementation_version="s6_t4_sentence_transformers_v1",
    )
    provider = SentenceTransformerEmbeddingProvider(model_spec)
    snapshot_id = "s6t57-real-synthetic-snapshot"
    query_text = "How do employees request leave approval?"
    documents = {
        "CH-" + "a" * 64: "Employees request leave by submitting a leave request with dates and reason for manager approval.",
        "CH-" + "b" * 64: "Employees submit travel receipts and an itinerary for reimbursement after a business trip.",
        "CH-" + "c" * 64: "Employees reset a password through account verification in the company portal.",
    }
    parent_ids = {
        "CH-" + "a" * 64: "DOC-LEAVE",
        "CH-" + "b" * 64: "DOC-TRAVEL",
        "CH-" + "c" * 64: "DOC-PASSWORD",
    }
    snapshot_fingerprint = _sha256("s6-t5.7-real-synthetic-snapshot")

    document_vectors = provider.embed_documents(tuple(documents.values()))
    assert tuple(len(vector) for vector in document_vectors) == (384, 384, 384)
    assert all(math.isfinite(value) for vector in document_vectors for value in vector)
    fingerprint = CollectionFingerprint.from_document_embedding_spec(
        corpus_hash=_sha256("s6-t5.7-real-synthetic-corpus"),
        corpus_manifest_version="s6-t5.7-real-v1",
        chunking_config_hash=_sha256("identity-chunks"),
        document_embedding_spec=model_spec,
        distance_metric="cosine",
        vector_schema_version="1.0",
        public_metadata_schema_version="1.1",
    )
    collection = VectorCollectionSpec(
        fingerprint=fingerprint.value,
        dimension=384,
        public_metadata_schema_version="1.1",
    )
    vector_documents = tuple(
        VectorDocument(
            doc_id=chunk_id,
            vector=vector,
            metadata={
                "doc_id": chunk_id,
                "parent_doc_id": parent_ids[chunk_id],
                "source_id": "synthetic-employee-policy",
                "source_type": "policy",
                "timestamp": "2026-07-26T00:00:00Z",
                "version": "v1",
                "content_hash": _sha256(content),
                "corpus_snapshot_id": snapshot_id,
                "language": "en",
            },
            content_hash=_sha256(content),
            content_ref=f"corpus:{snapshot_id}:{chunk_id}",
        )
        for (chunk_id, content), vector in zip(documents.items(), document_vectors, strict=True)
    )
    dataset_record = QueryRecord(
        query_id="dataset-query-real-integration",
        attack_id=None,
        category="synthetic-infrastructure",
        retrieval_query=query_text,
        generation_question="not exposed to retrieval runtime",
        expected_clean_doc_ids=("not exposed to retrieval runtime",),
        metadata={"dataset_split": "synthetic"},
    )
    projected = project_retriever_query(
        dataset_record,
        public_query_id="Q-1001",
        public_metadata={"delivery_layer": "retrieval", "scenario": "real-integration"},
    )
    request = RetrievalRequest.from_query(
        projected,
        request_schema_version="1.0",
        top_k=2,
        collection_fingerprint=collection.fingerprint,
        query_embedding_spec_hash=model_spec.fingerprint(scope="query"),
        retrieval_config_hash="e" * 64,
    )
    resolver = CorpusContentResolver(
        registry=StaticApprovedCorpusSnapshotRegistry(
            registrations={
                snapshot_id: (
                    snapshot_fingerprint,
                    InMemoryCorpusSnapshotReader(
                        corpus_snapshot_id=snapshot_id,
                        snapshot_fingerprint=snapshot_fingerprint,
                        chunks=documents,
                    ),
                )
            }
        )
    )
    builder = DeterministicContextBuilder(
        resolver=resolver,
        envelope_factory=CanonicalEvidenceEnvelopeFactory(),
    )
    config = ContextBuildConfig(
        context_schema_version="1.0",
        max_evidence_count=2,
        max_context_characters=5000,
    )

    temporary_directory = tempfile.TemporaryDirectory()
    root = Path(temporary_directory.name)
    writer: ChromaVectorStore | None = None
    reader: ChromaVectorStore | None = None
    try:
        writer = ChromaVectorStore(root)
        writer.create_or_open_collection(collection)
        writer.upsert(collection, vector_documents)
        before_evidence, before_trace = DenseRetriever(
            embedding_provider=provider,
            vector_store=writer,
            collection=collection,
            retrieval_config_hash="e" * 64,
        ).retrieve(request)
        before_package = builder.build(
            request=request,
            evidence=before_evidence,
            citation_mode=CitationMode.REQUIRED,
            config=config,
        )
        writer.close()
        writer = None

        reader = ChromaVectorStore(root)
        reader.create_or_open_collection(collection)
        after_evidence, after_trace = DenseRetriever(
            embedding_provider=provider,
            vector_store=reader,
            collection=collection,
            retrieval_config_hash="e" * 64,
        ).retrieve(request)
        after_package = builder.build(
            request=request,
            evidence=after_evidence,
            citation_mode=CitationMode.REQUIRED,
            config=config,
        )

        assert before_evidence
        assert after_evidence
        assert all(item.content_ref.scheme == "corpus" for item in before_evidence)
        assert tuple(item.evidence_uid for item in before_evidence) == tuple(item.evidence_uid for item in after_evidence)
        assert before_trace.trace_hash == after_trace.trace_hash
        assert before_package.rendered_context_hash == after_package.rendered_context_hash
        assert before_package.package_id == after_package.package_id
        assert after_package.evidence_count == 2
        assert all("content_ref" not in item.to_audit_dict() for item in after_evidence)
        audit_forms = "\n".join(
            (repr(after_evidence), str(after_trace.to_audit_dict()), repr(after_package), str(after_package.to_audit_dict()))
        )
        for forbidden in (query_text, *documents.values(), str(root), "ground_truth", "attack_goal"):
            assert forbidden not in audit_forms
    finally:
        if reader is not None:
            reader.close()
        if writer is not None:
            writer.close()
        temporary_directory.cleanup()

    assert not root.exists()
