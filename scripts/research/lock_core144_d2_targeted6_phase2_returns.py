"""Lock and validate targeted D2 returns; no adjudication or acceptance by vote."""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from scripts.research.lock_core144_d2_phase2_returns import CATEGORICAL, digest, save_new, strict_parse

REVIEWERS = ("R3_GPT", "R4_CODEX")
PRIOR = Path("experiments/core144_d2_phase2_excerpt_v3_review_20261015")
PRIOR_INDEX_SHA = "524e8a7b91bec0b0776f55cdfe4ad5c979f8f31a225b19b6a7e0aa812665fcf5"


def lock_pair(sources: dict[str, Path], output: Path) -> list[dict[str, Any]]:
    if set(sources) != set(REVIEWERS) or output.exists():
        raise ValueError("Exact reviewer pair and fresh immutable output required")
    manifest = []
    for reviewer in REVIEWERS:
        raw = sources[reviewer].read_bytes()
        path = output / "raw" / (reviewer + ".json")
        save_new(path, raw, readonly=True)
        if path.read_bytes() != raw or sources[reviewer].read_bytes() != raw:
            raise ValueError("Original byte-copy/source stability failure")
        manifest.append({"reviewer_code": reviewer, "actual_provider": "OPENAI_GPT" if reviewer == "R3_GPT" else "DOUBAO",
                         "original_path": str(sources[reviewer]), "locked_path": str(path),
                         "original_filename": sources[reviewer].name,
                         "sha256": digest(raw), "bytes": len(raw),
                         "locked_at_utc": datetime.now(timezone.utc).isoformat(),
                         "byte_copy_verified": True, "parsed_before_both_locks": False})
    save_new(output / "RAW_LOCK_MANIFEST_V1.json", manifest, readonly=True)
    return manifest


