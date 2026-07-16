"""Database-neutral VectorStore protocol."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from .models import (
    VectorCollectionInfo,
    VectorCollectionSpec,
    VectorDocument,
    VectorSearchHit,
    VectorSearchQuery,
)


@runtime_checkable
class VectorStore(Protocol):
    """Stable storage interface. Future Retrievers must depend on this, not Chroma."""

    def create_or_open_collection(
        self,
        collection: VectorCollectionSpec,
    ) -> VectorCollectionInfo:
        """Create compatible storage or open an exact fingerprint match."""

    def upsert(
        self,
        collection: VectorCollectionSpec,
        documents: Sequence[VectorDocument],
    ) -> None:
        """Insert or replace documents by ``doc_id``."""

    def query(
        self,
        collection: VectorCollectionSpec,
        query: VectorSearchQuery,
    ) -> tuple[VectorSearchHit, ...]:
        """Return stable ranked hits without database-specific payloads."""

    def count(self, collection: VectorCollectionSpec) -> int:
        """Return the number of rows in a collection."""

    def get_collection_info(
        self,
        collection: VectorCollectionSpec,
    ) -> VectorCollectionInfo:
        """Return stable collection metadata."""

    def close(self) -> None:
        """Close resources. A closed instance cannot be reopened."""
