from __future__ import annotations

from scripts.research.build_pilot4_ab_usability_repair import (
    FINAL_STATUS,
    PHASE1_GUIDE_TEMPLATE,
    PHASE1_HEADERS,
    PHASE1_QUICK_TEMPLATE,
    PHASE2_GUIDE_TEMPLATE,
    PHASE2_HEADERS,
    TEACHING_EXAMPLES,
    _normalized,
    _personalize,
    _similarity,
)


def test_v2_keeps_exact_return_schemas() -> None:
    assert PHASE1_HEADERS == [
        "blind_review_id",
        "text_naturalness",
        "local_internal_conflict",
        "phase1_issue",
        "phase1_reason",
    ]
    assert PHASE2_HEADERS == [
        "blind_review_id",
        "overall_fact_status",
        "version_claim_status",
        "authority_claim_status",
        "minimum_external_evidence_needed",
        "evidence_selection",
        "phase2_issue",
        "phase2_reason",
    ]


def test_phase1_reason_rule_matches_frozen_validator() -> None:
    assert "local_internal_conflict IN {YES, UNCERTAIN}" in PHASE1_GUIDE_TEMPLATE
    assert "OR phase1_issue != NONE" in PHASE1_GUIDE_TEMPLATE
    assert "单独为 `MINOR_ISSUE` 或 `UNNATURAL` 不会改变" in PHASE1_GUIDE_TEMPLATE


def test_phase1_manual_is_human_executable() -> None:
    for token in (
        "固定填写流程",
        "Boundary",
        "常见错误",
        "六条完整填写示例",
        "最终自检",
        "不要在 Packet Markdown 中填写答案",
    ):
        assert token in PHASE1_GUIDE_TEMPLATE
    assert len(TEACHING_EXAMPLES) >= 16


def test_phase2_manual_covers_frozen_decision_boundaries() -> None:
    for token in (
        "PRESENT-TIME SUBSTITUTION TEST",
        "CURRENTLY_CONSISTENT",
        "LEGITIMATE_VERSION_OR_HISTORY",
        "FACTUAL_CONFLICT",
        "INSUFFICIENT_EVIDENCE",
        "ONE_OFFICIAL_EVIDENCE",
        "MULTI_EVIDENCE_OR_VERSION_CHAIN",
        "evidence_selection",
        "LATE_DISCOVERED_CANDIDATE_DEFECT",
        "REASON_REQUIRED",
    ):
        assert token in PHASE2_GUIDE_TEMPLATE


def test_a_b_personalization_is_semantically_identical() -> None:
    for template in (
        PHASE1_GUIDE_TEMPLATE,
        PHASE1_QUICK_TEMPLATE,
        PHASE2_GUIDE_TEMPLATE,
    ):
        a = _personalize(template, "HUMAN-A01")
        b = _personalize(template, "HUMAN-B01")
        normalized_a = a.replace("HUMAN-A01", "HUMAN-X01").replace(
            "HUMAN_A01", "HUMAN_X01"
        )
        normalized_b = b.replace("HUMAN-B01", "HUMAN-X01").replace(
            "HUMAN_B01", "HUMAN_X01"
        )
        assert normalized_a == normalized_b


def test_teaching_similarity_is_conservative() -> None:
    assert _normalized("规则 A。") == "规则a"
    assert _similarity("甲规则要求预约。", "完全不同的库存说明。") < 0.5


def test_final_status_keeps_phase2_and_ground_truth_closed() -> None:
    assert "PHASE2_V2_PREBUILT_WITHHELD" in FINAL_STATUS
    assert "NO_GROUND_TRUTH_YET" in FINAL_STATUS
    assert "ANNOTATION_COMPLETE" not in FINAL_STATUS
