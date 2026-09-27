"""Focused, non-private regression checks for the Core144/D1 closeout gate."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

from formal240_core144_scope import build, sha  # noqa: E402
from formal240_remaining90_authority_surface_audit import pattern_flags  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "docs/research/stage6_1_hidden_knowledge_poisoning/formal240"
CORE = ROOT / "docs/research/stage6_1_hidden_knowledge_poisoning/core144"


def test_core144_is_exact_historical_matrix_subset() -> None:
    raw = (FORMAL / "PAPER1_FORMAL_240_GROUP_MATRIX_V1.jsonl").read_bytes()
    view, selection = build(raw)
    assert view == (CORE / "PAPER1_CORE144_GROUP_MATRIX_VIEW_V1.jsonl").read_bytes()
    assert selection == json.loads((CORE / "PAPER1_CORE144_DOMAIN_SELECTION_V1.json").read_text(encoding="utf-8"))
    assert selection["group_count"] == 144
    assert selection["candidate_count_planned"] == 432
    assert selection["deferred_external_extension_domains"] == ["D4", "D5"]
    assert selection["split_executed"] is False
    assert selection["training_started"] is False
    assert sha(view) == "745a891c6cd3709247df84c1a904d1127aa7797b049a3ea780fe9ac6eadc5b76"


def test_owner_overlay_has_exact_four_and_six_without_vote() -> None:
    overlay = json.loads((FORMAL / "PAPER1_FORMAL_D1_REMAINING90_PHASE1_OWNER_ADJUDICATION_OVERLAY_V1.json").read_text(encoding="utf-8"))
    assert {r["blind_review_id"] for r in overlay["local_internal_conflict_decisions"]} == {
        "D1BR-FB2590D87D27", "D1BR-194520C78747", "D1BR-566391C110ED", "D1BR-67D572512767"
    }
    assert all(r["owner_final"] == "YES" for r in overlay["local_internal_conflict_decisions"])
    assert len(overlay["naturalness_decisions"]) == 6
    assert all(r["owner_disposition"] == "NONBLOCKING_REVIEWER_VARIANCE" for r in overlay["naturalness_decisions"])
    assert overlay["majority_vote_used"] is False
    assert overlay["raw_returns_modified"] is False


def test_shortcut_gate_and_provider_registry() -> None:
    shortcut = json.loads((FORMAL / "PAPER1_FORMAL_D1_REMAINING90_AUTHORITY_SURFACE_SHORTCUT_AUDIT_V1.json").read_text(encoding="utf-8"))
    assert shortcut["authority_exact_normalized_syntactic_comma_and_second_clause_counts"] == {
        "CLEAN_CURRENT": 0, "POISON": 4, "HARD_NEGATIVE": 0
    }
    assert shortcut["surface_shortcut_blocker"] is True
    assert shortcut["phase2_release_authorized"] is False
    registry = json.loads((FORMAL / "PAPER1_FORMAL_D1_REVIEWER_REGISTRY_V1.json").read_text(encoding="utf-8"))
    r4 = next(r for r in registry["reviewers"] if r["reviewer_code"] == "R4-codex")
    assert r4["provider"] == "Doubao"
    assert r4["isolation_evidence"] == "OWNER_ATTESTED"


def test_surface_detector_distinguishes_old_and_new_structure() -> None:
    old = "同一文件公布机关既是国务院，同时又是人力资源社会保障部。"
    new = "国务院以第535号令公布该条例，而该条例的同一次公布也由人力资源社会保障部完成。"
    assert pattern_flags(old)["authority_exact_clause"]
    assert not pattern_flags(new)["authority_exact_clause"]


def test_new_closeout_markdown_links_resolve() -> None:
    files = [*CORE.glob("*.md")]
    files.extend(
        FORMAL / name
        for name in (
            "PAPER1_FORMAL_D1_REMAINING90_PHASE1_FINAL_GATE_V1.md",
            "PAPER1_FORMAL_D1_REMAINING90_TARGETED4_OWNER_SEND_CHECKLIST_V2.md",
            "PAPER1_CORE144_D1_PHASE1_DOCUMENTATION_CLOSEOUT_V1.md",
            "PAPER1_FORMAL_D1_REMAINING90_PHASE1_OWNER_ADJUDICATION_RECORD_V1.md",
        )
    )
    for file in files:
        for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", file.read_text(encoding="utf-8")):
            assert (file.parent / target.split("#", 1)[0]).exists(), (file.name, target)
