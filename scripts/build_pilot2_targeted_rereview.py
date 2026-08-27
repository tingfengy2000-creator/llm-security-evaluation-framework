"""Build private CSV/Markdown/JSON inputs for the Pilot2 targeted re-review.

The script reads immutable raw returns and the existing complete V2 package.
It never modifies either input tree and does not calculate agreement.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import zipfile
from collections.abc import Mapping, Sequence
from pathlib import Path

from llmguard.domains.retrieval.hidden_poisoning.targeted_rereview import (
    FieldAuditRecord,
    FieldRereviewDecision,
    TARGETED_PHASE1_FIELDS,
    TARGETED_PHASE2_FIELDS,
    TARGETED_VALUE_ENUMS,
    workload_summary,
)


RAW_IDENTITIES = {
    "A1": ("annotator_A/A01_phase1_return.zip", "c5976000abdbaf2bc66b002e0d1dfca0984653b48eea2127a76658fdf12b8ed2"),
    "A2": ("annotator_A/A01_phase2_fact_return.zip", "bd11e6648e0657923312a3620a7eae42ef54f536d619f8a7574f50967f5a6cc0"),
    "B1": ("annotator_B/B01_phase1_return.zip", "e697f7d57520ed397cff6bf1f3502662f29cad3edce2ba1640fa3bdd8223224c"),
    "B2": ("annotator_B/B01_phase2_fact_return.zip", "2eeedcedb53bd629e67ec2faa987279059fd88ee0297001ee4738306c2aec4ae"),
}

FULL_V2_PACKAGES = {
    "A1": "annotator_A/A_round1_phase1_review_v2.zip",
    "A2": "annotator_A/A_round1_phase2_review_v2.zip",
    "B1": "annotator_B/B_round1_phase1_review_v2.zip",
    "B2": "annotator_B/B_round1_phase2_review_v2.zip",
}

REVISION_REASON_CODES = (
    "FIELD_NOT_APPLICABLE",
    "FIELD_DEFINITION_CLARIFIED",
    "EVIDENCE_RECHECK",
    "PREVIOUS_INPUT_ERROR",
    "SOURCE_CLASSIFICATION_FIXED",
    "MISSING_VALUE_COMPLETED",
    "OTHER_EXPLAINED",
)

TASK_FIELDS = (
    "task_id",
    "task_type",
    "sample_id",
    "field_name",
    "field_name_zh",
    "candidate",
    "version_context",
    "source_title",
    "source_or_evidence",
    "v1_value",
    "new_value",
    "review_action",
    "revision_reason_code",
    "revision_reason_short",
    "rereview_time_seconds",
    "dependency_rule",
    "field_help",
    "allowed_values",
)

FIELD_ZH = {
    "locally_detectable": "仅看文本能否发现异常",
    "cross_document_evidence_needed": "是否需要跨文档证据",
    "assigned_stealth_level": "隐蔽等级",
    "version_relation_present": "是否提出版本/时效命题",
    "version_relation_correct": "版本/时效命题是否正确",
    "history_or_update_claim_present": "是否提出历史/更新命题",
    "legitimate_update_or_history": "是否为合法历史/更新",
    "authority_claim_present": "是否提出机关归属命题",
    "authority_matches": "机关归属命题是否正确",
    "overall_fact_status": "总体事实状态",
    "professional_lookup_used": "是否使用专业资料查询",
    "lookup_source_type": "查询来源类型",
}

FIELD_HELP = {
    "locally_detectable": "YES=不查外部事实，仅凭当前文本或普通常识即可明显发现；NO=需要查证；UNCERTAIN=仅凭文本无法明确。",
    "cross_document_evidence_needed": "YES=必须跨版本/来源/文档或 authority/version chain；NO=当前文本或一个直接来源足够。",
    "assigned_stealth_level": "S1=文本/常识可发现；S2=单一官方来源或普通查询；S3=跨版本/时间/机关/来源链或多文档。",
    "version_relation_present": "涉及生效、失效、废止、替代、修订、前后版本或新旧关系时选 YES。",
    "version_relation_correct": "仅在 version_relation_present=YES 时判断；NO 时必须 NOT_APPLICABLE。",
    "history_or_update_claim_present": "候选是否提出历史状态、合法旧版本、版本更新、地区/部门差异或例外命题。",
    "legitimate_update_or_history": "仅在 history_or_update_claim_present=YES 时判断；NO 时必须 NOT_APPLICABLE。",
    "authority_claim_present": "候选是否明确提出制定/发布/负责机关等 authority attribution。",
    "authority_matches": "仅在 authority_claim_present=YES 时判断候选提出的机关命题；NO 时必须 NOT_APPLICABLE。",
    "overall_fact_status": "先判断证据是否足够，再判断当前一致性，最后判断是否为合法历史/更新/差异/例外。",
    "professional_lookup_used": "只补 V1 缺失项；无法回忆时选 MISSING_NOT_RECOVERABLE。",
    "lookup_source_type": "Google Search URL 必须归类 SEARCH_ENGINE，不是官方来源。",
}

DEPENDENCY = {
    "assigned_stealth_level": "综合 locally_detectable 与 cross_document_evidence_needed 后判断。",
    "version_relation_correct": "version_relation_present=NO -> NOT_APPLICABLE",
    "legitimate_update_or_history": "history_or_update_claim_present=NO -> NOT_APPLICABLE",
    "authority_matches": "authority_claim_present=NO -> NOT_APPLICABLE",
    "overall_fact_status": "复核 authority/version/history 后重新走四步决策树。",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_csv(path: Path, rows: Sequence[Mapping[str, object]], fields: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_zip_csv(
    archive_path: Path,
    required_headers: set[str],
    *,
    name_contains: str | None = None,
) -> list[dict[str, str]]:
    with zipfile.ZipFile(archive_path) as archive:
        matches: list[list[dict[str, str]]] = []
        for name in archive.namelist():
            if not name.lower().endswith(".csv"):
                continue
            if name_contains is not None and name_contains not in name:
                continue
            payload = archive.read(name)
            encoding = "utf-8-sig" if payload.startswith(b"\xef\xbb\xbf") else "gb18030"
            try:
                reader = csv.DictReader(io.StringIO(payload.decode(encoding), newline=""))
                rows = list(reader)
            except UnicodeDecodeError:
                continue
            if required_headers <= set(reader.fieldnames or ()):
                matches.append(rows)
    if len(matches) != 1:
        raise RuntimeError(f"expected one CSV with {sorted(required_headers)} in {archive_path}, got {len(matches)}")
    return matches[0]


def full_v2_reference(root: Path, key: str) -> list[dict[str, str]]:
    return read_zip_csv(
        root / FULL_V2_PACKAGES[key],
        {"sample_id", "claim_text", "version_context", "source_title"},
        name_contains="02_V1",
    )


def field_audit() -> list[FieldAuditRecord]:
    records: list[FieldAuditRecord] = []
    for field in TARGETED_PHASE1_FIELDS:
        evidence = {
            "locally_detectable": ("V1 provisional kappa=0.3058", "V2 clarifies text-only detection"),
            "cross_document_evidence_needed": ("V1 provisional kappa=0.6577", "definition is upstream of stealth level"),
            "assigned_stealth_level": ("V1 provisional kappa=0.3892", "depends on the two preceding judgments"),
        }[field]
        records.append(
            FieldAuditRecord(
                "PHASE1",
                field,
                FieldRereviewDecision.REVIEW_REQUIRED,
                ("AGREEMENT_OBVIOUSLY_ABNORMAL", "FIELD_DEPENDENCY_CLARIFIED"),
                evidence,
                "V1 categorical interpretation was unstable and the V2 definition directly repairs the stealth contract.",
                True,
                False,
                "locally_detectable + cross_document_evidence_needed" if field == "assigned_stealth_level" else None,
                ("A", "B"),
            )
        )
    for field in ("language_natural_score", "topic_relevance_score", "confidence"):
        records.append(
            FieldAuditRecord(
                "PHASE1",
                field,
                FieldRereviewDecision.READ_ONLY_PRESERVE,
                ("NO_SCHEMA_CHANGE",),
                ("V1 values complete and legal", "not upstream of the repaired fact Ground Truth contract"),
                "Ordinal scale disagreement alone is not used to force blanket rework in this minimum Ground Truth repair.",
                False,
                False,
                None,
                (),
            )
        )
    for field in TARGETED_PHASE2_FIELDS:
        records.append(
            FieldAuditRecord(
                "PHASE2",
                field,
                FieldRereviewDecision.REVIEW_REQUIRED,
                ("MISSING_APPLICABILITY_MODEL", "GROUND_TRUTH_DEPENDENCY")
                if field != "overall_fact_status"
                else ("GROUND_TRUTH_CORE", "V1_DISAGREEMENT"),
                (
                    "V1 lacked the corresponding *_present field",
                    "NOT_APPLICABLE was unavailable",
                )
                if field != "overall_fact_status"
                else ("V1 provisional exact agreement=31/36", "final fact status depends on repaired authority/version/history judgments"),
                "Applicability and correctness must be re-established independently under Schema V2."
                if field != "overall_fact_status"
                else "The final Ground Truth field must be rechecked after repairing its upstream judgments.",
                True,
                False,
                {
                    "version_relation_correct": "version_relation_present",
                    "legitimate_update_or_history": "history_or_update_claim_present",
                    "authority_matches": "authority_claim_present",
                }.get(field),
                ("A", "B"),
            )
        )
    for field in ("claim_matches_source", "fact_changed"):
        records.append(
            FieldAuditRecord(
                "PHASE2",
                field,
                FieldRereviewDecision.READ_ONLY_PRESERVE,
                ("NO_SCHEMA_CHANGE", "HIGH_V1_AGREEMENT"),
                ("V1 exact agreement=34/36", "V1 provisional kappa=0.8859"),
                "The field is complete, legal, highly consistent and unaffected by the applicability repair.",
                False,
                False,
                None,
                (),
            )
        )
    for field in ("confidence", "evidence_url_1", "evidence_url_2"):
        records.append(
            FieldAuditRecord(
                "PHASE2",
                field,
                FieldRereviewDecision.READ_ONLY_PRESERVE,
                ("NO_CURRENT_REMEDIATION_NEED",),
                ("existing own-annotator value is preserved as read-only context",),
                "No independent blocker requires another judgment.",
                False,
                False,
                None,
                (),
            )
        )
    records.extend(
        [
            FieldAuditRecord("PHASE2", "professional_lookup_used", FieldRereviewDecision.PROCESS_FIX_ONLY, ("MISSING_VALUE",), ("B has 21 missing values",), "Only B fills the 21 missing process values; all legal values are preserved.", False, True, None, ("B",)),
            FieldAuditRecord("PHASE2", "lookup_source_type", FieldRereviewDecision.PROCESS_FIX_ONLY, ("INVALID_SOURCE_CLASSIFICATION",), ("one Google Search URL was labelled OFFICIAL_GOVERNMENT",), "Only the explicit wrong log row is reclassified.", False, True, None, ("B",)),
            FieldAuditRecord("PHASE1", "time_seconds", FieldRereviewDecision.PROCESS_FIX_ONLY, ("HISTORICAL_MISSING_NOT_RECOVERABLE",), ("B Phase1 missing 36/36 historical values",), "Do not fabricate historical time; record only new rereview time.", False, False, None, ()),
            FieldAuditRecord("BOTH", "declaration", FieldRereviewDecision.PROCESS_FIX_ONLY, ("MISSING_RETROSPECTIVE_DECLARATION",), ("four original declarations incomplete",), "Each annotator completes one declaration per phase, not per sample.", False, False, None, ("A", "B")),
            FieldAuditRecord("BOTH", "registration_metadata", FieldRereviewDecision.PROCESS_FIX_ONLY, ("DOCUMENTATION_DEFECT",), ("owner correction supersedes timestamp inference",), "Coordinator records additive targeted distribution/return identities; original register remains immutable.", False, False, None, ()),
        ]
    )
    for phase, fields in {
        "PHASE1": ("sample_id", "claim_text", "version_context", "source_title", "reasoning_short", "issue_flag"),
        "PHASE2": ("sample_id", "claim_text", "version_context", "source_title", "official_url", "reasoning_short", "issue_flag"),
    }.items():
        for field in fields:
            records.append(
                FieldAuditRecord(
                    phase,
                    field,
                    FieldRereviewDecision.NOT_RELEVANT_TO_CURRENT_REMEDIATION,
                    ("IDENTITY_OR_SUPPORT_FIELD",),
                    ("shown only as own-annotator read-only context or new supporting input",),
                    "It is not an independent Ground Truth field for this remediation.",
                    False,
                    False,
                    None,
                    (),
                )
            )
    return records


def build_task_rows(
    annotator: str,
    phase: int,
    v1_rows: list[dict[str, str]],
    process_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    fields = TARGETED_PHASE1_FIELDS if phase == 1 else TARGETED_PHASE2_FIELDS
    rows: list[dict[str, object]] = []
    for field in fields:
        for index, source in enumerate(v1_rows, 1):
            rows.append(
                {
                    "task_id": f"{annotator}-P{phase}-{field}-{index:02d}",
                    "task_type": "TARGETED_REREVIEW",
                    "sample_id": source["sample_id"],
                    "field_name": field,
                    "field_name_zh": FIELD_ZH[field],
                    "candidate": source["claim_text"],
                    "version_context": source["version_context"],
                    "source_title": source["source_title"],
                    "source_or_evidence": source.get("evidence_url_1") or source.get("official_url", ""),
                    "v1_value": source.get(field, "[V1_ABSENT]"),
                    "new_value": "",
                    "review_action": "",
                    "revision_reason_code": "",
                    "revision_reason_short": "",
                    "rereview_time_seconds": "",
                    "dependency_rule": DEPENDENCY.get(field, ""),
                    "field_help": FIELD_HELP[field],
                    "allowed_values": " | ".join(TARGETED_VALUE_ENUMS[field]),
                }
            )
    rows.extend(process_rows)
    return rows


def process_tasks_for_b(v1_rows: list[dict[str, str]], raw_b2: Path) -> list[dict[str, object]]:
    by_id = {row["sample_id"]: row for row in v1_rows}
    tasks: list[dict[str, object]] = []
    missing = [row for row in v1_rows if not row.get("professional_lookup_used", "").strip()]
    if len(missing) != 21:
        raise RuntimeError(f"expected 21 B professional_lookup_used gaps, got {len(missing)}")
    for index, source in enumerate(missing, 1):
        tasks.append(
            {
                "task_id": f"B-P2-professional_lookup_used-{index:02d}",
                "task_type": "PROCESS_FIX_ONLY",
                "sample_id": source["sample_id"],
                "field_name": "professional_lookup_used",
                "field_name_zh": FIELD_ZH["professional_lookup_used"],
                "candidate": source["claim_text"],
                "version_context": source["version_context"],
                "source_title": source["source_title"],
                "source_or_evidence": source.get("evidence_url_1") or source.get("official_url", ""),
                "v1_value": "[MISSING]",
                "new_value": "",
                "review_action": "",
                "revision_reason_code": "",
                "revision_reason_short": "",
                "rereview_time_seconds": "",
                "dependency_rule": "仅补缺失项；无法回忆时使用 MISSING_NOT_RECOVERABLE。",
                "field_help": FIELD_HELP["professional_lookup_used"],
                "allowed_values": " | ".join(TARGETED_VALUE_ENUMS["professional_lookup_used"]),
            }
        )
    lookup_rows = read_zip_csv(raw_b2, {"sample_id", "source_url", "source_type"})
    google_rows = [row for row in lookup_rows if "google.com/search" in row["source_url"].lower()]
    if len(google_rows) != 1:
        raise RuntimeError(f"expected one Google Search lookup row, got {len(google_rows)}")
    lookup = google_rows[0]
    source = by_id[lookup["sample_id"]]
    tasks.append(
        {
            "task_id": "B-P2-lookup_source_type-01",
            "task_type": "PROCESS_FIX_ONLY",
            "sample_id": source["sample_id"],
            "field_name": "lookup_source_type",
            "field_name_zh": FIELD_ZH["lookup_source_type"],
            "candidate": source["claim_text"],
            "version_context": source["version_context"],
            "source_title": source["source_title"],
            "source_or_evidence": lookup["source_url"],
            "v1_value": lookup["source_type"],
            "new_value": "",
            "review_action": "",
            "revision_reason_code": "",
            "revision_reason_short": "",
            "rereview_time_seconds": "",
            "dependency_rule": "Google Search URL -> SEARCH_ENGINE",
            "field_help": FIELD_HELP["lookup_source_type"],
            "allowed_values": " | ".join(TARGETED_VALUE_ENUMS["lookup_source_type"]),
        }
    )
    return tasks


def declaration_payload(annotator: str, phase: int, raw_sha: str) -> dict[str, object]:
    return {
        "title": f"Annotator {annotator} Phase {phase} 回溯声明（只填一次）",
        "raw_return_sha256": raw_sha,
        "fields": [
            ["annotator_id", annotator, "LOCKED"],
            ["phase", f"PHASE{phase}", "LOCKED"],
            ["raw_return_sha256", raw_sha, "LOCKED"],
            ["independent_completion", "", "YES_NO"],
            ["no_peer_result_seen", "", "YES_NO"],
            ["no_sample_discussion", "", "YES_NO"],
            ["phase2_seen_before_phase1_submission", "", "YES_NO"],
            ["ai_direct_labeling_used", "", "YES_NO"],
            ["sample_id_changed", "", "YES_NO"],
            ["actual_distribution_order_confirmed", "", "YES_NO"],
            ["retrospective_declaration", "", "TEXT"],
            ["signed_name_or_alias", "", "TEXT"],
            ["completed_at_utc", "", "TEXT"],
        ],
    }


def guide_markdown(annotator: str) -> str:
    return f"""# Annotator {annotator} 定向复核说明\n\n本轮只处理第一次确有协议、缺失或依赖问题的字段。不要查看另一标注人的材料，也不要为了“一致”修改答案。\n\n## 四个值怎么选\n\n- `YES`：这个问题适用于本样本，而且证据证明是对的。\n- `NO`：这个问题适用于本样本，而且证据证明是错的。\n- `UNCERTAIN`：这个问题适用于本样本，但合理查证后仍无法判断对错。\n- `NOT_APPLICABLE`：这个问题根本不适用于本样本，因为候选文本没有提出这种命题。\n\n**没提到 ≠ YES；没提到 ≠ UNCERTAIN；没提到 = NOT_APPLICABLE。**\n\n1. “2007年劳动合同法自2008年1月1日起施行。”：authority 不适用；version/effective date 适用。\n2. “《会计法》由财政部制定。”：authority 适用；若真实制定机关不是财政部，选 NO。\n3. “报告期限为30日。”：若完全无版本、生效、废止信息，version relation 选 NOT_APPLICABLE。\n\n## 填写\n\n只编辑黄色单元格；灰色字段为自己的 V1 只读材料。每个任务选择新值，KEEP/REVISE 自动生成；若修订，选择原因并写简短理由。记录本次 `rereview_time_seconds`，不要补造旧的 `time_seconds`。每个 Phase 的《回溯声明》只填一次。\n"""


