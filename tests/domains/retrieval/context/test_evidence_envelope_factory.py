from __future__ import annotations

import pytest

from llmguard.domains.retrieval.context.envelope import CanonicalEvidenceEnvelopeFactory
from llmguard.domains.retrieval.contracts import (
    ContentRef,
    EvidenceEnvelopeInputError,
    EvidenceEnvelopeIntegrityError,
    EvidenceEnvelopeRuntimeError,
)

from conftest import chunk_id, make_evidence, make_resolved


def test_factory_binds_canonical_evidence_and_resolved_content_only() -> None:
    evidence = make_evidence()
    resolved = make_resolved()

    envelope = CanonicalEvidenceEnvelopeFactory().create(
        evidence=evidence,
        resolved_content=resolved,
    )

    assert envelope.evidence_uid == evidence.evidence_uid
    assert envelope.public_metadata == evidence.public_metadata
    assert envelope.content == resolved.content


@pytest.mark.parametrize(
    "evidence,resolved",
    [
        (object(), make_resolved()),
        (make_evidence(), object()),
        (make_evidence(snapshot="synthetic-v2"), make_resolved()),
        (make_evidence(chunk=chunk_id("b")), make_resolved()),
        (make_evidence(content="other"), make_resolved()),
    ],
)
def test_factory_rejects_noncanonical_or_mismatched_inputs(
    evidence: object,
    resolved: object,
) -> None:
    factory = CanonicalEvidenceEnvelopeFactory()
    expected = EvidenceEnvelopeInputError if not hasattr(evidence, "content_ref") or not hasattr(resolved, "content") else EvidenceEnvelopeIntegrityError

    with pytest.raises(expected) as caught:
        factory.create(evidence=evidence, resolved_content=resolved)  # type: ignore[arg-type]

    assert caught.value.error_code in {"INVALID_EVIDENCE_ENVELOPE", "EVIDENCE_CONTENT_MISMATCH"}


def test_factory_rejects_legacy_reference_even_when_other_fields_match() -> None:
    evidence = make_evidence()
    object.__setattr__(evidence, "content_ref", ContentRef("chroma:legacy-record"))

    with pytest.raises(EvidenceEnvelopeIntegrityError) as caught:
        CanonicalEvidenceEnvelopeFactory().create(
            evidence=evidence,
            resolved_content=make_resolved(),
        )

    assert caught.value.error_code == "EVIDENCE_CONTENT_MISMATCH"


def test_factory_redacts_unknown_construction_failures_and_preserves_cause(monkeypatch: pytest.MonkeyPatch) -> None:
    evidence = make_evidence()
    resolved = make_resolved()

    def fail(**_: object) -> object:
        raise RuntimeError("synthetic body must not escape")

    monkeypatch.setattr("llmguard.domains.retrieval.context.envelope.EvidenceEnvelope", fail)
    with pytest.raises(EvidenceEnvelopeRuntimeError) as caught:
        CanonicalEvidenceEnvelopeFactory().create(evidence=evidence, resolved_content=resolved)

    assert caught.value.error_code == "UNEXPECTED_ENVELOPE_CONSTRUCTION_FAILURE"
    assert "synthetic body" not in str(caught.value)
    assert isinstance(caught.value.__cause__, RuntimeError)
