from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from llmguard.domains.retrieval.hidden_poisoning.external_blind_review import (
    PHASE1_FIELDS,
)
from llmguard.domains.retrieval.hidden_poisoning.pilot4_final import (
    computed_length_band,
    visible_char_count,
)
from scripts.research import prepare_pilot4_phase1_attempt2 as attempt2


SUBJECTS = {
    "P4Q-0de42010ea94": "中华人民共和国网络安全法",
    "P4Q-bf24bec76327": "中华人民共和国教育法",
    "P4Q-de8e6e7d3360": "中华人民共和国民办教育促进法实施条例",
    "P4Q-72e86646e3b5": "中华人民共和国会计法",
    "P4Q-6f022a267636": "中华人民共和国职业教育法",
}
KINDS = {
    "P4Q-0de42010ea94": "POISON_CANDIDATE",
    "P4Q-bf24bec76327": "CLEAN_CURRENT",
    "P4Q-de8e6e7d3360": "MATCHED_HARD_NEGATIVE",
    "P4Q-72e86646e3b5": "CLEAN_CURRENT",
    "P4Q-6f022a267636": "CLEAN_CURRENT",
}
COVERAGE = {
    "P4Q-0de42010ea94": "HKP_4_PROVENANCE_AUTHORITY|S3",
    "P4Q-bf24bec76327": "HKP_3_TEMPORAL_VERSION|S1",
    "P4Q-de8e6e7d3360": "HKP_4_PROVENANCE_AUTHORITY|S1",
    "P4Q-72e86646e3b5": "HKP_3_TEMPORAL_VERSION|S3",
    "P4Q-6f022a267636": "HKP_3_TEMPORAL_VERSION|S1",
}
DECLARED_BANDS = {
    "P4Q-0de42010ea94": "LONG",
    "P4Q-bf24bec76327": "MEDIUM",
    "P4Q-de8e6e7d3360": "SHORT",
    "P4Q-72e86646e3b5": "LONG",
    "P4Q-6f022a267636": "SHORT",
}


def _dummy_text(index: int) -> str:
    target = (45, 80, 140)[index % 3]
    subject = f"《测试制度{index:03d}》"
    text = subject + "自2024年1月1日起施行，适用于公共机构的规范管理。"
    return (text + "配套条款继续明确执行边界和责任主体。" * 10)[:target]


def _candidate_rows() -> list[dict[str, Any]]:
    repaired_ids = list(attempt2.REPAIR_SPECS)
    sample_ids = repaired_ids + [f"P4Q-fixture-{index:03d}" for index in range(67)]
    rows: list[dict[str, Any]] = []
    for index, sample_id in enumerate(sample_ids):
        if sample_id in attempt2.REPAIR_SPECS:
            spec = attempt2.REPAIR_SPECS[sample_id]
            text = str(spec["before"])
            subject = SUBJECTS[sample_id]
            evidence_ids = list(spec["source_evidence_ids"])
            candidate_kind = KINDS[sample_id]
            coverage = COVERAGE[sample_id]
            length_band = DECLARED_BANDS[sample_id]
        else:
            text = _dummy_text(index)
            subject = f"测试制度{index:03d}"
            evidence_ids = [f"FIX-E{index:03d}"]
            candidate_kind = (
                "CLEAN_CURRENT",
                "MATCHED_HARD_NEGATIVE",
                "POISON_CANDIDATE",
            )[index % 3]
            coverage = (
                "HKP_1_NUMERIC_ENTITY|S1",
                "HKP_2_CONDITION_EXCEPTION|S2",
                "HKP_3_TEMPORAL_VERSION|S3",
                "HKP_4_PROVENANCE_AUTHORITY|S1",
            )[index % 4]
            length_band = computed_length_band(text)
        intended = (
            coverage.rsplit("|", 1)[1] if candidate_kind == "POISON_CANDIDATE" else None
        )
        rows.append(
            {
                "sample_id": sample_id,
                "triplet_id": f"TRIPLET-{index // 3:02d}",
                "independence_group": f"GROUP-{index // 3:02d}",
                "primary_subject": subject,
                "length_band": length_band,
                "visible_char_count": visible_char_count(text),
                "phase1_view": {"candidate_text": text, "source_title": subject},
                "phase2_view": {
                    "candidate_text": text,
                    "source_title": subject,
                    "evidence_ids": evidence_ids,
                    "evidence_unit_count": len(evidence_ids),
                },
                "owner_only": {
                    "candidate_kind": candidate_kind,
                    "coverage_cell": coverage,
                    "semantic_attack_type": (
                        coverage.split("|", 1)[0]
                        if candidate_kind == "POISON_CANDIDATE"
                        else None
                    ),
                    "mutation_operator": "fixture" if intended else None,
                    "target_field": "fixture_field",
                    "intended_stealth": intended,
                    "hard_negative_type": (
                        "FIXTURE_SCOPE"
                        if candidate_kind == "MATCHED_HARD_NEGATIVE"
                        else None
                    ),
                    "s3_evidence_necessity": None,
                    "domain": (
                        "EDUCATION",
                        "EMPLOYMENT_HR",
                        "FINANCE_PROCUREMENT",
                        "INFORMATION_GOVERNANCE",
                    )[index % 4],
                    "actual_visible_char_count": visible_char_count(text),
                    "computed_length_band": computed_length_band(text),
                },
            }
        )
    return rows


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(
            json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n"
            for row in rows
        ),
        encoding="utf-8",
        newline="",
    )


