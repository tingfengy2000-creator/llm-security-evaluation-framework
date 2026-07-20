from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GOVERNANCE = ROOT / "docs" / "governance"
WINDOWS_ABSOLUTE_PATH = re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/]")
S6_T5_SPEC = (
    ROOT
    / "docs"
    / "superpowers"
    / "specs"
    / "2026-07-19-s6-t5-controlled-retrieval-traceable-context-design.md"
)
S6_T5_PLAN = (
    ROOT
    / "docs"
    / "superpowers"
    / "plans"
    / "2026-07-19-s6-t5-controlled-retrieval-traceable-context.md"
)
S6_T5_ADR = ROOT / "docs" / "architecture" / "0008_retrieval_context_boundary.md"


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

    def test_current_state_keeps_s6_t5_hardening_behind_second_approval_gate(self) -> None:
        state = (GOVERNANCE / "current_work_state.md").read_text(encoding="utf-8")

        self.assertIn("S6-T5 Design Hardening", state)
        self.assertIn("S6-T5 implementation: Not started", state)
        self.assertIn("S6-T5.1 implementation: Not approved", state)
        self.assertIn("Completed, pending second human review", state)
        self.assertIn("Approved now", state)
        self.assertIn("Not approved now", state)
        for forbidden_start in ("Trust", "LLM", "Groq"):
            with self.subTest(forbidden_start=forbidden_start):
                self.assertIn(forbidden_start, state)

    def test_current_state_records_s6_t5_1_hardening_without_approving_s6_t5_2(self) -> None:
        state = (GOVERNANCE / "current_work_state.md").read_text(encoding="utf-8")

        for required_term in (
            "S6-T5.1 Implementation Hardening",
            "Completed, pending final human acceptance",
            "S6-T5.1 implementation: `Completed and hardened`",
            "S6-T5.2 implementation: `Not approved`",
            "Final human review of S6-T5.1 deterministic contracts",
        ):
            with self.subTest(required_term=required_term):
                self.assertIn(required_term, state)

    def test_s6_t5_design_freeze_is_unique_and_behind_approval_gate(self) -> None:
        for path in (S6_T5_SPEC, S6_T5_PLAN, S6_T5_ADR):
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertTrue(path.is_file())

        self.assertEqual(
            [S6_T5_SPEC],
            sorted(S6_T5_SPEC.parent.glob("*s6-t5-controlled-retrieval*design.md")),
        )
        self.assertEqual(
            [S6_T5_PLAN],
            sorted(S6_T5_PLAN.parent.glob("*s6-t5-controlled-retrieval*.md")),
        )

        combined_design = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (S6_T5_SPEC, S6_T5_PLAN, S6_T5_ADR)
        )
        for required_boundary in (
            "RetrievedContextPackage",
            "TrustedContextPackage",
            "Evidence UID",
            "Citation ID",
            "ContentRef",
            "Ground Truth",
            "不得实现",
        ):
            with self.subTest(required_boundary=required_boundary):
                self.assertIn(required_boundary, combined_design)

        state = (GOVERNANCE / "current_work_state.md").read_text(encoding="utf-8")
        self.assertIn("Completed, pending second human review", state)
        self.assertIn("S6-T5 implementation: Not started", state)
        self.assertIn("S6-T5.1 implementation: Not approved", state)

    def test_s6_t5_hardening_keeps_one_contract_path_and_second_review_gate(self) -> None:
        spec = S6_T5_SPEC.read_text(encoding="utf-8")
        plan = S6_T5_PLAN.read_text(encoding="utf-8")
        adr = S6_T5_ADR.read_text(encoding="utf-8")
        state = (GOVERNANCE / "current_work_state.md").read_text(encoding="utf-8")

        for required_term in (
            "Existing Contract Migration Matrix",
            "RetrieverQueryRecord",
            "safe projection",
            "ContentRef",
            "legacy `chroma:`",
            "to_audit_dict()",
            "sensitive artifact",
            "CONTENT_HASH_MISMATCH",
            "EMPTY_RETRIEVAL",
            "Unicode code point",
            "LF",
        ):
            with self.subTest(required_term=required_term):
                self.assertIn(required_term, spec)

        self.assertIn(
            "不得在 retrieval/models.py 建立第二个 RetrievalEvidence",
            " ".join(plan.split()),
        )
        self.assertIn("safe projection", adr)
        self.assertIn("S6-T5 Design Hardening", state)
        self.assertIn("Completed, pending second human review", state)
        self.assertIn("S6-T5.1 implementation: Not approved", state)

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
