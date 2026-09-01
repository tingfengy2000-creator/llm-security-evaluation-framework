"""Pilot4 targeted-repair contracts and independent pre-annotation validators."""

from __future__ import annotations

import json
import re
import unicodedata
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

from .annotation_quality import (
    CandidatePreannotationInput,
    blind_cold_reader,
    evaluate_candidate_preannotation,
)
from .groups import GroupIdentityRecord
from .leakage import DeterministicSemanticNearDuplicateScanner, LeakageDocument

HKP1 = "HKP_1_NUMERIC_ENTITY"
HKP2 = "HKP_2_CONDITION_EXCEPTION"
HKP3 = "HKP_3_TEMPORAL_VERSION"
HKP4 = "HKP_4_PROVENANCE_AUTHORITY"

_ATTACK_BY_FIELD = {
    "numeric_scalar": HKP1,
    "entity_attribute": HKP1,
    "key_attribute": HKP1,
    "applicability_condition": HKP2,
    "exception_clause": HKP2,
    "scope_condition": HKP2,
    "prerequisite": HKP2,
    "effective_date": HKP3,
    "expiry_date": HKP3,
    "repeal_status": HKP3,
    "revision_sequence": HKP3,
    "validity_status": HKP3,
    "issuing_authority": HKP4,
    "stated_authority": HKP4,
    "joint_issuer": HKP4,
    "authority_level": HKP4,
    "primary_repost_attribution": HKP4,
}