def _fixture_inputs(tmp_path: Path) -> dict[str, Path]:
    rows = _candidate_rows()
    candidates = tmp_path / "candidates.jsonl"
    _write_jsonl(candidates, rows)

    required_evidence = {
        evidence_id
        for spec in attempt2.REPAIR_SPECS.values()
        for evidence_id in spec["source_evidence_ids"]
    }
    registry = tmp_path / "registry.json"
    _write_json(
        registry,
        {
            "records": [
                {
                    "evidence_id": evidence_id,
                    "content_hash": "a" * 64,
                    "source_snapshot_hash": "b" * 64,
                    "minimal_evidence_hash": "c" * 64,
                    "http_status": 200,
                    "retrieval_status": "HTTP_DOCUMENT_RETRIEVED_AND_CONTENT_MATCHED",
                    "source_url": f"https://example.gov/{evidence_id}",
                    "supported_proposition": f"{evidence_id}支持冻结命题。",
                    "official_page_title": f"官方页面{evidence_id}",
                    "verification_method": "HTTP_HTML_CONTENT_ANCHOR_MATCH",
                }
                for evidence_id in sorted(required_evidence)
            ]
        },
    )

    mapping = tmp_path / "mapping.json"
    mapping_records = [
        {"blind_review_id": blind_id, "sample_id": sample_id}
        for blind_id, sample_id in attempt2.EXPECTED_CONTROLLED_MAPPING.items()
    ] + [
        {
            "blind_review_id": f"BR-{index + 1000:010X}",
            "sample_id": f"P4Q-fixture-{index:03d}",
        }
        for index in range(67)
    ]
    _write_json(mapping, {"records": mapping_records})

    pool = tmp_path / "neutral_pool.json"
    _write_json(
        pool,
        {
            "items": [
                {
                    "sample_id": row["sample_id"],
                    "evidence_id": f"E{slot}",
                    "official_page_title": f"官方页面{slot}",
                    "official_source_url": (
                        f"https://example.gov/{row['sample_id']}/{slot}"
                    ),
                }
                for row in rows
                for slot in (1, 2)
            ]
        },
    )

    attempt1_ids = list(attempt2.OWNER_DISPOSITIONS) + [
        f"BR-{index + 2000:010X}" for index in range(67)
    ]
    attempt1_packet = tmp_path / "attempt1_phase1.jsonl"
    _write_jsonl(
        attempt1_packet,
        [
            {
                "blind_review_id": blind_id,
                "candidate_text": rows[index]["phase1_view"]["candidate_text"],
                "source_title": rows[index]["phase1_view"]["source_title"],
                **{field: "" for field in PHASE1_FIELDS},
            }
            for index, blind_id in enumerate(attempt1_ids)
        ],
    )

    phase_root = tmp_path / "attempt1_phase"
    _write_json(phase_root / "locked.json", {"status": "LOCKED"})
    return_root = tmp_path / "attempt1_return"
    raw = return_root / "raw" / "PILOT4_EXTERNAL_BLIND_PHASE1_RETURN.csv"
    raw.parent.mkdir(parents=True)
    raw.write_bytes(b"immutable-attempt1-return\n")
    guide = tmp_path / "phase2_guide.md"
    guide.write_text("# PILOT4 External Blind Phase2 Guide\n", encoding="utf-8")
    return {
        "candidate_corpus": candidates,
        "neutral_pool": pool,
        "source_registry": registry,
        "attempt1_mapping": mapping,
        "attempt1_phase1_packet": attempt1_packet,
        "attempt1_phase_root": phase_root,
        "attempt1_return_root": return_root,
        "phase2_guide_source": guide,
        "raw": raw,
    }


