"""Pinned D1 V2 source audit and mutually exclusive WORLD DESIGNS; zero API."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

from llmguard.domains.retrieval.hidden_poisoning.chinese5060.d1_access import D1_BINDINGS, D1Reader
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.p1_preparation import (
    audit_proposal, design_world, verify_source_texts,
)
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.snapshots import digest


def write(path: Path, value: Any) -> None:
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()
    if not re.fullmatch(r"W1-5060-P1-[A-Z0-9-]+", args.run_id):
        raise ValueError("INVALID_RUN_ID")
    output = Path("experiments/paper1_chinese5060") / args.run_id
    output.mkdir(parents=True, exist_ok=False)
    reader = D1Reader(args.workspace)
    queries = json.loads(reader.read("queries_v2"))["items"]
    proposals = json.loads(reader.read("answer_proposals_v2"))["items"]
    sources = json.loads(reader.read("sources"))["sources"]
    mapping = json.loads(reader.read("query_mapping"))
    versions = json.loads(reader.read("question_versions"))
    selection = json.loads(reader.read("selection"))
    bundle = json.loads(reader.read("bundle_manifest"))
    f5 = [json.loads(line) for line in reader.read("f5").splitlines()]
    verify_source_texts(sources)
    if selection["selection_uses_model_outcomes"] or selection["seed"] != 20261104:
        raise ValueError("PRIOR_PILOT_SELECTION_REQUIRED")
    selected_rows = selection["selected_candidates_evaluator_only"]
    selected_ids = {r["candidate_id"] for r in selected_rows}
    if len(selected_ids) != 36 or {r["group_evaluation_only"] for r in selected_rows} != set(selection["selected_groups_evaluator_only"]):
        raise ValueError("PILOT_IDENTITY_DRIFT")
    if {m["group_evaluator_only"] for m in mapping} != set(selection["selected_groups_evaluator_only"]):
        raise ValueError("QUERY_GROUP_COVERAGE_MISMATCH")
    if len(queries) != 12 or len(proposals) != 12 or len(mapping) != 12:
        raise ValueError("EXACT_PILOT12_REQUIRED")
    qlookup = {q["query_id"]: q for q in queries}
    source_lookup = {s["source_id"]: s for s in sources}
    mlookup = {m["review_id"]: m for m in mapping}
    by_candidate = {r["candidate_id"]: r for r in f5}
    selected_lookup = {r["candidate_id"]: r for r in selected_rows}
    matrix = []
    world_index = []
    evaluator_bindings = []
    public_cases = []
    if len(qlookup) != 12 or {p["query_id"] for p in proposals} != set(qlookup):
        raise ValueError("QUERY_ID_PAIRING_DRIFT")
    for number, proposal in enumerate(proposals, 1):
        query = qlookup[proposal["query_id"]]
        row = audit_proposal(query, proposal, source_lookup)
        control = mlookup[proposal["review_id"]]
        siblings = control["candidate_ids_evaluator_only"]
        if len(siblings) != 3 or not set(siblings) <= selected_ids:
            raise ValueError("WORLD_MEMBERSHIP_MISMATCH")
        old_coverage = []
        for cid in siblings:
            if selected_lookup[cid]["group_evaluation_only"] != control["group_evaluator_only"]:
                raise ValueError("CROSS_GROUP_CONTAMINATION")
            world = design_world(query, candidate_id=cid, candidate_text=by_candidate[cid]["candidate_text"],
                                 all_sibling_ids=siblings, sources=sources)
            write(output / (world["world_id"] + ".json"), world)
            world_index.append({"world_id": world["world_id"], "query_id": query["query_id"],
                                "corpus_hash": world["corpus_hash"], "documents": len(world["documents"]),
                                "candidate_documents": 1, "index_status": "NOT_BUILT"})
            evaluator_bindings.append({"world_id": world["world_id"], "candidate_id": cid,
                "group_evaluation_only": control["group_evaluator_only"],
                "role_evaluation_only": selected_lookup[cid]["role_evaluation_only"]})
            old_sources = set(control["world_source_document_ids_evaluator_only"][cid])
            old_coverage.append(set(row["required_source_ids_evaluator_only"]) <= old_sources)
        row["old_world_required_source_presence"] = old_coverage
        row["case_index"] = number
        matrix.append(row)
        public_cases.append({"case_index": number, "query_sha256": row["query_sha256"],
            "fact_fields": len(proposal["facts"]), "citation_count": row["citation_count"],
            "invalid_spans": row["invalid_citation_spans"],
            "required_sources": len(row["required_source_ids_evaluator_only"]),
            "source_publication_metadata_missing": row["publication_metadata_missing"],
            "source_effective_start_metadata_missing": row["effective_start_metadata_missing"],
            "old_worlds_with_required_sources_present": sum(old_coverage),
            "source_text_and_span_status": row["source_text_and_span_status"],
            "evaluation_freeze_status": row["evaluation_freeze_status"],
            "new_worlds": 3, "new_world_backgrounds": len(sources),
            "new_TopK_sufficiency": "UNKNOWN_NOT_RETRIEVED", "human_gold": False})
    if {b["candidate_id"] for b in evaluator_bindings} != selected_ids:
        raise ValueError("WORLD_SET_DRIFT")
    write(output / "QUERY_AUDIT_MATRIX_EVALUATOR_ONLY.json", matrix)
    write(output / "WORLD_BINDINGS_EVALUATOR_ONLY.json", evaluator_bindings)
    write(output / "WORLD_DESIGN_INDEX_PRIVATE.json", world_index)
    write(output / "ACCESS_RECEIPTS.json", reader.events)
    config = Path("docs/paper1/dual_machine/chinese5060/p1/P1_PROTOCOL_CANDIDATE.json")
    summary = {
        "run_id": args.run_id, "classification": "PREPARATION_NO_RETRIEVAL_OR_MODEL_EXPERIMENT",
        "source_sha": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "protocol_sha256": hashlib.sha256(config.read_bytes()).hexdigest(),
        "input_pins": {k: b.sha256 for k, b in D1_BINDINGS.items()},
        "queries": len(queries), "facts": sum(len(p["facts"]) for p in proposals),
        "citations": sum(r["citation_count"] for r in matrix), "invalid_citation_spans": sum(r["invalid_citation_spans"] for r in matrix),
        "source_text_hashes_verified": len(sources), "question_version_changes_preserved": len(versions),
        "prior_selection_unchanged": True, "sampling_rerun": False,
        "pilot_families": len({r["family_evaluation_only"] for r in selected_rows}),
        "pilot_poison_S": dict(Counter(r["derived_s_evaluation_only"] for r in selected_rows if r["role_evaluation_only"] == "POISON")),
        "world_designs": len(world_index), "world_design_index_hash": digest(world_index),
        "world_roles_evaluator_only": dict(Counter(b["role_evaluation_only"] for b in evaluator_bindings)),
        "documents_per_world": 1 + len(sources), "backgrounds_identical_across_worlds": True,
        "old_worlds_missing_at_least_one_cited_source": sum(3 - r["old_worlds_with_required_sources_present"] for r in public_cases),
        "HOLD_candidates_excluded": bundle["holds_candidates"],
        "new_indices_built": 0, "TopK_snapshots_created": 0, "human_gold": 0,
        "cases_needing_evaluation_adjudication": 12,
        "T1_trust_root": "NOT_VERIFIED_SOURCE_BUNDLE_NOT_AUTOMATIC_AUTHORITY",
        "paid_calls": 0, "paid_cost_CNY": "0", "B5_B6": "NOT_IMPLEMENTED", "D1_40": "NOT_RUN",
        "cases": public_cases,
    }
    write(output / "SUMMARY_PUBLIC.json", summary)
    evidence_index = [{"path": p.name, "bytes": p.stat().st_size,
                       "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
                      for p in sorted(output.iterdir()) if p.is_file()]
    write(output / "PRIVATE_EVIDENCE_INDEX.json", evidence_index)
    print(json.dumps({"run_id": args.run_id, "queries": 12, "world_designs": len(world_index),
                      "invalid_spans": summary["invalid_citation_spans"], "paid_calls": 0}))


if __name__ == "__main__":
    main()
