from __future__ import annotations

import json
from pathlib import Path
import csv
from io import StringIO

import pytest

from llmguard.domains.retrieval.hidden_poisoning.external_blind_review import (
    MANUAL_FIELDS,
    PHASE1_FIELDS,
    PHASE1_RETURN_FIELDS,
    PHASE2_FIELDS,
    PHASE2_RELEASE_REQUIREMENTS,
    assert_phase2_release_allowed,
    TITLE_ORIGINS,
    adjacent_same_group_count,
    blind_review_id,
    deterministic_constrained_blind_order,
    deterministic_blind_order,
    evidence_should_swap,
    extract_html_title,
    lexical_duplicate_qa,
    lock_phase1_raw_return,
    order_profile,
    validate_packet_rows,
    validate_phase1_packet_rows,
    validate_phase1_raw_return,
    validate_phase2_packet_rows,
)
from scripts.research.lock_pilot4_external_phase1_return import (
    build as build_phase1_return_lock,
)
from scripts.research.build_pilot4_external_blind_phase_packets import (
    build as build_phase_packets,
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


def _phase1_rows() -> list[dict[str, object]]:
    return [
        {
            "blind_review_id": row["blind_review_id"],
            "candidate_text": row["candidate_text"],
            "source_title": row["source_title"],
            **{field: "" for field in PHASE1_FIELDS},
        }
        for row in _rows()
    ]


def _phase2_rows() -> list[dict[str, object]]:
    return [
        {
            "blind_review_id": row["blind_review_id"],
            "candidate_text": row["candidate_text"],
            "source_title": row["source_title"],
            "evidence_pool": row["evidence_pool"],
            **{field: "" for field in PHASE2_FIELDS},
        }
        for row in _rows()
    ]


def _fake_prior(tmp_path: Path) -> Path:
    prior = tmp_path / "prior"
    external = prior / "external_blind_review"
    external.mkdir(parents=True)
    (external / "PILOT4_EXTERNAL_BLIND_REVIEW_PACKET.jsonl").write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in _rows()),
        encoding="utf-8",
    )
    staging = prior / "staging"
    staging.mkdir()
    (staging / "field_guide_cases.json").write_text(
        json.dumps(field_guide_cases(), ensure_ascii=False), encoding="utf-8"
    )
    owner = prior / "owner_only"
    owner.mkdir()
    mapping = owner / "blind_review_identity_mapping.json"
    mapping.write_text('{"classification":"OWNER_ONLY"}\n', encoding="utf-8")
    digest = __import__("hashlib").sha256(mapping.read_bytes()).hexdigest()
    (owner / "blind_review_identity_mapping.sha256").write_text(
        f"{digest}  {mapping.name}\n", encoding="utf-8"
    )
    title = prior / "title_provenance"
    title.mkdir()
    records = [
        {"blind_review_id": row["blind_review_id"], "evidence_id": item["evidence_id"]}
        for row in _rows()
        for item in row["evidence_pool"]
    ]
    (title / "evidence_display_title_records.json").write_text(
        json.dumps({"visible_slot_count": 144, "records": records}), encoding="utf-8"
    )
    qa = prior / "qa"
    qa.mkdir()
    (qa / "blind_order_leakage_qa.json").write_text(
        json.dumps(
            {
                "status": "PASS",
                "matched_triplet_adjacency_count": 0,
                "class_periodicity": {"exact_periods_2_to_12": []},
                "hkp_periodicity": {"exact_periods_2_to_12": []},
                "stealth_periodicity": {"exact_periods_2_to_12": []},
                "domain_periodicity": {"exact_periods_2_to_12": []},
            }
        ),
        encoding="utf-8",
    )
    return prior


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


def test_phase1_packet_contains_no_phase2_field() -> None:
    serialized = json.dumps(_phase1_rows(), ensure_ascii=False)
    assert all(field not in serialized for field in PHASE2_FIELDS)


def test_phase1_packet_url_count_is_zero() -> None:
    qa = validate_phase1_packet_rows(_phase1_rows())
    assert qa["evidence_url_count"] == 0


def test_phase1_packet_evidence_title_count_is_zero() -> None:
    qa = validate_phase1_packet_rows(_phase1_rows())
    assert qa["evidence_title_count"] == qa["evidence_id_count"] == 0


