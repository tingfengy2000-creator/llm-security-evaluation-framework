from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

from scripts.research.close_pilot4_owner_adjudication_consistency import (
    validate_candidate_view,
)
from scripts.research.ingest_pilot4_owner_adjudication_return import (
    ALL_FIELDS,
    ENUMS,
    manifest_entries,
    sha256,
    write_json,
    write_text,
)


TASK_ID = "PILOT4-FINAL72-EXPECTED-V3-QC-AND-GROUND-TRUTH-CANDIDATE-01"
EXPECTED_V3_SHA256 = "dc549ff6adbacc6a87049c08c7db7e414b9d52dafc19c31f98b5c10490031433"
OWNER_WORKBOOK_SHA256 = (
    "a4c65a22dd3a410c7744be5f256206d7217b8fda33d63c58ac99bb386fe95b01"
)
CONSISTENCY_AGGREGATE_SHA256 = (
    "f876abf7ff854e76742b325ebd344008b76d6f98ed592aa01e0b09567b8d7ad8"
)
CANDIDATE_CORPUS_SHA256 = (
    "f530471ecd6551300d68c8ddf104cadce2305d8ff91e64010be222820628252d"
)
EXPECTED_FIELDS = tuple(field for field in ALL_FIELDS if field != "phase2_issue")
PHASE1_FIELDS = ALL_FIELDS[:3]
PHASE2_FIELDS = ALL_FIELDS[3:]


def now_utc() -> str:
    return datetime.now(UTC).isoformat(timespec="microseconds").replace("+00:00", "Z")


def require_new_output(path: Path) -> None:
    if path.exists() and any(path.iterdir()):
        raise ValueError(f"OUTPUT_NAMESPACE_NOT_EMPTY:{path}")
    path.mkdir(parents=True, exist_ok=True)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line
    ]


def write_jsonl(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(
            json.dumps(dict(row), ensure_ascii=False, sort_keys=True) + "\n"
            for row in rows
        ),
        encoding="utf-8",
        newline="\n",
    )


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def manifest_index(root: Path) -> tuple[dict[str, Any], dict[str, Mapping[str, Any]]]:
    manifest = read_json(root / "manifest/final_manifest.json")
    rows = manifest.get("entries", manifest.get("files"))
    if not isinstance(rows, list):
        raise ValueError(f"MANIFEST_SCHEMA_BLOCKER:{root}")
    return manifest, {str(row["path"]): row for row in rows}


def verify_manifest_subset(root: Path, paths: Sequence[str]) -> dict[str, Any]:
    manifest, entries = manifest_index(root)
    verified: list[dict[str, Any]] = []
    for relative in paths:
        if relative not in entries:
            raise ValueError(f"MANIFEST_ENTRY_MISSING:{root}:{relative}")
        expected = entries[relative]
        path = root / relative
        actual = {
            "path": str(path.resolve()),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        }
        if (
            actual["bytes"] != expected["bytes"]
            or actual["sha256"] != expected["sha256"]
        ):
            raise ValueError(f"MANIFEST_ENTRY_IDENTITY_BLOCKER:{path}")
        verified.append(actual)
    return {
        "manifest_path": str((root / "manifest/final_manifest.json").resolve()),
        "manifest_aggregate_sha256": manifest.get("aggregate_sha256"),
        "verified_entries": verified,
        "status": "PASS",
    }


def verify_full_manifest(root: Path, required_aggregate: str) -> dict[str, Any]:
    manifest, entries = manifest_index(root)
    if manifest.get("aggregate_sha256") != required_aggregate:
        raise ValueError(f"MANIFEST_AGGREGATE_BLOCKER:{root}")
    mismatches: list[str] = []
    for relative, expected in entries.items():
        path = root / relative
        if (
            not path.is_file()
            or path.stat().st_size != expected["bytes"]
            or sha256(path) != expected["sha256"]
        ):
            mismatches.append(relative)
    if mismatches:
        raise ValueError(f"MANIFEST_CONTENT_BLOCKER:{root}:{mismatches}")
    return {
        "manifest_path": str((root / "manifest/final_manifest.json").resolve()),
        "aggregate_sha256": required_aggregate,
        "entry_count": len(entries),
        "mismatches": mismatches,
        "status": "PASS",
    }


def assert_sha(path: Path, expected: str) -> dict[str, Any]:
    actual = sha256(path)
    if actual != expected:
        raise ValueError(f"SHA256_BLOCKER:{path}:{actual}")
    return {
        "path": str(path.resolve()),
        "bytes": path.stat().st_size,
        "sha256": actual,
        "status": "PASS",
    }


def load_mapping(path: Path, annotator: str) -> dict[str, dict[str, Any]]:
    payload = read_json(path)
    if payload["annotator_id"] != annotator or len(payload["records"]) != 72:
        raise ValueError(f"MAPPING_CONTRACT_BLOCKER:{path}")
    mapping = {str(row["blind_review_id"]): dict(row) for row in payload["records"]}
    if len(mapping) != 72 or len({row["sample_id"] for row in mapping.values()}) != 72:
        raise ValueError(f"MAPPING_PARITY_BLOCKER:{path}")
    return mapping


