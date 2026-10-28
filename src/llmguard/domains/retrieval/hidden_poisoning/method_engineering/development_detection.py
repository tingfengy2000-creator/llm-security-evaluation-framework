"""Small, fixed family-isolated development detector utilities.

No file access, feature extraction, label invention or parameter search occurs
here. Numeric types follow the frozen extractor contract, never label effects.
"""

from __future__ import annotations

import math
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

BINARY_FEATURES = frozenset({
    "claimed_authority_match", "condition_conflict", "date_conflict",
    "document_identity_match", "entity_conflict", "exception_conflict",
    "negation_flip", "numeric_conflict", "official_repost", "official_source",
    "predicate_match", "relation_conflict", "subject_match", "version_identity_match",
})
TEMPORAL_FEATURES = frozenset({
    "current_fact_match", "historical_fact_match", "present_time_substitution_signal",
})


@dataclass(frozen=True)
class FamilyFold:
    family: str
    train: tuple[int, ...]
    validation: tuple[int, ...]


def family_folds(families: Sequence[str], groups: Sequence[str]) -> tuple[FamilyFold, ...]:
    """An entire fact family, including all its complete groups, is held out."""
    if not families or len(families) != len(groups):
        raise ValueError("nonempty aligned family/group arrays required")
    by_group: dict[str, set[str]] = {}
    for family, group in zip(families, groups, strict=True):
        by_group.setdefault(group, set()).add(family)
    if any(len(value) != 1 for value in by_group.values()):
        raise ValueError("one group cannot span multiple families")
    if len(set(families)) < 2:
        raise ValueError("at least two fact families required")
    folds = tuple(
        FamilyFold(
            family,
            tuple(i for i, other in enumerate(families) if other != family),
            tuple(i for i, other in enumerate(families) if other == family),
        )
        for family in sorted(set(families))
    )
    if Counter(i for fold in folds for i in fold.validation) != Counter(range(len(families))):
        raise ValueError("each candidate must be held out exactly once")
    return folds


def numeric_fold_preflight(
    rows: Sequence[Mapping[str, float | None]], names: Sequence[str],
    folds: Sequence[FamilyFold],
) -> dict[str, tuple[str, ...]]:
    """Null-only train columns block the condition; validation cannot rescue it."""
    if not names or len(names) != len(set(names)):
        raise ValueError("unique frozen feature names required")
    for row in rows:
        if list(row) != list(names):
            raise ValueError("feature-order mismatch")
        for value in row.values():
            if value is not None and not math.isfinite(value):
                raise ValueError("nonfinite feature")
    return {
        fold.family: tuple(
            name for name in names
            if not any(rows[i][name] is not None for i in fold.train)
        )
        for fold in folds
    }


def wilson_interval(tp: int, n: int, z: float = 1.959963984540054) -> tuple[float, float] | None:
    """Descriptive binomial interval; family-bootstrap is reported separately."""
    if n == 0:
        return None
    if not 0 <= tp <= n:
        raise ValueError("invalid numerator/denominator")
    p = tp / n
    divisor = 1 + z * z / n
    center = (p + z * z / (2 * n)) / divisor
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / divisor
    return max(0.0, center - half), min(1.0, center + half)


def poison_counts(
    labels: Sequence[int], probabilities: Sequence[float], mask: Sequence[bool],
    threshold: float = 0.5,
) -> tuple[int, int, float | None]:
    """Use the fixed threshold; zero positives means unavailable, not zero recall."""
    if len(labels) != len(probabilities) or len(labels) != len(mask):
        raise ValueError("aligned evaluation arrays required")
    n = sum(y == 1 and keep for y, keep in zip(labels, mask, strict=True))
    tp = sum(
        y == 1 and keep and probability >= threshold
        for y, probability, keep in zip(labels, probabilities, mask, strict=True)
    )
    return tp, n, tp / n if n else None
