"""Fail-closed Paper 1 annotation-field and candidate preflight gates."""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import Mapping

from .candidate_admission import (
    CandidateAdmissionStatus,
    evaluate_candidate_self_containment,
)
from .schema import SchemaValidationError


class FieldClass(str, Enum):
    ALWAYS_APPLICABLE = "ALWAYS_APPLICABLE"
    CONDITIONALLY_APPLICABLE = "CONDITIONALLY_APPLICABLE"
    PROCESS_ONLY = "PROCESS_ONLY"


@dataclass(frozen=True, slots=True, kw_only=True)
class AnnotationFieldSpec:
    field_name: str
    field_purpose: str
    field_class: FieldClass
    allowed_values: tuple[str, ...]
    yes_semantics: str
    no_semantics: str
    uncertain_semantics: str
    not_applicable_semantics: str
    applicability_condition: str
    dependency_fields: tuple[str, ...]
    evidence_requirement: str
    agreement_population: str
    missing_value_policy: str
    examples: tuple[str, ...]
    common_misinterpretations: tuple[str, ...]


def validate_annotation_field_schema(spec: AnnotationFieldSpec) -> None:
    """Reject fields whose value or applicability semantics remain ambiguous."""

    text_fields = (
        spec.field_name,
        spec.field_purpose,
        spec.yes_semantics,
        spec.no_semantics,
        spec.uncertain_semantics,
        spec.not_applicable_semantics,
        spec.applicability_condition,
        spec.evidence_requirement,
        spec.agreement_population,
        spec.missing_value_policy,
    )
    if any(not value.strip() for value in text_fields):
        raise SchemaValidationError("FIELD_SCHEMA_AMBIGUITY_BLOCKER: blank semantics")
    if len(set(spec.allowed_values)) != len(spec.allowed_values) or not spec.allowed_values:
        raise SchemaValidationError("FIELD_SCHEMA_AMBIGUITY_BLOCKER: allowed values")
    if len(spec.examples) < 5 or len(spec.common_misinterpretations) < 3:
        raise SchemaValidationError("FIELD_SCHEMA_AMBIGUITY_BLOCKER: examples")
    if spec.field_class is FieldClass.CONDITIONALLY_APPLICABLE:
        has_applicability_dependency = any(
            name.endswith("_present") for name in spec.dependency_fields
        )
        has_applicability_dependency = has_applicability_dependency or (
            spec.field_name == "assigned_stealth_level"
            and "overall_fact_status" in spec.dependency_fields
        )
        if not has_applicability_dependency or "NOT_APPLICABLE" not in spec.allowed_values:
            raise SchemaValidationError(
                "FIELD_SCHEMA_AMBIGUITY_BLOCKER: conditional applicability"
            )
    if spec.field_class is FieldClass.ALWAYS_APPLICABLE and (
        "NOT_APPLICABLE" in spec.allowed_values
    ):
        raise SchemaValidationError(
            "FIELD_SCHEMA_AMBIGUITY_BLOCKER: always-applicable N/A"
        )


GATE_NAMES = (
    "G1_SOURCE_TRACEABILITY",
    "G2_FACT_GROUNDING",
    "G3_MUTATION_VALIDITY",
    "G4_SUBJECT_UNIQUENESS",
    "G5_SELF_CONTAINMENT",
    "G6_FIELD_APPLICABILITY",
    "G7_MATCHED_TRIPLET_CONSISTENCY",
    "G8_COVERAGE_MATRIX",
    "G9_LABEL_LEAKAGE",
    "G10_EXACT_NORMALIZED_DUPLICATE",
    "G11_SEMANTIC_NEAR_DUPLICATE",
    "G12_BLIND_COLD_READER",
    "G13_ANNOTATION_ANSWERABILITY",
    "G14_RELEASE_POLICY",
)

_BARE_REFERENCE = re.compile(
    r"^(?:该)?(?:规定|条例|本办法|修订文本|20\d{2}年版|该文件)"
)


@dataclass(frozen=True, slots=True, kw_only=True)
class CandidatePreannotationInput:
    candidate_id: str
    candidate_text: str
    visible_context: str
    subject_mention: str
    canonical_subject_identity: str
    source_url: str
    source_hash: str
    fact_grounded: bool
    mutation_valid: bool
    field_applicability_defined: bool
    triplet_consistent: bool
    coverage_cell_present: bool
    label_isolated: bool
    duplicate_clear: bool
    semantic_duplicate_clear: bool
    release_policy: str


