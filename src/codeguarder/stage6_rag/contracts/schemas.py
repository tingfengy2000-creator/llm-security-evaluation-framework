from __future__ import annotations

import re
from collections.abc import Iterable, Mapping, Sequence
from datetime import datetime, timedelta

from codeguarder.stage6_rag.contracts.models import DocumentRecord


REQUIRED_DOCUMENT_FIELDS = {
    "doc_id",
    "content",
    "source_id",
    "source_type",
    "timestamp",
    "version",
    "content_hash",
}

FORBIDDEN_PIPELINE_FIELDS = {
    "poisoned",
    "label",
    "attack_goal",
    "expected_answer",
    "failure_type",
    "ground_truth",
}

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


class SchemaError(ValueError):
    """Raised when a Stage 6 pipeline record violates its schema."""


def _find_forbidden_field(value: object, path: str = "$") -> tuple[str, str] | None:
    if isinstance(value, Mapping):
        for key, nested_value in value.items():
            if isinstance(key, str) and key in FORBIDDEN_PIPELINE_FIELDS:
                return key, f"{path}.{key}"
            found = _find_forbidden_field(nested_value, f"{path}.{key}")
            if found is not None:
                return found
    elif isinstance(value, Sequence) and not isinstance(
        value, (str, bytes, bytearray)
    ):
        for index, nested_value in enumerate(value):
            found = _find_forbidden_field(nested_value, f"{path}[{index}]")
            if found is not None:
                return found
    return None


def _validate_utc_timestamp(value: str) -> None:
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as error:
        raise SchemaError("timestamp must be a valid UTC ISO-8601 value") from error
    if parsed.tzinfo is None or parsed.utcoffset() != timedelta(0):
        raise SchemaError("timestamp must include a UTC offset")


def validate_document(document: Mapping[str, object]) -> DocumentRecord:
    if not isinstance(document, Mapping):
        raise SchemaError("document must be a mapping")

    forbidden = _find_forbidden_field(document)
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

    for field_name in _DOCUMENT_STRING_FIELDS:
        value = document[field_name]
        if not isinstance(value, str) or not value.strip():
            raise SchemaError(f"{field_name} must be a non-empty string")

    timestamp = document["timestamp"]
    content_hash = document["content_hash"]
    assert isinstance(timestamp, str)
    assert isinstance(content_hash, str)
    _validate_utc_timestamp(timestamp)
    if _SHA256_PATTERN.fullmatch(content_hash) is None:
        raise SchemaError(
            "content_hash must be a lowercase 64-character SHA-256 hex digest"
        )

    return DocumentRecord(
        doc_id=document["doc_id"],
        content=document["content"],
        source_id=document["source_id"],
        source_type=document["source_type"],
        timestamp=timestamp,
        version=document["version"],
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
