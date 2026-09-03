from __future__ import annotations

import copy

import pytest

from scripts.research.build_pilot4_expected_v3_recompute import (
    CORRECTION_SPECS,
    RESIDUAL_DISPOSITIONS,
    _agreement,
    _diff_expected_rows,
)


def test_expected_v3_scope_is_exactly_seven_fields_on_six_candidates() -> None:
    assert len(CORRECTION_SPECS) == 7
    assert len({item["sample_id"] for item in CORRECTION_SPECS}) == 6
    assert len({(item["sample_id"], item["field"]) for item in CORRECTION_SPECS}) == 7


def test_expected_v3_scope_contains_only_owner_authorized_candidates() -> None:
    assert {item["sample_id"] for item in CORRECTION_SPECS} == {
        "P4Q-b4bb1a9b722b",
        "P4Q-afb8936eb07e",
        "P4Q-1affdb97e391",
        "P4Q-8f3f3210e05b",
        "P4Q-3bd40af7ed77",
        "P4Q-d1cea30f62e3",
    }


def test_each_correction_has_two_locked_evidence_hashes_and_independent_reason() -> (
    None
):
    for item in CORRECTION_SPECS:
        assert set(item["evidence"]) == {"E1", "E2"}
        assert all(len(value) == 64 for value in item["evidence"].values())
        assert item["reason"]
        assert item["guide_rule"].startswith("V3.2")


def test_residuals_are_only_two_nonblocking_reviewer_variances() -> None:
    assert len(RESIDUAL_DISPOSITIONS) == 2
    assert all(
        item["taxonomy"] == "R3-M1 REVIEWER_VARIANCE"
        for item in RESIDUAL_DISPOSITIONS.values()
    )
    assert (
        max(
            list(item["root_cause"] for item in RESIDUAL_DISPOSITIONS.values()).count(
                root
            )
            for root in {item["root_cause"] for item in RESIDUAL_DISPOSITIONS.values()}
        )
        == 2
    )


def test_control_threshold_is_exact_fraction_not_rounding() -> None:
    assert _agreement(14, 16)["fraction"] == 0.875
    assert _agreement(14, 16)["agree"] < 15
    assert _agreement(15, 16)["agree"] >= 15


def test_row_diff_detects_only_changed_fields() -> None:
    before = [{"sample_id": "P4Q-a", "field_a": "OLD", "field_b": "SAME"}]
    after = copy.deepcopy(before)
    after[0]["field_a"] = "NEW"
    assert _diff_expected_rows(before, after) == [
        {
            "sample_id": "P4Q-a",
            "field": "field_a",
            "old_value": "OLD",
            "new_value": "NEW",
        }
    ]


def test_row_diff_fails_closed_on_candidate_set_change() -> None:
    with pytest.raises(ValueError, match="EXPECTED_V3_CANDIDATE_SET_MUTATION_BLOCKER"):
        _diff_expected_rows(
            [{"sample_id": "P4Q-a", "field": "OLD"}],
            [{"sample_id": "P4Q-b", "field": "OLD"}],
        )
