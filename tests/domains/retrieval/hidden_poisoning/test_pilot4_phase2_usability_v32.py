from __future__ import annotations

from scripts.research import finalize_pilot4_phase2_usability_v32 as repair


def test_risk_assessment_freezes_semantics_and_requires_only_ux_repair() -> None:
    text = repair.risk_assessment()
    assert "PHASE2_FIELD_SCHEMA_REDESIGN_REQUIRED = FALSE" in text
    assert "PHASE2_HUMAN_GUIDE_REPAIR_REQUIRED = TRUE" in text
    assert "PHASE2_EXCEL_MINIMAL_USABILITY_REPAIR_REQUIRED = TRUE" in text
    assert "PHASE2_SEMANTIC_BLOCKER = FALSE" in text
    assert text.count("风险 HIGH") >= 6


def test_guide_v4_has_fixed_flow_all_fields_and_no_semantic_change() -> None:
    text = repair.guide_v4("HUMAN-A01")
    assert "GUIDE_V4_PROTOCOL_SEMANTIC_CHANGE = FALSE" in text
    assert "固定十步决策顺序" in text
    assert all(field in text for field in (*repair.ENUMS, "phase2_reason"))
    assert "当前时点替换测试" in text
    assert "十个常见返工错误" in text


def test_guide_v4_canonical_enums_are_complete() -> None:
    text = repair.guide_v4("HUMAN-B01")
    for values in repair.ENUMS.values():
        for value in values:
            assert f"`{value}`" in text


def test_ab_guides_are_semantically_equal_after_allowed_identity_normalization() -> None:
    a = repair.guide_v4("HUMAN-A01")
    b = repair.guide_v4("HUMAN-B01")
    normalized_a = a.replace("HUMAN-A01", "HUMAN-X01").replace("HUMAN_A01", "HUMAN_X01")
    normalized_b = b.replace("HUMAN-B01", "HUMAN-X01").replace("HUMAN_B01", "HUMAN_X01")
    assert normalized_a == normalized_b


def test_readme_v4_uses_official_url_first_and_snapshot_as_backup() -> None:
    text = repair.readme_v4("HUMAN-A01")
    assert "点击可见的 E1/E2 官方 URL" in text
    assert "冻结快照" in text
    assert "不要改 ID、Candidate、source title、URL、行数或顺序" in text
