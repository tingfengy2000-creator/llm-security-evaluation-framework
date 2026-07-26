"""Behavior-layer ports and deterministic test-only implementations for content resolution."""

from .errors import (
    CitationInputError,
    CitationIntegrityError,
    ContentResolutionError,
    ContentResolutionIntegrityError,
    ContentResolutionLookupError,
    ContentResolutionRuntimeError,
    ContextRenderingError,
    EvidenceEnvelopeInputError,
    EvidenceEnvelopeIntegrityError,
    EvidenceEnvelopeRuntimeError,
)
from .citation import render_citation_instruction
from .envelope import CanonicalEvidenceEnvelopeFactory
from .in_memory import (
    InMemoryCorpusSnapshotReader,
    StaticApprovedCorpusSnapshotRegistry,
    StaticLegacyContentRefAdapter,
)
from .protocols import (
    ApprovedCorpusSnapshotRegistry,
    ContentResolver,
    CorpusSnapshotReader,
    LegacyContentRefAdapter,
    EvidenceEnvelopeFactory,
)
from .rendering import escape_xml_attribute, escape_xml_text, render_evidence_block
from .resolver import CorpusContentResolver

__all__ = [
    "ApprovedCorpusSnapshotRegistry",
    "ContentResolutionError",
    "ContentResolutionIntegrityError",
    "ContentResolutionLookupError",
    "ContentResolutionRuntimeError",
    "CitationInputError",
    "CitationIntegrityError",
    "ContextRenderingError",
    "CanonicalEvidenceEnvelopeFactory",
    "EvidenceEnvelopeFactory",
    "EvidenceEnvelopeInputError",
    "EvidenceEnvelopeIntegrityError",
    "EvidenceEnvelopeRuntimeError",
    "ContentResolver",
    "CorpusContentResolver",
    "CorpusSnapshotReader",
    "InMemoryCorpusSnapshotReader",
    "LegacyContentRefAdapter",
    "StaticApprovedCorpusSnapshotRegistry",
    "StaticLegacyContentRefAdapter",
    "escape_xml_attribute",
    "escape_xml_text",
    "render_citation_instruction",
    "render_evidence_block",
]
