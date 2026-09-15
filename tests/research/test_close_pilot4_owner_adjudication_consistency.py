from scripts.research.close_pilot4_owner_adjudication_consistency import (
    apply_corrections,
    validate_candidate_view,
)


def candidate(
    sample_id: str,
    *,
    overall: str,
    minimum: str,
    issue: str = "NONE",
    version: str = "NOT_PRESENT",
) -> dict[str, object]:
    values = {
        "text_naturalness": "NATURAL",
        "local_internal_conflict": "NO",
        "phase1_issue": "NONE",
        "overall_fact_status": overall,
        "version_claim_status": version,
        "authority_claim_status": "NOT_PRESENT",
        "minimum_external_evidence_needed": minimum,
        "phase2_issue": issue,
    }
    return {
        "sample_id": sample_id,
        "fields": {
            field: {
                "value": value,
                "source": "OWNER_ADJUDICATION",
                "owner_reason": "raw E3 reason"
                if field == "version_claim_status"
                else "",
            }
            for field, value in values.items()
        },
    }


def test_correction_preserves_before_and_replaces_effective_reason() -> None:
    rows = [
        candidate(
            "P4Q-x",
            overall="CURRENTLY_CONSISTENT",
            minimum="ONE_OFFICIAL_EVIDENCE",
        )
    ]
    applied = apply_corrections(
        rows,
        [
            {
                "correction_id": "C-1",
                "source_finding_ids": [1],
                "sample_id": "P4Q-x",
                "field": "minimum_external_evidence_needed",
                "after": "NOT_APPLICABLE",
                "reason": "minimum only applies to factual conflict",
                "evidence_basis": "owner rule",
                "owner_decision_lineage": "owner",
            },
            {
                "correction_id": "C-2",
                "source_finding_ids": [2],
                "sample_id": "P4Q-x",
                "field": "version_claim_status",
                "after": "NOT_PRESENT",
                "reason": "E1 supports this effective reason",
                "evidence_basis": "frozen E1",
                "owner_decision_lineage": "owner",
            },
        ],
    )
    fields = rows[0]["fields"]
    assert fields["minimum_external_evidence_needed"]["value"] == "NOT_APPLICABLE"
    assert (
        fields["minimum_external_evidence_needed"]["pre_consistency_correction_value"]
        == "ONE_OFFICIAL_EVIDENCE"
    )
    assert (
        fields["version_claim_status"]["pre_consistency_correction_reason"]
        == "raw E3 reason"
    )
    assert (
        fields["version_claim_status"]["owner_reason"]
        == "E1 supports this effective reason"
    )
    assert sum(bool(item["value_changed"]) for item in applied) == 1


def test_validation_passes_closed_relations() -> None:
    rows = [
        candidate(
            "P4Q-a",
            overall="CURRENTLY_CONSISTENT",
            minimum="NOT_APPLICABLE",
        ),
        candidate(
            "P4Q-b",
            overall="INSUFFICIENT_EVIDENCE",
            minimum="NOT_APPLICABLE",
            issue="EVIDENCE_MISSING",
            version="PRESENT_EVIDENCE_INSUFFICIENT",
        ),
    ]
    for row in rows:
        row["fields"]["version_claim_status"]["owner_reason"] = "frozen E1/E2 only"
    result = validate_candidate_view(rows)
    assert result["status"] == "PASS"
    assert result["unresolved_consistency_blocker"] == 0
