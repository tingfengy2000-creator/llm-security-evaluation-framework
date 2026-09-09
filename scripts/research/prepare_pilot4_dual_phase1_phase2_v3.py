from __future__ import annotations

import argparse
import codecs
import csv
import hashlib
import io
import json
import os
import re
import shutil
import stat
import zipfile
from collections import Counter
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

from lxml import html
from pypdf import PdfReader


TASK_ID = "PILOT4-A-B-DUAL-PHASE1-RAW-LOCK-AND-HUMAN-FRIENDLY-PHASE2-RELEASE-01"
PHASE1_HEADERS = [
    "blind_review_id",
    "text_naturalness",
    "local_internal_conflict",
    "phase1_issue",
    "phase1_reason",
]
PHASE2_HEADERS = [
    "blind_review_id",
    "overall_fact_status",
    "version_claim_status",
    "authority_claim_status",
    "minimum_external_evidence_needed",
    "evidence_selection",
    "phase2_issue",
    "phase2_reason",
]
PHASE1_ENUMS = {
    "text_naturalness": {"NATURAL", "MINOR_ISSUE", "UNNATURAL"},
    "local_internal_conflict": {"YES", "NO", "UNCERTAIN"},
    "phase1_issue": {"NONE", "MISSING_CONTEXT", "AMBIGUOUS_REFERENCE", "OTHER"},
}
EXPECTED_PHASE1_SHA256 = {
    "HUMAN-A01": "bb74908f7433bca1c834e8e7ea8e8721316edb1a503202805f90dd0e974d8bac",
    "HUMAN-B01": "b27d291dcf86088dccc9a7fc7e5dda1e5c1e7af54ac7db7c3bad5d78b215daf2",
}
DISPLAY_HEADERS = {
    "blind_review_id": "blind_review_id（只读）",
    "candidate_text": "candidate_text（候选文本｜只读）",
    "source_title": "source_title（来源标题｜只读）",
    "view_e1": "查看E1",
    "view_e2": "查看E2",
    "overall_fact_status": "overall_fact_status【请填写】",
    "version_claim_status": "version_claim_status【请填写】",
    "authority_claim_status": "authority_claim_status【请填写】",
    "minimum_external_evidence_needed": "minimum_external_evidence_needed【请填写】",
    "evidence_selection": "evidence_selection【请填写】",
    "phase2_issue": "phase2_issue【请填写】",
    "phase2_reason": "phase2_reason【必须填写】",
    "filling_check": "填写检查（自动）",
}
PHASE2_ENUMS = {
    "overall_fact_status": [
        "CURRENTLY_CONSISTENT",
        "LEGITIMATE_VERSION_OR_HISTORY",
        "FACTUAL_CONFLICT",
        "INSUFFICIENT_EVIDENCE",
    ],
    "version_claim_status": [
        "NOT_PRESENT",
        "PRESENT_CORRECT",
        "PRESENT_INCORRECT",
        "PRESENT_EVIDENCE_INSUFFICIENT",
    ],
    "authority_claim_status": [
        "NOT_PRESENT",
        "PRESENT_CORRECT",
        "PRESENT_INCORRECT",
        "PRESENT_EVIDENCE_INSUFFICIENT",
    ],
    "minimum_external_evidence_needed": [
        "ONE_OFFICIAL_EVIDENCE",
        "MULTI_EVIDENCE_OR_VERSION_CHAIN",
        "NOT_APPLICABLE",
    ],
    "evidence_selection": ["NONE", "E1", "E2", "E1+E2"],
    "phase2_issue": [
        "NONE",
        "SOURCE_UNREACHABLE",
        "SOURCE_CONFLICT",
        "EVIDENCE_MISSING",
        "LATE_DISCOVERED_CANDIDATE_DEFECT",
        "OTHER",
    ],
}
FORBIDDEN_VISIBLE_TOKENS = [
    "sample_id",
    "candidate_kind",
    "expected_v3",
    "expected contract",
    "clean/poison",
    "poison_label",
    "hard negative",
    "hn subtype",
    "hkp",
    "intended_stealth",
    "control marker",
    "repair marker",
    "previous reviewer answer",
]


def _now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def _read_phase1_raw(path: Path) -> tuple[list[dict[str, str]], dict[str, Any]]:
    raw = path.read_bytes()
    if not raw.startswith(codecs.BOM_UTF8):
        raise ValueError(f"PHASE1_UTF8_BOM_BLOCKER:{path.name}")
    text = raw.decode("utf-8-sig", errors="strict")
    reader = csv.DictReader(io.StringIO(text, newline=""))
    if reader.fieldnames != PHASE1_HEADERS:
        raise ValueError(f"PHASE1_SCHEMA_BLOCKER:{path.name}:{reader.fieldnames}")
    rows = [dict(row) for row in reader]
    ids = [row["blind_review_id"] for row in rows]
    if len(rows) != 72 or len(set(ids)) != 72 or any(not value for value in ids):
        raise ValueError(f"PHASE1_ROW_ID_BLOCKER:{path.name}")
    for row_number, row in enumerate(rows, start=2):
        for field, allowed in PHASE1_ENUMS.items():
            if row[field] not in allowed:
                raise ValueError(
                    f"PHASE1_ENUM_BLOCKER:{path.name}:{row_number}:{field}:{row[field]}"
                )
        reason_required = (
            row["local_internal_conflict"] in {"YES", "UNCERTAIN"}
            or row["phase1_issue"] != "NONE"
        )
        if reason_required and not row["phase1_reason"].strip():
            raise ValueError(f"PHASE1_REASON_BLOCKER:{path.name}:{row_number}")
    return rows, {
        "filename": path.name,
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "encoding": "UTF-8 BOM",
        "columns": PHASE1_HEADERS,
        "row_count": len(rows),
        "unique_id_count": len(set(ids)),
        "duplicate_id_count": len(ids) - len(set(ids)),
        "enum_validation": "PASS",
        "conditional_reason_validation": "PASS",
        "descriptive_counts": {
            field: dict(sorted(Counter(row[field] for row in rows).items()))
            for field in PHASE1_ENUMS
        },
    }


