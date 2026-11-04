"""Independent material must discard old result and mapping fields recursively."""
from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any

import pytest

spec = importlib.util.spec_from_file_location("fast_b_cards", Path(__file__).resolve().parents[2]
    / "scripts/research/prepare_chinese5060_fast_b_blind_packet.py")
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def card() -> dict[str, Any]:
    return {"human_gold": False, "proposed_attack_target": None,
        "retrieval_or_model_results_consulted": False,
        "query": {"query_text": "虚构问题", "query_id": "SECRET_MAPPING"},
        "answer_atoms_provisional": [{"field": "事实", "value": "待审值", "citations": [],
                                      "reason": "OLD_AI_JUDGEMENT"}],
        "version_and_time_scope_provisional": "待审时间", "conditions_and_exceptions_provisional": [],
        "official_source_candidates": [{"source_id": "SOURCE-01", "official_url": "https://example.org/",
                                        "snapshot_text_sha256": "0" * 64, "metadata": {"role": "SECRET_ROLE"}}],
        "prediction": "OLD_PREDICTION", "role": "SECRET_ROLE", "world_id": "SECRET_WORLD"}


def test_blind_projection_discards_mapping_and_prior_judgements() -> None:
    result = module.project_card(card(), 1)
    serialized = str(result)
    for marker in ("SECRET_MAPPING", "OLD_AI_JUDGEMENT", "OLD_PREDICTION", "SECRET_ROLE", "SECRET_WORLD"):
        assert marker not in serialized
    assert result["question"] == "虚构问题"
    assert result["attack_target"] is None
    assert result["accepted_answer_atoms"] is None
    assert result["human_gold"] is False
    assert all(d["selection"] is None for d in result["decision_items"])


@pytest.mark.parametrize("key,value", [("human_gold", True), ("proposed_attack_target", "target"),
                                    ("retrieval_or_model_results_consulted", True)])
def test_signed_or_exposed_inputs_fail_closed(key: str, value: Any) -> None:
    value_card = card()
    value_card[key] = value
    with pytest.raises(ValueError, match="UNSIGNED_UNEXPOSED_CARD_REQUIRED"):
        module.project_card(value_card, 1)
