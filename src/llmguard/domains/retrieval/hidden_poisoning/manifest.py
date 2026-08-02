"""Pilot0 engineering-only Run Manifest contract."""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from pathlib import PurePosixPath
from typing import Mapping, Self

from .schema import SCHEMA_VERSION, CanonicalRecord, SchemaValidationError


_GIT_OBJECT_ID = re.compile(r"^(?:[0-9a-f]{40}|[0-9a-f]{64})$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_UTC = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


class ClaimsClassification(str, Enum):
    ENGINEERING_VALIDATION_ONLY = "ENGINEERING_VALIDATION_ONLY"


@dataclass(frozen=True, slots=True, kw_only=True)
class RunManifest(CanonicalRecord):
    run_id: str
    task_id: str
    run_type: str
    git_commit: str
    working_tree_state: str
    schema_version: str
    fixture_snapshot_hash: str
    split_hash: str
    configuration_hash: str
    seed: int
    start_utc: str
    end_utc: str
    exit_code: int
    result_path: str
    evidence_index: tuple[str, ...]
    claims_classification: ClaimsClassification

    @classmethod
    def from_mapping(cls, payload: Mapping[str, object]) -> Self:
        normalized = dict(payload)
        classification = normalized.get("claims_classification")
        if isinstance(classification, str):
            try:
                normalized["claims_classification"] = ClaimsClassification(classification)
            except ValueError:
                pass
        evidence_index = normalized.get("evidence_index")
        if isinstance(evidence_index, list):
            normalized["evidence_index"] = tuple(evidence_index)
        return CanonicalRecord.from_mapping.__func__(cls, normalized)  # type: ignore[attr-defined]

    def __post_init__(self) -> None:
        if not self.run_id or not self.task_id or not self.run_type:
            raise SchemaValidationError("run identity fields are required")
        if _GIT_OBJECT_ID.fullmatch(self.git_commit) is None:
            raise SchemaValidationError("git_commit must be a full Git object ID")
        for field_name in (
            "fixture_snapshot_hash",
            "split_hash",
            "configuration_hash",
        ):
            if _SHA256.fullmatch(getattr(self, field_name)) is None:
                raise SchemaValidationError(f"{field_name} must be a lowercase SHA256")
        if self.working_tree_state not in {"clean", "dirty"}:
            raise SchemaValidationError("working_tree_state must be clean or dirty")
        if self.schema_version != SCHEMA_VERSION:
            raise SchemaValidationError("unsupported schema_version")
        if _UTC.fullmatch(self.start_utc) is None or _UTC.fullmatch(self.end_utc) is None:
            raise SchemaValidationError("timestamps must use second-resolution UTC")
        if isinstance(self.seed, bool) or not isinstance(self.seed, int):
            raise SchemaValidationError("seed must be an integer")
        path = PurePosixPath(self.result_path)
        if path.is_absolute() or ".." in path.parts or not self.result_path:
            raise SchemaValidationError("result_path must be a safe relative path")
        if not self.evidence_index or any(not item for item in self.evidence_index):
            raise SchemaValidationError("evidence_index must not be empty")
        if self.claims_classification is not ClaimsClassification.ENGINEERING_VALIDATION_ONLY:
            raise SchemaValidationError("FORMAL_RESULT is prohibited for Pilot0")


__all__ = ["ClaimsClassification", "RunManifest"]
