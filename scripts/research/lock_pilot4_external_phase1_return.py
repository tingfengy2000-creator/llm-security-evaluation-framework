"""Lock and summarize a Pilot4 external Phase1 return without identity unlock.

The script reads exactly two semantic inputs: the raw reviewer CSV bytes and
the public Phase1 packet JSONL.  It never reads Phase2, an identity mapping, or
an expected contract, and it never rewrites reviewer decisions.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from llmguard.domains.retrieval.hidden_poisoning.external_blind_review import (
    PHASE2_RELEASE_REQUIREMENTS,
    assert_phase2_release_allowed,
    lock_phase1_raw_return,
    validate_phase1_packet_rows,
    validate_phase1_raw_return,
)


TASK_ID = "PILOT4-EXTERNAL-BLIND-PHASE1-RETURN-LOCK-AND-DEFECT-TRIAGE-01"
STATUS = (
    "PILOT4_EXTERNAL_BLIND_PHASE1_RETURN_LOCKED / "
    "OWNER_DEFECT_TRIAGE_PENDING / PHASE2_WITHHELD / NO_HUMAN_DISTRIBUTION"
)
RAW_FILENAME = "PILOT4_EXTERNAL_BLIND_PHASE1_RETURN.csv"
FORBIDDEN_TRIAGE_TOKENS = (
    "sample_id",
    "triplet_id",
    "candidate_kind",
    "hard_negative_type",
    "target_field",
    "expected_label",
    "expected_contract",
    "Evidence Pool",
    "official_source_url",
)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _file_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _markdown(value: object) -> str:
    return (
        str(value)
        .replace("\\", "\\\\")
        .replace("|", "\\|")
        .replace("\r\n", "<br>")
        .replace("\n", "<br>")
        .replace("\r", "<br>")
    )


def _write_blind_report(
    path: Path, title: str, rows: Sequence[Mapping[str, str]], purpose: str
) -> None:
    fields = (
        "blind_review_id",
        "candidate_text",
        "source_title",
        "text_naturalness",
        "local_internal_conflict",
        "phase1_issue",
        "phase1_reason",
    )
    lines = [
        f"# {title}",
        "",
        f"Purpose: {purpose}",
        "",
        "Identity boundary: blind ID only. No private identity, Phase2 evidence, or expected label is loaded or shown.",
        "",
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    lines.extend(
        "| " + " | ".join(_markdown(row[field]) for field in fields) + " |"
        for row in rows
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def _manifest_records(root: Path) -> list[dict[str, object]]:
    return [
        {
            "path": path.relative_to(root).as_posix(),
            "size": path.stat().st_size,
            "sha256": _file_sha256(path),
        }
        for path in sorted(root.rglob("*"))
        if path.is_file() and path != root / "manifest" / "manifest.json"
    ]


def build(
    source: Path,
    phase1_packet: Path,
    output: Path,
    *,
    expected_sha256: str,
    expected_issue_rows: Mapping[str, str],
    corroborating_copies: Sequence[Path] = (),
    received_at: str = "NOT_RECORDED",
) -> dict[str, object]:
    """Create a new additive return-lock namespace and stop before Phase2."""

    if output.exists():
        raise FileExistsError("PHASE1_RETURN_EVIDENCE_NAMESPACE_EXISTS")
    raw_bytes = source.read_bytes()
    raw_sha256 = sha256(raw_bytes).hexdigest()
    if raw_sha256 != expected_sha256.casefold():
        raise ValueError("RAW_RETURN_TRANSPORT_INTEGRITY_BLOCKER")

    transport_copies = []
    for copy in corroborating_copies:
        copy_bytes = copy.read_bytes()
        copy_sha256 = sha256(copy_bytes).hexdigest()
        byte_equal = copy_bytes == raw_bytes
        transport_copies.append(
            {
                "path": str(copy.resolve()),
                "size": len(copy_bytes),
                "sha256": copy_sha256,
                "byte_equal_to_source": byte_equal,
            }
        )
        if copy_sha256 != raw_sha256 or not byte_equal:
            raise ValueError("RAW_RETURN_TRANSPORT_INTEGRITY_BLOCKER")

    packet_rows = _load_jsonl(phase1_packet)
    packet_qa = validate_phase1_packet_rows(packet_rows)
    expected_ids = [str(row["blind_review_id"]) for row in packet_rows]
    validation = validate_phase1_raw_return(raw_bytes, expected_ids)
    rows = list(validation["rows"])
    issue_by_id = {
        str(row["blind_review_id"]): str(row["phase1_issue"])
        for row in rows
        if row["phase1_issue"] != "NONE"
    }
    if issue_by_id != dict(expected_issue_rows):
        raise ValueError("PHASE1_ISSUE_TRANSPORT_BLOCKER")

    public_by_id = {str(row["blind_review_id"]): row for row in packet_rows}

    def joined(row: Mapping[str, str]) -> dict[str, str]:
        public = public_by_id[row["blind_review_id"]]
        return {
            "blind_review_id": row["blind_review_id"],
            "candidate_text": str(public["candidate_text"]),
            "source_title": str(public["source_title"]),
            "text_naturalness": row["text_naturalness"],
            "local_internal_conflict": row["local_internal_conflict"],
            "phase1_issue": row["phase1_issue"],
            "phase1_reason": row["phase1_reason"],
        }

    issue_rows = [joined(row) for row in rows if row["phase1_issue"] != "NONE"]
    naturalness_rows = [
        joined(row) for row in rows if row["text_naturalness"] != "NATURAL"
    ]
    if len(issue_rows) != 5 or len(naturalness_rows) != 9:
        raise ValueError("PHASE1_RETURN_DESCRIPTIVE_COUNT_BLOCKER")

    output.mkdir(parents=False, exist_ok=False)
    raw_destination = output / "raw" / RAW_FILENAME
    locked_sha256 = lock_phase1_raw_return(raw_bytes, expected_ids, raw_destination)
    copied_bytes = raw_destination.read_bytes()
    if copied_bytes != raw_bytes or _file_sha256(raw_destination) != raw_sha256:
        raise ValueError("RAW_RETURN_COPY_INTEGRITY_BLOCKER")

    lock_timestamp = _utc_now()
    source_mtime = (
        datetime.fromtimestamp(source.stat().st_mtime, timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )
    lock_facts = {
        "PHASE1_RETURN_RECEIVED": True,
        "PHASE1_RETURN_SCHEMA_VALID": True,
        "PHASE1_RETURN_72_72": True,
        "PHASE1_RETURN_HASH_LOCKED": True,
        "PHASE1_RETURN_IMMUTABLE": True,
        "PHASE1_CANDIDATE_DEFECT_TRIAGE_RESOLVED": False,
        "EXPECTED_CONTRACT_LOADED": False,
        "IDENTITY_MAPPING_UNLOCKED": False,
        "PHASE2_RELEASED": False,
        "raw_filename": source.name,
        "raw_size": len(raw_bytes),
        "raw_sha256": locked_sha256,
        "received_at": received_at,
        "source_last_write_utc": source_mtime,
        "source_path": str(source.resolve()),
        "immutable_copy_path": raw_destination.relative_to(output).as_posix(),
        "immutable_copy_contract": "EXCLUSIVE_CREATE_PLUS_SHA256_LOCK",
        "lock_timestamp": lock_timestamp,
        "row_count": validation["row_count"],
        "unique_id_count": validation["unique_id_count"],
        "enum_validation": "PASS",
        "conditional_reason_validation": "PASS",
    }
    _write_json(output / "qa" / "phase1_return_lock.json", lock_facts)
    _write_json(
        output / "qa" / "input_transport_integrity.json",
        {
            "status": "PASS",
            "expected_sha256": expected_sha256.casefold(),
            "source_path": str(source.resolve()),
            "source_size": len(raw_bytes),
            "source_sha256": raw_sha256,
            "corroborating_copies": transport_copies,
            "immutable_copy_sha256": _file_sha256(raw_destination),
            "source_copy_byte_equal": copied_bytes == raw_bytes,
        },
    )
    summary = {
        key: validation[key]
        for key in (
            "status",
            "raw_sha256",
            "headers",
            "row_count",
            "unique_id_count",
            "duplicate_id_count",
            "blank_id_count",
            "missing_ids",
            "unexpected_ids",
            "invalid_enum_count",
            "required_reason_rows",
            "missing_required_reason_count",
            "text_naturalness_counts",
            "local_internal_conflict_counts",
            "phase1_issue_counts",
            "issue_row_count",
            "non_natural_row_count",
            "local_yes_row_count",
        )
    }
    summary.update(
        {
            "interpretation": "DESCRIPTIVE_ONLY",
            "accuracy_evaluated": False,
            "agreement_evaluated": False,
            "expected_match_evaluated": False,
            "ground_truth_correctness_evaluated": False,
        }
    )
    _write_json(output / "qa" / "external_phase1_return_summary.json", summary)

    gate = {
        requirement: bool(lock_facts[requirement])
        for requirement in PHASE2_RELEASE_REQUIREMENTS
    }
    try:
        assert_phase2_release_allowed(gate)
    except ValueError as error:
        release_result = str(error)
    else:  # pragma: no cover - impossible while defect triage remains false
        raise AssertionError("PHASE2_RELEASE_MUST_REMAIN_BLOCKED")
    _write_json(
        output / "qa" / "phase2_release_gate.json",
        {
            "status": "BLOCKED_PENDING_OWNER_DEFECT_TRIAGE",
            "requirements": gate,
            "release_function_result": release_result,
            "release_approved": False,
            "phase2_released": False,
        },
    )

    triage_path = output / "owner_preflight" / "PILOT4_PHASE1_BLIND_DEFECT_TRIAGE.md"
    naturalness_path = (
        output / "owner_preflight" / "PILOT4_PHASE1_NATURALNESS_OBSERVATIONS.md"
    )
    _write_blind_report(
        triage_path,
        "Pilot4 Phase1 Blind Candidate-Defect Triage",
        issue_rows,
        "Owner blind-level review of the five external reviewer issue reports before any Phase2 release.",
    )
    _write_blind_report(
        naturalness_path,
        "Pilot4 Phase1 Naturalness Observations",
        naturalness_rows,
        "Owner blind-level review of eight MINOR_ISSUE rows and one UNNATURAL row; no automatic text repair.",
    )
    preflight_text = triage_path.read_text(
        encoding="utf-8"
    ) + naturalness_path.read_text(encoding="utf-8")
    leaked_tokens = [
        token for token in FORBIDDEN_TRIAGE_TOKENS if token in preflight_text
    ]
    if leaked_tokens:
        raise ValueError(f"PHASE1_TRIAGE_IDENTITY_LEAKAGE_BLOCKER:{leaked_tokens}")
    _write_json(
        output / "qa" / "owner_preflight_qa.json",
        {
            "status": "PASS",
            "issue_row_count": len(issue_rows),
            "issue_ids": issue_by_id,
            "naturalness_observation_row_count": len(naturalness_rows),
            "local_yes_count_descriptive_only": validation["local_yes_row_count"],
            "forbidden_token_count": 0,
            "identity_mapping_unlocked": False,
            "expected_contract_loaded": False,
            "phase2_evidence_loaded": False,
        },
    )

    records = _manifest_records(output)
    manifest = {
        "task_id": TASK_ID,
        "status": STATUS,
        "created_at": lock_timestamp,
        "source_raw_sha256": raw_sha256,
        "phase1_packet_path": str(phase1_packet.resolve()),
        "phase1_packet_qa": packet_qa,
        "expected_contract_loaded": False,
        "identity_mapping_unlocked": False,
        "phase2_released": False,
        "candidate_defect_triage_resolved": False,
        "file_count_excluding_manifest": len(records),
        "records": records,
        "aggregate_sha256": sha256(
            json.dumps(records, ensure_ascii=False, separators=(",", ":")).encode(
                "utf-8"
            )
        ).hexdigest(),
    }
    _write_json(output / "manifest" / "manifest.json", manifest)
    if any(
        _file_sha256(output / str(record["path"])) != record["sha256"]
        for record in records
    ):
        raise ValueError("EVIDENCE_MANIFEST_RECOMPUTE_BLOCKER")
    return {
        "status": STATUS,
        "raw_sha256": raw_sha256,
        "raw_size": len(raw_bytes),
        "row_count": validation["row_count"],
        "unique_id_count": validation["unique_id_count"],
        "issue_row_count": len(issue_rows),
        "non_natural_row_count": len(naturalness_rows),
        "local_yes_row_count": validation["local_yes_row_count"],
        "phase2_release_approved": False,
        "output": str(output.resolve()),
        "manifest_file_count": len(records),
    }


def _expected_issue(value: str) -> tuple[str, str]:
    try:
        opaque_id, issue = value.split("=", 1)
    except ValueError as error:
        raise argparse.ArgumentTypeError("expected ID=ISSUE") from error
    return opaque_id, issue


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--phase1-packet", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--expected-sha256", required=True)
    parser.add_argument(
        "--expected-issue", action="append", type=_expected_issue, required=True
    )
    parser.add_argument("--corroborating-copy", action="append", type=Path, default=[])
    parser.add_argument("--received-at", default="NOT_RECORDED")
    args = parser.parse_args()
    result = build(
        args.source,
        args.phase1_packet,
        args.output,
        expected_sha256=args.expected_sha256,
        expected_issue_rows=dict(args.expected_issue),
        corroborating_copies=args.corroborating_copy,
        received_at=args.received_at,
    )
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
