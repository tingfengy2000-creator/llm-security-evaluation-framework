"""Build a label-blind, frozen-evidence Phase2 handoff for D1 HKP1 Batch-1.

This is a one-shot construction-QA packet builder, not annotation or GT creation.
It refuses to overwrite an existing release directory.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from html import unescape
from pathlib import Path
from typing import Any


ANCHORS = {
    "LC2012": "第十九条",
    "UI1999": "第十七条",
    "CL2002": "第二条",
    "LA2007": "第二十七条",
    "MW2020": "第十五条",
    "LD2014": "10%",
    "WH1994": "44小时",
    "WH1995": "40小时",
    "HD2013": "春节",
    "HD2024": "春节",
    "SW2023": "2690元",
    "SW2026": "2740元",
    "ML1988": "女职工产假90天",
    "ML2012": "第七条",
}

GUIDES = (
    "PAPER1_FORMAL_ANNOTATION_GUIDE_V4.md",
    "PAPER1_FORMAL_ANNOTATION_GUIDE_V4_1_CLARIFICATION.md",
    "PAPER1_FORMAL_ANNOTATION_GUIDE_V4_2_VERSION_SCOPE_DECISION.md",
)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def official_text(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        from pypdf import PdfReader

        raw = " ".join(page.extract_text() or "" for page in PdfReader(path).pages)
    else:
        raw = path.read_text(encoding="utf-8", errors="replace")
        raw = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", " ", raw, flags=re.I | re.S)
        raw = re.sub(r"<[^>]+>", " ", raw)
        raw = unescape(raw)
    return re.sub(r"\s+", " ", raw).strip()


def bounded_evidence(root: Path, source: dict[str, Any]) -> dict[str, str]:
    doc_id = source["evidence_doc_id"]
    if doc_id not in ANCHORS:
        raise ValueError(f"Unexpected Evidence document {doc_id}")
    raw_path = root / source["raw_path"]
    raw_bytes = raw_path.read_bytes()
    if len(raw_bytes) != source["raw_bytes"] or digest(raw_bytes) != source["raw_sha256"]:
        raise ValueError(f"Evidence snapshot hash mismatch for {doc_id}")
    plain = official_text(raw_path)
    anchor = ANCHORS[doc_id]
    anchor_match = re.search(r"\s*".join(re.escape(character) for character in anchor), plain)
    if anchor_match is None:
        raise ValueError(f"Evidence anchor not found for {doc_id}")
    position = anchor_match.start()
    excerpt = plain[max(0, position - 150) : position + 1150].strip()
    # Both fields are literal substrings of the frozen snapshot text; the first
    # retains document/version/date context, the second retains the rule.
    identity = plain[:650]
    if anchor_match.end() > position + 1150:
        raise ValueError(f"Evidence excerpt lost anchor for {doc_id}")
    return {
        "evidence_doc_id": doc_id,
        "title": source["document_title"],
        "official_url": source["official_url"],
        "snapshot_raw_sha256": source["raw_sha256"],
        "document_identity_excerpt": identity,
        "bounded_fact_excerpt": excerpt,
    }


def prompt(reviewer: str, packet_name: str, schema_name: str, return_name: str) -> str:
    return (
        f"# D1 HKP1 Batch-1 V4 Phase2 — {reviewer}\n\n"
        "Continue in the **same isolated conversation/task** that produced your newly locked "
        "Batch-1 V4 Phase1 return. Do not create a new Project, task or conversation "
        "for this Phase2. If that same session is unavailable, stop and tell the Owner; "
        "do not silently restart or reuse an older Canary session.\n\n"
        "The coordinator has locked both new Phase1 raw returns (30/30 exact schema, "
        "ID/order/enum); the primary pair passes with an Owner-approved, "
        "one-run-only R4 environment exception. This statement is run governance, "
        "not a candidate answer. Work independently and do not inspect the other "
        "reviewer's answer.\n\n"
        f"Read only `{packet_name}`, `{schema_name}`, "
        + ", ".join(f"`{name}`" for name in GUIDES)
        + ", and this prompt. The packet provides 30 opaque candidate IDs in the "
        "same order as Phase1 and frozen official Evidence excerpts/URLs. Use only "
        "those excerpts as factual evidence; URLs are provenance, not permission to "
        "search or add a new source. Do not access the repository, handoff folder, "
        "Owner/constructor packet, identity mapping, C/P/H/HKP/S, Expected/GT, "
        "older returns, another reviewer, external search or another AI. Your own "
        "Phase1 interaction is the only permitted previous review context.\n\n"
        "For each candidate independently fill exactly the Phase2 schema fields. "
        "Keep substantive, document-version and authority claims separate. A bare "
        "law/article citation does not create a version claim (V4.2). A candidate "
        "internal contradiction already confirmed in locked Phase1 requires "
        "`ZERO_EXTERNAL_EVIDENCE_REQUIRED`; actual `evidence_selection` records what "
        "you used, not the minimum. Treat a factual conflict as `phase2_issue=NONE` "
        "unless there is an independent real issue. If frozen Evidence is insufficient, "
        "record that honestly; do not infer missing metadata. Report any session "
        "or routing incident separately at run level, never in a candidate issue.\n\n"
        f"Return one raw UTF-8 JSON array of exactly 30 objects to `{return_name}` "
        "in packet ID order, with exact keys/legal English enums and a concise "
        "Evidence-bound reason. Do not normalize or resave the raw answer after "
        "submission. This is pre-annotation construction QA, not Ground Truth.\n"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--guide-dir", type=Path, required=True)
    parser.add_argument("--phase1-validation", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    root: Path = args.root
    out: Path = args.out
    if out.exists():
        raise FileExistsError(f"Refusing to overwrite {out}")

    gate = read_json(args.phase1_validation)
    if gate["r3_r4_primary_phase1_gate"] != "PASS_WITH_OWNER_APPROVED_BOUNDED_R4_ENVIRONMENT_EXCEPTION":
        raise ValueError("Phase1 primary-pair gate not passed")
    if not gate["phase2_release_authorized"] or gate["owner_decision"] != "BOUNDED_EQUIVALENCE_APPROVED_FOR_R4_RUN02_ONLY":
        raise ValueError("Owner bounded exception not authorized")

    pre = root / "preblind_v4"
    packet_name = "PAPER1_FORMAL_D1_HKP1_BATCH1_PHASE2_PACKAGE_V4.json"
    schema_name = "PAPER1_FORMAL_D1_HKP1_BATCH1_PHASE2_IMPORT_SCHEMA_V4.json"
    phase1 = read_json(pre / "PAPER1_FORMAL_D1_HKP1_BATCH1_R3_GPT_PHASE1_PACKAGE_V4.json")
    phase1_r4 = read_json(pre / "PAPER1_FORMAL_D1_HKP1_BATCH1_R4_CODEX_PHASE1_PACKAGE_V4.json")
    if phase1["records"] != phase1_r4["records"] or len(phase1["records"]) != 30:
        raise ValueError("Phase1 reviewer packet mismatch")
    ordered_ids = [row["blind_review_id"] for row in phase1["records"]]
    candidates = {
        row["blind_review_id"]: row
        for row in (
            json.loads(line)
            for line in (root / "construction_v4" / "PAPER1_FORMAL_D1_HKP1_BATCH1_CANDIDATES_V4.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
        )
    }
    if len(candidates) != 30 or set(candidates) != set(ordered_ids):
        raise ValueError("V4 Candidate/Phase1 ID mismatch")
    manifest = read_json(root / "preconstruction_v2" / "PAPER1_FORMAL_D1_HKP1_BATCH1_EVIDENCE_MANIFEST_V2.json")
    sources = {row["evidence_doc_id"]: row for row in manifest["snapshots"]}
    used_ids = {doc_id for row in candidates.values() for doc_id in row["frozen_evidence_doc_ids"]}
    if len(used_ids) != 14 or any(doc_id not in sources for doc_id in used_ids):
        raise ValueError("Unexpected official Evidence set")
    evidence = {doc_id: bounded_evidence(root, sources[doc_id]) for doc_id in sorted(used_ids)}

    records: list[dict[str, Any]] = []
    for phase1_row in phase1["records"]:
        blind_id = phase1_row["blind_review_id"]
        candidate = candidates[blind_id]
        if candidate["candidate_text"] != phase1_row["candidate_text"]:
            raise ValueError(f"Candidate text drift for {blind_id}")
        refs = candidate["frozen_evidence_doc_ids"]
        if len(refs) not in {1, 2}:
            raise ValueError(f"Unexpected Evidence cardinality for {blind_id}")
        public_evidence = [
            {"evidence_selection_id": f"E{index}", **evidence[doc_id]}
            for index, doc_id in enumerate(refs, start=1)
        ]
        records.append({"blind_review_id": blind_id, "candidate_text": candidate["candidate_text"], "evidence": public_evidence})

    packet = {
        "status": "PHASE2_RELEASED_AFTER_LOCKED_PHASE1_WITH_BOUNDED_R4_EXCEPTION",
        "evidence_scope": "Frozen official excerpts and URL provenance only; no outside Evidence",
        "records": records,
    }
    forbidden = {"construction_role", "group_slot_id", "target_s", "derived_s", "expected", "ground_truth", "hkp"}
    serialized = json.dumps(packet, ensure_ascii=False).lower()
    if any(term in serialized for term in forbidden):
        raise ValueError("Hidden construction/label marker leaked into Phase2 packet")
    if len({row["blind_review_id"] for row in records}) != 30:
        raise ValueError("Duplicate Phase2 blind ID")

    old_schema = read_json(root.parent / "paper1_formal240_d1_canary_20260922" / "PAPER1_FORMAL_D1_BLIND_REVIEW_IMPORT_SCHEMA_V2.json")
    schema = {
        "status": "BATCH1_V4_PHASE2_PREANNOTATION_QA_IMPORT_SCHEMA",
        "phase2": old_schema["phase2"],
        "each_return": "JSON array of exactly 30 objects; exact keys, IDs and packet order",
        "reviewer_independence": "R3/R4 continue their respective accepted Batch-1 Phase1 sessions; do not share answers",
        "not_ground_truth": True,
    }

    out.mkdir(parents=True)
    write_json(out / packet_name, packet)
    write_json(out / schema_name, schema)
    for guide in GUIDES:
        (out / guide).write_bytes((args.guide_dir / guide).read_bytes())
    for reviewer, prefix in (("R3-gpt", "R3_GPT"), ("R4-codex", "R4_CODEX")):
        return_name = f"PAPER1_FORMAL_D1_HKP1_BATCH1_{prefix}_PHASE2_RAW_RETURN_V4.json"
        prompt_name = f"PAPER1_FORMAL_D1_HKP1_BATCH1_{prefix}_PHASE2_PROMPT_V4.md"
        (out / prompt_name).write_text(prompt(reviewer, packet_name, schema_name, return_name), encoding="utf-8")

    file_hashes = {path.name: {"bytes": path.stat().st_size, "sha256": digest(path.read_bytes())} for path in sorted(out.iterdir())}
    write_json(
        out / "PAPER1_FORMAL_D1_HKP1_BATCH1_PHASE2_RELEASE_MANIFEST_V4.json",
        {
            "status": "RELEASED_TO_OWNER_FOR_SAME_SESSION_R3_R4_ONLY",
            "phase1_gate": gate["r3_r4_primary_phase1_gate"],
            "r4_exception_scope": gate["r4_bounded_equivalence"]["scope"],
            "candidate_count": len(records),
            "evidence_doc_count": len(evidence),
            "id_order_parity": ordered_ids == [row["blind_review_id"] for row in records],
            "files": file_hashes,
            "phase2_review_not_yet_executed": True,
        },
    )
    print(json.dumps({"status": "READY", "records": len(records), "evidence_docs": len(evidence), "out": str(out)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
