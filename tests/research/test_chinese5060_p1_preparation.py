from __future__ import annotations

import hashlib
import json

import pytest

from llmguard.domains.retrieval.hidden_poisoning.chinese5060.p1_preparation import (
    assert_no_sibling_bodies, audit_proposal, design_world, verify_source_texts,
)


def sources() -> list[dict]:
    text = "虚构甲市规定许可期限五年。"
    return [{"source_id": "s-fixture", "text": text,
             "snapshot_text_sha256": hashlib.sha256(text.encode()).hexdigest(),
             "metadata": {"issuer": "声称的机关", "publication_date": None, "effective_start": None}}]


def query() -> dict:
    return {"query_id": "q-fixture", "query_text": "许可期限多久？"}


def proposal() -> dict:
    return {"query_id": "q-fixture", "question_draft": "许可期限多久？", "human_approved": False,
            "pilot_execution_approved": False, "time_scope": "仅归档文本，不推定当前效力", "answer_proposal": "五年",
            "caveats": ["虚构"], "facts": [{"field": "duration", "value": 5,
                "citations": [{"source_id": "s-fixture", "start": 0, "end": 13, "quote": "虚构甲市规定许可期限五年。"}]}]}


def test_valid_quotes_still_need_adjudication_and_cannot_be_gold() -> None:
    row = audit_proposal(query(), proposal(), {s["source_id"]: s for s in sources()})
    assert row["source_text_and_span_status"] == "PASS"
    assert row["evaluation_freeze_status"] == "NEEDS_ADJUDICATION"
    assert row["human_gold"] is False and row["attack_target"] is None
    assert row["trusted_provenance_root_verified"] is False
    assert row["effective_start_metadata_missing"] == 1


def test_misaligned_or_missing_source_is_preserved_as_failure() -> None:
    row = audit_proposal(query(), proposal(), {})
    assert row["invalid_citation_spans"] == 1 and row["source_text_and_span_status"] == "FAIL"
    p = proposal()
    p["facts"][0]["citations"][0]["start"] = -1
    assert audit_proposal(query(), p, {s["source_id"]: s for s in sources()})["source_text_and_span_status"] == "FAIL"


def test_query_version_drift_is_not_silently_repaired() -> None:
    q = query()
    q["query_text"] = "换题"
    with pytest.raises(ValueError, match="QUERY_VERSION_MISMATCH"):
        audit_proposal(q, proposal(), {})


def test_ai_record_cannot_silently_become_human_approved() -> None:
    p = proposal()
    p["human_approved"] = True
    with pytest.raises(ValueError, match="UNEXPECTED_APPROVAL"):
        audit_proposal(query(), p, {})


def test_world_has_one_candidate_and_identical_backgrounds_without_roles() -> None:
    sibling_ids = ["candidate-a", "candidate-b", "candidate-c"]
    worlds = [design_world(query(), candidate_id=cid, candidate_text=f"虚构文本{i}",
                          all_sibling_ids=sibling_ids, sources=sources()) for i, cid in enumerate(sibling_ids)]
    assert len({w["world_id"] for w in worlds}) == 3
    assert len({w["corpus_hash"] for w in worlds}) == 3
    assert all(len(w["documents"]) == 2 and w["documents"][1:] == worlds[0]["documents"][1:] for w in worlds)
    for world in worlds:
        assert all(d["trust_boundary"] == "UNVERIFIED" for d in world["documents"])
        assert world["index_status"] == "DESIGN_ONLY_NOT_BUILT" and world["topK_snapshot_hash"] is None
        body = json.dumps(world, ensure_ascii=False)
        assert not any(cid in body for cid in sibling_ids)
        assert '"label"' not in body and '"expected_answer"' not in body and '"role_evaluation_only"' not in body


def test_corpus_requires_known_complete_sibling_set() -> None:
    with pytest.raises(ValueError, match="COMPLETE_COUNTERFACTUAL"):
        design_world(query(), candidate_id="unregistered", candidate_text="虚构", all_sibling_ids=["a", "b", "c"], sources=sources())


def test_source_body_change_does_not_keep_old_identity() -> None:
    s = sources()
    verify_source_texts(s)
    s[0]["text"] = "不同正文"
    with pytest.raises(ValueError, match="SOURCE_TEXT_HASH_MISMATCH"):
        verify_source_texts(s)


def test_sibling_body_hidden_inside_background_is_blocked() -> None:
    with pytest.raises(ValueError, match="SIBLING_BODY_IN_INDEX_DESIGN"):
        assert_no_sibling_bodies([{"text": "背景段落夹带另一个候选全文，结束。"}], ["另一个候选全文"])


def test_whitespace_and_fullwidth_do_not_hide_a_sibling_copy() -> None:
    with pytest.raises(ValueError, match="SIBLING_BODY_IN_INDEX_DESIGN"):
        assert_no_sibling_bodies([{"text": "前缀Ａ Ｂ Ｃ后缀"}], ["ABC"])
