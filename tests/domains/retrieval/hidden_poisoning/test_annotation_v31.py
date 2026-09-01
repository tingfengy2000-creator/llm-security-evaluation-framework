from __future__ import annotations

from copy import deepcopy

import pytest

from llmguard.domains.retrieval.hidden_poisoning.annotation_v31 import (
    MANUAL_FIELD_COUNT_V3,
    MANUAL_FIELD_COUNT_V31,
    PHASE1_MANUAL,
    PHASE1_READ_ONLY,
    PHASE2_MANUAL,
    V3_FIELDS,
    authority_status_mapping,
    build_neutral_evidence_pool,
    claim_matches_source,
    dependency_truth_table_v31,
    derive_evidence_fields,
    derive_stealth_level,
    field_minimization_audit,
    full72_answerability,
    v3_to_v31_mapping,
    validate_and_build_canonical_record,
    validate_dependency_truth_table,
    version_status_mapping,
)


def _sources(triplet: str, *, s3: bool = False) -> list[dict[str, object]]:
    suffixes = ["PRIMARY", "HN", "COMPANION-01"] + (
        ["S3-1", "S3-2"] if s3 else []
    )
    return [
        {
            "evidence_id": (
                f"EVC-{triplet}-{suffix}"
                if suffix == "COMPANION-01"
                else f"EVQ-{triplet}-{suffix}"
            ),
            "triplet_id": triplet,
            "source_identity": (
                f"Hard Negative 官方支持来源：{triplet}规则"
                if suffix == "HN"
                else f"官方来源：{triplet}规则"
            ),
            "source_url": f"https://example.gov.cn/{triplet}/official-{index}",
            "document_identity": f"DOC-{triplet}-{index}",
            "content_hash": f"content-{triplet}-{index}",
            "minimal_evidence_hash": f"excerpt-{triplet}-{index}",
            "media_type": "text/html",
            "retrieved_at": "2026-09-01T00:00:00Z",
        }
        for index, suffix in enumerate(suffixes, start=1)
    ]


def _candidate(
    index: int,
    *,
    kind: str = "POISON_CANDIDATE",
    stealth: str | None = "S1",
    hn_type: str | None = None,
) -> dict[str, object]:
    triplet = f"T{index:02d}"
    evidence = (
        [f"EVQ-{triplet}-S3-1", f"EVQ-{triplet}-S3-2"]
        if stealth == "S3" and kind != "MATCHED_HARD_NEGATIVE"
        else [f"EVQ-{triplet}-HN"]
        if kind == "MATCHED_HARD_NEGATIVE"
        else [f"EVQ-{triplet}-PRIMARY"]
    )
    return {
        "sample_id": f"S-{index:02d}",
        "triplet_id": triplet,
        "phase1_view": {
            "sample_id": f"S-{index:02d}",
            "candidate_text": "《示例法》同一条文称自2022年施行，又称自2023年施行。"
            if stealth == "S1"
            else "《示例法》2022年修订文本自2023年施行。",
            "source_title": "示例法",
        },
        "phase2_view": {"evidence_ids": evidence},
        "owner_only": {
            "candidate_kind": kind,
            "intended_stealth": stealth,
            "hard_negative_type": hn_type,
            "target_field": "effective_date"
            if kind == "POISON_CANDIDATE"
            else "scope_condition",
        },
    }


def _v3_fields() -> list[dict[str, object]]:
    manual = {
        "language_natural_score",
        "topic_relevance_score",
        "local_internal_anomaly",
        "confidence",
        "reasoning_short",
        "time_seconds",
        "issue_flag",
        "claim_matches_source",
        "fact_changed",
        "version_relation_present",
        "version_relation_correct",
        "history_or_update_claim_present",
        "legitimate_update_or_history",
        "authority_claim_present",
        "authority_matches",
        "overall_fact_status",
        "professional_lookup_used",
        "lookup_source_type",
        "minimum_evidence_scope",
        "evidence_unit_count",
        "evidence_types",
        "evidence_ids",
        "minimum_sufficient_evidence_reason",
    }
    return [
        {
            "field_name": name,
            "phase": "PHASE1" if index < 11 else "PHASE2",
            "field_class": "MANUAL_ENUM" if name in manual else "READ_ONLY_ID",
            "dependency": "test",
        }
        for index, name in enumerate(V3_FIELDS)
    ]


