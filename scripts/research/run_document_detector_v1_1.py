"""Run the frozen Final72 V1.1 development-only LOGO detector prototype.

No feature extraction, retrieval, evidence matching, label-driven selection, or
post-hoc tuning occurs here. Evaluation labels are joined only after the frozen
feature matrix and its identities have been checked.
"""
# mypy: disable-error-code=import-untyped

from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import statistics
import subprocess
import warnings
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.exceptions import ConvergenceWarning
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    balanced_accuracy_score,
    matthews_corrcoef,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

SEED = 20260922
TASK = "P1-FIRST-DOCUMENT-DETECTOR-V1_1-LOGO-PROTOTYPE-EXECUTION-01"
HASHES = {
    "gt": "9e6224ef2cb2cb8e729f9ab569d09589c951e6df4ed3327c63c82913066d720a",
    "feature_set": "a3190b3b3fd6f3323229a83f9c919143fdba9efe06f209ef492242cdc1e37ee8",
    "matrix": "2d418ae2fd6d22f848fcf812a6126fd68ff9b7b880c389a2ca510a5c94dd5b2d",
    "candidates": "f530471ecd6551300d68c8ddf104cadce2305d8ff91e64010be222820628252d",
}
VIEWS = {"S": "SEMANTIC", "E": "ENTITY_CLAIM", "P": "PROVENANCE", "T": "TEMPORAL_VERSION"}
COUNTS = {"S": 3, "E": 9, "P": 6, "T": 3}
FORBIDDEN = {
    "label", "target", "candidate_class", "hkp", "stealth", "expected", "owner",
    "annotator", "sample_id", "group_id", "path", "file", "evidence_selection",
    "risk_goal", "ground_truth", "oracle", "poison", "clean", "hard_negative",
}
PREFIX = "PAPER1_FINAL72_DOCUMENT_DETECTOR_"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def dump(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")


def dump_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(r, ensure_ascii=False, sort_keys=True, allow_nan=False) + "\n" for r in rows), encoding="utf-8")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def row_id(candidate_text: str) -> str:
    return "FR-" + hashlib.sha256(candidate_text.encode("utf-8")).hexdigest()[:16]


def model_names() -> dict[str, str]:
    return {
        "S-only": "S", "E-only": "E", "P-only": "P", "T-only": "T",
        "Full SEPT": "SEPT", "Full-S": "EPT", "Full-E": "SPT",
        "Full-P": "SET", "Full-T": "SEP",
    }


def safe_quantile(values: list[float], q: float) -> float:
    return float(np.quantile(np.asarray(values, dtype=float), q))


