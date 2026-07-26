from __future__ import annotations

from dataclasses import replace

import pytest

from llmguard.domains.retrieval.context import (
    CanonicalEvidenceEnvelopeFactory,
    DeterministicContextBuilder,
)
from llmguard.domains.retrieval.contracts import (
    CitationIntegrityError,
    CitationMode,
    ContentResolutionIntegrityError,
    ContentResolutionLookupError,
    ContextBuildConfig,
    ContextConstructionIntegrityError,
    ContextConstructionRuntimeError,
    EvidenceEnvelopeIntegrityError,
)

from test_context_builder import _builder, _evidence, _register, _request


def _config(*, count: int = 3, budget: int = 20_000) -> ContextBuildConfig:
    return ContextBuildConfig(
        context_schema_version="1.0",
        max_evidence_count=count,
        max_context_characters=budget,
    )


def test_max_evidence_count_is_an_ordered_exclusion_before_resolution() -> None:
    request = _request()
    first = _evidence(request, letter="a", rank=1, body="First")
    second = _evidence(request, letter="b", rank=2, body="Second")
    third = _evidence(request, letter="c", rank=3, body="Third")
    _register((first, "First"), (second, "Second"), (third, "Third"))
    builder, resolver = _builder(first, second, third)

    package = builder.build(
        request=request,
        evidence=(third, second, first),
        citation_mode=CitationMode.AVAILABLE,
        config=_config(count=1),
    )

    assert resolver.calls == [str(first.content_ref)]
    assert package.build_trace.max_count_excluded_uids == (
        second.evidence_uid,
        third.evidence_uid,
    )
    assert package.build_trace.decision_codes == (
        "INCLUDED",
        "MAX_EVIDENCE_COUNT_EXCLUDED",
        "MAX_EVIDENCE_COUNT_EXCLUDED",
    )


def test_exact_duplicate_is_deduplicated_but_semantic_conflict_fails_closed() -> None:
    request = _request()
    evidence = _evidence(request, letter="a", rank=1, body="First")
    _register((evidence, "First"))
    builder, resolver = _builder(evidence)

    package = builder.build(
        request=request,
        evidence=(evidence, evidence),
        citation_mode=CitationMode.OFF,
        config=_config(count=2),
    )
    assert resolver.calls == [str(evidence.content_ref)]
    assert package.build_trace.input_evidence_count == 2
    assert package.build_trace.deduplicated_evidence_count == 1

    conflicting = replace(evidence, source_id="different-source")
    with pytest.raises(ContextConstructionIntegrityError) as caught:
        builder.build(
            request=request,
            evidence=(evidence, conflicting),
            citation_mode=CitationMode.OFF,
            config=_config(count=2),
        )
    assert caught.value.error_code == "DUPLICATE_EVIDENCE_CONFLICT"
    assert "different-source" not in str(caught.value)


def test_mixed_snapshot_is_rejected_without_resolver_access() -> None:
    request = _request()
    first = _evidence(request, letter="a", rank=1, body="First")
    second = _evidence(request, letter="b", rank=2, body="Second")
    object.__setattr__(second, "corpus_snapshot_id", "other-snapshot")
    _register((first, "First"), (second, "Second"))
    builder, resolver = _builder(first, second)

    with pytest.raises(ContextConstructionIntegrityError) as caught:
        builder.build(
            request=request,
            evidence=(first, second),
            citation_mode=CitationMode.OFF,
            config=_config(),
        )
    assert caught.value.error_code == "REQUEST_EVIDENCE_MISMATCH"
    assert resolver.calls == []


def test_collection_mismatch_is_rejected_without_resolver_access() -> None:
    request = _request()
    evidence = _evidence(request, letter="a", rank=1, body="First")
    object.__setattr__(evidence, "collection_fingerprint", "f" * 64)
    builder, resolver = _builder(evidence)

    with pytest.raises(ContextConstructionIntegrityError) as caught:
        builder.build(
            request=request,
            evidence=(evidence,),
            citation_mode=CitationMode.OFF,
            config=_config(),
        )

    assert caught.value.error_code == "REQUEST_EVIDENCE_MISMATCH"
    assert resolver.calls == []


