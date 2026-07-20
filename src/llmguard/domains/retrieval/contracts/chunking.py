"""Stable, text-sensitive contracts for deterministic document chunking."""

from __future__ import annotations

import hashlib
import math
import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import Enum

from .hashing import canonical_json, canonical_json_sha256
from .content_ref import ContentRef
from .public_metadata import freeze_public_metadata, thaw_public_metadata
from .errors import (
    ChunkingConfigurationError,
    ChunkingInputError,
    ChunkingIntegrityError,
)


_SHA256 = re.compile(r"\A[0-9a-f]{64}\Z")
_PINNED_REVISION = re.compile(r"\A[0-9a-f]{40}\Z")
_CHUNK_ID = re.compile(r"\ACH-[0-9a-f]{64}\Z")
_SNAPSHOT_ID = re.compile(r"\A[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z")
_UTC_TIMESTAMP = re.compile(
    r"\A\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|\+00:00)\Z"
)


class ChunkingStrategy(str, Enum):
    """Contract vocabulary for current and future deterministic chunking modes."""

    IDENTITY = "identity"
    FIXED_TOKEN = "fixed_token"
    TOKEN_OVERLAP = "token_overlap"
    SENTENCE = "sentence"
    SEMANTIC = "semantic"


def _require_nonblank(
    value: object,
    field_name: str,
    *,
    error_type: type[ChunkingInputError | ChunkingConfigurationError] = ChunkingInputError,
) -> str:
    if not isinstance(value, str) or not value.strip():
        raise error_type(f"{field_name} must be a nonblank string")
    return value


def _require_pinned_revision(
    value: object,
    field_name: str,
    *,
    error_type: type[ChunkingConfigurationError] = ChunkingConfigurationError,
) -> str:
    if not isinstance(value, str) or _PINNED_REVISION.fullmatch(value) is None:
        raise error_type(f"{field_name} must be a pinned lowercase 40-character revision")
    return value


def _require_positive_optional(value: int | None, field_name: str) -> int | None:
    if value is None:
        return None
    if type(value) is not int or value <= 0:
        raise ChunkingConfigurationError(
            f"{field_name} must be a positive integer when provided"
        )
    return value


