from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from datetime import datetime, timedelta

from llmguard.domains.retrieval.contracts.models import (
    DocumentRecord,
    _find_forbidden_pipeline_field,
    _FORBIDDEN_PIPELINE_FIELD_NAMES,
)


REQUIRED_DOCUMENT_FIELDS = frozenset(
    {
        "doc_id",
        "content",
        "source_id",
        "source_type",
        "timestamp",
        "version",
        "content_hash",
    }
)

FORBIDDEN_PIPELINE_FIELDS = frozenset(_FORBIDDEN_PIPELINE_FIELD_NAMES)

_DOCUMENT_STRING_FIELDS = (
    "doc_id",
    "content",
    "source_id",
    "source_type",
    "timestamp",
    "version",
    "content_hash",
)
_SHA256_PATTERN = re.compile(r"[0-9a-f]{64}\Z")
_UTC_ISO8601_PATTERN = re.compile(
    r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}"
    r"(?:\.\d+)?(?:Z|\+00:00)\Z"
)


class SchemaError(ValueError):
    """Raised when a Stage 6 pipeline record violates its schema."""


def _validate_utc_timestamp(value: str) -> None:
    if _UTC_ISO8601_PATTERN.fullmatch(value) is None:
        raise SchemaError("timestamp must use canonical UTC ISO-8601 syntax")
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as error:
        raise SchemaError("timestamp must be a valid UTC ISO-8601 value") from error
    if parsed.tzinfo is None or parsed.utcoffset() != timedelta(0):
        raise SchemaError("timestamp must include a UTC offset")


def validate_document(document: Mapping[str, object]) -> DocumentRecord:
    if not isinstance(document, Mapping):
        raise SchemaError("document must be a mapping")

    forbidden = _find_forbidden_pipeline_field(document)
    if forbidden is not None:
        field_name, path = forbidden
        raise SchemaError(f"forbidden field '{field_name}' at {path}")

    document_fields = set(document)
    missing = REQUIRED_DOCUMENT_FIELDS - document_fields
    if missing:
        raise SchemaError(f"missing required fields: {sorted(missing)}")
    extra = document_fields - REQUIRED_DOCUMENT_FIELDS
    if extra:
        raise SchemaError(f"unexpected fields: {sorted(extra)}")

    validated_strings: dict[str, str] = {}
    for field_name in _DOCUMENT_STRING_FIELDS:
        value = document[field_name]
        if not isinstance(value, str) or not value.strip():
            raise SchemaError(f"{field_name} must be a non-empty string")
        validated_strings[field_name] = value

    timestamp = validated_strings["timestamp"]
    content_hash = validated_strings["content_hash"]
    _validate_utc_timestamp(timestamp)
    if _SHA256_PATTERN.fullmatch(content_hash) is None:
        raise SchemaError(
            "content_hash must be a lowercase 64-character SHA-256 hex digest"
        )

    return DocumentRecord(
        doc_id=validated_strings["doc_id"],
        content=validated_strings["content"],
        source_id=validated_strings["source_id"],
        source_type=validated_strings["source_type"],
        timestamp=timestamp,
        version=validated_strings["version"],
        content_hash=content_hash,
    )


def validate_document_collection(
    documents: Iterable[Mapping[str, object]],
) -> tuple[DocumentRecord, ...]:
    records: list[DocumentRecord] = []
    seen_doc_ids: set[str] = set()
    for document in documents:
        record = validate_document(document)
        if record.doc_id in seen_doc_ids:
            raise SchemaError(f"duplicate doc_id: {record.doc_id}")
        seen_doc_ids.add(record.doc_id)
        records.append(record)
    return tuple(records)
