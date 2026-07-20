"""Deterministic one-document/one-chunk baseline for S6-T5.1."""

from __future__ import annotations

import hashlib
from collections.abc import Mapping

from ..contracts import (
    ChunkRecord,
    ChunkingConfig,
    ChunkingStrategy,
    DocumentRecord,
    derive_chunk_id,
    format_corpus_content_ref,
)
from .errors import ChunkingConfigurationError, ChunkingIntegrityError, ChunkingInputError


class IdentityChunker:
    """Emit exactly one unchanged chunk after explicit content-integrity checking."""

    def chunk(
        self,
        document: DocumentRecord,
        *,
        corpus_snapshot_id: str,
        config: ChunkingConfig,
        public_metadata: Mapping[str, object] | None = None,
    ) -> tuple[ChunkRecord, ...]:
        if not isinstance(document, DocumentRecord):
            raise ChunkingInputError("document must be a DocumentRecord")
        if config.strategy is not ChunkingStrategy.IDENTITY:
            raise ChunkingConfigurationError(
                "IdentityChunker requires an identity ChunkingConfig"
            )
        actual_content_hash = hashlib.sha256(document.content.encode("utf-8")).hexdigest()
        if actual_content_hash != document.content_hash:
            raise ChunkingIntegrityError(
                f"document content hash mismatch for doc_id={document.doc_id}"
            )
        config_hash = config.fingerprint()
        chunk_id = derive_chunk_id(
            chunk_schema_version=config.schema_version,
            corpus_snapshot_id=corpus_snapshot_id,
            parent_doc_id=document.doc_id,
            chunk_index=0,
            content_hash=actual_content_hash,
            chunking_config_hash=config_hash,
        )
        chunk = ChunkRecord(
            chunk_id=chunk_id,
            parent_doc_id=document.doc_id,
            corpus_snapshot_id=corpus_snapshot_id,
            chunk_index=0,
            content=document.content,
            content_hash=actual_content_hash,
            content_ref=format_corpus_content_ref(corpus_snapshot_id, chunk_id),
            chunking_strategy=config.strategy.value,
            chunking_config_hash=config_hash,
            source_id=document.source_id,
            source_type=document.source_type,
            version=document.version,
            timestamp=document.timestamp,
            public_metadata={} if public_metadata is None else public_metadata,
        )
        return (chunk,)
