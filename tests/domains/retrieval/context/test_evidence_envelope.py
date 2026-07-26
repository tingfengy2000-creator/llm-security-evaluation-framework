from __future__ import annotations

from dataclasses import asdict, fields

import pytest

from llmguard.domains.retrieval.contracts import EvidenceEnvelope, EvidenceEnvelopeInputError

from conftest import body_hash, chunk_id


def _envelope(*, content: str = "Line one\r\nCafe\u0301", **overrides: object) -> EvidenceEnvelope:
    values: dict[str, object] = {
        "evidence_uid": "EV-" + "a" * 64,
        "doc_id": chunk_id(),
        "chunk_id": chunk_id(),
        "parent_doc_id": "parent-1",
        "source_id": "source-1",
        "source_type": "policy",
        "version": "v1",
        "timestamp": "2026-07-26T00:00:00Z",
        "content_hash": body_hash(content) if isinstance(content, str) else "a" * 64,
        "rank": 1,
        "distance": 0.25,
        "similarity": 0.75,
        "content": content,
        "public_metadata": {"language": "zh", "nested": {"kind": "synthetic"}},
    }
    values.update(overrides)
    return EvidenceEnvelope(**values)  # type: ignore[arg-type]


def test_envelope_is_frozen_slot_based_kw_only_and_hides_content_from_repr() -> None:
    body = "Synthetic secret body"
    envelope = _envelope(content=body)

    assert "citation_id" not in {item.name for item in fields(envelope)}
    assert body not in repr(envelope)
    assert envelope.content_length == len(body)
    with pytest.raises((AttributeError, TypeError)):
        envelope.rank = 2  # type: ignore[misc]


def test_envelope_preserves_exact_utf8_bytes_without_normalizing_content() -> None:
    body = "Line\r\nCafe\u0301"
    envelope = _envelope(content=body)

    assert envelope.content == body
    assert envelope.content_hash == body_hash(body)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("content", 42),
        ("content_hash", "0" * 64),
        ("rank", 0),
        ("distance", float("inf")),
        ("similarity", 1.1),
        ("public_metadata", {"poison_label": True}),
        ("public_metadata", {"path": "C:" + chr(92) + "private" + chr(92) + "file.txt"}),
    ],
)
def test_envelope_rejects_invalid_or_unsafe_input(field: str, value: object) -> None:
    with pytest.raises(EvidenceEnvelopeInputError) as caught:
        _envelope(**{field: value})

    assert caught.value.error_code == "INVALID_EVIDENCE_ENVELOPE"


def test_envelope_audit_is_allowlisted_and_asdict_remains_sensitive() -> None:
    body = "Synthetic secret body"
    envelope = _envelope(content=body)

    audit = envelope.to_audit_dict()
    assert "content" not in audit
    assert audit["content_length"] == len(body)
    assert body not in repr(audit)
    assert asdict(envelope)["content"] == body
    with pytest.raises(TypeError):
        envelope.public_metadata["extra"] = "blocked"  # type: ignore[index]
