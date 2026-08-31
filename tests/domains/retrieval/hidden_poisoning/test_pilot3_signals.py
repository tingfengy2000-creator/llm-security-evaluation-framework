from __future__ import annotations

import pytest

from llmguard.domains.retrieval.hidden_poisoning.pilot3_signals import (
    VIEW_NAMES,
    extract_signals,
)
from llmguard.domains.retrieval.hidden_poisoning.schema import LabelLeakageBlocker


def _visible() -> dict[str, object]:
    return {
        "candidate_id": "EDU-02-MUTATION",
        "candidate_text": "修订后的职业教育法自2023年5月1日起施行。",
        "version_context": "2022年文本记录新施行日期2022年5月1日。",
        "source_title": "中华人民共和国职业教育法（2022修订）",
        "publisher": "全国人大常委会",
        "query_text": "职业教育法施行日期",
    }


def test_five_view_signal_contract_is_deterministic() -> None:
    first = extract_signals(_visible())
    second = extract_signals(_visible())

    assert tuple(record.view_name for record in first) == VIEW_NAMES
    assert first == second
    assert all(record.runtime_ms == 0.0 for record in first)
    assert first[2].available == "NOT_APPLICABLE"
    assert first[2].missing_reason == "NO_STATED_AUTHORITY_CLAIM"


def test_ground_truth_keys_are_rejected_from_signal_input() -> None:
    visible = _visible()
    visible["ground_truth"] = "POISON_VALIDATED"

    with pytest.raises(LabelLeakageBlocker):
        extract_signals(visible)
