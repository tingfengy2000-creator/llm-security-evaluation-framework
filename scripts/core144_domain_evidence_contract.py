"""Lock source-bound Core144 facts before candidate construction (no GT input)."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalize(value: str) -> str:
    return re.sub(r"[\s,，]", "", value)


def save_new(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write((json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", type=Path, required=True)
    parser.add_argument("--captures", type=Path, required=True)
    parser.add_argument("--support-book", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError("Additive evidence contract output already exists")
    spec_bytes = args.spec.read_bytes()
    spec = json.loads(spec_bytes)
    sources: dict[str, Any] = {}
    for registry in sorted(args.captures.glob("source_capture_v*/snapshot_registry.json")):
        for row in json.loads(registry.read_bytes())["records"]:
            if row["capture_status"] != "CAPTURED_IDENTITY_ANCHORS_PRESENT":
                continue
            doc_id = row["evidence_doc_id"]
            raw = registry.parent / "raw" / f"{doc_id}.bin"
            text_path = registry.parent / "text" / f"{doc_id}.txt"
            if digest(raw.read_bytes()) != row["raw_sha256"]:
                raise ValueError(f"Raw parity failed: {doc_id}")
            text_bytes = text_path.read_bytes()
            if digest(text_bytes) != row["text_sha256"]:
                raise ValueError(f"Text parity failed: {doc_id}")
            sources[doc_id] = {**row, "capture_namespace": registry.parent.as_posix(),
                               "snapshot_text": text_bytes.decode("utf-8")}
    facts = []
    support: dict[str, Any] = {}
    if args.support_book:
        for item in json.loads(args.support_book.read_bytes())["sources"]:
            source = sources[item["doc"]]
            if not all(normalize(a) in normalize(source["snapshot_text"])
                       for a in item["anchors"]):
                raise ValueError(f"Supporting fact provenance absent: {item['doc']}")
            support[item["doc"]] = item
    for item in spec["facts"]:
        evidence = []
        for requirement in item["evidence"]:
            source = sources[requirement["doc"]]
            if not all(normalize(anchor) in normalize(source["snapshot_text"])
                       for anchor in requirement["anchors"]):
                raise ValueError(f"Evidence anchor absent: {item['fact_id']} / {requirement}")
            evidence.append({**requirement, "snapshot_sha256": source["raw_sha256"],
                             "text_sha256": source["text_sha256"],
                             "snapshot_locked_utc": source["locked_utc"],
                             "source_bound_supporting_facts": support.get(requirement["doc"])})
        facts.append({**item, "evidence": evidence,
                      "canonical_fact_created_utc": datetime.now(timezone.utc).isoformat()})
    ids = [item["fact_id"] for item in facts]
    if len(ids) != 48 or len(set(ids)) != 48:
        raise ValueError("Domain requires exactly 48 independent assigned fact cores")
    used = {e["doc"] for item in facts for e in item["evidence"]}
    metadata = []
    for doc_id in sorted(used):
        source = sources[doc_id]
        declared = spec["document_metadata"][doc_id]
        for anchor in declared["metadata_anchors"]:
            if normalize(anchor) not in normalize(source["snapshot_text"]):
                raise ValueError(f"Metadata provenance absent: {doc_id}: {anchor}")
        metadata.append({**declared, "evidence_doc_id": doc_id,
                         "source_host": source["source_host"],
                         "official_url": source["official_url"],
                         "snapshot_sha256": source["raw_sha256"],
                         "text_sha256": source["text_sha256"],
                         "capture_namespace": source["capture_namespace"],
                         "metadata_status": "SOURCE_BOUND_CONSTRUCTION_RECORD_NOT_GT"})
    save_new(args.output / "canonical_fact_records.json", {
        "domain": spec["domain"], "spec_sha256": digest(spec_bytes), "facts": facts,
        "status": "SOURCE_BOUND_FACTS_LOCKED_BEFORE_CANDIDATES_NOT_INDEPENDENT_REVIEW"})
    save_new(args.output / "evidence_metadata.json", {"documents": metadata,
        "unobserved_policy": "NULL_PLUS_NOT_OBSERVED_WITH_FROZEN_EVIDENCE"})
    save_new(args.output / "evidence_contract_lock.json", {
        "domain": spec["domain"], "fact_count": len(facts), "document_count": len(used),
        "facts_sha256": digest((args.output / "canonical_fact_records.json").read_bytes()),
        "metadata_sha256": digest((args.output / "evidence_metadata.json").read_bytes()),
        "locked_utc": datetime.now(timezone.utc).isoformat(), "candidate_count": 0,
        "no_expected_gt_human_model_input": True})
    print(json.dumps({"facts": len(facts), "documents": len(used), "candidates": 0}))


if __name__ == "__main__":
    main()
