from __future__ import annotations

import json
import math
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from types import MappingProxyType
from typing import TypeAlias


AuditValue: TypeAlias = (
    str
    | int
    | float
    | bool
    | None
    | list["AuditValue"]
    | dict[str, "AuditValue"]
)

_FORBIDDEN_PIPELINE_FIELD_NAMES = frozenset(
    {
        "poisoned",
        "label",
        "attack_goal",
        "expected_answer",
        "failure_type",
        "ground_truth",
    }
)
_NORMALIZED_FORBIDDEN_PIPELINE_FIELDS = frozenset(
    re.sub(r"[^a-z0-9]+", "", name.casefold())
    for name in _FORBIDDEN_PIPELINE_FIELD_NAMES
)

_GENERATOR_AUDIT_KEYS = frozenset(
    {
        "provider",
        "model",
        "model_name",
        "seed",
        "temperature",
        "max_tokens",
        "revision",
    }
)
_DETECTOR_RESULT_AUDIT_KEYS = frozenset(
    {
        "detector_id",
        "detector_name",
        "detector_source",
        "passed",
        "score",
        "matched",
        "rule_ids",
        "output_hash",
        "output_length",
        "method_version",
    }
)
_METRICS_AUDIT_KEYS = frozenset(
    {
        "rpr",
        "cir",
        "rmsr",
        "faithfulness",
        "cross_layer_leakage",
        "retrieval_poison_rate",
        "context_injection_rate",
        "retrieval_manipulation_success_rate",
        "cross_layer_leakage_rate",
    }
)
_LATENCY_AUDIT_KEYS = frozenset(
    {
        "retrieval_ms",
        "evidence_ms",
        "trust_ms",
        "context_ms",
        "generation_ms",
        "evaluation_ms",
        "total_ms",
    }
)
_VALIDATION_STATUS_AUDIT_KEYS = frozenset(
    {
        "status",
        "valid",
        "issue_codes",
        "method_version",
    }
)
_TRUST_SIGNAL_SUMMARY_AUDIT_KEYS = frozenset(
    {
        "signal_count",
        "signal_types",
        "method_versions",
        "evidence_hashes",
        "aggregate_score",
        "ranking_changed",
        "blocked_doc_ids",
    }
)

# Stage 6.1 signal extensions require an explicit feature contract.
EVIDENCE_FEATURE_ALLOWLISTS: Mapping[str, frozenset[str]] = MappingProxyType(
    {
        "provenance_signal": frozenset(
            {
                "source_id",
                "source_type",
                "timestamp",
                "version",
                "content_hash",
                "source_count",
                "document_count",
                "age_days",
            }
        ),
        "embedding_anomaly_signal": frozenset(
            {
                "rank",
                "distance",
                "similarity",
                "mean_distance",
                "std_distance",
                "z_score",
                "top_k",
            }
        ),
        "semantic_conflict_signal": frozenset(
            {
                "pair_count",
                "conflict_count",
                "max_conflict_score",
                "mean_conflict_score",
                "compared_doc_ids",
            }
        ),
        "source_diversity_signal": frozenset(
            {
                "source_count",
                "document_count",
                "diversity_ratio",
                "source_types",
            }
        ),
    }
)
_EVIDENCE_FEATURE_SEQUENCE_KEYS: Mapping[str, frozenset[str]] = MappingProxyType(
    {
        "semantic_conflict_signal": frozenset({"compared_doc_ids"}),
        "source_diversity_signal": frozenset({"source_types"}),
    }
)
_NORMALIZED_GROUND_TRUTH_FIELDS = frozenset({"groundtruth"})


def _find_normalized_field(
    value: object,
    normalized_fields: frozenset[str],
    path: str = "$",
) -> tuple[str, str] | None:
    if isinstance(value, Mapping):
        for key, nested_value in value.items():
            if isinstance(key, str):
                normalized_key = re.sub(r"[^a-z0-9]+", "", key.casefold())
                if normalized_key in normalized_fields:
                    return key, f"{path}.{key}"
            found = _find_normalized_field(
                nested_value,
                normalized_fields,
                f"{path}.{key}",
            )
            if found is not None:
                return found
    elif (
        isinstance(value, Sequence)
        and not isinstance(value, (str, bytes, bytearray))
    ) or isinstance(value, (set, frozenset)):
        for index, nested_value in enumerate(value):
            found = _find_normalized_field(
                nested_value,
                normalized_fields,
                f"{path}[{index}]",
            )
            if found is not None:
                return found
    return None


