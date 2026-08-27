"""Executable contracts for the Pilot2 Annotation Schema V2 re-review.

The contracts deliberately separate immutable V1 answers from V2 responses.
They validate applicability, process-field, and leakage boundaries; they do not
calculate agreement or adjudicate any label.
"""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from enum import Enum

from .schema import SchemaValidationError


class ApplicabilityCategory(str, Enum):
    ALWAYS_APPLICABLE = "ALWAYS_APPLICABLE"
    CONDITIONALLY_APPLICABLE = "CONDITIONALLY_APPLICABLE"
    PROCESS_ONLY = "PROCESS_ONLY"


class ResponseMode(str, Enum):
    TEMPLATE = "TEMPLATE"
    COMPLETED = "COMPLETED"


class OverallFactStatus(str, Enum):
    CURRENTLY_CONSISTENT = "CURRENTLY_CONSISTENT"
    LEGITIMATE_VERSION_OR_HISTORY = "LEGITIMATE_VERSION_OR_HISTORY"
    FACTUAL_CONFLICT = "FACTUAL_CONFLICT"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"


class LookupSourceType(str, Enum):
    OFFICIAL_PRIMARY_SOURCE = "OFFICIAL_PRIMARY_SOURCE"
    OFFICIAL_REPOST = "OFFICIAL_REPOST"
    SEARCH_ENGINE = "SEARCH_ENGINE"
    SECONDARY_REFERENCE = "SECONDARY_REFERENCE"
    AI_ASSISTED_EXPLANATION = "AI_ASSISTED_EXPLANATION"
    OTHER = "OTHER"


FOUR_VALUE_RESPONSES = frozenset({"YES", "NO", "UNCERTAIN", "NOT_APPLICABLE"})
PRESENT_RESPONSES = frozenset({"YES", "NO"})
CONDITIONAL_CORRECTNESS_RESPONSES = frozenset({"YES", "NO", "UNCERTAIN", "NOT_APPLICABLE"})
TERNARY_RESPONSES = frozenset({"YES", "NO", "UNCERTAIN"})
PROCESS_LOOKUP_RESPONSES = frozenset({"YES", "NO", "MISSING_NOT_RECOVERABLE"})
REVIEW_ACTIONS = frozenset({"KEEP", "REVISE"})
REVISION_REASON_CODES = frozenset(
    {
        "FIELD_NOT_APPLICABLE",
        "FIELD_DEFINITION_CLARIFIED",
        "EVIDENCE_RECHECK",
        "PREVIOUS_INPUT_ERROR",
        "SOURCE_CLASSIFICATION_FIXED",
        "MISSING_VALUE_COMPLETED",
        "OTHER_EXPLAINED",
    }
)
ISSUE_FLAGS = frozenset(
    {
        "NONE",
        "SOURCE_UNAVAILABLE",
        "SOURCE_CONFLICT",
        "MISSING_CONTEXT",
        "BROKEN_CANDIDATE",
        "VERSION_CHAIN_UNCLEAR",
        "PROFESSIONAL_SCOPE_LIMIT",
        "ENCODING_ISSUE",
        "MISSING_NOT_RECOVERABLE",
        "OTHER_EXPLAINED",
    }
)

PHASE1_V2_FIELDS = (
    "sample_id",
    "claim_text",
    "version_context",
    "source_title",
    "language_natural_score",
    "topic_relevance_score",
    "locally_detectable",
    "cross_document_evidence_needed",
    "assigned_stealth_level",
    "confidence",
    "reasoning_short",
    "time_seconds",
    "rereview_time_seconds",
    "issue_flag",
)

PHASE2_V2_FIELDS = (
    "sample_id",
    "claim_text",
    "version_context",
    "source_title",
    "official_url",
    "claim_matches_source",
    "fact_changed",
    "version_relation_present",
    "version_relation_correct",
    "history_or_update_claim_present",
    "legitimate_update_or_history",
    "authority_claim_present",
    "authority_matches",
    "overall_fact_status",
    "confidence",
    "evidence_url_1",
    "evidence_url_2",
    "reasoning_short",
    "professional_lookup_used",
    "time_seconds",
    "rereview_time_seconds",
    "issue_flag",
)

REVISION_LOG_FIELDS = (
    "sample_id",
    "field_name",
    "review_action",
    "previous_value",
    "new_value",
    "revision_reason_code",
    "revision_reason_short",
)

