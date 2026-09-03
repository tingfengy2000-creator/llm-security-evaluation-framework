from __future__ import annotations

import argparse
import csv
import hashlib
import hmac
import json
import random
import re
import secrets
import shutil
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


TASK_ID = "PILOT4-A-B-EXECUTION-APPROVAL-AND-PHASE1-PACKET-GENERATION-01"
DATE_TOKEN = "20260903"
FINAL_STATUS = (
    "PILOT4_A_B_EXECUTION_APPROVED / HUMAN_A01_PHASE1_PACKET_READY / "
    "HUMAN_B01_PHASE1_PACKET_READY / WAITING_FOR_OWNER_PHASE1_DISTRIBUTION / "
    "PHASE2_WITHHELD / NO_GROUND_TRUTH_YET"
)

CANDIDATE_SHA = "f530471ecd6551300d68c8ddf104cadce2305d8ff91e64010be222820628252d"
GUIDE_V32_SHA = "83fced51ddb509f6ba39feabfc717b88f4003eacf662982551d73fccf476d561"
EXPECTED_V3_SHA = "dc549ff6adbacc6a87049c08c7db7e414b9d52dafc19c31f98b5c10490031433"
EVIDENCE_V2_SHA = "44b5c71b840d7018d428a058f51bc5e4c8ad1219b90faf74c0b7d61cd83a622e"

HANDOFF = Path(r"E:\LLMGuard-Handoff")
CANDIDATES = HANDOFF / (
    "paper1_pilot4_phase1_owner_defect_repair_20260902/candidate_repairs/"
    "PILOT4_CANDIDATE_CORPUS_POST_EXTERNAL_PHASE1_REPAIR_V1.jsonl"
)
ATTEMPT2_MAPPING = HANDOFF / (
    "paper1_pilot4_phase1_owner_defect_repair_20260902/controlled_mapping/"
    "attempt2_owner_only_mapping.json"
)
PHASE2_PACKET = HANDOFF / (
    "paper1_pilot4_external_blind_phase1_attempt2_return_20260902/release/"
    "PILOT4_EXTERNAL_BLIND_PHASE2_ATTEMPT2_PACKET.jsonl"
)
GUIDE_V32 = HANDOFF / (
    "paper1_pilot4_protocol_targeted_repair_r3_20260902/guide/"
    "ANNOTATION_GUIDE_V3_2_TARGETED_REPAIR.md"
)
EXPECTED_V3 = HANDOFF / (
    "paper1_pilot4_expected_v3_gate_recompute_20260903/expected/"
    "PILOT4_EXPECTED_CONTRACT_V3_TARGETED_CORRECTION.json"
)
EVIDENCE_V2 = HANDOFF / (
    "paper1_pilot4_protocol_targeted_repair_r3_20260902/evidence_pool/"
    "PILOT4_EVIDENCE_POOL_V2_TARGETED_REPAIR.json"
)
TITLE_RECORDS = HANDOFF / (
    "paper1_pilot4_external_blind_review_packet_20260902/title_provenance/"
    "url_title_records.json"
)
SOURCE_SNAPSHOTS = HANDOFF / (
    "paper1_pilot4_external_blind_review_packet_20260902/title_provenance/"
    "source_snapshots"
)
R3_SNAPSHOTS = HANDOFF / (
    "paper1_pilot4_protocol_targeted_repair_r3_20260902/r3/reviewer/evidence_snapshots"
)
R3_MAPPING = HANDOFF / (
    "paper1_pilot4_protocol_targeted_repair_r3_20260902/r3/control/"
    "r3_identity_mapping.json"
)
ATTEMPT1_RAW_ROOT = HANDOFF / "paper1_pilot4_external_blind_phase1_return_20260902"

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


def _now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON_OBJECT_REQUIRED:{path}")
    return value


def _jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8-sig") as handle:
        for line in handle:
            if line.strip():
                value = json.loads(line)
                if not isinstance(value, dict):
                    raise ValueError(f"JSONL_OBJECT_REQUIRED:{path}")
                rows.append(value)
    return rows


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )


def _write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def _assert_sha(path: Path, expected: str) -> dict[str, Any]:
    actual = _sha256(path)
    if actual != expected:
        raise ValueError(f"ACCEPTED_STACK_IDENTITY_BLOCKER:{path}:{actual}")
    return {
        "path": str(path.resolve()),
        "bytes": path.stat().st_size,
        "sha256": actual,
        "status": "PASS",
    }


def _source_identity() -> dict[str, Any]:
    return {
        "candidate_corpus": _assert_sha(CANDIDATES, CANDIDATE_SHA),
        "guide_v3_2": _assert_sha(GUIDE_V32, GUIDE_V32_SHA),
        "expected_v3_control_plane_only": _assert_sha(EXPECTED_V3, EXPECTED_V3_SHA),
        "evidence_pool_v2": _assert_sha(EVIDENCE_V2, EVIDENCE_V2_SHA),
        "attempt2_mapping": {
            "path": str(ATTEMPT2_MAPPING.resolve()),
            "bytes": ATTEMPT2_MAPPING.stat().st_size,
            "sha256": _sha256(ATTEMPT2_MAPPING),
        },
        "phase2_base_packet": {
            "path": str(PHASE2_PACKET.resolve()),
            "bytes": PHASE2_PACKET.stat().st_size,
            "sha256": _sha256(PHASE2_PACKET),
        },
        "title_records": {
            "path": str(TITLE_RECORDS.resolve()),
            "bytes": TITLE_RECORDS.stat().st_size,
            "sha256": _sha256(TITLE_RECORDS),
        },
    }


