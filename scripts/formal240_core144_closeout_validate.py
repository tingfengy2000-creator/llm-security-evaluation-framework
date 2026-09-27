"""Validate additive Core144 scope and D1 targeted Phase1 handoff without writing data."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from formal240_core144_scope import FORMAL240_MATRIX_SHA, build as build_core
from formal240_remaining90_authority_surface_audit import (
    FOUR_IDS,
    MAPPING_SHA,
    PACKET_SHA,
    RAW_SHAS,
    audit,
    pattern_flags,
)
from formal240_remaining90_phase1_validate import read_json, sha256


AUDIT_SHA = "9041ae942e8958dd92bf846a4565fe0270e564dc04d7ac2864cae06a397eb531"
CURRENT_SHA = "428548caba9d613de52f4f8d3a35260a89679ecc4c5a7c0cb8b6013543c2c44a"
REPAIR_SHA = "fd1e1b38d02c97520b316c0969edfb40f83c7361051de4f25bc0ebe3903de6ff"


def exact_json(path: Path, expected_sha: str) -> Any:
    obj, raw = read_json(path)
    if sha256(raw) != expected_sha:
        raise ValueError(f"SHA mismatch: {path.name}")
    return obj


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def main() -> None:
    parser = argparse.ArgumentParser()
    for name in ("matrix", "view", "selection", "packet", "mapping", "r3", "r4", "r5", "audit", "overlay", "current", "repair", "release"):
        parser.add_argument(f"--{name}", required=True, type=Path)
    args = parser.parse_args()
    view, selection = build_core(args.matrix.read_bytes())
    require(sha256(args.matrix.read_bytes()) == FORMAL240_MATRIX_SHA, "historical matrix changed")
    require(args.view.read_bytes() == view, "Core144 view not exact frozen subset")
    require(json.loads(args.selection.read_text(encoding="utf-8")) == selection, "Core144 selection drift")
    require(not selection["split_executed"] and not selection["training_started"], "scope overclaim")

    packet = exact_json(args.packet, PACKET_SHA)
    mapping = exact_json(args.mapping, MAPPING_SHA)
    for name in ("r3", "r4", "r5"):
        exact_json(getattr(args, name), RAW_SHAS[name])
    saved_audit = exact_json(args.audit, AUDIT_SHA)
    reproduced = audit(packet, mapping)
    for key, value in reproduced.items():
        require(saved_audit[key] == value, f"surface audit not reproduced: {key}")
    require(saved_audit["surface_shortcut_blocker"], "surface blocker was silently removed")

    overlay = json.loads(args.overlay.read_text(encoding="utf-8"))
    require({r["blind_review_id"] for r in overlay["local_internal_conflict_decisions"]} == FOUR_IDS, "Owner four IDs drift")
    require(all(r["owner_final"] == "YES" and r["r3_raw"] == "NO" for r in overlay["local_internal_conflict_decisions"]), "Owner decision/raw drift")
    require(len(overlay["naturalness_decisions"]) == 6 and all(r["owner_disposition"] == "NONBLOCKING_REVIEWER_VARIANCE" for r in overlay["naturalness_decisions"]), "six naturalness dispositions drift")
    require(not overlay["majority_vote_used"] and not overlay["raw_returns_modified"], "invalid provenance")

    current = exact_json(args.current, CURRENT_SHA)["records"]
    repairs = exact_json(args.repair, REPAIR_SHA)["records"]
    old = packet["records"]
    require(len(current) == len(old) == 90 and len(repairs) == 4, "population drift")
    require(len({r["blind_review_id"] for r in current}) == 90, "duplicate new ID")
    require(sum(a == b for a, b in zip(old, current)) == 86, "86 unchanged ID/text parity failed")
    old_ids = {r["old_blind_review_id"] for r in repairs}
    new_ids = {r["new_blind_review_id"] for r in repairs}
    require(old_ids == FOUR_IDS and len(new_ids) == 4 and not new_ids.intersection({r["blind_review_id"] for r in old}), "repair identity drift")
    require(all(not r["evidence_changed"] and not r["fact_atoms_changed"] and r["triplet_length_ratio"] < 1.2 for r in repairs), "repair evidence/fact/style parity failed")
    require(all(not pattern_flags(r["candidate_text"])["authority_exact_clause"] for r in current), "old shortcut retained")
    root = args.release
    schema = root / "PAPER1_FORMAL_D1_REMAINING90_TARGETED4_PHASE1_IMPORT_SCHEMA_V2.json"
    require(schema.exists(), "release schema missing")
    for stem in ("R3_GPT", "R4_CODEX"):
        name = f"PAPER1_FORMAL_D1_REMAINING90_{stem}_TARGETED4_PHASE1_PACKAGE_V2.json"
        prompt = f"PAPER1_FORMAL_D1_REMAINING90_{stem}_TARGETED4_PHASE1_PROMPT_V2.md"
        release_rows = json.loads((root / name).read_text(encoding="utf-8"))["records"]
        require(len(release_rows) == 4 and {r["blind_review_id"] for r in release_rows} == new_ids, f"{stem} release IDs drift")
        require(all(set(r) == {"blind_review_id", "candidate_text"} for r in release_rows), f"{stem} hidden field leak")
        require({r["candidate_text"] for r in release_rows} == {r["new_text"] for r in repairs}, f"{stem} text drift")
        require((root / prompt).exists(), f"{stem} prompt missing")
    for path in root.iterdir():
        require(path.is_file() and path.suffix in {".json", ".md"}, "unexpected release file")
        data = path.read_text(encoding="utf-8")
        require(not data.startswith("\ufeff"), "UTF-8 BOM in reviewer release")
        for forbidden in ("CONTROLLED_POISON", "HARD_NEGATIVE", "target_stealth_design", "group_slot_id", "sample_id", "EXPECTED_V3"):
            require(forbidden not in data, f"reviewer release hidden-context leak: {path.name}")

    result = {
        "status": "PASS_TARGETED_PHASE1_REVIEW_REQUIRED",
        "core_groups": selection["group_count"],
        "core_planned_candidates": selection["candidate_count_planned"],
        "raw_hashes_unchanged": True,
        "old_candidates_unchanged": 86,
        "targeted_repair_count": 4,
        "phase2_release_authorized": False,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
