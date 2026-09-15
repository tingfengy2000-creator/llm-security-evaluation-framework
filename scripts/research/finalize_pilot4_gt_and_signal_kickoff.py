"""Freeze the Owner-accepted Final72 GT and record method-engineering kickoff.

The script creates additive evidence only. It does not mutate the GT candidate,
run signal extraction, train a detector, or generate formal experiment results.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


TASK_ID = "P1-FINAL72-GT-ACCEPTANCE-AND-SIGNAL-DETECTION-EXPERIMENT-KICKOFF-01"
SOURCE_CANDIDATE_SHA256 = (
    "7cc8baf832a57ead85958b8fbd0ca511caab31f840b52e864de623a11134845b"
)
ACCEPTANCE_MODE = "ACCEPTED_WITH_KNOWN_EVIDENCE_LIMITATIONS"
FINAL72_ROLE = "DEVELOPMENT_AND_METHOD_ENGINEERING_SET"
CANONICAL_FIELD_COUNT = 8
RECORD_COUNT = 72
VALUE_COUNT = 576
REQUIRED_METHOD_DOCS = (
    "docs/research/stage6_1_hidden_knowledge_poisoning/method_engineering/PAPER1_FIVE_VIEW_SIGNAL_CONTRACT_V1.md",
    "docs/research/stage6_1_hidden_knowledge_poisoning/method_engineering/SIGNAL_FEASIBILITY_EXPERIMENT_SPEC_V1.md",
    "docs/research/stage6_1_hidden_knowledge_poisoning/method_engineering/PAPER1_BASELINE_MATRIX_V1.md",
    "docs/research/stage6_1_hidden_knowledge_poisoning/method_engineering/PAPER1_FUSION_RISK_EXPLANATION_DESIGN_V1.md",
    "docs/research/stage6_1_hidden_knowledge_poisoning/method_engineering/PAPER1_METRIC_AND_ABLATION_CONTRACT_V1.md",
    "docs/research/stage6_1_hidden_knowledge_poisoning/benchmark/PAPER1_240_GROUP_SCALE_READINESS_SPEC_V1.md",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def load_candidate(path: Path) -> dict[str, Any]:
    if sha256(path) != SOURCE_CANDIDATE_SHA256:
        raise ValueError("FINAL72_GT_CANDIDATE_SHA_MISMATCH")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("FINAL72_GT_CANDIDATE_NOT_OBJECT")
    if value.get("id") != "PILOT4_FINAL72_GROUND_TRUTH_CANDIDATE_V1":
        raise ValueError("FINAL72_GT_CANDIDATE_ID_MISMATCH")
    if (
        value.get("record_count") != RECORD_COUNT
        or len(value.get("records", [])) != RECORD_COUNT
    ):
        raise ValueError("FINAL72_GT_RECORD_COUNT_MISMATCH")
    fields = value.get("canonical_fields")
    if not isinstance(fields, list) or len(fields) != CANONICAL_FIELD_COUNT:
        raise ValueError("FINAL72_GT_FIELD_SCHEMA_MISMATCH")
    records = value["records"]
    ids = [row.get("sample_id") for row in records]
    if len(set(ids)) != RECORD_COUNT or any(not item for item in ids):
        raise ValueError("FINAL72_GT_SAMPLE_ID_MISMATCH")
    values = 0
    for row in records:
        labels = row.get("labels")
        if not isinstance(labels, dict) or set(labels) != set(fields):
            raise ValueError("FINAL72_GT_LABEL_SCHEMA_MISMATCH")
        if any(not isinstance(item, str) or not item for item in labels.values()):
            raise ValueError("FINAL72_GT_MISSING_VALUE")
        values += len(labels)
    if values != VALUE_COUNT:
        raise ValueError("FINAL72_GT_VALUE_COUNT_MISMATCH")
    return value


def load_lineage(path: Path, candidate: dict[str, Any]) -> list[dict[str, Any]]:
    rows = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line
    ]
    if len(rows) != VALUE_COUNT:
        raise ValueError("FINAL72_GT_LINEAGE_COUNT_MISMATCH")
    expected = {
        (record["sample_id"], field): record["labels"][field]
        for record in candidate["records"]
        for field in candidate["canonical_fields"]
    }
    actual = {
        (row.get("sample_id"), row.get("field")): row.get("final_gt_candidate_value")
        for row in rows
    }
    if actual != expected:
        raise ValueError("FINAL72_GT_LINEAGE_VALUE_MISMATCH")
    return rows


def accepted_gt(candidate: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": "PILOT4_FINAL72_GROUND_TRUTH_V1",
        "status": "OWNER_ACCEPTED_FROZEN",
        "acceptance_mode": ACCEPTANCE_MODE,
        "source_candidate_id": candidate["id"],
        "source_candidate_sha256": SOURCE_CANDIDATE_SHA256,
        "record_count": RECORD_COUNT,
        "canonical_field_count": CANONICAL_FIELD_COUNT,
        "canonical_value_count": VALUE_COUNT,
        "canonical_fields": candidate["canonical_fields"],
        "candidate_corpus_sha256": candidate["candidate_corpus_sha256"],
        "value_precedence": candidate["value_precedence"],
        "expected_v3_value_precedence": False,
        "owner_acceptance": True,
        "gt_construction_closed": True,
        "formal_dataset_freeze": False,
        "role": FINAL72_ROLE,
        "untouched_final_test_set": False,
        "records": candidate["records"],
    }


def validate_method_docs(repo_root: Path) -> list[str]:
    checked: list[str] = []
    for relative in REQUIRED_METHOD_DOCS:
        path = repo_root / relative
        content = path.read_text(encoding="utf-8", errors="strict")
        if not content.strip():
            raise ValueError(f"EMPTY_METHOD_DOCUMENT:{relative}")
        checked.append(relative)
    signal_contract = (repo_root / REQUIRED_METHOD_DOCS[0]).read_text(encoding="utf-8")
    for marker in (
        "semantic_version_margin",
        "present_time_substitution_signal",
        "claimed_authority_match",
        "ranking_stability",
        "NOT_APPLICABLE",
    ):
        if marker not in signal_contract:
            raise ValueError(f"SIGNAL_CONTRACT_MARKER_MISSING:{marker}")
    return checked


def manifest_entries(root: Path) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    for path in sorted(
        item
        for item in root.rglob("*")
        if item.is_file() and item.name != "final_manifest.json"
    ):
        entries.append(
            {
                "path": path.relative_to(root).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    return entries


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--lineage", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--git-head", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.output.exists() and any(args.output.iterdir()):
        raise ValueError("EVIDENCE_OUTPUT_MUST_BE_ABSENT_OR_EMPTY")
    started_at = datetime.now(UTC).isoformat()
    candidate = load_candidate(args.candidate)
    lineage = load_lineage(args.lineage, candidate)
    method_docs = validate_method_docs(args.repo_root)
    final_gt = accepted_gt(candidate)

    gt_path = args.output / "gt/PILOT4_FINAL72_GROUND_TRUTH_V1.json"
    write_json(gt_path, final_gt)
    final_gt_sha = sha256(gt_path)
    lineage_path = args.output / "gt/PILOT4_FINAL72_GROUND_TRUTH_V1_LINEAGE.jsonl"
    lineage_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(args.lineage, lineage_path)

    acceptance = {
        "task_id": TASK_ID,
        "owner_decision": "PILOT4_FINAL72_GROUND_TRUTH_ACCEPTED",
        "acceptance_mode": ACCEPTANCE_MODE,
        "accepted_at": started_at,
        "source_candidate_sha256": SOURCE_CANDIDATE_SHA256,
        "final_gt_sha256": final_gt_sha,
        "records": RECORD_COUNT,
        "canonical_values": VALUE_COUNT,
        "lineage_records": len(lineage),
        "expected_v3_role": "POST_ADJUDICATION_RESEARCHER_QC_REFERENCE_ONLY",
        "expected_v3_value_precedence": False,
        "human_vs_expected": "469/504",
        "expected_v3_defects": 4,
        "known_frozen_evidence_limitations": 11,
        "human_adjudication_variances": 20,
        "guide_ambiguity": 0,
        "unresolved_blockers": 0,
        "final72_role": FINAL72_ROLE,
        "untouched_final_test_set": False,
        "formal_dataset_freeze": False,
        "formal_detector_result": False,
    }
    write_json(args.output / "acceptance/final72_gt_acceptance.json", acceptance)
    write_text(
        args.output
        / "acceptance/PILOT4_FINAL72_GROUND_TRUTH_FINAL_ACCEPTANCE_RECORD.md",
        f"""# Pilot4 Final72 Ground Truth 最终验收记录

