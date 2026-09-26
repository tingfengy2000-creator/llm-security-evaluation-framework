"""D1 Canary V4.2 is an additive Owner rule, not a raw-review rewrite."""

from __future__ import annotations

import hashlib
import json
import os
import re
import runpy
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "docs/research/stage6_1_hidden_knowledge_poisoning/formal240"
PREPARE = runpy.run_path(str(ROOT / "scripts/research/prepare_formal_d1_canary_v4_2.py"))


def data(name: str) -> dict:
    return json.loads((FORMAL / name).read_text(encoding="utf-8"))


def test_frozen_guides_and_schema_unchanged() -> None:
    shas = {
        "PAPER1_FORMAL_ANNOTATION_GUIDE_V4.md": "7a094210dbed5e9a9054a4c6f47b6229ce85b03d15c2454c0b320b7c62f37a7c",
        "PAPER1_FORMAL_ANNOTATION_GUIDE_V4_1_CLARIFICATION.md": "7032d2933248f9c9849e4be38065b17d7e327d1814788338d8df6d3aaa680ce2",
        "PAPER1_FORMAL_ANNOTATION_SCHEMA_V4.json": "497c1648ee7e301c329ddb37bb7ebe4153e13123dc7a0bd574b68ea2c2ea139f",
    }
    for name, expected in shas.items():
        assert hashlib.sha256((FORMAL / name).read_bytes()).hexdigest() == expected
    rules = data("PAPER1_FORMAL_ANNOTATION_CONSISTENCY_RULES_V4_2.json")
    assert rules["enum_sets_unchanged"] is True
    assert len(rules["rules"]) == 5


def test_candidate_only_scope_boundary_and_evidence_nonpropagation() -> None:
    bare_rule = PREPARE["bare_rule"]
    bare_rule("《示例培训法》第三条规定，申请人提交两份材料。")
    bare_rule("依《示例培训条例》第六条，机关应当在10日内答复。")
    with pytest.raises(AssertionError):
        bare_rule("《示例培训法》2010年修订版第三条规定，申请人提交两份材料。")
    with pytest.raises(AssertionError):
        bare_rule("《关于修改〈示例培训法〉的决定》第三条规定，自2020年施行。")
    assert "metadata" in data("PAPER1_FORMAL_ANNOTATION_CONSISTENCY_RULES_V4_2.json")["rules"][1]["if"].lower()


def test_all_15_cases_rederive_without_hidden_inputs() -> None:
    handoff_root = os.environ.get("PAPER1_HANDOFF_ROOT")
    if handoff_root is None:
        pytest.skip("Private frozen handoff root not supplied to this test environment")
    rebuilt_overlay, rebuilt_targeted = PREPARE["build"](Path(handoff_root))
    overlay = data("PAPER1_FORMAL_D1_CANARY_PHASE2_OWNER_SEMANTIC_ADJUDICATION_OVERLAY_V1.json")
    targeted = data("PAPER1_FORMAL_D1_CANARY_PHASE2_15ITEM_TARGETED_REREVIEW_PACKAGE_V1.json")
    assert rebuilt_overlay == overlay
    assert rebuilt_targeted == targeted
    assert overlay["case_counts"] == {"bare_substantive": 12, "amendment_decision": 1, "historical_comparison": 2}
    assert len(overlay["cases"]) == len(targeted["records"]) == 15
    assert len({row["blind_review_id"] for row in targeted["records"]}) == 15
    assert [row["blind_review_id"] for row in targeted["records"]] == [row["blind_review_id"] for row in overlay["cases"]]
    for case in overlay["cases"]:
        assert case["owner_semantic_value"] in {"NOT_PRESENT", "PRESENT_CORRECT", "LEGITIMATE_VERSION_OR_HISTORY"}
        assert case["decision_authority"].startswith("OWNER_GLOBAL_SEMANTIC_CLARIFICATION")
    assert overlay["historical_raw_modified"] is False
    assert overlay["candidate_or_evidence_modified"] is False


def test_blind_packet_has_only_allowed_data_and_symmetric_prompts() -> None:
    package = data("PAPER1_FORMAL_D1_CANARY_PHASE2_15ITEM_TARGETED_REREVIEW_PACKAGE_V1.json")
    for row in package["records"]:
        assert set(row) == {"blind_review_id", "candidate_text", "evidence", "target_field"}
        assert row["target_field"] in {"version_claim_status", "overall_fact_status"}
        assert [ev["evidence_selection_id"] for ev in row["evidence"]] == ["E1", "E2"]
    raw = json.dumps(package, ensure_ascii=False).lower()
    for forbidden in ("owner_semantic_value", "original_r3_value", "original_r4_value", "expected_v3", "ground_truth", "hkp", "target_s"):
        assert forbidden not in raw
    r3 = (FORMAL / "PAPER1_FORMAL_D1_R3_GPT_PHASE2_V4_2_TARGETED_PROMPT.md").read_text(encoding="utf-8")
    r4 = (FORMAL / "PAPER1_FORMAL_D1_R4_CODEX_PHASE2_V4_2_TARGETED_PROMPT.md").read_text(encoding="utf-8")
    assert r3.replace("R3-gpt", "REVIEWER").replace("R3_GPT", "REVIEWER") == r4.replace("R4-codex", "REVIEWER").replace("R4_CODEX", "REVIEWER")
    assert "15 unique IDs" in r3 and "actual file" in r3


def test_no_new_population_or_training_from_this_task() -> None:
    report = (FORMAL / "PAPER1_FORMAL_D1_CANARY_VERSION_SCOPE_REFINEMENT_REPORT_V1.md").read_text(encoding="utf-8")
    assert "not Formal Ground Truth" in report
    assert "does **not** accept the Canary" in report
    assert "Human A/B" in report and "remaining D1 40 groups" in report


def test_new_document_links_resolve() -> None:
    names = (
        "PAPER1_FORMAL_ANNOTATION_GUIDE_V4_2_VERSION_SCOPE_DECISION.md",
        "PAPER1_FORMAL_D1_CANARY_VERSION_SCOPE_REFINEMENT_REPORT_V1.md",
        "PAPER1_FORMAL_PRE_ANNOTATION_QA_POLICY_V1_2.md",
        "PAPER1_FORMAL_D1_CANARY_V4_2_DOCUMENTATION_CLOSEOUT_V1.md",
    )
    for name in names:
        path = FORMAL / name
        content = path.read_text(encoding="utf-8")
        for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", content):
            target = match.group(1)
            assert (path.parent / target).exists(), f"{name}: {target}"
