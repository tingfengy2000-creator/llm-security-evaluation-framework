"""Public query packets and fail-closed, model-free preparation gates."""
from __future__ import annotations

from typing import Any

FORBIDDEN = frozenset({
    "label", "poisoned", "poison_label", "attack_id", "attack_goal",
    "attack_category", "expected_answer", "ground_truth", "oracle",
    "derived_s_evaluation_only", "role_evaluation_only", "family_evaluation_only",
    "group_evaluation_only", "failure_type", "expected_behavior", "risk_goal", "stealth_level",
})
PACKET_KEYS = frozenset({"query_id", "query_text", "candidate_id", "retrieved_chunks", "retrieval_order"})
CHUNK_KEYS = frozenset({"chunk_id", "text", "source_id", "source_role", "publication_time",
                        "effective_time", "version", "trust_boundary"})
TRUST = frozenset({"INDEPENDENT_TRUSTED", "UNVERIFIED"})


def reject_evaluator_fields(value: Any) -> None:
    """Inspect all nested fields, including strings; never project before scanning."""
    if isinstance(value, dict):
        for key, child in value.items():
            if not isinstance(key, str) or key.lower() in FORBIDDEN or key.endswith("_evaluation_only"):
                raise ValueError("EVALUATOR_FIELD_IN_PUBLIC_PACKET")
            reject_evaluator_fields(child)
    elif isinstance(value, list):
        for child in value:
            reject_evaluator_fields(child)
    elif isinstance(value, str):
        # Key-shaped serialized annotations must not travel inside a free-form field.
        lowered = value.lower()
        if any(('"' + word + '"') in lowered or (word + "=") in lowered for word in FORBIDDEN):
            raise ValueError("SERIALIZED_EVALUATOR_ANNOTATION")
    elif value is not None and not isinstance(value, (bool, int, float)):
        raise ValueError("UNSUPPORTED_PUBLIC_VALUE")


def validate_packet(packet: dict[str, Any]) -> None:
    reject_evaluator_fields(packet)
    if set(packet) != PACKET_KEYS:
        raise ValueError("PACKET_SCHEMA")
    for name in ("query_id", "query_text", "candidate_id"):
        if not isinstance(packet[name], str) or not packet[name].strip():
            raise ValueError("NEEDS_ADJUDICATION")
    chunks = packet["retrieved_chunks"]
    if not isinstance(chunks, list) or not chunks:
        raise ValueError("EMPTY_RETRIEVAL_REQUIRES_SEPARATE_ABSTENTION_CONTROL")
    ids = []
    for chunk in chunks:
        if not isinstance(chunk, dict) or set(chunk) != CHUNK_KEYS:
            raise ValueError("CHUNK_SCHEMA")
        for name in ("chunk_id", "text", "source_id"):
            if not isinstance(chunk[name], str) or not chunk[name].strip():
                raise ValueError("CHUNK_IDENTITY_OR_TEXT")
        for name in ("source_role", "publication_time", "effective_time", "version"):
            if chunk[name] is not None and not isinstance(chunk[name], str):
                raise ValueError("METADATA_MUST_BE_STRING_OR_NULL")
        if chunk["trust_boundary"] not in TRUST:
            raise ValueError("TRUST_CANNOT_EXPOSE_ATTACK_ROLE")
        ids.append(chunk["chunk_id"])
    if len(ids) != len(set(ids)) or packet["retrieval_order"] != ids:
        raise ValueError("ORDER_OR_DUPLICATE_ID")


def validate_sibling_isolation(present_candidates: list[str], siblings: set[str]) -> None:
    """Control-plane check; sibling mapping is never attached to public chunks."""
    if len(set(present_candidates) & siblings) > 1:
        raise ValueError("COUNTERFACTUAL_SIBLINGS_MUST_BE_SEPARATE")


def no_defense(packet: dict[str, Any]) -> list[dict[str, Any]]:
    """B0's model-free context path; this is not a generated-answer experiment."""
    validate_packet(packet)
    return [dict(chunk) for chunk in packet["retrieved_chunks"]]
