"""Synthetic mechanical tests; not a factual endorsement of any real item."""

from __future__ import annotations

import pytest

from llmguard.domains.retrieval.hidden_poisoning.method_engineering.development_gate import (
    all_fold_statistics_observed,
    require_owner_signature,
    validate_numeric_features,
    validate_recommendation_pairs,
)


def test_null_recommendation_is_not_filled() -> None:
    rows = [{"candidate_id": "X", "field": "overall_fact_status", "AI_suggestion": None}]
    assert validate_recommendation_pairs(rows) == (0, 1)
    assert rows[0]["AI_suggestion"] is None


@pytest.mark.parametrize("value", ["CURRENTLY_CONSISTENT", "FACTUAL_CONFLICT"])
def test_frozen_enum(value: str) -> None:
    assert validate_recommendation_pairs(
        [{"candidate_id": "X", "field": "overall_fact_status", "AI_suggestion": value}]
    ) == (1, 0)


@pytest.mark.parametrize("field,value", [("unknown", None), ("overall_fact_status", "SAFE")])
def test_reject_undefined_fields_or_values(field: str, value: object) -> None:
    with pytest.raises(ValueError):
        validate_recommendation_pairs(
            [{"candidate_id": "X", "field": field, "AI_suggestion": value}]
        )


def test_duplicate_pair_rejected() -> None:
    row = {"candidate_id": "X", "field": "overall_fact_status", "AI_suggestion": None}
    with pytest.raises(ValueError):
        validate_recommendation_pairs([row, row])


@pytest.mark.parametrize("value", [None, 0.0, 1.0, -0.5])
def test_numeric_null_not_zero(value: float | None) -> None:
    validate_numeric_features({"signal": value}, ["signal"])


@pytest.mark.parametrize("name", ["label", "candidate_id", "group_id", "evidence_selection"])
def test_metadata_not_model_features(name: str) -> None:
    with pytest.raises(ValueError):
        validate_numeric_features({name: 1.0}, [name])


@pytest.mark.parametrize("value", [float("nan"), float("inf"), "YES"])
def test_invalid_numeric(value: object) -> None:
    with pytest.raises(ValueError):
        validate_numeric_features({"signal": value}, ["signal"])


def test_frozen_order_required() -> None:
    with pytest.raises(ValueError):
        validate_numeric_features({"b": 1.0, "a": 2.0}, ["a", "b"])


def test_install_approval_cannot_open_data_gate() -> None:
    for receipt in [None, {"runtime_install_approved": True, "max_gib": 4}]:
        with pytest.raises(PermissionError):
            require_owner_signature(receipt, eligibility_sha256="abc")


def test_specific_complete_development_signature() -> None:
    receipt = {
        "eligibility_sha256": "abc", "owner_signed": True, "scope": "D1_DEV_ONLY",
        "owner_name": "Owner", "signed_date": "2026-10-27",
        "whole_group_holds_retained": True, "applicable_QA_overlay_confirmed": True,
    }
    require_owner_signature(receipt, eligibility_sha256="abc")
    with pytest.raises(PermissionError):
        require_owner_signature(receipt, eligibility_sha256="different")


def test_test_fold_observations_do_not_rescue_train_missingness() -> None:
    assert all_fold_statistics_observed(
        [{"t": 0.2}, {"t": None}, {"t": None}], ["A", "B", "C"], ["t"]
    ) == {"A": ("t",), "B": (), "C": ()}


def test_family_alignment_fail_closed() -> None:
    with pytest.raises(ValueError):
        all_fold_statistics_observed([{"t": 0.1}], [], ["t"])
