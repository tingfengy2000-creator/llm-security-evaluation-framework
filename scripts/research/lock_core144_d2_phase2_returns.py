"""Byte-lock D2 Phase2 V2 returns, validate and compare without hidden labels.

No annotation correction, construction/Expected loading, GT, Human release,
split or model execution. Own frozen visible packets are the only row reference.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PREP = Path("experiments/core144_d2_d3_phase2_prep_20261007")
EXCERPTS = PREP / "output_v1/D2/excerpt_release_v2"
PACKAGE_SHA = {
    "R3_GPT": "7e06a18e9269c9ee44443736bf5fc6af7087df3d3f6c23ca3bfc0abe68ea1201",
    "R4_CODEX": "fcaef7ad607bd9f72ffdbf7d5aeb685007b5a44956eacd9b30ee321857f008c2",
}
CATEGORICAL = (
    "overall_fact_status", "version_claim_status", "authority_claim_status",
    "minimum_external_evidence_needed", "evidence_selection", "phase2_issue",
    "possible_accidental_secondary_error", "evidence_sufficiency",
)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def save_new(path: Path, value: Any, readonly: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = value if isinstance(value, bytes) else (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()
    with path.open("xb") as stream:
        stream.write(payload)
        stream.flush()
    if readonly:
        path.chmod(0o444)


def strict_parse(raw: bytes) -> Any:
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError("UTF-8 BOM violates current return contract")

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            if key in result:
                raise ValueError("Duplicate JSON object key")
            result[key] = value
        return result

    def nonfinite(value: str) -> Any:
        raise ValueError(f"Nonfinite JSON constant: {value}")

    return json.loads(raw.decode("utf-8", errors="strict"), object_pairs_hook=pairs, parse_constant=nonfinite)


def lock_sources(sources: list[dict[str, Any]], output: Path) -> list[dict[str, Any]]:
    if output.exists():
        raise ValueError("Fresh immutable output directory required")
    if len(sources) != 2 or {s["reviewer"] for s in sources} != set(PACKAGE_SHA):
        raise ValueError("Exact R3_GPT and R4_CODEX source pair required")
    manifest = []
    # No JSON parsing until BOTH originals and this manifest are saved.
    for source in sources:
        path = Path(source["source"])
        raw = path.read_bytes()
        destination = output / "raw" / f"PAPER1_CORE144_D2_{source['reviewer']}_PHASE2_RAW_RETURN_V2.json"
        save_new(destination, raw, readonly=True)
        if destination.read_bytes() != raw or path.read_bytes() != raw:
            raise ValueError("Raw byte-copy/source stability failure")
        manifest.append({"reviewer": source["reviewer"], "provider": "GPT" if source["reviewer"] == "R3_GPT" else "DOUBAO",
                         "source": str(path), "locked_path": str(destination), "sha256": digest(raw),
                         "bytes": len(raw), "locked_at_utc": datetime.now(timezone.utc).isoformat(),
                         "byte_copy_verified": True, "readonly_copy": True, "parsed_before_lock": False})
    save_new(output / "RAW_LOCK_MANIFEST_V1.json", manifest, readonly=True)
    return manifest


def validate_rows(rows: Any, packet: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    errors: list[dict[str, Any]] = []
    flags: list[dict[str, Any]] = []
    notes: list[dict[str, Any]] = []
    if not isinstance(rows, list):
        return {"structural_pass": False, "structural_errors": [{"code": "NOT_ARRAY"}], "rows": None,
                "consistency_flags": [], "note_reference_flags": []}
    expected = [r["blind_review_id"] for r in packet["records"]]
    by_id = {r["blind_review_id"]: r for r in packet["records"]}
    ids = []
    key_order_matches = 0
    legal_cells = 0
    for index, row in enumerate(rows):
        if not isinstance(row, dict) or set(row) != set(schema["keys"]):
            errors.append({"row": index, "code": "KEYS_NOT_EXACT"})
            continue
        key_order_matches += list(row) == schema["keys"]
        ident = row["blind_review_id"]
        if not all(isinstance(row[k], str) for k in schema["keys"]):
            errors.append({"row": index, "code": "NONSTRING_VALUE"})
            continue
        ids.append(ident)
        for field, legal in schema["enums"].items():
            if row[field] not in legal:
                errors.append({"id": ident, "field": field, "code": "ILLEGAL_ENUM", "value": row[field]})
            else:
                legal_cells += 1
        if not row["phase2_reason"].strip():
            errors.append({"id": ident, "code": "EMPTY_REASON"})
        if ident not in by_id:
            continue
        own = by_id[ident]
        status, minimum = row["overall_fact_status"], row["minimum_external_evidence_needed"]
        code = None
        if status != "FACTUAL_CONFLICT" and minimum != "NOT_APPLICABLE":
            code = "NONCONFLICT_REQUIRES_NOT_APPLICABLE"
        elif status == "FACTUAL_CONFLICT":
            if own["locked_phase1_local_internal_conflict"] == "YES" and minimum != "ZERO_EXTERNAL_EVIDENCE_REQUIRED":
                code = "LOCKED_LOCAL_YES_REQUIRES_ZERO"
            elif own["locked_phase1_local_internal_conflict"] != "YES" and minimum == "ZERO_EXTERNAL_EVIDENCE_REQUIRED":
                code = "ZERO_WITHOUT_LOCKED_LOCAL_YES"
            elif minimum == "NOT_APPLICABLE":
                code = "CONFLICT_MINIMUM_NOT_APPLICABLE"
        if code:
            flags.append({"id": ident, "code": code, "raw_values_unchanged": True})
        selected = set() if row["evidence_selection"] == "NONE" else set(row["evidence_selection"].split("+"))
        if not selected <= set(own["evidence"]):
            flags.append({"id": ident, "code": "UNSUPPLIED_EVIDENCE_SELECTED", "raw_values_unchanged": True})
        # Text-bound reference mismatch is a review lead, not an automatic finding.
        mentioned = set(re.findall(r"\bE[12]\b", row["phase2_reason"] + " " + row["reviewer_note"]))
        if not mentioned <= selected:
            notes.append({"id": ident, "code": "REASON_REFERENCE_OUTSIDE_RECORDED_SELECTION",
                          "mentioned": sorted(mentioned), "selected": sorted(selected),
                          "interpretation": "REQUIRES_CONTEXT_REVIEW_NOT_AUTOMATIC_ERROR"})
    if len(rows) != 144:
        errors.append({"code": "RECORD_COUNT_NOT_144", "count": len(rows)})
    if len(set(ids)) != 144:
        errors.append({"code": "UNIQUE_ID_COUNT_NOT_144", "count": len(set(ids))})
    if ids != expected:
        errors.append({"code": "ID_SET_OR_OWN_ORDER_MISMATCH"})
    return {"rows": len(rows), "unique_ids": len(set(ids)), "structural_pass": not errors,
            "structural_errors": errors, "legal_categorical_cells": legal_cells,
            "key_order_matching_rows": key_order_matches, "key_order_not_a_separate_schema_gate": True,
            "reason_nonblank_rows": sum(isinstance(r, dict) and isinstance(r.get("phase2_reason"), str)
                                        and bool(r["phase2_reason"].strip()) for r in rows),
            "consistency_flags": flags, "note_reference_flags": notes,
            "schema_validity_not_semantic_acceptance": True}


def compare_rows(r3: list[dict[str, Any]], r4: list[dict[str, Any]], packet: dict[str, Any]) -> dict[str, Any]:
    left, right = {r["blind_review_id"]: r for r in r3}, {r["blind_review_id"]: r for r in r4}
    ids = [r["blind_review_id"] for r in packet["records"]]
    comparisons = []
    for row in packet["records"]:
        ident = row["blind_review_id"]
        differing = [f for f in CATEGORICAL if left[ident][f] != right[ident][f]]
        if differing:
            comparisons.append({"blind_review_id": ident, "candidate_text": row["candidate_text"],
                                "fields": differing, "R3": left[ident], "R4": right[ident],
                                "classification": "PROCESS_ONLY_DIFFERENCE" if differing == ["evidence_selection"] else "SEMANTIC_REVIEW_REQUIRED",
                                "adjudicated": False})
    agreement = {f: {"agree": sum(left[i][f] == right[i][f] for i in ids), "total": 144,
                     "disagreement_ids": [i for i in ids if left[i][f] != right[i][f]]} for f in CATEGORICAL}
    return {"field_agreement": agreement, "disagreement_rows": len(comparisons),
            "semantic_disagreement_rows": sum(r["classification"] == "SEMANTIC_REVIEW_REQUIRED" for r in comparisons),
            "process_only_disagreement_rows": sum(r["classification"] == "PROCESS_ONLY_DIFFERENCE" for r in comparisons),
            "comparison_records": comparisons,
            "reason_exact_byte_equal_rows": sum(left[i]["phase2_reason"] == right[i]["phase2_reason"] for i in ids),
            "reason_wording_difference_not_a_categorical_failure": True,
            "distributions": {reviewer: {f: dict(Counter(r[f] for r in rows)) for f in CATEGORICAL}
                              for reviewer, rows in (("R3_GPT", r3), ("R4_CODEX", r4))},
            "GT_created": False, "raw_values_unchanged": True,
            "independent_semantic_adjudication_executed": False}


def run(repo: Path, output: Path, sources: list[dict[str, Any]], attested: bool) -> dict[str, Any]:
    locked = lock_sources(sources, output)
    # Seal preservation evidence before any parsing/row assessment.
    index_path = repo / PREP / "FINAL_EVIDENCE_INDEX_V1.json"
    if digest(index_path.read_bytes()) != "2e92f682cbba6261381388f3c5b62b6cd5aa63e7c073609a4fc2ee581a03a4f9":
        raise ValueError("Frozen preparation index changed")
    index = strict_parse(index_path.read_bytes())
    for name, item in index["files"].items():
        if digest((index_path.parent / name).read_bytes()) != item["sha256"]:
            raise ValueError("Frozen preparation artifact changed")
    validations, parsed, packets = {}, {}, {}
    schema = strict_parse((repo / EXCERPTS / "R3_GPT/PAPER1_CORE144_D2_PHASE2_IMPORT_SCHEMA_V1.json").read_bytes())
    for item in locked:
        reviewer = item["reviewer"]
        path = repo / EXCERPTS / reviewer / f"PAPER1_CORE144_D2_{reviewer}_PHASE2_PACKAGE_V2.json"
        if digest(path.read_bytes()) != PACKAGE_SHA[reviewer]:
            raise ValueError("Frozen own packet identity changed")
        packets[reviewer] = strict_parse(path.read_bytes())
        try:
            rows = strict_parse(Path(item["locked_path"]).read_bytes())
            validations[reviewer] = validate_rows(rows, packets[reviewer], schema)
            parsed[reviewer] = rows
        except (ValueError, UnicodeError) as error:
            validations[reviewer] = {"structural_pass": False, "parse_error": str(error), "rows": None}
    save_new(output / "STRUCTURAL_AND_CROSS_FIELD_VALIDATION_V1.json", validations)
    valid = all(v["structural_pass"] for v in validations.values())
    comparison = compare_rows(parsed["R3_GPT"], parsed["R4_CODEX"], packets["R3_GPT"]) if valid else None
    if comparison is not None:
        save_new(output / "CATEGORICAL_COMPARISON_V1.json", comparison)
        attention = []
        for reviewer, rows in parsed.items():
            for row in rows:
                if row["phase2_issue"] != "NONE" or row["possible_accidental_secondary_error"] != "NO" or row["evidence_sufficiency"] != "SUFFICIENT" or row["overall_fact_status"] == "INSUFFICIENT_EVIDENCE":
                    attention.append({"reviewer": reviewer, "raw_answer": row, "adjudicated": False})
        save_new(output / "REVIEWER_SHARED_OR_INDIVIDUAL_QUALITY_FLAGS_V1.json", attention)
    else:
        attention = []
    result = {"task": "P1-CORE144-D2-PHASE2-RAW-LOCK-AND-COMPARISON-01", "raw_locked": True,
              "R3_R4_structural_validation_pass": valid, "validation": validations,
              "isolation": "OWNER_ATTESTED" if attested else "PENDING_OWNER_ATTESTATION",
              "isolation_machine_proven": False, "reviewer_code_R4_CODEX_actual_provider": "DOUBAO",
              "semantic_disagreement_rows": comparison["semantic_disagreement_rows"] if comparison else None,
              "process_only_disagreement_rows": comparison["process_only_disagreement_rows"] if comparison else None,
              "quality_flag_records": len(attention), "frozen_preparation_files_reverified": len(index["files"]),
              "status": "RAW_LOCKED_VALID_COMPARISON_REVIEW_REQUIRED" if valid else "RAW_LOCKED_STRUCTURAL_BLOCKER",
              "D2_machine_preannotation_accepted": False, "Human_D2_release_authorized": False,
              "D3_still_withheld": True, "GT_created": False, "split_or_training_executed": False}
    save_new(output / "RAW_LOCK_AND_DOMAIN_GATE_V1.json", result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--input", type=Path, required=True)
    args = parser.parse_args()
    plan = strict_parse(args.input.read_bytes())
    print(json.dumps(run(args.repo.resolve(), args.output.resolve(), plan["sources"], plan["owner_attested"]), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
