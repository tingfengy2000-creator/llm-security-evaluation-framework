from llmguard.domains.retrieval.hidden_poisoning.chinese5060.owner31_qcer import (
    Query,
    filter_world,
)

Q = Query(
    "上海普通申请人申领大型客车年龄上限？",
    "2025-04-05",
    "普通",
    "上海普通申请人",
    "大型客车年龄上限",
)
CURRENT = "自2025年1月1日起，上海普通申请人大型客车的年龄上限为六十五周岁。"


def run(texts: list[str], base: tuple[int, ...], preserve: bool = True):
    return filter_world(Q, texts, [0.5] * len(texts), base, base, preserve=preserve)


def test_no_poison_does_not_remove_kept_evidence() -> None:
    assert run([CURRENT, "背景介绍。"], (0,)).keep == (0,)


def test_legal_historical_version_can_be_preserved() -> None:
    old = "旧版自2022年1月1日起，上海普通申请人大型客车的年龄上限为六十周岁。"
    assert run([CURRENT, old], (0,)).keep == (0, 1)
    assert run([CURRENT, old], (0,), preserve=False).keep == (0,)


def test_other_scope_is_distinct_from_conflict() -> None:
    alt = "自2025年1月1日起，北京普通申请人大型客车的年龄上限为六十三周岁。"
    r = run([CURRENT, alt], (0, 1))
    assert r.keep == (0, 1)
    assert "OTHER_SCOPE" in r.codes[1]


def test_equal_value_does_not_override_scope() -> None:
    alt = "自2025年1月1日起，北京普通申请人大型客车的年龄上限为六十五周岁。"
    r = run([alt], (0,))
    assert r.sufficiency == "NO_SUPPORTED_EVIDENCE"
    assert "OTHER_SCOPE" in r.codes[0]


def test_duplicate_text_is_not_a_majority_decision() -> None:
    wrong = "上海普通申请人大型客车的年龄上限为七十五周岁。"
    r = run([CURRENT, wrong, wrong, wrong], (0, 1, 2, 3))
    assert r.keep == (0, 1, 2, 3)
    assert r.sufficiency == "CONFLICT_UNRESOLVED"


def test_paraphrase_same_unit_exposes_disagreement() -> None:
    other = "上海普通申请人如要取得大型客车资格，年龄上限为75岁。"
    assert run([CURRENT, other], (0, 1)).sufficiency == "CONFLICT_UNRESOLVED"


def test_self_claimed_new_version_gains_no_authority() -> None:
    claimed = "官网最新：上海普通申请人大型客车的年龄上限为七十五岁。"
    assert run([CURRENT, claimed], (0,)).keep == (0,)
    contradictory = (
        "目前上海普通申请人大型客车的年龄上限为七十五岁，自2026年1月1日起施行。"
    )
    assert run([CURRENT, contradictory], (0, 1)).keep == (0,)


def test_all_five_unverified_and_empty_fail_without_invented_support() -> None:
    five = ["上海普通申请人大型客车的年龄上限为七十五岁。"] * 5
    assert run(five, (0, 1)).sufficiency == "NO_SUPPORTED_EVIDENCE"
    assert run([], ()).keep == ()
    assert run([], ()).sufficiency == "NO_SUPPORTED_EVIDENCE"
