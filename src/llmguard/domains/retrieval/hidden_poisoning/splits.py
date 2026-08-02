"""Deterministic configurable group-aware splitting."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from enum import Enum
from typing import Mapping

from .schema import LeakageBlocker, SchemaValidationError, canonical_sha256


class SplitName(str, Enum):
    TRAIN = "train"
    DEV = "dev"
    TEST = "test"


@dataclass(frozen=True, slots=True, kw_only=True)
class SplitConfig:
    train_ratio: float = 0.70
    dev_ratio: float = 0.15
    test_ratio: float = 0.15
    seed: int = 0

    def __post_init__(self) -> None:
        ratios = (self.train_ratio, self.dev_ratio, self.test_ratio)
        if any(value <= 0.0 for value in ratios) or abs(sum(ratios) - 1.0) > 1e-12:
            raise SchemaValidationError("split ratios must be positive and sum to one")
        if isinstance(self.seed, bool) or not isinstance(self.seed, int):
            raise SchemaValidationError("seed must be an integer")


@dataclass(frozen=True, slots=True, kw_only=True)
class SplitAssignment:
    record_id: str
    independence_group_id: str
    split: SplitName


def deterministic_group_split(
    groups_by_record: Mapping[str, str], *, config: SplitConfig
) -> tuple[SplitAssignment, ...]:
    if not groups_by_record:
        raise SchemaValidationError("groups_by_record must not be empty")
    group_splits: dict[str, SplitName] = {}
    train_boundary = config.train_ratio
    dev_boundary = train_boundary + config.dev_ratio
    for group_id in sorted(set(groups_by_record.values())):
        digest = hashlib.sha256(f"{config.seed}:{group_id}".encode()).digest()
        fraction = int.from_bytes(digest[:8], "big") / float(2**64)
        if fraction < train_boundary:
            split = SplitName.TRAIN
        elif fraction < dev_boundary:
            split = SplitName.DEV
        else:
            split = SplitName.TEST
        group_splits[group_id] = split
    assignments = tuple(
        SplitAssignment(
            record_id=record_id,
            independence_group_id=groups_by_record[record_id],
            split=group_splits[groups_by_record[record_id]],
        )
        for record_id in sorted(groups_by_record)
    )
    validate_group_split(assignments)
    return assignments


def validate_group_split(assignments: tuple[SplitAssignment, ...]) -> None:
    seen: dict[str, SplitName] = {}
    for assignment in assignments:
        previous = seen.setdefault(assignment.independence_group_id, assignment.split)
        if previous is not assignment.split:
            raise LeakageBlocker("CROSS_SPLIT_GROUP_LEAKAGE_BLOCKER")


def split_assignment_hash(assignments: tuple[SplitAssignment, ...]) -> str:
    return canonical_sha256(
        [
            {
                "record_id": item.record_id,
                "independence_group_id": item.independence_group_id,
                "split": item.split.value,
            }
            for item in sorted(assignments, key=lambda item: item.record_id)
        ]
    )


__all__ = [
    "SplitAssignment",
    "SplitConfig",
    "SplitName",
    "deterministic_group_split",
    "split_assignment_hash",
    "validate_group_split",
]
