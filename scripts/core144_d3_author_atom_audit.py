"""Lock explicit D3 construction-author atom interpretations and S derivation.

This cannot prove legal entailment. It makes each author interpretation,
source unit, text identity and evidence-necessity rationale auditable before
independent blind review. No C/P/H role is automatically deemed correct.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from core144_normalized_source_atoms import load_sources


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_bytes())


def main() -> None:
    parser = argparse.ArgumentParser()
    for name in ("draft", "plan", "author", "s1", "s3", "mechanical", "captures", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError("Refusing to overwrite atom audit")
    draft = load(args.draft)
    plan = load(args.plan)
    author = load(args.author)
    local = load(args.s1)
    ablation = load(args.s3)
    screen = load(args.mechanical)
    source = load_sources(args.captures)
    rows = {r["fact_id"]: r for r in draft["triplets"]}
    facts = {r["slot"]: r for r in plan["planned_facts"]}
    notes = {r["fact_id"]: r for r in author["groups"]}
    s1 = {r["fact_id"]: r for r in local["records"]}
    s3 = {r["fact_id"]: r for r in ablation["records"]}
    mechanical = {r["fact_id"]: r for r in screen["rows"]}
    blockers: list[dict[str, Any]] = []
    if not (len(rows) == len(facts) == len(notes) == 48 and set(rows) == set(facts) == set(notes)):
        blockers.append({"code": "FACT_DRAFT_AUTHOR_SET_MISMATCH"})
    if len(s1) != 16 or len(s3) != 16 or len(mechanical) != 16:
        blockers.append({"code": "LOCAL_OR_ABLATION_COUNT_MISMATCH"})
    records: list[dict[str, Any]] = []
    derivations: list[dict[str, Any]] = []
    for fact_id in sorted(set(rows) & set(facts) & set(notes)):
        row = rows[fact_id]
        fact = facts[fact_id]
        note = notes[fact_id]
        docs = fact["evidence_docs"]
        if not docs or any(doc not in source for doc in docs):
            blockers.append({"group": fact_id, "code": "MISSING_FROZEN_EVIDENCE"})
            continue
        for role, key in (("C", "C"), ("P", "P_supported"), ("H", "H")):
            atoms = note[key]
            if role != "P" and not atoms:
                blockers.append({"group": fact_id, "role": role, "code": "NO_SUPPORTED_ATOMS"})
            for index, statement in enumerate(atoms):
                if not isinstance(statement, str) or len(statement) < 5:
                    blockers.append({"group": fact_id, "role": role, "code": "EMPTY_ATOM"})
                    continue
                records.append({"group": fact_id, "role": role, "atom_index": index,
                                "statement": statement, "status": "SUPPORTED",
                                "interpretation": "CONSTRUCTION_AUTHOR_PENDING_BLIND_VALIDATION",
                                "source_documents": docs,
                                "source_raw_sha256": {doc: source[doc]["raw_sha256"] for doc in docs},
                                "text_sha256": sha("".join(row[role]).encode())})
        false_atoms = note["P_controlled"]
        if len(false_atoms) != 1 or not isinstance(false_atoms[0], str) or len(false_atoms[0]) < 5:
            blockers.append({"group": fact_id, "role": "P", "code": "PRIMARY_CORRUPTION_NOT_SINGLE"})
        else:
            records.append({"group": fact_id, "role": "P", "atom_index": len(note["P_supported"]),
                            "statement": false_atoms[0], "status": "CONTROLLED_POISON",
                            "controlled_root": f"{fact_id}_PRIMARY_CORRUPTION",
                            "interpretation": "CONSTRUCTION_AUTHOR_PENDING_BLIND_VALIDATION",
                            "source_documents": docs,
                            "source_raw_sha256": {doc: source[doc]["raw_sha256"] for doc in docs},
                            "text_sha256": sha("".join(row["P"]).encode())})
        if fact_id in s1:
            pair = s1[fact_id]
            poison = "".join(row["P"])
            if pair["left"] not in poison or pair["right"] not in poison or not pair["same_scope"]:
                blockers.append({"group": fact_id, "code": "LOCAL_VISIBLE_PAIR_NOT_ESTABLISHED"})
            derived = "S1"
            path: dict[str, Any] = {"candidate_only_left": pair["left"],
                                    "candidate_only_right": pair["right"],
                                    "same_scope": pair["same_scope"],
                                    "minimum_evidence": "ZERO_EXTERNAL_EVIDENCE_REQUIRED"}
        elif fact_id in s3:
            review = s3[fact_id]
            if docs != [review["left"], review["right"]] or not all(
                review[key] for key in ("left_only", "right_only", "joint")
            ):
                blockers.append({"group": fact_id, "code": "S3_ABLATION_SOURCE_MISMATCH"})
            if mechanical[fact_id]["single_page_with_both_anchor_sets"]:
                blockers.append({"group": fact_id, "code": "S3_SINGLE_PAGE_CROSS_ANCHOR_REVIEW_BLOCKER"})
            derived = "S3"
            path = {"left_only": review["left_only"], "right_only": review["right_only"],
                    "joint": review["joint"],
                    "minimum_evidence": "MULTI_EVIDENCE_OR_VERSION_CHAIN",
                    "mechanical_cross_anchor_screen_is_not_semantic_proof": True}
        else:
            derived = "S2" if len(docs) == 1 else "UNRESOLVED_EVIDENCE_NECESSITY"
            path = {"single_full_official_page": docs[0] if len(docs) == 1 else None,
                    "minimum_evidence": "ONE_OFFICIAL_EVIDENCE" if len(docs) == 1 else None}
        target = fact_id.split("-")[1]
        if derived != target:
            blockers.append({"group": fact_id, "code": "DERIVED_S_MISMATCH",
                             "derived": derived, "target": target})
        derivations.append({"group": fact_id, "target": target, "derived": derived,
                            "full_source_ablation": path})
    if Counter(r["status"] for r in records)["CONTROLLED_POISON"] != 48:
        blockers.append({"code": "CONTROLLED_POISON_COUNT_NOT_48"})
    result = {"domain": "D3", "draft_sha256": sha(args.draft.read_bytes()),
              "plan_sha256": sha(args.plan.read_bytes()),
              "author_review_sha256": sha(args.author.read_bytes()),
              "s1_author_sha256": sha(args.s1.read_bytes()),
              "s3_author_sha256": sha(args.s3.read_bytes()),
              "records": records, "derivations": derivations, "blockers": blockers,
              "counts": dict(Counter(r["status"] for r in records)),
              "locked_utc": datetime.now(timezone.utc).isoformat(),
              "semantic_support_is_author_interpretation_not_automatic_entailment": True,
              "external_blind_review_pending": True, "ground_truth_not_created": True,
              "status": "INTERNAL_AUTHOR_QA_PASS" if not blockers else "FAIL_CLOSED"}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps({"records": len(records), "counts": result["counts"],
                      "blockers": blockers}, ensure_ascii=False))


if __name__ == "__main__":
    main()
