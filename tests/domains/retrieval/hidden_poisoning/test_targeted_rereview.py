from __future__ import annotations

import pytest

from llmguard.domains.retrieval.hidden_poisoning.schema import SchemaValidationError
from llmguard.domains.retrieval.hidden_poisoning.targeted_rereview import (
    TARGETED_PHASE1_FIELDS,
    TARGETED_PHASE2_FIELDS,
    validate_targeted_task_row,
    workload_summary,
)


def _row() -> dict[str, str]:
    return {
        "task_id": "A-P2-authority_matches-01",
        "task_type": "TARGETED_REREVIEW",
        "sample_id": "S-01",
        "field_name": "authority_matches",
        "candidate": "example",
        "v1_value": "UNCERTAIN",
        "new_value": "NOT_APPLICABLE",
        "review_action": "REVISE",
        "revision_reason_code": "FIELD_NOT_APPLICABLE",
        "revision_reason_short": "候选没有提出机关命题",
        "rereview_time_seconds": "12",
    }


def test_targeted_scope_and_workload_are_frozen() -> None:
    assert TARGETED_PHASE1_FIELDS == (
        "locally_detectable",
        "cross_document_evidence_needed",
        "assigned_stealth_level",
    )
    assert len(TARGETED_PHASE2_FIELDS) == 7
    workload = workload_summary()
    assert workload["A_total_tasks_including_process_fixes"] == 360
    assert workload["B_total_tasks_including_process_fixes"] == 382
    assert workload["substantive_tasks_saved_per_annotator"] == 216


def test_completed_targeted_row_validates() -> None:
    validate_targeted_task_row(_row(), completed=True)


def test_targeted_row_rejects_evaluator_leakage() -> None:
    row = _row()
    row["ground_truth"] = "poison"
    with pytest.raises(SchemaValidationError, match="leaks evaluator-only"):
        validate_targeted_task_row(row, completed=True)


def test_targeted_row_rejects_inconsistent_action() -> None:
    row = _row()
    row["review_action"] = "KEEP"
    with pytest.raises(SchemaValidationError, match="must be derived"):
        validate_targeted_task_row(row, completed=True)
