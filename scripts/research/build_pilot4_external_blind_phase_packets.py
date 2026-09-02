"""Split the frozen Pilot4 blind-review artifact into release-gated phases.

This builder reads only the previously sanitized combined packet, independent
teaching cases, title provenance, and opaque mapping bytes.  It never loads an
expected contract and never creates a semantic answer.
"""

from __future__ import annotations

import argparse
import csv
from hashlib import sha256
import json
from pathlib import Path
import shutil
from typing import Any, Mapping, Sequence

from llmguard.domains.retrieval.hidden_poisoning.external_blind_review import (
    PHASE1_FIELDS,
    PHASE1_RETURN_FIELDS,
    PHASE2_FIELDS,
    PHASE2_RETURN_FIELDS,
    assert_phase2_release_allowed,
    validate_packet_rows,
    validate_phase1_packet_rows,
    validate_phase2_packet_rows,
)


TASK_ID = "PILOT4-EXTERNAL-BLIND-REVIEW-PHASE-SEPARATION-01"
NAMESPACE = "paper1_pilot4_external_blind_phase_separation_20260902"
STATUS = (
    "PILOT4_EXTERNAL_BLIND_PHASE1_PACKET_READY / "
    "WAITING_FOR_EXTERNAL_PHASE1_REVIEW / PHASE2_WITHHELD / "
    "NO_HUMAN_DISTRIBUTION"
)
HISTORICAL_PACKET_COMMIT = "5d6b4b57abd432f08cc606b567bf0c949102663b"
HISTORICAL_NAMESPACE = "paper1_pilot4_external_blind_review_packet_20260902"

PHASE1_ENUMS = {
    "text_naturalness": "NATURAL / MINOR_ISSUE / UNNATURAL",
    "local_internal_conflict": "YES / NO / UNCERTAIN",
    "phase1_issue": "NONE / MISSING_CONTEXT / AMBIGUOUS_REFERENCE / OTHER",
    "phase1_reason": "free text / 简短具体理由",
}

PHASE2_ENUMS = {
    "overall_fact_status": (
        "CURRENTLY_CONSISTENT / LEGITIMATE_VERSION_OR_HISTORY / "
        "FACTUAL_CONFLICT / INSUFFICIENT_EVIDENCE"
    ),
    "version_claim_status": (
        "NOT_PRESENT / PRESENT_CORRECT / PRESENT_INCORRECT / "
        "PRESENT_EVIDENCE_INSUFFICIENT"
    ),
    "authority_claim_status": (
        "NOT_PRESENT / PRESENT_CORRECT / PRESENT_INCORRECT / "
        "PRESENT_EVIDENCE_INSUFFICIENT"
    ),
    "minimum_external_evidence_needed": (
        "ONE_OFFICIAL_EVIDENCE / MULTI_EVIDENCE_OR_VERSION_CHAIN / NOT_APPLICABLE"
    ),
    "evidence_selection": "NONE / E1 / E2 / E1+E2",
    "phase2_issue": (
        "NONE / SOURCE_UNREACHABLE / SOURCE_CONFLICT / EVIDENCE_MISSING / "
        "LATE_DISCOVERED_CANDIDATE_DEFECT / OTHER"
    ),
    "phase2_reason": "free text / 简短具体理由",
}


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
    records = [
        {
            "path": path.relative_to(root).as_posix(),
            "size": path.stat().st_size,
            "sha256": file_sha256(path),
        }
        for path in sorted(root.rglob("*"))
        if path.is_file()
    ]
    return {
        "root_name": root.name,
        "file_count": len(records),
        "records": records,
        "aggregate_sha256": sha256(
            json.dumps(records, ensure_ascii=False, separators=(",", ":")).encode()
        ).hexdigest(),
    }


def _phase1_rows(combined: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "blind_review_id": row["blind_review_id"],
            "candidate_text": row["candidate_text"],
            "source_title": row["source_title"],
            **{field: "" for field in PHASE1_FIELDS},
        }
        for row in combined
    ]


def _phase2_rows(combined: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "blind_review_id": row["blind_review_id"],
            "candidate_text": row["candidate_text"],
            "source_title": row["source_title"],
            "evidence_pool": row["evidence_pool"],
            **{field: "" for field in PHASE2_FIELDS},
        }
        for row in combined
    ]


