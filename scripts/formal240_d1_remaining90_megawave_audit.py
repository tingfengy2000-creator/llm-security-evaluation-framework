"""Pre-release cross-batch integrity audit for one D1 90-row blind MegaWave.

Construction roles stay in the private audit. This script does not build a
reviewer package, inspect Expected/GT, run a detector, or accept any candidate.
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
FORMAL = REPO_ROOT / "docs/research/stage6_1_hidden_knowledge_poisoning/formal240"
FILES = {
    "HKP2": (
        "PAPER1_FORMAL_D1_HKP2_CANDIDATE_DRAFT_V8_NOT_RELEASED.jsonl",
        "PAPER1_FORMAL_D1_HKP2_CONSTRUCTION_SIDE_QA_V5.json",
        "PAPER1_FORMAL_D1_HKP2_INTERNAL_MECHANICAL_QA_V5.json",
        "PAPER1_FORMAL_D1_HKP2_EVIDENCE_PRECONTRACT_V1.json",
    ),
    "HKP3": (
        "PAPER1_FORMAL_D1_HKP3_CANDIDATE_DRAFT_V4_NOT_RELEASED.jsonl",
        "PAPER1_FORMAL_D1_HKP3_CONSTRUCTION_SIDE_QA_V4.json",
        "PAPER1_FORMAL_D1_HKP3_INTERNAL_MECHANICAL_QA_V4.json",
        "PAPER1_FORMAL_D1_HKP3_EVIDENCE_PRECONTRACT_V1.json",
    ),
    "HKP4": (
        "PAPER1_FORMAL_D1_HKP4_CANDIDATE_DRAFT_V1_NOT_RELEASED.jsonl",
        "PAPER1_FORMAL_D1_HKP4_CONSTRUCTION_SIDE_QA_V1.json",
        "PAPER1_FORMAL_D1_HKP4_INTERNAL_MECHANICAL_QA_V2.json",
        "PAPER1_FORMAL_D1_HKP4_EVIDENCE_PRECONTRACT_V1.json",
    ),
}
EXPECTED_S = {
    "HKP2": Counter({"S1": 3, "S2": 3, "S3": 4}),
    "HKP3": Counter({"S1": 4, "S2": 3, "S3": 3}),
    "HKP4": Counter({"S1": 4, "S2": 2, "S3": 4}),
}
NEED = {
    "S1": "ZERO_EXTERNAL_EVIDENCE_REQUIRED",
    "S2": "ONE_OFFICIAL_EVIDENCE",
    "S3": "MULTI_EVIDENCE_OR_VERSION_CHAIN",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(root_by_hkp: dict[str, Path]) -> dict[str, Any]:
    errors: list[str] = []
    alerts: list[str] = []
    all_rows: list[dict[str, Any]] = []
    source_hashes = {}
    family_by_cell: dict[tuple[str, str], set[str]] = defaultdict(set)
    family_clusters: Counter[str] = Counter()
    by_role_missing: dict[str, Counter[str]] = defaultdict(Counter)
    source_counts = {}
    for hkp, root in root_by_hkp.items():
        candidate_name, atom_name, mechanical_name, precontract_name = FILES[hkp]
        candidate_path = root / candidate_name
        atom_path = root / atom_name
        mechanical_path = root / mechanical_name
        precontract_path = FORMAL / precontract_name
        candidate_bytes = candidate_path.read_bytes()
        candidate_bytes.decode("utf-8", errors="strict")
        candidates = [json.loads(line) for line in candidate_bytes.decode("utf-8").splitlines()]
        atom = load(atom_path)
        mechanical = load(mechanical_path)
        precontract = load(precontract_path)
        source_hashes[hkp] = {
            "candidate_sha256": sha(candidate_path),
            "atom_qa_sha256": sha(atom_path),
            "mechanical_qa_sha256": sha(mechanical_path),
            "precontract_sha256": sha(precontract_path),
        }
        if atom["status"] != "CONSTRUCTION_SIDE_QA_PASS_NOT_BLIND_REVIEW":
            errors.append(f"construction atom gate failed: {hkp}")
        if mechanical["status"] != f"{hkp}_INTERNAL_MECHANICAL_QA_PASS_EXTERNAL_REVIEW_NOT_DONE":
            errors.append(f"mechanical gate failed: {hkp}")
        if atom["candidate_draft_sha256"] != sha(candidate_path) or mechanical["candidate_draft_sha256"] != sha(candidate_path):
            errors.append(f"candidate lock hash mismatch: {hkp}")
        if mechanical["construction_qa_sha256"] != sha(atom_path):
            errors.append(f"atom/mechanical lineage mismatch: {hkp}")
        groups = {g["group_slot_id"]: g for g in precontract["groups"]}
        ids = {r["group_slot_id"] for r in candidates}
        if len(candidates) != 30 or len(ids) != 10 or ids != set(groups):
            errors.append(f"30-row/10-group contract parity failed: {hkp}")
        if Counter(g["target_s"] for g in groups.values()) != EXPECTED_S[hkp]:
            errors.append(f"frozen S allocation failed: {hkp}")
        if Counter(r["role"] for r in candidates) != Counter(
            {"CLEAN_CURRENT": 10, "POISON": 10, "HARD_NEGATIVE": 10}
        ):
            errors.append(f"C/P/H distribution failed: {hkp}")
        source_counts[hkp] = mechanical["source_count"]
        for group in groups.values():
            cell = (hkp, group["target_s"])
            family = group["family_cluster_id"]
            if family in family_by_cell[cell]:
                errors.append(f"family repeated within HKP-by-S cell: {cell} {family}")
            family_by_cell[cell].add(family)
            family_clusters[family] += 1
            if group["evidence_path_precommit"] != NEED[group["target_s"]]:
                errors.append(f"target/evidence-path mismatch: {group['group_slot_id']}")
        for row in candidates:
            group = groups[row["group_slot_id"]]
            if row["target_s"] != group["target_s"] or row["family_cluster_id"] != group["family_cluster_id"]:
                errors.append(f"candidate/group metadata mismatch: {row['sample_id']}")
            if (group.get("neutral_query") and row["neutral_query"] != group["neutral_query"]) or row["evidence_refs"] != group["evidence_refs"]:
                errors.append(f"query/evidence lineage mismatch: {row['sample_id']}")
            if row["external_blind_review"] != "NOT_RELEASED":
                errors.append(f"premature release status: {row['sample_id']}")
            if re.search(r"(?i)poison|clean|hard.?negative|hkp|s[123]|ground.?truth|expected", row["candidate_text"]):
                errors.append(f"construction-label token in text: {row['sample_id']}")
            all_rows.append({"hkp": hkp, **row})
        for view_row in mechanical["view_readiness"]:
            by_role_missing[view_row["role"]][str(view_row["input_missing"])] += 1
    if len(all_rows) != 90 or len({r["sample_id"] for r in all_rows}) != 90:
        errors.append("90-row/global sample-ID uniqueness failed")
    if len({r["candidate_text"] for r in all_rows}) != len(all_rows):
        errors.append("exact duplicate candidate text across remaining90")
    if len({r["group_slot_id"] for r in all_rows}) != 30:
        errors.append("group count not thirty")
    if Counter(r["role"] for r in all_rows) != Counter(
        {"CLEAN_CURRENT": 30, "POISON": 30, "HARD_NEGATIVE": 30}
    ):
        errors.append("combined C/P/H distribution mismatch")
    if Counter(r["target_s"] for r in all_rows) != Counter(
        {"S1": 33, "S2": 24, "S3": 33}
    ):
        errors.append("combined target-S population mismatch")
    if len({json.dumps(dict(v), sort_keys=True) for v in by_role_missing.values()}) != 1:
        errors.append("input missingness differs by role across remaining90")

    near_duplicates = []
    for index, left in enumerate(all_rows):
        for right in all_rows[index + 1 :]:
            if left["group_slot_id"] == right["group_slot_id"]:
                continue
            ratio = difflib.SequenceMatcher(None, left["candidate_text"], right["candidate_text"]).ratio()
            if ratio >= 0.93:
                near_duplicates.append(
                    {"sample_id_a": left["sample_id"], "sample_id_b": right["sample_id"], "similarity": round(ratio, 4)}
                )
    if near_duplicates:
        alerts.append(f"cross-group near-duplicate pairs >=0.93: {len(near_duplicates)}")
    lexical_cues = {
        role: {
            pattern: sum(
                bool(re.search(pattern, row["candidate_text"]))
                for row in all_rows if row["role"] == role
            )
            for pattern in ("没有变化|保持不变|并无差别|并未改变", "未变|不变", "反而|不降反升")
        }
        for role in ("CLEAN_CURRENT", "POISON", "HARD_NEGATIVE")
    }
    no_change_roles = [
        role for role, values in lexical_cues.items() if values["没有变化|保持不变|并无差别|并未改变"] or values["未变|不变"]
    ]
    if no_change_roles == ["POISON"]:
        errors.append("unchanged-version phrase is poison-only across remaining90")
    if len(family_clusters) < 10:
        alerts.append("fewer than ten family clusters across thirty groups")
    return {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "status": "REMAINING90_INTERNAL_CROSS_BATCH_GATE_PASS_EXTERNAL_REVIEW_PENDING"
        if not errors
        else "REMAINING90_INTERNAL_CROSS_BATCH_GATE_BLOCKED",
        "candidate_count": len(all_rows),
        "group_count": len({r["group_slot_id"] for r in all_rows}),
        "role_counts": dict(Counter(r["role"] for r in all_rows)),
        "target_s_candidate_counts": dict(Counter(r["target_s"] for r in all_rows)),
        "hkp_candidate_counts": dict(Counter(r["hkp"] for r in all_rows)),
        "source_document_counts_by_hkp": source_counts,
        "family_cluster_count": len(family_clusters),
        "family_cluster_group_reuse": {k: v for k, v in family_clusters.items() if v > 1},
        "input_missingness_by_role": {k: dict(v) for k, v in by_role_missing.items()},
        "cross_group_near_duplicate_pairs": near_duplicates,
        "lexical_cue_counts_by_role": lexical_cues,
        "source_artifact_hashes": source_hashes,
        "alerts_requiring_owner_reading_not_automatic_failure": alerts,
        "errors": errors,
        "scientific_boundary": "Construction-side audit only; no R3/R4 return, no Human A/B, no GT, no split or detector.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hkp2-root", type=Path, required=True)
    parser.add_argument("--hkp3-root", type=Path, required=True)
    parser.add_argument("--hkp4-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"Refusing to overwrite: {args.output}")
    result = run({"HKP2": args.hkp2_root, "HKP3": args.hkp3_root, "HKP4": args.hkp4_root})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(result["status"], result["candidate_count"], result["group_count"], len(result["errors"]), result["alerts_requiring_owner_reading_not_automatic_failure"])
    if result["errors"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
