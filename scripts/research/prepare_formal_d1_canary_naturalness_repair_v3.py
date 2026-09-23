"""Lock D1 Canary R3/R4 Phase1 QA and prepare the two-item V3 style repair.

This script writes additive artifacts only. It never edits raw reviewer returns,
Candidate V2, the frozen evidence, or the Phase2 V3 package.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

FIELDS = (
    "text_naturalness",
    "local_internal_conflict",
    "self_containment",
    "ambiguous_referent",
    "meta_or_template_language",
)
R3_NAME = "PAPER1_FORMAL_D1_CANARY_R3_GPT_PHASE1_RAW_V1.json"
R4_NAME = "PAPER1_FORMAL_D1_CANARY_R4_CODEX_PHASE1_RAW_V1.json"
PHRASE_OLD = "《职工带薪年休假条例》第四条下，"
PHRASE_NEW = "根据《职工带薪年休假条例》第四条，"
TARGETS = ("D1BR-F3FA4889DA53", "D1BR-008E1E01060C")
CONFLICT_IDS = {"D1BR-0A533F363A06", "D1BR-F3FA4889DA53"}
EXPECTED_V2_SHA = "bd5085e4ba25c54731b9d5201ab7c48d2689060fea48436c9c972a19d1524176"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_bytes().decode("utf-8-sig"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def write_new(path: Path, data: Any, *, jsonl: bool = False) -> None:
    if jsonl:
        payload = "\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in data) + "\n"
    else:
        payload = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    with path.open("xb") as stream:
        stream.write(payload.encode("utf-8"))


def validate_return(
    rows: list[dict[str, Any]], packet: list[dict[str, Any]], schema: dict[str, Any]
) -> None:
    assert len(rows) == len(packet) == 24
    assert len({row["blind_review_id"] for row in rows}) == 24
    assert [row["blind_review_id"] for row in rows] == [row["blind_review_id"] for row in packet]
    expected_keys = set(schema)
    for row in rows:
        assert set(row) == expected_keys, row.get("blind_review_id")
        assert isinstance(row["issue_note"], str)
        for field in FIELDS:
            assert row[field] in schema[field], (row["blind_review_id"], field)


def check_attestation(path: Path, reviewer: str, raw_sha: str) -> dict[str, Any]:
    data = load_json(path)
    assert data["reviewer_id"] == reviewer
    assert data["phase"] == "PHASE1"
    assert data["attestation_status"] == "PASS"
    assert data["phase1_raw_sha256"] == raw_sha
    assert data["session_lineage_token"]
    assert data["evidence_basis"]
    for field in (
        "fresh_session_confirmed",
        "repo_access_prohibited",
        "owner_packet_not_seen",
        "old_reviewer_returns_not_seen",
        "label_mapping_not_seen",
        "phase2_not_seen_before_phase1_lock",
        "external_search_not_used",
    ):
        assert data[field] is True, field
    assert data["repo_access_occurred"] is False
    return data


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    source: Path = args.source
    output: Path = args.output
    assert source.is_dir() and output.is_dir()
    packet1_v2 = load_json(source / "PAPER1_FORMAL_D1_BLIND_REVIEW_PACKAGE_PHASE1_V2.json")
    schema = load_json(source / "PAPER1_FORMAL_D1_BLIND_REVIEW_IMPORT_SCHEMA_V2.json")["phase1"]
    r3 = load_json(output / R3_NAME)
    r4 = load_json(output / R4_NAME)
    assert isinstance(r3, list) and isinstance(r4, list)
    validate_return(r3, packet1_v2["records"], schema)
    validate_return(r4, packet1_v2["records"], schema)
    a3 = check_attestation(output / "R3_GPT_REVIEW_RUN_ATTESTATION_V1.json", "R3-gpt", sha(output / R3_NAME))
    a4 = check_attestation(output / "R4_CODEX_REVIEW_RUN_ATTESTATION_V1.json", "R4-codex", sha(output / R4_NAME))
    assert a3["session_lineage_token"] != a4["session_lineage_token"]
    agreement: dict[str, Any] = {
        "status": "OWNER_ATTESTED_INDEPENDENT_PHASE1_QA_NOT_GROUND_TRUTH",
        "source_r3_sha256": sha(output / R3_NAME),
        "source_r4_sha256": sha(output / R4_NAME),
        "r3_count": 24,
        "r4_count": 24,
        "exact_five_field_agreement": 0,
        "field_agreement": {},
        "disagreement_ids": [],
        "issue_note_policy": "Preserve raw wording; do not require byte-identical notes.",
    }
    for field in FIELDS:
        agreement["field_agreement"][field] = sum(x[field] == y[field] for x, y in zip(r3, r4, strict=True))
    for x, y in zip(r3, r4, strict=True):
        if all(x[field] == y[field] for field in FIELDS):
            agreement["exact_five_field_agreement"] += 1
        else:
            agreement["disagreement_ids"].append(x["blind_review_id"])
    assert agreement["exact_five_field_agreement"] == 24
    assert all(value == 24 for value in agreement["field_agreement"].values())
    assert {x["blind_review_id"] for x in r3 if x["local_internal_conflict"] == "YES"} == CONFLICT_IDS
    assert {x["blind_review_id"] for x in r4 if x["local_internal_conflict"] == "YES"} == CONFLICT_IDS
    for rows in (r3, r4):
        assert {x["blind_review_id"] for x in rows if x["text_naturalness"] == "MINOR_ISSUE"} == set(TARGETS)
        for row in rows:
            if row["blind_review_id"] in TARGETS:
                assert "第四条下" in row["issue_note"]

    # Hidden construction roles enter only after the raw-only reviewer comparison.
    candidate_path = source / "PAPER1_FORMAL_D1_CANARY_CANDIDATES_V2.jsonl"
    assert sha(candidate_path) == EXPECTED_V2_SHA
    candidate_v2 = load_jsonl(candidate_path)
    packet2_v3 = load_json(source / "PAPER1_FORMAL_D1_BLIND_REVIEW_PACKAGE_PHASE2_V3.json")
    assert len(candidate_v2) == len(packet1_v2["records"]) == len(packet2_v3["records"]) == 24
    assert [row["blind_review_id"] for row in candidate_v2] == [row["blind_review_id"] for row in packet1_v2["records"]]
    assert [row["blind_review_id"] for row in candidate_v2] == [row["blind_review_id"] for row in packet2_v3["records"]]
    for candidate, question, evidence in zip(candidate_v2, packet1_v2["records"], packet2_v3["records"], strict=True):
        assert candidate["candidate_text"] == question["candidate_text"] == evidence["candidate_text"]

    replacements: dict[str, str] = {}
    changed: list[dict[str, Any]] = []
    candidate_v3: list[dict[str, Any]] = []
    for row in candidate_v2:
        updated = dict(row)
        old_id = row["blind_review_id"]
        if old_id in TARGETS:
            old_text = row["candidate_text"]
            assert old_text.count(PHRASE_OLD) == 1
            new_text = old_text.replace(PHRASE_OLD, PHRASE_NEW, 1)
            assert new_text.replace(PHRASE_NEW, PHRASE_OLD, 1) == old_text
            new_id = "D1BR-" + hashlib.sha256((old_id + new_text + "V3").encode()).hexdigest()[:12].upper()
            replacements[old_id] = new_id
            updated["candidate_text"] = new_text
            updated["blind_review_id"] = new_id
            updated["candidate_version"] = "V3_TARGETED_NATURALNESS_REPAIR"
            updated["status"] = "CANDIDATE_V3_PENDING_R3_R4_TARGETED_PHASE1_REVIEW"
            assert {k for k in updated if updated[k] != row[k]} == {
                "candidate_text", "blind_review_id", "candidate_version", "status"
            }
            changed.append({
                "old_blind_review_id": old_id,
                "new_blind_review_id": new_id,
                "repair_from": old_text,
                "repair_to": new_text,
                "repair_reason": "Two owner-attested independent reviewers identified the same minor phrasing issue.",
                "reviewer_support": {"R3-gpt": "MINOR_ISSUE", "R4-codex": "MINOR_ISSUE"},
                "changed_span": {"from": PHRASE_OLD, "to": PHRASE_NEW},
                "semantic_invariance_status": "EXACT_SINGLE_SPAN_REPLACEMENT_FACT_ATOMS_AND_DESIGNED_CONFLICT_PRESERVED_PENDING_TARGETED_REVIEW",
                "frozen_evidence_doc_ids_unchanged": True,
                "construction_role_unchanged": True,
                "group_slot_id_unchanged": True,
            })
        candidate_v3.append(updated)
    assert set(replacements) == set(TARGETS) and len(changed) == 2
    assert len({row["blind_review_id"] for row in candidate_v3}) == 24
    assert sum(x == y for x, y in zip(candidate_v2, candidate_v3, strict=True)) == 22
    by_old = {row["blind_review_id"]: row for row in candidate_v2}
    assert "既享受年休假，也不享受年休假" in next(row["candidate_text"] for row in candidate_v3 if row["blind_review_id"] == replacements["D1BR-F3FA4889DA53"])
    for row in candidate_v3:
        old_id = next((key for key, value in replacements.items() if value == row["blind_review_id"]), row["blind_review_id"])
        old = by_old[old_id]
        assert row["frozen_evidence_doc_ids"] == old["frozen_evidence_doc_ids"]
        assert row["construction_role"] == old["construction_role"]
        assert row["group_slot_id"] == old["group_slot_id"]

    packet1_v3 = dict(packet1_v2)
    packet1_v3["status"] = "TARGETED_REPAIR_PENDING_REVIEW_NOT_GT"
    packet1_v3["supersedes_for_external_distribution"] = "PAPER1_FORMAL_D1_BLIND_REVIEW_PACKAGE_PHASE1_V2.json"
    packet1_v3["records"] = [
        {"blind_review_id": new["blind_review_id"], "candidate_text": new["candidate_text"]}
        for new in candidate_v3
    ]
    targeted = {
        "status": "TARGETED_PHASE1_REVIEW_ONLY_PHASE2_WITHHELD",
        "instruction": "Evaluate only the five Phase1 categorical fields and issue_note. Do not use external evidence, prior returns or hidden labels.",
        "schema_reference": "PAPER1_FORMAL_D1_BLIND_REVIEW_IMPORT_SCHEMA_V2.json",
        "records": [row for row in packet1_v3["records"] if row["blind_review_id"] in replacements.values()],
    }
    assert len(targeted["records"]) == 2
    assert all(set(row) == {"blind_review_id", "candidate_text"} for row in targeted["records"])
    packet2_v4 = dict(packet2_v3)
    packet2_v4["status"] = "PREBUILT_WITHHELD_PENDING_TARGETED_PHASE1_ACCEPTANCE"
    packet2_v4["supersedes_for_external_distribution"] = "PAPER1_FORMAL_D1_BLIND_REVIEW_PACKAGE_PHASE2_V3.json"
    packet2_v4["records"] = []
    for old, new, prior in zip(candidate_v2, candidate_v3, packet2_v3["records"], strict=True):
        item = dict(prior)
        item["blind_review_id"] = new["blind_review_id"]
        item["candidate_text"] = new["candidate_text"]
        assert item["evidence"] == prior["evidence"]
        if old["blind_review_id"] not in TARGETS:
            assert item == prior
        else:
            assert {key for key in item if item[key] != prior[key]} == {"blind_review_id", "candidate_text"}
        packet2_v4["records"].append(item)
    assert len(packet2_v4["records"]) == 24
    for row in targeted["records"]:
        assert set(row) == {"blind_review_id", "candidate_text"}
    for row in packet2_v4["records"]:
        assert "construction_role" not in row and "group_slot_id" not in row

    mapping_v2 = load_json(source / "PAPER1_FORMAL_D1_CANARY_BLIND_MAPPING_PRIVATE_V2.json")
    mapping_v3 = []
    for prior, new in zip(mapping_v2, candidate_v3, strict=True):
        assert prior["blind_review_id"] in by_old
        item = dict(prior)
        item["blind_review_id"] = new["blind_review_id"]
        item["candidate_version"] = new["candidate_version"]
        mapping_v3.append(item)

    ledger = {
        "status": "TARGETED_REPAIR_PREPARED_NOT_ACCEPTED",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "source_candidate_v2_sha256": sha(candidate_path),
        "source_phase1_v2_sha256": sha(source / "PAPER1_FORMAL_D1_BLIND_REVIEW_PACKAGE_PHASE1_V2.json"),
        "source_phase2_v3_sha256": sha(source / "PAPER1_FORMAL_D1_BLIND_REVIEW_PACKAGE_PHASE2_V3.json"),
        "reviewer_raw_sha256": {"R3-gpt": sha(output / R3_NAME), "R4-codex": sha(output / R4_NAME)},
        "changes": changed,
        "changed_count": 2,
        "unchanged_count": 22,
        "evidence_changed": False,
        "human_ab_authorized": False,
        "phase2_release_authorized": False,
        "next_gate": "Both original reviewer sessions must return targeted Phase1 checks for both new opaque IDs; only then accept V3 and release hash-locked Phase2 V4.",
    }
    names = {
        "PAPER1_FORMAL_D1_CANARY_R3_R4_PHASE1_AGREEMENT_V1.json": agreement,
        "PAPER1_FORMAL_D1_CANARY_CANDIDATES_V3.jsonl": candidate_v3,
        "PAPER1_FORMAL_D1_CANARY_NATURALNESS_REPAIR_LEDGER_V1.json": ledger,
        "PAPER1_FORMAL_D1_BLIND_REVIEW_PACKAGE_PHASE1_V3.json": packet1_v3,
        "PAPER1_FORMAL_D1_CANARY_TARGETED_PHASE1_REVIEW_PACKAGE_V1.json": targeted,
        "PAPER1_FORMAL_D1_CANARY_PHASE2_V4.json": packet2_v4,
        "PAPER1_FORMAL_D1_CANARY_BLIND_MAPPING_PRIVATE_V3.json": mapping_v3,
    }
    assert all(not (output / name).exists() for name in names)
    for name, value in names.items():
        write_new(output / name, value, jsonl=name.endswith(".jsonl"))
    manifest = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "raw_source_attachment_provenance": {
            "R3-gpt": "Owner-confirmed attachment 2 (9fb344d2-ab2b-42db-b38e-fd64464b087a)",
            "R4-codex": "Owner-confirmed attachment 1 (004edc62-10bd-4441-b8b7-10de349d80cb)",
        },
        "source_files_sha256": {name: sha(source / name) for name in (
            "PAPER1_FORMAL_D1_CANARY_CANDIDATES_V2.jsonl",
            "PAPER1_FORMAL_D1_BLIND_REVIEW_PACKAGE_PHASE1_V2.json",
            "PAPER1_FORMAL_D1_BLIND_REVIEW_PACKAGE_PHASE2_V3.json",
            "PAPER1_FORMAL_D1_BLIND_REVIEW_IMPORT_SCHEMA_V2.json",
            "PAPER1_FORMAL_D1_CANARY_BLIND_MAPPING_PRIVATE_V2.json",
        )},
        "output_files_sha256": {name: sha(output / name) for name in (
            R3_NAME, R4_NAME,
            "R3_GPT_REVIEW_RUN_ATTESTATION_V1.json", "R4_CODEX_REVIEW_RUN_ATTESTATION_V1.json",
            *names,
        )},
        "raw_locked_before_derived_outputs": True,
        "phase2_v4_withheld": True,
    }
    write_new(output / "PAPER1_FORMAL_D1_CANARY_R3_R4_PHASE1_REPAIR_SHA_MANIFEST_V1.json", manifest)
    assert Counter(row["construction_role"] for row in candidate_v2) == Counter(row["construction_role"] for row in candidate_v3)
    print(json.dumps({"agreement": agreement["exact_five_field_agreement"], "changed": len(changed), "manifest_sha256": sha(output / "PAPER1_FORMAL_D1_CANARY_R3_R4_PHASE1_REPAIR_SHA_MANIFEST_V1.json")}, sort_keys=True))


if __name__ == "__main__":
    main()
