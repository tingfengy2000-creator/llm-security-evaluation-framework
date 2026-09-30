"""Audit construction-author claim IR against byte-locked official atoms.

An explicit text-to-IR interpretation is not automatic entailment, external
review, Expected, or GT. No role automatically produces a support verdict.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evaluate(claim: dict[str, Any], atoms: dict[str, Any]) -> tuple[Any, list[str]]:
    refs = claim["refs"]
    values = [atoms[ref]["value"] for ref in refs]
    op = claim["op"]
    if op == "IDENTITY":
        value = values[0]
    elif op == "LT":
        value = values[0] < values[1]
    elif op == "GT":
        value = values[0] > values[1]
    elif op == "EQUAL":
        value = values[0] == values[1]
    elif op == "YEAR_GAP":
        value = abs(int(values[0][:4]) - int(values[1][:4]))
    elif op == "YEAR":
        value = int(values[0][:4])
    elif op == "CONTAINS":
        value = claim["member"] in values[0]
    elif op == "MATCHES_ACTOR":
        value = values[0] == claim["actor"]
    else:
        raise ValueError(f"Unknown IR operation: {op}")
    return value, sorted({atoms[ref]["doc"] for ref in refs})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--atoms", type=Path, required=True)
    parser.add_argument("--draft", type=Path, required=True)
    parser.add_argument("--claims", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    atom_lock = json.loads(args.atoms.read_bytes())
    atoms = {a["id"]: a for a in atom_lock["atoms"]}
    draft = json.loads(args.draft.read_bytes())
    texts = {r["fact_id"]: {role: "".join(r[role]) for role in "CPH"}
             for r in draft["triplets"]}
    specification = json.loads(args.claims.read_bytes())
    records = []
    blockers = []
    derivations = []
    for group in specification["groups"]:
        group_id = group["fact_id"]
        false_by_role: dict[str, list[dict[str, Any]]] = {}
        for role in "CPH":
            declarations = group[role]
            false_by_role[role] = []
            for index, claim in enumerate(declarations):
                value, docs = evaluate(claim, atoms)
                supported = value == claim["asserted_value"]
                designed = claim.get("controlled_root") == group["primary_root"]
                status = ("SUPPORTED" if supported else "CONTROLLED_POISON"
                          if designed else "UNSUPPORTED_ACCIDENTAL")
                if status == "UNSUPPORTED_ACCIDENTAL" or (role != "P" and not supported):
                    blockers.append({"group": group_id, "role": role,
                                     "code": "FALSE_UNDESIGNED_ATOM", "atom": index})
                if not supported:
                    false_by_role[role].append(claim)
                records.append({"group": group_id, "role": role, "atom_index": index,
                                "text_sha256": hashlib.sha256(texts[group_id][role].encode()).hexdigest(),
                                "source_expected_value": value, "status": status,
                                "source_documents": docs, "declaration": claim,
                                "source_refs": [atoms[r] for r in claim["refs"]]})
            if not declarations or not group["text_to_ir_review"][role]:
                blockers.append({"group": group_id, "role": role, "code": "IR_REVIEW_ABSENT"})
        false = false_by_role["P"]
        if not false or len({c.get("controlled_root") for c in false}) != 1:
            blockers.append({"group": group_id, "code": "CORRUPTION_ROOT_NOT_SINGLE"})
        local = group.get("local_contradiction")
        if local:
            # Validate separately interpreted same-field contradictory assertions.
            left = group["P"][local[0]]
            right = group["P"][local[1]]
            conflict = (left["field_identity"] == right["field_identity"]
                        and left["asserted_value"] != right["asserted_value"]
                        and left["scope"] == right["scope"])
            derived = "S1" if conflict else "INVALID_LOCAL_PATH"
        else:
            primary = false[0] if false else None
            docs = evaluate(primary, atoms)[1] if primary else []
            if len(docs) == 1:
                derived = "S2"
            elif len(docs) > 1 and group.get("full_source_ablation", {}).get("semantic_necessity_review"):
                derived = "S3"
            else:
                derived = "UNRESOLVED_EVIDENCE_NECESSITY"
        target = group_id.split("-")[1]
        if derived != target:
            blockers.append({"group": group_id, "code": "STEALTH_DESIGN_MISMATCH",
                             "derived": derived, "target": target})
        derivations.append({"group": group_id, "derived": derived, "target": target,
                            "full_source_ablation": group.get("full_source_ablation")})
    ids = [g["fact_id"] for g in specification["groups"]]
    if set(ids) != set(texts) or len(ids) != 48:
        blockers.append({"code": "DOMAIN_ID_MISMATCH"})
    result = {"source_atom_lock_sha256": sha(args.atoms), "draft_sha256": sha(args.draft),
              "claim_ir_sha256": sha(args.claims), "records": records,
              "derivations": derivations, "blockers": blockers,
              "locked_utc": datetime.now(timezone.utc).isoformat(),
              "interpretation_role": "SOURCE_BOUND_CONSTRUCTION_AUTHOR_NOT_INDEPENDENT_REVIEW",
              "automatic_entailment_claimed": False,
              "semantic_atom_coverage_is_explicit_author_review": True,
              "status": "PASS_DECLARED_IR_CHECKS" if not blockers else "FAIL",
              "domain_acceptance_not_implied": True}
    with args.output.open("xb") as stream:
        stream.write((json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode())
    print(json.dumps({"atoms": len(records), "blockers": blockers}, ensure_ascii=False))


if __name__ == "__main__":
    main()