def _require_probability(value: float | None, field_name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ChunkingConfigurationError(f"{field_name} must be a finite number")
    number = float(value)
    if not math.isfinite(number) or not 0.0 < number <= 1.0:
        raise ChunkingConfigurationError(f"{field_name} must be in (0, 1]")
    return number


@dataclass(frozen=True, slots=True, kw_only=True)
class ChunkingConfig:
    """Immutable configuration whose fingerprint includes only active semantics."""

    strategy: ChunkingStrategy
    schema_version: str
    implementation_version: str
    tokenizer_model_id: str | None = None
    tokenizer_revision: str | None = None
    max_tokens: int | None = None
    overlap_tokens: int | None = None
    sentence_splitter_id: str | None = None
    sentence_splitter_revision: str | None = None
    locale: str | None = None
    sentence_boundary_policy: str | None = None
    semantic_model_id: str | None = None
    semantic_model_revision: str | None = None
    semantic_threshold: float | None = None
    min_chunk_size: int | None = None
    max_chunk_size: int | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.strategy, ChunkingStrategy):
            raise ChunkingConfigurationError("strategy must be a ChunkingStrategy")
        _require_nonblank(
            self.schema_version,
            "schema_version",
            error_type=ChunkingConfigurationError,
        )
        _require_nonblank(
            self.implementation_version,
            "implementation_version",
            error_type=ChunkingConfigurationError,
        )
        _require_positive_optional(self.max_tokens, "max_tokens")
        _require_positive_optional(self.overlap_tokens, "overlap_tokens")
        _require_positive_optional(self.min_chunk_size, "min_chunk_size")
        _require_positive_optional(self.max_chunk_size, "max_chunk_size")

        if self.strategy is ChunkingStrategy.IDENTITY:
            self._require_only_common_fields()
        elif self.strategy is ChunkingStrategy.FIXED_TOKEN:
            self._validate_fixed_token()
        elif self.strategy is ChunkingStrategy.TOKEN_OVERLAP:
            self._validate_token_overlap()
        elif self.strategy is ChunkingStrategy.SENTENCE:
            self._validate_sentence()
        elif self.strategy is ChunkingStrategy.SEMANTIC:
            self._validate_semantic()
        else:  # pragma: no cover - exhaustive Enum validation above.
            raise ChunkingConfigurationError("unsupported chunking strategy")

    def _require_only_common_fields(self) -> None:
        if any(
            value is not None
            for value in (
                self.tokenizer_model_id,
                self.tokenizer_revision,
                self.max_tokens,
                self.overlap_tokens,
                self.sentence_splitter_id,
                self.sentence_splitter_revision,
                self.locale,
                self.sentence_boundary_policy,
                self.semantic_model_id,
                self.semantic_model_revision,
                self.semantic_threshold,
                self.min_chunk_size,
                self.max_chunk_size,
            )
        ):
            raise ChunkingConfigurationError(
                "identity strategy rejects algorithm-specific parameters"
            )

    def _validate_fixed_token(self) -> None:
        self._require_tokenizer_fields()
        if self.max_tokens is None or self.overlap_tokens is not None:
            raise ChunkingConfigurationError(
                "fixed_token requires max_tokens and rejects overlap_tokens"
            )
        self._require_absent(
            "fixed_token",
            self.sentence_splitter_id,
            self.sentence_splitter_revision,
            self.locale,
            self.sentence_boundary_policy,
            self.semantic_model_id,
            self.semantic_model_revision,
            self.semantic_threshold,
            self.min_chunk_size,
            self.max_chunk_size,
        )

    def _validate_token_overlap(self) -> None:
        self._require_tokenizer_fields()
        if self.max_tokens is None:
            raise ChunkingConfigurationError("token_overlap requires max_tokens")
        if self.overlap_tokens is None or self.overlap_tokens >= self.max_tokens:
            raise ChunkingConfigurationError(
                "overlap_tokens must be smaller than max_tokens"
            )
        self._require_absent(
            "token_overlap",
            self.sentence_splitter_id,
            self.sentence_splitter_revision,
            self.locale,
            self.sentence_boundary_policy,
            self.semantic_model_id,
            self.semantic_model_revision,
            self.semantic_threshold,
            self.min_chunk_size,
            self.max_chunk_size,
        )

    def _validate_sentence(self) -> None:
        _require_nonblank(
            self.sentence_splitter_id,
            "sentence_splitter_id",
            error_type=ChunkingConfigurationError,
        )
        _require_pinned_revision(self.sentence_splitter_revision, "sentence_splitter_revision")
        _require_nonblank(
            self.locale, "locale", error_type=ChunkingConfigurationError
        )
        _require_nonblank(
            self.sentence_boundary_policy,
            "sentence_boundary_policy",
            error_type=ChunkingConfigurationError,
        )
        self._validate_size_pair()
        self._require_absent(
            "sentence",
            self.tokenizer_model_id,
            self.tokenizer_revision,
            self.max_tokens,
            self.overlap_tokens,
            self.semantic_model_id,
            self.semantic_model_revision,
            self.semantic_threshold,
        )

    def _validate_semantic(self) -> None:
        _require_nonblank(
            self.semantic_model_id,
            "semantic_model_id",
            error_type=ChunkingConfigurationError,
        )
        _require_pinned_revision(self.semantic_model_revision, "semantic_model_revision")
        _require_probability(self.semantic_threshold, "semantic_threshold")
        if self.min_chunk_size is None or self.max_chunk_size is None:
            raise ChunkingConfigurationError(
                "semantic requires min_chunk_size and max_chunk_size"
            )
        self._validate_size_pair()
        self._require_absent(
            "semantic",
            self.tokenizer_model_id,
            self.tokenizer_revision,
            self.max_tokens,
            self.overlap_tokens,
            self.sentence_splitter_id,
            self.sentence_splitter_revision,
            self.locale,
            self.sentence_boundary_policy,
        )

    def _require_tokenizer_fields(self) -> None:
        _require_nonblank(
            self.tokenizer_model_id,
            "tokenizer_model_id",
            error_type=ChunkingConfigurationError,
        )
        _require_pinned_revision(self.tokenizer_revision, "tokenizer_revision")

    def _validate_size_pair(self) -> None:
        if (self.min_chunk_size is None) != (self.max_chunk_size is None):
            raise ChunkingConfigurationError(
                "min_chunk_size and max_chunk_size must be provided together"
            )
        if self.min_chunk_size is not None and self.min_chunk_size > self.max_chunk_size:  # type: ignore[operator]
            raise ChunkingConfigurationError(
                "min_chunk_size must not exceed max_chunk_size"
            )

    @staticmethod
    def _require_absent(strategy: str, *values: object) -> None:
        if any(value is not None for value in values):
            raise ChunkingConfigurationError(
                f"{strategy} configuration includes irrelevant parameters"
            )

    def canonical_payload(self) -> dict[str, object]:
        """Return the strategy-specific semantics that define reproducibility."""

        payload: dict[str, object] = {
            "implementation_version": self.implementation_version,
            "schema_version": self.schema_version,
            "strategy": self.strategy.value,
        }
        if self.strategy in {ChunkingStrategy.FIXED_TOKEN, ChunkingStrategy.TOKEN_OVERLAP}:
            payload.update(
                {
                    "max_tokens": self.max_tokens,
                    "tokenizer_model_id": self.tokenizer_model_id,
                    "tokenizer_revision": self.tokenizer_revision,
                }
            )
        if self.strategy is ChunkingStrategy.TOKEN_OVERLAP:
            payload["overlap_tokens"] = self.overlap_tokens
        if self.strategy is ChunkingStrategy.SENTENCE:
            payload.update(
                {
                    "locale": self.locale,
                    "max_chunk_size": self.max_chunk_size,
                    "min_chunk_size": self.min_chunk_size,
                    "sentence_boundary_policy": self.sentence_boundary_policy,
                    "sentence_splitter_id": self.sentence_splitter_id,
                    "sentence_splitter_revision": self.sentence_splitter_revision,
                }
            )
        if self.strategy is ChunkingStrategy.SEMANTIC:
            payload.update(
                {
                    "max_chunk_size": self.max_chunk_size,
                    "min_chunk_size": self.min_chunk_size,
                    "semantic_model_id": self.semantic_model_id,
                    "semantic_model_revision": self.semantic_model_revision,
                    "semantic_threshold": self.semantic_threshold,
                }
            )
        return payload

    def fingerprint(self) -> str:
        return canonical_json_sha256(self.canonical_payload())

    def canonical_json(self) -> str:
        """Serialize the active strategy semantics without machine-local state."""

        return canonical_json(self.canonical_payload())


