from __future__ import annotations

from dataclasses import dataclass
from typing import Any


ATTACK_LAYER_MAP = {
    "A1": "Training",
    "A2": "Training",
    "A3": "Retrieval",
    "A4": "Runtime",
    "A5": "Runtime",
    "A6": "Runtime",
    "B0": "Benign",
}


class SchemaError(ValueError):
    """Raised when a Stage 5 Paper dataset row is invalid."""


@dataclass(frozen=True)
class AttackSample:
    schema_version: str
    sample_id: str
    attack_id: str
    threat_layer: str
    attack_family: str
    variant: str
    risk_goal: str
    prompt: str
    expected_risk_patterns: tuple[str, ...]
    expected_guard_rules: tuple[str, ...]
    official_detector_names: tuple[str, ...]
    severity: str
    evidence_scope: str
    tool_execution_allowed: bool
    notes: str

    REQUIRED_FIELDS = {
        "schema_version",
        "sample_id",
        "attack_id",
        "threat_layer",
        "attack_family",
        "variant",
        "risk_goal",
        "prompt",
        "expected_risk_patterns",
        "expected_guard_rules",
        "official_detector_names",
        "severity",
        "evidence_scope",
        "tool_execution_allowed",
        "notes",
    }

    @property
    def benign(self) -> bool:
        return self.attack_id == "B0"

    @classmethod
    def from_dict(cls, row: dict[str, Any]) -> "AttackSample":
        missing = cls.REQUIRED_FIELDS - set(row)
        if missing:
            raise SchemaError(f"missing required fields: {sorted(missing)}")
        attack_id = row["attack_id"]
        if attack_id not in ATTACK_LAYER_MAP:
            raise SchemaError(f"unsupported attack_id: {attack_id}")
        if row["threat_layer"] != ATTACK_LAYER_MAP[attack_id]:
            raise SchemaError(
                f"{attack_id} requires threat_layer={ATTACK_LAYER_MAP[attack_id]}"
            )
        if row["severity"] not in {"low", "medium", "high"}:
            raise SchemaError(f"invalid severity: {row['severity']}")
        if not isinstance(row["tool_execution_allowed"], bool):
            raise SchemaError("tool_execution_allowed must be boolean")
        if attack_id == "A6" and row["tool_execution_allowed"]:
            raise SchemaError("A6 tool execution must remain disabled")
        if attack_id in {"A1", "A2"} and row["evidence_scope"] != "manifestation_simulation":
            raise SchemaError(f"{attack_id} requires manifestation_simulation scope")
        for field in (
            "schema_version",
            "sample_id",
            "attack_family",
            "variant",
            "risk_goal",
            "prompt",
            "evidence_scope",
            "notes",
        ):
            if not isinstance(row[field], str) or not row[field].strip():
                raise SchemaError(f"{field} must be a non-empty string")
        for field in (
            "expected_risk_patterns",
            "expected_guard_rules",
            "official_detector_names",
        ):
            if not isinstance(row[field], list) or not all(
                isinstance(value, str) and value for value in row[field]
            ):
                raise SchemaError(f"{field} must be a list of non-empty strings")
        return cls(
            schema_version=row["schema_version"],
            sample_id=row["sample_id"],
            attack_id=attack_id,
            threat_layer=row["threat_layer"],
            attack_family=row["attack_family"],
            variant=row["variant"],
            risk_goal=row["risk_goal"],
            prompt=row["prompt"],
            expected_risk_patterns=tuple(row["expected_risk_patterns"]),
            expected_guard_rules=tuple(row["expected_guard_rules"]),
            official_detector_names=tuple(row["official_detector_names"]),
            severity=row["severity"],
            evidence_scope=row["evidence_scope"],
            tool_execution_allowed=row["tool_execution_allowed"],
            notes=row["notes"],
        )
