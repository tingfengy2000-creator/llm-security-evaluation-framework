from __future__ import annotations

import ast
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GOVERNANCE = ROOT / "docs" / "governance"
SPEC = (
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
BLOCKER = GOVERNANCE / "s6_t5_4_protocol_blocker_record.md"
DECISION_REGISTER = GOVERNANCE / "project_owner_decision_register.md"
STATE = GOVERNANCE / "current_work_state.md"
README = ROOT / "stages" / "stage6_rag_security" / "README.md"
CONTEXT_ROOT = ROOT / "src" / "llmguard" / "domains" / "retrieval" / "context"
RETRIEVAL_ROOT = ROOT / "src" / "llmguard" / "domains" / "retrieval"


class S6T54ProtocolFreezeTests(unittest.TestCase):
    def test_protocol_freeze_records_the_only_stable_contract_owners(self) -> None:
        combined = "\n".join(
            path.read_text(encoding="utf-8") for path in (SPEC, PLAN, ADR)
        )

        for required in (
            "S6-T5.4-P1",
            "ContentResolver",
            "ResolvedContent",
            "src/llmguard/domains/retrieval/contracts/",
            "CorpusSnapshotReader",
            "ApprovedCorpusSnapshotRegistry",
            "LegacyContentRefAdapter",
            "exact-match allowlist",
            "mapping_hash",
            "contracts/errors.py",
            "ContentResolutionLookupError",
            "ContentResolutionIntegrityError",
            "ContentResolutionRuntimeError",
        ):
            with self.subTest(required=required):
                self.assertIn(required, combined)

        self.assertIn("content_ref: ContentRef", combined)
        self.assertIn("expected_content_hash: str", combined)
        self.assertIn(") -> ResolvedContent", combined)

    def test_freeze_preserves_minimum_permission_and_no_fallback_rules(self) -> None:
        spec = SPEC.read_text(encoding="utf-8")
        for required in (
            "只允许按 chunk ID 读取正文",
            "不提供 corpus 枚举、路径、metadata、标签或 Ground Truth",
            "不根据 doc_id/source_id/文件名/路径推导",
            "不允许任何 fallback",
            "不访问 Chroma",
            "短生命周期、进程内正文权限对象",
            "不得缓存、持久化或作为公共数据对象传播",
            "不提供普通正文序列化或 sensitive artifact export",
        ):
            with self.subTest(required=required):
                self.assertIn(required, spec)

    def test_human_acceptance_resolves_blocker_without_approving_implementation(
        self,
    ) -> None:
        blocker = BLOCKER.read_text(encoding="utf-8")
        state = STATE.read_text(encoding="utf-8")
        readme = README.read_text(encoding="utf-8")

        for required in (
            "GOV-S6-T5.4-P1-ACCEPTANCE",
            "S6-T5.4-P1: **HUMAN_ACCEPTED**",
            "RESOLVED_BY_APPROVED_PROTOCOL_FREEZE",
            "READY_FOR_SEPARATE_IMPLEMENTATION_APPROVAL",
            "S6-T5.4-I1",
            "NOT YET APPROVED",
            "S6-T5.5",
            "Formal RAG security experiment: **Not started**",
        ):
            with self.subTest(required=required):
                self.assertIn(required, state)

        for required in (
            "## 1. 发现背景",
            "## 2. 缺失的冻结契约",
            "## 3. 正确处置",
            "RESOLVED_BY_APPROVED_PROTOCOL_FREEZE",
        ):
            with self.subTest(required=required):
                self.assertIn(required, blocker)

        self.assertNotIn("四项协议尚未冻结", state)
        self.assertNotRegex(state, r"S6-T5\.3[^\n]*pending")
        self.assertIn("s6_t5_4_p1_status: `human_accepted`", readme)
        self.assertIn(
            "s6_t5_4_status: `ready_for_separate_implementation_approval`", readme
        )

    def test_context_package_cannot_own_a_stable_dto_copy(self) -> None:
        self.assertFalse(CONTEXT_ROOT.exists())
        for path in RETRIEVAL_ROOT.rglob("*.py"):
            module = ast.parse(path.read_text(encoding="utf-8"))
            defined = {
                node.name
                for node in module.body
                if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))
            }
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertNotIn("ResolvedContent", defined)

    def test_owner_decision_register_preserves_p1_freeze(self) -> None:
        register = DECISION_REGISTER.read_text(encoding="utf-8")
        self.assertIn("PODR-013", register)
        self.assertIn("PODR-014", register)
        self.assertIn("S6-T5.4-P1", register)
        self.assertIn("Content Resolution Contract and Permission Boundary Freeze", register)
        self.assertIn("RESOLVED_BY_APPROVED_PROTOCOL_FREEZE", register)


if __name__ == "__main__":
    unittest.main()