def _phase1_packet_markdown(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# PILOT4 External Blind Phase1 Packet",
        "",
        "Status: `WAITING_FOR_EXTERNAL_PHASE1_REVIEW`",
        "",
        "NO WEB / NO FACT LOOKUP IN PHASE1.",
        "",
        "Do not use web search, external factual lookup, or any official source during Phase1. Only judge the text shown in the packet.",
        "",
        "（Phase1 禁止事实查证，只依据候选文本本身判断。）",
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
            ]
        )
        for field in PHASE1_FIELDS:
            lines.append(f"- `{field}` ({PHASE1_ENUMS[field]}): ")
        lines.extend(["", "---", ""])
    return "\n".join(lines).rstrip() + "\n"


def _phase2_packet_markdown(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# PILOT4 External Blind Phase2 Packet",
        "",
        "Status: `DO_NOT_RELEASE_BEFORE_PHASE1_LOCK`",
        "",
        "Phase2 starts only after Phase1 return is locked. Official Evidence Pool may now be used.",
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
        for field in PHASE2_FIELDS:
            lines.append(f"- `{field}` ({PHASE2_ENUMS[field]}): ")
        lines.extend(["", "---", ""])
    return "\n".join(lines).rstrip() + "\n"


def _phase1_guide() -> str:
    return """# PILOT4 External Blind Phase1 Guide

NO WEB / NO FACT LOOKUP IN PHASE1.

Do not use web search, external factual lookup, or any official source during Phase1. Only judge the text shown in the packet.

（Phase1 禁止事实查证，只依据候选文本本身判断。）

## Fields / 字段

| Field | Allowed values | Meaning |
| --- | --- | --- |
| `text_naturalness` | NATURAL / MINOR_ISSUE / UNNATURAL | Judge expression quality only. / 只判断表达是否自然。 |
| `local_internal_conflict` | YES / NO / UNCERTAIN | Judge whether the shown text contradicts itself. / 只判断文本自身是否矛盾。 |
| `phase1_issue` | NONE / MISSING_CONTEXT / AMBIGUOUS_REFERENCE / OTHER | Record a defect visible in the shown text. / 记录文本本身可见的缺陷。 |
| `phase1_reason` | free text | Give a concrete reason tied to the shown wording. / 写出对应具体措辞的简短理由。 |

## Independent examples / 独立示例

- `NATURAL`: 《某市公共数据管理办法》自公布之日起施行。表达完整自然。
- `UNNATURAL`: 办法施行进行部门发布以后规定。语序明显破坏。
- `local_internal_conflict=YES`: 同一文本同时给出两个互斥的唯一施行日。
- `local_internal_conflict=NO`: 《某市采购办法》自2024年1月1日起施行。文本自身没有矛盾。
- `MISSING_CONTEXT`: “条例规定申请人应提交材料。”未唯一识别制度主体。
- `AMBIGUOUS_REFERENCE`: “《甲办法》与《乙办法》均被修订，它取消了备案要求。”中的“它”指代不明。

If web search or factual lookup is used, report `PHASE1_BLINDNESS_VIOLATION`; the return is invalid. / 如进行了事实查证，必须报告该违规，本轮返回失效。
"""


def _phase2_guide(cases: Sequence[Mapping[str, str]]) -> str:
    selected = [row for row in cases if row["field"] in PHASE2_FIELDS]
    lines = [
        "# PILOT4 External Blind Phase2 Guide",
        "",
        "Status: `DO_NOT_RELEASE_BEFORE_PHASE1_LOCK`",
        "",
        "Phase2 starts only after Phase1 return is locked. Official Evidence Pool may now be used.",
        "",
        "## Fields / 字段",
        "",
        "| Field | Allowed values |",
        "| --- | --- |",
    ]
    for field in PHASE2_FIELDS:
        lines.append(f"| `{field}` | {PHASE2_ENUMS[field]} |")
    lines.extend(
        [
            "",
            "## Independent teaching cases / 独立教学案例",
            "",
            "| Field | Case type | Fixture | Decision | Why |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in selected:
        values = {
            key: str(value).replace("|", "\\|").replace("\n", " ")
            for key, value in row.items()
        }
        lines.append(
            f"| `{values['field']}` | {values['category']} | {values['fixture']} | "
            f"`{values['decision']}` | {values['explanation']} |"
        )
    return "\n".join(lines).rstrip() + "\n"


def _write_csv(path: Path, headers: Sequence[str], ids: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        for opaque_id in ids:
            writer.writerow({"blind_review_id": opaque_id})


def _copy_history_assets(prior: Path, output: Path) -> None:
    owner = output / "owner_only"
    owner.mkdir(parents=True, exist_ok=True)
    for name in (
        "blind_review_identity_mapping.json",
        "blind_review_identity_mapping.sha256",
    ):
        shutil.copyfile(prior / "owner_only" / name, owner / name)
    provenance = output / "title_provenance"
    provenance.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(
        prior / "title_provenance" / "evidence_display_title_records.json",
        provenance / "evidence_display_title_records.json",
    )


def _write_manifest(output: Path) -> dict[str, Any]:
    entries = []
    for path in sorted(output.rglob("*")):
        if not path.is_file() or path == output / "manifest" / "manifest.json":
            continue
        relative = path.relative_to(output).as_posix()
        if relative.startswith("owner_only/"):
            visibility = "OWNER_ONLY"
        elif relative.startswith("external_blind_review/withheld_phase2/"):
            visibility = "WITHHELD_PHASE2 / DO_NOT_RELEASE_BEFORE_PHASE1_LOCK"
        elif relative in {
            "external_blind_review/PILOT4_EXTERNAL_BLIND_PHASE1_PACKET.md",
            "external_blind_review/PILOT4_EXTERNAL_BLIND_PHASE1_GUIDE.md",
        }:
            visibility = "PHASE1_REVIEWER_DISTRIBUTABLE"
        else:
            visibility = "CONTROL_PLANE_ONLY"
        entries.append(
            {
                "path": relative,
                "visibility": visibility,
                "size": path.stat().st_size,
                "sha256": file_sha256(path),
            }
        )
    manifest = {
        "task_id": TASK_ID,
        "namespace": NAMESPACE,
        "status": STATUS,
        "historical_packet_commit": HISTORICAL_PACKET_COMMIT,
        "historical_namespace": HISTORICAL_NAMESPACE,
        "historical_combined_packet_classification": (
            "COMBINED_PACKET_ENGINEERING_ARTIFACT / "
            "NOT_APPROVED_FOR_BLIND_SEMANTIC_REVIEW / "
            "SUPERSEDED_FOR_REVIEW_BY_PHASE_SEPARATED_PROTOCOL"
        ),
        "phase2_release_status": "DO_NOT_RELEASE_BEFORE_PHASE1_LOCK",
        "file_count": len(entries),
        "files": entries,
    }
    write_json(output / "manifest" / "manifest.json", manifest)
    return manifest


def build(prior: Path, output: Path) -> dict[str, Any]:
    if output.exists():
        raise FileExistsError("ADDITIVE_NAMESPACE_ALREADY_EXISTS")
    historical_pre = tree_identity(prior)
    combined = load_jsonl(
        prior / "external_blind_review" / "PILOT4_EXTERNAL_BLIND_REVIEW_PACKET.jsonl"
    )
    validate_packet_rows(combined)
    cases = load_json(prior / "staging" / "field_guide_cases.json")
    phase1_rows = _phase1_rows(combined)
    phase2_rows = _phase2_rows(combined)
    phase1_qa = validate_phase1_packet_rows(phase1_rows)
    phase2_qa = validate_phase2_packet_rows(phase2_rows)
    phase1_ids = [str(row["blind_review_id"]) for row in phase1_rows]
    phase2_ids = [str(row["blind_review_id"]) for row in phase2_rows]
    if phase1_ids != phase2_ids:
        raise ValueError("CROSS_PHASE_ID_PARITY_BLOCKER")

    external = output / "external_blind_review"
    withheld = external / "withheld_phase2"
    external.mkdir(parents=True)
    withheld.mkdir()
    write_jsonl(external / "PILOT4_EXTERNAL_BLIND_PHASE1_PACKET.jsonl", phase1_rows)
    (external / "PILOT4_EXTERNAL_BLIND_PHASE1_PACKET.md").write_text(
        _phase1_packet_markdown(phase1_rows), encoding="utf-8"
    )
    _write_csv(
        external / "PILOT4_EXTERNAL_BLIND_PHASE1_TEMPLATE.csv",
        PHASE1_RETURN_FIELDS,
        phase1_ids,
    )
    (external / "PILOT4_EXTERNAL_BLIND_PHASE1_GUIDE.md").write_text(
        _phase1_guide(), encoding="utf-8"
    )
    write_jsonl(withheld / "PILOT4_EXTERNAL_BLIND_PHASE2_PACKET.jsonl", phase2_rows)
    (withheld / "PILOT4_EXTERNAL_BLIND_PHASE2_PACKET.md").write_text(
        _phase2_packet_markdown(phase2_rows), encoding="utf-8"
    )
    _write_csv(
        withheld / "PILOT4_EXTERNAL_BLIND_PHASE2_TEMPLATE.csv",
        PHASE2_RETURN_FIELDS,
        phase2_ids,
    )
    (withheld / "PILOT4_EXTERNAL_BLIND_PHASE2_GUIDE.md").write_text(
        _phase2_guide(cases), encoding="utf-8"
    )
    (withheld / "README.md").write_text(
        "# WITHHELD PHASE2\n\nStatus: `DO_NOT_RELEASE_BEFORE_PHASE1_LOCK`.\n",
        encoding="utf-8",
    )
    (external / "PILOT4_EXTERNAL_REVIEWER_INSTRUCTIONS.md").write_text(
        """# PILOT4 External Reviewer Instructions

Controller note: the Phase1 reviewer receives only the Phase1 packet Markdown and Phase1 guide Markdown. Do not send this controller file during Phase1.

## Phase1

Do not use web search, external factual lookup, or any official source during Phase1. Only judge the text shown in the packet.

（Phase1 禁止事实查证，只依据候选文本本身判断。）

Any lookup is `PHASE1_BLINDNESS_VIOLATION` and invalidates the return.

## Phase2

Phase2 starts only after Phase1 return is locked. Official Evidence Pool may now be used. The same isolated reviewer continues; locked Phase1 answers are read-only and cannot be revised.
""",
        encoding="utf-8",
    )
    _copy_history_assets(prior, output)
    historical_post = tree_identity(prior)
    if historical_pre != historical_post:
        raise ValueError("HISTORICAL_PACKET_MUTATION_BLOCKER")

    phase1_external_text = "\n".join(
        (external / name).read_text(
            encoding="utf-8-sig" if name.endswith(".csv") else "utf-8"
        )
        for name in (
            "PILOT4_EXTERNAL_BLIND_PHASE1_PACKET.md",
            "PILOT4_EXTERNAL_BLIND_PHASE1_PACKET.jsonl",
            "PILOT4_EXTERNAL_BLIND_PHASE1_TEMPLATE.csv",
            "PILOT4_EXTERNAL_BLIND_PHASE1_GUIDE.md",
        )
    )
    forbidden_phase1_tokens = tuple(PHASE2_FIELDS) + (
        "official_source_url",
        "official_page_title",
        "evidence_id",
        "Evidence Pool",
        "E1+E2",
        "S2",
        "S3",
        "sample_id",
        "expected_contract",
    )
    leaked_phase1 = [
        token
        for token in forbidden_phase1_tokens
        if token.casefold() in phase1_external_text.casefold()
    ]
    if leaked_phase1:
        raise ValueError(f"PHASE1_EXTERNAL_LEAKAGE_BLOCKER:{leaked_phase1}")

    title_records = load_json(
        output / "title_provenance" / "evidence_display_title_records.json"
    )
    if title_records.get("visible_slot_count") != 144:
        raise ValueError("PHASE2_TITLE_PROVENANCE_BLOCKER")
    visible_slots = {
        (str(row["blind_review_id"]), str(row["evidence_id"]))
        for row in title_records["records"]
    }
    packet_slots = {
        (str(row["blind_review_id"]), str(item["evidence_id"]))
        for row in phase2_rows
        for item in row["evidence_pool"]
    }
    if packet_slots != visible_slots:
        raise ValueError("PHASE2_TITLE_PROVENANCE_PARITY_BLOCKER")
    historical_order_qa = load_json(prior / "qa" / "blind_order_leakage_qa.json")
    if (
        historical_order_qa.get("status") != "PASS"
        or historical_order_qa.get("matched_triplet_adjacency_count") != 0
    ):
        raise ValueError("FROZEN_ORDER_LEAKAGE_BLOCKER")

    gate = {
        name: False
        for name in (
            "PHASE1_RETURN_RECEIVED",
            "PHASE1_RETURN_SCHEMA_VALID",
            "PHASE1_RETURN_72_72",
            "PHASE1_RETURN_HASH_LOCKED",
            "PHASE1_RETURN_IMMUTABLE",
        )
    }
    try:
        assert_phase2_release_allowed(gate)
    except ValueError as error:
        release_error = str(error)
    else:
        raise ValueError("PHASE2_RELEASE_FAIL_CLOSED_BLOCKER")

    write_json(output / "qa" / "phase1_external_blindness_gate.json", phase1_qa)
    write_json(
        output / "qa" / "phase2_withheld_qa.json",
        {
            **phase2_qa,
            "release_status": "DO_NOT_RELEASE_BEFORE_PHASE1_LOCK",
            "actual_title_provenance": "144/144",
            "source_type_visible": 0,
            "evidence_role_visible": 0,
            "design_label_visible": 0,
            "expected_label_visible": 0,
            "owner_metadata_visible": 0,
            "minimum_path_visible": 0,
        },
    )
    write_json(
        output / "qa" / "cross_phase_identity_qa.json",
        {
            "status": "PASS",
            "phase1_phase2_id_parity": "72/72",
            "same_order": True,
            "original_sample_id_visible": 0,
            "mapping_location": "owner_only / excluded from both review phases",
        },
    )
    write_json(
        output / "qa" / "frozen_order_and_pattern_qa.json",
        {
            "status": "PASS",
            "source_namespace": HISTORICAL_NAMESPACE,
            "same_frozen_order_reused": True,
            "matched_triplet_adjacency_count": 0,
            "class_periodicity": historical_order_qa["class_periodicity"],
            "hkp_periodicity": historical_order_qa["hkp_periodicity"],
            "stealth_periodicity": historical_order_qa["stealth_periodicity"],
            "domain_periodicity": historical_order_qa["domain_periodicity"],
            "opaque_id_pattern_recoverability": ("NOT_ESTABLISHED / MACHINE_GATE_PASS"),
        },
    )
    write_json(
        output / "qa" / "phase2_release_gate.json",
        {
            "status": "BLOCKED_AS_REQUIRED",
            "gate": gate,
            "release_function_result": release_error,
            "release_approved": False,
        },
    )
    write_json(
        output / "qa" / "historical_packet_immutability.json",
        {
            "status": "PASS",
            "historical_commit": HISTORICAL_PACKET_COMMIT,
            "historical_namespace": HISTORICAL_NAMESPACE,
            "pre": historical_pre,
            "post": historical_post,
            "tree_equal": True,
        },
    )
    write_json(
        output / "governance" / "combined_packet_supersession.json",
        {
            "status": "SUPERSEDED_FOR_REVIEW_BY_PHASE_SEPARATED_PROTOCOL",
            "historical_packet_classification": (
                "COMBINED_PACKET_ENGINEERING_ARTIFACT / "
                "NOT_APPROVED_FOR_BLIND_SEMANTIC_REVIEW"
            ),
            "historical_packet_commit": HISTORICAL_PACKET_COMMIT,
            "historical_namespace": HISTORICAL_NAMESPACE,
            "historical_evidence_deleted_or_overwritten": False,
            "external_review_started": False,
            "human_distribution": False,
        },
    )
    (output / "README.md").write_text(
        f"""# Pilot4 External Blind Phase Separation

Status: `{STATUS}`

The prior combined packet is retained unchanged as `COMBINED_PACKET_ENGINEERING_ARTIFACT / NOT_APPROVED_FOR_BLIND_SEMANTIC_REVIEW` and is `SUPERSEDED_FOR_REVIEW_BY_PHASE_SEPARATED_PROTOCOL`.

Flow: `PHASE1 -> RETURN -> HASH LOCK -> PHASE2 RELEASE`.

Only these two files may be distributed now:

- `external_blind_review/PILOT4_EXTERNAL_BLIND_PHASE1_PACKET.md`
- `external_blind_review/PILOT4_EXTERNAL_BLIND_PHASE1_GUIDE.md`

Everything under `withheld_phase2` is `DO_NOT_RELEASE_BEFORE_PHASE1_LOCK`.
""",
        encoding="utf-8",
    )
    manifest = _write_manifest(output)
    return {
        "status": STATUS,
        "phase1_rows": len(phase1_rows),
        "phase2_rows": len(phase2_rows),
        "id_parity": "72/72",
        "phase2_release_approved": False,
        "historical_tree_equal": True,
        "manifest_files": manifest["file_count"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prior", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.prior, args.output), ensure_ascii=False))


if __name__ == "__main__":
    main()
