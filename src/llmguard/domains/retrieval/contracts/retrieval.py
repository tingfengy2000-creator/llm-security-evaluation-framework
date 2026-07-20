"""Stable runtime DTOs for retrieval requests, evidence summaries, and traces."""

from __future__ import annotations

import hashlib
import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field

from .errors import RetrievalInputError, RetrievalIntegrityError
from .identifiers import (
    derive_request_id,
    derive_evidence_uid,
    derive_trace_hash,
    derive_trace_id,
    require_public_identifier,
    require_public_query_id,
    require_sha256,
)
from .public_metadata import freeze_public_metadata, thaw_public_metadata
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import RetrievalEvidence

_QUERY_METADATA_ALLOWLIST = frozenset({"delivery_layer", "scenario", "variant"})


def _require_nonblank(value: object, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise RetrievalInputError(f"{field_name} must be a nonblank string")
    return value


def _require_positive_int(value: object, field_name: str) -> int:
    if type(value) is not int or value <= 0:
        raise RetrievalInputError(f"{field_name} must be a positive integer")
    return value


def _require_metric(value: object, field_name: str, *, minimum: float, maximum: float | None = None) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise RetrievalInputError("invalid retrieval metric", error_code="INVALID_RETRIEVAL_METRIC")
    number = float(value)
    if number < minimum or (maximum is not None and number > maximum):
        raise RetrievalInputError("invalid retrieval metric", error_code="INVALID_RETRIEVAL_METRIC")
    return number


@dataclass(frozen=True, slots=True, kw_only=True)
class RetrieverQueryRecord:
    """Minimal retriever-visible projection; evaluator fields are absent by type."""

    query_id: str
    retrieval_query: str = field(repr=False)
    public_metadata: Mapping[str, object]

    def __post_init__(self) -> None:
        object.__setattr__(self, "query_id", require_public_query_id(self.query_id))
        _require_nonblank(self.retrieval_query, "retrieval_query")
        object.__setattr__(
            self,
            "public_metadata",
            freeze_public_metadata(self.public_metadata, allowed_keys=_QUERY_METADATA_ALLOWLIST),
        )

    def to_audit_dict(self) -> dict[str, object]:
        return {"query_id": self.query_id, "public_metadata": thaw_public_metadata(self.public_metadata)}


@dataclass(frozen=True, slots=True, kw_only=True)
class RetrievalRequest:
    """Deterministic future retriever input that keeps query text out of audit forms."""

    request_schema_version: str
    request_id: str
    query_id: str
    retrieval_query: str = field(repr=False)
    retrieval_query_hash: str
    top_k: int
    collection_fingerprint: str
    query_embedding_spec_hash: str
    retrieval_config_hash: str

    def __post_init__(self) -> None:
        require_public_identifier(self.request_schema_version, "request_schema_version")
        require_public_identifier(self.request_id, "request_id")
        require_public_query_id(self.query_id)
        _require_nonblank(self.retrieval_query, "retrieval_query")
        expected_query_hash = hashlib.sha256(self.retrieval_query.encode("utf-8")).hexdigest()
        if self.retrieval_query_hash != expected_query_hash:
            raise RetrievalIntegrityError("retrieval query hash mismatch", error_code="RETRIEVAL_QUERY_HASH_MISMATCH")
        _require_positive_int(self.top_k, "top_k")
        for field_name in ("collection_fingerprint", "query_embedding_spec_hash", "retrieval_config_hash"):
            require_sha256(getattr(self, field_name), field_name)
        expected_request_id = derive_request_id(self._identity_payload())
        if self.request_id != expected_request_id:
            raise RetrievalIntegrityError("retrieval request identity mismatch", error_code="RETRIEVAL_REQUEST_ID_MISMATCH")

    @classmethod
    def from_query(
        cls,
        query: RetrieverQueryRecord,
        *,
        request_schema_version: str,
        top_k: int,
        collection_fingerprint: str,
        query_embedding_spec_hash: str,
        retrieval_config_hash: str,
    ) -> "RetrievalRequest":
        if not isinstance(query, RetrieverQueryRecord):
            raise RetrievalInputError("retrieval request requires a projected runtime query")
        query_hash = hashlib.sha256(query.retrieval_query.encode("utf-8")).hexdigest()
        payload = {
            "collection_fingerprint": collection_fingerprint,
            "query_embedding_spec_hash": query_embedding_spec_hash,
            "query_id": query.query_id,
            "retrieval_config_hash": retrieval_config_hash,
            "retrieval_query_hash": query_hash,
            "request_schema_version": request_schema_version,
            "top_k": top_k,
        }
        return cls(
            request_schema_version=request_schema_version,
            request_id=derive_request_id(payload),
            query_id=query.query_id,
            retrieval_query=query.retrieval_query,
            retrieval_query_hash=query_hash,
            top_k=top_k,
            collection_fingerprint=collection_fingerprint,
            query_embedding_spec_hash=query_embedding_spec_hash,
            retrieval_config_hash=retrieval_config_hash,
        )

    def _identity_payload(self) -> dict[str, object]:
        return {
            "collection_fingerprint": self.collection_fingerprint,
            "query_embedding_spec_hash": self.query_embedding_spec_hash,
            "query_id": self.query_id,
            "retrieval_config_hash": self.retrieval_config_hash,
            "retrieval_query_hash": self.retrieval_query_hash,
            "request_schema_version": self.request_schema_version,
            "top_k": self.top_k,
        }

    def to_audit_dict(self) -> dict[str, object]:
        return {
            "request_schema_version": self.request_schema_version,
            "request_id": self.request_id,
            "query_id": self.query_id,
            "retrieval_query_hash": self.retrieval_query_hash,
            "top_k": self.top_k,
            "collection_fingerprint": self.collection_fingerprint,
            "query_embedding_spec_hash": self.query_embedding_spec_hash,
            "retrieval_config_hash": self.retrieval_config_hash,
        }


@dataclass(frozen=True, slots=True, kw_only=True)
class RetrievalEvidenceSummary:
    evidence_uid: str
    doc_id: str
    chunk_id: str
    parent_doc_id: str
    rank: int
    distance: float
    similarity: float
    content_hash: str
    source_id: str
    version: str

    def __post_init__(self) -> None:
        require_public_identifier(self.evidence_uid, "evidence_uid")
        for field_name in ("doc_id", "chunk_id", "parent_doc_id", "source_id", "version"):
            require_public_identifier(getattr(self, field_name), field_name)
        _require_positive_int(self.rank, "rank")
        object.__setattr__(self, "distance", _require_metric(self.distance, "distance", minimum=0))
        object.__setattr__(self, "similarity", _require_metric(self.similarity, "similarity", minimum=-1, maximum=1))
        require_sha256(self.content_hash, "content_hash")

    @classmethod
    def from_evidence(cls, evidence: object) -> "RetrievalEvidenceSummary":
        required = ("evidence_uid", "doc_id", "chunk_id", "parent_doc_id", "rank", "distance", "similarity", "content_hash", "source_id", "version")
        if not all(hasattr(evidence, name) for name in required):
            raise RetrievalInputError("evidence summary requires a retrieval evidence record")
        return cls(**{name: getattr(evidence, name) for name in required})

    def to_audit_dict(self) -> dict[str, object]:
        return {
            "evidence_uid": self.evidence_uid, "doc_id": self.doc_id, "chunk_id": self.chunk_id,
            "parent_doc_id": self.parent_doc_id, "rank": self.rank, "distance": self.distance,
            "similarity": self.similarity, "content_hash": self.content_hash,
            "source_id": self.source_id, "version": self.version,
        }


@dataclass(frozen=True, slots=True, kw_only=True)
class RetrievalTrace:
    trace_schema_version: str
    trace_id: str
    trace_hash: str
    request_id: str
    query_id: str
    retrieval_query_hash: str
    query_embedding_spec_hash: str
    collection_fingerprint: str
    top_k: int
    candidate_count: int
    returned_count: int
    evidence_summaries: tuple[RetrievalEvidenceSummary, ...]
    retrieval_latency_ms: float

    def __post_init__(self) -> None:
        require_public_identifier(self.trace_schema_version, "trace_schema_version")
        require_public_identifier(self.trace_id, "trace_id")
        require_public_identifier(self.request_id, "request_id")
        require_public_query_id(self.query_id)
        for field_name in ("trace_hash", "retrieval_query_hash", "query_embedding_spec_hash", "collection_fingerprint"):
            require_sha256(getattr(self, field_name), field_name)
        _require_positive_int(self.top_k, "top_k")
        if type(self.candidate_count) is not int or self.candidate_count < 0:
            raise RetrievalInputError("candidate_count must be a nonnegative integer")
        summaries = tuple(self.evidence_summaries)
        if not all(isinstance(item, RetrievalEvidenceSummary) for item in summaries):
            raise RetrievalInputError("evidence_summaries must contain summaries")
        if self.returned_count != len(summaries) or self.candidate_count < self.returned_count:
            raise RetrievalIntegrityError("retrieval trace count mismatch", error_code="TRACE_COUNT_MISMATCH")
        ranks = tuple(item.rank for item in summaries)
        if ranks != tuple(range(1, len(summaries) + 1)):
            raise RetrievalIntegrityError("retrieval trace ranks are not stable", error_code="TRACE_COUNT_MISMATCH")
        object.__setattr__(self, "evidence_summaries", summaries)
        object.__setattr__(self, "retrieval_latency_ms", _require_metric(self.retrieval_latency_ms, "retrieval_latency_ms", minimum=0))
        expected_hash = derive_trace_hash(self._semantic_payload())
        if self.trace_hash != expected_hash:
            raise RetrievalIntegrityError("retrieval trace hash mismatch", error_code="TRACE_HASH_MISMATCH")
        if self.trace_id != derive_trace_id(self.trace_hash):
            raise RetrievalIntegrityError("retrieval trace identity mismatch", error_code="TRACE_HASH_MISMATCH")

    @classmethod
    def create(
        cls, *, trace_schema_version: str, request_id: str, query_id: str,
        retrieval_query_hash: str, query_embedding_spec_hash: str,
        collection_fingerprint: str, top_k: int, candidate_count: int,
        evidence_summaries: Sequence[RetrievalEvidenceSummary], retrieval_latency_ms: float,
    ) -> "RetrievalTrace":
        summaries = tuple(evidence_summaries)
        payload = cls._semantic_payload_from(
            trace_schema_version=trace_schema_version, request_id=request_id, query_id=query_id,
            retrieval_query_hash=retrieval_query_hash, query_embedding_spec_hash=query_embedding_spec_hash,
            collection_fingerprint=collection_fingerprint, top_k=top_k, candidate_count=candidate_count,
            returned_count=len(summaries), evidence_summaries=summaries,
        )
        trace_hash = derive_trace_hash(payload)
        return cls(
            trace_schema_version=trace_schema_version, trace_id=derive_trace_id(trace_hash), trace_hash=trace_hash,
            request_id=request_id, query_id=query_id, retrieval_query_hash=retrieval_query_hash,
            query_embedding_spec_hash=query_embedding_spec_hash, collection_fingerprint=collection_fingerprint,
            top_k=top_k, candidate_count=candidate_count, returned_count=len(summaries),
            evidence_summaries=summaries, retrieval_latency_ms=retrieval_latency_ms,
        )

    @staticmethod
    def _semantic_payload_from(**values: object) -> dict[str, object]:
        summaries = values["evidence_summaries"]
        assert isinstance(summaries, tuple)
        return {
            **{key: values[key] for key in (
                "trace_schema_version", "request_id", "query_id", "retrieval_query_hash",
                "query_embedding_spec_hash", "collection_fingerprint", "top_k", "candidate_count", "returned_count",
            )},
            "evidence_summaries": [item.to_audit_dict() for item in summaries],
        }

    def _semantic_payload(self) -> dict[str, object]:
        return self._semantic_payload_from(
            trace_schema_version=self.trace_schema_version, request_id=self.request_id, query_id=self.query_id,
            retrieval_query_hash=self.retrieval_query_hash, query_embedding_spec_hash=self.query_embedding_spec_hash,
            collection_fingerprint=self.collection_fingerprint, top_k=self.top_k, candidate_count=self.candidate_count,
            returned_count=self.returned_count, evidence_summaries=self.evidence_summaries,
        )

    def to_audit_dict(self) -> dict[str, object]:
        return {
            "trace_schema_version": self.trace_schema_version, "trace_id": self.trace_id,
            "trace_hash": self.trace_hash, "request_id": self.request_id, "query_id": self.query_id,
            "retrieval_query_hash": self.retrieval_query_hash,
            "query_embedding_spec_hash": self.query_embedding_spec_hash,
            "collection_fingerprint": self.collection_fingerprint, "top_k": self.top_k,
            "candidate_count": self.candidate_count, "returned_count": self.returned_count,
            "evidence_summaries": [item.to_audit_dict() for item in self.evidence_summaries],
            "retrieval_latency_ms": self.retrieval_latency_ms,
        }


def adapt_legacy_retrieval_evidence(*, query_id: str, legacy_doc_id: str, rank: int, distance: float,
    similarity: float, source_id: str, source_type: str, timestamp: str, version: str,
    content_hash: str, legacy_content_ref: str, evidence_schema_version: str,
    corpus_snapshot_id: str, chunk_id: str, parent_doc_id: str, retrieval_request_id: str,
    collection_fingerprint: str, public_metadata: Mapping[str, object]) -> "RetrievalEvidence":
    """Explicit migration adapter; legacy Chroma ref is validated but never authoritative."""
    from .content_ref import ContentRef
    from .models import RetrievalEvidence

    ContentRef(legacy_content_ref)
    require_public_identifier(legacy_doc_id, "legacy_doc_id")
    uid = derive_evidence_uid(
        evidence_schema_version=evidence_schema_version, corpus_snapshot_id=corpus_snapshot_id,
        chunk_id=chunk_id, content_hash=content_hash,
    )
    return RetrievalEvidence(
        evidence_schema_version=evidence_schema_version, evidence_uid=uid, query_id=query_id,
        retrieval_request_id=retrieval_request_id, corpus_snapshot_id=corpus_snapshot_id,
        doc_id=chunk_id, chunk_id=chunk_id, parent_doc_id=parent_doc_id,
        content_ref=ContentRef.corpus(corpus_snapshot_id, chunk_id), content_hash=content_hash,
        source_id=source_id, source_type=source_type, version=version, timestamp=timestamp,
        rank=rank, distance=distance, similarity=similarity,
        collection_fingerprint=collection_fingerprint, public_metadata=public_metadata,
    )
