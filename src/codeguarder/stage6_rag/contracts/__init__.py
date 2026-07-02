"""Stable public contracts for the Stage 6 RAG pipeline."""

from codeguarder.stage6_rag.contracts.models import (
    DocumentRecord,
    EvidenceSignal,
    QueryRecord,
    RAGAttemptRecord,
    RAGSecurityEnvelope,
    RetrievalEvidence,
    TrustAssessment,
)
from codeguarder.stage6_rag.contracts.schemas import (
    FORBIDDEN_PIPELINE_FIELDS,
    REQUIRED_DOCUMENT_FIELDS,
    SchemaError,
    validate_document,
    validate_document_collection,
)

__all__ = [
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
    "validate_document",
    "validate_document_collection",
]
