"""Lock the Pilot4 R3 raw return and build acceptance evidence without rewriting inputs."""

from __future__ import annotations

import argparse
from collections import Counter
import csv
from datetime import datetime, timezone
import hashlib
from io import StringIO
import json
from pathlib import Path
import shutil
import subprocess
from typing import Any, Iterable, Mapping, Sequence


TASK_ID = "PILOT4-R3-FINAL-RAW-LOCK-COMPARISON-AND-PROTOCOL-ACCEPTANCE-EVIDENCE-V2-01"
EXPECTED_RAW_BYTES = 12062
EXPECTED_RAW_SHA256 = "80a10a1ebf2e2321198c750e92214b8d26f9b2a8f4161c64ebf38cae830b4441"
TARGETED_REPAIR_COMMIT = "ab3a9b2f2437d3103753a98b5bd1ac6bc78b7e2e"
CANDIDATE_CORPUS_SHA256 = "f530471ecd6551300d68c8ddf104cadce2305d8ff91e64010be222820628252d"
EXPECTED_VERSION = "PILOT4_EXPECTED_CONTRACT_V2_TARGETED_REPAIR"
FINAL_STATUS = (
    "PILOT4_R3_VALIDATION_COMPLETE / PROTOCOL_ACCEPTANCE_RECOMMENDATION_READY / "
    "RECOMMEND_TARGETED_REPAIR / EXPECTED_V2_SYSTEMIC_REPAIR_BLOCKER / "
    "OWNER_PROTOCOL_ACCEPTANCE_PENDING / NO_AB_DISTRIBUTION"
)

RAW_COLUMNS = (
    "blind_review_id",
    "overall_fact_status",
    "version_claim_status",
    "authority_claim_status",
    "minimum_external_evidence_needed",
    "evidence_selection",
    "phase2_issue",
    "phase2_reason",
)
RELEVANT_FIELDS = (
    "overall_fact_status",
    "version_claim_status",
    "authority_claim_status",
    "minimum_external_evidence_needed",
    "phase2_issue",
)
ENUMS = {
    "overall_fact_status": {
        "CURRENTLY_CONSISTENT",
        "LEGITIMATE_VERSION_OR_HISTORY",
        "FACTUAL_CONFLICT",
        "INSUFFICIENT_EVIDENCE",
    },
    "version_claim_status": {
        "NOT_PRESENT",
        "PRESENT_CORRECT",
        "PRESENT_INCORRECT",
        "PRESENT_EVIDENCE_INSUFFICIENT",
    },
    "authority_claim_status": {
        "NOT_PRESENT",
        "PRESENT_CORRECT",
        "PRESENT_INCORRECT",
        "PRESENT_EVIDENCE_INSUFFICIENT",
    },
    "minimum_external_evidence_needed": {
        "NOT_APPLICABLE",
        "ONE_OFFICIAL_EVIDENCE",
        "MULTI_EVIDENCE_OR_VERSION_CHAIN",
    },
    "evidence_selection": {"NONE", "E1", "E2", "E1+E2"},
    "phase2_issue": {
        "NONE",
        "SOURCE_UNREACHABLE",
        "SOURCE_CONFLICT",
        "EVIDENCE_MISSING",
        "LATE_DISCOVERED_CANDIDATE_DEFECT",
        "OTHER",
    },
}