def _read_template_ids(path: Path) -> list[str]:
    raw = path.read_bytes()
    text = raw.decode("utf-8-sig", errors="strict")
    reader = csv.DictReader(io.StringIO(text, newline=""))
    if reader.fieldnames != PHASE1_HEADERS:
        raise ValueError(f"PHASE1_TEMPLATE_SCHEMA_BLOCKER:{path}")
    return [str(row["blind_review_id"]) for row in reader]


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    for line_number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        if not line.strip():
            continue
        item = json.loads(line)
        if not isinstance(item, dict):
            raise ValueError(f"JSONL_RECORD_BLOCKER:{path}:{line_number}")
        rows.append(item)
    return rows


def _extract_snapshot_text(path: Path) -> tuple[str, dict[str, Any]]:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        reader = PdfReader(str(path))
        page_texts = []
        for page_number, page in enumerate(reader.pages, start=1):
            page_texts.append(
                f"【PDF 第 {page_number} 页】\n{page.extract_text() or ''}"
            )
        text = "\n\n".join(page_texts)
        method = "pypdf_full_page_text"
        extra = {"pdf_page_count": len(reader.pages)}
    elif suffix in {".html", ".htm"}:
        document = html.fromstring(path.read_bytes())
        for node in document.xpath("//script|//style|//noscript|//svg"):
            node.drop_tree()
        text = document.text_content()
        method = "lxml_full_visible_text"
        extra = {}
    else:
        text = path.read_text(encoding="utf-8", errors="strict")
        method = "utf8_full_text"
        extra = {}
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t\f\v]+", " ", text)
    text = re.sub(r"\n[ \t]+", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    if not text:
        raise ValueError(f"SNAPSHOT_TEXT_EXTRACTION_BLOCKER:{path}")
    return text, {
        "snapshot_filename": path.name,
        "snapshot_bytes": path.stat().st_size,
        "snapshot_sha256": _sha256(path),
        "text_extraction_method": method,
        "extracted_character_count": len(text),
        "full_text_included": True,
        **extra,
    }


def _phase2_payload(
    v2_root: Path, annotator: str, phase1_ids: list[str]
) -> dict[str, Any]:
    tag = annotator.replace("HUMAN-", "")
    base = v2_root / "withheld_phase2" / annotator
    packet_path = base / f"PILOT4_AB_HUMAN_{tag}_PHASE2_PACKET.jsonl"
    rows = _read_jsonl(packet_path)
    ids = [str(row.get("blind_review_id", "")) for row in rows]
    if len(rows) != 72 or len(set(ids)) != 72:
        raise ValueError(f"PHASE2_PACKET_ID_BLOCKER:{annotator}")
    if ids != phase1_ids:
        raise ValueError(f"PHASE2_PHASE1_ORDER_PARITY_BLOCKER:{annotator}")

    workbook_rows: list[dict[str, Any]] = []
    snapshot_qa: list[dict[str, Any]] = []
    for row in rows:
        pool = row.get("evidence_pool")
        if not isinstance(pool, list) or len(pool) != 2:
            raise ValueError(
                f"PHASE2_EVIDENCE_POOL_BLOCKER:{annotator}:{row.get('blind_review_id')}"
            )
        evidence_payload = []
        for evidence in pool:
            evidence_id = str(evidence.get("evidence_id", ""))
            if evidence_id not in {"E1", "E2"}:
                raise ValueError(
                    f"PHASE2_EVIDENCE_ID_BLOCKER:{annotator}:{evidence_id}"
                )
            relative = Path(str(evidence.get("frozen_snapshot", "")))
            snapshot_path = base / relative
            if not snapshot_path.is_file():
                raise ValueError(f"PHASE2_SNAPSHOT_MISSING:{annotator}:{snapshot_path}")
            expected_sha = str(evidence.get("snapshot_sha256", "")).lower()
            actual_sha = _sha256(snapshot_path)
            if actual_sha != expected_sha:
                raise ValueError(
                    f"PHASE2_SNAPSHOT_SHA_BLOCKER:{annotator}:{snapshot_path.name}"
                )
            text, qa = _extract_snapshot_text(snapshot_path)
            evidence_payload.append(
                {
                    "evidence_id": evidence_id,
                    "official_page_title": str(evidence.get("official_page_title", "")),
                    "official_source_url": str(evidence.get("official_source_url", "")),
                    "snapshot_sha256": actual_sha,
                    "snapshot_text": text,
                }
            )
            snapshot_qa.append(
                {
                    "blind_review_id": row["blind_review_id"],
                    "evidence_id": evidence_id,
                    **qa,
                }
            )
        workbook_rows.append(
            {
                "blind_review_id": str(row["blind_review_id"]),
                "candidate_text": str(row["candidate_text"]),
                "source_title": str(row["source_title"]),
                "evidence_pool": evidence_payload,
            }
        )
    if len(snapshot_qa) != 144:
        raise ValueError(
            f"PHASE2_SNAPSHOT_COVERAGE_BLOCKER:{annotator}:{len(snapshot_qa)}"
        )
    return {
        "task_id": TASK_ID,
        "annotator": annotator,
        "status": "PHASE2_V3_DISTRIBUTION_PREPARATION",
        "rows": workbook_rows,
        "display_headers": DISPLAY_HEADERS,
        "phase2_enums": PHASE2_ENUMS,
        "snapshot_qa": snapshot_qa,
        "snapshot_coverage": "144/144",
        "mapping_loaded": False,
        "expected_loaded": False,
        "agreement_computed": False,
        "ground_truth_created": False,
    }


def _readme(annotator: str) -> str:
    tag = annotator.replace("HUMAN-", "")
    return f"""# Pilot4 {annotator} Phase2 V3 使用说明

状态：`PHASE2_V3_DISTRIBUTION_READY`。只有在项目负责人同时向 A/B 发放后才开始填写。

## 你只需要做什么

1. 打开 `PILOT4_AB_HUMAN_{tag}_PHASE2_ANNOTATION_WORKBOOK_V3.xlsx`。
2. 只填写 `01_标注表` 中带 **【请填写】** 或 **【必须填写】** 的七列。
3. 点击每行的 `查看E1` / `查看E2`，直接跳到 `02_证据` 阅读冻结证据正文；URL 只用于来源追溯。
4. 字段含义和固定判断顺序见 `03_字段说明`；不会填时先看 `04_填写示例`。
5. 提交前逐项检查 `05_提交前检查`，并确认主表 `填写检查（自动）` 全部显示 `OK`。

## 不要修改

不要修改 ID、Candidate、来源标题、Evidence、公式、Sheet 名称、行数、列数或行顺序。不要读取 Expected、mapping、另一位标注人的答案，也不要使用 AI assistant。

## 返回方式

使用 **Save As / 另存为**，最终只返回填写完成的 XLSX，精确文件名：

`PILOT4_AB_HUMAN_{tag}_PHASE2_RETURN.xlsx`

不要导出 CSV，也不要重复填写 CSV。项目负责人会先锁定你返回的原始 XLSX，再用确定性 exporter 生成机器使用的 exact 8-column CSV。
"""


def _independence_notice(annotator: str) -> str:
    return f"""# {annotator} Phase2 Independence Notice

1. 独立完成本工作簿，不与另一位 annotator 讨论、互看答案或共享候选顺序。
2. 只使用工作簿 `02_证据` 中提供的 E1/E2 冻结正文与官方 URL，不访问 repo、mapping、Expected、历史 reviewer 返回或控制面资料。
3. 不使用 LLM/AI assistant 进行判断、证据解释或理由撰写。
4. 不修改 blind ID、Candidate、Evidence、公式、Sheet、行、列或顺序。
5. 只向项目负责人返回填写完成的 XLSX；不要自行导出 CSV。
"""


def _owner_guide() -> str:
    return """# Pilot4 A/B Owner Phase2 Distribution Guide V3

状态：`DUAL_PHASE1_RAW_LOCKED / PHASE2_RELEASE_ALLOWED / PHASE2_V3_DISTRIBUTION_READY / NOT_YET_DISTRIBUTED`。

只有在本任务的双 Phase1 raw lock、两份 workbook QA、A/B semantic parity、leakage 与 144/144 snapshot coverage 全部 PASS 后，Owner 才能执行一次**同时分发**。

## 同时给 HUMAN-A01

只发送 `HUMAN-A01/phase2_v3_distribution/` 中三项：

- `PILOT4_AB_HUMAN_A01_PHASE2_ANNOTATION_WORKBOOK_V3.xlsx`
- `README_FOR_HUMAN_A01_PHASE2_V3.md`
- `PILOT4_AB_HUMAN_A01_PHASE2_INDEPENDENCE_NOTICE.md`

## 同时给 HUMAN-B01

只发送 `HUMAN-B01/phase2_v3_distribution/` 中三项：

- `PILOT4_AB_HUMAN_B01_PHASE2_ANNOTATION_WORKBOOK_V3.xlsx`
- `README_FOR_HUMAN_B01_PHASE2_V3.md`
- `PILOT4_AB_HUMAN_B01_PHASE2_INDEPENDENCE_NOTICE.md`

不得先给一人，不得交叉发送另一人的 workbook，不得发送 mapping、Expected、Phase1 comparison、QA、manifest、export contract 或任何 control-plane 文件。

未来 A 返回名：`PILOT4_AB_HUMAN_A01_PHASE2_RETURN.xlsx`。\x20\x20
未来 B 返回名：`PILOT4_AB_HUMAN_B01_PHASE2_RETURN.xlsx`。

收到后先 byte-lock 人工原始 XLSX，再调用确定性 exporter 生成 canonical 8-column CSV；不得只保留 CSV 而丢弃人工原始 XLSX。
"""


def prepare(handoff: Path, v2_root: Path, output: Path) -> None:
    if output.exists() and any(output.iterdir()):
        raise ValueError(f"OUTPUT_MUST_BE_NEW_OR_EMPTY:{output}")
    output.mkdir(parents=True, exist_ok=True)
    timestamp = _now()
    phase1_results: dict[str, Any] = {}
    payload_dir = output / "control" / "workbook_payloads"
    payload_dir.mkdir(parents=True, exist_ok=True)

    for annotator in ("HUMAN-A01", "HUMAN-B01"):
        tag = annotator.replace("HUMAN-", "")
        source = handoff / f"PILOT4_AB_HUMAN_{tag}_PHASE1_RETURN.csv"
        if not source.is_file():
            raise ValueError(f"PHASE1_RAW_NOT_FOUND:{source}")
        rows, qa = _read_phase1_raw(source)
        if qa["sha256"] != EXPECTED_PHASE1_SHA256[annotator]:
            raise ValueError(f"PHASE1_RAW_TRANSPORT_INTEGRITY_BLOCKER:{annotator}")
        template = (
            v2_root
            / annotator
            / "phase1"
            / f"PILOT4_AB_HUMAN_{tag}_PHASE1_RETURN_TEMPLATE_V2.csv"
        )
        template_ids = _read_template_ids(template)
        raw_ids = [row["blind_review_id"] for row in rows]
        if raw_ids != template_ids:
            raise ValueError(f"PHASE1_ID_ORDER_PARITY_BLOCKER:{annotator}")

        immutable = output / "raw_phase1" / annotator / source.name
        immutable.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, immutable)
        if immutable.read_bytes() != source.read_bytes():
            raise ValueError(f"PHASE1_IMMUTABLE_COPY_BLOCKER:{annotator}")
        os.chmod(immutable, stat.S_IREAD)
        qa.update(
            {
                "annotator": annotator,
                "source_path": str(source.resolve()),
                "source_mtime_utc": datetime.fromtimestamp(source.stat().st_mtime, UTC)
                .isoformat()
                .replace("+00:00", "Z"),
                "immutable_copy_relative_path": immutable.relative_to(
                    output
                ).as_posix(),
                "immutable_copy_sha256": _sha256(immutable),
                "immutable_copy_byte_parity": True,
                "locked_at_utc": timestamp,
                "id_set_parity": "72/72 PASS",
                "id_order_parity": "PASS",
            }
        )
        _write_json(output / "phase1_lock" / f"{annotator}_phase1_lock.json", qa)
        phase1_results[annotator] = qa

        payload = _phase2_payload(v2_root, annotator, raw_ids)
        _write_json(payload_dir / f"{annotator}_phase2_v3_payload.json", payload)
        contract = {
            "contract_id": f"PILOT4_{annotator}_PHASE2_XLSX_TO_CSV_V1",
            "annotator": annotator,
            "worksheet": "01_标注表",
            "header_row": 3,
            "expected_row_count": 72,
            "expected_blind_review_ids_in_order": raw_ids,
            "display_to_canonical_header": {
                DISPLAY_HEADERS[key]: key
                for key in [
                    "blind_review_id",
                    "overall_fact_status",
                    "version_claim_status",
                    "authority_claim_status",
                    "minimum_external_evidence_needed",
                    "evidence_selection",
                    "phase2_issue",
                    "phase2_reason",
                ]
            },
            "canonical_output_headers": PHASE2_HEADERS,
            "canonical_enums": PHASE2_ENUMS,
            "output_encoding": "UTF-8 BOM",
            "output_newline": "LF",
        }
        _write_json(
            output
            / "export"
            / "contracts"
            / f"{annotator}_phase2_export_contract.json",
            contract,
        )

        distribution = output / annotator / "phase2_v3_distribution"
        _write_text(
            distribution / f"README_FOR_HUMAN_{tag}_PHASE2_V3.md", _readme(annotator)
        )
        _write_text(
            distribution / f"PILOT4_AB_HUMAN_{tag}_PHASE2_INDEPENDENCE_NOTICE.md",
            _independence_notice(annotator),
        )

    _write_json(
        output / "phase1_lock" / "dual_phase1_lock_gate.json",
        {
            "task_id": TASK_ID,
            "evaluated_at": timestamp,
            "A_raw_sha_pass": True,
            "B_raw_sha_pass": True,
            "A_immutable_pass": True,
            "B_immutable_pass": True,
            "A_schema_pass": True,
            "B_schema_pass": True,
            "A_72_72_pass": True,
            "B_72_72_pass": True,
            "A_enum_reason_pass": True,
            "B_enum_reason_pass": True,
            "DUAL_PHASE1_LOCK_GATE": "PASS",
            "PHASE2_RELEASE_ALLOWED": True,
            "mapping_unlocked": False,
            "expected_v3_loaded": False,
            "agreement_computed": False,
        },
    )
    _write_json(
        output / "register" / "PILOT4_A_B_DISTRIBUTION_REGISTER_V3.json",
        {
            "task_id": TASK_ID,
            "updated_at": timestamp,
            "A_PHASE1_RETURN_RECEIVED": True,
            "B_PHASE1_RETURN_RECEIVED": True,
            "A_PHASE1_RETURN_LOCKED": True,
            "B_PHASE1_RETURN_LOCKED": True,
            "DUAL_PHASE1_LOCK_GATE": "PASS",
            "PHASE2_RELEASE_ALLOWED": True,
            "A_PHASE2_V3_READY": False,
            "B_PHASE2_V3_READY": False,
            "A_PHASE2_DISTRIBUTED": False,
            "B_PHASE2_DISTRIBUTED": False,
            "A_PHASE2_RETURN_RECEIVED": False,
            "B_PHASE2_RETURN_RECEIVED": False,
            "agreement_complete": False,
            "owner_adjudication_complete": False,
            "ground_truth_created": False,
            "PHASE2_RETURN_TRANSPORT_SEMANTIC_CHANGE": False,
            "mapping_unlocked": False,
            "expected_v3_loaded": False,
        },
    )
    _write_text(
        output / "PILOT4_A_B_OWNER_PHASE2_DISTRIBUTION_GUIDE_V3.md", _owner_guide()
    )
    _write_json(
        output / "qa" / "prepare_qa.json",
        {
            "status": "PASS",
            "task_id": TASK_ID,
            "phase1": phase1_results,
            "dual_phase1_gate": "PASS",
            "snapshot_payload_coverage": {
                "HUMAN-A01": "144/144",
                "HUMAN-B01": "144/144",
            },
            "mapping_unlocked": False,
            "expected_v3_loaded": False,
            "agreement_computed": False,
        },
    )


