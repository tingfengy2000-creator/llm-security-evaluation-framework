from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class SchemaError(ValueError):
    """Raised when an attack-matrix row violates the Stage 5 schema."""


@dataclass(frozen=True)
class AttackSample:
    id: str
    category: str
    variant: str
    risk_goal: str
    prompt: str
    expected_risk_patterns: tuple[str, ...]
    expected_guard: tuple[str, ...]
    severity: str
    notes: str

    REQUIRED_FIELDS = {
        "id",
        "category",
        "variant",
        "risk_goal",
        "prompt",
        "expected_risk_patterns",
        "expected_guard",
        "severity",
        "notes",
    }
    VALID_SEVERITIES = {"low", "medium", "high"}

    @property
    def benign(self) -> bool:
        return self.category == "benign"

    @classmethod
    def from_dict(cls, row: dict[str, Any]) -> "AttackSample":
        missing = cls.REQUIRED_FIELDS - set(row)
        if missing:
            raise SchemaError(f"missing required fields: {sorted(missing)}")
        if row["severity"] not in cls.VALID_SEVERITIES:
            raise SchemaError(f"invalid severity: {row['severity']!r}")
        for field in ("id", "category", "variant", "risk_goal", "prompt", "notes"):
            if not isinstance(row[field], str) or not row[field].strip():
                raise SchemaError(f"{field} must be a non-empty string")
        for field in ("expected_risk_patterns", "expected_guard"):
            value = row[field]
            if not isinstance(value, list) or not all(
                isinstance(item, str) and item for item in value
            ):
                raise SchemaError(f"{field} must be a list of non-empty strings")
        return cls(
            id=row["id"],
            category=row["category"],
            variant=row["variant"],
            risk_goal=row["risk_goal"],
            prompt=row["prompt"],
            expected_risk_patterns=tuple(row["expected_risk_patterns"]),
            expected_guard=tuple(row["expected_guard"]),
            severity=row["severity"],
            notes=row["notes"],
        )
