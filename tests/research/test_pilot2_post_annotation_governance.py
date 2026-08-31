from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RECORD = (
    ROOT
    / "docs"
    / "research"
    / "stage6_1_hidden_knowledge_poisoning"
    / "s6_1_p1_pilot2_post_annotation.md"
)
CURRENT = ROOT / "docs" / "governance" / "current_work_state.md"
OWNER = ROOT / "docs" / "governance" / "project_owner_decision_register.md"


def test_post_annotation_record_binds_inputs_and_stop_gate() -> None:
    text = RECORD.read_text(encoding="utf-8")

    for sha256 in (
        "9e301816bfdd00a0028719679d629b8518bfc21dd9ce70c231de4b4ad7690424",
        "b7865999655928e574d946852245a9a3fe5ee4817df6c593ce2ea339dfc95096",
        "f4e1864e7f47c231f006c7a8750421129f4438e6e49164bd7760edd3e6392c8d",
        "0572a0c6aaf60a200755ae4de4de651b80bfb661ddc15eaeda598e0e9310989d",
        "67081c0e3f7c32d42041ccc736316ed2f42fa979d417a76f577b4e90418d363a",
    ):
        assert sha256 in text

    assert "47" in text
    assert "37" in text
    assert "26" in text
    assert "OWNER_ADJUDICATION = REQUIRED / NOT_EXECUTED" in text
    assert "GROUND_TRUTH_CANDIDATE = NOT_GENERATED" in text
    assert "FORMAL_EXPERIMENT = NOT_STARTED" in text
    assert "AUTO_CONTINUE = NO" in text


def test_current_state_and_owner_decision_point_to_adjudication_gate() -> None:
    current = CURRENT.read_text(encoding="utf-8")
    owner = OWNER.read_text(encoding="utf-8")

    assert "S6.1-P1-PILOT2-POST-ANNOTATION" in current
    assert "FORMAL_AGREEMENT_V2: **COMPLETED_ON_A_B_V2_CURRENT_VALUES**" in current
    assert "OWNER_ADJUDICATION: **REQUIRED / NOT_EXECUTED / 26_CANDIDATES / 84_ISSUES**" in current
    assert "PODR-068: PILOT2 Post-Annotation Validation and Formal Agreement Approval" in owner
    assert "Do not auto-adjudicate or generate Ground Truth" in owner