def _candidate_rows() -> list[dict[str, Any]]:
    rows = _jsonl(CANDIDATES)
    ids = [str(row.get("sample_id", "")) for row in rows]
    if len(rows) != 72 or len(set(ids)) != 72 or "" in ids:
        raise ValueError("FINAL72_CANDIDATE_PARITY_BLOCKER")
    return rows


def _attempt2_map() -> dict[str, str]:
    records = _json(ATTEMPT2_MAPPING).get("records", [])
    result = {str(row["blind_review_id"]): str(row["sample_id"]) for row in records}
    if len(result) != 72 or len(set(result.values())) != 72:
        raise ValueError("ATTEMPT2_MAPPING_PARITY_BLOCKER")
    return result


def _old_ids() -> set[str]:
    result = set(_attempt2_map())
    if R3_MAPPING.is_file():
        payload = _json(R3_MAPPING)
        for row in payload.get("records", payload.get("mapping", [])):
            if isinstance(row, dict):
                value = row.get("r3_blind_review_id", row.get("blind_review_id"))
                if value:
                    result.add(str(value))
    if ATTEMPT1_RAW_ROOT.is_dir():
        for path in ATTEMPT1_RAW_ROOT.rglob("*.csv"):
            with path.open("r", encoding="utf-8-sig", newline="") as handle:
                reader = csv.DictReader(handle)
                if "blind_review_id" in (reader.fieldnames or []):
                    result.update(str(row["blind_review_id"]) for row in reader)
    return result


def _metadata(
    row: dict[str, Any], by_triplet: dict[str, dict[str, str]]
) -> dict[str, str]:
    owner = row["owner_only"]
    triplet = str(row["triplet_id"])
    coverage = str(owner.get("coverage_cell") or "")
    if coverage:
        hkp, _, stealth = coverage.partition("|")
        by_triplet.setdefault(triplet, {"hkp": hkp, "stealth": stealth})
    inherited = by_triplet.get(triplet, {"hkp": "NA", "stealth": "NA"})
    return {
        "triplet": triplet,
        "kind": str(owner.get("candidate_kind") or "NA"),
        "domain": str(owner.get("domain") or "NA"),
        "hkp": inherited["hkp"],
        "stealth": inherited["stealth"],
    }


def _max_run(values: list[str]) -> int:
    maximum = 0
    current = 0
    previous: str | None = None
    for value in values:
        current = current + 1 if value == previous else 1
        maximum = max(maximum, current)
        previous = value
    return maximum


