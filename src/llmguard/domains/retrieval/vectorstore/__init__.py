"""Provider-neutral vector storage contracts for S6-T4."""

from .base import VectorStore
from .chroma_store import ChromaVectorStore
from .fingerprint import CollectionFingerprint
from .in_memory_store import InMemoryVectorStore
from .models import (
    MetadataIsolationError,
    VectorCollectionInfo,
    VectorCollectionSpec,
    VectorDimensionError,
    VectorDocument,
    VectorSearchHit,
    VectorSearchQuery,
    VectorStoreConfigurationError,
    VectorStoreError,
    VectorStorePersistenceError,
    VectorStoreQueryError,
)

__all__ = [
    "CollectionFingerprint",
    "ChromaVectorStore",
    "InMemoryVectorStore",
    "MetadataIsolationError",
    "VectorCollectionInfo",
    "VectorCollectionSpec",
    "VectorDimensionError",
    "VectorDocument",
    "VectorSearchHit",
    "VectorSearchQuery",
    "VectorStore",
    "VectorStoreConfigurationError",
    "VectorStoreError",
    "VectorStorePersistenceError",
    "VectorStoreQueryError",
]
