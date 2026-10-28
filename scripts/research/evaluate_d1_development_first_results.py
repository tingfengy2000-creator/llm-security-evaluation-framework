"""Post-lock D1 development evaluation; never a formal benchmark evaluator.

Human-approved targets determine binary truth. Construction roles are joined
only here, after the new prediction seal, for Clean/HN evaluation strata.
"""
# mypy: disable-error-code=import-untyped
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import joblib
import numpy as np
from sklearn.metrics import average_precision_score, roc_auc_score

from llmguard.domains.retrieval.hidden_poisoning.method_engineering.development_detection import (
    family_folds,
    wilson_interval,
)
from scripts.research.run_d1_development_first_results import text_pipeline


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def lines(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def new(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write("\n")


def jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, allow_nan=False) + "\n")


def manual_auc_ap(y: np.ndarray, score: np.ndarray) -> tuple[float, float]:
    positive, negative = score[y == 1], score[y == 0]
    delta = positive[:, None] - negative[None, :]
    auc = float(((delta > 0).sum() + 0.5 * (delta == 0).sum()) / delta.size)
    # AP uses all items tied at a threshold together, not arbitrary tie ordering.
    ap, previous_tp = 0.0, 0
    for threshold in sorted(set(score.tolist()), reverse=True):
        selected = score >= threshold
        tp = int(y[selected].sum())
        ap += (tp - previous_tp) / len(positive) * tp / int(selected.sum())
        previous_tp = tp
    return auc, ap


def metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    y = np.asarray([row["binary_target"] for row in rows])
    scores = np.asarray([row["raw_decision_score"] for row in rows])
    pred = np.asarray([row["predicted_class"] for row in rows])
    result: dict[str, Any] = {}
    for level in ("S1", "S2", "S3", "Overall"):
        selected = np.asarray([row["binary_target"] == 1 and (level == "Overall" or row["derived_s"] == level) for row in rows])
        n, tp = int(selected.sum()), int(pred[selected].sum())
        result[level] = {"TP": tp, "N": n, "Recall": tp / n if n else None, "Wilson95": wilson_interval(tp, n)}
    for role, key in (("CLEAN_CURRENT", "Clean"), ("HARD_NEGATIVE", "HN")):
        selected = np.asarray([row["construction_role_evaluation_only"] == role for row in rows])
        n, fp = int(selected.sum()), int(pred[selected].sum())
        result[key] = {"FP": fp, "N": n, "FPR": fp / n if n else None, "Wilson95": wilson_interval(fp, n)}
    result["AUROC"] = float(roc_auc_score(y, scores)) if len(set(y)) == 2 else None
    result["AUPRC"] = float(average_precision_score(y, scores)) if y.sum() else None
    return result


def flat(m: dict[str, Any]) -> dict[str, float | None]:
    return {**{f"{key}_Recall": m[key]["Recall"] for key in ("S1", "S2", "S3", "Overall")},
            "Clean_FPR": m["Clean"]["FPR"], "HN_FPR": m["HN"]["FPR"],
            "AUROC": m["AUROC"], "AUPRC": m["AUPRC"]}