def load_inputs(paths: dict[str, Path]) -> tuple[list[dict[str, Any]], dict[str, list[str]], list[str], list[str]]:
    for name, expected in HASHES.items():
        if sha(paths[name]) != expected:
            raise ValueError(f"FROZEN_INPUT_SHA_MISMATCH: {name}")
    feature_set = json.loads(paths["feature_set"].read_text(encoding="utf-8"))
    matrix = read_jsonl(paths["matrix"])
    gt = json.loads(paths["gt"].read_text(encoding="utf-8"))
    candidates = read_jsonl(paths["candidates"])
    names = [f["feature_name"] for f in feature_set["features"]]
    if len(names) != 21 or len(set(names)) != 21 or len(matrix) != 72:
        raise ValueError("V1.1_FEATURE_SHAPE_INVALID")
    if {"host_publisher_relation", "publisher_issuer_match"} & set(names):
        raise ValueError("DEFERRED_PROVENANCE_LEAKAGE")
    if set(feature_set.get("excluded_oracle_features", [])) & set(names):
        raise ValueError("ORACLE_TEMPORAL_LEAKAGE")
    views = {v: [f["feature_name"] for f in feature_set["features"] if f["view"] == full] for v, full in VIEWS.items()}
    if {v: len(x) for v, x in views.items()} != COUNTS:
        raise ValueError("VIEW_COUNT_MISMATCH")
    if any((set(r) | set(r.get("features", {}))) & FORBIDDEN for r in matrix):
        raise ValueError("MODEL_MATRIX_LABEL_LEAKAGE")
    if any(set(r["features"]) != set(names) for r in matrix):
        raise ValueError("MATRIX_COLUMNS_MISMATCH")
    if len({r["feature_row_id"] for r in matrix}) != 72:
        raise ValueError("MATRIX_ID_DUPLICATE")
    if gt["role"] != "DEVELOPMENT_AND_METHOD_ENGINEERING_SET" or len(gt["records"]) != 72:
        raise ValueError("GT_ROLE_OR_SHAPE_INVALID")
    gt_ids = {r["sample_id"] for r in gt["records"]}
    if len(gt_ids) != 72 or len(candidates) != 72 or {r["sample_id"] for r in candidates} != gt_ids:
        raise ValueError("GT_CANDIDATE_ID_PARITY_FAIL")
    by_row = {r["feature_row_id"]: r["features"] for r in matrix}
    if {row_id(c["phase1_view"]["candidate_text"]) for c in candidates} != set(by_row):
        raise ValueError("CANDIDATE_MATRIX_ID_PARITY_FAIL")
    by_gt = {r["sample_id"]: r for r in gt["records"]}
    rows = []
    for c in candidates:
        kind = c["owner_only"]["candidate_kind"]
        if kind not in {"CLEAN_CURRENT", "POISON_CANDIDATE", "MATCHED_HARD_NEGATIVE"}:
            raise ValueError("UNKNOWN_CANDIDATE_KIND")
        rows.append({
            "sample_id": c["sample_id"], "group_id": c["triplet_id"],
            "true_class": kind, "target": int(kind == "POISON_CANDIDATE"),
            "domain": c["owner_only"].get("domain"),
            "features": by_row[row_id(c["phase1_view"]["candidate_text"])],
            "gt_linked": c["sample_id"] in by_gt,
        })
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in rows:
        groups[r["group_id"]].append(r)
    kinds = {"CLEAN_CURRENT", "POISON_CANDIDATE", "MATCHED_HARD_NEGATIVE"}
    if len(groups) != 24 or any(len(x) != 3 or {r["true_class"] for r in x} != kinds for x in groups.values()):
        raise ValueError("MATCHED_GROUP_STRUCTURE_FAIL")
    if len({r["sample_id"] for r in rows}) != 72 or not all(r["gt_linked"] for r in rows):
        raise ValueError("ROW_IDENTITY_FAIL")
    binary: list[str] = []
    continuous: list[str] = []
    for name in names:
        observed = [r["features"][name] for r in rows if r["features"][name] is not None]
        if not observed or any(isinstance(v, str) or not isinstance(v, (bool, int, float)) for v in observed):
            raise ValueError(f"NON_NUMERIC_OR_ALL_MISSING: {name}")
        if all(isinstance(v, bool) for v in observed):
            binary.append(name)
        else:
            if any(isinstance(v, bool) for v in observed) or not all(math.isfinite(float(v)) for v in observed):
                raise ValueError(f"MIXED_OR_NONFINITE_FEATURE: {name}")
            continuous.append(name)
    return rows, views, binary, continuous


def fold_indices(rows: list[dict[str, Any]]) -> list[tuple[str, list[int], list[int]]]:
    folds = []
    for group in sorted({r["group_id"] for r in rows}):
        test = [i for i, r in enumerate(rows) if r["group_id"] == group]
        train = [i for i, r in enumerate(rows) if r["group_id"] != group]
        if len(train) != 69 or len(test) != 3:
            raise ValueError("LOGO_FOLD_SHAPE_FAIL")
        folds.append((group, train, test))
    if len(folds) != 24 or Counter(i for _, _, test in folds for i in test) != Counter(range(72)):
        raise ValueError("OOF_FOLD_COVERAGE_FAIL")
    return folds


