"""Mechanical full-page S3 cross-anchor screen, not semantic sufficiency.

Only the already frozen official snapshot corpus is inspected. A hit is a
reason for manual review; a miss is not proof that a document lacks the fact.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from core144_normalized_source_atoms import load_sources


def normalized(value: str) -> str:
    return re.sub(r"[\s,，]", "", value)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--anchors", type=Path, required=True)
    parser.add_argument("--captures", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError("Refusing to overwrite ablation screen")
    plan = json.loads(args.plan.read_bytes())
    anchors = json.loads(args.anchors.read_bytes())["anchors_by_slot_in_evidence_doc_order"]
    sources = load_sources(args.captures)
    rows = []
    for fact in plan["planned_facts"]:
        if "-S3-" not in fact["slot"]:
            continue
        docs = fact["evidence_docs"]
        if len(docs) != 2:
            raise ValueError(f"S3 does not have two frozen units: {fact['slot']}")
        endpoint_anchors = anchors[fact["slot"]]
        if len(endpoint_anchors) != 2:
            raise ValueError(f"S3 anchors missing: {fact['slot']}")
        full_pages = []
        for doc_id, source in sorted(sources.items()):
            page = normalized(source["text"])
            endpoint_hits = [all(normalized(anchor) in page for anchor in items)
                             for items in endpoint_anchors]
            if any(endpoint_hits):
                full_pages.append({"doc": doc_id, "endpoint_anchor_hits": endpoint_hits,
                                   "contains_both_anchor_sets": all(endpoint_hits)})
        rows.append({"fact_id": fact["slot"], "frozen_evidence_docs": docs,
                     "endpoint_anchors": endpoint_anchors,
                     "source_corpus_pages_with_endpoint_hits": full_pages,
                     "single_page_with_both_anchor_sets": [p["doc"] for p in full_pages
                                                           if p["contains_both_anchor_sets"]],
                     "semantic_necessity_review_required": True})
    result = {"domain": "D3", "s3_groups": len(rows), "captured_official_pages": len(sources),
              "rows": rows, "all_units_are_complete_frozen_pages": True,
              "mechanical_anchor_screen_is_not_semantic_ablation": True,
              "candidate_or_label_used": False}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps({"s3_groups": len(rows), "single_page_joint_anchor_flags":
                      {r["fact_id"]: r["single_page_with_both_anchor_sets"] for r in rows
                       if r["single_page_with_both_anchor_sets"]}}, ensure_ascii=False))


if __name__ == "__main__":
    main()