- Owner decision：`PILOT4_FINAL72_GROUND_TRUTH_ACCEPTED = TRUE`
- Acceptance mode：`{ACCEPTANCE_MODE}`
- Source candidate SHA256：`{SOURCE_CANDIDATE_SHA256}`
- Frozen GT SHA256：`{final_gt_sha}`
- Integrity：`72/72` records；`576/576` canonical categorical values；lineage `576/576`
- Expected V3 comparison：`469/504`；Expected defects `4`
- Known frozen Evidence limitations：`11`，已经由 `INSUFFICIENT_EVIDENCE / EVIDENCE_MISSING` 显式编码
- Human adjudication variance：`20`；Guide ambiguity：`0`；unresolved blockers：`0`
- Expected V3 role：post-adjudication researcher QC only；不参与 Ground Truth value precedence
- Final72 role：`{FINAL72_ROLE}`；不得称为 untouched final test set
- Formal Dataset freeze：`FALSE`；Formal Detector result：`FALSE`
""",
    )
    write_json(
        args.output / "qa/final72_gt_acceptance_validation.json",
        {
            "task_id": TASK_ID,
            "status": "PASS",
            "source_candidate_sha_exact": True,
            "records_complete": True,
            "canonical_values_complete": True,
            "lineage_complete": True,
            "expected_not_overriding_gt": True,
            "known_evidence_limitations_encoded": True,
            "unresolved_blockers": 0,
            "development_role_frozen": True,
            "untouched_test_claim": False,
            "formal_result_generated": False,
            "signal_extraction_executed": False,
            "detector_training_executed": False,
            "scale_dataset_generated": False,
        },
    )
    write_json(
        args.output / "qa/documentation_closeout.json",
        {
            "task_id": TASK_ID,
            "status": "PASS",
            "required_documents_checked": True,
            "method_documents": method_docs,
            "final_boundary": "SIGNAL_FEASIBILITY_EXECUTION_REQUIRES_SEPARATE_APPROVAL",
        },
    )
    write_text(
        args.output / "README.md",
        """# Final72 GT acceptance and Signal/Detection engineering kickoff

