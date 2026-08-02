from __future__ import annotations

import pytest

from llmguard.domains.retrieval.hidden_poisoning import (
    ALLOWED_CHANGED_FIELDS,
    AttackType,
    HardNegativeType,
    MutationSpec,
    SchemaValidationError,
    validate_hard_negative_coverage,
    validate_mutation_fields,
)


@pytest.mark.parametrize("attack_type", list(AttackType))
def test_each_hkp_accepts_its_declared_field_contract(attack_type: AttackType) -> None:
    changed_field = next(iter(sorted(ALLOWED_CHANGED_FIELDS[attack_type])))
    spec = MutationSpec(
        attack_type=attack_type,
        changed_fields=(changed_field,),
        preserved_fields=("record_id", "entity_id", "claim_family"),
        source_record_id="SYN-01",
        mutation_id=f"M-{attack_type.value}",
        expected_fact_change="仅描述字段级合成事实变化",
        retrieval_relevance_constraint="变换前后保持同一合成查询主题",
        fluency_review_required=True,
        stealth_review_required=True,
    )
    assert spec.changed_fields == (changed_field,)


def test_hkp_prohibited_field_change_fails_closed() -> None:
    with pytest.raises(SchemaValidationError, match="HKP_PROHIBITED_FIELD_CHANGE"):
        validate_mutation_fields(AttackType.HKP_1_NUMERIC_ENTITY, ("effective_at",))


def test_mutation_cannot_change_preserved_identity() -> None:
    with pytest.raises(SchemaValidationError, match="disjoint"):
        MutationSpec(
            attack_type=AttackType.HKP_1_NUMERIC_ENTITY,
            changed_fields=("object_value",),
            preserved_fields=("record_id", "entity_id", "claim_family", "object_value"),
            source_record_id="SYN-01",
            mutation_id="M-1",
            expected_fact_change="合成变化",
            retrieval_relevance_constraint="保持主题",
            fluency_review_required=True,
            stealth_review_required=True,
        )


def test_all_twelve_hard_negative_types_are_required() -> None:
    coverage = validate_hard_negative_coverage(tuple(HardNegativeType))
    assert len(coverage) == 12
    assert all(count == 1 for count in coverage.values())
    with pytest.raises(SchemaValidationError, match="HARD_NEGATIVE_COVERAGE_BLOCKER"):
        validate_hard_negative_coverage(tuple(HardNegativeType)[:-1])
