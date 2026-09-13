from __future__ import annotations

from scripts.research.lock_pilot4_ab_phase2_returns import (
    cohen_kappa,
    exact_agreement,
    field_agreement,
)


def test_cohen_kappa_perfect_non_degenerate_agreement() -> None:
    assert cohen_kappa(["A", "B", "A"], ["A", "B", "A"]) == 1.0


def test_cohen_kappa_reports_unestimable_constant_marginals() -> None:
    assert cohen_kappa(["A", "A"], ["A", "A"]) is None


def test_field_and_exact_agreement_are_deterministic() -> None:
    a_rows = {"s1": {"field": "A"}, "s2": {"field": "B"}}
    b_rows = {"s1": {"field": "A"}, "s2": {"field": "A"}}

    metric = field_agreement(a_rows, b_rows, "field")
    exact, disagreements = exact_agreement(a_rows, b_rows, ("field",))

    assert metric["matches"] == 1
    assert metric["disagreements"] == 1
    assert metric["confusion_matrix_a_rows_b_columns"]["B"]["A"] == 1
    assert exact == 1
    assert disagreements == ["s2"]