def test_phase1_validator_rejects_phase2_key() -> None:
    rows = _phase1_rows()
    rows[0]["overall_fact_status"] = ""
    with pytest.raises(ValueError, match="PHASE1_PACKET_ROW_SCHEMA"):
        validate_phase1_packet_rows(rows)


def test_phase2_packet_has_two_distinct_evidence_slots() -> None:
    qa = validate_phase2_packet_rows(_phase2_rows())
    assert qa["evidence_slots"] == 144
    assert qa["e1_e2_distinct"] == "72/72"


def test_phase2_release_fails_without_locked_phase1_return() -> None:
    with pytest.raises(ValueError, match="PHASE2_RELEASE_GATE_BLOCKER"):
        assert_phase2_release_allowed({})


def test_phase2_release_requires_all_lock_and_triage_facts() -> None:
    gate = {name: True for name in PHASE2_RELEASE_REQUIREMENTS}
    assert assert_phase2_release_allowed(gate) == "PHASE2_RELEASE_APPROVED"
    gate["PHASE1_RETURN_HASH_LOCKED"] = False
    with pytest.raises(ValueError, match="PHASE1_RETURN_HASH_LOCKED"):
        assert_phase2_release_allowed(gate)
    gate["PHASE1_RETURN_HASH_LOCKED"] = True
    gate["PHASE1_CANDIDATE_DEFECT_TRIAGE_RESOLVED"] = False
    with pytest.raises(ValueError, match="PHASE1_CANDIDATE_DEFECT_TRIAGE_RESOLVED"):
        assert_phase2_release_allowed(gate)


def test_phase1_raw_return_is_byte_locked_and_non_overwritable(tmp_path: Path) -> None:
    ids = [str(row["blind_review_id"]) for row in _phase1_rows()]
    stream = StringIO()
    writer = csv.DictWriter(stream, fieldnames=PHASE1_RETURN_FIELDS)
    writer.writeheader()
    for opaque_id in ids:
        writer.writerow(
            {
                "blind_review_id": opaque_id,
                "text_naturalness": "NATURAL",
                "local_internal_conflict": "NO",
                "phase1_issue": "NONE",
                "phase1_reason": "The shown wording is complete and internally coherent.",
            }
        )
    raw = stream.getvalue().encode("utf-8")
    destination = tmp_path / "PILOT4_EXTERNAL_BLIND_PHASE1_RETURN.csv"
    digest = lock_phase1_raw_return(raw, ids, destination)
    assert destination.read_bytes() == raw
    assert digest in destination.with_suffix(".csv.sha256").read_text(encoding="utf-8")
    with pytest.raises(FileExistsError):
        lock_phase1_raw_return(raw, ids, destination)


def test_phase1_return_rejects_duplicate_identity(tmp_path: Path) -> None:
    ids = [str(row["blind_review_id"]) for row in _phase1_rows()]
    header = ",".join(PHASE1_RETURN_FIELDS) + "\n"
    returned = ids[:-1] + [ids[0]]
    body = "\n".join(f"{item},NATURAL,NO,NONE,reason" for item in returned)
    with pytest.raises(ValueError, match="PHASE1_RETURN_72_72"):
        lock_phase1_raw_return((header + body).encode(), ids, tmp_path / "raw.csv")


def test_phase1_return_accepts_reordered_complete_identity_set(tmp_path: Path) -> None:
    ids = [str(row["blind_review_id"]) for row in _phase1_rows()]
    header = ",".join(PHASE1_RETURN_FIELDS) + "\n"
    body = "\n".join(f"{item},NATURAL,NO,NONE,reason" for item in reversed(ids))
    destination = tmp_path / "raw.csv"
    lock_phase1_raw_return((header + body).encode(), ids, destination)
    assert destination.is_file()


def test_phase1_lock_refuses_existing_sidecar_before_raw_write(tmp_path: Path) -> None:
    ids = [str(row["blind_review_id"]) for row in _phase1_rows()]
    header = ",".join(PHASE1_RETURN_FIELDS) + "\n"
    body = "\n".join(f"{item},NATURAL,NO,NONE,reason" for item in ids)
    destination = tmp_path / "raw.csv"
    destination.with_suffix(".csv.sha256").write_text("occupied", encoding="utf-8")
    with pytest.raises(FileExistsError, match="LOCK_ALREADY_EXISTS"):
        lock_phase1_raw_return((header + body).encode(), ids, destination)
    assert not destination.exists()