def format_corpus_content_ref(corpus_snapshot_id: str, chunk_id: str) -> str:
    """Format the only S6-T5.1 content reference scheme without resolving it."""

    _validate_corpus_snapshot_id(corpus_snapshot_id)
    if not isinstance(chunk_id, str) or _CHUNK_ID.fullmatch(chunk_id) is None:
        raise ChunkingInputError("chunk_id must use the canonical CH-SHA256 form")
    return str(ContentRef.corpus(corpus_snapshot_id, chunk_id))


def derive_chunk_id(
    *,
    chunk_schema_version: str,
    corpus_snapshot_id: str,
    parent_doc_id: str,
    chunk_index: int,
    content_hash: str,
    chunking_config_hash: str,
) -> str:
    """Derive the stable identity of one deterministic chunk."""

    _require_nonblank(chunk_schema_version, "chunk_schema_version")
    _validate_corpus_snapshot_id(corpus_snapshot_id)
    _require_nonblank(parent_doc_id, "parent_doc_id")
    if type(chunk_index) is not int or chunk_index < 0:
        raise ChunkingInputError("chunk_index must be a nonnegative integer")
    _require_sha256(content_hash, "content_hash")
    _require_sha256(chunking_config_hash, "chunking_config_hash")
    digest = canonical_json_sha256(
        {
            "chunk_index": chunk_index,
            "chunk_schema_version": chunk_schema_version,
            "chunking_config_hash": chunking_config_hash,
            "content_hash": content_hash,
            "corpus_snapshot_id": corpus_snapshot_id,
            "parent_doc_id": parent_doc_id,
        }
    )
    return f"CH-{digest}"


