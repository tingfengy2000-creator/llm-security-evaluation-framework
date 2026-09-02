"""Lock first/final Pilot4 Phase2 returns before expected-contract access."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from llmguard.domains.retrieval.hidden_poisoning.external_blind_review import (
    PHASE2_FIELDS,
    lock_phase2_raw_return,
    validate_phase2_packet_rows,
    validate_phase2_raw_return,
)


TASK_ID = (
    "PILOT4-PHASE2-FINAL-RETURN-LOCK-EXPECTED-COMPARISON-AND-PROTOCOL-ACCEPTANCE-01"
)
FIRST_RAW_SHA256 = "d7aed1b2cdf0f7740404c527466d13507e6e06d9b4c34424d279a7c6ee88f6cd"
FIRST_RAW_SIZE = 15985
FINAL_RAW_SHA256 = "6f6cc042bd3f85a42ae5bf4f425df9c994eae1d230a13caf0e0a625de04792f1"
FINAL_RAW_SIZE = 16321
FIRST_LOCKED_FILENAME = (
    "PILOT4_EXTERNAL_BLIND_PHASE2_ATTEMPT2_RETURN_INTERMEDIATE_ACCESS_LIMITED.csv"
)
FINAL_LOCKED_FILENAME = "PILOT4_EXTERNAL_BLIND_PHASE2_ATTEMPT2_RETURN_FINAL.csv"

FINAL_EXPECTED_COUNTS: Mapping[str, Mapping[str, int]] = {
    "overall_fact_status_counts": {
        "CURRENTLY_CONSISTENT": 23,
        "LEGITIMATE_VERSION_OR_HISTORY": 24,
        "FACTUAL_CONFLICT": 24,
        "INSUFFICIENT_EVIDENCE": 1,
    },
    "version_claim_status_counts": {
        "NOT_PRESENT": 33,
        "PRESENT_CORRECT": 29,
        "PRESENT_INCORRECT": 9,
        "PRESENT_EVIDENCE_INSUFFICIENT": 1,
    },
    "authority_claim_status_counts": {
        "NOT_PRESENT": 54,
        "PRESENT_CORRECT": 12,
        "PRESENT_INCORRECT": 6,
        "PRESENT_EVIDENCE_INSUFFICIENT": 0,
    },
    "minimum_external_evidence_needed_counts": {
        "ONE_OFFICIAL_EVIDENCE": 13,
        "MULTI_EVIDENCE_OR_VERSION_CHAIN": 4,
        "NOT_APPLICABLE": 55,
    },
    "evidence_selection_counts": {"NONE": 4, "E1": 24, "E2": 25, "E1+E2": 19},
    "phase2_issue_counts": {
        "NONE": 71,
        "SOURCE_UNREACHABLE": 0,
        "SOURCE_CONFLICT": 0,
        "EVIDENCE_MISSING": 1,
        "LATE_DISCOVERED_CANDIDATE_DEFECT": 0,
        "OTHER": 0,
    },
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _file_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _expanded_counts(
    validation: Mapping[str, Any], expected: Mapping[str, Mapping[str, int]]
) -> dict[str, dict[str, int]]:
    return {
        field: {name: int(validation[field].get(name, 0)) for name in values}
        for field, values in expected.items()
    }


def _process_diff(
    first_rows: Sequence[Mapping[str, str]],
    final_rows: Sequence[Mapping[str, str]],
) -> dict[str, Any]:
    first_by_id = {row["blind_review_id"]: row for row in first_rows}
    final_by_id = {row["blind_review_id"]: row for row in final_rows}
    changed_rows: list[dict[str, Any]] = []
    field_counts: dict[str, int] = {field: 0 for field in PHASE2_FIELDS}
    for identity in first_by_id:
        field_changes = []
        for field in PHASE2_FIELDS:
            first_value = first_by_id[identity][field]
            final_value = final_by_id[identity][field]
            if first_value != final_value:
                field_counts[field] += 1
                field_changes.append(
                    {
                        "field": field,
                        "first_value": first_value,
                        "final_value": final_value,
                    }
                )
        if field_changes:
            changed_rows.append(
                {
                    "blind_review_id": identity,
                    "first_phase2_issue": first_by_id[identity]["phase2_issue"],
                    "final_phase2_issue": final_by_id[identity]["phase2_issue"],
                    "changes": field_changes,
                }
            )
    first_unreachable_ids = {
        row["blind_review_id"]
        for row in first_rows
        if row["phase2_issue"] == "SOURCE_UNREACHABLE"
    }
    changed_ids = {row["blind_review_id"] for row in changed_rows}
    extra_changed_ids = sorted(changed_ids - first_unreachable_ids)
    if len(changed_rows) != 25:
        raise ValueError("FIRST_FINAL_CHANGED_ROW_COUNT_BLOCKER")
    if len(first_unreachable_ids) != 23 or not first_unreachable_ids.issubset(
        changed_ids
    ):
        raise ValueError("SOURCE_UNREACHABLE_RESOLUTION_DIFF_BLOCKER")
    if extra_changed_ids != ["BR-46BC044669", "BR-C27BF02D5F"]:
        raise ValueError("FIRST_FINAL_EXTRA_REFINEMENT_BLOCKER")
    expected_special = {
        "BR-46BC044669": {
            "minimum_external_evidence_needed": (
                "NOT_APPLICABLE",
                "ONE_OFFICIAL_EVIDENCE",
            )
        },
        "BR-C27BF02D5F": {"evidence_selection": ("E2", "E1+E2")},
    }
    for identity, expected_fields in expected_special.items():
        changes = {
            change["field"]: (change["first_value"], change["final_value"])
            for row in changed_rows
            if row["blind_review_id"] == identity
            for change in row["changes"]
        }
        if any(
            changes.get(field) != values for field, values in expected_fields.items()
        ):
            raise ValueError("FIRST_FINAL_REFINEMENT_VALUE_BLOCKER")
        if "phase2_reason" not in changes:
            raise ValueError("FIRST_FINAL_REFINEMENT_REASON_BLOCKER")
    return {
        "status": "PASS / PROCESS_LEVEL_ONLY / EXPECTED_CONTRACT_NOT_LOADED",
        "changed_row_count": len(changed_rows),
        "changed_field_counts": field_counts,
        "first_source_unreachable_count": len(first_unreachable_ids),
        "source_unreachable_rows_changed": len(first_unreachable_ids & changed_ids),
        "final_source_unreachable_count": sum(
            row["phase2_issue"] == "SOURCE_UNREACHABLE" for row in final_rows
        ),
        "extra_refinement_row_count": len(extra_changed_ids),
        "extra_refinement_blind_ids": extra_changed_ids,
        "reason_changed_row_count": field_counts["phase2_reason"],
        "changed_rows": changed_rows,
    }


def lock(
    *,
    first_source: Path,
    final_source: Path,
    phase2_packet: Path,
    output: Path,
    first_expected_sha256: str = FIRST_RAW_SHA256,
    first_expected_size: int = FIRST_RAW_SIZE,
    final_expected_sha256: str = FINAL_RAW_SHA256,
    final_expected_size: int = FINAL_RAW_SIZE,
    final_expected_counts: Mapping[str, Mapping[str, int]] = FINAL_EXPECTED_COUNTS,
) -> dict[str, Any]:
    """Validate and lock raw returns without accepting expected inputs."""

    if output.exists():
        raise FileExistsError("ADDITIVE_NAMESPACE_ALREADY_EXISTS")
    first_bytes = first_source.read_bytes()
    final_bytes = final_source.read_bytes()
    first_hash = sha256(first_bytes).hexdigest()
    final_hash = sha256(final_bytes).hexdigest()
    if (
        first_hash != first_expected_sha256.casefold()
        or len(first_bytes) != first_expected_size
    ):
        raise ValueError("FIRST_PHASE2_RAW_TRANSPORT_INTEGRITY_BLOCKER")
    if (
        final_hash != final_expected_sha256.casefold()
        or len(final_bytes) != final_expected_size
    ):
        raise ValueError("FINAL_PHASE2_RAW_TRANSPORT_INTEGRITY_BLOCKER")

    packet_rows = _load_jsonl(phase2_packet)
    packet_qa = validate_phase2_packet_rows(packet_rows)
    expected_ids = [str(row["blind_review_id"]) for row in packet_rows]
    first_validation = validate_phase2_raw_return(first_bytes, expected_ids)
    final_validation = validate_phase2_raw_return(final_bytes, expected_ids)
    if first_validation["source_unreachable_row_count"] != 23:
        raise ValueError("FIRST_PHASE2_SOURCE_UNREACHABLE_HISTORY_BLOCKER")
    expanded = _expanded_counts(final_validation, final_expected_counts)
    if expanded != {
        field: dict(values) for field, values in final_expected_counts.items()
    }:
        raise ValueError("FINAL_PHASE2_DESCRIPTIVE_COUNT_BLOCKER")
    if final_validation["source_unreachable_row_count"] != 0:
        raise ValueError("FINAL_PHASE2_SOURCE_UNREACHABLE_BLOCKER")
    if final_validation["late_discovered_candidate_defect_count"] != 0:
        raise ValueError("FINAL_PHASE2_CANDIDATE_DEFECT_BLOCKER")
    issue_rows = [
        row for row in final_validation["rows"] if row["phase2_issue"] != "NONE"
    ]
    if len(issue_rows) != 1 or issue_rows[0]["blind_review_id"] != "BR-18F1D39495":
        raise ValueError("FINAL_PHASE2_SINGLE_ISSUE_IDENTITY_BLOCKER")
    process_diff = _process_diff(first_validation["rows"], final_validation["rows"])

    output.parent.mkdir(parents=True, exist_ok=True)
    output.mkdir(parents=False, exist_ok=False)
    for directory in ("comparison", "mismatch", "acceptance", "qa", "manifest"):
        (output / directory).mkdir(parents=True, exist_ok=False)
    first_destination = output / "raw" / FIRST_LOCKED_FILENAME
    final_destination = output / "raw" / FINAL_LOCKED_FILENAME
    lock_phase2_raw_return(first_bytes, expected_ids, first_destination)
    lock_phase2_raw_return(final_bytes, expected_ids, final_destination)
    if (
        first_destination.read_bytes() != first_bytes
        or final_destination.read_bytes() != final_bytes
    ):
        raise ValueError("PHASE2_RAW_BYTE_COPY_INTEGRITY_BLOCKER")
    lock_timestamp = _utc_now()
    _write_json(
        output / "comparison" / "first_vs_final_process_diff.json", process_diff
    )
    _write_json(
        output / "qa" / "final_phase2_raw_lock.json",
        {
            "status": "PASS",
            "task_id": TASK_ID,
            "EXTERNAL_PHASE2_ATTEMPT2_FINAL_RAW_RETURN": "IMMUTABLE",
            "FINAL_RAW_HASH_PASS": True,
            "FINAL_SCHEMA_PASS": True,
            "FINAL_72_ID_PASS": True,
            "FINAL_ENUM_PASS": True,
            "FINAL_RAW_IMMUTABLE": True,
            "EXPECTED_CONTRACT_LOADED": False,
            "IDENTITY_MAPPING_UNLOCKED": False,
            "FINAL_REVIEWER_EXPECTED_BLINDNESS": ("OWNER_ATTESTED_FROM_REVIEW_CONTEXT"),
            "owner_attestation": (
                "reviewer was instructed to make best efforts to access the supplied "
                "Evidence URLs, not to obtain hidden labels or expected answers"
            ),
            "external_evidence_scope_violation_detected": False,
            "first_source_path": str(first_source.resolve()),
            "first_source_filename": first_source.name,
            "first_raw_size": len(first_bytes),
            "first_raw_sha256": first_hash,
            "first_immutable_copy": first_destination.relative_to(output).as_posix(),
            "first_classification": (
                "INTERMEDIATE_REVIEWER_ACCESS_LIMITED_RETURN / "
                "VALID_PROCESS_EVIDENCE / NOT_FINAL_PHASE2_ANALYSIS_RETURN"
            ),
            "final_source_path": str(final_source.resolve()),
            "final_source_filename": final_source.name,
            "final_raw_size": len(final_bytes),
            "final_raw_sha256": final_hash,
            "final_immutable_copy": final_destination.relative_to(output).as_posix(),
            "FINAL_PHASE2_ANALYSIS_RETURN": (
                "SUPERSEDING_PHASE2_RETURN_AFTER_EVIDENCE_ACCESS_RETRY"
            ),
            "final_raw_lock_timestamp": lock_timestamp,
        },
    )
    _write_json(
        output / "qa" / "first_phase2_descriptive_summary.json",
        {key: value for key, value in first_validation.items() if key != "rows"},
    )
    _write_json(
        output / "qa" / "final_phase2_descriptive_summary.json",
        {
            **{key: value for key, value in final_validation.items() if key != "rows"},
            "counts_with_zero_enums": expanded,
            "interpretation": "DESCRIPTIVE_ONLY_BEFORE_EXPECTED_LOAD",
        },
    )
    _write_json(
        output / "qa" / "phase2_packet_parity.json",
        {
            **packet_qa,
            "first_return_id_parity": "72/72",
            "final_return_id_parity": "72/72",
        },
    )
    raw_lock_records = [
        {
            "path": path.relative_to(output).as_posix(),
            "size": path.stat().st_size,
            "sha256": _file_sha256(path),
        }
        for path in sorted(output.rglob("*"))
        if path.is_file()
    ]
    _write_json(
        output / "manifest" / "raw_lock_manifest.json",
        {
            "task_id": TASK_ID,
            "status": "FINAL_RAW_LOCKED / EXPECTED_CONTRACT_NOT_LOADED",
            "final_raw_lock_timestamp": lock_timestamp,
            "expected_contract_loaded": False,
            "identity_mapping_unlocked": False,
            "record_count": len(raw_lock_records),
            "records": raw_lock_records,
        },
    )
    if (
        first_source.read_bytes() != first_bytes
        or final_source.read_bytes() != final_bytes
    ):
        raise ValueError("SOURCE_RAW_MUTATION_BLOCKER")
    return {
        "status": "FINAL_RAW_LOCKED / EXPECTED_CONTRACT_NOT_LOADED",
        "first_raw_sha256": first_hash,
        "final_raw_sha256": final_hash,
        "final_raw_size": len(final_bytes),
        "changed_rows": process_diff["changed_row_count"],
        "source_unreachable_resolved": 23,
        "extra_refinement_rows": process_diff["extra_refinement_blind_ids"],
        "final_raw_lock_timestamp": lock_timestamp,
        "output": str(output.resolve()),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--first-source", type=Path, required=True)
    parser.add_argument("--final-source", type=Path, required=True)
    parser.add_argument("--phase2-packet", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = lock(
        first_source=args.first_source,
        final_source=args.final_source,
        phase2_packet=args.phase2_packet,
        output=args.output,
    )
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
