from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from llmguard.domains.retrieval.hidden_poisoning.method_engineering import (
    ABLATION_MATRIX,
    BASELINE_MATRIX,
    BREAKDOWN_AXES,
    EXPLANATION_CONTRACT,
    FIVE_VIEW_SIGNAL_REGISTRY,
    FORMAL_RESEARCH_QUESTIONS,
    METRIC_CONTRACTS,
    PAPER1_FUSION_DESIGN,
    PAPER1_RISK_CALIBRATION_DESIGN,
    SCALE_READINESS,
    DetectorFeatureVector,
    SignalObservation,
    SignalView,
    signals_for_view,
)
from scripts.research import finalize_pilot4_gt_and_signal_kickoff as kickoff


def test_five_view_registry_is_complete_and_unique() -> None:
    assert {signal.view for signal in FIVE_VIEW_SIGNAL_REGISTRY} == set(SignalView)
    assert len({signal.signal_name for signal in FIVE_VIEW_SIGNAL_REGISTRY}) == len(
        FIVE_VIEW_SIGNAL_REGISTRY
    )
    assert all(signals_for_view(view) for view in SignalView)
    assert {view: len(signals_for_view(view)) for view in SignalView} == {
        SignalView.SEMANTIC: 6,
        SignalView.ENTITY_CLAIM: 9,
        SignalView.PROVENANCE: 8,
        SignalView.TEMPORAL_VERSION: 9,
        SignalView.RETRIEVAL_BEHAVIOR: 10,
    }


def test_required_signals_are_registered() -> None:
    names = {signal.signal_name for signal in FIVE_VIEW_SIGNAL_REGISTRY}
    assert {
        "semantic_version_margin",
        "negation_flip",
        "claimed_authority_match",
        "present_time_substitution_signal",
        "ranking_stability",
    } <= names


def test_signal_contract_has_all_required_metadata() -> None:
    for signal in FIVE_VIEW_SIGNAL_REGISTRY:
        assert signal.definition
        assert signal.input_fields
        assert signal.applicability
        assert signal.missing_value_semantics
        assert signal.evidence_dependency
        assert signal.expected_attack_relevance
        assert signal.explanation_role


def test_not_applicable_is_not_encoded_as_safe_zero() -> None:
    observation = SignalObservation(
        signal_name="claimed_authority_match",
        view=SignalView.PROVENANCE,
        value=None,
        applicable=False,
        confidence=None,
        evidence_quality=None,
        missing_reason="NO_AUTHORITY_CLAIM",
    )
    payload = DetectorFeatureVector(
        candidate_id="C1", query_id=None, observations=(observation,)
    ).feature_payload()
    assert payload["claimed_authority_match__value"] is None
    assert payload["claimed_authority_match__applicable"] is False
    with pytest.raises(ValueError):
        SignalObservation(
            signal_name="claimed_authority_match",
            view=SignalView.PROVENANCE,
            value=0.0,
            applicable=False,
            confidence=None,
            evidence_quality=None,
            missing_reason="NO_AUTHORITY_CLAIM",
        )


def test_baseline_matrix_freezes_mlm_and_gmtp_roles() -> None:
    baselines = {baseline.name: baseline for baseline in BASELINE_MATRIX}
    assert (
        baselines["MLM_NATURALNESS"].role
        == "LEXICAL_NATURALNESS_BASELINE_AND_SEMANTIC_SIGNAL"
    )
    assert baselines["GMTP"].role == "STRONG_EXTERNAL_POISONING_DEFENSE_BASELINE"
    assert baselines["GMTP"].required_reproduction_record is True


