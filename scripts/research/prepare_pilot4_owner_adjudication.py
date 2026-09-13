from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

from scripts.research.lock_pilot4_ab_phase2_returns import (
    PHASE1_FIELDS,
    PHASE2_CORE_FIELDS,
    exact_agreement,
    field_agreement,
    read_csv,
    read_mapping,
    rows_by_sample,
)


TASK_ID = "PILOT4-A-B-OWNER-DEFECT-TRIAGE-AND-BLIND-ADJUDICATION-PREP-01"
EXPECTED_HEAD = "346f2e24c7459fbd68694969a481729bbc88c271"
FLAG_IDS = (
    "P4Q-3bd40af7ed77",
    "P4Q-954090e9f676",
    "P4Q-89bb0f45e834",
    "P4Q-3ed81a10fec6",
    "P4Q-0444c548e139",
)
ENUMS = {
    "text_naturalness": ["NATURAL", "MINOR_ISSUE", "UNNATURAL"],
    "local_internal_conflict": ["YES", "NO", "UNCERTAIN"],
    "phase1_issue": ["NONE", "MISSING_CONTEXT", "AMBIGUOUS_REFERENCE", "OTHER"],
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
    "phase2_issue": [
        "NONE",
        "SOURCE_UNREACHABLE",
        "SOURCE_CONFLICT",
        "EVIDENCE_MISSING",
        "LATE_DISCOVERED_CANDIDATE_DEFECT",
        "OTHER",
    ],
}
GUIDE_RULES = {
    "text_naturalness": "仅判断中文表达是否自然，不判断现实事实真伪。",
    "local_internal_conflict": "仅判断候选文本内部、无需外查即可发现的自相矛盾；事实可疑不等于内部冲突。",
    "phase1_issue": "判断文本是否缺少必要上下文、存在指代歧义或其他影响核心理解的文本问题。",
    "overall_fact_status": "先判断证据是否充分，再判断事实冲突；合法历史/版本命题用当前时点替换测试区分。",
    "version_claim_status": "判断候选是否提出版本命题；存在时再判断证据支持、否定或不足。",
    "authority_claim_status": "判断候选是否提出制定、发布、修订或主管机关命题；存在时再判断证据。",
    "minimum_external_evidence_needed": "仅 FACTUAL_CONFLICT 时判断；任一单独官方证据充分则 ONE，只有联合才充分则 MULTI。",
    "phase2_issue": "记录证据传输、证据池或候选本身的问题；不要用它替代事实状态判断。",
}


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


def mapped_phase1(
    path: Path, mapping: Mapping[str, Mapping[str, Any]]
) -> dict[str, dict[str, str]]:
    rows = read_csv(path)
    if len(rows) != 72:
        raise ValueError(f"PHASE1_ROW_COUNT_BLOCKER:{path}")
    return rows_by_sample(rows, mapping)


def mapped_phase2(
    path: Path, mapping: Mapping[str, Mapping[str, Any]]
) -> dict[str, dict[str, str]]:
    rows = read_csv(path)
    if len(rows) != 72:
        raise ValueError(f"PHASE2_ROW_COUNT_BLOCKER:{path}")
    return rows_by_sample(rows, mapping)


def weighted_kappa(
    values_a: Sequence[str], values_b: Sequence[str], order: Sequence[str]
) -> float | None:
    if len(values_a) != len(values_b) or not values_a:
        raise ValueError("WEIGHTED_KAPPA_INPUT_BLOCKER")
    index = {label: position for position, label in enumerate(order)}
    if any(value not in index for value in (*values_a, *values_b)):
        raise ValueError("WEIGHTED_KAPPA_ENUM_BLOCKER")
    denominator = max(1, len(order) - 1)
    observed = sum(
        abs(index[a] - index[b]) / denominator
        for a, b in zip(values_a, values_b, strict=True)
    ) / len(values_a)
    a_counts = Counter(values_a)
    b_counts = Counter(values_b)
    expected = sum(
        (a_counts[a] / len(values_a))
        * (b_counts[b] / len(values_b))
        * abs(index[a] - index[b])
        / denominator
        for a in order
        for b in order
    )
    return None if expected == 0 else 1 - observed / expected


