from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "docs" / "research"
STAGE = RESEARCH / "stage6_1_hidden_knowledge_poisoning"
WINDOWS_ABSOLUTE_PATH = re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/]")


def test_s6_1_lr1_control_plane_artifacts_exist_and_are_utf8() -> None:
    required = (
        RESEARCH / "paper_comparative_evidence_principle.md",
        STAGE / "README.md",
        STAGE / "paper1_research_route.md",
        STAGE / "paper1_benchmark_alignment_matrix.md",
        STAGE / "external_artifact_registry.md",
        STAGE / "baseline_reproduction_protocol.md",
        STAGE / "hardware_execution_policy.md",
        STAGE / "learning_notes.md",
    )

    for path in required:
        payload = path.read_bytes()
        assert payload
        assert not payload.startswith(b"\xef\xbb\xbf")
        payload.decode("utf-8")


def test_paper_first_principle_freezes_comparison_evidence_boundaries() -> None:
    text = (RESEARCH / "paper_comparative_evidence_principle.md").read_text(
        encoding="utf-8"
    )

    for required in (
        "Paper-First Comparative Evidence Principle",
        "Published Result",
        "Reproduced Result",
        "Our Method Result",
        "STRICT_COMPARISON_ELIGIBLE",
        "Safety、Utility、Efficiency、Reproducibility",
        "FORMAL_EXPERIMENT",
        "NOT STARTED",
    ):
        assert required in text


def test_external_matrix_has_required_fields_and_verified_sources() -> None:
    matrix = (STAGE / "paper1_benchmark_alignment_matrix.md").read_text(
        encoding="utf-8"
    )
    registry = (STAGE / "external_artifact_registry.md").read_text(encoding="utf-8")

    required_columns = (
        "paper",
        "venue",
        "year",
        "role_in_our_paper",
        "official_paper_url",
        "official_repo",
        "verified_commit/tag",
        "license",
        "datasets",
        "dataset_license",
        "attack",
        "defense",
        "retriever",
        "generator",
        "embedding model",
        "Top-K",
        "attack budget",
        "metrics",
        "published main results",
        "required GPU",
        "required RAM",
        "disk estimate",
        "original environment",
        "5090 compatibility issue",
        "reproduction status",
        "strict-comparison eligibility",
        "gap relative to our method",
        "unresolved questions",
    )
    header = next(line for line in matrix.splitlines() if line.startswith("| paper |"))
    for column in required_columns:
        assert f"| {column} " in header

    for required in (
        "f660d72174f06b13fae5163ce656e7b235db858f",
        "15b48d150f93711371eb8da22c211cd84a0cf4df",
        "e8f579743b23e0a3937076dcc0792fe29027cba3",
        "https://www.usenix.org/conference/usenixsecurity25/presentation/zou-poisonedrag",
        "https://aclanthology.org/2025.findings-acl.1263/",
        "https://aclanthology.org/2025.acl-long.230/",
        "LICENSE FILE NOT FOUND",
        "NOT_RUN",
    ):
        assert required in registry


def test_lr1_state_is_planning_only_and_preserves_formal_experiment_gate() -> None:
    state = (ROOT / "docs" / "governance" / "current_work_state.md").read_text(
        encoding="utf-8"
    )
    stage_readme = (STAGE / "README.md").read_text(encoding="utf-8")
    protocol = (STAGE / "baseline_reproduction_protocol.md").read_text(
        encoding="utf-8"
    )

    for text in (state, stage_readme):
        assert "S6.1-LR1" in text
        assert "COMPLETED_PENDING_HUMAN_ACCEPTANCE" in text
        assert "NOT STARTED" in text

    assert "REFERENCE_ONLY_DO_NOT_RUN" in protocol
    assert "不授权下载数据/模型" in protocol
    assert "S6.1-P1" in state
    assert "separate approval" in state


def test_new_research_docs_are_portable_and_do_not_claim_results() -> None:
    for path in STAGE.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        assert WINDOWS_ABSOLUTE_PATH.search(text) is None
        assert "REPRODUCTION_SUCCESS" not in text
        assert "OUR_METHOD_RESULT = COMPLETE" not in text
