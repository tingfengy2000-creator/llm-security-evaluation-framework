from __future__ import annotations

from dataclasses import FrozenInstanceError, fields

import pytest

from llmguard.domains.retrieval.hidden_poisoning import (
    EVALUATOR_ONLY_FIELDS,
    SCHEMA_VERSION,
    AttackType,
    BenchmarkRecord,
    FieldVisibility,
    LabelLeakageBlocker,
    RuntimeAudience,
    SchemaValidationError,
    StealthLevel,
    assert_no_label_leakage,
    evaluator_values,
    field_visibility,
    field_visibility_decision,
    project_runtime_payload,
)


def test_required_and_unknown_schema_fields_fail_closed(
    synthetic_records: tuple[BenchmarkRecord, ...],
) -> None:
    payload = synthetic_records[0].claim.canonical_payload()
    missing = dict(payload)
    missing.pop("record_id")
    with pytest.raises(SchemaValidationError, match="missing required fields"):
        type(synthetic_records[0].claim).from_mapping(missing)
    with pytest.raises(SchemaValidationError, match="unknown fields"):
        type(synthetic_records[0].claim).from_mapping({**payload, "unknown": True})
    with pytest.raises(SchemaValidationError, match="record payload is invalid"):
        BenchmarkRecord.from_mapping(synthetic_records[0].canonical_payload())


def test_canonical_serialization_and_sha_are_deterministic(
    synthetic_records: tuple[BenchmarkRecord, ...],
) -> None:
    record = synthetic_records[0]
    assert record.schema_version == SCHEMA_VERSION
    assert record.canonical_json() == record.canonical_json()
    assert record.sha256() == record.sha256()
    assert len(record.sha256()) == 64
    with pytest.raises(FrozenInstanceError):
        record.record_id = "changed"  # type: ignore[misc]


def test_required_enums_cover_protocol() -> None:
    assert {item.value for item in AttackType} == {
        "HKP_1_NUMERIC_ENTITY",
        "HKP_2_CONDITION_EXCEPTION",
        "HKP_3_TEMPORAL_VERSION",
        "HKP_4_PROVENANCE_AUTHORITY",
    }
    assert {item.value for item in StealthLevel} == {"S1", "S2", "S3"}


def test_central_policy_marks_every_evaluator_field_private() -> None:
    for field_name in EVALUATOR_ONLY_FIELDS:
        visibility = field_visibility(field_name)
        assert FieldVisibility.EVALUATOR_ONLY in visibility
        assert FieldVisibility.PRIVATE in visibility
        assert FieldVisibility.RETRIEVER not in visibility
        assert FieldVisibility.DETECTOR not in visibility


def test_central_policy_answers_all_benchmark_schema_visibility_questions(
    synthetic_records: tuple[BenchmarkRecord, ...],
) -> None:
    record = synthetic_records[0]
    schema_types = (type(record), type(record.claim), type(record.version), type(record.provenance))
    for field_name in {field.name for schema_type in schema_types for field in fields(schema_type)}:
        decision = field_visibility_decision(field_name)
        assert decision.evaluator is True
        assert isinstance(decision.retriever, bool)
        assert isinstance(decision.detector, bool)
        assert isinstance(decision.intervention, bool)
        assert isinstance(decision.releaseable, bool)
        assert isinstance(decision.private, bool)


@pytest.mark.parametrize(
    "audience",
    [
        RuntimeAudience.RETRIEVER,
        RuntimeAudience.DETECTOR,
        RuntimeAudience.INTERVENTION,
        RuntimeAudience.EMBEDDING,
        RuntimeAudience.FINGERPRINT,
    ],
)
def test_recursive_evaluator_field_leakage_blocks_every_runtime_input(
    audience: RuntimeAudience,
) -> None:
    with pytest.raises(LabelLeakageBlocker, match="LABEL_LEAKAGE_BLOCKER"):
        assert_no_label_leakage(
            {"safe": [{"nested": {"Ｇｒｏｕｎｄ＿Ｔｒｕｔｈ": "x"}}]},
            audience=audience,
        )


def test_evaluator_value_leakage_is_not_silently_deleted(
    synthetic_records: tuple[BenchmarkRecord, ...],
) -> None:
    record = synthetic_records[0]
    with pytest.raises(LabelLeakageBlocker, match="LABEL_LEAKAGE_BLOCKER"):
        assert_no_label_leakage(
            {"text": record.adjudicated_label},
            audience=RuntimeAudience.EMBEDDING,
            forbidden_values=evaluator_values(record),
        )
    with pytest.raises(LabelLeakageBlocker, match="LABEL_LEAKAGE_BLOCKER"):
        assert_no_label_leakage(record, audience=RuntimeAudience.DETECTOR)


def test_controlled_projection_contains_no_evaluator_fields_or_values(
    synthetic_records: tuple[BenchmarkRecord, ...],
) -> None:
    record = synthetic_records[0]
    for audience in RuntimeAudience:
        payload = project_runtime_payload(record, audience=audience)
        assert EVALUATOR_ONLY_FIELDS.isdisjoint(payload)
        assert_no_label_leakage(
            payload, audience=audience, forbidden_values=evaluator_values(record)
        )
