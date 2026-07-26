"""Static S6-T5.7 integration coverage for the accepted retrieval-context chain."""

from __future__ import annotations

import hashlib
from dataclasses import replace

import pytest

from llmguard.domains.retrieval.context import (
    CanonicalEvidenceEnvelopeFactory,
    CorpusContentResolver,
    DeterministicContextBuilder,
    InMemoryCorpusSnapshotReader,
    StaticApprovedCorpusSnapshotRegistry,
    StaticLegacyContentRefAdapter,
)
from llmguard.domains.retrieval.contracts import (
    CitationMode,
    ContentRef,
    ContentResolutionIntegrityError,
    ContentResolutionLookupError,
    ContextBuildConfig,
    ContextConstructionIntegrityError,
    QueryRecord,
    RetrievalEvidence,
    RetrievalRequest,
    RetrievalTrace,
    derive_evidence_uid,
    project_retriever_query,
)
from llmguard.domains.retrieval.embedding import EmbeddingModelSpec, StaticEmbeddingProvider
from llmguard.domains.retrieval.retrieval import DenseRetriever
from llmguard.domains.retrieval.vectorstore import (
    CollectionFingerprint,
    InMemoryVectorStore,
    VectorCollectionSpec,
    VectorDocument,
)


_REVISION = "16e5344fbfc7dfbbbe0019d30cec21e2940cb4e1"
_SNAPSHOT_ID = "s6t57-static-snapshot"
_CONFIG_HASH = "f" * 64
_QUERY = "synthetic runtime query"
_BODY_ONE = "First verified body with LF\nUnicode: \u96ea."
_BODY_TWO = "Second verified body with LF\nUnicode: \u6708."
_BODY_THREE = "Third verified body with LF\nUnicode: \u661f."


def _sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _chunk(letter: str) -> str:
    return "CH-" + letter * 64


def _provider() -> StaticEmbeddingProvider:
    spec = EmbeddingModelSpec(
        provider="static",
        model_id="llmguard/s6-t5-7-static",
        revision=_REVISION,
        dimension=3,
        normalize_embeddings=True,
        device="cpu",
        batch_size=1,
        trust_remote_code=False,
        local_files_only=True,
        implementation_version="s6_t5_7_static_v1",
    )
    return StaticEmbeddingProvider(
        spec,
        fixture_vectors={_QUERY: (1.0, 0.0, 0.0)},
    )


def _collection(provider: StaticEmbeddingProvider) -> VectorCollectionSpec:
    fingerprint = CollectionFingerprint.from_document_embedding_spec(
        corpus_hash=_sha256("s6-t5.7-static-corpus"),
        corpus_manifest_version="s6-t5.7-static-v1",
        chunking_config_hash=_sha256("identity-chunks"),
        document_embedding_spec=provider.model_spec,
        distance_metric="cosine",
        vector_schema_version="1.0",
        public_metadata_schema_version="1.1",
    )
    return VectorCollectionSpec(
        fingerprint=fingerprint.value,
        dimension=provider.dimension,
        public_metadata_schema_version="1.1",
    )


def _document(*, chunk_id: str, parent_doc_id: str, content: str, vector: tuple[float, ...]) -> VectorDocument:
    content_hash = _sha256(content)
    return VectorDocument(
        doc_id=chunk_id,
        vector=vector,
        metadata={
            "doc_id": chunk_id,
            "parent_doc_id": parent_doc_id,
            "source_id": "synthetic-policy",
            "source_type": "policy",
            "timestamp": "2026-07-26T00:00:00Z",
            "version": "v1",
            "content_hash": content_hash,
            "corpus_snapshot_id": _SNAPSHOT_ID,
            "language": "zh",
        },
        content_hash=content_hash,
        content_ref=f"corpus:{_SNAPSHOT_ID}:{chunk_id}",
    )


