from __future__ import annotations

import json
from pathlib import Path

import pytest

from llmguard.domains.retrieval.hidden_poisoning.external_blind_review import (
    MANUAL_FIELDS,
    TITLE_ORIGINS,
    adjacent_same_group_count,
    blind_review_id,
    deterministic_constrained_blind_order,
    deterministic_blind_order,
    evidence_should_swap,
    extract_html_title,
    lexical_duplicate_qa,
    order_profile,
    validate_packet_rows,
)
from scripts.research.build_pilot4_external_blind_packet import build
from scripts.research.prepare_pilot4_external_blind_owner_assets import (
    field_guide_cases,
)


def _rows() -> list[dict[str, object]]:
    return [
        {
            "blind_review_id": f"BR-{index:010X}",
            "candidate_text": f"《教学制度{index}》自2024年1月1日起施行。",
            "source_title": f"教学制度{index}",
            "phase1_questions": [
                {"field": field, "response": ""}
                for field in (
                    "text_naturalness",
                    "local_internal_conflict",
                    "phase1_issue",
                    "phase1_reason",
                )
            ],
            "evidence_pool": [
                {
                    "evidence_id": "E1",
                    "official_page_title": f"官方页面A{index}",
                    "official_source_url": f"https://example.gov/a/{index}",
                },
                {
                    "evidence_id": "E2",
                    "official_page_title": f"官方页面B{index}",
                    "official_source_url": f"https://example.gov/b/{index}",
                },
            ],
            "phase2_questions": [
                {"field": field, "response": ""}
                for field in (
                    "overall_fact_status",
                    "version_claim_status",
                    "authority_claim_status",
                    "minimum_external_evidence_needed",
                    "evidence_selection",
                    "phase2_issue",
                    "phase2_reason",
                )
            ],
        }
        for index in range(72)
    ]


def test_actual_html_title_is_source_backed() -> None:
    result = extract_html_title(
        "<html><head><title>某市公共数据管理办法</title></head></html>".encode(),
        "text/html; charset=utf-8",
    )
    assert result.display_title == "某市公共数据管理办法"
    assert result.title_origin == "HTML_TITLE"
    assert len(result.title_source_text_hash) == 64


def test_actual_html_title_survives_isolated_legacy_body_byte() -> None:
    result = extract_html_title(
        (
            b'<html><head><meta charset="utf-8"><title>'
            + "中华人民共和国政府信息公开条例".encode()
            + b"</title></head><body>legacy:\x81</body></html>"
        ),
        "text/html; charset=utf-8",
    )
    assert result.display_title == "中华人民共和国政府信息公开条例"
    assert result.title_origin == "HTML_TITLE"


def test_generic_portal_title_uses_actual_h1() -> None:
    result = extract_html_title(
        (
            "<html><head><title>中国政府网</title></head>"
            "<body><h1>某省科研经费管理办法</h1></body></html>"
        ).encode(),
        "text/html; charset=utf-8",
    )
    assert result.display_title == "某省科研经费管理办法"
    assert result.title_origin == "PAGE_H1"


def test_missing_actual_title_fails_closed() -> None:
    with pytest.raises(ValueError, match="SOURCE_TITLE_NEUTRALITY_BLOCKER"):
        extract_html_title(
            "<html><head><title>首页</title></head><body></body></html>".encode(),
            "text/html; charset=utf-8",
        )


@pytest.mark.parametrize(
    "forbidden",
    [
        "MANUAL_OVERRIDE",
        "OWNER_INTERPRETATION",
        "SOURCE_IDENTITY_FALLBACK",
        "SYNTHETIC_TITLE",
    ],
)
def test_title_origin_enum_excludes_unproven_sources(forbidden: str) -> None:
    assert forbidden not in TITLE_ORIGINS


def test_blind_id_is_stable_and_nonsequential() -> None:
    seed = bytes.fromhex("11" * 32)
    first = blind_review_id(seed, "internal-a")
    assert first == blind_review_id(seed, "internal-a")
    assert first != blind_review_id(seed, "internal-b")
    assert first.startswith("BR-") and len(first) == 13