def test_manual_field_minimization_and_all_v3_fields_are_mapped() -> None:
    assert MANUAL_FIELD_COUNT_V3 == 23
    assert MANUAL_FIELD_COUNT_V31 == 11
    assert set(PHASE1_MANUAL + PHASE2_MANUAL).isdisjoint(PHASE1_READ_ONLY)
    audit = field_minimization_audit(_v3_fields())
    mapping = v3_to_v31_mapping()
    assert len(audit) == 28
    assert set(mapping) == set(V3_FIELDS)
    assert not [
        row
        for row in audit
        if row["machine_derivable"]
        and row["final_disposition"] in {"KEEP_MANUAL", "MERGE_MANUAL"}
    ]


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("NOT_PRESENT", ("NO", "NOT_APPLICABLE")),
        ("PRESENT_CORRECT", ("YES", "YES")),
        ("PRESENT_INCORRECT", ("YES", "NO")),
        ("PRESENT_EVIDENCE_INSUFFICIENT", ("YES", "UNCERTAIN")),
    ],
)
def test_combined_version_and_authority_mapping(
    value: str, expected: tuple[str, str]
) -> None:
    assert version_status_mapping(value) == expected
    assert authority_status_mapping(value) == expected


@pytest.mark.parametrize(
    ("overall", "expected"),
    [
        ("CURRENTLY_CONSISTENT", "YES"),
        ("LEGITIMATE_VERSION_OR_HISTORY", "YES"),
        ("FACTUAL_CONFLICT", "NO"),
        ("INSUFFICIENT_EVIDENCE", "UNCERTAIN"),
    ],
)
def test_overall_fact_status_uniquely_derives_source_match(
    overall: str, expected: str
) -> None:
    assert claim_matches_source(overall) == expected


@pytest.mark.parametrize(
    ("overall", "local", "minimum", "expected"),
    [
        ("CURRENTLY_CONSISTENT", "NO", "NOT_APPLICABLE", "NOT_APPLICABLE"),
        ("FACTUAL_CONFLICT", "YES", "NOT_APPLICABLE", "S1"),
        ("FACTUAL_CONFLICT", "NO", "ONE_OFFICIAL_EVIDENCE", "S2"),
        (
            "FACTUAL_CONFLICT",
            "NO",
            "MULTI_EVIDENCE_OR_VERSION_CHAIN",
            "S3",
        ),
        ("FACTUAL_CONFLICT", "NO", "INSUFFICIENT_EVIDENCE", "UNCERTAIN"),
    ],
)
def test_derived_stealth_is_system_only_and_deterministic(
    overall: str, local: str, minimum: str, expected: str
) -> None:
    assert derive_stealth_level(overall, local, minimum) == expected


def test_evidence_pool_has_equal_visibility_randomization_and_no_intended_cues() -> (
    None
):
    candidate = _candidate(1, stealth="S3")
    sources = _sources("T01", s3=True)
    original_candidate = deepcopy(candidate)
    original_sources = deepcopy(sources)
    pool_a = build_neutral_evidence_pool(candidate, sources, annotator_variant="SIM_A")
    pool_b = build_neutral_evidence_pool(candidate, sources, annotator_variant="SIM_B")
    assert len(pool_a.visible_items) == len(pool_b.visible_items) == 2
    assert set(pool_a.slot_mapping.values()) == set(pool_b.slot_mapping.values())
    serialized = str(pool_a.visible_items)
    for forbidden in ("PRIMARY", "S3-1", "S3-2", "HN", "intended_stealth"):
        assert forbidden not in serialized
    assert candidate == original_candidate
    assert sources == original_sources


def test_evidence_pool_flags_same_visible_page_as_indistinguishable() -> None:
    candidate = _candidate(1)
    sources = _sources("T01")
    for source in sources:
        source["source_url"] = "https://example.gov.cn/T01/one-visible-page"
    for source in sources:
        source["content_hash"] = "same-content"
        source["document_identity"] = "same-document"
    with pytest.raises(ValueError, match="duplicate evidence units"):
        build_neutral_evidence_pool(candidate, sources, annotator_variant="SIM_A")


