from __future__ import annotations

import hashlib

import pytest

from llmguard.domains.retrieval.contracts import (
    ContentRef,
    ContentResolutionIntegrityError,
    ResolvedContent,
    RetrievalInputError,
)


def _content_hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def _reference() -> ContentRef:
    return ContentRef.corpus("synthetic-v1", "CH-" + "a" * 64)


def test_resolved_content_is_immutable_and_audit_safe() -> None:
    content = "Synthetic policy\nKeep exact bytes."
    resolved = ResolvedContent(
        resolution_schema_version="1.0",
        canonical_content_ref=_reference(),
        corpus_snapshot_id="synthetic-v1",
        chunk_id="CH-" + "a" * 64,
        content_hash=_content_hash(content),
        content=content,
    )

    assert resolved.content == content
    assert resolved.content_length == len(content)
    assert content not in repr(resolved)
    assert resolved.to_audit_dict() == {
        "resolution_schema_version": "1.0",
        "corpus_snapshot_id": "synthetic-v1",
        "chunk_id": "CH-" + "a" * 64,
        "content_hash": _content_hash(content),
        "content_length": len(content),
    }
    with pytest.raises(AttributeError):
        resolved.content = "replacement"  # type: ignore[misc]


def test_resolved_content_hash_uses_exact_utf8_bytes_without_normalization() -> None:
    crlf = "line one\r\nline two"
    nfd = "e\u0301"
    for content in (crlf, nfd):
        resolved = ResolvedContent(
            resolution_schema_version="1.0",
            canonical_content_ref=_reference(),
            corpus_snapshot_id="synthetic-v1",
            chunk_id="CH-" + "a" * 64,
            content_hash=_content_hash(content),
            content=content,
        )
        assert resolved.content == content
        assert resolved.content_hash == _content_hash(content)


def test_resolved_content_rejects_hash_mismatch_without_echoing_content() -> None:
    content = "Synthetic content that must stay out of the error."
    with pytest.raises(ContentResolutionIntegrityError) as caught:
        ResolvedContent(
            resolution_schema_version="1.0",
            canonical_content_ref=_reference(),
            corpus_snapshot_id="synthetic-v1",
            chunk_id="CH-" + "a" * 64,
            content_hash="0" * 64,
            content=content,
        )

    assert caught.value.error_code == "CONTENT_HASH_MISMATCH"
    assert content not in str(caught.value)


def test_resolved_content_rejects_invalid_hash_and_reference_consistency() -> None:
    with pytest.raises(RetrievalInputError, match="content_hash"):
        ResolvedContent(
            resolution_schema_version="1.0",
            canonical_content_ref=_reference(),
            corpus_snapshot_id="synthetic-v1",
            chunk_id="CH-" + "a" * 64,
            content_hash="upper-case-is-invalid",
            content="synthetic",
        )

    with pytest.raises(ContentResolutionIntegrityError):
        ResolvedContent(
            resolution_schema_version="1.0",
            canonical_content_ref=_reference(),
            corpus_snapshot_id="another-snapshot",
            chunk_id="CH-" + "a" * 64,
            content_hash=_content_hash("synthetic"),
            content="synthetic",
        )