RETROSPECTIVE_DECLARATION_FIELDS = (
    "annotator_id",
    "phase",
    "independent_completion",
    "no_peer_result_seen",
    "no_sample_discussion",
    "phase2_seen_before_phase1_submission",
    "ai_direct_labeling_used",
    "sample_id_changed",
    "actual_distribution_order_confirmed",
    "retrospective_declaration",
    "signed_name_or_alias",
    "completed_at_utc",
)

LOOKUP_REVIEW_FIELDS = (
    "sample_id",
    "lookup_utc",
    "source_url",
    "previous_source_type",
    "source_type_v2",
    "access_status",
    "notes",
    "review_action",
    "revision_reason_code",
)

PRESENT_TO_CORRECTNESS = {
    "version_relation_present": "version_relation_correct",
    "history_or_update_claim_present": "legitimate_update_or_history",
    "authority_claim_present": "authority_matches",
}

FORBIDDEN_ANNOTATOR_KEYS = frozenset(
    {
        "attack_type",
        "candidate_kind",
        "candidate_label",
        "candidate_intent",
        "mutation_operation",
        "mutation_spec",
        "expected_conclusion",
        "hard_negative_type",
        "candidate_stealth_level",
        "fact_change_description",
        "owner_mapping",
        "ground_truth",
        "poison_label",
        "attack_id",
    }
)


def _assert_exact_fields(row: Mapping[str, object], expected: Sequence[str]) -> None:
    actual = tuple(row)
    if actual != tuple(expected):
        raise SchemaValidationError(f"frozen V2 columns mismatch: {actual!r}")


def _assert_visible_identity(row: Mapping[str, object], fields: Sequence[str]) -> None:
    for field in fields:
        value = row[field]
        if not isinstance(value, str) or not value.strip():
            raise SchemaValidationError(f"{field} must preserve a non-empty visible identity")


def _assert_no_forbidden_keys(row: Mapping[str, object]) -> None:
    leaked = FORBIDDEN_ANNOTATOR_KEYS & set(row)
    if leaked:
        raise SchemaValidationError(f"annotator row exposes owner/evaluator-only keys: {sorted(leaked)}")


def apply_not_applicable_rules(row: MutableMapping[str, object]) -> None:
    """Apply the three V2 conditional applicability rules in place."""

    for present_field, correctness_field in PRESENT_TO_CORRECTNESS.items():
        if row.get(present_field) == "NO":
            row[correctness_field] = "NOT_APPLICABLE"


def validate_phase1_v2_row(
    row: Mapping[str, object], *, mode: ResponseMode = ResponseMode.COMPLETED
) -> None:
    _assert_exact_fields(row, PHASE1_V2_FIELDS)
    _assert_no_forbidden_keys(row)
    _assert_visible_identity(row, PHASE1_V2_FIELDS[:4])
    if mode is ResponseMode.TEMPLATE:
        return

    for field in ("language_natural_score", "topic_relevance_score", "confidence"):
        if str(row[field]) not in {"1", "2", "3", "4", "5"}:
            raise SchemaValidationError(f"{field} must be an integer score from 1 through 5")
    for field in ("locally_detectable", "cross_document_evidence_needed"):
        if row[field] not in TERNARY_RESPONSES:
            raise SchemaValidationError(f"{field} must be YES, NO, or UNCERTAIN")
    if row["assigned_stealth_level"] not in {"S1", "S2", "S3", "NOT_APPLICABLE", "UNCERTAIN"}:
        raise SchemaValidationError("assigned_stealth_level has an unsupported value")
    if not str(row["reasoning_short"]).strip():
        raise SchemaValidationError("reasoning_short is required")
    if not str(row["rereview_time_seconds"]).strip():
        raise SchemaValidationError("rereview_time_seconds is required")
    if row["issue_flag"] not in ISSUE_FLAGS:
        raise SchemaValidationError("issue_flag has an unsupported value")


