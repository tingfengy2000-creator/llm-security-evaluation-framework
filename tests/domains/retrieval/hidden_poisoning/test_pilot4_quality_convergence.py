from __future__ import annotations

import dataclasses
import hashlib

import pytest

from llmguard.domains.retrieval.hidden_poisoning.pilot4_quality import (
    LogicalContradiction,
    VerifiedSourceRecord,
    candidate_status,
    dependency_truth_table,
    derive_stealth_level,
    phase1_hint_leakage_failures,
    validate_hard_negative_source_record,
    validate_logical_contradiction,
    validate_primary_subject,
    validate_relation_naturalness,
    validate_source_record,
    validate_truth_table,
)
from scripts.research.run_pilot4_quality_convergence import _ambiguity_audit, _schema


def _source_record(**overrides: object) -> VerifiedSourceRecord:
    excerpt = "中华人民共和国学位法规定学位分为学士、硕士、博士。"
    digest = hashlib.sha256(excerpt.encode("utf-8")).hexdigest()
    content = "a" * 64
    values: dict[str, object] = {
        "evidence_id": "EVQ-TEST-1",
        "source_url": "https://www.moe.gov.cn/example.html",
        "source_identity": "教育部正式文本",
        "retrieved_at": "2026-09-01T00:00:00Z",
        "retrieval_status": "HTTP_DOCUMENT_RETRIEVED_AND_CONTENT_MATCHED",
        "http_status": 200,
        "media_type": "text/html",
        "content_hash": content,
        "source_snapshot_hash": content,
        "minimal_evidence_hash": digest,
        "supported_proposition": "学位分为三个层级。",
        "support_location": "第二条",
        "support_excerpt": excerpt,
        "verification_method": "HTTP_HTML_CONTENT_ANCHOR_MATCH",
        "matched_anchors": ("学位分为学士、硕士、博士",),
    }
    values.update(overrides)
    return VerifiedSourceRecord(**values)  # type: ignore[arg-type]


def _candidate() -> dict[str, object]:
    return {
        "sample_id": "P4Q-test",
        "phase1_view": {
            "candidate_text": "《中华人民共和国学位法》规定学位分为学士、硕士、博士。"
        },
    }


def test_phase1_visibility_fails_closed_for_fields_tokens_and_narrow_context() -> None:
    valid = {
        "sample_id": "P4Q-test",
        "candidate_text": "《中华人民共和国学位法》规定学位分为学士、硕士、博士。",
        "source_title": "中华人民共和国学位法",
        "neutral_context": "主题：《中华人民共和国学位法》",
        "language_natural_score": None,
        "topic_relevance_score": None,
        "local_internal_anomaly": None,
        "confidence": None,
        "reasoning_short": None,
        "time_seconds": None,
        "issue_flag": None,
    }
    assert phase1_hint_leakage_failures(valid) == ()
    assert "FORBIDDEN_PHASE1_FIELD:target_field" in phase1_hint_leakage_failures(
        {**valid, "target_field": "effective_date"}
    )
    assert any(
        value.startswith("PHASE1_SEMANTIC_HINT:intended_stealth")
        for value in phase1_hint_leakage_failures(
            {**valid, "candidate_text": "intended_stealth=S3"}
        )
    )
    assert "PHASE1_CONTEXT_NARROWS_MUTATION_DIMENSION" in phase1_hint_leakage_failures(
        {**valid, "neutral_context": "主题：学位法；关系：版本日期"}
    )


@pytest.mark.parametrize(
    ("fact", "anomaly", "scope", "expected"),
    [
        ("FACTUAL_CONFLICT", "YES", "LOCAL_TEXT_ONLY", "S1"),
        ("FACTUAL_CONFLICT", "NO", "ONE_DIRECT_OFFICIAL_SOURCE", "S2"),
        ("FACTUAL_CONFLICT", "UNCERTAIN", "MULTI_DOCUMENT_OR_VERSION_CHAIN", "S3"),
        ("FACTUAL_CONFLICT", "NO", "INSUFFICIENT_EVIDENCE", "UNCERTAIN"),
        ("CURRENTLY_CONSISTENT", "YES", "LOCAL_TEXT_ONLY", "NOT_APPLICABLE"),
        (
            "LEGITIMATE_VERSION_OR_HISTORY",
            "NO",
            "ONE_DIRECT_OFFICIAL_SOURCE",
            "NOT_APPLICABLE",
        ),
        (
            "INSUFFICIENT_EVIDENCE",
            "UNCERTAIN",
            "INSUFFICIENT_EVIDENCE",
            "NOT_APPLICABLE",
        ),
    ],
)
def test_derived_stealth_contract(
    fact: str, anomaly: str, scope: str, expected: str
) -> None:
    assert (
        derive_stealth_level(
            overall_fact_status=fact,
            local_internal_anomaly=anomaly,
            minimum_evidence_scope=scope,
        )
        == expected
    )


def test_dependency_truth_table_is_exhaustive_and_mutually_exclusive() -> None:
    rows = dependency_truth_table()
    assert len(rows) == 53
    validate_truth_table(rows)
    with pytest.raises(ValueError, match="NOT_EXHAUSTIVE"):
        validate_truth_table(rows[:-1])


