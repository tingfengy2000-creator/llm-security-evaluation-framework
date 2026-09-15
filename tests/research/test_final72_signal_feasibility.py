from __future__ import annotations

import json
from pathlib import Path

import pytest

from llmguard.domains.retrieval.hidden_poisoning.method_engineering import (
    FIVE_VIEW_SIGNAL_REGISTRY,
    SignalComputationStatus,
    SignalInstance,
    SignalOrientation,
    SignalView,
)
from llmguard.domains.retrieval.hidden_poisoning.method_engineering.feasibility import (
    SIGNAL_ORIENTATIONS,
    cliffs_delta,
    diagnostic_auroc,
    diagnostic_average_precision,
    extract_sample_signals,
    forbidden_key_hits,
    instance_to_dict,
    lexical_similarity,
    spearman,
    validate_orientation_contract,
)
from scripts.research import run_final72_signal_feasibility as study


def _safe_sample() -> dict[str, object]:
    return {
        "sample_id": "P4Q-safe0000000001",
        "candidate_text": "2017年版《示例管理规定》曾经施行，后来由2022年版替代。",
        "source_title": "示例管理规定",
        "primary_subject": "示例管理规定",
        "related_subjects": [],
        "evidence": [
            {
                "evidence_id": "E1",
                "official_source_title": "示例管理规定（2022年版）",
                "official_source_url": "https://example.gov.cn/current",
                "snapshot_text": "示例管理规定于2022年修订，自2022年5月1日起施行。",
                "content_hash": "a" * 64,
                "official_role": "ORIGINAL_ISSUING_AUTHORITY",
                "source_ref": f"E1:{'a' * 64}",
            },
            {
                "evidence_id": "E2",
                "official_source_title": "示例管理规定（2017年版）",
                "official_source_url": "https://example.gov.cn/history",
                "snapshot_text": "示例管理规定2017年版曾经施行。",
                "content_hash": "b" * 64,
                "official_role": "ORIGINAL_ISSUING_AUTHORITY",
                "source_ref": f"E2:{'b' * 64}",
            },
        ],
    }


def test_orientation_is_predeclared_for_all_42_signals() -> None:
    validate_orientation_contract()
    assert len(SIGNAL_ORIENTATIONS) == 42
    assert set(SIGNAL_ORIENTATIONS) == {
        signal.signal_name for signal in FIVE_VIEW_SIGNAL_REGISTRY
    }


def test_label_blind_sample_extraction_is_complete_and_deterministic() -> None:
    sample = _safe_sample()
    first = [instance_to_dict(item) for item in extract_sample_signals(sample)]
    second = [instance_to_dict(item) for item in extract_sample_signals(sample)]
    assert first == second
    assert len(first) == 42
    assert len({row["signal_name"] for row in first}) == 42
    assert forbidden_key_hits(first, study.FORBIDDEN_KEYS) == []
    assert {row["view"] for row in first} == {view.value for view in SignalView}


def test_null_is_not_zero_and_status_invariants_are_enforced() -> None:
    missing = SignalInstance(
        sample_id="P4Q-1",
        signal_name="retrieval_score",
        view=SignalView.RETRIEVAL_BEHAVIOR,
        value=None,
        applicable=True,
        confidence=None,
        computation_status=SignalComputationStatus.INPUT_MISSING,
        reason_code="NO_TRACE",
        reason="No retrieval trace.",
        source_refs=(),
        extractor_version="V1",
        orientation=SignalOrientation.NON_MONOTONIC,
    )
    assert missing.value is None
    with pytest.raises(ValueError):
        SignalInstance(
            sample_id="P4Q-1",
            signal_name="retrieval_score",
            view=SignalView.RETRIEVAL_BEHAVIOR,
            value=0.0,
            applicable=True,
            confidence=None,
            computation_status=SignalComputationStatus.INPUT_MISSING,
            reason_code="NO_TRACE",
            reason="No retrieval trace.",
            source_refs=(),
            extractor_version="V1",
            orientation=SignalOrientation.NON_MONOTONIC,
        )