def validate_phase2_v2_row(
    row: Mapping[str, object], *, mode: ResponseMode = ResponseMode.COMPLETED
) -> None:
    _assert_exact_fields(row, PHASE2_V2_FIELDS)
    _assert_no_forbidden_keys(row)
    _assert_visible_identity(row, PHASE2_V2_FIELDS[:5])
    if mode is ResponseMode.TEMPLATE:
        return

    for field in ("claim_matches_source", "fact_changed"):
        if row[field] not in TERNARY_RESPONSES:
            raise SchemaValidationError(f"{field} cannot be NOT_APPLICABLE")
    for present_field, correctness_field in PRESENT_TO_CORRECTNESS.items():
        present = row[present_field]
        correctness = row[correctness_field]
        if present not in PRESENT_RESPONSES:
            raise SchemaValidationError(f"{present_field} must be YES or NO")
        if correctness not in CONDITIONAL_CORRECTNESS_RESPONSES:
            raise SchemaValidationError(f"{correctness_field} has an unsupported value")
        if present == "NO" and correctness != "NOT_APPLICABLE":
            raise SchemaValidationError(f"{correctness_field} must be NOT_APPLICABLE when {present_field}=NO")
        if present == "YES" and correctness == "NOT_APPLICABLE":
            raise SchemaValidationError(f"{correctness_field} must be judged when {present_field}=YES")
    if row["overall_fact_status"] not in {value.value for value in OverallFactStatus}:
        raise SchemaValidationError("overall_fact_status has an unsupported value")
    if str(row["confidence"]) not in {"1", "2", "3", "4", "5"}:
        raise SchemaValidationError("confidence must be an integer score from 1 through 5")
    if not str(row["reasoning_short"]).strip():
        raise SchemaValidationError("reasoning_short is required")
    if row["professional_lookup_used"] not in PROCESS_LOOKUP_RESPONSES:
        raise SchemaValidationError("professional_lookup_used must be YES, NO, or MISSING_NOT_RECOVERABLE")
    if row["professional_lookup_used"] == "MISSING_NOT_RECOVERABLE" and row["issue_flag"] != "MISSING_NOT_RECOVERABLE":
        raise SchemaValidationError("unrecoverable lookup memory must be bound in issue_flag")
    if not str(row["rereview_time_seconds"]).strip():
        raise SchemaValidationError("rereview_time_seconds is required")
    if row["issue_flag"] not in ISSUE_FLAGS:
        raise SchemaValidationError("issue_flag has an unsupported value")


def validate_revision_row(row: Mapping[str, object], *, completed: bool) -> None:
    _assert_exact_fields(row, REVISION_LOG_FIELDS)
    if not str(row["sample_id"]).strip() or not str(row["field_name"]).strip():
        raise SchemaValidationError("revision rows require sample_id and field_name")
    if not completed:
        return
    action = row["review_action"]
    if action not in REVIEW_ACTIONS:
        raise SchemaValidationError("review_action must be KEEP or REVISE")
    if action == "KEEP":
        if row["new_value"] != row["previous_value"]:
            raise SchemaValidationError("KEEP requires new_value to equal previous_value")
        if str(row["revision_reason_code"]).strip():
            raise SchemaValidationError("KEEP must not provide a revision reason")
    else:
        if row["new_value"] == row["previous_value"]:
            raise SchemaValidationError("REVISE requires a changed value")
        if row["revision_reason_code"] not in REVISION_REASON_CODES:
            raise SchemaValidationError("REVISE requires an allowed revision reason")


def agreement_subset_rule(field_name: str) -> str:
    """Return the prepared calculation subset without calculating agreement."""

    reverse = {correctness: present for present, correctness in PRESENT_TO_CORRECTNESS.items()}
    if field_name in reverse:
        return f"BOTH_{reverse[field_name].upper()}_YES_ONLY"
    if field_name in PRESENT_TO_CORRECTNESS or field_name in {
        "claim_matches_source",
        "fact_changed",
        "overall_fact_status",
        "language_natural_score",
        "topic_relevance_score",
        "locally_detectable",
        "cross_document_evidence_needed",
        "assigned_stealth_level",
    }:
        return "ALL_SHARED_SAMPLE_IDS"
    return "EXCLUDED_PROCESS_OR_FREE_TEXT"


__all__ = [
    "ApplicabilityCategory",
    "CONDITIONAL_CORRECTNESS_RESPONSES",
    "FORBIDDEN_ANNOTATOR_KEYS",
    "FOUR_VALUE_RESPONSES",
    "ISSUE_FLAGS",
    "LOOKUP_REVIEW_FIELDS",
    "LookupSourceType",
    "OverallFactStatus",
    "PHASE1_V2_FIELDS",
    "PHASE2_V2_FIELDS",
    "PRESENT_RESPONSES",
    "PRESENT_TO_CORRECTNESS",
    "PROCESS_LOOKUP_RESPONSES",
    "RETROSPECTIVE_DECLARATION_FIELDS",
    "REVISION_LOG_FIELDS",
    "REVISION_REASON_CODES",
    "REVIEW_ACTIONS",
    "ResponseMode",
    "TERNARY_RESPONSES",
    "agreement_subset_rule",
    "apply_not_applicable_rules",
    "validate_phase1_v2_row",
    "validate_phase2_v2_row",
    "validate_revision_row",
]
