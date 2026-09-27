"""HKP4 authority-input and neutral-retrieval smoke before any blind release."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from formal240_d1_hkp2_internal_gate import _bm25, _grams, _source_text, _surface_features


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-draft", type=Path, required=True)
    parser.add_argument("--precontract", type=Path, required=True)
    parser.add_argument("--authority-evidence-audit", type=Path, required=True)
    parser.add_argument("--construction-qa", type=Path, required=True)
    parser.add_argument("--authority-metadata", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"Refusing to overwrite: {args.output}")
    evidence = load(args.authority_evidence_audit)
    atoms = load(args.construction_qa)
    contract = load(args.precontract)
    metadata = load(args.authority_metadata)
    rows = [
        json.loads(line)
        for line in args.candidate_draft.read_text(encoding="utf-8").splitlines()
    ]
    errors: list[str] = []
    if evidence["status"] != "PRECONSTRUCTION_AUTHORITY_EVIDENCE_GATE_PASS":
        errors.append("authority evidence gate failed")
    if atoms["status"] != "CONSTRUCTION_SIDE_QA_PASS_NOT_BLIND_REVIEW":
        errors.append("construction atom gate failed")
    if atoms["candidate_draft_sha256"] != sha(args.candidate_draft):
        errors.append("candidate/atom hash mismatch")
    groups = {g["group_slot_id"]: g for g in contract["groups"]}
    by_group: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_group[row["group_slot_id"]].append(row)
    if len(rows) != 30 or set(by_group) != set(groups):
        errors.append("30-row/10-group population parity failed")
    source_audit = evidence["sources"]
    metadata_by_id = {row["evidence_doc_id"]: row for row in metadata["documents"]}
    if set(metadata_by_id) != set(source_audit):
        errors.append("authority metadata/source identity parity failed")
    for doc_id, record in metadata_by_id.items():
        if not record["original_issuer"] or not record["authority_basis"]:
            errors.append(f"issuer provenance missing: {doc_id}")
    documents: dict[str, Counter[str]] = {}
    extraction: dict[str, dict[str, Any]] = {}
    for doc_id, source in source_audit.items():
        content = _source_text(Path(source["path"]))
        documents[doc_id] = _grams(content)
        extraction[doc_id] = {
            "characters": len(content),
            "snapshot_sha256": source["sha256"],
            "status": "RAW_OFFICIAL_SNAPSHOT_TEXT_EXTRACTION",
        }
        if len(content) < 40:
            errors.append(f"non-searchable source text: {doc_id}")
    df = Counter(term for doc in documents.values() for term in doc)
    avg_length = sum(sum(doc.values()) for doc in documents.values()) / len(documents)
    retrieval = []
    view = []
    surfaces = []
    attention: list[str] = []
    for group_id, members in sorted(by_group.items()):
        group = groups[group_id]
        if len(members) != 3 or len({m["neutral_query"] for m in members}) != 1:
            errors.append(f"triplet/query defect: {group_id}")
            continue
        query = members[0]["neutral_query"]
        if re.search(r"(?i)poison|clean|hard.?negative|hkp|s[123]|正确答案|错误答案", query):
            errors.append(f"label leak in neutral query: {group_id}")
        ranked = sorted(
            (
                (doc_id, _bm25(_grams(query), doc, df, len(documents), avg_length))
                for doc_id, doc in documents.items()
            ),
            key=lambda item: (-item[1], item[0]),
        )
        retrieval.append(
            {
                "group_slot_id": group_id,
                "query": query,
                "retriever": "CHINESE_CHARACTER_BIGRAM_BM25_K1_1.2_B_0.75_ENGINEERING_SMOKE",
                "corpus_document_count": len(documents),
                "top5": [
                    {
                        "rank": rank,
                        "evidence_doc_id": doc_id,
                        "score": round(score, 8),
                        "snapshot_sha256": source_audit[doc_id]["sha256"],
                    }
                    for rank, (doc_id, score) in enumerate(ranked[:5], start=1)
                ],
            }
        )
        if len(ranked) < 5 or ranked[0][1] <= 0:
            errors.append(f"retrieval smoke failed: {group_id}")
        triplet_surface = {
            member["role"]: _surface_features(member["candidate_text"])
            for member in members
        }
        surfaces.append({"group_slot_id": group_id, "by_role": triplet_surface})
        lengths = [item["characters"] for item in triplet_surface.values()]
        if max(lengths) / min(lengths) > 1.35:
            errors.append(f"length shortcut: {group_id}")
        for feature in ("law_titles", "year_expressions"):
            values = [item[feature] for item in triplet_surface.values()]
            if max(values) - min(values) > 1:
                errors.append(f"{feature} shortcut: {group_id}")
        numbers = [item["number_expressions"] for item in triplet_surface.values()]
        if max(numbers) - min(numbers) >= 4:
            attention.append(f"NUMERIC_SURFACE_REVIEW:{group_id}")
        if not group["original_issuer"] or not group["host_role"]:
            errors.append(f"issuer/host metadata absent: {group_id}")
        publisher_unknown = any(
            metadata_by_id[ref]["page_publisher"]
            == "NOT_OBSERVED_WITH_FROZEN_EVIDENCE"
            for ref in group["evidence_refs"]
        )
        for member in members:
            if member["evidence_refs"] != group["evidence_refs"]:
                errors.append(f"evidence lineage mismatch: {member['sample_id']}")
            view.append(
                {
                    "sample_id": member["sample_id"],
                    "group_slot_id": group_id,
                    "role": member["role"],
                    "S": "OBSERVED",
                    "E": "OBSERVED",
                    "P": "PARTIAL_ISSUER_AND_HOST_OBSERVED_PUBLISHER_UNKNOWN"
                    if publisher_unknown
                    else "OBSERVED_ISSUER_HOST_AND_PUBLISHER_ROLE",
                    "T": "NOT_APPLICABLE_NO_CANDIDATE_VERSION_CLAIM",
                    "R": "NEUTRAL_QUERY_AND_TRUSTED_CORPUS_OBSERVED",
                    "input_missing": 1 if publisher_unknown else 0,
                    "evidence_insufficient": 0,
                }
            )
    missingness = {
        role: {
            key: dict(Counter(row[key] for row in view if row["role"] == role))
            for key in ("S", "E", "P", "T", "R", "input_missing", "evidence_insufficient")
        }
        for role in ("CLEAN_CURRENT", "POISON", "HARD_NEGATIVE")
    }
    if len({json.dumps(value, sort_keys=True) for value in missingness.values()}) != 1:
        errors.append("view-input missingness differs by role")
    result = {
        "status": "HKP4_INTERNAL_MECHANICAL_QA_PASS_EXTERNAL_REVIEW_NOT_DONE"
        if not errors
        else "HKP4_INTERNAL_MECHANICAL_QA_BLOCKED",
        "candidate_draft_sha256": sha(args.candidate_draft),
        "authority_evidence_audit_sha256": sha(args.authority_evidence_audit),
        "construction_qa_sha256": sha(args.construction_qa),
        "authority_metadata_sha256": sha(args.authority_metadata),
        "group_count": len(by_group),
        "candidate_count": len(rows),
        "source_count": len(documents),
        "source_text_extraction": extraction,
        "retrieval_smoke": retrieval,
        "view_readiness": view,
        "missingness_by_role": missingness,
        "triplet_surface_parity": surfaces,
        "surface_attention_nonblocking": attention,
        "authority_limitation": "Host/page publisher/original issuer are separate. Jilin official repost page-publisher identity is unknown; its P input missingness is explicit and class-symmetric.",
        "boundary": "No blind package; no Expected, GT, split or model execution",
        "errors": errors,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(result["status"], len(rows), len(documents), len(errors), attention)
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
