from __future__ import annotations

import json
from pathlib import Path

from scripts.research.prepare_pilot4_owner_adjudication import ENUMS, FLAG_IDS


def test_owner_decision_contract_is_expected_blind_and_blank(tmp_path: Path) -> None:
    template = {
        "expected_v3_loaded": False,
        "candidate_defect_decisions": [
            {
                "sample_id": sample_id,
                "owner_defect_decision": "",
                "owner_defect_reason": "",
            }
            for sample_id in FLAG_IDS
        ],
    }
    path = tmp_path / "template.json"
    path.write_text(json.dumps(template), encoding="utf-8")
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert loaded["expected_v3_loaded"] is False
    assert len(loaded["candidate_defect_decisions"]) == 5
    assert all(
        not row["owner_defect_decision"] for row in loaded["candidate_defect_decisions"]
    )


def test_all_adjudicable_fields_have_full_canonical_enum_space() -> None:
    assert set(ENUMS) == {
        "text_naturalness",
        "local_internal_conflict",
        "phase1_issue",
        "overall_fact_status",
        "version_claim_status",
        "authority_claim_status",
        "minimum_external_evidence_needed",
        "phase2_issue",
    }
    assert "evidence_selection" not in ENUMS
    assert "derived_stealth_level" not in ENUMS
    assert len(ENUMS["overall_fact_status"]) == 4


def test_defect_identifiers_are_frozen() -> None:
    assert FLAG_IDS == (
        "P4Q-3bd40af7ed77",
        "P4Q-954090e9f676",
        "P4Q-89bb0f45e834",
        "P4Q-3ed81a10fec6",
        "P4Q-0444c548e139",
    )
