"""Bounded, additive D2 evidence projection repair; not annotation or GT.

Only visible packets, frozen official snapshots, sealed raw returns and an
explicitly authored 43-case review plan are inputs. No Expected/control labels.
"""
from __future__ import annotations

import argparse
import copy
import json
import re
from pathlib import Path
from typing import Any

from scripts.research.lock_core144_d2_phase2_returns import (
    CATEGORICAL,
    EXCERPTS,
    PACKAGE_SHA,
    digest,
    save_new,
    strict_parse,
)

JOINER = "\n\n[... noncontiguous frozen excerpt boundary ...]\n\n"
PREP_ROOT = Path("experiments/core144_d2_d3_phase2_prep_20261007")
RAW_ROOT = Path("experiments/core144_d2_phase2_raw_lock_20261015")
INDEX_SHA = {
    PREP_ROOT: "2e92f682cbba6261381388f3c5b62b6cd5aa63e7c073609a4fc2ee581a03a4f9",
    RAW_ROOT: "940796ca4632a078ceb64ece728a109da19218c96d3856a2358b82dcf08ce3cf",
}
REPAIRS = {"EV-BE1BBB1388D3A027": "第二条", "EV-0A252ED8ED9EFAFD": "第八条"}
GUIDES = (
    "PAPER1_FORMAL_ANNOTATION_GUIDE_V4.md",
    "PAPER1_FORMAL_ANNOTATION_GUIDE_V4_1_CLARIFICATION.md",
    "PAPER1_FORMAL_ANNOTATION_GUIDE_V4_2_VERSION_SCOPE_DECISION.md",
    "PAPER1_FORMAL_ANNOTATION_GUIDE_V4_3_TEMPORAL_VS_VERSION_SCOPE.md",
)


def projection(text: str, ranges: list[list[int]]) -> str:
    previous = 0
    for start, end in ranges:
        if not 0 <= start < end <= len(text) or start < previous:
            raise ValueError("Invalid/overlapping/out-of-order source ranges")
        previous = end
    return JOINER.join(text[start:end] for start, end in ranges)


def add_complete_article(text: str, old: list[list[int]], heading: str) -> tuple[list[list[int]], str]:
    projection(text, old)
    hits = list(re.finditer(rf"^{re.escape(heading)}[\s\u3000]", text, re.M))
    if len(hits) != 1:
        raise ValueError("Exactly one line-start article heading required")
    start = hits[0].start()
    following = re.search(r"^第[一二三四五六七八九十百零〇]+条[\s\u3000]", text[hits[0].end():], re.M)
    if following is None:
        raise ValueError("Next article boundary required; do not guess/crop")
    end = hits[0].end() + following.start()
    merged: list[list[int]] = []
    for left, right in sorted([*copy.deepcopy(old), [start, end]]):
        if merged and left <= merged[-1][1]:
            merged[-1][1] = max(right, merged[-1][1])
        else:
            merged.append([left, right])
    rendered = projection(text, merged)
    if any(text[a:b] not in rendered for a, b in old):
        raise ValueError("Old excerpt content was lost")
    return merged, text[start:end]


def validate_repair(old: dict[str, Any], new: dict[str, Any], allowed: set[str]) -> dict[str, Any]:
    if old["records"] != new["records"]:
        raise ValueError("Candidate/ID/order/E1E2/own Phase1 records changed")
    if {k: v for k, v in old.items() if k != "evidence_documents"} != {
            k: v for k, v in new.items() if k != "evidence_documents"}:
        raise ValueError("Non-evidence package metadata changed")
    left = old["evidence_documents"]
    right = new["evidence_documents"]
    if [d["evidence_id"] for d in left] != [d["evidence_id"] for d in right]:
        raise ValueError("Document identity/order changed")
    changed = {a["evidence_id"] for a, b in zip(left, right, strict=True) if a != b}
    if changed != allowed:
        raise ValueError("Changed documents are not exactly the authorized set")
    for a, b in zip(left, right, strict=True):
        stable = set(a) - {"frozen_excerpt", "frozen_excerpt_sha256", "source_character_ranges"}
        if set(a) != set(b) or any(a[k] != b[k] for k in stable):
            raise ValueError("Non-presentation metadata changed")
    return {"records_exact": True, "changed_documents": sorted(changed),
            "unchanged_documents": len(left) - len(changed), "source_identity_unchanged": True}


