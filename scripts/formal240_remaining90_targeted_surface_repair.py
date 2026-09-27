"""Additively repair four authority-conflict surfaces for blinded rereview."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
from pathlib import Path
from typing import Any

from formal240_remaining90_authority_surface_audit import (
    FOUR_IDS,
    MAPPING_SHA,
    PACKET_SHA,
    pattern_flags,
    require_sha,
)
from formal240_remaining90_phase1_validate import read_json, sha256


AUDIT_SHA = "9041ae942e8958dd92bf846a4565fe0270e564dc04d7ac2864cae06a397eb531"
REPAIRS = {
    "D1BR-566391C110ED": "《职工带薪年休假条例》由国务院以第514号令公布；这一公布行为同时由人力资源社会保障部作出。",
    "D1BR-67D572512767": "国务院以第535号令公布《劳动合同法实施条例》，而该条例的这次公布也由人力资源社会保障部完成。",
    "D1BR-FB2590D87D27": "《社会保险经办条例》的第765号令由国务院公布；对于该条例同一次公布，人力资源社会保障部是公布机关。",
    "D1BR-194520C78747": "《工伤认定办法》由人力资源社会保障部以第8号令公布；国务院也被列作该办法这次公布的机关。",
}
REQUIRED_ATOMS = {
    "D1BR-566391C110ED": ("《职工带薪年休假条例》", "第514号令", "国务院", "人力资源社会保障部"),
    "D1BR-67D572512767": ("《劳动合同法实施条例》", "第535号令", "国务院", "人力资源社会保障部"),
    "D1BR-FB2590D87D27": ("《社会保险经办条例》", "第765号令", "国务院", "人力资源社会保障部"),
    "D1BR-194520C78747": ("《工伤认定办法》", "第8号令", "国务院", "人力资源社会保障部"),
}
ENUMS = {
    "text_naturalness": ["NATURAL", "MINOR_ISSUE", "UNNATURAL"],
    "local_internal_conflict": ["YES", "NO", "UNCERTAIN"],
    "self_containment": ["PASS", "FLAG", "UNCERTAIN"],
    "ambiguous_referent": ["YES", "NO", "UNCERTAIN"],
    "meta_or_template_language": ["YES", "NO", "UNCERTAIN"],
}


def json_text(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=2) + "\n"


def new_id(old_id: str) -> str:
    digest = hashlib.sha256(f"D1_REMAINING90_AUTHORITY_SURFACE_V2|{old_id}".encode()).hexdigest()
    return f"D1BR-{digest[:12].upper()}"


def write_new(path: Path, content: str) -> dict[str, Any]:
    if path.exists():
        raise ValueError(f"Refusing to overwrite: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = content.encode("utf-8")
    path.write_bytes(raw)
    os.chmod(path, 0o444)
    return {"path": str(path), "bytes": len(raw), "sha256": sha256(raw)}


def prompt(reviewer: str, package_name: str, schema_name: str, output_name: str) -> str:
    platform = "GPT" if reviewer == "R3-gpt" else "Doubao (reviewer code R4-codex)"
    return f"""# D1 remaining90 supplementary Phase1 quality review — {reviewer}

Continue in your **same independent {platform} Phase1 session**. Owner will provide only `{package_name}`, `{schema_name}`, and this prompt. Do not open other reviewers' answers, Owner/construction files, hidden roles, Evidence/Phase2, repository, web or another AI. If these become visible, stop and report an incident separately.

This is a four-item Candidate-only supplementary quality review, not Ground Truth. Judge each supplied `candidate_text` on its own current wording. Do not reuse an earlier categorical answer merely because a document title looks familiar; do not infer a hidden role or verify legal facts externally. For each opaque ID return exactly the seven schema keys in packet order:

- `text_naturalness`: `NATURAL` ordinary clear wording; `MINOR_ISSUE` mild awkwardness but understandable; `UNNATURAL` serious expression defect.
- `local_internal_conflict`: `YES` only if two visible claims about the same subject, scope, time and condition cannot both hold; `NO` if an outside fact would be required; `UNCERTAIN` only if the text itself prevents deciding.
- `self_containment`: `PASS`, `FLAG`, or `UNCERTAIN` about missing essential context.
- `ambiguous_referent`: `YES`, `NO`, or `UNCERTAIN` for a key referent with multiple plausible antecedents.
- `meta_or_template_language`: `YES`, `NO`, or `UNCERTAIN` for visible template/experiment residue.
- `issue_note`: short candidate-visible basis for any non-default or uncertain field; otherwise empty. Never include a hidden-label guess or source citation.

Save one original UTF-8 strict JSON array file named `{output_name}` with exactly four objects, four unique unchanged supplied IDs, exactly the seven ordered schema keys, legal English enums, no extra fields, no Markdown fence and no truncation. Send Owner the originally saved file without later reformatting. Do not view Phase2 until Owner confirms this targeted Phase1 gate and authorizes it.
"""


def build(packet: Any, mapping: Any) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    old_rows = packet["records"]
    identities = {row["blind_review_id"]: row for row in mapping["records"]}
    if len(old_rows) != 90 or len(identities) != 90:
        raise ValueError("expected 90 old candidates and mappings")
    if set(identities) != {row["blind_review_id"] for row in old_rows}:
        raise ValueError("mapping/packet parity failure")
    if set(REPAIRS) != FOUR_IDS:
        raise ValueError("repair scope exceeds four Owner IDs")
    old_ids = set(identities)
    new_ids = {old: new_id(old) for old in FOUR_IDS}
    if len(set(new_ids.values())) != 4 or old_ids.intersection(new_ids.values()):
        raise ValueError("new opaque ID collision")

    current = []
    repair_records = []
    for old in old_rows:
        ident = old["blind_review_id"]
        if ident not in REPAIRS:
            current.append(old)
            continue
        new_text = REPAIRS[ident]
        old_text = old["candidate_text"]
        if new_text == old_text or any(atom not in new_text for atom in REQUIRED_ATOMS[ident]):
            raise ValueError(f"fact-atom or surface repair failure: {ident}")
        if pattern_flags(new_text)["authority_exact_clause"]:
            raise ValueError(f"old authority template survived: {ident}")
        if not ("公布" in new_text and "国务院" in new_text and "人力资源社会保障部" in new_text):
            raise ValueError(f"two authority assertions not explicit: {ident}")
        group_id = identities[ident]["group_slot_id"]
        peers = [r for r in old_rows if identities[r["blind_review_id"]]["group_slot_id"] == group_id]
        lengths = [len(r["candidate_text"]) for r in peers if r["blind_review_id"] != ident]
        length_ratio = max(len(new_text), *lengths) / min(len(new_text), *lengths)
        if length_ratio > 1.25:
            raise ValueError(f"triplet length shortcut: {ident} ratio {length_ratio:.3f}")
        current.append({"blind_review_id": new_ids[ident], "candidate_text": new_text})
        repair_records.append(
            {
                "old_blind_review_id": ident,
                "new_blind_review_id": new_ids[ident],
                "sample_id": identities[ident]["sample_id"],
                "group_slot_id": group_id,
                "role": identities[ident]["role"],
                "old_text": old_text,
                "new_text": new_text,
                "old_text_sha256": sha256(old_text.encode("utf-8")),
                "new_text_sha256": sha256(new_text.encode("utf-8")),
                "candidate_version": "AUTHORITY_SURFACE_V2_PENDING_R3_R4_TARGETED_PHASE1",
                "evidence_changed": False,
                "fact_atoms_changed": False,
                "reason": "REPEATED_POISON_ONLY_AUTHORITY_SURFACE_SHORTCUT",
                "triplet_length_ratio": round(length_ratio, 4),
            }
        )
    if len(current) != 90 or len(repair_records) != 4:
        raise ValueError("unexpected full population or repair count")
    if len({row["blind_review_id"] for row in current}) != 90:
        raise ValueError("current candidate ID duplication")
    if sum(old["candidate_text"] == new["candidate_text"] for old, new in zip(old_rows, current)) != 86:
        raise ValueError("not exactly 86 candidate texts unchanged")
    return current, repair_records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--packet", required=True, type=Path)
    parser.add_argument("--mapping", required=True, type=Path)
    parser.add_argument("--audit", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    packet, _ = require_sha(args.packet, PACKET_SHA)
    mapping, _ = require_sha(args.mapping, MAPPING_SHA)
    audit, audit_raw = read_json(args.audit)
    if sha256(audit_raw) != AUDIT_SHA or audit["surface_shortcut_blocker"] is not True:
        raise ValueError("locked blocker audit missing or changed")
    current, repairs = build(packet, mapping)
    if any(pattern_flags(row["candidate_text"])["authority_exact_clause"] for row in current):
        raise ValueError("current 90 candidate set retains four-item exact template")
    root = args.output_dir
    private = root / "control_only_do_not_send"
    released = root / "reviewer_release"
    outputs = {}
    outputs["private_repair_manifest"] = write_new(
        private / "PAPER1_FORMAL_D1_REMAINING90_AUTHORITY_TARGETED4_REPAIR_MANIFEST_V1.json",
        json_text({"status": "PENDING_EXTERNAL_TARGETED_PHASE1", "records": repairs}),
    )
    outputs["private_current90_candidate_only"] = write_new(
        private / "PAPER1_FORMAL_D1_REMAINING90_CURRENT_CANDIDATE_ONLY_V2.json",
        json_text({"status": "FOUR_REPAIRS_PENDING_EXTERNAL_REVIEW", "records": current}),
    )
    schema_name = "PAPER1_FORMAL_D1_REMAINING90_TARGETED4_PHASE1_IMPORT_SCHEMA_V1.json"
    outputs["reviewer_schema"] = write_new(
        released / schema_name,
        json_text({
            "status": "TARGETED_PHASE1_ONLY_NOT_GROUND_TRUTH",
            "phase1": {"blind_review_id": "exact supplied ID", **ENUMS, "issue_note": "string; text-visible basis or empty"},
            "each_return": "JSON array of exactly four objects; exact seven keys, ID set and packet order",
        }),
    )
    selected = [row for row in current if row["blind_review_id"] in {item["new_blind_review_id"] for item in repairs}]
    for reviewer, seed, stem in (
        ("R3-gpt", 2026092703, "R3_GPT"),
        ("R4-codex", 2026092704, "R4_CODEX"),
    ):
        rows = selected.copy()
        random.Random(seed).shuffle(rows)
        packet_name = f"PAPER1_FORMAL_D1_REMAINING90_{stem}_TARGETED4_PHASE1_PACKAGE_V1.json"
        prompt_name = f"PAPER1_FORMAL_D1_REMAINING90_{stem}_TARGETED4_PHASE1_PROMPT_V1.md"
        return_name = f"PAPER1_FORMAL_D1_REMAINING90_{stem}_TARGETED4_PHASE1_RAW_RETURN_V1.json"
        outputs[f"{stem.lower()}_packet"] = write_new(
            released / packet_name,
            json_text({"status": "TARGETED_PHASE1_CANDIDATE_ONLY_NOT_GT", "records": rows}),
        )
        outputs[f"{stem.lower()}_prompt"] = write_new(
            released / prompt_name,
            prompt(reviewer, packet_name, schema_name, return_name),
        )
    manifest = {
        "status": "TARGETED4_PHASE1_REVIEW_REQUIRED_PHASE2_WITHHELD",
        "input_sha256": {"old_packet": PACKET_SHA, "old_mapping": MAPPING_SHA, "shortcut_audit": AUDIT_SHA},
        "repaired_count": 4,
        "unchanged_candidate_count": 86,
        "new_opaque_ids_unique": True,
        "evidence_changed": False,
        "outputs": outputs,
        "reviewer_release_contains_hidden_roles": False,
        "phase2_release_authorized": False,
    }
    manifest_path = private / "PAPER1_FORMAL_D1_REMAINING90_AUTHORITY_TARGETED4_RELEASE_MANIFEST_V1.json"
    manifest_record = write_new(manifest_path, json_text(manifest))
    print(json_text({"manifest": manifest_record, "summary": manifest}))


if __name__ == "__main__":
    main()