NS_MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
NS_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS_PKG = "http://schemas.openxmlformats.org/package/2006/relationships"
ET.register_namespace("", NS_MAIN)
ET.register_namespace("r", NS_REL)


def _sheet_paths(parts: dict[str, bytes]) -> dict[str, str]:
    workbook = ET.fromstring(parts["xl/workbook.xml"])
    relationships = ET.fromstring(parts["xl/_rels/workbook.xml.rels"])
    rel_targets = {
        rel.attrib["Id"]: rel.attrib["Target"]
        for rel in relationships.findall(f"{{{NS_PKG}}}Relationship")
    }
    result = {}
    sheets = workbook.find(f"{{{NS_MAIN}}}sheets")
    if sheets is None:
        raise ValueError("XLSX_SHEETS_BLOCKER")
    for sheet in sheets:
        rel_id = sheet.attrib[f"{{{NS_REL}}}id"]
        target = rel_targets[rel_id].replace("\\", "/")
        if target.startswith("/"):
            target = target.lstrip("/")
        elif not target.startswith("xl/"):
            target = "xl/" + target.lstrip("./")
        result[sheet.attrib["name"]] = target
    return result


def _set_hidden_enum_and_names(parts: dict[str, bytes]) -> None:
    root = ET.fromstring(parts["xl/workbook.xml"])
    sheets = root.find(f"{{{NS_MAIN}}}sheets")
    if sheets is None:
        raise ValueError("XLSX_SHEETS_BLOCKER")
    found = False
    for sheet in sheets:
        if sheet.attrib.get("name") == "99_内部枚举":
            sheet.set("state", "hidden")
            found = True
    if not found:
        raise ValueError("ENUM_SHEET_MISSING_BLOCKER")
    existing = root.find(f"{{{NS_MAIN}}}definedNames")
    if existing is not None:
        root.remove(existing)
    defined = ET.Element(f"{{{NS_MAIN}}}definedNames")
    ranges = {
        "OVERALL_FACT_STATUS_VALUES": "$A$2:$A$5",
        "VERSION_CLAIM_STATUS_VALUES": "$B$2:$B$5",
        "AUTHORITY_CLAIM_STATUS_VALUES": "$C$2:$C$5",
        "MINIMUM_EVIDENCE_VALUES": "$D$2:$D$4",
        "EVIDENCE_SELECTION_VALUES": "$E$2:$E$5",
        "PHASE2_ISSUE_VALUES": "$F$2:$F$7",
    }
    for name, reference in ranges.items():
        node = ET.SubElement(defined, f"{{{NS_MAIN}}}definedName", {"name": name})
        node.text = f"'99_内部枚举'!{reference}"
    insert_at = list(root).index(sheets) + 1
    root.insert(insert_at, defined)
    parts["xl/workbook.xml"] = ET.tostring(root, encoding="utf-8", xml_declaration=True)