def recompute_stats(
    phase1_a: Mapping[str, Mapping[str, str]],
    phase1_b: Mapping[str, Mapping[str, str]],
    phase2_a: Mapping[str, Mapping[str, str]],
    phase2_b: Mapping[str, Mapping[str, str]],
) -> dict[str, Any]:
    p1_metrics = {
        field: field_agreement(phase1_a, phase1_b, field) for field in PHASE1_FIELDS
    }
    p2_metrics = {
        field: field_agreement(phase2_a, phase2_b, field)
        for field in (*PHASE2_CORE_FIELDS, "evidence_selection")
    }
    p1_exact, p1_samples = exact_agreement(phase1_a, phase1_b, PHASE1_FIELDS)
    p2_exact, p2_samples = exact_agreement(phase2_a, phase2_b, PHASE2_CORE_FIELDS)
    sample_ids = sorted(phase1_a)
    naturalness_a = [phase1_a[item]["text_naturalness"] for item in sample_ids]
    naturalness_b = [phase1_b[item]["text_naturalness"] for item in sample_ids]
    p1_metrics["text_naturalness"]["linear_weighted_kappa_supplementary"] = (
        weighted_kappa(naturalness_a, naturalness_b, ENUMS["text_naturalness"])
    )
    p1_metrics["text_naturalness"]["weighted_metric_status"] = (
        "SUPPLEMENTARY_ONLY_CANONICAL_PROTOCOL_DOES_NOT_DEFINE_WEIGHTING_SCHEME"
    )
    return {
        "task_id": TASK_ID,
        "classification": "PRE_ADJUDICATION_RAW_HUMAN_HUMAN_REPRODUCIBILITY_ONLY",
        "population": 72,
        "expected_v3_loaded": False,
        "thresholds_defined_post_hoc": False,
        "optional_gwet_ac1": "OPTIONAL_NOT_COMPUTED_NO_EXISTING_STABLE_PROJECT_IMPLEMENTATION",
        "phase1": {
            "field_metrics": p1_metrics,
            "exact_relevant_fields": f"{p1_exact}/72",
            "disagreement_sample_count": len(p1_samples),
            "interpretation": "QC_AND_CANDIDATE_QUALITY_REPRODUCIBILITY_NOT_BENCHMARK_LABEL_ACCURACY",
        },
        "phase2": {
            "field_metrics": p2_metrics,
            "exact_core_fields_excluding_evidence_selection": f"{p2_exact}/72",
            "disagreement_sample_count": len(p2_samples),
            "evidence_selection_interpretation": "DESCRIPTIVE_PROCESS_ONLY_NOT_GROUND_TRUTH",
        },
        "derived_stealth": "READ_ONLY_DETERMINISTIC_DERIVATION_NOT_DIRECTLY_ADJUDICATED",
    }


def verify_against_prior(stats: Mapping[str, Any], prior: Mapping[str, Any]) -> None:
    for phase in ("phase1", "phase2"):
        for field, metric in stats[phase]["field_metrics"].items():
            if field not in prior[phase]["field_metrics"]:
                continue
            old = prior[phase]["field_metrics"][field]
            for key in (
                "n",
                "matches",
                "disagreements",
                "raw_agreement",
                "cohen_kappa",
            ):
                if metric[key] != old[key]:
                    raise ValueError(
                        f"REPRODUCIBILITY_RECOMPUTE_MISMATCH:{phase}:{field}:{key}"
                    )


def evidence_by_sample(
    payload_path: Path, mapping: Mapping[str, Mapping[str, Any]]
) -> dict[str, dict[str, Any]]:
    payload = json.loads(payload_path.read_text(encoding="utf-8"))
    result: dict[str, dict[str, Any]] = {}
    for row in payload["rows"]:
        record = mapping[row["blind_review_id"]]
        sample_id = str(record["sample_id"])
        result[sample_id] = {
            "sample_id": sample_id,
            "triplet_id": str(record["triplet_id"]),
            "candidate_text": row["candidate_text"],
            "source_title": row["source_title"],
            "evidence_pool": row["evidence_pool"],
        }
    if len(result) != 72:
        raise ValueError("EVIDENCE_PAYLOAD_72_PARITY_BLOCKER")
    return result


def decision_status_formula_note() -> str:
    return (
        "缺陷决定为空 -> WAITING_FOR_DEFECT_TRIAGE；CONFIRMED_DEFECT -> QUARANTINED_NO_GT_ADJUDICATION；"
        "NEEDS_TARGETED_REREVIEW -> ON_HOLD_TARGETED_REREVIEW；ANNOTATOR_INTERPRETATION_VARIANCE -> READY_FOR_OWNER_ADJUDICATION。"
    )


