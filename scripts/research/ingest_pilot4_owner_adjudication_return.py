from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence
from xml.etree import ElementTree as ET

from scripts.research.lock_pilot4_ab_phase2_returns import (
    NS_MAIN,
    read_csv,
    read_mapping,
    rows_by_sample,
    sheet_paths,
    validation_contract,
    workbook_parts,
    worksheet_rows,
)
from scripts.research.prepare_pilot4_owner_adjudication import ENUMS


TASK_ID = "PILOT4-A-B-OWNER-ADJUDICATION-RETURN-LOCK-AND-CONSISTENCY-PREFLIGHT-01"
SHEETS = [
    "00_使用说明",
    "01_五个Candidate缺陷优先判定",
    "02_普通字段仲裁",
    "03_证据详情",
    "04_枚举速查",
    "05_提交检查",
    "06_一致性统计",
]
DEFECT_ENUM = {
    "CONFIRMED_DEFECT",
    "ANNOTATOR_INTERPRETATION_VARIANCE",
    "NEEDS_TARGETED_REREVIEW",
}
PHASE1_FIELDS = ("text_naturalness", "local_internal_conflict", "phase1_issue")
PHASE2_FIELDS = (
    "overall_fact_status",
    "version_claim_status",
    "authority_claim_status",
    "minimum_external_evidence_needed",
    "phase2_issue",
)
ALL_FIELDS = (*PHASE1_FIELDS, *PHASE2_FIELDS)
EXPLICIT_REVISION_RULE_SAMPLE = "P4Q-0dd2bf0608a7"


def now_utc() -> str:
    return datetime.now(UTC).isoformat(timespec="microseconds").replace("+00:00", "Z")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def require_new_output(path: Path) -> None:
    if path.exists() and any(path.iterdir()):
        raise ValueError(f"OUTPUT_NAMESPACE_NOT_EMPTY:{path}")
    path.mkdir(parents=True, exist_ok=True)


def header_records(rows: Mapping[int, Mapping[int, str]]) -> list[dict[str, str]]:
    header = rows[1]
    width = max(header)
    names = [header.get(column, "") for column in range(1, width + 1)]
    records: list[dict[str, str]] = []
    for row_number in sorted(number for number in rows if number >= 2):
        values = rows[row_number]
        if not any(values.values()):
            continue
        records.append(
            {
                name: values.get(column, "").strip()
                for column, name in enumerate(names, start=1)
                if name
            }
        )
    return records


def workbook_safety(parts: Mapping[str, bytes]) -> dict[str, Any]:
    root = ET.fromstring(parts["xl/workbook.xml"])
    hidden = [
        node.attrib["name"]
        for node in root.findall(f".//{{{NS_MAIN}}}sheet")
        if node.attrib.get("state", "visible") != "visible"
    ]
    forbidden = [
        name
        for name in parts
        if name.lower().endswith("vbaproject.bin")
        or "/comments" in name.lower()
        or name.startswith("xl/externalLinks/")
    ]
    if hidden or forbidden:
        raise ValueError(
            f"WORKBOOK_SAFETY_BLOCKER:hidden={hidden}:forbidden={forbidden}"
        )
    return {
        "hidden_sheets": hidden,
        "forbidden_parts": forbidden,
        "macros": 0,
        "comments": 0,
        "external_links": 0,
    }


