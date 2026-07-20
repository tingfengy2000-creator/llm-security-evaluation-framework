from __future__ import annotations

from dataclasses import fields

import pytest

from llmguard.domains.retrieval.contracts import QueryRecord
from llmguard.domains.retrieval.contracts.projections import project_retriever_query


def _raw_query() -> QueryRecord:
    return QueryRecord(
        query_id="R1-Q01",
        attack_id="R1-A01",
        category="R1",
        retrieval_query="find annual leave guidance",
        generation_question="How do I request leave?",
        expected_clean_doc_ids=("C-LEAVE-01",),
        metadata={"delivery_layer": "retrieval", "scenario": "policy", "variant": 1},
    )


def test_projection_keeps_only_runtime_safe_fields_and_exact_query() -> None:
    runtime = project_retriever_query(
        _raw_query(),
        public_query_id="Q-0001",
        public_metadata={"delivery_layer": "retrieval", "scenario": "policy", "variant": 1},
    )

    assert runtime.query_id == "Q-0001"
    assert runtime.retrieval_query == "find annual leave guidance"
    assert {field.name for field in fields(runtime)} == {
        "query_id",
        "retrieval_query",
        "public_metadata",
    }
    assert "generation_question" not in repr(runtime)
    assert "find annual leave guidance" not in repr(runtime)
    assert runtime.to_audit_dict() == {
        "query_id": "Q-0001",
        "public_metadata": {
            "delivery_layer": "retrieval",
            "scenario": "policy",
            "variant": 1,
        },
    }


def test_projection_requires_explicit_safe_identifier_and_metadata_allowlist() -> None:
    with pytest.raises(ValueError, match="UNSAFE_QUERY_PROJECTION"):
        project_retriever_query(
            _raw_query(),
            public_query_id="R1-Q01",
            public_metadata={"delivery_layer": "retrieval"},
        )
    with pytest.raises(ValueError, match="UNSAFE_QUERY_PROJECTION"):
        project_retriever_query(
            _raw_query(),
            public_query_id="Q-0001",
            public_metadata={"attack_id": "R1-A01"},
        )