def _find_forbidden_pipeline_field(
    value: object,
    path: str = "$",
) -> tuple[str, str] | None:
    return _find_normalized_field(
        value,
        _NORMALIZED_FORBIDDEN_PIPELINE_FIELDS,
        path,
    )


def _deep_freeze(value: object) -> object:
    if isinstance(value, Mapping):
        if not all(isinstance(key, str) for key in value):
            raise TypeError("mapping keys must be strings")
        return MappingProxyType(
            {
                key: _deep_freeze(value[key])
                for key in sorted(value)
            }
        )
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return tuple(_deep_freeze(item) for item in value)
    if isinstance(value, (set, frozenset)):
        frozen_items = tuple(_deep_freeze(item) for item in value)
        return tuple(sorted(frozen_items, key=_frozen_sort_key))
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    raise TypeError(f"unsupported immutable value type: {type(value).__name__}")


def _frozen_sort_key(value: object) -> str:
    return json.dumps(
        _thaw_json_value(value),
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    )


def _thaw_json_value(value: object) -> AuditValue:
    if isinstance(value, Mapping):
        return {
            key: _thaw_json_value(value[key])
            for key in sorted(value)
        }
    if isinstance(value, tuple):
        return [_thaw_json_value(item) for item in value]
    return _audit_scalar(value, "value")


def _freeze_mapping(
    value: Mapping[str, object],
    field_name: str,
) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{field_name} must be a mapping")
    frozen = _deep_freeze(value)
    assert isinstance(frozen, Mapping)
    return frozen


def _audit_scalar(value: object, path: str) -> str | int | float | bool | None:
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float) and math.isfinite(value):
        return value
    raise ValueError(f"{path} must contain only JSON-safe scalar values")


def _audit_sequence(value: object, path: str) -> list[AuditValue]:
    if not isinstance(value, tuple):
        raise ValueError(f"{path} must be a deterministic sequence")
    return [_audit_scalar(item, path) for item in value]


def _allowlisted_audit_mapping(
    value: Mapping[str, object],
    *,
    allowed_keys: frozenset[str],
    sequence_keys: frozenset[str] = frozenset(),
    field_name: str,
) -> dict[str, AuditValue]:
    unknown = set(value) - allowed_keys
    if unknown:
        raise ValueError(f"{field_name} contains unknown keys: {sorted(unknown)}")

    result: dict[str, AuditValue] = {}
    for key in sorted(value):
        item = value[key]
        if isinstance(item, Mapping):
            raise ValueError(f"{field_name}.{key} nested mappings are not allowed")
        if key in sequence_keys:
            result[key] = _audit_sequence(item, f"{field_name}.{key}")
        else:
            if isinstance(item, tuple):
                raise ValueError(f"{field_name}.{key} sequences are not allowed")
            result[key] = _audit_scalar(item, f"{field_name}.{key}")
    return result


@dataclass(frozen=True)
class DocumentRecord:
    doc_id: str
    content: str
    source_id: str
    source_type: str
    timestamp: str
    version: str
    content_hash: str


@dataclass(frozen=True)
class QueryRecord:
    query_id: str
    attack_id: str | None
    category: str
    retrieval_query: str
    generation_question: str
    expected_clean_doc_ids: tuple[str, ...]
    metadata: Mapping[str, object]

    def __post_init__(self) -> None:
        if not isinstance(self.metadata, Mapping):
            raise ValueError("metadata must be a mapping")
        forbidden = _find_forbidden_pipeline_field(self.metadata, "$.metadata")
        if forbidden is not None:
            field_name, path = forbidden
            raise ValueError(f"forbidden field '{field_name}' at {path}")
        object.__setattr__(
            self,
            "expected_clean_doc_ids",
            tuple(self.expected_clean_doc_ids),
        )
        object.__setattr__(
            self,
            "metadata",
            _freeze_mapping(self.metadata, "metadata"),
        )


