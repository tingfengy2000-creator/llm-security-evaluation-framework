from __future__ import annotations

import pytest

from llmguard.domains.retrieval.context.envelope import CanonicalEvidenceEnvelopeFactory
from llmguard.domains.retrieval.contracts import (
    CitationBinding,
    CitationMode,
    ContextBuildConfig,
    ContextBuildTrace,
    ContextConstructionIntegrityError,
    RetrievedContextPackage,
)

from conftest import make_evidence, make_resolved


def _uid(letter: str) -> str:
    return "EV-" + letter * 64


def _config(*, count: int = 2, budget: int = 4096) -> ContextBuildConfig:
    return ContextBuildConfig(
        context_schema_version="1.0",
        max_evidence_count=count,
        max_context_characters=budget,
    )


def _trace_values(*, config: ContextBuildConfig, uid: str = _uid("a")) -> dict[str, object]:
    return {
        "trace_schema_version": "1.0",
        "request_id": "RQ-synthetic",
        "query_id": "Q-0001",
        "corpus_snapshot_id": "synthetic-v1",
        "context_build_config_hash": config.context_build_config_hash,
        "input_evidence_count": 1,
        "deduplicated_evidence_count": 1,
        "count_selected_count": 1,
        "resolved_count": 1,
        "included_count": 1,
        "stable_candidate_uids": (uid,),
        "count_selected_uids": (uid,),
        "max_count_excluded_uids": (),
        "resolved_uids": (uid,),
        "included_uids": (uid,),
        "budget_excluded_uids": (),
        "instruction_budget_not_attempted_uids": (),
        "not_attempted_after_budget_cutoff_uids": (),
        "decision_codes": ("INCLUDED",),
    }


def _trace(
    *, config: ContextBuildConfig, uid: str = _uid("a"), **overrides: object
) -> ContextBuildTrace:
    values = _trace_values(config=config, uid=uid)
    values.update(overrides)
    return ContextBuildTrace.create(**values)


def _binding() -> tuple[object, CitationBinding]:
    evidence = make_evidence(content="Synthetic private context")
    envelope = CanonicalEvidenceEnvelopeFactory().create(
        evidence=evidence,
        resolved_content=make_resolved(content="Synthetic private context"),
    )
    return envelope, CitationBinding(
        citation_id="E1",
        evidence_uid=envelope.evidence_uid,
        chunk_id=envelope.chunk_id,
        parent_doc_id=envelope.parent_doc_id,
        content_hash=envelope.content_hash,
        source_id=envelope.source_id,
        version=envelope.version,
        rank=envelope.rank,
    )


def _package(*, config: ContextBuildConfig) -> RetrievedContextPackage:
    envelope, binding = _binding()
    trace = _trace(config=config, uid=envelope.evidence_uid)
    return RetrievedContextPackage.create(
        request_id="RQ-synthetic",
        query_id="Q-0001",
        citation_mode=CitationMode.REQUIRED,
        evidence_envelopes=(envelope,),  # type: ignore[arg-type]
        citation_bindings=(binding,),
        rendered_context="Synthetic private context rendered",
        abstention_required=False,
        abstention_reason_codes=(),
        context_schema_version=config.context_schema_version,
        context_build_config_hash=config.context_build_config_hash,
        max_evidence_count=config.max_evidence_count,
        max_context_characters=config.max_context_characters,
        build_trace=trace,
    )


