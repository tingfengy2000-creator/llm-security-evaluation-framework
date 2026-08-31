from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RECORD = (
    ROOT
    / "docs"
    / "research"
    / "stage6_1_hidden_knowledge_poisoning"
    / "s6_1_p1_pilot2_adjudication_closure.md"
)
CURRENT = ROOT / "docs" / "governance" / "current_work_state.md"
OWNER = ROOT / "docs" / "governance" / "project_owner_decision_register.md"


def test_adjudication_closure_record_binds_owner_input_and_fail_closed_status() -> None:
    text = RECORD.read_text(encoding="utf-8")

    assert "cf47a6c3ffada717a2a0dee2b67d6b92ebfb6236d599fb8a4daf2957e292dcb1" in text
    assert "84/84" in text
    assert "26/26" in text
    assert "OWNER_ADJUDICATION_CONSISTENCY_BLOCKER" in text
    assert "OWNER_RECONFIRMATION = REQUIRED_FOR_4_CANDIDATES" in text
    assert "GROUND_TRUTH_CANDIDATE = NOT_GENERATED" in text
    assert "PILOT3_ENTRY = NOT_STARTED" in text
    assert "AUTO_CONTINUE = NO" in text


def test_current_state_and_owner_register_preserve_the_stop_gate() -> None:
    current = CURRENT.read_text(encoding="utf-8")
    owner = OWNER.read_text(encoding="utf-8")

    assert "S6.1-P1-PILOT2-ADJUDICATION-CLOSURE-AND-PILOT3-ENTRY" in current
    assert "4_CANDIDATE_RECONFIRMATION_REQUIRED" in current
    assert "PILOT3: **NOT_STARTED / BLOCKED_BY_PILOT2_OWNER_CONSISTENCY**" in current
    assert "PODR-069: PILOT2 Adjudication Closure" in owner
    assert "Ground Truth,\n  Pilot2 closure and Pilot3 have not occurred" in owner