def test_deterministic_order_has_no_adjacent_triplet() -> None:
    identities = [f"row-{index}" for index in range(72)]
    groups = {
        identity: f"group-{index // 3}" for index, identity in enumerate(identities)
    }
    order = deterministic_blind_order(identities, groups, bytes.fromhex("22" * 32))
    assert order == deterministic_blind_order(
        identities, groups, bytes.fromhex("22" * 32)
    )
    assert order != identities
    assert adjacent_same_group_count(order, groups) == 0


def test_constrained_order_limits_profile_runs() -> None:
    identities = [f"row-{index}" for index in range(24)]
    groups = {
        identity: f"group-{index // 3}" for index, identity in enumerate(identities)
    }
    profiles = {
        identity: {
            "class": f"class-{index % 3}",
            "domain": f"domain-{index % 4}",
        }
        for index, identity in enumerate(identities)
    }
    order = deterministic_constrained_blind_order(
        identities, groups, profiles, bytes(32)
    )
    assert adjacent_same_group_count(order, groups) == 0
    assert (
        max(
            order_profile([profiles[item][field] for item in order])["maximum_run"]
            for field in ("class", "domain")
        )
        <= 2
    )


def test_order_profile_detects_periodicity() -> None:
    profile = order_profile(["A", "B"] * 12)
    assert profile["exact_periods_2_to_12"] == [2, 4, 6, 8, 10, 12]


def test_evidence_order_uses_a_separate_stable_digest() -> None:
    seed = bytes.fromhex("33" * 32)
    assert evidence_should_swap(seed, "BR-ABCDEF1234") == evidence_should_swap(
        seed, "BR-ABCDEF1234"
    )


def test_valid_packet_has_72_unique_rows() -> None:
    qa = validate_packet_rows(_rows())
    assert qa == {
        "status": "PASS",
        "candidate_count": 72,
        "blind_id_unique_count": 72,
        "machine_semantic_answer_generation": 0,
    }


@pytest.mark.parametrize(
    "key",
    [
        "sample_id",
        "triplet_id",
        "owner_only",
        "candidate_kind",
        "target_field",
        "expected_contract",
    ],
)
def test_packet_rejects_private_or_design_key(key: str) -> None:
    rows = _rows()
    rows[0][key] = "leak"
    with pytest.raises(ValueError, match="ROW_SCHEMA|KEY_LEAKAGE"):
        validate_packet_rows(rows)


def test_packet_rejects_duplicate_evidence_url() -> None:
    rows = _rows()
    evidence = rows[0]["evidence_pool"]
    assert isinstance(evidence, list)
    evidence[1]["official_source_url"] = evidence[0]["official_source_url"]
    with pytest.raises(ValueError, match="EVIDENCE_DUPLICATE"):
        validate_packet_rows(rows)


def test_packet_rejects_nonempty_result() -> None:
    rows = _rows()
    questions = rows[0]["phase1_questions"]
    assert isinstance(questions, list)
    questions[0]["response"] = "NATURAL"
    with pytest.raises(ValueError, match="NONEMPTY_RESPONSE"):
        validate_packet_rows(rows)


def test_cross_group_duplicate_gate_passes_parallel_matched_cases() -> None:
    qa = lexical_duplicate_qa(
        ["《甲办法》规定期限为十日。", "《甲办法》规定期限为十一日。"],
        ["same", "same"],
    )
    assert qa["status"] == "PASS"


def test_exact_duplicate_gate_fails_even_within_group() -> None:
    qa = lexical_duplicate_qa(["同一文本", "同一文本"], ["same", "same"])
    assert qa["status"] == "BLOCKED"
    assert qa["exact_duplicate_pair_count"] == 1


def test_field_guide_represents_all_manual_fields() -> None:
    cases = field_guide_cases()
    assert {row["field"] for row in cases} == set(MANUAL_FIELDS)