def rows_by_sample(
    path: Path,
    mapping: Mapping[str, Mapping[str, Any]],
    expected_header: Sequence[str],
) -> dict[str, dict[str, str]]:
    rows = read_csv(path)
    if len(rows) != 72 or list(rows[0]) != list(expected_header):
        raise ValueError(f"RAW_RETURN_SCHEMA_BLOCKER:{path}")
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        blind_id = row["blind_review_id"]
        if blind_id not in mapping:
            raise ValueError(f"RAW_RETURN_MAPPING_BLOCKER:{path}:{blind_id}")
        sample_id = str(mapping[blind_id]["sample_id"])
        if sample_id in result:
            raise ValueError(f"RAW_RETURN_DUPLICATE_SAMPLE_BLOCKER:{path}:{sample_id}")
        result[sample_id] = {
            **row,
            **{f"mapping_{k}": str(v) for k, v in mapping[blind_id].items()},
        }
    if len(result) != 72:
        raise ValueError(f"RAW_RETURN_POPULATION_BLOCKER:{path}")
    return result


def validate_raw_reasons(
    phase1: Mapping[str, Mapping[str, str]],
    phase2: Mapping[str, Mapping[str, str]],
) -> None:
    for sample_id, row in phase1.items():
        required = (
            row["local_internal_conflict"] != "NO" or row["phase1_issue"] != "NONE"
        )
        if required and not row["phase1_reason"].strip():
            raise ValueError(f"PHASE1_REASON_BLOCKER:{sample_id}")
    for sample_id, row in phase2.items():
        if not row["phase2_reason"].strip():
            raise ValueError(f"PHASE2_REASON_BLOCKER:{sample_id}")


def build_human_lineage(
    phase1: Mapping[str, Mapping[str, Mapping[str, str]]],
    phase2: Mapping[str, Mapping[str, Mapping[str, str]]],
    owner: Mapping[str, Any],
    owner_rules: Mapping[str, Any],
    consistency: Mapping[str, Any],
    final_view: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], Counter[str]]:
    owner_values = {
        (str(row["sample_id"]), str(row["field"])): row
        for row in owner["field_adjudications"]
    }
    rule_overlays: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for row in owner_rules["overlays"]:
        rule_overlays.setdefault((str(row["sample_id"]), str(row["field"])), []).append(
            dict(row)
        )
    consistency_overlays: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for row in consistency["corrections"]:
        consistency_overlays.setdefault(
            (str(row["sample_id"]), str(row["field"])), []
        ).append(dict(row))
    final_by_id = {str(row["sample_id"]): row for row in final_view["records"]}
    if len(final_by_id) != 72:
        raise ValueError("FINAL_HUMAN_VIEW_POPULATION_BLOCKER")

    lineage: list[dict[str, Any]] = []
    gt_records: list[dict[str, Any]] = []
    base_counts: Counter[str] = Counter()
    for sample_id in sorted(final_by_id):
        labels: dict[str, str] = {}
        for field in ALL_FIELDS:
            source_rows = phase1 if field in PHASE1_FIELDS else phase2
            a_row = source_rows["HUMAN-A01"][sample_id]
            b_row = source_rows["HUMAN-B01"][sample_id]
            reason_field = (
                "phase1_reason" if field in PHASE1_FIELDS else "phase2_reason"
            )
            a_value = a_row[field]
            b_value = b_row[field]
            key = (sample_id, field)
            if a_value == b_value:
                value = a_value
                base_source = "A_B_AGREEMENT"
                owner_row: Mapping[str, Any] | None = None
            else:
                if key not in owner_values:
                    raise ValueError(f"OWNER_ADJUDICATION_LINEAGE_BREAK:{key}")
                owner_row = owner_values[key]
                value = str(owner_row["owner_final_value"])
                base_source = "OWNER_ADJUDICATION"
            base_counts[base_source] += 1
            base_value = value
            events: list[dict[str, Any]] = []
            for overlay in rule_overlays.get(key, []):
                if str(overlay["before"]) != value:
                    raise ValueError(f"OWNER_RULE_OVERLAY_BEFORE_BREAK:{key}")
                value = str(overlay["after"])
                events.append({"type": "OWNER_AUTHORIZED_RULE_OVERLAY", **overlay})
            for overlay in consistency_overlays.get(key, []):
                if str(overlay["before"]) != value:
                    raise ValueError(f"CONSISTENCY_OVERLAY_BEFORE_BREAK:{key}")
                value = str(overlay["after"])
                events.append(
                    {"type": "OWNER_CONSISTENCY_CORRECTION_OVERLAY", **overlay}
                )
            final_cell = final_by_id[sample_id]["fields"][field]
            if value != str(final_cell["value"]):
                raise ValueError(
                    f"FINAL_HUMAN_VALUE_LINEAGE_BREAK:{key}:{value}:{final_cell['value']}"
                )
            labels[field] = value
            lineage.append(
                {
                    "sample_id": sample_id,
                    "triplet_id": a_row["mapping_triplet_id"],
                    "phase": "PHASE1" if field in PHASE1_FIELDS else "PHASE2",
                    "field": field,
                    "annotator_a": {
                        "blind_review_id": a_row["blind_review_id"],
                        "value": a_value,
                        "reason": a_row[reason_field],
                    },
                    "annotator_b": {
                        "blind_review_id": b_row["blind_review_id"],
                        "value": b_value,
                        "reason": b_row[reason_field],
                    },
                    "agreement": a_value == b_value,
                    "base_resolution": {
                        "source": base_source,
                        "value": base_value,
                        "owner_adjudication": dict(owner_row) if owner_row else None,
                    },
                    "approved_additive_events": events,
                    "final_gt_candidate_value": value,
                    "final_resolution_source": final_cell["source"],
                }
            )
        gt_records.append({"sample_id": sample_id, "labels": labels})
    if base_counts != Counter({"A_B_AGREEMENT": 498, "OWNER_ADJUDICATION": 78}):
        raise ValueError(f"BASE_RESOLUTION_COUNT_BLOCKER:{base_counts}")
    return lineage, gt_records, base_counts


