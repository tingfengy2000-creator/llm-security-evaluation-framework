"""Minimal behavior-layer protocols for controlled corpus content resolution."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol

from llmguard.domains.retrieval.contracts import (
    ContentRef,
    EvidenceEnvelope,
    ResolvedContent,
    RetrievalEvidence,
    RetrievalRequest,
    CitationMode,
    ContextBuildConfig,
    RetrievedContextPackage,
)


class ContextBuilder(Protocol):
    """Build one deterministic sensitive context package from retrieved evidence."""

    def build(
        self,
        *,
        request: RetrievalRequest,
        evidence: Sequence[RetrievalEvidence],
        citation_mode: CitationMode,
        config: ContextBuildConfig,
    ) -> RetrievedContextPackage:
        """Construct one package without retriever, model, or trust dependencies."""


class ContentResolver(Protocol):
    """Resolve only an opaque reference and expected hash into verified content."""

    def resolve(
        self,
        *,
        content_ref: ContentRef,
        expected_content_hash: str,
    ) -> ResolvedContent:
        """Resolve one controlled content capability."""


class EvidenceEnvelopeFactory(Protocol):
    """Create one envelope only from canonical evidence and verified content."""

    def create(
        self,
        *,
        evidence: RetrievalEvidence,
        resolved_content: ResolvedContent,
    ) -> EvidenceEnvelope:
        """Bind public retrieval provenance to one verified sensitive body."""


class CorpusSnapshotReader(Protocol):
    """Read exactly one approved chunk without corpus enumeration."""

    @property
    def corpus_snapshot_id(self) -> str:
        """Return the public snapshot identity."""

    @property
    def snapshot_fingerprint(self) -> str:
        """Return the pinned public snapshot fingerprint."""

    def read_chunk(
        self,
        *,
        chunk_id: str,
    ) -> str:
        """Read the exact body for one known chunk identifier."""


class ApprovedCorpusSnapshotRegistry(Protocol):
    """Return a reader only for explicitly approved snapshot registrations."""

    def get_reader(
        self,
        *,
        corpus_snapshot_id: str,
    ) -> CorpusSnapshotReader:
        """Return one approved reader without exposing registry enumeration."""


class LegacyContentRefAdapter(Protocol):
    """Map an exact legacy reference to a validated canonical corpus reference."""

    @property
    def mapping_version(self) -> str:
        """Return the public immutable mapping version."""

    @property
    def mapping_hash(self) -> str:
        """Return the deterministic hash of the mapping contract."""

    def to_canonical(
        self,
        *,
        legacy_content_ref: ContentRef,
    ) -> ContentRef:
        """Map one exact legacy reference without fallback derivation."""