def array_for(rows: list[dict[str, Any]], names: list[str]) -> np.ndarray:
    return np.asarray([[float(r["features"][n]) if r["features"][n] is not None else np.nan for n in names] for r in rows], dtype=float)


def pipeline(names: list[str], binary: list[str], continuous: list[str]) -> Pipeline:
    c_idx = [names.index(n) for n in names if n in continuous]
    b_idx = [names.index(n) for n in names if n in binary]
    transformers = []
    if c_idx:
        transformers.append(("continuous", Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]), c_idx))
    if b_idx:
        transformers.append(("binary", SimpleImputer(strategy="most_frequent"), b_idx))
    return Pipeline([
        ("preprocess", ColumnTransformer(transformers=transformers, remainder="drop")),
        ("classifier", LogisticRegression(penalty="l2", C=1.0, solver="liblinear", max_iter=2000, class_weight="balanced", random_state=SEED)),
    ])


def fit_logo(rows: list[dict[str, Any]], names: list[str], binary: list[str], continuous: list[str], folds: list[tuple[str, list[int], list[int]]], targets: np.ndarray) -> dict[str, Any]:
    x = array_for(rows, names)
    scores = np.full(len(rows), np.nan)
    probs = np.full(len(rows), np.nan)
    coefficients = []
    fold_details = []
    convergence = 0
    for fold_id, train, test in folds:
        if any(np.all(np.isnan(x[train, j])) for j in range(x.shape[1])):
            raise ValueError(f"ALL_MISSING_TRAIN_FEATURE:{fold_id}")
        model = pipeline(names, binary, continuous)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always", ConvergenceWarning)
            model.fit(x[train], targets[train])
        convergence += sum(issubclass(w.category, ConvergenceWarning) for w in caught)
        scores[test] = model.decision_function(x[test])
        probs[test] = model.predict_proba(x[test])[:, 1]
        trained = model.named_steps["classifier"]
        transformed_names = [n for n in names if n in continuous] + [n for n in names if n in binary]
        coefficients.append({"fold_id": fold_id, "coefficients": dict(zip(transformed_names, map(float, trained.coef_[0]), strict=True)), "intercept": float(trained.intercept_[0]), "iterations": int(trained.n_iter_[0])})
        fold_details.append({"fold_id": fold_id, "train_count": 69, "validation_count": 3, "train_groups": 23, "validation_group": fold_id, "train_only_imputer": True, "train_only_scaler": True})
    if np.isnan(scores).any() or np.isnan(probs).any() or not np.isfinite(scores).all():
        raise ValueError("OOF_NONFINITE_OR_INCOMPLETE")
    return {"score": scores, "probability": probs, "coefficients": coefficients, "folds": fold_details, "convergence_warnings": convergence}


def recall_at_fpr(y: np.ndarray, scores: np.ndarray, fpr: float) -> dict[str, Any]:
    negatives = int((y == 0).sum())
    allowance = math.floor(fpr * negatives)
    candidates = [math.inf, *sorted(set(map(float, scores)), reverse=True)]
    best = 0.0
    for cutoff in candidates:
        predicted = scores >= cutoff
        fp = int(((y == 0) & predicted).sum())
        if fp <= allowance:
            best = max(best, float(((y == 1) & predicted).sum() / (y == 1).sum()))
    return {"recall": best, "max_false_positives": allowance, "negative_count": negatives, "descriptive_only": True}


