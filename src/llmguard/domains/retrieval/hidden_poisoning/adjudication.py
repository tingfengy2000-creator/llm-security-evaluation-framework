"""Owner-adjudication validation contracts for the Pilot2 closure gate.

The validator reads row mappings derived from the immutable owner workbook.  It
never changes an owner value and deliberately stops before Ground Truth
construction when one field has an invalid or conflicting final decision.
"""

from __future__ import annotations

import re
from collections import defaultdict
from collections.abc import Mapping, Sequence
from dataclasses import dataclass


OWNER_FIELD_ENUMS: Mapping[str, frozenset[str]] = {
    "locally_detectable": frozenset({"YES", "NO", "UNCERTAIN"}),
    "cross_document_evidence_needed": frozenset({"YES", "NO", "UNCERTAIN"}),
    "assigned_stealth_level": frozenset(
        {"S1", "S2", "S3", "NOT_APPLICABLE", "UNCERTAIN"}
    ),
    "version_relation_present": frozenset({"YES", "NO"}),
    "version_relation_correct": frozenset(
        {"YES", "NO", "UNCERTAIN", "NOT_APPLICABLE"}
    ),
    "history_or_update_claim_present": frozenset({"YES", "NO"}),
    "legitimate_update_or_history": frozenset(
        {"YES", "NO", "UNCERTAIN", "NOT_APPLICABLE"}
    ),
    "authority_claim_present": frozenset({"YES", "NO"}),
    "authority_matches": frozenset({"YES", "NO", "UNCERTAIN", "NOT_APPLICABLE"}),
    "overall_fact_status": frozenset(
        {
            "CURRENTLY_CONSISTENT",
            "LEGITIMATE_VERSION_OR_HISTORY",
            "FACTUAL_CONFLICT",
            "INSUFFICIENT_EVIDENCE",
        }
    ),
}

_FIELD_ALIASES: Mapping[str, tuple[str, ...]] = {
    "locally_detectable": ("locally_detectable",),
    "cross_document_evidence_needed": (
        "cross_document_evidence_needed",
        "cross_document",
    ),
    "assigned_stealth_level": ("assigned_stealth_level", "stealth"),
    "version_relation_present": ("version_relation_present",),
    "version_relation_correct": ("version_relation_correct",),
    "history_or_update_claim_present": ("history_or_update_claim_present",),
    "legitimate_update_or_history": ("legitimate_update_or_history",),
    "authority_claim_present": ("authority_claim_present",),
    "authority_matches": ("authority_matches",),
    "overall_fact_status": ("overall_fact_status", "overall"),
}


@dataclass(frozen=True, slots=True)
class OwnerAdjudicationProblem:
    problem_type: str
    canonical_candidate_id: str
    issue_ids: tuple[str, ...]
    field: str
    observed_value: str
    detail: str


@dataclass(frozen=True, slots=True)
class OwnerAdjudicationValidation:
    issue_count: int
    candidate_count: int
    pending_count: int
    problems: tuple[OwnerAdjudicationProblem, ...]

    @property
    def passed(self) -> bool:
        return self.pending_count == 0 and not self.problems


@dataclass(frozen=True, slots=True)
class OwnerCorrection:
    """Owner-authored overlay that preserves, but supersedes, workbook evidence."""

    canonical_candidate_id: str
    field: str
    final_value: str
    authority: str = "PROJECT_REQUIREMENTS_OWNER"


def _required(row: Mapping[str, object], key: str) -> str:
    value = str(row.get(key, "")).strip()
    return value


def _extract_composite_value(field: str, text: str) -> str | None:
    allowed = sorted(OWNER_FIELD_ENUMS[field], key=len, reverse=True)
    aliases = _FIELD_ALIASES[field]
    value_pattern = "|".join(re.escape(value) for value in allowed)
    alias_pattern = "|".join(re.escape(alias) for alias in aliases)
    pattern = re.compile(
        rf"(?:{alias_pattern})\s*(?:==|=|-|but)?\s*({value_pattern})(?![A-Z0-9_])"
    )
    values = set(pattern.findall(text))
    if len(values) != 1:
        return None
    return next(iter(values))


