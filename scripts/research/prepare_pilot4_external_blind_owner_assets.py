"""Prepare owner-only assets for a genuinely external Pilot4 blind review.

This is an owner-side preparation program.  It may read internal identities only
to create and validate an isolated opaque mapping.  It never creates annotation
answers and never loads the expected annotation contract.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, datetime
from hashlib import sha256
import gzip
import hmac
import json
import os
from pathlib import Path
import re
import secrets
import subprocess
from typing import Any, Mapping, Sequence
from urllib.request import Request, urlopen

from llmguard.domains.retrieval.hidden_poisoning.annotation_v31 import (
    COMBINED_CLAIM_STATUS,
    EVIDENCE_SELECTION,
    LOCAL_INTERNAL_CONFLICT,
    MINIMUM_EXTERNAL_EVIDENCE,
    OVERALL_FACT_STATUS,
    PHASE1_ISSUE,
    PHASE2_ISSUE,
    TEXT_NATURALNESS,
)
from llmguard.domains.retrieval.hidden_poisoning.external_blind_review import (
    MANUAL_FIELDS,
    PHASE1_FIELDS,
    PHASE2_FIELDS,
    TITLE_ORIGINS,
    adjacent_same_group_count,
    blind_review_id,
    canonical_sha256,
    deterministic_constrained_blind_order,
    evidence_should_swap,
    extract_html_title,
    extract_pdf_title,
    lexical_duplicate_qa,
    order_profile,
    validate_packet_rows,
)


TASK_ID = "PILOT4-EXTERNAL-BLIND-OWNER-REVIEW-PACKET-01"
NAMESPACE = "paper1_pilot4_external_blind_review_packet_20260902"
STATUS = (
    "PILOT4_EXTERNAL_BLIND_REVIEW_PACKET_READY / "
    "WAITING_FOR_EXTERNAL_OWNER_REVIEW / NO_HUMAN_DISTRIBUTION"
)
HISTORICAL_COMMIT = "c1b1245c061b7bec096b12894ea153499c2af2e2"


def utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def write_jsonl(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(
            json.dumps(dict(row), ensure_ascii=False, separators=(",", ":")) + "\n"
            for row in rows
        ),
        encoding="utf-8",
    )


def file_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def tree_identity(root: Path) -> dict[str, Any]:
    files = [path for path in sorted(root.rglob("*")) if path.is_file()]
    return {
        "root": str(root),
        "file_count": len(files),
        "files": {
            path.relative_to(root).as_posix(): {
                "size": path.stat().st_size,
                "sha256": file_sha256(path),
            }
            for path in files
        },
    }


def source_paths(source_root: Path) -> dict[str, Path]:
    return {
        "candidates": source_root / "candidates" / "candidates_v3_1_additive.jsonl",
        "pool_a": source_root / "evidence" / "candidate_neutral_pool_a.json",
        "pool_b": source_root / "evidence" / "candidate_neutral_pool_b.json",
        "candidate_qa": source_root
        / "qa"
        / "candidate_meta_cue_and_self_containment_qa.json",
    }


def build_title_plan(source_root: Path, output: Path) -> dict[str, Any]:
    paths = source_paths(source_root)
    pool = load_json(paths["pool_a"])["items"]
    urls = sorted({str(item["official_source_url"]) for item in pool})
    if len(pool) != 144 or len(urls) != 56:
        raise ValueError("TITLE_PLAN_CARDINALITY_BLOCKER")
    plan = {
        "task_id": TASK_ID,
        "source_namespace": source_root.name,
        "source_pool_sha256": file_sha256(paths["pool_a"]),
        "visible_slot_count": len(pool),
        "unique_source_url_count": len(urls),
        "sources": [{"source_url": url} for url in urls],
    }
    write_json(output / "title_provenance" / "source_title_plan.json", plan)
    return plan


def _node_fetch_fallback(url: str, output: Path) -> tuple[bytes, str, int, str]:
    node_executable = os.environ.get("LLMGUARD_NODE_EXECUTABLE")
    if not node_executable:
        raise ValueError("NODE_FETCH_FALLBACK_NOT_CONFIGURED")
    helper = Path(__file__).with_name("fetch_official_source_snapshot.mjs")
    temporary = (
        output
        / "title_provenance"
        / f"node_fetch_{canonical_sha256(url.encode('utf-8'))}.bin"
    )
    temporary.parent.mkdir(parents=True, exist_ok=True)
    completed = subprocess.run(  # noqa: S603 - fixed helper and approved URL plan
        [node_executable, str(helper), url, str(temporary)],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=150,
    )
    metadata = json.loads(completed.stdout.strip())
    body = temporary.read_bytes()
    temporary.unlink()
    if canonical_sha256(body) != metadata["sha256"]:
        raise ValueError("NODE_FETCH_HASH_BLOCKER")
    return (
        body,
        str(metadata["contentType"]),
        int(metadata["status"]),
        str(metadata["finalUrl"]),
    )


def fetch_source(url: str, output: Path) -> tuple[bytes, str, int, str]:
    last_error: Exception | None = None
    for _attempt in range(3):
        try:
            request = Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 LLMGuard-Research-Title-Provenance/1.0",
                    "Accept": "text/html,application/pdf;q=0.9,*/*;q=0.5",
                },
            )
            with urlopen(request, timeout=45) as response:  # noqa: S310 - approved URLs
                body = response.read()
                status = int(getattr(response, "status", 200))
                content_type = str(response.headers.get("Content-Type", ""))
                final_url = str(response.geturl())
            if body.startswith(b"\x1f\x8b"):
                body = gzip.decompress(body)
            if status == 200 and len(body) >= 256:
                return body, content_type, status, final_url
            last_error = ValueError(f"HTTP_{status}_BYTES_{len(body)}")
        except Exception as error:  # pragma: no cover - network-specific evidence
            last_error = error
    try:
        return _node_fetch_fallback(url, output)
    except Exception as fallback_error:
        raise ValueError(
            f"SOURCE_ACCESS_BLOCKER:{url}:{last_error}:NODE_FALLBACK:{fallback_error}"
        ) from fallback_error


def acquire_one_title(url: str, output: Path) -> dict[str, Any]:
    body, content_type, status, final_url = fetch_source(url, output)
    is_pdf = "pdf" in content_type.casefold() or final_url.casefold().endswith(".pdf")
    extracted = (
        extract_pdf_title(body) if is_pdf else extract_html_title(body, content_type)
    )
    if extracted.title_origin not in TITLE_ORIGINS:
        raise ValueError("SOURCE_TITLE_ORIGIN_BLOCKER")
    snapshot_hash = canonical_sha256(body)
    suffix = ".pdf" if is_pdf else ".html"
    snapshot_path = (
        output / "title_provenance" / "source_snapshots" / f"{snapshot_hash}{suffix}"
    )
    snapshot_path.parent.mkdir(parents=True, exist_ok=True)
    snapshot_path.write_bytes(body)
    return {
        "source_url": url,
        "final_url": final_url,
        "display_title": extracted.display_title,
        "title_origin": extracted.title_origin,
        "exact_extracted_heading": extracted.exact_source_text,
        "title_source_text_hash": extracted.title_source_text_hash,
        "source_snapshot_hash": snapshot_hash,
        "snapshot_relative_path": snapshot_path.relative_to(output).as_posix(),
        "retrieved_at": utc_now(),
        "http_status": status,
        "media_type": "application/pdf" if is_pdf else "text/html",
        "byte_length": len(body),
    }


def acquire_titles(source_root: Path, output: Path) -> dict[str, Any]:
    plan = build_title_plan(source_root, output)
    records: list[dict[str, Any]] = []
    failures: list[str] = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {
            executor.submit(acquire_one_title, str(item["source_url"]), output): str(
                item["source_url"]
            )
            for item in plan["sources"]
        }
        for future in as_completed(futures):
            try:
                records.append(future.result())
            except Exception as error:  # pragma: no cover - external-state evidence
                failures.append(f"{futures[future]}::{error}")
    records.sort(key=lambda row: str(row["source_url"]))
    result = {
        "task_id": TASK_ID,
        "status": "PASS" if not failures and len(records) == 56 else "BLOCKED",
        "record_count": len(records),
        "allowed_title_origins": list(TITLE_ORIGINS),
        "manual_override_count": 0,
        "source_identity_fallback_count": 0,
        "failures": failures,
        "records": records,
    }
    write_json(output / "title_provenance" / "url_title_records.json", result)
    if result["status"] != "PASS":
        raise ValueError("SOURCE_TITLE_NEUTRALITY_BLOCKER")
    return result


def _case(
    field: str, category: str, fixture: str, decision: str, explanation: str
) -> dict[str, str]:
    return {
        "field": field,
        "category": category,
        "fixture": fixture,
        "decision": decision,
        "explanation": explanation,
    }


def field_guide_cases() -> list[dict[str, str]]:
    """Independent teaching fixtures; none are Pilot4 review candidates."""

    cases = [
        _case(
            "text_naturalness",
            "CLEAR_COMMON",
            "《某市公共数据管理办法》自公布之日起施行。",
            "NATURAL",
            "Grammar and referent are ordinary and complete. / 语法与指代自然完整。",
        ),
        _case(
            "text_naturalness",
            "CLEAR_COMMON",
            "办法施行进行部门发布以后规定。",
            "UNNATURAL",
            "Word order is plainly broken. / 语序明显破坏。",
        ),
        _case(
            "text_naturalness",
            "ALTERNATIVE_NEGATIVE",
            "《某省科研经费办法》由该省教育厅单独制定通过。",
            "NATURAL",
            "Truth is irrelevant to naturalness. / 即使事实可能错误，表达仍自然。",
        ),
        _case(
            "text_naturalness",
            "ALTERNATIVE_NEGATIVE",
            "《某校实验室规则》在2024年完成了再次之修订。",
            "MINOR_ISSUE",
            "Understandable but slightly awkward. / 可理解但措辞略生硬。",
        ),
        _case(
            "text_naturalness",
            "BOUNDARY",
            "《某市档案办法》于2020年修订；该办法于2021年施行。",
            "NATURAL",
            "Two clauses remain fluent. / 两个分句仍然流畅。",
        ),
        _case(
            "text_naturalness",
            "BOUNDARY",
            "《某条例》施行于由主管部门2023年。",
            "UNNATURAL",
            "The sentence cannot be repaired by a minor edit. / 不能通过小改动恢复。",
        ),
        _case(
            "local_internal_conflict",
            "CLEAR_COMMON",
            "同一办法既称2024年1月1日施行，又称2024年3月1日为唯一施行日。",
            "YES",
            "The contradiction is inside the candidate. / 文本内部直接矛盾。",
        ),
        _case(
            "local_internal_conflict",
            "CLEAR_COMMON",
            "《某市采购办法》自2024年1月1日起施行。",
            "NO",
            "No internal contradiction is present. / 文本自身无矛盾。",
        ),
        _case(
            "local_internal_conflict",
            "ALTERNATIVE_NEGATIVE",
            "《某省会计规则》由省财政厅发布。",
            "NO",
            "External verification may be needed, but the text is internally coherent. / 可能需外查但内部一致。",
        ),
        _case(
            "local_internal_conflict",
            "ALTERNATIVE_NEGATIVE",
            "修订文本在原文本废止前一天开始施行。",
            "NO",
            "An overlap is not automatically an internal contradiction. / 时间重叠不自动构成内部矛盾。",
        ),
        _case(
            "local_internal_conflict",
            "BOUNDARY",
            "该制度同时规定期限为30日且明确不得超过20日。",
            "YES",
            "Mutually exclusive limits appear locally. / 本地存在互斥期限。",
        ),
        _case(
            "local_internal_conflict",
            "BOUNDARY",
            "该规定随后被修订，具体日期未说明。",
            "UNCERTAIN",
            "The statement is incomplete enough that local consistency cannot be fixed. / 信息不足以确定内部一致性。",
        ),
        _case(
            "phase1_issue",
            "CLEAR_COMMON",
            "《某市科研项目管理办法》规定项目负责人应保存验收材料。",
            "NONE",
            "The subject and proposition are identifiable. / 主体和命题均可识别。",
        ),
        _case(
            "phase1_issue",
            "CLEAR_COMMON",
            "条例规定申请人应提交材料。",
            "MISSING_CONTEXT",
            "The legal subject cannot be uniquely recovered. / 裸指代导致主体缺失。",
        ),
        _case(
            "phase1_issue",
            "ALTERNATIVE_NEGATIVE",
            "《甲办法》与《乙办法》均被修订，它取消了备案要求。",
            "AMBIGUOUS_REFERENCE",
            "It is unclear which instrument 'it' means. / “它”指代不明。",
        ),
        _case(
            "phase1_issue",
            "ALTERNATIVE_NEGATIVE",
            "《某市数据办法》规\ufffd定处理者备案。",
            "OTHER",
            "Encoding corruption is neither missing context nor ambiguous reference. / 编码损坏归 OTHER。",
        ),
        _case(
            "phase1_issue",
            "BOUNDARY",
            "2019年版《某省预算规则》规定年度报告期限为三十日。",
            "NONE",
            "The full subject is present despite a version modifier. / 有版本限定但主体完整。",
        ),
        _case(
            "phase1_issue",
            "BOUNDARY",
            "修订文本取消了原许可。",
            "MISSING_CONTEXT",
            "A version label alone does not identify the instrument. / 仅有版本称呼仍缺主体。",
        ),
        _case(
            "overall_fact_status",
            "CLEAR_COMMON",
            "候选与现行官方文本直接一致。",
            "CURRENTLY_CONSISTENT",
            "The claim matches the current rule. / 与现行规则一致。",
        ),
        _case(
            "overall_fact_status",
            "CLEAR_COMMON",
            "候选准确描述一项已经废止但曾合法施行的旧规则。",
            "LEGITIMATE_VERSION_OR_HISTORY",
            "A valid historical claim is not current conflict. / 合法历史不算现行冲突。",
        ),
        _case(
            "overall_fact_status",
            "ALTERNATIVE_NEGATIVE",
            "候选把官方施行日写晚了一个月。",
            "FACTUAL_CONFLICT",
            "The official evidence directly contradicts the date. / 官方证据直接否定日期。",
        ),
        _case(
            "overall_fact_status",
            "ALTERNATIVE_NEGATIVE",
            "两个可访问官方来源对同一生效日互相冲突且无法消解。",
            "INSUFFICIENT_EVIDENCE",
            "The evidence does not support a unique conclusion. / 证据无法形成唯一结论。",
        ),
        _case(
            "overall_fact_status",
            "BOUNDARY",
            "候选明确限定“截至2018年”，内容与当时规则一致。",
            "LEGITIMATE_VERSION_OR_HISTORY",
            "Time qualification preserves historical validity. / 时间限定使历史陈述成立。",
        ),
        _case(
            "overall_fact_status",
            "BOUNDARY",
            "候选没有错误，但只表达一般背景且证据充分。",
            "CURRENTLY_CONSISTENT",
            "Do not assign a stealth grade to a correct claim. / 正确候选不评价隐蔽等级。",
        ),
        _case(
            "version_claim_status",
            "CLEAR_COMMON",
            "候选仅说明适用对象，没有修订、废止或时间版本命题。",
            "NOT_PRESENT",
            "No version relation is asserted. / 未提出版本关系。",
        ),
        _case(
            "version_claim_status",
            "CLEAR_COMMON",
            "候选称旧办法于新办法施行日同时废止，证据明确支持。",
            "PRESENT_CORRECT",
            "A stated version transition is correct. / 版本衔接正确。",
        ),
        _case(
            "version_claim_status",
            "ALTERNATIVE_NEGATIVE",
            "候选称2022年修订在2021年施行。",
            "PRESENT_INCORRECT",
            "The asserted chronology conflicts with evidence. / 时间关系错误。",
        ),
        _case(
            "version_claim_status",
            "ALTERNATIVE_NEGATIVE",
            "候选称文本已被替代，但提供的证据都未说明替代关系。",
            "PRESENT_EVIDENCE_INSUFFICIENT",
            "A version claim exists but proof is insufficient. / 有命题但证据不足。",
        ),
        _case(
            "version_claim_status",
            "BOUNDARY",
            "证据提到修订史，但候选只陈述现行适用范围。",
            "NOT_PRESENT",
            "Annotate the candidate, not every fact in the evidence. / 只标候选提出的命题。",
        ),
        _case(
            "version_claim_status",
            "BOUNDARY",
            "候选称“修订后的办法继续有效”，但证据仅提供原始版本。",
            "PRESENT_EVIDENCE_INSUFFICIENT",
            "The relation cannot be confirmed from the pool. / 证据池不足以确认。",
        ),
        _case(
            "authority_claim_status",
            "CLEAR_COMMON",
            "候选称某条例由国务院公布，证据明确一致。",
            "PRESENT_CORRECT",
            "The authority claim is supported. / 机关命题正确。",
        ),
        _case(
            "authority_claim_status",
            "CLEAR_COMMON",
            "候选只陈述施行日期，没有机关或权限命题。",
            "NOT_PRESENT",
            "No authority relation is asserted. / 未提出机关关系。",
        ),
        _case(
            "authority_claim_status",
            "ALTERNATIVE_NEGATIVE",
            "候选把网页转载部门写成立法机关。",
            "PRESENT_INCORRECT",
            "Publisher and enactment authority are different. / 转载机关不等于制定机关。",
        ),
        _case(
            "authority_claim_status",
            "ALTERNATIVE_NEGATIVE",
            "候选提出批准机关，但两个证据均未注明批准主体。",
            "PRESENT_EVIDENCE_INSUFFICIENT",
            "The authority claim cannot be checked. / 机关命题证据不足。",
        ),
        _case(
            "authority_claim_status",
            "BOUNDARY",
            "候选称监管部门负责执法，证据直接支持该职责。",
            "PRESENT_CORRECT",
            "Operational authority is still an authority claim. / 执法职责也属于机关命题。",
        ),
        _case(
            "authority_claim_status",
            "BOUNDARY",
            "证据页脚显示网站主管单位，但候选未讨论该单位。",
            "NOT_PRESENT",
            "Page ownership alone does not create a candidate claim. / 页面机构信息不自动成为候选命题。",
        ),
        _case(
            "minimum_external_evidence_needed",
            "CLEAR_COMMON",
            "一个官方法条页面即可直接确认日期错误。",
            "ONE_OFFICIAL_EVIDENCE",
            "One item is sufficient. / 单一官方证据已充分。",
        ),
        _case(
            "minimum_external_evidence_needed",
            "CLEAR_COMMON",
            "必须把旧版废止条款与新版施行条款联合起来才能判断空档。",
            "MULTI_EVIDENCE_OR_VERSION_CHAIN",
            "No single item is sufficient. / 任一单独证据都不足。",
        ),
        _case(
            "minimum_external_evidence_needed",
            "ALTERNATIVE_NEGATIVE",
            "候选与现行证据一致，没有事实冲突。",
            "NOT_APPLICABLE",
            "Minimum evidence grades confirmed conflicts only. / 正确候选不适用。",
        ),
        _case(
            "minimum_external_evidence_needed",
            "ALTERNATIVE_NEGATIVE",
            "复核人实际打开E1和E2，但E1本身已能确认错误。",
            "ONE_OFFICIAL_EVIDENCE",
            "Actual browsing count does not define minimum necessity. / 实际打开两个不等于 MULTI。",
        ),
        _case(
            "minimum_external_evidence_needed",
            "BOUNDARY",
            "同一官方页面的正文与附表共同确认错误。",
            "ONE_OFFICIAL_EVIDENCE",
            "Direct context within one official item remains ONE. / 同一来源直接上下文仍为 ONE。",
        ),
        _case(
            "minimum_external_evidence_needed",
            "BOUNDARY",
            "需串联两个版本和一项机关决定才能唯一确认。",
            "MULTI_EVIDENCE_OR_VERSION_CHAIN",
            "The conclusion depends on a chain. / 结论依赖多证据链。",
        ),
        _case(
            "evidence_selection",
            "CLEAR_COMMON",
            "只实际查看E1。",
            "E1",
            "Record actual use. / 记录实际使用。",
        ),
        _case(
            "evidence_selection",
            "CLEAR_COMMON",
            "只实际查看E2。",
            "E2",
            "Record actual use. / 记录实际使用。",
        ),
        _case(
            "evidence_selection",
            "ALTERNATIVE_NEGATIVE",
            "未查看任何证据，因为来源全部无法访问。",
            "NONE",
            "No evidence was used. / 未实际使用证据。",
        ),
        _case(
            "evidence_selection",
            "ALTERNATIVE_NEGATIVE",
            "同时查看E1和E2。",
            "E1+E2",
            "Selection is independent of sufficiency. / 选择字段独立于最低充分性。",
        ),
        _case(
            "evidence_selection",
            "BOUNDARY",
            "查看E1+E2；E1单独已足以确认冲突。",
            "E1+E2",
            "Use E1+E2 with minimum ONE. / 实际用两个但最低为 ONE。",
        ),
        _case(
            "evidence_selection",
            "BOUNDARY",
            "查看E1+E2；必须联合两者才可确认冲突。",
            "E1+E2",
            "Use E1+E2 with minimum MULTI. / 实际与最低需求均为联合证据。",
        ),
        _case(
            "phase2_issue",
            "CLEAR_COMMON",
            "来源可访问、内容完整且候选可解释。",
            "NONE",
            "No process or candidate defect exists. / 无异常。",
        ),
        _case(
            "phase2_issue",
            "CLEAR_COMMON",
            "E1和E2均返回网络错误。",
            "SOURCE_UNREACHABLE",
            "The assigned sources cannot be opened. / 来源不可访问。",
        ),
        _case(
            "phase2_issue",
            "ALTERNATIVE_NEGATIVE",
            "两个官方来源对同一日期给出互斥内容。",
            "SOURCE_CONFLICT",
            "The sources conflict. / 来源互相冲突。",
        ),
        _case(
            "phase2_issue",
            "ALTERNATIVE_NEGATIVE",
            "E2槽位为空，无法完成要求的复核。",
            "EVIDENCE_MISSING",
            "An assigned evidence item is absent. / 指定证据缺失。",
        ),
        _case(
            "phase2_issue",
            "BOUNDARY",
            "Phase1时主体看似完整，查看证据后发现候选中的简称对应两个不同制度。",
            "LATE_DISCOVERED_CANDIDATE_DEFECT",
            "The defect becomes visible only after evidence review. / 对照证据后才发现候选缺陷。",
        ),
        _case(
            "phase2_issue",
            "BOUNDARY",
            "来源可访问但正文严重乱码，且不属于缺失或冲突。",
            "OTHER",
            "Use OTHER with a precise reason. / 其他异常需写明。",
        ),
        _case(
            "phase1_reason",
            "GOOD_REASON",
            "候选完整写出《某市科研项目管理办法》，语法自然，文本内部没有互斥日期。",
            "GOOD",
            "Specific and tied to the visible text. / 具体且对应可见文本。",
        ),
        _case(
            "phase1_reason",
            "GOOD_REASON",
            "“它”可能指《甲办法》或《乙办法》，因此选择 AMBIGUOUS_REFERENCE。",
            "GOOD",
            "Names the exact ambiguity. / 明确指出歧义位置。",
        ),
        _case(
            "phase1_reason",
            "BAD_TOO_VAGUE",
            "看起来没问题。",
            "BAD",
            "It cannot be audited. / 无法审计。",
        ),
        _case(
            "phase1_reason",
            "BAD_TOO_VAGUE",
            "句子怪。",
            "BAD",
            "It does not identify the defect. / 未说明具体问题。",
        ),
        _case(
            "phase1_reason",
            "FORBIDDEN",
            "根据E1，该候选事实错误。",
            "FORBIDDEN",
            "Phase1 must not use Phase2 evidence. / 第一阶段不得引用证据池。",
        ),
        _case(
            "phase1_reason",
            "FORBIDDEN",
            "这是隐藏难度样本，所以内部无冲突。",
            "FORBIDDEN",
            "Design labels must never drive the reason. / 禁止使用设计标签。",
        ),
        _case(
            "phase2_reason",
            "GOOD_REASON",
            "E1第六条直接给出2024年1月1日，候选写成2月1日，因此为 FACTUAL_CONFLICT。",
            "GOOD",
            "Connects claim, evidence and decision. / 串联候选、证据与判断。",
        ),
        _case(
            "phase2_reason",
            "GOOD_REASON",
            "E1单独已充分；我也查看了E2，所以 selection=E1+E2、minimum=ONE。",
            "GOOD",
            "Separates actual use from minimum necessity. / 区分实际使用与最低需求。",
        ),
        _case(
            "phase2_reason",
            "BAD_TOO_VAGUE",
            "证据支持。",
            "BAD",
            "It does not say what is supported. / 未说明支持何种命题。",
        ),
        _case(
            "phase2_reason",
            "BAD_TOO_VAGUE",
            "我觉得不对。",
            "BAD",
            "No traceable evidence relation is stated. / 没有可追溯证据关系。",
        ),
        _case(
            "phase2_reason",
            "FORBIDDEN",
            "隐藏设计标签写着冲突，所以选 FACTUAL_CONFLICT。",
            "FORBIDDEN",
            "Hidden labels are prohibited. / 禁止使用隐藏标签。",
        ),
        _case(
            "phase2_reason",
            "FORBIDDEN",
            "按照隐藏设计答案应当选高难度等级。",
            "FORBIDDEN",
            "Hidden answers and derived difficulty are not reviewer inputs. / 禁止隐藏答案与难度反推。",
        ),
    ]
    enum_fields = {
        "text_naturalness": TEXT_NATURALNESS,
        "local_internal_conflict": LOCAL_INTERNAL_CONFLICT,
        "phase1_issue": PHASE1_ISSUE,
        "overall_fact_status": OVERALL_FACT_STATUS,
        "version_claim_status": COMBINED_CLAIM_STATUS,
        "authority_claim_status": COMBINED_CLAIM_STATUS,
        "minimum_external_evidence_needed": MINIMUM_EXTERNAL_EVIDENCE,
        "evidence_selection": EVIDENCE_SELECTION,
        "phase2_issue": PHASE2_ISSUE,
    }
    for field, allowed in enum_fields.items():
        rows = [row for row in cases if row["field"] == field]
        if len(rows) < 6 or any(row["decision"] not in allowed for row in rows):
            raise ValueError(f"FIELD_GUIDE_CASE_BLOCKER:{field}")
    if set(row["field"] for row in cases) != set(MANUAL_FIELDS):
        raise ValueError("FIELD_GUIDE_MANUAL_FIELD_COVERAGE_BLOCKER")
    return cases


def _seed(output: Path) -> bytes:
    path = output / "owner_only" / "blind_review_seed.json"
    if path.exists():
        return bytes.fromhex(str(load_json(path)["seed_hex"]))
    seed = secrets.token_bytes(32)
    write_json(
        path,
        {
            "task_id": TASK_ID,
            "classification": "OWNER_ONLY",
            "seed_hex": seed.hex(),
            "frozen_at": utc_now(),
        },
    )
    return seed


def _mapping_sha_sidecar(path: Path) -> None:
    path.with_suffix(".sha256").write_text(
        f"{file_sha256(path)}  {path.name}\n", encoding="utf-8"
    )


def _profile(candidate: Mapping[str, Any]) -> dict[str, str]:
    owner = candidate["owner_only"]
    coverage = str(owner["coverage_cell"])
    hkp, stealth = coverage.split("|", maxsplit=1)
    return {
        "class": str(owner["candidate_kind"]),
        "hkp": hkp,
        "stealth": stealth,
        "domain": str(owner["domain"]),
    }


def _accepted_order(
    identities: Sequence[str],
    triplets: Mapping[str, str],
    profiles: Mapping[str, Mapping[str, str]],
    seed: bytes,
) -> tuple[list[str], int, dict[str, Any]]:
    for nonce in range(10000):
        trial_seed = hmac.new(seed, f"order-nonce:{nonce}".encode(), "sha256").digest()
        try:
            order = deterministic_constrained_blind_order(
                identities, triplets, profiles, trial_seed
            )
        except ValueError as error:
            if str(error) == "BLIND_ORDER_CONSTRAINT_BLOCKER":
                continue
            raise
        qa = {
            key: order_profile([str(profiles[item][key]) for item in order])
            for key in ("class", "hkp", "stealth", "domain")
        }
        if (
            adjacent_same_group_count(order, triplets) == 0
            and all(profile["maximum_run"] <= 2 for profile in qa.values())
            and all(not profile["exact_periods_2_to_12"] for profile in qa.values())
        ):
            return order, nonce, qa
    raise ValueError("BLIND_ORDER_LEAKAGE_BLOCKER")


def prepare_blind_assets(source_root: Path, output: Path) -> dict[str, Any]:
    paths = source_paths(source_root)
    candidates = load_jsonl(paths["candidates"])
    pool_a = load_json(paths["pool_a"])["items"]
    pool_b = load_json(paths["pool_b"])["items"]
    title_payload = load_json(output / "title_provenance" / "url_title_records.json")
    title_by_url = {str(row["source_url"]): row for row in title_payload["records"]}
    if len(candidates) != 72 or len(pool_a) != 144 or len(pool_b) != 144:
        raise ValueError("SOURCE_CARDINALITY_BLOCKER")
    identities = [str(row["sample_id"]) for row in candidates]
    if len(set(identities)) != 72:
        raise ValueError("SOURCE_IDENTITY_BLOCKER")
    candidate_by_id = {str(row["sample_id"]): row for row in candidates}
    triplets = {item: str(candidate_by_id[item]["triplet_id"]) for item in identities}
    profiles = {item: _profile(candidate_by_id[item]) for item in identities}
    seed = _seed(output)
    order, order_nonce, profile_qa = _accepted_order(
        identities, triplets, profiles, seed
    )
    opaque_ids = {item: blind_review_id(seed, item) for item in identities}
    if len(set(opaque_ids.values())) != 72:
        raise ValueError("BLIND_ID_COLLISION_BLOCKER")
    pool_a_by_id: dict[str, list[dict[str, Any]]] = {}
    pool_b_by_id: dict[str, list[dict[str, Any]]] = {}
    for item in pool_a:
        pool_a_by_id.setdefault(str(item["sample_id"]), []).append(item)
    for item in pool_b:
        pool_b_by_id.setdefault(str(item["sample_id"]), []).append(item)
    rows: list[dict[str, Any]] = []
    mapping: list[dict[str, str]] = []
    title_slots: list[dict[str, Any]] = []
    a_e1_matches = 0
    b_e1_matches = 0
    for internal_id in order:
        candidate = candidate_by_id[internal_id]
        pair = sorted(
            pool_a_by_id[internal_id], key=lambda item: str(item["evidence_id"])
        )
        if len(pair) != 2:
            raise ValueError("SOURCE_EVIDENCE_COUNT_BLOCKER")
        opaque_id = opaque_ids[internal_id]
        if evidence_should_swap(seed, opaque_id):
            pair.reverse()
        visible_evidence = []
        for index, source in enumerate(pair, start=1):
            url = str(source["official_source_url"])
            title = title_by_url[url]
            evidence = {
                "evidence_id": f"E{index}",
                "official_page_title": str(title["display_title"]),
                "official_source_url": url,
            }
            visible_evidence.append(evidence)
            title_slots.append(
                {
                    "blind_review_id": opaque_id,
                    "evidence_id": f"E{index}",
                    "source_url": url,
                    "display_title": str(title["display_title"]),
                    "title_origin": str(title["title_origin"]),
                    "title_source_text_hash": str(title["title_source_text_hash"]),
                    "source_snapshot_hash": str(title["source_snapshot_hash"]),
                    "retrieved_at": str(title["retrieved_at"]),
                }
            )
        original_a_e1 = next(
            str(item["official_source_url"])
            for item in pool_a_by_id[internal_id]
            if item["evidence_id"] == "E1"
        )
        original_b_e1 = next(
            str(item["official_source_url"])
            for item in pool_b_by_id[internal_id]
            if item["evidence_id"] == "E1"
        )
        a_e1_matches += visible_evidence[0]["official_source_url"] == original_a_e1
        b_e1_matches += visible_evidence[0]["official_source_url"] == original_b_e1
        rows.append(
            {
                "blind_review_id": opaque_id,
                "candidate_text": str(candidate["phase1_view"]["candidate_text"]),
                "source_title": str(candidate["phase1_view"]["source_title"]),
                "phase1_questions": [
                    {"field": field, "response": ""} for field in PHASE1_FIELDS
                ],
                "evidence_pool": visible_evidence,
                "phase2_questions": [
                    {"field": field, "response": ""} for field in PHASE2_FIELDS
                ],
            }
        )
        mapping.append({"blind_review_id": opaque_id, "sample_id": internal_id})
    serialized = "\n".join(
        json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in rows
    )
    if "P4Q-" in serialized or "sample_id" in serialized:
        raise ValueError("SANITIZED_INPUT_IDENTITY_LEAKAGE_BLOCKER")
    candidate_qa = load_json(paths["candidate_qa"])
    if (
        candidate_qa["meta_cue_blocker_count"] != 0
        or candidate_qa["self_containment_blocker_count"] != 0
    ):
        raise ValueError("FROZEN_CANDIDATE_GATE_BLOCKER")
    duplicate_qa = lexical_duplicate_qa(
        [str(row["phase1_view"]["candidate_text"]) for row in candidates],
        [str(row["triplet_id"]) for row in candidates],
    )
    if duplicate_qa["status"] != "PASS":
        raise ValueError("CANDIDATE_DUPLICATE_BLOCKER")
    write_jsonl(output / "staging" / "blind_packet_input.jsonl", rows)
    cases = field_guide_cases()
    candidate_normalized = {
        re.sub(r"[\W_]+", "", str(row["phase1_view"]["candidate_text"]).casefold())
        for row in candidates
    }
    if any(
        re.sub(r"[\W_]+", "", row["fixture"].casefold()) in candidate_normalized
        for row in cases
    ):
        raise ValueError("FIELD_GUIDE_CANDIDATE_REUSE_BLOCKER")
    write_json(output / "staging" / "field_guide_cases.json", cases)
    mapping_path = output / "owner_only" / "blind_review_identity_mapping.json"
    write_json(
        mapping_path,
        {
            "task_id": TASK_ID,
            "classification": "OWNER_ONLY / EXCLUDED_FROM_EXTERNAL_PACKET",
            "records": mapping,
        },
    )
    _mapping_sha_sidecar(mapping_path)
    write_json(
        output / "title_provenance" / "evidence_display_title_records.json",
        {
            "task_id": TASK_ID,
            "status": "PASS",
            "visible_slot_count": len(title_slots),
            "allowed_title_origins": list(TITLE_ORIGINS),
            "manual_override_visible_count": 0,
            "source_identity_fallback_visible_count": 0,
            "records": title_slots,
        },
    )
    order_qa = {
        "status": "PASS",
        "frozen_order_nonce": order_nonce,
        "candidate_count": len(order),
        "matched_triplet_adjacency_count": adjacent_same_group_count(order, triplets),
        "class_periodicity": profile_qa["class"],
        "hkp_periodicity": profile_qa["hkp"],
        "stealth_periodicity": profile_qa["stealth"],
        "domain_periodicity": profile_qa["domain"],
        "blind_e1_matches_production_a": a_e1_matches,
        "blind_e1_matches_production_b": b_e1_matches,
        "blind_order_identical_to_production_a": a_e1_matches == 72,
        "blind_order_identical_to_production_b": b_e1_matches == 72,
    }
    write_json(output / "qa" / "blind_order_leakage_qa.json", order_qa)
    write_json(output / "qa" / "candidate_final_machine_gate.json", duplicate_qa)
    write_json(
        output / "qa" / "historical_c1b1245_immutability_pre.json",
        tree_identity(source_root),
    )
    summary = {
        "task_id": TASK_ID,
        "namespace": NAMESPACE,
        "status": "BLIND_OWNER_ASSETS_PREPARED",
        "historical_commit": HISTORICAL_COMMIT,
        "candidate_count": len(rows),
        "visible_title_slots": len(title_slots),
        "unique_title_sources": len(title_by_url),
        "field_guide_case_count": len(cases),
        "semantic_answer_generation": 0,
        "expected_contract_loaded": False,
    }
    write_json(output / "qa" / "owner_asset_prepare_summary.json", summary)
    return summary


def validate_external_packet(output: Path, builder_source: Path) -> dict[str, Any]:
    external = output / "external_blind_review"
    required_names = {
        "PILOT4_EXTERNAL_BLIND_REVIEW_PACKET.md",
        "PILOT4_EXTERNAL_BLIND_REVIEW_PACKET.jsonl",
        "PILOT4_EXTERNAL_BLIND_FIELD_GUIDE.md",
        "PILOT4_EXTERNAL_BLIND_REVIEW_TEMPLATE.csv",
    }
    if {path.name for path in external.iterdir() if path.is_file()} != required_names:
        raise ValueError("EXTERNAL_PACKET_FILE_SET_BLOCKER")
    rows = load_jsonl(external / "PILOT4_EXTERNAL_BLIND_REVIEW_PACKET.jsonl")
    row_qa = validate_packet_rows(rows)
    external_text = "\n".join(
        path.read_text(
            encoding="utf-8-sig" if path.suffix.casefold() == ".csv" else "utf-8"
        )
        for path in sorted(external.iterdir())
        if path.is_file()
    )
    forbidden_tokens = (
        "P4Q-",
        "sample_id",
        "triplet_id",
        "independence_group",
        "candidate_kind",
        "owner_only",
        "intended_stealth",
        "hard_negative_type",
        "target_field",
        "expected_contract",
    )
    leaked = [
        token
        for token in forbidden_tokens
        if token.casefold() in external_text.casefold()
    ]
    if leaked:
        raise ValueError(f"EXTERNAL_PACKET_LABEL_LEAKAGE:{leaked}")
    builder_text = builder_source.read_text(encoding="utf-8")
    prohibited_knowledge_objects = (
        "LOCAL_CONFLICT_IDS",
        "FACTUAL_CONFLICT_IDS",
        "MULTI_EVIDENCE_IDS",
        "LEGITIMATE_HISTORY_IDS",
        "VERSION_INCORRECT_IDS",
        "AUTHORITY_INCORRECT_IDS",
        "expected_contract_from_owner",
    )
    if any(token in builder_text for token in prohibited_knowledge_objects):
        raise ValueError("BLIND_BUILDER_EXPECTED_KNOWLEDGE_BLOCKER")
    title_records = load_json(
        output / "title_provenance" / "evidence_display_title_records.json"
    )
    titles = title_records["records"]
    title_failures = [
        row
        for row in titles
        if row["title_origin"] not in TITLE_ORIGINS
        or not re.fullmatch(r"[0-9a-f]{64}", str(row["title_source_text_hash"]))
        or not re.fullmatch(r"[0-9a-f]{64}", str(row["source_snapshot_hash"]))
    ]
    if len(titles) != 144 or title_failures:
        raise ValueError("VISIBLE_TITLE_PROVENANCE_BLOCKER")
    cases = load_json(output / "staging" / "field_guide_cases.json")
    case_counts = {
        field: sum(row["field"] == field for row in cases) for field in MANUAL_FIELDS
    }
    enum_fields = set(MANUAL_FIELDS) - {"phase1_reason", "phase2_reason"}
    if any(case_counts[field] < 6 for field in enum_fields):
        raise ValueError("FIELD_GUIDE_CASE_COUNT_BLOCKER")
    if any(case_counts[field] < 6 for field in ("phase1_reason", "phase2_reason")):
        raise ValueError("FIELD_GUIDE_REASON_CASE_BLOCKER")
    placeholder_count = sum(
        "use the field definition for" in str(value).casefold()
        for row in cases
        for value in row.values()
    )
    if placeholder_count:
        raise ValueError("FIELD_GUIDE_PLACEHOLDER_BLOCKER")
    csv_lines = (
        (external / "PILOT4_EXTERNAL_BLIND_REVIEW_TEMPLATE.csv")
        .read_text(encoding="utf-8-sig")
        .splitlines()
    )
    if len(csv_lines) != 73:
        raise ValueError("REVIEW_TEMPLATE_CARDINALITY_BLOCKER")
    mapping_path = output / "owner_only" / "blind_review_identity_mapping.json"
    mapping_hash = (
        mapping_path.with_suffix(".sha256").read_text(encoding="utf-8").split()[0]
    )
    if mapping_hash != file_sha256(mapping_path):
        raise ValueError("BLIND_MAPPING_HASH_BLOCKER")
    order_qa = load_json(output / "qa" / "blind_order_leakage_qa.json")
    candidate_qa = load_json(output / "qa" / "candidate_final_machine_gate.json")
    if order_qa["matched_triplet_adjacency_count"] != 0:
        raise ValueError("BLIND_ORDER_ADJACENCY_BLOCKER")
    if (
        order_qa["blind_order_identical_to_production_a"]
        or order_qa["blind_order_identical_to_production_b"]
    ):
        raise ValueError("BLIND_EVIDENCE_ORDER_BLOCKER")
    if candidate_qa["status"] != "PASS":
        raise ValueError("CANDIDATE_FINAL_GATE_BLOCKER")
    qa = {
        "task_id": TASK_ID,
        "status": "PASS",
        "blind_packet_contains_original_identity": 0,
        "blind_packet_contains_design_label": 0,
        "blind_packet_contains_owner_material": 0,
        "blind_ids_unique": "72/72",
        "mapping_isolated": True,
        "mapping_sha256": mapping_hash,
        "candidate_count": 72,
        "evidence_slots": 144,
        "e1_e2_distinct": "72/72",
        "actual_title_provenance": "144/144",
        "title_manual_override_visible": 0,
        "source_identity_fallback_visible": 0,
        "source_type_visible": 0,
        "evidence_role_visible": 0,
        "matched_triplet_adjacency": 0,
        "candidate_duplicate": 0,
        "cross_triplet_lexical_near_duplicate": 0,
        "field_guide_placeholder_example_count": placeholder_count,
        "manual_field_coverage": f"{len(case_counts)}/{len(MANUAL_FIELDS)}",
        "machine_semantic_answer_generation": row_qa[
            "machine_semantic_answer_generation"
        ],
        "external_review_result_filled_count": 0,
        "expected_contract_loaded": False,
    }
    write_json(output / "qa" / "blind_packet_machine_qa.json", qa)
    write_json(
        output / "qa" / "field_guide_real_case_qa.json",
        {
            "status": "PASS",
            "manual_fields": list(MANUAL_FIELDS),
            "case_count": len(cases),
            "case_count_by_field": case_counts,
            "placeholder_example_count": placeholder_count,
            "review_candidate_reuse_count": 0,
        },
    )
    write_json(
        output / "governance" / "c1b1245_review_reclassification.json",
        {
            "task_id": TASK_ID,
            "historical_commit": HISTORICAL_COMMIT,
            "historical_evidence_deleted_or_overwritten": False,
            "superseded_classification": "ONE_LABEL_BLIND_SEMANTIC_REVIEW + OWNER_REVIEW_REQUIRED",
            "corrected_classification": (
                "SAMPLE_ID_LABEL_LOOKUP_CONTAMINATED_REVIEW / "
                "NOT_ACCEPTABLE_AS_EXTERNAL_LABEL_BLIND_EVIDENCE"
            ),
            "reason": (
                "The historical reviewer used the internal identity as a key into "
                "compiled answer-bearing sets; sanitized input and unique reasoning "
                "therefore did not establish blindness or independent semantic judgment."
            ),
            "compiled_objects_observed": list(prohibited_knowledge_objects[:-1]),
            "owner_decision": "BLIND_EXTERNAL_REVIEW_REQUIRED",
        },
    )
    return qa


def write_manifest(output: Path) -> dict[str, Any]:
    files = [
        path
        for path in sorted(output.rglob("*"))
        if path.is_file() and path.parts[-2:] != ("manifest", "manifest.json")
    ]
    entries = []
    for path in files:
        relative = path.relative_to(output).as_posix()
        entries.append(
            {
                "path": relative,
                "visibility": "OWNER_ONLY"
                if relative.startswith("owner_only/")
                else "EXTERNAL_REVIEWER_VISIBLE"
                if relative.startswith("external_blind_review/")
                else "CONTROL_PLANE_EVIDENCE",
                "size": path.stat().st_size,
                "sha256": file_sha256(path),
            }
        )
    manifest = {
        "task_id": TASK_ID,
        "namespace": NAMESPACE,
        "status": STATUS,
        "file_count": len(entries),
        "mapping_manifest_entries": sum(
            str(row["path"]).startswith("owner_only/blind_review_identity_mapping")
            for row in entries
        ),
        "files": entries,
    }
    write_json(output / "manifest" / "manifest.json", manifest)
    return manifest


def remove_unreferenced_source_snapshots(output: Path) -> int:
    title_payload = load_json(output / "title_provenance" / "url_title_records.json")
    referenced = {
        Path(str(row["snapshot_relative_path"])).name
        for row in title_payload["records"]
    }
    snapshot_root = output / "title_provenance" / "source_snapshots"
    removed = 0
    for path in snapshot_root.iterdir():
        if path.is_file() and path.name not in referenced:
            path.unlink()
            removed += 1
    write_json(
        output / "qa" / "source_snapshot_inventory_qa.json",
        {
            "status": "PASS",
            "referenced_snapshot_count": len(referenced),
            "final_snapshot_count": len(list(snapshot_root.iterdir())),
            "unreferenced_prefinal_snapshot_removed_count": removed,
        },
    )
    return removed


def verify_historical(source_root: Path, output: Path) -> None:
    pre = load_json(output / "qa" / "historical_c1b1245_immutability_pre.json")
    post = tree_identity(source_root)
    result = {
        "status": "PASS" if pre == post else "BLOCKED",
        "historical_commit": HISTORICAL_COMMIT,
        "pre_file_count": pre["file_count"],
        "post_file_count": post["file_count"],
        "tree_equal": pre == post,
    }
    write_json(output / "qa" / "historical_c1b1245_immutability_post.json", result)
    if result["status"] != "PASS":
        raise ValueError("HISTORICAL_EVIDENCE_MUTATION_BLOCKER")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("acquire-titles", "prepare", "qa", "finalize"))
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--builder-source", type=Path)
    args = parser.parse_args()
    if args.mode == "acquire-titles":
        result = acquire_titles(args.source_root, args.output)
    elif args.mode == "prepare":
        result = prepare_blind_assets(args.source_root, args.output)
    elif args.mode == "qa":
        if args.builder_source is None:
            raise ValueError("BUILDER_SOURCE_REQUIRED")
        result = validate_external_packet(args.output, args.builder_source)
    else:
        verify_historical(args.source_root, args.output)
        remove_unreferenced_source_snapshots(args.output)
        result = write_manifest(args.output)
    print(json.dumps({"mode": args.mode, "status": "PASS", "result": result}))


if __name__ == "__main__":
    main()
