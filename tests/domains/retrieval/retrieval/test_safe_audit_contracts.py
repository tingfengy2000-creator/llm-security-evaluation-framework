from __future__ import annotations

import json

from llmguard.domains.retrieval.contracts import (
    RetrievalRequest,
    RetrieverQueryRecord,
)


def test_runtime_audit_forms_are_json_safe_and_exclude_sensitive_text() -> None:
    request = RetrievalRequest.from_query(
        RetrieverQueryRecord(
            query_id="Q-0001",
            retrieval_query="find annual leave guidance",
            public_metadata={"delivery_layer": "retrieval"},
        ),
        request_schema_version="1.0",
        top_k=1,
        collection_fingerprint="a" * 64,
        query_embedding_spec_hash="b" * 64,
        retrieval_config_hash="c" * 64,
    )
    serialized = json.dumps(request.to_audit_dict(), allow_nan=False)
    assert "find annual leave guidance" not in serialized