@dataclass(frozen=True)
class RetrievalEvidence:
    query_id: str
    doc_id: str
    rank: int
    distance: float
    similarity: float
    source_id: str
    source_type: str
    timestamp: str
    version: str
    content_hash: str
    content_ref: str

    def to_audit_dict(self) -> dict[str, AuditValue]:
        return {
            "query_id": self.query_id,
            "doc_id": self.doc_id,
            "rank": self.rank,
            "distance": self.distance,
            "similarity": self.similarity,
            "source_id": self.source_id,
            "source_type": self.source_type,
            "timestamp": self.timestamp,
            "version": self.version,
            "content_hash": self.content_hash,
            "content_ref": self.content_ref,
        }


@dataclass(frozen=True)
class EvidenceSignal:
    signal_type: str
    query_id: str
    doc_ids: tuple[str, ...]
    value: float
    features: Mapping[str, object]
    method_version: str
    evidence_hash: str

    def __post_init__(self) -> None:
        allowed_keys = EVIDENCE_FEATURE_ALLOWLISTS.get(self.signal_type)
        if allowed_keys is None:
            raise ValueError(f"unknown signal_type: {self.signal_type}")
        if not isinstance(self.features, Mapping):
            raise ValueError("features must be a mapping")

        forbidden = _find_normalized_field(
            self.features,
            _NORMALIZED_GROUND_TRUTH_FIELDS,
            "$.features",
        )
        if forbidden is not None:
            field_name, path = forbidden
            raise ValueError(f"forbidden field '{field_name}' at {path}")

        unknown = set(self.features) - allowed_keys
        if unknown:
            raise ValueError(f"features contains unknown keys: {sorted(unknown)}")

        object.__setattr__(self, "doc_ids", tuple(self.doc_ids))
        object.__setattr__(
            self,
            "features",
            _freeze_mapping(self.features, "features"),
        )

    def to_audit_dict(self) -> dict[str, AuditValue]:
        return {
            "signal_type": self.signal_type,
            "query_id": self.query_id,
            "doc_ids": list(self.doc_ids),
            "value": self.value,
            "features": _allowlisted_audit_mapping(
                self.features,
                allowed_keys=EVIDENCE_FEATURE_ALLOWLISTS[self.signal_type],
                sequence_keys=_EVIDENCE_FEATURE_SEQUENCE_KEYS.get(
                    self.signal_type,
                    frozenset(),
                ),
                field_name="features",
            ),
            "method_version": self.method_version,
            "evidence_hash": self.evidence_hash,
        }


@dataclass(frozen=True)
class TrustAssessment:
    mode: str
    aggregate_score: float | None
    ranking_changed: bool
    blocked_doc_ids: tuple[str, ...]
    signals: tuple[EvidenceSignal, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "blocked_doc_ids", tuple(self.blocked_doc_ids))
        object.__setattr__(self, "signals", tuple(self.signals))

    @classmethod
    def off(cls) -> TrustAssessment:
        return cls(
            mode="off",
            aggregate_score=None,
            ranking_changed=False,
            blocked_doc_ids=(),
            signals=(),
        )

    @classmethod
    def observe(cls, signals: Sequence[EvidenceSignal]) -> TrustAssessment:
        return cls(
            mode="observe",
            aggregate_score=None,
            ranking_changed=False,
            blocked_doc_ids=(),
            signals=tuple(signals),
        )