def validate_targeted(rows: Any, packet: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    errors: list[dict[str, Any]] = []
    flags: list[dict[str, Any]] = []
    reference_flags: list[dict[str, Any]] = []
    if not isinstance(rows, list):
        return {"structural_pass": False, "errors": [{"code": "NOT_ARRAY"}], "consistency_flags": []}
    expected = [r["blind_review_id"] for r in packet["records"]]
    by_id = {r["blind_review_id"]: r for r in packet["records"]}
    ids, cells, key_order = [], 0, 0
    for position, row in enumerate(rows):
        if not isinstance(row, dict) or set(row) != set(schema["keys"]):
            errors.append({"position": position, "code": "KEYS_NOT_EXACT"})
            continue
        if not all(isinstance(row[k], str) for k in schema["keys"]):
            errors.append({"position": position, "code": "NONSTRING"})
            continue
        ident = row["blind_review_id"]
        ids.append(ident)
        key_order += list(row) == schema["keys"]
        for field, legal in schema["enums"].items():
            if row[field] not in legal:
                errors.append({"id": ident, "field": field, "code": "ILLEGAL_ENUM"})
            else:
                cells += 1
        if not row["phase2_reason"].strip():
            errors.append({"id": ident, "code": "EMPTY_REASON"})
        if ident not in by_id:
            continue
        own = by_id[ident]
        status, minimum = row["overall_fact_status"], row["minimum_external_evidence_needed"]
        code = None
        if status != "FACTUAL_CONFLICT" and minimum != "NOT_APPLICABLE":
            code = "NONCONFLICT_MINIMUM"
        elif status == "FACTUAL_CONFLICT":
            if own["locked_phase1_local_internal_conflict"] == "YES" and minimum != "ZERO_EXTERNAL_EVIDENCE_REQUIRED":
                code = "LOCAL_YES_REQUIRES_ZERO"
            elif own["locked_phase1_local_internal_conflict"] != "YES" and minimum == "ZERO_EXTERNAL_EVIDENCE_REQUIRED":
                code = "ZERO_WITHOUT_LOCAL_YES"
            elif minimum == "NOT_APPLICABLE":
                code = "CONFLICT_MINIMUM_NA"
        if code:
            flags.append({"id": ident, "code": code})
        selected = set() if row["evidence_selection"] == "NONE" else set(row["evidence_selection"].split("+"))
        if not selected <= set(own["evidence"]):
            flags.append({"id": ident, "code": "UNSUPPLIED_EVIDENCE_SELECTED"})
        mentioned = set(re.findall(r"\bE[12]\b", row["phase2_reason"] + " " + row["reviewer_note"]))
        if not mentioned <= selected:
            reference_flags.append({"id": ident, "code": "REASON_REFERENCE_OUTSIDE_SELECTION",
                                    "mentioned": sorted(mentioned), "selected": sorted(selected),
                                    "not_automatic_semantic_error": True})
    if len(rows) != schema["record_count"] or len(rows) != len(expected):
        errors.append({"code": "COUNT_MISMATCH"})
    if len(set(ids)) != len(expected):
        errors.append({"code": "DUPLICATE_MISSING_OR_UNEXPECTED_ID"})
    if ids != expected:
        errors.append({"code": "ID_OR_OWN_ORDER_MISMATCH"})
    return {"structural_pass": not errors, "errors": errors, "rows": len(rows), "unique_ids": len(set(ids)),
            "id_order_exact": ids == expected, "legal_categorical_cells": cells,
            "key_order_matching_rows": key_order, "key_order_not_separate_semantic_gate": True,
            "reasons_nonblank": sum(isinstance(r, dict) and isinstance(r.get("phase2_reason"), str) and
                                     bool(r["phase2_reason"].strip()) for r in rows),
            "consistency_flags": flags, "reference_flags": reference_flags,
            "schema_validity_not_factual_acceptance": True}


def run(repo: Path, sources: dict[str, Path], output: Path) -> dict[str, Any]:
    # Preserve both originals before JSON parsing, including on malformed returns.
    locked = lock_pair(sources, output)
    index_data = (repo / PRIOR / "FINAL_EVIDENCE_INDEX_V1.json").read_bytes()
    if digest(index_data) != PRIOR_INDEX_SHA:
        raise ValueError("Prior sealed index changed")
    index = strict_parse(index_data)
    for name, entry in index["files"].items():
        raw = (repo / PRIOR / name).read_bytes()
        if digest(raw) != entry["sha256"] or len(raw) != entry["bytes"]:
            raise ValueError("Prior artifact changed: " + name)
    results, validated, packets = {}, {}, {}
    for reviewer in REVIEWERS:
        directory = repo / PRIOR / "output_v2/reviewer_release" / reviewer
        packets[reviewer] = strict_parse((directory / f"PAPER1_CORE144_D2_{reviewer}_TARGETED6_PHASE2_PACKAGE_V3.json").read_bytes())
        schema = strict_parse((directory / "PAPER1_CORE144_D2_TARGETED6_PHASE2_IMPORT_SCHEMA_V3.json").read_bytes())
        try:
            results[reviewer] = strict_parse((output / "raw" / (reviewer + ".json")).read_bytes())
            validated[reviewer] = validate_targeted(results[reviewer], packets[reviewer], schema)
        except (ValueError, UnicodeError) as error:
            validated[reviewer] = {"structural_pass": False, "error_type": type(error).__name__,
                                   "consistency_flags": []}
    save_new(output / "STRUCTURAL_AND_CROSS_FIELD_VALIDATION_V1.json", validated)
    if not all(v["structural_pass"] for v in validated.values()):
        summary = {"structural_pass": False, "status": "RAW_LOCKED_VALIDATION_BLOCKER", "raw_rewritten": False}
        save_new(output / "SUMMARY_V1.json", summary)
        return summary
    left, right = ({r["blind_review_id"]: r for r in results[who]} for who in REVIEWERS)
    comparisons = []
    for row in packets["R3_GPT"]["records"]:
        ident = row["blind_review_id"]
        comparisons.append({"blind_review_id": ident, "candidate": row,
                            "R3_GPT": left[ident], "R4_CODEX": right[ident],
                            "different_fields": [f for f in CATEGORICAL if left[ident][f] != right[ident][f]],
                            "adjudicated": False})
    agreement = {field: {"agree": sum(left[i][field] == right[i][field] for i in left), "total": len(left),
                         "disagreement_ids": [i for i in left if left[i][field] != right[i][field]]}
                 for field in CATEGORICAL}
    prior_reviews = strict_parse((repo / PRIOR / "output_v2/BOUNDED43_RULE_REVIEW_PROPOSALS_V1.json").read_bytes())
    before = {r["blind_review_id"]: r for r in prior_reviews}
    changes = []
    for reviewer in REVIEWERS:
        for row in results[reviewer]:
            old = before[row["blind_review_id"]]["before"][reviewer]
            changes.append({"reviewer": reviewer, "blind_review_id": row["blind_review_id"],
                            "before": old, "after": row,
                            "changed_fields": [k for k in row if row[k] != old[k]],
                            "lineage": "V2 raw -> V3 targeted raw, not silent replacement",
                            "effective_annotation": None})
    save_new(output / "TARGETED6_COMPARISON_V1.json", {"field_agreement": agreement, "records": comparisons,
                                                      "reason_wording_not_a_literal_equality_gate": True})
    save_new(output / "V2_TO_V3_TARGETED_RETURN_LINEAGE_V1.json", changes)
    summary = {"structural_pass": True, "rows_each": 6, "prior_sealed_files_unchanged": len(index["files"]),
               "categorical_agreement": agreement, "different_rows": sum(bool(r["different_fields"]) for r in comparisons),
               "cross_field_flags": sum(len(v["consistency_flags"]) for v in validated.values()),
               "raw_sha256": {r["reviewer_code"]: r["sha256"] for r in locked},
               "status": "STRUCTURALLY_VALID_SEMANTIC_REVIEW_PENDING", "human_release_authorized": False,
               "GT_created": False, "Expected_loaded": False, "raw_rewritten": False}
    save_new(output / "SUMMARY_V1.json", summary)
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--r3", type=Path, required=True)
    parser.add_argument("--r4", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(Path.cwd(), {"R3_GPT": args.r3, "R4_CODEX": args.r4}, args.output), ensure_ascii=False, indent=2))
