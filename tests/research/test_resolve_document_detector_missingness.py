"""Focused tests for the Owner-approved provenance A→C repair gate."""

from __future__ import annotations

from typing import Any

import pytest

from scripts.research.resolve_document_detector_missingness import (
    BLOCKED,
    metadata_audit,
    post_lock_preflight,
    project_v1_to_c,
    row_id,
)


def _feature_set() -> dict[str, Any]:
    names = [*BLOCKED, *(f"feature_{i:02d}" for i in range(21))]
    return {
        "features": [
            {"feature_name": name, "view": "PROVENANCE"}
            for name in names
        ],
        "retrieval_behavior_included": False,
        "selection_used_performance": False,
        "excluded_oracle_features": [],
    }


def _matrix() -> list[dict[str, Any]]:
    names = [row["feature_name"] for row in _feature_set()["features"]]
    return [
        {
            "feature_row_id": row_id(f"candidate-{i}"),
            "features": {name: None if name in BLOCKED else float(i) for name in names},
        }
        for i in range(72)
    ]


def test_option_c_is_exact_additive_projection() -> None:
    original = _matrix()
    new_set, projected = project_v1_to_c(_feature_set(), original)
    assert len(new_set["features"]) == 21
    assert len(projected) == 72
    assert new_set["exclusion_basis"] == "MEASURABILITY_ONLY_NO_LABEL_OR_PERFORMANCE_SELECTION"
    for before, after in zip(original, projected, strict=True):
        assert before["feature_row_id"] == after["feature_row_id"]
        assert after["features"] == {
            key: value for key, value in before["features"].items() if key not in BLOCKED
        }
        assert all(before["features"][name] is None for name in BLOCKED)


def test_option_c_rejects_observed_deferred_value() -> None:
    original = _matrix()
    original[0]["features"][BLOCKED[0]] = 1.0
    with pytest.raises(ValueError, match="all-missing"):
        project_v1_to_c(_feature_set(), original)


def test_metadata_roles_are_not_invented_candidate_features() -> None:
    corpus = [
        {
            "evidence_doc_id": f"TED-{i}", "source_host": "official.example",
            "publisher": "Agency" if i == 0 else None,
            "issuer": "Agency" if i == 0 else None,
            "snapshot_id": f"SNAP-{i}", "snapshot_sha256": str(i),
            "metadata_source": "FROZEN_SNAPSHOT",
            "metadata_status": {"issuer": "SUPPORTED"},
        }
        for i in range(57)
    ]
    trace = [
        {"candidate_id": f"C-{candidate}", "evidence_doc_id": f"TED-{rank-1}", "rank": rank}
        for candidate in range(72) for rank in range(1, 6)
    ]
    audit, coverage = metadata_audit(corpus, trace)
    assert len(audit) == 72
    assert coverage["top5"]["publisher_and_issuer"] == 72
    assert all(row["publisher_issuer_same_doc_available"] for row in audit)
    assert all(row[BLOCKED[0]]["status"] == "INPUT_MISSING" for row in audit)
    assert all(row[BLOCKED[1]]["candidate_level_computable"] is False for row in audit)


def test_logo_fold_statistics_are_train_only() -> None:
    candidates = [
        {
            "sample_id": f"C-{i}", "triplet_id": f"G-{i//3}",
            "phase1_view": {"candidate_text": f"candidate-{i}"},
            "owner_only": {
                "candidate_kind": (
                    "CLEAN_CURRENT", "POISON_CANDIDATE", "MATCHED_HARD_NEGATIVE"
                )[i % 3],
                "domain": "test",
            },
        }
        for i in range(72)
    ]
    feature_set, matrix = project_v1_to_c(_feature_set(), _matrix())
    audit = [
        {"candidate_id": f"C-{i}", **{name: {"status": "INPUT_MISSING"} for name in BLOCKED}}
        for i in range(72)
    ]
    result = post_lock_preflight(candidates, matrix, feature_set, audit, "LOCKED")
    assert result["fold_count"] == 24
    assert result["all_fold_statistics_exist"]
    assert all(fold["train_candidates"] == 69 for fold in result["folds"])
    assert result["excluded_missingness_class_proxy"] is False
    for row in matrix[3:]:
        row["features"]["feature_00"] = None
    blocked = post_lock_preflight(candidates, matrix, feature_set, audit, "LOCKED")
    assert blocked["all_fold_statistics_exist"] is False
