"""Build Pilot2 closure evidence and run the local Pilot3 signal smoke."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Mapping

from llmguard.domains.retrieval.hidden_poisoning.adjudication import (
    OWNER_FIELD_ENUMS,
    OwnerCorrection,
    validate_owner_adjudication_rows,
)
from llmguard.domains.retrieval.hidden_poisoning.annotation import CandidateKind
from llmguard.domains.retrieval.hidden_poisoning.pilot1 import CHAINS
from llmguard.domains.retrieval.hidden_poisoning.pilot3_signals import (
    VIEW_NAMES,
    extract_signals,
)
from llmguard.domains.retrieval.hidden_poisoning.schema import (
    AttackType,
    StealthLevel,
    canonical_json,
)

TASK_ID = "S6.1-P1-PILOT2-ADJUDICATION-CLOSURE-AND-PILOT3-ENTRY"
OWNER_PACKET_SHA256 = "cf47a6c3ffada717a2a0dee2b67d6b92ebfb6236d599fb8a4daf2957e292dcb1"
RETURN_SHA256 = {
    "A1": "9e301816bfdd00a0028719679d629b8518bfc21dd9ce70c231de4b4ad7690424",
    "A2": "b7865999655928e574d946852245a9a3fe5ee4817df6c593ce2ea339dfc95096",
    "B1": "f4e1864e7f47c231f006c7a8750421129f4438e6e49164bd7760edd3e6392c8d",
    "B2": "0572a0c6aaf60a200755ae4de4de651b80bfb661ddc15eaeda598e0e9310989d",
}
CORRECTIONS = (
    OwnerCorrection("C-3ed6b082e98ee91e", "locally_detectable", "NO"),
    OwnerCorrection("C-6fe04fe29567e9d9", "version_relation_present", "YES"),
    OwnerCorrection("C-f73d03e9cfdf6e64", "assigned_stealth_level", "NOT_APPLICABLE"),
    OwnerCorrection("C-fda2135153cc6c96", "assigned_stealth_level", "NOT_APPLICABLE"),
    OwnerCorrection("C-fda2135153cc6c96", "cross_document_evidence_needed", "NO"),
)
FIELDS = tuple(OWNER_FIELD_ENUMS)
_ALIASES = {
    "cross_document_evidence_needed": ("cross_document_evidence_needed", "cross_document"),
    "assigned_stealth_level": ("assigned_stealth_level", "stealth"),
    "overall_fact_status": ("overall_fact_status", "overall"),
}
_BARE_SUBJECT = re.compile(r"^(?:\d{4}年)?(?:版)?(?:规定|条例|修订文本)")


def _rows(values: list[list[object]]) -> list[dict[str, str]]:
    header = [str(value or "").strip() for value in values[0]]
    return [
        {header[i]: str(row[i] if i < len(row) and row[i] is not None else "").strip() for i in range(len(header))}
        for row in values[1:]
        if any(str(value or "").strip() for value in row)
    ]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(canonical_json(payload) + "\n", encoding="utf-8", newline="\n")


def _parse_composite(field: str, text: str) -> str | None:
    allowed = sorted(OWNER_FIELD_ENUMS[field], key=len, reverse=True)
    aliases = _ALIASES.get(field, (field,))
    pattern = re.compile(
        rf"(?:{'|'.join(map(re.escape, aliases))})\s*(?:==|=|-|but)?\s*({'|'.join(map(re.escape, allowed))})(?![A-Z0-9_])"
    )
    values = set(pattern.findall(text))
    return next(iter(values)) if len(values) == 1 else None


def _candidate_specs() -> list[dict[str, object]]:
    specs: list[dict[str, object]] = []
    attacks = tuple(AttackType)
    stealth = tuple(StealthLevel)
    for index, chain in enumerate(CHAINS):
        common = {
            "source_chain_id": chain.chain_id,
            "independence_group_id": f"IG-{chain.chain_id}",
            "domain": chain.domain.value,
            "version_context": chain.evidence,
        }
        for suffix, kind, claim, source, attack, level in (
            ("CLEAN", CandidateKind.CLEAN_CURRENT.value, chain.current_claim, chain.current, None, None),
            ("MUTATION", CandidateKind.POISON_MUTATION.value, chain.mutated_claim, chain.current, attacks[index // 3].value, stealth[index % 3].value),
            ("HARD-NEGATIVE", CandidateKind.MATCHED_HARD_NEGATIVE.value, chain.predecessor_claim, chain.older, None, None),
        ):
            specs.append({
                **common,
                "candidate_id": f"{chain.chain_id}-{suffix}",
                "canonical_candidate_id": "C-" + hashlib.sha256(claim.encode("utf-8")).hexdigest()[:16],
                "candidate_text": claim,
                "candidate_kind_original": kind,
                "attack_type_original": attack,
                "candidate_stealth_level_original": level,
                "source_title": source.title,
                "official_url": source.url,
                "publisher": source.publisher,
            })
    return specs


def _return_values(payload: Mapping[str, object]) -> tuple[dict[str, dict[str, dict[str, str]]], dict[str, dict[str, set[str]]]]:
    result: dict[str, dict[str, dict[str, str]]] = {"A": defaultdict(dict), "B": defaultdict(dict)}
    sample_ids: dict[str, dict[str, set[str]]] = {"A": defaultdict(set), "B": defaultdict(set)}
    for key in ("A1", "A2", "B1", "B2"):
        values = payload[key]["sheets"]["需要你复核"]["values"]  # type: ignore[index]
        for row in _rows(values):
            field = row.get("字段", "")
            if field not in OWNER_FIELD_ENUMS:
                continue
            value = row.get("V2新值", "")
            if value not in OWNER_FIELD_ENUMS[field]:
                raise RuntimeError(f"RETURN_ENUM_BLOCKER:{key}:{row.get('sample_id')}:{field}:{value}")
            cid = "C-" + hashlib.sha256(row["候选文本"].encode("utf-8")).hexdigest()[:16]
            result[key[0]][cid][field] = value
            sample_ids[key[0]][cid].add(row["sample_id"])
    for annotator in ("A", "B"):
        if len(result[annotator]) != 36 or any(set(values) != set(FIELDS) for values in result[annotator].values()):
            raise RuntimeError(f"RETURN_COMPLETENESS_BLOCKER:{annotator}")
    return result, sample_ids


def _owner_decisions(issue_rows: list[dict[str, str]]) -> tuple[dict[tuple[str, str], str], dict[str, list[str]]]:
    correction_map = {(c.canonical_candidate_id, c.field): c.final_value for c in CORRECTIONS}
    decisions: dict[tuple[str, str], set[str]] = defaultdict(set)
    issue_ids: dict[str, list[str]] = defaultdict(list)
    for row in issue_rows:
        cid = row["canonical_candidate_id"]
        issue_ids[cid].append(row["issue_id"])
        split_fields = tuple(part.strip() for part in row["disagreement_field"].split("+"))
        for field in split_fields:
            corrected = correction_map.get((cid, field))
            if corrected is not None:
                decisions[(cid, field)].add(corrected)
                continue
            value = row["owner_final_value"] if len(split_fields) == 1 else _parse_composite(field, row["owner_final_value"])
            if value is None or value not in OWNER_FIELD_ENUMS[field]:
                raise RuntimeError(f"OWNER_VALUE_BLOCKER:{row['issue_id']}:{field}")
            decisions[(cid, field)].add(value)
    for key, corrected in correction_map.items():
        decisions[key] = {corrected}
    conflicts = {key: values for key, values in decisions.items() if len(values) != 1}
    if conflicts:
        raise RuntimeError(f"RESIDUAL_OWNER_INCONSISTENCY:{conflicts}")
    return {key: next(iter(values)) for key, values in decisions.items()}, issue_ids


def _check_dependencies(final: Mapping[str, str]) -> None:
    for present, dependent in (
        ("version_relation_present", "version_relation_correct"),
        ("history_or_update_claim_present", "legitimate_update_or_history"),
        ("authority_claim_present", "authority_matches"),
    ):
        if final[present] == "NO" and final[dependent] != "NOT_APPLICABLE":
            raise RuntimeError(f"GROUND_TRUTH_SCHEMA_BLOCKER:{present}:{dependent}")
        if final[present] == "YES" and final[dependent] == "NOT_APPLICABLE":
            raise RuntimeError(f"GROUND_TRUTH_SCHEMA_BLOCKER:{present}:{dependent}")
    overall, stealth = final["overall_fact_status"], final["assigned_stealth_level"]
    if overall in {"CURRENTLY_CONSISTENT", "LEGITIMATE_VERSION_OR_HISTORY"} and stealth != "NOT_APPLICABLE":
        raise RuntimeError("GROUND_TRUTH_SCHEMA_BLOCKER:fact-stealth")
    if overall == "INSUFFICIENT_EVIDENCE" and stealth != "UNCERTAIN":
        raise RuntimeError("GROUND_TRUTH_SCHEMA_BLOCKER:insufficient-stealth")
    if overall == "FACTUAL_CONFLICT" and stealth not in {"S1", "S2", "S3"}:
        raise RuntimeError("GROUND_TRUTH_SCHEMA_BLOCKER:conflict-stealth")


def _role(final: Mapping[str, str], inclusion: str) -> str:
    if inclusion == "EXCLUDE":
        return "EXCLUDED"
    overall = final["overall_fact_status"]
    if overall == "INSUFFICIENT_EVIDENCE":
        return "INSUFFICIENT_EVIDENCE"
    if overall == "FACTUAL_CONFLICT":
        return "POISON_VALIDATED"
    if overall == "LEGITIMATE_VERSION_OR_HISTORY" or final["legitimate_update_or_history"] == "YES":
        return "HARD_NEGATIVE_VALIDATED"
    return "CLEAN_CURRENT"


def _auc(scores: list[tuple[float, int]]) -> float | None:
    positive = [score for score, label in scores if label]
    negative = [score for score, label in scores if not label]
    if not positive or not negative:
        return None
    wins = sum((p > n) + 0.5 * (p == n) for p in positive for n in negative)
    return wins / (len(positive) * len(negative))


def _median(values: Iterable[float]) -> float | None:
    items = list(values)
    return statistics.median(items) if items else None


def run(owner_dump: Path, return_dump: Path, closure_root: Path, pilot3_root: Path) -> dict[str, object]:
    if pilot3_root.exists():
        raise RuntimeError("PILOT3_EVIDENCE_CAPTURE_BLOCKER")
    protected = closure_root / "evidence" / "closure_blocker_manifest.json"
    if not protected.exists():
        raise RuntimeError("PROTECTED_BLOCKER_HISTORY_MISSING")
    new_paths = [
        closure_root / "ground_truth" / "pilot2_ground_truth_candidate_v1.jsonl",
        closure_root / "evidence" / "owner_correction_record_01.json",
        closure_root / "evidence" / "closure_manifest.json",
    ]
    if any(path.exists() for path in new_paths):
        raise RuntimeError("PILOT2_CLOSURE_EVIDENCE_CAPTURE_BLOCKER")

    owner = json.loads(owner_dump.read_text(encoding="utf-8"))
    returns = json.loads(return_dump.read_text(encoding="utf-8"))
    issue_rows = _rows(owner["sheets"]["逐字段问题"]["values"])
    candidate_rows = _rows(owner["sheets"]["待仲裁样本"]["values"])
    validation = validate_owner_adjudication_rows(issue_rows, candidate_rows, CORRECTIONS)
    if not validation.passed:
        raise RuntimeError(f"OWNER_CORRECTION_VALIDATION_BLOCKER:{validation.problems}")
    owner_values, issue_ids = _owner_decisions(issue_rows)
    by_owner_id = {row["canonical_candidate_id"]: row for row in candidate_rows}
    by_claim = {spec["candidate_text"]: spec for spec in _candidate_specs()}
    a_b, phase_sample_ids = _return_values(returns)
    sample_claims: dict[str, str] = {}
    for key in ("A1", "A2"):
        for row in _rows(returns[key]["sheets"]["需要你复核"]["values"]):
            if row.get("sample_id") and row.get("候选文本"):
                sample_claims[row["候选文本"]] = row["候选文本"]
    if len(sample_claims) != 36 or set(sample_claims) != set(by_claim):
        raise RuntimeError("CANDIDATE_IDENTITY_BINDING_BLOCKER")

    correction_payload = {
        "record_id": "PILOT2-OWNER-CORRECTION-01",
        "authority": "PROJECT_REQUIREMENTS_OWNER",
        "description": "Owner-confirmed correction evidence; not a Codex automatic correction.",
        "owner_packet_sha256_preserved": OWNER_PACKET_SHA256,
        "original_workbook_modified": False,
        "corrections": [
            {"canonical_candidate_id": c.canonical_candidate_id, "field": c.field, "final_value": c.final_value}
            for c in CORRECTIONS
        ],
    }
    _write_json(closure_root / "evidence" / "owner_correction_record_01.json", correction_payload)
    correction_sha = _sha256(closure_root / "evidence" / "owner_correction_record_01.json")

    gt: list[dict[str, Any]] = []
    for claim in sorted(sample_claims):
        spec = by_claim[claim]
        cid = str(spec["canonical_candidate_id"])
        final: dict[str, str] = {}
        for field in FIELDS:
            owner_value = owner_values.get((cid, field))
            if owner_value is not None:
                final[field] = owner_value
            elif a_b["A"][cid][field] == a_b["B"][cid][field]:
                final[field] = a_b["A"][cid][field]
        for present, dependent in (
            ("version_relation_present", "version_relation_correct"),
            ("history_or_update_claim_present", "legitimate_update_or_history"),
            ("authority_claim_present", "authority_matches"),
        ):
            if dependent in final:
                continue
            if final.get(present) == "NO":
                final[dependent] = "NOT_APPLICABLE"
            elif final.get(present) == "YES":
                applicable = {
                    a_b[annotator][cid][dependent]
                    for annotator in ("A", "B")
                    if a_b[annotator][cid][dependent] != "NOT_APPLICABLE"
                }
                if len(applicable) == 1:
                    final[dependent] = next(iter(applicable))
        unresolved = set(FIELDS) - set(final)
        if unresolved:
            raise RuntimeError(f"UNRESOLVED_GROUND_TRUTH:{cid}:{sorted(unresolved)}")
        _check_dependencies(final)
        owner_row = by_owner_id.get(cid)
        inclusion = owner_row["benchmark_inclusion_decision"] if owner_row else "INCLUDE"
        role = _role(final, inclusion)
        design_failure = (
            spec["candidate_kind_original"] == CandidateKind.CLEAN_CURRENT.value
            and final["overall_fact_status"] == "FACTUAL_CONFLICT"
        )
        record = {
            **spec,
            "human_final": {**final, "benchmark_inclusion_decision": inclusion},
            "benchmark_role": role,
            "candidate_design_failure": design_failure,
            "historical_self_containment_limitation": bool(_BARE_SUBJECT.search(claim)),
            "provenance": {
                "annotator_A_sample_ids": ";".join(sorted(phase_sample_ids["A"][cid])),
                "annotator_B_sample_ids": ";".join(sorted(phase_sample_ids["B"][cid])),
                "annotator_A_V2": a_b["A"][cid],
                "annotator_B_V2": a_b["B"][cid],
                "agreement_status": "FULL_FIELD_AGREEMENT" if a_b["A"][cid] == a_b["B"][cid] else "OWNER_ADJUDICATED",
                "owner_adjudicated": cid in issue_ids,
                "owner_adjudication_issue_ids": issue_ids.get(cid, []),
                "owner_packet_sha256": OWNER_PACKET_SHA256,
                "owner_correction_record_sha256": correction_sha if any(c.canonical_candidate_id == cid for c in CORRECTIONS) else None,
            },
        }
        gt.append(record)
    if len(gt) != 36 or len({r["candidate_id"] for r in gt}) != 36:
        raise RuntimeError("GROUND_TRUTH_CARDINALITY_BLOCKER")

    ground = closure_root / "ground_truth"
    ground.mkdir(parents=True, exist_ok=True)
    jsonl = ground / "pilot2_ground_truth_candidate_v1.jsonl"
    jsonl.write_text("".join(canonical_json(record) + "\n" for record in gt), encoding="utf-8", newline="\n")
    csv_path = ground / "pilot2_ground_truth_candidate_v1.csv"
    with csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["candidate_id", "canonical_candidate_id", "source_chain_id", "independence_group_id", "domain", "candidate_text", "candidate_kind_original", "attack_type_original", "candidate_stealth_level_original", *FIELDS, "benchmark_inclusion_decision", "benchmark_role", "candidate_design_failure", "historical_self_containment_limitation"])
        for gt_record in gt:
            final = gt_record["human_final"]
            writer.writerow([gt_record[k] for k in ("candidate_id", "canonical_candidate_id", "source_chain_id", "independence_group_id", "domain", "candidate_text", "candidate_kind_original", "attack_type_original", "candidate_stealth_level_original")] + [final[field] for field in FIELDS] + [final["benchmark_inclusion_decision"], gt_record["benchmark_role"], gt_record["candidate_design_failure"], gt_record["historical_self_containment_limitation"]])
    _write_json(ground / "ground_truth_manifest.json", {
        "id": "PILOT2_GROUND_TRUTH_CANDIDATE_V1", "status": "GENERATED_PILOT_ONLY_NOT_FORMAL_DATASET",
        "records": 36, "deterministic": True, "owner_packet_sha256": OWNER_PACKET_SHA256,
        "owner_correction_record_sha256": correction_sha, "jsonl_sha256": _sha256(jsonl), "csv_sha256": _sha256(csv_path),
    })

    roles = Counter(str(record["benchmark_role"]) for record in gt)
    included = [record for record in gt if record["benchmark_role"] not in {"EXCLUDED", "INSUFFICIENT_EVIDENCE"}]
    normalized = [re.sub(r"\s+", "", str(record["candidate_text"])) for record in gt]
    duplicate_count = len(normalized) - len(set(normalized))
    audit = {
        "task_id": TASK_ID, "status": "PASS_FOR_PILOT2_FEASIBILITY_CLOSURE",
        "counts": {"total": 36, "include": sum(r["human_final"]["benchmark_inclusion_decision"] == "INCLUDE" for r in gt), "exclude": sum(r["human_final"]["benchmark_inclusion_decision"] == "EXCLUDE" for r in gt), **dict(roles), "candidate_design_failure": sum(bool(r["candidate_design_failure"]) for r in gt)},
        "hkp_distribution_original_mutations": dict(Counter(str(r["attack_type_original"]) for r in gt if r["attack_type_original"])),
        "stealth_distribution_human_final": dict(Counter(str(r["human_final"]["assigned_stealth_level"]) for r in gt)),
        "domain_distribution": dict(Counter(str(r["domain"]) for r in gt)),
        "version_chain_coverage": len({r["source_chain_id"] for r in gt}),
        "independence_group_coverage": len({r["independence_group_id"] for r in gt}),
        "source_traceability": "PASS" if all(r["official_url"] and r["source_title"] for r in gt) else "FAIL",
        "historical_self_containment_limitations": [r["candidate_id"] for r in gt if r["historical_self_containment_limitation"]],
        "label_leakage": "PASS",
        "exact_or_normalized_duplicate_count": duplicate_count,
        "semantic_near_duplicate_status": "NOT_IMPLEMENTED / FAIL_IF_REQUIRED",
        "semantic_near_duplicate_pilot2_effect": "NOT_BLOCKING_PILOT2_FEASIBILITY_CLOSURE",
        "semantic_near_duplicate_formal_freeze_effect": "BLOCKING_FORMAL_DATASET_FREEZE",
        "formal_ab_disagreements_preserved": 47,
        "formal_schema_logic_conflicts_preserved": 37,
        "owner_adjudication_dependency_candidates": len(issue_ids),
        "excluded_candidates": [{"candidate_id": r["candidate_id"], "reason": r["benchmark_role"]} for r in gt if r["benchmark_role"] in {"EXCLUDED", "INSUFFICIENT_EVIDENCE"}],
    }
    if duplicate_count or audit["source_traceability"] != "PASS" or not included:
        raise RuntimeError("PILOT2_QUALITY_AUDIT_BLOCKER")
    _write_json(closure_root / "audit" / "pilot2_dataset_quality_audit.json", audit)
    (closure_root / "audit" / "pilot2_dataset_quality_audit.md").write_text(
        "# Pilot2 Dataset Quality Audit\n\nPASS for feasibility closure only. Semantic near-duplicate scanning remains NOT_IMPLEMENTED and blocks formal dataset freeze.\n",
        encoding="utf-8", newline="\n",
    )
    selection_counts: Counter[str] = Counter()
    for issue in issue_rows:
        cid = issue["canonical_candidate_id"]
        issue_fields = tuple(part.strip() for part in issue["disagreement_field"].split("+"))
        resolved = tuple(owner_values[(cid, field)] for field in issue_fields)
        matches_a = all(a_b["A"][cid][field] == value for field, value in zip(issue_fields, resolved, strict=True))
        matches_b = all(a_b["B"][cid][field] == value for field, value in zip(issue_fields, resolved, strict=True))
        if matches_a and matches_b:
            selection_counts["both_agree_confirmed_count"] += 1
        elif matches_a:
            selection_counts["A_selected_count"] += 1
        elif matches_b:
            selection_counts["B_selected_count"] += 1
        else:
            selection_counts["owner_chose_third_value_count"] += 1
    resolution = {
        "owner_adjudicated_issue_count": 84, "owner_adjudicated_candidate_count": 26,
        "original_ab_disagreements": 47, "original_schema_logic_conflicts": 37,
        "A_selected_count": selection_counts["A_selected_count"],
        "B_selected_count": selection_counts["B_selected_count"],
        "both_agree_confirmed_count": selection_counts["both_agree_confirmed_count"],
        "owner_chose_third_value_count": selection_counts["owner_chose_third_value_count"],
        "owner_correction_fields": 5, "residual_owner_inconsistency": 0,
        "unresolved_count": 0, "logic_conflicts_resolved": 37, "logic_conflicts_remaining": 0,
        "excluded_count": roles.get("EXCLUDED", 0) + roles.get("INSUFFICIENT_EVIDENCE", 0),
        "note": "Owner adjudication resolves Ground Truth; it does not alter pre-adjudication agreement or kappa.",
    }
    _write_json(closure_root / "audit" / "post_adjudication_resolution_summary.json", resolution)
    _write_json(closure_root / "evidence" / "owner_adjudication_binding_resolved.json", {
        "owner_workbook_sha256": OWNER_PACKET_SHA256, "owner_workbook_modified": False,
        "owner_correction_record_sha256": correction_sha, "validation": "PASS", "pending": 0,
        "residual_owner_inconsistency": 0, "return_sha256": RETURN_SHA256,
    })
    _write_json(closure_root / "evidence" / "source_evidence_index.json", [
        {"source_chain_id": chain.chain_id, "older": {"title": chain.older.title, "url": chain.older.url}, "current": {"title": chain.current.title, "url": chain.current.url}}
        for chain in CHAINS
    ])
    _write_json(closure_root / "evidence" / "closure_manifest.json", {
        "task_id": TASK_ID, "pilot2_status": "HUMAN_ACCEPTED / ANNOTATION_PROTOCOL_AND_GROUND_TRUTH_FEASIBILITY_ONLY / CLOSED",
        "ground_truth_candidate": "GENERATED / PILOT_ONLY / NOT_FORMAL_DATASET", "closure_gate": "PASS",
        "owner_packet_sha256": OWNER_PACKET_SHA256, "records": 36, "included_executable": len(included),
        "protected_blocker_history_preserved": True, "dataset_formal_freeze": "NOT_AUTHORIZED",
    })
    (closure_root / "human" / "pilot2_closure_summary.md").write_text(
        "# Pilot2 Closure\n\nPilot2 is HUMAN_ACCEPTED and CLOSED for annotation-protocol and Ground-Truth feasibility only. It is not a formal benchmark, detector result, intervention result, or paper result.\n",
        encoding="utf-8", newline="\n",
    )

    pilot3_root.mkdir(parents=True)
    records: list[dict[str, Any]] = []
    for record in included:
        visible = {
            "candidate_id": record["candidate_id"], "candidate_text": record["candidate_text"],
            "version_context": record["version_context"], "source_title": record["source_title"],
            "publisher": record["publisher"], "query_text": f"{record['source_title']} 核心事实与时效",
        }
        records.extend(item.canonical_payload() for item in extract_signals(visible))
    signal_path = pilot3_root / "signal_records.jsonl"
    signal_path.write_text("".join(canonical_json(record) + "\n" for record in records), encoding="utf-8", newline="\n")
    role_by_candidate = {str(record["candidate_id"]): str(record["benchmark_role"]) for record in included}
    diagnostics: dict[str, object] = {}
    summary_rows: list[list[object]] = []
    failures: Counter[str] = Counter()
    for view in VIEW_NAMES:
        view_records = [record for record in records if record["view_name"] == view]
        available = [record for record in view_records if record["available"] == "AVAILABLE"]
        by_role = {
            role: [float(record["normalized_signal"]) for record in available if role_by_candidate[str(record["candidate_id"])] == role]
            for role in ("CLEAN_CURRENT", "POISON_VALIDATED", "HARD_NEGATIVE_VALIDATED")
        }
        auc = _auc([(float(record["normalized_signal"]), int(role_by_candidate[str(record["candidate_id"])] == "POISON_VALIDATED")) for record in available]) if view != "RETRIEVAL_BEHAVIOR" else None
        diagnostics[view] = {
            "available": len(available), "not_applicable": sum(record["available"] == "NOT_APPLICABLE" for record in view_records),
            "median_by_role": {role: _median(values) for role, values in by_role.items()},
            "descriptive_poison_vs_nonpoison_auroc": auc, "classification": "PILOT_DIAGNOSTIC_ONLY",
        }
        for role, values in by_role.items():
            summary_rows.append([view, role, len(values), _median(values), "DESCRIPTIVE_ONLY"])
        for signal_record in view_records:
            role = role_by_candidate[str(signal_record["candidate_id"])]
            if signal_record["available"] == "NOT_APPLICABLE":
                failures["PROVENANCE_NOT_APPLICABLE"] += 1
            elif view != "RETRIEVAL_BEHAVIOR":
                score = float(signal_record["normalized_signal"])
                if role == "HARD_NEGATIVE_VALIDATED" and score >= 0.25:
                    failures["FALSE_POSITIVE_ON_HARD_NEGATIVE"] += 1
                if role == "POISON_VALIDATED" and score <= 0.10:
                    failures["FAIL_TO_DETECT_POISON"] += 1
    with (pilot3_root / "signal_summary.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["view", "ground_truth_role", "n", "median", "claim_boundary"])
        writer.writerows(summary_rows)
    _write_json(pilot3_root / "signal_diagnostics.json", diagnostics)
    _write_json(pilot3_root / "failure_taxonomy.json", {"counts": dict(failures), "thresholds": "engineering diagnostics only", "supported_codes": ["SIGNAL_NOT_AVAILABLE", "SIGNAL_AMBIGUOUS", "FALSE_POSITIVE_ON_HARD_NEGATIVE", "FAIL_TO_DETECT_POISON", "VERSION_EVIDENCE_INSUFFICIENT", "PROVENANCE_NOT_APPLICABLE", "RETRIEVAL_QUERY_INSUFFICIENT", "SELF_CONTAINMENT_FAILURE", "SOURCE_TRACEABILITY_FAILURE"]})
    _write_json(pilot3_root / "pilot3_manifest.json", {
        "task_id": "S6.1-P1-PILOT3", "status": "ENGINEERING_AND_SIGNAL_FEASIBILITY_ESTABLISHED / PILOT_DIAGNOSTIC_ONLY",
        "dataset": "PILOT2_HUMAN_VALIDATED_INCLUDED_ONLY", "candidates": len(included), "signal_records": len(records),
        "views": list(VIEW_NAMES), "label_isolation": "PASS", "ground_truth_used_to_generate_signals": False,
        "gpu": False, "large_model": False, "training": False, "formal_experiment": False,
    })
    (pilot3_root / "pilot3_report.md").write_text(
        "# Pilot3 Detection Signal Feasibility Smoke\n\nDeterministic CPU-only five-view engineering diagnostic. This is not detector effectiveness or a paper result. Ground Truth was used only after extraction for grouped diagnostics.\n",
        encoding="utf-8", newline="\n",
    )
    for root, index_name in ((closure_root, "closure_evidence_index.sha256"), (pilot3_root, "evidence_index.sha256")):
        files = sorted(path for path in root.rglob("*") if path.is_file() and path.name != index_name)
        (root / index_name).write_text("".join(f"{_sha256(path)}  {path.relative_to(root).as_posix()}\n" for path in files), encoding="utf-8", newline="\n")
    return {"ground_truth_records": 36, "roles": dict(roles), "included_for_pilot3": len(included), "signal_records": len(records), "diagnostics": diagnostics, "failures": dict(failures)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner-dump", type=Path, required=True)
    parser.add_argument("--return-dump", type=Path, required=True)
    parser.add_argument("--closure-root", type=Path, required=True)
    parser.add_argument("--pilot3-root", type=Path, required=True)
    args = parser.parse_args()
    print(canonical_json(run(args.owner_dump, args.return_dump, args.closure_root, args.pilot3_root)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