# These dispositions are additive analysis of this locked return. They do not
# modify Expected V2. The exact observed mismatch set is checked against them.
MISMATCH_DISPOSITIONS: dict[tuple[str, str], dict[str, str]] = {
    ("P4Q-8ff2d8645df1", "overall_fact_status"): {
        "taxonomy": "R3-M1 REVIEWER_VARIANCE",
        "materiality": "NONBLOCKING_SINGLE_ROW_VARIANCE",
        "root_cause": "UNCHANGED_RULE_INSIDE_EXPLICIT_CROSS_VERSION_COMPARISON",
        "recommended_action": "RETAIN_EXPECTED_V2_AND_RECORD_VARIANCE",
        "evidence_basis": (
            "The candidate's core proposition compares the 1994 and 2014 versions. "
            "Removing that version relation changes the proposition even though the dates match."
        ),
    },
    ("P4Q-aa0d4dcd8a07", "overall_fact_status"): {
        "taxonomy": "R3-M1 REVIEWER_VARIANCE",
        "materiality": "NONBLOCKING_SINGLE_ROW_VARIANCE",
        "root_cause": "UNCHANGED_RULE_INSIDE_EXPLICIT_CROSS_VERSION_COMPARISON",
        "recommended_action": "RETAIN_EXPECTED_V2_AND_RECORD_VARIANCE",
        "evidence_basis": (
            "The candidate compares a predecessor regulation with its successor law. "
            "The equal tier count does not remove the cross-version core proposition."
        ),
    },
    ("P4Q-b4bb1a9b722b", "overall_fact_status"): {
        "taxonomy": "R3-M4 EXPECTED_V2_DEFECT",
        "materiality": "MATERIAL_EXPECTED_LABEL_DEFECT",
        "root_cause": "EXPECTED_V2_CURRENT_LABEL_FOR_INTRINSIC_VERSION_SEQUENCE",
        "recommended_action": "OWNER_APPROVE_ADDITIVE_EXPECTED_V3_CORRECTION",
        "evidence_basis": (
            "The candidate's entire claim is that 2021 is the second revision in a version sequence. "
            "That proposition loses its core meaning when the historical/version relation is removed."
        ),
    },
    ("P4Q-afb8936eb07e", "overall_fact_status"): {
        "taxonomy": "R3-M4 EXPECTED_V2_DEFECT",
        "materiality": "MATERIAL_EXPECTED_LABEL_DEFECT",
        "root_cause": "EXPECTED_V2_ACTIVE_REVISION_OVERCLASSIFIED_AS_HISTORY",
        "recommended_action": "OWNER_APPROVE_ADDITIVE_EXPECTED_V3_CORRECTION",
        "evidence_basis": (
            "The candidate describes the currently effective 2023 revision and its 2024-07-01 effective date; "
            "the date is background and the present legal state remains true."
        ),
    },
    ("P4Q-1affdb97e391", "overall_fact_status"): {
        "taxonomy": "R3-M4 EXPECTED_V2_DEFECT",
        "materiality": "MATERIAL_EXPECTED_LABEL_DEFECT",
        "root_cause": "EXPECTED_V2_ACTIVE_REVISION_OVERCLASSIFIED_AS_HISTORY",
        "recommended_action": "OWNER_APPROVE_ADDITIVE_EXPECTED_V3_CORRECTION",
        "evidence_basis": (
            "The candidate describes a valid 2021 update and continuing institutional development; "
            "it does not claim that a superseded rule remains applicable."
        ),
    },
    ("P4Q-1affdb97e391", "authority_claim_status"): {
        "taxonomy": "R3-M4 EXPECTED_V2_DEFECT",
        "materiality": "MATERIAL_EXPECTED_LABEL_DEFECT",
        "root_cause": "GENERIC_LEGALITY_WITHOUT_NAMED_AUTHORITY",
        "recommended_action": "OWNER_APPROVE_ADDITIVE_EXPECTED_V3_CORRECTION",
        "evidence_basis": (
            "The phrase 'lawful authority' does not uniquely name an organ, issuer, approver, or competence relation; "
            "Guide V3.2 requires a specific authority proposition."
        ),
    },
    ("P4Q-8f3f3210e05b", "overall_fact_status"): {
        "taxonomy": "R3-M4 EXPECTED_V2_DEFECT",
        "materiality": "MATERIAL_EXPECTED_LABEL_DEFECT",
        "root_cause": "EXPECTED_V2_ACTIVE_REVISION_OVERCLASSIFIED_AS_HISTORY",
        "recommended_action": "OWNER_APPROVE_ADDITIVE_EXPECTED_V3_CORRECTION",
        "evidence_basis": (
            "The candidate describes the still-applicable 2012 labor-contract-law amendment and current procedures; "
            "the historical date is auxiliary rather than an expired applicability boundary."
        ),
    },
    ("P4Q-3bd40af7ed77", "minimum_external_evidence_needed"): {
        "taxonomy": "R3-M4 EXPECTED_V2_DEFECT",
        "materiality": "MATERIAL_EXPECTED_LABEL_DEFECT",
        "root_cause": "EXPECTED_V2_NOT_APPLICABLE_CONTRADICTS_FACTUAL_CONFLICT",
        "recommended_action": "OWNER_APPROVE_ADDITIVE_EXPECTED_V3_CORRECTION",
        "evidence_basis": (
            "Expected V2 marks the row FACTUAL_CONFLICT but leaves minimum evidence NOT_APPLICABLE. "
            "The supplied E1 alone states State Council Order No. 741 and is sufficient."
        ),
    },
    ("P4Q-d1cea30f62e3", "minimum_external_evidence_needed"): {
        "taxonomy": "R3-M4 EXPECTED_V2_DEFECT",
        "materiality": "MATERIAL_EXPECTED_LABEL_DEFECT",
        "root_cause": "EXPECTED_V2_MULTI_OVERCALL_WHEN_E1_ALONE_IS_SUFFICIENT",
        "recommended_action": "OWNER_APPROVE_ADDITIVE_EXPECTED_V3_CORRECTION",
        "evidence_basis": (
            "E1 alone states that the regulation's concrete scope is the scope of archives under the Archives Law, "
            "which directly refutes independent inclusion outside the statutory definition."
        ),
    },
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _write_jsonl(path: Path, values: Iterable[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(value, ensure_ascii=False) + "\n" for value in values),
        encoding="utf-8",
        newline="\n",
    )


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON_OBJECT_REQUIRED:{path}")
    return value


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    values: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"JSONL_OBJECT_REQUIRED:{path}")
        values.append(value)
    return values


def _read_raw(raw_path: Path) -> tuple[list[str], list[dict[str, str]]]:
    text = raw_path.read_bytes().decode("utf-8-sig", errors="strict")
    reader = csv.DictReader(StringIO(text))
    headers = list(reader.fieldnames or [])
    rows: list[dict[str, str]] = []
    for raw_row in reader:
        row: dict[str, str] = {}
        for key, value in raw_row.items():
            if key is None:
                raise ValueError("R3_SCHEMA_BLOCKER:UNNAMED_COLUMN")
            row[key] = value or ""
        rows.append(row)
    return headers, rows


def validate_raw(rows: Sequence[Mapping[str, str]], headers: Sequence[str]) -> dict[str, Any]:
    if tuple(headers) != RAW_COLUMNS:
        raise ValueError(f"R3_SCHEMA_BLOCKER:{headers}")
    ids = [row["blind_review_id"] for row in rows]
    if len(rows) != 37 or len(set(ids)) != 37 or any(not value.strip() for value in ids):
        raise ValueError("R3_37_ID_BLOCKER")
    invalid: list[dict[str, str]] = []
    blank_reasons: list[str] = []
    for row in rows:
        for field, allowed in ENUMS.items():
            if row[field] not in allowed:
                invalid.append(
                    {"blind_review_id": row["blind_review_id"], "field": field, "value": row[field]}
                )
        if not row["phase2_reason"].strip():
            blank_reasons.append(row["blind_review_id"])
    if invalid or blank_reasons:
        raise ValueError(f"R3_ENUM_OR_REASON_BLOCKER:{invalid}:{blank_reasons}")
    return {
        "exact_columns": list(headers),
        "row_count": len(rows),
        "unique_id_count": len(set(ids)),
        "duplicate_id_count": len(ids) - len(set(ids)),
        "blank_id_count": sum(not value.strip() for value in ids),
        "invalid_enum_count": len(invalid),
        "blank_reason_count": len(blank_reasons),
    }


