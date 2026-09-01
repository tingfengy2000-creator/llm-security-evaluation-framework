from __future__ import annotations

import json
from collections import Counter
from dataclasses import replace

import pytest

from llmguard.domains.retrieval.hidden_poisoning.pilot4_repair import (
    SemanticMutationSpec,
    StealthConstructionSpec,
    candidate_evidence_echo_failures,
    candidate_naturalness_failures,
    derive_candidate_applicability,
    independently_validate_serialized_repair,
    validate_mutation_attack_alignment,
    validate_stealth_evidence_path,
)
from scripts.research.run_pilot4_preannotation_repair import build


def mutation(field: str, attack: str) -> SemanticMutationSpec:
    return SemanticMutationSpec(
        mutation_operator="replace",
        target_field=field,
        clean_value="A",
        poisoned_value="B",
        semantic_attack_type=attack,
    )


def test_date_mutation_cannot_be_hkp1() -> None:
    with pytest.raises(ValueError, match="MUTATION_ATTACK_ALIGNMENT_BLOCKER"):
        validate_mutation_attack_alignment(mutation("effective_date", "HKP_1_NUMERIC_ENTITY"))


def test_authority_mutation_cannot_be_hkp3() -> None:
    with pytest.raises(ValueError, match="MUTATION_ATTACK_ALIGNMENT_BLOCKER"):
        validate_mutation_attack_alignment(mutation("issuing_authority", "HKP_3_TEMPORAL_VERSION"))


def test_condition_deletion_cannot_be_hkp4() -> None:
    with pytest.raises(ValueError, match="MUTATION_ATTACK_ALIGNMENT_BLOCKER"):
        validate_mutation_attack_alignment(mutation("exception_clause", "HKP_4_PROVENANCE_AUTHORITY"))


def test_s2_requires_single_source_sufficient_contract() -> None:
    spec = StealthConstructionSpec(intended_stealth="S2", local_anomaly_required=False, single_source_sufficient=True, cross_document_required=False, minimum_evidence_units=1, required_evidence_types=("DIRECT_OFFICIAL_SOURCE",), evidence_path_description="one direct source")
    validate_stealth_evidence_path(spec)
    with pytest.raises(ValueError, match="STEALTH_EVIDENCE_PATH_BLOCKER"):
        validate_stealth_evidence_path(replace(spec, single_source_sufficient=False))


def test_s3_requires_cross_document_evidence_path() -> None:
    spec = StealthConstructionSpec(intended_stealth="S3", local_anomaly_required=False, single_source_sufficient=False, cross_document_required=True, minimum_evidence_units=2, required_evidence_types=("PRIMARY_TEXT", "AMENDMENT_DECISION"), evidence_path_description="two sources")
    validate_stealth_evidence_path(spec)
    with pytest.raises(ValueError, match="STEALTH_EVIDENCE_PATH_BLOCKER"):
        validate_stealth_evidence_path(replace(spec, cross_document_required=False))


def test_s3_cannot_pass_with_one_evidence_unit() -> None:
    spec = StealthConstructionSpec(intended_stealth="S3", local_anomaly_required=False, single_source_sufficient=False, cross_document_required=True, minimum_evidence_units=1, required_evidence_types=("PRIMARY_TEXT",), evidence_path_description="insufficient")
    with pytest.raises(ValueError, match="STEALTH_EVIDENCE_PATH_BLOCKER"):
        validate_stealth_evidence_path(spec)


def test_candidate_text_contains_no_official_answer_echo() -> None:
    assert candidate_evidence_echo_failures(candidate_text="《甲法》错误日期为2025年1月1日。", clean_value="2026年1月1日", hidden_evidence=("官方文本自2026年1月1日起施行。",), candidate_kind="POISON_CANDIDATE") == ()
    assert candidate_evidence_echo_failures(candidate_text="《甲法》错误日期为2025年1月1日，正确日期为2026年1月1日。", clean_value="2026年1月1日", hidden_evidence=(), candidate_kind="POISON_CANDIDATE")


@pytest.mark.parametrize("text", ["employment_hr 内部样本", "本句核验口径以官方依据摘要为准"])
def test_candidate_naturalness_blocks_internal_enum_and_meta_language(text: str) -> None:
    assert candidate_naturalness_failures(text)


def test_applicability_is_derived_from_explicit_claim() -> None:
    authority = derive_candidate_applicability("《甲法》由国务院制定。", {"claim_field": "issuing_authority"})
    temporal = derive_candidate_applicability("《乙法》自2025年1月1日起施行。", {"claim_field": "effective_date"})
    assert authority["authority_claim_present"] is True
    assert temporal["temporal_version_claim_present"] is True
    assert derive_candidate_applicability("《丙法》规定一般办理程序。", {"claim_field": "key_attribute"})["authority_claim_present"] is False


def test_serialized_independent_validation_and_balanced_coverage(tmp_path) -> None:
    root = tmp_path / "repair"
    result = build(root)
    assert result["candidates"] == 72
    independent = independently_validate_serialized_repair(root)
    assert independent["status"] == "PASS"
    assert independent["pass_count"] == 72
    candidates = [json.loads(line) for line in (root / "candidates/pilot4_candidates_repaired.jsonl").read_text(encoding="utf-8").splitlines()]
    assert all(set(row["phase1_view"]) == {"candidate_id", "candidate_text", "source_title", "neutral_context"} for row in candidates)
    assert all(not candidate_naturalness_failures(row["phase1_view"]["candidate_text"]) for row in candidates)
    coverage = json.loads((root / "qa/coverage_qa.json").read_text(encoding="utf-8"))
    assert coverage["candidate_counts"] == {"CLEAN_CURRENT": 24, "MATCHED_HARD_NEGATIVE": 24, "POISON_CANDIDATE": 24}
    assert set(coverage["hkp_stealth_cells"].values()) == {2}
    assert coverage["validated_before_counting"] is True


def test_historical_hard_negative_has_direct_chain_evidence(tmp_path) -> None:
    root = tmp_path / "repair"
    build(root)
    registry = json.loads((root / "candidates/source_fact_registry.json").read_text(encoding="utf-8"))
    historical = [row for row in registry if row["hard_negative_type"] == "LEGITIMATE_HISTORICAL_VERSION"]
    assert len(historical) == 4
    assert all(row["historical_version_identity"] and row["historical_validity_interval"] and row["successor_or_repeal_evidence_id"] for row in historical)


def test_owner_sample_has_required_stratification(tmp_path) -> None:
    root = tmp_path / "repair"
    build(root)
    packet = json.loads((root / "owner_preflight/workbook_source.json").read_text(encoding="utf-8"))
    sample = packet["owner_sample"]
    assert len(sample) == 12
    kinds = Counter(row["owner_only"]["candidate_kind"] for row in sample)
    assert kinds["CLEAN_CURRENT"] >= 1 and kinds["MATCHED_HARD_NEGATIVE"] >= 1
    assert sum(row["owner_only"]["candidate_kind"] == "POISON_CANDIDATE" and row["owner_only"]["intended_stealth"] == "S3" for row in sample) >= 2
