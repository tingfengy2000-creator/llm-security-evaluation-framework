"""Forward-only D1 Canary reviewer identity and isolation gate checks."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "docs/research/stage6_1_hidden_knowledge_poisoning/formal240"


def _read(name: str) -> str:
    return (FORMAL / name).read_text(encoding="utf-8")


def test_v2_plan_requires_both_fresh_phase1_locks_and_isolated_codex() -> None:
    plan = _read("PAPER1_FORMAL_D1_CANARY_R3_GPT_R4_CODEX_REVIEW_PLAN_V2.md")
    assert "R3-gpt" in plan and "R4-codex" in plan
    assert "both" in plan.lower() and "Phase1 raw locks" in plan
    assert "new projectless task in an empty, isolated directory" in plan.lower()
    assert "not proof of filesystem isolation" in plan
    assert "R4_CODEX_INDEPENDENCE_INVALID=TRUE" in plan
    assert "Different model/system implementations" in plan
    assert "as a model benchmark" in plan
    assert "none of these artifacts exists yet" in plan


def test_attestation_is_run_level_and_has_required_identity_fields() -> None:
    schema = json.loads(_read("PAPER1_FORMAL_D1_FRESH_REVIEW_RUN_ATTESTATION_SCHEMA_V1.json"))
    required = set(schema["required"])
    assert {
        "reviewer_id",
        "review_platform",
        "fresh_session_confirmed",
        "repo_access_prohibited",
        "repo_access_occurred",
        "owner_packet_not_seen",
        "old_reviewer_returns_not_seen",
        "label_mapping_not_seen",
        "phase2_not_seen_before_phase1_lock",
        "external_search_not_used",
        "allowed_files",
        "started_at",
    } <= required
    assert schema["properties"]["reviewer_id"]["enum"] == ["R3-gpt", "R4-codex"]
    assert schema["properties"]["attestation_status"]["enum"] == ["PENDING", "PASS", "FAIL"]
    assert "candidate" in schema["title"].lower()


def test_phase_prompts_have_identical_review_semantics_and_codex_only_isolation() -> None:
    for phase in ("PHASE1", "PHASE2"):
        gpt = _read(f"PAPER1_FORMAL_D1_R3_GPT_BLIND_REVIEWER_PROMPT_{phase}_V4_1.md")
        codex = _read(f"PAPER1_FORMAL_D1_R4_CODEX_BLIND_REVIEWER_PROMPT_{phase}_V4_1.md")
        common_codex = codex.split("\nCodex-specific execution boundary:", 1)[0]
        assert gpt.replace("R3-gpt", "REVIEWER") == common_codex.replace("R4-codex", "REVIEWER")
        assert "Codex-specific execution boundary:" in codex
        assert "projectless" in codex and "Do not run `rg`" in codex
        for prompt in (gpt, codex):
            assert "D1BR-" not in prompt and "P4Q-" not in prompt
            assert re.search(r"(?<![A-Z0-9])R[12](?![A-Z0-9])", prompt) is None
            assert "other reviewers' work" in prompt or "another reviewer's work" in prompt
            assert "exactly one JSON array of 24 objects" in prompt
            assert "both fresh" in prompt
        if phase == "PHASE1":
            assert "PACKAGE_PHASE1_V2.json" in gpt
            assert "PACKAGE_PHASE2_V3.json" not in gpt
            assert "GUIDE_V4_1_CLARIFICATION.md" not in gpt
            assert "search the web" in codex
        else:
            assert "PACKAGE_PHASE2_V3.json" in gpt
            assert "GUIDE_V4_1_CLARIFICATION.md" in gpt
            assert "same session" in codex
            assert "reviewer/session/routing defects" in codex


def test_old_raw_and_future_raw_not_reclassified_as_current_returns() -> None:
    plan = _read("PAPER1_FORMAL_D1_CANARY_R3_GPT_R4_CODEX_REVIEW_PLAN_V2.md")
    closeout = _read("PAPER1_FORMAL_D1_FRESH_REVIEWER_IDENTITY_CLOSEOUT_V1.md")
    assert "old R1/R2 names/raw" in plan
    assert "historical R1/R2" in closeout
    for future_raw in (
        "PAPER1_FORMAL_D1_CANARY_R3_GPT_PHASE1_RAW_V1.json",
        "PAPER1_FORMAL_D1_CANARY_R4_CODEX_PHASE1_RAW_V1.json",
        "PAPER1_FORMAL_D1_CANARY_R3_GPT_PHASE2_RAW_V1.json",
        "PAPER1_FORMAL_D1_CANARY_R4_CODEX_PHASE2_RAW_V1.json",
    ):
        assert future_raw in plan
        assert not (FORMAL / future_raw).exists()


def test_new_control_plane_files_are_portable_and_linked() -> None:
    names = (
        "PAPER1_FORMAL_D1_CANARY_R3_GPT_R4_CODEX_REVIEW_PLAN_V2.md",
        "PAPER1_FORMAL_D1_FRESH_REVIEWER_IDENTITY_CLOSEOUT_V1.md",
        "PAPER1_FORMAL_D1_FRESH_REVIEW_RUN_ATTESTATION_SCHEMA_V1.json",
        "PAPER1_FORMAL_D1_R3_GPT_BLIND_REVIEWER_PROMPT_PHASE1_V4_1.md",
        "PAPER1_FORMAL_D1_R3_GPT_BLIND_REVIEWER_PROMPT_PHASE2_V4_1.md",
        "PAPER1_FORMAL_D1_R4_CODEX_BLIND_REVIEWER_PROMPT_PHASE1_V4_1.md",
        "PAPER1_FORMAL_D1_R4_CODEX_BLIND_REVIEWER_PROMPT_PHASE2_V4_1.md",
    )
    for name in names:
        raw = (FORMAL / name).read_bytes()
        text = raw.decode("utf-8", errors="strict")
        assert not raw.startswith(b"\xef\xbb\xbf")
        assert b"\r\n" not in raw
        assert re.search(r"(?<![A-Za-z])[A-Za-z]:[/\\]", text) is None
        for target in re.findall(r"(?<!!)\[[^]]+\]\(([^)]+)\)", text):
            assert (FORMAL / target.split("#", 1)[0]).resolve().exists()