def build_payload(
    packet: Sequence[Mapping[str, str]],
    flags: Sequence[Mapping[str, str]],
    evidence: Mapping[str, Mapping[str, Any]],
    p1_a: Mapping[str, Mapping[str, str]],
    p1_b: Mapping[str, Mapping[str, str]],
    p2_a: Mapping[str, Mapping[str, str]],
    p2_b: Mapping[str, Mapping[str, str]],
    stats: Mapping[str, Any],
) -> dict[str, Any]:
    if len(packet) != 78 or len(flags) != 5:
        raise ValueError("DISAGREEMENT_OR_FLAG_COUNT_BLOCKER")
    if any(
        row["field"] in {"evidence_selection", "derived_stealth_level"}
        for row in packet
    ):
        raise ValueError("NON_ADJUDICABLE_FIELD_LEAKAGE_BLOCKER")
    flag_set = {str(row["sample_id"]) for row in flags}
    if flag_set != set(FLAG_IDS):
        raise ValueError("FLAG_SAMPLE_SET_BLOCKER")
    defect_rows: list[dict[str, Any]] = []
    for sample_id in FLAG_IDS:
        item = evidence[sample_id]
        pool = {row["evidence_id"]: row for row in item["evidence_pool"]}
        defect_rows.append(
            {
                "sample_id": sample_id,
                "triplet_id": item["triplet_id"],
                "candidate_text": item["candidate_text"],
                "source_title": item["source_title"],
                "a_phase1_issue": p1_a[sample_id]["phase1_issue"],
                "a_phase1_reason": p1_a[sample_id]["phase1_reason"],
                "b_phase1_issue": p1_b[sample_id]["phase1_issue"],
                "b_phase1_reason": p1_b[sample_id]["phase1_reason"],
                "a_overall": p2_a[sample_id]["overall_fact_status"],
                "b_overall": p2_b[sample_id]["overall_fact_status"],
                "a_version": p2_a[sample_id]["version_claim_status"],
                "b_version": p2_b[sample_id]["version_claim_status"],
                "a_authority": p2_a[sample_id]["authority_claim_status"],
                "b_authority": p2_b[sample_id]["authority_claim_status"],
                "a_minimum": p2_a[sample_id]["minimum_external_evidence_needed"],
                "b_minimum": p2_b[sample_id]["minimum_external_evidence_needed"],
                "e1_title": pool["E1"]["official_page_title"],
                "e1_url": pool["E1"]["official_source_url"],
                "e2_title": pool["E2"]["official_page_title"],
                "e2_url": pool["E2"]["official_source_url"],
                "owner_defect_decision": "",
                "owner_defect_reason": "",
            }
        )
    ordinary: list[dict[str, Any]] = sorted(
        (dict(row) for row in packet),
        key=lambda row: (row["sample_id"], row["phase"], row["field"]),
    )
    for row in ordinary:
        row["guide_rule"] = GUIDE_RULES[row["field"]]
        row["allowed_values"] = ENUMS[row["field"]]
        row["owner_final_value"] = ""
        row["owner_decision_reason"] = ""
    relevant = sorted({row["sample_id"] for row in ordinary} | flag_set)
    evidence_rows: list[dict[str, str]] = []
    for sample_id in relevant:
        item = evidence[sample_id]
        for unit in item["evidence_pool"]:
            evidence_rows.append(
                {
                    "sample_id": sample_id,
                    "candidate_text": item["candidate_text"],
                    "evidence_id": unit["evidence_id"],
                    "title": unit["official_page_title"],
                    "url": unit["official_source_url"],
                    "snapshot_sha256": unit["snapshot_sha256"],
                    "snapshot_text": unit["snapshot_text"],
                }
            )
    return {
        "task_id": TASK_ID,
        "generated_at": now_utc(),
        "expected_v3_loaded": False,
        "owner_decisions_prefilled": 0,
        "defect_routing_rule": decision_status_formula_note(),
        "defect_rows": defect_rows,
        "ordinary_rows": ordinary,
        "evidence_rows": evidence_rows,
        "enums": ENUMS,
        "guide_rules": GUIDE_RULES,
        "stats": stats,
    }


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--prior-root", type=Path, required=True)
    parser.add_argument("--phase1-root", type=Path, required=True)
    parser.add_argument("--mapping-root", type=Path, required=True)
    parser.add_argument("--payload", type=Path, required=True)
    parser.add_argument("--git-head", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    require_new_output(args.output)
    if args.git_head != EXPECTED_HEAD:
        raise ValueError(f"UNEXPECTED_GIT_HEAD:{args.git_head}")
    p1a_path = (
        args.phase1_root / "raw_phase1/HUMAN-A01/PILOT4_AB_HUMAN_A01_PHASE1_RETURN.csv"
    )
    p1b_path = (
        args.phase1_root / "raw_phase1/HUMAN-B01/PILOT4_AB_HUMAN_B01_PHASE1_RETURN.csv"
    )
    p2a_raw_path = (
        args.prior_root
        / "raw_phase2/HUMAN-A01/PILOT4_AB_HUMAN_A01_PHASE2_ANNOTATION_WORKBOOK_V3_2.xlsx"
    )
    p2b_raw_path = (
        args.prior_root
        / "raw_phase2/HUMAN-B01/PILOT4_AB_HUMAN_B01_PHASE2_ANNOTATION_WORKBOOK_V3_2.xlsx"
    )
    p2a_path = (
        args.prior_root
        / "canonical_phase2_csv/HUMAN-A01/PILOT4_AB_HUMAN_A01_PHASE2_RETURN.csv"
    )
    p2b_path = (
        args.prior_root
        / "canonical_phase2_csv/HUMAN-B01/PILOT4_AB_HUMAN_B01_PHASE2_RETURN.csv"
    )
    map_a_path = args.mapping_root / "PILOT4_AB_A_IDENTITY_MAPPING.json"
    map_b_path = args.mapping_root / "PILOT4_AB_B_IDENTITY_MAPPING.json"
    raw_hashes = {
        p1a_path: (
            3313,
            "bb74908f7433bca1c834e8e7ea8e8721316edb1a503202805f90dd0e974d8bac",
        ),
        p1b_path: (
            3658,
            "b27d291dcf86088dccc9a7fc7e5dda1e5c1e7af54ac7db7c3bad5d78b215daf2",
        ),
        p2a_raw_path: (
            554781,
            "7fc043e294ad6455d9ff1bb87928e04bdfd5d1f0be0cc3ab76958abe0466a5b4",
        ),
        p2b_raw_path: (
            550353,
            "20cc4cca61f033ccd8e26ee8b9fcdb2fe29eeed4ea3e498931529ad24575347c",
        ),
    }
    canonical_hashes = {
        p2a_path: (
            14325,
            "622f62d5b15a96c229e0cf18ba7f314e156ba2effb5e6666c6602cb7e543b7ea",
        ),
        p2b_path: (
            16052,
            "5ba6fd2629062eebc0d0e1c5391a9dc888cdd101b32e7553b8aa287f5761f3e0",
        ),
    }
    integrity: list[dict[str, Any]] = []
    canonical_integrity: list[dict[str, Any]] = []
    for path, (size, digest) in raw_hashes.items():
        actual = {
            "path": str(path.resolve()),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        }
        actual["status"] = (
            "PASS" if actual["bytes"] == size and actual["sha256"] == digest else "FAIL"
        )
        integrity.append(actual)
        if actual["status"] != "PASS":
            raise ValueError(f"RAW_INTEGRITY_BLOCKER:{path}")
    for path, (size, digest) in canonical_hashes.items():
        actual = {
            "path": str(path.resolve()),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        }
        actual["status"] = (
            "PASS" if actual["bytes"] == size and actual["sha256"] == digest else "FAIL"
        )
        canonical_integrity.append(actual)
        if actual["status"] != "PASS":
            raise ValueError(f"CANONICAL_DERIVATIVE_INTEGRITY_BLOCKER:{path}")
    mapping_a, map_a_audit = read_mapping(map_a_path, "HUMAN-A01")
    mapping_b, map_b_audit = read_mapping(map_b_path, "HUMAN-B01")
    p1a, p1b = mapped_phase1(p1a_path, mapping_a), mapped_phase1(p1b_path, mapping_b)
    p2a, p2b = mapped_phase2(p2a_path, mapping_a), mapped_phase2(p2b_path, mapping_b)
    if set(p1a) != set(p1b) or set(p1a) != set(p2a) or set(p1a) != set(p2b):
        raise ValueError("FOUR_RAW_SAMPLE_PARITY_BLOCKER")
    stats = recompute_stats(p1a, p1b, p2a, p2b)
    prior_stats_path = args.prior_root / "comparison/pilot4_ab_agreement_preflight.json"
    verify_against_prior(
        stats, json.loads(prior_stats_path.read_text(encoding="utf-8"))
    )
    packet_path = args.prior_root / "mismatch/PILOT4_AB_OWNER_ADJUDICATION_PACKET.csv"
    flags_path = (
        args.prior_root / "mismatch/late_discovered_candidate_defect_flags.json"
    )
    packet = read_csv_dicts(packet_path)
    flags = json.loads(flags_path.read_text(encoding="utf-8"))
    evidence = evidence_by_sample(args.payload, mapping_a)
    payload = build_payload(packet, flags, evidence, p1a, p1b, p2a, p2b, stats)

    write_json(
        args.output / "qa/four_raw_integrity.json",
        {
            "status": "PASS",
            "raw_count": 4,
            "canonical_derivative_count": 2,
            "four_locked_human_raws": integrity,
            "canonical_phase2_derivatives": canonical_integrity,
        },
    )
    write_json(
        args.output / "qa/mapping_integrity.json",
        {"status": "PASS", "A": map_a_audit, "B": map_b_audit},
    )
    write_json(
        args.output / "qa/expected_blindness_audit.json",
        {
            "status": "PASS",
            "expected_v3_loaded": False,
            "expected_contract_path_opened": False,
            "expected_values_exposed_to_owner": 0,
            "researcher_answer_hints_exposed": 0,
            "note": "Expected V3 remained sealed; this task used only locked A/B returns, mappings, accepted guide rules, candidates and frozen evidence.",
        },
    )
    write_json(
        args.output / "reproducibility/pre_adjudication_reproducibility.json", stats
    )
    write_json(args.output / "control/workbook_payload.json", payload)
    decision_template = {
        "task_id": TASK_ID,
        "classification": "BLANK_OWNER_DECISION_TEMPLATE",
        "expected_v3_loaded": False,
        "candidate_defect_decisions": [
            {"sample_id": item, "owner_defect_decision": "", "owner_defect_reason": ""}
            for item in FLAG_IDS
        ],
        "field_adjudications": [
            {
                "sample_id": row["sample_id"],
                "phase": row["phase"],
                "field": row["field"],
                "owner_final_value": "",
                "owner_decision_reason": "",
            }
            for row in payload["ordinary_rows"]
        ],
    }
    write_json(
        args.output / "control/PILOT4_AB_OWNER_DECISION_TEMPLATE_V1.json",
        decision_template,
    )
    write_json(
        args.output / "control/future_owner_decision_import_contract.json",
        {
            "task_id": TASK_ID,
            "steps": [
                "LOCK_RETURNED_OWNER_WORKBOOK_RAW_BYTES_AND_SHA256",
                "VALIDATE_WORKBOOK_STRUCTURE_ENUMS_BLANK_REQUIREMENTS_AND_PROVENANCE",
                "EXTRACT_FIVE_DEFECT_DECISIONS",
                "ROUTE_CONFIRMED_DEFECT_TO_QUARANTINE_AND_TARGETED_REREVIEW_TO_HOLD",
                "EXTRACT_ONLY_ELIGIBLE_FIELD_ADJUDICATIONS",
                "CREATE_IMMUTABLE_OWNER_DECISION_RECORD",
                "ONLY_THEN_ALLOW_EXPECTED_V3_LOAD_FOR_RESEARCHER_QC",
                "IF_NO_BLOCKER_GENERATE_GROUND_TRUTH_CANDIDATE",
            ],
            "automatic_expected_wins": False,
            "ground_truth_generation_now": False,
        },
    )
    write_text(
        args.output / "README.md",
        f"""# Pilot4 Owner Expected-blind Adjudication Preparation\n\n"
        f"Task: `{TASK_ID}`\n\n"
        "This additive package freezes raw-only A/B reproducibility and prepares a blank, Chinese-friendly Owner workbook. "
        "Expected V3 was not loaded. No Owner decision, Ground Truth, Dataset freeze, Detector, Training, 5090, or formal experiment was executed.\n\n"
        "## Required order\n\n"
        "1. Complete the five Candidate-defect decisions first.\n"
        "2. Only rows routed as `READY_FOR_OWNER_ADJUDICATION` may receive field adjudication.\n"
        "3. Return the workbook unchanged except for yellow Owner input cells.\n"
        "4. A later separately authorized task must raw-lock and validate the returned workbook before any Expected V3 comparison.\n"
        """,
    )
    write_json(
        args.output / "manifest/pre_workbook_manifest.json",
        {
            "task_id": TASK_ID,
            "generated_at": now_utc(),
            "git_head": args.git_head,
            "status": "OWNER_EXPECTED_BLIND_ADJUDICATION_WORKBOOK_INPUT_READY",
            "counts": {
                "raws_verified": 4,
                "canonical_phase2_derivatives_verified": 2,
                "defect_rows": 5,
                "material_disagreements": 78,
                "evidence_samples": len(
                    {row["sample_id"] for row in payload["evidence_rows"]}
                ),
            },
            "expected_v3_loaded": False,
        },
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