def test_fusion_risk_and_explanation_boundaries() -> None:
    assert PAPER1_FUSION_DESIGN.primary_estimator == "LOGISTIC_REGRESSION"
    assert set(PAPER1_FUSION_DESIGN.nonlinear_comparators) == {"XGBOOST", "LIGHTGBM"}
    assert "LARGE_TRANSFORMER_FUSION" in PAPER1_FUSION_DESIGN.forbidden_estimators
    assert (
        PAPER1_RISK_CALIBRATION_DESIGN.selection_population
        == "DEVELOPMENT_PROTOCOL_ONLY"
    )
    assert EXPLANATION_CONTRACT["free_form_llm_only_allowed"] is False


def test_metric_ablation_and_scale_contracts() -> None:
    metrics = {metric.name: metric for metric in METRIC_CONTRACTS}
    assert metrics["HARD_NEGATIVE_FPR"].population == "HARD_NEGATIVE_ONLY"
    assert "Hard Negative" in metrics["HARD_NEGATIVE_FPR"].definition
    assert len(ABLATION_MATRIX) == 11
    assert set(BREAKDOWN_AXES) == {"HKP1", "HKP2", "HKP3", "HKP4", "S1", "S2", "S3"}
    assert SCALE_READINESS["independent_groups"] == 240
    assert SCALE_READINESS["generated"] is False
    assert (
        SCALE_READINESS["split_rule"]
        == "VERSION_CHAIN_GROUP_AWARE_NO_CHAIN_ACROSS_TRAIN_DEV_TEST"
    )
    assert len(FORMAL_RESEARCH_QUESTIONS) == 5


def _candidate() -> dict[str, object]:
    fields = [
        "text_naturalness",
        "local_internal_conflict",
        "phase1_issue",
        "overall_fact_status",
        "version_claim_status",
        "authority_claim_status",
        "minimum_external_evidence_needed",
        "phase2_issue",
    ]
    records = [
        {
            "sample_id": f"P4Q-{index:016x}",
            "labels": {field: "VALUE" for field in fields},
        }
        for index in range(72)
    ]
    return {
        "id": "PILOT4_FINAL72_GROUND_TRUTH_CANDIDATE_V1",
        "record_count": 72,
        "canonical_fields": fields,
        "candidate_corpus_sha256": "a" * 64,
        "value_precedence": [
            "A_B_CONSENSUS",
            "OWNER_EXPECTED_BLIND_ADJUDICATION_FOR_DISAGREEMENTS",
        ],
        "records": records,
    }


def test_gt_acceptance_preserves_values_and_freezes_development_role(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    candidate = _candidate()
    candidate_path = tmp_path / "candidate.json"
    candidate_path.write_text(json.dumps(candidate), encoding="utf-8")
    digest = hashlib.sha256(candidate_path.read_bytes()).hexdigest()
    monkeypatch.setattr(kickoff, "SOURCE_CANDIDATE_SHA256", digest)
    loaded = kickoff.load_candidate(candidate_path)
    final = kickoff.accepted_gt(loaded)
    assert final["id"] == "PILOT4_FINAL72_GROUND_TRUTH_V1"
    assert final["owner_acceptance"] is True
    assert final["role"] == "DEVELOPMENT_AND_METHOD_ENGINEERING_SET"
    assert final["untouched_final_test_set"] is False
    assert final["formal_dataset_freeze"] is False
    assert final["records"] == candidate["records"]
    assert final["expected_v3_value_precedence"] is False


def test_method_documents_are_complete_and_do_not_claim_results() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    checked = kickoff.validate_method_docs(repo_root)
    assert len(checked) == 6
    feasibility = (repo_root / checked[1]).read_text(encoding="utf-8")
    assert "EXECUTED / DEVELOPMENT_SET_DIAGNOSTIC_ONLY" in feasibility
    assert "本结果不是 Detector、正式 test 或论文效果" in feasibility
    assert "HYPOTHESIS / EXPERIMENTAL QUESTION" in feasibility
    scale = (repo_root / checked[-1]).read_text(encoding="utf-8")
    assert "DATA_NOT_GENERATED" in scale
    assert "VERSION_CHAIN_GROUP_AWARE" in scale