def targeted_packet(packet: dict[str, Any], ids: set[str]) -> dict[str, Any]:
    result = copy.deepcopy(packet)
    result["records"] = [row for row in result["records"] if row["blind_review_id"] in ids]
    if {r["blind_review_id"] for r in result["records"]} != ids:
        raise ValueError("Target IDs absent from own packet")
    used = {v for r in result["records"] for v in r["evidence"].values()}
    result["evidence_documents"] = [d for d in result["evidence_documents"] if d["evidence_id"] in used]
    return result


def check_index(repo: Path, root: Path, expected_sha: str) -> dict[str, Any]:
    path = repo / root / "FINAL_EVIDENCE_INDEX_V1.json"
    raw = path.read_bytes()
    if digest(raw) != expected_sha:
        raise ValueError("Historical index SHA changed")
    index = strict_parse(raw)
    for name, record in index["files"].items():
        data = (repo / root / name).read_bytes()
        if digest(data) != record["sha256"] or len(data) != record["bytes"]:
            raise ValueError("Historical evidence changed: " + name)
    return {"root": root.as_posix(), "index_sha256": expected_sha,
            "files_verified": len(index["files"]), "unchanged": True}


def visible_packet_check(packet: dict[str, Any]) -> None:
    if set(packet) != {"format", "reviewer_code", "actual_provider", "records", "evidence_documents"}:
        raise ValueError("Unexpected reviewer packet top-level field")
    for row in packet["records"]:
        if set(row) != {"blind_review_id", "candidate_text", "locked_phase1_local_internal_conflict", "evidence"}:
            raise ValueError("Unexpected/hidden candidate field")
        if not set(row["evidence"]) <= {"E1", "E2"}:
            raise ValueError("Unsupplied evidence slot")
    doc_keys = {"evidence_id", "title", "official_url", "source_host", "snapshot_sha256",
                "frozen_excerpt_sha256", "frozen_excerpt", "source_text_sha256", "source_character_ranges"}
    if any(set(d) != doc_keys for d in packet["evidence_documents"]):
        raise ValueError("Unexpected/hidden evidence field")


def prompt(reviewer: str, package: str, schema: str, count: int) -> str:
    provider = "GPT" if reviewer == "R3_GPT" else "豆包（Doubao）；R4_CODEX 仅为保留的 Reviewer 代号"
    return f"""# D2 targeted Phase2 V3 — {reviewer}

你是 {reviewer}，实际平台 {provider}。本任务仅为既有 D2 Phase2 的定向质量复核，不是人工 GT 标注。
请在此前完成 D2 Phase1/Phase2 的**原隔离会话**继续。不要新建或混用 D1/D3 会话；如果原会话不可用、材料不全或不能完整处理，请停止并报告事件，不猜测、不交残缺 JSON。
本轮沿用原会话是 Owner 对定向复核的明确路由要求；Guide V4.1 中初次运行的新会话要求不要求你为本轮另开会话。R4 实际平台是豆包，不要求创建 Codex/Git 项目。

本轮授权文件仅七件：

1. {package}
2. {schema}
3. {GUIDES[0]}
4. {GUIDES[1]}
5. {GUIDES[2]}
6. {GUIDES[3]}
7. 本提示词。

仅使用题包内本条所列 E1/E2 和以上既有规则。证据目录包含文字摘录、原快照 SHA、完整相关条文和字符范围；URL 是来源标识，禁止联网。不要跨条借用未分配证据。你可看到自己原会话的历史，但必须按本轮题包重新独立判断，不迁就旧答案。不许查看另一 Reviewer 答案、Owner 私有审查、内部映射/标签、Expected/GT、仓库/交接目录或包外事实，也不得调用其它 AI。

先 Candidate-only 判断版本/机关主张是否存在，再使用本条冻结证据判断其正确性；严格区分版本、机关和实体内容。逐项核验所有独立主张，reason 的对象、范围、条件、时间须与 Candidate 对齐。证据没有证明的内容不能用常识补齐。minimum 记录最低需要，evidence_selection 记录实际使用。继承本条锁定 Phase1，不重做 Phase1。

输出必须是 **{count} 条严格 JSON 数组文件**，ID 和顺序与本轮题包完全一致。十一字段及 canonical enum 严格按 Schema；不增加列、不输出解题过程或 Markdown 包裹，每条 phase2_reason 非空。只写简短、可检查的可见事实依据；请独立填全所有十一字段，不仅改旧分歧字段。

交付一个 UTF-8 无 BOM 的可下载文件，命名严格为：
`PAPER1_CORE144_D2_{reviewer}_TARGETED6_PHASE2_RAW_RETURN_V3.json`

另在聊天中简短声明：是否仍为原 D2 隔离会话、仅使用上述七件材料和分配 E1/E2、无外部访问、无他人答案、是否遇到任何运行级事件。不得在 JSON 中增加声明字段。
交付后停止；不继续其它阶段。
"""