@dataclass(frozen=True, slots=True, kw_only=True)
class CandidateGateResult:
    candidate_id: str
    gate_results: Mapping[str, str]
    status: str


def blind_cold_reader(candidate_text: str, visible_context: str) -> Mapping[str, object]:
    """Inspect only fields available to a future annotator."""

    del visible_context
    subject_matches = re.findall(r"《[^》]{2,80}》", candidate_text)
    subject_unique = len(set(subject_matches)) == 1
    bare = bool(_BARE_REFERENCE.search(candidate_text.strip()))
    fact_recoverable = bool(
        re.search(
            r"施行|修订|修正|修改|调整|废止|发布|制定|机关|负责|适用|有效|"
            r"追责|通过|层级|个月|门槛|条款|管理|义务|权利|事项|文本",
            candidate_text,
        )
    )
    authority_claim = bool(re.search(r"由|制定机关|发布机关|联合发布", candidate_text))
    version_relation = bool(re.search(r"施行|修订|修正|修改|废止|替代|现行|原始文本", candidate_text))
    history_update = bool(re.search(r"历史|原始|曾经|修订|修正|修改|更新|替代|废止", candidate_text))
    failure_reasons: list[str] = []
    if not subject_unique:
        failure_reasons.append("SUBJECT_NOT_UNIQUE")
    if not fact_recoverable:
        failure_reasons.append("FACT_CLAIM_NOT_RECOVERABLE")
    if bare:
        failure_reasons.append("REQUIRED_CONTEXT_MISSING")
    return {
        "subject_unique": subject_unique,
        "core_fact_claim_recoverable": fact_recoverable,
        "authority_claim_present": authority_claim,
        "version_relation_present": version_relation,
        "history_or_update_claim_present": history_update,
        "required_context_missing": bare,
        "bare_reference_present": bare,
        "annotation_questions_unambiguous": not failure_reasons,
        "failure_reasons": failure_reasons,
        "status": "PASS" if not failure_reasons else "FAIL",
    }


def evaluate_candidate_preannotation(
    item: CandidatePreannotationInput,
) -> CandidateGateResult:
    """Run the permanent G1-G14 candidate admission gate."""

    self_containment = evaluate_candidate_self_containment(
        candidate_id=item.candidate_id,
        claim_text=item.candidate_text,
        subject_mention=item.subject_mention,
        canonical_subject_identity=item.canonical_subject_identity,
        subject_uniquely_identifiable=True,
    )
    cold = blind_cold_reader(item.candidate_text, item.visible_context)
    checks = {
        "G1_SOURCE_TRACEABILITY": bool(item.source_url and len(item.source_hash) == 64),
        "G2_FACT_GROUNDING": item.fact_grounded,
        "G3_MUTATION_VALIDITY": item.mutation_valid,
        "G4_SUBJECT_UNIQUENESS": self_containment.status
        is CandidateAdmissionStatus.ELIGIBLE_FOR_ANNOTATION,
        "G5_SELF_CONTAINMENT": cold["status"] == "PASS",
        "G6_FIELD_APPLICABILITY": item.field_applicability_defined,
        "G7_MATCHED_TRIPLET_CONSISTENCY": item.triplet_consistent,
        "G8_COVERAGE_MATRIX": item.coverage_cell_present,
        "G9_LABEL_LEAKAGE": item.label_isolated,
        "G10_EXACT_NORMALIZED_DUPLICATE": item.duplicate_clear,
        "G11_SEMANTIC_NEAR_DUPLICATE": item.semantic_duplicate_clear,
        "G12_BLIND_COLD_READER": cold["status"] == "PASS",
        "G13_ANNOTATION_ANSWERABILITY": cold["annotation_questions_unambiguous"] is True,
        "G14_RELEASE_POLICY": item.release_policy == "HASH_ONLY",
    }
    results = {name: "PASS" if checks[name] else "FAIL" for name in GATE_NAMES}
    return CandidateGateResult(
        candidate_id=item.candidate_id,
        gate_results=results,
        status="PASS" if all(checks.values()) else "FAIL",
    )


__all__ = [
    "AnnotationFieldSpec",
    "CandidateGateResult",
    "CandidatePreannotationInput",
    "FieldClass",
    "GATE_NAMES",
    "blind_cold_reader",
    "evaluate_candidate_preannotation",
    "validate_annotation_field_schema",
]
