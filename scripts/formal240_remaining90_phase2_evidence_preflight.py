"""Read-only frozen-evidence preflight for the D1 remaining90 Phase2 handoff.

This does not release reviewer materials. In particular, the two three-snapshot
groups need an explicit Owner decision before any E1/E2-only projection is used.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from formal240_batch1_phase2_release import official_text


PROPOSED_TWO_SOURCE_PROJECTION = {
    "F240-D1-HKP3-S1-C2": ["HD2013", "HD2024"],
    "F240-D1-HKP3-S1-C3": ["EV-INJURY-CURRENT", "EV-INJURY-2010-AMENDMENT"],
}
REQUIRED_TEXT = {
    "HD2013": ("第三次修订",),
    "HD2024": ("第三次修订", "第四次修订"),
    "EV-INJURY-CURRENT": ("2010年12月20日",),
    "EV-INJURY-2010-AMENDMENT": ("2010年12月20日", "自2011年1月1日起施行"),
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read(path: Path) -> tuple[Any, str]:
    raw = path.read_bytes()
    return json.loads(raw.decode("utf-8-sig")), digest(raw)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence-manifest", type=Path, required=True)
    parser.add_argument("--group-manifest", type=Path, required=True)
    parser.add_argument("--mapping", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    evidence, evidence_sha = read(args.evidence_manifest)
    groups, groups_sha = read(args.group_manifest)
    mapping, mapping_sha = read(args.mapping)
    candidate, candidate_sha = read(args.candidate)
    require(len(evidence["records"]) == 23, "official snapshot population changed")
    require(len(groups["records"]) == 30, "group population changed")
    require(len(mapping["records"]) == len(candidate["records"]) == 90, "90-row population changed")

    sources: dict[str, dict[str, Any]] = {}
    source_audit: list[dict[str, Any]] = []
    total_extracted = 0
    for row in evidence["records"]:
        path = Path(row["private_snapshot_path"])
        raw = path.read_bytes()
        require(digest(raw) == row["sha256"], f"snapshot hash mismatch: {path.name}")
        plain = official_text(path)
        require(bool(plain), f"empty extracted official text: {path.name}")
        total_extracted += len(plain)
        aliases = [item["evidence_id"] for item in row["aliases"]]
        for alias in aliases:
            require(alias not in sources or sources[alias]["sha256"] == row["sha256"], f"ambiguous alias {alias}")
            sources[alias] = {"sha256": row["sha256"], "text": plain}
        source_audit.append({
            "snapshot_sha256": row["sha256"],
            "official_url": row["official_url"],
            "raw_bytes": len(raw),
            "extracted_characters": len(plain),
            "aliases": aliases,
            "raw_hash_verified": True,
        })

    ids = [row["blind_review_id"] for row in candidate["records"]]
    require(len(set(ids)) == 90, "candidate ID duplication")
    mapped = {row["sample_id"]: row for row in mapping["records"]}
    require(len(mapped) == 90, "mapping sample duplication")
    require(len({row["group_slot_id"] for row in mapping["records"]}) == 30, "mapping group count")
    group_ids = {row["group_slot_id"] for row in groups["records"]}
    require(group_ids == {row["group_slot_id"] for row in mapping["records"]}, "mapping group set")
    require({row["blind_review_id"] for row in mapping["records"]} != set(ids), "repaired ID lineage not detected")

    triples: list[dict[str, Any]] = []
    evidence_cards = {1: 0, 2: 0, 3: 0}
    for group in groups["records"]:
        refs = group["evidence_refs"]
        require(len(refs) in evidence_cards, f"unexpected evidence count: {group['group_slot_id']}")
        evidence_cards[len(refs)] += 1
        require(all(ref in sources for ref in refs), f"unknown evidence ref: {group['group_slot_id']}")
        require(len([row for row in mapping["records"] if row["group_slot_id"] == group["group_slot_id"]]) == 3,
                f"triplet missing: {group['group_slot_id']}")
        if len(refs) == 3:
            slot = group["group_slot_id"]
            require(slot in PROPOSED_TWO_SOURCE_PROJECTION, f"unplanned three-source group: {slot}")
            pair = PROPOSED_TWO_SOURCE_PROJECTION[slot]
            require(set(pair).issubset(refs), f"projection not a frozen subset: {slot}")
            for alias in pair:
                compact = "".join(sources[alias]["text"].split())
                for phrase in REQUIRED_TEXT[alias]:
                    require("".join(phrase.split()) in compact, f"projection anchor missing: {alias} {phrase}")
            triples.append({
                "group_slot_id": slot,
                "original_frozen_refs": refs,
                "proposed_e1_e2_refs": pair,
                "privately_retained_not_projected": [ref for ref in refs if ref not in pair],
                "selected_snapshot_sha256": [sources[ref]["sha256"] for ref in pair],
                "literal_source_anchor_check": True,
                "owner_approval_required": True,
                "phase2_reviewer_release_authorized_by_this_preflight": False,
            })
    require(evidence_cards == {1: 15, 2: 13, 3: 2}, "frozen evidence-cardinality distribution drift")
    require(len(triples) == 2, "three-source group count drift")
    report = {
        "status": "EVIDENCE_PREFLIGHT_PASS_PHASE2_PROJECTION_OWNER_DECISION_PENDING",
        "source_manifest_sha256": evidence_sha,
        "group_manifest_sha256": groups_sha,
        "mapping_sha256": mapping_sha,
        "candidate_sha256": candidate_sha,
        "official_snapshots": 23,
        "raw_snapshot_hashes_pass": 23,
        "extracted_text_characters_total": total_extracted,
        "group_count": 30,
        "candidate_count": 90,
        "evidence_cardinality_by_group": {str(k): v for k, v in evidence_cards.items()},
        "two_source_projection_proposals": triples,
        "snapshot_audit": source_audit,
        "release_status": "WITHHELD_UNTIL_OWNER_BOUNDED_PROJECTION_DECISION_AND_RUN_ATTESTATION",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps({key: report[key] for key in ("status", "official_snapshots", "group_count", "candidate_count", "evidence_cardinality_by_group")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
