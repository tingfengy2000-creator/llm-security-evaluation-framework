"""Validate D1 Canary targeted repair and write additive primary Phase1 QA."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


FIELDS = (
    "text_naturalness", "local_internal_conflict", "self_containment",
    "ambiguous_referent", "meta_or_template_language",
)
OLD_IDS = ("D1BR-F3FA4889DA53", "D1BR-008E1E01060C")
NEW_IDS = ("D1BR-C9E69F1920D5", "D1BR-5654C8EF39A1")
EXPECTED = (
    ("NATURAL", "YES", "PASS", "NO", "NO"),
    ("NATURAL", "NO", "PASS", "NO", "NO"),
)
FULL_SHA = {
    "R3-gpt": "323584b020cad90e382c9d7b202e20acd5ecbe2acabb0111180d6d059b44f36d",
    "R4-codex": "afb0af1b61e927af61c76620f0a2ef76443c2123c07704dd7a56144a08f60e74",
}
RAW_NAMES = {
    "R3-gpt": ("PAPER1_FORMAL_D1_CANARY_R3_GPT_PHASE1_RAW_V1.json", "PAPER1_FORMAL_D1_CANARY_R3_GPT_TARGETED_PHASE1_RAW_V1.json"),
    "R4-codex": ("PAPER1_FORMAL_D1_CANARY_R4_CODEX_PHASE1_RAW_V1.json", "PAPER1_FORMAL_D1_CANARY_R4_CODEX_TARGETED_PHASE1_RAW_V1.json"),
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path: Path) -> Any:
    return json.loads(path.read_bytes())


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def write(path: Path, value: Any) -> None:
    with path.open("xb") as stream:
        stream.write((json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))


def text_atoms(value: str) -> dict[str, Any]:
    return {
        "titles": re.findall(r"《[^》]+》", value),
        "numbers": re.findall(r"\d+", value),
        "institutions": [x for x in ("国务院", "人力资源社会保障部", "社会保险经办机构", "用人单位") if x in value],
        "contradiction": "既享受" in value and "不享受" in value,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    for key in ("source", "previous", "locked", "output", "matrix"):
        parser.add_argument(f"--{key}", type=Path, required=True)
    args = parser.parse_args()
    assert args.output.is_dir()
    schema = read(args.source / "PAPER1_FORMAL_D1_BLIND_REVIEW_IMPORT_SCHEMA_V2.json")["phase1"]
    packet_old = read(args.source / "PAPER1_FORMAL_D1_BLIND_REVIEW_PACKAGE_PHASE1_V2.json")["records"]
    targeted = read(args.previous / "PAPER1_FORMAL_D1_CANARY_TARGETED_PHASE1_REVIEW_PACKAGE_V1.json")["records"]
    assert [r["blind_review_id"] for r in targeted] == list(NEW_IDS)
    locked_manifest = read(args.locked / "PAPER1_FORMAL_D1_CANARY_TARGETED_PHASE1_RAW_LOCK_MANIFEST_V1.json")
    assert locked_manifest["raw_lock_before_private_mapping_load"] is True

    primary: dict[str, Any] = {}
    for reviewer, (full_name, target_name) in RAW_NAMES.items():
        full_path, target_path = args.previous / full_name, args.locked / target_name
        assert sha(full_path) == FULL_SHA[reviewer]
        assert sha(target_path) == locked_manifest["reviewers"][reviewer]["sha256"]
        full, target = read(full_path), read(target_path)
        assert len(full) == 24 and len(target) == 2
        assert [r["blind_review_id"] for r in full] == [r["blind_review_id"] for r in packet_old]
        assert [r["blind_review_id"] for r in target] == list(NEW_IDS)
        for row in target:
            assert set(row) == set(schema) and isinstance(row["issue_note"], str)
            assert all(row[field] in schema[field] for field in FIELDS)
        assert all(tuple(row[f] for f in FIELDS) == values for row, values in zip(target, EXPECTED, strict=True))
        primary[reviewer] = {"full_sha256": sha(full_path), "targeted_sha256": sha(target_path), "full": full, "targeted": target}

    r3, r4 = primary["R3-gpt"]["targeted"], primary["R4-codex"]["targeted"]
    per_field = {field: sum(a[field] == b[field] for a, b in zip(r3, r4, strict=True)) for field in FIELDS}
    exact = sum(all(a[field] == b[field] for field in FIELDS) for a, b in zip(r3, r4, strict=True))
    assert exact == 2 and all(count == 2 for count in per_field.values())
    assert "PAPER1_FORMAL_D1_CANARY_TARGETE" in r3[0]["issue_note"]
    assert "PAPER1_FORMAL_D1_CANARY_TARGETE" not in r4[0]["issue_note"]
    agreement = {
        "status": "PRIMARY_GATING_TARGETED_REVIEW_ACCEPTED",
        "reviewer_roles": {"R3-gpt": "PRIMARY_GATING_1", "R4-codex": "PRIMARY_GATING_2", "R5-claude": "AUXILIARY_NON_GATING"},
        "count": 2, "per_field_agreement": per_field, "exact_five_field_agreement": exact,
        "disagreement_ids": [],
        "r3_note_artifact": "NON_BLOCKING_REVIEWER_NOTE_ARTIFACT_REFERENCE; raw preserved; categorical values usable",
        "targeted_naturalness_repair_accepted": True,
        "designed_internal_conflict_preserved": True,
        "nonconflict_candidate_remains_no_conflict": True,
        "independence_evidence": "OWNER_ATTESTED_NOT_MACHINE_VERIFIED",
    }

    # Private construction lineage is consulted only after both targeted raw locks.
    old_path = args.source / "PAPER1_FORMAL_D1_CANARY_CANDIDATES_V2.jsonl"
    new_path = args.previous / "PAPER1_FORMAL_D1_CANARY_CANDIDATES_V3.jsonl"
    p2_old_path = args.source / "PAPER1_FORMAL_D1_BLIND_REVIEW_PACKAGE_PHASE2_V3.json"
    p2_new_path = args.previous / "PAPER1_FORMAL_D1_CANARY_PHASE2_V4.json"
    assert sha(old_path) == "bd5085e4ba25c54731b9d5201ab7c48d2689060fea48436c9c972a19d1524176"
    assert sha(new_path) == "6210a6de8f519fb4a58334ff531954b67e774375d021d099dea050f8fe47032e"
    assert sha(p2_new_path) == "2daf08286581cb8d28e70ab95ea844e5cdf41e2a6916980bf41b0a90a548ac38"
    old, new = read_jsonl(old_path), read_jsonl(new_path)
    p2_old, p2_new = read(p2_old_path)["records"], read(p2_new_path)["records"]
    repair = read(args.previous / "PAPER1_FORMAL_D1_CANARY_NATURALNESS_REPAIR_LEDGER_V1.json")
    changes = {row["old_blind_review_id"]: row for row in repair["changes"]}
    assert set(changes) == set(OLD_IDS)
    assert len(old) == len(new) == len(p2_old) == len(p2_new) == 24
    assert len({r["blind_review_id"] for r in new}) == 24
    candidate_map: dict[str, str] = {}
    for before, after, before_p2, after_p2 in zip(old, new, p2_old, p2_new, strict=True):
        old_id = before["blind_review_id"]
        if old_id in changes:
            delta = changes[old_id]
            assert after["blind_review_id"] == delta["new_blind_review_id"]
            assert after["candidate_text"] == before["candidate_text"].replace(delta["changed_span"]["from"], delta["changed_span"]["to"], 1)
            assert text_atoms(before["candidate_text"]) == text_atoms(after["candidate_text"])
            assert before["group_slot_id"] == after["group_slot_id"]
            assert before["construction_role"] == after["construction_role"]
            assert before["frozen_evidence_doc_ids"] == after["frozen_evidence_doc_ids"]
        else:
            assert before == after
        candidate_map[old_id] = after["blind_review_id"]
        assert before_p2["blind_review_id"] == old_id
        assert after_p2["blind_review_id"] == after["blind_review_id"]
        assert before_p2["evidence"] == after_p2["evidence"]
        assert after_p2["candidate_text"] == after["candidate_text"]
        assert set(after_p2) == {"blind_review_id", "candidate_text", "evidence"}

    overlays: dict[str, Any] = {}
    for reviewer in RAW_NAMES:
        by_new = {row["blind_review_id"]: row for row in primary[reviewer]["targeted"]}
        rows = []
        for previous_row in primary[reviewer]["full"]:
            old_id = previous_row["blind_review_id"]
            new_id = candidate_map[old_id]
            selected = by_new[new_id] if old_id in changes else previous_row
            rows.append({"blind_review_id": new_id, "reviewer_id": reviewer, "values": selected,
                         "lineage": "TARGETED_LOCKED_RAW" if old_id in changes else "FULL_LOCKED_RAW_UNCHANGED",
                         "source_raw_sha256": primary[reviewer]["targeted_sha256"] if old_id in changes else primary[reviewer]["full_sha256"]})
        assert len(rows) == 24 and [row["blind_review_id"] for row in rows] == [row["blind_review_id"] for row in new]
        overlays[reviewer] = rows
    overlay = {"status": "PHASE1_PRIMARY_ACCEPTED_OVERLAY_NOT_RAW", "candidate_v3_sha256": sha(new_path),
               "raw_values_rewritten": False, "reviewers": overlays}

    # Bounded mechanical re-QA: frozen evidence, declared fact path, metadata and
    # query/view inputs are checked; this is not a new independent factual audit.
    selection = read(args.source / "PAPER1_FORMAL_D1_CANARY_GROUP_SELECTION_V1.json")
    selected = selection["selected_group_slots"]
    matrix = read_jsonl(args.matrix)
    assert sha(args.matrix) == selection["formal_matrix_sha256"]
    assert len(selected) == 8 and set(selected).issubset({row["group_slot_id"] for row in matrix})
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in new:
        grouped[row["group_slot_id"]].append(row)
        assert "《" in row["candidate_text"] and "》" in row["candidate_text"]
        assert "第四条下" not in row["candidate_text"]
    assert set(grouped) == set(selected)
    assert all(len(rows) == 3 and {r["construction_role"] for r in rows} == {"CLEAN_CURRENT", "POISON", "HARD_NEGATIVE"} for rows in grouped.values())
    style = {group: max(len(r["candidate_text"]) for r in rows) - min(len(r["candidate_text"]) for r in rows) for group, rows in grouped.items()}
    assert all(spread <= 10 for spread in style.values())
    manifest = read(args.source / "PAPER1_FORMAL_D1_CANARY_EVIDENCE_MANIFEST_V3.json")
    snapshot_checks = 0
    for item in manifest:
        raw = args.source / item["snapshot_raw_html"]
        txt = args.source / item["snapshot_extracted_text"]
        assert sha(raw) == item["snapshot_raw_sha256"] and raw.stat().st_size == item["snapshot_raw_bytes"]
        assert hashlib.sha256(txt.read_text(encoding="utf-8").encode("utf-8")).hexdigest() == item["snapshot_text_sha256"]
        snapshot_checks += 1
    assert snapshot_checks == 14
    facts = read(args.source / "PAPER1_FORMAL_D1_CANARY_CANONICAL_EVIDENCE_FACT_RECORD_V1.json")
    assert {row["group_slot_id"] for row in facts["groups"]} == set(selected)
    metadata = read(args.source / "PAPER1_FORMAL_D1_CANARY_METADATA_AUDIT_V1.json")
    assert metadata["documents"] == 14 and metadata["raw_snapshot_sha_pass"] == "14/14"
    queries = read(args.source / "PAPER1_FORMAL_D1_CANARY_PREGEN_VIEW_QUERY_CONTRACT_V1.json")["group_queries"]
    assert {row["group_slot_id"] for row in queries} == set(selected)
    assert all(not any(term in row["neutral_query"] for term in ("POISON", "CLEAN", "HARD_NEGATIVE", "HKP", "S1", "S2", "S3")) for row in queries)
    preflight = read(args.source / "PAPER1_FORMAL_D1_CANARY_SIGNAL_INPUT_OBSERVABILITY_PREFLIGHT_V1.json")
    assert preflight["registry_signals"] == 42
    forbidden = ("construction_role", "group_slot_id", "target_stealth", "derived_stealth", "expected_v3", "ground_truth", "hkp1", "hkp2", "hkp3", "hkp4")
    assert not any(term in p2_new_path.read_text(encoding="utf-8").lower() for term in forbidden)
    mechanical = {
        "status": "BOUNDED_MECHANICAL_REQA_PASS_NOT_FULL_FACTUAL_CERTIFICATION",
        "candidate_v2_sha256_unchanged": sha(old_path), "candidate_v3_sha256": sha(new_path),
        "candidate_count": 24, "changed": 2, "unchanged": 22,
        "fixed_evidence_snapshots_sha_pass": snapshot_checks,
        "evidence_identity_excerpt_and_snapshot_sha_parity": "24/24_EXACT",
        "fact_atoms_in_two_repaired_rows": "EXACT_EXTRACTED_TITLE_NUMBER_INSTITUTION_CONTRADICTION_PARITY",
        "fact_path_unchanged": True, "metadata_baseline_unchanged": True,
        "neutral_query_eight_group_mapping": "PASS", "s_e_p_t_r_preflight_source_unchanged": True,
        "style_length_spread_by_group": style, "self_containment_primary_reviewer": "R3_R4_24_OF_24_PASS",
        "phase2_v4_sha256": sha(p2_new_path), "phase2_v4_rows": 24,
        "phase2_blind_label_leakage": 0,
        "limitations": ["Heuristic atom/style checks cannot prove exhaustive factual correctness.",
                        "Phase2 factual and evidence sufficiency review is still pending.",
                        "Metadata/view readiness retains earlier explicit missingness limitations."],
    }
    manifest_out = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "candidate_v3_path": str(new_path), "candidate_v3_sha256": sha(new_path),
        "phase2_v4_path": str(p2_new_path), "phase2_v4_sha256": sha(p2_new_path),
        "primary_raw_lock_manifest_sha256": sha(args.locked / "PAPER1_FORMAL_D1_CANARY_TARGETED_PHASE1_RAW_LOCK_MANIFEST_V1.json"),
        "r3_targeted_raw_sha256": primary["R3-gpt"]["targeted_sha256"],
        "r4_targeted_raw_sha256": primary["R4-codex"]["targeted_sha256"],
        "repair_ledger_sha256": sha(args.previous / "PAPER1_FORMAL_D1_CANARY_NATURALNESS_REPAIR_LEDGER_V1.json"),
        "phase2_prebuilt_promoted_without_rewrite": True,
        "r5_auxiliary_raw": "NOT_LOCKED_OWNER_PASTED_CHAT_TEXT_ONLY_NON_GATING",
    }
    outputs = {
        "PAPER1_FORMAL_D1_CANARY_R3_R4_TARGETED_AGREEMENT_V1.json": agreement,
        "PAPER1_FORMAL_D1_CANARY_PHASE1_FINAL_OVERLAY_V1.json": overlay,
        "PAPER1_FORMAL_D1_CANARY_V3_MECHANICAL_REQA_V1.json": mechanical,
        "PAPER1_FORMAL_D1_CANARY_FINAL_V3_MANIFEST_V1.json": manifest_out,
    }
    assert all(not (args.output / name).exists() for name in outputs)
    for name, data in outputs.items():
        write(args.output / name, data)
    print(json.dumps({"primary_exact_agreement": exact, "candidate_v3_sha256": sha(new_path),
                      "phase2_v4_sha256": sha(p2_new_path), "mechanical": mechanical["status"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