@pytest.mark.parametrize(
    "field",
    [
        "text_naturalness",
        "local_internal_conflict",
        "phase1_issue",
        "overall_fact_status",
        "version_claim_status",
        "authority_claim_status",
        "minimum_external_evidence_needed",
        "evidence_selection",
        "phase2_issue",
    ],
)
def test_each_enum_field_has_six_real_cases(field: str) -> None:
    assert sum(row["field"] == field for row in field_guide_cases()) >= 6


def test_reason_fields_include_good_bad_and_forbidden_cases() -> None:
    cases = field_guide_cases()
    for field in ("phase1_reason", "phase2_reason"):
        categories = {row["category"] for row in cases if row["field"] == field}
        assert categories == {"GOOD_REASON", "BAD_TOO_VAGUE", "FORBIDDEN"}


def test_field_guide_contains_no_definition_template_placeholder() -> None:
    serialized = json.dumps(field_guide_cases(), ensure_ascii=False).casefold()
    assert "use the field definition for" not in serialized


def test_minimum_evidence_examples_separate_actual_use() -> None:
    rows = [
        row
        for row in field_guide_cases()
        if row["field"] == "minimum_external_evidence_needed"
    ]
    assert any(
        "实际打开" in row["fixture"] and row["decision"] == "ONE_OFFICIAL_EVIDENCE"
        for row in rows
    )
    assert {row["decision"] for row in rows} == {
        "ONE_OFFICIAL_EVIDENCE",
        "MULTI_EVIDENCE_OR_VERSION_CHAIN",
        "NOT_APPLICABLE",
    }


def test_evidence_selection_examples_cover_one_and_multi_boundaries() -> None:
    rows = [row for row in field_guide_cases() if row["field"] == "evidence_selection"]
    boundary = [row for row in rows if row["category"] == "BOUNDARY"]
    assert len(boundary) == 2
    assert all(row["decision"] == "E1+E2" for row in boundary)


def test_candidate_defect_examples_cover_phase_boundary() -> None:
    cases = field_guide_cases()
    decisions = {row["decision"] for row in cases}
    assert "MISSING_CONTEXT" in decisions
    assert "AMBIGUOUS_REFERENCE" in decisions
    assert "LATE_DISCOVERED_CANDIDATE_DEFECT" in decisions


def test_naturalness_case_is_independent_of_truth() -> None:
    cases = field_guide_cases()
    assert any(
        row["field"] == "text_naturalness"
        and row["decision"] == "NATURAL"
        and "事实可能错误" in row["explanation"]
        for row in cases
    )


def test_external_builder_source_contains_no_compiled_answer_sets() -> None:
    source = Path("scripts/research/build_pilot4_external_blind_packet.py").read_text(
        encoding="utf-8"
    )
    for token in (
        "LOCAL_CONFLICT_IDS",
        "FACTUAL_CONFLICT_IDS",
        "MULTI_EVIDENCE_IDS",
        "LEGITIMATE_HISTORY_IDS",
        "VERSION_INCORRECT_IDS",
        "AUTHORITY_INCORRECT_IDS",
        "expected_contract_from_owner",
    ):
        assert token not in source


def test_external_builder_creates_four_unfilled_files(tmp_path: Path) -> None:
    input_path = tmp_path / "input.jsonl"
    input_path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in _rows()),
        encoding="utf-8",
    )
    cases_path = tmp_path / "cases.json"
    cases_path.write_text(
        json.dumps(field_guide_cases(), ensure_ascii=False), encoding="utf-8"
    )
    output = tmp_path / "external"
    result = build(input_path, cases_path, output)
    assert result["review_result_filled_count"] == 0
    assert {path.name for path in output.iterdir()} == {
        "PILOT4_EXTERNAL_BLIND_REVIEW_PACKET.md",
        "PILOT4_EXTERNAL_BLIND_REVIEW_PACKET.jsonl",
        "PILOT4_EXTERNAL_BLIND_FIELD_GUIDE.md",
        "PILOT4_EXTERNAL_BLIND_REVIEW_TEMPLATE.csv",
    }
    assert (
        len(
            (output / "PILOT4_EXTERNAL_BLIND_REVIEW_TEMPLATE.csv")
            .read_text(encoding="utf-8-sig")
            .splitlines()
        )
        == 73
    )
