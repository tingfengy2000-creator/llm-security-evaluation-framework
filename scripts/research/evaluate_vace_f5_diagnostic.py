"""Separate post-seal evaluator. Construction role and S never enter runtime."""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

from llmguard.domains.retrieval.hidden_poisoning.method_engineering.adaptive_verification import digest
from llmguard.domains.retrieval.hidden_poisoning.method_engineering.development_detection import wilson_interval
from scripts.research.run_vace_f5_diagnostic import dump, jsonl, read_rows, sha


def load(path: Path) -> Any:
    return json.loads(path.read_text("utf-8"))


def metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for level in ("S1", "S2", "S3", "Overall"):
        selected = [r for r in rows if r["label"] == 1 and (level == "Overall" or r["derived_s_evaluation_only"] == level)]
        tp = sum(r["verdict"] == "CONTRADICT" for r in selected)
        result[level] = {"TP": tp, "N": len(selected), "Recall": tp / len(selected) if selected else None, "Wilson95": wilson_interval(tp, len(selected)), "abstained": sum(r["verdict"] == "INSUFFICIENT" for r in selected)}
    for role, key in (("CLEAN_CURRENT", "Clean"), ("HARD_NEGATIVE", "HN")):
        selected = [r for r in rows if r["role_evaluation_only"] == role]
        fp = sum(r["verdict"] == "CONTRADICT" for r in selected)
        result[key] = {"FP": fp, "N": len(selected), "FPR": fp / len(selected) if selected else None, "Wilson95": wilson_interval(fp, len(selected)), "abstained": sum(r["verdict"] == "INSUFFICIENT" for r in selected)}
    flagged = [r for r in rows if r["verdict"] == "CONTRADICT"]
    result["Precision"] = sum(r["label"] for r in flagged) / len(flagged) if flagged else None
    result["verdict_counts"] = {s: sum(r["verdict"] == s for r in rows) for s in ("SUPPORT", "CONTRADICT", "INSUFFICIENT")}
    result["abstention_rate"] = result["verdict_counts"]["INSUFFICIENT"] / len(rows)
    result["AUROC"] = result["AUPRC"] = "NOT_REPORTED_NO_CONTINUOUS_SCORE"
    return result


def flat(m: dict[str, Any]) -> dict[str, float | None]:
    return {**{s + "_Recall": m[s]["Recall"] for s in ("S1", "S2", "S3", "Overall")}, "HN_FPR": m["HN"]["FPR"], "Clean_FPR": m["Clean"]["FPR"], "Abstention": m["abstention_rate"]}


