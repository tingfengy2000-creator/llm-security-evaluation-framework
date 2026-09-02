from __future__ import annotations

from copy import deepcopy

from llmguard.domains.retrieval.hidden_poisoning.external_blind_review import (
    PHASE2_FIELDS,
)
from scripts.research.compare_pilot4_final_blind_review import _taxonomy
from scripts.research.lock_pilot4_phase2_final_return import _process_diff


def _row(blind_id: str) -> dict[str, str]:
    return {
        "blind_review_id": blind_id,
        "overall_fact_status": "CURRENTLY_CONSISTENT",
        "version_claim_status": "NOT_PRESENT",
        "authority_claim_status": "NOT_PRESENT",
        "minimum_external_evidence_needed": "NOT_APPLICABLE",
        "evidence_selection": "NONE",
        "phase2_issue": "NONE",
        "phase2_reason": "final reason",
    }


def test_first_final_process_diff_reproduces_frozen_shape() -> None:
    unreachable_ids = ["BR-18F1D39495"] + [f"BR-{index:010X}" for index in range(22)]
    extra_ids = ["BR-46BC044669", "BR-C27BF02D5F"]
    remaining_ids = [f"BR-{index:010X}" for index in range(100, 147)]
    identities = unreachable_ids + extra_ids + remaining_ids
    assert len(identities) == 72
    final_rows = [_row(identity) for identity in identities]
    first_rows = deepcopy(final_rows)
    first_by_id = {row["blind_review_id"]: row for row in first_rows}
    final_by_id = {row["blind_review_id"]: row for row in final_rows}
    for identity in unreachable_ids:
        first_by_id[identity]["phase2_issue"] = "SOURCE_UNREACHABLE"
        first_by_id[identity]["phase2_reason"] = "first access limitation"
    final_by_id["BR-18F1D39495"]["phase2_issue"] = "EVIDENCE_MISSING"
    first_by_id["BR-46BC044669"]["minimum_external_evidence_needed"] = "NOT_APPLICABLE"
    final_by_id["BR-46BC044669"]["minimum_external_evidence_needed"] = (
        "ONE_OFFICIAL_EVIDENCE"
    )
    first_by_id["BR-46BC044669"]["phase2_reason"] = "first refinement"
    first_by_id["BR-C27BF02D5F"]["evidence_selection"] = "E2"
    final_by_id["BR-C27BF02D5F"]["evidence_selection"] = "E1+E2"
    first_by_id["BR-C27BF02D5F"]["phase2_reason"] = "first refinement"

    result = _process_diff(first_rows, final_rows)

    assert result["changed_row_count"] == 25
    assert result["source_unreachable_rows_changed"] == 23
    assert result["final_source_unreachable_count"] == 0
    assert result["extra_refinement_blind_ids"] == extra_ids
    assert set(result["changed_field_counts"]) == set(PHASE2_FIELDS)


def test_evidence_level_taxonomy_does_not_automatically_prefer_expected() -> None:
    assert _taxonomy("PHASE2", "overall_fact_status", "BR-0000000001")[0] == (
        "M2 / GUIDE_AMBIGUITY"
    )
    assert _taxonomy("PHASE2", "version_claim_status", "BR-0000000001")[0] == (
        "M5 / EXPECTED_CONTRACT_DEFECT"
    )
    assert _taxonomy("PHASE2", "phase2_issue", "BR-18F1D39495")[0] == (
        "M4 / EVIDENCE_POOL_DEFECT"
    )
    assert (
        _taxonomy("PHASE2", "minimum_external_evidence_needed", "BR-46BC044669")[0]
        == "M9 / PROCESS_ONLY_DIFFERENCE"
    )
