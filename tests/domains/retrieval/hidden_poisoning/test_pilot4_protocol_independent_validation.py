from __future__ import annotations

from pathlib import Path

import pytest

from llmguard.domains.retrieval.hidden_poisoning.annotation_v31 import (
    MINIMUM_EXTERNAL_EVIDENCE,
    build_neutral_evidence_pool,
    derive_stealth_level,
    full72_answerability,
)
from scripts.research.run_pilot4_protocol_independent_validation import (
    CANDIDATE_REPAIRS,
    INDEPENDENCE_STATUS,
    META_CUE_PHRASES,
    REVIEW_MODE,
    _examples,
    _field_specs,
    _review_visible_row,
    _semantic_candidate_qa,
)


def _source(evidence_id: str, title: str, url: str) -> dict[str, object]:
    return {
        "evidence_id": evidence_id,
        "triplet_id": "T-01",
        "source_identity": f"researcher identity for {title}",
        "official_page_title": title,
        "display_title_origin": "ACTUAL_PAGE_TITLE",
        "source_url": url,
        "content_hash": f"hash-{evidence_id}",
        "document_identity": f"doc-{evidence_id}",
        "minimal_evidence_hash": f"excerpt-{evidence_id}",
        "media_type": "text/html",
    }


def _candidate(sample_id: str, text: str) -> dict[str, object]:
    return {
        "sample_id": sample_id,
        "triplet_id": "T-01",
        "primary_subject": "中华人民共和国示例法",
        "phase1_view": {
            "sample_id": sample_id,
            "candidate_text": text,
            "source_title": "中华人民共和国示例法",
        },
        "phase2_view": {"evidence_ids": ["EVQ-T-01-PRIMARY"]},
        "owner_only": {
            "candidate_kind": "CLEAN_CURRENT",
            "intended_stealth": None,
            "hard_negative_type": None,
            "target_field": "scope_condition",
        },
    }


def test_minimum_evidence_has_only_one_multi_and_not_applicable() -> None:
    assert MINIMUM_EXTERNAL_EVIDENCE == (
        "ONE_OFFICIAL_EVIDENCE",
        "MULTI_EVIDENCE_OR_VERSION_CHAIN",
        "NOT_APPLICABLE",
    )


@pytest.mark.parametrize(
    "minimum",
    ["ONE_OFFICIAL_EVIDENCE", "MULTI_EVIDENCE_OR_VERSION_CHAIN"],
)
def test_local_uncertain_never_derives_s2_or_s3(minimum: str) -> None:
    assert derive_stealth_level("FACTUAL_CONFLICT", "UNCERTAIN", minimum) == "UNCERTAIN"


def test_label_aware_answerability_is_explicitly_not_independent() -> None:
    candidates = [
        _candidate(f"S-{index:02d}", "《中华人民共和国示例法》规定示例范围。")
        for index in range(72)
    ]
    sources = [
        _source("EVQ-T-01-PRIMARY", "示例法", "https://gov.example/one"),
        _source("EVC-T-01-COMPANION-01", "示例法解读", "https://gov.example/two"),
    ]
    result = full72_answerability(candidates, sources)
    assert result["evidence_classification"] == "LABEL_AWARE_ENGINEERING_CHECK_ONLY"
    assert result["independent_answerability_evidence"] is False


def test_evidence_pool_shows_four_neutral_columns_and_not_interpretive_identity() -> (
    None
):
    candidate = _candidate("S-01", "《中华人民共和国示例法》规定示例范围。")
    sources = [
        _source("EVQ-T-01-PRIMARY", "示例法", "https://gov.example/one"),
        _source("EVC-T-01-COMPANION-01", "示例法解读", "https://gov.example/two"),
    ]
    pool = build_neutral_evidence_pool(candidate, sources, annotator_variant="A")
    assert set(pool.visible_items[0]) == {
        "sample_id",
        "evidence_id",
        "official_page_title",
        "official_source_url",
    }
    assert "researcher identity" not in str(pool.visible_items)