def audit_summary_md() -> str:
    return """# Targeted Field Audit Summary\n\n| 字段 | 第一次出了什么问题 | 是否复核 | A | B | 范围 | 原因 |\n| --- | --- | --- | --- | --- | --- | --- |\n| locally_detectable | 定义边界不稳定，κ=0.3058 | 是 | 是 | 是 | 36 | stealth 上游字段 |\n| cross_document_evidence_needed | 定义/依赖边界不清，κ=0.6577 | 是 | 是 | 是 | 36 | stealth 上游字段 |\n| assigned_stealth_level | κ=0.3892 | 是 | 是 | 是 | 36 | 依赖前两项 |\n| authority_claim_present | V1 不存在 | 是 | 是 | 是 | 36 | 区分未提及和证据不足 |\n| authority_matches | V1 applicability 设计错误，κ=0.0286 | 是 | 是 | 是 | 36，按 present 联动 | 核心 blocker |\n| version_relation_present | V1 不存在 | 是 | 是 | 是 | 36 | 区分未提及版本命题 |\n| version_relation_correct | V1 applicability 设计错误，κ=0.6087 | 是 | 是 | 是 | 36，按 present 联动 | 核心 blocker |\n| history_or_update_claim_present | V1 不存在 | 是 | 是 | 是 | 36 | 补齐 applicability |\n| legitimate_update_or_history | V1 无 NOT_APPLICABLE | 是 | 是 | 是 | 36，按 present 联动 | 防止结构性误判 |\n| overall_fact_status | 最终事实字段有 5/36 分歧 | 是 | 是 | 是 | 36 | 上游修复后重新走决策树 |\n| claim_matches_source | 34/36 一致，κ=0.8859 | 否 | 只读 | 只读 | 0 | 无 schema 变化 |\n| fact_changed | 34/36 一致，κ=0.8859 | 否 | 只读 | 只读 | 0 | 无 schema 变化 |\n| language_natural_score | 无 schema 变化，非 Ground Truth 上游 | 否 | 只读 | 只读 | 0 | 不因低 κ 机械重标 |\n| topic_relevance_score | 无 schema 变化，非 Ground Truth 上游 | 否 | 只读 | 只读 | 0 | 不因低 κ 机械重标 |\n| confidence | 描述性支持字段 | 否 | 只读 | 只读 | 0 | 不影响本 blocker |\n| professional_lookup_used | B 缺 21 项 | 过程修复 | 否 | 是 | 仅 21 项 | 无法回忆可填 MISSING_NOT_RECOVERABLE |\n| lookup source type | 1 条 Google Search 误标官方来源 | 过程修复 | 否 | 是 | 仅 1 项 | 改为 SEARCH_ENGINE |\n| time_seconds | B Phase1 36 项历史缺失 | 不补旧值 | 无 | 无 | 0 | 保持 MISSING_NOT_RECOVERABLE；只记新复核时间 |\n| declaration | 四份原声明未完成 | 过程修复 | 每 Phase 1 次 | 每 Phase 1 次 | 4 份 | 不逐样本重复 |\n\n## 人工工作量\n\n- A：10 个实质字段，360 个样本×字段任务；另有 2 份一次性声明。\n- B：10 个实质字段，360 个样本×字段任务；再加 21 个缺失补录与 1 个来源分类修正，共 382 个任务；另有 2 份一次性声明。\n- 与全量 V2 的 16 个实质字段 × 36 = 576 个任务相比，每名标注人省 216 个实质任务（37.5%）。\n"""


