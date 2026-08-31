from __future__ import annotations

from copy import deepcopy

from llmguard.domains.retrieval.hidden_poisoning.adjudication import (
    OwnerCorrection,
    validate_owner_adjudication_rows,
)


def _candidate(candidate_id: str) -> dict[str, str]:
    return {
        "canonical_candidate_id": candidate_id,
        "owner_resolution_status": "RESOLVED",
        "benchmark_inclusion_decision": "INCLUDE",
    }


def _issue(
    issue_id: str,
    candidate_id: str,
    field: str,
    value: str,
) -> dict[str, str]:
    return {
        "issue_id": issue_id,
        "canonical_candidate_id": candidate_id,
        "disagreement_field": field,
        "owner_final_value": value,
        "owner_rationale": "owner checked the evidence",
        "benchmark_inclusion_decision": "INCLUDE",
    }


def test_owner_adjudication_validation_accepts_executable_unique_values() -> None:
    issues = [
        _issue("D-001", "C-1", "locally_detectable", "NO"),
        _issue(
            "L-001",
            "C-1",
            "overall_fact_status + assigned_stealth_level",
            "overall_fact_status=LEGITIMATE_VERSION_OR_HISTORY; "
            "assigned_stealth_level=NOT_APPLICABLE",
        ),
    ]
    before = deepcopy(issues)

    result = validate_owner_adjudication_rows(issues, [_candidate("C-1")])

    assert result.passed
    assert result.issue_count == 2
    assert result.candidate_count == 1
    assert issues == before


def test_owner_adjudication_validation_fails_on_invalid_and_conflicting_values() -> None:
    issues = [
        _issue("D-001", "C-1", "locally_detectable", "NO"),
        _issue(
            "L-001",
            "C-1",
            "assigned_stealth_level + locally_detectable",
            "assigned_stealth_level=S2; locally_detectable=YES",
        ),
        _issue(
            "L-002",
            "C-2",
            "assigned_stealth_level + cross_document_evidence_needed",
            "assigned_stealth_level=LEGITIMATE_VERSION_OR_HISTORY; "
            "cross_document_evidence_needed=NO",
        ),
        _issue("D-002", "C-3", "version_relation_present", "YES;"),
    ]

    result = validate_owner_adjudication_rows(
        issues,
        [_candidate("C-1"), _candidate("C-2"), _candidate("C-3")],
    )

    assert not result.passed
    assert result.pending_count == 0
    assert {(problem.problem_type, problem.canonical_candidate_id) for problem in result.problems} == {
        ("CONFLICTING_OWNER_DECISIONS", "C-1"),
        ("OWNER_FINAL_VALUE_INVALID", "C-2"),
        ("OWNER_FINAL_VALUE_INVALID", "C-3"),
    }


def test_owner_adjudication_validation_rejects_pending_rows() -> None:
    pending = _issue("D-001", "C-1", "locally_detectable", "")

    result = validate_owner_adjudication_rows([pending], [_candidate("C-1")])

    assert not result.passed
    assert result.pending_count == 1


def test_owner_correction_supersedes_without_mutating_workbook_rows() -> None:
    issues = [
        _issue("D-001", "C-1", "locally_detectable", "YES"),
        _issue("L-001", "C-1", "locally_detectable", "NO"),
        _issue("D-002", "C-2", "version_relation_present", "YES;"),
    ]
    before = deepcopy(issues)
    corrections = (
        OwnerCorrection("C-1", "locally_detectable", "NO"),
        OwnerCorrection("C-2", "version_relation_present", "YES"),
    )

    result = validate_owner_adjudication_rows(
        issues, [_candidate("C-1"), _candidate("C-2")], corrections
    )

    assert result.passed
    assert issues == before
