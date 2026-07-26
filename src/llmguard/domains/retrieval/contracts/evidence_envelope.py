"""Stable sensitive evidence and citation contracts for controlled rendering."""

from __future__ import annotations

import hashlib
import math
import re
from collections.abc import Iterator, Mapping
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum

from .errors import CitationInputError, EvidenceEnvelopeInputError
from .identifiers import (
    require_chunk_id,
    require_evidence_uid,
    require_public_identifier,
    require_sha256,
)
from .public_metadata import freeze_public_metadata, thaw_public_metadata

_UTC_ISO8601 = re.compile(
    r"\A\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|\+00:00)\Z"
)
_CITATION_ID = re.compile(r"\AE(?:[1-9][0-9]*)\Z")


class _FrozenPublicMetadata(Mapping[str, object]):
    """Keep runtime metadata immutable while making sensitive ``asdict`` explicit."""

    __slots__ = ("_value",)
    _value: Mapping[str, object]

    def __init__(self, value: Mapping[str, object]) -> None:
        object.__setattr__(self, "_value", value)

    def __setattr__(self, name: str, value: object) -> None:
        raise AttributeError("frozen public metadata cannot be modified")

    def __delattr__(self, name: str) -> None:
        raise AttributeError("frozen public metadata cannot be modified")

    def __getitem__(self, key: str) -> object:
        return self._value[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self._value)

    def __len__(self) -> int:
        return len(self._value)

    def __deepcopy__(self, memo: dict[int, object]) -> object:
        """Return a detached sensitive copy for dataclasses.asdict()."""

        return thaw_public_metadata(self._value)


def _invalid_envelope() -> EvidenceEnvelopeInputError:
    return EvidenceEnvelopeInputError("evidence envelope is invalid")


def _invalid_binding() -> CitationInputError:
    return CitationInputError(
        "citation binding is invalid",
        error_code="INVALID_CITATION_BINDING",
    )


def _require_timestamp(value: object) -> str:
    if not isinstance(value, str) or _UTC_ISO8601.fullmatch(value) is None:
        raise _invalid_envelope()
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (TypeError, ValueError, OverflowError) as error:
        raise _invalid_envelope() from error
    if parsed.tzinfo is None or parsed.utcoffset() != timedelta(0):
        raise _invalid_envelope()
    return value


def _require_metric(value: object, *, minimum: float, maximum: float | None = None) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise _invalid_envelope()
    try:
        number = float(value)
    except (OverflowError, TypeError, ValueError) as error:
        raise _invalid_envelope() from error
    if not math.isfinite(number) or number < minimum or (maximum is not None and number > maximum):
        raise _invalid_envelope()
    return number


def _require_identifier(value: object, name: str) -> str:
    try:
        return require_public_identifier(value, name)
    except ValueError as error:
        raise _invalid_envelope() from error


def _require_chunk(value: object) -> str:
    try:
        return require_chunk_id(value)
    except ValueError as error:
        raise _invalid_envelope() from error


def _require_digest(value: object, name: str) -> str:
    try:
        return require_sha256(value, name)
    except ValueError as error:
        raise _invalid_envelope() from error


class CitationMode(str, Enum):
    """Closed citation-instruction modes; arbitrary strings are not accepted."""

    OFF = "off"
    AVAILABLE = "available"
    REQUIRED = "required"


@dataclass(frozen=True, slots=True, kw_only=True)
class EvidenceEnvelope:
    """A verified body plus public retrieval provenance for one future block."""

    evidence_uid: str
    doc_id: str
    chunk_id: str
    parent_doc_id: str
    source_id: str
    source_type: str
    version: str
    timestamp: str
    content_hash: str
    rank: int
    distance: float
    similarity: float
    content: str = field(repr=False)
    public_metadata: Mapping[str, object]

    def __post_init__(self) -> None:
        try:
            require_evidence_uid(self.evidence_uid)
        except ValueError as error:
            raise _invalid_envelope() from error
        _require_chunk(self.doc_id)
        _require_chunk(self.chunk_id)
        if self.doc_id != self.chunk_id:
            raise _invalid_envelope()
        for name in ("parent_doc_id", "source_id", "source_type", "version"):
            _require_identifier(getattr(self, name), name)
        _require_timestamp(self.timestamp)
        _require_digest(self.content_hash, "content_hash")
        if type(self.rank) is not int or self.rank <= 0:
            raise _invalid_envelope()
        object.__setattr__(self, "distance", _require_metric(self.distance, minimum=0.0))
        object.__setattr__(self, "similarity", _require_metric(self.similarity, minimum=-1.0, maximum=1.0))
        if not isinstance(self.content, str):
            raise _invalid_envelope()
        if hashlib.sha256(self.content.encode("utf-8")).hexdigest() != self.content_hash:
            raise _invalid_envelope()
        try:
            frozen = freeze_public_metadata(
                self.public_metadata,
                error_type=EvidenceEnvelopeInputError,
            )
        except (TypeError, ValueError, OverflowError) as error:
            raise _invalid_envelope() from error
        object.__setattr__(self, "public_metadata", _FrozenPublicMetadata(frozen))

    @property
    def content_length(self) -> int:
        """Return the original Unicode code-point length without rendering changes."""

        return len(self.content)

    def to_audit_dict(self) -> dict[str, object]:
        """Return the only ordinary, content-free audit representation."""

        return {
            "evidence_uid": self.evidence_uid,
            "doc_id": self.doc_id,
            "chunk_id": self.chunk_id,
            "parent_doc_id": self.parent_doc_id,
            "source_id": self.source_id,
            "source_type": self.source_type,
            "version": self.version,
            "timestamp": self.timestamp,
            "content_hash": self.content_hash,
            "rank": self.rank,
            "distance": self.distance,
            "similarity": self.similarity,
            "content_length": self.content_length,
            "public_metadata": thaw_public_metadata(self.public_metadata),
        }


@dataclass(frozen=True, slots=True, kw_only=True)
class CitationBinding:
    """One package-local citation identity bound to stable evidence identifiers."""

    citation_id: str
    evidence_uid: str
    chunk_id: str
    parent_doc_id: str
    content_hash: str
    source_id: str
    version: str
    rank: int

    def __post_init__(self) -> None:
        if (
            not isinstance(self.citation_id, str)
            or len(self.citation_id) > 128
            or _CITATION_ID.fullmatch(self.citation_id) is None
        ):
            raise CitationInputError("citation id is invalid", error_code="INVALID_CITATION_ID")
        try:
            require_evidence_uid(self.evidence_uid)
            require_chunk_id(self.chunk_id)
            for name in ("parent_doc_id", "source_id", "version"):
                require_public_identifier(getattr(self, name), name)
            require_sha256(self.content_hash, "content_hash")
        except ValueError as error:
            raise _invalid_binding() from error
        if type(self.rank) is not int or self.rank <= 0:
            raise _invalid_binding()

    def to_audit_dict(self) -> dict[str, str | int]:
        """Return all binding fields; this DTO intentionally has no plaintext."""

        return {
            "citation_id": self.citation_id,
            "evidence_uid": self.evidence_uid,
            "chunk_id": self.chunk_id,
            "parent_doc_id": self.parent_doc_id,
            "content_hash": self.content_hash,
            "source_id": self.source_id,
            "version": self.version,
            "rank": self.rank,
        }