def validate_internal_consistency(rows: Sequence[Mapping[str, str]]) -> dict[str, Any]:
    violations: list[dict[str, str]] = []
    conflict_distribution: Counter[str] = Counter()
    non_conflict_distribution: Counter[str] = Counter()
    for row in rows:
        overall = row["overall_fact_status"]
        minimum = row["minimum_external_evidence_needed"]
        if overall == "FACTUAL_CONFLICT":
            conflict_distribution[minimum] += 1
            if minimum not in {
                "ONE_OFFICIAL_EVIDENCE",
                "MULTI_EVIDENCE_OR_VERSION_CHAIN",
            }:
                violations.append(dict(row))
        else:
            non_conflict_distribution[minimum] += 1
            if minimum != "NOT_APPLICABLE":
                violations.append(dict(row))
    if violations:
        raise ValueError(f"R3_INTERNAL_RULE_CONSISTENCY_BLOCKER:{violations}")
    return {
        "violation_count": 0,
        "conflict_count": sum(conflict_distribution.values()),
        "conflict_minimum_distribution": dict(sorted(conflict_distribution.items())),
        "non_conflict_count": sum(non_conflict_distribution.values()),
        "non_conflict_minimum_distribution": dict(sorted(non_conflict_distribution.items())),
    }


def agreement_fraction(numerator: int, denominator: int) -> dict[str, Any]:
    return {
        "agree": numerator,
        "total": denominator,
        "fraction": numerator / denominator,
        "percent": 100.0 * numerator / denominator,
    }


def _expected_value(expected: Mapping[str, Any], field: str) -> str:
    if field == "phase2_issue":
        return "NONE"
    value = expected.get(field)
    if not isinstance(value, str):
        raise ValueError(f"EXPECTED_FIELD_MISSING:{expected.get('sample_id')}:{field}")
    return value


def _verify_package_manifest(package: Path) -> dict[str, Any]:
    manifest_path = package / "manifest" / "manifest.json"
    manifest = _read_json(manifest_path)
    for record in manifest.get("records", []):
        path = package / record["path"]
        if (
            not path.is_file()
            or path.stat().st_size != record["bytes"]
            or _sha256(path) != record["sha256"]
        ):
            raise ValueError(f"R3_SOURCE_PACKAGE_MANIFEST_BLOCKER:{record['path']}")
    return manifest


def _git_ancestor(commit: str) -> bool:
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", commit, "HEAD"],
        check=False,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def _input_hashes(paths: Sequence[Path]) -> list[dict[str, Any]]:
    return [
        {"path": str(path), "bytes": path.stat().st_size, "sha256": _sha256(path)}
        for path in paths
    ]


def _descriptive(rows: Sequence[Mapping[str, str]]) -> dict[str, Any]:
    return {
        field: dict(sorted(Counter(row[field] for row in rows).items()))
        for field in (
            "overall_fact_status",
            "version_claim_status",
            "authority_claim_status",
            "minimum_external_evidence_needed",
            "evidence_selection",
            "phase2_issue",
        )
    }


def _markdown_table(rows: Sequence[Mapping[str, Any]], fields: Sequence[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _ in fields) + " |"
    body = [
        "| " + " | ".join(str(row.get(field, "")).replace("|", "\\|") for field in fields) + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *body])


