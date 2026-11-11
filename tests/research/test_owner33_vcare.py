from llmguard.domains.retrieval.hidden_poisoning.chinese5060.owner31_qcer import Query
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.owner33_vcare import (
    budget,
    intent,
    lookup,
    trigger,
    verify,
)

QUERY = Query(
    "上海居民按全国规定问端午节法定假日",
    "2025-07-01",
    "国定",
    "上海居民",
    "端午节法定假日",
)
SOURCE = {
    "entity": "端午节",
    "attribute": "statutory_days",
    "value": 2,
    "scope": "NATIONAL_PUBLIC",
    "effective_from": "2025-01-01",
    "effective_to_exclusive": None,
    "evidence_sha256": "fictional",
}
GOOD = "端午节法定假日为两天。"
WRONG = "端午节法定假日为五天。"


def test_reference_controls_and_scope() -> None:
    q = intent(QUERY)
    anchor = lookup([SOURCE], q)
    texts = [GOOD, WRONG, "北京居民端午节法定假日为两天。"]
    assert trigger(q, texts, (1,), (1,)) == "VISIBLE_CONFLICT"
    full = verify(q, texts, (1,), anchor, 1)
    assert full.keep == (0,)
    assert full.codes == (
        "RESTORE_BOUND_REFERENCE_AGREEMENT",
        "DROP_BOUND_CONFLICT",
        "OUTSIDE_OR_UNRESOLVED_B2",
    )
    assert verify(q, texts, (1,), anchor, 1, edit=False).keep == (1,)
    assert verify(q, texts, (1,), anchor, 1, rescue=False).keep == ()
    assert verify(q, texts, (1,), anchor, 1, scope=False).keep == (0, 2)
    assert budget(texts, full.keep, anchor) <= 4096


def test_no_anchor_no_change_and_history_remains() -> None:
    q = intent(QUERY)
    old = "自2014年1月1日起端午节法定假日为五天。"
    assert verify(q, [GOOD, old], (1,), None, 1).keep == (1,)
    assert verify(q, [GOOD, old], (1,), SOURCE, 1).keep == (0, 1)
    assert lookup([SOURCE, SOURCE], q) is None
    assert lookup([{**SOURCE, "effective_to_exclusive": QUERY.event_date}], q) is None


def test_first_application_and_scope_cannot_be_filled_by_age_atom() -> None:
    q = Query(
        "普通人首次申领大型客车", "2025-07-01", "首次", "上海普通人", "大型客车申领年龄"
    )
    assert intent(q) is None
    assert verify(None, [WRONG], (0,), SOURCE, 1).keep == (0,)
