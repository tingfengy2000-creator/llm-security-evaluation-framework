from __future__ import annotations

from dataclasses import asdict, fields

import pytest

from llmguard.domains.retrieval.contracts import (
    EvidenceEnvelope,
    EvidenceEnvelopeInputError,
    require_evidence_uid,
)

from conftest import body_hash, chunk_id, make_evidence, make_resolved
from llmguard.domains.retrieval.context.envelope import CanonicalEvidenceEnvelopeFactory


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


def test_public_metadata_wrapper_is_slot_based_deeply_immutable_and_audit_stable() -> None:
    envelope = _envelope(
        public_metadata={"nested": {"items": ["one", "two"]}, "language": "zh"}
    )
    metadata = envelope.public_metadata
    before = envelope.to_audit_dict()

    assert not hasattr(metadata, "__dict__")
    with pytest.raises((AttributeError, TypeError)):
        metadata._value = {}  # type: ignore[attr-defined,misc]
    with pytest.raises(TypeError):
        metadata._value["poison_label"] = True  # type: ignore[attr-defined,index]
    with pytest.raises(TypeError):
        metadata["nested"]["label"] = "bad"  # type: ignore[index]
    with pytest.raises(TypeError):
        metadata["nested"]["items"][0] = "changed"  # type: ignore[index]

    assert envelope.to_audit_dict() == before
    sensitive_copy = asdict(envelope)
    assert sensitive_copy["content"] == envelope.content
    assert sensitive_copy["public_metadata"] == before["public_metadata"]


@pytest.mark.parametrize(
    "timestamp",
    [
        "2026-07-26T00:00:00Z",
        "2026-07-26T00:00:00.1Z",
        "2026-07-26T00:00:00.123456Z",
        "2026-07-26T00:00:00.1234567Z",
        "2026-07-26T00:00:00.123456789+00:00",
    ],
)
def test_envelope_factory_accepts_every_canonical_retrieval_timestamp(timestamp: str) -> None:
    evidence = make_evidence(timestamp=timestamp)

    envelope = CanonicalEvidenceEnvelopeFactory().create(
        evidence=evidence,
        resolved_content=make_resolved(),
    )

    assert envelope.timestamp == timestamp


@pytest.mark.parametrize(
    "timestamp",
    ["2026-07-26T00:00:00-02:00", "2026-07-26T00:00:00", "2026-02-30T00:00:00Z", "2026-07-26T00:00:00Z\n", 42],
)
def test_envelope_rejects_noncanonical_timestamp_with_fixed_error(timestamp: object) -> None:
    with pytest.raises(EvidenceEnvelopeInputError) as caught:
        _envelope(timestamp=timestamp)

    assert caught.value.error_code == "INVALID_EVIDENCE_ENVELOPE"
    assert str(caught.value) == "evidence envelope is invalid [INVALID_EVIDENCE_ENVELOPE]"


@pytest.mark.parametrize("field", ["distance", "similarity"])
def test_envelope_maps_huge_metric_to_fixed_input_error(field: str) -> None:
    with pytest.raises(EvidenceEnvelopeInputError) as caught:
        _envelope(**{field: 10**10000})

    assert caught.value.error_code == "INVALID_EVIDENCE_ENVELOPE"
    assert str(caught.value) == "evidence envelope is invalid [INVALID_EVIDENCE_ENVELOPE]"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("distance", True),
        ("similarity", False),
        ("distance", float("inf")),
        ("distance", float("-inf")),
        ("similarity", float("nan")),
    ],
)
def test_envelope_maps_all_nonfinite_or_boolean_metrics_to_fixed_input_error(
    field: str,
    value: object,
) -> None:
    with pytest.raises(EvidenceEnvelopeInputError) as caught:
        _envelope(**{field: value})

    assert caught.value.error_code == "INVALID_EVIDENCE_ENVELOPE"
    assert str(caught.value) == "evidence envelope is invalid [INVALID_EVIDENCE_ENVELOPE]"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("evidence_uid", "public-id"),
        ("evidence_uid", "EV-" + "a" * 63),
        ("evidence_uid", "EV-" + "A" * 64),
        ("evidence_uid", "EV-" + "a" * 64 + " "),
        ("content", 42),
        ("content_hash", "0" * 64),
        ("rank", False),
        ("distance", float("nan")),
        ("similarity", float("-inf")),
        ("public_metadata", {"ground_truth": "forbidden"}),
        ("public_metadata", {"path": "C:" + chr(92) + "private"}),
        ("public_metadata", {"unsupported": object()}),
    ],
)
def test_all_envelope_input_errors_use_fixed_public_message(field: str, value: object) -> None:
    with pytest.raises(EvidenceEnvelopeInputError) as caught:
        _envelope(**{field: value})

    assert caught.value.error_code == "INVALID_EVIDENCE_ENVELOPE"
    assert str(caught.value) == "evidence envelope is invalid [INVALID_EVIDENCE_ENVELOPE]"


def test_envelope_metadata_type_depth_and_cycle_fail_with_one_public_message() -> None:
    cyclic: dict[str, object] = {}
    cyclic["self"] = cyclic
    deeply_nested: dict[str, object] = {}
    cursor = deeply_nested
    for index in range(34):
        next_value: dict[str, object] = {}
        cursor[f"level_{index}"] = next_value
        cursor = next_value

    for metadata in ([], cyclic, deeply_nested):
        with pytest.raises(EvidenceEnvelopeInputError) as caught:
            _envelope(public_metadata=metadata)

        assert caught.value.error_code == "INVALID_EVIDENCE_ENVELOPE"
        assert str(caught.value) == "evidence envelope is invalid [INVALID_EVIDENCE_ENVELOPE]"


def test_canonical_evidence_uid_helper_rejects_noncanonical_values() -> None:
    assert require_evidence_uid("EV-" + "a" * 64) == "EV-" + "a" * 64
    for value in ("EV-" + "a" * 63, "EV-" + "A" * 64, "EV-" + "a" * 64 + "\n", "evidence-1"):
        with pytest.raises(ValueError):
            require_evidence_uid(value)
