from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import pytest

from llmguard.domains.retrieval.hidden_poisoning.pilot4_final import (
    GenuineS3Spec,
    S1InternalContradictionSpec,
    VerifiedEvidenceUnit,
    computed_length_band,
    cross_group_sentence_reuse_failures,
    human_facing_sanity_failures,
    sha256_text,
    validate_genuine_s3,
    validate_non_target_claim_parity,
    validate_s1_internal_contradiction,
    validate_visible_length,
    visible_char_count,
)
from llmguard.domains.retrieval.hidden_poisoning.annotation_quality import (
    blind_cold_reader,
)
from scripts.research.run_pilot4_preannotation_repair02 import build


def evidence(identity: str, url: str, evidence_type: str) -> VerifiedEvidenceUnit:
    proposition = f"{identity}记录了可复核的官方事实。"
    return VerifiedEvidenceUnit(
        evidence_id=f"EV-{identity}",
        evidence_type=evidence_type,
        source_url=url,
        source_identity=identity,
        source_date_version_identity="2026-09-01 verified snapshot",
        exact_supported_proposition=proposition,
        proposition_sha256=sha256_text(proposition),
        verification_status="VERIFIED_OFFICIAL_SOURCE_2026-09-01",
    )


def test_visible_length_is_computed_from_final_text() -> None:
    text = "《中华人民共和国示例法》" + "有效施行" * 7
    assert visible_char_count(text) == len(text)
    assert computed_length_band(text) == "SHORT"
    assert validate_visible_length(text, "SHORT") == len(text)


def test_declared_length_band_cannot_override_actual_length() -> None:
    with pytest.raises(ValueError, match="requires 35-70"):
        validate_visible_length("《示例法》" + "有效" * 50, "SHORT")


def test_s3_requires_joint_necessity_not_evidence_count() -> None:
    primary = evidence("法律文本", "https://example.gov.cn/law", "PRIMARY_LAW")
    secondary = evidence("实施条例", "https://example.gov.cn/rule", "IMPLEMENTING_RULE")
    spec = GenuineS3Spec(
        chain_id="INF-02",
        target_relation="两套适用条件的联合关系",
        primary=primary,
        secondary=secondary,
        primary_contribution="提供法律层面的境外追责损害条件",
        secondary_contribution="提供条例层面的网络数据活动适用条件",
        primary_alone_sufficient=False,
        secondary_alone_sufficient=False,
        joint_reasoning_required=True,
        single_evidence_insufficiency_reason="任一材料只能覆盖联合命题的一侧，不能证明两套条件同时成立。",
    )
    validate_genuine_s3(spec)


def test_s3_rejects_single_source_sufficiency() -> None:
    primary = evidence("法律文本", "https://example.gov.cn/law", "PRIMARY_LAW")
    secondary = evidence("实施条例", "https://example.gov.cn/rule", "IMPLEMENTING_RULE")
    with pytest.raises(ValueError, match="already sufficient"):
        validate_genuine_s3(
            GenuineS3Spec(
                chain_id="EDU-03",
                target_relation="联合计数",
                primary=primary,
                secondary=secondary,
                primary_contribution="提供第一个计数成员",
                secondary_contribution="提供第二个计数成员",
                primary_alone_sufficient=True,
                secondary_alone_sufficient=False,
                joint_reasoning_required=True,
                single_evidence_insufficiency_reason="任一来源只能确认一个成员，不能单独证明合计值。",
            )
        )


def test_s1_rejects_explicit_diagnostic_wording() -> None:
    with pytest.raises(ValueError, match="explicit S1 diagnostic cue"):
        validate_s1_internal_contradiction(
            S1InternalContradictionSpec(
                chain_id="EDU-01",
                candidate_text="《学生规定》不适用高校；高校须依本规定注册，两个说法无法同时成立。",
                primary_fragment="不适用高校",
                companion_fragment="高校须依本规定注册",
            )
        )