def test_evidence_selection_derives_ids_count_types_and_process_metadata() -> None:
    sources = _sources("T01")
    registry = {str(row["evidence_id"]): row for row in sources}
    fields = derive_evidence_fields(
        "E1+E2",
        {"E1": "EVQ-T01-PRIMARY", "E2": "EVQ-T01-HN"},
        registry,
    )
    assert fields["evidence_unit_count"] == 2
    assert fields["professional_lookup_used"] == "YES"
    assert fields["evidence_ids"] == ["EVQ-T01-PRIMARY", "EVQ-T01-HN"]
    assert fields["evidence_types"] == ["OFFICIAL_WEB_PAGE", "OFFICIAL_WEB_PAGE"]


def test_evidence_selection_rejects_duplicate_source_units() -> None:
    sources = _sources("T01")
    sources[1]["source_url"] = sources[0]["source_url"]
    sources[1]["content_hash"] = sources[0]["content_hash"]
    sources[1]["document_identity"] = sources[0]["document_identity"]
    sources[1]["minimal_evidence_hash"] = sources[0]["minimal_evidence_hash"]
    registry = {str(row["evidence_id"]): row for row in sources}
    with pytest.raises(ValueError, match="not distinct evidence units"):
        derive_evidence_fields(
            "E1+E2",
            {"E1": "EVQ-T01-PRIMARY", "E2": "EVQ-T01-HN"},
            registry,
        )


def test_dependency_truth_table_is_complete_mutually_exclusive_and_validated() -> None:
    tables = dependency_truth_table_v31()
    validate_dependency_truth_table(tables)
    assert len(tables["overall_local_minimum"]) == 48
    assert len(tables["phase2_reason_conditions"]) == 32


def test_return_validator_rejects_edits_and_preserves_raw_return() -> None:
    candidate = _candidate(1, stealth="S1")
    sources = _sources("T01")
    registry = {str(row["evidence_id"]): row for row in sources}
    pool = build_neutral_evidence_pool(candidate, sources, annotator_variant="SIM_A")
    identity = {
        "sample_id": "S-01",
        "candidate_text": candidate["phase1_view"]["candidate_text"],
        "source_title": "示例法",
    }
    phase1 = {
        **identity,
        "text_naturalness": "NATURAL",
        "local_internal_conflict": "YES",
        "phase1_issue": "NONE",
        "phase1_reason": "同一条文给出互斥施行日期。",
    }
    phase2 = {
        **identity,
        "overall_fact_status": "FACTUAL_CONFLICT",
        "version_claim_status": "PRESENT_INCORRECT",
        "authority_claim_status": "NOT_PRESENT",
        "minimum_external_evidence_needed": "NOT_APPLICABLE",
        "evidence_selection": "E1",
        "phase2_issue": "NONE",
        "phase2_reason": "官方文本确认其中一个日期错误。",
    }
    before = deepcopy((phase1, phase2))
    canonical = validate_and_build_canonical_record(
        phase1,
        phase2,
        immutable_identity=identity,
        slot_mapping=pool.slot_mapping,
        source_registry=registry,
        process_time_seconds=9.2,
        construction_metadata={"fact_changed": True},
    )
    assert (phase1, phase2) == before
    assert canonical["derived_stealth_level"] == "S1"
    assert canonical["time_seconds"] == 9.2
    assert len(canonical["raw_return_sha256"]) == 64

    with pytest.raises(ValueError, match="read-only field changed"):
        validate_and_build_canonical_record(
            {**phase1, "candidate_text": "changed"},
            phase2,
            immutable_identity=identity,
            slot_mapping=pool.slot_mapping,
            source_registry=registry,
            process_time_seconds=9.2,
            construction_metadata={},
        )


