from __future__ import annotations

from dataclasses import replace

import pytest

from llmguard.domains.retrieval.contracts import RetrievalEvidenceSummary, RetrievalTrace


def _summary() -> RetrievalEvidenceSummary:
    return RetrievalEvidenceSummary(
        evidence_uid="EV-" + "a" * 64,
        doc_id="CH-" + "b" * 64,
        chunk_id="CH-" + "b" * 64,
        parent_doc_id="D-001",
        rank=1,
        distance=0.1,
        similarity=0.9,
        content_hash="c" * 64,
        source_id="handbook",
        version="1.0",
    )


def _trace(latency: float = 12.5, top_k: int = 3) -> RetrievalTrace:
    return RetrievalTrace.create(
        trace_schema_version="1.0",
        request_id="RQ-" + "d" * 64,
        query_id="Q-0001",
        retrieval_query_hash="e" * 64,
        query_embedding_spec_hash="f" * 64,
        collection_fingerprint="a" * 64,
        top_k=top_k,
        candidate_count=1,
        evidence_summaries=(_summary(),),
        retrieval_latency_ms=latency,
    )


def test_trace_hash_ignores_latency_but_tracks_semantic_fields() -> None:
    assert _trace(1).trace_hash == _trace(99).trace_hash
    assert _trace(1).trace_id == _trace(99).trace_id
    assert _trace(1).trace_hash != _trace(1, top_k=2).trace_hash


def test_trace_rejects_count_and_order_inconsistency() -> None:
    with pytest.raises(ValueError, match="TRACE_COUNT_MISMATCH"):
        replace(_trace(), returned_count=2)