def metrics(y: np.ndarray, scores: np.ndarray, probs: np.ndarray, rows: list[dict[str, Any]]) -> dict[str, Any]:
    pred = (probs >= 0.5).astype(int)
    tn = int(((y == 0) & (pred == 0)).sum())
    fp = int(((y == 0) & (pred == 1)).sum())
    fn = int(((y == 1) & (pred == 0)).sum())
    tp = int(((y == 1) & (pred == 1)).sum())
    hn = [i for i, r in enumerate(rows) if r["true_class"] == "MATCHED_HARD_NEGATIVE"]
    p = float(precision_score(y, pred, zero_division=0))
    r = float(recall_score(y, pred, zero_division=0))
    f1_manual = 0.0 if p + r == 0 else 2 * p * r / (p + r)
    result: dict[str, Any] = {
        "auroc": float(roc_auc_score(y, scores)), "auprc": float(average_precision_score(y, scores)),
        "precision_at_0_5": p, "recall_at_0_5": r, "f1_at_0_5": f1_manual,
        "balanced_accuracy_at_0_5": float(balanced_accuracy_score(y, pred)),
        "specificity_at_0_5": tn / (tn + fp), "mcc_at_0_5": float(matthews_corrcoef(y, pred)),
        "hn_fpr_at_0_5": float(pred[hn].sum() / len(hn)),
        "confusion": {"tn": tn, "fp": fp, "fn": fn, "tp": tp},
        "recall_at_1pct_fpr": "NOT_RELIABLY_ESTIMABLE_ON_FINAL72",
        "recall_at_5pct_fpr": recall_at_fpr(y, scores, 0.05),
        "development_oof_diagnostic": True,
    }
    if not math.isclose(result["balanced_accuracy_at_0_5"], (tp / (tp + fn) + tn / (tn + fp)) / 2):
        raise AssertionError("METRIC_RECOMPUTATION_FAIL")
    return result


def matched(rows: list[dict[str, Any]], scores: np.ndarray) -> dict[str, Any]:
    groups: dict[str, dict[str, int]] = defaultdict(dict)
    for i, row in enumerate(rows):
        groups[row["group_id"]][row["true_class"]] = i
    per_group: list[dict[str, Any]] = []
    for group, members in sorted(groups.items()):
        p, c, h = (float(scores[members[k]]) for k in ("POISON_CANDIDATE", "CLEAN_CURRENT", "MATCHED_HARD_NEGATIVE"))
        ph, pc = p - h, p - c
        per_group.append({"group_id": group, "poison_score": p, "hn_score": h, "clean_score": c, "p_hn_margin": ph, "p_clean_margin": pc, "p_hn_outcome": "win" if ph > 0 else "tie" if ph == 0 else "loss", "p_clean_outcome": "win" if pc > 0 else "tie" if pc == 0 else "loss", "poison_top": bool(p > h and p > c)})
    def pair(field: str) -> dict[str, Any]:
        ct = Counter(g[field] for g in per_group)
        return {"win": ct["win"], "tie": ct["tie"], "loss": ct["loss"], "strict_pairwise_accuracy": ct["win"] / 24}
    def margins(field: str) -> dict[str, float]:
        vals = [float(g[field]) for g in per_group]
        return {"mean": statistics.mean(vals), "median": statistics.median(vals), "q1": safe_quantile(vals, 0.25), "q3": safe_quantile(vals, 0.75)}
    return {"poison_vs_hn": pair("p_hn_outcome"), "poison_vs_clean": pair("p_clean_outcome"), "poison_top_triplet_rate": sum(g["poison_top"] for g in per_group) / 24, "p_hn_margin": margins("p_hn_margin"), "p_clean_margin": margins("p_clean_margin"), "groups": per_group}


def bootstrap(rows: list[dict[str, Any]], y: np.ndarray, scores: np.ndarray, n: int = 2000) -> dict[str, Any]:
    rng = np.random.default_rng(SEED)
    by_group: dict[str, list[int]] = defaultdict(list)
    for i, row in enumerate(rows):
        by_group[row["group_id"]].append(i)
    groups = sorted(by_group)
    matching = matched(rows, scores)["groups"]
    by_match = {g["group_id"]: g for g in matching}
    values: dict[str, list[float]] = defaultdict(list)
    for _ in range(n):
        picked = rng.choice(groups, size=24, replace=True)
        idx = [i for g in picked for i in by_group[str(g)]]
        values["auroc"].append(float(roc_auc_score(y[idx], scores[idx])))
        values["auprc"].append(float(average_precision_score(y[idx], scores[idx])))
        selected = [by_match[str(g)] for g in picked]
        values["poison_vs_hn"].append(sum(g["p_hn_outcome"] == "win" for g in selected) / 24)
        values["poison_vs_clean"].append(sum(g["p_clean_outcome"] == "win" for g in selected) / 24)
        values["poison_top_triplet"].append(sum(g["poison_top"] for g in selected) / 24)
    return {"seed": SEED, "resamples": n, "unit": "matched_group", "interval_kind": "development_descriptive_percentile_95", "intervals": {k: {"lower": safe_quantile(v, 0.025), "upper": safe_quantile(v, 0.975), "median": safe_quantile(v, 0.5)} for k, v in values.items()}}


