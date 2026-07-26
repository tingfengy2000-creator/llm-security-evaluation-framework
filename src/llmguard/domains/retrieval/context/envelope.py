"""Behavior-layer canonical construction for one sensitive evidence envelope."""

from __future__ import annotations

from llmguard.domains.retrieval.contracts import (
    ContentRef,
    EvidenceEnvelope,
    EvidenceEnvelopeInputError,
    EvidenceEnvelopeIntegrityError,
    EvidenceEnvelopeRuntimeError,
    ResolvedContent,
    RetrievalEvidence,
)


class CanonicalEvidenceEnvelopeFactory:
    """Bind only canonical evidence provenance to one verified resolved body."""

    def create(
        self,
        *,
        evidence: RetrievalEvidence,
        resolved_content: ResolvedContent,
    ) -> EvidenceEnvelope:
        if not isinstance(evidence, RetrievalEvidence) or not isinstance(
            resolved_content,
            ResolvedContent,
        ):
            raise EvidenceEnvelopeInputError("evidence envelope is invalid")
        try:
            content_ref = evidence.content_ref
            if not isinstance(content_ref, ContentRef) or content_ref.scheme != "corpus":
                raise EvidenceEnvelopeIntegrityError("evidence does not match resolved content")
            if (
                content_ref != resolved_content.canonical_content_ref
                or evidence.corpus_snapshot_id != resolved_content.corpus_snapshot_id
                or evidence.chunk_id != resolved_content.chunk_id
                or evidence.content_hash != resolved_content.content_hash
            ):
                raise EvidenceEnvelopeIntegrityError("evidence does not match resolved content")
            return EvidenceEnvelope(
                evidence_uid=evidence.evidence_uid,
                doc_id=evidence.doc_id,
                chunk_id=evidence.chunk_id,
                parent_doc_id=evidence.parent_doc_id,
                source_id=evidence.source_id,
                source_type=evidence.source_type,
                version=evidence.version,
                timestamp=evidence.timestamp,
                content_hash=evidence.content_hash,
                rank=evidence.rank,
                distance=evidence.distance,
                similarity=evidence.similarity,
                content=resolved_content.content,
                public_metadata=evidence.public_metadata,
            )
        except (EvidenceEnvelopeInputError, EvidenceEnvelopeIntegrityError):
            raise
        except Exception as error:
            raise EvidenceEnvelopeRuntimeError(
                "evidence envelope construction failed"
            ) from error
