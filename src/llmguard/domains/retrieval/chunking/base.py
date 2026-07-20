"""Behavior boundary for deterministic chunking implementations."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol

from ..contracts import ChunkRecord, ChunkingConfig, DocumentRecord


class Chunker(Protocol):
    """Transform one verified document into deterministic chunk contracts."""

    def chunk(
        self,
        document: DocumentRecord,
        *,
        corpus_snapshot_id: str,
        config: ChunkingConfig,
        public_metadata: Mapping[str, object] | None = None,
    ) -> tuple[ChunkRecord, ...]:
        """Return ordered chunks without accessing retrieval or evaluation state."""
