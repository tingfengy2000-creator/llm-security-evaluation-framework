"""Stable, sensitive content-resolution contract owned by the retrieval domain."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field

from .content_ref import ContentRef
from .errors import ContentResolutionIntegrityError
from .identifiers import require_chunk_id, require_public_identifier, require_sha256


@dataclass(frozen=True, slots=True, kw_only=True)
class ResolvedContent:
    """A short-lived in-process capability for verified corpus content.

    Ordinary audit paths must use :meth:`to_audit_dict`; this DTO intentionally
    has no general serialization or sensitive-artifact export method.
    """

    resolution_schema_version: str
    canonical_content_ref: ContentRef
    corpus_snapshot_id: str
    chunk_id: str
    content_hash: str
    content: str = field(repr=False)

    def __post_init__(self) -> None:
        require_public_identifier(
            self.resolution_schema_version,
            "resolution_schema_version",
        )
        if not isinstance(self.canonical_content_ref, ContentRef):
            raise ContentResolutionIntegrityError(
                "content resolution contract is invalid",
                error_code="CORPUS_SNAPSHOT_INTEGRITY_FAILURE",
            )
        if self.canonical_content_ref.scheme != "corpus":
            raise ContentResolutionIntegrityError(
                "content resolution contract is invalid",
                error_code="CORPUS_SNAPSHOT_INTEGRITY_FAILURE",
            )
        require_public_identifier(self.corpus_snapshot_id, "corpus_snapshot_id")
        require_chunk_id(self.chunk_id)
        require_sha256(self.content_hash, "content_hash")
        if not isinstance(self.content, str):
            raise ContentResolutionIntegrityError(
                "content resolution contract is invalid",
                error_code="CONTENT_RESOLUTION_FAILURE",
            )
        if (
            self.canonical_content_ref.corpus_snapshot_id != self.corpus_snapshot_id
            or self.canonical_content_ref.chunk_id != self.chunk_id
        ):
            raise ContentResolutionIntegrityError(
                "content resolution contract is invalid",
                error_code="CORPUS_SNAPSHOT_INTEGRITY_FAILURE",
            )
        if hashlib.sha256(self.content.encode("utf-8")).hexdigest() != self.content_hash:
            raise ContentResolutionIntegrityError(
                "content hash does not match",
                error_code="CONTENT_HASH_MISMATCH",
            )

    @property
    def content_length(self) -> int:
        """Return the exact Python Unicode code-point length of the body."""

        return len(self.content)

    def to_audit_dict(self) -> dict[str, str | int]:
        """Return the only ordinary audit representation of this sensitive DTO."""

        return {
            "resolution_schema_version": self.resolution_schema_version,
            "corpus_snapshot_id": self.corpus_snapshot_id,
            "chunk_id": self.chunk_id,
            "content_hash": self.content_hash,
            "content_length": self.content_length,
        }
