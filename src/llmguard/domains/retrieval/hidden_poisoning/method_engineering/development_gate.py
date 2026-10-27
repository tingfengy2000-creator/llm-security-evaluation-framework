"""Fail-closed checks for unsigned development QA and materialized features.

These checks do not create labels, approve a dataset, fit a model or score it.
An Owner signature receipt is a separately ingested control-plane artifact.
"""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence

from ..external_blind_review import PHASE1_RETURN_ENUMS
from ..formal_annotation_v4 import CLAIM, ISSUE, LOCAL, MINIMUM, OVERALL, SELECTION

_FIELD_ENUMS = {
    **PHASE1_RETURN_ENUMS,
    "overall_fact_status": OVERALL,
    "version_claim_status": CLAIM,
    "authority_claim_status": CLAIM,
    "minimum_external_evidence_needed": MINIMUM,
    "evidence_selection": SELECTION,
    "phase2_issue": ISSUE,
    "local_internal_conflict": LOCAL,
    "evidence_sufficiency": frozenset({"SUFFICIENT", "INSUFFICIENT", "UNCERTAIN"}),
}

_FORBIDDEN_FEATURES = frozenset(
    {
        "candidate_id", "sample_id", "group_id", "family", "family_cluster",
        "label", "target", "true_class", "hkp", "target_s", "derived_s",
        "evidence_selection", "expected", "owner", "annotator", "path",
    }
)


def validate_recommendation_pairs(
    rows: Sequence[Mapping[str, object]],
) -> tuple[int, int]:
    """Check identity, uniqueness and frozen enums without assigning null fields."""
    seen: set[tuple[str, str]] = set()
    nonnull = 0
    for row in rows:
        sample_id, field = row.get("candidate_id"), row.get("field")
        if not isinstance(sample_id, str) or not isinstance(field, str):
            raise ValueError("recommendation identity missing")
        pair = (sample_id, field)
        if pair in seen:
            raise ValueError("duplicate candidate/field")
        seen.add(pair)
        value = row.get("AI_suggestion")
        allowed = _FIELD_ENUMS.get(field)
        if allowed is None:
            raise ValueError("unknown recommendation field")
        if value is not None:
            if value not in allowed:
                raise ValueError("illegal frozen enum")
            nonnull += 1
    return nonnull, len(rows) - nonnull


def validate_numeric_features(
    values: Mapping[str, object], names: Sequence[str]
) -> None:
    """Only frozen numeric/null feature columns enter the model-facing view."""
    if len(names) != len(set(names)) or set(names) & _FORBIDDEN_FEATURES:
        raise ValueError("feature-name leakage or duplication")
    if list(values) != list(names):
        raise ValueError("frozen feature order mismatch")
    for value in values.values():
        if value is not None and (
            not isinstance(value, (int, float)) or not math.isfinite(float(value))
        ):
            raise ValueError("nonfinite or nonnumeric feature")


def require_owner_signature(
    receipt: Mapping[str, object] | None, *, eligibility_sha256: str
) -> None:
    """Runtime installation approval and AI suggestions are not dataset signatures."""
    if receipt is None:
        raise PermissionError("D1_DATA_QUALITY_GATE_PENDING")
    if (
        receipt.get("eligibility_sha256") != eligibility_sha256
        or receipt.get("owner_signed") is not True
        or receipt.get("scope") != "D1_DEV_ONLY"
        or not receipt.get("owner_name")
        or not receipt.get("signed_date")
        or receipt.get("whole_group_holds_retained") is not True
        or receipt.get("applicable_QA_overlay_confirmed") is not True
    ):
        raise PermissionError("incomplete or wrong-scope Owner signature")


def all_fold_statistics_observed(
    rows: Sequence[Mapping[str, float | None]],
    families: Sequence[str],
    names: Sequence[str],
) -> dict[str, tuple[str, ...]]:
    """Preflight only: report null-only training columns in each family holdout.

    No imputer/scaler is fit. The held-out family's values cannot rescue a
    missing training-fold statistic. Unknown/N/A values remain null.
    """
    if len(rows) != len(families) or not rows:
        raise ValueError("rows and families must be nonempty and aligned")
    return {
        family: tuple(
            name for name in names
            if not any(
                row[name] is not None
                for row, other in zip(rows, families, strict=True)
                if other != family
            )
        )
        for family in sorted(set(families))
    }