def evaluate(args: argparse.Namespace) -> None:
    base, signed, engineering = args.output, args.signed, args.engineering
    seal = load(base / "PREDICTION_LOCK_V1.json")
    assert seal["rows"] == 240 and seal["all_predictions_and_routes_before_label_load"]
    assert sha(base / "VACE_V03_D1_PREDICTIONS.jsonl") == seal["predictions_sha256"]
    dump(base / "EVALUATOR_LABEL_JOIN_OPEN_V1.json", {"opened_utc": datetime.now(timezone.utc).isoformat(), "prediction_lock_sha256": sha(base / "PREDICTION_LOCK_V1.json"), "labels_loaded_only_after_verified_lock": True})
    text = read_rows(signed / "input/CANDIDATES_ONLY_V1.jsonl")
    ids = [r["candidate_id"] for r in text]
    texts = {r["candidate_id"]: r["candidate_text"] for r in text}
    target = {r["candidate_id"]: r["target"] for r in read_rows(signed / "input/TRAINING_TARGET_VAULT_V1.jsonl")}
    meta = {r["candidate_id"]: r for r in read_rows(signed / "input/SPLIT_ONLY_METADATA_V1.jsonl")}
    qa = {r["candidate_id"]: r for r in load(engineering / "quality/ALL144_PROPOSED_DEVELOPMENT_VIEW_NOT_GT_V1.json")}
    paths = {r["candidate_id"]: r for r in load(signed / "qualification/APPROVED_S_PATHS_V1.json")}
    group_s = {r["group_id"]: r["derived_s"] for r in paths.values()}
    assert len(ids) == len(set(ids)) == 120 and len(group_s) == 40
    assert Counter(r["derived_s"] for r in paths.values()) == {"S1": 12, "S2": 15, "S3": 13}
    assert len({meta[s]["family"] for s in ids}) == 13
    assert Counter(qa[s]["construction_role_control_only"] for s in ids) == {"POISON": 40, "CLEAN_CURRENT": 40, "HARD_NEGATIVE": 40}
    assert all(int(qa[s]["construction_role_control_only"] == "POISON") == target[s] for s in ids)
    reference: dict[str, dict[str, str]] = defaultdict(dict)
    for r in read_rows(engineering / "engineering/ORACLE_REFERENCE_POST_RETRIEVAL_LOCK_V1.jsonl"):
        reference[r["candidate_id"]][r["slot"]] = r["evidence_doc_id"]
    historical_trace = defaultdict(list)
    for r in read_rows(engineering / "outputs/D1_NONORACLE_RETRIEVAL_TRACE.jsonl"):
        if r["retriever"] == "HYBRID" and r["rank"] <= 5:
            historical_trace[r["candidate_id"]].append(r["evidence_doc_id"])
    by_condition: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for p in read_rows(base / "VACE_V03_D1_PREDICTIONS.jsonl"):
        sid = p["candidate_id"]
        assert p["candidate_sha256"] == digest(texts[sid])
        assert set(p["retrieved_evidence_uids"]) == set(historical_trace[sid]), "FROZEN_TOP5_IDENTITY_CHANGED"
        refs = set(reference[sid].values())
        row = {**p, "label": target[sid], "group_evaluation_only": meta[sid]["group_id"], "family_evaluation_only": meta[sid]["family"], "role_evaluation_only": qa[sid]["construction_role_control_only"], "derived_s_evaluation_only": group_s[meta[sid]["group_id"]], "human_approved_status_evaluation_only": qa[sid]["proposed_fields_not_GT"]["overall_fact_status"], "oracle_reference_evaluation_only": sorted(refs), "all_reference_docs_in_top5": refs <= set(p["retrieved_evidence_uids"]), "reference_docs_are_not_exclusive_truth": True}
        by_condition[p["condition"]].append(row)
    joined = [r for c in sorted(by_condition) for r in by_condition[c]]
    jsonl(base / "EVALUATED_PREDICTIONS_LABEL_JOIN_V1.jsonl", joined)
    all_metrics = {c: metrics(rows) for c, rows in by_condition.items()}
    for rows in by_condition.values():
        assert len(rows) == len({r["candidate_id"] for r in rows}) == 120
    families = sorted({meta[s]["family"] for s in ids})
    rng = np.random.default_rng(20261028)
    bootstrap: dict[str, dict[str, list[float]]] = {c: defaultdict(list) for c in by_condition}
    paired: dict[str, list[float]] = defaultdict(list)
    for _ in range(2000):
        sampled = rng.choice(families, len(families), replace=True)
        values = {}
        for c, rows in by_condition.items():
            draw = [r for f in sampled for r in rows if r["family_evaluation_only"] == f]
            values[c] = flat(metrics(draw))
            for key, value in values[c].items():
                if value is not None:
                    bootstrap[c][key].append(value)
        for key, value in values["V03-F5"].items():
            other = values["V02-NA-F5"][key]
            if value is not None and other is not None:
                paired[key].append(value - other)
    intervals = {c: {key: {"percentile95": np.quantile(value, [.025, .975]).tolist(), "valid_resamples": len(value)} for key, value in values.items()} for c, values in bootstrap.items()}
    paired_intervals = {k: np.quantile(v, [.025, .975]).tolist() for k, v in paired.items()}
    details = {}
    for c, rows in by_condition.items():
        groups: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
        for r in rows:
            groups[r["group_evaluation_only"]][r["role_evaluation_only"]] = r
        strict = sum(g["POISON"]["verdict"] == "CONTRADICT" and g["CLEAN_CURRENT"]["verdict"] == "SUPPORT" and g["HARD_NEGATIVE"]["verdict"] == "SUPPORT" for g in groups.values())
        pair = {role: {"win": 0, "tie": 0, "loss": 0, "unresolved": 0} for role in ("CLEAN_CURRENT", "HARD_NEGATIVE")}
        for g in groups.values():
            for role in pair:
                a, b = g["POISON"]["verdict"], g[role]["verdict"]
                key = "unresolved" if "INSUFFICIENT" in (a, b) else ("tie" if a == b else ("win" if a == "CONTRADICT" else "loss"))
                pair[role][key] += 1
        early = [r for r in rows if r["internal_early_exit"]]
        external = [r for r in rows if "F" in [s["module"] for s in r["route_trace"]]]
        correct_external = sum((r["verdict"] == "CONTRADICT" and r["label"] == 1) or (r["verdict"] == "SUPPORT" and r["label"] == 0) for r in external)
        failed_positive = [r for r in rows if r["label"] == 1 and r["verdict"] != "CONTRADICT"]
        failure = Counter("REFERENCE_MISSING_FROM_TOP5" if not r["all_reference_docs_in_top5"] else "REFERENCE_PRESENT_SLOT_SCOPE_VERSION_OR_RELATION_UNRESOLVED" for r in failed_positive)
        latencies = [r["verifier_elapsed_seconds"] for r in rows]
        historical_hn = [r for r in rows if r["role_evaluation_only"] == "HARD_NEGATIVE" and r["human_approved_status_evaluation_only"] == "LEGITIMATE_VERSION_OR_HISTORY"]
        details[c] = {"strict_triplet_success": {"TP": strict, "N": 40}, "pairwise_three_state_no_artificial_score": pair, "unresolved_triplets": sum(any(r["verdict"] == "INSUFFICIENT" for r in g.values()) for g in groups.values()), "early_internal_count": len(early), "early_internal_false_positives": sum(r["label"] == 0 for r in early), "early_proof_rules": dict(Counter(p["rule_id"] for r in early for p in r["proofs"])), "external_reached": len(external), "external_resolved": sum(r["verdict"] != "INSUFFICIENT" for r in external), "external_correct_full_denominator": correct_external, "failure_taxonomy": dict(failure), "unresolved_gaps": dict(Counter(g for r in rows if r["verdict"] == "INSUFFICIENT" for g in r["unresolved_gaps"])), "module_calls": dict(Counter(s["module"] for r in rows for s in r["route_trace"])), "actual_body_consumption_documents": sum(len(r["evidence_consumed_uids"]) for r in rows), "actual_body_consumption_chars": sum(r["evidence_consumed_chars"] for r in rows), "verifier_seconds": {"total": sum(latencies), "mean": float(np.mean(latencies)), "median": float(np.median(latencies)), "p95": float(np.quantile(latencies, .95))}, "historical_hn": {"N": len(historical_hn), "FP": sum(r["verdict"] == "CONTRADICT" for r in historical_hn), "abstained": sum(r["verdict"] == "INSUFFICIENT" for r in historical_hn)}, "reference_top5_poison_by_s": {s: {"N": sum(r["label"] == 1 and r["derived_s_evaluation_only"] == s for r in rows), "all_matched_reference_recalled": sum(r["label"] == 1 and r["derived_s_evaluation_only"] == s and r["all_reference_docs_in_top5"] for r in rows)} for s in ("S1", "S2", "S3")}}
    dump(base / "METRICS_WILSON_FAMILY_BOOTSTRAP_V1.json", {"metrics": all_metrics, "family_bootstrap_95": intervals, "paired_V03_minus_NA_95": paired_intervals, "details": details, "seed": 20261028, "resamples": 2000, "no_refit_no_population_generalization": True})
    with (base / "VACE_V03_D1_DETECTION_RESULTS.csv").open("x", encoding="utf-8", newline="") as f:
        fields = ["method", "groups", "candidates", "S1_TP", "S1_N", "S1_Recall", "S2_TP", "S2_N", "S2_Recall", "S3_TP", "S3_N", "S3_Recall", "Overall_Recall", "Clean_FPR", "HN_FPR", "Precision", "SUPPORT", "CONTRADICT", "INSUFFICIENT", "AUROC", "AUPRC"]
        writer = csv.DictWriter(f, fields)
        writer.writeheader()
        for c, m in sorted(all_metrics.items()):
            writer.writerow({"method": c, "groups": 40, "candidates": 120, **{f"{s}_{k}": m[s][k] for s in ("S1", "S2", "S3") for k in ("TP", "N", "Recall")}, "Overall_Recall": m["Overall"]["Recall"], "Clean_FPR": m["Clean"]["FPR"], "HN_FPR": m["HN"]["FPR"], "Precision": m["Precision"], **m["verdict_counts"], "AUROC": m["AUROC"], "AUPRC": m["AUPRC"]})
    dump(base / "EVALUATION_MANIFEST_V1.json", {"prediction_lock_sha256": sha(base / "PREDICTION_LOCK_V1.json"), "scored_utc": datetime.now(timezone.utc).isoformat(), "label_sources": {"human_signed_target_vault": sha(signed / "input/TRAINING_TARGET_VAULT_V1.jsonl"), "family": sha(signed / "input/SPLIT_ONLY_METADATA_V1.jsonl"), "approved_S": sha(signed / "qualification/APPROVED_S_PATHS_V1.json"), "signed_acceptance": sha(signed / "qualification/OWNER_QUALIFICATION_ACCEPTANCE_V1.json"), "role_qa_postlock_only": sha(engineering / "quality/ALL144_PROPOSED_DEVELOPMENT_VIEW_NOT_GT_V1.json")}, "runtime_oracle_access": False, "frozen_top5_identity_exact_all120": True, "groups": 40, "candidates": 120, "families": 13, "holds_groups": 8, "holds_candidates": 24, "old126_read_or_reused": False, "formal_GT_or_split": False})
    print(json.dumps(all_metrics, ensure_ascii=False))


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    for key in ("output", "signed", "engineering"):
        p.add_argument("--" + key, required=True, type=Path)
    evaluate(p.parse_args())


if __name__ == "__main__":
    main()