def test_attempt2_builder_repairs_only_five_and_remains_release_gated(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    paths = _fixture_inputs(tmp_path)
    monkeypatch.setattr(
        attempt2,
        "ATTEMPT1_RAW_SHA256",
        hashlib.sha256(paths.pop("raw").read_bytes()).hexdigest(),
    )
    output = tmp_path / "attempt2"
    result = attempt2.build(output=output, seed=bytes.fromhex("44" * 32), **paths)

    assert result["owner_dispositions"] == 5
    assert result["controlled_mapping_count"] == 5
    assert result["repair_count"] == result["semantic_parity_pass_count"] == 5
    assert result["source_verification_pass_count"] == 5
    assert result["unaffected_candidate_count"] == 67
    assert result["unaffected_candidate_text_changed"] == 0
    assert result["final_candidate_count"] == 72
    assert result["attempt2_blind_id_count"] == 72
    assert result["attempt1_id_reuse_count"] == 0
    assert result["phase2_released"] is False

    owner = json.loads(
        (output / "owner_decision" / "owner_defect_adjudication.json").read_text(
            encoding="utf-8"
        )
    )
    assert len(owner["records"]) == 5
    assert {row["disposition"] for row in owner["records"]} == {
        "REVIEWER_ISSUE_ACCEPTED / CANDIDATE_LOCAL_REPAIR_REQUIRED"
    }
    unlocked = json.loads(
        (
            output / "controlled_mapping" / "controlled_mapping_unlock_log.json"
        ).read_text(encoding="utf-8")
    )
    assert unlocked["records"] == [
        {"blind_review_id": blind_id, "sample_id": sample_id}
        for blind_id, sample_id in attempt2.EXPECTED_CONTROLLED_MAPPING.items()
    ]
    assert unlocked["unauthorized_mapping_output_count"] == 0

    audit = json.loads(
        (output / "candidate_repairs" / "five_candidate_repair_audit.json").read_text(
            encoding="utf-8"
        )
    )
    assert {
        (row["sample_id"], row["before"], row["after"]) for row in audit["records"]
    } == {
        (sample_id, spec["before"], spec["after"])
        for sample_id, spec in attempt2.REPAIR_SPECS.items()
    }
    for row in audit["records"]:
        assert row["semantic_parity"] is True
        assert row["source_verification"] == "PASS"
        assert row["self_containment"] == "PASS"
        assert row["naturalness"] == "PASS"
        assert row["meta_cue"] == "PASS"
        assert row["answer_echo"] == "PASS"
        assert row["candidate_class_parity"] is True
        assert row["hkp_parity"] is True
        assert row["stealth_intent_parity"] is True
        assert row["evidence_necessity_parity"] is True

    order_qa = json.loads(
        (output / "qa" / "attempt2_order_leakage_qa.json").read_text(encoding="utf-8")
    )
    assert order_qa["status"] == "PASS"
    assert order_qa["matched_triplet_adjacency_count"] == 0
    assert order_qa["attempt1_id_reuse_count"] == 0
    assert all(
        not profile["exact_periods_2_to_12"]
        and profile["maximum_run"] <= profile["maximum_run_allowed"]
        for profile in order_qa["profiles"].values()
    )
    leakage = json.loads(
        (output / "qa" / "attempt2_phase1_leakage_qa.json").read_text(encoding="utf-8")
    )
    assert leakage["url_count"] == leakage["forbidden_token_count"] == 0

    phase1 = [
        json.loads(line)
        for line in (
            output
            / "attempt2_packet"
            / "PILOT4_EXTERNAL_BLIND_PHASE1_ATTEMPT2_PACKET.jsonl"
        )
        .read_text(encoding="utf-8")
        .splitlines()
    ]
    phase2 = [
        json.loads(line)
        for line in (
            output
            / "withheld_phase2"
            / "PILOT4_EXTERNAL_BLIND_PHASE2_ATTEMPT2_PACKET.jsonl"
        )
        .read_text(encoding="utf-8")
        .splitlines()
    ]
    assert [row["blind_review_id"] for row in phase1] == [
        row["blind_review_id"] for row in phase2
    ]
    assert all(
        set(row)
        == {"blind_review_id", "candidate_text", "source_title", *PHASE1_FIELDS}
        for row in phase1
    )
    gate = json.loads(
        (output / "qa" / "attempt2_phase2_release_gate.json").read_text(
            encoding="utf-8"
        )
    )
    assert gate["status"] == "BLOCKED_AS_REQUIRED"
    assert all(value is False for value in gate["gate"].values())
    manifest = json.loads(
        (output / "manifest" / "manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["expected_contract_loaded"] is False
    assert manifest["attempt1_expected_comparison_executed"] is False
    assert manifest["attempt2_review_executed"] is False
    assert manifest["phase2_released"] is False
