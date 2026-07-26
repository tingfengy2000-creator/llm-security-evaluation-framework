from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GOVERNANCE = ROOT / "docs" / "governance"
DECISION_REGISTER = GOVERNANCE / "project_owner_decision_register.md"
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
S6_T5_4_BLOCKER = GOVERNANCE / "s6_t5_4_protocol_blocker_record.md"
S6_T5_BASELINE_REPORT = GOVERNANCE / "s6_t5_baseline_acceptance_report.md"


class ContextPersistenceTests(unittest.TestCase):
    def test_canonical_context_files_exist(self) -> None:
        required = (
            ROOT / "AGENTS.md",
            GOVERNANCE / "long_term_research_requirements.md",
            DECISION_REGISTER,
            ROOT / "PROJECT_MASTER_CONTEXT.md",
            GOVERNANCE / "current_work_state.md",
            GOVERNANCE / "context_recovery_protocol.md",
            S6_T5_BASELINE_REPORT,
        )

        for path in required:
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertTrue(path.is_file())

    def test_agents_points_to_authoritative_context_and_protocols(self) -> None:
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        references = (
            "docs/governance/long_term_research_requirements.md",
            "docs/governance/project_owner_decision_register.md",
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

    def test_s6_t5_baseline_report_preserves_candidate_status_and_boundaries(
        self,
    ) -> None:
        report = S6_T5_BASELINE_REPORT.read_text(encoding="utf-8")
        state = (GOVERNANCE / "current_work_state.md").read_text(encoding="utf-8")

        for required in (
            "S6-T5 Controlled Retrieval and Traceable Context Baseline Acceptance Report",
            "Completed, pending human acceptance",
            "b136ee2",
            "b6cedf3",
            "c1e8c16",
            "PENDING_GIT_COMMIT",
            "BLK-HIST-001",
            "Stage 6.1 formal research: NOT APPROVED",
            "Formal RAG security experiment: NOT STARTED",
            "accepted S6-T5 baseline SHA",
            "不创建 tag、分支或 Stage 6.1 任务",
        ):
            with self.subTest(required=required):
                self.assertIn(required, report)

        self.assertIn("S6-T5.8: **Completed, pending human acceptance**", state)
        self.assertIn("Stage 6.1 formal research: NOT APPROVED", state)
        self.assertIn("PENDING_GIT_COMMIT", state)

    def test_project_owner_decision_register_preserves_current_and_historical_facts(
        self,
    ) -> None:
        register = DECISION_REGISTER.read_text(encoding="utf-8")

        for required in (
            "Project Owner Confirmed Requirements and Decision Register",
            "long_term_research_requirements.md",
            "PROJECT_MASTER_CONTEXT.md",
            "current_work_state.md",
            "experiment_master_record.md",
            "PODR-001",
            "PODR-011",
            "LLMGuard Research Framework",
            "llmguard",
            "codeguarder",
            "Stage 1–5",
            "RAG Security Research",
            "LLM Security Evaluation Platform",
            "AI Guard Engineering",
            "Agent Security Extension",
            "Stage 6.1 Hidden Knowledge Poisoning Detection",
            "Stage 6.2 Multi-Evidence Trustworthy Retrieval",
            "Stage 7",
            "不属于论文二",
            "《面向检索增强生成系统的隐蔽知识污染检测与多证据可信检索关键技术研究》",
            "RetrievedContextPackage",
            "TrustedContextPackage",
            "GOV-ER1",
            "S6-T5.2",
            "parent_doc_id",
            "ChunkRecord.parent_doc_id",
            "VectorDocument.metadata[\"parent_doc_id\"]",
            "VectorSearchHit.metadata[\"parent_doc_id\"]",
            "RetrievalEvidence.parent_doc_id",
            "schema `1.0`",
            "schema `1.1`",
            "RESOLVED_BY_VERSIONED_PUBLIC_METADATA_CONTRACT",
            "2ad3d9c",
            "bfc329b",
            "3c22615",
            "Completed, pending human acceptance",
            "Not approved",
        ):
            with self.subTest(required=required):
                self.assertIn(required, register)

        for forbidden_label in (
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
        ):
            with self.subTest(forbidden_label=forbidden_label):
                self.assertIn(forbidden_label, register)

        self.assertIn("历史快照", register)
        self.assertIn(
            "不得把“S6-T5.3 已批准但阻塞、未实现 DenseRetriever”写成当前状态",
            register,
        )

    def test_context_entrypoints_reference_decision_register(self) -> None:
        references = (
            (ROOT / "AGENTS.md", "docs/governance/project_owner_decision_register.md"),
            (
                GOVERNANCE / "context_recovery_protocol.md",
                "docs/governance/project_owner_decision_register.md",
            ),
            (
                ROOT / "PROJECT_MASTER_CONTEXT.md",
                "docs/governance/project_owner_decision_register.md",
            ),
        )

        for path, required_reference in references:
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertIn(required_reference, text)

    def test_decision_register_is_safe_for_repository_persistence(self) -> None:
        text = DECISION_REGISTER.read_text(encoding="utf-8")
        self.assertIsNone(WINDOWS_ABSOLUTE_PATH.search(text))
        self.assertNotRegex(text, r"(?i)(?:gsk_|sk-|bearer\s+|groq_api_key|openai_api_key)")

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

    def test_current_state_records_owner_acceptance_of_dense_retriever(self) -> None:
        state = (GOVERNANCE / "current_work_state.md").read_text(encoding="utf-8")

        for required in (
            "Last accepted implementation stage task: `S6-T5.6 Deterministic Context Package Implementation`",
            "Last accepted integration-validation task: `S6-T5.7 Controlled Retrieval Context Pipeline Integration`",
            "Last accepted implementation commit: `b136ee2`",
            "Last accepted integration evidence commit: `b6cedf3`",
            "Retrieval Runtime Contracts and IDs",
            "GOV-ER1: **HUMAN_ACCEPTED**",
            "GOV-ER1-H1: **HUMAN_ACCEPTED**",
            "S6-T5.2 `Retrieval Runtime Contracts and IDs`: **HUMAN_ACCEPTED**",
            "GOV-PODR1: **HUMAN_ACCEPTED**",
            "S6-T5.3-P1: **HUMAN_ACCEPTED**",
            "S6-T5.3: **HUMAN_ACCEPTED**",
            "S6-T5.3-H1: **HUMAN_ACCEPTED**",
            "S6-T5.4-P1: **HUMAN_ACCEPTED**",
            "S6-T5.4: **HUMAN_ACCEPTED**",
            "S6-T5.4-I1: **HUMAN_ACCEPTED**",
            "S6-T5.4-H1: **HUMAN_ACCEPTED**",
            "`S6-T5.5-I1`, `S6-T5.5-H1` and parent `S6-T5.5` are **HUMAN_ACCEPTED**",
            "S6-T5.5-I1: **HUMAN_ACCEPTED**",
            "S6-T5.5-H1: **HUMAN_ACCEPTED**",
            "S6-T5.5: **HUMAN_ACCEPTED**",
            "S6-T5.6: HUMAN_ACCEPTED",
            "S6-T5.6-I1: HUMAN_ACCEPTED",
            "S6-T5.6-I1-H1: HUMAN_ACCEPTED",
            "S6-T5.7: **HUMAN_ACCEPTED**",
            "S6-T5.8: **Completed, pending human acceptance**",
            "Formal RAG security experiment: NOT STARTED",
            "S6-T5.3 DenseRetriever",
        ):
            with self.subTest(required=required):
                self.assertIn(required, state)
        for forbidden_start in ("ContentResolver", "Trust", "LLM", "Groq"):
            with self.subTest(forbidden_start=forbidden_start):
                self.assertIn(forbidden_start, state)

    def test_s6_t5_4_protocol_blocker_preserves_history_after_resolution(self) -> None:
        state = (GOVERNANCE / "current_work_state.md").read_text(encoding="utf-8")
        blocker = S6_T5_4_BLOCKER.read_text(encoding="utf-8")

        self.assertTrue(S6_T5_4_BLOCKER.is_file())
        for required in (
            "S6-T5.4",
            "RESOLVED_BY_APPROVED_PROTOCOL_FREEZE",
            "S6-T5.4-I1: **HUMAN_ACCEPTED**",
            "S6-T5.4-H1: **HUMAN_ACCEPTED**",
            "S6-T5.5",
            "Formal RAG security experiment: NOT STARTED",
        ):
            with self.subTest(required=required):
                self.assertIn(required, state)

        for required in (
            "Resolver Protocol 的准确返回类型",
            "corpus snapshot 的受控读取接口",
            "legacy `chroma:` fixture 到 corpus 的唯一映射",
            "错误分类的归属",
            "不创建 `src/llmguard/domains/retrieval/context/`",
            "RESOLVED_BY_APPROVED_PROTOCOL_FREEZE",
        ):
            with self.subTest(required=required):
                self.assertIn(required, blocker)

    def test_stage6_readme_top_metadata_tracks_accepted_protocol_and_unapproved_implementation(
        self,
    ) -> None:
        readme = (ROOT / "stages" / "stage6_rag_security" / "README.md").read_text(
            encoding="utf-8"
        )

        for required in (
            "s6_t5_3_dense_retriever_human_accepted",
            "s6_t5_3_h1_human_accepted",
            "s6_t5_4_status: `human_accepted`",
            "s6_t5_4_p1_status: `human_accepted`",
            "s6_t5_4_i1_status: `human_accepted`",
            "s6_t5_4_h1_status: `human_accepted`",
        ):
            with self.subTest(required=required):
                self.assertIn(required, readme)

        self.assertNotIn("s6_t5_3_dense_retriever_completed_pending_human_acceptance", readme)
        self.assertNotIn("s6_t5_3_h1_completed_pending_human_review", readme)

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
        self.assertIn("S6-T5.2", state)
        self.assertIn("S6-T5.3 DenseRetriever", state)

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
        self.assertIn("S6-T5.2", state)
        self.assertIn("**HUMAN_ACCEPTED**", state)
        self.assertIn("`S6-T5.5-P1`", state)
        self.assertTrue(
            (GOVERNANCE / "s6_t5_4_completion_record.md").is_file(),
        )

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
            DECISION_REGISTER,
            GOVERNANCE / "current_work_state.md",
            GOVERNANCE / "context_recovery_protocol.md",
        )

        for path in paths:
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertIsNone(WINDOWS_ABSOLUTE_PATH.search(text))


if __name__ == "__main__":
    unittest.main()
