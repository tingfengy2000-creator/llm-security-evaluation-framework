"""Fictional probes only; no real D1 text or data-dependent rule tuning."""
from __future__ import annotations

import pytest

from llmguard.domains.retrieval.hidden_poisoning.method_engineering.surface_baseline import (
    GENERAL,
    ORIGINAL,
    predict_surface,
)


def test_original_exact_lexical_transcription() -> None:
    assert [r.expression for r in ORIGINAL] == [r"既.*(?:又|也)", r"同时又|又是|又享有|同时允许", r"同一"]
    assert len(GENERAL) == 6


@pytest.mark.parametrize("text,flag", [
    ("甲既负责接收，也负责归档。", 1),  # Legitimate cue-bearing sentence is still flagged.
    ("同一对象拥有不同属性。", 1),
    ("甲同时允许两类合规申请。", 1),
    ("甲仅接收申请。", 0),
    ("甲既接收。\n乙也处理。", 0),
])
def test_original_means_surface_flag_not_factual_truth(text: str, flag: int) -> None:
    assert predict_surface(text, "A0-original")[0] == flag


@pytest.mark.parametrize("text", ["所有合规申请均可办理。", "无需提交附加材料。", "除甲类外均适用。"])
def test_general_legitimate_absolute_and_exception_cues(text: str) -> None:
    assert predict_surface(text, "A0-general")[0] == 1


def test_unknown_rule_set_fails() -> None:
    with pytest.raises(KeyError):
        predict_surface("甲", "unknown")


def test_deterministic_binary_output() -> None:
    a = predict_surface("甲允许且不允许同一项操作。", "A0-general")
    assert a == predict_surface("甲允许且不允许同一项操作。", "A0-general")
    assert a[0] in (0, 1) and isinstance(a[1], tuple)
