"""Build a D3 canonical-fact input from source-first, overlap-audited inputs."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def write_new(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(obj, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--anchors", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--preflight", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError("Refusing to overwrite fact spec")
    plan = json.loads(args.plan.read_bytes())
    anchors = json.loads(args.anchors.read_bytes())
    metadata = json.loads(args.metadata.read_bytes())
    preflight = json.loads(args.preflight.read_bytes())
    if (not preflight["source_identity_preflight_pass"]
            or not preflight["per_fact_anchor_validation_done"]
            or preflight["cells_with_transitive_source_overlap"]
            or preflight["plan_sha256"] != hashlib.sha256(args.plan.read_bytes()).hexdigest()
            or preflight["metadata_sha256"] != hashlib.sha256(args.metadata.read_bytes()).hexdigest()
            or preflight["anchor_plan_sha256"] != hashlib.sha256(args.anchors.read_bytes()).hexdigest()):
        raise ValueError("Source-bound preflight failed or input parity changed")
    component_for = {}
    for members in preflight["source_overlap_component_members"]:
        cluster_id = "D3-EC-" + hashlib.sha256("|".join(members).encode()).hexdigest()[:10]
        component_for.update({doc_id: cluster_id for doc_id in members})
    documents = {}
    for doc_id, row in metadata["documents"].items():
        documents[doc_id] = {
            "title": row["title"], "family": row["family"],
            "page_publisher": None, "original_issuer": row["issuer"],
            "adoption_authority": row["adopter"], "revision_authority": None,
            "publication_date": None, "effective_start": row["effective_start"],
            "effective_end": None, "version_identity": row["version_role"],
            "role": row["version_role"],
            "repost_relation": "OFFICIAL_HOST_PAGE_PUBLISHER_NOT_INFERRED_FROM_HOST",
            "metadata_anchors": row["metadata_anchors"],
            "unknown_metadata_policy": metadata["unknown_metadata_policy"],
            "effective_end_status": "NOT_OBSERVED_NO_OPEN_ENDED_INTERVAL_CLAIM",
        }
    facts = []
    for row in plan["planned_facts"]:
        slot = row["slot"]
        docs = row["evidence_docs"]
        per_doc = anchors["anchors_by_slot_in_evidence_doc_order"][slot]
        clusters = {component_for[doc_id] for doc_id in docs}
        if len(clusters) != 1:
            raise ValueError(f"Comparative evidence crosses unrecorded cluster: {slot}")
        families = sorted({metadata["documents"][doc_id]["family"] for doc_id in docs})
        facts.append({
            "fact_id": slot, "family": row["family"], "core": row["core"],
            "subject": " / ".join(metadata["documents"][doc_id]["title"] for doc_id in docs),
            "canonical_fact": row["fact"],
            "evidence": [{"doc": doc_id, "anchors": anchor_list}
                         for doc_id, anchor_list in zip(docs, per_doc, strict=True)],
            "family_cluster_id": next(iter(clusters)),
            "evidence_family_id": "D3-NORMATIVE-" + "-".join(families),
            "source_family": "OFFICIAL_DOCUMENT_ISSUANCE_FAMILY-" + "-".join(families),
            "version_family_id": "D3-" + "-".join(families),
            "primary_factual_core_id": row["core"],
            "source_first_note": "Anchors verified before Candidate text; semantic/ablation QA separate.",
        })
    if len(facts) != 48:
        raise ValueError("Frozen 48-slot population required")
    write_new(args.output, {
        "domain": "D3", "scope": "SOURCE_FIRST_CANONICAL_FACTS_NOT_GT_NOT_REVIEWER_RESULT",
        "source_plan_sha256": preflight["plan_sha256"],
        "source_preflight_sha256": hashlib.sha256(args.preflight.read_bytes()).hexdigest(),
        "document_metadata": documents, "facts": facts,
    })
    print(json.dumps({"facts": len(facts), "metadata_docs": len(documents),
                      "conservative_clusters": len(set(component_for.values()))}))


if __name__ == "__main__":
    main()
