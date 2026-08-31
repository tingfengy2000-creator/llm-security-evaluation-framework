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
RESOLUTION = (
    ROOT
    / "docs"
    / "research"
    / "stage6_1_hidden_knowledge_poisoning"
    / "s6_1_p1_pilot2_closure_and_pilot3_signal_feasibility.md"
)


def test_adjudication_closure_record_preserves_blocker_and_adds_resolution() -> None:
    text = RECORD.read_text(encoding="utf-8")

    assert "cf47a6c3ffada717a2a0dee2b67d6b92ebfb6236d599fb8a4daf2957e292dcb1" in text
    assert "84/84" in text
    assert "26/26" in text
    assert "OWNER_ADJUDICATION_CONSISTENCY_BLOCKER" in text
    assert "OWNER_RECONFIRMATION = REQUIRED_FOR_4_CANDIDATES" in text
    assert "GROUND_TRUTH_CANDIDATE = NOT_GENERATED" in text
    assert "PILOT3_ENTRY = NOT_STARTED" in text
    assert "AUTO_CONTINUE = NO" in text
    assert "RESIDUAL_OWNER_INCONSISTENCY = 0" in text
    assert "GENERATED_PILOT_ONLY_NOT_FORMAL_DATASET" in text
    assert "PILOT_DIAGNOSTIC_ONLY" in text


def test_current_state_and_owner_register_record_closed_feasibility_gate() -> None:
    current = CURRENT.read_text(encoding="utf-8")
    owner = OWNER.read_text(encoding="utf-8")

    assert "S6.1-P1-PILOT2-ADJUDICATION-CLOSURE-AND-PILOT3-ENTRY" in current
    assert "GROUND_TRUTH_CANDIDATE: **GENERATED / 36_RECORDS / PILOT_ONLY / NOT_FORMAL_DATASET**" in current
    assert "PILOT3: **ENGINEERING_AND_SIGNAL_FEASIBILITY_ESTABLISHED / PILOT_DIAGNOSTIC_ONLY / STOPPED**" in current
    assert "PODR-069: PILOT2 Adjudication Closure" in owner
    assert "PODR-070: PILOT2 Owner Correction, Ground Truth Closure and Pilot3 Smoke" in owner
    assert "Dataset formal freeze" in owner


def test_resolution_record_freezes_claim_boundary_and_metrics() -> None:
    text = RESOLUTION.read_text(encoding="utf-8")

    assert "CLEAN_CURRENT=1" in text
    assert "POISON_VALIDATED=12" in text
    assert "HARD_NEGATIVE_VALIDATED=23" in text
    assert "value `17` times, B's `53` times" in text
    assert "third/composite value `14` times" in text
    assert "ENGINEERING_AND_SIGNAL_FEASIBILITY_ESTABLISHED / PILOT_DIAGNOSTIC_ONLY" in text
    assert "does not mean `DETECTOR_EFFECTIVENESS_ESTABLISHED`" in text
    assert "DO_NOT_ENTER_240_GROUP_YET" in text