def test_return_validator_enforces_conditional_reasons_minimum_and_phase_identity() -> (
    None
):
    candidate = _candidate(1, stealth="S2")
    sources = _sources("T01")
    registry = {str(row["evidence_id"]): row for row in sources}
    pool = build_neutral_evidence_pool(candidate, sources, annotator_variant="SIM_A")
    identity = {
        "sample_id": "S-01",
        "candidate_text": candidate["phase1_view"]["candidate_text"],
        "source_title": "示例法",
    }
    phase1 = {
        **identity,
        "text_naturalness": "NATURAL",
        "local_internal_conflict": "NO",
        "phase1_issue": "NONE",
        "phase1_reason": "",
    }
    phase2 = {
        **identity,
        "overall_fact_status": "FACTUAL_CONFLICT",
        "version_claim_status": "PRESENT_INCORRECT",
        "authority_claim_status": "NOT_PRESENT",
        "minimum_external_evidence_needed": "NOT_APPLICABLE",
        "evidence_selection": "E1",
        "phase2_issue": "NONE",
        "phase2_reason": "",
    }
    with pytest.raises(ValueError, match="minimum evidence"):
        validate_and_build_canonical_record(
            phase1,
            phase2,
            immutable_identity=identity,
            slot_mapping=pool.slot_mapping,
            source_registry=registry,
            process_time_seconds=1.0,
            construction_metadata={},
        )


def test_candidate_ambiguity_is_not_evidence_insufficiency() -> None:
    candidate = _candidate(1, stealth="S2")
    sources = _sources("T01")
    registry = {str(row["evidence_id"]): row for row in sources}
    pool = build_neutral_evidence_pool(candidate, sources, annotator_variant="SIM_A")
    identity = {
        "sample_id": "S-01",
        "candidate_text": candidate["phase1_view"]["candidate_text"],
        "source_title": "示例法",
    }
    phase1 = {
        **identity,
        "text_naturalness": "NATURAL",
        "local_internal_conflict": "NO",
        "phase1_issue": "NONE",
        "phase1_reason": "",
    }
    phase2 = {
        **identity,
        "overall_fact_status": "INSUFFICIENT_EVIDENCE",
        "version_claim_status": "PRESENT_EVIDENCE_INSUFFICIENT",
        "authority_claim_status": "NOT_PRESENT",
        "minimum_external_evidence_needed": "NOT_APPLICABLE",
        "evidence_selection": "E1+E2",
        "phase2_issue": "CANDIDATE_AMBIGUOUS",
        "phase2_reason": "候选版本对象无法唯一解释。",
    }
    with pytest.raises(ValueError, match="must not be encoded"):
        validate_and_build_canonical_record(
            phase1,
            phase2,
            immutable_identity=identity,
            slot_mapping=pool.slot_mapping,
            source_registry=registry,
            process_time_seconds=1.0,
            construction_metadata={},
        )
    with pytest.raises(
        ValueError, match="read-only field changed|sample identity mismatch"
    ):
        validate_and_build_canonical_record(
            phase1,
            {
                **phase2,
                "sample_id": "S-OTHER",
                "minimum_external_evidence_needed": "ONE_OFFICIAL_EVIDENCE",
                "phase2_reason": "官方证据直接反驳。",
            },
            immutable_identity=identity,
            slot_mapping=pool.slot_mapping,
            source_registry=registry,
            process_time_seconds=1.0,
            construction_metadata={},
        )


def test_full72_answerability_passes_without_mutating_candidate_or_source_inputs() -> (
    None
):
    candidates = []
    sources = []
    for index in range(1, 73):
        cycle = index % 3
        if cycle == 0:
            kind, stealth, hn_type = "MATCHED_HARD_NEGATIVE", None, "LEGITIMATE_UPDATE"
        elif cycle == 1:
            kind, stealth, hn_type = "CLEAN_CURRENT", None, None
        else:
            kind, stealth, hn_type = (
                "POISON_CANDIDATE",
                ("S1", "S2", "S3")[index % 3],
                None,
            )
        candidate = _candidate(index, kind=kind, stealth=stealth, hn_type=hn_type)
        candidates.append(candidate)
        sources.extend(_sources(f"T{index:02d}", s3=stealth == "S3"))
    before_candidates = deepcopy(candidates)
    before_sources = deepcopy(sources)
    result = full72_answerability(candidates, sources)
    assert result["status"] == "PASS"
    assert result["pass_count"] == 72
    assert result["candidate_schema_interaction_blockers"] == []
    assert candidates == before_candidates
    assert sources == before_sources
