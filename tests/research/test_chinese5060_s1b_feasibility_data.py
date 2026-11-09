from __future__ import annotations

import pytest

from llmguard.domains.retrieval.hidden_poisoning.chinese5060 import s1b_feasibility_data as prep


def test_dual_offsets_for_cjk_and_non_bmp() -> None:
    text = "🪶案卷七"
    evidence = prep.span(text, 1, 3)
    assert (evidence["byte_start"], evidence["byte_end"]) == (4, 10)
    assert text.encode()[4:10].decode() == "案卷"
    assert evidence["sha256"] == prep.sha("案卷".encode())


def test_linked_support_requires_scope_on_both_sides() -> None:
    atom, raw = prep.parse_atom("A~样本甲/加压组/静置时长~-~4~小时~样本甲加压组对应丁项。^丁项静置时长〔4小时〕。")
    block, support = prep.minimal_support("", atom, raw, 0)
    assert "〔" not in block
    assert prep.support_matches([(0, len(block))], support)
    pivot = block.index("\n")
    assert prep.support_matches([(0, pivot), (pivot + 1, len(block))], support)
    assert not prep.support_matches([(pivot + 1, len(block))], support)
    assert not prep.support_matches([(0, len(block) + 1)], support)
    assert not prep.support_matches([(0, len(block)), (pivot, len(block))], support)


def test_same_value_wrong_scope_cannot_satisfy_support() -> None:
    atom, raw = prep.parse_atom("A~仪器/左湾/用量~-~7~升~仪器在左湾使用，用量〔7升〕。")
    wrong_scope = "仪器在右湾使用，用量7升。\n"
    block, support = prep.minimal_support(wrong_scope, atom, raw, len(wrong_scope))
    value = len(wrong_scope) + block.index("7升")
    assert not prep.support_matches([(value, value + 2)], support)
    assert not prep.support_matches([(0, len(wrong_scope) - 1)], support)
    assert prep.support_matches([(len(wrong_scope), len(wrong_scope + block))], support)


def test_active_bounds_exact_scope_and_unverified_revision() -> None:
    state, _ = prep.parse_atom(
        "A~机具/试行版/限额~2024-02-01:2024-02-29~9~件~机具试行版限额〔9件〕，2024-02-01 至 2024-02-29。"
    )
    assert prep.applicable(state, "机具/试行版/限额", "2024-02-29")
    assert not prep.applicable(state, "机具/试行版/限额", "2024-03-01")
    assert not prep.applicable(state, "机具/旧版/限额", "2024-02-29")
    assert not prep.applicable({**state, "state": "U"}, "机具/试行版/限额", "2024-02-29")


def test_invalid_date_wrong_anchor_and_unsupported_tag_fail_closed() -> None:
    with pytest.raises(ValueError):
        prep.parse_atom("A~馆牌/重贴日~-~2025-02-29~DATE~馆牌重贴日〔2025-02-29〕。")
    with pytest.raises(ValueError, match="NO_VISIBLE_U_CUE"):
        prep.parse_atom("U~馆牌/新版/重贴费~-~4~元~馆牌新版重贴费〔4元〕。")
    atom, raw = prep.parse_atom("A~馆牌/重贴费~-~4~元~馆牌重贴费〔5元〕。")
    with pytest.raises(ValueError, match="VALUE_MARKER_MISMATCH"):
        prep.minimal_support("", atom, raw, 0)
