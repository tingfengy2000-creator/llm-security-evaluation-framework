"""Stable collection provenance that deliberately excludes local and label state."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass


_SHA256 = re.compile(r"\A[0-9a-f]{64}\Z")
_REVISION = re.compile(r"\A[0-9a-f]{40}\Z")


def _require_hash(value: object, field_name: str, *, length: int) -> str:
    pattern = _SHA256 if length == 64 else _REVISION
    if not isinstance(value, str) or pattern.fullmatch(value) is None:
        raise ValueError(f"{field_name} must be a lowercase {length}-character digest")
    return value


@dataclass(frozen=True, slots=True)
class CollectionFingerprint:
    """Canonical provenance input for a non-overwritable vector collection."""

    corpus_hash: str
    corpus_manifest_version: str
    chunking_config_hash: str
    embedding_model_id: str
    embedding_revision: str
    embedding_dimension: int
    normalize_embeddings: bool
    distance_metric: str
    vector_schema_version: str
    public_metadata_schema_version: str

    def __post_init__(self) -> None:
        _require_hash(self.corpus_hash, "corpus_hash", length=64)
        _require_hash(self.chunking_config_hash, "chunking_config_hash", length=64)
        _require_hash(self.embedding_revision, "embedding_revision", length=40)
        for field_name in (
            "corpus_manifest_version",
            "embedding_model_id",
            "distance_metric",
            "vector_schema_version",
            "public_metadata_schema_version",
        ):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a nonblank string")
        if type(self.embedding_dimension) is not int or self.embedding_dimension <= 0:
            raise ValueError("embedding_dimension must be a positive integer")
        if type(self.normalize_embeddings) is not bool:
            raise ValueError("normalize_embeddings must be a boolean")

    def canonical_payload(self) -> dict[str, object]:
        return {
            "chunking_config_hash": self.chunking_config_hash,
            "corpus_hash": self.corpus_hash,
            "corpus_manifest_version": self.corpus_manifest_version,
            "distance_metric": self.distance_metric,
            "embedding_dimension": self.embedding_dimension,
            "embedding_model_id": self.embedding_model_id,
            "embedding_revision": self.embedding_revision,
            "normalize_embeddings": self.normalize_embeddings,
            "public_metadata_schema_version": self.public_metadata_schema_version,
            "vector_schema_version": self.vector_schema_version,
        }

    def canonical_json(self) -> str:
        return json.dumps(
            self.canonical_payload(),
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=True,
        )

    @property
    def value(self) -> str:
        return hashlib.sha256(self.canonical_json().encode("utf-8")).hexdigest()