@dataclass(frozen=True)
class RAGAttemptRecord:
    attempt_id: str
    run_id: str
    query_id: str
    attack_id: str | None
    guard_mode: str
    retrieval_policy: str
    retrieval_evidence: tuple[RetrievalEvidence, ...]
    evidence_signals: tuple[EvidenceSignal, ...]
    context_hash: str
    context_length: int
    generator: Mapping[str, object]
    final_answer_hash: str
    final_answer_length: int
    detector_results: tuple[Mapping[str, object], ...]
    metrics: Mapping[str, object]
    failure_types: tuple[str, ...]
    latency: Mapping[str, object]
    validation_status: Mapping[str, object]

    def __post_init__(self) -> None:
        if self.retrieval_policy not in {"off", "observe"}:
            raise ValueError("retrieval_policy must be 'off' or 'observe'")
        object.__setattr__(
            self,
            "retrieval_evidence",
            tuple(self.retrieval_evidence),
        )
        object.__setattr__(
            self,
            "evidence_signals",
            tuple(self.evidence_signals),
        )
        object.__setattr__(self, "failure_types", tuple(self.failure_types))
        object.__setattr__(
            self,
            "generator",
            _freeze_mapping(self.generator, "generator"),
        )
        object.__setattr__(
            self,
            "detector_results",
            tuple(
                _freeze_mapping(result, "detector_results item")
                for result in self.detector_results
            ),
        )
        object.__setattr__(
            self,
            "metrics",
            _freeze_mapping(self.metrics, "metrics"),
        )
        object.__setattr__(
            self,
            "latency",
            _freeze_mapping(self.latency, "latency"),
        )
        object.__setattr__(
            self,
            "validation_status",
            _freeze_mapping(self.validation_status, "validation_status"),
        )

    def to_audit_dict(self) -> dict[str, AuditValue]:
        return {
            "attempt_id": self.attempt_id,
            "run_id": self.run_id,
            "query_id": self.query_id,
            "attack_id": self.attack_id,
            "guard_mode": self.guard_mode,
            "retrieval_policy": self.retrieval_policy,
            "retrieval_evidence": [
                item.to_audit_dict() for item in self.retrieval_evidence
            ],
            "evidence_signals": [
                item.to_audit_dict() for item in self.evidence_signals
            ],
            "context_hash": self.context_hash,
            "context_length": self.context_length,
            "generator": _allowlisted_audit_mapping(
                self.generator,
                allowed_keys=_GENERATOR_AUDIT_KEYS,
                field_name="generator",
            ),
            "final_answer_hash": self.final_answer_hash,
            "final_answer_length": self.final_answer_length,
            "detector_results": [
                _allowlisted_audit_mapping(
                    result,
                    allowed_keys=_DETECTOR_RESULT_AUDIT_KEYS,
                    sequence_keys=frozenset({"rule_ids"}),
                    field_name="detector_results item",
                )
                for result in self.detector_results
            ],
            "metrics": _allowlisted_audit_mapping(
                self.metrics,
                allowed_keys=_METRICS_AUDIT_KEYS,
                field_name="metrics",
            ),
            "failure_types": list(self.failure_types),
            "latency": _allowlisted_audit_mapping(
                self.latency,
                allowed_keys=_LATENCY_AUDIT_KEYS,
                field_name="latency",
            ),
            "validation_status": _allowlisted_audit_mapping(
                self.validation_status,
                allowed_keys=_VALIDATION_STATUS_AUDIT_KEYS,
                sequence_keys=frozenset({"issue_codes"}),
                field_name="validation_status",
            ),
        }


@dataclass(frozen=True)
class RAGSecurityEnvelope:
    query_id: str
    retrieved_doc_ids: tuple[str, ...]
    evidence_hashes: tuple[str, ...]
    trust_signal_summary: Mapping[str, object]
    retrieval_policy: str
    failure_types: tuple[str, ...]
    context_hash: str
    final_answer_hash: str
    run_id: str

    def __post_init__(self) -> None:
        if self.retrieval_policy not in {"off", "observe"}:
            raise ValueError("retrieval_policy must be 'off' or 'observe'")
        object.__setattr__(
            self,
            "retrieved_doc_ids",
            tuple(self.retrieved_doc_ids),
        )
        object.__setattr__(
            self,
            "evidence_hashes",
            tuple(self.evidence_hashes),
        )
        object.__setattr__(self, "failure_types", tuple(self.failure_types))
        object.__setattr__(
            self,
            "trust_signal_summary",
            _freeze_mapping(
                self.trust_signal_summary,
                "trust_signal_summary",
            ),
        )

    def to_audit_dict(self) -> dict[str, AuditValue]:
        return {
            "query_id": self.query_id,
            "retrieved_doc_ids": list(self.retrieved_doc_ids),
            "evidence_hashes": list(self.evidence_hashes),
            "trust_signal_summary": _allowlisted_audit_mapping(
                self.trust_signal_summary,
                allowed_keys=_TRUST_SIGNAL_SUMMARY_AUDIT_KEYS,
                sequence_keys=frozenset(
                    {
                        "signal_types",
                        "method_versions",
                        "evidence_hashes",
                        "blocked_doc_ids",
                    }
                ),
                field_name="trust_signal_summary",
            ),
            "retrieval_policy": self.retrieval_policy,
            "failure_types": list(self.failure_types),
            "context_hash": self.context_hash,
            "final_answer_hash": self.final_answer_hash,
            "run_id": self.run_id,
        }
