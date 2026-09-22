"""Strict comparator checks for the additive OOF evidence-reconstruction gate."""

from __future__ import annotations

import pytest

from scripts.research.reconstruct_detector_oof_v1_1 import TOLERANCE, check_equal


def test_tolerance_is_predeclared_and_strict() -> None:
    assert TOLERANCE == 1e-12
    check_equal({"metrics": {"auroc": 0.5}}, {"metrics": {"auroc": 0.5}}, "root")


def test_numeric_drift_fails_closed() -> None:
    with pytest.raises(ValueError, match="SUMMARY_NUMERIC_MISMATCH"):
        check_equal({"auroc": 0.50000000001}, {"auroc": 0.5}, "root")


def test_missing_machine_summary_field_fails_closed() -> None:
    with pytest.raises(ValueError, match="SUMMARY_STRUCTURE_MISMATCH"):
        check_equal({"metrics": {"auroc": 0.5}}, {"metrics": {"auroc": 0.5, "auprc": 0.3}}, "root")


def test_exact_categorical_and_count_identity() -> None:
    with pytest.raises(ValueError, match="SUMMARY_VALUE_MISMATCH"):
        check_equal({"win": 18, "status": "old"}, {"win": 19, "status": "old"}, "root")
