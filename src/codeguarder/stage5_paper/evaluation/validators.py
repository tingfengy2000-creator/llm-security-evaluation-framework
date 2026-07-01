from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    message: str
    sample_id: str | None = None
    attempt_id: str | None = None


def validate_prompt_hash_parity(
    records: Iterable[Mapping[str, Any]],
) -> list[ValidationIssue]:
    grouped = defaultdict(list)
    for record in records:
        grouped[str(record.get("sample_id"))].append(record)
    issues = []
    for sample_id, group in grouped.items():
        codes = {record.get("guard_code") for record in group}
        hashes = {record.get("prompt_hash") for record in group}
        if codes != {"P", "I", "O", "F"} or len(hashes) != 1 or None in hashes:
            issues.append(
                ValidationIssue(
                    "prompt_hash_parity",
                    "P/I/O/F must share one non-null prompt hash",
                    sample_id,
                )
            )
    return issues


def validate_output_only(
    records: Iterable[Mapping[str, Any]],
) -> list[ValidationIssue]:
    issues = []
    for record in records:
        if record.get("guard_code") != "O":
            continue
        sample_id = str(record.get("sample_id"))
        checks = (
            ("output_only_input_guard", record.get("input_guard_enabled") is False),
            ("output_only_output_guard", record.get("output_guard_enabled") is True),
            ("output_only_input_block", record.get("input_blocked") is False),
            ("output_only_upstream", record.get("upstream_called") is True),
            ("output_only_raw_hash", bool(record.get("raw_model_output_hash"))),
        )
        for code, valid in checks:
            if not valid:
                issues.append(ValidationIssue(code, "output-only invariant failed", sample_id))
    return issues
