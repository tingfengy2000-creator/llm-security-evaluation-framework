"""Bounded contract checks for the Formal240 D1 90-row Phase1 release."""

from __future__ import annotations

import sys
import re
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

from formal240_d1_remaining90_phase1_package import opaque_id, prompt, shuffled  # noqa: E402


def synthetic_rows() -> list[dict[str, str]]:
    return [
        {"sample_id": f"sample-{g}-{r}", "group_slot_id": f"group-{g}", "hkp": f"HKP{2 + (g % 3)}"}
        for g in range(30)
        for r in range(3)
    ]


def test_blind_ids_stable_and_distinct() -> None:
    ids = [opaque_id(row["sample_id"]) for row in synthetic_rows()]
    assert len(ids) == len(set(ids)) == 90
    assert all(value.startswith("D1BR-") for value in ids)
    assert opaque_id("sample-1-0") == opaque_id("sample-1-0")


def test_shuffles_are_cross_group_and_not_hkp_blocked() -> None:
    rows = synthetic_rows()
    first = shuffled(rows, 2026092701)
    second = shuffled(rows, 2026092702)
    assert {r["sample_id"] for r in first} == {r["sample_id"] for r in rows}
    assert {r["sample_id"] for r in second} == {r["sample_id"] for r in rows}
    assert [r["sample_id"] for r in first] != [r["sample_id"] for r in second]
    for ordered in (first, second):
        assert all(ordered[i]["group_slot_id"] != ordered[i + 1]["group_slot_id"] for i in range(89))
        assert all(len({ordered[i + j]["hkp"] for j in range(3)}) > 1 for i in range(88))


def test_r4_prompt_requires_fresh_projectless_and_no_phase2() -> None:
    text = prompt("R4", "packet.json", "schema.json", "return.json")
    assert "NEW projectless Codex task" in text
    assert "not a new Codex Project" in text
    assert "Do not view Phase2" in text
    assert "array of exactly 90 objects" in text


def test_r3_prompt_requires_fresh_independent_session() -> None:
    text = prompt("R3", "packet.json", "schema.json", "return.json")
    assert "fresh, independent GPT session" in text
    assert "Do not browse the web" in text
    assert "same isolated session" in text.lower()


def test_task_documentation_relative_links_resolve() -> None:
    root = Path(__file__).resolve().parents[2]
    files = [
        root / "PROJECT_MASTER_CONTEXT.md",
        root / "docs/governance/current_work_state.md",
        root / "docs/governance/experiment_master_record.md",
        root / "docs/governance/research_execution_log.md",
        root / "docs/research/stage6_1_hidden_knowledge_poisoning/README.md",
        root / "docs/research/stage6_1_hidden_knowledge_poisoning/human/experiment_ledger_tingfeng.md",
        root / "docs/research/stage6_1_hidden_knowledge_poisoning/agent/experiment_ledger_agentUse.md",
        root / "docs/research/stage6_1_hidden_knowledge_poisoning/stage_process/S6.1-P1_work_process.md",
        *sorted((root / "docs/research/stage6_1_hidden_knowledge_poisoning/formal240").glob("PAPER1_FORMAL_D1_REMAINING90_PHASE1_*.md")),
    ]
    for path in files:
        text = path.read_text(encoding="utf-8")
        for target in re.findall(r"\]\(([^)]+)\)", text):
            if target.startswith(("http:", "https:", "#", "mailto:")):
                continue
            assert (path.parent / target).exists(), f"{path}: {target}"
