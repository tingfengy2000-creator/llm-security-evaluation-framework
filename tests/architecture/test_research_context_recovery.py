from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GOVERNANCE = ROOT / "docs" / "governance"
RESEARCH = ROOT / "docs" / "research" / "stage6_1_hidden_knowledge_poisoning"
LEARNING = ROOT / "docs" / "learning"

AUTHORITY_MAP = GOVERNANCE / "context_authority_map.md"
PO_MHEP = GOVERNANCE / "project_owner_sovereignty_and_mandatory_escalation_principle.md"
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
W2_ATTEMPT1_REVIEW = RESEARCH / "s6_1_r0_fu1_w2_attempt1_control_plane_review.md"
W2_H2_RESUME02_REVIEW = RESEARCH / "s6_1_r0_fu1_w2_h2_resume02_control_plane_review.md"
P1_PROTOCOL_CANDIDATE = RESEARCH / "s6_1_p1_protocol_candidate.md"
P1_R1_PROTOCOL_CANDIDATE = RESEARCH / "s6_1_p1_r1_protocol_review_candidate.md"
PILOT2_RETURN_OWNER_CORRECTION = RESEARCH / "s6_1_p1_pilot2_return_owner_correction.md"
PILOT2_ANNOTATION_V2 = RESEARCH / "s6_1_p1_pilot2_annotation_v2.md"
LONG_TERM_REQUIREMENTS = GOVERNANCE / "long_term_research_requirements.md"
AGENTS = ROOT / "AGENTS.md"
PAPER1_README = RESEARCH / "README.md"
HUMAN_DIR = RESEARCH / "human"
AGENT_DIR = RESEARCH / "agent"
STAGE_PROCESS_DIR = RESEARCH / "stage_process"
TINGFENG_LEDGER = HUMAN_DIR / "experiment_ledger_tingfeng.md"
OWNER_REQUIREMENTS = HUMAN_DIR / "owner_requirement_register.md"
RESEARCH_PLAN = HUMAN_DIR / "research_plan_authority.md"
AGENT_LEDGER = AGENT_DIR / "experiment_ledger_agentUse.md"
CONTEXT_ARCHIVE = AGENT_DIR / "llm_context_archive.md"

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
            PO_MHEP,
            EXECUTION_LOG,
            DUAL_MACHINE_POLICY,
            LEARNING / "README.md",
            LEARNING / "STAGE_LEARNING_GUIDE_TEMPLATE.md",
            LEARNING / "stage6_1_hidden_poisoning.md",
            R0_PROTOCOL,
            R0_I_REVIEW,
            FU1_RESOLUTION,
            W2_ATTEMPT1_REVIEW,
            W2_H2_RESUME02_REVIEW,
            P1_PROTOCOL_CANDIDATE,
            P1_R1_PROTOCOL_CANDIDATE,
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
            "PODR-054",
            "PODR-055",
            "PODR-056",
            "PODR-057",
            "PODR-058",
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
            "REL-2026-0015",
            "REL-2026-0016",
            "REL-2026-0017",
            "REL-2026-0018",
            "REL-2026-0019",
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
        self.assertLess(
            text.index("## REL-2026-0015"),
            text.index("## REL-2026-0016"),
        )
        self.assertLess(
            text.index("## REL-2026-0016"),
            text.index("## REL-2026-0017"),
        )
        self.assertLess(
            text.index("## REL-2026-0017"),
            text.index("## REL-2026-0018"),
        )
        self.assertLess(
            text.index("## REL-2026-0018"),
            text.index("## REL-2026-0019"),
        )

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
        self.assertIn("S6.1-R0-FU1: **HUMAN_ACCEPTED / CLOSED**", state)
        self.assertIn("S6.1-R0-FU1-P0: **HUMAN_ACCEPTED**", state)
        self.assertIn("S6.1-R0-FU1-L1: **HUMAN_ACCEPTED**", state)
        self.assertIn("SUPERSEDED_BY_LOCAL_L1 / NOT FAILED", state)
        self.assertIn("READY_FOR_OWNER_EXECUTION_APPROVAL / NOT_YET_EXECUTED", state)
        self.assertIn(
            "S6.1-R0-FU1-W2: **HUMAN_ACCEPTED / ENGINEERING_FEASIBILITY_ONLY / CLOSED**",
            state,
        )
        self.assertIn("W2_ATTEMPT1_EVIDENCE_BLOCKER", state)
        self.assertIn("RESOLVED_BY_CORRECTION_02", state)
        self.assertIn("VALID_BLOCKED_ENGINEERING_RUN / MODEL_DOWNLOAD_BLOCKER", state)
        self.assertIn("OFFLINE_MODEL_ARTIFACTS_VERIFIED_ON_5090", state)
        self.assertIn(
            "S6.1-P1: **APPROVED_FOR_PILOT0_INFRASTRUCTURE_ONLY / NOT FORMAL_EXPERIMENT**",
            state,
        )
        self.assertIn("REAL_DATA_PILOT / 240_GROUP_PILOT: **NOT APPROVED / NOT STARTED**", state)
        self.assertIn("Dataset: **NOT FROZEN**", state)
        self.assertIn("Detector: **NOT IMPLEMENTED**", state)
        self.assertIn("Training: **NOT STARTED**", state)
        self.assertIn("Our Method Result: **NONE**", state)
        self.assertIn("Dataset Generation: **NOT APPROVED**", state)
        self.assertIn("Detector Implementation: **NOT APPROVED**", state)
        self.assertIn("Model Training: **NOT APPROVED**", state)
        self.assertIn("PO-MHEP", state)
        self.assertIn("HIGHEST_INTERNAL_PROJECT_EXECUTION_AUTHORITY", state)
        self.assertIn("NO_SELF_APPROVAL_AUTHORITY", state)
        self.assertIn("CONTROL_PLANE_REVIEW_PASS / FINAL_CLOSURE_APPLIED", state)
        self.assertIn("aa06e4cd03cb4d1eeb008514d81bc4d41e98f88614df046e008ac1f1544def45", state)
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
        self.assertIn("S6.1-P1-PILOT0: **COMPLETED_PENDING_REVIEW**", state)
        self.assertIn("REAL_DATA_PILOT / 240_GROUP_PILOT: **NOT APPROVED / NOT STARTED**", state)

    def test_w2_attempt1_gap_history_and_correction02_closure_are_both_preserved(self) -> None:
        review = W2_ATTEMPT1_REVIEW.read_text(encoding="utf-8")
        state = CURRENT_STATE.read_text(encoding="utf-8")
        combined = "\n".join(
            (
                review,
                state,
                FU1_RESOLUTION.read_text(encoding="utf-8"),
                DECISION_REGISTER.read_text(encoding="utf-8"),
                EXECUTION_LOG.read_text(encoding="utf-8"),
                MASTER_RECORD.read_text(encoding="utf-8"),
            )
        )
        for required in (
            "6acdbb8038e57b1d3e88028350fc08046d73a826ba9dd167452bfc0dd834170f",
            "18/18",
            "16/16",
            "8411af2042774f1a18eec95e97a14ade088acbc35f09942ae9ffea4e8ea5fc06",
            "MODEL_DOWNLOAD_BLOCKER",
            "smoke_executed=false",
            "main LLMGuard repository HEAD evidence",
            "Disk/resource smoke limits: NOT_EVALUATED",
            "W2_ATTEMPT1_EVIDENCE_BLOCKER",
            "W2_TASK_OWNED_DISK_HARD_CEILING = 10 GiB",
            "APPROVED_TO_PREPARE_OFFLINE_ARTIFACTS",
            "BLOCKED_BY_W2_ATTEMPT1_EVIDENCE_BLOCKER",
            "No model download or offline bundle was performed",
            "S6.1-P1 = NOT STARTED",
            "FORMAL_EXPERIMENT = NOT STARTED",
            "d911063e3a00daba3f8dcfea6f3e6e3b484e79f4f0fe8853a53ff9d8c415279e",
            "safe members `6/6`",
            "correction index `4/4`",
            "5399301224",
            "5492817920",
            "6442450944",
            "MEASUREMENT_TOOL=du",
            "no concrete `du` commands",
            "CORRECTION_DU_COMMAND_EVIDENCE_MISSING",
        ):
            with self.subTest(required=required):
                self.assertIn(required, combined)

        self.assertIn("S6.1-R0-FU1-W2-ATTEMPT1: **VALID_BLOCKED_ENGINEERING_RUN", state)
        self.assertIn("RESOLVED_BY_CORRECTION_02_CONTROL_PLANE_REVIEW", state)
        self.assertIn("OFFLINE_MODEL_ARTIFACTS_VERIFIED_ON_5090", state)
        self.assertIn("No model download or offline bundle was performed", review)

    def test_po_mhep_is_highest_execution_authority_and_fail_closed(self) -> None:
        principle = PO_MHEP.read_text(encoding="utf-8")
        authority = AUTHORITY_MAP.read_text(encoding="utf-8")
        agents = AGENTS.read_text(encoding="utf-8")
        long_term = LONG_TERM_REQUIREMENTS.read_text(encoding="utf-8")
        state = CURRENT_STATE.read_text(encoding="utf-8")
        combined = "\n".join((principle, authority, agents, long_term, state))

        for required in (
            "PO-MHEP",
            "HUMAN_ACCEPTED",
            "HIGHEST_INTERNAL_PROJECT_EXECUTION_AUTHORITY",
            "Permanent",
            "NO",
            "L0 — Dynamic Git Facts and Immutable Raw Evidence",
            "L0.5 — PO-MHEP",
            "HUMAN_DECISION_REQUIRED",
            "Auto Continue = NO",
            "real API",
            "system-level installation",
            "large model/data/index download",
            "algorithm-semantic patch",
            "Paper and research risk",
            "Evidence and governance risk",
            "context conflicts",
            "OBSERVED_FACT",
            "SOURCE_DERIVED_FACT",
            "INFERENCE",
            "UNKNOWN",
            "FORWARD_RISK_REVIEW",
            "PAPER_RISK_REVIEW",
            "CONTEXT_PERSISTENCE_CHECK",
            "NO_SELF_APPROVAL_AUTHORITY",
            "STOP",
            "RETURN_TO_CONTROL_PLANE",
        ):
            with self.subTest(required=required):
                self.assertIn(required, combined)

        self.assertIn("## L0.5 — Project Owner Sovereignty and Mandatory Escalation", authority)
        self.assertLess(agents.index("context_authority_map.md"), agents.index("project_owner_sovereignty"))
        self.assertIn("Mandatory Startup Protocol", agents)
        self.assertIn("project_owner_sovereignty_and_mandatory_escalation_principle.md", agents)
        self.assertIn("唯一动态任务状态入口", state)

    def test_correction02_final_closure_and_h1_artifacts_do_not_advance_w2(self) -> None:
        state = CURRENT_STATE.read_text(encoding="utf-8")
        fu1 = FU1_RESOLUTION.read_text(encoding="utf-8")
        master = MASTER_RECORD.read_text(encoding="utf-8")
        combined = "\n".join((state, fu1, master, PO_MHEP.read_text(encoding="utf-8")))

        for required in (
            "S6.1-R0-FU1-W2: **HUMAN_ACCEPTED / ENGINEERING_FEASIBILITY_ONLY / CLOSED**",
            "VALID_BLOCKED_ENGINEERING_RUN / MODEL_DOWNLOAD_BLOCKER",
            "RESOLVED_BY_CORRECTION_02_CONTROL_PLANE_REVIEW",
            "OFFLINE_MODEL_ARTIFACTS_PREPARED_PENDING_5090_VERIFICATION",
            "S6.1-P1: **APPROVED_FOR_PILOT0_INFRASTRUCTURE_ONLY / NOT FORMAL_EXPERIMENT**",
            "FORMAL_EXPERIMENT = NOT STARTED",
            "S6.1-R0-FU1-W2-ATTEMPT1-CORRECTION-02",
            "APPROVED_TO_START / NOT SENT / NOT EXECUTED",
            "PODR-057",
            "REL-2026-0018",
            "PODR-058",
            "REL-2026-0019",
            'LC_ALL=C du -sb -- "$CONDA_PREFIX"',
            'LC_ALL=C du -sB1 -- "$CONDA_PREFIX"',
            "command -V du",
            "type -a du",
            "du --version",
            "uname -a",
            "date -u",
            "conda env list --json",
            "5399301224",
            "5492817920",
            "33556",
            "3194",
            "6442450944",
            "correction_index.sha256",
            "17/17",
            "MATERIALITY_AND_FINAL_CLOSURE_RULE",
            "DISK_MEASUREMENT_MATERIAL_MISMATCH",
            "W2_ATTEMPT1_CORRECTION02_EVIDENCE_READY_FOR_CONTROL_PLANE_REVIEW",
            "VALID_BLOCKED_ENGINEERING_RUN / MODEL_DOWNLOAD_BLOCKER",
            "REUSABLE_W2_PREFLIGHT_EVIDENCE",
            "no new H1 owner approval is required",
            "FORWARD_RISK_REVIEW = PASS_WITH_GUARDRAILS",
            "PAPER_RISK_REVIEW = PASS_WITH_CLAIMS_BOUNDARY",
            "fcfa3f14c98e0103cb5a1de2f0449fa000d179e2e01d74baa6fec4b013503622",
            "aa06e4cd03cb4d1eeb008514d81bc4d41e98f88614df046e008ac1f1544def45",
            "1320352375",
            "438708922",
            "881643453",
        ):
            with self.subTest(required=required):
                self.assertIn(required, combined)

        self.assertNotIn("models loaded = true", combined.lower())
        self.assertNotIn("W2 completed\nW2 accepted", combined)

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
            PO_MHEP,
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

    def test_paper1_restructured_directories_and_canonical_files_exist(self) -> None:
        for directory in (HUMAN_DIR, AGENT_DIR, STAGE_PROCESS_DIR):
            with self.subTest(directory=directory.relative_to(ROOT)):
                self.assertTrue(directory.is_dir())

        required = (
            TINGFENG_LEDGER,
            OWNER_REQUIREMENTS,
            RESEARCH_PLAN,
            AGENT_LEDGER,
            CONTEXT_ARCHIVE,
            STAGE_PROCESS_DIR / "S6.1-LR1_work_process.md",
            STAGE_PROCESS_DIR / "S6.1-R0_work_process.md",
            STAGE_PROCESS_DIR / "S6.1-R0-FU1_work_process.md",
            STAGE_PROCESS_DIR / "S6.1-P1_work_process.md",
        )
        for path in required:
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertTrue(path.is_file())

        processes = sorted(STAGE_PROCESS_DIR.glob("*_work_process.md"))
        self.assertEqual(4, len(processes))
        self.assertEqual(4, len({path.name.split("_work_process.md")[0] for path in processes}))
        expected_sections = (
            "阶段目标",
            "进入条件",
            "已批准范围",
            "执行环境",
            "源码、数据与模型身份",
            "工作拆解",
            "实际执行过程",
            "关键命令",
            "输入",
            "输出",
            "结果",
            "证据与哈希",
            "失败与 blocker",
            "失败分析",
            "解决方式",
            "人工决定",
            "允许宣称",
            "禁止宣称",
            "阶段退出条件",
            "当前状态",
            "下一审批门",
        )
        for path in processes:
            text = path.read_text(encoding="utf-8")
            headings = re.findall(r"^## (\d+)\. (.+)$", text, re.MULTILINE)
            with self.subTest(process=path.name):
                self.assertEqual(
                    [(str(index), title) for index, title in enumerate(expected_sections, 1)],
                    headings,
                )
                self.assertIsNone(re.search(r"\b(?:LOCAL|RTX5090|Worker)\b", text, re.I))

    def test_paper1_start_here_order_and_document_roles(self) -> None:
        readme = PAPER1_README.read_text(encoding="utf-8")
        self.assertTrue(readme.startswith("# Paper 1 Start Here\n"))
        ordered_links = (
            "human/experiment_ledger_tingfeng.md",
            "agent/experiment_ledger_agentUse.md",
            "../../governance/current_work_state.md",
            "human/research_plan_authority.md",
            "../../governance/experiment_master_record.md",
        )
        positions = [readme.index(link) for link in ordered_links]
        self.assertEqual(sorted(positions), positions)

        requirements = OWNER_REQUIREMENTS.read_text(encoding="utf-8")
        plan = RESEARCH_PLAN.read_text(encoding="utf-8")
        route = PAPER1_ROUTE.read_text(encoding="utf-8")
        audit = EXECUTION_LOG.read_text(encoding="utf-8")
        self.assertIn("PAPER1_OWNER_REQUIREMENT_AUTHORITY", requirements)
        self.assertIn("唯一登记项目需求提出人已明确确认需求", requirements)
        self.assertIn("Document Authority = `PAPER1_RESEARCH_PLAN_AUTHORITY`", plan)
        self.assertIn("Change Permission = `OWNER_CONFIRMATION_REQUIRED`", plan)
        self.assertIn("Current Plan Status = `ACCEPTED_CURRENT_RESEARCH_PLAN`", plan)
        self.assertIn("Primary Authority = `human/research_plan_authority.md`", route)
        self.assertIn("Document Role = `HISTORICAL_AND_SUPPORTING_RESEARCH_ROUTE`", route)
        self.assertIn("ACCEPTED_CURRENT_RESEARCH_PLAN", CURRENT_STATE.read_text(encoding="utf-8"))
        self.assertIn("项目级追加式审计日志", audit)
        self.assertIn("它不是 Paper 1 人类实验总账", audit)
        self.assertEqual(1, audit.count("## REL-2026-0020"))
        self.assertEqual(1, audit.count("## REL-2026-0021"))
        self.assertEqual(1, audit.count("## REL-2026-0022"))
        self.assertEqual(1, audit.count("## REL-2026-0023"))
        self.assertEqual(1, audit.count("## REL-2026-0024"))

    def test_human_docs_are_chinese_first_without_long_english_blocks(self) -> None:
        for path in HUMAN_DIR.glob("*.md"):
            text = path.read_text(encoding="utf-8")
            prose = re.sub(r"`[^`]*`", "", text)
            chinese = len(re.findall(r"[\u4e00-\u9fff]", prose))
            english = len(re.findall(r"[A-Za-z]", prose))
            with self.subTest(path=path.relative_to(ROOT)):
                if path == TINGFENG_LEDGER:
                    # The primary human ledger intentionally retains a large bilingual
                    # glossary, status enums and route table while keeping Chinese prose.
                    self.assertGreater(chinese, 4_000)
                else:
                    self.assertGreater(chinese, english)
                non_code_paragraphs = re.split(r"\n\s*\n", re.sub(r"```.*?```", "", text, flags=re.S))
                for paragraph in non_code_paragraphs:
                    if len(paragraph) < 240:
                        continue
                    self.assertTrue(
                        re.search(r"[\u4e00-\u9fff]", paragraph),
                        f"unnecessary long English block in {path.name}",
                    )

        summary = TINGFENG_LEDGER.read_text(encoding="utf-8").split(
            "## 0. 先看这里：5 分钟了解 Paper 1", 1
        )[1].split("## 1.", 1)[0]
        self.assertLessEqual(len(re.findall(r"[\u4e00-\u9fff]", summary)), 500)

    def test_agent_views_are_derived_and_context_archive_has_no_authority(self) -> None:
        ledger = AGENT_LEDGER.read_text(encoding="utf-8")
        archive = CONTEXT_ARCHIVE.read_text(encoding="utf-8")
        for required in (
            "Document Role = `LLM_STRUCTURED_EXPERIMENT_LEDGER`",
            "Authority = `DERIVED_INFORMATION_VIEW`",
            "Can Override Owner Requirement = `NO`",
            "Can Override Research Plan = `NO`",
            "Can Override Raw Evidence = `NO`",
            "Primary Human Mirror = `../human/experiment_ledger_tingfeng.md`",
            "run_id",
            "source_blob",
            "artifact_sha256",
            "claims_prohibited",
            "next_gate",
        ):
            self.assertIn(required, ledger)
        for required in (
            "This document is a context recovery artifact.",
            "owner requirement authority",
            "research plan authority",
            "raw evidence",
            "formal result",
            "## Historical Context Checkpoints",
        ):
            self.assertIn(required, archive)

    def test_human_and_agent_ledgers_share_current_experiment_state(self) -> None:
        human = TINGFENG_LEDGER.read_text(encoding="utf-8")
        agent = AGENT_LEDGER.read_text(encoding="utf-8")
        shared_states = (
            "HUMAN_ACCEPTED_AS_PROTOCOL_FRAMEWORK",
            "PILOT4_BALANCED_SET_REPAIRED",
            "READY_FOR_SECOND_OWNER_PREFLIGHT",
            "PREANNOTATION_ONLY",
            "NO_HUMAN_DISTRIBUTION",
            "NOT FROZEN",
            "NOT IMPLEMENTED",
            "NOT STARTED",
            "NONE",
        )
        for state in shared_states:
            with self.subTest(state=state):
                self.assertIn(state, human)
                self.assertIn(state, agent)
        self.assertIn(
            "S6.1-R0-FU1-W2-H2-RESUME-01: VALID_BLOCKED_EVIDENCE / "
            "OFFLINE_BUNDLE_SHA_BLOCKER / H2-B NOT EXECUTED / call_count=0",
            agent,
        )
        self.assertIn(
            "S6.1-R0-FU1-W2-H2-RESUME-02: CONTROL_PLANE_REVIEW_PASS / "
            "ENGINEERING_SMOKE_EVIDENCE_ACCEPTED / call_count=1",
            agent,
        )
        self.assertIn("H2_historical_preapproval: PROPOSED / NOT CANONICAL / NOT APPROVED", agent)
        self.assertIn("Agent Experiment Ledger", human)
        self.assertIn("CONTROL_PLANE_REVIEW_PASS / ENGINEERING_SMOKE_EVIDENCE_ACCEPTED", human)

    def test_h2_resume02_control_plane_review_closes_only_minimal_feasibility(self) -> None:
        review = W2_H2_RESUME02_REVIEW.read_text(encoding="utf-8")
        current = CURRENT_STATE.read_text(encoding="utf-8")
        master = MASTER_RECORD.read_text(encoding="utf-8")
        audit = EXECUTION_LOG.read_text(encoding="utf-8")
        combined = "\n".join((review, current, master, audit))

        for required in (
            "58da856a81ad89b858af2c041ff617e16156ec254410b07e6511c2888203f563",
            "15625",
            "25/25 PASS",
            "18/18 PASS",
            "call_count=1",
            "OFFLINE_MODEL_ARTIFACTS_VERIFIED_ON_5090",
            "CONTROL_PLANE_REVIEW_PASS / ENGINEERING_SMOKE_EVIDENCE_ACCEPTED",
            "RESOLVED_BY_H2_RESUME02_CONTROL_PLANE_REVIEW",
            "APPROVED_TO_START / NOT COMPLETED / NOT ACCEPTED",
            "S6.1-P1 = NOT STARTED",
            "Formal Experiment `NOT STARTED`",
            "REL-2026-0023",
        ):
            with self.subTest(required=required):
                self.assertIn(required, combined)

        self.assertIn("The single-call authorization is consumed", review)
        self.assertIn("not establish benchmark reproduction", review)
        self.assertIn("W2_ACCEPTANCE_SCOPE", current)

    def test_h2_conditional_approval_contract_is_frozen_and_non_experimental(self) -> None:
        human = TINGFENG_LEDGER.read_text(encoding="utf-8")
        agent = AGENT_LEDGER.read_text(encoding="utf-8")
        process = (STAGE_PROCESS_DIR / "S6.1-R0-FU1_work_process.md").read_text(
            encoding="utf-8"
        )
        current = CURRENT_STATE.read_text(encoding="utf-8")
        decisions = DECISION_REGISTER.read_text(encoding="utf-8")
        master = MASTER_RECORD.read_text(encoding="utf-8")
        combined = "\n".join((human, agent, process, current, decisions, master))

        for required in (
            "PODR-059",
            "APPROVED_TO_START / NOT SENT / NOT EXECUTED",
            "CONDITIONAL_WITHIN_H2_ONLY",
            "H2-A 失败不得进入 H2-B",
            "HF_HUB_OFFLINE=1",
            "TRANSFORMERS_OFFLINE=1",
            "HF_HUB_DISABLE_TELEMETRY=1",
            "TOKENIZERS_PARALLELISM=false",
            "importlib.util.spec_from_file_location",
            'doc_ids=["benign", "poisoned"]',
            "W2_RESUME02_ENGINEERING_SMOKE_COMPLETED_PENDING_REVIEW",
            "OFFLINE_BUNDLE_SHA_BLOCKER",
            "COMPATIBILITY_PATCH_REVIEW_REQUIRED",
            "WORKER_RESOURCE_APPROVAL_REQUIRED",
            "APPROVED_TO_START / NOT COMPLETED / NOT ACCEPTED",
            "S6.1-P1 = NOT STARTED",
            "Our Method Result = NONE",
            "Formal Experiment = NOT STARTED",
        ):
            with self.subTest(required=required):
                self.assertIn(required, combined)

        self.assertEqual(1, process.count("filter_documents("))
        self.assertEqual(21, len(re.findall(r"^## \d+\.", process, re.MULTILINE)))
        self.assertIn("不得修改 `method.py`", process)
        self.assertIn("network fallback", combined)
        self.assertIn("HUMAN_ACCEPTED / ENGINEERING_FEASIBILITY_ONLY / CLOSED", combined)

    def test_w2_owner_acceptance_and_p1_candidate_are_narrow_and_consistent(self) -> None:
        current = CURRENT_STATE.read_text(encoding="utf-8")
        decisions = DECISION_REGISTER.read_text(encoding="utf-8")
        master = MASTER_RECORD.read_text(encoding="utf-8")
        human = TINGFENG_LEDGER.read_text(encoding="utf-8")
        agent = AGENT_LEDGER.read_text(encoding="utf-8")
        process = (STAGE_PROCESS_DIR / "S6.1-R0-FU1_work_process.md").read_text(
            encoding="utf-8"
        )
        candidate = P1_PROTOCOL_CANDIDATE.read_text(encoding="utf-8")
        combined = "\n".join((current, decisions, master, human, agent, process))

        for required in (
            "PODR-061",
            "OR-020",
            "HUMAN_ACCEPTED / ENGINEERING_FEASIBILITY_ONLY / CLOSED",
            "S6.1-R0-FU1 = HUMAN_ACCEPTED / CLOSED",
            "W2_ENGINEERING_OBJECTIVE = SATISFIED",
            "W2_RUNTIME_GATE = CLOSED",
            "FROZEN_SINGLE_SAMPLE_DETECTION_CORE_ENGINEERING_FEASIBILITY_ONLY",
            "RESOLVED_BY_H2_RESUME02_AND_OWNER_ACCEPTANCE",
            "GMTP_REPRODUCTION = NOT ESTABLISHED",
            "DETECTION_EFFECTIVENESS = NOT ESTABLISHED",
            "STRICT_BASELINE_COMPARISON = NOT ESTABLISHED",
            "58da856a81ad89b858af2c041ff617e16156ec254410b07e6511c2888203f563",
            "25/25 PASS",
            "18/18 PASS",
            "call_count=1",
            "H2-B NOT EXECUTED / call_count=0",
            "这是单次冻结样本的工程观察，不是检测性能结论",
            "Dataset = NOT FROZEN",
            "Detector = NOT IMPLEMENTED",
            "Training = NOT STARTED",
            "Our Method Result = NONE",
            "Formal Experiment = NOT STARTED",
        ):
            with self.subTest(required=required):
                self.assertIn(required, combined)

        for required in (
            "Authority = `NON_CANONICAL_CANDIDATE`",
            "Status = `CONTRACT_CANDIDATE / NOT APPROVED / NOT STARTED`",
            "RQ1：",
            "RQ5：",
            "HKP-1",
            "HKP-4",
            "S1、S2、S3",
            "Semantic View",
            "Retrieval-Behavior View",
            "AUPRC",
            "F1 at frozen threshold",
            "Recall at controlled FPR",
            "Holm correction",
            "不少于 5 个随机种子",
            "Option A",
            "Option B",
            "Option C",
            "HUMAN_DECISION_REQUIRED_BEFORE_P1_APPROVAL",
        ):
            with self.subTest(required=required):
                self.assertIn(required, candidate)

        self.assertEqual(1, len(list(STAGE_PROCESS_DIR.glob("S6.1-R0-FU1_work_process.md"))))

    def test_p1_r1_framework_acceptance_opens_only_pilot0_infrastructure(self) -> None:
        candidate = P1_R1_PROTOCOL_CANDIDATE.read_text(encoding="utf-8")
        old_candidate = P1_PROTOCOL_CANDIDATE.read_text(encoding="utf-8")
        requirements = OWNER_REQUIREMENTS.read_text(encoding="utf-8")
        plan = RESEARCH_PLAN.read_text(encoding="utf-8")
        current = CURRENT_STATE.read_text(encoding="utf-8")
        decisions = DECISION_REGISTER.read_text(encoding="utf-8")
        master = MASTER_RECORD.read_text(encoding="utf-8")
        audit = EXECUTION_LOG.read_text(encoding="utf-8")
        human = TINGFENG_LEDGER.read_text(encoding="utf-8")
        agent = AGENT_LEDGER.read_text(encoding="utf-8")
        context = CONTEXT_ARCHIVE.read_text(encoding="utf-8")
        combined = "\n".join(
            (
                requirements,
                plan,
                current,
                decisions,
                master,
                audit,
                human,
                agent,
                context,
                candidate,
            )
        )

        for required in (
            "OR-021",
            "PODR-062",
            "REL-2026-0025",
            "P1_R1_BASE_COMMIT = aabe504d55626fb31008822b7bbabd3b32e2afd4",
            "DETOXIFICATION_OPTION = OPTION_B",
            "DETOXIFICATION_TECHNICAL_SCOPE = OPTION_B_CONFIRMED",
            "OPTION_B_DETECTION_AND_LIGHTWEIGHT_RETRIEVAL_INTERVENTION",
            "OR-022",
            "S6.1-P1-R1: **HUMAN_ACCEPTED_AS_PROTOCOL_FRAMEWORK**",
            "S6.1-P1: **APPROVED_FOR_PILOT0_INFRASTRUCTURE_ONLY / NOT FORMAL_EXPERIMENT**",
            "REAL_DATA_PILOT / 240_GROUP_PILOT: **NOT APPROVED / NOT STARTED**",
            "P1 numeric parameters: **PENDING_PILOT_EVIDENCE**",
            "4f381451688150016b1a518895ad75149cfdfdac4cd512dd6062becba04b2ed0",
            "Dataset = NOT FROZEN",
            "Detector = NOT IMPLEMENTED",
            "Retrieval Intervention = NOT IMPLEMENTED",
            "Training = NOT STARTED",
            "Our Method Result = NONE",
            "Formal Experiment = NOT STARTED",
            "HUMAN_ACCEPTED / ENGINEERING_FEASIBILITY_ONLY / CLOSED",
            "S6.1-R0-FU1 = HUMAN_ACCEPTED / CLOSED",
        ):
            with self.subTest(required=required):
                self.assertIn(required, combined)

        for required in (
            "Document Role = `P1_APPROVAL_GRADE_REVIEW_CANDIDATE`",
            "Authority = `NON_CANONICAL_CANDIDATE`",
            "Creation Status Snapshot = `REVIEW_CANDIDATE / NOT APPROVED / NOT STARTED`",
            "Supersedes Candidate Draft",
            "RQ1：",
            "RQ6：",
            "Query-Document Unit",
            "Retrieval-Set Unit",
            "independence_group_id",
            "PUBLIC_TRACEABLE_CHINESE_DOCUMENTS + CONTROLLED_MUTATION + HUMAN_REVIEW",
            "Retriever visible",
            "Detector visible",
            "Evaluator only",
            "DATA_SPLIT_LEAKAGE_BLOCKER",
            "Hard Filtering",
            "Soft Downweighting",
            "co-primary endpoints",
            "10,000",
            "2,000",
            "Holm correction",
            "Stage A — Pilot",
            "MINIMAL_PUBLISHABLE_MATRIX",
            "FULL_MATRIX",
            "RESOURCE_BUDGET_REVIEW_REQUIRED",
            "P1 获批前以下二十项必须全部满足",
            "FORWARD_RISK_REVIEW = PASS_FOR_REVIEW_CANDIDATE_ONLY",
            "PAPER_RISK_REVIEW = FRAMEWORK_ACCEPTED_WITH_OPEN_FREEZES",
            "Historical Decision Checklist 与当前下一门",
        ):
            with self.subTest(required=required):
                self.assertIn(required, candidate)

        for excluded in (
            "trusted context package",
            "完整上下文构造",
            "多证据可信上下文生成",
            "复杂端到端 Agent 防御",
            "生产级 RAG 平台",
            "完整可信检索链",
        ):
            with self.subTest(excluded=excluded):
                self.assertIn(excluded, candidate)

        self.assertTrue(old_candidate)
        self.assertNotIn("DETOXIFICATION_OPTION = OPTION_A", combined)
        self.assertNotIn("DETOXIFICATION_OPTION = OPTION_C", combined)
        self.assertIn("它明确不包括 trusted context package", candidate)
        self.assertIn("EXCLUDED_FROM_PAPER1_BY_OR-021", requirements)
        for mirror in (human, agent):
            for marker in (
                "HUMAN_ACCEPTED_AS_PROTOCOL_FRAMEWORK",
                "READY_FOR_SECOND_OWNER_PREFLIGHT",
                "NOT FROZEN",
                "NOT IMPLEMENTED",
                "Formal Experiment",
            ):
                with self.subTest(mirror=mirror[:32], marker=marker):
                    self.assertIn(marker, mirror)
        self.assertTrue((STAGE_PROCESS_DIR / "S6.1-P1_work_process.md").is_file())

    def test_h2_resume02_rollover_preserves_resume01_and_single_call_gate(self) -> None:
        process = (STAGE_PROCESS_DIR / "S6.1-R0-FU1_work_process.md").read_text(
            encoding="utf-8"
        )
        requirements = OWNER_REQUIREMENTS.read_text(encoding="utf-8")
        decisions = DECISION_REGISTER.read_text(encoding="utf-8")
        current = CURRENT_STATE.read_text(encoding="utf-8")
        audit = EXECUTION_LOG.read_text(encoding="utf-8")
        combined = "\n".join((process, requirements, decisions, current, audit))

        for required in (
            "OR-018",
            "OR-019",
            "PODR-060",
            "REL-2026-0022",
            "941557aa00be58210015165078bbb3c1cbdd2250cab0755c37198e7b7e26e89d",
            "4570",
            "OFFLINE_BUNDLE_SHA_BLOCKER",
            "EVIDENCE_CAPTURE_BLOCKER",
            "~/experiments/s6_1_r0_fu1/w2/resume_02",
            "s6_1_r0_fu1_w2_resume02_evidence_20260801.tar.gz",
            "E 盘 `LLMGuard-Handoff`",
            "APPROVED_TO_START / NOT EXECUTED",
            "call_count=0",
            "不得自动创建 `resume_03`",
            "APPROVED_TO_START / NOT COMPLETED / NOT ACCEPTED",
        ):
            with self.subTest(required=required):
                self.assertIn(required, combined)

        self.assertIn("不得覆盖、删除、改名或合并 resume_01", decisions)
        self.assertIn("H2-B 的唯一一次调用授权尚未使用", decisions)
        self.assertEqual(1, process.count("filter_documents("))

    def test_key_evidence_is_consistent_across_ledgers_and_fu1_process(self) -> None:
        human = TINGFENG_LEDGER.read_text(encoding="utf-8")
        texts = [
            AGENT_LEDGER.read_text(encoding="utf-8"),
            (STAGE_PROCESS_DIR / "S6.1-R0-FU1_work_process.md").read_text(encoding="utf-8"),
        ]
        identities = (
            "fcfa3f14c98e0103cb5a1de2f0449fa000d179e2e01d74baa6fec4b013503622",
            "17/17 PASS",
            "s6_1_r0_fu1_w2_models_20260801.tar.gz",
            "1222137698",
            "aa06e4cd03cb4d1eeb008514d81bc4d41e98f88614df046e008ac1f1544def45",
            "abe8c1493371369031bcb1e02acb754cf4e162fa",
            "86b5e0934494bd15c9632b12f734a8a67f723594",
            "438708922",
            "881643453",
            "1320352375",
            "19/19 PASS",
        )
        for identity in identities:
            for index, text in enumerate(texts):
                with self.subTest(identity=identity, document=index):
                    self.assertIn(identity, text)
        self.assertIn("Agent Experiment Ledger", human)
        self.assertIn("S6.1-R0-FU1", human)
        self.assertNotIn(identities[0], human)

    def test_new_paper1_docs_are_portable_utf8_lf_and_link_complete(self) -> None:
        new_docs = (
            PAPER1_README,
            TINGFENG_LEDGER,
            OWNER_REQUIREMENTS,
            RESEARCH_PLAN,
            AGENT_LEDGER,
            CONTEXT_ARCHIVE,
            P1_R1_PROTOCOL_CANDIDATE,
            PILOT2_RETURN_OWNER_CORRECTION,
            PILOT2_ANNOTATION_V2,
            *(STAGE_PROCESS_DIR.glob("*_work_process.md")),
        )
        link_pattern = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
        secret_pattern = re.compile(
            r"(?i)(?:api[_-]?key|access[_-]?token|secret|password)\s*[:=]\s*[A-Za-z0-9_\-]{12,}"
        )
        for path in new_docs:
            raw = path.read_bytes()
            text = raw.decode("utf-8")
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertFalse(raw.startswith(b"\xef\xbb\xbf"))
                self.assertNotIn(b"\r\n", raw)
                self.assertIsNone(WINDOWS_ABSOLUTE_PATH.search(text))
                self.assertIsNone(secret_pattern.search(text))
                for target in link_pattern.findall(text):
                    if "://" in target or target.startswith("#"):
                        continue
                    resolved = (path.parent / target.split("#", 1)[0]).resolve()
                    self.assertTrue(resolved.exists(), f"broken link {target} in {path}")

        forbidden_suffixes = {".tar", ".gz", ".zip", ".7z", ".bin", ".safetensors"}
        tracked_candidates = [path for path in RESEARCH.rglob("*") if path.is_file()]
        for path in tracked_candidates:
            self.assertFalse(
                any(path.name.lower().endswith(suffix) for suffix in forbidden_suffixes),
                f"raw artifact or model bundle under documentation tree: {path}",
            )

    def test_pilot2_owner_correction_preserves_history_and_blocks_auto_agreement(self) -> None:
        correction = PILOT2_RETURN_OWNER_CORRECTION.read_text(encoding="utf-8")
        combined = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (
                CURRENT_STATE,
                DECISION_REGISTER,
                MASTER_RECORD,
                EXECUTION_LOG,
                OWNER_REQUIREMENTS,
                TINGFENG_LEDGER,
                AGENT_LEDGER,
                CONTEXT_ARCHIVE,
                PILOT2_RETURN_OWNER_CORRECTION,
            )
        )
        for required in (
            "PODR-063",
            "OR-025",
            "REL-2026-0029",
            "PROTOCOL_AND_ANNOTATION_SCHEMA_BLOCKER",
            "RESOLVED_BY_OWNER_CONFIRMED_ACTUAL_DISTRIBUTION_ORDER",
            "OPEN_FOR_CORRECTION_AND_EVIDENCE_BINDING",
            "PENDING_SCHEMA_V2_REREVIEW_AND_RETURN_VALIDATION",
            "ANNOTATION_SCHEMA_V2 + A/B INDEPENDENT RE-REVIEW",
            "Auto Continue = `NO`",
        ):
            with self.subTest(required=required):
                self.assertIn(required, combined)

        self.assertIn("original coordinator registration CSV", correction)
        self.assertIn("original preflight inference", correction)
        self.assertIn("raw return remains immutable", correction)
        self.assertIn(
            "The original blind-contamination inference was based on incorrect registration metadata",
            correction,
        )
        self.assertNotIn("FORMAL_AGREEMENT = ESTABLISHED", combined)

    def test_pilot2_annotation_v2_is_ready_without_agreement_or_adjudication(self) -> None:
        combined = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (
                CURRENT_STATE,
                DECISION_REGISTER,
                MASTER_RECORD,
                EXECUTION_LOG,
                OWNER_REQUIREMENTS,
                TINGFENG_LEDGER,
                AGENT_LEDGER,
                CONTEXT_ARCHIVE,
                PILOT2_ANNOTATION_V2,
            )
        )
        for required in (
            "PODR-064",
            "OR-026",
            "REL-2026-0030",
            "PILOT2_ROUND1_RAW = PRESERVED_IMMUTABLE",
            "A_PHASE1_STRICT_BLINDNESS = OWNER_CONFIRMED_PRESERVED",
            "ANNOTATION_SCHEMA_V2 = IMPLEMENTED",
            "A_B_REREVIEW = READY_FOR_HUMAN_EXECUTION",
            "FORMAL_AGREEMENT_V2 = NOT_YET_ESTABLISHED",
            "ROUND1_RAW_MANIFEST",
            "Auto Continue = `NO`",
        ):
            with self.subTest(required=required):
                self.assertIn(required, combined)

        self.assertIn("version_relation_present = NO -> version_relation_correct = NOT_APPLICABLE", combined)
        self.assertIn("authority proposition expressed by the candidate", combined)
        self.assertNotIn("FORMAL_AGREEMENT_RECOVERED", combined)


if __name__ == "__main__":
    unittest.main()