@pytest.mark.parametrize(
    "overrides",
    (
        {
            "input_evidence_count": 3,
            "deduplicated_evidence_count": 3,
            "count_selected_count": 3,
            "resolved_count": 3,
            "included_count": 2,
            "stable_candidate_uids": (_uid("a"), _uid("b"), _uid("c")),
            "count_selected_uids": (_uid("a"), _uid("b"), _uid("c")),
            "resolved_uids": (_uid("a"), _uid("b"), _uid("c")),
            "included_uids": (_uid("a"), _uid("c")),
            "budget_excluded_uids": (_uid("b"),),
            "decision_codes": ("INCLUDED", "BUDGET_EXCLUDED", "INCLUDED"),
        },
        {
            "input_evidence_count": 2,
            "deduplicated_evidence_count": 2,
            "count_selected_count": 2,
            "resolved_count": 2,
            "included_count": 0,
            "stable_candidate_uids": (_uid("a"), _uid("b")),
            "count_selected_uids": (_uid("a"), _uid("b")),
            "resolved_uids": (_uid("a"), _uid("b")),
            "included_uids": (),
            "budget_excluded_uids": (_uid("a"), _uid("b")),
            "decision_codes": ("BUDGET_EXCLUDED", "BUDGET_EXCLUDED"),
        },
        {
            "input_evidence_count": 2,
            "deduplicated_evidence_count": 2,
            "count_selected_count": 2,
            "resolved_count": 1,
            "included_count": 1,
            "stable_candidate_uids": (_uid("a"), _uid("b")),
            "count_selected_uids": (_uid("a"), _uid("b")),
            "resolved_uids": (_uid("a"),),
            "included_uids": (_uid("a"),),
            "instruction_budget_not_attempted_uids": (_uid("b"),),
            "decision_codes": ("INCLUDED", "NOT_ATTEMPTED_INSTRUCTION_BUDGET_EXHAUSTED"),
        },
        {
            "input_evidence_count": 1,
            "deduplicated_evidence_count": 0,
            "count_selected_count": 0,
            "resolved_count": 0,
            "included_count": 0,
            "stable_candidate_uids": (),
            "count_selected_uids": (),
            "resolved_uids": (),
            "included_uids": (),
            "decision_codes": (),
        },
        {
            "input_evidence_count": 0,
            "deduplicated_evidence_count": 0,
            "count_selected_count": 0,
            "resolved_count": 0,
            "included_count": 0,
            "stable_candidate_uids": (),
            "count_selected_uids": (),
            "resolved_uids": (),
            "included_uids": (),
            "corpus_snapshot_id": "synthetic-v1",
            "decision_codes": (),
        },
        {
            "input_evidence_count": 2,
            "deduplicated_evidence_count": 2,
            "count_selected_count": 2,
            "resolved_count": 2,
            "included_count": 1,
            "stable_candidate_uids": (_uid("a"), _uid("b")),
            "count_selected_uids": (_uid("a"), _uid("b")),
            "resolved_uids": (_uid("b"), _uid("a")),
            "included_uids": (_uid("a"),),
            "budget_excluded_uids": (_uid("b"),),
            "decision_codes": ("INCLUDED", "BUDGET_EXCLUDED"),
        },
    ),
)
def test_trace_rejects_malformed_frozen_scenarios(overrides: dict[str, object]) -> None:
    with pytest.raises(ContextConstructionIntegrityError) as caught:
        _trace(config=_config(), **overrides)

    assert caught.value.error_code == "INVALID_RETRIEVED_CONTEXT_PACKAGE"
    assert "EV-" not in str(caught.value)


def test_package_rejects_limits_changed_without_a_new_config_hash() -> None:
    config = _config()
    package = _package(config=config)
    object.__setattr__(package, "max_evidence_count", config.max_evidence_count + 1)

    with pytest.raises(ContextConstructionIntegrityError) as caught:
        package.__post_init__()

    assert caught.value.error_code == "INVALID_RETRIEVED_CONTEXT_PACKAGE"


def test_package_rejects_budget_changed_without_a_new_config_hash() -> None:
    config = _config()
    package = _package(config=config)
    object.__setattr__(package, "max_context_characters", config.max_context_characters + 1)

    with pytest.raises(ContextConstructionIntegrityError) as caught:
        package.__post_init__()

    assert caught.value.error_code == "INVALID_RETRIEVED_CONTEXT_PACKAGE"


def test_package_rejects_trace_config_hash_that_differs_from_its_limits() -> None:
    package_config = _config(count=2, budget=4096)
    trace_config = _config(count=3, budget=4096)
    envelope, binding = _binding()
    trace = _trace(config=trace_config, uid=envelope.evidence_uid)

    with pytest.raises(ContextConstructionIntegrityError) as caught:
        RetrievedContextPackage.create(
            request_id="RQ-synthetic",
            query_id="Q-0001",
            citation_mode=CitationMode.REQUIRED,
            evidence_envelopes=(envelope,),  # type: ignore[arg-type]
            citation_bindings=(binding,),
            rendered_context="Synthetic private context rendered",
            abstention_required=False,
            abstention_reason_codes=(),
            context_schema_version=package_config.context_schema_version,
            context_build_config_hash=package_config.context_build_config_hash,
            max_evidence_count=package_config.max_evidence_count,
            max_context_characters=package_config.max_context_characters,
            build_trace=trace,
        )

    assert caught.value.error_code == "INVALID_RETRIEVED_CONTEXT_PACKAGE"


