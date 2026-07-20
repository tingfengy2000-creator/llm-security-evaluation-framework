from __future__ import annotations

from llmguard.domains.retrieval.attacks import RetrieverQueryRecord as attacks_type
from llmguard.domains.retrieval.contracts import (
    RetrieverQueryRecord,
    adapt_legacy_retrieval_evidence,
)


def test_attack_loader_reexports_the_single_canonical_runtime_query_type() -> None:
    assert attacks_type is RetrieverQueryRecord


def test_legacy_evidence_adapter_requires_explicit_chunk_context() -> None:
    evidence = adapt_legacy_retrieval_evidence(
        query_id="Q-0001",
        legacy_doc_id="fixture-doc",
        rank=1,
        distance=0.1,
        similarity=0.9,
        source_id="handbook",
        source_type="policy",
        timestamp="2026-07-01T00:00:00Z",
        version="1.0",
        content_hash="a" * 64,
        legacy_content_ref="chroma:fixture-doc",
        evidence_schema_version="1.0",
        corpus_snapshot_id="stage6-v1",
        chunk_id="CH-" + "b" * 64,
        parent_doc_id="D-001",
        retrieval_request_id="RQ-" + "c" * 64,
        collection_fingerprint="d" * 64,
        public_metadata={"delivery_layer": "retrieval"},
    )
    assert evidence.doc_id == "CH-" + "b" * 64
    assert evidence.content_ref == "corpus:stage6-v1:CH-" + "b" * 64