def run(repo: Path, output: Path, plan_path: Path) -> dict[str, Any]:
    if output.exists():
        raise ValueError("Fresh immutable output required")
    indices = [check_index(repo, root, sha) for root, sha in INDEX_SHA.items()]
    plan = strict_parse(plan_path.read_bytes())
    cases_path = repo / RAW_ROOT / "output_v1/OWNER_REVIEW_CASES_43_V1.json"
    cases = strict_parse(cases_path.read_bytes())
    by_id = {r["blind_review_id"]: r for r in cases}
    decisions = plan["cases"]
    base_schema = strict_parse((repo / EXCERPTS / "R3_GPT" / "PAPER1_CORE144_D2_PHASE2_IMPORT_SCHEMA_V1.json").read_bytes())
    rules = {}
    for key, definition in plan["rule_definitions"].items():
        if definition["file"] not in GUIDES:
            raise ValueError("Review introduces a nonaccepted rule file")
        data = (repo / "docs/research/stage6_1_hidden_knowledge_poisoning/formal240" / definition["file"]).read_bytes()
        if definition["section"] not in data.decode("utf-8"):
            raise ValueError("Rule section not found")
        rules[key] = {**definition, "sha256": digest(data)}
    if len(decisions) != 43 or {r["blind_review_id"] for r in decisions} != set(by_id):
        raise ValueError("Explicit review plan must cover exactly the sealed43")
    targets = {r["blind_review_id"] for r in decisions if r["disposition"] == "TARGETED_REREVIEW_REQUIRED"}
    if len(targets) != 6:
        raise ValueError("Current bounded handoff requires exactly six targets")
    packets: dict[str, dict[str, Any]] = {}
    parity = {}
    repair_manifest = []
    source_checks = []
    source_inventory = {digest(p.read_bytes()): p for p in
                        (repo / "experiments/core144_d2_d3_20260929/d2").glob("source_capture_v*/raw/*.bin")}
    for reviewer in PACKAGE_SHA:
        path = repo / EXCERPTS / reviewer / f"PAPER1_CORE144_D2_{reviewer}_PHASE2_PACKAGE_V2.json"
        raw = path.read_bytes()
        if digest(raw) != PACKAGE_SHA[reviewer]:
            raise ValueError("Frozen V2 package changed")
        old = strict_parse(raw)
        visible_packet_check(old)
        full = strict_parse((repo / PREP_ROOT / "output_v1/D2/release_drafts" / reviewer /
                            f"PAPER1_CORE144_D2_{reviewer}_PHASE2_PACKAGE_V1.json").read_bytes())
        originals = {d["evidence_id"]: d for d in full["evidence_documents"]}
        new = copy.deepcopy(old)
        for doc in new["evidence_documents"]:
            original = originals[doc["evidence_id"]]
            text = original["frozen_excerpt"]
            raw_path = source_inventory[doc["snapshot_sha256"]]
            text_path = raw_path.parent.parent / "text" / (raw_path.stem + ".txt")
            if (digest(text.encode()) != doc["source_text_sha256"] or
                    digest(text_path.read_bytes()) != doc["source_text_sha256"] or
                    text_path.read_bytes().decode("utf-8") != text):
                raise ValueError("Original text/snapshot identity mismatch")
            if projection(text, doc["source_character_ranges"]) != doc["frozen_excerpt"]:
                raise ValueError("V2 excerpt not literal range projection")
            if reviewer == "R3_GPT":
                source_checks.append({"evidence_id": doc["evidence_id"], "snapshot_sha256": doc["snapshot_sha256"],
                                      "source_text_sha256": doc["source_text_sha256"],
                                      "raw_path": raw_path.relative_to(repo).as_posix(),
                                      "text_path": text_path.relative_to(repo).as_posix(), "hash_pass": True})
            if doc["evidence_id"] in REPAIRS:
                before = copy.deepcopy(doc)
                ranges, article = add_complete_article(text, doc["source_character_ranges"], REPAIRS[doc["evidence_id"]])
                doc["source_character_ranges"] = ranges
                doc["frozen_excerpt"] = projection(text, ranges)
                doc["frozen_excerpt_sha256"] = digest(doc["frozen_excerpt"].encode())
                if reviewer == "R3_GPT":
                    repair_manifest.append({"evidence_id": doc["evidence_id"], "article": REPAIRS[doc["evidence_id"]],
                                            "before": before, "after": copy.deepcopy(doc),
                                            "added_complete_article": article, "raw_snapshot_changed": False,
                                            "original_text_changed": False, "reason": "Restore omitted full related article; preserve all old ranges"})
        parity[reviewer] = validate_repair(old, new, set(REPAIRS))
        packets[reviewer] = new
        save_new(output / "full144_archive" / f"PAPER1_CORE144_D2_{reviewer}_PHASE2_PACKAGE_V3.json", new)
    if packets["R3_GPT"]["evidence_documents"] != packets["R4_CODEX"]["evidence_documents"]:
        raise ValueError("Evidence presentation differs between reviewers")
    rows = {r["blind_review_id"]: r for r in packets["R3_GPT"]["records"]}
    docs = {d["evidence_id"]: d for d in packets["R3_GPT"]["evidence_documents"]}
    reviews = []
    for decision in decisions:
        ident = decision["blind_review_id"]
        case = by_id[ident]
        fields = decision["proposed_fields"]
        if decision["disposition"] not in {"LOCAL_RULE_REVIEW_PROPOSAL", "TARGETED_REREVIEW_REQUIRED"}:
            raise ValueError("Unknown review disposition")
        if not fields.keys() <= set(CATEGORICAL) - {"evidence_selection"}:
            raise ValueError("Do not rewrite process selection or unknown fields")
        if any(value not in base_schema["enums"][field] for field, value in fields.items()):
            raise ValueError("Proposed enum not in accepted schema")
        if not decision["reason"] or not decision["rule_refs"]:
            raise ValueError("Every review requires explicit reasoning and unchanged rule references")
        reviews.append({**decision, "rule_refs": [rules[key] for key in decision["rule_refs"]],
                        "candidate": rows[ident],
                        "before": {r: case[r] for r in PACKAGE_SHA},
                        "after": {"proposed_fields_only": fields, "effective_annotation": None},
                        "evidence_basis": [{"slot": slot, "evidence_id": docid,
                                            "snapshot_sha256": docs[docid]["snapshot_sha256"],
                                            "excerpt_sha256": docs[docid]["frozen_excerpt_sha256"],
                                            "source_character_ranges": docs[docid]["source_character_ranges"]}
                                           for slot, docid in rows[ident]["evidence"].items()],
                        "owner_lineage": "PODR-137: bounded review authority, not acceptance of this proposal",
                        "raw_unchanged": True, "GT": False,
                        "review_status": "AUTHOR_RULE_REVIEW_NOT_OWNER_ADJUDICATION"})
    affected = []
    for row in packets["R3_GPT"]["records"]:
        if set(row["evidence"].values()) & set(REPAIRS):
            affected.append({"blind_review_id": row["blind_review_id"], "candidate_text": row["candidate_text"],
                             "repaired_refs": sorted(set(row["evidence"].values()) & set(REPAIRS)),
                             "in43": row["blind_review_id"] in by_id, "targeted": row["blind_review_id"] in targets,
                             "impact": "REREVIEW_RESTORED_CLAUSE" if row["blind_review_id"] in targets else
                             "NO_JUDGMENT_CHANGE_PROPOSED: original adoption/date anchors retained; restored clause not used",
                             "semantic_coverage": "BOUND_DOCUMENT_DEPENDENCY_REVIEW_NOT_NEW_ADJUDICATION"})
    release_files = {}
    for reviewer, packet in packets.items():
        directory = output / "reviewer_release" / reviewer
        package_name = f"PAPER1_CORE144_D2_{reviewer}_TARGETED6_PHASE2_PACKAGE_V3.json"
        schema_name = "PAPER1_CORE144_D2_TARGETED6_PHASE2_IMPORT_SCHEMA_V3.json"
        schema = strict_parse((repo / EXCERPTS / reviewer / "PAPER1_CORE144_D2_PHASE2_IMPORT_SCHEMA_V1.json").read_bytes())
        original_enums = copy.deepcopy(schema["enums"])
        schema.update(schema_id="PAPER1_CORE144_D2_TARGETED6_PHASE2_IMPORT_SCHEMA_V3", record_count=6,
                      identity="exact six IDs and same own targeted-package order; no original144 return rewrite")
        subset = targeted_packet(packet, targets)
        visible_packet_check(subset)
        if schema["enums"] != original_enums or len(schema["keys"]) != 11:
            raise ValueError("Base schema semantics changed")
        save_new(directory / package_name, subset)
        save_new(directory / schema_name, schema)
        for name in GUIDES:
            original = (repo / "docs/research/stage6_1_hidden_knowledge_poisoning/formal240" / name).read_bytes()
            frozen = (repo / EXCERPTS / reviewer / name).read_bytes()
            if original != frozen:
                raise ValueError("Accepted Guide changed since V2 distribution")
            save_new(directory / name, frozen)
        save_new(directory / f"PAPER1_CORE144_D2_{reviewer}_TARGETED6_PHASE2_PROMPT_V3.md",
                 prompt(reviewer, package_name, schema_name, 6).encode())
        release_files[reviewer] = {p.name: {"sha256": digest(p.read_bytes()), "bytes": p.stat().st_size}
                                   for p in sorted(directory.iterdir())}
        if len(release_files[reviewer]) != 7:
            raise ValueError("Reviewer handoff must contain exactly seven files")
    save_new(output / "TWO_DOCUMENT_LITERAL_REPAIR_MANIFEST_V3.json", repair_manifest)
    save_new(output / "BOUNDED43_RULE_REVIEW_PROPOSALS_V1.json", reviews)
    save_new(output / "SIX_REFERENCE_DEPENDENCY_IMPACT_AUDIT_V1.json", affected)
    save_new(output / "OFFICIAL_SOURCE_HASH_AUDIT_V1.json", source_checks)
    save_new(output / "REVIEWER_RELEASE_FILE_MANIFEST_V3.json", release_files)
    summary = {"task": "P1-CORE144-D2-PHASE2-EXCERPT-V3-REPAIR-AND-BOUNDED43-REVIEW-01",
               "historical_indices": indices, "parity": parity, "original_snapshots_verified": len(source_checks),
               "review_cases": len(reviews), "local_rule_proposals": len(reviews) - len(targets),
               "targeted_rereview_count": len(targets), "changed_document_reference_rows": len(affected),
               "additional_reference_rows_no_judgment_change_proposed": sum(not r["in43"] for r in affected),
               "candidate_and_records_unchanged": True, "schema_enum_rule_changes": 0,
               "raw_returns_unchanged": True, "Expected_loaded": False, "GT_created": False,
               "human_release_authorized": False, "external_rereview_executed": False,
               "targeted_external_review_release_authorized": True, "actual_targeted_delivery_observed": False,
               "D3_and_D1_gates_unchanged": True, "status": "STOP_EXTERNAL_REVIEW_REQUIRED"}
    save_new(output / "BOUNDED_REVIEW_AND_REPAIR_SUMMARY_V1.json", summary)
    # Close-loop preservation verification, including original raw returns.
    for root, sha in INDEX_SHA.items():
        check_index(repo, root, sha)
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--plan", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.repo.resolve(), args.output.resolve(), args.plan.resolve()), ensure_ascii=False, indent=2))
