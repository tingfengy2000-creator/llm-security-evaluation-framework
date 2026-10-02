"""Read-only D3 source/fact-plan preflight; no candidate or GT access."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _norm(value: str) -> str:
    return re.sub(r"\s", "", value)


def inspect(plan: dict[str, Any], metadata: dict[str, Any], captures: Path,
            anchor_plan: dict[str, Any] | None = None) -> dict[str, Any]:
    records: dict[str, dict[str, Any]] = {}
    failures: list[dict[str, str]] = []
    for registry_path in sorted(captures.glob("source_capture_v*/snapshot_registry.json")):
        registry = json.loads(registry_path.read_bytes())
        for row in registry["records"]:
            source_id = row["evidence_doc_id"]
            if source_id in records:
                failures.append({"code": "DUPLICATE_SOURCE_ID", "source": source_id})
                continue
            raw_path = registry_path.parent / "raw" / f"{source_id}.bin"
            text_path = registry_path.parent / "text" / f"{source_id}.txt"
            if _sha(raw_path.read_bytes()) != row.get("raw_sha256"):
                failures.append({"code": "RAW_SHA_MISMATCH", "source": source_id})
            text_bytes = text_path.read_bytes()
            if _sha(text_bytes) != row.get("text_sha256"):
                failures.append({"code": "TEXT_SHA_MISMATCH", "source": source_id})
            if row.get("capture_status") != "CAPTURED_IDENTITY_ANCHORS_PRESENT":
                failures.append({"code": "CAPTURE_IDENTITY_FAILED", "source": source_id})
            records[source_id] = {**row, "text": text_bytes.decode("utf-8")}

    cells: dict[str, list[dict[str, Any]]] = defaultdict(list)
    used_sources: set[str] = set()
    for fact in plan["planned_facts"]:
        slot = fact["slot"]
        if not re.fullmatch(r"HKP[1-4]-S[1-3]-C[1-4]", slot):
            failures.append({"code": "BAD_SLOT", "slot": slot})
        cells["-".join(slot.split("-")[:2])].append(fact)
        if (slot.split("-")[1] == "S3") != (len(fact["evidence_docs"]) == 2):
            failures.append({"code": "EVIDENCE_PATH_CARDINALITY", "slot": slot})
        for source_id in fact["evidence_docs"]:
            used_sources.add(source_id)
            if source_id not in records or source_id not in metadata["documents"]:
                failures.append({"code": "UNBOUND_SOURCE", "slot": slot, "source": source_id})
        if anchor_plan is not None:
            declared = anchor_plan["anchors_by_slot_in_evidence_doc_order"].get(slot)
            if declared is None or len(declared) != len(fact["evidence_docs"]):
                failures.append({"code": "PER_FACT_ANCHOR_CARDINALITY", "slot": slot})
            else:
                for source_id, anchors in zip(fact["evidence_docs"], declared, strict=True):
                    if source_id not in records or not anchors:
                        continue
                    visible = _norm(records[source_id]["text"])
                    for anchor in anchors:
                        if _norm(anchor) not in visible:
                            failures.append({"code": "FACT_ANCHOR_ABSENT", "slot": slot,
                                             "source": source_id, "anchor": anchor})
    for cell, facts in cells.items():
        if len(facts) != 4 or len({f["family"] for f in facts}) != 4:
            failures.append({"code": "CELL_NOT_FOUR_INDEPENDENT_FAMILIES", "cell": cell})
        if len({f["core"] for f in facts}) != 4:
            failures.append({"code": "CELL_FACTUAL_CORE_DUPLICATE", "cell": cell})
    if len(plan["planned_facts"]) != 48 or len(cells) != 12:
        failures.append({"code": "FROZEN_SLOT_COUNT_MISMATCH"})
    if set(metadata["documents"]) != used_sources:
        failures.append({"code": "METADATA_SOURCE_SET_MISMATCH"})
    if anchor_plan is not None and set(anchor_plan["anchors_by_slot_in_evidence_doc_order"]) != {
            fact["slot"] for fact in plan["planned_facts"]}:
        failures.append({"code": "PER_FACT_ANCHOR_SLOT_SET_MISMATCH"})
    for source_id in sorted(used_sources & records.keys() & metadata["documents"].keys()):
        document = metadata["documents"][source_id]
        visible = _norm(records[source_id]["text"])
        for anchor in document["metadata_anchors"]:
            if _norm(anchor) not in visible:
                failures.append({"code": "METADATA_ANCHOR_ABSENT", "source": source_id,
                                 "anchor": anchor})

    # This is a conservative *diagnostic*, not a formal split. A comparison
    # using two documents creates an overlap edge; transitive closure reveals
    # how many truly disjoint evidence-source islands the plan has.
    parent = {source_id: source_id for source_id in used_sources}

    def find(source_id: str) -> str:
        while parent[source_id] != source_id:
            parent[source_id] = parent[parent[source_id]]
            source_id = parent[source_id]
        return source_id

    for fact in plan["planned_facts"]:
        docs = fact["evidence_docs"]
        for source_id in docs[1:]:
            parent[find(source_id)] = find(docs[0])
    family_first: dict[str, str] = {}
    for source_id in sorted(used_sources):
        family = metadata["documents"][source_id]["family"]
        if family in family_first:
            parent[find(source_id)] = find(family_first[family])
        else:
            family_first[family] = source_id
    components: dict[str, list[str]] = defaultdict(list)
    for source_id in sorted(used_sources):
        components[find(source_id)].append(source_id)
    overlap_cells = []
    for cell, facts in cells.items():
        component_ids = [find(f["evidence_docs"][0]) for f in facts]
        if len(set(component_ids)) < len(component_ids):
            overlap_cells.append({"cell": cell, "source_overlap_component_ids": component_ids,
                                  "status": "SPLIT_FAMILY_REVIEW_REQUIRED_NOT_AUTO_BLOCKER"})

    return {
        "status": "SOURCE_PREFLIGHT_ONLY_NO_CANONICAL_FACT_LOCK_NO_CANDIDATE_ACCEPTANCE",
        "source_captures": len(records),
        "used_sources": len(used_sources),
        "planned_fact_slots": len(plan["planned_facts"]),
        "cell_counts": dict(sorted((cell, len(facts)) for cell, facts in cells.items())),
        "planned_target_s": dict(sorted(Counter(f["slot"].split("-")[1]
                                                for f in plan["planned_facts"]).items())),
        "metadata_source_records": len(metadata["documents"]),
        "transitive_source_overlap_components": len(components),
        "source_overlap_component_members": sorted(components.values(), key=lambda row: row[0]),
        "cells_with_transitive_source_overlap": overlap_cells,
        "failures": failures,
        "source_identity_preflight_pass": not failures,
        "per_fact_anchor_validation_done": anchor_plan is not None,
        "s3_ablation_validation_done": False,
        "candidate_count": 0,
        "reviewer_release_allowed": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--anchor-plan", type=Path)
    parser.add_argument("--captures", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    plan = json.loads(args.plan.read_bytes())
    metadata = json.loads(args.metadata.read_bytes())
    anchors = json.loads(args.anchor_plan.read_bytes()) if args.anchor_plan else None
    result = inspect(plan, metadata, args.captures, anchors)
    result["plan_sha256"] = _sha(args.plan.read_bytes())
    result["metadata_sha256"] = _sha(args.metadata.read_bytes())
    result["anchor_plan_sha256"] = _sha(args.anchor_plan.read_bytes()) if args.anchor_plan else None
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps({k: result[k] for k in ("source_captures", "used_sources",
                                                "planned_fact_slots", "failures")},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