def permutation(rows: list[dict[str, Any]], names: list[str], binary: list[str], continuous: list[str], folds: list[tuple[str, list[int], list[int]]], observed: dict[str, float], n: int = 200) -> dict[str, Any]:
    rng = np.random.default_rng(SEED)
    groups: dict[str, list[int]] = defaultdict(list)
    for i, row in enumerate(rows):
        groups[row["group_id"]].append(i)
    values: dict[str, list[float]] = {"auroc": [], "auprc": []}
    for _ in range(n):
        pseudo = np.zeros(72, dtype=int)
        for group in sorted(groups):
            pseudo[int(rng.choice(groups[group]))] = 1
        run = fit_logo(rows, names, binary, continuous, folds, pseudo)
        values["auroc"].append(float(roc_auc_score(pseudo, run["score"])))
        values["auprc"].append(float(average_precision_score(pseudo, run["score"])))
    return {"seed": SEED, "permutations": n, "scheme": "WITHIN_GROUP_POISON_IDENTITY", "distribution": {key: {"mean": statistics.mean(v), "median": statistics.median(v), "q025": safe_quantile(v, 0.025), "q975": safe_quantile(v, 0.975), "max": max(v), "empirical_p_like_ge_observed": (1 + sum(x >= observed[key] for x in v)) / (n + 1)} for key, v in values.items()}, "formal_significance_claim": False}


def coefficient_report(folds: list[dict[str, Any]], views: dict[str, list[str]]) -> dict[str, Any]:
    names = sorted(folds[0]["coefficients"])
    per = {}
    for name in names:
        vals = [f["coefficients"][name] for f in folds]
        pos, neg = sum(v > 1e-9 for v in vals), sum(v < -1e-9 for v in vals)
        per[name] = {"mean": statistics.mean(vals), "median": statistics.median(vals), "std": statistics.pstdev(vals), "min": min(vals), "max": max(vals), "positive_folds": pos, "negative_folds": neg, "near_zero_folds": 24 - pos - neg, "sign_stability": max(pos, neg) / 24}
    view = {v: {"mean_abs_coefficient": statistics.mean(abs(per[n]["mean"]) for n in names), "mean_sign_stability": statistics.mean(per[n]["sign_stability"] for n in names)} for v, names in views.items()}
    return {"fold_coefficients": folds, "per_feature": per, "per_view": view, "causal_importance_claim": False}


