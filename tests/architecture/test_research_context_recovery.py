from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GOVERNANCE = ROOT / "docs" / "governance"
RESEARCH = ROOT / "docs" / "research" / "stage6_1_hidden_knowledge_poisoning"
LEARNING = ROOT / "docs" / "learning"

AUTHORITY_MAP = GOVERNANCE / "context_authority_map.md"
EXECUTION_LOG = GOVERNANCE / "research_execution_log.md"
DUAL_MACHINE_POLICY = GOVERNANCE / "dual_machine_execution_policy.md"
DECISION_REGISTER = GOVERNANCE / "project_owner_decision_register.md"
CURRENT_STATE = GOVERNANCE / "current_work_state.md"
MASTER_RECORD = GOVERNANCE / "experiment_master_record.md"
PAPER1_ROUTE = RESEARCH / "paper1_research_route.md"
R0_PROTOCOL = RESEARCH / "s6_1_r0_reproduction_preflight.md"
BENCHMARK_MATRIX = RESEARCH / "paper1_benchmark_alignment_matrix.md"
BASELINE_PROTOCOL = RESEARCH / "baseline_reproduction_protocol.md"
ARTIFACT_REGISTRY = RESEARCH / "external_artifact_registry.md"
R0_I_REVIEW = RESEARCH / "s6_1_r0_i_control_plane_review.md"
FU1_RESOLUTION = RESEARCH / "s6_1_r0_fu1_targeted_resolution.md"
LONG_TERM_REQUIREMENTS = GOVERNANCE / "long_term_research_requirements.md"

WINDOWS_ABSOLUTE_PATH = re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/]")
AUTHORITY_LEVEL = re.compile(r"^## L(?P<level>[0-9]) — ", re.MULTILINE)

ROUTE_SECTIONS = (
    "Working Title",
    "Research Problem",
    "Motivation",
    "Research Gap",
    "Threat Model",
    "External Baselines",
    "External Benchmark Track",
    "Versioned Chinese Benchmark Track",
    "Generalization Track",
    "Dataset Strategy",
    "Attack Taxonomy",
    "Stealth Model",
    "Hard Negatives",
    "Multi-View Detection",
    "Baselines",
    "Proposed Method Boundary",
    "Metrics",
    "Statistics",
    "Ablation",
    "Cross-domain Evaluation",
    "Unseen Attack Evaluation",
    "Adaptive Attack Plan",
    "Resource Plan",
    "Dual-machine Execution",
    "Known Risks",
    "Confirmed Decisions",
    "Pending Decisions",
    "Claims Boundary",
    "Publication Positioning",
    "Next Gate",
)


