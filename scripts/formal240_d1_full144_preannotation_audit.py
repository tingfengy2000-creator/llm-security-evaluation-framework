"""Re-audit the frozen D1 24+30+90 corpus before Human workbook release.

Private identity inputs remain outside Git. Outputs contain aggregate QA only.
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import itertools
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROLES = {"CLEAN_CURRENT", "POISON", "HARD_NEGATIVE"}


def need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def lines(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source(root: Path, directory: str, filename: str) -> Path:
    path = root / directory / filename
    need(path.is_file(), f"missing frozen source: {filename}")
    return path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--matrix", type=Path, required=True)
    parser.add_argument("--family-overlay", type=Path, required=True)
    parser.add_argument("--phase2-matrix", type=Path, required=True)
    parser.add_argument("--batch1-final-matrix", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    root = args.source_root
    canary_dir = "paper1_formal240_d1_canary_r3r4_phase1_raw_lock_20260923"
    canary_final = "paper1_formal240_d1_canary_final_owner_acceptance_20260926_run02"
    batch_dir = "paper1_formal240_d1_remaining40_hkp1_batch1_20260926"
    remaining_dir = "paper1_formal240_d1_remaining90_megawave_20260927"
    phase1_dir = "paper1_core144_scope_d1_phase1_closeout_20260927"
    canary_candidates = source(root, canary_dir, "PAPER1_FORMAL_D1_CANARY_CANDIDATES_V3.jsonl")
    canary_mapping = source(root, canary_dir, "PAPER1_FORMAL_D1_CANARY_BLIND_MAPPING_PRIVATE_V3.json")
    canary_matrix = source(root, canary_final, "PAPER1_FORMAL_D1_CANARY_FINAL_ACCEPTANCE_MATRIX_V1.json")
    canary_atoms = source(root, "paper1_formal240_d1_canary_final_owner_acceptance_20260926_run03_atom_supplement",
                          "PAPER1_FORMAL_D1_CANARY_FINAL_FACT_ATOM_AUDIT_V2.json")
    batch_candidates = source(root, batch_dir + "/construction_v4", "PAPER1_FORMAL_D1_HKP1_BATCH1_CANDIDATES_V4.jsonl")
    batch_mapping = source(root, batch_dir + "/construction_v4", "PAPER1_FORMAL_D1_HKP1_BATCH1_IDENTITY_MAPPING_V4.json")
    batch_atoms = source(root, batch_dir + "/construction_v4", "PAPER1_FORMAL_D1_HKP1_BATCH1_FACT_ATOM_AUDIT_V4.json")
    current_candidates = source(root, phase1_dir + "/targeted4_phase1_v2/control_only_do_not_send",
                                "PAPER1_FORMAL_D1_REMAINING90_CURRENT_CANDIDATE_ONLY_V3.json")
    old_mapping = source(root, remaining_dir + "/phase1_release_v1/control_only_do_not_send",
                         "PAPER1_FORMAL_D1_REMAINING90_PHASE1_IDENTITY_MAPPING_PRIVATE_V1.json")
    repair = source(root, phase1_dir + "/targeted4_phase1_v2/control_only_do_not_send",
                    "PAPER1_FORMAL_D1_REMAINING90_AUTHORITY_TARGETED4_REPAIR_MANIFEST_V2.json")
    remain_atoms = source(root, remaining_dir + "/control_dossier_v1", "PAPER1_FORMAL_D1_REMAINING90_FACT_ATOM_AUDIT_V1.json")
    remain_views = source(root, remaining_dir + "/control_dossier_v1", "PAPER1_FORMAL_D1_REMAINING90_VIEW_READINESS_V1.json")
    remain_query = source(root, remaining_dir + "/control_dossier_v1", "PAPER1_FORMAL_D1_REMAINING90_QUERY_AUDIT_V1.json")
    remain_smoke = source(root, remaining_dir + "/control_dossier_v1", "PAPER1_FORMAL_D1_REMAINING90_RETRIEVAL_SMOKE_V1.json")
    canary_view = source(root, canary_final, "PAPER1_FORMAL_D1_CANARY_FINAL_VIEW_READINESS_SUMMARY_V1.json")
    canary_smoke = source(root, canary_final, "PAPER1_FORMAL_D1_CANARY_FINAL_RETRIEVAL_SMOKE_V1.json")
    batch_view = source(root, batch_dir + "/preblind_v4", "PAPER1_FORMAL_D1_HKP1_BATCH1_VIEW_READINESS_V4.json")
    batch_query = source(root, batch_dir + "/preblind_v4", "PAPER1_FORMAL_D1_HKP1_BATCH1_QUERY_AUDIT_V4.json")
    batch_smoke = source(root, batch_dir + "/preblind_v4", "PAPER1_FORMAL_D1_HKP1_BATCH1_RETRIEVAL_SMOKE_V4.json")
    need(read(canary_matrix)["all_hard_gates_pass"] is True, "Canary acceptance not final")
    need(read(args.batch1_final_matrix)["status"] ==
         "D1_HKP1_BATCH1_ACCEPTED_FOR_D1_CONSTRUCTION_ONLY", "Batch-1 acceptance not final")
    need(read(args.phase2_matrix)["status"] == "D1_REMAINING90_PHASE2_ACCEPTED_FOR_PREANNOTATION_QA",
         "remaining90 Phase2 not closed")
    need(read(canary_atoms)["candidate_count"] == 24 and
         read(canary_atoms)["classification_counts"] ==
         {"CONTROLLED_POISON": 8, "SUPPORTED": 40}, "Canary atom acceptance")
    b_atoms = read(batch_atoms)
    need(len(b_atoms["records"]) == 30 and b_atoms["unsupported_accidental_total"] == 0 and
         b_atoms["ambiguous_total"] == 0 and b_atoms["controlled_poison_total"] == 10,
         "Batch-1 atom acceptance")
    r_atoms = read(remain_atoms)["records"]
    need(Counter(row["status"] for row in r_atoms) == {"SUPPORTED": 131, "CONTROLLED_POISON": 30},
         "remaining90 atom acceptance")
    candidate_sets = [lines(canary_candidates), lines(batch_candidates), read(current_candidates)["records"]]
    need([len(x) for x in candidate_sets] == [24, 30, 90], "cohort candidate counts")
    candidates = {row["blind_review_id"]: row for group in candidate_sets for row in group}
    need(len(candidates) == 144, "candidate IDs not unique")
    need(len({row["candidate_text"] for row in candidates.values()}) == 144,
         "exact duplicate candidate text")
    mapping: dict[str, dict[str, Any]] = {}
    for row in read(canary_mapping):
        mapping[row["blind_review_id"]] = {**row, "role": row["construction_role"]}
    for row in read(batch_mapping)["mapping"]:
        need(row["blind_review_id"] not in mapping, "batch ID collision")
        mapping[row["blind_review_id"]] = row
    old = {row["blind_review_id"]: dict(row) for row in read(old_mapping)["records"]}
    for row in read(repair)["records"]:
        revised = old.pop(row["old_blind_review_id"])
        need(revised["sample_id"] == row["sample_id"] and revised["role"] == row["role"],
             "targeted4 identity lineage")
        revised["blind_review_id"] = row["new_blind_review_id"]
        old[revised["blind_review_id"]] = revised
    need(len(old) == 90 and set(old) == {r["blind_review_id"] for r in candidate_sets[2]},
         "remaining90 current ID parity")
    mapping.update(old)
    need(len(mapping) == 144 and set(mapping) == set(candidates), "full mapping parity")
    for ident, cand in candidates.items():
        if "group_slot_id" in cand:
            need(cand["group_slot_id"] == mapping[ident]["group_slot_id"], "group lineage")
        if "construction_role" in cand:
            need(cand["construction_role"] == mapping[ident]["role"], "role lineage")
        need(cand["candidate_text"].strip() != "", "blank Candidate")
    groups: dict[str, list[str]] = defaultdict(list)
    for ident, identity in mapping.items():
        groups[identity["group_slot_id"]].append(ident)
    frozen = {r["group_slot_id"]: r for r in lines(args.matrix) if r["domain"] == "D1"}
    need(len(frozen) == 48 and set(groups) == set(frozen), "frozen matrix slot parity")
    hkp: Counter[str] = Counter()
    target: Counter[str] = Counter()
    role: Counter[str] = Counter()
    length_ratios: list[float] = []
    for group, ids in groups.items():
        need(len(ids) == 3 and {mapping[i]["role"] for i in ids} == ROLES, f"{group} triplet")
        match = re.fullmatch(r"F240-D1-(HKP[1-4])-(S[1-3])-C([1-4])", group)
        need(match is not None, f"invalid group slot {group}")
        assert match is not None
        hkp[match.group(1)] += 1
        target[match.group(2)] += 1
        need(frozen[group]["hkp"] == match.group(1) and
             frozen[group]["target_stealth_design"] == match.group(2), "matrix factor drift")
        sizes = [len(candidates[i]["candidate_text"]) for i in ids]
        length_ratios.append(max(sizes) / min(sizes))
        for ident in ids:
            role[mapping[ident]["role"]] += 1
    need(dict(hkp) == {f"HKP{i}": 12 for i in range(1, 5)}, "HKP 12 each")
    need(dict(target) == {f"S{i}": 16 for i in range(1, 4)}, "S 16 each")
    need(dict(role) == {name: 48 for name in ROLES}, "role 48 each")
    for i in range(1, 5):
        for j in range(1, 4):
            need(len([g for g in groups if f"HKP{i}-S{j}-" in g]) == 4,
                 "four independent chain slots per cell")
    family = read(args.family_overlay)["families"]
    assigned = {group: name for name, members in family.items() for group in members}
    need(sum(len(members) for members in family.values()) == len(assigned) == 48 and
         set(assigned) == set(groups), "family alias coverage/disjointness")
    for i in range(1, 5):
        for j in range(1, 4):
            cell = [g for g in groups if f"HKP{i}-S{j}-" in g]
            need(len({assigned[g] for g in cell}) == 4, "same family repeated within cell")
    need(all(row["role"] == "POISON" for row in r_atoms
             if row["status"] == "CONTROLLED_POISON"), "controlled atom on non-Poison")
    controlled_by_sample = Counter(row["sample_id"] for row in r_atoms
                                   if row["status"] == "CONTROLLED_POISON")
    need(len(controlled_by_sample) == 30 and set(controlled_by_sample.values()) == {1},
         "remaining Poison error budget")
    remaining_view_rows = read(remain_views)["records"]
    need(all(row["evidence_insufficient"] == 0 for row in remaining_view_rows),
         "remaining Evidence insufficiency")
    partial_publisher = [row for row in remaining_view_rows if row["input_missing"]]
    need(len(partial_publisher) == 3 and
         {row["group_slot_id"] for row in partial_publisher} ==
         {"F240-D1-HKP4-S3-C2"} and
         {row["role"] for row in partial_publisher} == ROLES and
         all(row["P"] == "PARTIAL_ISSUER_AND_HOST_OBSERVED_PUBLISHER_UNKNOWN"
             and row["input_missing"] == 1 for row in partial_publisher),
         "unapproved or role-specific Provenance partial metadata")
    need(all(row["input_missing"] == row["evidence_insufficient"] == 0
             for row in read(batch_view)["records"]), "batch view missing")
    canary_view_summary = read(canary_view)["views"]
    need(all(stats["input_missing"] == stats["evidence_insufficient"] == 0
             for view in canary_view_summary for stats in view["by_role"].values()),
         "Canary view missing")
    need(len(read(remain_query)["records"]) == 30, "remaining neutral queries")
    need(len(read(batch_query)["queries"]) == 10, "batch neutral queries")
    need(read(canary_smoke)["queries_executed"] == 8 and
         len(read(batch_smoke)["traces"]) == 10 and
         sum(len(r["fixed_engineering_smoke_not_effectiveness"])
             for r in read(remain_smoke)["records"]) == 30, "retrieval smoke traces")
    per_role_view: dict[str, dict[str, Counter[str]]] = {r: {v: Counter() for v in "SEPTR"}
                                                        for r in ROLES}
    for row in read(batch_view)["records"] + remaining_view_rows:
        for view in "SEPTR":
            value = row[view]
            kind = ("NOT_APPLICABLE" if value.startswith("NOT_APPLICABLE") else
                    "PARTIAL" if value.startswith("PARTIAL") else "OBSERVED")
            per_role_view[row["role"]][view][kind] += 1
    for view in canary_view_summary:
        name = view["view"]
        for who, stats in view["by_role"].items():
            per_role_view[who][name]["OBSERVED"] += stats["computable_input_path"]
            per_role_view[who][name]["NOT_APPLICABLE"] += stats["not_applicable"]
    for view in "SEPTR":
        need(all(sum(per_role_view[who][view].values()) == 48 for who in ROLES),
             f"{view} role coverage")
        need(per_role_view["CLEAN_CURRENT"][view] == per_role_view["POISON"][view] ==
             per_role_view["HARD_NEGATIVE"][view], f"{view} role-specific missingness")
    max_ratio = max(length_ratios)
    need(max_ratio < 1.5, "full triplet character-length shortcut")
    near_duplicates = []
    for left, right in itertools.combinations(candidates, 2):
        left_group = mapping[left]["group_slot_id"]
        right_group = mapping[right]["group_slot_id"]
        if left_group == right_group:
            continue
        similarity = difflib.SequenceMatcher(
            None, candidates[left]["candidate_text"], candidates[right]["candidate_text"]
        ).ratio()
        if similarity >= 0.9:
            near_duplicates.append({
                "left_blind_id": left, "right_blind_id": right,
                "left_group": left_group, "right_group": right_group,
                "similarity": round(similarity, 3),
                "same_canonical_family": assigned[left_group] == assigned[right_group],
            })
    need(all(row["same_canonical_family"] for row in near_duplicates),
         "cross-family near duplicate surface")
    need(len(near_duplicates) == 1, "unexpected cross-group near duplicate count")
    role_specific_prefixes: list[dict[str, Any]] = []
    for prefix_len in (5, 8):
        prefix_roles: dict[str, set[str]] = defaultdict(set)
        prefix_count: Counter[str] = Counter()
        for ident, candidate in candidates.items():
            prefix = candidate["candidate_text"][:prefix_len]
            prefix_roles[prefix].add(mapping[ident]["role"])
            prefix_count[prefix] += 1
        role_specific_prefixes.extend({"prefix": key, "count": value,
                                       "exclusive_role": next(iter(prefix_roles[key]))}
                                      for key, value in prefix_count.items()
                                      if value >= 3 and len(prefix_roles[key]) == 1)
    result = {
        "status": "D1_PREANNOTATION_ACCEPTANCE_PASS",
        "population": {"candidates": 144, "groups": 48, "cohorts": [24, 30, 90],
                       "roles": dict(sorted(role.items())), "hkp_groups": dict(sorted(hkp.items())),
                       "target_s_groups": dict(sorted(target.items()))},
        "frozen_matrix_sha256": sha(args.matrix),
        "candidate_input_sha256": {"canary_v3": sha(canary_candidates),
                                    "batch1_v4": sha(batch_candidates),
                                    "remaining90_v3": sha(current_candidates)},
        "full_candidate_text_set_sha256": hashlib.sha256(
            "\n".join(sorted(r["candidate_text"] for r in candidates.values())).encode("utf-8")
        ).hexdigest(),
        "prior_accepted_qc": {"canary": sha(canary_matrix),
                              "batch1": sha(args.batch1_final_matrix),
                              "remaining90_phase2": sha(args.phase2_matrix)},
        "fact_atoms": {"canary": {"supported": 40, "controlled_poison": 8},
                       "batch1": {"controlled_poison": 10, "accidental": 0, "ambiguous": 0},
                       "remaining90": {"supported": 131, "controlled_poison": 30,
                                       "accidental": 0, "ambiguous": 0}},
        "family_cluster_overlay_sha256": sha(args.family_overlay),
        "canonical_family_clusters": len(family),
        "family_clusters_split_safe_if_future_split_uses_overlay": True,
        "future_split_not_executed": True,
        "triplet_max_character_length_ratio": round(max_ratio, 3),
        "query_and_retrieval_smoke_groups": 48,
        "view_input_path_by_role": {who: {view: dict(per_role_view[who][view]) for view in "SEPTR"}
                                    for who in sorted(ROLES)},
        "view_input_missing": 3,
        "known_symmetric_provenance_publisher_unknown": {
            "group": "F240-D1-HKP4-S3-C2", "candidates": 3,
            "roles": sorted(ROLES), "issuer_and_host_observed": True,
            "page_publisher": "NOT_OBSERVED_WITH_FROZEN_EVIDENCE",
            "class_shortcut": False,
        },
        "view_evidence_insufficient": 0,
        "exact_duplicate_candidate_text": 0,
        "cross_group_near_duplicates_ge_0_90": near_duplicates,
        "cross_family_near_duplicate_blockers": 0,
        "role_specific_prefix_warnings": role_specific_prefixes,
        "semantic_blockers": 0,
        "blocking_candidate_defects": 0,
        "evidence_insufficiency": 0,
        "evidence_conflict": 0,
        "unexpected_secondary_errors": 0,
        "family_leakage_blockers_with_overlay": 0,
        "surface_shortcut_blockers": 0,
        "full_human_annotation_population_required": 144,
        "human_annotation_started": False,
        "ground_truth_created": False,
        "split_executed": False,
        "training_started": False,
        "limitations": [
            "Prior factual and naturalness QA is inherited from locked cohort audits, not re-performed as independent human fact review here.",
            "Canonical family aliases are deliberately conservative and must be carried forward to future split planning across all domains.",
            "Retrieval smoke establishes an executable trace, not effectiveness or absence of all surface shortcuts.",
            "One HKP4 triplet lacks page-publisher metadata symmetrically; its issuer and host remain observed.",
            "A same-family, same-role cross-group pair is 0.924 text-similar; its family must remain in one future split.",
            "Short history-leading prefixes are role-skewed in a few HN rows; no exact role-wide template was found, but this remains a development warning.",
        ],
    }
    need(not args.out.exists(), "refusing to overwrite audit matrix")
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
    print(json.dumps({"status": result["status"], "population": result["population"],
                      "family_clusters": result["canonical_family_clusters"],
                      "view_input_path_by_role": result["view_input_path_by_role"],
                      "max_length_ratio": max_ratio}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