def _apply_text_contract(
    parts: dict[str, bytes], sheet_paths: dict[str, str], contract: dict[str, Any]
) -> None:
    sheet_roots = {
        name: ET.fromstring(parts[sheet_path])
        for name, sheet_path in sheet_paths.items()
    }
    cell_indexes = {
        name: {
            cell.attrib.get("r", ""): cell
            for cell in root.findall(f".//{{{NS_MAIN}}}c")
        }
        for name, root in sheet_roots.items()
    }
    internal_hyperlinks: list[tuple[str, str, str]] = []
    for entry in contract["entries"]:
        sheet_name = str(entry["sheet"])
        reference = str(entry["cell"])
        contract_cell = cell_indexes.get(sheet_name, {}).get(reference)
        if contract_cell is None:
            raise ValueError(f"TEXT_CONTRACT_CELL_BLOCKER:{sheet_name}:{reference}")
        formula_text = str(entry.get("formula", ""))
        hyperlink_match = re.fullmatch(
            r'HYPERLINK\("#\'02_证据\'!([A-Z]+\d+)","([^"]+)"\)', formula_text
        )
        if hyperlink_match:
            formula = contract_cell.find(f"{{{NS_MAIN}}}f")
            if formula is not None:
                contract_cell.remove(formula)
            value = contract_cell.find(f"{{{NS_MAIN}}}v")
            if value is None:
                value = ET.SubElement(contract_cell, f"{{{NS_MAIN}}}v")
            value.text = hyperlink_match.group(2)
            contract_cell.set("t", "str")
            internal_hyperlinks.append(
                (
                    reference,
                    f"'02_证据'!{hyperlink_match.group(1)}",
                    hyperlink_match.group(2),
                )
            )
        elif "formula" in entry:
            formula = contract_cell.find(f"{{{NS_MAIN}}}f")
            if formula is None:
                formula = ET.SubElement(contract_cell, f"{{{NS_MAIN}}}f")
            formula.text = str(entry["formula"])
            value = contract_cell.find(f"{{{NS_MAIN}}}v")
            if value is None:
                value = ET.SubElement(contract_cell, f"{{{NS_MAIN}}}v")
            value.text = str(entry.get("cachedValue", ""))
            contract_cell.set("t", "str")
        else:
            value = contract_cell.find(f"{{{NS_MAIN}}}v")
            if value is None:
                value = ET.SubElement(contract_cell, f"{{{NS_MAIN}}}v")
            value.text = str(entry["value"])
            contract_cell.set("t", "str")

    main_root = sheet_roots["01_标注表"]
    old_hyperlinks = main_root.find(f"{{{NS_MAIN}}}hyperlinks")
    if old_hyperlinks is not None:
        main_root.remove(old_hyperlinks)
    hyperlinks = ET.Element(f"{{{NS_MAIN}}}hyperlinks")
    for reference, location, display in internal_hyperlinks:
        ET.SubElement(
            hyperlinks,
            f"{{{NS_MAIN}}}hyperlink",
            {"ref": reference, "location": location, "display": display},
        )
    validations = main_root.find(f"{{{NS_MAIN}}}dataValidations")
    if validations is None:
        raise ValueError("TEXT_CONTRACT_DATA_VALIDATION_BLOCKER")
    validation_contract = {
        str(item["range"]): item for item in contract["validationMessages"]
    }
    for validation in validations:
        sqref = validation.attrib.get("sqref", "")
        item = validation_contract.get(sqref)
        if item is None:
            raise ValueError(f"TEXT_CONTRACT_VALIDATION_RANGE_BLOCKER:{sqref}")
        validation.set("promptTitle", str(item["title"]))
        validation.set("prompt", str(item["prompt"]))
        validation.set("errorTitle", str(contract["validationErrorTitle"]))
        validation.set("error", str(contract["validationErrorMessage"]))
        validation.set("showInputMessage", "1")
        validation.set("showErrorMessage", "1")
    children = list(main_root)
    insert_after = children.index(validations) + 1
    main_root.insert(insert_after, hyperlinks)

    for sheet_name, root in sheet_roots.items():
        parts[sheet_paths[sheet_name]] = ET.tostring(
            root, encoding="utf-8", xml_declaration=True
        )


