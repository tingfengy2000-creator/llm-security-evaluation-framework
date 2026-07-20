"""Explicit Dataset QueryRecord to retriever runtime projection."""

from __future__ import annotations

from collections.abc import Mapping

from .errors import RetrievalProjectionError
from .models import QueryRecord
from .retrieval import RetrieverQueryRecord


def project_retriever_query(
    query: QueryRecord, *, public_query_id: str, public_metadata: Mapping[str, object]
) -> RetrieverQueryRecord:
    """Project exact retrieval text while dropping all evaluator-facing fields."""

    if not isinstance(query, QueryRecord):
        raise RetrievalProjectionError("unsafe query projection", error_code="UNSAFE_QUERY_PROJECTION")
    if public_query_id == query.query_id or not public_query_id.startswith("Q-"):
        raise RetrievalProjectionError("unsafe query projection", error_code="UNSAFE_QUERY_PROJECTION")
    try:
        return RetrieverQueryRecord(
            query_id=public_query_id,
            retrieval_query=query.retrieval_query,
            public_metadata=public_metadata,
        )
    except ValueError as error:
        raise RetrievalProjectionError("unsafe query projection", error_code="UNSAFE_QUERY_PROJECTION") from error