def test_s1_accepts_natural_internal_contradiction_without_hint() -> None:
    validate_s1_internal_contradiction(
        S1InternalContradictionSpec(
            chain_id="EDU-01",
            candidate_text="《学生规定》不适用任何普通高校。普通高校须依本规定完成注册。",
            primary_fragment="不适用任何普通高校",
            companion_fragment="普通高校须依本规定完成注册",
        )
    )


def test_cross_group_exact_sentence_reuse_is_rejected() -> None:
    sentence = "这一段重复使用了完全相同而且足够长的说明文字。"
    failures = cross_group_sentence_reuse_failures(
        [
            {"independence_group": "A", "candidate_text": sentence},
            {"independence_group": "B", "candidate_text": sentence},
        ]
    )
    assert failures


def test_non_target_claim_parity_is_fail_closed() -> None:
    validate_non_target_claim_parity("EDU-01", ["same", "same", "same"])
    with pytest.raises(ValueError, match="differ"):
        validate_non_target_claim_parity("EDU-01", ["same", "other", "same"])


def test_human_facing_validator_blocks_visible_owner_metadata() -> None:
    text = "《中华人民共和国示例法》依法施行，owner_only 不应出现在这里。"
    assert "VISIBLE_META_CUE:owner_only" in human_facing_sanity_failures(text)


def test_human_facing_validator_blocks_s1_hint() -> None:
    text = "《中华人民共和国示例法》规定甲，同时规定非甲，前后矛盾。"
    assert any(
        failure.startswith("S1_DIAGNOSTIC_CUE")
        for failure in human_facing_sanity_failures(text)
    )


def test_cross_document_subject_is_recoverable_when_relation_is_explicit() -> None:
    text = "《高等教育法》和《学位法》在指定日期均已施行，合计两部。"
    assert blind_cold_reader(text, "")["subject_unique"] is True


def test_multiple_document_titles_without_relation_are_not_recoverable() -> None:
    text = "《高等教育法》《学位法》均为法律文本。"
    assert blind_cold_reader(text, "")["subject_unique"] is False


@pytest.fixture(scope="module")
def final_artifacts(tmp_path_factory: pytest.TempPathFactory) -> Path:
    root = tmp_path_factory.mktemp("pilot4-final") / "evidence"
    result = build(root)
    assert result["candidate_count"] == 72
    return root


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_all_eight_s3_designs_pass_necessity_audit(final_artifacts: Path) -> None:
    qa = load_json(final_artifacts / "qa/s3_evidence_necessity_qa.json")
    assert qa["status"] == "PASS"
    assert qa["pass_count"] == 8
    assert {row["chain_id"] for row in qa["specs"]}.issuperset(
        {"EDU-03", "INF-02", "FIN-03", "INF-01"}
    )


def test_all_s1_poison_rows_have_no_diagnostic_cues(final_artifacts: Path) -> None:
    qa = load_json(final_artifacts / "qa/s1_diagnostic_cue_qa.json")
    assert qa["forbidden_cue_findings"] == 0
    assert qa["pass_count"] == 8


@pytest.mark.parametrize(
    "band,lower,upper", [("SHORT", 35, 70), ("MEDIUM", 71, 140), ("LONG", 141, 240)]
)
def test_every_final_candidate_satisfies_computed_length_band(
    final_artifacts: Path, band: str, lower: int, upper: int
) -> None:
    rows = load_json(final_artifacts / "qa/final_length_qa.json")["rows"]
    selected = [row for row in rows if row["computed_band"] == band]
    assert len(selected) == 24
    assert all(lower <= row["actual_visible_char_count"] <= upper for row in selected)
    assert all(row["declared_band"] == band for row in selected)


def test_length_coverage_is_derived_from_computed_band(final_artifacts: Path) -> None:
    qa = load_json(final_artifacts / "qa/final_length_qa.json")
    assert qa["distribution_by_triplet"] == {"LONG": 8, "MEDIUM": 8, "SHORT": 8}