def validate_owner_adjudication_rows(
    issue_rows: Sequence[Mapping[str, object]],
    candidate_rows: Sequence[Mapping[str, object]],
    corrections: Sequence[OwnerCorrection] = (),
) -> OwnerAdjudicationValidation:
    """Validate completion, enums and cross-row owner-decision uniqueness."""

    problems: list[OwnerAdjudicationProblem] = []
    decisions: dict[tuple[str, str], list[tuple[str, str]]] = defaultdict(list)
    pending_count = 0
    correction_map: dict[tuple[str, str], OwnerCorrection] = {}
    for owner_correction in corrections:
        key = (owner_correction.canonical_candidate_id, owner_correction.field)
        if owner_correction.field not in OWNER_FIELD_ENUMS:
            raise ValueError(f"unknown corrected field: {owner_correction.field}")
        if owner_correction.final_value not in OWNER_FIELD_ENUMS[owner_correction.field]:
            raise ValueError(
                f"invalid corrected value for {owner_correction.field}: {owner_correction.final_value}"
            )
        if key in correction_map and correction_map[key] != owner_correction:
            raise ValueError(f"conflicting owner corrections for {key}")
        correction_map[key] = owner_correction

    for row in issue_rows:
        issue_id = _required(row, "issue_id")
        candidate_id = _required(row, "canonical_candidate_id")
        disagreement_field = _required(row, "disagreement_field")
        owner_final = _required(row, "owner_final_value")
        owner_rationale = _required(row, "owner_rationale")
        inclusion = _required(row, "benchmark_inclusion_decision")
        if not owner_final or not owner_rationale or not inclusion or "PENDING" in owner_final:
            pending_count += 1
            continue

        expected_fields = tuple(part.strip() for part in disagreement_field.split("+"))
        for field in expected_fields:
            if field not in OWNER_FIELD_ENUMS:
                problems.append(
                    OwnerAdjudicationProblem(
                        problem_type="UNKNOWN_FIELD",
                        canonical_candidate_id=candidate_id,
                        issue_ids=(issue_id,),
                        field=field,
                        observed_value=owner_final,
                        detail="field is outside the frozen ten-field owner schema",
                    )
                )
                continue
            field_correction = correction_map.get((candidate_id, field))
            if field_correction is not None:
                decisions[(candidate_id, field)].append(
                    (f"OWNER_CORRECTION:{issue_id}", field_correction.final_value)
                )
                continue
            if len(expected_fields) == 1:
                value = owner_final if owner_final in OWNER_FIELD_ENUMS[field] else None
            else:
                value = _extract_composite_value(field, owner_final)
            if value is None:
                problems.append(
                    OwnerAdjudicationProblem(
                        problem_type="OWNER_FINAL_VALUE_INVALID",
                        canonical_candidate_id=candidate_id,
                        issue_ids=(issue_id,),
                        field=field,
                        observed_value=owner_final,
                        detail="owner value is not an executable member of the field enum",
                    )
                )
                continue
            decisions[(candidate_id, field)].append((issue_id, value))

    for row in candidate_rows:
        if (
            _required(row, "owner_resolution_status") != "RESOLVED"
            or not _required(row, "benchmark_inclusion_decision")
        ):
            pending_count += 1

    for (candidate_id, field), values in sorted(decisions.items()):
        field_correction = correction_map.get((candidate_id, field))
        if field_correction is not None:
            values = [("OWNER_CORRECTION", field_correction.final_value)]
        unique_values = {value for _, value in values}
        if len(unique_values) <= 1:
            continue
        problems.append(
            OwnerAdjudicationProblem(
                problem_type="CONFLICTING_OWNER_DECISIONS",
                canonical_candidate_id=candidate_id,
                issue_ids=tuple(issue_id for issue_id, _ in values),
                field=field,
                observed_value=" | ".join(
                    f"{issue_id}={value}" for issue_id, value in values
                ),
                detail="one candidate field has more than one owner final value",
            )
        )

    return OwnerAdjudicationValidation(
        issue_count=len(issue_rows),
        candidate_count=len(candidate_rows),
        pending_count=pending_count,
        problems=tuple(problems),
    )


__all__ = [
    "OWNER_FIELD_ENUMS",
    "OwnerAdjudicationProblem",
    "OwnerAdjudicationValidation",
    "OwnerCorrection",
    "validate_owner_adjudication_rows",
]
