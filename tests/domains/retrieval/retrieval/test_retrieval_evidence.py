from __future__ import annotations

from dataclasses import replace

import pytest

from llmguard.domains.retrieval.contracts import RetrievalEvidence, derive_evidence_uid


def _evidence() -> RetrievalEvidence:
    uid = derive_evidence_uid(
        evidence_schema_version="1.0",
        corpus_snapshot_id="stage6-v1",
        chunk_id="CH-" + "a" * 64,
        content_hash="b" * 64,
    )
    return RetrievalEvidence(
        evidence_schema_version="1.0",
        evidence_uid=uid,
        query_id="Q-0001",
        retrieval_request_id="RQ-" + "c" * 64,
        corpus_snapshot_id="stage6-v1",
        doc_id="CH-" + "a" * 64,
        chunk_id="CH-" + "a" * 64,
        parent_doc_id="D-001",
        content_ref="corpus:stage6-v1:CH-" + "a" * 64,
        content_hash="b" * 64,
        source_id="handbook",
        source_type="policy",
        version="1.0",
        timestamp="2026-07-01T00:00:00Z",
        rank=1,
        distance=0.1,
        similarity=0.9,
        collection_fingerprint="d" * 64,
        public_metadata={"delivery_layer": "retrieval"},
    )


def test_evidence_is_chunk_level_and_audit_safe() -> None:
    evidence = _evidence()
    assert evidence.doc_id == evidence.chunk_id
    assert "content_ref" not in evidence.to_audit_dict()
    assert "corpus:" not in repr(evidence)


def test_evidence_rejects_uid_and_metric_tampering() -> None:
    with pytest.raises(ValueError, match="EVIDENCE_UID_MISMATCH"):
        replace(_evidence(), evidence_uid="EV-" + "e" * 64)
    with pytest.raises(ValueError, match="INVALID_RETRIEVAL_METRIC"):
        replace(_evidence(), distance=-0.1)
