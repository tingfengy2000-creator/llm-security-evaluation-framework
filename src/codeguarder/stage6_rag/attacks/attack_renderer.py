from __future__ import annotations

import re
import unicodedata
from collections.abc import Mapping, Sequence

from codeguarder.stage6_rag.contracts import QueryRecord


PUBLIC_QUERY_FIELDS = frozenset(
    {
        "query_id",
        "attack_id",
        "category",
        "retrieval_query",
        "generation_question",
        "expected_clean_doc_ids",
        "metadata",
    }
)
GENERATION_QUESTION_INJECTION_PATTERNS = (
    r"(?:ignore|disregard|override)(?:the|all|any)?"
    r"(?:previous|prior|all|above)instructions?",
    r"(?:ignore|disregard|override)(?:the|all|any)?instructions?"
    r"(?:(?:stated|given|written|from)?(?:above|earlier|before))?",
    r"forget(?:allofyour|allof|allyour|allthe|all|your|the)?"
    r"(?:prior|previous)?instructions?",
    r"reveal(?:the|your)?(?:(?:hidden)?(?:system|developer)|hidden)prompt",
    r"show(?:the|your)?(?:(?:hidden)?(?:system|developer)|hidden)prompt",
    r"act(?:like|as)(?:an?)?dan",
    r"pretendyouare(?:an?)?dan",
    r"doanythingnow",
    r"bypass(?:all|any|the|allthe)?"
    r"(?:safeguards?|guardrails|safety|protections?|safetyprotections?"
    r"|filters?|contentfilters?|safetyfilters?|securityfilters?)",
)


def render_query_record(raw_record: Mapping[str, object]) -> QueryRecord:
    """Convert one public query object without consulting evaluator labels."""
    if not isinstance(raw_record, Mapping):
        raise ValueError("query record must be a mapping")
    fields = set(raw_record)
    missing = PUBLIC_QUERY_FIELDS - fields
    extra = fields - PUBLIC_QUERY_FIELDS
    if missing:
        raise ValueError(f"query record missing required fields: {sorted(missing)}")
    if extra:
        raise ValueError(f"query record has unexpected fields: {sorted(extra)}")

    query_id = _require_string(raw_record["query_id"], "query_id")
    attack_id_value = raw_record["attack_id"]
    attack_id = (
        None
        if attack_id_value is None
        else _require_string(attack_id_value, "attack_id")
    )
    category = _require_string(raw_record["category"], "category")
    retrieval_query = _require_string(
        raw_record["retrieval_query"],
        "retrieval_query",
    )
    generation_question = _require_string(
        raw_record["generation_question"],
        "generation_question",
    )
    normalized_question = _compact_security_text(generation_question)
    if any(
        re.search(pattern, normalized_question)
        for pattern in GENERATION_QUESTION_INJECTION_PATTERNS
    ):
        raise ValueError("generation_question contains a direct injection pattern")
    expected_ids = raw_record["expected_clean_doc_ids"]
    if not isinstance(expected_ids, Sequence) or isinstance(
        expected_ids,
        (str, bytes, bytearray),
    ):
        raise ValueError("expected_clean_doc_ids must be a sequence")
    expected_clean_doc_ids = tuple(
        _require_string(doc_id, f"expected_clean_doc_ids[{index}]")
        for index, doc_id in enumerate(expected_ids)
    )
    metadata = raw_record["metadata"]
    if not isinstance(metadata, Mapping):
        raise ValueError("metadata must be a mapping")

    if attack_id is not None and metadata.get("delivery_layer") != "retrieval":
        raise ValueError("attack queries must use the retrieval delivery layer")

    return QueryRecord(
        query_id=query_id,
        attack_id=attack_id,
        category=category,
        retrieval_query=retrieval_query,
        generation_question=generation_question,
        expected_clean_doc_ids=expected_clean_doc_ids,
        metadata=metadata,
    )


def _require_string(value: object, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a nonblank string")
    return value


def _compact_security_text(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).casefold()
    return re.sub(r"[^a-z0-9]+", "", normalized)
