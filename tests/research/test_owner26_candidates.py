from dataclasses import replace

import pytest

from llmguard.domains.retrieval.hidden_poisoning.chinese5060.owner26_candidates import (
    Claim,
    bound_span,
    m1,
    m2,
    parse_extraction,
    parse_verify,
)


def claim(value: str, scope: str = "北室") -> Claim:
    text = scope + value + "天"
    return Claim(bound_span(text, value + "天", 2, len(text)), value, "天", "numeric",
                 bound_span(text, scope, 0, 2), None, None)


def test_literal_utf8_and_verifier_rejects_wrong_rank_or_bool() -> None:
    span = bound_span("北室三天", "三天", 2, 4)
    assert (span.byte_start, span.byte_end) == (6, 12)
    suspect = {"rank": 1, "quote": "三天", "start": 2, "end": 4, "reason": "假设控制"}
    chunks = ["北室三天", "南室九天", "甲", "乙", "丙"]
    assert parse_verify({"suspects": [suspect]}, chunks) == ("OK", (1,))
    for bad in ({**suspect, "rank": True}, {**suspect, "rank": 2}):
        assert parse_verify({"suspects": [bad]}, chunks) == ("ERROR_KEEP_ALL", ())


def test_extraction_requires_value_unit_scope_and_exact_quote() -> None:
    text = "北室三天"
    row = {"normalized_value": "三", "unit": "天", "answer_type": "numeric", "negation": False,
           "answer_quote": "三天", "character_start": 2, "character_end": 4,
           "scope": {"quote": "北室", "start": 0, "end": 2},
           "condition": None, "effective_date_or_version": None}
    assert parse_extraction({"status": "ANSWER", "claims": [row]}, text)[0] == "ANSWER"
    for change in ({"normalized_value": "九"}, {"scope": None}, {"negation": True}, {"character_start": 1}):
        assert parse_extraction({"status": "ANSWER", "claims": [{**row, **change}]}, text)[0] == "UNKNOWN"


def test_m1_false_consensus_reinclusion_is_a_counterexample() -> None:
    poison = claim("9")
    assert m1({1}, {1: poison, 2: poison, 3: claim("9", "南室")}) == {1, 2}
    versioned = replace(poison, version=bound_span("第九版", "第九版", 0, 3))
    assert m1({1}, {1: poison, 2: versioned}) == {1}
    assert m1({1, 3}, {1: poison, 2: poison, 3: claim("7")}) == {1, 3}


@pytest.mark.parametrize("poison_count", [3, 4, 5])
def test_m2_majority_without_independence_and_compromised_sources(poison_count: int) -> None:
    ranks = set(range(1, 6))
    claims = {i: claim("9" if i <= poison_count else "7") for i in ranks}
    texts = {i: f"北室说明第{i}段，限{claims[i].value}天。" for i in ranks}
    assert m2(ranks, claims, texts, {}) == (ranks, "SOURCE_CORRELATION_UNKNOWN")
    identities = {i: str(i) for i in ranks}
    keep, state = m2(ranks, claims, texts, identities)
    assert state == "MAJORITY_FILTERED"
    assert keep == set(range(1, poison_count + 1))
    duplicate_text = {i: texts[1] if i <= poison_count else texts[i] for i in ranks}
    expected = {4, 5} if poison_count == 3 else ranks
    assert m2(ranks, claims, duplicate_text, identities)[0] == expected
