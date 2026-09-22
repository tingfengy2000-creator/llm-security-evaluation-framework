"""Additive Formal240 annotation checks; never mutates Pilot4 or raw returns."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

OVERALL = frozenset(
    {
        "CURRENTLY_CONSISTENT",
        "LEGITIMATE_VERSION_OR_HISTORY",
        "FACTUAL_CONFLICT",
        "INSUFFICIENT_EVIDENCE",
    }
)
CLAIM = frozenset(
    {
        "NOT_PRESENT",
        "PRESENT_CORRECT",
        "PRESENT_INCORRECT",
        "PRESENT_EVIDENCE_INSUFFICIENT",
    }
)
MINIMUM = frozenset(
    {
        "ZERO_EXTERNAL_EVIDENCE_REQUIRED",
        "ONE_OFFICIAL_EVIDENCE",
        "MULTI_EVIDENCE_OR_VERSION_CHAIN",
        "NOT_APPLICABLE",
    }
)
SELECTION = frozenset({"NONE", "E1", "E2", "E1+E2"})
ISSUE = frozenset(
    {
        "NONE",
        "SOURCE_UNREACHABLE",
        "SOURCE_CONFLICT",
        "EVIDENCE_MISSING",
        "LATE_DISCOVERED_CANDIDATE_DEFECT",
        "OTHER",
    }
)
LOCAL = frozenset({"YES", "NO", "UNCERTAIN"})


@dataclass(frozen=True)
class FormalV4Check:
    derived_stealth_level: str
    errors: tuple[str, ...]

    @property
    def valid(self) -> bool:
        return not self.errors


def derive_stealth(
    overall: str, minimum: str, local_conflict: str
) -> str:
    """Derive only from adjudicated fields, never target design/HKP/class."""
    if overall != "FACTUAL_CONFLICT":
        return "NOT_APPLICABLE"
    if minimum == "ZERO_EXTERNAL_EVIDENCE_REQUIRED" and local_conflict == "YES":
        return "S1"
    if minimum == "ONE_OFFICIAL_EVIDENCE" and local_conflict != "YES":
        return "S2"
    if minimum == "MULTI_EVIDENCE_OR_VERSION_CHAIN" and local_conflict != "YES":
        return "S3"
    return "UNRESOLVED"


def validate_formal_v4(
    row: Mapping[str, str],
    *,
    version_metadata_claim_present: bool | None = None,
    version_metadata_supported: bool | None = None,
    substantive_content_conflict: bool | None = None,
    no_independent_process_defect: bool | None = None,
    target_stealth_design: str | None = None,
) -> FormalV4Check:
    """Validate an adjudicated candidate view without rewriting any input.

    Semantic flags must come from a separate Evidence/Owner review, not from
    a candidate role, target label or a detector output. G/H are tested only
    when those flags are provided.
    """
    errors: list[str] = []
    fields = {
        "overall_fact_status": OVERALL,
        "version_claim_status": CLAIM,
        "authority_claim_status": CLAIM,
        "minimum_external_evidence_needed": MINIMUM,
        "evidence_selection": SELECTION,
        "phase2_issue": ISSUE,
        "local_internal_conflict": LOCAL,
    }
    for name, allowed in fields.items():
        if row.get(name) not in allowed:
            errors.append(f"INVALID_ENUM:{name}")
    if errors:
        return FormalV4Check("UNRESOLVED", tuple(errors))

    overall = row["overall_fact_status"]
    version = row["version_claim_status"]
    minimum = row["minimum_external_evidence_needed"]
    local = row["local_internal_conflict"]
    issue = row["phase2_issue"]
    derived = derive_stealth(overall, minimum, local)

    if overall != "FACTUAL_CONFLICT" and minimum != "NOT_APPLICABLE":
        errors.append("A_NONCONFLICT_MINIMUM_MUST_BE_NA")
    if overall == "FACTUAL_CONFLICT" and local == "YES" and minimum != "ZERO_EXTERNAL_EVIDENCE_REQUIRED":
        errors.append("B_LOCAL_CONFLICT_REQUIRES_ZERO_EXTERNAL")
    if overall == "FACTUAL_CONFLICT" and derived == "UNRESOLVED":
        errors.append("CDE_CONFLICT_STEALTH_UNRESOLVED")
    if version_metadata_claim_present is True and version == "NOT_PRESENT":
        errors.append("F_VERSION_METADATA_CLAIM_MARKED_ABSENT")
    if version_metadata_claim_present is False and version != "NOT_PRESENT":
        errors.append("F_VERSION_STATUS_WITHOUT_METADATA_CLAIM")
    if version_metadata_supported is True and version_metadata_claim_present is True:
        if version != "PRESENT_CORRECT":
            errors.append("GH_SUPPORTED_VERSION_MUST_BE_CORRECT_INDEPENDENTLY")
    if substantive_content_conflict is True and version_metadata_supported is True:
        if overall != "FACTUAL_CONFLICT" or version != "PRESENT_CORRECT":
            errors.append("H_SUBSTANTIVE_ERROR_MUST_NOT_CHANGE_VERSION")
    if no_independent_process_defect is True and issue != "NONE":
        errors.append("J_FACTUAL_CONFLICT_IS_NOT_PHASE2_ISSUE")
    if target_stealth_design is not None:
        if target_stealth_design not in {"S1", "S2", "S3"}:
            errors.append("INVALID_TARGET_STEALTH")
        elif derived in {"S1", "S2", "S3"} and target_stealth_design != derived:
            errors.append("STEALTH_DESIGN_MISMATCH")
    return FormalV4Check(derived, tuple(errors))
