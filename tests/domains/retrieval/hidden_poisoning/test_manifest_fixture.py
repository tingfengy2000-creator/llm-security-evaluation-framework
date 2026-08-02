from __future__ import annotations

import pytest

from llmguard.domains.retrieval.hidden_poisoning import (
    SCHEMA_VERSION,
    AttackType,
    BenchmarkLabel,
    BenchmarkRecord,
    ClaimsClassification,
    HardNegativeType,
    RunManifest,
    RuntimeAudience,
    SchemaValidationError,
    StealthLevel,
    assert_no_label_leakage,
    canonical_sha256,
    evaluator_values,
    project_runtime_payload,
    validate_hard_negative_coverage,
)


def _manifest(fixture_hash: str) -> RunManifest:
    return RunManifest(
        run_id="RUN-PILOT0-SYNTHETIC-01",
        task_id="S6.1-P1-PILOT0",
        run_type="synthetic_engineering_validation",
        git_commit="4b0395584627636f5f13658a990614d8f39561eb",
        working_tree_state="dirty",
        schema_version=SCHEMA_VERSION,
        fixture_snapshot_hash=fixture_hash,
        split_hash="1" * 64,
        configuration_hash="2" * 64,
        seed=20260802,
        start_utc="2026-08-02T00:00:00Z",
        end_utc="2026-08-02T00:00:01Z",
        exit_code=0,
        result_path="synthetic/pilot0-result.json",
        evidence_index=("targeted-tests", "fixture-hash"),
        claims_classification=ClaimsClassification.ENGINEERING_VALIDATION_ONLY,
    )


def test_fixture_covers_twelve_hkp_stealth_pairs_and_hard_negatives(
    synthetic_records: tuple[BenchmarkRecord, ...],
) -> None:
    poison = [item for item in synthetic_records if item.label is BenchmarkLabel.POISON]
    pairs = {(item.attack_type, item.stealth_level) for item in poison}
    assert pairs == {(attack, stealth) for attack in AttackType for stealth in StealthLevel}
    hard_negatives = [
        item.hard_negative_type
        for item in synthetic_records
        if item.label is BenchmarkLabel.HARD_NEGATIVE
    ]
    coverage = validate_hard_negative_coverage(
        tuple(item for item in hard_negatives if item is not None)
    )
    assert set(coverage) == set(HardNegativeType)


def test_fixture_snapshot_is_deterministic_and_synthetic(
    synthetic_records: tuple[BenchmarkRecord, ...], synthetic_fixture_hash: str
) -> None:
    assert synthetic_fixture_hash == "4f381451688150016b1a518895ad75149cfdfdac4cd512dd6062becba04b2ed0"
    assert synthetic_fixture_hash == canonical_sha256(
        [record.canonical_payload() for record in synthetic_records]
    )
    assert len(synthetic_fixture_hash) == 64
    for record in synthetic_records:
        assert "纯合成" in record.document_text
        assert "个人或机构" in record.document_text


def test_fixture_runtime_projection_contains_no_evaluator_leakage(
    synthetic_records: tuple[BenchmarkRecord, ...],
) -> None:
    for record in synthetic_records:
        payload = project_runtime_payload(record, audience=RuntimeAudience.DETECTOR)
        assert_no_label_leakage(
            payload,
            audience=RuntimeAudience.DETECTOR,
            forbidden_values=evaluator_values(record),
        )


def test_run_manifest_is_deterministic_and_engineering_only(
    synthetic_fixture_hash: str,
) -> None:
    manifest = _manifest(synthetic_fixture_hash)
    assert manifest.claims_classification is ClaimsClassification.ENGINEERING_VALIDATION_ONLY
    assert manifest.sha256() == manifest.sha256()
    assert manifest.canonical_payload()["schema_version"] == SCHEMA_VERSION
    assert RunManifest.from_mapping(manifest.canonical_payload()) == manifest


def test_run_manifest_rejects_missing_unknown_and_formal_claims(
    synthetic_fixture_hash: str,
) -> None:
    payload = _manifest(synthetic_fixture_hash).canonical_payload()
    missing = dict(payload)
    missing.pop("run_id")
    with pytest.raises(SchemaValidationError, match="missing required fields"):
        RunManifest.from_mapping(missing)
    with pytest.raises(SchemaValidationError, match="unknown fields"):
        RunManifest.from_mapping({**payload, "model_result": "forbidden"})
    with pytest.raises(SchemaValidationError, match="record payload is invalid"):
        RunManifest.from_mapping({**payload, "claims_classification": "FORMAL_RESULT"})
