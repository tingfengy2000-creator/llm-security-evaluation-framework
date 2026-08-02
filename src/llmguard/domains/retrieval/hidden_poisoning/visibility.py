"""Central field visibility and fail-closed evaluator-label isolation."""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass, fields, is_dataclass
from enum import Enum
from typing import Iterator, Mapping

from .schema import BenchmarkRecord, FieldVisibility, LabelLeakageBlocker


class RuntimeAudience(str, Enum):
    RETRIEVER = "retriever"
    DETECTOR = "detector"
    INTERVENTION = "intervention"
    EMBEDDING = "embedding"
    FINGERPRINT = "fingerprint"


EVALUATOR_ONLY_FIELDS = frozenset(
    {
        "label",
        "attack_type",
        "stealth_level",
        "mutation_operation",
        "changed_claim_fields",
        "annotator_labels",
        "adjudicated_label",
        "rationale",
        "hard_negative_type",
        "split",
        "evaluator_notes",
    }
)

FORBIDDEN_RUNTIME_KEYS = EVALUATOR_ONLY_FIELDS | frozenset(
    {
        "poisoned",
        "poison_label",
        "attack_id",
        "attack_goal",
        "attack_category",
        "expected_answer",
        "expected_behavior",
        "failure_type",
        "ground_truth",
        "oracle",
        "risk_goal",
    }
)

_BASE_RUNTIME_FIELDS = frozenset(
    {
        "record_id",
        "document_text",
        "entity_id",
        "claim_family",
        "version_chain_id",
        "source_document_family",
        "schema_version",
    }
)

_DETECTOR_PRIVATE_FIELDS = frozenset(
    {
        "claim",
        "version",
        "provenance",
        "subject",
        "predicate",
        "object_value",
        "numeric_value",
        "unit",
        "conditions",
        "relation_id",
        "current_record_id",
        "predecessor_record_id",
        "successor_record_id",
        "effective_at",
        "expires_at",
        "repealed_at",
        "supersedes",
        "amends",
        "provenance_id",
        "source_id",
        "source_type",
        "authority_level",
        "jurisdiction",
        "department",
        "citation_reference",
    }
)

_GROUP_PRIVATE_FIELDS = frozenset(
    {"mutation_template_family", "near_duplicate_cluster"}
)

FIELD_POLICY: Mapping[str, frozenset[FieldVisibility]] = {
    "record_id": frozenset(
        {
            FieldVisibility.RETRIEVER,
            FieldVisibility.DETECTOR,
            FieldVisibility.INTERVENTION,
            FieldVisibility.RELEASEABLE,
        }
    ),
    "document_text": frozenset(
        {
            FieldVisibility.RETRIEVER,
            FieldVisibility.DETECTOR,
            FieldVisibility.PRIVATE,
        }
    ),
    "entity_id": frozenset(
        {FieldVisibility.RETRIEVER, FieldVisibility.DETECTOR, FieldVisibility.PRIVATE}
    ),
    "claim_family": frozenset(
        {FieldVisibility.RETRIEVER, FieldVisibility.DETECTOR, FieldVisibility.PRIVATE}
    ),
    "version_chain_id": frozenset(
        {FieldVisibility.DETECTOR, FieldVisibility.PRIVATE}
    ),
    "source_document_family": frozenset(
        {FieldVisibility.DETECTOR, FieldVisibility.PRIVATE}
    ),
    "schema_version": frozenset(
        {
            FieldVisibility.RETRIEVER,
            FieldVisibility.DETECTOR,
            FieldVisibility.INTERVENTION,
            FieldVisibility.RELEASEABLE,
        }
    ),
    **{
        field: frozenset({FieldVisibility.DETECTOR, FieldVisibility.PRIVATE})
        for field in _DETECTOR_PRIVATE_FIELDS
    },
    **{field: frozenset({FieldVisibility.PRIVATE}) for field in _GROUP_PRIVATE_FIELDS},
    **{
        field: frozenset({FieldVisibility.EVALUATOR_ONLY, FieldVisibility.PRIVATE})
        for field in EVALUATOR_ONLY_FIELDS
    },
}