class ResearchContextRecoveryTests(unittest.TestCase):
    def test_canonical_recovery_files_exist(self) -> None:
        required = (
            AUTHORITY_MAP,
            EXECUTION_LOG,
            DUAL_MACHINE_POLICY,
            LEARNING / "README.md",
            LEARNING / "STAGE_LEARNING_GUIDE_TEMPLATE.md",
            LEARNING / "stage6_1_hidden_poisoning.md",
            R0_PROTOCOL,
            R0_I_REVIEW,
            FU1_RESOLUTION,
        )
        for path in required:
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertTrue(path.is_file())

    def test_authority_levels_are_unique_and_ordered(self) -> None:
        text = AUTHORITY_MAP.read_text(encoding="utf-8")
        levels = [int(match.group("level")) for match in AUTHORITY_LEVEL.finditer(text)]
        self.assertEqual(list(range(10)), levels)
        self.assertEqual(len(levels), len(set(levels)))
        for required in (
            "Git / Raw Evidence Authority",
            "OWNER-CONFIRMED DECISION AUTHORITY",
            "APPEND-ONLY CHRONOLOGICAL RESEARCH LEDGER",
            "NON_AUTHORITATIVE_EDUCATIONAL_MATERIAL",
            "CONTEXT_CONFLICT_BLOCKER",
            "Git dynamic facts override stale branch/SHA text",
            "New Codex Context Recovery Checklist",
            "Context Recovery Report",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_owner_decision_register_is_the_confirmed_decision_authority(self) -> None:
        text = DECISION_REGISTER.read_text(encoding="utf-8")
        for required in (
            "OWNER-CONFIRMED DECISION AUTHORITY",
            "PENDING_CONFIRMATION",
            "UNKNOWN",
            "PODR-036",
            "Paper-First Comparative Evidence Principle",
            "HIGHEST_RESEARCH_METHOD_PRIORITY_FOR_PAPER_WORK",
            "PoisonedRAG",
            "GMTP",
            "SafeRAG",
            "EcoSafeRAG",
            "DEFERRED",
            "Semantic",
            "Entity-Claim",
            "Provenance",
            "Temporal-Version",
            "Retrieval-Behavior",
            "LOCAL / CONTROL_PLANE",
            "RTX5090 / COMPUTE_WORKER",
            "PODR-041",
            "PODR-042",
            "PODR-043",
            "PODR-044",
            "PODR-045",
            "PODR-046",
            "PODR-047",
            "PODR-048",
            "PODR-049",
            "PODR-050",
            "PODR-051",
            "PODR-052",
            "PODR-053",
            "S6.1-LR1: HUMAN_ACCEPTED",
            "Git-Native Research Context Recovery Governance: HUMAN_ACCEPTED",
            "s6-t5-rag-baseline-v1",
            "S6.1-R0",
            "RTX5090_BOOTSTRAP_READY",
            "S6.1-R0: APPROVED_TO_START",
            "Control-Plane-First Token Economy Principle",
            "LONG_TERM_DUAL_MACHINE_EXECUTION_PRINCIPLE",
            "RETURNED_FOR_WORKER_CORRECTION",
            "S6.1-R0 = HUMAN_ACCEPTED_WITH_BLOCKERS",
            "S6.1-R0-FU1 = APPROVED",
            "LOCAL-FIRST / WORKER-GATED",
            "S6.1-R0-FU1-P0 = HUMAN_ACCEPTED",
            "S6.1-R0-FU1-L1 = HUMAN_ACCEPTED",
            "SUPERSEDED_BY_LOCAL_L1 / NOT FAILED",
            "READY_FOR_OWNER_EXECUTION_APPROVAL / NOT_YET_EXECUTED",
            "S6.1-R0-FU1-W2 = APPROVED_TO_START",
            "DETECTION_CORE_COMPATIBILITY_SMOKE",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_research_execution_log_is_append_only_and_complete(self) -> None:
        text = EXECUTION_LOG.read_text(encoding="utf-8")
        for required in (
            "APPEND-ONLY CHRONOLOGICAL RESEARCH LEDGER",
            "CORRECTION",
            "SUPERSEDING_RECORD",
            "REL-2026-0001",
            "REL-2026-0002",
            "REL-2026-0003",
            "REL-2026-0004",
            "REL-2026-0005",
            "REL-2026-0006",
            "REL-2026-0007",
            "REL-2026-0008",
            "REL-2026-0009",
            "REL-2026-0010",
            "REL-2026-0011",
            "REL-2026-0012",
            "REL-2026-0013",
            "REL-2026-0014",
            "Machine Role",
            "Initial Status",
            "Final Status",
            "Previous Gate",
            "Dataset Snapshot",
            "Model / Revision",
            "Environment Identity",
            "Claims Allowed",
            "Claims Prohibited",
            "Blocker ID",
            "Owner Decisions",
            "Design Changes",
            "Next Approval Gate",
            "Auto Continue",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)
        self.assertIn("Auto Continue: `NO`", text)

    def test_current_state_and_experiment_control_plane_keep_distinct_roles(self) -> None:
        state = CURRENT_STATE.read_text(encoding="utf-8")
        master = MASTER_RECORD.read_text(encoding="utf-8")
        self.assertIn("唯一动态任务状态入口", state)
        self.assertIn("S6.1-LR1", state)
        self.assertIn("Status: **HUMAN_ACCEPTED**", state)
        self.assertIn("FORMAL_EXPERIMENT = NOT STARTED", state)
        self.assertIn("S6.1-R0: **APPROVED_TO_START**", state)
        self.assertIn("S6.1-R0-I: **RETURNED_FOR_WORKER_CORRECTION**", state)
        self.assertIn("Parent S6.1-R0: **HUMAN_ACCEPTED_WITH_BLOCKERS**", state)
        self.assertIn(
            "RTX5090 Compute Worker Bootstrap: **HUMAN_ACCEPTED / RTX5090_BOOTSTRAP_READY**",
            state,
        )
        self.assertIn("S6.1-R0-FU1: **APPROVED / LOCAL-FIRST / WORKER-GATED**", state)
        self.assertIn("S6.1-R0-FU1-P0: **HUMAN_ACCEPTED**", state)
        self.assertIn("S6.1-R0-FU1-L1: **HUMAN_ACCEPTED**", state)
        self.assertIn("SUPERSEDED_BY_LOCAL_L1 / NOT FAILED", state)
        self.assertIn("READY_FOR_OWNER_EXECUTION_APPROVAL / NOT_YET_EXECUTED", state)
        self.assertIn("S6.1-R0-FU1-W2: **APPROVED_TO_START / NOT_YET_EXECUTED**", state)
        self.assertIn("S6.1-P1: **NOT STARTED", state)
        self.assertIn("Dataset: **NOT FROZEN**", state)
        self.assertIn("Detector: **NOT IMPLEMENTED**", state)
        self.assertIn("Training: **NOT STARTED**", state)
        self.assertIn("Our Method Result: **NONE**", state)
        self.assertIn("Dataset Generation: **NOT APPROVED**", state)
        self.assertIn("Detector Implementation: **NOT APPROVED**", state)
        self.assertIn("Model Training: **NOT APPROVED**", state)
        self.assertIn("唯一的实验控制面", master)
        for field in (
            "blocker_id",
            "discovered_at",
            "stage",
            "task",
            "machine",
            "severity",
            "why_it_blocks",
            "affected_scope",
            "attempt_1_result",
            "attempt_2_result",
            "temporary_workaround",
            "final_resolution",
            "resolution_commit",
            "resolution_run",
            "resolved_at",
            "status",
        ):
            with self.subTest(field=field):
                self.assertIn(field, master)
        for status in ("OPEN", "MITIGATED", "RESOLVED", "ACCEPTED_TECHNICAL_DEBT"):
            self.assertIn(status, master)
        self.assertIn("WORKAROUND is not RESOLVED", master)

    def test_license_governance_separates_access_use_comparison_and_redistribution(self) -> None:
        for path in (
            BENCHMARK_MATRIX,
            BASELINE_PROTOCOL,
            ARTIFACT_REGISTRY,
            PAPER1_ROUTE,
        ):
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.relative_to(ROOT)):
                for required in (
                    "SOURCE_ACCESS",
                    "INTERNAL_REPRODUCTION",
                    "STRICT_COMPARISON_ELIGIBILITY",
                    "REDISTRIBUTION_ELIGIBILITY",
                    "CODE_LICENSE",
                    "DATASET_LICENSE",
                ):
                    self.assertIn(required, text)

        registry = ARTIFACT_REGISTRY.read_text(encoding="utf-8")
        self.assertIn("PERMITTED_SUBJECT_TO_MIT_CONDITIONS", registry)
        self.assertIn("NOT_BLOCKED_BY_CURRENT_RESEARCH_PLAN", registry)
        self.assertIn("LICENSE_NOT_CONFIRMED", registry)
        self.assertIn("TO_VERIFY", registry)

    def test_r0_is_defined_as_an_unstarted_engineering_preflight(self) -> None:
        text = R0_PROTOCOL.read_text(encoding="utf-8")
        for required in (
            "S6.1-R0",
            "Paper 1 Reproduction Environment and Baseline Feasibility Validation",
            "ENGINEERING_VALIDATION / REPRODUCTION_PREFLIGHT",
            "APPROVED_TO_START",
            "RTX5090 / COMPUTE_WORKER",
            "Original Paper Environment",
            "RTX5090 Compatibility Environment",
            "peak VRAM",
            "compatibility patches",
            "does not produce Paper Result",
            "external research directory",
            "Auto Continue = NO",
            "R0-A",
            "R0-B",
            "R0-C",
            "R0-D",
            "R0-E",
            "R0-F",
            "R0-G",
            "R0-H",
            "R0-I",
            "poisonedrag-compat",
            "gmtp-compat",
            "saferag-compat",
            "MINIMUM_DATA_REQUIREMENT",
            "EXTERNAL_API_REQUIRED",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_worker_bootstrap_snapshot_is_precise_and_non_experimental(self) -> None:
        text = R0_PROTOCOL.read_text(encoding="utf-8")
        for required in (
            "S6.1-R0-B0",
            "HUMAN_ACCEPTED / RTX5090_BOOTSTRAP_READY",
            "Windows 11 Pro 25H2",
            "Build 26200",
            "Intel Core i9-14900",
            "31.84 GB",
            "Ubuntu 24.04 LTS",
            "PyTorch 2.13.0+cu130",
            "PyTorch CUDA Runtime 13.0",
            "Compute Capability (12, 0)",
            "RTX5090_GPU_TEST_OK",
            "BF16_TEST_OK",
            "NON_BLOCKING_ENVIRONMENT_COMPLETENESS_OBSERVATION",
            "No module named 'numpy'",
            "CUDA Toolkit 13.3 installed",
            "FORMAL_EXPERIMENT = NOT STARTED",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)
        self.assertIn("不得写成", text)

    def test_paper1_route_is_unique_and_complete(self) -> None:
        routes = sorted(ROOT.glob("**/paper1_research_route.md"))
        self.assertEqual([PAPER1_ROUTE], routes)
        text = PAPER1_ROUTE.read_text(encoding="utf-8")
        positions = []
        for index, section in enumerate(ROUTE_SECTIONS, start=1):
            marker = f"## {index}. {section}"
            with self.subTest(marker=marker):
                self.assertIn(marker, text)
            positions.append(text.index(marker))
        self.assertEqual(sorted(positions), positions)
        for required in (
            "HKP-1",
            "HKP-2",
            "HKP-3",
            "HKP-4",
            "Published Result",
            "Reproduced Result",
            "Our Method Result",
            "NON_STRICT_COMPARISON",
            "PODR Decision ID",
            "Research Execution Log ID",
        ):
            self.assertIn(required, text)

    def test_dual_machine_policy_uses_git_and_fails_closed(self) -> None:
        text = DUAL_MACHINE_POLICY.read_text(encoding="utf-8")
        for required in (
            "LOCAL = CONTROL_PLANE",
            "RTX5090 = COMPUTE_WORKER",
            "Context Sync = Git",
            "Codex memory is not a context authority",
            "RESEARCH_ROUTE_REVIEW_REQUIRED",
            "RunManifest.git_commit",
            "dataset snapshot",
            "config hash",
            "model revision",
            "environment fingerprint",
            "fail closed",
            "Control-Plane-First Token Economy Principle",
            "DELEGATE_TO_LOCAL_CONTROL_PLANE",
        ):
                self.assertIn(required, text)

    def test_token_economy_is_resource_governance_not_scientific_priority(self) -> None:
        for path in (LONG_TERM_REQUIREMENTS, DUAL_MACHINE_POLICY):
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.relative_to(ROOT)):
                for required in (
                    "Control-Plane-First Token Economy Principle",
                    "LONG_TERM_DUAL_MACHINE_EXECUTION_PRINCIPLE",
                    "research quality",
                    "reproducibility",
                    "evidence quality",
                    "Paper-First Comparative Evidence",
                    "label isolation",
                    "immutable history",
                ):
                    self.assertIn(required, text)

    def test_r0_i_review_fails_closed_on_material_evidence_mismatch(self) -> None:
        text = R0_I_REVIEW.read_text(encoding="utf-8")
        for required in (
            "RETURNED_FOR_WORKER_CORRECTION",
            "0ce85a2bfe24e0456f9d29edc40659786d4273fcfc634df8749aee6d0e3aa9cc",
            "EVIDENCE_INDEX_VERIFIED: 18/18",
            "f660d72174f06b13fae5163ce656e7b235db858f",
            "15b48d150f93711371eb8da22c211cd84a0cf4df",
            "e8f579743b23e0a3937076dcc0792fe29027cba3",
            "advertised samples absent",
            "data/poisoned_documents",
            "Docker is a convenience environment",
            "DATASET_ARTIFACT_ONLY",
            "EXECUTED_SCRIPT_HASH_NOT_BOUND",
            "R0-FU1: RECOMMEND",
            "R0-FU1 = NOT APPROVED",
            "FORMAL_EXPERIMENT = NOT STARTED",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_r0_corrected_evidence_acceptance_is_additive_and_claim_limited(self) -> None:
        review = R0_I_REVIEW.read_text(encoding="utf-8")
        protocol = R0_PROTOCOL.read_text(encoding="utf-8")
        state = CURRENT_STATE.read_text(encoding="utf-8")
        register = DECISION_REGISTER.read_text(encoding="utf-8")
        execution = EXECUTION_LOG.read_text(encoding="utf-8")
        matrix = BENCHMARK_MATRIX.read_text(encoding="utf-8")
        registry = ARTIFACT_REGISTRY.read_text(encoding="utf-8")
        combined = "\n".join(
            (review, protocol, state, register, execution, matrix, registry)
        )

        for required in (
            "HUMAN_ACCEPTED_WITH_BLOCKERS",
            "ENGINEERING_VALIDATION / REPRODUCTION_PREFLIGHT",
            "904d79c59e35c6aeb157540049b0f44262b86e5c1c5b3e8d4e96ee2fad3f1c6b",
            "fd7617eca689fa46fc6908f94aa4fa158aaae4d277bb17943bbcc1baf74db9bc",
            "f062f038c4bfd19a8ca942a9910b1e0d218759d4",
            "8a38c9f54b963703ae3279f36f53c49083fd76b0f7e96ea27707b728b915db7e",
            "ENGINEERING_FEASIBILITY_IDENTIFIED / P1_PROTOCOL_BLOCKED",
            "ENGINEERING_FEASIBILITY_IDENTIFIED / TARGETED_EXECUTION_BLOCKERS_REMAIN",
            "PARTIAL_REPRODUCTION_READY / DATASET_ARTIFACT_ONLY",
            "BENCHMARK_ARTIFACT_AVAILABLE",
            "API_FREE_ATTACK_GENERATION = NOT ESTABLISHED",
            "P1_PROTOCOL_BLOCKER",
            "FORMAL_EXPERIMENT_ENVIRONMENT_BLOCKER",
            "REDISTRIBUTION_ONLY_ISSUE",
            "APPROVAL_RECOMMENDED / NOT APPROVED",
            "FORMAL_EXPERIMENT = NOT STARTED",
        ):
            with self.subTest(required=required):
                self.assertIn(required, combined)

        self.assertIn("Historical First Review Identity", review)
        self.assertIn("RETURNED_FOR_WORKER_CORRECTION", review)
        self.assertIn("No R0-FU1, S6.1-P1, Dataset, Detector, Training", review)

    def test_fu1_w2_approval_preserves_frozen_contract_and_does_not_open_p1(self) -> None:
        resolution = FU1_RESOLUTION.read_text(encoding="utf-8")
        state = CURRENT_STATE.read_text(encoding="utf-8")
        combined = "\n".join(
            (
                resolution,
                state,
                DECISION_REGISTER.read_text(encoding="utf-8"),
                EXECUTION_LOG.read_text(encoding="utf-8"),
                MASTER_RECORD.read_text(encoding="utf-8"),
                BENCHMARK_MATRIX.read_text(encoding="utf-8"),
                ARTIFACT_REGISTRY.read_text(encoding="utf-8"),
            )
        )
        for required in (
            "COMPLETED_PENDING_OWNER_REVIEW",
            "PRIMARY_EXTERNAL_DATASET_CANDIDATE = NQ",
            "SECONDARY_FALLBACK_DATASET = HotpotQA",
            "AUTHOR_RELEASED_ATTACK_ARTIFACT_USABLE = PARTIAL",
            "AUTHOR_RELEASED_ATTACK_TEXT_ARTIFACT = IDENTITY_VERIFIED",
            "OFFICIAL_LM_TARGETED_ASSEMBLY = DETERMINISTICALLY_VERIFIED",
            "API_FREE_REUSE_OF_RELEASED_ATTACK_TEXTS = VERIFIED_FEASIBLE",
            "API_FREE_ATTACK_GENERATION = NOT ESTABLISHED",
            "d1da818b28da7013864ea465ff88ad4c3ca29562",
            "44df711454a9bada08e72e9e4a003a2cc845c43707ac93a3493e5168ec415cf2",
            "a29630c42508adbb421cc5ee23eac9bbcd58be44",
            "31fb59905812e7656f7206f416dc53228a3089390b0ecd9f0c9e9575dbfc250b",
            "e795764af1655c8de777c4f265400922512e0ab905cdd073b39cca7cc19d9c96",
            "0bb73269d9294a0417fab16314656c14465472f3b539f4617002839dd98114ac",
            "2f891304ab4fbf620e6befe0566600c2e7904832b7da3fafd157e0d90836f1c7",
            "3449b7d5ad7ec0e72d83b35e9c433a0ca9fd2411e2ed7ca6bd8ff46e7e72ffdf",
            "c82243914a79cacfdbc081cfc4d21524251e8d5c383fd85f509bbec1a924641b",
            "ef79bbb3741499e288b615fe5ca45cc85a9606fbf2cdc5ac53f3d6d7d1cb474d",
            "f22b7576c27926a07a7138e952cf3ee6b86c982b584a3078f3364577d32c60a7",
            "beir-cellar/beir",
            "f062f038c4bfd19a8ca942a9910b1e0d218759d4",
            "DETECTION_ONLY_CALL_PATH",
            "CORE_DETECTOR_DEPENDENCY",
            "RETRIEVAL_PREPARATION_DEPENDENCY",
            "INDEXING_DEPENDENCY",
            "GENERATION_DEPENDENCY",
            "EVALUATION_ONLY_DEPENDENCY",
            "abe8c1493371369031bcb1e02acb754cf4e162fa",
            "86b5e0934494bd15c9632b12f734a8a67f723594",
            "0233a26ecc56d7baf1448b86a114e328beece60624aa88304fa3553e90421e44",
            "ret_type=contriever",
            "remove_threshold=0.2",
            "remove_lambda=1.0",
            "gmtp-compat",
            "GMTP-packaged",
            "SAFERAG_BENCHMARK_ARTIFACT_CONTRACT",
            "6508f154817910e1f55926c1fee22bca411255df",
            "STRICTLY_COMPARABLE",
            "PARTIALLY_COMPARABLE",
            "TRANSFER_EVALUATION_ONLY",
            "BENCHMARK_REFERENCE_ONLY",
            "S6.1-R0-FU1-P0 = HUMAN_ACCEPTED",
            "S6.1-R0-FU1-L1 = HUMAN_ACCEPTED",
            "SUPERSEDED_BY_LOCAL_L1",
            "READY_FOR_OWNER_EXECUTION_APPROVAL / NOT_YET_EXECUTED",
            "S6.1-R0-FU1-W2 = APPROVED_TO_START",
            "ENGINEERING_VALIDATION / DETECTION_CORE_COMPATIBILITY_SMOKE",
            "UNEXPECTED_CORE_IMPORT_DEPENDENCY",
            "COMPATIBILITY_PATCH_REVIEW_REQUIRED",
            "WORKER_RESOURCE_APPROVAL_REQUIRED",
            "~/experiments/s6_1_r0_fu1/w2/",
            "OWNER_LARGE_ARTIFACT_APPROVAL_REQUIRED",
            "S6.1-P1_ENTRY_CRITERIA",
            "FORMAL_EXPERIMENT = NOT STARTED",
        ):
            with self.subTest(required=required):
                self.assertIn(required, combined)

        self.assertNotIn("S6.1-R0-FU1-W2: **APPROVED_TO_EXECUTE**", state)
        self.assertIn("S6.1-P1 is not automatically authorized", state)

    def test_learning_guides_are_non_authoritative(self) -> None:
        for path in (
            LEARNING / "README.md",
            LEARNING / "STAGE_LEARNING_GUIDE_TEMPLATE.md",
            LEARNING / "stage6_1_hidden_poisoning.md",
        ):
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertIn("NON_AUTHORITATIVE_EDUCATIONAL_MATERIAL", text)
                self.assertNotIn("FORMAL_EXPERIMENT = COMPLETE", text)

    def test_new_context_files_are_portable_and_preserve_baselines(self) -> None:
        paths = (
            AUTHORITY_MAP,
            EXECUTION_LOG,
            DUAL_MACHINE_POLICY,
            PAPER1_ROUTE,
            LEARNING / "README.md",
            LEARNING / "STAGE_LEARNING_GUIDE_TEMPLATE.md",
            LEARNING / "stage6_1_hidden_poisoning.md",
        )
        for path in paths:
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertIsNone(WINDOWS_ABSOLUTE_PATH.search(text))

        combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
        for required in (
            "18cf2741c8383d35604715af6ebf8cbaa2a3ddf1",
            "4ecf73a",
            "b136ee2",
            "b6cedf3",
            "Stage 1–5",
            "immutable",
            "FORMAL_EXPERIMENT = NOT STARTED",
        ):
            self.assertIn(required, combined)


if __name__ == "__main__":
    unittest.main()
