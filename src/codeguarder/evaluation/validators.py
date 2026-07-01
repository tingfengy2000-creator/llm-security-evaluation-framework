from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any


GUARD_MODES = {"passthrough", "input-only", "output-only", "full-guard"}


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    message: str
    sample_id: str | None = None


def validate_prompt_hash_parity(
    records: Iterable[Mapping[str, Any]],
) -> list[ValidationIssue]:
    grouped: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for record in records:
        grouped[str(record.get("sample_id"))].append(record)
    issues = []
    for sample_id, group in grouped.items():
        modes = {record.get("guard_mode") for record in group}
        hashes = {record.get("prompt_hash") for record in group}
        if modes != GUARD_MODES or len(hashes) != 1 or None in hashes:
            issues.append(
                ValidationIssue(
                    "prompt_hash_parity",
                    f"expected four modes with one prompt hash; got modes={sorted(modes)}",
                    sample_id,
                )
            )
    return issues


def validate_raw_output_hash_parity(
    records: Iterable[Mapping[str, Any]],
) -> list[ValidationIssue]:
    grouped: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for record in records:
        if record.get("upstream_called"):
            grouped[str(record.get("sample_id"))].append(record)
    issues = []
    for sample_id, group in grouped.items():
        hashes = {record.get("raw_model_output_hash") for record in group}
        if None in hashes or len(hashes) > 1:
            issues.append(
                ValidationIssue(
                    "raw_output_hash_parity",
                    f"upstream-called modes produced {len(hashes)} raw hashes",
                    sample_id,
                )
            )
    return issues


def validate_output_only(
    records: Iterable[Mapping[str, Any]],
) -> list[ValidationIssue]:
    issues = []
    for record in records:
        if record.get("guard_mode") != "output-only":
            continue
        sample_id = str(record.get("sample_id"))
        if record.get("input_guard_enabled") is not False:
            issues.append(ValidationIssue("output_only_input_guard", "input guard must be disabled", sample_id))
        if record.get("output_guard_enabled") is not True:
            issues.append(ValidationIssue("output_only_output_guard", "output guard must be enabled", sample_id))
        if record.get("upstream_called") is not True:
            issues.append(ValidationIssue("output_only_upstream", "upstream must be called", sample_id))
        if record.get("input_blocked") is not False:
            issues.append(ValidationIssue("output_only_input_block", "input must not be blocked", sample_id))
        if not record.get("raw_model_output_hash"):
            issues.append(ValidationIssue("output_only_raw_hash", "raw output hash is required", sample_id))
    return issues


def validate_no_secret_leak(paths: Iterable[Path]) -> list[ValidationIssue]:
    markers = ("groq_api_key", "openai_api_key", "gsk_", "sk-", "bearer")
    issues = []
    for path in paths:
        if not path.is_file():
            continue
        content = path.read_text(encoding="utf-8", errors="replace").lower()
        if any(marker in content for marker in markers):
            issues.append(ValidationIssue("secret_leak", f"credential marker found in {path}"))
    return issues


def validate_report_integrity(
    records: Iterable[Mapping[str, Any]], expected_sample_ids: set[str]
) -> list[ValidationIssue]:
    grouped: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for record in records:
        grouped[str(record.get("sample_id"))].append(record)
    issues = []
    for sample_id in sorted(expected_sample_ids):
        group = grouped.get(sample_id, [])
        modes = {record.get("guard_mode") for record in group}
        complete = modes == GUARD_MODES and all(
            "failure_types" in record and bool(record.get("prompt_hash"))
            for record in group
        )
        if not complete:
            issues.append(
                ValidationIssue(
                    "report_integrity",
                    f"incomplete modes or fields: {sorted(modes)}",
                    sample_id,
                )
            )
    unexpected = set(grouped) - expected_sample_ids
    for sample_id in sorted(unexpected):
        issues.append(ValidationIssue("report_integrity", "unexpected sample", sample_id))
    return issues