def test_known_resolution_failure_propagates_and_never_becomes_abstention() -> None:
    request = _request()
    evidence = _evidence(request, letter="a", rank=1, body="First")

    class MissingResolver:
        def resolve(self, **_: object) -> object:
            raise ContentResolutionLookupError("private reference", error_code="UNKNOWN_CONTENT_REF")

    builder = DeterministicContextBuilder(
        resolver=MissingResolver(),  # type: ignore[arg-type]
        envelope_factory=CanonicalEvidenceEnvelopeFactory(),
    )
    with pytest.raises(ContentResolutionLookupError) as caught:
        builder.build(
            request=request,
            evidence=(evidence,),
            citation_mode=CitationMode.REQUIRED,
            config=_config(),
        )
    assert caught.value.error_code == "UNKNOWN_CONTENT_REF"
    assert "private reference" not in str(caught.value)


def test_content_integrity_failure_is_redacted_and_never_becomes_abstention() -> None:
    request = _request()
    evidence = _evidence(request, letter="a", rank=1, body="Sensitive body")

    class HashMismatchResolver:
        def resolve(self, **_: object) -> object:
            raise ContentResolutionIntegrityError(
                "Sensitive body and private reference",
                error_code="CONTENT_HASH_MISMATCH",
            )

    builder = DeterministicContextBuilder(
        resolver=HashMismatchResolver(),  # type: ignore[arg-type]
        envelope_factory=CanonicalEvidenceEnvelopeFactory(),
    )
    with pytest.raises(ContentResolutionIntegrityError) as caught:
        builder.build(
            request=request,
            evidence=(evidence,),
            citation_mode=CitationMode.REQUIRED,
            config=_config(),
        )

    assert caught.value.error_code == "CONTENT_HASH_MISMATCH"
    assert "Sensitive body" not in str(caught.value)
    assert caught.value.__cause__ is not None


def test_unknown_factory_failure_is_redacted_as_context_runtime_error() -> None:
    request = _request()
    evidence = _evidence(request, letter="a", rank=1, body="Sensitive body")
    _register((evidence, "Sensitive body"))
    _, resolver = _builder(evidence)

    class ExplodingFactory:
        def create(self, **_: object) -> object:
            raise RuntimeError("Sensitive body and hidden metadata must not escape")

    builder = DeterministicContextBuilder(
        resolver=resolver,
        envelope_factory=ExplodingFactory(),  # type: ignore[arg-type]
    )
    with pytest.raises(ContextConstructionRuntimeError) as caught:
        builder.build(
            request=request,
            evidence=(evidence,),
            citation_mode=CitationMode.REQUIRED,
            config=_config(),
        )
    assert caught.value.error_code == "UNEXPECTED_CONTEXT_CONSTRUCTION_FAILURE"
    assert "Sensitive body" not in str(caught.value)


def test_renderer_binding_failure_is_redacted_and_fails_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    request = _request()
    evidence = _evidence(request, letter="a", rank=1, body="Sensitive body")
    _register((evidence, "Sensitive body"))
    builder, _ = _builder(evidence)

    def _raise_for_test(**_: object) -> str:
        raise CitationIntegrityError("Sensitive body must not escape")

    monkeypatch.setattr(
        "llmguard.domains.retrieval.context.builder.render_evidence_block",
        _raise_for_test,
    )
    with pytest.raises(CitationIntegrityError) as caught:
        builder.build(
            request=request,
            evidence=(evidence,),
            citation_mode=CitationMode.REQUIRED,
            config=_config(),
        )

    assert caught.value.error_code == "CITATION_BINDING_MISMATCH"
    assert "Sensitive body" not in str(caught.value)
    assert caught.value.__cause__ is not None


def test_dependency_context_construction_errors_are_not_trusted_from_resolver() -> None:
    request = _request()
    evidence = _evidence(request, letter="a", rank=1, body="Sensitive body")

    class InjectedResolver:
        def resolve(self, **_: object) -> object:
            raise ContextConstructionIntegrityError(
                "Sensitive body from injected resolver",
                error_code="INJECTED_RESOLVER_SECRET",
            )

    builder = DeterministicContextBuilder(
        resolver=InjectedResolver(),  # type: ignore[arg-type]
        envelope_factory=CanonicalEvidenceEnvelopeFactory(),
    )
    with pytest.raises(ContextConstructionRuntimeError) as caught:
        builder.build(
            request=request,
            evidence=(evidence,),
            citation_mode=CitationMode.REQUIRED,
            config=_config(),
        )

    assert caught.value.error_code == "UNEXPECTED_CONTEXT_CONSTRUCTION_FAILURE"
    assert "Sensitive body" not in str(caught.value)
    assert "INJECTED_RESOLVER_SECRET" not in str(caught.value)
    assert caught.value.__cause__ is not None