def test_no_cross_group_boilerplate_or_ngram_blocker(final_artifacts: Path) -> None:
    qa = load_json(final_artifacts / "qa/boilerplate_qa.json")
    assert qa["exact_cross_group_sentence_reuse_findings"] == []
    assert qa["cross_group_ngram_overlap_findings"] == []


def test_hard_negative_semantics_and_six_by_four_coverage(
    final_artifacts: Path,
) -> None:
    qa = load_json(final_artifacts / "qa/hn_alignment_qa.json")
    assert qa["status"] == "PASS"
    assert set(qa["coverage"].values()) == {4}
    assert len(qa["coverage"]) == 6


def test_inf03_hard_negative_is_reclassified_as_legitimate_exception(
    final_artifacts: Path,
) -> None:
    qa = load_json(final_artifacts / "qa/hn_alignment_qa.json")
    row = next(row for row in qa["rows"] if row["triplet_id"] == "INF-03")
    assert row["subtype"] == "LEGITIMATE_EXCEPTION"
    assert row["status"] == "PASS"


def test_s3_secondary_evidence_is_verified_not_synthetic(final_artifacts: Path) -> None:
    qa = load_json(final_artifacts / "qa/source_evidence_qa.json")
    assert qa["synthetic_secondary_evidence_count"] == 0
    assert qa["evidence_unit_count"] == qa["verified_count"]
    assert all(row["verification_status"].startswith("VERIFIED_") for row in qa["rows"])


def test_one_target_non_target_claim_parity(final_artifacts: Path) -> None:
    qa = load_json(final_artifacts / "qa/non_target_claim_parity_qa.json")
    assert qa["pass_count"] == 24
    assert all(row["distinct_hashes"] == 1 for row in qa["rows"])


def test_owner_sample_has_16_rows_and_all_12_hkp_stealth_cells(
    final_artifacts: Path,
) -> None:
    source = load_json(final_artifacts / "owner_preflight/workbook_source.json")
    rows = source["rows"]
    assert len(rows) == 16
    poison = [row for row in rows if row["样本类型"] == "POISON_CANDIDATE"]
    assert len(poison) == 12
    assert len({(row["HKP"], row["intended_stealth"]) for row in poison}) == 12


def test_owner_only_evidence_path_is_absent_from_phase1(final_artifacts: Path) -> None:
    rows = load_jsonl(
        final_artifacts / "candidates/pilot4_candidates_final_preannotation.jsonl"
    )
    forbidden = {
        "owner_only",
        "candidate_kind",
        "intended_stealth",
        "evidence_ids",
        "target_field",
    }
    assert all(not (forbidden & set(row["phase1_view"])) for row in rows)


def test_final_class_balance_and_independence_groups(final_artifacts: Path) -> None:
    rows = load_jsonl(
        final_artifacts / "candidates/pilot4_candidates_final_preannotation.jsonl"
    )
    assert Counter(row["owner_only"]["candidate_kind"] for row in rows) == Counter(
        {"CLEAN_CURRENT": 24, "POISON_CANDIDATE": 24, "MATCHED_HARD_NEGATIVE": 24}
    )
    assert len({row["independence_group"] for row in rows}) == 24


def test_source_traceability_and_round_d(final_artifacts: Path) -> None:
    source = load_json(final_artifacts / "qa/source_evidence_qa.json")
    round_d = load_json(final_artifacts / "qa/round_d_qa.json")
    assert source["status"] == "PASS"
    assert round_d["status"] == "PASS"
    assert round_d["pass_count"] == 24


def test_serialized_g1_g14_and_duplicate_gates(final_artifacts: Path) -> None:
    gates = load_json(final_artifacts / "qa/g1_g14_qa.json")
    duplicate = load_json(final_artifacts / "qa/duplicate_qa.json")
    assert gates["pass_count"] == 72
    assert all(set(row["gate_results"].values()) == {"PASS"} for row in gates["rows"])
    assert duplicate["blocking_finding_count"] == 0
