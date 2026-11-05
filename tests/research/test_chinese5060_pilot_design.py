import hashlib
import json

import pytest

from llmguard.domains.retrieval.hidden_poisoning.chinese5060.pilot_design import canonical_hash, length_plan, messages, select_contexts


def chunks():
    return [{"chunk_id": str(i), "text": "虚构原文", "content_hash": hashlib.sha256("虚构原文".encode()).hexdigest()} for i in range(5)]


def test_no_evaluation_metadata_accepted_in_runtime_context():
    with pytest.raises(ValueError, match="NEUTRAL_CONTEXT_SHAPE"):
        messages("原问题", [{"id": "C1", "text": "原文", "expected_answer": "SECRET"}])


def test_deletion_preserves_original_citation_ids_order_and_text():
    contexts = select_contexts(chunks(), [1, 3], ["0", "2", "4"])
    assert [r["id"] for r in contexts] == ["C1", "C3", "C5"]
    value = messages("原问题", contexts)
    assert json.loads(value[1]["content"]) == {"question": "原问题", "context": contexts}


def test_freeze_drift_is_not_silently_repaired():
    with pytest.raises(ValueError, match="RETAINED_ORDER"):
        select_contexts(chunks(), [], ["4", "3", "2", "1", "0"])
    data = chunks()
    data[0]["text"] = "变更"
    with pytest.raises(ValueError, match="SOURCE_TEXT_DRIFT"):
        select_contexts(data, [], ["0", "1", "2", "3", "4"])


def test_empty_context_can_be_designed_without_provider_call():
    assert select_contexts(chunks(), list(range(5)), []) == []
    assert len(messages("原问题", [])) == 2


def test_proxy_overflow_is_marked_and_exact_tokens_remain_unknown():
    plan = length_plan(messages("原问题", [{"id": "C1", "text": "文" * 2000}]))
    assert plan["proxy_over_4096"] and plan["exact_model_tokens"] is None
    assert canonical_hash(messages("原问题", [])) != canonical_hash(messages("另一问题", []))