def test_retrieval_and_models_fail_closed_without_frozen_inputs() -> None:
    rows = [instance_to_dict(item) for item in extract_sample_signals(_safe_sample())]
    by_name = {row["signal_name"]: row for row in rows}
    assert (
        by_name["mlm_masked_token_naturalness"]["computation_status"]
        == "MODEL_UNAVAILABLE"
    )
    assert by_name["ppl_naturalness"]["computation_status"] == "MODEL_UNAVAILABLE"
    retrieval = [row for row in rows if row["view"] == "RETRIEVAL_BEHAVIOR"]
    assert len(retrieval) == 10
    assert {row["computation_status"] for row in retrieval} == {"INPUT_MISSING"}
    assert all(row["value"] is None for row in retrieval)


def test_present_time_substitution_emits_auditable_details() -> None:
    rows = [instance_to_dict(item) for item in extract_sample_signals(_safe_sample())]
    record = next(
        row for row in rows if row["signal_name"] == "present_time_substitution_signal"
    )
    assert record["computation_status"] == "COMPUTED"
    assert record["details"] == {
        "historical_support": True,
        "current_support": False,
        "version_sensitive": True,
        "current_misbinding_indicator": False,
    }


def test_diagnostic_statistics_are_descriptive_and_deterministic() -> None:
    positive = [0.8, 0.9, 1.0]
    negative = [0.0, 0.1, 0.2]
    assert diagnostic_auroc(positive, negative) == 1.0
    assert diagnostic_average_precision([1.0, 1.0], [1.0, 1.0]) == 0.5
    assert cliffs_delta(positive, negative) == 1.0
    assert spearman([1.0, 2.0, 3.0], [2.0, 4.0, 6.0]) == pytest.approx(1.0)
    assert lexical_similarity("中华人民共和国", "中华人民共和国教育部") > 0.5


def test_raw_schema_cannot_contain_analysis_labels() -> None:
    assert not set(study.RAW_FIELDS) & study.FORBIDDEN_KEYS
    contaminated = [{"sample_id": "P4Q-1", "labels": {"class": "POISON"}}]
    assert forbidden_key_hits(contaminated, study.FORBIDDEN_KEYS) == ["labels"]


def test_execution_script_has_physical_three_step_cli() -> None:
    parser = study.parser()
    prepare = parser.parse_args(
        [
            "prepare",
            "--candidate-corpus",
            "candidate.jsonl",
            "--evidence-pool",
            "pool.json",
            "--source-registry",
            "source.json",
            "--companion-registry",
            "companion.json",
            "--evidence-repair",
            "repair.json",
            "--snapshot-provenance",
            "provenance.jsonl",
            "--snapshot-root",
            "snapshots",
            "--output",
            "output",
        ]
    )
    extract = parser.parse_args(["extract", "--output", "output"])
    analyze = parser.parse_args(
        [
            "analyze",
            "--output",
            "output",
            "--ground-truth",
            "gt.json",
            "--candidate-corpus",
            "candidate.jsonl",
            "--mismatch-taxonomy",
            "mismatch.jsonl",
        ]
    )
    finalize = parser.parse_args(["finalize", "--output", "output", "--repo-root", "."])
    assert prepare.command == "prepare"
    assert extract.command == "extract"
    assert analyze.command == "analyze"
    assert finalize.command == "finalize"


def test_lock_manifest_detects_raw_mutation(tmp_path: Path) -> None:
    raw = tmp_path / "raw.jsonl"
    raw.write_text(json.dumps({"sample_id": "P4Q-1"}) + "\n", encoding="utf-8")
    digest = study.sha256_file(raw)
    raw.write_text(json.dumps({"sample_id": "P4Q-2"}) + "\n", encoding="utf-8")
    assert study.sha256_file(raw) != digest