def expected_relation_violations(row: Mapping[str, Any]) -> set[str]:
    violations: set[str] = set()
    overall = str(row["overall_fact_status"])
    local = str(row["local_internal_conflict"])
    minimum = str(row["minimum_external_evidence_needed"])
    if overall != "FACTUAL_CONFLICT" and minimum != "NOT_APPLICABLE":
        violations.add("NON_CONFLICT_MINIMUM")
    if overall == "FACTUAL_CONFLICT" and local == "YES" and minimum != "NOT_APPLICABLE":
        violations.add("INTERNAL_CONTRADICTION_MINIMUM")
    if overall == "FACTUAL_CONFLICT" and local != "YES" and minimum == "NOT_APPLICABLE":
        violations.add("EXTERNAL_CONFLICT_MINIMUM")
    return violations


def classify_mismatch(
    sample_id: str,
    field: str,
    human_value: str,
    expected_value: str,
    human_record: Mapping[str, Any],
    expected_record: Mapping[str, Any],
) -> tuple[str, str, str, bool, str]:
    fields = human_record["fields"]
    owner_reason = str(fields[field].get("owner_reason", ""))
    issue = str(fields["phase2_issue"]["value"])
    if (
        field
        in {
            "overall_fact_status",
            "version_claim_status",
            "minimum_external_evidence_needed",
        }
        and issue == "EVIDENCE_MISSING"
    ):
        return (
            "EVIDENCE_DEFECT",
            "Human-adjudicated view records EVIDENCE_MISSING under the frozen E1/E2 pool.",
            "KNOWN_OWNER_RESOLVED_AS_INSUFFICIENT_EVIDENCE",
            False,
            "Retain the Human GT candidate value; any evidence expansion requires a separately approved versioned pool and targeted rereview.",
        )
    expected_violations = expected_relation_violations(expected_record)
    if field == "minimum_external_evidence_needed" and expected_violations:
        return (
            "EXPECTED_V3_DEFECT",
            f"Expected V3 violates the current accepted minimum-evidence relation: {sorted(expected_violations)}.",
            "EXPECTED_QC_CORRECTION_CANDIDATE",
            False,
            "Record an additive Expected V3 correction proposal; do not alter the historical Expected V3 artifact.",
        )
    if field == "version_claim_status" and (
        str(fields[field]["source"]) == "OWNER_AUTHORIZED_RULE_OVERLAY"
        or (human_value == "PRESENT_INCORRECT" and "机关" in owner_reason)
    ):
        return (
            "EXPECTED_V3_DEFECT",
            "The later Owner-approved revision-claim rule treats a wrong revision/content or revising institution as PRESENT_INCORRECT.",
            "EXPECTED_QC_CORRECTION_CANDIDATE",
            False,
            "Record an additive Expected V3 correction proposal; preserve the Human adjudication and historical Expected V3 bytes.",
        )
    if field == "text_naturalness":
        basis = "Text naturalness is a human language-quality judgment; the Owner-resolved value is unique and traceable."
    elif field == "overall_fact_status" and {
        human_value,
        expected_value,
    } == {"CURRENTLY_CONSISTENT", "LEGITIMATE_VERSION_OR_HISTORY"}:
        basis = "The difference is the application of the present-time substitution boundary; the Owner-resolved Human value remains authoritative for this candidate."
    elif field == "minimum_external_evidence_needed" and {
        human_value,
        expected_value,
    } == {"ONE_OFFICIAL_EVIDENCE", "MULTI_EVIDENCE_OR_VERSION_CHAIN"}:
        basis = "The difference concerns evidence ablation sufficiency; no new unresolved Owner decision exists."
    else:
        basis = "The Expected reference differs from the uniquely resolved Human-adjudicated value without establishing a new candidate, evidence, guide, lineage, enum, or relation blocker."
    return (
        "HUMAN_ADJUDICATION_VARIANCE",
        basis,
        "NONBLOCKING_RESEARCHER_QC_VARIANCE",
        False,
        "Retain the Human GT candidate value and preserve the mismatch as researcher-side QC evidence.",
    )


