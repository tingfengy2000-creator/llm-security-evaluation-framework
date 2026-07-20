from __future__ import annotations

import hashlib
from dataclasses import replace

import pytest

from llmguard.domains.retrieval.contracts import RetrievalRequest, RetrieverQueryRecord


def _request() -> RetrievalRequest:
    query = RetrieverQueryRecord(
        query_id="Q-0001",
        retrieval_query="find annual leave guidance",
        public_metadata={"delivery_layer": "retrieval"},
    )
    return RetrievalRequest.from_query(
        query,
        request_schema_version="1.0",
        top_k=3,
        collection_fingerprint="a" * 64,
        query_embedding_spec_hash="b" * 64,
        retrieval_config_hash="c" * 64,
    )


def test_request_has_exact_utf8_query_hash_and_deterministic_identifier() -> None:
    first = _request()
    second = _request()
    assert first == second
    assert first.retrieval_query_hash == hashlib.sha256(
        b"find annual leave guidance"
    ).hexdigest()
    assert first.request_id.startswith("RQ-")
    assert "find annual leave guidance" not in repr(first)
    assert "retrieval_query" not in first.to_audit_dict()


def test_request_rejects_hash_and_identifier_tampering() -> None:
    with pytest.raises(ValueError, match="RETRIEVAL_QUERY_HASH_MISMATCH"):
        replace(_request(), retrieval_query_hash="d" * 64)
    with pytest.raises(ValueError, match="RETRIEVAL_REQUEST_ID_MISMATCH"):
        replace(_request(), request_id="RQ-" + "d" * 64)