def _phase1_return_bytes() -> tuple[bytes, dict[str, str]]:
    rows = _phase1_rows()
    expected_issues = {
        str(rows[index]["blind_review_id"]): (
            "AMBIGUOUS_REFERENCE" if index % 2 == 0 else "MISSING_CONTEXT"
        )
        for index in range(5)
    }
    stream = StringIO()
    writer = csv.DictWriter(stream, fieldnames=PHASE1_RETURN_FIELDS)
    writer.writeheader()
    for index, packet_row in enumerate(rows):
        opaque_id = str(packet_row["blind_review_id"])
        issue = expected_issues.get(opaque_id, "NONE")
        writer.writerow(
            {
                "blind_review_id": opaque_id,
                "text_naturalness": (
                    "MINOR_ISSUE"
                    if index < 8
                    else "UNNATURAL"
                    if index == 8
                    else "NATURAL"
                ),
                "local_internal_conflict": "YES" if index < 6 else "NO",
                "phase1_issue": issue,
                "phase1_reason": "reviewer reason" if index < 6 else "",
            }
        )
    return stream.getvalue().encode("utf-8"), expected_issues


def test_phase1_return_reason_is_conditional_not_globally_required() -> None:
    raw, _ = _phase1_return_bytes()
    ids = [str(row["blind_review_id"]) for row in _phase1_rows()]
    validation = validate_phase1_raw_return(raw, ids)
    assert validation["required_reason_rows"] == 6
    assert validation["missing_required_reason_count"] == 0
    assert validation["issue_row_count"] == 5
    assert validation["non_natural_row_count"] == 9
    assert validation["local_yes_row_count"] == 6


def test_phase1_return_rejects_missing_conditionally_required_reason() -> None:
    raw, _ = _phase1_return_bytes()
    text = raw.decode("utf-8").replace("reviewer reason", "", 1)
    ids = [str(row["blind_review_id"]) for row in _phase1_rows()]
    with pytest.raises(ValueError, match="PHASE1_RETURN_REASON_BLOCKER"):
        validate_phase1_raw_return(text.encode("utf-8"), ids)


