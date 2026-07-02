from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
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

_BODY_FIELD_NAMES = frozenset(
    {
        "answer",
        "answer_body",
        "body",
        "content",
        "document",
        "document_body",
        "document_content",
        "final_answer",
    }
)


def _canonical_audit_value(value: object) -> AuditValue:
    if isinstance(value, Mapping):
        result: dict[str, AuditValue] = {}
        for key in sorted(value):
            if not isinstance(key, str):
                raise TypeError("audit mapping keys must be strings")
            if key.lower() in _BODY_FIELD_NAMES:
                continue
            result[key] = _canonical_audit_value(value[key])
        return result
    if isinstance(value, (set, frozenset)):
        serialized = [_canonical_audit_value(item) for item in value]
        return sorted(
            serialized,
            key=lambda item: json.dumps(
                item,
                ensure_ascii=True,
                separators=(",", ":"),
                sort_keys=True,
            ),
        )
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_canonical_audit_value(item) for item in value]
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    raise TypeError(f"unsupported audit value type: {type(value).__name__}")


def _canonical_audit_mapping(value: Mapping[str, object]) -> dict[str, AuditValue]:
    serialized = _canonical_audit_value(value)
    if not isinstance(serialized, dict):
        raise TypeError("audit value must be a mapping")
    return serialized


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

    def to_audit_dict(self) -> dict[str, AuditValue]:
        return {
            "signal_type": self.signal_type,
            "query_id": self.query_id,
            "doc_ids": list(self.doc_ids),
            "value": self.value,
            "features": _canonical_audit_mapping(self.features),
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
    retrieval_policy: Mapping[str, object]
    retrieval_evidence: tuple[RetrievalEvidence, ...]
    evidence_signals: tuple[EvidenceSignal, ...]
    context_hash: str
    context_length: int
    generator: Mapping[str, object]
    final_answer_hash: str
    final_answer_length: int
    detector_results: Mapping[str, object]
    metrics: Mapping[str, object]
    failure_types: tuple[str, ...]
    latency: Mapping[str, object]
    validation_status: str

    def to_audit_dict(self) -> dict[str, AuditValue]:
        return {
            "attempt_id": self.attempt_id,
            "run_id": self.run_id,
            "query_id": self.query_id,
            "attack_id": self.attack_id,
            "guard_mode": self.guard_mode,
            "retrieval_policy": _canonical_audit_mapping(self.retrieval_policy),
            "retrieval_evidence": [
                item.to_audit_dict() for item in self.retrieval_evidence
            ],
            "evidence_signals": [
                item.to_audit_dict() for item in self.evidence_signals
            ],
            "context_hash": self.context_hash,
            "context_length": self.context_length,
            "generator": _canonical_audit_mapping(self.generator),
            "final_answer_hash": self.final_answer_hash,
            "final_answer_length": self.final_answer_length,
            "detector_results": _canonical_audit_mapping(self.detector_results),
            "metrics": _canonical_audit_mapping(self.metrics),
            "failure_types": list(self.failure_types),
            "latency": _canonical_audit_mapping(self.latency),
            "validation_status": self.validation_status,
        }


@dataclass(frozen=True)
class RAGSecurityEnvelope:
    query_id: str
    retrieved_doc_ids: tuple[str, ...]
    evidence_hashes: tuple[str, ...]
    trust_signal_summary: Mapping[str, object]
    retrieval_policy: Mapping[str, object]
    failure_types: tuple[str, ...]
    context_hash: str
    final_answer_hash: str
    run_id: str

    def to_audit_dict(self) -> dict[str, AuditValue]:
        return {
            "query_id": self.query_id,
            "retrieved_doc_ids": list(self.retrieved_doc_ids),
            "evidence_hashes": list(self.evidence_hashes),
            "trust_signal_summary": _canonical_audit_mapping(
                self.trust_signal_summary
            ),
            "retrieval_policy": _canonical_audit_mapping(self.retrieval_policy),
            "failure_types": list(self.failure_types),
            "context_hash": self.context_hash,
            "final_answer_hash": self.final_answer_hash,
            "run_id": self.run_id,
        }