def main() -> None:
    parser = argparse.ArgumentParser()
    for key in ("gt", "feature_set", "matrix", "candidates", "protocol", "output"):
        parser.add_argument(f"--{key.replace('_', '-')}", type=Path, required=True)
    args = parser.parse_args()
    paths = {k: getattr(args, k) for k in ("gt", "feature_set", "matrix", "candidates", "protocol")}
    out: Path = args.output
    if out.exists() and any(out.iterdir()):
        raise ValueError("OUTPUT_NAMESPACE_NOT_EMPTY")
    if not paths["protocol"].is_file():
        raise ValueError("PROTOCOL_MISSING")
    rows, views, binary, continuous = load_inputs(paths)
    folds = fold_indices(rows)
    names_by_model = {model: [n for view in membership for n in views[view]] for model, membership in model_names().items()}
    expected_counts = {"S-only": 3, "E-only": 9, "P-only": 6, "T-only": 3, "Full SEPT": 21, "Full-S": 18, "Full-E": 12, "Full-P": 15, "Full-T": 18}
    if {k: len(v) for k, v in names_by_model.items()} != expected_counts:
        raise ValueError("MODEL_FEATURE_COUNT_FAIL")
    for _, train, _ in folds:
        if any(all(rows[i]["features"][n] is None for i in train) for n in names_by_model["Full SEPT"]):
            raise ValueError("FOLD_LOCAL_IMPUTATION_UNDEFINED")
    out.mkdir(parents=True, exist_ok=True)
    code_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    manifest = {
        "task": TASK, "status": "PRE_FIT_LOCKED", "pre_fit_lock_timestamp": stamp(),
        "frozen_input_sha256": HASHES, "protocol_sha256": sha(paths["protocol"]),
        "code_commit": code_commit, "script_sha256": sha(Path(__file__)),
        "python_version": platform.python_version(), "sklearn_version": sklearn.__version__,
        "seed": SEED, "model": "LogisticRegression(l2,C=1.0,liblinear,max_iter=2000,class_weight=balanced)",
        "folds": [{"fold_id": f, "train_groups": 23, "train_rows": 69, "validation_rows": 3, "validation_sample_ids": [rows[i]["sample_id"] for i in test]} for f, _, test in folds],
        "model_feature_counts": expected_counts, "binary_features": binary, "continuous_features": continuous,
        "forbidden_feature_hits": [], "development_only": True,
    }
    dump(out / "run_manifest_pre_fit.json", manifest)
    y = np.asarray([r["target"] for r in rows], dtype=int)
    results: dict[str, dict[str, Any]] = {}
    for model, names in names_by_model.items():
        run = fit_logo(rows, names, binary, continuous, folds, y)
        result = {"features": names, "metrics": metrics(y, run["score"], run["probability"], rows), "matched": matched(rows, run["score"]), "run": run}
        results[model] = result
    full = results["Full SEPT"]
    full_scores, full_probs = full["run"]["score"], full["run"]["probability"]
    oof = [{"sample_id": r["sample_id"], "group_id": r["group_id"], "true_class": r["true_class"], "binary_target": r["target"], "fold_id": r["group_id"], "decision_score": float(full_scores[i]), "uncalibrated_probability": float(full_probs[i]), "predicted_class_at_0_5": int(full_probs[i] >= 0.5)} for i, r in enumerate(rows)]
    dump_jsonl(out / (PREFIX + "OOF_PREDICTIONS_V1_1.jsonl"), oof)
    compact = {model: {"feature_count": len(x["features"]), "metrics": x["metrics"], "matched": {k: v for k, v in x["matched"].items() if k != "groups"}} for model, x in results.items()}
    dump(out / (PREFIX + "METRICS_V1_1.json"), {"development_oof": True, "full_sept": compact["Full SEPT"], "all_models": compact})
    dump(out / (PREFIX + "VIEW_COMPARISON_V1_1.json"), {k: compact[k] for k in ("S-only", "E-only", "P-only", "T-only", "Full SEPT")})
    dump(out / (PREFIX + "ABLATION_V1_1.json"), {k: compact[k] for k in ("Full-S", "Full-E", "Full-P", "Full-T")})
    dump(out / (PREFIX + "MATCHED_ANALYSIS_V1_1.json"), full["matched"])
    dump(out / (PREFIX + "COEFFICIENT_ANALYSIS_V1_1.json"), coefficient_report(full["run"]["coefficients"], views))
    dump(out / (PREFIX + "BOOTSTRAP_V1_1.json"), bootstrap(rows, y, full_scores))
    perm = permutation(rows, names_by_model["Full SEPT"], binary, continuous, folds, {"auroc": full["metrics"]["auroc"], "auprc": full["metrics"]["auprc"]})
    dump(out / (PREFIX + "PERMUTATION_CONTROL_V1_1.json"), perm)
    hard = [g for g in full["matched"]["groups"] if g["p_hn_outcome"] != "win" or g["p_clean_outcome"] != "win"]
    errors = []
    for g in full["matched"]["groups"]:
        tags = []
        if g["p_hn_margin"] <= 0:
            tags.append("POISON_BELOW_OR_TIED_HN")
        if g["p_clean_margin"] <= 0:
            tags.append("POISON_BELOW_OR_TIED_CLEAN")
        if g["hn_score"] >= 0:
            tags.append("HN_SCORED_HIGH")
        if g["clean_score"] >= 0:
            tags.append("CLEAN_SCORED_HIGH")
        if max(g["poison_score"], g["hn_score"], g["clean_score"]) - min(g["poison_score"], g["hn_score"], g["clean_score"]) < 0.1:
            tags.append("ALL_TRIPLET_SCORES_SIMILAR")
        if tags:
            errors.append({"group_id": g["group_id"], "tags": tags})
    high_trigger = full["metrics"]["auroc"] >= 0.95 or full["metrics"]["auprc"] >= 0.90 or full["matched"]["poison_vs_hn"]["strict_pairwise_accuracy"] >= 0.90
    perm_abnormal = perm["distribution"]["auroc"]["mean"] >= 0.65 or perm["distribution"]["auprc"]["mean"] >= 0.5
    audit = {
        "high_performance_trigger": high_trigger,
        "permutation_abnormal_heuristic": perm_abnormal,
        "feature_label_id_leakage": False, "group_crossing": False,
        "source_domain_label_crosscheck": {"counts": {d: dict(Counter(r["true_class"] for r in rows if r["domain"] == d)) for d in sorted({r["domain"] for r in rows})}},
        "missingness_by_class": {n: {kind: sum(r["features"][n] is None for r in rows if r["true_class"] == kind) for kind in ("CLEAN_CURRENT", "POISON_CANDIDATE", "MATCHED_HARD_NEGATIVE")} for n in names_by_model["Full SEPT"]},
        "constant_features": [n for n in names_by_model["Full SEPT"] if len({r["features"][n] for r in rows if r["features"][n] is not None}) <= 1],
        "corpus_simplicity_limitation": "57-document trusted corpus; development-only retrieval setting may be an easy shortcut",
        "version_identity_risk": "inspect frozen feature lineage; no group or version ID used as direct model feature",
        "no_posthoc_repair": True,
    }
    coef = np.asarray([[f["coefficients"][n] for n in sorted(names_by_model["Full SEPT"])] for f in full["run"]["coefficients"]])
    overfit = {"train_rows_per_fold": 69, "features": 21, "feature_train_ratio": 21 / 69, "convergence_warnings": full["run"]["convergence_warnings"], "max_absolute_coefficient": float(np.max(np.abs(coef))), "max_coefficient_std": float(np.max(np.std(coef, axis=0))), "p_lt_0_01": int((full_probs < 0.01).sum()), "p_gt_0_99": int((full_probs > 0.99).sum()), "not_formal_generalization": True}
    dump(out / (PREFIX + "FAILURE_ANALYSIS_V1_1.json"), {"hard_groups": hard, "error_taxonomy": errors, "leakage_sanity_audit": audit, "overfitting_audit": overfit})
    hashes = {p.name: sha(p) for p in sorted(out.iterdir()) if p.is_file()}
    dump(out / "result_hash_manifest.json", {"task": TASK, "status": "RESULTS_HASH_LOCKED", "locked_at": stamp(), "files_sha256": hashes})
    print(json.dumps({"output": str(out), "metrics": full["metrics"], "matched": {k: v for k, v in full["matched"].items() if k != "groups"}, "permutation": perm["distribution"], "high_performance_trigger": high_trigger, "permutation_abnormal": perm_abnormal, "hard_groups": [g["group_id"] for g in hard]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
