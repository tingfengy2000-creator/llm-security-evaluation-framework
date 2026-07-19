"""Stable collection provenance that deliberately excludes local and label state."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass

from ..embedding.model_spec import EmbeddingModelSpec

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
    document_embedding_spec_hash: str
    distance_metric: str
    vector_schema_version: str
    public_metadata_schema_version: str

    def __post_init__(self) -> None:
        _require_hash(self.corpus_hash, "corpus_hash", length=64)
        _require_hash(self.chunking_config_hash, "chunking_config_hash", length=64)
        _require_hash(
            self.document_embedding_spec_hash,
            "document_embedding_spec_hash",
            length=64,
        )
        for field_name in (
            "corpus_manifest_version",
            "distance_metric",
            "vector_schema_version",
            "public_metadata_schema_version",
        ):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a nonblank string")

    @classmethod
    def from_document_embedding_spec(
        cls,
        *,
        corpus_hash: str,
        corpus_manifest_version: str,
        chunking_config_hash: str,
        document_embedding_spec: EmbeddingModelSpec,
        distance_metric: str,
        vector_schema_version: str,
        public_metadata_schema_version: str,
    ) -> CollectionFingerprint:
        """Build collection provenance from document-vector settings only.

        ``query_prefix`` is intentionally excluded because it cannot alter an
        already persisted document vector. It belongs in a future RunManifest.
        """

        return cls(
            corpus_hash=corpus_hash,
            corpus_manifest_version=corpus_manifest_version,
            chunking_config_hash=chunking_config_hash,
            document_embedding_spec_hash=document_embedding_spec.fingerprint(
                scope="document"
            ),
            distance_metric=distance_metric,
            vector_schema_version=vector_schema_version,
            public_metadata_schema_version=public_metadata_schema_version,
        )

    def canonical_payload(self) -> dict[str, object]:
        return {
            "chunking_config_hash": self.chunking_config_hash,
            "corpus_hash": self.corpus_hash,
            "corpus_manifest_version": self.corpus_manifest_version,
            "distance_metric": self.distance_metric,
            "document_embedding_spec_hash": self.document_embedding_spec_hash,
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
