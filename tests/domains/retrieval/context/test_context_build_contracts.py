from __future__ import annotations

import hashlib
from dataclasses import asdict

import pytest

from llmguard.domains.retrieval.context.envelope import CanonicalEvidenceEnvelopeFactory
from llmguard.domains.retrieval.contracts import (
    CitationBinding,
    CitationMode,
    ContextBuildConfig,
    ContextBuildConfigurationError,
    ContextBuildTrace,
    ContextConstructionIntegrityError,
    RetrievedContextPackage,
)

from conftest import make_evidence, make_resolved


def _binding(citation_id: str = "E1") -> tuple[object, CitationBinding]:
    evidence = make_evidence(content="Synthetic private context")
    envelope = CanonicalEvidenceEnvelopeFactory().create(
        evidence=evidence,
        resolved_content=make_resolved(content="Synthetic private context"),
    )
    return envelope, CitationBinding(
        citation_id=citation_id,
        evidence_uid=envelope.evidence_uid,
        chunk_id=envelope.chunk_id,
        parent_doc_id=envelope.parent_doc_id,
        content_hash=envelope.content_hash,
        source_id=envelope.source_id,
        version=envelope.version,
        rank=envelope.rank,
    )


def _trace(*, evidence_uid: str, included: bool = True) -> ContextBuildTrace:
    return ContextBuildTrace.create(
        trace_schema_version="1.0",
        request_id="RQ-synthetic",
        query_id="Q-0001",
        corpus_snapshot_id="synthetic-v1",
        context_build_config_hash=ContextBuildConfig(
            context_schema_version="1.0",
            max_evidence_count=2,
            max_context_characters=4096,
        ).context_build_config_hash,
        input_evidence_count=1,
        deduplicated_evidence_count=1,
        count_selected_count=1,
        resolved_count=1 if included else 0,
        included_count=1 if included else 0,
        stable_candidate_uids=(evidence_uid,),
        count_selected_uids=(evidence_uid,),
        max_count_excluded_uids=(),
        resolved_uids=(evidence_uid,) if included else (),
        included_uids=(evidence_uid,) if included else (),
        budget_excluded_uids=() if included else (evidence_uid,),
        instruction_budget_not_attempted_uids=(),
        not_attempted_after_budget_cutoff_uids=(),
        decision_codes=("INCLUDED" if included else "BUDGET_EXCLUDED",),
    )


def test_context_build_config_is_deterministic_and_audit_safe() -> None:
    first = ContextBuildConfig(
        context_schema_version="1.0",
        max_evidence_count=2,
        max_context_characters=4096,
    )
    second = ContextBuildConfig(
        context_schema_version="1.0",
        max_evidence_count=2,
        max_context_characters=4096,
    )

    assert first.context_build_config_hash == second.context_build_config_hash
    assert len(first.context_build_config_hash) == 64
    assert first.to_audit_dict() == {
        "context_schema_version": "1.0",
        "max_evidence_count": 2,
        "max_context_characters": 4096,
        "context_build_config_hash": first.context_build_config_hash,
    }


@pytest.mark.parametrize("value", [True, False, 0, -1, 1.5, 2**53])
def test_context_build_config_rejects_non_json_safe_limits(value: object) -> None:
    with pytest.raises(ContextBuildConfigurationError) as caught:
        ContextBuildConfig(
            context_schema_version="1.0",
            max_evidence_count=value,  # type: ignore[arg-type]
            max_context_characters=4096,
        )

    assert caught.value.error_code == "INVALID_CONTEXT_BUILD_CONFIG"
    assert str(value) not in str(caught.value)