def permutation_control(base: Path, config: dict[str, Any]) -> dict[str, Any]:
    text = lines(base / "input/CANDIDATES_ONLY_V1.jsonl")
    meta = lines(base / "input/SPLIT_ONLY_METADATA_V1.jsonl")
    ids = [row["candidate_id"] for row in text]
    assert ids == [row["candidate_id"] for row in meta]
    groups: dict[str, list[int]] = defaultdict(list)
    for i, row in enumerate(meta):
        groups[row["group_id"]].append(i)
    rng = np.random.default_rng(config["permutation_control"]["seed"])
    shuffled = np.zeros(len(ids), dtype=int)
    for group in sorted(groups):
        assert len(groups[group]) == 3
        shuffled[int(rng.choice(groups[group]))] = 1
    scores, probabilities = np.full(len(ids), np.nan), np.full(len(ids), np.nan)
    models = []
    for fold in family_folds([r["family"] for r in meta], [r["group_id"] for r in meta]):
        model = text_pipeline(config)
        train, validation = list(fold.train), list(fold.validation)
        model.fit([text[i]["candidate_text"] for i in train], shuffled[train])
        scores[validation] = model.decision_function([text[i]["candidate_text"] for i in validation])
        probabilities[validation] = model.predict_proba([text[i]["candidate_text"] for i in validation])[:, 1]
        path = base / "models" / f"PERMUTATION_A_{fold.family}.joblib"
        assert not path.exists()
        joblib.dump(model, path, compress=3)
        models.append({"path": str(path.relative_to(base)), "sha256": sha(path)})
    assert np.isfinite(scores).all()
    jsonl(base / "PERMUTATION_CONTROL_PREDICTIONS_V1.jsonl", [
        {"candidate_id": sid, "fold": meta[i]["family"], "permuted_target": int(shuffled[i]),
         "raw_score": float(scores[i]), "uncalibrated_probability": float(probabilities[i])}
        for i, sid in enumerate(ids)
    ])
    auc, ap = manual_auc_ap(shuffled, scores)
    assert abs(auc - roc_auc_score(shuffled, scores)) < 1e-12
    assert abs(ap - average_precision_score(shuffled, scores)) < 1e-12
    return {"AUROC": auc, "AUPRC": ap, "random_AP_prevalence": 1 / 3,
            "seed": config["permutation_control"]["seed"], "positive": 40,
            "negative": 80, "models": models,
            "one_fixed_control_not_a_permutation_p_value": True}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--engineering-root", type=Path, required=True)
    args = parser.parse_args()
    base, prior = args.run_root.resolve(), args.engineering_root.resolve()
    seal = load(base / "PREDICTION_LOCK_V1.json")
    assert sha(base / "PREDICTIONS_LABEL_BLIND_LOCKED_V1.jsonl") == seal["prediction_sha256"]
    assert seal["rows"] == 480
    assert all(value["status"] == "EXECUTED" for value in seal["execution"].values())
    config = load(base / "CONFIG_FREEZE_V1.json")
    # No evaluation roles, S or Oracle reference loaded until the prediction seal was verified.
    new(base / "EVALUATION_ROLE_JOIN_OPEN_V1.json", {
        "prediction_lock_sha256": sha(base / "PREDICTION_LOCK_V1.json"),
        "opened_utc": datetime.now(timezone.utc).isoformat(), "after_lock_verified": True,
        "evaluation_script_sha256": sha(Path(__file__)),
    })
    qa_path = prior / "quality/ALL144_PROPOSED_DEVELOPMENT_VIEW_NOT_GT_V1.json"
    qa = {r["candidate_id"]: r for r in load(qa_path)}
    texts = lines(base / "input/CANDIDATES_ONLY_V1.jsonl")
    ids = [r["candidate_id"] for r in texts]
    target = {r["candidate_id"]: r["target"] for r in lines(base / "input/TRAINING_TARGET_VAULT_V1.jsonl")}
    meta = {r["candidate_id"]: r for r in lines(base / "input/SPLIT_ONLY_METADATA_V1.jsonl")}
    s_paths = {r["candidate_id"]: r for r in load(base / "qualification/APPROVED_S_PATHS_V1.json")}
    group_s = {r["group_id"]: r["derived_s"] for r in s_paths.values()}
    assert len(group_s) == 40
    for r in texts:
        q = qa[r["candidate_id"]]
        assert q["candidate_text"] == r["candidate_text"]
        assert q["group_id"] == meta[r["candidate_id"]]["group_id"]
        assert q["family"] == meta[r["candidate_id"]]["family"]
        assert int(q["construction_role_control_only"] == "POISON") == target[r["candidate_id"]]
    roles = Counter(qa[sid]["construction_role_control_only"] for sid in ids)
    assert roles == {"POISON": 40, "CLEAN_CURRENT": 40, "HARD_NEGATIVE": 40}, roles
    assert Counter(r["derived_s"] for r in s_paths.values()) == {"S1": 12, "S2": 15, "S3": 13}

    retrieval = defaultdict(list)
    for r in lines(prior / "outputs/D1_NONORACLE_RETRIEVAL_TRACE.jsonl"):
        if r["retriever"] == "HYBRID" and r["rank"] <= 5:
            retrieval[r["candidate_id"]].append(r)
    reference: dict[str, dict[str, str]] = defaultdict(dict)
    for r in lines(prior / "engineering/ORACLE_REFERENCE_POST_RETRIEVAL_LOCK_V1.jsonl"):
        reference[r["candidate_id"]][r["slot"]] = r["evidence_doc_id"]
    availability: dict[str, dict[str, list[dict[str, Any]]]] = {}
    for condition in ("NONORACLE", "ORACLE"):
        by_sid = defaultdict(list)
        for r in lines(prior / "engineering" / f"{condition}_SIGNAL_AVAILABILITY_V1.jsonl"):
            by_sid[r["sample_id"]].append(r)
        availability[condition] = by_sid

    predictions = lines(base / "PREDICTIONS_LABEL_BLIND_LOCKED_V1.jsonl")
    joined, by_condition = [], defaultdict(list)
    for p in predictions:
        sid, condition = p["candidate_id"], p["condition"]
        assert sid in meta and p["fold_id"] == meta[sid]["family"]
        assert p["predicted_class"] == int(p["uncalibrated_probability"] >= 0.5)
        assert abs(1 / (1 + np.exp(-p["raw_decision_score"])) - p["uncalibrated_probability"]) < 1e-12
        names = config["conditions"][condition].get("feature_names", [])
        setting = "ORACLE" if condition == "C" else "NONORACLE"
        rows = [r for r in availability[setting][sid] if r["signal_name"] in names]
        row = {**p, "binary_target": target[sid], "group_id_evaluation_only": meta[sid]["group_id"],
               "family_evaluation_only": meta[sid]["family"],
               "construction_role_evaluation_only": qa[sid]["construction_role_control_only"],
               "derived_s": group_s[meta[sid]["group_id"]],
               "derived_s_applies_to_poison_only": target[sid] == 1,
               "approved_overall_status": qa[sid]["proposed_fields_not_GT"]["overall_fact_status"],
               "retrieved_evidence_identity": [] if condition == "A" else (
                   list(reference[sid].values()) if condition == "C" else [r["evidence_doc_id"] for r in sorted(retrieval[sid], key=lambda r: r["rank"]) ]),
               "feature_availability": dict(Counter(r["computation_status"] for r in rows)),
               "feature_schema": config["conditions"][condition].get("contract", "CANDIDATE_ONLY"),
               "input_lock_sha256": sha(base / "INPUT_LOCK_V1.json"),
               "prediction_lock_sha256": sha(base / "PREDICTION_LOCK_V1.json")}
        joined.append(row)
        by_condition[condition].append(row)
    jsonl(base / "D1_MODEL_OOF_PREDICTIONS.jsonl", joined)
    full_metrics: dict[str, Any] = {}
    for condition, rows in by_condition.items():
        assert len(rows) == len({r["candidate_id"] for r in rows}) == 120
        full_metrics[condition] = metrics(rows)
        y = np.asarray([r["binary_target"] for r in rows])
        score = np.asarray([r["raw_decision_score"] for r in rows])
        auc, ap = manual_auc_ap(y, score)
        assert abs(auc - full_metrics[condition]["AUROC"]) < 1e-12
        assert abs(ap - full_metrics[condition]["AUPRC"]) < 1e-12

    families = sorted({meta[sid]["family"] for sid in ids})
    positions = {family: [i for i, sid in enumerate(ids) if meta[sid]["family"] == family] for family in families}
    samples: dict[str, dict[str, list[float]]] = {c: defaultdict(list) for c in by_condition}
    paired: dict[str, list[float]] = defaultdict(list)
    rng = np.random.default_rng(config["uncertainty"]["seed"])
    for _ in range(config["uncertainty"]["family_bootstrap_resamples"]):
        draw = rng.choice(families, size=len(families), replace=True)
        index = [i for family in draw for i in positions[str(family)]]
        resampled = {}
        for condition, rows in by_condition.items():
            assert [r["candidate_id"] for r in rows] == ids
            resampled[condition] = flat(metrics([rows[i] for i in index]))
            for key, value in resampled[condition].items():
                if value is not None:
                    samples[condition][key].append(value)
        for key in resampled["B2"]:
            left, right = resampled["B2"][key], resampled["C"][key]
            if left is not None and right is not None:
                paired[key].append(right - left)
    intervals = {c: {k: {"percentile95": np.quantile(v, [0.025, 0.975]).tolist(), "valid_resamples": len(v)} for k, v in data.items()} for c, data in samples.items()}
    deltas = {}
    for key, values in paired.items():
        left, right = flat(full_metrics["B2"])[key], flat(full_metrics["C"])[key]
        assert left is not None and right is not None
        deltas[key] = {"C_minus_B2": right - left,
                       "paired_family_percentile95": np.quantile(values, [0.025, 0.975]).tolist(),
                       "valid_resamples": len(values)}
    new(base / "D1_METRICS_AND_UNCERTAINTY_V1.json", {"metrics": full_metrics, "family_bootstrap": intervals,
        "Oracle_same_column_contrast": deltas, "family_count": 13, "group_count": 40,
        "candidate_count": 120, "independent_metric_recalculation": "PASS"})
    output = []
    for condition, m in full_metrics.items():
        r = {"method": condition, "status": "EXECUTED", "groups": 40, "candidates": 120,
             "families": 13, "threshold": 0.5, "scope": "D1_DEV_EXPOSED"}
        for level in ("S1", "S2", "S3"):
            for key in ("TP", "N", "Recall"):
                r[f"{level}_{key}"] = m[level][key]
            r[f"{level}_Wilson95_low"], r[f"{level}_Wilson95_high"] = m[level]["Wilson95"]
            r[f"{level}_Clean_N"] = m[level]["N"]
            r[f"{level}_HN_N"] = m[level]["N"]
        r.update({"Overall_Poison_TP": m["Overall"]["TP"], "Overall_Poison_N": 40,
                  "Overall_Recall": m["Overall"]["Recall"], "Clean_FP": m["Clean"]["FP"],
                  "Clean_N": 40, "Clean_FPR": m["Clean"]["FPR"], "HN_FP": m["HN"]["FP"],
                  "HN_N": 40, "HN_FPR": m["HN"]["FPR"], "AUROC": m["AUROC"], "AUPRC": m["AUPRC"]})
        output.append(r)
    with (base / "D1_FIRST_DETECTION_RESULTS.csv").open("x", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(output[0]))
        writer.writeheader()
        writer.writerows(output)

    retrieval_analysis, misses = {}, []
    for level in ("S1", "S2", "S3"):
        selected = [sid for sid in s_paths if s_paths[sid]["derived_s"] == level]
        stats: dict[str, Any] = {"Poison_N": len(selected), "E1_available": 0, "E2_available": 0,
                                 "E1_hit": 0, "E2_hit": 0, "Both_available": 0, "Both_hit": 0,
                                 "Any_hit": 0, "Oracle_FN_despite_packet_available": 0,
                                 "Both_hit_nonOracle_FN": 0}
        predmap = {c: {r["candidate_id"]: r for r in data} for c, data in by_condition.items()}
        for sid in selected:
            docs = {r["evidence_doc_id"] for r in retrieval[sid]}
            ref = reference[sid]
            hit = {slot: doc in docs for slot, doc in ref.items()}
            for slot in ("E1", "E2"):
                stats[f"{slot}_available"] += int(slot in ref)
                stats[f"{slot}_hit"] += int(hit.get(slot, False))
            both = "E1" in ref and "E2" in ref
            stats["Both_available"] += int(both)
            stats["Both_hit"] += int(both and all(hit.values()))
            stats["Any_hit"] += int(any(hit.values()))
            stats["Oracle_FN_despite_packet_available"] += int(predmap["C"][sid]["predicted_class"] == 0)
            stats["Both_hit_nonOracle_FN"] += int(both and all(hit.values()) and predmap["B2"][sid]["predicted_class"] == 0)
            if any(predmap[c][sid]["predicted_class"] == 0 for c in predmap):
                misses.append({"candidate_id": sid, "S": level, "reference_hits_top5": hit,
                    "predictions": {c: predmap[c][sid]["predicted_class"] for c in predmap},
                    "retrieval_missing_reference": [slot for slot, value in hit.items() if not value],
                    "primary_conclusion": "PACKET_RETRIEVAL_MISS_OBSERVED" if not all(hit.values()) else "REFERENCE_RECALLED_REPRESENTATION_OR_CLASSIFIER_FAILURE",
                    "causal_localization": "UNRESOLVED_WITHOUT_ATOM_ALIGNED_INTERVENTION"})
        retrieval_analysis[level] = stats
    historical: dict[str, dict[str, Any]] = {}
    for condition, rows in by_condition.items():
        hn = [r for r in rows if r["construction_role_evaluation_only"] == "HARD_NEGATIVE"]
        historical[condition] = {}
        for history in (True, False):
            chosen = [r for r in hn if (r["approved_overall_status"] == "LEGITIMATE_VERSION_OR_HISTORY") == history]
            historical[condition]["historical" if history else "other_legitimate"] = {
                "FP": sum(r["predicted_class"] for r in chosen), "N": len(chosen)}
    new(base / "D1_RETRIEVAL_AND_FAILURE_ANALYSIS_V1.json", {"by_approved_S": retrieval_analysis,
        "Hard_Negative_by_approved_status": historical, "false_negative_samples": misses,
        "reference_recall_is_not_detection_recall": True,
        "reference_documents_are_not_unique_absolute_relevance_truth": True})
    control = permutation_control(base, config)
    new(base / "D1_PERMUTATION_CONTROL_V1.json", control)
    diagnostics = {}
    for condition, rows in by_condition.items():
        folds = load(base / "models" / f"{condition}_FOLD_TRAINING_RECORDS_V1.json")
        diagnostics[condition] = {
            "fold_count": len(folds), "convergence_warnings": sum(r["convergence_warnings"] for r in folds),
            "max_abs_coefficient": max(float(np.abs(r["coefficient"]).max()) for r in folds),
            "max_iterations": max(r["iterations"] for r in folds),
            "min_train_samples": min(r["train_sample_count"] for r in folds),
            "max_train_samples": max(r["train_sample_count"] for r in folds),
            "probability_below01_or_above99": sum(r["uncalibrated_probability"] < .01 or r["uncalibrated_probability"] > .99 for r in rows),
            "family_AUROC": {family: metrics([r for r in rows if r["family_evaluation_only"] == family])["AUROC"] for family in families},
            "high_performance_sanity_trigger": full_metrics[condition]["AUROC"] >= .95 or full_metrics[condition]["AUPRC"] >= .95,
        }
    new(base / "D1_MODEL_DIAGNOSTICS_V1.json", diagnostics)
    new(base / "EVALUATION_COMPLETION_V1.json", {
        "script_sha256": sha(Path(__file__)), "qa_join_source_sha256": sha(qa_path),
        "predictions_480_4x120": True, "post_lock_join": True, "old126_not_read": True,
        "independent_AUC_AP_PASS": True, "finished_utc": datetime.now(timezone.utc).isoformat(),
    })
    print(json.dumps({"metrics": full_metrics, "permutation_AUC": control["AUROC"], "permutation_AP": control["AUPRC"]}))


if __name__ == "__main__":
    main()
