from __future__ import annotations

from dataclasses import asdict

from llmguard.domains.retrieval.context.envelope import CanonicalEvidenceEnvelopeFactory

from conftest import make_evidence, make_resolved


def test_asdict_is_sensitive_but_the_ordinary_audit_surface_is_not() -> None:
    content = "Synthetic confidential body"
    envelope = CanonicalEvidenceEnvelopeFactory().create(
        evidence=make_evidence(content=content),
        resolved_content=make_resolved(content=content),
    )

    assert asdict(envelope)["content"] == content
    assert content not in repr(envelope)
    assert content not in str(envelope.to_audit_dict())
    assert not hasattr(envelope, "to_dict")
    assert not hasattr(envelope, "export_content")
