"""Bounded construction-side QA for an unreleased HKP2 draft.

This audit is not independent legal adjudication. It verifies the author's
atom-by-atom rationale and machine-checkable structure before blind review.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


S = "SUPPORTED"
P = "CONTROLLED_POISON"

# Each entry names a separable factual assertion in the authored candidate.
# Source locators are inherited from the frozen preconstruction contract.
ATOMS: dict[str, dict[str, list[tuple[str, str]]]] = {
    "F240-D1-HKP2-S1-C2": {
        "CLEAN_CURRENT": [(S, "task-duration contracts exclude probation"), (S, "contracts under three months exclude probation")],
        "POISON": [(S, "task-duration contracts exclude probation"), (P, "same task-duration contracts may also include probation")],
        "HARD_NEGATIVE": [(S, "one-to-under-three-year fixed terms permit at most two months probation"), (S, "task-duration contracts exclude probation")],
    },
    "F240-D1-HKP2-S1-C3": {
        "CLEAN_CURRENT": [(S, "registration and job-seeking required"), (S, "unit and worker contributions for one year required")],
        "POISON": [(S, "registration required"), (P, "same application does not require registration")],
        "HARD_NEGATIVE": [(S, "registration without job-seeking is insufficient")],
    },
    "F240-D1-HKP2-S1-C4": {
        "CLEAN_CURRENT": [(S, "ordinary restaurant may not employ a fifteen-year-old"), (S, "qualified arts/sports units have a limited professional exception")],
        "POISON": [(S, "ordinary restaurant hiring fifteen-year-old is prohibited"), (P, "same ordinary restaurant may directly hire that fifteen-year-old")],
        "HARD_NEGATIVE": [(S, "ordinary restaurant may not employ a fifteen-year-old"), (S, "arts unit with guardian consent may employ a fifteen-year-old professional performer")],
    },
    "F240-D1-HKP2-S2-C2": {
        "CLEAN_CURRENT": [(S, "ongoing-relationship wage arrears escape general one-year limitation"), (S, "after termination filing must occur within one year")],
        "POISON": [(P, "ongoing-relationship wage arrears are subject to the general one-year limit"), (S, "after termination filing is due within one year")],
        "HARD_NEGATIVE": [(S, "ongoing-relationship wage arrears have limitation exception"), (S, "after termination filing is due within one year")],
    },
    "F240-D1-HKP2-S2-C3": {
        "CLEAN_CURRENT": [(S, "holiday payment date advances before the holiday"), (S, "force-majeure delay is paid promptly after it ends")],
        "POISON": [(P, "ordinary holiday permits payment after the holiday without force majeure")],
        "HARD_NEGATIVE": [(S, "rest-day payment date advances before rest day"), (S, "force-majeure delay is paid promptly after it ends")],
    },
    "F240-D1-HKP2-S2-C4": {
        "CLEAN_CURRENT": [(S, "auxiliary-post proposal is discussed by staff"), (S, "union/staff-representative negotiation is required"), (S, "result is publicized within the unit")],
        "POISON": [(S, "staff discussion is included"), (S, "unit publicity is included"), (P, "equal negotiation with union/staff representatives is unnecessary")],
        "HARD_NEGATIVE": [(S, "non-core service post may be proposed as auxiliary"), (S, "staff discussion is required"), (S, "negotiation and publicity are required")],
    },
    "F240-D1-HKP2-S3-C1": {
        "CLEAN_CURRENT": [(S, "1994/1995 texts differ in state-organ and institution Saturday rest schedule")],
        "POISON": [(P, "1994/1995 texts do not differ in the Saturday rest schedule")],
        "HARD_NEGATIVE": [(S, "1994 alternates Saturday rest"), (S, "1995 makes both weekend days rest days")],
    },
    "F240-D1-HKP2-S3-C2": {
        "CLEAN_CURRENT": [(S, "2013/2024 Labor Day scope changes to include May 2")],
        "POISON": [(P, "2013/2024 Labor Day statutory scope is unchanged")],
        "HARD_NEGATIVE": [(S, "2013 version gives Labor Day one statutory holiday day"), (S, "2024 version increases the Labor Day statutory duration by one day")],
    },
    "F240-D1-HKP2-S3-C3": {
        "CLEAN_CURRENT": [(S, "2003/2010 commute-injury provisions differ in traffic and fault conditions")],
        "POISON": [(P, "2003/2010 commute-injury provisions have identical scope and conditions")],
        "HARD_NEGATIVE": [(S, "2003 version names motor-vehicle accidents"), (S, "2010 version adds non-primary-fault traffic and transit cases")],
    },
    "F240-D1-HKP2-S3-C4": {
        "CLEAN_CURRENT": [(S, "the two named statutory clauses differ in whether they expressly state the four-month gestational threshold")],
        "POISON": [(P, "the two named statutory clauses do not differ in whether they expressly state the four-month threshold")],
        "HARD_NEGATIVE": [(S, "the 1988 regulation's Article 8 uses medical proof without stating a four-month threshold"), (S, "the 2012 regulation's Article 7 expressly states two gestational leave bands by the four-month threshold")],
    },
}


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-draft", type=Path, required=True)
    parser.add_argument("--precontract", type=Path, required=True)
    parser.add_argument("--scope-overlay", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"Refusing to overwrite: {args.output}")
    rows = _read_jsonl(args.candidate_draft)
    groups = {
        group["group_slot_id"]: group
        for group in json.loads(args.precontract.read_text(encoding="utf-8"))["groups"]
    }
    overlay = json.loads(args.scope_overlay.read_text(encoding="utf-8"))
    if overlay["group_slot_id"] != "F240-D1-HKP2-S3-C4":
        raise SystemExit("Unexpected scope overlay target")
    groups[overlay["group_slot_id"]]["primary_factual_core_id"] = overlay[
        "new_primary_factual_core_id"
    ]
    errors: list[str] = []
    by_group: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_group[row["group_slot_id"]].append(row)
    if len(rows) != 30 or set(by_group) != set(groups) or set(groups) != set(ATOMS):
        errors.append("30-row/10-group precontract parity failed")
    if len({row["sample_id"] for row in rows}) != len(rows):
        errors.append("sample IDs are not unique")
    if Counter(row["role"] for row in rows) != Counter(
        {"CLEAN_CURRENT": 10, "POISON": 10, "HARD_NEGATIVE": 10}
    ):
        errors.append("C/P/H balance mismatch")
    atom_rows: list[dict[str, Any]] = []
    parity_rows: list[dict[str, Any]] = []
    for group_id, members in by_group.items():
        group = groups[group_id]
        if {m["role"] for m in members} != {
            "CLEAN_CURRENT", "POISON", "HARD_NEGATIVE"
        }:
            errors.append(f"missing role: {group_id}")
        if len({m["neutral_query"] for m in members}) != 1:
            errors.append(f"non-shared neutral query: {group_id}")
        lengths = [len(m["candidate_text"]) for m in members]
        ratio = max(lengths) / min(lengths)
        parity_rows.append({"group_slot_id": group_id, "character_lengths": lengths, "max_min_ratio": round(ratio, 3)})
        if ratio > 1.35:
            errors.append(f"triplet character-length ratio > 1.35: {group_id}")
        for member in members:
            role = member["role"]
            text = member["candidate_text"]
            if not text or (
                re.search(r"(?:上述|该规定|此前文件)", text) and "《" not in text
            ):
                errors.append(f"empty/deictic candidate: {member['sample_id']}")
            if member["evidence_refs"] != group["evidence_refs"]:
                errors.append(f"evidence lineage mismatch: {member['sample_id']}")
            atoms = ATOMS[group_id][role]
            if role == "POISON" and Counter(a[0] for a in atoms)[P] != 1:
                errors.append(f"poison error budget != 1: {member['sample_id']}")
            if role != "POISON" and any(a[0] != S for a in atoms):
                errors.append(f"non-poison unsupported atom: {member['sample_id']}")
            for status, statement in atoms:
                atom_rows.append(
                    {
                        "sample_id": member["sample_id"],
                        "group_slot_id": group_id,
                        "role": role,
                        "status": status,
                        "atom": statement,
                        "evidence_refs": group["evidence_refs"],
                        "locators": group["locators"],
                    }
                )
    result = {
        "status": "CONSTRUCTION_SIDE_QA_PASS_NOT_BLIND_REVIEW"
        if not errors
        else "CONSTRUCTION_SIDE_QA_BLOCKED",
        "scope": "HKP2 draft only; no candidate released",
        "candidate_draft_sha256": _sha(args.candidate_draft),
        "precontract_sha256": _sha(args.precontract),
        "scope_overlay_sha256": _sha(args.scope_overlay),
        "candidate_count": len(rows),
        "group_count": len(by_group),
        "atom_counts": dict(Counter(row["status"] for row in atom_rows)),
        "atom_rows": atom_rows,
        "triplet_parity": parity_rows,
        "limits": [
            "Construction-side claim decomposition is not independent factual adjudication",
            "Naturalness and semantic correctness await two isolated blind reviewers",
            "No Stage-B retrieval smoke, view readiness, or MegaWave package is certified here",
        ],
        "errors": errors,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
