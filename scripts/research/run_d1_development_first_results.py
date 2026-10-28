"""Execute only the signed, fixed D1 development conditions in a sealed run.

The prediction process reads sanitized text/numeric matrices, training targets
and split-only metadata. Evaluation roles, S strata, Human returns and Oracle
matching are not opened here. All preprocessing is fitted on train folds only.
"""
# mypy: disable-error-code=import-untyped
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import warnings
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.exceptions import ConvergenceWarning
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from llmguard.domains.retrieval.hidden_poisoning.method_engineering.development_detection import (
    BINARY_FEATURES,
    family_folds,
    numeric_fold_preflight,
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def new(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write("\n")


def lr(config: dict[str, Any]) -> LogisticRegression:
    return LogisticRegression(**config["config"]["model"])


def numeric_pipeline(names: list[str], config: dict[str, Any]) -> Pipeline:
    continuous = [i for i, name in enumerate(names) if name not in BINARY_FEATURES]
    binary = [i for i, name in enumerate(names) if name in BINARY_FEATURES]
    transforms = []
    if continuous:
        transforms.append(("continuous", Pipeline([
            ("imputer", SimpleImputer(strategy="median", add_indicator=False)),
            ("scaler", StandardScaler()),
        ]), continuous))
    if binary:
        transforms.append(("binary", SimpleImputer(strategy="most_frequent", add_indicator=False), binary))
    return Pipeline([
        ("preprocess", ColumnTransformer(transforms, remainder="drop")),
        ("classifier", lr(config)),
    ])


def text_pipeline(config: dict[str, Any]) -> Pipeline:
    vectorizer = dict(config["config"]["vectorizer"])
    vectorizer["ngram_range"] = tuple(vectorizer["ngram_range"])
    return Pipeline([("vectorizer", TfidfVectorizer(**vectorizer)), ("classifier", lr(config))])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-root", required=True, type=Path)
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--source-lock", default="EXECUTION_SOURCE_LOCK_V1.json")
    args = parser.parse_args()
    base = args.run_root.resolve()
    config = json.loads((base / "CONFIG_FREEZE_V1.json").read_text(encoding="utf-8"))
    lock = json.loads((base / "INPUT_LOCK_V1.json").read_text(encoding="utf-8"))
    assert sha(base / "CONFIG_FREEZE_V1.json") == lock["config_sha256"]
    for record in lock["files"]:
        assert sha(base / record["path"]) == record["sha256"], record["path"]
    signed = json.loads((base / "qualification/OWNER_QUALIFICATION_ACCEPTANCE_V1.json").read_text(encoding="utf-8"))
    assert signed["Owner_signed"] is True and signed["scope"] == "D1_DEV_ONLY"
    assert signed["only_five_logical_cells_changed"] is True
    assert sha(base / "raw/OWNER_SIGNED_ACTUAL_RETURN_V1.xlsx") == signed["raw_signed_sha256"]
    assert sklearn.__version__ == config["runtime"]["sklearn"]
    texts = read(base / "input/CANDIDATES_ONLY_V1.jsonl")
    targets = read(base / "input/TRAINING_TARGET_VAULT_V1.jsonl")
    metadata = read(base / "input/SPLIT_ONLY_METADATA_V1.jsonl")
    ids = [record["candidate_id"] for record in texts]
    assert len(ids) == len(set(ids)) == 120
    assert ids == [row["candidate_id"] for row in targets] == [row["candidate_id"] for row in metadata]
    assert all(set(row) == {"candidate_id", "candidate_text"} for row in texts)
    assert all(set(row) == {"candidate_id", "target"} for row in targets)
    y = np.asarray([row["target"] for row in targets], dtype=int)
    assert Counter(y.tolist()) == {0: 80, 1: 40}
    folds = family_folds([row["family"] for row in metadata], [row["group_id"] for row in metadata])
    assert len(folds) == 13
    matrices: dict[str, Any] = {"A": [row["candidate_text"] for row in texts]}
    names_by_condition: dict[str, list[str]] = {}
    status: dict[str, Any] = {}
    for condition in ["A", "B1", "B2", "C", "C21_REFERENCE"]:
        fold_stats: dict[str, Any] = {}
        if condition != "A":
            data = read(base / "input" / (f"{condition}_NUMERIC_V1.jsonl"))
            assert [row["candidate_id"] for row in data] == ids
            names = list(data[0]["features"])
            expected = config["conditions"]["B1" if condition == "C21_REFERENCE" else condition]["feature_names"]
            assert names == expected
            names_by_condition[condition] = names
            fold_stats = numeric_fold_preflight([row["features"] for row in data], names, folds)
            matrices[condition] = np.asarray([
                [np.nan if row["features"][name] is None else row["features"][name] for name in names]
                for row in data
            ], dtype=float)
        else:
            assert all(isinstance(text, str) and len(text) >= 3 for text in matrices["A"])
        for fold in folds:
            assert set(y[list(fold.train)]) == {0, 1}
        blocked = any(bool(value) for value in fold_stats.values())
        status[condition] = {
            "status": "BLOCKED" if blocked else "PREFLIGHT_PASS",
            "all_missing_training_columns_by_family": fold_stats,
            "folds": len(folds), "eligible_candidates": 120,
        }
    assert names_by_condition["B2"] == names_by_condition["C"]
    assert status["C21_REFERENCE"]["status"] == "BLOCKED"
    if args.preflight_only:
        new(base / "PREFLIGHT_V1.json", {
            "conditions": status,
            "folds": [{"family": fold.family, "train": list(fold.train), "validation": list(fold.validation)} for fold in folds],
            "source_sha256": sha(Path(__file__)), "fit_started": False,
        })
        print(json.dumps(status))
        return
    preflight = json.loads((base / "PREFLIGHT_V1.json").read_text(encoding="utf-8"))
    assert preflight["conditions"] == json.loads(json.dumps(status))
    source_lock = json.loads((base / args.source_lock).read_text(encoding="utf-8"))
    assert source_lock["runner_sha256"] == sha(Path(__file__))
    assert source_lock["executed_git_commit"] == subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    for record in source_lock["code"]:
        assert sha(Path(record["path"])) == record["sha256"]
    output = []
    model_index = []
    execution: dict[str, dict[str, Any]] = {}
    for condition in ["A", "B1", "B2", "C"]:
        if status[condition]["status"] != "PREFLIGHT_PASS":
            execution[condition] = {"status": "BLOCKED", "reason": "ALL_MISSING_TRAIN_FEATURE"}
            continue
        scores = np.full(120, np.nan)
        probabilities = np.full(120, np.nan)
        fold_records = []
        try:
            for fold in folds:
                train, test = list(fold.train), list(fold.validation)
                model = text_pipeline(config) if condition == "A" else numeric_pipeline(names_by_condition[condition], config)
                data = matrices[condition]
                xtrain = [data[i] for i in train] if condition == "A" else data[train]
                xtest = [data[i] for i in test] if condition == "A" else data[test]
                with warnings.catch_warnings(record=True) as caught:
                    warnings.simplefilter("always", ConvergenceWarning)
                    model.fit(xtrain, y[train])
                convergence = sum(issubclass(w.category, ConvergenceWarning) for w in caught)
                if convergence:
                    raise RuntimeError("CONVERGENCE_WARNING_CONDITION_BLOCKED")
                scores[test] = model.decision_function(xtest)
                probabilities[test] = model.predict_proba(xtest)[:, 1]
                transform = model.named_steps["vectorizer"] if condition == "A" else model.named_steps["preprocess"]
                if condition == "A":
                    assert int(transform.idf_.shape[0]) > 0
                    statistics = {"vocabulary_count": len(transform.vocabulary_), "idf_sha256": hashlib.sha256(transform.idf_.tobytes()).hexdigest()}
                else:
                    names = names_by_condition[condition]
                    cc = [i for i, name in enumerate(names) if name not in BINARY_FEATURES]
                    bb = [i for i, name in enumerate(names) if name in BINARY_FEATURES]
                    cont = transform.named_transformers_["continuous"]
                    binary_imputer = transform.named_transformers_["binary"]
                    assert np.allclose(cont.named_steps["imputer"].statistics_, np.nanmedian(data[train][:, cc], axis=0))
                    observed = data[train][:, bb]
                    modes = [min(Counter(column[np.isfinite(column)]).items(), key=lambda item: (-item[1], item[0]))[0] for column in observed.T]
                    assert np.array_equal(binary_imputer.statistics_, np.asarray(modes))
                    filled = cont.named_steps["imputer"].transform(data[train][:, cc])
                    assert np.allclose(cont.named_steps["scaler"].mean_, filled.mean(axis=0))
                    statistics = {"continuous_names": [names[i] for i in cc], "median": cont.named_steps["imputer"].statistics_.tolist(), "scaler_mean": cont.named_steps["scaler"].mean_.tolist(), "scaler_scale": cont.named_steps["scaler"].scale_.tolist(), "binary_names": [names[i] for i in bb], "mode": binary_imputer.statistics_.tolist()}
                fitted = model.named_steps["classifier"]
                record = {
                    "condition": condition, "held_family": fold.family,
                    "train_candidate_ids": [ids[i] for i in train],
                    "validation_candidate_ids": [ids[i] for i in test],
                    "preprocessing_fit_on_train_only_verified": True,
                    "statistics": statistics,
                    "coefficient": fitted.coef_[0].tolist(), "intercept": float(fitted.intercept_[0]),
                    "iterations": int(fitted.n_iter_[0]), "convergence_warnings": convergence,
                    "train_sample_count": len(train), "validation_count": len(test),
                }
                model_path = base / "models" / f"{condition}_{fold.family}.joblib"
                model_path.parent.mkdir(parents=True, exist_ok=True)
                assert not model_path.exists()
                joblib.dump(model, model_path, compress=3)
                model_index.append({"path": str(model_path.relative_to(base)), "sha256": sha(model_path), "condition": condition, "fold": fold.family, "final_model": False})
                fold_records.append(record)
            assert np.isfinite(scores).all() and np.isfinite(probabilities).all()
            for i, sid in enumerate(ids):
                output.append({
                    "candidate_id": sid, "condition": condition, "fold_id": metadata[i]["family"],
                    "raw_decision_score": float(scores[i]), "uncalibrated_probability": float(probabilities[i]),
                    "predicted_class": int(probabilities[i] >= config["config"]["threshold"]),
                    "run_id": config["run_id"],
                })
            execution[condition] = {"status": "EXECUTED", "OOF": 120, "folds": 13}
            new(base / "models" / f"{condition}_FOLD_TRAINING_RECORDS_V1.json", fold_records)
        except Exception as error:
            execution[condition] = {"status": "BLOCKED_RUNTIME", "reason": repr(error), "partial_folds": len(fold_records)}
            new(base / f"{condition}_EXECUTION_FAILURE_V1.json", execution[condition])
    prediction = base / "PREDICTIONS_LABEL_BLIND_LOCKED_V1.jsonl"
    with prediction.open("x", encoding="utf-8", newline="\n") as handle:
        for row in output:
            handle.write(json.dumps(row, ensure_ascii=False, allow_nan=False) + "\n")
    new(base / "PREDICTION_LOCK_V1.json", {
        "prediction_sha256": sha(prediction), "rows": len(output), "execution": execution,
        "models": model_index, "config_sha256": sha(base / "CONFIG_FREEZE_V1.json"),
        "preflight_sha256": sha(base / "PREFLIGHT_V1.json"),
        "code_source_lock_sha256": sha(base / args.source_lock),
        "label_roles_S_and_Oracle_mapping_loaded_in_this_process": False,
        "training_targets_from_signed_human_QA_vault": True,
        "locked_utc": datetime.now(timezone.utc).isoformat(),
    })
    print(json.dumps({"predictions_locked": len(output), "execution": execution}))


if __name__ == "__main__":
    main()
