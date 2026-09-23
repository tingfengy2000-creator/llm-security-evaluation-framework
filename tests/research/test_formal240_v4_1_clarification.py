"""Forward-only D1 Canary V4.1 field clarification and reviewer packet gates."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "docs/research/stage6_1_hidden_knowledge_poisoning/formal240"


def _text(name: str) -> str:
    return (FORMAL / name).read_text(encoding="utf-8")


def _json(name: str) -> dict:
    return json.loads(_text(name))


def test_frozen_v4_guide_and_schema_unchanged() -> None:
    expected = {
        "PAPER1_FORMAL_ANNOTATION_GUIDE_V4.md": "7a094210dbed5e9a9054a4c6f47b6229ce85b03d15c2454c0b320b7c62f37a7c",
        "PAPER1_FORMAL_ANNOTATION_SCHEMA_V4.json": "497c1648ee7e301c329ddb37bb7ebe4153e13123dc7a0bd574b68ea2c2ea139f",
    }
    for name, digest in expected.items():
        assert hashlib.sha256((FORMAL / name).read_bytes()).hexdigest() == digest


def test_v4_1_is_additive_and_enums_unchanged() -> None:
    rules = _json("PAPER1_FORMAL_ANNOTATION_CONSISTENCY_RULES_V4_1.json")
    schema = _json("PAPER1_FORMAL_ANNOTATION_SCHEMA_V4.json")
    assert rules["enum_sets_unchanged"] is True
    assert rules["enum_changed"] is False
    assert rules["historical_raw_returns_immutable"] is True
    assert schema["phase2"]["version_claim_status"] == [
        "NOT_PRESENT", "PRESENT_CORRECT", "PRESENT_INCORRECT", "PRESENT_EVIDENCE_INSUFFICIENT"
    ]
    assert schema["phase2"]["authority_claim_status"] == [
        "NOT_PRESENT", "PRESENT_CORRECT", "PRESENT_INCORRECT", "PRESENT_EVIDENCE_INSUFFICIENT"
    ]


def test_five_field_scope_boundary_cases_frozen() -> None:
    rules = _json("PAPER1_FORMAL_ANNOTATION_CONSISTENCY_RULES_V4_1.json")
    cases = {case["id"]: case for case in rules["teaching_cases_not_dataset_answers"]}
    assert cases["PUBLICATION_ALONE"]["version_claim_status"] == "NOT_PRESENT"
    assert cases["REVISION_EFFECTIVE_TRANSITION"]["version_claim_scope"].startswith("PRESENT")
    assert cases["OPERATIONAL_ACTOR"]["authority_claim_status"] == "NOT_PRESENT"
    assert cases["ISSUER_PUBLISHER"]["authority_claim_scope"].startswith("PRESENT")
    assert cases["WRONG_REVIEWER_SESSION"]["record_level"] == "review_run_metadata / blind_review_process_QA"
    assert cases["WRONG_REVIEWER_SESSION"]["candidate_phase2_issue_change"] == "NONE_FROM_RUN_INCIDENT"
    ids = {rule["id"] for rule in rules["rules"]}
    assert len(ids) == 5
    assert "V4_1_REVIEWER_PROCESS_IS_RUN_LEVEL" in ids


def test_guide_explains_boundary_without_canary_answer_leakage() -> None:
    guide = _text("PAPER1_FORMAL_ANNOTATION_GUIDE_V4_1_CLARIFICATION.md")
    assert "publication" in guide.lower() and "version" in guide.lower()
    assert "operational" in guide.lower() and "authority" in guide.lower()
    assert "review_run_metadata" in guide
    assert "D1BR-" not in guide
    assert re.search(r"(?<![A-Z0-9])R[12](?![A-Z0-9])", guide) is None


def test_r3_r4_prompts_are_symmetric_and_blind() -> None:
    for phase in ("PHASE1", "PHASE2"):
        r3 = _text(f"PAPER1_FORMAL_D1_R3_BLIND_REVIEWER_PROMPT_{phase}_V4_1.md")
        r4 = _text(f"PAPER1_FORMAL_D1_R4_BLIND_REVIEWER_PROMPT_{phase}_V4_1.md")
        assert r3.replace("R3", "RX") == r4.replace("R4", "RX")
        for prompt in (r3, r4):
            assert "D1BR-" not in prompt
            assert re.search(r"(?<![A-Z0-9])R[12](?![A-Z0-9])", prompt) is None
            assert "Clean" not in prompt and "Poison" not in prompt
            assert "HKP" not in prompt and "S1" not in prompt
            assert "same session" in prompt if phase == "PHASE2" else "fresh, independent session" in prompt
    phase1 = _text("PAPER1_FORMAL_D1_R3_BLIND_REVIEWER_PROMPT_PHASE1_V4_1.md")
    phase2 = _text("PAPER1_FORMAL_D1_R3_BLIND_REVIEWER_PROMPT_PHASE2_V4_1.md")
    assert "PACKAGE_PHASE2_V3.json" not in phase1
    assert "GUIDE_V4_1_CLARIFICATION.md" not in phase1
    assert "PACKAGE_PHASE2_V3.json" in phase2
    assert "GUIDE_V4_1_CLARIFICATION.md" in phase2
