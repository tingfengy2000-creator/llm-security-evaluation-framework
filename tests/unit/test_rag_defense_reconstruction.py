from __future__ import annotations

import copy

import pytest

from llmguard.domains.retrieval.hidden_poisoning.rag_defense_reconstruction.contracts import (
    no_defense, reject_evaluator_fields, validate_packet, validate_sibling_isolation,
)
from llmguard.domains.retrieval.hidden_poisoning.rag_defense_reconstruction.evaluation_preparation import (
    audit_existing_packets, select_groups,
)


def packet():
    return {"query_id": "Q-0001", "query_text": "2024年规则适用多久？", "candidate_id": "D-0001",
            "retrieval_order": ["R-1"], "retrieved_chunks": [{"chunk_id": "R-1", "text": "虚构规则说明。",
            "source_id": "S-1", "source_role": None, "publication_time": None, "effective_time": None,
            "version": None, "trust_boundary": "UNVERIFIED"}]}


@pytest.mark.parametrize("field", ["label", "expected_answer", "attack_goal", "oracle", "role_evaluation_only"])
def test_nested_evaluation_leak_is_rejected(field):
    with pytest.raises(ValueError):
        reject_evaluator_fields({"metadata": [{field: "hidden"}]})


def test_serialized_evaluation_leak_is_rejected():
    with pytest.raises(ValueError):
        reject_evaluator_fields({"text": '{"expected_answer":"secret"}'})


def test_b0_preserves_context_and_does_not_add_metadata():
    p = packet()
    assert no_defense(p) == p["retrieved_chunks"]
    assert no_defense(p) is not p["retrieved_chunks"]


@pytest.mark.parametrize("field", ["query_text", "query_id", "candidate_id"])
def test_missing_query_identity_blocks(field):
    p = packet()
    p[field] = None
    with pytest.raises(ValueError):
        validate_packet(p)


@pytest.mark.parametrize("trust", ["POISON", "ATTACKER_CONTROLLED", "CLEAN", "UNKNOWN"])
def test_trust_is_not_evaluator_attack_role(trust):
    p = packet()
    p["retrieved_chunks"][0]["trust_boundary"] = trust
    with pytest.raises(ValueError):
        validate_packet(p)


def test_same_group_siblings_cannot_be_mixed():
    with pytest.raises(ValueError):
        validate_sibling_isolation(["a", "b", "x"], {"a", "b", "c"})
    validate_sibling_isolation(["a", "x"], {"a", "b", "c"})


def test_order_and_duplicates_are_checked():
    p = packet()
    p["retrieved_chunks"].append(copy.deepcopy(p["retrieved_chunks"][0]))
    p["retrieval_order"].append("R-1")
    with pytest.raises(ValueError):
        validate_packet(p)


def labels():
    return [{"group_evaluation_only": f"{s}-{i}", "derived_s_evaluation_only": s,
             "role_evaluation_only": role} for s in ("S1", "S2", "S3") for i in range(6)
            for role in ("CLEAN_CURRENT", "POISON", "HARD_NEGATIVE")]


def test_selection_independent_of_input_order_and_exact_strata():
    data = labels()
    chosen = select_groups(data)
    assert chosen == select_groups(list(reversed(data)))
    assert len(chosen) == 12
    assert [sum(g.startswith(s) for g in chosen) for s in ("S1", "S2", "S3")] == [4, 4, 4]


def test_partial_triplet_rejected():
    with pytest.raises(ValueError):
        select_groups(labels()[:-1])


def test_quality_audit_does_not_invent_qa_or_fill_dates():
    rows = [{"candidate_text": "虚构事实。", "evidence": [{"document_uid": "D-1", "metadata": {}}]}]
    result = audit_existing_packets(rows)
    assert result["status"] == "NEEDS_ADJUDICATION"
    assert result["query_text_present"] == result["independent_QA_answer_adjudication_present"] == 0
    assert result["metadata_gaps"]["effective_start_missing"] == 1
    assert rows[0]["evidence"][0]["metadata"] == {}
