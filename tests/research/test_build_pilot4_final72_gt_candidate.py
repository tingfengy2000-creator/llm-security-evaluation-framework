from scripts.research.build_pilot4_final72_gt_candidate import (
    classify_mismatch,
    compare_expected,
    no_expected_keys,
)


def human_record(sample_id: str, **updates: str) -> dict[str, object]:
    values = {
        "text_naturalness": "NATURAL",
        "local_internal_conflict": "NO",
        "phase1_issue": "NONE",
        "overall_fact_status": "CURRENTLY_CONSISTENT",
        "version_claim_status": "NOT_PRESENT",
        "authority_claim_status": "NOT_PRESENT",
        "minimum_external_evidence_needed": "NOT_APPLICABLE",
        "phase2_issue": "NONE",
    }
    values.update(updates)
    return {
        "sample_id": sample_id,
        "fields": {
            field: {"value": value, "source": "A_B_AGREEMENT", "owner_reason": ""}
            for field, value in values.items()
        },
    }


def expected_row(sample_id: str, **updates: str) -> dict[str, object]:
    row: dict[str, object] = {
        "sample_id": sample_id,
        "text_naturalness": "NATURAL",
        "local_internal_conflict": "NO",
        "phase1_issue": "NONE",
        "overall_fact_status": "CURRENTLY_CONSISTENT",
        "version_claim_status": "NOT_PRESENT",
        "authority_claim_status": "NOT_PRESENT",
        "minimum_external_evidence_needed": "NOT_APPLICABLE",
    }
    row.update(updates)
    return row


def test_compare_does_not_invent_expected_phase2_issue() -> None:
    humans = [human_record(f"P4Q-{index:02d}") for index in range(72)]
    expected = {"rows": [expected_row(f"P4Q-{index:02d}") for index in range(72)]}
    comparisons, mismatches, summary = compare_expected(humans, expected)
    assert len(comparisons) == 576
    assert summary["comparable_field_count"] == 504
    assert summary["expected_field_not_defined_count"] == 72
    assert summary["exact_match_count"] == 504
    assert not mismatches
    issue_rows = [row for row in comparisons if row["field"] == "phase2_issue"]
    assert {row["comparison_status"] for row in issue_rows} == {
        "EXPECTED_FIELD_NOT_DEFINED"
    }
    assert all(row["expected_v3_value"] is None for row in issue_rows)


def test_known_evidence_defect_is_nonblocking() -> None:
    human = human_record(
        "P4Q-evidence",
        overall_fact_status="INSUFFICIENT_EVIDENCE",
        version_claim_status="PRESENT_EVIDENCE_INSUFFICIENT",
        phase2_issue="EVIDENCE_MISSING",
    )
    taxonomy = classify_mismatch(
        "P4Q-evidence",
        "overall_fact_status",
        "INSUFFICIENT_EVIDENCE",
        "FACTUAL_CONFLICT",
        human,
        expected_row(
            "P4Q-evidence",
            overall_fact_status="FACTUAL_CONFLICT",
            version_claim_status="PRESENT_INCORRECT",
            minimum_external_evidence_needed="ONE_OFFICIAL_EVIDENCE",
        ),
    )
    assert taxonomy[0] == "EVIDENCE_DEFECT"
    assert taxonomy[3] is False


def test_expected_relation_defect_does_not_override_human() -> None:
    human = human_record(
        "P4Q-internal",
        local_internal_conflict="YES",
        overall_fact_status="FACTUAL_CONFLICT",
    )
    taxonomy = classify_mismatch(
        "P4Q-internal",
        "minimum_external_evidence_needed",
        "NOT_APPLICABLE",
        "ONE_OFFICIAL_EVIDENCE",
        human,
        expected_row(
            "P4Q-internal",
            local_internal_conflict="YES",
            overall_fact_status="FACTUAL_CONFLICT",
            minimum_external_evidence_needed="ONE_OFFICIAL_EVIDENCE",
        ),
    )
    assert taxonomy[0] == "EXPECTED_V3_DEFECT"
    assert taxonomy[3] is False


def test_expected_key_leakage_guard() -> None:
    assert no_expected_keys({"records": [{"sample_id": "P4Q-x", "labels": {}}]})
    assert not no_expected_keys({"expected_v3": "forbidden"})
