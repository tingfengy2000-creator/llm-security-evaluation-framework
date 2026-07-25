"""Deterministic in-memory reference implementations for isolated resolver tests."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType

from llmguard.domains.retrieval.contracts import (
    ContentRef,
    ContentResolutionIntegrityError,
    ContentResolutionLookupError,
    RetrievalInputError,
    canonical_json_sha256,
)
from llmguard.domains.retrieval.contracts.identifiers import (
    require_chunk_id,
    require_public_identifier,
    require_sha256,
)

from .protocols import CorpusSnapshotReader


@dataclass(frozen=True, slots=True, kw_only=True, init=False)
class InMemoryCorpusSnapshotReader:
    """A fixed synthetic chunk mapping that neither scans nor reads files."""

    corpus_snapshot_id: str
    snapshot_fingerprint: str
    _chunks: Mapping[str, str] = field(repr=False)

    def __init__(
        self,
        *,
        corpus_snapshot_id: str,
        snapshot_fingerprint: str,
        chunks: Mapping[str, str],
    ) -> None:
        snapshot_id = require_public_identifier(
            corpus_snapshot_id,
            "corpus_snapshot_id",
        )
        fingerprint = require_sha256(snapshot_fingerprint, "snapshot_fingerprint")
        if not isinstance(chunks, Mapping):
            raise RetrievalInputError("synthetic chunk mapping is invalid")
        frozen_chunks: dict[str, str] = {}
        for chunk_id, content in chunks.items():
            frozen_chunks[require_chunk_id(chunk_id)] = self._require_content(content)
        object.__setattr__(self, "corpus_snapshot_id", snapshot_id)
        object.__setattr__(self, "snapshot_fingerprint", fingerprint)
        object.__setattr__(self, "_chunks", MappingProxyType(frozen_chunks))

    @staticmethod
    def _require_content(content: object) -> str:
        if not isinstance(content, str):
            raise RetrievalInputError("synthetic chunk content is invalid")
        return content

    def read_chunk(self, *, chunk_id: str) -> str:
        chunk = require_chunk_id(chunk_id)
        try:
            return self._chunks[chunk]
        except KeyError as error:
            raise ContentResolutionLookupError(
                "approved corpus chunk is unavailable",
                error_code="UNKNOWN_CORPUS_CHUNK",
            ) from error


@dataclass(frozen=True, slots=True, kw_only=True, init=False)
class StaticApprovedCorpusSnapshotRegistry:
    """An exact, immutable allowlist of approved in-memory snapshot readers."""

    _registrations: Mapping[str, tuple[str, CorpusSnapshotReader]] = field(repr=False)

    def __init__(
        self,
        *,
        registrations: Mapping[str, tuple[str, CorpusSnapshotReader]],
    ) -> None:
        if not isinstance(registrations, Mapping):
            raise RetrievalInputError("approved snapshot registrations are invalid")
        frozen: dict[str, tuple[str, CorpusSnapshotReader]] = {}
        for snapshot_id, registration in registrations.items():
            approved_id = require_public_identifier(snapshot_id, "corpus_snapshot_id")
            if not isinstance(registration, tuple) or len(registration) != 2:
                raise RetrievalInputError("approved snapshot registration is invalid")
            pinned_fingerprint, reader = registration
            frozen[approved_id] = (
                require_sha256(pinned_fingerprint, "snapshot_fingerprint"),
                reader,
            )
        object.__setattr__(self, "_registrations", MappingProxyType(frozen))

    def get_reader(self, *, corpus_snapshot_id: str) -> CorpusSnapshotReader:
        snapshot_id = require_public_identifier(corpus_snapshot_id, "corpus_snapshot_id")
        try:
            pinned_fingerprint, reader = self._registrations[snapshot_id]
        except KeyError as error:
            raise ContentResolutionLookupError(
                "approved corpus snapshot is unavailable",
                error_code="UNKNOWN_CORPUS_SNAPSHOT",
            ) from error
        try:
            reader_snapshot_id = reader.corpus_snapshot_id
            reader_fingerprint = reader.snapshot_fingerprint
        except Exception as error:
            raise ContentResolutionIntegrityError(
                "approved corpus snapshot integrity check failed",
                error_code="CORPUS_SNAPSHOT_INTEGRITY_FAILURE",
            ) from error
        if reader_snapshot_id != snapshot_id or reader_fingerprint != pinned_fingerprint:
            raise ContentResolutionIntegrityError(
                "approved corpus snapshot integrity check failed",
                error_code="CORPUS_SNAPSHOT_INTEGRITY_FAILURE",
            )
        return reader


@dataclass(frozen=True, slots=True, kw_only=True, init=False)
class StaticLegacyContentRefAdapter:
    """An immutable full-reference mapping with no inferred fallback behavior."""

    mapping_version: str
    _mappings: Mapping[ContentRef, ContentRef] = field(repr=False)
    mapping_hash: str

    def __init__(
        self,
        *,
        mapping_version: str,
        mappings: Mapping[ContentRef, ContentRef],
    ) -> None:
        version = require_public_identifier(mapping_version, "mapping_version")
        if not isinstance(mappings, Mapping):
            raise RetrievalInputError("legacy content mapping is invalid")
        frozen: dict[ContentRef, ContentRef] = {}
        entries: list[dict[str, str]] = []
        for legacy, canonical in mappings.items():
            if not isinstance(legacy, ContentRef) or legacy.scheme != "chroma":
                raise RetrievalInputError("legacy content mapping is invalid")
            if not isinstance(canonical, ContentRef) or canonical.scheme != "corpus":
                raise ContentResolutionIntegrityError(
                    "legacy content mapping is invalid",
                    error_code="CORPUS_SNAPSHOT_INTEGRITY_FAILURE",
                )
            frozen[legacy] = canonical
            entries.append(
                {
                    "canonical_content_ref": str(canonical),
                    "legacy_content_ref": str(legacy),
                }
            )
        entries.sort(key=lambda item: item["legacy_content_ref"])
        object.__setattr__(self, "mapping_version", version)
        object.__setattr__(self, "_mappings", MappingProxyType(frozen))
        object.__setattr__(
            self,
            "mapping_hash",
            canonical_json_sha256(
                {
                    "mapping_version": version,
                    "mappings": entries,
                }
            ),
        )

    def to_canonical(self, *, legacy_content_ref: ContentRef) -> ContentRef:
        if not isinstance(legacy_content_ref, ContentRef) or legacy_content_ref.scheme != "chroma":
            raise ContentResolutionLookupError(
                "approved legacy content reference is unavailable",
                error_code="UNKNOWN_CONTENT_REF",
            )
        try:
            return self._mappings[legacy_content_ref]
        except KeyError as error:
            raise ContentResolutionLookupError(
                "approved legacy content reference is unavailable",
                error_code="UNKNOWN_CONTENT_REF",
            ) from error