def _unlock_editable_styles(parts: dict[str, bytes], main_sheet_path: str) -> None:
    style_root = ET.fromstring(parts["xl/styles.xml"])
    cell_xfs = style_root.find(f"{{{NS_MAIN}}}cellXfs")
    if cell_xfs is None:
        raise ValueError("XLSX_CELL_XFS_BLOCKER")
    sheet_root = ET.fromstring(parts[main_sheet_path])
    editable_cells = []
    style_ids: set[int] = set()
    for cell in sheet_root.findall(f".//{{{NS_MAIN}}}c"):
        ref = cell.attrib.get("r", "")
        match = re.fullmatch(r"([A-Z]+)(\d+)", ref)
        if (
            match
            and match.group(1) in {"F", "G", "H", "I", "J", "K", "L"}
            and 4 <= int(match.group(2)) <= 75
        ):
            style_id = int(cell.attrib.get("s", "0"))
            style_ids.add(style_id)
            editable_cells.append((cell, style_id))
    mapping: dict[int, int] = {}
    xfs = list(cell_xfs)
    for style_id in sorted(style_ids):
        base = deepcopy(xfs[style_id])
        for child in list(base):
            if child.tag == f"{{{NS_MAIN}}}protection":
                base.remove(child)
        ET.SubElement(base, f"{{{NS_MAIN}}}protection", {"locked": "0"})
        base.set("applyProtection", "1")
        mapping[style_id] = len(cell_xfs)
        cell_xfs.append(base)
    cell_xfs.set("count", str(len(cell_xfs)))
    for cell, old_style in editable_cells:
        cell.set("s", str(mapping[old_style]))
    parts["xl/styles.xml"] = ET.tostring(
        style_root, encoding="utf-8", xml_declaration=True
    )
    parts[main_sheet_path] = ET.tostring(
        sheet_root, encoding="utf-8", xml_declaration=True
    )