def validate_defect_rows(
    records: Sequence[Mapping[str, str]], prior: Mapping[str, Any]
) -> list[dict[str, str]]:
    if len(records) != 5:
        raise ValueError(f"DEFECT_ROW_COUNT_BLOCKER:{len(records)}")
    prior_by_id = {str(row["sample_id"]): row for row in prior["defect_rows"]}
    result: list[dict[str, str]] = []
    for row in records:
        sample_id = row["sample_id"]
        if sample_id not in prior_by_id:
            raise ValueError(f"DEFECT_SAMPLE_PARITY_BLOCKER:{sample_id}")
        baseline = prior_by_id[sample_id]
        static_checks = {
            "triplet_id": "triplet_id",
            "candidate_text": "candidate_text",
            "source_title": "source_title",
            "A phase1_issue": "a_phase1_issue",
            "A phase1_reason": "a_phase1_reason",
            "B phase1_issue": "b_phase1_issue",
            "B phase1_reason": "b_phase1_reason",
            "A overall": "a_overall",
            "B overall": "b_overall",
            "A version": "a_version",
            "B version": "b_version",
            "A authority": "a_authority",
            "B authority": "b_authority",
            "A minimum": "a_minimum",
            "B minimum": "b_minimum",
            "E1 title": "e1_title",
            "E1 URL": "e1_url",
            "E2 title": "e2_title",
            "E2 URL": "e2_url",
        }
        for workbook_key, payload_key in static_checks.items():
            if row.get(workbook_key, "") != str(baseline[payload_key]):
                raise ValueError(
                    f"DEFECT_READONLY_VALUE_BLOCKER:{sample_id}:{workbook_key}"
                )
        decision = row.get("Owner Candidate缺陷决定", "")
        reason = row.get("Owner缺陷理由", "")
        route = row.get("后续路由状态", "")
        if decision not in DEFECT_ENUM or not reason:
            raise ValueError(f"DEFECT_OWNER_COMPLETENESS_BLOCKER:{sample_id}")
        if decision == "CONFIRMED_DEFECT" and route != "QUARANTINE_PENDING_OWNER_SCOPE":
            raise ValueError(f"DEFECT_ROUTE_BLOCKER:{sample_id}:{route}")
        if decision == "NEEDS_TARGETED_REREVIEW" and route != "TARGETED_REREVIEW_HOLD":
            raise ValueError(f"DEFECT_ROUTE_BLOCKER:{sample_id}:{route}")
        if (
            decision == "ANNOTATOR_INTERPRETATION_VARIANCE"
            and route != "READY_FOR_OWNER_ADJUDICATION"
        ):
            raise ValueError(f"DEFECT_ROUTE_BLOCKER:{sample_id}:{route}")
        result.append(
            {
                "sample_id": sample_id,
                "owner_defect_decision": decision,
                "owner_defect_reason": reason,
                "route": route,
            }
        )
    return result


def validate_ordinary_rows(
    records: Sequence[Mapping[str, str]], prior: Mapping[str, Any]
) -> list[dict[str, str]]:
    if len(records) != 78:
        raise ValueError(f"ORDINARY_ROW_COUNT_BLOCKER:{len(records)}")
    prior_by_key = {
        (str(row["sample_id"]), str(row["field"])): row
        for row in prior["ordinary_rows"]
    }
    if len(prior_by_key) != 78:
        raise ValueError("PRIOR_ORDINARY_KEY_BLOCKER")
    result: list[dict[str, str]] = []
    for row in records:
        key = (row["sample_id"], row["field"])
        if key not in prior_by_key:
            raise ValueError(f"ORDINARY_SAMPLE_FIELD_PARITY_BLOCKER:{key}")
        baseline = prior_by_key[key]
        static_checks = {
            "triplet_id": "triplet_id",
            "phase": "phase",
            "candidate_text": "candidate_text",
            "A blind_review_id": "a_blind_review_id",
            "A value": "a_value",
            "A reason": "a_reason",
            "B blind_review_id": "b_blind_review_id",
            "B value": "b_value",
            "B reason": "b_reason",
            "Guide规则摘要": "guide_rule",
        }
        for workbook_key, payload_key in static_checks.items():
            if row.get(workbook_key, "") != str(baseline[payload_key]):
                raise ValueError(
                    f"ORDINARY_READONLY_VALUE_BLOCKER:{key}:{workbook_key}"
                )
        if row.get("当前状态") != "READY_FOR_OWNER_ADJUDICATION":
            raise ValueError(f"ORDINARY_ROUTE_BLOCKER:{key}:{row.get('当前状态')}")
        final = row.get("Owner最终值", "")
        reason = row.get("Owner仲裁理由", "")
        allowed = set(ENUMS[row["field"]])
        if final not in allowed or not reason:
            raise ValueError(f"ORDINARY_OWNER_COMPLETENESS_BLOCKER:{key}:{final}")
        result.append(
            {
                "sample_id": row["sample_id"],
                "triplet_id": row["triplet_id"],
                "phase": row["phase"],
                "field": row["field"],
                "a_value": row["A value"],
                "a_reason": row["A reason"],
                "b_value": row["B value"],
                "b_reason": row["B reason"],
                "owner_final_value": final,
                "owner_decision_reason": reason,
            }
        )
    if set(prior_by_key) != {(row["sample_id"], row["field"]) for row in result}:
        raise ValueError("ORDINARY_78_KEY_PARITY_BLOCKER")
    return result


