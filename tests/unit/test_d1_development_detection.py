"""Synthetic family/metric boundary tests, not real D1 performance."""

from __future__ import annotations

import math

import pytest

from llmguard.domains.retrieval.hidden_poisoning.method_engineering.development_detection import (
    BINARY_FEATURES,
    TEMPORAL_FEATURES,
    family_folds,
    numeric_fold_preflight,
    poison_counts,
    wilson_interval,
)


def test_frozen_semantic_feature_types() -> None:
    assert len(BINARY_FEATURES) == 14
    assert len(TEMPORAL_FEATURES) == 3
    assert not BINARY_FEATURES & TEMPORAL_FEATURES


def test_complete_family_isolation_and_oof() -> None:
    families = ["A"] * 6 + ["B"] * 3 + ["C"] * 3
    groups = ["g1"] * 3 + ["g2"] * 3 + ["g3"] * 3 + ["g4"] * 3
    folds = family_folds(families, groups)
    assert len(folds) == 3
    assert sorted(i for fold in folds for i in fold.validation) == list(range(12))
    for fold in folds:
        assert not set(groups[i] for i in fold.train) & set(groups[i] for i in fold.validation)


def test_group_cannot_cross_family() -> None:
    with pytest.raises(ValueError):
        family_folds(["A", "B"], ["g", "g"])


@pytest.mark.parametrize("families,groups", [([], []), (["A"], []), (["A"], ["g"])])
def test_invalid_fold_inputs(families: list[str], groups: list[str]) -> None:
    with pytest.raises(ValueError):
        family_folds(families, groups)


def test_train_only_missingness_and_zero_is_observed() -> None:
    folds = family_folds(["A", "B", "C"], ["a", "b", "c"])
    rows: list[dict[str, float | None]] = [{"signal": 0.0}, {"signal": None}, {"signal": None}]
    assert numeric_fold_preflight(rows, ["signal"], folds) == {
        "A": ("signal",), "B": (), "C": (),
    }
    assert rows[1]["signal"] is None


def test_nonfinite_features_fail_closed() -> None:
    folds = family_folds(["A", "B"], ["a", "b"])
    with pytest.raises(ValueError):
        numeric_fold_preflight([{"x": math.nan}, {"x": 0.0}], ["x"], folds)


def test_frozen_order_required() -> None:
    folds = family_folds(["A", "B"], ["a", "b"])
    with pytest.raises(ValueError):
        numeric_fold_preflight([{"b": 0.0, "a": 1.0}] * 2, ["a", "b"], folds)


@pytest.mark.parametrize("tp,n", [(0, 12), (12, 12), (3, 13)])
def test_wilson_contains_observed_rate(tp: int, n: int) -> None:
    interval = wilson_interval(tp, n)
    assert interval is not None
    assert interval[0] <= tp / n + 1e-14
    assert interval[1] >= tp / n - 1e-14
    assert 0 <= interval[0] <= interval[1] <= 1


def test_wilson_missing_denominator_is_not_zero() -> None:
    assert wilson_interval(0, 0) is None
    with pytest.raises(ValueError):
        wilson_interval(3, 2)


def test_fixed_threshold_and_poison_denominator() -> None:
    assert poison_counts([1, 1, 0], [0.5, 0.49, 0.9], [True] * 3) == (1, 2, 0.5)
    assert poison_counts([0], [0.9], [True]) == (0, 0, None)


def test_metric_arrays_must_align() -> None:
    with pytest.raises(ValueError):
        poison_counts([1], [], [True])