def _protect_sheets_and_bind_validations(
    parts: dict[str, bytes], sheet_paths: dict[str, str]
) -> None:
    validation_names = {
        "F": "OVERALL_FACT_STATUS_VALUES",
        "G": "VERSION_CLAIM_STATUS_VALUES",
        "H": "AUTHORITY_CLAIM_STATUS_VALUES",
        "I": "MINIMUM_EVIDENCE_VALUES",
        "J": "EVIDENCE_SELECTION_VALUES",
        "K": "PHASE2_ISSUE_VALUES",
    }
    for sheet_name, sheet_path in sheet_paths.items():
        root = ET.fromstring(parts[sheet_path])
        if root.find(f"{{{NS_MAIN}}}sheetProtection") is None:
            protection = ET.Element(
                f"{{{NS_MAIN}}}sheetProtection",
                {
                    "sheet": "1",
                    "objects": "1",
                    "scenarios": "1",
                    "formatCells": "1",
                    "formatColumns": "1",
                    "formatRows": "1",
                    "insertColumns": "1",
                    "insertRows": "1",
                    "deleteColumns": "1",
                    "deleteRows": "1",
                    "sort": "1",
                    "autoFilter": "1",
                    "selectLockedCells": "1",
                    "selectUnlockedCells": "0",
                },
            )
            children = list(root)
            sheet_data = root.find(f"{{{NS_MAIN}}}sheetData")
            insert_at = (
                children.index(sheet_data) + 1
                if sheet_data is not None
                else len(children)
            )
            root.insert(insert_at, protection)
        if sheet_name == "01_标注表":
            validations = root.find(f"{{{NS_MAIN}}}dataValidations")
            if validations is None or len(validations) != 6:
                raise ValueError("XLSX_DATA_VALIDATION_COUNT_BLOCKER")
            seen = set()
            for validation in validations:
                sqref = validation.attrib.get("sqref", "")
                column_match = re.match(r"([A-Z]+)", sqref)
                if not column_match or column_match.group(1) not in validation_names:
                    raise ValueError(f"XLSX_DATA_VALIDATION_RANGE_BLOCKER:{sqref}")
                column = column_match.group(1)
                formula = validation.find(f"{{{NS_MAIN}}}formula1")
                if formula is None:
                    formula = ET.SubElement(validation, f"{{{NS_MAIN}}}formula1")
                formula.text = validation_names[column]
                validation.set("showInputMessage", "1")
                validation.set("showErrorMessage", "1")
                validation.set("allowBlank", "0")
                seen.add(column)
            if seen != set(validation_names):
                raise ValueError(f"XLSX_DATA_VALIDATION_PARITY_BLOCKER:{seen}")
        parts[sheet_path] = ET.tostring(root, encoding="utf-8", xml_declaration=True)


def patch_workbook(path: Path, text_contract_path: Path) -> None:
    with zipfile.ZipFile(path, "r") as archive:
        parts = {name: archive.read(name) for name in archive.namelist()}
    sheet_paths = _sheet_paths(parts)
    if list(sheet_paths) != [
        "01_标注表",
        "02_证据",
        "03_字段说明",
        "04_填写示例",
        "05_提交前检查",
        "99_内部枚举",
    ]:
        raise ValueError(f"XLSX_SHEET_ORDER_BLOCKER:{list(sheet_paths)}")
    text_contract = json.loads(text_contract_path.read_text(encoding="utf-8"))
    _apply_text_contract(parts, sheet_paths, text_contract)
    _set_hidden_enum_and_names(parts)
    _unlock_editable_styles(parts, sheet_paths["01_标注表"])
    _protect_sheets_and_bind_validations(parts, sheet_paths)
    temporary = path.with_suffix(".patched.tmp.xlsx")
    with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, content in parts.items():
            archive.writestr(name, content)
    temporary.replace(path)


def _xlsx_visible_strings(path: Path) -> str:
    strings = []
    with zipfile.ZipFile(path, "r") as archive:
        if "xl/sharedStrings.xml" in archive.namelist():
            shared_root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
            for item in shared_root.findall(f"{{{NS_MAIN}}}si"):
                strings.append(
                    "".join(
                        node.text or "" for node in item.findall(f".//{{{NS_MAIN}}}t")
                    )
                )
        for name in archive.namelist():
            if name.startswith("xl/worksheets/") and name.endswith(".xml"):
                root = ET.fromstring(archive.read(name))
                for node in root.findall(f".//{{{NS_MAIN}}}t"):
                    if node.text:
                        strings.append(node.text)
                for cell in root.findall(f".//{{{NS_MAIN}}}c"):
                    if cell.attrib.get("t") != "str":
                        continue
                    value = cell.find(f"{{{NS_MAIN}}}v")
                    if value is not None and value.text:
                        strings.append(value.text)
    return "\n".join(strings)


