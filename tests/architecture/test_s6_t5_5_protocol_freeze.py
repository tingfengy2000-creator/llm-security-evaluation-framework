from __future__ import annotations

import ast
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GOVERNANCE = ROOT / "docs" / "governance"
RETRIEVAL_ROOT = ROOT / "src" / "llmguard" / "domains" / "retrieval"
REVIEW_RECORD = GOVERNANCE / "s6_t5_5_protocol_review_record.md"


class S6T55ProtocolFreezeTests(unittest.TestCase):
    def test_review_record_freezes_citation_timing_and_factory_inputs(self) -> None:
        text = REVIEW_RECORD.read_text(encoding="utf-8")

        for required in (
            "Completed, pending human acceptance",
            "S6-T5.5 NOT APPROVED",
            "`EvidenceEnvelope` **不持有** `citation_id`",
            "EvidenceEnvelopeFactory.create",
            "RetrievalEvidence",
            "ResolvedContent",
            "未来 `ContextBuilder`",
            "`E1 ... En`",
            "不使用 `None`、空字符串、`E0`",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_review_record_freezes_safe_rendering_and_export_boundaries(self) -> None:
        text = REVIEW_RECORD.read_text(encoding="utf-8")

        for required in (
            "escape_xml_text()",
            "escape_xml_attribute()",
            "CRLF/CR 转为 LF",
            "不做 Unicode normalization",
            "Escaping **只**保护结构边界",
            "deny-by-default",
            "Citation Accuracy",
            "不调用 LLM",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_h1_freezes_canonical_factory_inputs_without_legacy_mapping(self) -> None:
        text = REVIEW_RECORD.read_text(encoding="utf-8")

        for required in (
            "Factory **只接受 canonical RetrievalEvidence**",
            "scheme 必须为 `corpus`",
            "`resolved_content.canonical_content_ref`",
            "`evidence.corpus_snapshot_id`、`chunk_id`、`content_hash`",
            "`EVIDENCE_CONTENT_MISMATCH`",
            "legacy `chroma:` 只属于已验收 ContentResolver 的**输入**边界",
            "它不进入 EnvelopeFactory",
            "DocumentRecord、ChunkRecord、裸 metadata 或裸正文 str",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_h1_freezes_renderer_binding_identity_and_fail_closed_error(self) -> None:
        text = REVIEW_RECORD.read_text(encoding="utf-8")

        for required in (
            "def render_evidence_block(",
            "envelope: EvidenceEnvelope",
            "binding: CitationBinding",
            "`evidence_uid`、`chunk_id`、`parent_doc_id`、`content_hash`、`source_id`、`version`、`rank`",
            "`CITATION_BINDING_MISMATCH`",
            "citation binding does not match evidence",
            "不返回\npartial/empty block、不跳过后继续、不重编号掩盖错误，也不解释为 abstention",
            "S6-T5.6 ContextBuilder",
            "才可实际执行 Citation allocation、创建 Binding",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_current_governance_records_i1_h1_and_parent_as_human_accepted(self) -> None:
        state = (GOVERNANCE / "current_work_state.md").read_text(encoding="utf-8")
        master_record = (GOVERNANCE / "experiment_master_record.md").read_text(
            encoding="utf-8"
        )

        for text in (state, master_record):
            for required in (
                "S6-T5.5-P1",
                "HUMAN_ACCEPTED",
                "S6-T5.5",
                "Formal RAG security experiment",
            ):
                with self.subTest(required=required):
                    self.assertIn(required, text)

        self.assertIn("EvidenceEnvelope", state)
        self.assertIn("ContextBuilder", state)
        self.assertIn("S6-T5.5-P1-H1", state)
        self.assertIn("S6-T5.5-I1: **HUMAN_ACCEPTED**", state)
        self.assertIn("S6-T5.5-H1: **HUMAN_ACCEPTED**", state)
        self.assertIn("S6-T5.5: **HUMAN_ACCEPTED**", state)
        self.assertIn("Last accepted implementation commit: `6da27a6`", state)
        self.assertIn("S6-T5.6-P1", state)
        self.assertIn("S6-T5.7+", state)
        self.assertIn("S6-T5.6-I1: Completed, pending human acceptance", state)

    def test_acceptance_preserves_protocol_history_without_claiming_implementation(self) -> None:
        review = REVIEW_RECORD.read_text(encoding="utf-8")
        register = (GOVERNANCE / "project_owner_decision_register.md").read_text(
            encoding="utf-8"
        )

        for text in (review, register):
            for required in (
                "S6-T5.5-P1",
                "S6-T5.5-P1-H1",
                "HUMAN_ACCEPTED",
                "READY_FOR_SEPARATE_IMPLEMENTATION_APPROVAL",
                "NOT YET APPROVED",
                "11a72f7",
                "25fb83d",
            ):
                with self.subTest(required=required):
                    self.assertIn(required, text)

        self.assertIn("不创建或验证", review)
        self.assertIn("历史 pending/review 快照", review)
        self.assertIn("全仓 secret-shape", review)

    def test_s6_t5_4_acceptance_remains_intact(self) -> None:
        state = (GOVERNANCE / "current_work_state.md").read_text(encoding="utf-8")

        for required in (
            "S6-T5.4-P1: **HUMAN_ACCEPTED**",
            "S6-T5.4-I1: **HUMAN_ACCEPTED**",
            "S6-T5.4-H1: **HUMAN_ACCEPTED**",
            "S6-T5.4: **HUMAN_ACCEPTED**",
        ):
            with self.subTest(required=required):
                self.assertIn(required, state)

    def test_canonical_governance_entrypoints_record_the_same_p1_boundary(self) -> None:
        paths = (
            ROOT / "PROJECT_MASTER_CONTEXT.md",
            GOVERNANCE / "project_owner_decision_register.md",
            ROOT / "stages" / "stage6_rag_security" / "README.md",
        )
        for path in paths:
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertIn("S6-T5.5-P1", text)
                self.assertIn("S6-T5.5", text)
                self.assertIn("human_accepted", text.lower())
                expected_not_approved = (
                    "not_approved"
                    if path.name == "README.md"
                    else "NOT APPROVED"
                )
                self.assertIn(expected_not_approved, text)

    def test_canonical_governance_entrypoints_record_h1_and_i1_boundary(
        self,
    ) -> None:
        paths = (
            ROOT / "PROJECT_MASTER_CONTEXT.md",
            GOVERNANCE / "project_owner_decision_register.md",
            ROOT / "stages" / "stage6_rag_security" / "README.md",
        )
        for path in paths:
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertIn("S6-T5.5-P1-H1", text)
                self.assertIn("canonical", text)
                self.assertIn("CITATION_BINDING_MISMATCH", text)
                self.assertIn("S6-T5.5-I1", text)
                expected_not_approved = (
                    "not_approved"
                    if path.name == "README.md"
                    else "NOT APPROVED"
                )
                self.assertIn(expected_not_approved, text)

    def test_i1_keeps_dtos_in_contracts_and_context_builder_protocol_canonical(self) -> None:
        owners: dict[str, list[str]] = {
            "EvidenceEnvelope": [],
            "CitationBinding": [],
            "ContextBuilder": [],
        }
        for path in RETRIEVAL_ROOT.rglob("*.py"):
            module = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(module):
                if isinstance(node, ast.ClassDef) and node.name in owners:
                    owners[node.name].append(str(path.relative_to(ROOT)))

        assert owners["EvidenceEnvelope"] == [
            "src\\llmguard\\domains\\retrieval\\contracts\\evidence_envelope.py"
        ]
        assert owners["CitationBinding"] == [
            "src\\llmguard\\domains\\retrieval\\contracts\\evidence_envelope.py"
        ]
        assert owners["ContextBuilder"] == [
            "src\\llmguard\\domains\\retrieval\\context\\protocols.py"
        ]
        self.assertFalse((RETRIEVAL_ROOT / "context" / "models.py").exists())

    def test_i1_h1_acceptance_preserves_additive_contract_hardening_history(self) -> None:
        state = (GOVERNANCE / "current_work_state.md").read_text(encoding="utf-8")
        review = REVIEW_RECORD.read_text(encoding="utf-8")
        completion = (GOVERNANCE / "s6_t5_5_completion_record.md").read_text(
            encoding="utf-8"
        )

        for required in (
            "Last accepted stage task: `S6-T5.6 Context Package Protocol`",
            "S6-T5.5-H1: **HUMAN_ACCEPTED**",
            "S6-T5.5-I1: **HUMAN_ACCEPTED**",
            "S6-T5.5: **HUMAN_ACCEPTED**",
            "Last accepted implementation commit: `6da27a6`",
            "S6-T5.6: Completed, pending human acceptance",
            "S6-T5.6-I1: Completed, pending human acceptance",
            "S6-T5.7+: NOT APPROVED",
            "Formal RAG security experiment: NOT STARTED",
        ):
            with self.subTest(required=required):
                self.assertIn(required, state)

        for required in (
            "INVALID_CITATION_BINDING",
            "citation binding is invalid",
            "EV-[0-9a-f]{64}",
            "metadata wrapper",
            "31 passed, 1527 subtests passed",
            "41 passed, 1595 subtests passed",
            "2cacef7",
            "6da27a6",
            "HUMAN_ACCEPTED",
        ):
            with self.subTest(required=required):
                self.assertIn(required, review + completion)


    def test_acceptance_record_keeps_later_capabilities_and_formal_experiment_closed(
        self,
    ) -> None:
        state = (GOVERNANCE / "current_work_state.md").read_text(encoding="utf-8")
        register = (GOVERNANCE / "project_owner_decision_register.md").read_text(
            encoding="utf-8"
        )
        master = (GOVERNANCE / "experiment_master_record.md").read_text(
            encoding="utf-8"
        )

        for text in (state, register, master):
            for required in (
                "S6-T5.5-I1",
                "S6-T5.5-H1",
                "S6-T5.5",
                "HUMAN_ACCEPTED",
                "S6-T5.6",
                "NOT APPROVED",
            ):
                with self.subTest(required=required):
                    self.assertIn(required, text)

        self.assertIn("PODR-022", register)
        self.assertIn("2cacef7", register)
        self.assertIn("6da27a6", register)
        self.assertIn("ENGINEERING_VALIDATED_HUMAN_ACCEPTED", master)
        self.assertIn("Formal RAG security experiment: NOT STARTED", state)
        self.assertIn("Formal RAG security experiment", register)
        self.assertIn("NOT STARTED", register)
        self.assertIn("Formal RAG security experiment", master)
        self.assertIn("NOT STARTED", master)


if __name__ == "__main__":
    unittest.main()