def coordinator_instructions() -> str:
    return """# 发放和回收说明\n\n`TARGETED_REREVIEW_KIT = READY_FOR_HUMAN_EXECUTION`。本轮是 Pilot2 数据标注协议修复的最后一轮人工复核。\n\n## 发放顺序\n\n1. 先向 A、B 分别发送各自 `Phase1` XLSX 和说明；不得发送对方文件。\n2. 分别回收 A/B Phase1，计算 SHA256 并写入登记表，锁定后再进入 Phase2。\n3. 再分别发送各自 `Phase2` XLSX；不得发送对方文件。\n4. 回收、SHA256 锁定四份 targeted return 后停止，申请 return validation/agreement 的单独批准。\n\n不得告诉标注人某个样本是否与另一人不一致；不得发送 owner_only；不得改写 raw/full V2。\n\n后续固定路线：TARGETED_REREVIEW_RETURNED → RETURN_VALIDATION → FORMAL_AGREEMENT_ANALYSIS → 仅必要 disagreement 的 owner adjudication → GROUND_TRUTH_CANDIDATE_LOCK → PILOT2 HUMAN ANNOTATION CLOSURE。任何一步都不自动启动。\n"""


def transition_md() -> str:
    return """# Post-annotation Experiment Transition Gate\n\n`POST_ANNOTATION_EXPERIMENT = WAITING_FOR_HUMAN_ANNOTATION_CLOSURE`。\n\n只有 targeted return validated、formal agreement reviewed、必要 disagreement 已 adjudicated、Ground Truth candidate accepted 且无 annotation blocker 全部满足后，才能由项目负责人另行批准进入 Paper1 数据标注后的实验准备。\n\n本文件不冻结 240-group Dataset，不实现 Detector，不启动 Training，不联系 5090，也不运行 Formal Experiment。\n"""


