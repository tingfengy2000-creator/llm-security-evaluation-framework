"""Sealed control-plane audit of D1 remaining90 Phase1 surface shortcuts."""

from __future__ import annotations

import argparse
import json
import os
import re
from collections import Counter
from pathlib import Path
from typing import Any

from formal240_remaining90_phase1_validate import read_json, sha256


RAW_SHAS = {
    "r3": "36a14d40f530bd2f9566f18f36acdce07a11a43b0c56142b8bb41e6af84f1e14",
    "r4": "d3aa0c1470b5dffab91217157a6b808f73531ae9fc3bbee21ef8626500759f04",
    "r5": "788061588e4a42cbb80fda6aaf866944bc2cc027bbc589076f2313820ad463e3",
}
PACKET_SHA = "4d4c346bebb7933af6c5bdd7a7c7e5b4f6619b7f36508d80520015d2c5d516ed"
MAPPING_SHA = "14595f10049421dbea29464a04c2b8b45c70eeff5dda45a96d866462a47d8c57"
FOUR_IDS = {
    "D1BR-FB2590D87D27",
    "D1BR-194520C78747",
    "D1BR-566391C110ED",
    "D1BR-67D572512767",
}
ROLES = ("CLEAN_CURRENT", "POISON", "HARD_NEGATIVE")


def require_sha(path: Path, expected: str) -> tuple[Any, bytes]:
    obj, raw = read_json(path)
    if sha256(raw) != expected:
        raise ValueError(f"frozen SHA256 mismatch: {path.name}")
    return obj, raw


def normalized(text: str) -> str:
    return re.sub(r"[\s，,。；;：:]", "", text)


def pattern_flags(text: str) -> dict[str, bool]:
    compact = normalized(text)
    authority_clause = re.search(r"公布机关既是[^。；]*同时又是", text)
    return {
        "exact_ji_shi_tongshi_you_shi": "既是" in text and "同时又是" in text,
        "authority_exact_clause": authority_clause is not None,
        "authority_normalized_clause": bool(
            re.search(r"公布机关既是.+同时又是", compact)
        ),
        "authority_syntactic_dual_predicate": bool(
            re.search(r"公布机关既是[^。；]*又是", text)
        ),
        "authority_comma_pattern": bool(
            re.search(r"公布机关既是[^，。；]*，同时又是", text)
        ),
        "authority_second_clause_position": bool(
            re.search(r"(?:公布|公布；)[^。；]*[，；]公布机关既是", text)
        ),
        "same_document_dual_authority_lexicon": (
            "同一《" in text
            and "公布机关" in text
            and "国务院" in text
            and "人力资源社会保障部" in text
        ),
    }


def audit(packet: Any, mapping: Any) -> dict[str, Any]:
    if not isinstance(packet, dict) or not isinstance(packet.get("records"), list):
        raise ValueError("invalid blind packet")
    if not isinstance(mapping, dict) or not isinstance(mapping.get("records"), list):
        raise ValueError("invalid sealed mapping")
    texts = packet["records"]
    identities = mapping["records"]
    if len(texts) != 90 or len(identities) != 90:
        raise ValueError("expected 90 packet and 90 mapping records")
    by_id = {row["blind_review_id"]: row for row in identities}
    if len(by_id) != 90 or len({row["blind_review_id"] for row in texts}) != 90:
        raise ValueError("duplicate blind ID")
    if set(by_id) != {row["blind_review_id"] for row in texts}:
        raise ValueError("mapping/packet ID set mismatch")
    role_counts = Counter(row["role"] for row in identities)
    if {role: role_counts[role] for role in ROLES} != dict.fromkeys(ROLES, 30):
        raise ValueError(f"unbalanced or invalid roles: {dict(role_counts)}")
    annotated = []
    for row in texts:
        ident = row["blind_review_id"]
        role = by_id[ident]["role"]
        if role not in ROLES:
            raise ValueError(f"invalid role: {role}")
        annotated.append(
            {
                "blind_review_id": ident,
                "role": role,
                "group_slot_id": by_id[ident]["group_slot_id"],
                "flags": pattern_flags(row["candidate_text"]),
            }
        )
    names = list(annotated[0]["flags"])
    patterns: dict[str, dict[str, Any]] = {}
    for name in names:
        hits = [row for row in annotated if row["flags"][name]]
        patterns[name] = {
            "counts_by_role": {role: sum(row["role"] == role for row in hits) for role in ROLES},
            "hit_count": len(hits),
            "hit_ids": [row["blind_review_id"] for row in hits],
            "hit_group_slots": [row["group_slot_id"] for row in hits],
        }
    authority_hits = set(patterns["authority_exact_clause"]["hit_ids"])
    if authority_hits != FOUR_IDS:
        raise ValueError("the four adjudicated IDs do not match the exact authority template")
    for name in (
        "authority_exact_clause",
        "authority_normalized_clause",
        "authority_syntactic_dual_predicate",
        "authority_comma_pattern",
    ):
        if patterns[name]["counts_by_role"] != {
            "CLEAN_CURRENT": 0,
            "POISON": 4,
            "HARD_NEGATIVE": 0,
        }:
            raise ValueError(f"unexpected authority-pattern role distribution: {name}")
    return {
        "scope": "SEALED_CONSTRUCTION_CONTROL_PLANE_NOT_REVIEWER_RELEASE",
        "records": 90,
        "role_denominators": {role: role_counts[role] for role in ROLES},
        "patterns": patterns,
        "four_adjudicated_ids_exact_pattern_parity": True,
        "surface_shortcut_blocker": True,
        "decision_reason": (
            "The exact and normalized same-document dual-promulgating-organ clause "
            "appears in four distinct groups, all four Poison and zero Clean/HN. "
            "This repeated authority-specific string is a trivial positive cue, "
            "not merely a legitimate semantic contradiction signal."
        ),
        "next_gate": "TARGETED_FOUR_CANDIDATE_SURFACE_REPAIR_AND_R3_R4_PHASE1_REREVIEW",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--r3", required=True, type=Path)
    parser.add_argument("--r4", required=True, type=Path)
    parser.add_argument("--r5", required=True, type=Path)
    parser.add_argument("--packet", required=True, type=Path)
    parser.add_argument("--mapping", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    for name in ("r3", "r4", "r5"):
        require_sha(getattr(args, name), RAW_SHAS[name])
    packet, _ = require_sha(args.packet, PACKET_SHA)
    mapping, _ = require_sha(args.mapping, MAPPING_SHA)
    result = audit(packet, mapping)
    result["input_sha256"] = {
        "r3_raw": RAW_SHAS["r3"],
        "r4_raw": RAW_SHAS["r4"],
        "r5_raw": RAW_SHAS["r5"],
        "candidate_packet": PACKET_SHA,
        "sealed_mapping": MAPPING_SHA,
    }
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(rendered)
    os.chmod(args.output, 0o444)
    print(rendered)


if __name__ == "__main__":
    main()