def _periods(values: list[str]) -> list[int]:
    return [
        period
        for period in range(1, min(12, len(values) // 2) + 1)
        if all(values[index] == values[index % period] for index in range(len(values)))
    ]


def _order_qa(order: list[dict[str, Any]]) -> dict[str, Any]:
    by_triplet: dict[str, dict[str, str]] = {}
    metadata = [_metadata(row, by_triplet) for row in order]
    # Recompute after every triplet's coverage cell has been encountered.
    metadata = [_metadata(row, by_triplet) for row in order]
    fields = ["kind", "domain", "hkp", "stealth"]
    adjacent = sum(
        metadata[index]["triplet"] == metadata[index - 1]["triplet"]
        for index in range(1, len(metadata))
    )
    report: dict[str, Any] = {
        "matched_triplet_adjacency_count": adjacent,
        "periodic_patterns": {
            field: _periods([item[field] for item in metadata]) for field in fields
        },
        "max_runs": {
            field: _max_run([item[field] for item in metadata]) for field in fields
        },
    }
    report["status"] = (
        "PASS"
        if adjacent == 0
        and all(not periods for periods in report["periodic_patterns"].values())
        and report["max_runs"]["kind"] <= 3
        and report["max_runs"]["domain"] <= 4
        else "FAIL"
    )
    return report


def _random_order(
    rows: list[dict[str, Any]], seed: bytes
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rng = random.Random(int.from_bytes(seed, "big"))
    for attempt in range(1, 100_001):
        ordered = list(rows)
        rng.shuffle(ordered)
        qa = _order_qa(ordered)
        if qa["status"] == "PASS":
            qa["accepted_shuffle_attempt"] = attempt
            return ordered, qa
    raise ValueError("INDEPENDENT_ORDER_LEAKAGE_QA_BLOCKER")


def _opaque_ids(rows: list[dict[str, Any]], seed: bytes, label: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for row in rows:
        sample_id = str(row["sample_id"])
        token = (
            hmac.new(seed, sample_id.encode("utf-8"), hashlib.sha256)
            .hexdigest()[:12]
            .upper()
        )
        result[sample_id] = f"AB-{label}-{token}"
    if len(result) != 72 or len(set(result.values())) != 72:
        raise ValueError(f"OPAQUE_ID_COLLISION_BLOCKER:{label}")
    return result


def _final_evidence() -> tuple[dict[str, list[dict[str, str]]], dict[str, Path]]:
    mapping = _attempt2_map()
    pools: dict[str, list[dict[str, str]]] = {}
    for row in _jsonl(PHASE2_PACKET):
        blind_id = str(row["blind_review_id"])
        pools[mapping[blind_id]] = [dict(item) for item in row["evidence_pool"]]
    repair = _json(EVIDENCE_V2)
    for change in repair.get("changes", []):
        pools[str(change["sample_id"])] = [dict(item) for item in change["new_E1_E2"]]

    title_rows = _json(TITLE_RECORDS).get("records", [])
    snapshot_hash_by_url = {
        str(row["source_url"]): str(row["source_snapshot_hash"]) for row in title_rows
    }
    for change in repair.get("changes", []):
        snapshot_hash_by_url[str(change["official_url"])] = str(
            change["snapshot_sha256"]
        )

    physical: dict[str, Path] = {}
    for root in (SOURCE_SNAPSHOTS, R3_SNAPSHOTS):
        for path in root.rglob("*"):
            if path.is_file():
                physical[_sha256(path)] = path
    snapshot_by_url: dict[str, Path] = {}
    for items in pools.values():
        if len(items) != 2:
            raise ValueError("EVIDENCE_PAIR_SIZE_BLOCKER")
        for item in items:
            url = str(item["official_source_url"])
            digest = snapshot_hash_by_url.get(url)
            if not digest or digest not in physical:
                raise ValueError(f"FROZEN_SNAPSHOT_MISSING:{url}")
            snapshot_by_url[url] = physical[digest]
    if len(pools) != 72:
        raise ValueError("EVIDENCE_POOL_72_BLOCKER")
    return pools, snapshot_by_url


def _phase1_guide(annotator: str, return_filename: str) -> str:
    return f"""# Pilot4 {annotator} Phase1 Guide

Status: `DISTRIBUTABLE_PHASE1`{'  '}
Annotator: `{annotator}`{'  '}
Expected return filename: `{return_filename}`

## Scope

Independently review all 72 candidate texts. Phase1 is limited to language naturalness, text-internal conflict, missing context, and ambiguous reference. Do not verify facts, browse the web, open official sources, or use any outside factual material.

During this human annotation, do not use ChatGPT, Claude, Gemini, Copilot, or any other LLM/AI assistant to judge labels, summarize candidates, explain material, or draft reasons.

## Canonical values

- `text_naturalness`: `NATURAL`, `MINOR_ISSUE`, `UNNATURAL`
- `local_internal_conflict`: `YES`, `NO`, `UNCERTAIN`
- `phase1_issue`: `NONE`, `MISSING_CONTEXT`, `AMBIGUOUS_REFERENCE`, `OTHER`
- `phase1_reason`: concise text required when any selected value records an issue, conflict, uncertainty, minor issue, or unnaturalness; otherwise it may be blank.

## Self-contained candidate rule

The factual subject of a law, policy, institution, or standard must be uniquely identifiable from the candidate text. A bare reference such as “the regulation”, “the revised text”, or “the 2017 version” that cannot be uniquely recovered is `MISSING_CONTEXT`. Do not rewrite the candidate.

## Return rules

Keep every opaque ID unchanged. Fill only the four answer columns in the supplied CSV. Do not add, remove, or rename columns or rows. Return only `{return_filename}` to the Owner. Do not discuss results with the other annotator and do not continue to the second phase until the Owner releases it simultaneously to both annotators.
"""


def _notice(annotator: str) -> str:
    return f"""# {annotator} Independence and Isolation Notice

The Project Owner attests that `{annotator}` is one of two different real human annotators and that the two annotators work independently without shared annotation context or access to each other's answers.

The annotator must preserve these conditions:

1. Work independently and do not exchange answers or candidate order.
2. Do not access hidden expected answers, identity mappings, canonical sample identifiers, candidate classes, design strata, prior reviewer answers, mismatch analyses, or repair history.
3. Do not use an LLM/AI assistant for any annotation judgment, summary, evidence interpretation, or reason drafting.
4. Return the completed CSV only to the Project Owner.
5. Do not begin the second phase until the Project Owner explicitly releases it after both first-phase raw returns have been validated and immutably locked.

Owner attestation source: `{TASK_ID}`.
"""


def _phase1_readme(annotator: str, return_filename: str) -> str:
    return f"""# README for {annotator}

1. Read `PILOT4_AB_{annotator.replace("-", "_")}_PHASE1_GUIDE.md` and the independence notice.
2. Review all 72 rows in the packet independently.
3. Do not discuss the work with the other annotator and do not use any AI assistant.
4. Do not look up facts or open outside sources in Phase1.
5. Do not edit candidate text or opaque IDs.
6. In the CSV template, fill only the four answer columns. Do not add columns or rows.
7. Save the completed file as `{return_filename}` and return only that CSV to the Owner.
8. Do not begin the second phase unless the Owner explicitly releases it.
"""


def _phase1_packet(
    annotator: str, ordered: list[dict[str, Any]], ids: dict[str, str]
) -> str:
    lines = [
        f"# Pilot4 {annotator} Phase1 Packet",
        "",
        "Fill answers in the separate CSV template. Candidate text and opaque IDs are immutable.",
        "",
        "| blind_review_id | candidate_text | source_title | text_naturalness | local_internal_conflict | phase1_issue | phase1_reason |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in ordered:
        view = row["phase1_view"]
        candidate = str(view["candidate_text"]).replace("|", "\\|").replace("\n", " ")
        title = str(view["source_title"]).replace("|", "\\|").replace("\n", " ")
        lines.append(
            f"| {ids[str(row['sample_id'])]} | {candidate} | {title} |  |  |  |  |"
        )
    return "\n".join(lines)


def _phase2_wrapper(annotator: str, return_filename: str) -> str:
    return f"""# Pilot4 {annotator} Phase2 Operational Guide

Status: `DO_NOT_DISTRIBUTE` until the dual-Phase1 release gate passes.{'  '}
Future return filename: `{return_filename}`

When formally released, read `ANNOTATION_GUIDE_V3_2_TARGETED_REPAIR.md` in this directory and use only the supplied frozen official snapshots and their official URL provenance. Unrelated external sources are outside the formal evidence environment.

Do not use ChatGPT, Claude, Gemini, Copilot, or any other LLM/AI assistant to judge labels, summarize candidates, interpret evidence, or draft reasons. Do not alter candidate text, opaque IDs, rows, or schema. Fill only the seven answer columns in the supplied CSV and return only the completed CSV to the Owner.
"""


def _owner_distribution_guide() -> str:
    return f"""# Pilot4 A/B 人工标注分发指南

当前只允许分发 Phase1。Phase2 已预构建，但状态为 `DO_NOT_DISTRIBUTE`。

## 给 HUMAN-A01

只发送 `HUMAN-A01/phase1/` 目录中的五个文件：packet、guide、return template、independence notice 和 README。不要发送 `mapping/`、`owner_control/`、`qa/`、`manifest/`、`register/` 或 `withheld_phase2/`。

## 给 HUMAN-B01

只发送 `HUMAN-B01/phase1/` 目录中的五个文件：packet、guide、return template、independence notice 和 README。不要发送 `mapping/`、`owner_control/`、`qa/`、`manifest/`、`register/` 或 `withheld_phase2/`。

## 回收

HUMAN-A01 必须只返回 `PILOT4_AB_HUMAN_A01_PHASE1_RETURN.csv`。{'  '}
HUMAN-B01 必须只返回 `PILOT4_AB_HUMAN_B01_PHASE1_RETURN.csv`。

收到后不要用 Excel 重新保存、规范化或改写 raw CSV；原字节直接交给下一条 Codex 锁定任务。只有两份 Phase1 return 都完成 schema/72-row/hash/immutable lock 后，才允许同时向两人释放各自的 Phase2。不得先向任何一人单独释放。
"""


def _future_lock_contract() -> dict[str, Any]:
    required = [
        "RECEIVED",
        "SCHEMA_VALID",
        "ROW_PARITY_72_72",
        "HASH_LOCKED",
        "IMMUTABLE",
    ]
    return {
        "contract_id": "PILOT4_A_B_FOUR_RAW_LOCK_BEFORE_COMPARISON_V1",
        "raw_returns": {
            "HUMAN-A01_PHASE1": "PILOT4_AB_HUMAN_A01_PHASE1_RETURN.csv",
            "HUMAN-B01_PHASE1": "PILOT4_AB_HUMAN_B01_PHASE1_RETURN.csv",
            "HUMAN-A01_PHASE2": "PILOT4_AB_HUMAN_A01_PHASE2_RETURN.csv",
            "HUMAN-B01_PHASE2": "PILOT4_AB_HUMAN_B01_PHASE2_RETURN.csv",
        },
        "required_state_per_raw": required,
        "phase2_release_rule": "BOTH_PHASE1_RAWS_MUST_SATISFY_ALL_REQUIRED_STATES_THEN_SIMULTANEOUS_RELEASE",
        "comparison_rule": "ALL_FOUR_RAWS_MUST_SATISFY_ALL_REQUIRED_STATES",
        "mapping_unlock_before_four_locks": False,
        "expected_v3_load_before_four_locks": False,
        "agreement_computed": False,
        "ground_truth_created": False,
    }


def _build_phase2(
    output: Path,
    annotator: str,
    ordered: list[dict[str, Any]],
    ids: dict[str, str],
    pools: dict[str, list[dict[str, str]]],
    snapshots: dict[str, Path],
) -> tuple[int, list[dict[str, Any]]]:
    base = output / "withheld_phase2" / annotator
    snapshot_dir = base / "evidence_snapshots"
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    packet_rows: list[dict[str, Any]] = []
    lines = [
        f"# Pilot4 {annotator} Phase2 Packet",
        "",
        "Status: `DO_NOT_DISTRIBUTE`.",
        "",
    ]
    slot_count = 0
    for position, row in enumerate(ordered, start=1):
        sample_id = str(row["sample_id"])
        blind_id = ids[sample_id]
        evidence_rows: list[dict[str, str]] = []
        lines.extend(
            [
                f"## {position}. {blind_id}",
                "",
                f"- Candidate text: {row['phase2_view']['candidate_text']}",
                f"- Source title: {row['phase2_view']['source_title']}",
            ]
        )
        for evidence in pools[sample_id]:
            evidence_id = str(evidence["evidence_id"])
            url = str(evidence["official_source_url"])
            source = snapshots[url]
            destination_name = f"{blind_id}_{evidence_id}{source.suffix.lower()}"
            destination = snapshot_dir / destination_name
            shutil.copyfile(source, destination)
            if _sha256(destination) != _sha256(source):
                raise ValueError("SNAPSHOT_COPY_INTEGRITY_BLOCKER")
            relative = f"evidence_snapshots/{destination_name}"
            evidence_rows.append(
                {
                    "evidence_id": evidence_id,
                    "official_page_title": str(evidence["official_page_title"]),
                    "official_source_url": url,
                    "frozen_snapshot": relative,
                    "snapshot_sha256": _sha256(destination),
                }
            )
            lines.extend(
                [
                    f"- {evidence_id} title: {evidence['official_page_title']}",
                    f"- {evidence_id} official URL: {url}",
                    f"- {evidence_id} frozen snapshot: `{relative}`",
                ]
            )
            slot_count += 1
        lines.extend(["", "Fill the seven answer fields in the return CSV.", ""])
        packet_rows.append(
            {
                "blind_review_id": blind_id,
                "candidate_text": row["phase2_view"]["candidate_text"],
                "source_title": row["phase2_view"]["source_title"],
                "evidence_pool": evidence_rows,
                **{header: "" for header in PHASE2_HEADERS[1:]},
            }
        )
    tag = annotator.replace("-", "_")
    _write_jsonl(base / f"PILOT4_AB_{tag}_PHASE2_PACKET.jsonl", packet_rows)
    _write_text(base / f"PILOT4_AB_{tag}_PHASE2_PACKET.md", "\n".join(lines))
    _write_text(
        base / f"PILOT4_AB_{tag}_PHASE2_GUIDE.md",
        _phase2_wrapper(annotator, f"PILOT4_AB_{tag}_PHASE2_RETURN.csv"),
    )
    shutil.copyfile(GUIDE_V32, base / GUIDE_V32.name)
    _write_text(
        base / "DO_NOT_DISTRIBUTE.md",
        "# DO NOT DISTRIBUTE\n\nPHASE2_RELEASE_ALLOWED = FALSE. Both Phase1 raw returns must be received, schema-valid, 72/72, hash-locked, and immutable before simultaneous release.",
    )
    return slot_count, packet_rows


def prepare(output: Path) -> None:
    if output.exists() and any(output.iterdir()):
        raise ValueError(f"OUTPUT_MUST_BE_NEW_OR_EMPTY:{output}")
    output.mkdir(parents=True, exist_ok=True)
    timestamp = _now()
    identities = _source_identity()
    rows = _candidate_rows()
    canonical_ids = {str(row["sample_id"]) for row in rows}
    old_ids = _old_ids()
    pools, snapshots = _final_evidence()
    if set(pools) != canonical_ids:
        raise ValueError("EVIDENCE_CANDIDATE_PARITY_BLOCKER")

    seed_a = secrets.token_bytes(32)
    seed_b = secrets.token_bytes(32)
    order_a, order_qa_a = _random_order(rows, seed_a)
    order_b, order_qa_b = _random_order(rows, seed_b)
    if [row["sample_id"] for row in order_a] == [row["sample_id"] for row in order_b]:
        raise ValueError("A_B_ORDER_IDENTITY_BLOCKER")
    ids_a = _opaque_ids(rows, seed_a, "A")
    ids_b = _opaque_ids(rows, seed_b, "B")
    set_a, set_b = set(ids_a.values()), set(ids_b.values())
    if set_a & set_b or (set_a | set_b) & old_ids:
        raise ValueError("OPAQUE_ID_NAMESPACE_REUSE_BLOCKER")

    roster = {
        "task_id": TASK_ID,
        "created_at": timestamp,
        "annotators": [
            {"annotator_id": "HUMAN-A01", "role": "INDEPENDENT_HUMAN_ANNOTATOR"},
            {"annotator_id": "HUMAN-B01", "role": "INDEPENDENT_HUMAN_ANNOTATOR"},
        ],
        "personal_identifiers_recorded": False,
        "owner_attestation": {
            "DIFFERENT_PERSONS": True,
            "INDEPENDENT": True,
            "NO_RESULT_SHARING": True,
            "NO_EXPECTED_ACCESS": True,
            "NO_MAPPING_ACCESS": True,
            "NO_PRIOR_REVIEW_ACCESS": True,
            "NO_LLM_ASSISTANCE": True,
            "source": "OWNER_EXPLICIT_TASK_INSTRUCTION",
        },
    }
    approval = {
        "task_id": TASK_ID,
        "recorded_at": timestamp,
        "PILOT4_ANNOTATION_PROTOCOL_ACCEPTED": True,
        "ACCEPTANCE_MODE": "ACCEPTED_WITH_NONBLOCKING_NOTES",
        "PILOT4_CALIBRATION_CLOSED": True,
        "PILOT4_A_B_EXECUTION_APPROVED": True,
        "ANNOTATOR_A": "HUMAN-A01",
        "ANNOTATOR_B": "HUMAN-B01",
        "OWNER_INDEPENDENCE_ATTESTATION": True,
        "PILOT4_A_B_PHASE1_PACKET_GENERATION_APPROVED": True,
        "PILOT4_A_B_PHASE1_DISTRIBUTION_APPROVED": True,
        "A_B_DISTRIBUTION_STARTED": False,
        "PILOT4_A_B_PHASE2_RELEASE_APPROVED": False,
        "GROUND_TRUTH_CREATED": False,
        "DATASET_FROZEN": False,
        "FORMAL_EXPERIMENT_APPROVED": False,
        "owner_role": "FINAL_DISAGREEMENT_ADJUDICATION_ONLY",
        "owner_participates_in_independent_first_round_annotation": False,
    }
    _write_json(output / "owner_control" / "PILOT4_A_B_ANNOTATOR_ROSTER.json", roster)
    _write_json(
        output / "owner_control" / "PILOT4_A_B_EXECUTION_APPROVAL_RECORD.json", approval
    )
    _write_json(
        output / "owner_control" / "PILOT4_ACCEPTED_STACK_REVALIDATION.json", identities
    )
    _write_json(
        output / "owner_control" / "PILOT4_A_B_FUTURE_RAW_RETURN_LOCK_CONTRACT.json",
        _future_lock_contract(),
    )
    _write_text(
        output / "PILOT4_A_B_OWNER_DISTRIBUTION_GUIDE.md", _owner_distribution_guide()
    )

    specs: list[dict[str, Any]] = []
    mapping_payloads: dict[str, dict[str, Any]] = {}
    phase2_rows: dict[str, list[dict[str, Any]]] = {}
    for annotator, ordered, ids, seed, order_qa in (
        ("HUMAN-A01", order_a, ids_a, seed_a, order_qa_a),
        ("HUMAN-B01", order_b, ids_b, seed_b, order_qa_b),
    ):
        tag = annotator.replace("-", "_")
        phase1_dir = output / annotator / "phase1"
        return_name = f"PILOT4_AB_{tag}_PHASE1_RETURN.csv"
        _write_text(
            phase1_dir / f"PILOT4_AB_{tag}_PHASE1_PACKET.md",
            _phase1_packet(annotator, ordered, ids),
        )
        _write_text(
            phase1_dir / f"PILOT4_AB_{tag}_PHASE1_GUIDE.md",
            _phase1_guide(annotator, return_name),
        )
        _write_text(
            phase1_dir / f"PILOT4_AB_{tag}_PHASE1_INDEPENDENCE_NOTICE.md",
            _notice(annotator),
        )
        _write_text(
            phase1_dir / f"README_FOR_{tag}.md",
            _phase1_readme(annotator, return_name),
        )
        mapping_records = [
            {
                "position": position,
                "blind_review_id": ids[str(row["sample_id"])],
                "sample_id": str(row["sample_id"]),
                "triplet_id": str(row["triplet_id"]),
            }
            for position, row in enumerate(ordered, start=1)
        ]
        mapping_payloads[annotator] = {
            "classification": "CONTROL_PLANE_ONLY",
            "annotator_id": annotator,
            "seed_hex": seed.hex(),
            "seed_sha256": hashlib.sha256(seed).hexdigest(),
            "order_policy": "INDEPENDENT_DETERMINISTIC_RANDOMIZED_ORDER",
            "records": mapping_records,
        }
        _write_json(
            output / "mapping" / f"PILOT4_AB_{annotator[-3]}_IDENTITY_MAPPING.json",
            mapping_payloads[annotator],
        )
        _write_json(output / "qa" / f"{tag}_order_leakage_qa.json", order_qa)
        slots, built_phase2_rows = _build_phase2(
            output, annotator, ordered, ids, pools, snapshots
        )
        if slots != 144:
            raise ValueError(f"PHASE2_SNAPSHOT_SLOT_BLOCKER:{annotator}")
        phase2_rows[annotator] = built_phase2_rows
        specs.extend(
            [
                {
                    "path": str(
                        phase1_dir / f"PILOT4_AB_{tag}_PHASE1_RETURN_TEMPLATE.csv"
                    ),
                    "sheet_name": f"{tag}_Phase1",
                    "headers": PHASE1_HEADERS,
                    "rows": [
                        [ids[str(row["sample_id"])], "", "", "", ""] for row in ordered
                    ],
                },
                {
                    "path": str(
                        output
                        / "withheld_phase2"
                        / annotator
                        / f"PILOT4_AB_{tag}_PHASE2_RETURN_TEMPLATE.csv"
                    ),
                    "sheet_name": f"{tag}_Phase2",
                    "headers": PHASE2_HEADERS,
                    "rows": [
                        [ids[str(row["sample_id"])], *([""] * 7)] for row in ordered
                    ],
                },
            ]
        )

    _write_json(
        output / "mapping" / "PILOT4_AB_ORDER_CONTROL.json",
        {
            "classification": "CONTROL_PLANE_ONLY",
            "A_seed_sha256": mapping_payloads["HUMAN-A01"]["seed_sha256"],
            "B_seed_sha256": mapping_payloads["HUMAN-B01"]["seed_sha256"],
            "orders_equal": False,
            "seeds_equal": False,
        },
    )
    register = {
        "task_id": TASK_ID,
        "updated_at": timestamp,
        "A_PHASE1_PACKET_READY": True,
        "B_PHASE1_PACKET_READY": True,
        "A_PHASE1_DISTRIBUTED": False,
        "B_PHASE1_DISTRIBUTED": False,
        "A_PHASE1_RETURN_RECEIVED": False,
        "B_PHASE1_RETURN_RECEIVED": False,
        "A_PHASE1_RETURN_SCHEMA_VALID": False,
        "B_PHASE1_RETURN_SCHEMA_VALID": False,
        "A_PHASE1_RETURN_72_72": False,
        "B_PHASE1_RETURN_72_72": False,
        "A_PHASE1_RETURN_HASH_LOCKED": False,
        "B_PHASE1_RETURN_HASH_LOCKED": False,
        "A_PHASE1_RETURN_IMMUTABLE": False,
        "B_PHASE1_RETURN_IMMUTABLE": False,
        "PHASE2_RELEASE_ALLOWED": False,
        "A_B_DISTRIBUTION_STARTED": False,
        "GROUND_TRUTH_CREATED": False,
    }
    _write_json(output / "register" / "PILOT4_A_B_DISTRIBUTION_REGISTER.json", register)
    _write_json(
        output / "qa" / "opaque_identity_qa.json",
        {
            "status": "PASS",
            "A_unique": len(set_a),
            "B_unique": len(set_b),
            "A_B_overlap": len(set_a & set_b),
            "old_id_reuse": len((set_a | set_b) & old_ids),
            "attempt1_attempt2_r3_known_id_count": len(old_ids),
            "A_B_same_canonical_candidate_set": (
                {row["sample_id"] for row in order_a}
                == {row["sample_id"] for row in order_b}
                == canonical_ids
            ),
        },
    )
    _write_json(
        output / "qa" / "phase2_prebuild_qa.json",
        {
            "status": "PASS",
            "A_rows": len(phase2_rows["HUMAN-A01"]),
            "B_rows": len(phase2_rows["HUMAN-B01"]),
            "A_evidence_slots": sum(
                len(row["evidence_pool"]) for row in phase2_rows["HUMAN-A01"]
            ),
            "B_evidence_slots": sum(
                len(row["evidence_pool"]) for row in phase2_rows["HUMAN-B01"]
            ),
            "fact_equivalent_by_sample": True,
            "delivery_policy": "FROZEN_OFFICIAL_SNAPSHOT_PLUS_URL_PROVENANCE",
            "phase2_release_allowed": False,
        },
    )
    _write_json(
        output / "qa" / "csv_authoring_spec.json",
        {"task_id": TASK_ID, "outputs": specs},
    )
    _write_json(
        output / "qa" / "prepare_complete.json",
        {"status": "PASS", "prepared_at": timestamp, "csv_output_count": len(specs)},
    )


def _validate_template(path: Path, headers: list[str]) -> dict[str, Any]:
    raw = path.read_bytes()
    if not raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError(f"CSV_UTF8_BOM_REQUIRED:{path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    if reader.fieldnames != headers or len(rows) != 72:
        raise ValueError(f"CSV_TEMPLATE_SCHEMA_BLOCKER:{path}")
    ids = [row["blind_review_id"] for row in rows]
    if len(set(ids)) != 72 or any(not value for value in ids):
        raise ValueError(f"CSV_TEMPLATE_ID_BLOCKER:{path}")
    if any(row[field] != "" for row in rows for field in headers[1:]):
        raise ValueError(f"CSV_TEMPLATE_LABEL_PREFILL_BLOCKER:{path}")
    return {
        "path": str(path),
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "rows": len(rows),
        "columns": reader.fieldnames,
        "annotation_prefill_count": 0,
    }


def _reviewer_visible_files(output: Path, annotator: str) -> list[Path]:
    return sorted(
        path for path in (output / annotator / "phase1").rglob("*") if path.is_file()
    )


def _leakage_qa(output: Path, annotator: str, other: str) -> dict[str, Any]:
    files = _reviewer_visible_files(output, annotator)
    text = "\n".join(path.read_text(encoding="utf-8-sig") for path in files)
    forbidden_patterns = {
        "sample_id": r"\bsample_id\b|P4Q-[0-9a-f]+",
        "expected": r"EXPECTED_V3|EXPECTED_CONTRACT",
        "mapping": r"IDENTITY_MAPPING|canonical candidate identity",
        "candidate_class": r"CLEAN_CURRENT|POISON_FACT|HARD_NEGATIVE",
        "hkp": r"\bHKP[_-]",
        "stealth": r"\bS[123]\b|intended_stealth",
        "hn_subtype": r"hard_negative_type|HN_SUBTYPE",
        "evidence_content": r"official_source_url|frozen_snapshot|evidence_pool|\bE[12] title\b",
        "phase2_fields": r"overall_fact_status|version_claim_status|authority_claim_status|minimum_external_evidence_needed|evidence_selection|phase2_issue|phase2_reason",
        "old_reviewer_id": r"\bBR-[A-F0-9]{10}\b|\bR3-[A-F0-9]{12}\b",
        "prior_result": r"R1_RETURN|R2_RETURN|R3_RETURN|prior mismatch",
        "repair_marker": r"REPAIR_HISTORY|TARGETED_REPAIR|mismatch_taxonomy",
        "other_annotator": re.escape(other),
    }
    counts = {
        key: len(re.findall(pattern, text, flags=re.IGNORECASE))
        for key, pattern in forbidden_patterns.items()
    }
    url_count = len(re.findall(r"https?://", text, flags=re.IGNORECASE))
    result = {
        "annotator": annotator,
        "reviewer_visible_file_count": len(files),
        "forbidden_pattern_counts": counts,
        "url_count": url_count,
        "status": "PASS" if not any(counts.values()) and url_count == 0 else "FAIL",
    }
    if result["status"] != "PASS":
        raise ValueError(
            f"PHASE1_REVIEWER_VISIBLE_LEAKAGE_BLOCKER:{annotator}:{result}"
        )
    return result


def _role(relative: str) -> str:
    normalized = relative.replace("\\", "/")
    if normalized.startswith("HUMAN-A01/phase1/") or normalized.startswith(
        "HUMAN-B01/phase1/"
    ):
        return "DISTRIBUTABLE_PHASE1"
    if normalized.startswith("withheld_phase2/"):
        return "WITHHELD_PHASE2"
    return "CONTROL_PLANE_ONLY"


def finalize(output: Path) -> None:
    timestamp = _now()
    validations: list[dict[str, Any]] = []
    for annotator in ("HUMAN-A01", "HUMAN-B01"):
        tag = annotator.replace("-", "_")
        validations.append(
            _validate_template(
                output
                / annotator
                / "phase1"
                / f"PILOT4_AB_{tag}_PHASE1_RETURN_TEMPLATE.csv",
                PHASE1_HEADERS,
            )
        )
        validations.append(
            _validate_template(
                output
                / "withheld_phase2"
                / annotator
                / f"PILOT4_AB_{tag}_PHASE2_RETURN_TEMPLATE.csv",
                PHASE2_HEADERS,
            )
        )
    leakage = [
        _leakage_qa(output, "HUMAN-A01", "HUMAN-B01"),
        _leakage_qa(output, "HUMAN-B01", "HUMAN-A01"),
    ]
    _write_json(
        output / "qa" / "csv_template_validation.json",
        {"status": "PASS", "templates": validations},
    )
    _write_json(
        output / "qa" / "reviewer_visible_leakage_qa.json",
        {"status": "PASS", "results": leakage},
    )

    identities = _json(
        output / "owner_control" / "PILOT4_ACCEPTED_STACK_REVALIDATION.json"
    )
    current = _source_identity()
    if identities != current:
        raise ValueError("ACCEPTED_SOURCE_IMMUTABILITY_BLOCKER")
    phase2_qa = _json(output / "qa" / "phase2_prebuild_qa.json")
    if (
        phase2_qa.get("A_evidence_slots") != 144
        or phase2_qa.get("B_evidence_slots") != 144
    ):
        raise ValueError("PHASE2_SLOT_FINALIZATION_BLOCKER")
    register = _json(output / "register" / "PILOT4_A_B_DISTRIBUTION_REGISTER.json")
    if register.get("PHASE2_RELEASE_ALLOWED") or register.get(
        "A_B_DISTRIBUTION_STARTED"
    ):
        raise ValueError("DISTRIBUTION_BOUNDARY_BLOCKER")

    manifest_path = output / "manifest" / "final_manifest.json"
    files = []
    for path in sorted(
        item for item in output.rglob("*") if item.is_file() and item != manifest_path
    ):
        relative = path.relative_to(output).as_posix()
        files.append(
            {
                "path": relative,
                "bytes": path.stat().st_size,
                "sha256": _sha256(path),
                "role": _role(relative),
                "distribution_eligibility": _role(relative),
            }
        )
    manifest = {
        "task_id": TASK_ID,
        "created_at": timestamp,
        "root": str(output.resolve()),
        "status": FINAL_STATUS,
        "file_count_excluding_manifest": len(files),
        "files": files,
        "manifest_self_hash": "EXCLUDED_TO_AVOID_RECURSION",
    }
    _write_json(manifest_path, manifest)
    _write_json(
        output / "qa" / "final_package_qa.json",
        {
            "status": "PASS",
            "finalized_at": timestamp,
            "phase1_templates": 2,
            "phase2_templates": 2,
            "reviewer_visible_leakage": "PASS",
            "phase2_withheld": True,
            "ground_truth_created": False,
            "manifest_pre_final_qa_sha256": _sha256(manifest_path),
            "final_manifest_self_hash_policy": "EXTERNAL_SHA256_ONLY_TO_AVOID_RECURSION",
        },
    )
    # Rebuild once so final_package_qa is included.
    files = []
    for path in sorted(
        item for item in output.rglob("*") if item.is_file() and item != manifest_path
    ):
        relative = path.relative_to(output).as_posix()
        files.append(
            {
                "path": relative,
                "bytes": path.stat().st_size,
                "sha256": _sha256(path),
                "role": _role(relative),
                "distribution_eligibility": _role(relative),
            }
        )
    manifest["file_count_excluding_manifest"] = len(files)
    manifest["files"] = files
    _write_json(manifest_path, manifest)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["prepare", "finalize"])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.mode == "prepare":
        prepare(args.output.resolve())
    else:
        finalize(args.output.resolve())
    print(
        json.dumps(
            {"status": "PASS", "mode": args.mode, "output": str(args.output.resolve())}
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