def mapped_rows(
    path: Path, mapping: Mapping[str, Mapping[str, Any]]
) -> dict[str, dict[str, str]]:
    rows = read_csv(path)
    if len(rows) != 72:
        raise ValueError(f"RETURN_ROW_COUNT_BLOCKER:{path}:{len(rows)}")
    return rows_by_sample(rows, mapping)


def build_resolved_records(
    p1a: Mapping[str, Mapping[str, str]],
    p1b: Mapping[str, Mapping[str, str]],
    p2a: Mapping[str, Mapping[str, str]],
    p2b: Mapping[str, Mapping[str, str]],
    owner_rows: Sequence[Mapping[str, str]],
) -> tuple[list[dict[str, Any]], Counter[str]]:
    owner = {
        (row["sample_id"], row["field"]): row["owner_final_value"] for row in owner_rows
    }
    owner_reason = {
        (row["sample_id"], row["field"]): row["owner_decision_reason"]
        for row in owner_rows
    }
    source_counts: Counter[str] = Counter()
    records: list[dict[str, Any]] = []
    for sample_id in sorted(p1a):
        record: dict[str, Any] = {"sample_id": sample_id, "fields": {}}
        for fields, a_rows, b_rows in (
            (PHASE1_FIELDS, p1a, p1b),
            (PHASE2_FIELDS, p2a, p2b),
        ):
            for field in fields:
                a_value = a_rows[sample_id][field]
                b_value = b_rows[sample_id][field]
                key = (sample_id, field)
                if a_value == b_value:
                    value = a_value
                    source = "A_B_AGREEMENT"
                    reason = ""
                else:
                    if key not in owner:
                        raise ValueError(f"MISSING_OWNER_ADJUDICATION:{key}")
                    value = owner[key]
                    source = "OWNER_ADJUDICATION"
                    reason = owner_reason[key]
                record["fields"][field] = {
                    "value": value,
                    "source": source,
                    "owner_reason": reason,
                }
                source_counts[source] += 1
        records.append(record)
    if source_counts != Counter({"A_B_AGREEMENT": 498, "OWNER_ADJUDICATION": 78}):
        raise ValueError(f"RESOLUTION_SOURCE_COUNT_BLOCKER:{source_counts}")
    return records, source_counts


def field_value(record: Mapping[str, Any], field: str) -> str:
    return str(record["fields"][field]["value"])


def set_overlay(
    record: dict[str, Any],
    field: str,
    value: str,
    rule_id: str,
    rationale: str,
) -> dict[str, Any]:
    cell = record["fields"][field]
    before = str(cell["value"])
    cell["pre_overlay_value"] = before
    cell["value"] = value
    cell["source_before_overlay"] = cell["source"]
    cell["source"] = "OWNER_AUTHORIZED_RULE_OVERLAY"
    cell["owner_rule_id"] = rule_id
    return {
        "sample_id": record["sample_id"],
        "field": field,
        "before": before,
        "after": value,
        "changed": before != value,
        "owner_rule_id": rule_id,
        "rationale": rationale,
    }