def test_official_title_origin_is_mandatory() -> None:
    candidate = _candidate("S-01", "《中华人民共和国示例法》规定示例范围。")
    sources = [
        {
            **_source("EVQ-T-01-PRIMARY", "示例法", "https://gov.example/one"),
            "display_title_origin": "OWNER_INTERPRETIVE_IDENTITY",
        },
        _source("EVC-T-01-COMPANION-01", "示例法解读", "https://gov.example/two"),
    ]
    with pytest.raises(ValueError, match="official display_title_origin"):
        build_neutral_evidence_pool(candidate, sources, annotator_variant="A")


def test_five_named_candidate_repairs_remove_verification_meta_cues() -> None:
    ids = {
        "P4Q-02a9af3fa54f",
        "P4Q-0de42010ea94",
        "P4Q-73babd35d250",
        "P4Q-7ffa7d6b1c39",
        "P4Q-2646679ef239",
    }
    assert ids <= set(CANDIDATE_REPAIRS)
    for sample_id in ids:
        text, _ = CANDIDATE_REPAIRS[sample_id]
        assert not [phrase for phrase in META_CUE_PHRASES if phrase in text]


def test_semantic_meta_cue_gate_and_self_containment_are_separate() -> None:
    candidate = _candidate(
        "S-01",
        "《中华人民共和国示例法》的结论需要核对两个来源。",
    )
    qa = _semantic_candidate_qa([candidate] * 72)
    assert qa["meta_cue_blocker_count"] == 72
    assert qa["self_containment_blocker_count"] == 0


def test_naturalness_examples_are_truth_and_context_independent() -> None:
    rows = [row for row in _examples() if row["field_name"] == "text_naturalness"]
    assert len(rows) == 6
    assert any("日期真伪不影响自然度" in row["why"] for row in rows)
    assert any("另由 phase1_issue 判断" in row["why"] for row in rows)
    assert all("事实错误所以" not in row["why"] for row in rows)


def test_field_guide_has_separate_phase_specs_and_seven_human_columns() -> None:
    specs = _field_specs()
    assert len([row for row in specs if row["phase"] == "PHASE1"]) == 4
    assert len([row for row in specs if row["phase"] == "PHASE2"]) == 7
    visible_keys = {
        "field_name",
        "chinese_explanation",
        "judging",
        "applicable",
        "definitions",
        "key_rule",
        "common_mistake",
    }
    assert visible_keys <= set(specs[0])


def test_one_review_is_not_mislabeled_as_independent_ab() -> None:
    assert REVIEW_MODE == "ONE_LABEL_BLIND_SEMANTIC_REVIEW + OWNER_REVIEW_REQUIRED"
    assert INDEPENDENCE_STATUS == "INDEPENDENCE_NOT_ESTABLISHED_BY_MACHINE"


def test_label_blind_review_rejects_hidden_fields() -> None:
    row = {
        "sample_id": "P4Q-8fadbe1bcde2",
        "primary_subject": "中华人民共和国示例法",
        "candidate_text": "《中华人民共和国示例法》规定示例范围。",
        "source_title": "中华人民共和国示例法",
        "evidence_pool": [
            {"official_page_title": "示例法", "evidence_id": "E1"},
            {"official_page_title": "示例法解读", "evidence_id": "E2"},
        ],
        "owner_only": {},
    }
    with pytest.raises(ValueError, match="LABEL_BLIND_INPUT_LEAKAGE_BLOCKER"):
        _review_visible_row(row)


def test_workbook_builder_keeps_dependency_table_machine_only() -> None:
    builder = Path("scripts/research/build_pilot4_v31_workbooks.mjs").read_text(
        encoding="utf-8"
    )
    assert "DEPENDENCY_TABLE_VISIBILITY_BLOCKER" in builder
    assert 'worksheets.add("Dependency Table' not in builder
    assert (
        'const evidenceHeaders = ["sample_id", "evidence_id", "official_page_title", "official_source_url"]'
        in builder
    )