def test_different_limits_require_different_legal_package_identities() -> None:
    first_config = _config(count=2, budget=4096)
    second_config = _config(count=3, budget=4096)
    first = _package(config=first_config)
    second = _package(config=second_config)

    assert first.context_build_config_hash != second.context_build_config_hash
    assert first.package_id != second.package_id


def test_abstention_reason_must_match_trace_scenario() -> None:
    config = _config()
    trace = _trace(
        config=config,
        uid=_uid("a"),
        resolved_count=0,
        included_count=0,
        resolved_uids=(),
        included_uids=(),
        instruction_budget_not_attempted_uids=(_uid("a"),),
        decision_codes=("NOT_ATTEMPTED_INSTRUCTION_BUDGET_EXHAUSTED",),
    )

    with pytest.raises(ContextConstructionIntegrityError) as caught:
        RetrievedContextPackage.create(
            request_id="RQ-synthetic",
            query_id="Q-0001",
            citation_mode=CitationMode.OFF,
            evidence_envelopes=(),
            citation_bindings=(),
            rendered_context="",
            abstention_required=True,
            abstention_reason_codes=("EMPTY_RETRIEVAL",),
            context_schema_version=config.context_schema_version,
            context_build_config_hash=config.context_build_config_hash,
            max_evidence_count=config.max_evidence_count,
            max_context_characters=config.max_context_characters,
            build_trace=trace,
        )

    assert caught.value.error_code == "INVALID_RETRIEVED_CONTEXT_PACKAGE"


@pytest.mark.parametrize(
    ("trace_overrides", "wrong_reason"),
    (
        (
            {
                "input_evidence_count": 0,
                "deduplicated_evidence_count": 0,
                "count_selected_count": 0,
                "resolved_count": 0,
                "included_count": 0,
                "stable_candidate_uids": (),
                "count_selected_uids": (),
                "max_count_excluded_uids": (),
                "resolved_uids": (),
                "included_uids": (),
                "budget_excluded_uids": (),
                "instruction_budget_not_attempted_uids": (),
                "not_attempted_after_budget_cutoff_uids": (),
                "decision_codes": (),
                "corpus_snapshot_id": "",
            },
            "CONTEXT_BUDGET_EXHAUSTED",
        ),
        (
            {
                "input_evidence_count": 2,
                "deduplicated_evidence_count": 2,
                "count_selected_count": 2,
                "resolved_count": 1,
                "included_count": 0,
                "stable_candidate_uids": (_uid("a"), _uid("b")),
                "count_selected_uids": (_uid("a"), _uid("b")),
                "resolved_uids": (_uid("a"),),
                "included_uids": (),
                "budget_excluded_uids": (_uid("a"),),
                "not_attempted_after_budget_cutoff_uids": (_uid("b"),),
                "decision_codes": (
                    "BUDGET_EXCLUDED",
                    "NOT_ATTEMPTED_AFTER_BUDGET_CUTOFF",
                ),
            },
            "EMPTY_RETRIEVAL",
        ),
    ),
)
def test_each_structural_abstention_reason_rejects_a_different_valid_trace(
    trace_overrides: dict[str, object],
    wrong_reason: str,
) -> None:
    config = _config()
    trace = _trace(config=config, **trace_overrides)

    with pytest.raises(ContextConstructionIntegrityError) as caught:
        RetrievedContextPackage.create(
            request_id="RQ-synthetic",
            query_id="Q-0001",
            citation_mode=CitationMode.OFF,
            evidence_envelopes=(),
            citation_bindings=(),
            rendered_context="",
            abstention_required=True,
            abstention_reason_codes=(wrong_reason,),
            context_schema_version=config.context_schema_version,
            context_build_config_hash=config.context_build_config_hash,
            max_evidence_count=config.max_evidence_count,
            max_context_characters=config.max_context_characters,
            build_trace=trace,
        )

    assert caught.value.error_code == "INVALID_RETRIEVED_CONTEXT_PACKAGE"
