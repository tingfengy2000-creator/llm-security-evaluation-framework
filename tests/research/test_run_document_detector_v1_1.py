"""Regression checks for the prespecified Final72 detector execution contract."""

from __future__ import annotations

import numpy as np
import pytest

from scripts.research.run_document_detector_v1_1 import (
    fold_indices,
    matched,
    metrics,
    pipeline,
    recall_at_fpr,
)


def _rows() -> list[dict]:
    return [
        {"sample_id": f"s-{g}-{kind}", "group_id": f"g-{g}", "true_class": kind,
         "target": int(kind == "POISON_CANDIDATE"), "features": {"x": float(g)}}
        for g in range(24)
        for kind in ("CLEAN_CURRENT", "POISON_CANDIDATE", "MATCHED_HARD_NEGATIVE")
    ]


def test_logo_is_24_whole_triplets() -> None:
    rows = _rows()
    folds = fold_indices(rows)
    assert len(folds) == 24
    assert all(len(train) == 69 and len(test) == 3 for _, train, test in folds)
    for group, train, test in folds:
        assert {rows[i]["group_id"] for i in test} == {group}
        assert group not in {rows[i]["group_id"] for i in train}


def test_matched_ties_are_not_wins() -> None:
    rows = _rows()
    scores = np.zeros(72)
    result = matched(rows, scores)
    assert result["poison_vs_hn"] == {
        "win": 0, "tie": 24, "loss": 0, "strict_pairwise_accuracy": 0.0,
    }
    assert result["poison_top_triplet_rate"] == 0.0


def test_preprocessor_statistics_are_train_only() -> None:
    x_train = np.asarray([[1.0, 0.0], [3.0, 1.0], [np.nan, 1.0], [5.0, 0.0]])
    y_train = np.asarray([0, 1, 0, 1])
    model = pipeline(["continuous", "binary"], ["binary"], ["continuous"])
    model.fit(x_train, y_train)
    pre = model.named_steps["preprocess"]
    cont = pre.named_transformers_["continuous"]
    assert cont.named_steps["imputer"].statistics_[0] == 3.0
    assert cont.named_steps["scaler"].mean_[0] == 3.0
    _ = model.predict_proba(np.asarray([[10000.0, np.nan]]))
    assert cont.named_steps["imputer"].statistics_[0] == 3.0
    assert cont.named_steps["scaler"].mean_[0] == 3.0
    assert len(model.named_steps["classifier"].coef_[0]) == 2


def test_5_percent_fpr_is_discrete_without_interpolation() -> None:
    y = np.asarray([1, 1, *([0] * 48)])
    scores = np.asarray([0.9, 0.8, *np.linspace(0.7, 0.0, 48)])
    result = recall_at_fpr(y, scores, 0.05)
    assert result["max_false_positives"] == 2
    assert result["recall"] == 1.0


def test_hn_fpr_uses_hn_only() -> None:
    rows = _rows()
    y = np.asarray([r["target"] for r in rows])
    scores = np.asarray([0.0, 1.0, -1.0] * 24)
    probs = np.asarray([0.4, 0.6, 0.4] * 24)
    result = metrics(y, scores, probs, rows)
    assert result["hn_fpr_at_0_5"] == 0.0
    assert result["recall_at_1pct_fpr"] == "NOT_RELIABLY_ESTIMABLE_ON_FINAL72"


def test_missing_training_statistic_fails_closed() -> None:
    model = pipeline(["x"], [], ["x"])
    with pytest.raises(ValueError):
        # sklearn must not be given a one-class target.
        model.fit(np.asarray([[np.nan], [np.nan]]), np.asarray([0, 0]))
