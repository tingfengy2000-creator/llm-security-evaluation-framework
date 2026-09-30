"""Mechanical draft QA. It never converts writer role into factual support."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inspect(spec: dict[str, Any]) -> dict[str, Any]:
    rows = spec["triplets"]
    domain = spec["domain"]
    cells: Counter[str] = Counter()
    surfaces: list[dict[str, Any]] = []
    flags = []
    grams: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        cells["-".join(row["fact_id"].split("-")[:2])] += 1
        text_by_role = {role: "".join(row[role]) for role in "CPH"}
        if len(set(text_by_role.values())) < 3:
            flags.append({"group": row["fact_id"], "code": "DUPLICATE_TRIPLET_TEXT"})
        for role, text in text_by_role.items():
            if re.search(r"Poison|CLEAN_CURRENT|HARD_NEGATIVE|HKP[1-4]|Phase[12]|GT|Expected", text):
                flags.append({"group": row["fact_id"], "code": "EXPERIMENT_LANGUAGE", "role": role})
            if re.search(r"该文件|上述规定|此办法", text):
                flags.append({"group": row["fact_id"], "code": "REFERENT_REVIEW_REQUIRED", "role": role})
            if len(text) < 25:
                flags.append({"group": row["fact_id"], "code": "UNDERDEVELOPED_TEXT", "role": role})
            for gram in set(text[i:i + 4] for i in range(len(text) - 3)):
                grams[role][gram] += 1
        lengths = {r: len(t) for r, t in text_by_role.items()}
        ratio = max(lengths.values()) / min(lengths.values())
        similarity = SequenceMatcher(None, text_by_role["C"], text_by_role["H"]).ratio()
        if ratio > 1.4:
            flags.append({"group": row["fact_id"], "code": "LENGTH_REVIEW_REQUIRED", "ratio": ratio})
        if similarity > 0.85:
            flags.append({"group": row["fact_id"], "code": "HN_PARAPHRASE_REVIEW_REQUIRED", "similarity": similarity})
        surfaces.append({"group": row["fact_id"], "lengths": lengths,
                         "max_min_length_ratio": ratio, "C_H_sequence_similarity": similarity,
                         "per_role": {r: {"sentence_count": t.count("。"),
                                          "number_count": len(re.findall(r"\d+|[一二三四五六七八九十百]+", t)),
                                          "law_title_count": t.count("《"),
                                          "date_count": len(re.findall(r"\d{4}年", t)),
                                          "punctuation_count": len(re.findall(r"[，。；：、]", t)),
                                          "version_cues": len(re.findall(r"修正|修订|现行|施行|废止|原始", t)),
                                          "history_cues": len(re.findall(r"历史|原于|旧|原始", t))}
                                      for r, t in text_by_role.items()}})
    exclusive = []
    for role in "CPH":
        others = set().union(*(grams[r] for r in "CPH" if r != role))
        for gram, count in grams[role].items():
            if count >= 5 and gram not in others:
                exclusive.append({"role": role, "gram": gram, "candidate_count": count,
                                  "status": "MANUAL_SHORTCUT_REVIEW_REQUIRED_NOT_AUTO_PASS"})
    exact = (len(rows) == 48 and len({r["fact_id"] for r in rows}) == 48
             and len(cells) == 12 and set(cells.values()) == {4})
    return {"domain": domain, "groups": len(rows), "draft_texts": 3 * len(rows),
            "cell_counts": dict(sorted(cells.items())), "structural_counts_pass": exact,
            "surface_rows": surfaces, "flags": flags,
            "role_exclusive_frequent_4grams": sorted(exclusive, key=lambda r: (-r["candidate_count"], r["gram"])),
            "semantic_atoms_validated": False, "full_source_ablation_validated": False,
            "domain_accepted": False, "reviewer_release_allowed": False,
            "status": "MECHANICAL_DRAFT_QA_ONLY_SEMANTIC_GATES_NOT_BYPASSED"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--draft", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = inspect(json.loads(args.draft.read_bytes()))
    result["draft_sha256"] = sha(args.draft)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps({"groups": result["groups"], "draft_texts": result["draft_texts"],
                      "flags": result["flags"], "exclusive_grams": result["role_exclusive_frequent_4grams"]},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
