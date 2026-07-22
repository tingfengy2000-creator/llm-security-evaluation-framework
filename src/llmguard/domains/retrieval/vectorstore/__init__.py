"""Provider-neutral vector storage contracts for S6-T4."""

from .base import VectorStore
from .chroma_store import ChromaVectorStore
from .fingerprint import CollectionFingerprint
from .in_memory_store import InMemoryVectorStore
from .models import (
    PUBLIC_METADATA_FIELDS,
    PUBLIC_METADATA_SCHEMA_VERSIONS,
    RETRIEVAL_READY_METADATA_FIELDS,
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
    validate_metadata_for_schema,
    validate_public_metadata,
    validate_retrieval_ready_metadata,
)

__all__ = [
    "CollectionFingerprint",
    "ChromaVectorStore",
    "InMemoryVectorStore",
    "MetadataIsolationError",
    "PUBLIC_METADATA_FIELDS",
    "PUBLIC_METADATA_SCHEMA_VERSIONS",
    "RETRIEVAL_READY_METADATA_FIELDS",
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
    "validate_metadata_for_schema",
    "validate_public_metadata",
    "validate_retrieval_ready_metadata",
]
