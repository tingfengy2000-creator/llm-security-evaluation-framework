"""Render reviewer-facing files from an already anonymous input stream.

This program has no access to the private identity mapping or annotation
design metadata.  It only formats the supplied opaque review rows and teaching
fixtures; it never fills a reviewer response.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any, Mapping, Sequence


PHASE1_FIELDS = (
    "text_naturalness",
    "local_internal_conflict",
    "phase1_issue",
    "phase1_reason",
)

PHASE2_FIELDS = (
    "overall_fact_status",
    "version_claim_status",
    "authority_claim_status",
    "minimum_external_evidence_needed",
    "evidence_selection",
    "phase2_issue",
    "phase2_reason",
)

ROW_FIELDS = (
    "blind_review_id",
    "candidate_text",
    "source_title",
    "phase1_questions",
    "evidence_pool",
    "phase2_questions",
)

EVIDENCE_FIELDS = (
    "evidence_id",
    "official_page_title",
    "official_source_url",
)

ENUMS = {
    "text_naturalness": "NATURAL / MINOR_ISSUE / UNNATURAL",
    "local_internal_conflict": "YES / NO / UNCERTAIN",
    "phase1_issue": "NONE / MISSING_CONTEXT / AMBIGUOUS_REFERENCE / OTHER",
    "overall_fact_status": "CURRENTLY_CONSISTENT / LEGITIMATE_VERSION_OR_HISTORY / FACTUAL_CONFLICT / INSUFFICIENT_EVIDENCE",
    "version_claim_status": "NOT_PRESENT / PRESENT_CORRECT / PRESENT_INCORRECT / PRESENT_EVIDENCE_INSUFFICIENT",
    "authority_claim_status": "NOT_PRESENT / PRESENT_CORRECT / PRESENT_INCORRECT / PRESENT_EVIDENCE_INSUFFICIENT",
    "minimum_external_evidence_needed": "ONE_OFFICIAL_EVIDENCE / MULTI_EVIDENCE_OR_VERSION_CHAIN / NOT_APPLICABLE",
    "evidence_selection": "NONE / E1 / E2 / E1+E2",
    "phase2_issue": "NONE / SOURCE_UNREACHABLE / SOURCE_CONFLICT / EVIDENCE_MISSING / LATE_DISCOVERED_CANDIDATE_DEFECT / OTHER",
    "phase1_reason": "free text / 简短具体理由",
    "phase2_reason": "free text / 简短具体理由",
}

DEFINITIONS = {
    "text_naturalness": "Judge expression quality only, independent of truth. / 只判断表达自然度，与事实正误分离。",
    "local_internal_conflict": "Can the candidate contradict itself without external evidence? / 不看外部证据时，候选自身是否矛盾。",
    "phase1_issue": "Record a defect visible before opening evidence. / 记录打开证据前即可发现的候选缺陷。",
    "phase1_reason": "Give a concrete reason tied only to the visible candidate. / 只依据候选文本写具体理由。",
    "overall_fact_status": "Judge the candidate against the supplied official evidence. / 根据所给官方证据判断总体事实状态。",
    "version_claim_status": "Judge a version, amendment, repeal or history relation only when the candidate asserts one. / 仅在候选提出版本关系时判断。",
    "authority_claim_status": "Judge an enactment, approval, publication, supervision or enforcement authority relation only when asserted. / 仅在候选提出机关关系时判断。",
    "minimum_external_evidence_needed": "Record the smallest evidence set required to confirm an established conflict. / 只记录确认已存在冲突所需的最小证据集。",
    "evidence_selection": "Record the evidence actually used; this is independent of minimum necessity. / 记录实际查看的证据，与最低充分性分离。",
    "phase2_issue": "Record source or late-discovered candidate defects found during evidence review. / 记录证据阶段发现的来源问题或迟发现候选缺陷。",
    "phase2_reason": "Connect the candidate claim, evidence and selected decision. / 明确串联候选命题、证据和判断。",
}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def write_jsonl(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    path.write_text(
        "".join(
            json.dumps(dict(row), ensure_ascii=False, separators=(",", ":")) + "\n"
            for row in rows
        ),
        encoding="utf-8",
    )


def validate_rows(rows: Sequence[Mapping[str, Any]]) -> None:
    if len(rows) != 72:
        raise ValueError("ROW_COUNT_BLOCKER")
    ids = []
    for row in rows:
        if tuple(row) != ROW_FIELDS:
            raise ValueError("ROW_SCHEMA_BLOCKER")
        ids.append(str(row["blind_review_id"]))
        if len(row["evidence_pool"]) != 2:
            raise ValueError("EVIDENCE_COUNT_BLOCKER")
        if any(tuple(item) != EVIDENCE_FIELDS for item in row["evidence_pool"]):
            raise ValueError("EVIDENCE_SCHEMA_BLOCKER")
        if [item["field"] for item in row["phase1_questions"]] != list(PHASE1_FIELDS):
            raise ValueError("PHASE1_SCHEMA_BLOCKER")
        if [item["field"] for item in row["phase2_questions"]] != list(PHASE2_FIELDS):
            raise ValueError("PHASE2_SCHEMA_BLOCKER")
        if any(item["response"] != "" for item in row["phase1_questions"]):
            raise ValueError("NONEMPTY_RESPONSE_BLOCKER")
        if any(item["response"] != "" for item in row["phase2_questions"]):
            raise ValueError("NONEMPTY_RESPONSE_BLOCKER")
    if len(set(ids)) != 72:
        raise ValueError("OPAQUE_ID_BLOCKER")


def packet_markdown(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# PILOT4 External Blind Review Packet",
        "",
        "Status: `WAITING_FOR_EXTERNAL_BLIND_REVIEW`",
        "",
        "Complete every Phase 1 question before using the Phase 2 evidence shown below it. "
        "Do not infer any project design category. / 请先完成每条的 Phase 1，再使用其下方 Phase 2 证据；不要推测项目设计类别。",
        "",
        "Return the completed CSV or an equivalent list keyed only by `blind_review_id`. "
        "/ 请仅以 `blind_review_id` 为身份返回完整字段。",
        "",
    ]
    for index, row in enumerate(rows, start=1):
        lines.extend(
            [
                f"## {index}. {row['blind_review_id']}",
                "",
                f"**Source title / 主题标题：** {row['source_title']}",
                "",
                f"**Candidate / 候选文本：** {row['candidate_text']}",
                "",
                "### Phase 1 — Candidate only / 第一阶段：只看候选",
                "",
            ]
        )
        for field in PHASE1_FIELDS:
            lines.append(f"- `{field}` ({ENUMS[field]}): ")
        lines.extend(
            [
                "",
                "---",
                "",
                "### Phase 2 — Official evidence pool / 第二阶段：官方证据池",
                "",
            ]
        )
        for evidence in row["evidence_pool"]:
            lines.extend(
                [
                    f"**{evidence['evidence_id']}**",
                    "",
                    f"- official_page_title: {evidence['official_page_title']}",
                    f"- official_source_url: {evidence['official_source_url']}",
                    "",
                ]
            )
        lines.extend(["### Phase 2 questions / 第二阶段问题", ""])
        for field in PHASE2_FIELDS:
            lines.append(f"- `{field}` ({ENUMS[field]}): ")
        lines.extend(["", "---", ""])
    return "\n".join(lines).rstrip() + "\n"


def guide_markdown(cases: Sequence[Mapping[str, str]]) -> str:
    lines = [
        "# PILOT4 External Blind Field Guide",
        "",
        "Read time: approximately 10–15 minutes. / 预计阅读时间：10–15 分钟。",
        "",
        "The guide uses independent teaching fixtures, not review-packet candidates. "
        "/ 本指南只使用独立教学案例，不使用审核包中的候选文本。",
        "",
        "## Workflow / 操作顺序",
        "",
        "1. Finish Phase 1 from the candidate text only. / 只依据候选文本完成第一阶段。",
        "2. Then inspect E1/E2 and finish Phase 2. / 再查看 E1/E2 完成第二阶段。",
        "3. Record actual evidence use separately from minimum necessity. / 区分实际使用证据与最低充分证据。",
        "4. If a candidate defect is discovered, use the phase-specific issue field. / 候选缺陷必须记录在对应阶段。",
        "",
        "## Field definitions / 字段定义",
        "",
        "| Phase | Field | Allowed values | Practical definition |",
        "| --- | --- | --- | --- |",
    ]
    for field in PHASE1_FIELDS + PHASE2_FIELDS:
        phase = "Phase 1" if field in PHASE1_FIELDS else "Phase 2"
        lines.append(f"| {phase} | `{field}` | {ENUMS[field]} | {DEFINITIONS[field]} |")
    lines.extend(
        [
            "",
            "## Key boundaries / 关键边界",
            "",
            "- Opening two pages does not make the minimum requirement MULTI when either page alone is sufficient. "
            "/ 实际打开两个页面，不代表最低需求一定是 MULTI。",
            "- `evidence_selection=E1+E2` may coexist with `minimum_external_evidence_needed=ONE_OFFICIAL_EVIDENCE`. "
            "/ 实际使用 E1+E2 可以与最低需求 ONE 同时成立。",
            "- Phase 1 uses `MISSING_CONTEXT` or `AMBIGUOUS_REFERENCE`; use "
            "`LATE_DISCOVERED_CANDIDATE_DEFECT` only when evidence review reveals a defect that was not reasonably visible earlier. "
            "/ 第一阶段记录缺失语境或歧义；只有对照证据后才发现的候选缺陷才进入迟发现缺陷。",
            "- Naturalness is independent of truth and self-containment. / 自然度与事实正误、自包含性相互独立。",
            "",
            "## Case-based examples / 真实边界案例",
            "",
            "| Field | Case type | Independent fixture | Decision | Why |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in cases:
        escaped = {
            key: str(value).replace("|", "\\|").replace("\n", " ")
            for key, value in row.items()
        }
        lines.append(
            f"| `{escaped['field']}` | {escaped['category']} | {escaped['fixture']} | "
            f"`{escaped['decision']}` | {escaped['explanation']} |"
        )
    return "\n".join(lines).rstrip() + "\n"


def build(input_path: Path, cases_path: Path, output: Path) -> dict[str, Any]:
    rows = load_jsonl(input_path)
    cases = json.loads(cases_path.read_text(encoding="utf-8"))
    validate_rows(rows)
    output.mkdir(parents=True, exist_ok=False)
    write_jsonl(output / "PILOT4_EXTERNAL_BLIND_REVIEW_PACKET.jsonl", rows)
    (output / "PILOT4_EXTERNAL_BLIND_REVIEW_PACKET.md").write_text(
        packet_markdown(rows), encoding="utf-8"
    )
    (output / "PILOT4_EXTERNAL_BLIND_FIELD_GUIDE.md").write_text(
        guide_markdown(cases), encoding="utf-8"
    )
    with (output / "PILOT4_EXTERNAL_BLIND_REVIEW_TEMPLATE.csv").open(
        "w", encoding="utf-8-sig", newline=""
    ) as handle:
        writer = csv.DictWriter(
            handle, fieldnames=("blind_review_id",) + PHASE1_FIELDS + PHASE2_FIELDS
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({"blind_review_id": row["blind_review_id"]})
    return {
        "status": "PASS",
        "candidate_count": len(rows),
        "field_guide_case_count": len(cases),
        "review_result_filled_count": 0,
        "output": str(output),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.input, args.cases, args.output)))


if __name__ == "__main__":
    main()
