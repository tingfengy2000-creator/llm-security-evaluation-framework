"""Contracts for the Pilot2 annotator-friendly targeted re-review.

The targeted view narrows human work without changing the immutable Round1
returns or the complete Annotation Schema V2 package.  It intentionally does
not calculate agreement or adjudicate labels.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum

from .annotation_v2 import FORBIDDEN_ANNOTATOR_KEYS
from .schema import SchemaValidationError


class FieldRereviewDecision(str, Enum):
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    READ_ONLY_PRESERVE = "READ_ONLY_PRESERVE"
    PROCESS_FIX_ONLY = "PROCESS_FIX_ONLY"
    NOT_RELEVANT_TO_CURRENT_REMEDIATION = "NOT_RELEVANT_TO_CURRENT_REMEDIATION"


@dataclass(frozen=True)
class FieldAuditRecord:
    phase: str
    field_name: str
    decision: FieldRereviewDecision
    issue_type: tuple[str, ...]
    evidence: tuple[str, ...]
    why_rereview_needed: str
    all_36_rows_required: bool
    only_invalid_or_missing_rows_required: bool
    dependent_applicability_field: str | None
    annotators: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        value = asdict(self)
        value["decision"] = self.decision.value
        return value


TARGETED_PHASE1_FIELDS = (
    "locally_detectable",
    "cross_document_evidence_needed",
    "assigned_stealth_level",
)

TARGETED_PHASE2_FIELDS = (
    "version_relation_present",
    "version_relation_correct",
    "history_or_update_claim_present",
    "legitimate_update_or_history",
    "authority_claim_present",
    "authority_matches",
    "overall_fact_status",
)

PROCESS_FIX_COUNTS = {
    "A": {"professional_lookup_used": 0, "lookup_source_type": 0},
    "B": {"professional_lookup_used": 21, "lookup_source_type": 1},
}

TARGETED_VALUE_ENUMS = {
    "locally_detectable": ("YES", "NO", "UNCERTAIN"),
    "cross_document_evidence_needed": ("YES", "NO", "UNCERTAIN"),
    "assigned_stealth_level": ("S1", "S2", "S3", "NOT_APPLICABLE", "UNCERTAIN"),
    "version_relation_present": ("YES", "NO"),
    "version_relation_correct": ("YES", "NO", "UNCERTAIN", "NOT_APPLICABLE"),
    "history_or_update_claim_present": ("YES", "NO"),
    "legitimate_update_or_history": ("YES", "NO", "UNCERTAIN", "NOT_APPLICABLE"),
    "authority_claim_present": ("YES", "NO"),
    "authority_matches": ("YES", "NO", "UNCERTAIN", "NOT_APPLICABLE"),
    "overall_fact_status": (
        "CURRENTLY_CONSISTENT",
        "LEGITIMATE_VERSION_OR_HISTORY",
        "FACTUAL_CONFLICT",
        "INSUFFICIENT_EVIDENCE",
    ),
    "professional_lookup_used": ("YES", "NO", "MISSING_NOT_RECOVERABLE"),
    "lookup_source_type": (
        "OFFICIAL_PRIMARY_SOURCE",
        "OFFICIAL_REPOST",
        "SEARCH_ENGINE",
        "SECONDARY_REFERENCE",
        "AI_ASSISTED_EXPLANATION",
        "OTHER",
    ),
}


def workload_summary(sample_count: int = 36) -> dict[str, object]:
    substantive_fields = len(TARGETED_PHASE1_FIELDS) + len(TARGETED_PHASE2_FIELDS)
    substantive_tasks = substantive_fields * sample_count
    full_v2_substantive_fields = 16
    full_v2_substantive_tasks = full_v2_substantive_fields * sample_count
    return {
        "sample_count_per_phase": sample_count,
        "targeted_substantive_fields": substantive_fields,
        "targeted_substantive_tasks_per_annotator": substantive_tasks,
        "full_v2_substantive_fields": full_v2_substantive_fields,
        "full_v2_substantive_tasks_per_annotator": full_v2_substantive_tasks,
        "substantive_tasks_saved_per_annotator": full_v2_substantive_tasks - substantive_tasks,
        "substantive_reduction_percent": 37.5,
        "A_total_tasks_including_process_fixes": substantive_tasks,
        "B_total_tasks_including_process_fixes": substantive_tasks + 22,
        "one_time_declarations_per_annotator": 2,
    }


def validate_targeted_task_row(row: dict[str, str], *, completed: bool) -> None:
    leaked = FORBIDDEN_ANNOTATOR_KEYS & set(row)
    if leaked:
        raise SchemaValidationError(f"targeted row leaks evaluator-only fields: {sorted(leaked)}")
    required = {
        "task_id",
        "task_type",
        "sample_id",
        "field_name",
        "candidate",
        "v1_value",
        "new_value",
        "review_action",
        "revision_reason_code",
        "revision_reason_short",
        "rereview_time_seconds",
    }
    missing = required - set(row)
    if missing:
        raise SchemaValidationError(f"targeted row is missing columns: {sorted(missing)}")
    field = row["field_name"]
    if field not in TARGETED_VALUE_ENUMS:
        raise SchemaValidationError(f"unsupported targeted field: {field}")
    if not completed:
        return
    if row["new_value"] not in TARGETED_VALUE_ENUMS[field]:
        raise SchemaValidationError(f"unsupported value for {field}: {row['new_value']}")
    expected_action = "KEEP" if row["new_value"] == row["v1_value"] else "REVISE"
    if row["review_action"] != expected_action:
        raise SchemaValidationError("review_action must be derived from V1 and V2 values")
    if not row["revision_reason_short"].strip():
        raise SchemaValidationError("revision_reason_short is required")
    try:
        seconds = int(row["rereview_time_seconds"])
    except ValueError as error:
        raise SchemaValidationError("rereview_time_seconds must be an integer") from error
    if seconds < 0:
        raise SchemaValidationError("rereview_time_seconds cannot be negative")


__all__ = [
    "FieldAuditRecord",
    "FieldRereviewDecision",
    "PROCESS_FIX_COUNTS",
    "TARGETED_PHASE1_FIELDS",
    "TARGETED_PHASE2_FIELDS",
    "TARGETED_VALUE_ENUMS",
    "validate_targeted_task_row",
    "workload_summary",
]
