"""Materialize an additive D3 source-first plan repair, never touching prior inputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def write_new(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--anchors", type=Path, required=True)
    parser.add_argument("--overlay", type=Path, required=True)
    parser.add_argument("--output-plan", type=Path, required=True)
    parser.add_argument("--output-anchors", type=Path, required=True)
    args = parser.parse_args()
    if args.output_plan.exists() or args.output_anchors.exists():
        raise ValueError("Additive outputs already exist")
    plan = json.loads(args.plan.read_bytes())
    anchor_plan = json.loads(args.anchors.read_bytes())
    overlay = json.loads(args.overlay.read_bytes())
    replacements = {row["slot"]: row for row in overlay["replacements"]}
    if len(replacements) != len(overlay["replacements"]):
        raise ValueError("Duplicate replacement slot")
    original = {row["slot"] for row in plan["planned_facts"]}
    if not replacements.keys() <= original:
        raise ValueError("Replacement does not belong to frozen slots")
    new_facts = []
    for row in plan["planned_facts"]:
        replacement = replacements.get(row["slot"])
        if replacement is None:
            new_facts.append(row)
            continue
        new_facts.append({key: replacement[key] for key in
                          ("slot", "family", "core", "evidence_docs", "fact")})
        anchor_plan["anchors_by_slot_in_evidence_doc_order"][row["slot"]] = replacement["anchors"]
    plan["planned_facts"] = new_facts
    plan["status"] = "UNACCEPTED_SOURCE_FIRST_FACT_PLAN_V2_NO_CANDIDATES"
    plan["repair_overlay"] = args.overlay.name
    anchor_plan["status"] = "UNACCEPTED_PER_FACT_ANCHOR_PLAN_V2"
    anchor_plan["repair_overlay"] = args.overlay.name
    write_new(args.output_plan, plan)
    write_new(args.output_anchors, anchor_plan)
    print(json.dumps({"replaced": len(replacements), "facts": len(new_facts)}))


if __name__ == "__main__":
    main()
