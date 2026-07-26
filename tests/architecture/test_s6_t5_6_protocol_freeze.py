from __future__ import annotations

import ast
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GOVERNANCE = ROOT / "docs" / "governance"
RETRIEVAL_ROOT = ROOT / "src" / "llmguard" / "domains" / "retrieval"
REVIEW_RECORD = GOVERNANCE / "s6_t5_6_protocol_review_record.md"


class S6T56ProtocolFreezeTests(unittest.TestCase):
    def test_protocol_record_freezes_budget_citation_and_package_boundaries(self) -> None:
        text = REVIEW_RECORD.read_text(encoding="utf-8")

        for required in (
            "S6-T5.6-P1",
            "Completed, pending human acceptance",
            "ContextBuildConfig",
            "ContextBuilder",
            "RetrievedContextPackage",
            "ContextBuildTrace",
            "Unicode code point",
            "E{included_count + 1}",
            "临时 Binding",
            "不消费 Citation ID",
            "稳定前缀选择",
            "(rank ascending, evidence_uid ascending)",
            "DUPLICATE_EVIDENCE_CONFLICT",
            "NO_EVIDENCE_AFTER_DEDUPLICATION",
            "移除",
            "EMPTY_RETRIEVAL",
            "CONTEXT_BUDGET_EXHAUSTED",
            "NO_COMPLETE_EVIDENCE_BLOCK_FITS",
            "rendered_context_hash",
            "PK-<full_sha256>",
            "S6-T5.7+",
            "NOT APPROVED",
            "NOT STARTED",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_protocol_record_keeps_context_builder_dependencies_narrow(self) -> None:
        text = REVIEW_RECORD.read_text(encoding="utf-8")

        for required in (
            "ContentResolver",
            "EvidenceEnvelopeFactory",
            "RetrievalTrace 不属于 build 必需输入",
            "不得通过 build 参数传入",
            "Ground Truth",
            "Chroma",
            "EmbeddingProvider",
            "LLM",
            "TrustAggregator",
            "RetrievalPolicy",
            "不读取 Stage 6 fixture",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_design_freeze_does_not_create_context_builder_or_package_source(self) -> None:
        owners: dict[str, list[str]] = {
            "ContextBuilder": [],
            "RetrievedContextPackage": [],
            "ContextBuildConfig": [],
            "ContextBuildTrace": [],
        }
        for path in RETRIEVAL_ROOT.rglob("*.py"):
            module = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(module):
                if isinstance(node, ast.ClassDef) and node.name in owners:
                    owners[node.name].append(str(path.relative_to(ROOT)))

        for class_name, paths in owners.items():
            with self.subTest(class_name=class_name):
                self.assertEqual([], paths)

    def test_current_governance_keeps_s6_t5_6_and_formal_experiment_closed(self) -> None:
        state = (GOVERNANCE / "current_work_state.md").read_text(encoding="utf-8")
        master = (GOVERNANCE / "experiment_master_record.md").read_text(
            encoding="utf-8"
        )

        for text in (state, master):
            for required in (
                "S6-T5.6",
                "NOT APPROVED",
                "Formal RAG security experiment",
                "NOT STARTED",
            ):
                with self.subTest(required=required):
                    self.assertIn(required, text)

    def test_h1_freezes_sequential_resolution_and_trace_identity(self) -> None:
        text = REVIEW_RECORD.read_text(encoding="utf-8")

        for required in (
            "S6-T5.6-P1-H1",
            "Completed, pending human review",
            "sequential resolution",
            "instruction 本身超过预算",
            "不得调用 ContentResolver",
            "逐条执行",
            "NOT_ATTEMPTED_AFTER_BUDGET_CUTOFF",
            "evidence.query_id == request.query_id",
            "evidence.retrieval_request_id == request.request_id",
            "evidence.collection_fingerprint == request.collection_fingerprint",
            "1 <= evidence.rank <= request.top_k",
            "相同 corpus_snapshot_id",
            "public_metadata 的深层语义值",
            "trace_schema_version",
            "count_selected_count",
            "not_attempted_after_budget_cutoff_uids",
            "trace_hash",
            "trace_id = CT-<full_sha256>",
            "context_build_trace_hash",
            "不包含 package_id",
            "NO_COMPLETE_EVIDENCE_BLOCK_FITS",
            "stable-prefix policy cannot admit the first candidate",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_h1_marks_old_reason_code_historical_and_keeps_source_absent(self) -> None:
        plan = (
            ROOT
            / "docs"
            / "superpowers"
            / "plans"
            / "2026-07-19-s6-t5-controlled-retrieval-traceable-context.md"
        ).read_text(encoding="utf-8")
        specification = (
            ROOT
            / "docs"
            / "superpowers"
            / "specs"
            / "2026-07-19-s6-t5-controlled-retrieval-traceable-context-design.md"
        ).read_text(encoding="utf-8")

        for text in (plan, specification):
            self.assertIn("removed from active baseline by S6-T5.6-P1", text)
            self.assertIn("sequential resolve", text)

        for source_name in (
            "ContextBuilder",
            "RetrievedContextPackage",
            "ContextBuildTrace",
            "ContextBuildConfig",
        ):
            with self.subTest(source_name=source_name):
                self.assertNotIn(
                    f"class {source_name}",
                    "\n".join(
                        path.read_text(encoding="utf-8")
                        for path in RETRIEVAL_ROOT.rglob("*.py")
                    ),
                )


if __name__ == "__main__":
    unittest.main()
