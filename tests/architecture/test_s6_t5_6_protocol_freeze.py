from __future__ import annotations

import ast
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GOVERNANCE = ROOT / "docs" / "governance"
RETRIEVAL_ROOT = ROOT / "src" / "llmguard" / "domains" / "retrieval"
REVIEW_RECORD = GOVERNANCE / "s6_t5_6_protocol_review_record.md"
SPECIFICATION = (
    ROOT
    / "docs"
    / "superpowers"
    / "specs"
    / "2026-07-19-s6-t5-controlled-retrieval-traceable-context-design.md"
)
PLAN = (
    ROOT
    / "docs"
    / "superpowers"
    / "plans"
    / "2026-07-19-s6-t5-controlled-retrieval-traceable-context.md"
)
ADR = ROOT / "docs" / "architecture" / "0008_retrieval_context_boundary.md"


def _section(text: str, heading: str) -> str:
    start = text.index(heading)
    next_heading = text.find("\n## ", start + len(heading))
    return text[start:] if next_heading == -1 else text[start:next_heading]


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
        plan = PLAN.read_text(encoding="utf-8")
        specification = SPECIFICATION.read_text(encoding="utf-8")

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

    def test_h2_freezes_one_active_sequential_build_order(self) -> None:
        active_sections = (
            _section(SPECIFICATION.read_text(encoding="utf-8"), "## 12."),
            _section(PLAN.read_text(encoding="utf-8"), "## 8."),
            _section(ADR.read_text(encoding="utf-8"), "### 12."),
        )
        required_order = (
            "validate `ContextBuildConfig`",
            "validate Request, citation mode and Evidence sequence types",
            "validate all Request/Evidence provenance",
            "stable sort",
            "exact UID duplicate/conflict handling",
            "apply `max_evidence_count`",
            "render the fixed citation instruction",
            "EMPTY_RETRIEVAL",
            "CONTEXT_BUDGET_EXHAUSTED",
            "sequentially for each count-selected candidate",
            "first non-fit",
            "NOT_ATTEMPTED_AFTER_BUDGET_CUTOFF",
            "assemble Trace and Package",
        )
        for active in active_sections:
            positions = [active.index(item) for item in required_order]
            self.assertEqual(positions, sorted(positions))
            self.assertNotIn("再解析正文并验证 hash，再分配 Citation ID", active)
            self.assertNotIn("resolve each remaining body", active)

    def test_h2_freezes_instruction_budget_decision_and_trace_partition(self) -> None:
        text = REVIEW_RECORD.read_text(encoding="utf-8")
        for required in (
            "S6-T5.6-P1-H2",
            "Completed, pending human review",
            "instruction_budget_not_attempted_uids",
            "NOT_ATTEMPTED_INSTRUCTION_BUDGET_EXHAUSTED",
            "len(decision_codes) == len(stable_candidate_uids)",
            "不相交划分",
            "budget_excluded_uids 长度只能为 0 或 1",
            "trace_id == \"CT-\" + trace_hash",
            "trace_id",
            "package_id",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

        active_sections = (
            _section(SPECIFICATION.read_text(encoding="utf-8"), "## 12."),
            _section(PLAN.read_text(encoding="utf-8"), "## 8."),
            _section(ADR.read_text(encoding="utf-8"), "### 12."),
        )
        for active in active_sections:
            with self.subTest(active=active[:32]):
                self.assertNotIn("validate global rank/cardinality", active)
                self.assertNotIn("future policy-filtered/subset Evidence", active)
                self.assertNotIn("len(stable_candidates) <= request.top_k", active)

    def test_h2_removes_redundant_package_trace_hash_field(self) -> None:
        text = REVIEW_RECORD.read_text(encoding="utf-8")
        package_fields = _section(text, "## 9. Future RetrievedContextPackage")
        self.assertIn("and `build_trace`", package_fields)
        self.assertIn("not a second persisted DTO field", package_fields)
        self.assertIn("context_build_trace_hash = build_trace.trace_hash", package_fields)
        self.assertIn("context_build_trace_hash", package_fields)
        self.assertNotIn(
            "and `context_build_trace_hash`, `build_trace`",
            package_fields,
        )

    def test_protocol_acceptance_keeps_implementation_separately_unapproved(self) -> None:
        state = (GOVERNANCE / "current_work_state.md").read_text(encoding="utf-8")
        master = (GOVERNANCE / "experiment_master_record.md").read_text(
            encoding="utf-8"
        )
        decisions = (GOVERNANCE / "project_owner_decision_register.md").read_text(
            encoding="utf-8"
        )
        review = REVIEW_RECORD.read_text(encoding="utf-8")

        for required in (
            "GOV-S6-T5.6-P1-ACCEPTANCE",
            "S6-T5.6-P1: HUMAN_ACCEPTED",
            "S6-T5.6-P1-H1: HUMAN_ACCEPTED",
            "S6-T5.6-P1-H2: HUMAN_ACCEPTED",
            "S6-T5.6: READY_FOR_SEPARATE_IMPLEMENTATION_APPROVAL",
            "S6-T5.6-I1: NOT YET APPROVED",
            "S6-T5.7+: NOT APPROVED",
            "Formal RAG security experiment: NOT STARTED",
            "Last accepted implementation commit: `6da27a6`",
            "Protocol acceptance closure commit: `432b07e`",
        ):
            with self.subTest(required=required):
                self.assertIn(required, state)

        for text in (master, decisions, review):
            for required in (
                "GOV-S6-T5.6-P1-ACCEPTANCE",
                "HUMAN_ACCEPTED",
                "READY_FOR_SEPARATE_IMPLEMENTATION_APPROVAL",
                "NOT YET APPROVED",
                "6da27a6",
                "432b07e",
            ):
                with self.subTest(required=required):
                    self.assertIn(required, text)

        self.assertNotIn("Last accepted implementation commit: `432b07e`", state)


if __name__ == "__main__":
    unittest.main()
