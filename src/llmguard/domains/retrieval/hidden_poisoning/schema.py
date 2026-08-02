"""Canonical Paper 1 Pilot0 schema contracts.

The records in this module are synthetic/offline engineering contracts.  They do
not represent a frozen Benchmark or a detector implementation.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import MISSING, asdict, dataclass, fields, is_dataclass
from enum import Enum
from types import MappingProxyType
from typing import ClassVar, Mapping, Self


SCHEMA_VERSION = "paper1-pilot0-v1"
_IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")


class HiddenPoisoningError(ValueError):
    """Base error for fail-closed Pilot0 contracts."""


class SchemaValidationError(HiddenPoisoningError):
    """Raised when a canonical schema contract is invalid."""


class LabelLeakageBlocker(HiddenPoisoningError):
    """Raised when evaluator-only data reaches a runtime-facing input."""


class LeakageBlocker(HiddenPoisoningError):
    """Raised when a split or identity leakage invariant is violated."""


class AttackType(str, Enum):
    HKP_1_NUMERIC_ENTITY = "HKP_1_NUMERIC_ENTITY"
    HKP_2_CONDITION_EXCEPTION = "HKP_2_CONDITION_EXCEPTION"
    HKP_3_TEMPORAL_VERSION = "HKP_3_TEMPORAL_VERSION"
    HKP_4_PROVENANCE_AUTHORITY = "HKP_4_PROVENANCE_AUTHORITY"


class StealthLevel(str, Enum):
    S1 = "S1"
    S2 = "S2"
    S3 = "S3"


class HardNegativeType(str, Enum):
    LEGITIMATE_UPDATE = "LEGITIMATE_UPDATE"
    HISTORICAL_VERSION = "HISTORICAL_VERSION"
    NOT_YET_EFFECTIVE = "NOT_YET_EFFECTIVE"
    LEGITIMATE_EXCEPTION = "LEGITIMATE_EXCEPTION"
    REGIONAL_DIFFERENCE = "REGIONAL_DIFFERENCE"
    DEPARTMENT_DIFFERENCE = "DEPARTMENT_DIFFERENCE"
    AUTHORITY_CONFLICT = "AUTHORITY_CONFLICT"
    SAME_NAME_ENTITY = "SAME_NAME_ENTITY"
    DIFFERENT_TIME_SCOPE = "DIFFERENT_TIME_SCOPE"
    BENIGN_REWORDING = "BENIGN_REWORDING"
    NON_MALICIOUS_OMISSION = "NON_MALICIOUS_OMISSION"
    MULTI_SOURCE_COEXISTENCE = "MULTI_SOURCE_COEXISTENCE"


class FieldVisibility(str, Enum):
    RETRIEVER = "RETRIEVER"
    DETECTOR = "DETECTOR"
    INTERVENTION = "INTERVENTION"
    EVALUATOR_ONLY = "EVALUATOR_ONLY"
    RELEASEABLE = "RELEASEABLE"
    PRIVATE = "PRIVATE"


class BenchmarkLabel(str, Enum):
    CLEAN = "CLEAN"
    POISON = "POISON"
    HARD_NEGATIVE = "HARD_NEGATIVE"


class EvidenceState(str, Enum):
    AVAILABLE = "AVAILABLE"
    MISSING_EVIDENCE = "MISSING_EVIDENCE"
    INCONSISTENT = "INCONSISTENT"


class AbstentionAction(str, Enum):
    ABSTAIN = "ABSTAIN"


class AbstentionReason(str, Enum):
    MISSING_TEMPORAL_EVIDENCE = "MISSING_TEMPORAL_EVIDENCE"
    MISSING_PROVENANCE_EVIDENCE = "MISSING_PROVENANCE_EVIDENCE"
    INCOMPLETE_VERSION_CHAIN = "INCOMPLETE_VERSION_CHAIN"
    INCONSISTENT_CLAIM_IDENTITY = "INCONSISTENT_CLAIM_IDENTITY"
    INSUFFICIENT_RETAINED_DOCUMENTS = "INSUFFICIENT_RETAINED_DOCUMENTS"
    INVALID_CALIBRATED_RISK = "INVALID_CALIBRATED_RISK"


def _canonical(value: object) -> object:
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value) and not isinstance(value, type):
        return _canonical(asdict(value))
    if isinstance(value, Mapping):
        return {str(key): _canonical(item) for key, item in sorted(value.items())}
    if isinstance(value, (tuple, list)):
        return [_canonical(item) for item in value]
    if isinstance(value, (set, frozenset)):
        return sorted((_canonical(item) for item in value), key=repr)
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    raise SchemaValidationError(f"unsupported canonical value type: {type(value).__name__}")


def canonical_json(value: object) -> str:
    return json.dumps(
        _canonical(value), ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )


def canonical_sha256(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _require_text(value: object, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SchemaValidationError(f"{field_name} must be a non-empty string")
    return value


def _require_identifier(value: object, field_name: str) -> str:
    text = _require_text(value, field_name)
    if _IDENTIFIER.fullmatch(text) is None:
        raise SchemaValidationError(f"{field_name} must be a canonical identifier")
    return text


def _require_schema_version(value: object) -> None:
    if value != SCHEMA_VERSION:
        raise SchemaValidationError("unsupported schema_version")


def _freeze_mapping(value: Mapping[str, object], field_name: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise SchemaValidationError(f"{field_name} must be a mapping")
    frozen: dict[str, object] = {}
    for key, item in value.items():
        if not isinstance(key, str) or not key:
            raise SchemaValidationError(f"{field_name} keys must be non-empty strings")
        _canonical(item)
        frozen[key] = item
    return MappingProxyType(frozen)


class CanonicalRecord:
    schema_version: str
    EXPECTED_SCHEMA_VERSION: ClassVar[str] = SCHEMA_VERSION

    def canonical_payload(self) -> dict[str, object]:
        payload = _canonical(
            {
                field.name: getattr(self, field.name)
                for field in fields(self)  # type: ignore[arg-type]
            }
        )
        if not isinstance(payload, dict):  # pragma: no cover - dataclass invariant.
            raise SchemaValidationError("canonical record payload must be an object")
        return payload

    def canonical_json(self) -> str:
        return canonical_json(self.canonical_payload())

    def sha256(self) -> str:
        return canonical_sha256(self.canonical_payload())

    @classmethod
    def from_mapping(cls, payload: Mapping[str, object]) -> Self:
        if not isinstance(payload, Mapping):
            raise SchemaValidationError("record payload must be a mapping")
        allowed = {
            field.name for field in fields(cls) if field.init  # type: ignore[arg-type]
        }
        unknown = set(payload) - allowed
        missing = {
            field.name
            for field in fields(cls)  # type: ignore[arg-type]
            if field.init
            and field.default is MISSING
            and field.default_factory is MISSING
            and field.name not in payload
        }
        if unknown:
            raise SchemaValidationError(f"unknown fields: {sorted(unknown)}")
        if missing:
            raise SchemaValidationError(f"missing required fields: {sorted(missing)}")
        try:
            return cls(**dict(payload))  # type: ignore[arg-type]
        except (TypeError, ValueError) as exc:
            raise SchemaValidationError("record payload is invalid") from exc


@dataclass(frozen=True, slots=True, kw_only=True)
class ClaimRecord(CanonicalRecord):
    record_id: str
    entity_id: str
    claim_family: str
    subject: str
    predicate: str
    object_value: str
    numeric_value: float | None = None
    unit: str | None = None
    conditions: tuple[str, ...] = ()
    schema_version: str = SCHEMA_VERSION

    def __post_init__(self) -> None:
        _require_identifier(self.record_id, "record_id")
        _require_identifier(self.entity_id, "entity_id")
        _require_identifier(self.claim_family, "claim_family")
        _require_text(self.subject, "subject")
        _require_text(self.predicate, "predicate")
        _require_text(self.object_value, "object_value")
        if self.numeric_value is not None and not math.isfinite(self.numeric_value):
            raise SchemaValidationError("numeric_value must be finite")
        if not all(isinstance(item, str) and item for item in self.conditions):
            raise SchemaValidationError("conditions must contain non-empty strings")
        _require_schema_version(self.schema_version)


@dataclass(frozen=True, slots=True, kw_only=True)
class VersionRelation(CanonicalRecord):
    relation_id: str
    version_chain_id: str
    current_record_id: str
    predecessor_record_id: str | None
    successor_record_id: str | None
    effective_at: str | None
    expires_at: str | None
    repealed_at: str | None
    supersedes: tuple[str, ...] = ()
    amends: tuple[str, ...] = ()
    schema_version: str = SCHEMA_VERSION

    def __post_init__(self) -> None:
        _require_identifier(self.relation_id, "relation_id")
        _require_identifier(self.version_chain_id, "version_chain_id")
        _require_identifier(self.current_record_id, "current_record_id")
        for name in ("predecessor_record_id", "successor_record_id"):
            value = getattr(self, name)
            if value is not None:
                _require_identifier(value, name)
        for name in ("effective_at", "expires_at", "repealed_at"):
            value = getattr(self, name)
            if value is not None:
                _require_text(value, name)
        for name in ("supersedes", "amends"):
            for record_id in getattr(self, name):
                _require_identifier(record_id, name)
        _require_schema_version(self.schema_version)


@dataclass(frozen=True, slots=True, kw_only=True)
class ProvenanceRecord(CanonicalRecord):
    provenance_id: str
    source_id: str
    source_document_family: str
    source_type: str
    authority_level: str
    jurisdiction: str
    department: str
    citation_reference: str
    schema_version: str = SCHEMA_VERSION

    def __post_init__(self) -> None:
        for name in ("provenance_id", "source_id", "source_document_family"):
            _require_identifier(getattr(self, name), name)
        for name in (
            "source_type",
            "authority_level",
            "jurisdiction",
            "department",
            "citation_reference",
        ):
            _require_text(getattr(self, name), name)
        _require_schema_version(self.schema_version)


@dataclass(frozen=True, slots=True, kw_only=True)
class BenchmarkRecord(CanonicalRecord):
    record_id: str
    claim: ClaimRecord
    version: VersionRelation
    provenance: ProvenanceRecord
    document_text: str
    entity_id: str
    claim_family: str
    version_chain_id: str
    source_document_family: str
    mutation_template_family: str
    near_duplicate_cluster: str
    label: BenchmarkLabel
    attack_type: AttackType | None = None
    stealth_level: StealthLevel | None = None
    mutation_operation: str | None = None
    changed_claim_fields: tuple[str, ...] = ()
    annotator_labels: tuple[str, ...] = ()
    adjudicated_label: str | None = None
    rationale: str | None = None
    hard_negative_type: HardNegativeType | None = None
    split: str | None = None
    evaluator_notes: str | None = None
    schema_version: str = SCHEMA_VERSION

    def __post_init__(self) -> None:
        if not isinstance(self.claim, ClaimRecord):
            raise SchemaValidationError("claim must be a ClaimRecord")
        if not isinstance(self.version, VersionRelation):
            raise SchemaValidationError("version must be a VersionRelation")
        if not isinstance(self.provenance, ProvenanceRecord):
            raise SchemaValidationError("provenance must be a ProvenanceRecord")
        _require_identifier(self.record_id, "record_id")
        _require_text(self.document_text, "document_text")
        for name in (
            "entity_id",
            "claim_family",
            "version_chain_id",
            "source_document_family",
            "mutation_template_family",
            "near_duplicate_cluster",
        ):
            _require_identifier(getattr(self, name), name)
        if not isinstance(self.label, BenchmarkLabel):
            raise SchemaValidationError("label must be a BenchmarkLabel")
        if self.label is BenchmarkLabel.POISON:
            if not isinstance(self.attack_type, AttackType) or not isinstance(
                self.stealth_level, StealthLevel
            ):
                raise SchemaValidationError("poison records require attack_type and stealth_level")
        if self.label is BenchmarkLabel.HARD_NEGATIVE and not isinstance(
            self.hard_negative_type, HardNegativeType
        ):
            raise SchemaValidationError("hard-negative records require hard_negative_type")
        if self.label is not BenchmarkLabel.POISON and any(
            value is not None
            for value in (self.attack_type, self.stealth_level, self.mutation_operation)
        ):
            raise SchemaValidationError("non-poison records must not carry attack fields")
        if self.label is not BenchmarkLabel.HARD_NEGATIVE and self.hard_negative_type is not None:
            raise SchemaValidationError("only hard-negative records may carry hard_negative_type")
        if (
            self.record_id != self.version.current_record_id
            or self.entity_id != self.claim.entity_id
            or self.claim_family != self.claim.claim_family
            or self.version_chain_id != self.version.version_chain_id
            or self.source_document_family != self.provenance.source_document_family
        ):
            raise SchemaValidationError("nested record identities must be consistent")
        _require_schema_version(self.schema_version)


@dataclass(frozen=True, slots=True, kw_only=True)
class RetrievalCandidate(CanonicalRecord):
    document_id: str
    retrieval_score: float
    calibrated_risk: float | None
    metadata: Mapping[str, object]
    schema_version: str = SCHEMA_VERSION

    def __post_init__(self) -> None:
        _require_identifier(self.document_id, "document_id")
        if not math.isfinite(self.retrieval_score):
            raise SchemaValidationError("retrieval_score must be finite")
        if self.calibrated_risk is not None and not math.isfinite(self.calibrated_risk):
            raise SchemaValidationError("calibrated_risk must be finite")
        object.__setattr__(self, "metadata", _freeze_mapping(self.metadata, "metadata"))
        _require_schema_version(self.schema_version)


@dataclass(frozen=True, slots=True, kw_only=True)
class ViewEvidence(CanonicalRecord):
    view_name: str
    document_id: str
    view_score: float
    evidence_items: tuple[str, ...]
    missing_evidence: bool
    confidence: float
    explanation_fragment: str
    schema_version: str = SCHEMA_VERSION

    def __post_init__(self) -> None:
        _require_identifier(self.view_name, "view_name")
        _require_identifier(self.document_id, "document_id")
        if not math.isfinite(self.view_score):
            raise SchemaValidationError("view_score must be finite")
        if not 0.0 <= self.confidence <= 1.0:
            raise SchemaValidationError("confidence must be within [0,1]")
        _require_text(self.explanation_fragment, "explanation_fragment")
        _require_schema_version(self.schema_version)


@dataclass(frozen=True, slots=True, kw_only=True)
class DetectorOutput(CanonicalRecord):
    document_id: str
    calibrated_risk: float
    view_evidence: tuple[ViewEvidence, ...]
    explanation: str
    abstained: bool = False
    schema_version: str = SCHEMA_VERSION

    def __post_init__(self) -> None:
        _require_identifier(self.document_id, "document_id")
        if not 0.0 <= self.calibrated_risk <= 1.0:
            raise SchemaValidationError("calibrated_risk must be within [0,1]")
        _require_text(self.explanation, "explanation")
        if not all(isinstance(item, ViewEvidence) for item in self.view_evidence):
            raise SchemaValidationError("view_evidence must contain ViewEvidence records")
        _require_schema_version(self.schema_version)


@dataclass(frozen=True, slots=True, kw_only=True)
class EvidenceAvailability(CanonicalRecord):
    document_id: str
    temporal: EvidenceState
    provenance: EvidenceState
    version_chain_complete: bool
    claim_identity_consistent: bool
    schema_version: str = SCHEMA_VERSION

    def __post_init__(self) -> None:
        _require_identifier(self.document_id, "document_id")
        if not isinstance(self.temporal, EvidenceState) or not isinstance(
            self.provenance, EvidenceState
        ):
            raise SchemaValidationError("evidence states must be canonical enums")
        _require_schema_version(self.schema_version)


@dataclass(frozen=True, slots=True, kw_only=True)
class AbstentionDecision(CanonicalRecord):
    reason_code: AbstentionReason
    affected_document_ids: tuple[str, ...]
    required_evidence: tuple[str, ...]
    safe_next_action: str
    action: AbstentionAction = AbstentionAction.ABSTAIN
    schema_version: str = SCHEMA_VERSION

    def __post_init__(self) -> None:
        if not isinstance(self.reason_code, AbstentionReason):
            raise SchemaValidationError("reason_code must be canonical")
        if self.action is not AbstentionAction.ABSTAIN:
            raise SchemaValidationError("abstention action must be ABSTAIN")
        if not self.affected_document_ids:
            raise SchemaValidationError("affected_document_ids must not be empty")
        for document_id in self.affected_document_ids:
            _require_identifier(document_id, "affected_document_ids")
        if not self.required_evidence:
            raise SchemaValidationError("required_evidence must not be empty")
        _require_text(self.safe_next_action, "safe_next_action")
        _require_schema_version(self.schema_version)


__all__ = [
    "SCHEMA_VERSION",
    "AbstentionDecision",
    "AbstentionAction",
    "AbstentionReason",
    "AttackType",
    "BenchmarkLabel",
    "BenchmarkRecord",
    "CanonicalRecord",
    "ClaimRecord",
    "DetectorOutput",
    "EvidenceAvailability",
    "EvidenceState",
    "FieldVisibility",
    "HardNegativeType",
    "HiddenPoisoningError",
    "LabelLeakageBlocker",
    "LeakageBlocker",
    "ProvenanceRecord",
    "RetrievalCandidate",
    "SchemaValidationError",
    "StealthLevel",
    "VersionRelation",
    "ViewEvidence",
    "canonical_json",
    "canonical_sha256",
]
