"""HKP2 preblind mechanical gate, excluding external reviewer acceptance.

Uses only frozen official snapshots and group-neutral queries for retrieval
smoke. Never loads expected labels, GT, or model performance feedback.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source_text(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        import pypdf

        return " ".join(
            page.extract_text() or "" for page in pypdf.PdfReader(path).pages
        )
    raw = path.read_text(encoding="utf-8", errors="replace")
    return html.unescape(re.sub(r"<[^>]+>", " ", raw))


def _grams(value: str) -> Counter[str]:
    value = re.sub(r"\s+", "", value)
    return Counter(value[i : i + 2] for i in range(max(0, len(value) - 1)))


def _bm25(
    query: Counter[str],
    document: Counter[str],
    df: Counter[str],
    n_docs: int,
    average_length: float,
) -> float:
    length = sum(document.values())
    score = 0.0
    for term in query:
        frequency = document.get(term, 0)
        if not frequency:
            continue
        inverse_document_frequency = math.log(
            1 + (n_docs - df[term] + 0.5) / (df[term] + 0.5)
        )
        score += (
            inverse_document_frequency
            * frequency
            * 2.2
            / (frequency + 1.2 * (0.25 + 0.75 * length / average_length))
        )
    return score


def _surface_features(text: str) -> dict[str, int]:
    return {
        "characters": len(text),
        "rough_tokens": len(re.findall(r"[\u4e00-\u9fff]|[A-Za-z]+|\d+", text)),
        "sentences": len(re.findall(r"[。！？]", text)),
        "punctuation": len(re.findall(r"[，。；：、！？（）()]", text)),
        "number_expressions": len(
            re.findall(r"\d+|[一二三四五六七八九十百千]+", text)
        ),
        "year_expressions": len(re.findall(r"(?:19|20)\d{2}", text)),
        "institution_mentions": len(
            re.findall(r"国务院|人力资源社会保障部|用工单位|职工代表大会|工会", text)
        ),
        "law_titles": text.count("《"),
        "version_cues": len(re.findall(r"原版|修订版|现行版|历史版|发布文本|年文本", text)),
        "semicolon": text.count("；"),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-draft", type=Path, required=True)
    parser.add_argument("--precontract", type=Path, required=True)
    parser.add_argument("--scope-overlay", type=Path, required=True)
    parser.add_argument("--temporal-overlay", type=Path, required=True)
    parser.add_argument("--derived-1988-text", type=Path, required=True)
    parser.add_argument("--derived-1988-provenance", type=Path, required=True)
    parser.add_argument("--evidence-identity-audit", type=Path, required=True)
    parser.add_argument("--construction-qa", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"Refusing to overwrite: {args.output}")
    evidence_audit = _json(args.evidence_identity_audit)
    construction_qa = _json(args.construction_qa)
    precontract = _json(args.precontract)
    scope_overlay = _json(args.scope_overlay)
    temporal_overlay = _json(args.temporal_overlay)
    derived_provenance = _json(args.derived_1988_provenance)
    rows = [
        json.loads(line)
        for line in args.candidate_draft.read_text(encoding="utf-8").splitlines()
    ]
    errors: list[str] = []
    if evidence_audit["status"] != "PRECONSTRUCTION_EVIDENCE_IDENTITY_GATE_PASS":
        errors.append("evidence identity gate not passed")
    if construction_qa["status"] != "CONSTRUCTION_SIDE_QA_PASS_NOT_BLIND_REVIEW":
        errors.append("construction-side atom/parity QA not passed")
    if construction_qa["candidate_draft_sha256"] != _sha(args.candidate_draft):
        errors.append("candidate/atom-audit SHA mismatch")
    if construction_qa["scope_overlay_sha256"] != _sha(args.scope_overlay):
        errors.append("scope-repair overlay SHA mismatch")
    if derived_provenance["source_raw_sha256"] != evidence_audit["sources"][
        "ML1988_HUBEI_GAZETTE"
    ]["sha256"]:
        errors.append("derived 1988 text does not point to locked PDF")
    if "第八条" not in args.derived_1988_text.read_text(encoding="utf-8"):
        errors.append("derived 1988 clause locator missing")

    groups = {group["group_slot_id"]: group for group in precontract["groups"]}
    group_id = scope_overlay["group_slot_id"]
    groups[group_id]["primary_factual_core_id"] = scope_overlay[
        "new_primary_factual_core_id"
    ]
    temporal = {row["group_slot_id"]: row for row in temporal_overlay["groups"]}
    if len(temporal) != 4 or {g for g in temporal if "-S3-" not in g}:
        errors.append("S3 temporal metadata coverage is not four groups")
    for group in temporal.values():
        refs = {version["evidence_doc_id"] for version in group["versions"]}
        if refs != set(groups[group["group_slot_id"]]["evidence_refs"]):
            errors.append(f"temporal version/evidence mismatch: {group['group_slot_id']}")
        for version in group["versions"]:
            if not version["effective_start"] or not version["authority"]:
                errors.append(f"temporal metadata missing: {group['group_slot_id']}")

    by_group: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_group[row["group_slot_id"]].append(row)
    if len(rows) != 30 or len(by_group) != 10:
        errors.append("candidate population not 30/10")
    source_audit = evidence_audit["sources"]
    documents: dict[str, Counter[str]] = {}
    extraction_status: dict[str, dict[str, Any]] = {}
    for doc_id, source in source_audit.items():
        if doc_id == "ML1988_HUBEI_GAZETTE":
            content = args.derived_1988_text.read_text(encoding="utf-8")
            extraction = "VISUALLY_VERIFIED_DERIVED_ARTICLE8_NOT_RAW_OCR"
        else:
            content = _source_text(Path(source["path"]))
            extraction = "RAW_SNAPSHOT_TEXT_EXTRACTION"
        documents[doc_id] = _grams(content)
        extraction_status[doc_id] = {
            "text_length": len(content),
            "status": extraction,
            "snapshot_sha256": source["sha256"],
        }
        if len(content) < 40:
            errors.append(f"non-searchable evidence text: {doc_id}")

    docfreq = Counter(term for doc in documents.values() for term in doc)
    mean_length = sum(sum(doc.values()) for doc in documents.values()) / len(documents)
    retrieval = []
    view = []
    surfaces = []
    surface_attention: list[str] = []
    for gid, members in sorted(by_group.items()):
        group = groups[gid]
        queries = {member["neutral_query"] for member in members}
        if len(queries) != 1:
            errors.append(f"triplet query is not shared: {gid}")
            continue
        query = next(iter(queries))
        if re.search(r"(?i)poison|clean|hard.?negative|hkp|s[123]|正确答案|错误答案", query):
            errors.append(f"label leak in neutral query: {gid}")
        qgrams = _grams(query)
        ranked = sorted(
            (
                (doc_id, _bm25(qgrams, text, docfreq, len(documents), mean_length))
                for doc_id, text in documents.items()
            ),
            key=lambda item: (-item[1], item[0]),
        )
        retrieval.append(
            {
                "group_slot_id": gid,
                "neutral_query": query,
                "retriever": "CHINESE_CHARACTER_BIGRAM_BM25_K1_1.2_B_0.75_ENGINEERING_SMOKE",
                "corpus_document_count": len(documents),
                "top5": [
                    {
                        "rank": idx,
                        "evidence_doc_id": doc_id,
                        "score": round(score, 8),
                        "snapshot_sha256": source_audit[doc_id]["sha256"],
                    }
                    for idx, (doc_id, score) in enumerate(ranked[:5], start=1)
                ],
            }
        )
        if len(ranked) < 5 or ranked[0][1] <= 0:
            errors.append(f"retrieval smoke failed: {gid}")
        triplet_surface = {
            member["role"]: _surface_features(member["candidate_text"])
            for member in members
        }
        surfaces.append({"group_slot_id": gid, "by_role": triplet_surface})
        lengths = [item["characters"] for item in triplet_surface.values()]
        if max(lengths) / min(lengths) > 1.35:
            errors.append(f"character-length surface shortcut: {gid}")
        for feature in ("law_titles", "year_expressions"):
            values = [item[feature] for item in triplet_surface.values()]
            if max(values) - min(values) > 1:
                errors.append(f"{feature} role-skew: {gid}")
        nums = [item["number_expressions"] for item in triplet_surface.values()]
        if max(nums) - min(nums) >= 4:
            surface_attention.append(f"NUMERIC_SURFACE_DIFFERENCE_REVIEW:{gid}")
        for member in members:
            text = member["candidate_text"]
            if "《" not in text or "》" not in text:
                errors.append(f"candidate document identity absent: {member['sample_id']}")
            view.append(
                {
                    "sample_id": member["sample_id"],
                    "group_slot_id": gid,
                    "role": member["role"],
                    "S": "OBSERVED",
                    "E": "OBSERVED",
                    "P": "NOT_APPLICABLE_NO_ISSUER_OR_PUBLISHER_CLAIM",
                    "T": "OBSERVED" if gid in temporal else "NOT_APPLICABLE_NO_TEMPORAL_COMPARISON",
                    "R": "NEUTRAL_QUERY_AND_TRUSTED_CORPUS_OBSERVED",
                    "input_missing": 0,
                    "evidence_insufficient": 0,
                }
            )
        if group["target_s"] == "S3" and len(group["evidence_refs"]) != 2:
            errors.append(f"S3 lacks two-source path: {gid}")
        if group["target_s"] != "S3" and len(group["evidence_refs"]) != 1:
            errors.append(f"S1/S2 source path not single-source: {gid}")
    by_role = {
        role: {
            key: dict(Counter(row[key] for row in view if row["role"] == role))
            for key in ("S", "E", "P", "T", "R", "input_missing", "evidence_insufficient")
        }
        for role in ("CLEAN_CURRENT", "POISON", "HARD_NEGATIVE")
    }
    if len({json.dumps(value, sort_keys=True) for value in by_role.values()}) != 1:
        errors.append("view-input missingness differs by role")
    result = {
        "status": "HKP2_INTERNAL_MECHANICAL_QA_PASS_EXTERNAL_REVIEW_NOT_DONE"
        if not errors
        else "HKP2_INTERNAL_MECHANICAL_QA_BLOCKED",
        "candidate_draft_sha256": _sha(args.candidate_draft),
        "evidence_identity_audit_sha256": _sha(args.evidence_identity_audit),
        "construction_qa_sha256": _sha(args.construction_qa),
        "temporal_overlay_sha256": _sha(args.temporal_overlay),
        "derived_1988_excerpt_sha256": _sha(args.derived_1988_text),
        "derived_1988_provenance_sha256": _sha(args.derived_1988_provenance),
        "group_count": len(by_group),
        "candidate_count": len(rows),
        "source_count": len(documents),
        "text_extraction": extraction_status,
        "view_readiness": view,
        "missingness_by_role": by_role,
        "retrieval_smoke": retrieval,
        "triplet_surface_parity": surfaces,
        "surface_attention_nonblocking": surface_attention,
        "boundary": "No blind package, no Expected, no GT, no detector model",
        "errors": errors,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