def _runtime_chain() -> tuple[
    RetrievalRequest,
    tuple[RetrievalEvidence, ...],
    RetrievalTrace,
    DeterministicContextBuilder,
]:
    provider = _provider()
    collection = _collection(provider)
    store = InMemoryVectorStore()
    store.create_or_open_collection(collection)
    chunks = {
        _chunk("a"): _BODY_ONE,
        _chunk("b"): _BODY_TWO,
        _chunk("c"): _BODY_THREE,
    }
    store.upsert(
        collection,
        (
            _document(chunk_id=_chunk("a"), parent_doc_id="DOC-001", content=_BODY_ONE, vector=(1.0, 0.0, 0.0)),
            _document(chunk_id=_chunk("b"), parent_doc_id="DOC-002", content=_BODY_TWO, vector=(0.8, 0.2, 0.0)),
            _document(chunk_id=_chunk("c"), parent_doc_id="DOC-003", content=_BODY_THREE, vector=(0.7, 0.3, 0.0)),
        ),
    )
    dataset_record = QueryRecord(
        query_id="dataset-query-unsafe-to-expose",
        attack_id="attack-id-must-not-reach-runtime",
        category="synthetic",
        retrieval_query=_QUERY,
        generation_question="generation-question-must-not-reach-runtime",
        expected_clean_doc_ids=("expected-clean-doc-must-not-reach-runtime",),
        metadata={"dataset_split": "synthetic"},
    )
    projected = project_retriever_query(
        dataset_record,
        public_query_id="Q-0001",
        public_metadata={"delivery_layer": "retrieval", "scenario": "synthetic"},
    )
    request = RetrievalRequest.from_query(
        projected,
        request_schema_version="1.0",
        top_k=3,
        collection_fingerprint=collection.fingerprint,
        query_embedding_spec_hash=provider.model_spec.fingerprint(scope="query"),
        retrieval_config_hash=_CONFIG_HASH,
    )
    evidence, trace = DenseRetriever(
        embedding_provider=provider,
        vector_store=store,
        collection=collection,
        retrieval_config_hash=_CONFIG_HASH,
    ).retrieve(request)
    snapshot_fingerprint = _sha256("s6-t5.7-static-snapshot")
    reader = InMemoryCorpusSnapshotReader(
        corpus_snapshot_id=_SNAPSHOT_ID,
        snapshot_fingerprint=snapshot_fingerprint,
        chunks=chunks,
    )
    resolver = CorpusContentResolver(
        registry=StaticApprovedCorpusSnapshotRegistry(
            registrations={_SNAPSHOT_ID: (snapshot_fingerprint, reader)}
        )
    )
    builder = DeterministicContextBuilder(
        resolver=resolver,
        envelope_factory=CanonicalEvidenceEnvelopeFactory(),
    )
    return request, evidence, trace, builder


def _config(*, budget: int = 5000) -> ContextBuildConfig:
    return ContextBuildConfig(
        context_schema_version="1.0",
        max_evidence_count=3,
        max_context_characters=budget,
    )


def test_static_pipeline_projects_evaluator_fields_and_builds_deterministic_package() -> None:
    request, evidence, trace, builder = _runtime_chain()
    first = builder.build(
        request=request,
        evidence=evidence,
        citation_mode=CitationMode.REQUIRED,
        config=_config(),
    )
    second = builder.build(
        request=request,
        evidence=evidence,
        citation_mode=CitationMode.REQUIRED,
        config=_config(),
    )

    assert tuple(item.citation_id for item in first.citation_bindings) == ("E1", "E2", "E3")
    assert first.evidence_count == 3
    assert first.request_id == request.request_id
    assert first.rendered_context_hash == _sha256(first.rendered_context)
    assert trace.trace_hash == _runtime_chain()[2].trace_hash
    assert first.package_id == second.package_id
    assert first.rendered_context_hash == second.rendered_context_hash
    assert first.build_trace.trace_hash == second.build_trace.trace_hash
    assert tuple(item.evidence_uid for item in evidence) == tuple(
        item.evidence_uid for item in _runtime_chain()[1]
    )

    runtime_forms = "\n".join(
        (
            repr(request),
            str(request.to_audit_dict()),
            repr(evidence),
            "\n".join(str(item.to_audit_dict()) for item in evidence),
            repr(trace),
            str(trace.to_audit_dict()),
            repr(first),
            str(first.to_audit_dict()),
        )
    )
    for evaluator_only in (
        "attack-id-must-not-reach-runtime",
        "expected-clean-doc-must-not-reach-runtime",
        "generation-question-must-not-reach-runtime",
        "expected_answer",
        "attack_goal",
        "failure_type",
        "ground_truth",
        "oracle",
        "stealth_level",
        _QUERY,
        _BODY_ONE,
    ):
        assert evaluator_only not in runtime_forms