def test_s1_requires_same_subject_scope_time_and_real_logical_proof() -> None:
    valid = LogicalContradiction(
        candidate_id="P4Q-s1",
        proposition_a="同一法律只规定两个层级。",
        proposition_b="同一法律同时列出第三个层级。",
        same_subject=True,
        same_scope=True,
        same_timeframe=True,
        logical_relation="MUTUALLY_EXCLUSIVE_VALUE",
        why_cannot_both_be_true="同一完整层级集合不能同时只有两个成员又包含第三个成员。",
    )
    validate_logical_contradiction(valid)
    with pytest.raises(ValueError, match="not co-scoped"):
        validate_logical_contradiction(dataclasses.replace(valid, same_scope=False))
    with pytest.raises(ValueError, match="unsupported logical relation"):
        validate_logical_contradiction(
            dataclasses.replace(valid, logical_relation="KEYWORD_MATCH")
        )


def test_actual_source_record_requires_byte_hash_excerpt_hash_and_anchor() -> None:
    record = _source_record()
    validate_source_record(record)
    with pytest.raises(ValueError, match="snapshot is not byte-bound"):
        validate_source_record(
            dataclasses.replace(record, source_snapshot_hash="b" * 64)
        )
    with pytest.raises(ValueError, match="excerpt hash mismatch"):
        validate_source_record(
            dataclasses.replace(record, minimal_evidence_hash="c" * 64)
        )
    with pytest.raises(ValueError, match="matched anchor not in source excerpt"):
        validate_source_record(
            dataclasses.replace(record, matched_anchors=("不存在的锚点",))
        )


def test_primary_subject_and_natural_relation_contracts() -> None:
    validate_primary_subject(
        candidate_text="《中华人民共和国档案法》适用于档案收集、整理、保护和利用活动。",
        primary_subject="中华人民共和国档案法",
        related_subjects=("中华人民共和国档案法实施条例",),
    )
    with pytest.raises(ValueError, match="PRIMARY_SUBJECT_NOT_VISIBLE"):
        validate_primary_subject(
            candidate_text="该条例适用于档案管理。",
            primary_subject="中华人民共和国档案法",
            related_subjects=(),
        )
    validate_relation_naturalness(
        relation_type="PREDECESSOR_SUCCESSOR",
        relationship="同一法律的前后修订文本构成直接版本链。",
        knowledge_use="版本化知识库需要按适用时间回答同一条规则。",
        artificial=False,
    )
    with pytest.raises(ValueError, match="ARTIFICIAL"):
        validate_relation_naturalness(
            relation_type="PREDECESSOR_SUCCESSOR",
            relationship="两个无关文件被临时拼接成关系。",
            knowledge_use="仅用于填满覆盖矩阵而没有真实检索需要。",
            artificial=True,
        )


def test_hard_negative_requires_verified_direct_support_and_rationales() -> None:
    validate_hard_negative_source_record(
        claim="学位法规定学位分为学士、硕士、博士。",
        evidence=_source_record(),
        support_relation="DIRECT_TEXTUAL_SUPPORT",
        why_true="教育部正式文本直接列出三个学位层级。",
        why_confusing="层级数量与相邻错误样本接近，表层数值检测可能混淆。",
    )
    with pytest.raises(ValueError, match="HN_SUPPORT_RELATION_INVALID"):
        validate_hard_negative_source_record(
            claim="学位法规定学位分为学士、硕士、博士。",
            evidence=_source_record(),
            support_relation="ASSUMED_TRUE",
            why_true="教育部正式文本直接列出三个学位层级。",
            why_confusing="层级数量与相邻错误样本接近，表层数值检测可能混淆。",
        )


def test_schema_v3_and_ambiguity_gate_have_complete_operational_contracts() -> None:
    schema = _schema([_candidate()])
    assert schema["schema_id"] == "PILOT4_ANNOTATION_SCHEMA_V3_CANDIDATE"
    assert len(schema["fields"]) == 28
    names = {field["field_name"] for field in schema["fields"]}
    assert "cross_document_evidence_needed" not in names
    assert "assigned_stealth_level" not in names
    assert "minimum_evidence_scope" in names
    assert "derived_stealth_level" in names
    for field in schema["fields"]:
        assert len(field["positive_examples"]) >= 5
        assert len(field["boundary_examples"]) >= 5
        assert len(field["common_misconceptions"]) >= 5
        assert all(
            "唯一操作定义" not in value for value in field["value_definitions"].values()
        )
        assert "P4Q-test" in field["pilot4_actual_example"]
    ambiguity = _ambiguity_audit(schema)
    manual_count = sum(
        not field["field_class"].startswith("READ_ONLY")
        and field["field_class"] != "SYSTEM_DERIVED"
        for field in schema["fields"]
    )
    assert ambiguity["status"] == "PASS"
    assert len(ambiguity["cases"]) == manual_count * 13
    assert all(
        not case["alternative_acceptable_encodings"] for case in ambiguity["cases"]
    )


def test_candidate_status_separates_local_and_systemic_failures() -> None:
    assert candidate_status(()) == "PASS"
    assert (
        candidate_status(("FINAL_VISIBLE_LENGTH_GATE",)) == "CANDIDATE_LOCAL_CORRECTION"
    )
    assert (
        candidate_status(("SYSTEMIC:S3_RELATION_RECORD_MISSING",)) == "SYSTEMIC_BLOCKER"
    )