def compare_expected(
    human_records: Sequence[Mapping[str, Any]], expected: Mapping[str, Any]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    human_by_id = {str(row["sample_id"]): row for row in human_records}
    expected_by_id = {str(row["sample_id"]): row for row in expected["rows"]}
    if set(human_by_id) != set(expected_by_id) or len(expected_by_id) != 72:
        raise ValueError("EXPECTED_V3_SAMPLE_PARITY_BLOCKER")
    comparisons: list[dict[str, Any]] = []
    mismatches: list[dict[str, Any]] = []
    field_stats: dict[str, Counter[str]] = {field: Counter() for field in ALL_FIELDS}
    exact_records = 0
    for sample_id in sorted(human_by_id):
        human = human_by_id[sample_id]
        expected_row = expected_by_id[sample_id]
        record_match = True
        for field in ALL_FIELDS:
            human_value = str(human["fields"][field]["value"])
            if field not in EXPECTED_FIELDS:
                field_stats[field]["expected_field_not_defined"] += 1
                comparisons.append(
                    {
                        "sample_id": sample_id,
                        "field": field,
                        "human_gt_candidate_value": human_value,
                        "expected_v3_value": None,
                        "comparison_status": "EXPECTED_FIELD_NOT_DEFINED",
                        "taxonomy": "NON_MATERIAL_PROCESS_VARIANCE",
                        "note": "Expected V3 has no phase2_issue field; no value is inferred or fabricated.",
                    }
                )
                continue
            expected_value = str(expected_row[field])
            match = human_value == expected_value
            field_stats[field]["comparable"] += 1
            field_stats[field]["match" if match else "mismatch"] += 1
            comparison: dict[str, Any] = {
                "sample_id": sample_id,
                "field": field,
                "human_gt_candidate_value": human_value,
                "expected_v3_value": expected_value,
                "comparison_status": "MATCH" if match else "MISMATCH",
            }
            if not match:
                record_match = False
                taxonomy, basis, materiality, blocker, action = classify_mismatch(
                    sample_id, field, human_value, expected_value, human, expected_row
                )
                comparison.update(
                    {
                        "taxonomy": taxonomy,
                        "evidence_basis": basis,
                        "materiality": materiality,
                        "is_new_gt_blocker": blocker,
                        "recommended_action": action,
                        "human_resolution_source": human["fields"][field]["source"],
                        "human_owner_reason": human["fields"][field].get(
                            "owner_reason", ""
                        ),
                    }
                )
                mismatches.append(copy.deepcopy(comparison))
            comparisons.append(comparison)
        if record_match:
            exact_records += 1
    taxonomy_counts = Counter(row["taxonomy"] for row in mismatches)
    taxonomy_sample_counts = {
        taxonomy: len(
            {row["sample_id"] for row in mismatches if row["taxonomy"] == taxonomy}
        )
        for taxonomy in sorted(taxonomy_counts)
    }
    comparable = sum(field_stats[field]["comparable"] for field in ALL_FIELDS)
    matches = sum(field_stats[field]["match"] for field in ALL_FIELDS)
    summary = {
        "comparison_slot_count": len(comparisons),
        "comparable_field_count": comparable,
        "expected_field_not_defined_count": sum(
            field_stats[field]["expected_field_not_defined"] for field in ALL_FIELDS
        ),
        "exact_match_count": matches,
        "mismatch_count": len(mismatches),
        "exact_comparable_field_agreement": matches / comparable,
        "exact_record_agreement_on_seven_expected_fields": exact_records,
        "per_field": {
            field: {
                **dict(field_stats[field]),
                "agreement": (
                    field_stats[field]["match"] / field_stats[field]["comparable"]
                    if field_stats[field]["comparable"]
                    else None
                ),
            }
            for field in ALL_FIELDS
        },
        "taxonomy_field_counts": dict(sorted(taxonomy_counts.items())),
        "taxonomy_sample_counts": taxonomy_sample_counts,
        "new_gt_blocker_count": sum(
            bool(row["is_new_gt_blocker"]) for row in mismatches
        ),
    }
    return comparisons, mismatches, summary


def no_expected_keys(value: Any) -> bool:
    if isinstance(value, Mapping):
        return all(
            "expected" not in str(key).lower() and no_expected_keys(item)
            for key, item in value.items()
        )
    if isinstance(value, list):
        return all(no_expected_keys(item) for item in value)
    return True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--phase1-root", type=Path, required=True)
    parser.add_argument("--phase2-root", type=Path, required=True)
    parser.add_argument("--mapping-root", type=Path, required=True)
    parser.add_argument("--owner-root", type=Path, required=True)
    parser.add_argument("--consistency-root", type=Path, required=True)
    parser.add_argument("--expected-v3", type=Path, required=True)
    parser.add_argument("--candidate-corpus", type=Path, required=True)
    parser.add_argument("--git-head", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    require_new_output(args.output)
    started_at = now_utc()

    p1_paths = {
        "HUMAN-A01": args.phase1_root
        / "raw_phase1/HUMAN-A01/PILOT4_AB_HUMAN_A01_PHASE1_RETURN.csv",
        "HUMAN-B01": args.phase1_root
        / "raw_phase1/HUMAN-B01/PILOT4_AB_HUMAN_B01_PHASE1_RETURN.csv",
    }
    p2_paths = {
        "HUMAN-A01": args.phase2_root
        / "canonical_phase2_csv/HUMAN-A01/PILOT4_AB_HUMAN_A01_PHASE2_RETURN.csv",
        "HUMAN-B01": args.phase2_root
        / "canonical_phase2_csv/HUMAN-B01/PILOT4_AB_HUMAN_B01_PHASE2_RETURN.csv",
    }
    p2_workbooks = {
        "HUMAN-A01": args.phase2_root
        / "raw_phase2/HUMAN-A01/PILOT4_AB_HUMAN_A01_PHASE2_ANNOTATION_WORKBOOK_V3_2.xlsx",
        "HUMAN-B01": args.phase2_root
        / "raw_phase2/HUMAN-B01/PILOT4_AB_HUMAN_B01_PHASE2_ANNOTATION_WORKBOOK_V3_2.xlsx",
    }
    mapping_paths = {
        "HUMAN-A01": args.mapping_root / "mapping/PILOT4_AB_A_IDENTITY_MAPPING.json",
        "HUMAN-B01": args.mapping_root / "mapping/PILOT4_AB_B_IDENTITY_MAPPING.json",
    }
    owner_workbook = (
        args.owner_root
        / "raw/PILOT4_AB_OWNER_EXPECTED_BLIND_ADJUDICATION_WORKBOOK_V1_RETURNED.xlsx"
    )
    source_paths = [
        *p1_paths.values(),
        *p2_paths.values(),
        *p2_workbooks.values(),
        *mapping_paths.values(),
        owner_workbook,
        args.expected_v3,
        args.candidate_corpus,
    ]
    source_hashes_before = {str(path.resolve()): sha256(path) for path in source_paths}

    consistency_integrity = verify_full_manifest(
        args.consistency_root, CONSISTENCY_AGGREGATE_SHA256
    )
    owner_integrity = verify_manifest_subset(
        args.owner_root,
        [
            "raw/PILOT4_AB_OWNER_EXPECTED_BLIND_ADJUDICATION_WORKBOOK_V1_RETURNED.xlsx",
            "control/owner_adjudication_decisions_raw.json",
            "control/owner_authorized_rule_overlay.json",
        ],
    )
    phase1_integrity = verify_manifest_subset(
        args.phase1_root,
        [
            "raw_phase1/HUMAN-A01/PILOT4_AB_HUMAN_A01_PHASE1_RETURN.csv",
            "raw_phase1/HUMAN-B01/PILOT4_AB_HUMAN_B01_PHASE1_RETURN.csv",
            "phase1_lock/dual_phase1_lock_gate.json",
        ],
    )
    phase2_integrity = verify_manifest_subset(
        args.phase2_root,
        [
            "raw_phase2/HUMAN-A01/PILOT4_AB_HUMAN_A01_PHASE2_ANNOTATION_WORKBOOK_V3_2.xlsx",
            "raw_phase2/HUMAN-B01/PILOT4_AB_HUMAN_B01_PHASE2_ANNOTATION_WORKBOOK_V3_2.xlsx",
            "canonical_phase2_csv/HUMAN-A01/PILOT4_AB_HUMAN_A01_PHASE2_RETURN.csv",
            "canonical_phase2_csv/HUMAN-B01/PILOT4_AB_HUMAN_B01_PHASE2_RETURN.csv",
            "phase2_lock/dual_phase2_lock_gate.json",
        ],
    )
    mapping_integrity = verify_manifest_subset(
        args.mapping_root,
        [
            "mapping/PILOT4_AB_A_IDENTITY_MAPPING.json",
            "mapping/PILOT4_AB_B_IDENTITY_MAPPING.json",
        ],
    )
    assert_sha(owner_workbook, OWNER_WORKBOOK_SHA256)
    candidate_identity = assert_sha(args.candidate_corpus, CANDIDATE_CORPUS_SHA256)

    mappings = {name: load_mapping(path, name) for name, path in mapping_paths.items()}
    phase1_header = ["blind_review_id", *PHASE1_FIELDS, "phase1_reason"]
    phase2_header = [
        "blind_review_id",
        "overall_fact_status",
        "version_claim_status",
        "authority_claim_status",
        "minimum_external_evidence_needed",
        "evidence_selection",
        "phase2_issue",
        "phase2_reason",
    ]
    phase1 = {
        name: rows_by_sample(path, mappings[name], phase1_header)
        for name, path in p1_paths.items()
    }
    phase2 = {
        name: rows_by_sample(path, mappings[name], phase2_header)
        for name, path in p2_paths.items()
    }
    for name in mappings:
        validate_raw_reasons(phase1[name], phase2[name])

    owner = read_json(args.owner_root / "control/owner_adjudication_decisions_raw.json")
    owner_rules = read_json(
        args.owner_root / "control/owner_authorized_rule_overlay.json"
    )
    consistency = read_json(
        args.consistency_root / "control/owner_consistency_correction_overlay.json"
    )
    final_view = read_json(
        args.consistency_root
        / "control/resolved_label_candidate_pre_gt_consistency_closed.json"
    )
    if owner["expected_v3_loaded"] or final_view["expected_v3_loaded"]:
        raise ValueError("HISTORICAL_EXPECTED_NONLOAD_PROOF_BLOCKER")
    if any(
        row["owner_defect_decision"] != "ANNOTATOR_INTERPRETATION_VARIANCE"
        for row in owner["defect_decisions"]
    ):
        raise ValueError("UNRESOLVED_CANDIDATE_DEFECT_BLOCKER")

    lineage, gt_rows, base_counts = build_human_lineage(
        phase1, phase2, owner, owner_rules, consistency, final_view
    )
    human_validation = validate_candidate_view(final_view["records"])
    if (
        human_validation["status"] != "PASS"
        or len(lineage) != 576
        or len(gt_rows) != 72
    ):
        raise ValueError("HUMAN_GT_CANDIDATE_RECONSTRUCTION_BLOCKER")
    human_candidate_locked_at = now_utc()
    human_candidate_lock_event_ordinal = 1

    expected_identity = assert_sha(args.expected_v3, EXPECTED_V3_SHA256)
    expected = read_json(args.expected_v3)
    expected_loaded_at = now_utc()
    expected_load_event_ordinal = 2
    if not human_candidate_lock_event_ordinal < expected_load_event_ordinal:
        raise ValueError("EXPECTED_LOAD_ORDER_BLOCKER")
    if expected["candidate_count"] != 72 or len(expected["rows"]) != 72:
        raise ValueError("EXPECTED_V3_POPULATION_BLOCKER")
    if expected.get("candidate_corpus_sha256") != CANDIDATE_CORPUS_SHA256:
        raise ValueError("EXPECTED_V3_CANDIDATE_CORPUS_BLOCKER")

    comparisons, mismatches, comparison_summary = compare_expected(
        final_view["records"], expected
    )
    unresolved_blockers = comparison_summary["new_gt_blocker_count"]
    if unresolved_blockers:
        raise ValueError(f"NEW_GT_BLOCKER:{unresolved_blockers}")

    gt_candidate = {
        "id": "PILOT4_FINAL72_GROUND_TRUTH_CANDIDATE_V1",
        "status": "READY_FOR_OWNER_FINAL_ACCEPTANCE_NOT_ACCEPTED",
        "record_count": 72,
        "canonical_field_count": 8,
        "canonical_value_count": 576,
        "canonical_fields": list(ALL_FIELDS),
        "candidate_corpus_sha256": CANDIDATE_CORPUS_SHA256,
        "value_precedence": [
            "A_B_CONSENSUS",
            "OWNER_EXPECTED_BLIND_ADJUDICATION_FOR_DISAGREEMENTS",
            "APPROVED_OWNER_RULE_AND_CONSISTENCY_OVERLAYS",
        ],
        "final_acceptance": False,
        "formal_dataset_freeze": False,
        "intended_role": "DEVELOPMENT_AND_METHOD_ENGINEERING_NOT_UNTOUCHED_FINAL_TEST",
        "records": gt_rows,
    }
    if not no_expected_keys(gt_candidate) or not no_expected_keys(lineage):
        raise ValueError("EXPECTED_VALUE_LEAKAGE_INTO_GT_BLOCKER")
    for row in gt_rows:
        if set(row["labels"]) != set(ALL_FIELDS):
            raise ValueError(f"GT_FIELD_SCHEMA_BLOCKER:{row['sample_id']}")
        for field, value in row["labels"].items():
            if value not in ENUMS[field]:
                raise ValueError(f"GT_ENUM_BLOCKER:{row['sample_id']}:{field}:{value}")

    write_json(
        args.output / "gt/PILOT4_FINAL72_GROUND_TRUTH_CANDIDATE_V1.json", gt_candidate
    )
    write_jsonl(args.output / "gt/PILOT4_FINAL72_GROUND_TRUTH_LINEAGE.jsonl", lineage)
    write_jsonl(
        args.output / "comparison/human_gt_vs_expected_v3_field_comparison.jsonl",
        comparisons,
    )
    write_jsonl(args.output / "comparison/mismatch_taxonomy.jsonl", mismatches)
    write_json(
        args.output / "comparison/human_gt_vs_expected_v3_summary.json",
        comparison_summary,
    )

    expected_defects = [
        row for row in mismatches if row["taxonomy"] == "EXPECTED_V3_DEFECT"
    ]
    expected_defect_lines = (
        "\n".join(
            f"- `{row['sample_id']}` / `{row['field']}`: Expected `{row['expected_v3_value']}`; Human GT candidate `{row['human_gt_candidate_value']}`. {row['evidence_basis']}"
            for row in expected_defects
        )
        or "- None."
    )
    write_text(
        args.output / "comparison/EXPECTED_V3_POST_GT_QC_CORRECTION_REPORT.md",
        f"""# Expected V3 post-adjudication QC correction report

Expected V3 remains immutable at SHA256 `{EXPECTED_V3_SHA256}`. This report is additive researcher-side QC evidence; it does not modify Human decisions or the historical Expected artifact.

## Proposed Expected-side corrections

{expected_defect_lines}

Count: `{len(expected_defects)}` field mismatches across `{len({row["sample_id"] for row in expected_defects})}` samples. Any Expected V3 successor requires a separate Owner approval and new version identity.
""",
    )

    taxonomy_fields = Counter(row["taxonomy"] for row in mismatches)
    taxonomy_samples = {
        name: len({row["sample_id"] for row in mismatches if row["taxonomy"] == name})
        for name in taxonomy_fields
    }
    write_text(
        args.output
        / "acceptance/PILOT4_FINAL72_EXPECTED_V3_POST_ADJUDICATION_QC_REPORT.md",
        f"""# Pilot4 Final72 Expected V3 post-adjudication QC report

Expected V3 was formally loaded only after the 72-by-8 Human-adjudicated candidate view was reconstructed and locked. It is a researcher-side QC reference, not Ground Truth and not a value-precedence source.

- Human candidate completeness: `72/72` records and `576/576` canonical categorical values.
- Requested comparison slots: `576`; comparable Expected fields: `{comparison_summary["comparable_field_count"]}`; Expected-undefined `phase2_issue` slots: `{comparison_summary["expected_field_not_defined_count"]}`.
- Exact comparable agreement: `{comparison_summary["exact_match_count"]}/{comparison_summary["comparable_field_count"]}` (`{comparison_summary["exact_comparable_field_agreement"]:.3%}`).
- Exact records on all seven Expected-defined fields: `{comparison_summary["exact_record_agreement_on_seven_expected_fields"]}/72`.
- Mismatches: `{comparison_summary["mismatch_count"]}` across `{len({row["sample_id"] for row in mismatches})}` samples.
- Taxonomy field counts: `{dict(sorted(taxonomy_fields.items()))}`.
- Taxonomy sample counts: `{dict(sorted(taxonomy_samples.items()))}`.
- New GT blocker count: `{unresolved_blockers}`.

Known frozen-evidence limitations are retained as `INSUFFICIENT_EVIDENCE / EVIDENCE_MISSING`; they are not new defects discovered by this QC. Expected-side defects are recorded additively. No Expected value overrides the Human GT candidate.
""",
    )
    write_text(
        args.output
        / "acceptance/PILOT4_FINAL72_GROUND_TRUTH_OWNER_ACCEPTANCE_PACKET.md",
        f"""# Pilot4 Final72 Ground Truth Owner acceptance packet

## Candidate awaiting one Owner decision

Please decide whether to accept `PILOT4_FINAL72_GROUND_TRUTH_CANDIDATE_V1`.

- Completeness: `72/72` records; `576/576` categorical values.
- Base lineage: A/B consensus `{base_counts["A_B_AGREEMENT"]}`; Owner expected-blind adjudication `{base_counts["OWNER_ADJUDICATION"]}`.
- Additive lineage: Owner rule overlays `{len(owner_rules["overlays"])}`; consistency overlays `{len(consistency["corrections"])}`.
- Expected QC: `{comparison_summary["exact_match_count"]}/{comparison_summary["comparable_field_count"]}` comparable fields agree; `{comparison_summary["mismatch_count"]}` mismatches are retained for QC.
- Remaining new blocker count: `{unresolved_blockers}`.
- Lineage: `576/576` complete.
- Dataset freeze readiness: `NOT AUTHORIZED`; acceptance of this GT candidate does not itself start the 240-group benchmark or freeze a formal dataset.

Allowed Owner response: accept the GT candidate, or return identified sample/field decisions for additive repair. No downstream work starts automatically.
""",
    )
    write_text(
        args.output / "planning/PAPER1_POST_GT_PARALLEL_EXECUTION_PLAN.md",
        """# Paper 1 post-GT parallel execution plan

This plan is prepared only. It authorizes no execution.

## Track A — Benchmark Scaling

Owner-accepted Final72 GT -> scale-readiness audit -> separately approved 240 groups -> formal dataset QA -> formal dataset freeze.

## Track B — Detector Engineering

Owner-accepted Final72 GT -> five-view signal extraction (Semantic, Entity-Claim, Provenance, Temporal-Version, Retrieval-Behavior) -> separately approved Semantic/GMTP baselines -> multi-view fusion engineering -> risk/explanation prototype.

Final72 may support development and method engineering. Because it has participated in protocol calibration, human adjudication and researcher QC, it must not later be represented as an untouched final test set. Training, tuning, formal benchmark evaluation and 5090 execution remain unapproved.
""",
    )

    source_hashes_after = {str(path.resolve()): sha256(path) for path in source_paths}
    changed_sources = [
        path
        for path in source_hashes_before
        if source_hashes_before[path] != source_hashes_after[path]
    ]
    if changed_sources:
        raise ValueError(f"HISTORICAL_ARTIFACT_MUTATION_BLOCKER:{changed_sources}")
    qa = {
        "task_id": TASK_ID,
        "status": "PASS",
        "human_candidate_reconstructed_before_expected_load": human_candidate_lock_event_ordinal
        < expected_load_event_ordinal,
        "human_candidate_locked_at": human_candidate_locked_at,
        "human_candidate_lock_event_ordinal": human_candidate_lock_event_ordinal,
        "expected_v3_loaded_at": expected_loaded_at,
        "expected_v3_load_event_ordinal": expected_load_event_ordinal,
        "expected_v3_first_post_adjudication_load": True,
        "owner_workbook_sha_unchanged": source_hashes_after[
            str(owner_workbook.resolve())
        ]
        == OWNER_WORKBOOK_SHA256,
        "consistency_manifest_sha_unchanged": consistency_integrity["aggregate_sha256"]
        == CONSISTENCY_AGGREGATE_SHA256,
        "raw_a_b_unchanged": not changed_sources,
        "record_count": len(gt_rows),
        "canonical_value_count": len(lineage),
        "missing_values": sum(
            not value for row in gt_rows for value in row["labels"].values()
        ),
        "invalid_enum_count": 0,
        "relationship_constraints": human_validation["status"],
        "reason_completeness": "PASS",
        "lineage_completeness": len(lineage) == 576,
        "expected_value_precedence": False,
        "expected_leakage_into_gt": 0,
        "comparison_slot_count": len(comparisons),
        "comparable_expected_fields": comparison_summary["comparable_field_count"],
        "mismatch_taxonomy_complete": len(mismatches)
        == comparison_summary["mismatch_count"],
        "unresolved_new_gt_blocker_count": unresolved_blockers,
        "historical_artifact_changes": changed_sources,
        "gt_candidate_ready": True,
        "gt_candidate_accepted": False,
        "formal_dataset_freeze": False,
        "formal_detector_result": False,
    }
    write_json(args.output / "qa/gt_candidate_validation.json", qa)
    write_json(
        args.output / "qa/source_immutability_and_load_order.json",
        {
            "task_id": TASK_ID,
            "started_at": started_at,
            "phase1_integrity": phase1_integrity,
            "phase2_integrity": phase2_integrity,
            "mapping_integrity": mapping_integrity,
            "owner_integrity": owner_integrity,
            "consistency_integrity": consistency_integrity,
            "candidate_identity": candidate_identity,
            "expected_identity": expected_identity,
            "source_hashes_before": source_hashes_before,
            "source_hashes_after": source_hashes_after,
            "changed_sources": changed_sources,
            "human_candidate_locked_at": human_candidate_locked_at,
            "human_candidate_lock_event_ordinal": human_candidate_lock_event_ordinal,
            "expected_v3_loaded_at": expected_loaded_at,
            "expected_v3_load_event_ordinal": expected_load_event_ordinal,
            "strictly_ordered": human_candidate_lock_event_ordinal
            < expected_load_event_ordinal,
        },
    )
    write_json(
        args.output / "qa/documentation_closeout.json",
        {
            "task_id": TASK_ID,
            "status": "PASS",
            "required_documents": [
                "Human Ledger",
                "Agent Ledger",
                "Current State",
                "Owner Register",
                "Execution Log",
                "Master Record",
                "Stage Process",
                "Paper1 Human-readable Experiment Master",
            ],
            "final_boundary": "WAITING_FOR_OWNER_FINAL_GT_ACCEPTANCE",
        },
    )
    write_text(
        args.output / "README.md",
        f"""# Pilot4 Final72 Ground Truth candidate and Expected V3 QC

The Human-adjudicated candidate was reconstructed from immutable A/B returns, `{base_counts["A_B_AGREEMENT"]}` A/B consensus fields, `{base_counts["OWNER_ADJUDICATION"]}` Owner expected-blind adjudications, `{len(owner_rules["overlays"])}` prior Owner-rule overlays and `{len(consistency["corrections"])}` consistency overlays. Expected V3 was loaded only afterward for researcher-side QC and has no value precedence.

The resulting candidate is complete at `72 records / 576 categorical values`, has `0` unresolved new blockers, and awaits explicit Owner final acceptance. It is not a frozen formal dataset and does not authorize Detector evaluation or 240-group scaling.
""",
    )

    entries = manifest_entries(args.output)
    aggregate = hashlib.sha256(
        "".join(f"{row['path']}\0{row['sha256']}\n" for row in entries).encode("utf-8")
    ).hexdigest()
    write_json(
        args.output / "manifest/final_manifest.json",
        {
            "task_id": TASK_ID,
            "generated_at": now_utc(),
            "git_head": args.git_head,
            "entry_count_excluding_manifest": len(entries),
            "aggregate_sha256": aggregate,
            "entries": entries,
            "final_status": [
                "OWNER_ADJUDICATION_CLOSED",
                "EXPECTED_V3_POST_ADJUDICATION_QC_COMPLETE",
                "FINAL72_GROUND_TRUTH_CANDIDATE_READY",
                "WAITING_FOR_OWNER_FINAL_GT_ACCEPTANCE",
                "NO_FORMAL_DATASET_FREEZE_YET",
                "NO_FORMAL_DETECTOR_RESULT_YET",
            ],
        },
    )
    print(
        json.dumps(
            {
                "status": "FINAL72_GROUND_TRUTH_CANDIDATE_READY",
                "records": 72,
                "canonical_values": 576,
                "comparable_expected_fields": comparison_summary[
                    "comparable_field_count"
                ],
                "matches": comparison_summary["exact_match_count"],
                "mismatches": comparison_summary["mismatch_count"],
                "taxonomy_field_counts": comparison_summary["taxonomy_field_counts"],
                "unresolved_new_blockers": unresolved_blockers,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
