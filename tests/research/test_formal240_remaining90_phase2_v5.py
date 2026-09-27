"""Non-private regression checks for the bounded D1 Phase2 V5 handoff."""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

from formal240_remaining90_phase2_evidence_preflight import PROPOSED_TWO_SOURCE_PROJECTION  # noqa: E402
from formal240_remaining90_phase2_release_v5 import GUIDES, reviewer_prompt  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "docs/research/stage6_1_hidden_knowledge_poisoning/formal240"


def test_projection_is_exact_two_group_exception() -> None:
    assert PROPOSED_TWO_SOURCE_PROJECTION == {
        "F240-D1-HKP3-S1-C2": ["HD2013", "HD2024"],
        "F240-D1-HKP3-S1-C3": ["EV-INJURY-CURRENT", "EV-INJURY-2010-AMENDMENT"],
    }
    assert all(len(refs) == 2 for refs in PROPOSED_TWO_SOURCE_PROJECTION.values())


def test_phase2_prompts_preserve_provider_and_same_session_boundary() -> None:
    r3 = reviewer_prompt("R3-gpt", "r3.json", "schema.json", "r3-return.json")
    r4 = reviewer_prompt("R4-codex", "r4.json", "schema.json", "r4-return.json")
    assert "R3-gpt (GPT)" in r3
    assert "R4-codex (Doubao)" in r4
    for value in (r3, r4):
        assert "same isolated conversation" in value
        assert "Do not start a new" in value
        assert "one authoritative 90-row MegaWave" in value
        assert "ZERO_EXTERNAL_EVIDENCE_REQUIRED" in value
        assert "not Ground Truth" in value
        assert all(name in value for name in GUIDES)


def test_v5_owner_documents_have_resolving_relative_links() -> None:
    for name in (
        "PAPER1_FORMAL_D1_REMAINING90_TARGETED4_PHASE1_LOCK_AND_GATE_V1.md",
        "PAPER1_FORMAL_D1_REMAINING90_PHASE2_EVIDENCE_PROJECTION_DECISION_V1.md",
        "PAPER1_FORMAL_D1_REMAINING90_PHASE2_RELEASE_RECORD_V5.md",
        "PAPER1_FORMAL_D1_REMAINING90_PHASE2_OWNER_SEND_CHECKLIST_V5.md",
    ):
        path = FORMAL / name
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
            assert (path.parent / target.split("#", 1)[0]).exists(), (path.name, target)
