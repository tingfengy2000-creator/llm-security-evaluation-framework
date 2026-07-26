from __future__ import annotations

import hashlib

import pytest

from llmguard.domains.retrieval.context import (
    CanonicalEvidenceEnvelopeFactory,
    DeterministicContextBuilder,
)
from llmguard.domains.retrieval.context.citation import render_citation_instruction
from llmguard.domains.retrieval.context.rendering import render_evidence_block
from llmguard.domains.retrieval.contracts import (
    CitationBinding,
    CitationMode,
    ContentRef,
    ContextBuildConfig,
    ContextConstructionIntegrityError,
    ResolvedContent,
    RetrievalEvidence,
    RetrievalRequest,
    RetrieverQueryRecord,
    derive_evidence_uid,
)


def _hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _request(*, top_k: int = 3) -> RetrievalRequest:
    return RetrievalRequest.from_query(
        RetrieverQueryRecord(
            query_id="Q-0001",
            retrieval_query="Synthetic request that must not be audited.",
            public_metadata={"scenario": "synthetic"},
        ),
        request_schema_version="1.0",
        top_k=top_k,
        collection_fingerprint="b" * 64,
        query_embedding_spec_hash="c" * 64,
        retrieval_config_hash="d" * 64,
    )


def _evidence(
    request: RetrievalRequest,
    *,
    letter: str,
    rank: int,
    body: str,
) -> RetrievalEvidence:
    chunk_id = "CH-" + letter * 64
    digest = _hash(body)
    return RetrievalEvidence(
        evidence_schema_version="1.0",
        evidence_uid=derive_evidence_uid(
            evidence_schema_version="1.0",
            corpus_snapshot_id="synthetic-v1",
            chunk_id=chunk_id,
            content_hash=digest,
        ),
        query_id=request.query_id,
        retrieval_request_id=request.request_id,
        corpus_snapshot_id="synthetic-v1",
        doc_id=chunk_id,
        chunk_id=chunk_id,
        parent_doc_id="parent-" + letter,
        content_ref=ContentRef.corpus("synthetic-v1", chunk_id),
        content_hash=digest,
        source_id="source-" + letter,
        source_type="synthetic",
        version="v1",
        timestamp="2026-07-26T00:00:00Z",
        rank=rank,
        distance=0.1 * rank,
        similarity=1.0 - (0.1 * rank),
        collection_fingerprint=request.collection_fingerprint,
        public_metadata={"language": "zh"},
    )


class _CountingResolver:
    def __init__(self, bodies: dict[str, str]) -> None:
        self._bodies = bodies
        self.calls: list[str] = []

    def resolve(
        self,
        *,
        content_ref: ContentRef,
        expected_content_hash: str,
    ) -> ResolvedContent:
        self.calls.append(str(content_ref))
        body = self._bodies[str(content_ref)]
        return ResolvedContent(
            resolution_schema_version="1.0",
            canonical_content_ref=content_ref,
            corpus_snapshot_id=content_ref.corpus_snapshot_id or "",
            chunk_id=content_ref.chunk_id or "",
            content_hash=expected_content_hash,
            content=body,
        )


def _builder(*evidence: RetrievalEvidence) -> tuple[DeterministicContextBuilder, _CountingResolver]:
    resolver = _CountingResolver(
        {str(item.content_ref): _body_from_hash(item.content_hash) for item in evidence}
    )
    return (
        DeterministicContextBuilder(
            resolver=resolver,
            envelope_factory=CanonicalEvidenceEnvelopeFactory(),
        ),
        resolver,
    )


_BODIES: dict[str, str] = {}


def _body_from_hash(digest: str) -> str:
    return _BODIES[digest]


def _binding_for(item: RetrievalEvidence, citation_id: str) -> CitationBinding:
    return CitationBinding(
        citation_id=citation_id,
        evidence_uid=item.evidence_uid,
        chunk_id=item.chunk_id,
        parent_doc_id=item.parent_doc_id,
        content_hash=item.content_hash,
        source_id=item.source_id,
        version=item.version,
        rank=item.rank,
    )


def _config(*, count: int, budget: int) -> ContextBuildConfig:
    return ContextBuildConfig(
        context_schema_version="1.0",
        max_evidence_count=count,
        max_context_characters=budget,
    )


def _register(*items: tuple[RetrievalEvidence, str]) -> None:
    for evidence, body in items:
        _BODIES[evidence.content_hash] = body


def test_builder_sorts_stably_and_assigns_package_local_citations() -> None:
    request = _request()
    high = _evidence(request, letter="a", rank=1, body="First body")
    low = _evidence(request, letter="b", rank=2, body="Second body")
    _register((high, "First body"), (low, "Second body"))
    builder, resolver = _builder(high, low)

    package = builder.build(
        request=request,
        evidence=(low, high),
        citation_mode=CitationMode.REQUIRED,
        config=_config(count=2, budget=20_000),
    )

    assert resolver.calls == [str(high.content_ref), str(low.content_ref)]
    assert tuple(item.evidence_uid for item in package.evidence_envelopes) == (
        high.evidence_uid,
        low.evidence_uid,
    )
    assert tuple(item.citation_id for item in package.citation_bindings) == ("E1", "E2")
    assert package.abstention_required is False
    assert package.build_trace.decision_codes == ("INCLUDED", "INCLUDED")