def test_static_pipeline_stable_prefix_cutoff_does_not_access_later_candidates(monkeypatch: pytest.MonkeyPatch) -> None:
    request, evidence, _trace, builder = _runtime_chain()
    first_only = builder.build(
        request=request,
        evidence=evidence[:1],
        citation_mode=CitationMode.OFF,
        config=_config(),
    )
    counts = {"resolve": 0, "factory": 0, "render": 0}
    original_resolve = builder._resolver.resolve  # type: ignore[attr-defined]
    original_create = builder._envelope_factory.create  # type: ignore[attr-defined]
    original_render = DeterministicContextBuilder._render_candidate

    def counted_resolve(*, content_ref: ContentRef, expected_content_hash: str) -> object:
        counts["resolve"] += 1
        return original_resolve(content_ref=content_ref, expected_content_hash=expected_content_hash)

    def counted_create(*, evidence: RetrievalEvidence, resolved_content: object) -> object:
        counts["factory"] += 1
        return original_create(evidence=evidence, resolved_content=resolved_content)  # type: ignore[arg-type]

    def counted_render(*, envelope: object, binding: object) -> str:
        counts["render"] += 1
        return original_render(envelope=envelope, binding=binding)  # type: ignore[arg-type]

    monkeypatch.setattr(builder._resolver, "resolve", counted_resolve)  # type: ignore[attr-defined]
    monkeypatch.setattr(builder._envelope_factory, "create", counted_create)  # type: ignore[attr-defined]
    monkeypatch.setattr(DeterministicContextBuilder, "_render_candidate", staticmethod(counted_render))

    package = builder.build(
        request=request,
        evidence=evidence,
        citation_mode=CitationMode.OFF,
        config=_config(budget=len(first_only.rendered_context)),
    )

    assert package.abstention_required is False
    assert package.evidence_count == 1
    assert package.build_trace.budget_excluded_uids == (evidence[1].evidence_uid,)
    assert package.build_trace.not_attempted_after_budget_cutoff_uids == (evidence[2].evidence_uid,)
    assert counts == {"resolve": 2, "factory": 2, "render": 2}


@pytest.mark.parametrize("failure", ("unknown_ref", "hash_mismatch", "provenance_mismatch", "duplicate_conflict"))
def test_static_pipeline_failures_are_closed_and_redacted(failure: str) -> None:
    request, evidence, _trace, builder = _runtime_chain()
    sensitive = "body-or-query-must-not-leak"
    if failure == "unknown_ref":
        unknown = replace(
            evidence[0],
            content_ref=ContentRef.corpus(_SNAPSHOT_ID, _chunk("f")),
            chunk_id=_chunk("f"),
            doc_id=_chunk("f"),
            evidence_uid=derive_evidence_uid(
                evidence_schema_version=evidence[0].evidence_schema_version,
                corpus_snapshot_id=evidence[0].corpus_snapshot_id,
                chunk_id=_chunk("f"),
                content_hash=evidence[0].content_hash,
            ),
        )
        with pytest.raises(ContentResolutionLookupError) as captured:
            builder.build(request=request, evidence=(unknown,), citation_mode=CitationMode.OFF, config=_config())
    elif failure == "hash_mismatch":
        wrong_hash = "0" * 64
        bad = replace(
            evidence[0],
            content_hash=wrong_hash,
            evidence_uid=derive_evidence_uid(
                evidence_schema_version=evidence[0].evidence_schema_version,
                corpus_snapshot_id=evidence[0].corpus_snapshot_id,
                chunk_id=evidence[0].chunk_id,
                content_hash=wrong_hash,
            ),
        )
        with pytest.raises(ContentResolutionIntegrityError) as captured:
            builder.build(request=request, evidence=(bad,), citation_mode=CitationMode.OFF, config=_config())
    elif failure == "provenance_mismatch":
        bad = replace(evidence[0], retrieval_request_id="RQ-other")
        with pytest.raises(ContextConstructionIntegrityError) as captured:
            builder.build(request=request, evidence=(bad,), citation_mode=CitationMode.OFF, config=_config())
    else:
        conflict = replace(evidence[0], rank=2, source_id="other-source")
        with pytest.raises(ContextConstructionIntegrityError) as captured:
            builder.build(request=request, evidence=(evidence[0], conflict), citation_mode=CitationMode.OFF, config=_config())

    assert sensitive not in str(captured.value)
    assert _QUERY not in str(captured.value)
    assert _BODY_ONE not in str(captured.value)


def test_static_pipeline_legacy_chroma_reference_requires_exact_synthetic_mapping() -> None:
    content = _BODY_ONE
    chunk_id = _chunk("a")
    fingerprint = _sha256("legacy-snapshot")
    canonical = ContentRef.corpus(_SNAPSHOT_ID, chunk_id)
    resolver = CorpusContentResolver(
        registry=StaticApprovedCorpusSnapshotRegistry(
            registrations={
                _SNAPSHOT_ID: (
                    fingerprint,
                    InMemoryCorpusSnapshotReader(
                        corpus_snapshot_id=_SNAPSHOT_ID,
                        snapshot_fingerprint=fingerprint,
                        chunks={chunk_id: content},
                    ),
                )
            }
        ),
        legacy_adapter=StaticLegacyContentRefAdapter(
            mapping_version="1.0",
            mappings={ContentRef("chroma:legacy-row-a"): canonical},
        ),
    )

    resolved = resolver.resolve(content_ref=ContentRef("chroma:legacy-row-a"), expected_content_hash=_sha256(content))
    assert resolved.canonical_content_ref == canonical
    with pytest.raises(ContentResolutionLookupError):
        resolver.resolve(content_ref=ContentRef("chroma:legacy-row-b"), expected_content_hash=_sha256(content))