def _validate_patched_workbook(
    path: Path, payload: dict[str, Any], text_contract: dict[str, Any]
) -> dict[str, Any]:
    with zipfile.ZipFile(path, "r") as archive:
        names = set(archive.namelist())
        if "xl/vbaProject.bin" in names:
            raise ValueError(f"XLSX_MACRO_BLOCKER:{path.name}")
        parts = {name: archive.read(name) for name in names}
    sheet_paths = _sheet_paths(parts)
    workbook_root = ET.fromstring(parts["xl/workbook.xml"])
    sheets = workbook_root.find(f"{{{NS_MAIN}}}sheets")
    enum_hidden = sheets is not None and any(
        sheet.attrib.get("name") == "99_内部枚举"
        and sheet.attrib.get("state") == "hidden"
        for sheet in sheets
    )
    main = ET.fromstring(parts[sheet_paths["01_标注表"]])
    validations = main.find(f"{{{NS_MAIN}}}dataValidations")
    formulas = [node.text or "" for node in main.findall(f".//{{{NS_MAIN}}}f")]
    hyperlinks = main.find(f"{{{NS_MAIN}}}hyperlinks")
    internal_hyperlink_count = 0 if hyperlinks is None else len(hyperlinks)
    qa_formula_count = sum(1 for value in formulas if "minimum逻辑不一致" in value)
    style_root = ET.fromstring(parts["xl/styles.xml"])
    cell_xfs = style_root.find(f"{{{NS_MAIN}}}cellXfs")
    if cell_xfs is None:
        raise ValueError("XLSX_CELL_XFS_BLOCKER")
    xfs = list(cell_xfs)
    editable_unlocked = 0
    for cell in main.findall(f".//{{{NS_MAIN}}}c"):
        ref = cell.attrib.get("r", "")
        if re.fullmatch(r"[F-L](?:[4-9]|[1-6][0-9]|7[0-5])", ref):
            style_id = int(cell.attrib.get("s", "0"))
            protection = xfs[style_id].find(f"{{{NS_MAIN}}}protection")
            if protection is not None and protection.attrib.get("locked") == "0":
                editable_unlocked += 1
    visible = _xlsx_visible_strings(path)
    lowered = visible.casefold()
    leaked = [
        token for token in FORBIDDEN_VISIBLE_TOKENS if token.casefold() in lowered
    ]
    if leaked:
        raise ValueError(f"REVIEWER_VISIBLE_LEAKAGE_BLOCKER:{path.name}:{leaked}")
    required_chinese = [
        "证据足够吗",
        "当前状态",
        "实际用了哪些",
        "事实错误本身不是 issue",
        "1–3 句话",
    ]
    missing_chinese = [item for item in required_chinese if item not in visible]
    if missing_chinese:
        raise ValueError(f"CHINESE_HELP_COVERAGE_BLOCKER:{path.name}:{missing_chinese}")
    if validations is None or len(validations) != 6:
        raise ValueError(f"DROPDOWN_BLOCKER:{path.name}")
    validation_formula_names = {
        node.text or "" for node in validations.findall(f".//{{{NS_MAIN}}}formula1")
    }
    expected_validation_names = {
        "OVERALL_FACT_STATUS_VALUES",
        "VERSION_CLAIM_STATUS_VALUES",
        "AUTHORITY_CLAIM_STATUS_VALUES",
        "MINIMUM_EVIDENCE_VALUES",
        "EVIDENCE_SELECTION_VALUES",
        "PHASE2_ISSUE_VALUES",
    }
    if validation_formula_names != expected_validation_names:
        raise ValueError(
            f"DROPDOWN_INTERNAL_RANGE_BLOCKER:{path.name}:{validation_formula_names}"
        )
    if internal_hyperlink_count != 144 or qa_formula_count != 72:
        raise ValueError(
            f"FORMULA_COVERAGE_BLOCKER:{path.name}:{internal_hyperlink_count}:{qa_formula_count}"
        )
    if editable_unlocked != 72 * 7:
        raise ValueError(
            f"EDITABLE_CELL_PROTECTION_BLOCKER:{path.name}:{editable_unlocked}"
        )

    contract_mismatch_count = 0
    sheet_roots = {
        name: ET.fromstring(parts[sheet_path])
        for name, sheet_path in sheet_paths.items()
    }
    cell_indexes = {
        name: {
            cell.attrib.get("r", ""): cell
            for cell in root.findall(f".//{{{NS_MAIN}}}c")
        }
        for name, root in sheet_roots.items()
    }
    hyperlink_index = {
        node.attrib.get("ref", ""): node
        for node in (list(hyperlinks) if hyperlinks is not None else [])
    }
    for entry in text_contract["entries"]:
        sheet_name = str(entry["sheet"])
        reference = str(entry["cell"])
        verified_cell = cell_indexes.get(sheet_name, {}).get(reference)
        if verified_cell is None:
            contract_mismatch_count += 1
            continue
        formula_text = str(entry.get("formula", ""))
        hyperlink_match = re.fullmatch(
            r'HYPERLINK\("#\'02_证据\'!([A-Z]+\d+)","([^"]+)"\)', formula_text
        )
        if hyperlink_match:
            node = hyperlink_index.get(reference)
            value = verified_cell.find(f"{{{NS_MAIN}}}v")
            if (
                node is None
                or node.attrib.get("location")
                != f"'02_证据'!{hyperlink_match.group(1)}"
                or node.attrib.get("display") != hyperlink_match.group(2)
                or value is None
                or value.text != hyperlink_match.group(2)
            ):
                contract_mismatch_count += 1
        elif "formula" in entry:
            formula = verified_cell.find(f"{{{NS_MAIN}}}f")
            if formula is None or formula.text != formula_text:
                contract_mismatch_count += 1
        else:
            value = verified_cell.find(f"{{{NS_MAIN}}}v")
            if value is None or value.text != str(entry["value"]):
                contract_mismatch_count += 1
    if contract_mismatch_count:
        raise ValueError(
            f"XLSX_TEXT_CONTRACT_PARITY_BLOCKER:{path.name}:{contract_mismatch_count}"
        )

    evidence_root = sheet_roots["02_证据"]
    evidence_max_row = max(
        int(row.attrib["r"]) for row in evidence_root.findall(f".//{{{NS_MAIN}}}row")
    )
    invalid_hyperlink_targets = 0
    for node in hyperlink_index.values():
        match = re.fullmatch(r"'02_证据'!A(\d+)", node.attrib.get("location", ""))
        if not match or not 1 <= int(match.group(1)) <= evidence_max_row:
            invalid_hyperlink_targets += 1
    if invalid_hyperlink_targets:
        raise ValueError(
            f"INTERNAL_HYPERLINK_TARGET_BLOCKER:{path.name}:{invalid_hyperlink_targets}"
        )
    return {
        "filename": path.name,
        "bytes": path.stat().st_size,
        "sha256": _sha256(path),
        "sheet_order": list(sheet_paths),
        "visible_sheet_count": 5,
        "enum_sheet_hidden": enum_hidden,
        "sheet_protection_count": sum(
            1
            for sheet_path in sheet_paths.values()
            if ET.fromstring(parts[sheet_path]).find(f"{{{NS_MAIN}}}sheetProtection")
            is not None
        ),
        "data_validation_count": len(validations),
        "internal_hyperlink_count": internal_hyperlink_count,
        "logic_qa_formula_count": qa_formula_count,
        "annotation_row_count": len(payload["rows"]),
        "candidate_visible_count": sum(
            bool(row["candidate_text"]) for row in payload["rows"]
        ),
        "snapshot_coverage": payload["snapshot_coverage"],
        "snapshot_full_text_count": sum(
            int(item["full_text_included"]) for item in payload["snapshot_qa"]
        ),
        "reviewer_visible_leakage_count": len(leaked),
        "macro_present": False,
        "protection": "PROTECTION_BEST_EFFORT / PASSWORDLESS_SHEET_PROTECTION",
        "editable_annotation_cell_count": editable_unlocked,
        "text_contract_entry_count": len(text_contract["entries"]),
        "text_contract_mismatch_count": contract_mismatch_count,
        "invalid_internal_hyperlink_target_count": invalid_hyperlink_targets,
    }


