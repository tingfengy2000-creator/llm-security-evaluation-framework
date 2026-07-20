"""Deterministic, path-safe identifiers for retrieval runtime contracts."""

from __future__ import annotations

import re

from .errors import RetrievalInputError
from .hashing import canonical_json_sha256

_SHA256 = re.compile(r"\A[0-9a-f]{64}\Z")
_CHUNK_ID = re.compile(r"\ACH-[0-9a-f]{64}\Z")
_PUBLIC_QUERY_ID = re.compile(r"\AQ-[0-9]{4,}\Z")
_SAFE_ID = re.compile(r"\A[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z")
_ABSOLUTE_PATH = re.compile(r"(?:\A[A-Za-z]:[\\/]|\A[\\/]{2}|\A/|\Afile:)", re.IGNORECASE)


def require_sha256(value: object, field_name: str) -> str:
    if not isinstance(value, str) or _SHA256.fullmatch(value) is None:
        raise RetrievalInputError(f"{field_name} must be a lowercase SHA-256 digest")
    return value


def require_public_identifier(value: object, field_name: str, *, pattern: re.Pattern[str] | None = None) -> str:
    if not isinstance(value, str) or not value or len(value) > 128 or "\n" in value or "\r" in value:
        raise RetrievalInputError(f"{field_name} must be a bounded public identifier")
    if _ABSOLUTE_PATH.search(value) is not None or (pattern or _SAFE_ID).fullmatch(value) is None:
        raise RetrievalInputError(f"{field_name} must be a safe non-path identifier")
    return value


def require_public_query_id(value: object) -> str:
    return require_public_identifier(value, "query_id", pattern=_PUBLIC_QUERY_ID)


def require_chunk_id(value: object) -> str:
    return require_public_identifier(value, "chunk_id", pattern=_CHUNK_ID)


def derive_evidence_uid(*, evidence_schema_version: str, corpus_snapshot_id: str, chunk_id: str, content_hash: str) -> str:
    require_public_identifier(evidence_schema_version, "evidence_schema_version")
    require_public_identifier(corpus_snapshot_id, "corpus_snapshot_id")
    require_chunk_id(chunk_id)
    require_sha256(content_hash, "content_hash")
    return "EV-" + canonical_json_sha256({
        "chunk_id": chunk_id,
        "content_hash": content_hash,
        "corpus_snapshot_id": corpus_snapshot_id,
        "evidence_schema_version": evidence_schema_version,
    })


def derive_request_id(payload: dict[str, object]) -> str:
    return "RQ-" + canonical_json_sha256(payload)


def derive_trace_hash(payload: dict[str, object]) -> str:
    return canonical_json_sha256(payload)


def derive_trace_id(trace_hash: str) -> str:
    return "RT-" + require_sha256(trace_hash, "trace_hash")