def test_instruction_budget_exhaustion_never_calls_resolver() -> None:
    request = _request()
    first = _evidence(request, letter="a", rank=1, body="First body")
    _register((first, "First body"))
    builder, resolver = _builder(first)
    instruction = render_citation_instruction(mode=CitationMode.REQUIRED)

    package = builder.build(
        request=request,
        evidence=(first,),
        citation_mode=CitationMode.REQUIRED,
        config=_config(count=1, budget=len(instruction) - 1),
    )

    assert resolver.calls == []
    assert package.abstention_reason_codes == ("CONTEXT_BUDGET_EXHAUSTED",)
    assert package.build_trace.decision_codes == (
        "NOT_ATTEMPTED_INSTRUCTION_BUDGET_EXHAUSTED",
    )


def test_first_nonfit_stops_without_consuming_a_citation() -> None:
    request = _request()
    first = _evidence(request, letter="a", rank=1, body="First body")
    second = _evidence(request, letter="b", rank=2, body="Second body")
    _register((first, "First body"), (second, "Second body"))
    builder, resolver = _builder(first, second)
    instruction = render_citation_instruction(mode=CitationMode.REQUIRED)

    package = builder.build(
        request=request,
        evidence=(first, second),
        citation_mode=CitationMode.REQUIRED,
        config=_config(count=2, budget=len(instruction)),
    )

    assert resolver.calls == [str(first.content_ref)]
    assert package.abstention_reason_codes == ("NO_COMPLETE_EVIDENCE_BLOCK_FITS",)
    assert package.citation_bindings == ()
    assert package.build_trace.decision_codes == (
        "BUDGET_EXCLUDED",
        "NOT_ATTEMPTED_AFTER_BUDGET_CUTOFF",
    )


def test_partial_fit_uses_unicode_code_points_and_stable_prefix_cutoff() -> None:
    request = _request()
    first = _evidence(request, letter="a", rank=1, body="中文正文")
    second = _evidence(request, letter="b", rank=2, body="Second body that is deliberately longer")
    _register((first, "中文正文"), (second, "Second body that is deliberately longer"))
    builder, resolver = _builder(first, second)
    factory = CanonicalEvidenceEnvelopeFactory()
    first_block = render_evidence_block(
        envelope=factory.create(
            evidence=first,
            resolved_content=ResolvedContent(
                resolution_schema_version="1.0",
                canonical_content_ref=first.content_ref,
                corpus_snapshot_id=first.corpus_snapshot_id,
                chunk_id=first.chunk_id,
                content_hash=first.content_hash,
                content="中文正文",
            ),
        ),
        binding=_binding_for(first, "E1"),
    )
    budget = len(render_citation_instruction(mode=CitationMode.REQUIRED) + first_block)

    package = builder.build(
        request=request,
        evidence=(first, second),
        citation_mode=CitationMode.REQUIRED,
        config=_config(count=2, budget=budget),
    )

    assert resolver.calls == [str(first.content_ref), str(second.content_ref)]
    assert tuple(item.citation_id for item in package.citation_bindings) == ("E1",)
    assert package.build_trace.decision_codes == ("INCLUDED", "BUDGET_EXCLUDED")
    assert len(package.rendered_context) == budget


def test_partial_fit_never_resolves_candidates_after_the_first_nonfit() -> None:
    request = _request()
    first = _evidence(request, letter="a", rank=1, body="First body")
    second = _evidence(request, letter="b", rank=2, body="Second body that is deliberately longer")
    third = _evidence(request, letter="c", rank=3, body="Third body must remain unvisited")
    _register(
        (first, "First body"),
        (second, "Second body that is deliberately longer"),
        (third, "Third body must remain unvisited"),
    )
    builder, resolver = _builder(first, second, third)
    factory = CanonicalEvidenceEnvelopeFactory()
    first_block = render_evidence_block(
        envelope=factory.create(
            evidence=first,
            resolved_content=ResolvedContent(
                resolution_schema_version="1.0",
                canonical_content_ref=first.content_ref,
                corpus_snapshot_id=first.corpus_snapshot_id,
                chunk_id=first.chunk_id,
                content_hash=first.content_hash,
                content="First body",
            ),
        ),
        binding=_binding_for(first, "E1"),
    )

    package = builder.build(
        request=request,
        evidence=(third, second, first),
        citation_mode=CitationMode.REQUIRED,
        config=_config(
            count=3,
            budget=len(render_citation_instruction(mode=CitationMode.REQUIRED) + first_block),
        ),
    )

    assert resolver.calls == [str(first.content_ref), str(second.content_ref)]
    assert third.content_ref not in resolver.calls
    assert package.build_trace.decision_codes == (
        "INCLUDED",
        "BUDGET_EXCLUDED",
        "NOT_ATTEMPTED_AFTER_BUDGET_CUTOFF",
    )


def test_empty_retrieval_returns_deterministic_structural_abstention() -> None:
    request = _request()
    builder, resolver = _builder()

    package = builder.build(
        request=request,
        evidence=(),
        citation_mode=CitationMode.OFF,
        config=_config(count=1, budget=100),
    )

    assert resolver.calls == []
    assert package.abstention_reason_codes == ("EMPTY_RETRIEVAL",)
    assert package.rendered_context == ""
    assert package.build_trace.corpus_snapshot_id == ""


def test_request_evidence_mismatch_and_duplicate_conflict_fail_closed() -> None:
    request = _request()
    evidence = _evidence(request, letter="a", rank=1, body="First body")
    _register((evidence, "First body"))
    builder, _ = _builder(evidence)
    object.__setattr__(evidence, "query_id", "Q-9999")

    with pytest.raises(ContextConstructionIntegrityError) as mismatch:
        builder.build(
            request=request,
            evidence=(evidence,),
            citation_mode=CitationMode.OFF,
            config=_config(count=1, budget=1000),
        )
    assert mismatch.value.error_code == "REQUEST_EVIDENCE_MISMATCH"
