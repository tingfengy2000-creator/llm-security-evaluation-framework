"""Hard-negative taxonomy coverage helpers."""

from __future__ import annotations

from collections import Counter
from typing import Iterable

from .schema import HardNegativeType, SchemaValidationError


def hard_negative_coverage(
    hard_negatives: Iterable[HardNegativeType],
) -> dict[HardNegativeType, int]:
    counts = Counter(hard_negatives)
    return {kind: counts[kind] for kind in HardNegativeType}


def validate_hard_negative_coverage(
    hard_negatives: Iterable[HardNegativeType], *, require_all_types: bool = True
) -> dict[HardNegativeType, int]:
    coverage = hard_negative_coverage(hard_negatives)
    if require_all_types:
        missing = [kind.value for kind, count in coverage.items() if count == 0]
        if missing:
            raise SchemaValidationError(f"HARD_NEGATIVE_COVERAGE_BLOCKER: {missing}")
    return coverage


__all__ = ["hard_negative_coverage", "validate_hard_negative_coverage"]