def apply_owner_rule_overlays(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    overlays: list[dict[str, Any]] = []
    for record in records:
        if (
            field_value(record, "local_internal_conflict") == "YES"
            and field_value(record, "overall_fact_status") == "FACTUAL_CONFLICT"
        ):
            overlays.append(
                set_overlay(
                    record,
                    "minimum_external_evidence_needed",
                    "NOT_APPLICABLE",
                    "OWNER_RULE_INTERNAL_CONTRADICTION_MINIMUM_20260914",
                    "事实冲突已由候选文本内部确认，外部证据需求问题不适用。",
                )
            )
            if field_value(record, "phase2_issue") != "NONE":
                raise ValueError(
                    f"OWNER_INTERNAL_CONTRADICTION_PHASE2_ISSUE_BLOCKER:{record['sample_id']}"
                )
    revision = next(
        record
        for record in records
        if record["sample_id"] == EXPLICIT_REVISION_RULE_SAMPLE
    )
    overlays.append(
        set_overlay(
            revision,
            "version_claim_status",
            "PRESENT_INCORRECT",
            "OWNER_RULE_EXPLICIT_REVISION_CLAIM_20260915",
            "出现修订命题即存在版本关系；修订机关或修订内容事实错误时标记 PRESENT_INCORRECT，authority 另行判断。",
        )
    )
    return overlays


def consistency_findings(
    records: Sequence[Mapping[str, Any]], owner_rows: Sequence[Mapping[str, str]]
) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for record in records:
        sample_id = str(record["sample_id"])
        overall = field_value(record, "overall_fact_status")
        minimum = field_value(record, "minimum_external_evidence_needed")
        issue = field_value(record, "phase2_issue")
        if overall != "FACTUAL_CONFLICT" and minimum != "NOT_APPLICABLE":
            findings.append(
                {
                    "sample_id": sample_id,
                    "finding": "MINIMUM_NON_CONFLICT_MUST_BE_NOT_APPLICABLE",
                    "current": {"overall_fact_status": overall, "minimum": minimum},
                    "suggested_owner_correction": {
                        "minimum_external_evidence_needed": "NOT_APPLICABLE"
                    },
                    "materiality": "GROUND_TRUTH_BLOCKER",
                }
            )
        if issue == "EVIDENCE_MISSING" and overall != "INSUFFICIENT_EVIDENCE":
            findings.append(
                {
                    "sample_id": sample_id,
                    "finding": "DECISIVE_OVERALL_WITH_EVIDENCE_MISSING_REQUIRES_OWNER_CLARIFICATION",
                    "current": {"overall_fact_status": overall, "phase2_issue": issue},
                    "suggested_owner_correction": {
                        "option_a": "phase2_issue=NONE with an evidence-based reason",
                        "option_b": "overall_fact_status=INSUFFICIENT_EVIDENCE if the missing evidence is material",
                    },
                    "materiality": "GROUND_TRUTH_BLOCKER",
                }
            )
    evidence_pattern = re.compile(
        r"(?:(?<![A-Za-z0-9_])E3(?![A-Za-z0-9_])|证据\s*3)", re.IGNORECASE
    )
    for row in owner_rows:
        if evidence_pattern.search(row["owner_decision_reason"]):
            findings.append(
                {
                    "sample_id": row["sample_id"],
                    "field": row["field"],
                    "finding": "UNBOUND_E3_PROVENANCE_REFERENCE",
                    "current": {
                        "owner_final_value": row["owner_final_value"],
                        "owner_decision_reason": row["owner_decision_reason"],
                    },
                    "suggested_owner_correction": (
                        "If E3 means E1, correct the reason reference additively; otherwise provide E3 title, URL, snapshot and SHA256."
                    ),
                    "materiality": "PROVENANCE_BLOCKER",
                }
            )
    return findings


def manifest_entries(root: Path) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.name == "final_manifest.json":
            continue
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
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--workbook", type=Path, required=True)
    parser.add_argument("--prior-root", type=Path, required=True)
    parser.add_argument("--phase1-root", type=Path, required=True)
    parser.add_argument("--phase2-root", type=Path, required=True)
    parser.add_argument("--mapping-root", type=Path, required=True)
    parser.add_argument("--git-head", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    require_new_output(args.output)
    timestamp = now_utc()

    source_sha = sha256(args.workbook)
    source_bytes = args.workbook.stat().st_size
    raw_path = (
        args.output
        / "raw/PILOT4_AB_OWNER_EXPECTED_BLIND_ADJUDICATION_WORKBOOK_V1_RETURNED.xlsx"
    )
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(args.workbook, raw_path)
    if sha256(raw_path) != source_sha or raw_path.stat().st_size != source_bytes:
        raise ValueError("RETURNED_WORKBOOK_IMMUTABLE_COPY_BLOCKER")

    parts = workbook_parts(raw_path)
    names, paths = sheet_paths(parts)
    if names != SHEETS:
        raise ValueError(f"WORKBOOK_SHEET_CONTRACT_BLOCKER:{names}")
    safety = workbook_safety(parts)
    validations = {
        SHEETS[1]: validation_contract(parts, paths[SHEETS[1]]),
        SHEETS[2]: validation_contract(parts, paths[SHEETS[2]]),
    }
    if len(validations[SHEETS[1]]) != 1 or len(validations[SHEETS[2]]) != 7:
        raise ValueError("WORKBOOK_VALIDATION_CONTRACT_BLOCKER")
    prior = json.loads(
        (args.prior_root / "control/workbook_payload.json").read_text(encoding="utf-8")
    )
    defect_records = validate_defect_rows(
        header_records(worksheet_rows(parts, paths[SHEETS[1]])), prior
    )
    ordinary_records = validate_ordinary_rows(
        header_records(worksheet_rows(parts, paths[SHEETS[2]])), prior
    )
    checks = worksheet_rows(parts, paths[SHEETS[5]])
    check_statuses = [checks[row].get(4, "") for row in range(4, 9)]
    if check_statuses != ["PASS"] * 5:
        raise ValueError(f"WORKBOOK_OWNER_CHECK_BLOCKER:{check_statuses}")

    map_a, map_a_audit = read_mapping(
        args.mapping_root / "PILOT4_AB_A_IDENTITY_MAPPING.json", "HUMAN-A01"
    )
    map_b, map_b_audit = read_mapping(
        args.mapping_root / "PILOT4_AB_B_IDENTITY_MAPPING.json", "HUMAN-B01"
    )
    p1a_path = args.phase1_root / "HUMAN-A01/PILOT4_AB_HUMAN_A01_PHASE1_RETURN.csv"
    p1b_path = args.phase1_root / "HUMAN-B01/PILOT4_AB_HUMAN_B01_PHASE1_RETURN.csv"
    p2a_path = args.phase2_root / "HUMAN-A01/PILOT4_AB_HUMAN_A01_PHASE2_RETURN.csv"
    p2b_path = args.phase2_root / "HUMAN-B01/PILOT4_AB_HUMAN_B01_PHASE2_RETURN.csv"
    p1a, p1b = mapped_rows(p1a_path, map_a), mapped_rows(p1b_path, map_b)
    p2a, p2b = mapped_rows(p2a_path, map_a), mapped_rows(p2b_path, map_b)
    if not (set(p1a) == set(p1b) == set(p2a) == set(p2b)):
        raise ValueError("FOUR_RETURN_SAMPLE_PARITY_BLOCKER")
    resolved, source_counts = build_resolved_records(
        p1a, p1b, p2a, p2b, ordinary_records
    )
    overlays = apply_owner_rule_overlays(resolved)
    findings = consistency_findings(resolved, ordinary_records)

    choices: Counter[str] = Counter()
    for row in ordinary_records:
        final = row["owner_final_value"]
        if final == row["a_value"] and final == row["b_value"]:
            choices["BOTH"] += 1
        elif final == row["a_value"]:
            choices["A"] += 1
        elif final == row["b_value"]:
            choices["B"] += 1
        else:
            choices["THIRD_VALUE"] += 1

    decision_record = {
        "task_id": TASK_ID,
        "recorded_at": timestamp,
        "classification": "IMMUTABLE_OWNER_DECISION_EXTRACTION",
        "owner_attribution": "PROJECT_REQUIREMENT_OWNER_HUMAN_DECISION",
        "returned_workbook": {
            "source_path": str(args.workbook.resolve()),
            "raw_copy_path": str(raw_path.resolve()),
            "bytes": source_bytes,
            "sha256": source_sha,
            "prior_blank_workbook_bytes": 522429,
            "prior_blank_workbook_sha256": "252501902ea9fdbfccc63b52fe18a27e9d96208be4a8c329503da25e512e8f38",
        },
        "defect_decisions": defect_records,
        "field_adjudications": ordinary_records,
        "counts": {
            "defect_decisions": len(defect_records),
            "field_adjudications": len(ordinary_records),
            "owner_choice": dict(sorted(choices.items())),
        },
        "raw_workbook_modified_by_codex": False,
        "expected_v3_loaded": False,
        "ground_truth_generated": False,
    }
    write_json(
        args.output / "control/owner_adjudication_decisions_raw.json", decision_record
    )
    write_json(
        args.output / "control/owner_authorized_rule_overlay.json",
        {
            "task_id": TASK_ID,
            "classification": "ADDITIVE_OWNER_AUTHORIZED_RULE_OVERLAY",
            "owner_decisions_overwritten_in_raw_workbook": False,
            "overlays": overlays,
            "changed_values": sum(bool(row["changed"]) for row in overlays),
            "no_change_confirmations": sum(not row["changed"] for row in overlays),
        },
    )
    write_json(
        args.output / "control/resolved_label_candidate_pre_gt.json",
        {
            "task_id": TASK_ID,
            "classification": "OWNER_PRIORITIZED_PRE_GROUND_TRUTH_CANDIDATE",
            "status": "BLOCKED_PENDING_TARGETED_OWNER_CORRECTIONS",
            "record_count": 72,
            "field_count": 576,
            "source_counts": dict(source_counts),
            "expected_v3_loaded": False,
            "ground_truth": False,
            "records": resolved,
        },
    )
    write_json(
        args.output / "qa/workbook_structure_validation.json",
        {
            "task_id": TASK_ID,
            "validated_at": timestamp,
            "status": "PASS",
            "workbook_bytes": source_bytes,
            "workbook_sha256": source_sha,
            "sheet_names": names,
            "sheet_count": len(names),
            "defect_rows": len(defect_records),
            "ordinary_rows": len(ordinary_records),
            "defect_data_validation_contracts": 1,
            "ordinary_data_validation_contracts": 7,
            "owner_check_sheet": "5/5 PASS",
            "safety": safety,
            "read_only_payload_parity": True,
            "expected_v3_loaded": False,
        },
    )
    write_json(
        args.output / "qa/relational_consistency_validation.json",
        {
            "task_id": TASK_ID,
            "status": "BLOCKED",
            "owner_rule_overlay_count": len(overlays),
            "owner_rule_overlay_changed_values": sum(
                bool(row["changed"]) for row in overlays
            ),
            "findings": findings,
            "finding_count": len(findings),
            "finding_sample_count": len({row["sample_id"] for row in findings}),
            "expected_v3_loaded": False,
            "ground_truth_generation_allowed": False,
        },
    )
    source_integrity = []
    for path in (p1a_path, p1b_path, p2a_path, p2b_path):
        source_integrity.append(
            {
                "path": str(path.resolve()),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    write_json(
        args.output / "qa/source_return_and_mapping_integrity.json",
        {
            "status": "PASS",
            "returns": source_integrity,
            "mappings": {"A": map_a_audit, "B": map_b_audit},
            "sample_parity": "72/72",
        },
    )

    blocker_lines = [
        "# PILOT4 Owner Return Consistency Blocker 01",
        "",
        f"Task: `{TASK_ID}`",
        "",
        "Owner 返回工作簿已经按原始字节锁定，5 个缺陷决定和 78 个字段仲裁均已提取。以下项目不会回写原工作簿，也不会被描述为 Codex 自动仲裁。",
        "",
        "## 已应用的 Owner 规则覆盖",
        "",
        f"- 内部矛盾且 overall 为 FACTUAL_CONFLICT：minimum 固定为 NOT_APPLICABLE（{sum(r['owner_rule_id'].endswith('20260914') for r in overlays)} 个样本）。",
        "- P4Q-0dd2bf0608a7：显式‘修订’命题按 Owner 冻结规则把 version 绑定为 PRESENT_INCORRECT；authority 仍单独判断。",
        "",
        "## 仍需 Owner 最小确认",
        "",
    ]
    for index, finding in enumerate(findings, start=1):
        blocker_lines.append(
            f"{index}. `{finding['sample_id']}` / `{finding.get('field', '-')}` — `{finding['finding']}`；当前 `{json.dumps(finding['current'], ensure_ascii=False)}`；建议 `{json.dumps(finding['suggested_owner_correction'], ensure_ascii=False)}`。"
        )
    blocker_lines.extend(
        [
            "",
            "## Gate",
            "",
            "- `OWNER_RETURN_RAW_LOCKED = TRUE`",
            "- `OWNER_DECISIONS_EXTRACTED = 5 + 78`",
            "- `EXPECTED_V3_LOADED = FALSE`",
            "- `GROUND_TRUTH_GENERATED = FALSE`",
            "- `OWNER_CORRECTION_REQUIRED = TRUE`",
            "",
            "Owner 可直接在聊天中逐项确认建议值或提供 E3 provenance；不需要重新保存或覆盖原工作簿。",
        ]
    )
    write_text(
        args.output / "blocker/PILOT4_OWNER_RETURN_CONSISTENCY_BLOCKER_01.md",
        "\n".join(blocker_lines),
    )
    write_text(
        args.output / "README.md",
        f"""# Pilot4 Owner adjudication return lock and consistency preflight

Task: `{TASK_ID}`

The Owner-returned workbook is preserved byte-for-byte at `{raw_path.relative_to(args.output).as_posix()}` with SHA256 `{source_sha}`. Five Candidate-defect decisions and 78 field adjudications were complete, enum-valid and traceable to the previously prepared payload. Owner choices are authoritative except where an already approved Owner rule is bound as a separate additive overlay.

The pre-Ground-Truth candidate contains 72 samples and 576 adjudicable fields: 498 come from A/B agreement and 78 from Owner adjudication. Expected V3 was not loaded. Ground Truth was not generated because targeted relational/provenance corrections remain open; see `blocker/PILOT4_OWNER_RETURN_CONSISTENCY_BLOCKER_01.md`.
""",
    )
    write_text(
        args.output / "acceptance/PILOT4_OWNER_RETURN_LOCK_EVIDENCE.md",
        f"""# Pilot4 Owner Return Lock Evidence

- Returned workbook: `{args.workbook.resolve()}`
- Immutable copy: `{raw_path.resolve()}`
- Bytes: `{source_bytes}`
- SHA256: `{source_sha}`
- Defect decisions: `5/5` complete; all five are `ANNOTATOR_INTERPRETATION_VARIANCE`.
- Field adjudications: `78/78` complete; reasons `78/78` complete.
- Choice distribution: A `46`, B `26`, third value `6`.
- Resolved label candidate: `72 samples / 576 fields`; A/B agreement `498`, Owner adjudication `78`.
- Expected V3 loaded: `false`.
- Ground Truth generated: `false`.
- Current gate: `OWNER_RETURN_CONSISTENCY_BLOCKER / OWNER_CORRECTION_REQUIRED`.
""",
    )

    entries = manifest_entries(args.output)
    aggregate = hashlib.sha256(
        "".join(f"{row['path']}\0{row['sha256']}\n" for row in entries).encode("utf-8")
    ).hexdigest()
    write_json(
        args.output / "manifest/final_manifest.json",
        {
            "task_id": TASK_ID,
            "generated_at": timestamp,
            "git_head": args.git_head,
            "entry_count_excluding_manifest": len(entries),
            "aggregate_sha256": aggregate,
            "entries": entries,
            "final_status": [
                "OWNER_ADJUDICATION_RETURN_RAW_LOCKED",
                "WORKBOOK_STRUCTURE_ENUM_COMPLETENESS_PASS",
                "OWNER_DECISIONS_EXTRACTED_5_PLUS_78",
                "OWNER_RULE_OVERLAYS_BOUND_ADDITIVELY",
                "OWNER_RETURN_CONSISTENCY_BLOCKER",
                "OWNER_CORRECTION_REQUIRED",
                "EXPECTED_V3_NOT_LOADED",
                "NO_GROUND_TRUTH_YET",
            ],
        },
    )
    print(
        json.dumps(
            {
                "status": "OWNER_RETURN_CONSISTENCY_BLOCKER",
                "workbook_sha256": source_sha,
                "defect_decisions": len(defect_records),
                "field_adjudications": len(ordinary_records),
                "owner_rule_overlays": len(overlays),
                "findings": len(findings),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
