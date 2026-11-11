"""Fixture-only checks for the Owner28 one-shot scorer. No sealed labels."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_scorer():
    path = Path(__file__).resolve().parents[2] / "scripts/research/score_owner28_oneshot.py"
    spec = importlib.util.spec_from_file_location("score_owner28_oneshot", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_fixture_ratios_and_date_regex_do_not_touch_sealed_inputs() -> None:
    module = load_scorer()
    module.fixture_check()


def test_empty_denominator_is_not_applicable() -> None:
    module = load_scorer()
    empty = module.arm_rates(module.empty_roles(), module.empty_roles())
    assert empty["poison_retained"]["status"] == "NOT_APPLICABLE"
    assert empty["clean_false_delete"]["status"] == "NOT_APPLICABLE"
    assert empty["hn_false_delete"]["status"] == "NOT_APPLICABLE"
    assert empty["background_deleted"]["status"] == "NOT_APPLICABLE"
