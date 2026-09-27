"""HKP3 preblind mechanical gate; no external acceptance or label feedback."""

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
    parser.add_argument("--evidence-identity-audit", type=Path, required=True)
    parser.add_argument("--construction-qa", type=Path, required=True)
    parser.add_argument("--derived-1988-text", type=Path, required=True)
    parser.add_argument("--derived-1988-provenance", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"Refusing to overwrite: {args.output}")
    evidence = load(args.evidence_identity_audit)
    atoms = load(args.construction_qa)
    contract = load(args.precontract)
    provenance = load(args.derived_1988_provenance)
    rows = [
        json.loads(line)
        for line in args.candidate_draft.read_text(encoding="utf-8").splitlines()
    ]
    errors: list[str] = []
    if evidence["status"] != "PRECONSTRUCTION_EVIDENCE_IDENTITY_GATE_PASS":
        errors.append("evidence identity gate failed")
    if atoms["status"] != "CONSTRUCTION_SIDE_QA_PASS_NOT_BLIND_REVIEW":
        errors.append("construction-side atom gate failed")
    if atoms["candidate_draft_sha256"] != sha(args.candidate_draft):
        errors.append("candidate/atom audit hash mismatch")
    if provenance["source_raw_sha256"] != evidence["sources"]["ML1988_HUBEI_GAZETTE"]["sha256"]:
        errors.append("1988 derived excerpt not linked to raw official PDF")
    excerpt = args.derived_1988_text.read_text(encoding="utf-8")
    if "第八条" not in excerpt or "九十天" not in excerpt:
        errors.append("derived 1988 general maternity clause absent")
    groups = {g["group_slot_id"]: g for g in contract["groups"]}
    by_group: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_group[row["group_slot_id"]].append(row)
    if len(rows) != 30 or set(by_group) != set(groups):
        errors.append("population parity not 30 rows/10 groups")
    source_audit = evidence["sources"]
    documents: dict[str, Counter[str]] = {}
    extraction: dict[str, dict[str, Any]] = {}
    for doc_id, source in source_audit.items():
        if doc_id == "ML1988_HUBEI_GAZETTE":
            content = excerpt
            extraction_status = "VISUALLY_CHECKED_DERIVED_ARTICLE8_NOT_RAW_OCR"
        else:
            content = _source_text(Path(source["path"]))
            extraction_status = "RAW_SNAPSHOT_TEXT_EXTRACTION"
        documents[doc_id] = _grams(content)
        extraction[doc_id] = {
            "characters": len(content),
            "status": extraction_status,
            "snapshot_sha256": source["sha256"],
        }
        if len(content) < 40:
            errors.append(f"source text too short for smoke: {doc_id}")
    df = Counter(term for doc in documents.values() for term in doc)
    avg_length = sum(sum(doc.values()) for doc in documents.values()) / len(documents)
    retrieval = []
    view = []
    surfaces = []
    attention: list[str] = []
    for group_id, members in sorted(by_group.items()):
        group = groups[group_id]
        if len(members) != 3 or len({m["neutral_query"] for m in members}) != 1:
            errors.append(f"triplet query/role defect: {group_id}")
            continue
        query = members[0]["neutral_query"]
        if re.search(r"(?i)poison|clean|hard.?negative|hkp|s[123]|正确答案|错误答案", query):
            errors.append(f"neutral query label leak: {group_id}")
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
        by_role = {
            member["role"]: _surface_features(member["candidate_text"])
            for member in members
        }
        surfaces.append({"group_slot_id": group_id, "by_role": by_role})
        lengths = [item["characters"] for item in by_role.values()]
        if max(lengths) / min(lengths) > 1.35:
            errors.append(f"length shortcut: {group_id}")
        for feature in ("law_titles", "year_expressions"):
            values = [item[feature] for item in by_role.values()]
            if max(values) - min(values) > 1:
                errors.append(f"{feature} shortcut: {group_id}")
        numeric = [item["number_expressions"] for item in by_role.values()]
        if max(numeric) - min(numeric) >= 4:
            attention.append(f"NUMERIC_SURFACE_REVIEW:{group_id}")
        for member in members:
            if not group["version_path"] or not group["evidence_refs"]:
                errors.append(f"temporal version path absent: {group_id}")
            if member["evidence_refs"] != group["evidence_refs"]:
                errors.append(f"source lineage differs: {member['sample_id']}")
            view.append(
                {
                    "sample_id": member["sample_id"],
                    "group_slot_id": group_id,
                    "role": member["role"],
                    "S": "OBSERVED",
                    "E": "OBSERVED",
                    "P": "NOT_APPLICABLE_NO_ISSUER_OR_PUBLISHER_CLAIM",
                    "T": "OBSERVED_VERSION_PATH",
                    "R": "NEUTRAL_QUERY_AND_TRUSTED_CORPUS_OBSERVED",
                    "input_missing": 0,
                    "evidence_insufficient": 0,
                }
            )
        expected_need = {"S1": 2, "S2": 1, "S3": 2}[group["target_s"]]
        if len(group["evidence_refs"]) < expected_need:
            errors.append(f"precommitted evidence path incomplete: {group_id}")
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
        "status": "HKP3_INTERNAL_MECHANICAL_QA_PASS_EXTERNAL_REVIEW_NOT_DONE"
        if not errors
        else "HKP3_INTERNAL_MECHANICAL_QA_BLOCKED",
        "candidate_draft_sha256": sha(args.candidate_draft),
        "evidence_identity_audit_sha256": sha(args.evidence_identity_audit),
        "construction_qa_sha256": sha(args.construction_qa),
        "derived_1988_excerpt_sha256": sha(args.derived_1988_text),
        "group_count": len(by_group),
        "candidate_count": len(rows),
        "source_count": len(documents),
        "source_text_extraction": extraction,
        "retrieval_smoke": retrieval,
        "view_readiness": view,
        "missingness_by_role": missingness,
        "triplet_surface_parity": surfaces,
        "surface_attention_nonblocking": attention,
        "boundary": "No blind package; no Expected, GT, split, or model execution",
        "errors": errors,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(result["status"], len(rows), len(documents), len(errors), attention)
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
