"""Refine derived Pilot4 taxonomy while preserving every locked source artifact."""

from __future__ import annotations

from collections import Counter
import csv
from hashlib import sha256
from io import StringIO
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from scripts.research.compare_pilot4_final_blind_review import (
    PHASE1_EXPECTED_FIELDS,
    PHASE2_EXPECTED_FIELDS,
    _acceptance_markdown,
    _build_mismatches,
    _file_sha256,
)


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON_OBJECT_REQUIRED:{path}")
    return value


def _atomic_text(path: Path, value: str) -> None:
    temporary = path.with_name(path.name + ".taxonomy-refinement.tmp")
    if temporary.exists():
        raise FileExistsError(f"REFINEMENT_TEMP_ALREADY_EXISTS:{temporary}")
    temporary.write_text(value, encoding="utf-8", newline="\n")
    temporary.replace(path)


def _atomic_json(path: Path, value: object) -> None:
    _atomic_text(path, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def _mismatch_csv(rows: Sequence[Mapping[str, Any]]) -> str:
    fields = (
        "phase",
        "blind_review_id",
        "sample_id",
        "candidate_class",
        "hkp",
        "intended_stealth",
        "field",
        "reviewer_value",
        "expected_value",
        "evidence",
        "taxonomy",
        "materiality",
        "recommended_action",
    )
    stream = StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow(
            {
                field: (
                    json.dumps(row[field], ensure_ascii=False, sort_keys=True)
                    if field == "evidence"
                    else row[field]
                )
                for field in fields
            }
        )
    return "\ufeff" + stream.getvalue()


def refine(output: Path) -> dict[str, Any]:
    """Replace only derived taxonomy/acceptance views and record the refinement."""

    audit_path = output / "qa" / "derived_taxonomy_refinement_audit.json"
    if audit_path.exists():
        raise FileExistsError("DERIVED_TAXONOMY_ALREADY_REFINED")
    raw_paths = sorted((output / "raw").glob("*.csv"))
    raw_before = {path.name: _file_sha256(path) for path in raw_paths}
    phase1 = _read_json(output / "comparison" / "phase1_expected_comparison.json")
    phase2 = _read_json(output / "comparison" / "phase2_expected_comparison.json")
    mismatch_json_path = output / "mismatch" / "all_mismatches.json"
    mismatch_csv_path = output / "mismatch" / "all_mismatches.csv"
    acceptance_json_path = (
        output / "acceptance" / "protocol_acceptance_recommendation.json"
    )
    acceptance_md_path = (
        output / "acceptance" / "PILOT4_ANNOTATION_PROTOCOL_ACCEPTANCE_EVIDENCE.md"
    )
    qa_path = output / "qa" / "final_comparison_qa.json"
    manifest_path = output / "manifest" / "final_manifest.json"
    derived_paths = (
        mismatch_json_path,
        mismatch_csv_path,
        acceptance_json_path,
        acceptance_md_path,
        qa_path,
        manifest_path,
    )
    before_hashes = {
        path.relative_to(output).as_posix(): _file_sha256(path)
        for path in derived_paths
    }

    phase1_rows = phase1["traceable_rows"]
    phase2_rows = phase2["traceable_rows"]
    mismatches = _build_mismatches(
        "PHASE1", phase1_rows, PHASE1_EXPECTED_FIELDS
    ) + _build_mismatches("PHASE2", phase2_rows, PHASE2_EXPECTED_FIELDS)
    taxonomy_counts = dict(
        sorted(Counter(row["taxonomy"] for row in mismatches).items())
    )
    _atomic_json(
        mismatch_json_path,
        {
            "status": "PASS / TAXONOMY_COMPLETE / DERIVED_REFINEMENT_01",
            "mismatch_count": len(mismatches),
            "taxonomy_counts": taxonomy_counts,
            "no_automatic_expected_wins": True,
            "reviewer_values_rewritten": False,
            "expected_values_rewritten": False,
            "records": mismatches,
        },
    )
    _atomic_text(mismatch_csv_path, _mismatch_csv(mismatches))
    criteria = {
        "CLEAR": "FAIL_PRIMARY_STATUS_BOUNDARY_16_ROWS",
        "REPRODUCIBLE": "PASS",
        "ANSWERABLE": "TARGETED_FAIL_1_OF_72_PLUS_PRIMARY_LABEL_BOUNDARY",
        "NON_LEAKING": "PASS_BY_OWNER_ATTESTED_REVIEW_CONTEXT",
        "EVIDENCE_SUFFICIENT": "TARGETED_FAIL_1_OF_72",
        "SCALABLE": "HOLD_UNTIL_GUIDE_AND_EXPECTED_CONTRACT_REPAIR",
    }
    acceptance = {
        "status": "PROTOCOL_ACCEPTANCE_RECOMMENDATION_READY",
        "recommendation": "RECOMMEND_TARGETED_REPAIR",
        "owner_final_acceptance_recorded": False,
        "formal_ab_distribution_authorized": False,
        "systemic_blocker_detected": True,
        "systemic_blockers": [
            "OVERALL_FACT_STATUS_CURRENT_VS_LEGITIMATE_BOUNDARY_16_ROWS"
        ],
        "targeted_material_blocker_categories": [
            "EXPECTED_CONTRACT_FIELD_DEFECTS",
            "MINIMUM_EVIDENCE_CONTRACT_REVIEW",
            "BR-18F1D39495_EVIDENCE_POOL_DESIGN_DEFECT",
        ],
        "criteria": criteria,
        "access_lesson": (
            "LIVE_URL_ACCESS_CAN_BE_TRANSIENT_IN_EXTERNAL_REVIEW_ENVIRONMENT"
        ),
        "access_lesson_status": "PROVISIONAL_PENDING_FINAL_ACCEPTANCE",
        "future_robustness_mechanism": ("URL_PROVENANCE_PLUS_FROZEN_EVIDENCE_SNAPSHOT"),
    }
    _atomic_json(acceptance_json_path, acceptance)
    _atomic_text(
        acceptance_md_path,
        _acceptance_markdown(
            phase1=phase1,
            phase2=phase2,
            mismatches=mismatches,
            taxonomy_counts=taxonomy_counts,
        ),
    )
    qa = _read_json(qa_path)
    qa.update(
        {
            "mismatch_taxonomy_complete": True,
            "derived_taxonomy_refinement": "DERIVED_REFINEMENT_01",
            "systemic_blocker_detected": True,
            "systemic_blocker": (
                "OVERALL_FACT_STATUS_CURRENT_VS_LEGITIMATE_BOUNDARY_16_ROWS"
            ),
            "reviewer_values_rewritten": False,
            "expected_values_rewritten": False,
        }
    )
    _atomic_json(qa_path, qa)
    raw_after = {path.name: _file_sha256(path) for path in raw_paths}
    if raw_after != raw_before:
        raise ValueError("RAW_CHANGED_DURING_DERIVED_REFINEMENT")
    refined_without_manifest = derived_paths[:-1]
    after_hashes = {
        path.relative_to(output).as_posix(): _file_sha256(path)
        for path in refined_without_manifest
    }
    audit = {
        "status": "PASS",
        "scope": "DERIVED_TAXONOMY_AND_ACCEPTANCE_ONLY",
        "reason": (
            "Initial field-based taxonomy was refined after evidence-level review "
            "identified a systemic primary-label boundary and expected-contract defects."
        ),
        "raw_hashes_before": raw_before,
        "raw_hashes_after": raw_after,
        "raw_values_changed": False,
        "reviewer_values_changed": False,
        "expected_source_values_changed": False,
        "derived_artifact_hashes_before": before_hashes,
        "derived_artifact_hashes_after": after_hashes,
        "taxonomy_counts_after": taxonomy_counts,
    }
    _atomic_json(audit_path, audit)
    manifest_records = [
        {
            "path": path.relative_to(output).as_posix(),
            "size": path.stat().st_size,
            "sha256": _file_sha256(path),
        }
        for path in sorted(output.rglob("*"))
        if path.is_file() and path != manifest_path
    ]
    old_manifest = _read_json(manifest_path)
    old_manifest.update(
        {
            "status": (
                "PILOT4_FINAL_BLIND_REVIEW_COMPARISON_COMPLETE / "
                "PROTOCOL_ACCEPTANCE_RECOMMENDATION_READY / "
                "OWNER_PROTOCOL_ACCEPTANCE_PENDING / NO_AB_DISTRIBUTION"
            ),
            "recommendation": "RECOMMEND_TARGETED_REPAIR",
            "derived_taxonomy_refinement": "DERIVED_REFINEMENT_01",
            "record_count": len(manifest_records),
            "records": manifest_records,
        }
    )
    _atomic_json(manifest_path, old_manifest)
    return {
        "status": "PASS / DERIVED_TAXONOMY_REFINED",
        "mismatch_count": len(mismatches),
        "taxonomy_counts": taxonomy_counts,
        "raw_values_changed": False,
        "reviewer_values_changed": False,
        "expected_source_values_changed": False,
        "recommendation": "RECOMMEND_TARGETED_REPAIR",
        "audit_sha256": sha256(audit_path.read_bytes()).hexdigest(),
    }


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(refine(args.output), ensure_ascii=False))


if __name__ == "__main__":
    main()
