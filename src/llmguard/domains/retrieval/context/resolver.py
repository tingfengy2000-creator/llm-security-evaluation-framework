"""Controlled corpus resolution without file access, caching, or provider dependencies."""

from __future__ import annotations

import hashlib

from llmguard.domains.retrieval.contracts import (
    ContentRef,
    ContentResolutionError,
    ContentResolutionIntegrityError,
    ContentResolutionLookupError,
    ContentResolutionRuntimeError,
    ResolvedContent,
    RetrievalInputError,
)
from llmguard.domains.retrieval.contracts.identifiers import require_sha256

from .protocols import (
    ApprovedCorpusSnapshotRegistry,
    ContentResolver,
    LegacyContentRefAdapter,
)


class CorpusContentResolver(ContentResolver):
    """Resolve one verified corpus chunk through injected minimum-permission ports."""

    _RESOLUTION_SCHEMA_VERSION = "1.0"

    def __init__(
        self,
        *,
        registry: ApprovedCorpusSnapshotRegistry,
        legacy_adapter: LegacyContentRefAdapter | None = None,
    ) -> None:
        self._registry = registry
        self._legacy_adapter = legacy_adapter

    @property
    def registry(self) -> ApprovedCorpusSnapshotRegistry:
        """Expose the injected registry only for composition and isolated tests."""

        return self._registry

    def resolve(
        self,
        *,
        content_ref: ContentRef,
        expected_content_hash: str,
    ) -> ResolvedContent:
        if not isinstance(content_ref, ContentRef):
            raise RetrievalInputError("content resolver requires a content reference")
        expected_hash = require_sha256(expected_content_hash, "expected_content_hash")
        canonical_ref = self._canonicalize(content_ref)
        snapshot_id = canonical_ref.corpus_snapshot_id
        chunk_id = canonical_ref.chunk_id
        if snapshot_id is None or chunk_id is None:
            raise ContentResolutionIntegrityError(
                "content resolution contract is invalid",
                error_code="CORPUS_SNAPSHOT_INTEGRITY_FAILURE",
            )
        reader = self._get_reader(snapshot_id)
        self._validate_reader_identity(reader, snapshot_id)
        content = self._read_chunk(reader, chunk_id)
        if hashlib.sha256(content.encode("utf-8")).hexdigest() != expected_hash:
            raise ContentResolutionIntegrityError(
                "content hash does not match",
                error_code="CONTENT_HASH_MISMATCH",
            )
        try:
            return ResolvedContent(
                resolution_schema_version=self._RESOLUTION_SCHEMA_VERSION,
                canonical_content_ref=canonical_ref,
                corpus_snapshot_id=snapshot_id,
                chunk_id=chunk_id,
                content_hash=expected_hash,
                content=content,
            )
        except ContentResolutionError:
            raise
        except Exception as error:
            raise ContentResolutionRuntimeError(
                "content resolution failed",
                error_code="CONTENT_RESOLUTION_FAILURE",
            ) from error

    def _canonicalize(self, content_ref: ContentRef) -> ContentRef:
        if content_ref.scheme == "corpus":
            return content_ref
        if content_ref.scheme != "chroma" or self._legacy_adapter is None:
            raise ContentResolutionLookupError(
                "approved content reference is unavailable",
                error_code="UNKNOWN_CONTENT_REF",
            )
        try:
            canonical_ref = self._legacy_adapter.to_canonical(
                legacy_content_ref=content_ref,
            )
        except ContentResolutionError:
            raise
        except Exception as error:
            raise ContentResolutionRuntimeError(
                "content resolution failed",
                error_code="CONTENT_RESOLUTION_FAILURE",
            ) from error
        if not isinstance(canonical_ref, ContentRef):
            raise ContentResolutionIntegrityError(
                "legacy content mapping is invalid",
                error_code="CORPUS_SNAPSHOT_INTEGRITY_FAILURE",
            )
        try:
            revalidated_ref = ContentRef(str(canonical_ref))
        except Exception as error:
            raise ContentResolutionIntegrityError(
                "legacy content mapping is invalid",
                error_code="CORPUS_SNAPSHOT_INTEGRITY_FAILURE",
            ) from error
        if revalidated_ref.scheme != "corpus":
            raise ContentResolutionIntegrityError(
                "legacy content mapping is invalid",
                error_code="CORPUS_SNAPSHOT_INTEGRITY_FAILURE",
            )
        return revalidated_ref

    def _get_reader(self, snapshot_id: str) -> object:
        try:
            return self._registry.get_reader(corpus_snapshot_id=snapshot_id)
        except ContentResolutionError:
            raise
        except Exception as error:
            raise ContentResolutionRuntimeError(
                "content resolution failed",
                error_code="CONTENT_RESOLUTION_FAILURE",
            ) from error

    @staticmethod
    def _validate_reader_identity(reader: object, snapshot_id: str) -> None:
        try:
            reader_snapshot_id = reader.corpus_snapshot_id  # type: ignore[attr-defined]
            reader_fingerprint = reader.snapshot_fingerprint  # type: ignore[attr-defined]
            require_sha256(reader_fingerprint, "snapshot_fingerprint")
        except ContentResolutionError:
            raise
        except Exception as error:
            raise ContentResolutionIntegrityError(
                "approved corpus snapshot integrity check failed",
                error_code="CORPUS_SNAPSHOT_INTEGRITY_FAILURE",
            ) from error
        if reader_snapshot_id != snapshot_id:
            raise ContentResolutionIntegrityError(
                "approved corpus snapshot integrity check failed",
                error_code="CORPUS_SNAPSHOT_INTEGRITY_FAILURE",
            )

    @staticmethod
    def _read_chunk(reader: object, chunk_id: str) -> str:
        try:
            content = reader.read_chunk(chunk_id=chunk_id)  # type: ignore[attr-defined]
        except ContentResolutionError:
            raise
        except Exception as error:
            raise ContentResolutionRuntimeError(
                "content resolution failed",
                error_code="CONTENT_RESOLUTION_FAILURE",
            ) from error
        if not isinstance(content, str):
            raise ContentResolutionRuntimeError(
                "content resolution failed",
                error_code="CONTENT_RESOLUTION_FAILURE",
            )
        return content
