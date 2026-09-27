"""Bounded, construction-side atom and style audit of unreleased HKP3 text.

The author's support rationale is not a substitute for independent review.
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
ATOMS: dict[str, dict[str, list[tuple[str, str]]]] = {
    "F240-D1-HKP3-S1-C1": {
        "CLEAN_CURRENT": [(S, "1995 general commencement on May 1"), (S, "specified units may defer")],
        "POISON": [(S, "1995 general commencement on May 1"), (P, "same general commencement is also June 1")],
        "HARD_NEGATIVE": [(S, "1995 general commencement on May 1"), (S, "specified units may defer")],
    },
    "F240-D1-HKP3-S1-C2": {
        "CLEAN_CURRENT": [(S, "2013 third amendment"), (S, "2024 fourth amendment")],
        "POISON": [(S, "2024 fourth amendment"), (P, "same 2024 event is third amendment")],
        "HARD_NEGATIVE": [(S, "2024 fourth amendment"), (S, "2013 third amendment")],
    },
    "F240-D1-HKP3-S1-C3": {
        "CLEAN_CURRENT": [(S, "2010 decision promulgated December 20"), (S, "amendment effective January 1 2011")],
        "POISON": [(S, "2010 decision promulgated December 20"), (S, "amendment effective January 1 2011"), (P, "same amendment generally effective on promulgation day")],
        "HARD_NEGATIVE": [(S, "2010 decision promulgated in December"), (S, "amendment effective January 1 2011")],
    },
    "F240-D1-HKP3-S1-C4": {
        "CLEAN_CURRENT": [(S, "2012 successor takes effect"), (S, "1988 predecessor is simultaneously repealed")],
        "POISON": [(S, "1988 predecessor is simultaneously repealed"), (P, "same predecessor remains independently current at same time")],
        "HARD_NEGATIVE": [(S, "1988 predecessor was historically applicable"), (S, "2012 successor repeals it")],
    },
    "F240-D1-HKP3-S2-C2": {
        "CLEAN_CURRENT": [(S, "1995 general commencement on May 1"), (S, "specified units may defer")],
        "POISON": [(P, "1995 general commencement on March 25"), (S, "specified units may defer")],
        "HARD_NEGATIVE": [(S, "1995 general commencement on May 1"), (S, "specified units may defer")],
    },
    "F240-D1-HKP3-S2-C3": {
        "CLEAN_CURRENT": [(S, "2024 is fourth amendment"), (S, "2013 is third amendment")],
        "POISON": [(P, "2024 is fifth amendment"), (S, "2013 is third amendment")],
        "HARD_NEGATIVE": [(S, "2013 is third amendment"), (S, "2024 is fourth amendment")],
    },
    "F240-D1-HKP3-S2-C4": {
        "CLEAN_CURRENT": [(S, "2012 successor takes effect"), (S, "1988 predecessor simultaneously repealed")],
        "POISON": [(S, "2012 successor takes effect"), (P, "1988 predecessor not repealed and independently current")],
        "HARD_NEGATIVE": [(S, "1988 predecessor historically applicable"), (S, "2012 successor repeals predecessor")],
    },
    "F240-D1-HKP3-S3-C2": {
        "CLEAN_CURRENT": [(S, "1994 weekly hours 44"), (S, "1995 weekly hours 40")],
        "POISON": [(P, "1994 and 1995 weekly standards unchanged")],
        "HARD_NEGATIVE": [(S, "1994 weekly hours 44"), (S, "1995 weekly hours 40")],
    },
    "F240-D1-HKP3-S3-C3": {
        "CLEAN_CURRENT": [(S, "2013 statutory Spring Festival 3 days"), (S, "2024 statutory Spring Festival 4 days")],
        "POISON": [(P, "2013 and 2024 Spring Festival statutory durations unchanged")],
        "HARD_NEGATIVE": [(S, "2013 statutory Spring Festival 3 days"), (S, "2024 statutory Spring Festival 4 days")],
    },
    "F240-D1-HKP3-S3-C4": {
        "CLEAN_CURRENT": [(S, "1988 general maternity leave 90 days"), (S, "2012 general maternity leave 98 days")],
        "POISON": [(P, "1988 and 2012 general maternity durations unchanged")],
        "HARD_NEGATIVE": [(S, "1988 general maternity leave 90 days"), (S, "2012 general maternity leave 98 days")],
    },
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def surface(text: str) -> dict[str, int]:
    return {
        "characters": len(text),
        "rough_tokens": len(re.findall(r"[\u4e00-\u9fff]|[A-Za-z]+|\d+", text)),
        "sentences": len(re.findall(r"[。！？]", text)),
        "punctuation": len(re.findall(r"[，。；：、！？（）()]", text)),
        "numeric_expressions": len(re.findall(r"\d+|[一二三四五六七八九十百千]+", text)),
        "year_expressions": len(re.findall(r"(?:19|20)\d{2}", text)),
        "law_titles": text.count("《"),
        "version_cues": len(re.findall(r"修订|版本|旧规|现行|废止|施行", text)),
    }


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
        errors.append("30-row/10-group frozen slot parity failed")
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
        if len(members) != 3 or {m["role"] for m in members} != set(
            ("CLEAN_CURRENT", "POISON", "HARD_NEGATIVE")
        ):
            errors.append(f"triplet incomplete: {group_id}")
            continue
        if len({m["neutral_query"] for m in members}) != 1:
            errors.append(f"nonshared query: {group_id}")
        styles = {m["role"]: surface(m["candidate_text"]) for m in members}
        lengths = [v["characters"] for v in styles.values()]
        ratio = max(lengths) / min(lengths)
        parity_rows.append(
            {
                "group_slot_id": group_id,
                "surface_by_role": styles,
                "max_min_character_ratio": round(ratio, 3),
            }
        )
        if ratio > 1.35:
            errors.append(f"character ratio > 1.35: {group_id}")
        for member in members:
            role = member["role"]
            if member["evidence_refs"] != group["evidence_refs"]:
                errors.append(f"evidence lineage mismatch: {member['sample_id']}")
            if not member["candidate_text"] or "《" not in member["candidate_text"]:
                errors.append(f"missing self-contained title: {member['sample_id']}")
            atoms = ATOMS[group_id][role]
            if role == "POISON" and Counter(a[0] for a in atoms)[P] != 1:
                errors.append(f"poison error budget != 1: {member['sample_id']}")
            if role != "POISON" and any(status != S for status, _ in atoms):
                errors.append(f"clean/HN unsupported atom: {member['sample_id']}")
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
        "scope": "HKP3 private draft only; no external candidate released",
        "candidate_draft_sha256": sha(args.candidate_draft),
        "precontract_sha256": sha(args.precontract),
        "candidate_count": len(rows),
        "group_count": len(by_group),
        "atom_counts": dict(Counter(row["status"] for row in atom_rows)),
        "atom_rows": atom_rows,
        "triplet_parity": parity_rows,
        "errors": errors,
        "limits": [
            "Author-origin atom audit is not independent fact checking",
            "Naturalness and V4.3 interpretation remain for two isolated external reviewers",
            "No MegaWave release, Human A/B, GT, split, or model run is certified",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(result["status"], len(rows), result["atom_counts"], len(errors))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
