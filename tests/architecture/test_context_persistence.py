from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GOVERNANCE = ROOT / "docs" / "governance"
WINDOWS_ABSOLUTE_PATH = re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/]")


class ContextPersistenceTests(unittest.TestCase):
    def test_canonical_context_files_exist(self) -> None:
        required = (
            ROOT / "AGENTS.md",
            GOVERNANCE / "long_term_research_requirements.md",
            ROOT / "PROJECT_MASTER_CONTEXT.md",
            GOVERNANCE / "current_work_state.md",
            GOVERNANCE / "context_recovery_protocol.md",
        )

        for path in required:
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertTrue(path.is_file())

    def test_agents_points_to_authoritative_context_and_protocols(self) -> None:
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        references = (
            "docs/governance/long_term_research_requirements.md",
            "PROJECT_MASTER_CONTEXT.md",
            "docs/governance/current_work_state.md",
            "docs/governance/context_recovery_protocol.md",
        )

        for reference in references:
            with self.subTest(reference=reference):
                self.assertIn(reference, agents)
        self.assertIn("Mandatory Startup Protocol", agents)
        self.assertIn("Completion Protocol", agents)
        self.assertIn("Stage 1–5", agents)
        self.assertIn("不可变", agents)
        self.assertIn("Label Isolation", agents)
        self.assertIn("Approval Gate", agents)
        self.assertIn("未获批准", agents)

    def test_agents_contains_all_runtime_label_isolation_terms(self) -> None:
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        forbidden_labels = (
            "poisoned",
            "poison_label",
            "label",
            "attack_id",
            "attack_goal",
            "attack_category",
            "expected_answer",
            "expected_behavior",
            "failure_type",
            "ground_truth",
            "oracle",
            "risk_goal",
            "stealth_level",
        )

        for label in forbidden_labels:
            with self.subTest(label=label):
                self.assertIn(label, agents)

    def test_current_state_keeps_s6_t5_behind_approval_gate(self) -> None:
        state = (GOVERNANCE / "current_work_state.md").read_text(encoding="utf-8")

        self.assertIn("S6-T5 Design Freeze", state)
        self.assertIn("S6-T5 implementation: Not started", state)
        self.assertIn("Approved now", state)
        self.assertIn("Not approved now", state)
        for forbidden_start in ("Trust", "LLM", "Groq"):
            with self.subTest(forbidden_start=forbidden_start):
                self.assertIn(forbidden_start, state)

    def test_long_term_requirements_keep_mandatory_research_capabilities(self) -> None:
        requirements = (
            GOVERNANCE / "long_term_research_requirements.md"
        ).read_text(encoding="utf-8")
        required_terms = (
            "Citation Accuracy",
            "abstention_required",
            "fixed token window",
            "overlap",
            "sentence",
            "semantic",
            "BM25",
            "Hybrid",
            "reranker",
            "Stage 7",
            "Tool Injection",
            "Memory Poisoning",
            "Planning Manipulation",
            "Ground Truth",
            "CCF",
        )

        casefolded = requirements.casefold()
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term.casefold(), casefolded)

    def test_no_duplicate_long_term_requirement_sources_are_created(self) -> None:
        forbidden_duplicates = (
            GOVERNANCE / "research_requirements_memory.md",
            GOVERNANCE / "long_term_requirements.md",
            GOVERNANCE / "project_memory.md",
        )

        for path in forbidden_duplicates:
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertFalse(path.exists())

    def test_new_context_files_do_not_persist_absolute_windows_paths(self) -> None:
        paths = (
            ROOT / "AGENTS.md",
            GOVERNANCE / "current_work_state.md",
            GOVERNANCE / "context_recovery_protocol.md",
        )

        for path in paths:
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertIsNone(WINDOWS_ABSOLUTE_PATH.search(text))


if __name__ == "__main__":
    unittest.main()
