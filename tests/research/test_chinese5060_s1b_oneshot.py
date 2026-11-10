from __future__ import annotations

from typing import Any

from llmguard.domains.retrieval.hidden_poisoning.chinese5060 import s1b_oneshot_adapter as adapter
from llmguard.domains.retrieval.hidden_poisoning.chinese5060 import s1b_oneshot_scoring as evaluator
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.s1b_feasibility_data import span


def support(text: str, outer: tuple[int, int], *cues: tuple[int, int]) -> dict[str, Any]:
    return {"window": span(text, *outer), "requires": [span(text, *x) for x in cues]}


def gold(*supports: dict[str, Any]) -> dict[str, Any]:
    return {"status": "ANSWER", "value": "7", "unit": "元", "document_title": "", "selector": "甲/费用",
            "accepted_span_sets": list(supports), "reason": None}


def result(text: str, candidate: dict[str, Any], *supports: dict[str, Any]) -> dict[str, Any]:
    return evaluator.score(adapter.project(candidate, text), gold(*supports), {"atoms": []}, text)


def test_equivalent_windows_and_cross_scope_same_scalar() -> None:
    text = "甲费用7元\n乙费用7元\n甲费用7元"
    a = support(text, (0, 5), (0, 3), (3, 5))
    b = support(text, (12, 17), (12, 15), (15, 17))
    for i, j in ((0, 5), (12, 17), (6, 11), (0, 17), (3, 5)):
        raw = {"status": "DECIDED", "value": "7.00", "unit": "元", "source_span": {"start": i, "end": j}}
        scored = result(text, raw, a, b)
        assert scored["value_hit"]
        assert scored["status"] == ("CORRECT" if (i, j) in {(0, 5), (12, 17)} else "WRONG")


def test_native_cross_paragraph_support_and_no_silent_widening() -> None:
    text = "甲接乙\n乙费用7元"
    proof = support(text, (0, 9), (0, 3), (4, 7), (7, 9))
    raw = {"status": "DECIDED", "value": "7", "unit": "元", "source_span": {"start": 7, "end": 9}}
    assert result(text, raw, proof)["status"] == "WRONG"
    candidate = {**raw, "rejections": [], "scope_spans": {"link": {"start": 0, "end": 3},
                                                          "clause": {"start": 4, "end": 9}}}
    assert result(text, {**raw, "candidates": [candidate]}, proof)["status"] == "CORRECT"
    assert result(text, {**raw, "candidates": [candidate, candidate]}, proof)["status"] == "WRONG"


def test_missing_span_and_malformed_utf8_report_separately() -> None:
    text = "🪶甲费用7元"
    raw = {"status": "DECIDED", "value": "7", "unit": "元"}
    assert "MISSING_SPAN" in result(text, raw, support(text, (1, 6), (1, 6)))["issues"]
    invalid = {**raw, "source_span": {"start": 1, "end": 6, "byte_start": 1}}
    record = adapter.invoke(lambda q, e: invalid, {"id": "fixture", "query": "?", "evidence": text})
    assert record["projection"]["status"] == "ERROR"
    assert record["raw"] == invalid


def test_exact_unit_and_zero_denominator() -> None:
    text = "甲费用7元"
    raw = {"status": "DECIDED", "value": "7", "unit": "万元", "source_span": {"start": 0, "end": 5}}
    assert result(text, raw, support(text, (0, 5), (0, 5)))["value_hit"] is False
    assert evaluator.rate(0, 0)["point"] is None
    assert evaluator.rate(0, 10)["wilson95"][1] > 0
