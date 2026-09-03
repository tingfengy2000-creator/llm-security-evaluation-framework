from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from scripts.research.finalize_pilot4_protocol_acceptance import (
    KEPT_PROVISIONAL,
    PROMOTED_LESSONS,
    build_ab_contract,
    validate_ab_contract,
)


def test_ab_contract_is_candidate_only() -> None:
    contract = build_ab_contract()
    validate_ab_contract(contract)
    assert contract["status"] == "CANDIDATE_FOR_OWNER_APPROVAL"
    assert contract["execution_approved"] is False
    assert contract["distribution_started"] is False
    assert contract["ground_truth_created"] is False


def test_ab_contract_freezes_independent_human_roles() -> None:
    roles = build_ab_contract()["roles"]
    assert roles["annotator_A"] == "INDEPENDENT_HUMAN_ANNOTATOR"
    assert roles["annotator_B"] == "INDEPENDENT_HUMAN_ANNOTATOR"
    assert roles["adjudicator"] == "PROJECT_OWNER_DISAGREEMENT_ONLY"


def test_phase2_follows_both_phase1_locks() -> None:
    order = build_ab_contract()["phase_order"]
    assert order.index("COLLECT_VALIDATE_AND_HASH_LOCK_BOTH_PHASE1_RETURNS") < order.index(
        "RELEASE_A_AND_B_PHASE2_WITH_FROZEN_SNAPSHOTS_AND_URL_PROVENANCE"
    )


def test_hidden_identifiers_are_forbidden() -> None:
    contract = build_ab_contract()
    forbidden = set(contract["annotator_forbidden_fields"])
    assert {"sample_id", "candidate_kind", "HKP", "expected_contract", "owner_mapping"} <= forbidden
    assert contract["identity_policy"]["canonical_sample_id_visible"] is False


def test_expected_v3_is_not_ground_truth() -> None:
    gate = build_ab_contract()["ground_truth_gate"]
    assert gate["expected_v3_is_ground_truth"] is False
    assert gate["dataset_freeze_requires_separate_owner_approval"] is True


def test_evidence_selection_is_descriptive() -> None:
    agreement = build_ab_contract()["agreement"]
    assert agreement["evidence_selection_role"] == "DESCRIPTIVE_PROCESS_OBSERVATION_ONLY"
    assert "evidence_selection" not in agreement["phase2_fields"]


def test_lesson_promotion_is_explicit_subset() -> None:
    assert len(PROMOTED_LESSONS) == 13
    assert len(set(PROMOTED_LESSONS)) == 13
    assert len(KEPT_PROVISIONAL) == 4
    assert set(PROMOTED_LESSONS).isdisjoint(KEPT_PROVISIONAL)


def test_contract_validation_fails_if_distribution_started() -> None:
    contract = build_ab_contract()
    contract["distribution_started"] = True
    with pytest.raises(ValueError, match="A_B_DISTRIBUTION_BOUNDARY_BLOCKER"):
        validate_ab_contract(contract)


def test_json_serialization_is_utf8_and_stable(tmp_path: Path) -> None:
    path = tmp_path / "contract.json"
    text = json.dumps(build_ab_contract(), ensure_ascii=False, indent=2) + "\n"
    path.write_text(text, encoding="utf-8")
    assert json.loads(path.read_text(encoding="utf-8"))["population"]["candidate_count"] == 72
    assert hashlib.sha256(path.read_bytes()).hexdigest()
