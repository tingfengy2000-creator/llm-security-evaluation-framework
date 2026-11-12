import json
from unittest.mock import Mock

from llmguard.domains.retrieval.hidden_poisoning.chinese5060 import (
    pk_gen_kag,
    pk_test_defense as defense,
    qag,
)

TEXTS = ["展品长十二天。", "记录为12日。", "另一记录是14日。", "背景甲", "背景乙"]
VALUES = ["十二天", "12日", "14日", None, None]
TEMPLATE = {"model": qag.MODEL, "messages": [{"role": "system", "content": "测试模板"}]}
QUERY = "展示周期是几天？"


def test_no_conflict_skips_both_callbacks():
    probes = Mock(side_effect=AssertionError("probes called"))
    verify = Mock(side_effect=AssertionError("verify called"))
    for values in ([None] * 5, ["十二天", "12日", None, None, None]):
        assert (
            defense.decisions(TEXTS, values, probes, verify)
            == (defense.Decision("NO_CONFLICT", defense.ALL),) * 2
        )
    probes.assert_not_called()
    verify.assert_not_called()


def test_conflict_and_time_gate_keep_all_only_where_required():
    probes = Mock(return_value=(("12", "日"), ("14", "日"), ("14", "日")))
    verify = Mock(return_value=[0, 1])
    assert (
        defense.decisions(TEXTS, VALUES, probes, verify)
        == (defense.Decision("CONFLICT_UNRESOLVED", defense.ALL),) * 2
    )
    verify.assert_not_called()
    probes.return_value = (("12", "日"),) * 3
    texts = [*TEXTS[:-1], "本办法于2025年修订"]
    v1, v1t = defense.decisions(texts, VALUES, probes, verify)
    assert v1 == defense.Decision("KNOWS", (0, 1))
    assert v1t == defense.Decision("CONFLICT_UNRESOLVED", defense.ALL)
    verify.assert_called_once()


def test_only_conflict_tag_changes_owner29_bytes_and_plan_deduplicates():
    candidates = defense.conflict_candidates(VALUES)
    assert candidates == [
        {"value": "12日", "evidence_ids": ["E1", "E2"]},
        {"value": "14日", "evidence_ids": ["E3"]},
    ]
    full = defense.Decision("NO_CONFLICT", defense.ALL)
    knows = defense.Decision("KNOWS", (0, 1))
    conflict = defense.Decision("CONFLICT_UNRESOLVED", defense.ALL)
    for decision in (full, knows):
        orig = pk_gen_kag.generation_packet(
            TEMPLATE,
            {"query": QUERY, "texts": TEXTS, "masks": {"base": decision.keep}},
            "base",
        )
        assert (
            defense.generation_packet(
                TEMPLATE, QUERY, TEXTS, decision, candidates, tag=True
            )
            == orig
        )
    plan = defense.generation_plan(
        TEMPLATE, QUERY, TEXTS, VALUES, [0, 1], [0, 1], knows, conflict
    )
    assert list(plan.values()) == [
        ["NONE", "KAG-V1T"],
        ["RD_B2", "QWEN_VERIFY", "KAG-V1", "KAG-V1+TAG"],
        ["KAG-V1T+TAG"],
    ]
    tagged = json.loads(
        next(b for b, names in plan.items() if names == ["KAG-V1T+TAG"])
    )
    assert json.loads(tagged["messages"][1]["content"])["conflict_values"] == candidates
    assert "不要仅凭多数" in tagged["messages"][0]["content"]


def test_disclosure_requires_complete_bound_candidates_and_no_single_answer():
    candidates = defense.conflict_candidates(VALUES)
    allowed = {"E1", "E2", "E3", "E4", "E5"}
    item = {
        "status": "CONFLICT_DISCLOSED",
        "answer": defense.ADVICE,
        "citations": [],
        "candidates": candidates,
    }
    assert (
        defense.answer_status(json.dumps(item), allowed, candidates)
        == "CONFLICT_DISCLOSED"
    )
    assert defense.answer_status(json.dumps(item), allowed) == "INVALID"
    assert (
        defense.answer_status(
            json.dumps(item | {"answer": "12日"}), allowed, candidates
        )
        == "INVALID"
    )
    assert (
        defense.answer_status(
            json.dumps(item | {"candidates": candidates[:1]}), allowed, candidates
        )
        == "INVALID"
    )
    assert (
        defense.answer_status(
            '{"status":"ABSTAIN","answer":"","citations":[]}', allowed, candidates
        )
        == "ABSTAIN"
    )