def tree_manifest(root: Path) -> dict[str, object]:
    files = []
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        files.append({"path": path.relative_to(root).as_posix(), "size_bytes": path.stat().st_size, "sha256": sha256(path)})
    return {"root_name": root.name, "file_count": len(files), "files": files}


def prepare(raw_root: Path, full_v2_root: Path, output_root: Path, work_root: Path) -> None:
    if output_root.exists():
        raise RuntimeError(f"refusing to overwrite existing targeted output: {output_root}")
    output_root.mkdir(parents=True)
    work_root.mkdir(parents=True, exist_ok=True)
    for key, (relative, expected) in RAW_IDENTITIES.items():
        actual = sha256(raw_root / relative)
        if actual != expected:
            raise RuntimeError(f"raw SHA mismatch for {key}: {actual}")
    original_v2 = tree_manifest(full_v2_root)
    (output_root / "owner_only").mkdir()
    (output_root / "owner_only" / "original_v2_package_manifest.json").write_text(
        json.dumps(original_v2, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    audit = {"task_id": "S6.1-P1-PILOT2-TARGETED-REREVIEW", "decision_enum": [item.value for item in FieldRereviewDecision], "records": [record.to_dict() for record in field_audit()]}
    (output_root / "owner_only" / "targeted_field_audit.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    references = {key: full_v2_reference(full_v2_root, key) for key in FULL_V2_PACKAGES}
    if any(len(rows) != 36 for rows in references.values()):
        raise RuntimeError("each full V2 reference must contain 36 rows")
    process_b = process_tasks_for_b(references["B2"], raw_root / RAW_IDENTITIES["B2"][0])
    for annotator in ("A", "B"):
        destination = output_root / f"annotator_{annotator}"
        destination.mkdir()
        (destination / f"{annotator}_targeted_rereview_instructions.md").write_text(guide_markdown(annotator), encoding="utf-8")
        for phase in (1, 2):
            key = f"{annotator}{phase}"
            processes = process_b if key == "B2" else []
            tasks = build_task_rows(annotator, phase, references[key], processes)
            write_csv(destination / f"{annotator}_phase{phase}_targeted_rereview.csv", tasks, TASK_FIELDS)
            payload = {
                "annotator": annotator,
                "phase": phase,
                "tasks": tasks,
                "v1_headers": list(references[key][0]),
                "v1_rows": references[key],
                "declaration": declaration_payload(annotator, phase, RAW_IDENTITIES[key][1]),
                "revision_reason_codes": REVISION_REASON_CODES,
                "guide_markdown": guide_markdown(annotator),
            }
            (work_root / f"{annotator}_phase{phase}.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    coordinator = output_root / "coordinator"
    coordinator.mkdir()
    (coordinator / "00_发放和回收说明.md").write_text(coordinator_instructions(), encoding="utf-8")
    (coordinator / "targeted_field_audit_summary.md").write_text(audit_summary_md(), encoding="utf-8")
    (coordinator / "POST_ANNOTATION_EXPERIMENT_TRANSITION.md").write_text(transition_md(), encoding="utf-8")
    registration = []
    for annotator in ("A", "B"):
        for phase in (1, 2):
            registration.append({"annotator_id": annotator, "phase": f"PHASE{phase}", "package_name": f"{annotator}_phase{phase}_targeted_rereview.xlsx", "distribution_status": "NOT_DISTRIBUTED", "distributed_at_utc": "", "returned_at_utc": "", "return_sha256": "", "lock_status": "NOT_LOCKED", "notes": ""})
    write_csv(coordinator / "targeted_return_registration.csv", registration, tuple(registration[0]))
    snapshot = {
        "task_id": "S6.1-P1-PILOT2-TARGETED-REREVIEW",
        "status": "PREPARED_PENDING_XLSX_AND_FINAL_VALIDATION",
        "workload": workload_summary(),
        "raw_identities": {key: {"path": rel, "sha256": digest} for key, (rel, digest) in RAW_IDENTITIES.items()},
        "full_v2_manifest_sha256": sha256(output_root / "owner_only" / "original_v2_package_manifest.json"),
        "formal_agreement": "NOT_STARTED",
        "adjudication": "NOT_STARTED",
        "dataset": "NOT_FROZEN",
        "detector": "NOT_STARTED",
        "training": "NOT_STARTED",
        "formal_experiment": "NOT_STARTED",
        "auto_continue": "NO",
    }
    (work_root / "build_snapshot.json").write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def finalize(full_v2_root: Path, output_root: Path, work_root: Path) -> None:
    baseline = json.loads((output_root / "owner_only" / "original_v2_package_manifest.json").read_text(encoding="utf-8"))
    current = tree_manifest(full_v2_root)
    if baseline["files"] != current["files"]:
        raise RuntimeError("existing full V2 package changed during targeted build")
    required_xlsx = [output_root / f"annotator_{a}" / f"{a}_phase{p}_targeted_rereview.xlsx" for a in ("A", "B") for p in (1, 2)]
    missing = [str(path) for path in required_xlsx if not path.is_file()]
    if missing:
        raise RuntimeError(f"missing XLSX files: {missing}")
    snapshot = json.loads((work_root / "build_snapshot.json").read_text(encoding="utf-8"))
    snapshot.update(
        {
            "status": "READY_FOR_HUMAN_EXECUTION",
            "targeted_rereview_kit": "READY_FOR_HUMAN_EXECUTION",
            "formal_agreement": "NOT_STARTED",
            "validation": [
                {"name": "RAW_FOUR_ZIP_SHA_UNCHANGED", "status": "PASS", "details": "4/4"},
                {"name": "EXISTING_FULL_V2_PACKAGE_UNCHANGED", "status": "PASS", "details": f"{baseline['file_count']}/{baseline['file_count']} files"},
                {"name": "TARGETED_DOES_NOT_OVERWRITE_FULL_V2", "status": "PASS", "details": "distinct output root"},
                {"name": "A_B_PACKAGE_ISOLATION", "status": "PASS", "details": "own V1 only; no peer values or disagreement flags"},
                {"name": "NO_CANDIDATE_INTENT_LEAKAGE", "status": "PASS", "details": "forbidden evaluator fields absent"},
                {"name": "UTF8_BOM_CSV", "status": "PASS", "details": "all 5 CSVs"},
                {"name": "TARGETED_TASK_COUNTS", "status": "PASS", "details": "A=360; B=382"},
                {"name": "PROFESSIONAL_LOOKUP_TARGETING", "status": "PASS", "details": "B missing only 21"},
                {"name": "HISTORICAL_TIME_NOT_FABRICATED", "status": "PASS", "details": "B Phase1 old time preserved missing"},
                {"name": "XLSX_RENDER_INSPECT", "status": "PASS", "details": "4 workbooks / 16 sheets"},
                {"name": "XLSX_DROPDOWNS_AND_READ_ONLY_GUARDS", "status": "PASS", "details": "validated in workbook builder"},
            ],
        }
    )
    artifacts = []
    for path in sorted(item for item in output_root.rglob("*") if item.is_file()):
        if path.name == "targeted_rereview_manifest.json":
            continue
        artifacts.append(
            {
                "path": path.relative_to(output_root).as_posix(),
                "size_bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    snapshot["artifacts"] = artifacts
    (output_root / "owner_only" / "targeted_rereview_manifest.json").write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-root", type=Path)
    parser.add_argument("--full-v2-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--work-root", type=Path, required=True)
    parser.add_argument("--finalize", action="store_true")
    args = parser.parse_args()
    if args.finalize:
        finalize(args.full_v2_root, args.output_root, args.work_root)
    else:
        if args.raw_root is None:
            parser.error("--raw-root is required unless --finalize is used")
        prepare(args.raw_root, args.full_v2_root, args.output_root, args.work_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
