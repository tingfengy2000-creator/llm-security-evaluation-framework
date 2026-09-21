from __future__ import annotations

import argparse
import json
from pathlib import Path

import pytest

from scripts.research.run_first_document_detector_preflight import (
    BINARY_FEATURES,
    LR_CONFIG,
    execute,
    freeze_missingness_policy,
    row_id,
    validate_feature_inputs,
    validate_groups,
)


def _feature(name: str) -> dict[str, object]:
    return {
        "feature_name": name,
        "missing_value_policy": "LEAVE_NULL; not a model feature",
    }


def test_all_missing_feature_is_blocking() -> None:
    feature_set = {
        "features": [_feature("host_publisher_relation")],
        "excluded_oracle_features": [],
        "retrieval_behavior_included": False,
        "selection_used_performance": False,
    }
    matrix = [
        {"feature_row_id": "FR-a", "features": {"host_publisher_relation": None}},
        {"feature_row_id": "FR-b", "features": {"host_publisher_relation": None}},
    ]
    decision = freeze_missingness_policy(feature_set, matrix)[0]
    assert decision.blocking is True
    assert decision.fold_local_policy == "UNRESOLVED_ALL_MISSING_NO_NEUTRAL_VALUE"


def test_observed_binary_uses_fold_local_mode() -> None:
    name = next(iter(BINARY_FEATURES))
    feature_set = {
        "features": [_feature(name)],
        "excluded_oracle_features": [],
        "retrieval_behavior_included": False,
        "selection_used_performance": False,
    }
    matrix = [
        {"feature_row_id": "FR-a", "features": {name: True}},
        {"feature_row_id": "FR-b", "features": {name: None}},
    ]
    decision = freeze_missingness_policy(feature_set, matrix)[0]
    assert decision.blocking is False
    assert decision.fold_local_policy == "TRAIN_FOLD_MODE"
    assert decision.scaler_policy == "NO_SCALER"


def test_continuous_uses_fold_local_median_and_scaler() -> None:
    feature_set = {
        "features": [_feature("semantic_version_margin")],
        "excluded_oracle_features": [],
        "retrieval_behavior_included": False,
        "selection_used_performance": False,
    }
    matrix = [
        {"feature_row_id": "FR-a", "features": {"semantic_version_margin": 0.2}},
        {"feature_row_id": "FR-b", "features": {"semantic_version_margin": None}},
    ]
    decision = freeze_missingness_policy(feature_set, matrix)[0]
    assert decision.fold_local_policy == "TRAIN_FOLD_MEDIAN"
    assert decision.scaler_policy == "TRAIN_FOLD_STANDARD_SCALER"


def test_frozen_lr_has_no_search_or_calibration() -> None:
    assert LR_CONFIG == {
        "estimator": "LogisticRegression",
        "penalty": "l2",
        "C": 1.0,
        "solver": "liblinear",
        "max_iter": 2000,
        "class_weight": "balanced",
        "random_state": 20260921,
        "hyperparameter_search": False,
        "probability_semantics": "UNCALIBRATED_MODEL_PROBABILITY",
    }


def test_feature_validator_rejects_label_keys() -> None:
    feature_set = {
        "features": [_feature("semantic_version_margin")],
        "excluded_oracle_features": [],
        "retrieval_behavior_included": False,
        "selection_used_performance": False,
    }
    matrix = [
        {
            "feature_row_id": "FR-a",
            "target": 1,
            "features": {"semantic_version_margin": 0.1},
        }
    ]
    result = validate_feature_inputs(feature_set, matrix)
    assert result["checks"]["forbidden_top_level_keys_zero"] is False


def test_group_validator_builds_24_logo_folds() -> None:
    candidates = []
    matrix = []
    aliases = ["CLEAN_CURRENT", "POISON_CANDIDATE", "MATCHED_HARD_NEGATIVE"]
    for group_index in range(24):
        for class_name in aliases:
            text = f"candidate-{group_index}-{class_name}"
            candidates.append(
                {
                    "sample_id": f"S-{group_index}-{class_name}",
                    "triplet_id": f"G-{group_index:02d}",
                    "phase1_view": {"candidate_text": text},
                    "owner_only": {"candidate_kind": class_name},
                }
            )
            matrix.append({"feature_row_id": row_id(text), "features": {}})
    result = validate_groups(candidates, matrix)
    assert result["pass"] is True
    assert len(result["fold_plan"]) == 24
    assert all(row["train_candidate_count"] == 69 for row in result["fold_plan"])
    assert all(row["validation_candidate_count"] == 3 for row in result["fold_plan"])


def test_execute_gate_remains_machine_readable(tmp_path: Path) -> None:
    payload = {
        "blocking_gates_pass": False,
        "blocking_features": [{"feature_name": "host_publisher_relation"}],
    }
    target = tmp_path / "preflight"
    target.mkdir()
    (target / "PAPER1_FIRST_DOCUMENT_DETECTOR_PREFLIGHT_V1.json").write_text(
        json.dumps(payload), encoding="utf-8"
    )
    loaded = json.loads(
        (target / "PAPER1_FIRST_DOCUMENT_DETECTOR_PREFLIGHT_V1.json").read_text(
            encoding="utf-8"
        )
    )
    assert loaded["blocking_gates_pass"] is False
    assert loaded["blocking_features"][0]["feature_name"] == "host_publisher_relation"
    with pytest.raises(RuntimeError, match="PHASE_B_BLOCKED_BY_PREFLIGHT"):
        execute(argparse.Namespace(output=tmp_path))


@pytest.mark.parametrize("name", ["host_publisher_relation", "publisher_issuer_match"])
def test_known_all_missing_features_are_binary(name: str) -> None:
    assert name in BINARY_FEATURES
