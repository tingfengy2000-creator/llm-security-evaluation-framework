"""Opaque content references; validation only, never content resolution."""

from __future__ import annotations

import re

from .errors import ContentRefError
from .identifiers import require_chunk_id, require_public_identifier

_CANONICAL = re.compile(r"\Acorpus:([A-Za-z0-9][A-Za-z0-9._-]{0,127}):(CH-[0-9a-f]{64})\Z")
_LEGACY = re.compile(r"\Achroma:([A-Za-z0-9][A-Za-z0-9._-]{0,127})(?::([A-Za-z0-9][A-Za-z0-9._-]{0,127}))?\Z")
_PATH = re.compile(r"(?:\A[A-Za-z]:[\\/]|\A[\\/]{2}|\A/|\Afile:)", re.IGNORECASE)


class ContentRef(str):
    """A string-compatible opaque reference accepted by storage adapters."""

    def __new__(cls, value: str) -> "ContentRef":
        if not isinstance(value, str) or len(value) > 300 or _PATH.search(value) is not None:
            raise ContentRefError("content_ref is invalid", error_code="INVALID_CONTENT_REF")
        canonical = _CANONICAL.fullmatch(value)
        legacy = _LEGACY.fullmatch(value)
        if canonical is not None:
            require_public_identifier(canonical.group(1), "corpus_snapshot_id")
            require_chunk_id(canonical.group(2))
        elif legacy is not None:
            require_public_identifier(legacy.group(1), "legacy_content_id")
            if legacy.group(2) is not None:
                require_public_identifier(legacy.group(2), "legacy_content_id")
        else:
            scheme = value.split(":", 1)[0] if ":" in value else ""
            code = "INVALID_CONTENT_REF_SCHEME" if scheme else "INVALID_CONTENT_REF"
            raise ContentRefError("content_ref is invalid", error_code=code)
        return str.__new__(cls, value)

    @property
    def scheme(self) -> str:
        return self.split(":", 1)[0]

    @property
    def corpus_snapshot_id(self) -> str | None:
        matched = _CANONICAL.fullmatch(self)
        return matched.group(1) if matched is not None else None

    @property
    def chunk_id(self) -> str | None:
        matched = _CANONICAL.fullmatch(self)
        return matched.group(2) if matched is not None else None

    @classmethod
    def corpus(cls, corpus_snapshot_id: str, chunk_id: str) -> "ContentRef":
        require_public_identifier(corpus_snapshot_id, "corpus_snapshot_id")
        require_chunk_id(chunk_id)
        return cls(f"corpus:{corpus_snapshot_id}:{chunk_id}")
