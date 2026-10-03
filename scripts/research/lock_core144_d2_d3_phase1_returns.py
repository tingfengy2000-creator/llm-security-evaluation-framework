"""Byte-lock Core144 Phase1 originals and audit only candidate-visible inputs."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

FIELDS = (
    "text_naturalness",
    "local_internal_conflict",
    "self_containment",
    "ambiguous_referent",
    "meta_or_template_language",
)
DEFAULTS = ("NATURAL", "NO", "PASS", "NO", "NO")
PACKAGE_HASHES = {
    (
        "D2",
        "R3_GPT",
    ): "174bf1873c92850347c4dc5da6ddc36921a58cfb20ee900175554162925ca695",
    (
        "D2",
        "R4_CODEX",
    ): "326303673c4c0d9383f4184eab2d1563944882e05bd544ea2f3e90c28fc76160",
    (
        "D3",
        "R3_GPT",
    ): "f58d1bf0fc8f124061ae3b763345fc83f7ae9ceb5ac608a6c5039baef3d14b7b",
    (
        "D3",
        "R4_CODEX",
    ): "131ef410d4be786d39c3da1c7d0999f55f4be45b5068d86f9184905878720cd1",
}
SCHEMA_HASH = "d143d5edce1434ac2e0be0e3a818c0ebe2fd0d58499c6962a7ca68e443aa3307"


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise ValueError(f"non-JSON constant: {value}")


def parse(raw: bytes) -> Any:
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError("UTF-8 BOM is not allowed by the reviewer contract")
    return json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=unique_object,
        parse_constant=reject_constant,
    )


def save_new(path: Path, data: Any) -> None:
    payload = (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    with path.open("xb") as stream:
        stream.write(payload)
    os.chmod(path, 0o444)


def lock_original(source: Path, target: Path) -> dict[str, Any]:
    raw = source.read_bytes()
    with target.open("xb") as stream:
        stream.write(raw)
    os.chmod(target, 0o444)
    if target.read_bytes() != raw or source.read_bytes() != raw:
        raise ValueError("original changed during lock or byte-copy failure")
    return {
        "source_path": str(source.resolve()),
        "locked_path": str(target.resolve()),
        "bytes": len(raw),
        "sha256": digest(raw),
        "byte_parity": True,
        "read_only_copy": True,
        "locked_at_utc": now(),
        "provider": "DOUBAO" if "R4_CODEX" in target.name else "GPT",
    }


def validate(
    raw: bytes, packet: list[dict[str, Any]], schema: dict[str, Any]
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    report: dict[str, Any] = {"errors": [], "validation_pass": False}
    try:
        rows = parse(raw)
    except (ValueError, UnicodeError) as exc:
        report["errors"].append(str(exc))
        return report, []
    if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
        report["errors"].append("return must be a JSON array of objects")
        return report, []
    keys = schema["keys"]
    expected_ids = [row["blind_review_id"] for row in packet]
    ids = [row.get("blind_review_id") for row in rows]
    report.update(
        records=len(rows),
        unique_ids=len(set(ident for ident in ids if isinstance(ident, str))),
        count_exact=len(rows) == 144,
        id_order_exact=ids == expected_ids,
        id_set_exact=set(ident for ident in ids if isinstance(ident, str))
        == set(expected_ids),
        key_order_exact=all(list(row) == keys for row in rows),
    )
    if not report["count_exact"] or not report["id_order_exact"]:
        report["errors"].append("record count / reviewer-specific ID order mismatch")
    for index, row in enumerate(rows):
        if set(row) != set(keys):
            report["errors"].append(f"row {index + 1}: schema keys mismatch")
            continue
        if any(not isinstance(row[key], str) for key in keys):
            report["errors"].append(f"row {index + 1}: all values must be strings")
            continue
        for field in FIELDS:
            if row[field] not in schema["enums"][field]:
                report["errors"].append(f"row {index + 1}: illegal {field}")
        flagged = any(row[field] != default for field, default in zip(FIELDS, DEFAULTS))
        if flagged and not row["issue_note"].strip():
            report["errors"].append(
                f"row {index + 1}: flagged field requires issue_note"
            )
    if report["errors"]:
        return report, rows
    report.update(
        validation_pass=True,
        exact_schema_keys=True,
        legal_enums=True,
        required_notes_pass=True,
        utf8_without_bom=True,
        duplicate_json_keys=0,
        distributions={
            field: dict(Counter(row[field] for row in rows)) for field in FIELDS
        },
        nonblank_notes=sum(bool(row["issue_note"].strip()) for row in rows),
    )
    return report, rows


def compare(
    packet: list[dict[str, Any]], r3: list[dict[str, Any]], r4: list[dict[str, Any]]
) -> dict[str, Any]:
    left = {row["blind_review_id"]: row for row in r3}
    right = {row["blind_review_id"]: row for row in r4}
    agreement = {}
    disagreements = []
    flags = []
    for field in FIELDS:
        ids = [row["blind_review_id"] for row in packet]
        differing = [
            ident for ident in ids if left[ident][field] != right[ident][field]
        ]
        agreement[field] = {
            "agree": 144 - len(differing),
            "total": 144,
            "agreement_rate": (144 - len(differing)) / 144,
            "disagreement_ids": differing,
        }
    for row in packet:
        ident = row["blind_review_id"]
        differing = [
            field for field in FIELDS if left[ident][field] != right[ident][field]
        ]
        item = {
            "blind_review_id": ident,
            "candidate_text": row["candidate_text"],
            "r3": left[ident],
            "r4": right[ident],
            "different_fields": differing,
        }
        if differing:
            disagreements.append(item)
        if any(
            result[field] != default
            for result in (left[ident], right[ident])
            for field, default in zip(FIELDS, DEFAULTS)
        ):
            flags.append(item)
    return {
        "categorical_agreement": agreement,
        "disagreement_rows": disagreements,
        "disagreement_row_count": len(disagreements),
        "disagreement_cell_count": sum(
            len(row["different_fields"]) for row in disagreements
        ),
        "flagged_rows": flags,
        "issue_note_raw_identical_rows": sum(
            left[ident]["issue_note"] == right[ident]["issue_note"] for ident in left
        ),
        "issue_note_semantics": "TEXT_VISIBLE_TRIAGE_REQUIRED_NOT_LITERAL_AGREEMENT_GATE",
    }


def build_triage(output: Path) -> dict[str, Any]:
    """Create a separate Owner-only decision view; never change original results."""
    qa = parse((output / "PHASE1_VALIDATION_AND_COMPARISON_V1.json").read_bytes())
    triage: dict[str, Any] = {
        "scope": "OWNER_ONLY_TEXT_VISIBLE_TRIAGE_NOT_EXTERNAL_REVIEWER_PACKAGE",
        "raw_values_changed": False,
        "candidate_text_changed": False,
        "hidden_mapping_labels_expected_gt_or_evidence_loaded": False,
        "owner_decision_required": True,
        "domains": {},
    }
    lines = [
        "# D2/D3 Phase1 定向诊断与 Owner 决策包 V1",
        "",
        "仅供 Owner / 本机控制面阅读。不可发给 R3/R4 或新盲审员，内含已有答案。",
        "原始返回和候选原文均保持不变。本表只读取冻结候选题包和已锁定的 Phase1 原答；",
        "未加载角色、HKP、S、映射、Expected、GT、Evidence 或人工标注答案。",
        "",
        "两域 Phase2 暂扣。分歧数不是已确认错误数；双方一致的内部矛盾 YES 也不能单独认定出题缺陷。",
        "每一条需判断真实文本缺陷、合法范围限定或个人表达偏好。不得以投票改写 raw。",
        "",
        "建议优先审阅 D3 两条共同 self_containment=FLAG、两条共同元语言 YES 和",
        "CBR-81E40769899B68 的必要条件缺失；D2 八条共同元语言 YES 要逐句区分",
        "必要事实范围说明与对比较/文本处理过程的叙述。",
        "",
        "## 核心条件缺口",
        "",
        "D3 CBR-81E40769899B68 前句仅禁止‘在可替代时’唯一使用人脸识别，",
        "后句仅交代当事人拒绝。拒绝并不推出有替代方式；就 Candidate 自身无法确定",
        "两句适用条件相同。此为文本内条件诊断，未借助法律事实或内部目标标签。",
        "建议保留 R3 UNCERTAIN、R4 YES 原答，先由 Owner 决定是否补明条件并定向重审。",
        "",
    ]
    for domain, item in qa["domains"].items():
        comparison = item.get("comparison")
        if comparison is None:
            triage["domains"][domain] = {
                "gate": "INVALID_RETURN_BLOCKER",
                "phase2_release_authorized": False,
            }
            continue
        issues = [
            row
            for row in comparison["flagged_rows"]
            if row["different_fields"]
            or any(
                result[field] != default
                for result in (row["r3"], row["r4"])
                for field, default in zip(FIELDS, DEFAULTS)
                if field != "local_internal_conflict"
            )
        ]
        consensus = {
            "self_containment_flag": [
                row["blind_review_id"]
                for row in issues
                if row["r3"]["self_containment"]
                == row["r4"]["self_containment"]
                == "FLAG"
            ],
            "meta_language_yes": [
                row["blind_review_id"]
                for row in issues
                if row["r3"]["meta_or_template_language"]
                == row["r4"]["meta_or_template_language"]
                == "YES"
            ],
            "minor_naturalness": [
                row["blind_review_id"]
                for row in issues
                if row["r3"]["text_naturalness"]
                == row["r4"]["text_naturalness"]
                == "MINOR_ISSUE"
            ],
        }
        triage["domains"][domain] = {
            "issue_rows": len(issues),
            "categorical_disagreement_rows": comparison["disagreement_row_count"],
            "categorical_disagreement_cells": comparison["disagreement_cell_count"],
            "consensus_flags": consensus,
            "items": issues,
            "gate": "OWNER_DECISION_REQUIRED_PHASE2_WITHHELD",
            "phase2_release_authorized": False,
        }
        lines += [
            f"## {domain}：{len(issues)} 条需审阅的候选",
            "",
            f"分类分歧 {comparison['disagreement_row_count']} 条 / {comparison['disagreement_cell_count']} 字段；",
            "另含双方一致但仍需处理的文本质量标记。",
            "",
        ]
        for row in issues:
            lines += [
                f"### {row['blind_review_id']}",
                "",
                row["candidate_text"],
                "",
                "| 字段 | R3-GPT 原值 | R4-Doubao 原值 |",
                "|---|---|---|",
            ]
            lines.extend(
                f"| {field} | {row['r3'][field]} | {row['r4'][field]} |"
                for field in FIELDS
            )
            lines += [
                "",
                f"R3 原始 issue_note：{row['r3']['issue_note'] or '（空）'}",
                "",
                f"R4 原始 issue_note：{row['r4']['issue_note'] or '（空）'}",
                "",
                "Owner 决策：待填写；原件不改，后续决定另建 overlay / repair 版本。",
                "",
            ]
    save_new(output / "PHASE1_OWNER_TRIAGE_V1.json", triage)
    with (output / "PAPER1_CORE144_D2_D3_PHASE1_OWNER_DECISION_PACKET_V1.md").open(
        "x", encoding="utf-8", newline="\n"
    ) as stream:
        stream.write("\n".join(lines) + "\n")
    save_new(
        output / "PHASE1_GATE_V1.json",
        {
            "domains": {
                domain: {"phase2_release_authorized": False, "gate": item["gate"]}
                for domain, item in triage["domains"].items()
            },
            "raw_locks_complete": True,
            "owner_session_attestation": "OWNER_ATTESTED",
            "human_ab_started": False,
            "gt_created": False,
            "split_executed": False,
            "training_started": False,
        },
    )
    return triage


def finalize_receipt(repo: Path, output: Path) -> dict[str, Any]:
    """Run scoped checks and index preserved evidence in a new receipt."""
    report_path = (
        "docs/research/stage6_1_hidden_knowledge_poisoning/core144/"
        "PAPER1_CORE144_D2_D3_PHASE1_RAW_LOCK_AND_GATE_V1.md"
    )
    state_path = (
        "docs/research/stage6_1_hidden_knowledge_poisoning/core144/"
        "PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V4.md"
    )
    documents = [
        "PROJECT_MASTER_CONTEXT.md",
        "docs/governance/current_work_state.md",
        "docs/governance/experiment_master_record.md",
        "docs/governance/project_owner_decision_register.md",
        "docs/governance/research_execution_log.md",
        "docs/research/stage6_1_hidden_knowledge_poisoning/README.md",
        "docs/research/stage6_1_hidden_knowledge_poisoning/agent/experiment_ledger_agentUse.md",
        "docs/research/stage6_1_hidden_knowledge_poisoning/core144/README.md",
        "docs/research/stage6_1_hidden_knowledge_poisoning/human/experiment_ledger_tingfeng.md",
        "docs/research/stage6_1_hidden_knowledge_poisoning/human/owner_requirement_register.md",
        "docs/research/stage6_1_hidden_knowledge_poisoning/stage_process/S6.1-P1_work_process.md",
        report_path,
        state_path,
    ]
    task_files = documents + [
        "scripts/research/lock_core144_d2_d3_phase1_returns.py",
        "tests/research/test_core144_d2_d3_phase1_lock.py",
    ]
    checks: dict[str, Any] = {}

    def command(args: list[str]) -> str:
        process = subprocess.run(
            args, cwd=repo, capture_output=True, text=True, encoding="utf-8"
        )
        if process.returncode:
            raise ValueError(f"check failed: {args}: {process.stdout}{process.stderr}")
        return process.stdout + process.stderr

    worktrees = command(["git", "worktree", "list", "--porcelain"])
    matches = [
        entry
        for entry in worktrees.split("\n\n")
        if "branch refs/heads/research/stage6-1-hidden-poisoning" in entry.splitlines()
    ]
    if len(matches) != 1:
        raise ValueError("dynamic worktree uniqueness failure")
    bound = next(
        line[9:] for line in matches[0].splitlines() if line.startswith("worktree ")
    )
    if Path(bound).resolve() != repo.resolve():
        raise ValueError("worktree does not bind this audit directory")
    checks["dynamic_worktree_unique"] = True

    manifest = parse((output / "RAW_LOCK_MANIFEST_V1.json").read_bytes())
    for item in manifest["raw_artifacts"].values():
        original = Path(item["source_path"]).read_bytes()
        locked = Path(item["locked_path"])
        if original != locked.read_bytes() or digest(original) != item["sha256"]:
            raise ValueError("raw source/copy SHA or byte parity failure")
        if locked.stat().st_mode & 0o222:
            raise ValueError("locked raw is no longer read-only")
    checks["four_originals_still_byte_identical_read_only"] = True
    checks["owner_isolation_evidence"] = "OWNER_ATTESTED_NOT_MACHINE_PROOF"
    gate = parse((output / "PHASE1_GATE_V1.json").read_bytes())
    if any(item["phase2_release_authorized"] for item in gate["domains"].values()):
        raise ValueError("open Phase1 triage must hold Phase2")
    checks["phase2_held_both_domains"] = True

    expected_hashes = dict(PACKAGE_HASHES)
    for domain in ("D2", "D3"):
        reviewer_dir = (
            repo
            / "experiments/core144_d2_d3_20260929"
            / domain.lower()
            / "domain_release_v1/reviewer"
        )
        schema = reviewer_dir / f"PAPER1_CORE144_{domain}_PHASE1_IMPORT_SCHEMA_V1.json"
        if digest(schema.read_bytes()) != SCHEMA_HASH:
            raise ValueError("frozen schema changed")
        for reviewer in ("R3_GPT", "R4_CODEX"):
            package = (
                reviewer_dir
                / f"PAPER1_CORE144_{domain}_{reviewer}_PHASE1_PACKAGE_V1.json"
            )
            if digest(package.read_bytes()) != expected_hashes[(domain, reviewer)]:
                raise ValueError("frozen candidate-only package changed")
    checks["frozen_candidate_packets_and_schema_unchanged"] = True

    preexisting = {
        "docs/superpowers/specs/2026-07-01-stage6-rag-security-trustworthy-retrieval-design.md",
        "docs/research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_HUMAN_ANNOTATION_MASTER_GUIDE_V1.pdf",
    }
    tracked_changed = set(
        command(["git", "diff", "--name-only", manifest["source_head"]]).splitlines()
    )
    untracked = set(
        command(["git", "ls-files", "--others", "--exclude-standard"]).splitlines()
    )
    if (tracked_changed | untracked) - set(task_files) - preexisting:
        raise ValueError("unexpected changes outside task whitelist")
    checks["task_changes_limited_to_code_tests_and_governance"] = True
    checks["workbooks_candidates_evidence_contracts_stage1_to_5_not_edited"] = True
    checks["preexisting_design_and_pdf_excluded_from_task"] = True

    public_texts = {}
    for filename in task_files:
        content = (repo / filename).read_bytes().decode("utf-8", errors="strict")
        if filename in untracked:
            new_text = content
        else:
            diff = command(["git", "diff", "--unified=0", "--", filename])
            new_text = "\n".join(
                line[1:]
                for line in diff.splitlines()
                if line.startswith("+") and not line.startswith("+++")
            )
        public_texts[filename] = new_text
        for target in re.findall(r"\]\(([^)]+)\)", new_text):
            if "://" in target or target.startswith("#"):
                continue
            destination = (repo / filename).parent / target.split("#", 1)[0]
            if not destination.exists():
                raise ValueError(
                    f"broken new local Markdown link: {filename}: {target}"
                )
    checks["task_files_utf8"] = True
    checks["new_markdown_links_resolve"] = True
    pattern = re.compile(
        r"[CDE]:[/\\]|sk-[A-Za-z0-9]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY-----"
    )
    if any(pattern.search(value) for value in public_texts.values()):
        raise ValueError("public additions contain a secret/private absolute path")
    checks["task_public_additions_secret_private_path_scan"] = "PASS"
    for filename in documents:
        if "2026-10-03" not in (repo / filename).read_text(encoding="utf-8"):
            raise ValueError("missing current documentation checkpoint")
    checks["mandatory_documentation_closeout"] = "PASS"
    checks["research_authority_lessons_unchanged_no_semantic_decision"] = True
    command(
        [
            "git",
            "check-ignore",
            str(output.relative_to(repo) / "RAW_LOCK_MANIFEST_V1.json"),
        ]
    )
    checks["private_evidence_git_ignored"] = True

    python = str(repo / ".venv/Scripts/python.exe")
    commands = [
        [
            python,
            "-m",
            "unittest",
            "discover",
            "-s",
            "tests/research",
            "-p",
            "test_core144_d2_d3_phase1_lock.py",
            "-v",
        ],
        [python, "-m", "ruff", "check", *task_files[-2:]],
        [
            python,
            "-m",
            "mypy",
            "--ignore-missing-imports",
            "--explicit-package-bases",
            *task_files[-2:],
        ],
        ["git", "diff", "--check", "--", *task_files],
    ]
    runs = [
        {"command": args, "exit_code": 0, "output": command(args)} for args in commands
    ]
    receipt = {
        "created_at_utc": now(),
        "source_head": manifest["source_head"],
        "scope": "MECHANICAL_CHECKS_PASS_SEMANTIC_ACCEPTANCE_PENDING",
        "checks": checks,
        "command_results": runs,
        "task_files": task_files,
        "no_candidate_raw_or_rule_rewrite": True,
        "no_human_gt_split_training_or_new_review_executed": True,
    }
    save_new(output / "QA_AND_EXECUTION_RECEIPT_V1.json", receipt)
    index = {
        "created_at_utc": now(),
        "files": [
            {
                "path": path.relative_to(output).as_posix(),
                "sha256": digest(path.read_bytes()),
                "bytes": path.stat().st_size,
            }
            for path in sorted(output.rglob("*"))
            if path.is_file()
        ],
        "audit_implementation": [
            {"path": filename, "sha256": digest((repo / filename).read_bytes())}
            for filename in task_files[-2:]
        ],
    }
    save_new(output / "FINAL_EVIDENCE_INDEX_V1.json", index)
    return receipt


def run(
    repo: Path, output: Path, sources: dict[tuple[str, str], Path]
) -> dict[str, Any]:
    if output.exists():
        raise ValueError(
            "use a fresh additive output namespace; overwrite is prohibited"
        )
    output.mkdir(parents=True)
    raw_dir = output / "raw"
    raw_dir.mkdir()
    locks = {}
    for (domain, reviewer), source in sources.items():
        filename = f"PAPER1_CORE144_{domain}_{reviewer}_PHASE1_RAW_RETURN_V1.json"
        locks[f"{domain}_{reviewer}"] = lock_original(source, raw_dir / filename)
    lock_manifest = {
        "scope": "CORE144_D2_D3_PHASE1_RAW_LOCK",
        "source_head": "79c65219845379a710a076ee50f791b0faad9c1c",
        "owner_attestation": {
            "status": "OWNER_ATTESTED",
            "statement": "Owner confirms all four reviews ran in completely fresh isolated sessions.",
            "machine_proven_session_isolation": False,
            "platform_session_ids": None,
        },
        "raw_artifacts": locks,
        "all_raw_locked_before_validation": True,
        "raw_lock_complete_at_utc": now(),
    }
    save_new(output / "RAW_LOCK_MANIFEST_V1.json", lock_manifest)
    result: dict[str, Any] = {
        "scope": "CANDIDATE_ONLY_PREANNOTATION_QA_NOT_GT",
        "validation_started_at_utc": now(),
        "construction_mapping_loaded": False,
        "expected_gt_or_evidence_loaded": False,
        "domains": {},
    }
    for domain in ("D2", "D3"):
        reviewer_dir = (
            repo
            / "experiments/core144_d2_d3_20260929"
            / domain.lower()
            / "domain_release_v1/reviewer"
        )
        schema_raw = (
            reviewer_dir / f"PAPER1_CORE144_{domain}_PHASE1_IMPORT_SCHEMA_V1.json"
        ).read_bytes()
        if digest(schema_raw) != SCHEMA_HASH:
            raise ValueError("frozen schema SHA mismatch")
        schema = parse(schema_raw)
        packets = {}
        reports = {}
        valid_rows = {}
        for reviewer in ("R3_GPT", "R4_CODEX"):
            package_raw = (
                reviewer_dir
                / f"PAPER1_CORE144_{domain}_{reviewer}_PHASE1_PACKAGE_V1.json"
            ).read_bytes()
            if digest(package_raw) != PACKAGE_HASHES[(domain, reviewer)]:
                raise ValueError("frozen reviewer package SHA mismatch")
            packet = parse(package_raw)
            if (
                not isinstance(packet, list)
                or len(packet) != 144
                or any(
                    set(row) != {"blind_review_id", "candidate_text"} for row in packet
                )
            ):
                raise ValueError("candidate-only packet contract mismatch")
            packets[reviewer] = packet
            raw = Path(locks[f"{domain}_{reviewer}"]["locked_path"]).read_bytes()
            reports[reviewer], valid_rows[reviewer] = validate(raw, packet, schema)
        texts = [
            {row["blind_review_id"]: row["candidate_text"] for row in packets[reviewer]}
            for reviewer in ("R3_GPT", "R4_CODEX")
        ]
        if texts[0] != texts[1] or len(texts[0]) != 144:
            raise ValueError("reviewer packet information parity failure")
        item: dict[str, Any] = {
            "validation": reports,
            "packet_information_parity": True,
        }
        structural_pass = all(report["validation_pass"] for report in reports.values())
        item["structural_pass"] = structural_pass
        if structural_pass:
            item["comparison"] = compare(
                packets["R3_GPT"], valid_rows["R3_GPT"], valid_rows["R4_CODEX"]
            )
        item["phase2_release_authorized"] = False
        item["gate_status"] = (
            "PHASE1_TRIAGE_PENDING" if structural_pass else "INVALID_RETURN_BLOCKER"
        )
        result["domains"][domain] = item
    result["validation_completed_at_utc"] = now()
    save_new(output / "PHASE1_VALIDATION_AND_COMPARISON_V1.json", result)
    save_new(
        output / "INPUT_OUTPUT_INDEX_V1.json",
        {
            "files": [
                {
                    "path": str(path.relative_to(output)),
                    "sha256": digest(path.read_bytes()),
                    "bytes": path.stat().st_size,
                }
                for path in sorted(output.rglob("*"))
                if path.is_file()
            ],
            "reviewer_input_hashes": {
                f"{domain}_{reviewer}": value
                for (domain, reviewer), value in PACKAGE_HASHES.items()
            },
            "schema_sha256": SCHEMA_HASH,
        },
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    for name in ("d2-r3", "d2-r4", "d3-r3", "d3-r4"):
        parser.add_argument(f"--{name}", required=True, type=Path)
    args = parser.parse_args()
    sources = {
        ("D2", "R3_GPT"): args.d2_r3,
        ("D2", "R4_CODEX"): args.d2_r4,
        ("D3", "R3_GPT"): args.d3_r3,
        ("D3", "R4_CODEX"): args.d3_r4,
    }
    result = run(args.repo.resolve(), args.output.resolve(), sources)
    print(
        json.dumps(
            {
                domain: {
                    "structural_pass": item["structural_pass"],
                    "validation": item["validation"],
                    "agreement": item.get("comparison", {}).get(
                        "categorical_agreement"
                    ),
                    "disagreement_rows": item.get("comparison", {}).get(
                        "disagreement_row_count"
                    ),
                    "gate": item["gate_status"],
                }
                for domain, item in result["domains"].items()
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