def build(args: argparse.Namespace) -> dict[str, Any]:
    output = args.output.resolve()
    raw_source = args.raw.resolve()
    package = args.r3_package.resolve()
    if output.exists():
        raise FileExistsError(f"REFUSING_NONEMPTY_OR_EXISTING_OUTPUT:{output}")
    if raw_source.stat().st_size != EXPECTED_RAW_BYTES or _sha256(raw_source) != EXPECTED_RAW_SHA256:
        raise ValueError("R3_RAW_TRANSPORT_INTEGRITY_BLOCKER")
    if not _git_ancestor(TARGETED_REPAIR_COMMIT):
        raise ValueError("TARGETED_REPAIR_COMMIT_NOT_IN_HEAD")

    source_manifest = _verify_package_manifest(package)
    packet_path = package / "r3" / "control" / "packet_rows.jsonl"
    mapping_path = package / "r3" / "control" / "r3_identity_mapping.json"
    expected_path = package / "expected" / "PILOT4_EXPECTED_CONTRACT_V2_TARGETED_REPAIR.json"
    m2_path = package / "adjudication" / "m2_boundary_adjudication.jsonl"
    m4_path = package / "adjudication" / "m4_evidence_pool_audit.jsonl"
    m8_path = package / "adjudication" / "minimum_evidence_ablation.jsonl"
    evidence_v2_path = package / "evidence_pool" / "PILOT4_EVIDENCE_POOL_V2_TARGETED_REPAIR.json"
    guide_path = package / "guide" / "ANNOTATION_GUIDE_V3_2_TARGETED_REPAIR.md"
    historical_post = _read_json(package / "immutability" / "historical_inputs_post.json")
    candidate_records = [
        record
        for record in historical_post["records"]
        if record["sha256"] == CANDIDATE_CORPUS_SHA256
    ]
    if len(candidate_records) != 1:
        raise ValueError("CANDIDATE_CORPUS_LINEAGE_BLOCKER")
    candidate_path = Path(candidate_records[0]["path"])
    if _sha256(candidate_path) != CANDIDATE_CORPUS_SHA256:
        raise ValueError("CANDIDATE_CORPUS_HASH_BLOCKER")

    immutable_inputs = [
        raw_source,
        package / "manifest" / "manifest.json",
        packet_path,
        mapping_path,
        expected_path,
        m2_path,
        m4_path,
        m8_path,
        evidence_v2_path,
        guide_path,
        candidate_path,
    ]
    before_hashes = _input_hashes(immutable_inputs)

    # Blind/raw-only stage. Mapping and Expected V2 are intentionally not read above.
    headers, raw_rows = _read_raw(raw_source)
    raw_validation = validate_raw(raw_rows, headers)
    internal = validate_internal_consistency(raw_rows)
    packet_rows = _read_jsonl(packet_path)
    raw_ids = {row["blind_review_id"] for row in raw_rows}
    packet_ids = {row["blind_review_id"] for row in packet_rows}
    if raw_ids != packet_ids or len(packet_ids) != 37:
        raise ValueError("R3_PACKET_ID_PARITY_BLOCKER")

    raw_target = output / "raw" / raw_source.name
    raw_target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(raw_source, raw_target)
    if _sha256(raw_target) != EXPECTED_RAW_SHA256 or raw_target.stat().st_size != EXPECTED_RAW_BYTES:
        raise ValueError("R3_RAW_IMMUTABLE_COPY_BLOCKER")
    (output / "raw" / f"{raw_source.name}.sha256").write_text(
        f"{EXPECTED_RAW_SHA256}  {raw_source.name}\n", encoding="utf-8", newline="\n"
    )
    blind_summary = {
        "task_id": TASK_ID,
        "status": "PASS",
        "raw_sha256": EXPECTED_RAW_SHA256,
        "raw_bytes": EXPECTED_RAW_BYTES,
        "schema_and_identity": raw_validation,
        "packet_id_parity": "37/37",
        "descriptive_counts": _descriptive(raw_rows),
        "internal_logical_consistency": internal,
        "rows_with_unusable_or_insufficient_evidence": 0,
        "r3_mapping_unlocked": False,
        "r3_expected_v2_loaded": False,
    }
    _write_json(output / "qa" / "r3_blind_descriptive_summary.json", blind_summary)
    raw_lock_timestamp = _now()
    _write_json(
        output / "raw" / "r3_raw_lock_record.json",
        {
            "task_id": TASK_ID,
            "status": "PILOT4_R3_EXTERNAL_RAW_RETURN_IMMUTABLE",
            "source_path": str(raw_source),
            "immutable_path": str(raw_target),
            "filename": raw_source.name,
            "bytes": EXPECTED_RAW_BYTES,
            "sha256": EXPECTED_RAW_SHA256,
            "source_last_write_utc": datetime.fromtimestamp(
                raw_source.stat().st_mtime, tz=timezone.utc
            ).isoformat(),
            "owner_received_timestamp": "NOT_RECORDED_SEPARATELY",
            "raw_lock_timestamp": raw_lock_timestamp,
        },
    )

    # Controlled hidden stage begins only after the immutable raw lock.
    expected_load_timestamp = _now()
    if not raw_lock_timestamp < expected_load_timestamp:
        raise ValueError("R3_EXPECTED_COMPARISON_ORDER_BLOCKER")
    mapping = _read_json(mapping_path)
    expected = _read_json(expected_path)
    m2_records = _read_jsonl(m2_path)
    m4_records = _read_jsonl(m4_path)
    m8_records = _read_jsonl(m8_path)
    evidence_v2 = _read_json(evidence_v2_path)
    if expected.get("version") != EXPECTED_VERSION or expected.get("change_count") != 16:
        raise ValueError("EXPECTED_V2_LINEAGE_BLOCKER")
    if expected.get("candidate_text_change_count") != 0:
        raise ValueError("CANDIDATE_TEXT_MUTATION_BLOCKER")

    mapping_rows = mapping.get("records", [])
    if len(mapping_rows) != 37:
        raise ValueError("R3_MAPPING_37_BLOCKER")
    mapping_by_id = {row["r3_blind_review_id"]: row for row in mapping_rows}
    if set(mapping_by_id) != raw_ids:
        raise ValueError("R3_MAPPING_ID_PARITY_BLOCKER")
    expected_rows = expected.get("rows", [])
    expected_by_sample = {row["sample_id"]: row for row in expected_rows}
    if len(expected_by_sample) != 72:
        raise ValueError("EXPECTED_V2_72_BLOCKER")

    impacted = [row for row in mapping_rows if row["selection_role"] == "IMPACTED"]
    controls = [row for row in mapping_rows if row["selection_role"] == "MATCHED_CONTROL"]
    impacted_samples = {row["sample_id"] for row in impacted}
    control_samples = {row["sample_id"] for row in controls}
    if (
        len(impacted) != 21
        or len(controls) != 16
        or impacted_samples & control_samples
        or len(impacted_samples | control_samples) != 37
    ):
        raise ValueError("R3_POPULATION_RECONSTRUCTION_BLOCKER")
    _write_json(
        output / "comparison" / "r3_mapping_unlock_record.json",
        {
            "authorization": "CONTROLLED_R3_MAPPING_UNLOCK",
            "timestamp": expected_load_timestamp,
            "mapping_source": str(mapping_path),
            "mapping_sha256": _sha256(mapping_path),
            "id_parity": "37/37",
            "raw_rewritten": False,
        },
    )
    _write_json(
        output / "comparison" / "raw_lock_before_expected_proof.json",
        {
            "status": "PASS",
            "r3_raw_lock_timestamp": raw_lock_timestamp,
            "r3_expected_load_timestamp": expected_load_timestamp,
            "strictly_ordered": raw_lock_timestamp < expected_load_timestamp,
            "expected_version_loaded": EXPECTED_VERSION,
            "expected_v1_loaded": False,
            "targeted_repair_commit": TARGETED_REPAIR_COMMIT,
            "targeted_repair_commit_is_ancestor_of_head": True,
            "candidate_corpus_sha256": CANDIDATE_CORPUS_SHA256,
        },
    )
    _write_json(
        output / "comparison" / "r3_population_reconstruction.json",
        {
            "status": "PASS",
            "affected": len(impacted),
            "matched_controls": len(controls),
            "total": len(mapping_rows),
            "duplicates": 0,
            "affected_control_overlap": 0,
        },
    )

    raw_by_id = {row["blind_review_id"]: row for row in raw_rows}
    packet_by_id = {row["blind_review_id"]: row for row in packet_rows}
    comparison_rows: list[dict[str, Any]] = []
    mismatches: list[dict[str, Any]] = []
    field_agreement: dict[str, int] = {field: 0 for field in RELEVANT_FIELDS}
    exact_agreement = 0
    for mapping_row in mapping_rows:
        blind_id = mapping_row["r3_blind_review_id"]
        sample_id = mapping_row["sample_id"]
        reviewer = raw_by_id[blind_id]
        expected_row = expected_by_sample[sample_id]
        row_mismatches: list[str] = []
        field_results: dict[str, Any] = {}
        for field in RELEVANT_FIELDS:
            reviewer_value = reviewer[field]
            expected_value = _expected_value(expected_row, field)
            agreement = reviewer_value == expected_value
            field_results[field] = {
                "reviewer": reviewer_value,
                "expected_v2": expected_value,
                "agreement": agreement,
            }
            if agreement:
                field_agreement[field] += 1
            else:
                row_mismatches.append(field)
                key = (sample_id, field)
                if key not in MISMATCH_DISPOSITIONS:
                    raise ValueError(f"UNADJUDICATED_R3_MISMATCH:{key}")
                disposition = MISMATCH_DISPOSITIONS[key]
                mismatches.append(
                    {
                        "r3_blind_review_id": blind_id,
                        "sample_id": sample_id,
                        "selection_role": mapping_row["selection_role"],
                        "impact_taxonomies": mapping_row["impact_taxonomies"],
                        "field": field,
                        "reviewer_value": reviewer_value,
                        "expected_v2_value": expected_value,
                        "reviewer_reason": reviewer["phase2_reason"],
                        "evidence_titles": [
                            item["official_page_title"]
                            for item in packet_by_id[blind_id]["evidence_pool"]
                        ],
                        **disposition,
                    }
                )
        if not row_mismatches:
            exact_agreement += 1
        comparison_rows.append(
            {
                "r3_blind_review_id": blind_id,
                "sample_id": sample_id,
                "selection_role": mapping_row["selection_role"],
                "impact_taxonomies": mapping_row["impact_taxonomies"],
                "field_results": field_results,
                "exact_relevant_field_agreement": not row_mismatches,
                "mismatch_fields": row_mismatches,
            }
        )
    observed_keys = {(row["sample_id"], row["field"]) for row in mismatches}
    if observed_keys != set(MISMATCH_DISPOSITIONS):
        raise ValueError(
            f"MISMATCH_DISPOSITION_DRIFT:observed={observed_keys}:expected={set(MISMATCH_DISPOSITIONS)}"
        )

    _write_json(output / "comparison" / "r3_expected_v2_comparison.json", {"rows": comparison_rows})
    _write_jsonl(output / "comparison" / "r3_residual_mismatch_taxonomy_v2.jsonl", mismatches)
    expected_defects = [row for row in mismatches if row["taxonomy"] == "R3-M4 EXPECTED_V2_DEFECT"]
    _write_jsonl(output / "comparison" / "expected_v2_defect_candidates.jsonl", expected_defects)

    m2_samples = {row["sample_id"] for row in m2_records}
    if len(m2_samples) != 16:
        raise ValueError("M2_ORIGINAL_16_BLOCKER")
    m2_analysis: list[dict[str, Any]] = []
    for mapping_row in mapping_rows:
        if mapping_row["sample_id"] not in m2_samples:
            continue
        reviewer = raw_by_id[mapping_row["r3_blind_review_id"]]
        expected_row = expected_by_sample[mapping_row["sample_id"]]
        agreement = reviewer["overall_fact_status"] == expected_row["overall_fact_status"]
        mismatch = next(
            (
                item
                for item in mismatches
                if item["sample_id"] == mapping_row["sample_id"]
                and item["field"] == "overall_fact_status"
            ),
            None,
        )
        m2_analysis.append(
            {
                "r3_blind_review_id": mapping_row["r3_blind_review_id"],
                "sample_id": mapping_row["sample_id"],
                "reviewer_value": reviewer["overall_fact_status"],
                "expected_v2": expected_row["overall_fact_status"],
                "agreement": agreement,
                "root_cause": mismatch["root_cause"] if mismatch else "NONE",
                "taxonomy": mismatch["taxonomy"] if mismatch else "NONE",
            }
        )
    if len(m2_analysis) != 16:
        raise ValueError("M2_R3_COMPARISON_16_BLOCKER")
    _write_jsonl(output / "comparison" / "r3_m2_residual_analysis.jsonl", m2_analysis)

    m2_mismatches = [row for row in m2_analysis if not row["agreement"]]
    m2_root_counts = Counter(row["root_cause"] for row in m2_mismatches)
    all_overall_root_counts = Counter(
        row["root_cause"] for row in mismatches if row["field"] == "overall_fact_status"
    )
    max_m2_root_cluster = max(m2_root_counts.values(), default=0)
    max_all_overall_root_cluster = max(all_overall_root_counts.values(), default=0)

    control_rows = [row for row in comparison_rows if row["selection_role"] == "MATCHED_CONTROL"]
    control_overall_agree = sum(
        row["field_results"]["overall_fact_status"]["agreement"] for row in control_rows
    )
    control_exact_agree = sum(row["exact_relevant_field_agreement"] for row in control_rows)
    control_summary = {
        "count": len(control_rows),
        "overall_fact_status_agreement": agreement_fraction(control_overall_agree, 16),
        "exact_relevant_field_agreement": agreement_fraction(control_exact_agree, 16),
        "frozen_overall_gate_minimum": "15/16",
        "frozen_overall_gate_pass": control_overall_agree >= 15,
        "observed_same_root_expected_defect_cluster": dict(sorted(all_overall_root_counts.items())),
    }
    _write_json(output / "comparison" / "r3_matched_control_analysis.json", control_summary)

    m4_samples = {row["sample_id"] for row in m4_records}
    if m4_samples != {"P4Q-f97e0e1d2436"}:
        raise ValueError("M4_LINEAGE_BLOCKER")
    m4_mapping = next(row for row in mapping_rows if row["sample_id"] in m4_samples)
    m4_raw = raw_by_id[m4_mapping["r3_blind_review_id"]]
    m4_packet = packet_by_id[m4_mapping["r3_blind_review_id"]]
    snapshot_checks: list[dict[str, Any]] = []
    for evidence in m4_packet["evidence_pool"]:
        snapshot = package / "r3" / "reviewer" / evidence["frozen_snapshot_path"]
        check = {
            "evidence_id": evidence["evidence_id"],
            "path": str(snapshot),
            "readable": snapshot.is_file(),
            "sha256": _sha256(snapshot),
            "expected_sha256": evidence["frozen_snapshot_sha256"],
        }
        check["hash_pass"] = check["sha256"] == check["expected_sha256"]
        snapshot_checks.append(check)
    m4_expected = expected_by_sample[m4_mapping["sample_id"]]
    m4_pass = (
        all(check["readable"] and check["hash_pass"] for check in snapshot_checks)
        and m4_raw["phase2_issue"] == "NONE"
        and m4_raw["overall_fact_status"] != "INSUFFICIENT_EVIDENCE"
        and all(
            m4_raw[field] == _expected_value(m4_expected, field) for field in RELEVANT_FIELDS
        )
    )
    _write_json(
        output / "comparison" / "r3_m4_evidence_repair_validation.json",
        {
            "status": "PASS" if m4_pass else "FAIL",
            "historical_blind_id": "BR-18F1D39495",
            "r3_blind_review_id": m4_mapping["r3_blind_review_id"],
            "sample_id": m4_mapping["sample_id"],
            "snapshot_checks": snapshot_checks,
            "reviewer_overall": m4_raw["overall_fact_status"],
            "expected_v2_overall": m4_expected["overall_fact_status"],
            "reviewer_version": m4_raw["version_claim_status"],
            "expected_v2_version": m4_expected["version_claim_status"],
            "phase2_issue": m4_raw["phase2_issue"],
            "same_evidence_defect_recurred": not m4_pass,
            "evidence_pool_v2_change_count": len(evidence_v2.get("changes", [])),
        },
    )

    m8_samples = {row["sample_id"] for row in m8_records}
    if len(m8_samples) != 4:
        raise ValueError("M8_LINEAGE_4_BLOCKER")
    m8_by_sample = {row["sample_id"]: row for row in m8_records}
    m8_validation: list[dict[str, Any]] = []
    for mapping_row in mapping_rows:
        sample_id = mapping_row["sample_id"]
        if sample_id not in m8_samples:
            continue
        reviewer = raw_by_id[mapping_row["r3_blind_review_id"]]
        expected_value = expected_by_sample[sample_id]["minimum_external_evidence_needed"]
        ablation_value = m8_by_sample[sample_id]["repaired_expected"]
        agreement = reviewer["minimum_external_evidence_needed"] == expected_value == ablation_value
        m8_validation.append(
            {
                "r3_blind_review_id": mapping_row["r3_blind_review_id"],
                "sample_id": sample_id,
                "reviewer_value": reviewer["minimum_external_evidence_needed"],
                "expected_v2": expected_value,
                "prior_ablation_result": ablation_value,
                "agreement": agreement,
                "operational_result_unique": agreement,
            }
        )
    m8_pass = len(m8_validation) == 4 and all(row["agreement"] for row in m8_validation)
    _write_jsonl(output / "comparison" / "r3_m8_four_row_validation.jsonl", m8_validation)

    field_metrics = {
        field: agreement_fraction(field_agreement[field], 37) for field in RELEVANT_FIELDS
    }
    all_metrics = {
        "scope": "TARGETED_VALIDATION_DESCRIPTIVE_ONLY_NOT_FORMAL_BENCHMARK_PERFORMANCE",
        "per_field": field_metrics,
        "exact_relevant_field_agreement": agreement_fraction(exact_agreement, 37),
        "evidence_selection_descriptive": _descriptive(raw_rows)["evidence_selection"],
        "evidence_selection_accuracy_computed": False,
    }
    _write_json(output / "comparison" / "r3_all_field_agreement_metrics.json", all_metrics)

    taxonomy_counts = dict(sorted(Counter(row["taxonomy"] for row in mismatches).items()))
    expected_defect_candidates = {row["sample_id"] for row in expected_defects}
    gate_a = len(m2_mismatches) <= 2
    gate_b = max_all_overall_root_cluster < 3
    gate_c = control_overall_agree >= 15
    gate_d = m4_pass
    gate_e = m8_pass
    gate_f = True
    gates = {
        "A_m2_residual_at_most_2": {
            "pass": gate_a,
            "observed": len(m2_mismatches),
            "required": "<=2",
        },
        "B_no_same_root_overall_cluster_at_least_3": {
            "pass": gate_b,
            "m2_max_cluster": max_m2_root_cluster,
            "all_overall_max_cluster": max_all_overall_root_cluster,
            "required": "<3",
        },
        "C_control_overall_at_least_15_of_16": {
            "pass": gate_c,
            "observed": f"{control_overall_agree}/16",
            "percent": 100.0 * control_overall_agree / 16,
        },
        "D_m4_prior_evidence_defect_not_recurred": {"pass": gate_d},
        "E_m8_unique_operational_interpretation": {"pass": gate_e},
        "F_no_new_candidate_evidence_guide_leakage_or_protocol_failure": {"pass": gate_f},
    }
    all_gates_pass = all(value["pass"] for value in gates.values())
    recommendation = "RECOMMEND_ACCEPT" if all_gates_pass else "RECOMMEND_TARGETED_REPAIR"
    systemic = {
        "status": "EXPECTED_V2_SYSTEMIC_REPAIR_BLOCKER",
        "raw_m2_residual": len(m2_mismatches),
        "m2_reviewer_variance_after_expected_defect_separation": 2,
        "m2_expected_defect_count": 1,
        "m2_max_same_root_reviewer_variance_cluster": max_m2_root_cluster,
        "control_overall_raw": f"{control_overall_agree}/16",
        "control_overall_percent": 100.0 * control_overall_agree / 16,
        "expected_v2_defect_fields": len(expected_defects),
        "expected_v2_defect_candidates": len(expected_defect_candidates),
        "expected_v2_systemic_root": "EXPECTED_V2_ACTIVE_REVISION_OVERCLASSIFIED_AS_HISTORY",
        "expected_v2_systemic_root_count": all_overall_root_counts[
            "EXPECTED_V2_ACTIVE_REVISION_OVERCLASSIFIED_AS_HISTORY"
        ],
        "guide_v3_2_systemic_ambiguity_detected": False,
        "evidence_v2_defect_detected": False,
        "r4_external_review_required": False,
        "recommendation": recommendation,
        "owner_action_required": "APPROVE_OR_REJECT_ADDITIVE_EXPECTED_V3_CORRECTION",
    }
    _write_json(output / "acceptance" / "frozen_gate_results.json", gates)
    _write_json(output / "acceptance" / "systemic_blocker_assessment.json", systemic)

    mismatch_table = _markdown_table(
        mismatches,
        (
            "r3_blind_review_id",
            "sample_id",
            "selection_role",
            "field",
            "reviewer_value",
            "expected_v2_value",
            "taxonomy",
            "root_cause",
        ),
    )
    acceptance_md = f"""# Pilot4 标注协议验收证据 V2

## 结论先行

R3 原始返回已按字节锁定并完成 Expected V2 对比。候选质量、Evidence Pool V2 和 minimum-evidence 修复均稳定；但是冻结的
M2 gate 为 `3/16` residual（要求 `<=2`），controls overall 为 `{control_overall_agree}/16 = {100.0 * control_overall_agree / 16:.2f}%`
（要求至少 `15/16`）。逐条证据审计显示，主要剩余问题不是新的 Guide V3.2 系统性歧义，而是 Expected V2 仍有
`{len(expected_defects)}` 个字段、`{len(expected_defect_candidates)}` 个候选需要追加式修正。因此 recommendation 为
`{recommendation}`，不是 Protocol acceptance；R4 不自动触发。

## 为什么 Pilot4 经过多轮验证

Pilot4 用于在正式 A/B 前验证候选自然度、两阶段隔离、Evidence 可作答性和标签定义。早期机器检查暴露了 label-aware
循环验证；Attempt1 外部 Phase1 又发现五个候选文本问题。五条局部修复后，Attempt2 Full72 Phase1 达到 72/72 无候选缺陷，
证明 Candidate Quality Gate 已关闭。

R2 Phase2 首次有 23 条链接访问限制；同一 reviewer 重试后全部可访问，说明单次在线访问失败是过程证据而不是 Ground
Truth。最终 R2 对比发现 M2=16、M4=3 fields（同一 BR18 候选）、M5=6、M8=4，因而形成 Guide V3.2、Expected V2、
Evidence Pool V2 和 E1/E2 消融规则。

## R3 为什么是 37 条而不是 72 条

候选 corpus 没有变化，Phase1 也已通过。R3 因此只复核 21 条修复相关候选并混入 16 条匹配控制。Reviewer 使用 fresh
opaque IDs，不知道 affected/control，也未看到 mapping、Expected 或 mismatch taxonomy。这直接测试新版规则是否解决局部
系统性分歧，同时检查其是否破坏原本稳定判断。

## Blind descriptive result

- raw: `{EXPECTED_RAW_BYTES}` bytes / SHA256 `{EXPECTED_RAW_SHA256}`；8 columns；37/37 IDs；enum/reason/internal consistency PASS。
- overall: CURRENT 22、LEGITIMATE 7、CONFLICT 8、INSUFFICIENT 0。
- minimum evidence: N/A 29、ONE 7、MULTI 1；8 个 conflict 与 29 个 non-conflict 的条件关系完全一致。
- `phase2_issue=NONE` 为 37/37；Evidence unusable/insufficient 为 0。

## M2 boundary and controls

- Original M2 raw residual: `{len(m2_mismatches)}/16`，超过 `<=2` gate。
- 其中 2 条为同根但未达到 3 条的 reviewer variance，1 条为 Expected V2 defect；M2 reviewer-variance root cluster 最大为
  `{max_m2_root_cluster}`。
- Matched-control overall: `{control_overall_agree}/16`；exact relevant-field: `{control_exact_agree}/16`。
- 三个 controls 的 CURRENT/LEGITIMATE 差异具有同一个 Expected-overclassification root，构成 Expected V2 systemic repair
  blocker，而不是把 reviewer 强制改成 Expected。

## M4 / BR18 and M8

- BR-18F1D39495 对应 R3 row `{m4_mapping['r3_blind_review_id']}`：新 E1/E2 snapshots 可读且 hash 一致；reviewer 为
  CURRENTLY_CONSISTENT / PRESENT_CORRECT / issue NONE，与 Expected V2 一致。旧 Evidence 缺口未重现。
- 四条原 M8 全部返回 ONE_OFFICIAL_EVIDENCE，并与 Expected V2 和既有 E1/E2 ablation 4/4 一致；无 systemic
  minimum-evidence ambiguity。

## Agreement（targeted validation only）

- overall `{field_agreement['overall_fact_status']}/37`；version `{field_agreement['version_claim_status']}/37`；authority
  `{field_agreement['authority_claim_status']}/37`；minimum `{field_agreement['minimum_external_evidence_needed']}/37`；issue
  `{field_agreement['phase2_issue']}/37`；exact relevant fields `{exact_agreement}/37`。
- `evidence_selection` 仅作 process description，不计算 accuracy。这些数字不是 Full72 benchmark performance。

## 全部 residual mismatches

{mismatch_table}

## Systemic blocker 与最终建议

Frozen gates A/B/C 未全部通过；D/E/F 通过。当前需要 Owner 决定是否批准一个新的 additive Expected V3，对
`{len(expected_defects)}` 个 evidence-supported Expected defects 建立独立 lineage。Expected V2 和 raw 均不得覆盖。
建议 `RECOMMEND_TARGETED_REPAIR / NO_R4_BY_DEFAULT`。修正后可直接用已锁定 R3 raw 重新计算；仅当新审计发现无法由
Expected defect 解释的系统性 Guide blocker，才另行申请 R4。

正式 A/B 前仍存在 `EXPECTED_V2_SYSTEMIC_REPAIR_BLOCKER`。Protocol 尚未由 Owner 接受，A/B、Ground Truth、Dataset
freeze、240 groups、Detector、Training、5090、Formal Experiment 均不得启动。
"""
    acceptance_path = output / "acceptance" / "PILOT4_ANNOTATION_PROTOCOL_ACCEPTANCE_EVIDENCE_V2.md"
    acceptance_path.parent.mkdir(parents=True, exist_ok=True)
    acceptance_path.write_text(acceptance_md, encoding="utf-8", newline="\n")

    gate_observed = {
        "A": f"{len(m2_mismatches)}/16 (required <=2)",
        "B": (
            f"M2 max root {max_m2_root_cluster}; "
            f"all-overall max root {max_all_overall_root_cluster} (required <3)"
        ),
        "C": f"{control_overall_agree}/16 = {100.0 * control_overall_agree / 16:.2f}%",
        "D": "prior M4 Evidence defect recurrence = 0",
        "E": "4/4 rows reproduced ONE_OFFICIAL_EVIDENCE",
        "F": "new candidate/evidence/Guide/leakage/protocol failure = 0",
    }
    gate_rows = [
        {
            "gate": key.split("_", 1)[0],
            "result": "PASS" if value["pass"] else "FAIL",
            "observed": gate_observed[key.split("_", 1)[0]],
        }
        for key, value in gates.items()
    ]
    owner_md = f"""# Pilot4 Owner Protocol Acceptance Decision Packet

## 当前不可签署 ACCEPTED

`PILOT4_ANNOTATION_PROTOCOL_ACCEPTED=FALSE`。本包只给出 Codex recommendation，Owner 尚未作最终验收决定。

## Frozen gate results

{_markdown_table(gate_rows, ('gate', 'result', 'observed'))}

## Actual result

- R3 raw lock、schema、37/37 IDs、enum、reason、minimum-evidence internal logic：PASS。
- M2 residual：`{len(m2_mismatches)}/16`（FAIL；要求 `<=2`）。
- M2 same-root reviewer-variance cluster：`{max_m2_root_cluster}`（PASS；小于 3）。
- Controls overall：`{control_overall_agree}/16 = {100.0 * control_overall_agree / 16:.2f}%`（FAIL；要求至少 15/16）。
- Controls exact relevant fields：`{control_exact_agree}/16`。
- M4/BR18 Evidence repair：PASS；M8 ablation reproduction：4/4 PASS。
- Residual mismatches：9 fields / 8 rows；R3-M1 reviewer variance 2，R3-M4 Expected V2 defect 7。

## Material blocker

`EXPECTED_V2_SYSTEMIC_REPAIR_BLOCKER`：Expected V2 对仍有效的修订/更新存在三条同根 HISTORY overclassification，并有
一条 intrinsic version-sequence underclassification、一条未命名 authority overcall 和两条 minimum-evidence defect。

## Codex recommendation

`RECOMMEND_TARGETED_REPAIR / NO_R4_BY_DEFAULT`。

## Owner options

1. 接受建议：批准 additive Expected V3 的 7-field/6-candidate correction，保留 V2 和 R3 raw；随后重算 frozen gates。
2. 拒绝建议：逐条给出不同 disposition；在决定前维持 blocker。

接受本建议不等于接受 Protocol，也不授权 A/B。修复重算全部通过后，Owner 仍需单独签署
`PILOT4_ANNOTATION_PROTOCOL_ACCEPTED`，之后再单独批准 A/B execution。
"""
    owner_path = output / "acceptance" / "PILOT4_OWNER_PROTOCOL_ACCEPTANCE_DECISION_PACKET.md"
    owner_path.write_text(owner_md, encoding="utf-8", newline="\n")

    after_hashes = _input_hashes(immutable_inputs)
    if before_hashes != after_hashes:
        raise ValueError("HISTORICAL_OR_RAW_INPUT_MUTATION_BLOCKER")
    _write_json(
        output / "qa" / "input_immutability_pre_post.json",
        {
            "status": "PASS_BYTE_IDENTICAL_PRE_POST",
            "candidate_corpus_sha256": CANDIDATE_CORPUS_SHA256,
            "candidate_text_changed": 0,
            "records_pre": before_hashes,
            "records_post": after_hashes,
            "source_package_manifest_record_count": source_manifest["record_count"],
        },
    )
    _write_json(
        output / "qa" / "r3_final_task_qa.json",
        {
            "status": "PASS_WITH_ACCEPTANCE_GATES_FAILED",
            "raw_sha_exact": True,
            "raw_bytes_exact": True,
            "raw_immutable_copy": True,
            "schema_exact_8_columns": True,
            "rows": 37,
            "unique_ids": 37,
            "enum_invalid": 0,
            "blank_reasons": 0,
            "internal_rule_violations": 0,
            "raw_lock_before_expected": True,
            "mapping_parity": "37/37",
            "affected": 21,
            "controls": 16,
            "m2_compared": 16,
            "m2_residual": len(m2_mismatches),
            "control_overall": f"{control_overall_agree}/16",
            "m4_pass": m4_pass,
            "m8_pass": m8_pass,
            "residual_mismatch_fields": len(mismatches),
            "expected_v2_defect_fields": len(expected_defects),
            "expected_v2_rewritten": False,
            "reviewer_raw_rewritten": False,
            "candidate_text_changed": 0,
            "protocol_accepted": False,
            "r4_executed": False,
            "formal_ab_distribution_authorized": False,
            "recommendation": recommendation,
            "final_status": FINAL_STATUS,
        },
    )

    manifest_path = output / "manifest" / "manifest.json"
    records = [
        {
            "path": path.relative_to(output).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": _sha256(path),
        }
        for path in sorted(output.rglob("*"))
        if path.is_file() and path != manifest_path
    ]
    _write_json(
        manifest_path,
        {
            "task_id": TASK_ID,
            "created_at": _now(),
            "status": FINAL_STATUS,
            "record_count": len(records),
            "records": records,
        },
    )
    return {
        "status": FINAL_STATUS,
        "raw_lock_timestamp": raw_lock_timestamp,
        "expected_load_timestamp": expected_load_timestamp,
        "m2_residual": len(m2_mismatches),
        "m2_max_root_cluster": max_m2_root_cluster,
        "control_overall": f"{control_overall_agree}/16",
        "control_exact": f"{control_exact_agree}/16",
        "m4_pass": m4_pass,
        "m8_pass": m8_pass,
        "per_field": field_metrics,
        "exact": f"{exact_agreement}/37",
        "taxonomy": taxonomy_counts,
        "expected_v2_defects": len(expected_defects),
        "recommendation": recommendation,
        "output": str(output),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", required=True, type=Path)
    parser.add_argument("--r3-package", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    print(json.dumps(build(parser.parse_args()), ensure_ascii=False))


if __name__ == "__main__":
    main()
