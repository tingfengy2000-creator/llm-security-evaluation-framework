"""POST_SEAL_EVALUATOR: join only approved old evaluator rows after the role-free lock."""
import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from llmguard.domains.retrieval.hidden_poisoning.chinese5060.readonly_analysis import VerifiedReader, flip_key


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--allowlist", type=Path, required=True)
    parser.add_argument("--role-free", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    lock = json.loads((args.role_free / "ROLE_FREE_OUTPUT_LOCK.json").read_bytes())
    if lock["status"] != "COMPLETE_36_ROLE_FREE_FEATURES":
        raise ValueError("ROLE_FREE_COMPLETE_LOCK_REQUIRED")
    for r in lock["records"]:
        if hashlib.sha256((args.role_free / r["path"]).read_bytes()).hexdigest() != r["sha256"]:
            raise ValueError("ROLE_FREE_LOCK_CHANGED")
    features = json.loads((args.role_free / "ROLE_FREE_FEATURES_PRIVATE.json").read_bytes())
    reader = VerifiedReader(args.root, json.loads(args.allowlist.read_bytes()))
    pair_key = next(p for p in reader.allow if p.endswith("PAIR_EVALUATOR_ROWS_PRIVATE.json"))
    old = reader.json(pair_key)
    by_method = {m: {r["world_id"]: r for r in old if r["method"] == m} for m in ("B1", "B2")}
    full = {r: Counter({"00": 0, "01": 0, "10": 0, "11": 0}) for r in ("POISON", "CLEAN_CURRENT", "HARD_NEGATIVE")}
    conditional = {r: Counter({"00": 0, "01": 0, "10": 0, "11": 0}) for r in full}
    miss: Counter[str] = Counter()
    private_rows = []
    tie_cross: Counter[str] = Counter()
    flip_contexts: Counter[str] = Counter()
    removed_counts: dict[str, Counter[str]] = {m: Counter() for m in ("B1", "B2")}
    residuals: dict[str, Counter[str]] = {m: Counter() for m in ("B1", "B2")}
    for f in features:
        wid = f["world_id"]
        a, b = by_method["B1"][wid], by_method["B2"][wid]
        if a["role"] != b["role"] or a["retrieved_candidate_indices"] != b["retrieved_candidate_indices"]:
            raise ValueError("PAIRED_EVALUATOR_BINDING_DRIFT")
        role = a["role"]
        indices = set(a["retrieved_candidate_indices"])
        flags = {}
        for method, old_row in (("B1", a), ("B2", b)):
            trace = f[method]
            deleted = set(trace["removed_indices"])
            flagged = bool(deleted & indices)
            entire = bool(indices) and indices <= deleted
            if (flagged != old_row["candidate_any_removed"] or entire != old_row["candidate_all_retrieved_removed"]
                    or sorted(deleted) != old_row["removed_indices"] or len(indices-deleted) != old_row["candidate_chunks_remaining"]):
                raise ValueError("OLD_EVALUATION_NOT_REPRODUCED")
            flags[method] = flagged
            removed_counts[method][role] += flagged
            residuals[method][role] += len(indices-deleted)
            if len(indices) > 1 or (flagged and not entire) != old_row["partial_with_residual"]:
                raise ValueError("CANDIDATE_CHUNK_SCOPE_DRIFT")
            candidate_boundary = bool(indices & set(trace["cutoff_tie_group"])) and trace["boundary_tie"]
            reason = ("CUTOFF_TIE_SELECTED" if flagged else "CUTOFF_TIE_RETAINED") if candidate_boundary else (
                "SAVED_SCORE_SELECTED" if flagged else "SAVED_SCORE_RETAINED")
            if not indices:
                reason = "RETRIEVAL_MISS_NOT_FILTER_DECISION"
            tie_cross[f'{method}|{role}|present={int(bool(indices))}|flag={int(flagged)}|any_tie={int(trace["any_score_tie"])}|boundary={int(trace["boundary_tie"])}|candidate_boundary={int(candidate_boundary)}'] += 1
            private_rows.append({"world_id": wid, "method": method, "role": role, "candidate_indices": sorted(indices),
                "candidate_flag": flagged, "all_retrieved_removed": entire, "partial": flagged and not entire,
                "remaining": len(indices-deleted), "observed_rule_category": reason,
                "stage1_count_correctness": "UNIDENTIFIABLE_BACKGROUND_GT_ABSENT", "source_status": "SOURCE_UNVERIFIED",
                "HN_historical_expiry_condition_consistency": "NEEDS_INDEPENDENT_ADJUDICATION" if role == "HARD_NEGATIVE" else "NOT_ASSESSED",
                "target": "UNKNOWN_NOT_INFERRED", "evidence_refs": f["evidence_refs"]})
        cell = flip_key(flags["B1"], flags["B2"])
        full[role][cell] += 1
        if indices:
            conditional[role][cell] += 1
        else:
            miss[role] += 1
        if flags["B1"] != flags["B2"]:
            flip_contexts[f'{role}|n_adv_changed={int(f["n_adv_changed"])}|B1_boundary={int(f["B1"]["boundary_tie"])}|B2_boundary={int(f["B2"]["boundary_tie"])}|B1_any_tie={int(f["B1"]["any_score_tie"])}|B2_any_tie={int(f["B2"]["any_score_tie"])}'] += 1
    assert {r: sum(c.values()) for r, c in full.items()} == {r: 12 for r in full}
    assert sum(sum(c.values()) for c in conditional.values()) == 29
    assert removed_counts["B1"] == {"POISON": 1, "CLEAN_CURRENT": 1, "HARD_NEGATIVE": 2}
    assert removed_counts["B2"] == {"POISON": 2, "CLEAN_CURRENT": 4, "HARD_NEGATIVE": 2}
    args.output.mkdir(exist_ok=False)
    def write(name, value):
        (args.output / name).write_bytes((json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode())
    write("EVALUATOR_CASES_PRIVATE.json", private_rows)
    write("PAIR_FLIP_AGGREGATE.json", {"cell_definition": "B1_flag_then_B2_flag", "full": full, "conditional": conditional,
        "misses": miss, "any_equals_all_retrieved": True, "partial": 0, "remaining_candidate_chunks": residuals,
        "recomputed_removed_counts": removed_counts, "basis": "LOCAL_PRIVATE_EVIDENCE_VERIFIED_NOT_NEW_EXPERIMENT"})
    write("TIE_ASSOCIATION_SUMMARY.json", {"cross_table": tie_cross, "candidate_flip_contexts": flip_contexts,
        "causality": "NOT_IDENTIFIED_NO_COUNTERFACTUAL_OR_RERUN", "do_not_treat_all_ties_as_cutoff_ties": True})
    write("EVALUATOR_ACCESS_LOG.json", reader.events)
    print(json.dumps({"full": full, "conditional": conditional, "misses": miss, "flip_contexts": flip_contexts}))


if __name__ == "__main__":
    main()