def test_context_build_trace_requires_complete_disjoint_decision_partition() -> None:
    evidence_uid = "EV-" + "a" * 64
    trace = _trace(evidence_uid=evidence_uid)

    assert trace.trace_id == "CT-" + trace.trace_hash
    assert trace.included_uids == (evidence_uid,)
    assert "Synthetic private context" not in repr(trace)
    assert "content_ref" not in str(trace.to_audit_dict())

    with pytest.raises(ContextConstructionIntegrityError) as caught:
        ContextBuildTrace.create(
            trace_schema_version="1.0",
            request_id="RQ-synthetic",
            query_id="Q-0001",
            corpus_snapshot_id="synthetic-v1",
            context_build_config_hash=trace.context_build_config_hash,
            input_evidence_count=1,
            deduplicated_evidence_count=1,
            count_selected_count=1,
            resolved_count=1,
            included_count=1,
            stable_candidate_uids=(evidence_uid,),
            count_selected_uids=(evidence_uid,),
            max_count_excluded_uids=(),
            resolved_uids=(evidence_uid,),
            included_uids=(evidence_uid,),
            budget_excluded_uids=(),
            instruction_budget_not_attempted_uids=(),
            not_attempted_after_budget_cutoff_uids=(),
            decision_codes=("BUDGET_EXCLUDED",),
        )

    assert caught.value.error_code == "INVALID_RETRIEVED_CONTEXT_PACKAGE"


def test_package_recomputes_identity_and_keeps_rendered_context_sensitive() -> None:
    envelope, binding = _binding()
    trace = _trace(evidence_uid=envelope.evidence_uid)  # type: ignore[attr-defined]
    rendered_context = "Synthetic private context rendered"
    package = RetrievedContextPackage.create(
        request_id="RQ-synthetic",
        query_id="Q-0001",
        citation_mode=CitationMode.REQUIRED,
        evidence_envelopes=(envelope,),  # type: ignore[arg-type]
        citation_bindings=(binding,),
        rendered_context=rendered_context,
        abstention_required=False,
        abstention_reason_codes=(),
        context_schema_version="1.0",
        context_build_config_hash=trace.context_build_config_hash,
        max_evidence_count=2,
        max_context_characters=4096,
        build_trace=trace,
    )

    assert package.package_id.startswith("PK-")
    assert package.rendered_context_hash == hashlib.sha256(
        rendered_context.encode("utf-8")
    ).hexdigest()
    assert package.build_trace.trace_hash == trace.trace_hash
    assert rendered_context not in repr(package)
    assert rendered_context not in str(package.to_audit_dict())
    assert asdict(package)["rendered_context"] == rendered_context

    object.__setattr__(package, "package_id", "PK-" + "0" * 64)
    with pytest.raises(ContextConstructionIntegrityError):
        package.__post_init__()


def test_abstention_package_requires_exactly_one_reason_and_empty_sensitive_fields() -> None:
    trace = ContextBuildTrace.create(
        trace_schema_version="1.0",
        request_id="RQ-synthetic",
        query_id="Q-0001",
        corpus_snapshot_id="",
        context_build_config_hash="a" * 64,
        input_evidence_count=0,
        deduplicated_evidence_count=0,
        count_selected_count=0,
        resolved_count=0,
        included_count=0,
        stable_candidate_uids=(),
        count_selected_uids=(),
        max_count_excluded_uids=(),
        resolved_uids=(),
        included_uids=(),
        budget_excluded_uids=(),
        instruction_budget_not_attempted_uids=(),
        not_attempted_after_budget_cutoff_uids=(),
        decision_codes=(),
    )
    package = RetrievedContextPackage.create(
        request_id="RQ-synthetic",
        query_id="Q-0001",
        citation_mode=CitationMode.OFF,
        evidence_envelopes=(),
        citation_bindings=(),
        rendered_context="",
        abstention_required=True,
        abstention_reason_codes=("EMPTY_RETRIEVAL",),
        context_schema_version="1.0",
        context_build_config_hash="a" * 64,
        max_evidence_count=1,
        max_context_characters=1,
        build_trace=trace,
    )
    assert package.evidence_count == 0
    assert package.rendered_context_hash == hashlib.sha256(b"").hexdigest()
