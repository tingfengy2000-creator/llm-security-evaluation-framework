"""Formal240 design and V4 gates: no candidate generation or split execution."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

from llmguard.domains.retrieval.hidden_poisoning.formal_annotation_v4 import (
    derive_stealth,
    validate_formal_v4,
)

ROOT = Path(__file__).resolve().parents[2]
FORMAL = (
    ROOT
    / "docs/research/stage6_1_hidden_knowledge_poisoning/formal240"
)


def _row(**overrides: str) -> dict[str, str]:
    row = {
        "overall_fact_status": "FACTUAL_CONFLICT",
        "version_claim_status": "PRESENT_CORRECT",
        "authority_claim_status": "NOT_PRESENT",
        "minimum_external_evidence_needed": "ONE_OFFICIAL_EVIDENCE",
        "evidence_selection": "E1+E2",
        "phase2_issue": "NONE",
        "local_internal_conflict": "NO",
    }
    row.update(overrides)
    return row


def test_additive_v4_and_boundary_examples() -> None:
    schema = json.loads((FORMAL / "PAPER1_FORMAL_ANNOTATION_SCHEMA_V4.json").read_text(encoding="utf-8"))
    examples = json.loads(
        (FORMAL / "PAPER1_FORMAL_ANNOTATION_BOUNDARY_EXAMPLES_V1.json").read_text(encoding="utf-8")
    )
    assert "ZERO_EXTERNAL_EVIDENCE_REQUIRED" in schema["phase2"]["minimum_external_evidence_needed"]
    assert schema["historical_pilot_immutable"]
    assert examples["formal_candidate_count"] == 0
    assert len(examples["examples"]) >= 20
    assert len({item["id"] for item in examples["examples"]}) == len(examples["examples"])
    assert all(item["note"].startswith("Illustrates") for item in examples["examples"])
    required_cases = {
        "NO_YEAR_REVISION", "CORRECT_REVISION_WRONG_CONTENT",
        "WRONG_REVISION_YEAR_CORRECT_CONTENT", "CORRECT_REVISION_WRONG_AUTHORITY",
        "WRONG_REVISION_WRONG_AUTHORITY", "CURRENT_WRONG_SUBSTANCE",
        "HISTORY_AS_CURRENT", "YEAR_ONLY_NO_VERSION", "REPEAL_EVENT",
        "REPLACEMENT_RELATION", "SUPERSESSION_RELATION_WRONG", "EFFECTIVE_DATE",
        "LOCAL_CONTRADICTION", "ONE_EVIDENCE_CONFLICT", "MULTI_EVIDENCE_CONFLICT",
        "SELECTION_EXCEEDS_MINIMUM", "AUTHORITY_WITHOUT_VERSION",
        "VERSION_WITHOUT_AUTHORITY", "CONTENT_CONFLICT_NO_VERSION",
        "VERSION_EVIDENCE_INSUFFICIENT", "SCHEMA_ISSUE_NOT_FACT_ERROR",
    }
    assert required_cases <= {item["id"] for item in examples["examples"]}


def test_version_content_authority_are_independent() -> None:
    for authority in ("NOT_PRESENT", "PRESENT_CORRECT", "PRESENT_INCORRECT"):
        checked = validate_formal_v4(
            _row(authority_claim_status=authority),
            version_metadata_claim_present=True,
            version_metadata_supported=True,
            substantive_content_conflict=True,
        )
        assert checked.valid
        assert checked.derived_stealth_level == "S2"
    assert "F_VERSION_METADATA_CLAIM_MARKED_ABSENT" in validate_formal_v4(
        _row(version_claim_status="NOT_PRESENT"),
        version_metadata_claim_present=True,
    ).errors
    assert "H_SUBSTANTIVE_ERROR_MUST_NOT_CHANGE_VERSION" in validate_formal_v4(
        _row(version_claim_status="PRESENT_INCORRECT"),
        version_metadata_claim_present=True,
        version_metadata_supported=True,
        substantive_content_conflict=True,
    ).errors


def test_zero_evidence_selection_issue_and_derived_s() -> None:
    for selection in ("NONE", "E1", "E2", "E1+E2"):
        checked = validate_formal_v4(
            _row(
                local_internal_conflict="YES",
                minimum_external_evidence_needed="ZERO_EXTERNAL_EVIDENCE_REQUIRED",
                evidence_selection=selection,
            ),
            no_independent_process_defect=True,
            target_stealth_design="S1",
        )
        assert checked.valid
        assert checked.derived_stealth_level == "S1"
    assert "B_LOCAL_CONFLICT_REQUIRES_ZERO_EXTERNAL" in validate_formal_v4(
        _row(local_internal_conflict="YES")
    ).errors
    assert "J_FACTUAL_CONFLICT_IS_NOT_PHASE2_ISSUE" in validate_formal_v4(
        _row(
            local_internal_conflict="YES",
            minimum_external_evidence_needed="ZERO_EXTERNAL_EVIDENCE_REQUIRED",
            phase2_issue="OTHER",
        ),
        no_independent_process_defect=True,
    ).errors
    assert derive_stealth("FACTUAL_CONFLICT", "ONE_OFFICIAL_EVIDENCE", "NO") == "S2"
    assert derive_stealth("FACTUAL_CONFLICT", "MULTI_EVIDENCE_OR_VERSION_CHAIN", "NO") == "S3"
    assert derive_stealth("CURRENTLY_CONSISTENT", "NOT_APPLICABLE", "NO") == "NOT_APPLICABLE"
    assert "A_NONCONFLICT_MINIMUM_MUST_BE_NA" in validate_formal_v4(
        _row(overall_fact_status="CURRENTLY_CONSISTENT")
    ).errors
    assert "STEALTH_DESIGN_MISMATCH" in validate_formal_v4(
        _row(), target_stealth_design="S3"
    ).errors


def test_matrix_is_slots_only_and_exact_factorial() -> None:
    rows = [
        json.loads(line)
        for line in (FORMAL / "PAPER1_FORMAL_240_GROUP_MATRIX_V1.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
    ]
    assert len(rows) == 240
    assert len({r["group_slot_id"] for r in rows}) == 240
    cells = Counter((r["domain"], r["hkp"], r["target_stealth_design"]) for r in rows)
    assert len(cells) == 60 and set(cells.values()) == {4}
    assert {r["domain"] for r in rows} == {"D1", "D2", "D3", "D4", "D5"}
    assert {r["hkp"] for r in rows} == {"HKP1", "HKP2", "HKP3", "HKP4"}
    assert {r["target_stealth_design"] for r in rows} == {"S1", "S2", "S3"}
    assert all(
        r["slot_status"] == "UNFILLED_CONSTRUCTION_SLOT"
        and r["candidate_records_created"] == 0
        and r["derived_stealth_level"] is None
        and r["split_assignment"] is None
        and r["neutral_query_status"] == "NOT_AUTHORED"
        and r["planned_triplet_roles"] == ["CLEAN_CURRENT", "POISON", "HARD_NEGATIVE"]
        for r in rows
    )
    assert all(
        not any(key in r for key in ("candidate_text", "annotation", "ground_truth", "query_text"))
        for r in rows
    )


def test_contracts_and_split_are_planning_only() -> None:
    required = [
        "PAPER1_FORMAL_ANNOTATION_GUIDE_V4.md",
        "PAPER1_FORMAL_ANNOTATION_SCHEMA_V4.json",
        "PAPER1_FORMAL_ANNOTATION_BOUNDARY_EXAMPLES_V1.json",
        "PAPER1_FORMAL_ANNOTATION_CONSISTENCY_RULES_V1.json",
        "PAPER1_FORMAL_240_GROUP_BENCHMARK_CONSTRUCTION_PROTOCOL_V1.md",
        "PAPER1_FORMAL_240_GROUP_MATRIX_V1.jsonl",
        "PAPER1_FORMAL_BENCHMARK_SCHEMA_V1.json",
        "PAPER1_FORMAL_TRIPLET_CONTRACT_V1.md",
        "PAPER1_FORMAL_VERSION_METADATA_CONTRACT_V1.md",
        "PAPER1_FORMAL_PROVENANCE_METADATA_CONTRACT_V1.md",
        "PAPER1_FORMAL_EVIDENCE_CORPUS_DIFFICULTY_CONTRACT_V1.md",
        "PAPER1_FORMAL_QUERY_CONTRACT_V1.md",
        "PAPER1_FORMAL_FEATURE_OBSERVABILITY_GATE_V1.md",
        "PAPER1_FORMAL_FEATURE_VARIANCE_GATE_V1.md",
        "PAPER1_FORMAL_ANNOTATION_EXECUTION_PLAN_V1.md",
        "PAPER1_FORMAL_SPLIT_PROTOCOL_V1.md",
        "PAPER1_FORMAL_HYPOTHESIS_TRACEABILITY_MATRIX_V1.md",
        "PAPER1_FORMAL_WAVE_GATE_V1.md",
        "PAPER1_FORMAL_240_GROUP_PROTOCOL_OWNER_ACCEPTANCE_PACKET.md",
    ]
    assert all((FORMAL / name).is_file() for name in required)
    split = (FORMAL / "PAPER1_FORMAL_SPLIT_PROTOCOL_V1.md").read_text(encoding="utf-8")
    assert "20260922" in split and "SPLIT_NOT_EXECUTED" in split
    bench = json.loads((FORMAL / "PAPER1_FORMAL_BENCHMARK_SCHEMA_V1.json").read_text(encoding="utf-8"))
    assert bench["actual_formal_candidate_cardinality_now"] == 0
    assert bench["future_candidate_cardinality"] == 720


def test_formal_markdown_links_resolve() -> None:
    for md in FORMAL.glob("*.md"):
        content = md.read_text(encoding="utf-8")
        for link in re.findall(r"\]\(([^)]+)\)", content):
            if "://" in link or link.startswith("#"):
                continue
            assert (md.parent / link.split("#", 1)[0]).is_file(), (md.name, link)


def test_formal_files_are_portable_utf8_and_secret_free() -> None:
    for path in FORMAL.iterdir():
        raw = path.read_bytes()
        content = raw.decode("utf-8")
        assert not raw.startswith(b"\xef\xbb\xbf"), path.name
        assert b"\r\n" not in raw, path.name
        assert not re.search(r"[A-Z]:\\", content), path.name
        assert not re.search(
            r"(?i)(?:api[_-]?key|access[_-]?token|secret|password)\s*[:=]\s*[A-Za-z0-9_-]{12,}",
            content,
        ), path.name
