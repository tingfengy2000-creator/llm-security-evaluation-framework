from __future__ import annotations

import json
from dataclasses import replace

import pytest

from llmguard.domains.retrieval.hidden_poisoning import (
    AnnotationFieldSpec,
    CandidatePreannotationInput,
    DeterministicSemanticNearDuplicateScanner,
    FieldClass,
    GroupIdentityRecord,
    LeakageDocument,
    ProvenanceApplicability,
    SchemaValidationError,
    StructuredProvenance,
    VersionFact,
    VersionValidityStatus,
    assess_provenance,
    classify_version_fact,
    evaluate_candidate_preannotation,
    hard_negative_adjustment,
    validate_annotation_field_schema,
)
from scripts.research.run_pilot4_preannotation import build


def _field() -> AnnotationFieldSpec:
    return AnnotationFieldSpec(
        field_name="authority_matches",
        field_purpose="判断明确提出的制定机关是否正确",
        field_class=FieldClass.CONDITIONALLY_APPLICABLE,
        allowed_values=("YES", "NO", "UNCERTAIN", "NOT_APPLICABLE"),
        yes_semantics="官方证据支持",
        no_semantics="官方证据反驳",
        uncertain_semantics="证据不足",
        not_applicable_semantics="未提出机关命题",
        applicability_condition="authority_claim_present=YES",
        dependency_fields=("authority_claim_present",),
        evidence_requirement="直接官方证据",
        agreement_population="双方present=YES子集",
        missing_value_policy="不允许缺失",
        examples=("a", "b", "c", "d", "e"),
        common_misinterpretations=("host=issuer", "missing=uncertain", "ignore dependency"),
    )


def test_annotation_field_schema_gate_fails_ambiguous_conditional_field() -> None:
    validate_annotation_field_schema(_field())
    with pytest.raises(SchemaValidationError, match="FIELD_SCHEMA_AMBIGUITY_BLOCKER"):
        validate_annotation_field_schema(replace(_field(), dependency_fields=()))


def test_candidate_g1_g14_gate_and_blind_reader() -> None:
    item = CandidatePreannotationInput(
        candidate_id="P4-X",
        candidate_text="《中华人民共和国数据安全法》由全国人大常委会通过并自2021年9月1日起施行。",
        visible_context="官方文本记录通过机关和施行日期。",
        subject_mention="《中华人民共和国数据安全法》",
        canonical_subject_identity="中华人民共和国数据安全法",
        source_url="https://www.npc.gov.cn/example",
        source_hash="a" * 64,
        fact_grounded=True,
        mutation_valid=True,
        field_applicability_defined=True,
        triplet_consistent=True,
        coverage_cell_present=True,
        label_isolated=True,
        duplicate_clear=True,
        semantic_duplicate_clear=True,
        release_policy="HASH_ONLY",
    )
    result = evaluate_candidate_preannotation(item)
    assert result.status == "PASS"
    assert len(result.gate_results) == 14
    broken = replace(item, candidate_text="该条例自2021年9月1日起施行。")
    assert evaluate_candidate_preannotation(broken).status == "FAIL"


def _identity(record_id: str, chain: str) -> GroupIdentityRecord:
    return GroupIdentityRecord(
        record_id=record_id,
        entity_id=f"E-{chain}",
        claim_family=f"CF-{chain}",
        version_chain_id=chain,
        source_document_family=f"SF-{chain}",
        mutation_template_family=f"MT-{chain}",
        near_duplicate_cluster=f"ND-{chain}",
    )


def test_semantic_scanner_is_triplet_and_independence_group_aware() -> None:
    scanner = DeterministicSemanticNearDuplicateScanner(similarity_threshold=0.8)
    within = (
        LeakageDocument(record_id="A", text="《甲法》自2021年1月1日起施行。", group_identity=_identity("A", "C1"), split="P"),
        LeakageDocument(record_id="B", text="《甲法》自2022年1月1日起施行。", group_identity=_identity("B", "C1"), split="P"),
    )
    assert scanner.scan(within, required=True) == ()
    cross = within + (
        LeakageDocument(record_id="C", text="《甲法》自2021年1月1日起施行。", group_identity=_identity("C", "C2"), split="P"),
    )
    assert scanner.scan(cross, required=True)


def test_structured_temporal_and_provenance_contracts() -> None:
    historical = VersionFact(
        document_id="D1",
        subject_id="S1",
        version_id="V1",
        publication_date="2017-01-01",
        effective_date="2017-09-01",
        expiry_date="2021-01-01",
        repeal_date=None,
        predecessor=None,
        successor="V2",
        amends=(),
        supersedes=(),
        authority="全国人大常委会",
        validity_interval=("2017-09-01", "2021-01-01"),
        source_evidence=("official",),
    )
    assert classify_version_fact(historical, as_of="2019-01-01") is VersionValidityStatus.HISTORICAL_VALID
    assert classify_version_fact(historical, as_of="2019-01-01", claimed_version_id="V9") is VersionValidityStatus.VERSION_CONFLICT
    no_claim = StructuredProvenance(stated_authority=None, actual_authority="国务院", publisher="国家网信办", issuing_authority="国务院", source_family="网络数据安全管理条例", primary_or_repost="REPOST", joint_issuers=(), authority_level="行政法规", source_url="https://www.cac.gov.cn/x", source_hash="b" * 64)
    assessed = assess_provenance(no_claim)
    assert assessed.applicability is ProvenanceApplicability.PROVENANCE_NOT_APPLICABLE
    assert assessed.risk is None
    assert hard_negative_adjustment(historical_valid=True, legitimate_exception=True, scope_qualified=True) == 1.0


def test_pilot4_builder_hits_all_balanced_targets(tmp_path) -> None:
    output = tmp_path / "pilot4"
    result = build(output)
    assert result["candidates"] == 72
    coverage = json.loads((output / "qa/coverage_qa.json").read_text(encoding="utf-8"))
    assert coverage["candidate_counts"] == {
        "CLEAN_CURRENT": 24,
        "MATCHED_HARD_NEGATIVE": 24,
        "POISON_CANDIDATE": 24,
    }
    assert set(coverage["hkp_stealth_cells"].values()) == {2}
    assert coverage["length_triplet_counts"] == {"LONG": 8, "MEDIUM": 8, "SHORT": 8}
    assert coverage["authority_applicable_triplets"] >= 12
    assert coverage["temporal_applicable_triplets"] >= 12
    assert coverage["query_count"] >= 48
    assert all(value >= 1 for value in coverage["hard_negative_subtypes"].values())
    duplicate_qa = json.loads((output / "qa/near_duplicate_qa.json").read_text(encoding="utf-8"))
    assert duplicate_qa["exact_duplicate_findings"] == []
    assert duplicate_qa["normalized_duplicate_findings"] == []
    assert duplicate_qa["semantic_near_duplicate_findings"] == []
    candidates = [json.loads(line) for line in (output / "candidates/pilot4_candidates.jsonl").read_text(encoding="utf-8").splitlines()]
    assert len(candidates) == 72
    assert all(row["ground_truth_status"] == "NOT_ESTABLISHED" for row in candidates)
    assert len({row["triplet_id"] for row in candidates}) == 24
