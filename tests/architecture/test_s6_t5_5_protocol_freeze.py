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

    def test_current_governance_keeps_implementation_and_experiments_closed(self) -> None:
        state = (GOVERNANCE / "current_work_state.md").read_text(encoding="utf-8")
        master_record = (GOVERNANCE / "experiment_master_record.md").read_text(
            encoding="utf-8"
        )

        for text in (state, master_record):
            for required in (
                "S6-T5.5-P1",
                "Completed, pending human acceptance",
                "S6-T5.5",
                "NOT APPROVED",
                "Formal RAG security experiment",
            ):
                with self.subTest(required=required):
                    self.assertIn(required, text)

        self.assertIn("EvidenceEnvelope implementation", state)
        self.assertIn("ContextBuilder", state)

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
                self.assertIn("citation_id", text)
                self.assertIn("S6-T5.5", text)
                self.assertIn("NOT APPROVED", text)

    def test_protocol_review_has_not_created_s6_t5_5_business_types(self) -> None:
        forbidden_definitions: list[str] = []
        for path in RETRIEVAL_ROOT.rglob("*.py"):
            module = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(module):
                if isinstance(node, ast.ClassDef) and node.name in {
                    "EvidenceEnvelope",
                    "CitationBinding",
                    "ContextBuilder",
                }:
                    forbidden_definitions.append(str(path.relative_to(ROOT)))

        self.assertEqual([], forbidden_definitions)
        self.assertFalse((RETRIEVAL_ROOT / "context" / "citation.py").exists())
        self.assertFalse((RETRIEVAL_ROOT / "context" / "rendering.py").exists())
        self.assertFalse((RETRIEVAL_ROOT / "context" / "models.py").exists())


if __name__ == "__main__":
    unittest.main()
