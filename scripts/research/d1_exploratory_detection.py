"""Fixed candidate-only development diagnostic with family-isolated fit.

Construction roles are not accepted by the fitting interface. They may be joined
by an evaluation caller only after the label-blind prediction file is locked.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer  # type: ignore[import-untyped]
from sklearn.linear_model import LogisticRegression  # type: ignore[import-untyped]
from sklearn.metrics import average_precision_score, roc_auc_score  # type: ignore[import-untyped]

SEED = 20261027
METHOD = "A_CANDIDATE_ONLY_CHAR23_TFIDF_LR_V1"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def new_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write("\n")


def fit_configuration() -> dict[str, Any]:
    return {
        "seed": SEED,
        "vectorizer": {
            "analyzer": "char",
            "ngram_range": [2, 3],
            "lowercase": False,
            "min_df": 1,
            "max_df": 1.0,
            "sublinear_tf": True,
            "norm": "l2",
        },
        "model": {
            "penalty": "l2",
            "C": 1.0,
            "solver": "liblinear",
            "max_iter": 2000,
            "class_weight": "balanced",
            "random_state": SEED,
        },
        "threshold": 0.5,
        "score": "decision_function",
        "probability": "UNCALIBRATED",
        "cv": "LEAVE_ONE_CANONICAL_FACT_FAMILY_OUT",
        "bootstrap": 2000,
        "bootstrap_unit": "CANONICAL_FACT_FAMILY",
        "hyperparameter_search": False,
    }


def family_folds(ids: list[str], families: dict[str, str]) -> list[dict[str, Any]]:
    if len(set(ids)) != len(ids) or set(ids) != set(families):
        raise ValueError("Family map and unique visible IDs must align exactly")
    if len(set(families.values())) < 2:
        raise ValueError("At least two independent families are needed")
    folds = []
    for n, family in enumerate(sorted(set(families.values())), 1):
        test = [i for i, ident in enumerate(ids) if families[ident] == family]
        train = [i for i, ident in enumerate(ids) if families[ident] != family]
        if {families[ids[i]] for i in train} & {families[ids[i]] for i in test}:
            raise ValueError("Family leakage")
        folds.append(
            {"fold_id": f"F{n:02d}", "train_indices": train, "test_indices": test}
        )
    if Counter(i for fold in folds for i in fold["test_indices"]) != Counter(
        range(len(ids))
    ):
        raise ValueError("Each sample must be held out exactly once")
    return folds


def predict_oof(
    visible: list[dict[str, str]],
    training_targets: dict[str, int],
    folds: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if any(set(r) != {"candidate_id", "candidate_text"} for r in visible):
        raise ValueError(
            "Only opaque ID and Candidate text accepted by feature interface"
        )
    ids = [r["candidate_id"] for r in visible]
    if set(training_targets) != set(ids) or any(
        v not in (0, 1) for v in training_targets.values()
    ):
        raise ValueError("Training-fold provisional targets must align exactly")
    predictions, models = {}, []
    config = fit_configuration()
    for fold in folds:
        train, test = fold["train_indices"], fold["test_indices"]
        if set(train) & set(test) or set(train) | set(test) != set(range(len(ids))):
            raise ValueError("Invalid disjoint fold partition")
        # No validation target is read by the vectorizer, classifier fit or predict.
        y_train = np.asarray([training_targets[ids[i]] for i in train], dtype=np.int64)
        if len(set(y_train)) != 2:
            raise ValueError("Both training classes are required in every fold")
        vc = dict(config["vectorizer"])
        vc["ngram_range"] = tuple(vc["ngram_range"])
        vectorizer = TfidfVectorizer(**vc)
        x_train = vectorizer.fit_transform(
            [visible[i]["candidate_text"] for i in train]
        )
        x_test = vectorizer.transform([visible[i]["candidate_text"] for i in test])
        classifier = LogisticRegression(**config["model"])
        classifier.fit(x_train, y_train)
        probabilities = classifier.predict_proba(x_test)[:, 1]
        raw = classifier.decision_function(x_test)
        coefficients = (
            classifier.coef_.astype("<f8").tobytes()
            + classifier.intercept_.astype("<f8").tobytes()
        )
        vocab = json.dumps(
            {k: int(v) for k, v in vectorizer.vocabulary_.items()},
            sort_keys=True,
            ensure_ascii=False,
        ).encode()
        model_id = "A-" + sha(coefficients + vocab)[:20]
        models.append(
            {
                "fold_id": fold["fold_id"],
                "model_id": model_id,
                "training_ids": [ids[i] for i in train],
                "held_out_ids": [ids[i] for i in test],
                "vocabulary_sha256": sha(vocab),
                "vocabulary_size": len(vectorizer.vocabulary_),
                "coefficient_sha256": sha(coefficients),
                "max_abs_coefficient": float(np.max(np.abs(classifier.coef_))),
                "n_iter": int(classifier.n_iter_[0]),
                "imputer_used": False,
                "vectorizer_fit_scope": "TRAIN_FAMILIES_ONLY",
                "threshold": 0.5,
            }
        )
        for j, idx in enumerate(test):
            if idx in predictions:
                raise ValueError("Repeated held-out sample")
            predictions[idx] = {
                "candidate_id": ids[idx],
                "method": METHOD,
                "fold_id": fold["fold_id"],
                "raw_prediction_score": float(raw[j]),
                "oof_probability": float(probabilities[j]),
                "oof_prediction": int(probabilities[j] >= 0.5),
                "model_id": model_id,
                "feature_availability": {
                    "candidate_text": True,
                    "nonzero_tfidf_features": int(x_test[j].nnz),
                },
                "retrieved_evidence_identity": [],
                "evidence_setting": "CANDIDATE_ONLY",
            }
    if len(predictions) != len(ids):
        raise ValueError("Incomplete OOF coverage")
    return [predictions[i] for i in range(len(ids))], models


def lock_predictions(path: Path, predictions: list[dict[str, Any]]) -> dict[str, Any]:
    forbidden = {
        "label",
        "target",
        "true_class",
        "construction_role",
        "group_id",
        "family",
        "derived_s",
        "hkp",
    }

    def contaminated(value: Any) -> bool:
        if isinstance(value, dict):
            return bool(set(value) & forbidden) or any(
                contaminated(v) for v in value.values()
            )
        return isinstance(value, list) and any(contaminated(v) for v in value)

    if contaminated(predictions):
        raise ValueError("Evaluation metadata cannot enter the prediction lock")
    raw = "".join(
        json.dumps(r, ensure_ascii=False, sort_keys=True, allow_nan=False) + "\n"
        for r in predictions
    ).encode()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(raw)
    result = {
        "path": path.name,
        "sha256": sha(raw),
        "rows": len(predictions),
        "locked_at_utc": datetime.now(timezone.utc).isoformat(),
        "construction_roles_loaded_for_evaluation": False,
    }
    new_json(path.with_suffix(".lock.json"), result)
    path.chmod(0o444)
    return result


def metrics(rows: list[dict[str, Any]]) -> dict[str, float | int | None]:
    result: dict[str, float | int | None] = {}
    positive = [r for r in rows if r["label"] == 1]
    negative = [r for r in rows if r["label"] == 0]
    for level in ("S1", "S2", "S3"):
        subset = [r for r in positive if r["derived_s"] == level]
        count = sum(r["oof_prediction"] == 1 for r in subset)
        result.update(
            {
                level + "_TP": count,
                level + "_N": len(subset),
                level + "_Recall": count / len(subset) if subset else None,
            }
        )
    hn = [r for r in rows if r["true_class"] == "HARD_NEGATIVE"]
    result["Overall_Recall"] = (
        sum(r["oof_prediction"] == 1 for r in positive) / len(positive)
        if positive
        else None
    )
    hn_fp = sum(r["oof_prediction"] == 1 for r in hn)
    result["HN_FP"] = hn_fp
    result["HN_N"] = len(hn)
    result["HN_FPR"] = hn_fp / len(hn) if hn else None
    result["AUROC"] = (
        float(
            roc_auc_score(
                [r["label"] for r in rows], [r["oof_probability"] for r in rows]
            )
        )
        if positive and negative
        else None
    )
    result["AUPRC"] = (
        float(
            average_precision_score(
                [r["label"] for r in rows], [r["oof_probability"] for r in rows]
            )
        )
        if positive
        else None
    )
    return result


def cluster_intervals(
    rows: list[dict[str, Any]], repetitions: int = 2000
) -> dict[str, Any]:
    families = sorted({r["family"] for r in rows})
    by_family = {f: [r for r in rows if r["family"] == f] for f in families}
    rng = np.random.default_rng(SEED)
    names = [
        "S1_Recall",
        "S2_Recall",
        "S3_Recall",
        "Overall_Recall",
        "HN_FPR",
        "AUROC",
        "AUPRC",
    ]
    draws: dict[str, list[float]] = {n: [] for n in names}
    for _ in range(repetitions):
        sample = [
            r
            for f in rng.choice(families, size=len(families), replace=True)
            for r in by_family[f]
        ]
        values = metrics(sample)
        for n in names:
            value = values[n]
            if value is not None:
                draws[n].append(float(value))
    return {
        n: {
            "lower": float(np.quantile(v, 0.025)) if v else None,
            "upper": float(np.quantile(v, 0.975)) if v else None,
            "valid_resamples": len(v),
            "requested_resamples": repetitions,
        }
        for n, v in draws.items()
    }