@dataclass(frozen=True, slots=True)
class FieldVisibilityDecision:
    retriever: bool
    detector: bool
    intervention: bool
    evaluator: bool
    releaseable: bool
    private: bool


def field_visibility(field_name: str) -> frozenset[FieldVisibility]:
    try:
        return FIELD_POLICY[field_name]
    except KeyError as exc:
        raise LabelLeakageBlocker(f"LABEL_LEAKAGE_BLOCKER: unknown field {field_name}") from exc


def field_visibility_decision(field_name: str) -> FieldVisibilityDecision:
    policy = field_visibility(field_name)
    return FieldVisibilityDecision(
        retriever=FieldVisibility.RETRIEVER in policy,
        detector=FieldVisibility.DETECTOR in policy,
        intervention=FieldVisibility.INTERVENTION in policy,
        evaluator=True,
        releaseable=FieldVisibility.RELEASEABLE in policy,
        private=FieldVisibility.PRIVATE in policy,
    )


def _normalized_key(value: object) -> str:
    return unicodedata.normalize("NFKC", str(value)).casefold().replace("-", "_")


def _walk(value: object) -> Iterator[object]:
    if is_dataclass(value) and not isinstance(value, type):
        for field in fields(value):  # type: ignore[arg-type]
            yield field.name
            yield from _walk(getattr(value, field.name))
    elif isinstance(value, Mapping):
        for key, item in value.items():
            yield key
            yield from _walk(item)
    elif isinstance(value, (tuple, list, set, frozenset)):
        for item in value:
            yield from _walk(item)
    else:
        yield value


def evaluator_values(record: BenchmarkRecord) -> frozenset[str]:
    values: set[str] = set()
    for field_name in EVALUATOR_ONLY_FIELDS:
        value = getattr(record, field_name)
        for item in _walk(value):
            if item is not None:
                text = item.value if isinstance(item, Enum) else str(item)
                if text:
                    values.add(_normalized_key(text))
    return frozenset(values)


def assert_no_label_leakage(
    payload: object,
    *,
    audience: RuntimeAudience,
    forbidden_values: frozenset[str] = frozenset(),
) -> None:
    if not isinstance(audience, RuntimeAudience):
        raise LabelLeakageBlocker("LABEL_LEAKAGE_BLOCKER: invalid runtime audience")
    normalized_evaluator_fields = {_normalized_key(name) for name in FORBIDDEN_RUNTIME_KEYS}
    for item in _walk(payload):
        normalized = _normalized_key(item)
        if normalized in normalized_evaluator_fields or normalized in forbidden_values:
            raise LabelLeakageBlocker(
                f"LABEL_LEAKAGE_BLOCKER: evaluator-only data in {audience.value} input"
            )


def project_runtime_payload(
    record: BenchmarkRecord, *, audience: RuntimeAudience
) -> dict[str, object]:
    if audience in {RuntimeAudience.RETRIEVER, RuntimeAudience.EMBEDDING}:
        allowed = frozenset(
            {"record_id", "document_text", "entity_id", "claim_family", "schema_version"}
        )
    elif audience is RuntimeAudience.FINGERPRINT:
        allowed = frozenset({"record_id", "entity_id", "claim_family", "schema_version"})
    elif audience is RuntimeAudience.DETECTOR:
        allowed = _BASE_RUNTIME_FIELDS
    else:
        allowed = frozenset({"record_id", "schema_version"})
    payload = {name: getattr(record, name) for name in sorted(allowed)}
    assert_no_label_leakage(
        payload, audience=audience, forbidden_values=evaluator_values(record)
    )
    return payload


__all__ = [
    "EVALUATOR_ONLY_FIELDS",
    "FIELD_POLICY",
    "FORBIDDEN_RUNTIME_KEYS",
    "FieldVisibilityDecision",
    "RuntimeAudience",
    "assert_no_label_leakage",
    "evaluator_values",
    "field_visibility",
    "field_visibility_decision",
    "project_runtime_payload",
]
