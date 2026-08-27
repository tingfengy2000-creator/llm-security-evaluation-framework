from __future__ import annotations

from collections import OrderedDict

import pytest

from llmguard.domains.retrieval.hidden_poisoning.annotation_v2 import (
    PHASE1_V2_FIELDS,
    PHASE2_V2_FIELDS,
    REVISION_LOG_FIELDS,
    ResponseMode,
    agreement_subset_rule,
    apply_not_applicable_rules,
    validate_phase1_v2_row,
    validate_phase2_v2_row,
    validate_revision_row,
)
from llmguard.domains.retrieval.hidden_poisoning.schema import SchemaValidationError


def _phase2_row() -> OrderedDict[str, object]:
    values: dict[str, object] = {
        "sample_id": "S-1",
        "claim_text": "候选事实。",
        "version_context": "版本语境。",
        "source_title": "官方来源",
        "official_url": "https://example.invalid/official",
        "claim_matches_source": "YES",
        "fact_changed": "NO",
        "version_relation_present": "NO",
        "version_relation_correct": "NOT_APPLICABLE",
        "history_or_update_claim_present": "NO",
        "legitimate_update_or_history": "NOT_APPLICABLE",
        "authority_claim_present": "NO",
        "authority_matches": "NOT_APPLICABLE",
        "overall_fact_status": "CURRENTLY_CONSISTENT",
        "confidence": "5",
        "evidence_url_1": "https://example.invalid/evidence",
        "evidence_url_2": "",
        "reasoning_short": "官方证据直接支持。",
        "professional_lookup_used": "NO",
        "time_seconds": "120",
        "rereview_time_seconds": "45",
        "issue_flag": "NONE",
    }
    return OrderedDict((field, values[field]) for field in PHASE2_V2_FIELDS)


def _phase1_row() -> OrderedDict[str, object]:
    values: dict[str, object] = {
        "sample_id": "S-1",
        "claim_text": "候选事实。",
        "version_context": "版本语境。",
        "source_title": "官方来源",
        "language_natural_score": "5",
        "topic_relevance_score": "5",
        "locally_detectable": "NO",
        "cross_document_evidence_needed": "YES",
        "assigned_stealth_level": "S3",
        "confidence": "4",
        "reasoning_short": "需要跨版本证据。",
        "time_seconds": "120",
        "rereview_time_seconds": "35",
        "issue_flag": "NONE",
    }
    return OrderedDict((field, values[field]) for field in PHASE1_V2_FIELDS)


def test_phase1_and_phase2_valid_completed_rows_pass() -> None:
    validate_phase1_v2_row(_phase1_row())
    validate_phase2_v2_row(_phase2_row())


def test_not_applicable_rules_cover_all_three_conditional_fields() -> None:
    row = _phase2_row()
    row["version_relation_correct"] = "YES"
    row["legitimate_update_or_history"] = "UNCERTAIN"
    row["authority_matches"] = "NO"
    apply_not_applicable_rules(row)
    assert row["version_relation_correct"] == "NOT_APPLICABLE"
    assert row["legitimate_update_or_history"] == "NOT_APPLICABLE"
    assert row["authority_matches"] == "NOT_APPLICABLE"
    validate_phase2_v2_row(row)


@pytest.mark.parametrize(
    ("present_field", "correctness_field"),
    [
        ("version_relation_present", "version_relation_correct"),
        ("history_or_update_claim_present", "legitimate_update_or_history"),
        ("authority_claim_present", "authority_matches"),
    ],
)
def test_present_yes_requires_a_correctness_judgment(
    present_field: str, correctness_field: str
) -> None:
    row = _phase2_row()
    row[present_field] = "YES"
    row[correctness_field] = "NOT_APPLICABLE"
    with pytest.raises(SchemaValidationError):
        validate_phase2_v2_row(row)


def test_always_applicable_fields_reject_not_applicable() -> None:
    row = _phase2_row()
    row["claim_matches_source"] = "NOT_APPLICABLE"
    with pytest.raises(SchemaValidationError):
        validate_phase2_v2_row(row)


def test_process_lookup_missing_requires_issue_binding() -> None:
    row = _phase2_row()
    row["professional_lookup_used"] = "MISSING_NOT_RECOVERABLE"
    with pytest.raises(SchemaValidationError):
        validate_phase2_v2_row(row)
    row["issue_flag"] = "MISSING_NOT_RECOVERABLE"
    validate_phase2_v2_row(row)


def test_template_mode_keeps_frozen_columns_but_allows_blank_responses() -> None:
    row = _phase2_row()
    for field in PHASE2_V2_FIELDS[5:]:
        row[field] = ""
    validate_phase2_v2_row(row, mode=ResponseMode.TEMPLATE)
    row.move_to_end("claim_text")
    with pytest.raises(SchemaValidationError):
        validate_phase2_v2_row(row, mode=ResponseMode.TEMPLATE)


def test_revision_contract_rejects_agreement_improvement_reason() -> None:
    values: dict[str, object] = {
        "sample_id": "S-1",
        "field_name": "authority_matches",
        "review_action": "REVISE",
        "previous_value": "YES",
        "new_value": "NOT_APPLICABLE",
        "revision_reason_code": "AGREEMENT_IMPROVEMENT",
        "revision_reason_short": "",
    }
    row = OrderedDict((field, values[field]) for field in REVISION_LOG_FIELDS)
    with pytest.raises(SchemaValidationError):
        validate_revision_row(row, completed=True)


def test_agreement_rules_are_prepared_without_calculation() -> None:
    assert agreement_subset_rule("authority_claim_present") == "ALL_SHARED_SAMPLE_IDS"
    assert agreement_subset_rule("authority_matches") == "BOTH_AUTHORITY_CLAIM_PRESENT_YES_ONLY"
    assert agreement_subset_rule("professional_lookup_used") == "EXCLUDED_PROCESS_OR_FREE_TEXT"
