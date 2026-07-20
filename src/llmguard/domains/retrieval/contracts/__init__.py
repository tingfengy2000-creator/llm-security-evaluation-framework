"""Stable public contracts for the canonical Retrieval Security domain."""

from .chunking import (
    ChunkRecord,
    ChunkingConfig,
    ChunkingStrategy,
    derive_chunk_id,
    format_corpus_content_ref,
)
from .errors import (
    ChunkingConfigurationError,
    ChunkingContractError,
    ChunkingInputError,
    ChunkingIntegrityError,
)
from .hashing import canonical_json, canonical_json_sha256
from .models import (
    DocumentRecord,
    EvidenceSignal,
    QueryRecord,
    RAGAttemptRecord,
    RAGSecurityEnvelope,
    RetrievalEvidence,
    TrustAssessment,
)
from .schemas import (
    FORBIDDEN_PIPELINE_FIELDS,
    REQUIRED_DOCUMENT_FIELDS,
    SchemaError,
    validate_document,
    validate_document_collection,
)

__all__ = [
    "ChunkRecord",
    "ChunkingConfig",
    "ChunkingConfigurationError",
    "ChunkingContractError",
    "ChunkingInputError",
    "ChunkingIntegrityError",
    "ChunkingStrategy",
    "DocumentRecord",
    "EvidenceSignal",
    "FORBIDDEN_PIPELINE_FIELDS",
    "QueryRecord",
    "RAGAttemptRecord",
    "RAGSecurityEnvelope",
    "REQUIRED_DOCUMENT_FIELDS",
    "RetrievalEvidence",
    "SchemaError",
    "TrustAssessment",
    "canonical_json",
    "canonical_json_sha256",
    "derive_chunk_id",
    "format_corpus_content_ref",
    "validate_document",
    "validate_document_collection",
]
