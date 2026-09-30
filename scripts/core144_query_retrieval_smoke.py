"""Engineering-only label-blind smoke on frozen official source text."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from llmguard.domains.retrieval.hidden_poisoning.method_engineering.retrieval_harness import (
    CharacterNgramBM25,
    RetrievalDocument,
)

from core144_normalized_source_atoms import load_sources


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def save(path: Path, value: Any) -> None:
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queries", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--captures", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    queries = json.loads(args.queries.read_bytes())["queries"]
    if len(queries) != 48 or any(set(q) != {"query_id", "query_text"} for q in queries):
        raise ValueError("Retriever-visible query schema or count invalid")
    sources = load_sources(args.captures)
    metadata = json.loads(args.metadata.read_bytes())["documents"]
    documents = [RetrievalDocument(doc_id=d["evidence_doc_id"],
                 candidate_text=sources[d["evidence_doc_id"]]["text"],
                 source_title=d["title"], primary_subject="") for d in metadata]
    retriever = CharacterNgramBM25(documents, k1=1.2, b=0.75, ngram_sizes=(2, 3))
    manifest = [{"evidence_doc_id": d.doc_id,
                 "snapshot_sha256": sources[d.doc_id]["raw_sha256"],
                 "text_sha256": sources[d.doc_id]["text_sha256"]} for d in documents]
    save(args.output / "trusted_corpus_membership.json", manifest)
    save(args.output / "run_input_lock.json", {
        "locked_utc": datetime.now(timezone.utc).isoformat(),
        "query_sha256": sha(args.queries.read_bytes()),
        "corpus_sha256": sha((args.output / "trusted_corpus_membership.json").read_bytes()),
        "config": retriever.configuration(), "k": 5,
        "query_or_ranking_reads_labels": False, "no_training_or_tuning": True})
    rows = []
    for q in queries:
        scores = retriever.score(q["query_text"])
        if scores != retriever.score(q["query_text"]):
            raise ValueError("Determinism parity failed")
        order = sorted(range(len(documents)), key=lambda i: (-scores[i], documents[i].doc_id))
        for rank, i in enumerate(order[:5], 1):
            rows.append({"query_id": q["query_id"], "query": q["query_text"],
                         "evidence_doc_id": documents[i].doc_id,
                         "rank": rank, "raw_score": scores[i],
                         "retriever_id": retriever.retriever_id})
    save(args.output / "top5_trace.json", rows)
    save(args.output / "report.json", {"queries": len(queries), "traces": len(rows),
         "deterministic": True, "top5_trace_sha256": sha((args.output / "top5_trace.json").read_bytes()),
         "input_lock_sha256": sha((args.output / "run_input_lock.json").read_bytes()),
         "status": "PASS_ENGINEERING_IO_ONLY", "quality_selection_performed": False,
         "formal_retrieval_result_claimed": False})
    print(json.dumps({"queries": len(queries), "traces": len(rows), "documents": len(documents)}))


if __name__ == "__main__":
    main()