def test_phase1_return_lock_builds_blind_only_defect_gate(tmp_path: Path) -> None:
    packet = tmp_path / "PILOT4_EXTERNAL_BLIND_PHASE1_PACKET.jsonl"
    packet.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in _phase1_rows()),
        encoding="utf-8",
    )
    raw, expected_issues = _phase1_return_bytes()
    source = tmp_path / "source.csv"
    copy = tmp_path / "copy.csv"
    source.write_bytes(raw)
    copy.write_bytes(raw)
    output = tmp_path / "locked"
    result = build_phase1_return_lock(
        source,
        packet,
        output,
        expected_sha256=__import__("hashlib").sha256(raw).hexdigest(),
        expected_issue_rows=expected_issues,
        corroborating_copies=[copy],
    )
    assert result["issue_row_count"] == 5
    assert result["non_natural_row_count"] == 9
    assert result["local_yes_row_count"] == 6
    assert result["phase2_release_approved"] is False
    assert (
        output / "raw" / "PILOT4_EXTERNAL_BLIND_PHASE1_RETURN.csv"
    ).read_bytes() == raw
    gate = json.loads(
        (output / "qa" / "phase2_release_gate.json").read_text(encoding="utf-8")
    )
    assert gate["requirements"]["PHASE1_CANDIDATE_DEFECT_TRIAGE_RESOLVED"] is False
    assert gate["release_approved"] is False
    triage = (
        output / "owner_preflight" / "PILOT4_PHASE1_BLIND_DEFECT_TRIAGE.md"
    ).read_text(encoding="utf-8")
    assert triage.count("\n| BR-") == 5
    assert "sample_id" not in triage
    manifest = json.loads(
        (output / "manifest" / "manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["expected_contract_loaded"] is False
    assert manifest["identity_mapping_unlocked"] is False
    assert manifest["phase2_released"] is False


def test_phase_builder_creates_separated_release_gated_artifacts(
    tmp_path: Path,
) -> None:
    prior = _fake_prior(tmp_path)
    before = {
        path.relative_to(prior).as_posix(): path.read_bytes()
        for path in prior.rglob("*")
        if path.is_file()
    }
    output = tmp_path / "separated"
    result = build_phase_packets(prior, output)
    assert result["phase1_rows"] == result["phase2_rows"] == 72
    assert result["phase2_release_approved"] is False
    assert (
        output / "external_blind_review" / "PILOT4_EXTERNAL_BLIND_PHASE1_PACKET.md"
    ).is_file()
    assert (
        output
        / "external_blind_review"
        / "withheld_phase2"
        / "PILOT4_EXTERNAL_BLIND_PHASE2_PACKET.md"
    ).is_file()
    after = {
        path.relative_to(prior).as_posix(): path.read_bytes()
        for path in prior.rglob("*")
        if path.is_file()
    }
    assert before == after


def test_phase_builder_preserves_cross_phase_identity_and_order(tmp_path: Path) -> None:
    output = tmp_path / "separated"
    build_phase_packets(_fake_prior(tmp_path), output)
    phase1 = [
        json.loads(line)
        for line in (
            output
            / "external_blind_review"
            / "PILOT4_EXTERNAL_BLIND_PHASE1_PACKET.jsonl"
        )
        .read_text(encoding="utf-8")
        .splitlines()
    ]
    phase2 = [
        json.loads(line)
        for line in (
            output
            / "external_blind_review"
            / "withheld_phase2"
            / "PILOT4_EXTERNAL_BLIND_PHASE2_PACKET.jsonl"
        )
        .read_text(encoding="utf-8")
        .splitlines()
    ]
    assert [row["blind_review_id"] for row in phase1] == [
        row["blind_review_id"] for row in phase2
    ]


def test_phase1_external_files_exclude_phase2_and_identity_leakage(
    tmp_path: Path,
) -> None:
    output = tmp_path / "separated"
    build_phase_packets(_fake_prior(tmp_path), output)
    external = output / "external_blind_review"
    text = "\n".join(
        path.read_text(encoding="utf-8-sig" if path.suffix == ".csv" else "utf-8")
        for path in external.iterdir()
        if path.is_file() and "INSTRUCTIONS" not in path.name
    )
    assert "sample_id" not in text
    assert "official_source_url" not in text
    assert all(field not in text for field in PHASE2_FIELDS)


def test_phase1_guide_has_no_phase2_evidence_or_s_level_hint(tmp_path: Path) -> None:
    output = tmp_path / "separated"
    build_phase_packets(_fake_prior(tmp_path), output)
    guide = (
        output / "external_blind_review" / "PILOT4_EXTERNAL_BLIND_PHASE1_GUIDE.md"
    ).read_text(encoding="utf-8")
    assert "Phase2" not in guide
    assert "Evidence Pool" not in guide
    assert "S2" not in guide and "S3" not in guide


def test_phase2_external_packet_excludes_private_and_expected_keys(
    tmp_path: Path,
) -> None:
    output = tmp_path / "separated"
    build_phase_packets(_fake_prior(tmp_path), output)
    text = (
        output
        / "external_blind_review"
        / "withheld_phase2"
        / "PILOT4_EXTERNAL_BLIND_PHASE2_PACKET.jsonl"
    ).read_text(encoding="utf-8")
    for token in (
        "sample_id",
        "triplet_id",
        "target_field",
        "expected_answer",
        "owner_decision",
        "source_role",
        "source_type",
    ):
        assert token not in text


def test_combined_packet_is_marked_superseded_without_mutation(tmp_path: Path) -> None:
    output = tmp_path / "separated"
    prior = _fake_prior(tmp_path)
    original = (
        prior / "external_blind_review" / "PILOT4_EXTERNAL_BLIND_REVIEW_PACKET.jsonl"
    ).read_bytes()
    build_phase_packets(prior, output)
    governance = json.loads(
        (output / "governance" / "combined_packet_supersession.json").read_text(
            encoding="utf-8"
        )
    )
    assert governance["status"] == "SUPERSEDED_FOR_REVIEW_BY_PHASE_SEPARATED_PROTOCOL"
    assert (
        prior / "external_blind_review" / "PILOT4_EXTERNAL_BLIND_REVIEW_PACKET.jsonl"
    ).read_bytes() == original


def test_phase_builder_binds_frozen_zero_adjacency_order(tmp_path: Path) -> None:
    output = tmp_path / "separated"
    build_phase_packets(_fake_prior(tmp_path), output)
    qa = json.loads(
        (output / "qa" / "frozen_order_and_pattern_qa.json").read_text(encoding="utf-8")
    )
    assert qa["same_frozen_order_reused"] is True
    assert qa["matched_triplet_adjacency_count"] == 0
