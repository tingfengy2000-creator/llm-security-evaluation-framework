from __future__ import annotations

import pytest

from scripts.research.lock_compare_pilot4_r3_acceptance import (
    MISMATCH_DISPOSITIONS,
    RAW_COLUMNS,
    agreement_fraction,
    validate_internal_consistency,
    validate_raw,
)


def _row(*, overall: str, minimum: str, row_id: int = 1) -> dict[str, str]:
    return {
        "blind_review_id": f"R3-{row_id:012X}",
        "overall_fact_status": overall,
        "version_claim_status": "NOT_PRESENT",
        "authority_claim_status": "NOT_PRESENT",
        "minimum_external_evidence_needed": minimum,
        "evidence_selection": "E1",
        "phase2_issue": "NONE",
        "phase2_reason": "证据理由完整。",
    }


def test_minimum_evidence_internal_rule_accepts_frozen_distribution() -> None:
    rows = [
        *[
            _row(overall="FACTUAL_CONFLICT", minimum="ONE_OFFICIAL_EVIDENCE", row_id=index)
            for index in range(1, 8)
        ],
        _row(
            overall="FACTUAL_CONFLICT",
            minimum="MULTI_EVIDENCE_OR_VERSION_CHAIN",
            row_id=8,
        ),
        *[
            _row(overall="CURRENTLY_CONSISTENT", minimum="NOT_APPLICABLE", row_id=index)
            for index in range(9, 38)
        ],
    ]
    result = validate_internal_consistency(rows)
    assert result["conflict_count"] == 8
    assert result["non_conflict_count"] == 29
    assert result["violation_count"] == 0


@pytest.mark.parametrize(
    ("overall", "minimum"),
    [
        ("CURRENTLY_CONSISTENT", "ONE_OFFICIAL_EVIDENCE"),
        ("FACTUAL_CONFLICT", "NOT_APPLICABLE"),
    ],
)
def test_minimum_evidence_internal_rule_fails_closed(overall: str, minimum: str) -> None:
    with pytest.raises(ValueError, match="R3_INTERNAL_RULE_CONSISTENCY_BLOCKER"):
        validate_internal_consistency([_row(overall=overall, minimum=minimum)])


def test_control_threshold_does_not_round_14_of_16_to_ninety_percent() -> None:
    result = agreement_fraction(14, 16)
    assert result["fraction"] == 0.875
    assert result["percent"] == 87.5
    assert result["agree"] < 15


def test_control_threshold_accepts_only_at_least_15_of_16() -> None:
    assert agreement_fraction(15, 16)["fraction"] >= 0.90
    assert agreement_fraction(14, 16)["fraction"] < 0.90


def test_locked_mismatch_dispositions_preserve_expected_as_non_absolute() -> None:
    taxonomy = [value["taxonomy"] for value in MISMATCH_DISPOSITIONS.values()]
    assert taxonomy.count("R3-M1 REVIEWER_VARIANCE") == 2
    assert taxonomy.count("R3-M4 EXPECTED_V2_DEFECT") == 7
    assert len(MISMATCH_DISPOSITIONS) == 9


def test_raw_validator_rejects_wrong_schema_before_hidden_load() -> None:
    rows = [
        _row(overall="CURRENTLY_CONSISTENT", minimum="NOT_APPLICABLE", row_id=index)
        for index in range(1, 38)
    ]
    with pytest.raises(ValueError, match="R3_SCHEMA_BLOCKER"):
        validate_raw(rows, RAW_COLUMNS[:-1])
