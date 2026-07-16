"""Immutable, hashable configuration for an embedding model provider."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass

from .base import EmbeddingConfigurationError


_IMMUTABLE_REVISION = re.compile(r"\A[0-9a-f]{40}\Z")
_LOCAL_PATH_MARKER = re.compile(r"(?:^[A-Za-z]:[\\/]|^[/\\]|[\\/])")


def _require_nonblank_string(value: object, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise EmbeddingConfigurationError(f"{field_name} must be a nonblank string")
    return value


@dataclass(frozen=True, slots=True)
class EmbeddingModelSpec:
    """Reproducible model settings with local-only details excluded from its hash."""

    provider: str
    model_id: str
    revision: str
    dimension: int
    normalize_embeddings: bool
    device: str
    batch_size: int
    trust_remote_code: bool = False
    local_files_only: bool = False
    implementation_version: str = "s6_t4_v1"
    cache_dir_ref: str | None = None
    expected_output_dtype: str = "float32"
    query_prefix: str = ""
    document_prefix: str = ""

    def __post_init__(self) -> None:
        _require_nonblank_string(self.provider, "provider")
        _require_nonblank_string(self.model_id, "model_id")
        _require_nonblank_string(self.device, "device")
        _require_nonblank_string(self.implementation_version, "implementation_version")
        _require_nonblank_string(self.expected_output_dtype, "expected_output_dtype")
        if _IMMUTABLE_REVISION.fullmatch(self.revision) is None:
            raise EmbeddingConfigurationError(
                "revision must be a pinned lowercase 40-character commit hash"
            )
        if type(self.dimension) is not int or self.dimension <= 0:
            raise EmbeddingConfigurationError("dimension must be a positive integer")
        if type(self.batch_size) is not int or self.batch_size <= 0:
            raise EmbeddingConfigurationError("batch_size must be a positive integer")
        if type(self.normalize_embeddings) is not bool:
            raise EmbeddingConfigurationError("normalize_embeddings must be a boolean")
        if self.trust_remote_code is not False:
            raise EmbeddingConfigurationError("trust_remote_code must remain false")
        if type(self.local_files_only) is not bool:
            raise EmbeddingConfigurationError("local_files_only must be a boolean")
        if not isinstance(self.query_prefix, str) or not isinstance(
            self.document_prefix, str
        ):
            raise EmbeddingConfigurationError("query_prefix and document_prefix must be strings")
        if self.cache_dir_ref is not None:
            _require_nonblank_string(self.cache_dir_ref, "cache_dir_ref")
            if _LOCAL_PATH_MARKER.search(self.cache_dir_ref) is not None:
                raise EmbeddingConfigurationError(
                    "cache_dir_ref must be a non-path symbolic reference"
                )

    def canonical_payload(self) -> dict[str, object]:
        """Return only output-relevant, platform-independent configuration values."""

        return {
            "batch_size": self.batch_size,
            "dimension": self.dimension,
            "device": self.device,
            "document_prefix": self.document_prefix,
            "expected_output_dtype": self.expected_output_dtype,
            "implementation_version": self.implementation_version,
            "local_files_only": self.local_files_only,
            "model_id": self.model_id,
            "normalize_embeddings": self.normalize_embeddings,
            "provider": self.provider,
            "query_prefix": self.query_prefix,
            "revision": self.revision,
            "trust_remote_code": self.trust_remote_code,
        }

    def canonical_json(self) -> str:
        """Return canonical UTF-8-safe JSON without machine-local cache information."""

        return json.dumps(
            self.canonical_payload(),
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=True,
        )

    def fingerprint(self) -> str:
        """Return a stable SHA-256 hash for collection and audit provenance."""

        return hashlib.sha256(self.canonical_json().encode("utf-8")).hexdigest()
