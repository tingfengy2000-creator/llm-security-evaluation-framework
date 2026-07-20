from __future__ import annotations

from llmguard.domains.retrieval.contracts import derive_evidence_uid


def test_evidence_uid_is_deterministic_and_semantic() -> None:
    first = derive_evidence_uid(
        evidence_schema_version="1.0",
        corpus_snapshot_id="stage6-v1",
        chunk_id="CH-" + "a" * 64,
        content_hash="b" * 64,
    )
    assert first == derive_evidence_uid(
        evidence_schema_version="1.0",
        corpus_snapshot_id="stage6-v1",
        chunk_id="CH-" + "a" * 64,
        content_hash="b" * 64,
    )
    assert first != derive_evidence_uid(
        evidence_schema_version="1.0",
        corpus_snapshot_id="stage6-v1",
        chunk_id="CH-" + "c" * 64,
        content_hash="b" * 64,
    )
