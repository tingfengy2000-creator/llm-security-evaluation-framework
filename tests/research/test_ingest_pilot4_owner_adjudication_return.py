from scripts.research.ingest_pilot4_owner_adjudication_return import (
    apply_owner_rule_overlays,
    consistency_findings,
)


def record(sample_id: str, **values: str) -> dict[str, object]:
    defaults = {
        "text_naturalness": "NATURAL",
        "local_internal_conflict": "NO",
        "phase1_issue": "NONE",
        "overall_fact_status": "CURRENTLY_CONSISTENT",
        "version_claim_status": "NOT_PRESENT",
        "authority_claim_status": "NOT_PRESENT",
        "minimum_external_evidence_needed": "NOT_APPLICABLE",
        "phase2_issue": "NONE",
    }
    defaults.update(values)
    return {
        "sample_id": sample_id,
        "fields": {
            field: {"value": value, "source": "OWNER_ADJUDICATION", "owner_reason": "r"}
            for field, value in defaults.items()
        },
    }


def test_internal_contradiction_rule_is_additive_and_sets_minimum() -> None:
    rows = [
        record(
            "P4Q-0dd2bf0608a7",
            local_internal_conflict="YES",
            overall_fact_status="FACTUAL_CONFLICT",
            minimum_external_evidence_needed="ONE_OFFICIAL_EVIDENCE",
        )
    ]
    overlays = apply_owner_rule_overlays(rows)
    fields = rows[0]["fields"]
    assert fields["minimum_external_evidence_needed"]["value"] == "NOT_APPLICABLE"
    assert (
        fields["minimum_external_evidence_needed"]["pre_overlay_value"]
        == "ONE_OFFICIAL_EVIDENCE"
    )
    assert fields["version_claim_status"]["value"] == "PRESENT_INCORRECT"
    assert len(overlays) == 2


def test_consistency_finds_nonconflict_minimum_and_unbound_e3() -> None:
    rows = [
        record(
            "P4Q-example",
            overall_fact_status="CURRENTLY_CONSISTENT",
            minimum_external_evidence_needed="ONE_OFFICIAL_EVIDENCE",
        )
    ]
    owner_rows = [
        {
            "sample_id": "P4Q-example",
            "field": "version_claim_status",
            "owner_final_value": "PRESENT_CORRECT",
            "owner_decision_reason": "仅通过E3即可判断",
        }
    ]
    findings = consistency_findings(rows, owner_rows)
    assert {item["finding"] for item in findings} == {
        "MINIMUM_NON_CONFLICT_MUST_BE_NOT_APPLICABLE",
        "UNBOUND_E3_PROVENANCE_REFERENCE",
    }