def test_factory_and_renderer_context_errors_are_not_trusted_from_dependencies(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    request = _request()
    evidence = _evidence(request, letter="a", rank=1, body="Sensitive body")
    _register((evidence, "Sensitive body"))
    _, resolver = _builder(evidence)

    class InjectedFactory:
        def create(self, **_: object) -> object:
            raise ContextConstructionIntegrityError(
                "Sensitive body from injected factory",
                error_code="INJECTED_FACTORY_SECRET",
            )

    factory_builder = DeterministicContextBuilder(
        resolver=resolver,
        envelope_factory=InjectedFactory(),  # type: ignore[arg-type]
    )
    with pytest.raises(ContextConstructionRuntimeError) as factory_error:
        factory_builder.build(
            request=request,
            evidence=(evidence,),
            citation_mode=CitationMode.REQUIRED,
            config=_config(),
        )

    def _raise_for_test(**_: object) -> str:
        raise ContextConstructionIntegrityError(
            "Sensitive body from injected renderer",
            error_code="INJECTED_RENDERER_SECRET",
        )

    monkeypatch.setattr(
        "llmguard.domains.retrieval.context.builder.render_evidence_block",
        _raise_for_test,
    )
    renderer_builder = DeterministicContextBuilder(
        resolver=resolver,
        envelope_factory=CanonicalEvidenceEnvelopeFactory(),
    )
    with pytest.raises(ContextConstructionRuntimeError) as renderer_error:
        renderer_builder.build(
            request=request,
            evidence=(evidence,),
            citation_mode=CitationMode.REQUIRED,
            config=_config(),
        )

    for caught in (factory_error, renderer_error):
        assert caught.value.error_code == "UNEXPECTED_CONTEXT_CONSTRUCTION_FAILURE"
        assert "Sensitive body" not in str(caught.value)
        assert "INJECTED_" not in str(caught.value)
        assert caught.value.__cause__ is not None


def test_dependency_custom_codes_fall_back_to_their_boundary_default(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    request = _request()
    evidence = _evidence(request, letter="a", rank=1, body="Sensitive body")
    _register((evidence, "Sensitive body"))

    class CustomCodeResolver:
        def resolve(self, **_: object) -> object:
            raise ContentResolutionLookupError(
                "Sensitive resolver detail",
                error_code="CUSTOM_RESOLVER_SECRET",
            )

    resolver_builder = DeterministicContextBuilder(
        resolver=CustomCodeResolver(),  # type: ignore[arg-type]
        envelope_factory=CanonicalEvidenceEnvelopeFactory(),
    )
    with pytest.raises(ContentResolutionLookupError) as resolver_error:
        resolver_builder.build(
            request=request,
            evidence=(evidence,),
            citation_mode=CitationMode.REQUIRED,
            config=_config(),
        )

    _, resolver = _builder(evidence)

    class CustomCodeFactory:
        def create(self, **_: object) -> object:
            raise EvidenceEnvelopeIntegrityError(
                "Sensitive factory detail",
                error_code="CUSTOM_FACTORY_SECRET",
            )

    factory_builder = DeterministicContextBuilder(
        resolver=resolver,
        envelope_factory=CustomCodeFactory(),  # type: ignore[arg-type]
    )
    with pytest.raises(EvidenceEnvelopeIntegrityError) as factory_error:
        factory_builder.build(
            request=request,
            evidence=(evidence,),
            citation_mode=CitationMode.REQUIRED,
            config=_config(),
        )

    def _raise_for_test(**_: object) -> str:
        raise CitationIntegrityError(
            "Sensitive renderer detail",
            error_code="CUSTOM_RENDERER_SECRET",
        )

    monkeypatch.setattr(
        "llmguard.domains.retrieval.context.builder.render_evidence_block",
        _raise_for_test,
    )
    renderer_builder = DeterministicContextBuilder(
        resolver=resolver,
        envelope_factory=CanonicalEvidenceEnvelopeFactory(),
    )
    with pytest.raises(CitationIntegrityError) as renderer_error:
        renderer_builder.build(
            request=request,
            evidence=(evidence,),
            citation_mode=CitationMode.REQUIRED,
            config=_config(),
        )

    expected = (
        (resolver_error, "UNKNOWN_CONTENT_REF"),
        (factory_error, "EVIDENCE_CONTENT_MISMATCH"),
        (renderer_error, "CITATION_BINDING_MISMATCH"),
    )
    for caught, code in expected:
        assert caught.value.error_code == code
        assert "Sensitive" not in str(caught.value)
        assert "CUSTOM_" not in str(caught.value)
        assert caught.value.__cause__ is not None