@dataclass(frozen=True, slots=True, kw_only=True)
class ChunkRecord:
    """The sole stable DTO emitted by a chunker before future retrieval work."""

    chunk_schema_version: str
    chunk_id: str
    parent_doc_id: str
    corpus_snapshot_id: str
    chunk_index: int
    content: str = field(repr=False)
    content_hash: str
    content_ref: str
    chunking_strategy: str
    chunking_config_hash: str
    source_id: str
    source_type: str
    version: str
    timestamp: str
    public_metadata: Mapping[str, object]

    def __post_init__(self) -> None:
        if not isinstance(self.chunk_id, str) or _CHUNK_ID.fullmatch(self.chunk_id) is None:
            raise ChunkingInputError("chunk_id must use the canonical CH-SHA256 form")
        _require_nonblank(self.chunk_schema_version, "chunk_schema_version")
        _require_nonblank(self.parent_doc_id, "parent_doc_id")
        _validate_corpus_snapshot_id(self.corpus_snapshot_id)
        if type(self.chunk_index) is not int or self.chunk_index < 0:
            raise ChunkingInputError("chunk_index must be a nonnegative integer")
        _require_nonblank(self.content, "content")
        _require_sha256(self.content_hash, "content_hash")
        actual_hash = hashlib.sha256(self.content.encode("utf-8")).hexdigest()
        if actual_hash != self.content_hash:
            raise ChunkingIntegrityError(
                "chunk content hash mismatch",
                error_code="CHUNK_CONTENT_HASH_MISMATCH",
            )
        expected_chunk_id = derive_chunk_id(
            chunk_schema_version=self.chunk_schema_version,
            corpus_snapshot_id=self.corpus_snapshot_id,
            parent_doc_id=self.parent_doc_id,
            chunk_index=self.chunk_index,
            content_hash=self.content_hash,
            chunking_config_hash=self.chunking_config_hash,
        )
        if expected_chunk_id != self.chunk_id:
            raise ChunkingIntegrityError(
                "chunk identity mismatch",
                error_code="CHUNK_ID_MISMATCH",
            )
        if self.content_ref != format_corpus_content_ref(
            self.corpus_snapshot_id, self.chunk_id
        ):
            raise ChunkingIntegrityError(
                "content reference mismatch",
                error_code="CONTENT_REFERENCE_MISMATCH",
            )
        if self.chunking_strategy not in {strategy.value for strategy in ChunkingStrategy}:
            raise ChunkingInputError("chunking_strategy is not supported")
        _require_sha256(self.chunking_config_hash, "chunking_config_hash")
        _require_nonblank(self.source_id, "source_id")
        _require_nonblank(self.source_type, "source_type")
        _require_nonblank(self.version, "version")
        if not isinstance(self.timestamp, str) or _UTC_TIMESTAMP.fullmatch(self.timestamp) is None:
            raise ChunkingInputError("timestamp must use UTC ISO-8601 syntax")
        object.__setattr__(
            self,
            "public_metadata",
            freeze_public_metadata(self.public_metadata, error_type=ChunkingInputError),
        )

    def to_audit_dict(self) -> dict[str, object]:
        """Return provenance safe for logs; plaintext chunk content is excluded."""

        return {
            "chunk_schema_version": self.chunk_schema_version,
            "chunk_id": self.chunk_id,
            "parent_doc_id": self.parent_doc_id,
            "corpus_snapshot_id": self.corpus_snapshot_id,
            "chunk_index": self.chunk_index,
            "content_hash": self.content_hash,
            "content_length": len(self.content),
            "content_ref": self.content_ref,
            "chunking_strategy": self.chunking_strategy,
            "chunking_config_hash": self.chunking_config_hash,
            "source_id": self.source_id,
            "source_type": self.source_type,
            "version": self.version,
            "timestamp": self.timestamp,
            "public_metadata": thaw_public_metadata(self.public_metadata),
        }


def _validate_corpus_snapshot_id(value: object) -> str:
    if not isinstance(value, str) or _SNAPSHOT_ID.fullmatch(value) is None:
        raise ChunkingInputError("corpus_snapshot_id must be a safe non-path identifier")
    return value


def _require_sha256(value: object, field_name: str) -> str:
    if not isinstance(value, str) or _SHA256.fullmatch(value) is None:
        raise ChunkingInputError(f"{field_name} must be a lowercase SHA-256 digest")
    return value
