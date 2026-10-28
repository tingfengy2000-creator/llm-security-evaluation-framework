"""Static specification checks only: never execute a router, detector or model."""
from __future__ import annotations

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SPECS = ROOT / "docs/research/stage6_1_hidden_knowledge_poisoning/core144/vace_lite"
FILES = (
    "VACE_LITE_V03_ADAPTIVE_METHOD_SPEC.md",
    "VACE_V02_V03_COMPARISON.md",
    "VACE_V03_ABLATION_AND_EVALUATION_PLAN.md",
    "VACE_V03_OWNER_REVIEW_PACKET.md",
)


@pytest.mark.parametrize("name", FILES)
def test_required_utf8_artifact_and_draft_boundary(name: str) -> None:
    text = (SPECS / name).read_text(encoding="utf-8")
    assert "\ufffd" not in text
    assert "2026-10-28" in text and "PODR-148" in text
    assert "OWNER" in text.upper()


def test_six_slot_compatibility_and_module_interfaces() -> None:
    text = (SPECS / FILES[0]).read_text(encoding="utf-8")
    for slot in ("subject", "predicate", "value_unit", "scope", "time_version", "source_role"):
        assert slot in text
    for state in ("PROVEN_CONFLICT", "NOT_PROVEN", "UNRESOLVED", "SUPPORT", "CONTRADICT", "INSUFFICIENT"):
        assert state in text
    assert "模块输入输出合同" in text and "路由优先级" in text


def test_proof_before_early_exit_and_missing_not_safe() -> None:
    text = (SPECS / FILES[0]).read_text(encoding="utf-8")
    assert "A0阴性不能跳过I" in text
    assert "I未发现冲突" in text
    assert "预算停止不能变成SUPPORT" in text
    assert "不映射为Poison或Clean" in text
    assert "不采用A0 OR B1" in text


def test_leakage_cache_and_frozen_pool_contracts_documented() -> None:
    text = (SPECS / FILES[0]).read_text(encoding="utf-8")
    for item in ("construction_role", "minimum_external_evidence_needed", "evidence_selection", "白名单schema", "缓存键", "FROZEN_CORPUS_GAP"):
        assert item in text
    assert "标注" not in text.split("Runtime仅获", 1)[1].split("禁止字段", 1)[0]


def test_no_straw_v02_or_idealized_performance() -> None:
    text = (SPECS / FILES[1]).read_text(encoding="utf-8")
    assert "B1" in text and "不是V0.2" in text
    assert "POSTHOC_IDEALIZED_S_LABEL_ROUTE" in text
    assert "NOT_EXECUTED/UNKNOWN" in text
    assert "不是实测" in text


def test_fair_evidence_coverage_and_cost_required() -> None:
    text = (SPECS / FILES[2]).read_text(encoding="utf-8")
    for item in ("L0-F5", "V02-NA-CONTROL-F5", "V03-F5", "V03-E2", "ABL-I-EXIT", "ABL-A0-PRIORITY", "ABL-ADAPT"):
        assert item in text
    for item in ("HN-FPR≤10%", "≤20%", "复核预算", "外层", "mean/median/p95", "D2/D3", "source/version-family", "同池"):
        assert item in text
    assert "弃权/解析失败不计TP" in text


def test_owner_gate_has_no_implementation_approval() -> None:
    text = (SPECS / FILES[3]).read_text(encoding="utf-8")
    assert "VACE_LITE_V03_OWNER_REVIEW_REQUIRED" in text
    assert "不改Research Plan Authority" in text
    assert "无新模型、路由预测、性能表或正式合同变更" in text