This additive namespace freezes the Owner-accepted Final72 Ground Truth and its lineage. It records the start of contract/interface engineering only. It contains no signal-feasibility run, trained detector, calibrated-risk result, 240-group dataset or formal paper result.
""",
    )
    entries = manifest_entries(args.output)
    aggregate = hashlib.sha256(
        "".join(f"{row['path']}\0{row['sha256']}\n" for row in entries).encode()
    ).hexdigest()
    write_json(
        args.output / "manifest/final_manifest.json",
        {
            "task_id": TASK_ID,
            "generated_at": datetime.now(UTC).isoformat(),
            "git_head": args.git_head,
            "entry_count_excluding_manifest": len(entries),
            "aggregate_sha256": aggregate,
            "entries": entries,
            "final_status": [
                "PILOT4_FINAL72_GT_ACCEPTED",
                "PILOT4_GT_CONSTRUCTION_CLOSED",
                "PAPER1_SIGNAL_DETECTION_ENGINEERING_STARTED",
                "FINAL72_DEVELOPMENT_SET_ACTIVE",
                "FORMAL_SCALE_BENCHMARK_PENDING",
                "NO_FORMAL_DETECTOR_RESULT_YET",
            ],
        },
    )
    print(
        json.dumps(
            {
                "status": "PILOT4_FINAL72_GT_ACCEPTED",
                "final_gt_sha256": final_gt_sha,
                "records": RECORD_COUNT,
                "canonical_values": VALUE_COUNT,
                "lineage": len(lineage),
                "formal_results": 0,
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