def _manifest(output: Path) -> dict[str, Any]:
    entries = []
    for path in sorted(output.rglob("*")):
        if not path.is_file() or path == output / "manifest" / "final_manifest.json":
            continue
        entries.append(
            {
                "path": path.relative_to(output).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": _sha256(path),
            }
        )
    aggregate = hashlib.sha256(
        "\n".join(f"{item['sha256']}  {item['path']}" for item in entries).encode(
            "utf-8"
        )
    ).hexdigest()
    return {
        "task_id": TASK_ID,
        "generated_at": _now(),
        "entry_count_excluding_manifest": len(entries),
        "physical_file_count_including_manifest": len(entries) + 1,
        "aggregate_sha256": aggregate,
        "entries": entries,
    }


def finalize(output: Path, exporter_source: Path) -> None:
    workbook_qa: dict[str, Any] = {}
    payloads: dict[str, dict[str, Any]] = {}
    for annotator in ("HUMAN-A01", "HUMAN-B01"):
        tag = annotator.replace("HUMAN-", "")
        payload = json.loads(
            (
                output
                / "control"
                / "workbook_payloads"
                / f"{annotator}_phase2_v3_payload.json"
            ).read_text(encoding="utf-8")
        )
        payloads[annotator] = payload
        workbook = (
            output
            / annotator
            / "phase2_v3_distribution"
            / f"PILOT4_AB_HUMAN_{tag}_PHASE2_ANNOTATION_WORKBOOK_V3.xlsx"
        )
        text_contract_path = (
            output
            / "qa"
            / "workbook_artifact_tool"
            / "cell_text_contract"
            / f"{annotator}.json"
        )
        text_contract = json.loads(text_contract_path.read_text(encoding="utf-8"))
        patch_workbook(
            workbook,
            text_contract_path,
        )
        workbook_qa[annotator] = _validate_patched_workbook(
            workbook, payload, text_contract
        )
    a = workbook_qa["HUMAN-A01"]
    b = workbook_qa["HUMAN-B01"]
    parity = {
        "normalized_semantic_parity": all(
            a[key] == b[key]
            for key in [
                "sheet_order",
                "visible_sheet_count",
                "enum_sheet_hidden",
                "sheet_protection_count",
                "data_validation_count",
                "internal_hyperlink_count",
                "logic_qa_formula_count",
                "annotation_row_count",
                "candidate_visible_count",
                "snapshot_coverage",
                "snapshot_full_text_count",
                "reviewer_visible_leakage_count",
                "macro_present",
                "protection",
                "editable_annotation_cell_count",
                "text_contract_entry_count",
                "text_contract_mismatch_count",
                "invalid_internal_hyperlink_target_count",
            ]
        ),
        "allowed_differences": [
            "annotator ID",
            "opaque IDs",
            "Candidate order",
            "Evidence order",
            "filename",
        ],
        "A_B_order_identical": [
            row["blind_review_id"] for row in payloads["HUMAN-A01"]["rows"]
        ]
        == [row["blind_review_id"] for row in payloads["HUMAN-B01"]["rows"]],
        "rule_change_count": 0,
        "canonical_enum_change_count": 0,
        "transport_semantic_change": False,
    }
    if not parity["normalized_semantic_parity"] or parity["A_B_order_identical"]:
        raise ValueError(f"AB_PHASE2_WORKBOOK_SEMANTIC_PARITY_BLOCKER:{parity}")
    _write_json(
        output / "qa" / "AB_PHASE2_WORKBOOK_SEMANTIC_PARITY_REPORT.json", parity
    )
    _write_json(
        output / "qa" / "workbook_structural_qa.json", {"status": "PASS", **workbook_qa}
    )

    export_target = output / "export" / exporter_source.name
    export_target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(exporter_source, export_target)
    _write_text(
        output / "export" / "README.md",
        """# Deterministic Phase2 XLSX to CSV exporter

Future use only, after raw XLSX byte lock:

```powershell
python export_pilot4_phase2_xlsx.py --input <locked-return.xlsx> --contract contracts/HUMAN-A01_phase2_export_contract.json --output <canonical-return.csv> --blocker-output <export-blocker.json>
```

The exporter reads only the explicit English display-to-canonical header contract, preserves annotator-local order, validates 72/72 IDs, enums, all reasons and minimum logic, and emits UTF-8 BOM with LF. It never exports Candidate, Evidence, Chinese helper columns or the QA formula.
""",
    )
    register_path = output / "register" / "PILOT4_A_B_DISTRIBUTION_REGISTER_V3.json"
    register = json.loads(register_path.read_text(encoding="utf-8"))
    register["A_PHASE2_V3_READY"] = True
    register["B_PHASE2_V3_READY"] = True
    register["PHASE2_V3_DISTRIBUTION_READY"] = True
    register["updated_at"] = _now()
    _write_json(register_path, register)
    _write_json(
        output / "qa" / "final_gate_qa.json",
        {
            "status": "PASS",
            "DUAL_PHASE1_LOCK_GATE": "PASS",
            "PHASE2_RELEASE_ALLOWED": True,
            "PHASE2_V3_DISTRIBUTION_READY": True,
            "A_workbook_qa": "PASS",
            "B_workbook_qa": "PASS",
            "A_B_semantic_parity": "PASS",
            "A_snapshot_coverage": "144/144",
            "B_snapshot_coverage": "144/144",
            "mapping_unlocked": False,
            "expected_v3_loaded": False,
            "agreement_computed": False,
            "A_PHASE2_DISTRIBUTED": False,
            "B_PHASE2_DISTRIBUTED": False,
            "ground_truth_created": False,
        },
    )
    _write_json(output / "manifest" / "final_manifest.json", _manifest(output))


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    prepare_parser = subparsers.add_parser("prepare")
    prepare_parser.add_argument("--handoff", type=Path, required=True)
    prepare_parser.add_argument("--v2-root", type=Path, required=True)
    prepare_parser.add_argument("--output", type=Path, required=True)
    finalize_parser = subparsers.add_parser("finalize")
    finalize_parser.add_argument("--output", type=Path, required=True)
    finalize_parser.add_argument("--exporter-source", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "prepare":
        prepare(args.handoff.resolve(), args.v2_root.resolve(), args.output.resolve())
    else:
        finalize(args.output.resolve(), args.exporter_source.resolve())
    print(json.dumps({"status": "PASS", "command": args.command}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
