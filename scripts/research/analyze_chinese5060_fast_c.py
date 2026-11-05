"""ROLE_FREE_ANALYST: pure statistics of immutable profiles; never open labels."""
import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from llmguard.domains.retrieval.hidden_poisoning.chinese5060.readonly_analysis import VerifiedReader, stage_features


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--allowlist", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    allow = json.loads(args.allowlist.read_bytes())
    reader = VerifiedReader(args.root, allow)
    args.output.mkdir(exist_ok=False)
    methods = {}
    for method in ("B1", "B2"):
        key = next(p for p in allow if p.endswith(method + "_RESULTS_PRIVATE.json"))
        raw = reader.json(key)
        if len(raw) != 36 or len({r["world_id"] for r in raw}) != 36:
            raise ValueError("ALL_36_REQUIRED")
        methods[method] = {r["world_id"]: stage_features(r) for r in raw}
    if set(methods["B1"]) != set(methods["B2"]):
        raise ValueError("PAIRED_WORLD_IDENTITY_MISMATCH")
    paired = []
    for wid in sorted(methods["B1"]):
        a, b = methods["B1"][wid], methods["B2"][wid]
        paired.append({"world_id": wid, "B1": a, "B2": b,
            "n_adv_changed": a["n_adv"] != b["n_adv"], "n_tfidf_changed": a["n_tfidf"] != b["n_tfidf"],
            "removed_indices_changed": a["removed_indices"] != b["removed_indices"],
            "evidence_refs": [{"path": p, "sha256": h, "field": "observations.n_adv/n_tfidf/frequency_scores; removed_indices",
                               "confidence": "DIRECT_SAVED_TRACE"} for p, h in allow.items()]})
    coverage = {method: {field: sum(r["coverage"][field] for r in rows.values())
                         for field in next(iter(rows.values()))["coverage"]} for method, rows in methods.items()}
    stats = {method: {"any_score_tie": sum(r["any_score_tie"] for r in rows.values()),
        "boundary_tie": sum(r["boundary_tie"] for r in rows.values()),
        "saved_selection_recomputed": sum(r["stage2_status"] == "SAVED_SELECTION_RECOMPUTED_EXACTLY" for r in rows.values())}
        for method, rows in methods.items()}
    summary = {"worlds": 36, "role_free": True, "trace_coverage": coverage, "tie_counts": stats,
        "n_adv_changed": sum(r["n_adv_changed"] for r in paired), "n_tfidf_changed": sum(r["n_tfidf_changed"] for r in paired),
        "removed_indices_changed": sum(r["removed_indices_changed"] for r in paired),
        "stage1_and_selection_change_table": dict(Counter(f'{int(r["n_adv_changed"])}{int(r["removed_indices_changed"])}' for r in paired)),
        "model_inference_calls": 0, "new_API_calls": 0}
    def write(name, value):
        p = args.output / name
        p.write_bytes((json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode())
        return {"path": name, "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
    records = [write("ROLE_FREE_FEATURES_PRIVATE.json", paired), write("ROLE_FREE_SUMMARY.json", summary),
               write("ROLE_FREE_ACCESS_LOG.json", reader.events)]
    write("ROLE_FREE_OUTPUT_LOCK.json", {"status": "COMPLETE_36_ROLE_FREE_FEATURES", "records": records})
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
