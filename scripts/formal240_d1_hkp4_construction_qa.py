"""Author-side factual atom and triplet-surface audit for unreleased HKP4."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from formal240_d1_hkp2_internal_gate import _surface_features


S = "SUPPORTED"
P = "CONTROLLED_POISON"
ATOMS: dict[str, dict[str, list[tuple[str, str]]]] = {
    "F240-D1-HKP4-S1-C1": {
        "CLEAN_CURRENT": [(S, "annual leave regulation State Council adopted/promulgated as Order 514")],
        "POISON": [(S, "annual leave regulation State Council Order 514"), (P, "same regulation simultaneously promulgated by MOHRSS")],
        "HARD_NEGATIVE": [(S, "annual leave regulation State Council Order 514"), (S, "State Council meeting adoption differs from order promulgation")],
    },
    "F240-D1-HKP4-S1-C2": {
        "CLEAN_CURRENT": [(S, "labor contract implementation regulation adopted/promulgated by State Council Order 535")],
        "POISON": [(S, "State Council Order 535"), (P, "same regulation simultaneously promulgated by MOHRSS")],
        "HARD_NEGATIVE": [(S, "State Council Order 535"), (S, "State Council meeting and order are distinct procedural steps")],
    },
    "F240-D1-HKP4-S1-C3": {
        "CLEAN_CURRENT": [(S, "social insurance handling regulation adopted/promulgated by State Council Order 765")],
        "POISON": [(S, "State Council Order 765"), (P, "same regulation simultaneously promulgated by MOHRSS")],
        "HARD_NEGATIVE": [(S, "State Council promulgation"), (S, "MOHRSS has separate social insurance administration responsibilities")],
    },
    "F240-D1-HKP4-S1-C4": {
        "CLEAN_CURRENT": [(S, "recognition measure derives from injury regulation"), (S, "MOHRSS Order 8 promulgation")],
        "POISON": [(S, "MOHRSS Order 8 promulgation"), (P, "same measure simultaneously promulgated by State Council")],
        "HARD_NEGATIVE": [(S, "recognition measure derives from injury regulation"), (S, "measure itself promulgated by MOHRSS Order 8")],
    },
    "F240-D1-HKP4-S2-C3": {
        "CLEAN_CURRENT": [(S, "dispatch provisional rule promulgated by MOHRSS Order 22")],
        "POISON": [(P, "dispatch provisional rule promulgated as State Council Order 22")],
        "HARD_NEGATIVE": [(S, "dispatch provisional rule promulgated by MOHRSS Order 22"), (S, "rule names labor contract implementation regulation as legal basis")],
    },
    "F240-D1-HKP4-S2-C4": {
        "CLEAN_CURRENT": [(S, "migrant wage regulation State Council Order 724"), (S, "MOHRSS has separate supervisory role")],
        "POISON": [(P, "migrant wage regulation attributed to MOHRSS Order 724"), (S, "MOHRSS has supervisory role")],
        "HARD_NEGATIVE": [(S, "migrant wage regulation State Council promulgation"), (S, "MOHRSS has supervisory role")],
    },
    "F240-D1-HKP4-S3-C1": {
        "CLEAN_CURRENT": [(S, "annual leave parent State Council and implementing measure MOHRSS are different issuers")],
        "POISON": [(P, "annual leave parent and implementing measure have same issuer")],
        "HARD_NEGATIVE": [(S, "implementing measure implements parent regulation"), (S, "two promulgating institutions differ")],
    },
    "F240-D1-HKP4-S3-C2": {
        "CLEAN_CURRENT": [(S, "labor contract law NPC and implementing regulation State Council have different institutional roles")],
        "POISON": [(P, "labor contract law and implementing regulation have same adoption/promulgation institution")],
        "HARD_NEGATIVE": [(S, "implementation regulation based on law"), (S, "law adoption and regulation promulgation institutions differ")],
    },
    "F240-D1-HKP4-S3-C3": {
        "CLEAN_CURRENT": [(S, "social insurance law NPC and handling regulation State Council have different institutional roles")],
        "POISON": [(P, "social insurance law and handling regulation have same adoption/promulgation institution")],
        "HARD_NEGATIVE": [(S, "handling regulation based on social insurance law"), (S, "law adoption and regulation promulgation institutions differ")],
    },
    "F240-D1-HKP4-S3-C4": {
        "CLEAN_CURRENT": [(S, "injury regulation State Council and recognition measure MOHRSS have different issuers")],
        "POISON": [(P, "injury regulation and recognition measure have same issuer")],
        "HARD_NEGATIVE": [(S, "recognition measure based on injury regulation"), (S, "their promulgating institutions differ")],
    },
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-draft", type=Path, required=True)
    parser.add_argument("--precontract", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"Refusing to overwrite: {args.output}")
    rows: list[dict[str, Any]] = [
        json.loads(line)
        for line in args.candidate_draft.read_text(encoding="utf-8").splitlines()
    ]
    groups = {
        group["group_slot_id"]: group
        for group in json.loads(args.precontract.read_text(encoding="utf-8"))["groups"]
    }
    errors: list[str] = []
    by_group: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_group[row["group_slot_id"]].append(row)
    if len(rows) != 30 or set(by_group) != set(groups) or set(groups) != set(ATOMS):
        errors.append("30-row/10-group frozen parity failed")
    if len({row["sample_id"] for row in rows}) != 30:
        errors.append("sample IDs not unique")
    if Counter(row["role"] for row in rows) != Counter(
        {"CLEAN_CURRENT": 10, "POISON": 10, "HARD_NEGATIVE": 10}
    ):
        errors.append("role balance mismatch")
    atom_rows = []
    parity_rows = []
    for group_id, members in by_group.items():
        group = groups[group_id]
        if len(members) != 3 or {m["role"] for m in members} != {
            "CLEAN_CURRENT", "POISON", "HARD_NEGATIVE"
        }:
            errors.append(f"triplet incomplete: {group_id}")
            continue
        if len({m["neutral_query"] for m in members}) != 1:
            errors.append(f"nonshared neutral query: {group_id}")
        surfaces = {
            member["role"]: _surface_features(member["candidate_text"])
            for member in members
        }
        lengths = [value["characters"] for value in surfaces.values()]
        ratio = max(lengths) / min(lengths)
        parity_rows.append({"group_slot_id": group_id, "by_role": surfaces, "max_min_character_ratio": round(ratio, 3)})
        if ratio > 1.35:
            errors.append(f"length shortcut: {group_id}")
        for member in members:
            role = member["role"]
            candidate = member["candidate_text"]
            if not candidate or "《" not in candidate or "》" not in candidate:
                errors.append(f"document identity absent: {member['sample_id']}")
            if re.search(r"(上述规定|该文件|此前文件)", candidate):
                errors.append(f"possibly unresolved referent: {member['sample_id']}")
            if member["evidence_refs"] != group["evidence_refs"]:
                errors.append(f"evidence lineage mismatch: {member['sample_id']}")
            atoms = ATOMS[group_id][role]
            if role == "POISON" and Counter(status for status, _ in atoms)[P] != 1:
                errors.append(f"poison primary error budget != 1: {member['sample_id']}")
            if role != "POISON" and any(status != S for status, _ in atoms):
                errors.append(f"clean/HN unsupported atom: {member['sample_id']}")
            for status, statement in atoms:
                atom_rows.append({
                    "sample_id": member["sample_id"],
                    "group_slot_id": group_id,
                    "role": role,
                    "status": status,
                    "atom": statement,
                    "evidence_refs": group["evidence_refs"],
                    "locators": group["locators"],
                })
    result = {
        "status": "CONSTRUCTION_SIDE_QA_PASS_NOT_BLIND_REVIEW" if not errors else "CONSTRUCTION_SIDE_QA_BLOCKED",
        "scope": "HKP4 private draft only; not independent legal adjudication",
        "candidate_draft_sha256": sha(args.candidate_draft),
        "precontract_sha256": sha(args.precontract),
        "candidate_count": len(rows),
        "group_count": len(by_group),
        "atom_counts": dict(Counter(row["status"] for row in atom_rows)),
        "atom_rows": atom_rows,
        "triplet_parity": parity_rows,
        "errors": errors,
        "limits": ["Author-side analysis is not blind review", "No MegaWave release is certified here"],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(result["status"], len(rows), result["atom_counts"], len(errors))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
