"""Validate the additive D1 remaining90 Phase2 semantic closeout.

The raw lock must predate this program: construction identity is deliberately
loaded only after the locked reviewer comparison has passed all raw gates.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


SEMANTIC_FIELDS = {"overall_fact_status", "version_claim_status"}
EXPECTED_AGREEMENT = {
    "overall_fact_status": 88,
    "version_claim_status": 83,
    "authority_claim_status": 90,
    "minimum_external_evidence_needed": 90,
    "evidence_selection": 78,
    "phase2_issue": 90,
    "possible_accidental_secondary_error": 90,
    "evidence_sufficiency": 90,
}


def need(condition: bool, explanation: str) -> None:
    if not condition:
        raise ValueError(explanation)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    for name in (
        "lock-report", "r3", "r4", "packet", "overlay", "mapping",
        "repair-manifest", "out",
    ):
        parser.add_argument(f"--{name}", required=True, type=Path)
    args = parser.parse_args()
    lock = read_json(args.lock_report)
    need(lock["status"] == "REVIEWER_RAW_LOCKED_BEFORE_CONSTRUCTION_TARGET_LOAD", "raw lock state")
    need(lock["construction_target_loaded"] is False, "construction target was loaded at lock")
    for name in ("r3", "r4"):
        need(digest(getattr(args, name)) == lock[name]["source_sha256"], f"{name} raw digest")
        need(len(getattr(args, name).read_bytes()) == lock[name]["source_bytes"], f"{name} bytes")
    need({key: value["agree"] for key, value in lock["agreement"].items()} ==
         EXPECTED_AGREEMENT, "agreement values")
    rows = {name: read_json(getattr(args, name)) for name in ("r3", "r4")}
    by = {name: {r["blind_review_id"]: r for r in value} for name, value in rows.items()}
    need(all(len(value) == 90 for value in by.values()), "reviewer row count")
    packet = read_json(args.packet)
    visible = {r["blind_review_id"]: r["candidate_text"] for r in packet["records"]}
    need(set(visible) == set(by["r3"]) == set(by["r4"]), "visible ID universe")
    overlay = read_json(args.overlay)
    records = overlay["records"]
    need(len(records) == 9, "nine semantic field decisions required")
    actual_semantic = {
        (ident, field)
        for ident in visible
        for field in SEMANTIC_FIELDS
        if by["r3"][ident][field] != by["r4"][ident][field]
    }
    covered = {(r["blind_id"], r["disagreement_field"]) for r in records}
    need(len(covered) == 9 and covered == actual_semantic, "semantic disagreement coverage")
    for row in records:
        ident, field = row["blind_id"], row["disagreement_field"]
        need(row["r3_value"] == by["r3"][ident][field], f"{ident} {field} R3 lineage")
        need(row["r4_value"] == by["r4"][ident][field], f"{ident} {field} R4 lineage")
        need(row["final_semantic_value"] in {row["r3_value"], row["r4_value"]},
             f"{ident} {field} novel enum")
        need(row["candidate_span"] in visible[ident], f"{ident} candidate span")
        need(row["rule_source"] and row["owner_adjudication_reason"], f"{ident} reason")
    process_diffs = [ident for ident in visible if
                     by["r3"][ident]["evidence_selection"] !=
                     by["r4"][ident]["evidence_selection"]]
    need(len(process_diffs) == 12, "process-difference count")
    need(all(row["disagreement_field"] != "evidence_selection" for row in records),
         "process values may not be overwritten")
    semantic = {key: row["final_semantic_value"] for row in records
                for key in [(row["blind_id"], row["disagreement_field"])]}
    final_rows: dict[str, dict[str, str]] = {}
    for ident in visible:
        final_rows[ident] = {}
        for field in ("overall_fact_status", "version_claim_status",
                      "authority_claim_status", "minimum_external_evidence_needed",
                      "phase2_issue", "possible_accidental_secondary_error",
                      "evidence_sufficiency"):
            final_rows[ident][field] = semantic.get((ident, field), by["r3"][ident][field])
    old_mapping = read_json(args.mapping)["records"]
    repairs = read_json(args.repair_manifest)["records"]
    mapping = {r["blind_review_id"]: dict(r) for r in old_mapping}
    for repair in repairs:
        old_id, new_id = repair["old_blind_review_id"], repair["new_blind_review_id"]
        need(old_id in mapping and new_id not in mapping, "repair mapping lineage")
        updated = mapping.pop(old_id)
        for field in ("sample_id", "group_slot_id", "role"):
            need(updated[field] == repair[field], "repair changes construction identity")
        updated["blind_review_id"] = new_id
        mapping[new_id] = updated
    need(set(mapping) == set(visible) and len(mapping) == 90, "mapping after targeted4")
    groups: dict[str, list[tuple[str, dict[str, str]]]] = defaultdict(list)
    for ident, identity in mapping.items():
        groups[identity["group_slot_id"]].append((ident, identity))
    need(len(groups) == 30, "30 groups")
    target_to_min = {
        "S1": "ZERO_EXTERNAL_EVIDENCE_REQUIRED",
        "S2": "ONE_OFFICIAL_EVIDENCE",
        "S3": "MULTI_EVIDENCE_OR_VERSION_CHAIN",
    }
    derived: Counter[str] = Counter()
    for group, members in groups.items():
        need(len(members) == 3 and {r["role"] for _, r in members} ==
             {"CLEAN_CURRENT", "POISON", "HARD_NEGATIVE"}, f"{group} triplet")
        for ident, identity in members:
            row = final_rows[ident]
            need(row["phase2_issue"] == "NONE" and row["evidence_sufficiency"] ==
                 "SUFFICIENT" and row["possible_accidental_secondary_error"] == "NO",
                 f"{ident} safety")
            if identity["role"] == "POISON":
                need(row["overall_fact_status"] == "FACTUAL_CONFLICT", f"{ident} poison")
                need(row["minimum_external_evidence_needed"] ==
                     target_to_min[identity["target_s"]], f"{ident} derived S mismatch")
                derived[identity["target_s"]] += 1
            else:
                need(row["overall_fact_status"] != "FACTUAL_CONFLICT", f"{ident} nonpoison")
                need(row["minimum_external_evidence_needed"] == "NOT_APPLICABLE",
                     f"{ident} nonconflict minimum")
    need(dict(derived) == {"S1": 11, "S2": 8, "S3": 11}, "derived S distribution")
    output = {
        "status": "D1_REMAINING90_PHASE2_ACCEPTED_FOR_PREANNOTATION_QA",
        "raw_lock_utc": lock["locked_at_utc"],
        "construction_mapping_loaded_after_raw_lock": True,
        "reviewer_isolation_proof": "OWNER_ATTESTED",
        "r4_reviewer_code": "R4-codex",
        "r4_provider": "Doubao",
        "raw_sha256": {name: lock[name]["source_sha256"] for name in ("r3", "r4")},
        "raw_comparison_sha256": digest(args.lock_report),
        "semantic_overlay_sha256": digest(args.overlay),
        "agreement": EXPECTED_AGREEMENT,
        "semantic_disagreement_fields": 9,
        "semantic_disagreement_candidates": 7,
        "semantic_blockers_remaining": 0,
        "process_only_evidence_selection_difference_count": 12,
        "process_difference_ids": sorted(process_diffs),
        "process_values_preserved_per_reviewer": True,
        "phase2_safety_gate": "PASS",
        "factual_conflict_per_reviewer": 30,
        "groups": 30,
        "candidate_count": 90,
        "derived_s": dict(sorted(derived.items())),
        "construction_roles_not_used_to_select_semantic_overlay": True,
        "raw_reviewer_values_rewritten": False,
        "human_annotation_not_started": True,
        "ground_truth_not_created": True,
    }
    need(not args.out.exists(), "refusing to overwrite acceptance output")
    args.out.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
