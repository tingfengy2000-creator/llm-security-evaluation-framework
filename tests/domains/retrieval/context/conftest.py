from __future__ import annotations

import hashlib

from llmguard.domains.retrieval.contracts import (
    ContentRef,
    ResolvedContent,
    RetrievalEvidence,
    derive_evidence_uid,
)


def body_hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def chunk_id(letter: str = "a") -> str:
    return "CH-" + letter * 64


def make_evidence(
    *,
    content: str = "Synthetic policy body.",
    snapshot: str = "synthetic-v1",
    chunk: str | None = None,
    rank: int = 1,
    source_id: str = "source-1",
    version: str = "v1",
) -> RetrievalEvidence:
    selected_chunk = chunk or chunk_id()
    digest = body_hash(content)
    return RetrievalEvidence(
        evidence_schema_version="1.0",
        evidence_uid=derive_evidence_uid(
            evidence_schema_version="1.0",
            corpus_snapshot_id=snapshot,
            chunk_id=selected_chunk,
            content_hash=digest,
        ),
        query_id="Q-0001",
        retrieval_request_id="RQ-synthetic",
        corpus_snapshot_id=snapshot,
        doc_id=selected_chunk,
        chunk_id=selected_chunk,
        parent_doc_id="parent-1",
        content_ref=ContentRef.corpus(snapshot, selected_chunk),
        content_hash=digest,
        source_id=source_id,
        source_type="policy",
        version=version,
        timestamp="2026-07-26T00:00:00Z",
        rank=rank,
        distance=0.25,
        similarity=0.75,
        collection_fingerprint="b" * 64,
        public_metadata={"language": "zh"},
    )


def make_resolved(
    *,
    content: str = "Synthetic policy body.",
    snapshot: str = "synthetic-v1",
    chunk: str | None = None,
) -> ResolvedContent:
    selected_chunk = chunk or chunk_id()
    return ResolvedContent(
        resolution_schema_version="1.0",
        canonical_content_ref=ContentRef.corpus(snapshot, selected_chunk),
        corpus_snapshot_id=snapshot,
        chunk_id=selected_chunk,
        content_hash=body_hash(content),
        content=content,
    )