_META_LANGUAGE = re.compile(
    r"核验范围|核验口径|官方依据摘要|标注|实验|Ground\s*Truth|"
    r"主体和核验口径|本句主体名称|上述完整命名|公开证据由|核验时应"
)
_INTERNAL_ENUM = re.compile(
    r"employment_hr|finance_procurement|information_governance|"
    r"clean_current|poison_candidate|matched_hard_negative|HKP_[1-4]",
    re.IGNORECASE,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class SemanticMutationSpec:
    mutation_operator: str
    target_field: str
    clean_value: str
    poisoned_value: str
    semantic_attack_type: str


@dataclass(frozen=True, slots=True, kw_only=True)
class StealthConstructionSpec:
    intended_stealth: str
    local_anomaly_required: bool
    single_source_sufficient: bool
    cross_document_required: bool
    minimum_evidence_units: int
    required_evidence_types: tuple[str, ...]
    evidence_path_description: str


def validate_mutation_attack_alignment(spec: SemanticMutationSpec) -> None:
    expected = _ATTACK_BY_FIELD.get(spec.target_field)
    if expected is None or expected != spec.semantic_attack_type:
        raise ValueError(
            "MUTATION_ATTACK_ALIGNMENT_BLOCKER: "
            f"field={spec.target_field};expected={expected};actual={spec.semantic_attack_type}"
        )
    if spec.clean_value == spec.poisoned_value:
        raise ValueError("MUTATION_DID_NOT_CHANGE_FACT")


def validate_stealth_evidence_path(spec: StealthConstructionSpec) -> None:
    valid = {
        "S1": spec.local_anomaly_required
        and not spec.single_source_sufficient
        and not spec.cross_document_required,
        "S2": not spec.local_anomaly_required
        and spec.single_source_sufficient
        and not spec.cross_document_required
        and spec.minimum_evidence_units == 1,
        "S3": not spec.local_anomaly_required
        and not spec.single_source_sufficient
        and spec.cross_document_required
        and spec.minimum_evidence_units >= 2
        and len(set(spec.required_evidence_types)) >= 2,
    }
    if not valid.get(spec.intended_stealth, False):
        raise ValueError("STEALTH_EVIDENCE_PATH_BLOCKER")


def derive_candidate_applicability(
    candidate_text: str, structured_claim: Mapping[str, object]
) -> Mapping[str, bool]:
    """Derive view applicability without reading attack or candidate labels."""

    target = str(structured_claim.get("claim_field", ""))
    authority = target in {
        "issuing_authority",
        "stated_authority",
        "joint_issuer",
        "authority_level",
        "primary_repost_attribution",
    } or bool(
        re.search(r"由.{1,30}(?:制定|发布|通过|修订)|制定机关|发布机关", candidate_text)
    )
    temporal = target in {
        "effective_date",
        "expiry_date",
        "repeal_status",
        "revision_sequence",
        "validity_status",
    } or bool(
        re.search(r"施行|生效|废止|修订|修正|修改|替代|现行|历史版本", candidate_text)
    )
    history = target in {
        "repeal_status",
        "revision_sequence",
        "validity_status",
    } or bool(
        re.search(r"曾|原始文本|旧文本|历史版本|修订|修正|废止|替代", candidate_text)
    )
    condition = target in {
        "applicability_condition",
        "exception_clause",
        "scope_condition",
        "prerequisite",
    } or bool(re.search(r"适用|不适用|仅限|除外|条件|情形", candidate_text))
    numeric_entity = target in {
        "numeric_scalar",
        "entity_attribute",
        "key_attribute",
    } or bool(
        re.search(r"\d|一|二|三|四|五|六|七|八|九|十|数量|层级|个月", candidate_text)
    )
    return {
        "authority_claim_present": authority,
        "temporal_version_claim_present": temporal,
        "history_update_claim_present": history,
        "condition_exception_claim_present": condition,
        "numeric_entity_claim_present": numeric_entity,
    }


def candidate_naturalness_failures(candidate_text: str) -> tuple[str, ...]:
    failures: list[str] = []
    if _META_LANGUAGE.search(candidate_text):
        failures.append("AUDIT_OR_ANNOTATION_META_LANGUAGE")
    if _INTERNAL_ENUM.search(candidate_text):
        failures.append("INTERNAL_ENUM_TOKEN")
    if candidate_text.count("官方") >= 2:
        failures.append("OFFICIAL_EVIDENCE_PADDING")
    if re.search(r"事实以|依据摘要|核验依据|正确答案", candidate_text):
        failures.append("ANSWER_OR_AUDIT_PHRASE")
    return tuple(failures)


def candidate_evidence_echo_failures(
    *,
    candidate_text: str,
    clean_value: str,
    hidden_evidence: Sequence[str],
    candidate_kind: str,
) -> tuple[str, ...]:
    if candidate_kind != "POISON_CANDIDATE":
        return ()
    failures: list[str] = []
    if clean_value and clean_value in candidate_text:
        failures.append("CORRECT_VALUE_ECHO")
    for evidence in hidden_evidence:
        compact = evidence.strip()
        if len(compact) >= 12 and compact in candidate_text:
            failures.append("SOURCE_EVIDENCE_ECHO")
            break
    return tuple(failures)


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def independently_validate_serialized_repair(root: Path) -> Mapping[str, object]:
    """Reload serialized artifacts and independently recompute G1-G14 inputs."""

    candidates = _load_jsonl(root / "candidates/pilot4_candidates_repaired.jsonl")
    registry = _load_json(root / "candidates/source_fact_registry.json")
    assert isinstance(registry, list)
    by_triplet = {str(item["triplet_id"]): item for item in registry}
    poison_coverage = Counter(
        str(row["owner_only"]["coverage_cell"])
        for row in candidates
        if row["owner_only"]["candidate_kind"] == "POISON_CANDIDATE"
    )
    exact_owners: dict[str, str] = {}
    normalized_owners: dict[str, str] = {}
    duplicate_ids: set[str] = set()
    for row in candidates:
        candidate_id = str(row["candidate_id"])
        text = str(row["phase1_view"]["candidate_text"])
        normalized = re.sub(r"\W+", "", unicodedata.normalize("NFKC", text).casefold())
        for key, owners in ((text, exact_owners), (normalized, normalized_owners)):
            previous = owners.get(key)
            if previous is None:
                owners[key] = candidate_id
            else:
                duplicate_ids.update((previous, candidate_id))
    documents = tuple(
        LeakageDocument(
            record_id=str(row["candidate_id"]),
            text=str(row["phase1_view"]["candidate_text"]),
            group_identity=GroupIdentityRecord(
                record_id=str(row["candidate_id"]),
                entity_id=str(row["triplet_id"]),
                claim_family=f"CF-{row['triplet_id']}",
                version_chain_id=str(row["triplet_id"]),
                source_document_family=f"SF-{row['triplet_id']}",
                mutation_template_family=f"MT-{row['triplet_id']}",
                near_duplicate_cluster=f"ND-{row['triplet_id']}",
            ),
            split="PREFLIGHT",
        )
        for row in candidates
    )
    semantic_findings = DeterministicSemanticNearDuplicateScanner(
        similarity_threshold=0.88
    ).scan(documents, required=True)
    semantic_duplicate_ids = {
        candidate_id
        for finding in semantic_findings
        for candidate_id in (finding.left_record_id, finding.right_record_id)
    }
    phase1_forbidden = {
        "candidate_kind",
        "semantic_attack_type",
        "intended_stealth",
        "correct_evidence",
        "hard_negative_type",
        "mutation_spec",
    }
    results: list[dict[str, Any]] = []
    for row in candidates:
        triplet = str(row["triplet_id"])
        source = by_triplet[triplet]
        phase1 = row["phase1_view"]
        assert isinstance(phase1, dict)
        owner = row["owner_only"]
        assert isinstance(owner, dict)
        claim = row["structured_claim"]
        assert isinstance(claim, dict)
        text = str(phase1["candidate_text"])
        kind = str(owner["candidate_kind"])
        mutation = SemanticMutationSpec(**source["mutation_spec"])
        validate_mutation_attack_alignment(mutation)
        applicability = derive_candidate_applicability(text, claim)
        stored_applicability = row["derived_applicability"]
        assert isinstance(stored_applicability, dict)
        source_traceable = (
            str(source["official_source"]).startswith("https://")
            and len(str(source["source_hash"])) == 64
        )
        if kind == "CLEAN_CURRENT":
            fact_grounded = claim == source["clean_claim_struct"]
            mutation_valid = True
        elif kind == "MATCHED_HARD_NEGATIVE":
            fact_grounded = claim == source["hard_negative_claim_struct"]
            mutation_valid = True
        else:
            fact_grounded = claim["claim_field"] == mutation.target_field
            mutation_valid = (
                claim["claim_value"] == mutation.poisoned_value
                and source["clean_claim_struct"]["claim_value"] == mutation.clean_value
            )
        visible_blob = json.dumps(phase1, ensure_ascii=False).lower()
        label_isolated = not (phase1_forbidden & set(phase1)) and not any(
            token.lower() in visible_blob
            for token in (
                str(owner.get("candidate_kind", "")),
                str(owner.get("semantic_attack_type", "")),
                str(owner.get("intended_stealth", "")),
            )
            if token
        )
        triplet_rows = [item for item in candidates if item["triplet_id"] == triplet]
        triplet_consistent = (
            len(triplet_rows) == 3
            and len({item["phase1_view"]["source_title"] for item in triplet_rows}) == 1
        )
        natural = not candidate_naturalness_failures(text)
        echo_clear = not candidate_evidence_echo_failures(
            candidate_text=text,
            clean_value=mutation.clean_value,
            hidden_evidence=[
                str(unit["evidence_text"]) for unit in source["evidence_units"]
            ],
            candidate_kind=kind,
        )
        gate = evaluate_candidate_preannotation(
            CandidatePreannotationInput(
                candidate_id=str(row["candidate_id"]),
                candidate_text=text,
                visible_context=str(phase1["neutral_context"]),
                subject_mention=f"《{source['subject']}》",
                canonical_subject_identity=str(source["subject"]),
                source_url=str(source["official_source"]) if source_traceable else "",
                source_hash=str(source["source_hash"]),
                fact_grounded=fact_grounded,
                mutation_valid=mutation_valid,
                field_applicability_defined=applicability == stored_applicability,
                triplet_consistent=triplet_consistent,
                coverage_cell_present=(
                    bool(owner.get("coverage_cell"))
                    and poison_coverage[str(owner["coverage_cell"])] == 2
                ),
                label_isolated=label_isolated,
                duplicate_clear=str(row["candidate_id"]) not in duplicate_ids,
                semantic_duplicate_clear=(
                    str(row["candidate_id"]) not in semantic_duplicate_ids
                ),
                release_policy=str(source["release_policy"]),
            )
        )
        failures = [] if natural and echo_clear else ["NATURALNESS_OR_ECHO"]
        if gate.status != "PASS":
            failures.extend(
                name for name, status in gate.gate_results.items() if status != "PASS"
            )
        results.append(
            {
                "candidate_id": row["candidate_id"],
                "status": "PASS" if not failures else "FAIL",
                "gate_results": dict(gate.gate_results),
                "naturalness": natural,
                "evidence_echo_clear": echo_clear,
                "phase1_fields_used": sorted(phase1),
                "cold_reader": blind_cold_reader(text, str(phase1["neutral_context"])),
                "failures": failures,
            }
        )
    return {
        "validator": "SERIALIZED_ARTIFACT_RELOAD_V1",
        "candidate_count": len(results),
        "pass_count": sum(item["status"] == "PASS" for item in results),
        "status": "PASS"
        if all(item["status"] == "PASS" for item in results)
        else "FAIL",
        "rows": results,
    }


__all__ = [
    "SemanticMutationSpec",
    "StealthConstructionSpec",
    "candidate_evidence_echo_failures",
    "candidate_naturalness_failures",
    "derive_candidate_applicability",
    "independently_validate_serialized_repair",
    "validate_mutation_attack_alignment",
    "validate_stealth_evidence_path",
]
