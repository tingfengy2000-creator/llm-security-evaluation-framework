from __future__ import annotations

import argparse
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

from scripts.research.lock_pilot4_ab_phase2_returns import (
    NS_MAIN,
    sheet_paths,
    validation_contract,
    workbook_parts,
    worksheet_rows,
)


TASK_ID = "PILOT4-A-B-OWNER-DEFECT-TRIAGE-AND-BLIND-ADJUDICATION-PREP-01"
SHEETS = [
    "00_使用说明",
    "01_五个Candidate缺陷优先判定",
    "02_普通字段仲裁",
    "03_证据详情",
    "04_枚举速查",
    "05_提交检查",
    "06_一致性统计",
]


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--workbook", type=Path, required=True)
    parser.add_argument("--git-head", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    parts = workbook_parts(args.workbook)
    names, paths = sheet_paths(parts)
    if names != SHEETS:
        raise ValueError(f"WORKBOOK_SHEET_CONTRACT_BLOCKER:{names}")
    workbook_root = ET.fromstring(parts["xl/workbook.xml"])
    hidden = [
        node.attrib["name"]
        for node in workbook_root.findall(f".//{{{NS_MAIN}}}sheet")
        if node.attrib.get("state", "visible") != "visible"
    ]
    if hidden:
        raise ValueError(f"HIDDEN_SHEET_BLOCKER:{hidden}")
    forbidden_parts = [
        name
        for name in parts
        if name.lower().endswith("vbaProject.bin".lower())
        or "/comments" in name.lower()
        or name.startswith("xl/externalLinks/")
    ]
    if forbidden_parts:
        raise ValueError(f"WORKBOOK_FORBIDDEN_PART_BLOCKER:{forbidden_parts}")
    defect_rows = worksheet_rows(parts, paths[SHEETS[1]])
    ordinary_rows = worksheet_rows(parts, paths[SHEETS[2]])
    if len([row for row in defect_rows if 2 <= row <= 6]) != 5:
        raise ValueError("DEFECT_ROW_COUNT_BLOCKER")
    if len([row for row in ordinary_rows if 2 <= row <= 79]) != 78:
        raise ValueError("ORDINARY_ROW_COUNT_BLOCKER")
    for row_number in range(2, 7):
        if defect_rows.get(row_number, {}).get(23, "") or defect_rows.get(
            row_number, {}
        ).get(24, ""):
            raise ValueError(f"DEFECT_OWNER_PREFILL_BLOCKER:{row_number}")
    for row_number in range(2, 80):
        if ordinary_rows.get(row_number, {}).get(16, "") or ordinary_rows.get(
            row_number, {}
        ).get(17, ""):
            raise ValueError(f"FIELD_OWNER_PREFILL_BLOCKER:{row_number}")
        field = ordinary_rows.get(row_number, {}).get(4, "")
        if field in {
            "evidence_selection",
            "derived_stealth_level",
            "assigned_stealth_level",
        }:
            raise ValueError(f"NON_ADJUDICABLE_FIELD_BLOCKER:{row_number}:{field}")
    validations_defect = validation_contract(parts, paths[SHEETS[1]])
    validations_ordinary = validation_contract(parts, paths[SHEETS[2]])
    if not validations_defect or not validations_ordinary:
        raise ValueError("DATA_VALIDATION_BLOCKER")
    raw_xml = b"\n".join(parts.values())
    formula_errors = [
        token
        for token in (b"#REF!", b"#DIV/0!", b"#VALUE!", b"#NAME?", b"#N/A")
        if token in raw_xml
    ]
    if formula_errors:
        raise ValueError(f"FORMULA_ERROR_TOKEN_BLOCKER:{formula_errors}")
    payload = json.loads(
        (args.root / "control/workbook_payload.json").read_text(encoding="utf-8")
    )
    if payload["expected_v3_loaded"] is not False:
        raise ValueError("EXPECTED_LOAD_BLOCKER")
    if len(payload["defect_rows"]) != 5 or len(payload["ordinary_rows"]) != 78:
        raise ValueError("PAYLOAD_COUNT_BLOCKER")
    if any(
        row["owner_defect_decision"] or row["owner_defect_reason"]
        for row in payload["defect_rows"]
    ):
        raise ValueError("PAYLOAD_DEFECT_PREFILL_BLOCKER")
    if any(
        row["owner_final_value"] or row["owner_decision_reason"]
        for row in payload["ordinary_rows"]
    ):
        raise ValueError("PAYLOAD_FIELD_PREFILL_BLOCKER")
    qa = {
        "task_id": TASK_ID,
        "validated_at": now_utc(),
        "status": "PASS",
        "workbook": {
            "path": str(args.workbook.resolve()),
            "bytes": args.workbook.stat().st_size,
            "sha256": sha256(args.workbook),
            "sheet_names": names,
            "hidden_sheets": 0,
            "macros": 0,
            "comments": 0,
            "external_links": 0,
            "defect_rows": 5,
            "ordinary_material_rows": 78,
            "owner_prefilled_cells": 0,
            "data_validation_contracts": len(validations_defect)
            + len(validations_ordinary),
            "formula_error_tokens": 0,
        },
        "expected_v3_loaded": False,
        "expected_values_exposed": 0,
        "evidence_selection_direct_adjudication_rows": 0,
        "derived_stealth_direct_adjudication_rows": 0,
        "ground_truth_generated": False,
    }
    write_json(args.root / "qa/final_workbook_validation.json", qa)
    write_text(
        args.root / "acceptance/PILOT4_AB_OWNER_ADJUDICATION_PREPARATION_EVIDENCE.md",
        f"""# Pilot4 A/B Owner 盲态仲裁准备证据\n\n"
        f"- Task: `{TASK_ID}`\n"
        f"- Git HEAD: `{args.git_head}`\n"
        "- 四份 A/B 原始返回：已按既有 SHA256 重新验证，未修改。\n"
        "- 仲裁前一致性：已从原始返回重新计算并与既有 preflight 一致。\n"
        "- Candidate 缺陷优先表：5 行，Owner 决定与理由均为空。\n"
        "- 普通字段仲裁表：78 行实质分歧；不含 evidence_selection，不直接仲裁 derived stealth。\n"
        "- Evidence：按 sample 分组嵌入冻结正文，并保留官方 URL 与 snapshot SHA256。\n"
        "- Expected V3：未加载、未比较、未向 Owner 暴露。\n"
        "- Ground Truth：未生成。\n\n"
        "当前唯一下一步是 Owner 按工作簿顺序完成 5 个缺陷分流，再完成可进入仲裁的字段。返回后必须先做原始字节锁定和结构校验。\n"
        """,
    )
    entries = []
    for path in sorted(args.root.rglob("*")):
        if not path.is_file() or path.name == "final_manifest.json":
            continue
        entries.append(
            {
                "path": path.relative_to(args.root).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    aggregate = hashlib.sha256(
        "".join(f"{entry['path']}\0{entry['sha256']}\n" for entry in entries).encode(
            "utf-8"
        )
    ).hexdigest()
    write_json(
        args.root / "manifest/final_manifest.json",
        {
            "task_id": TASK_ID,
            "generated_at": now_utc(),
            "git_head": args.git_head,
            "entry_count_excluding_manifest": len(entries),
            "aggregate_sha256": aggregate,
            "entries": entries,
            "final_status": [
                "PILOT4_AB_ALL_FOUR_RAWS_LOCKED",
                "PRE_ADJUDICATION_REPRODUCIBILITY_FROZEN",
                "OWNER_DEFECT_TRIAGE_WORKBOOK_READY",
                "OWNER_EXPECTED_BLIND_ADJUDICATION_WORKBOOK_READY",
                "EXPECTED_V3_NOT_LOADED",
                "OWNER_DECISION_REQUIRED",
                "NO_GROUND_TRUTH_YET",
            ],
        },
    )
    print(json.dumps(qa, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
