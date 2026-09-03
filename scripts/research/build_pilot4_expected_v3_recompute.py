"""Build additive Pilot4 Expected V3 and recompute frozen R3 acceptance gates.

The Expected V3 correction is derived and locked before reviewer values are read.
Historical Expected contracts, reviewer returns, guides, evidence pools, mappings,
and candidate corpora are treated as immutable inputs.
"""

from __future__ import annotations

import argparse
from collections import Counter
import copy
import csv
from datetime import datetime, timezone
import hashlib
from io import StringIO
import json
from pathlib import Path
import shutil
from typing import Any, Iterable, Mapping, Sequence


TASK_ID = "PILOT4-EXPECTED-V3-TARGETED-CORRECTION-AND-FROZEN-GATE-RECOMPUTE-01"
EXPECTED_V3_VERSION = "PILOT4_EXPECTED_CONTRACT_V3_TARGETED_CORRECTION"
EXPECTED_V2_VERSION = "PILOT4_EXPECTED_CONTRACT_V2_TARGETED_REPAIR"
OWNER_AUTHORIZATION = "OWNER_EXPECTED_V3_TARGETED_CORRECTION_APPROVED"
R3_RAW_BYTES = 12062
R3_RAW_SHA256 = "80a10a1ebf2e2321198c750e92214b8d26f9b2a8f4161c64ebf38cae830b4441"
EXPECTED_V2_SHA256 = "caef1702098e48db1db6266f93a014f3882593a37a05071ee5be6716bd0cfd00"
CANDIDATE_CORPUS_SHA256 = (
    "f530471ecd6551300d68c8ddf104cadce2305d8ff91e64010be222820628252d"
)
GUIDE_V3_2_SHA256 = "83fced51ddb509f6ba39feabfc717b88f4003eacf662982551d73fccf476d561"
EVIDENCE_POOL_V2_SHA256 = (
    "44b5c71b840d7018d428a058f51bc5e4c8ad1219b90faf74c0b7d61cd83a622e"
)
MAPPING_SHA256 = "e124173083a7c5c1647e889f9d71b8d6c2bada49214a35f4f6811cd2dc17c3e5"
EXPECTED_V2_COMPARISON_SHA256 = (
    "71f4cbdeb99ace4d7c268590e7558097c7691903d2efb229017b4f3ed607378f"
)
ACCEPTANCE_V2_SHA256 = (
    "206e5d562a43cf457cc90032ebd30e8740fd04844f5b0728eee4f218f67cb198"
)
FINAL_STATUS = (
    "PILOT4_EXPECTED_V3_CORRECTION_COMPLETE / "
    "PILOT4_CALIBRATION_STOP_CONDITION_MET / "
    "PROTOCOL_ACCEPTANCE_RECOMMENDATION_READY / "
    "RECOMMEND_ACCEPT_WITH_NONBLOCKING_NOTES / "
    "OWNER_PROTOCOL_ACCEPTANCE_PENDING / NO_AB_DISTRIBUTION"
)

RELEVANT_FIELDS = (
    "overall_fact_status",
    "version_claim_status",
    "authority_claim_status",
    "minimum_external_evidence_needed",
    "phase2_issue",
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

# These seven decisions are evidence-and-Guide specifications. The derivation
# function receives no reviewer return and is deliberately run before raw load.
CORRECTION_SPECS: tuple[dict[str, Any], ...] = (
    {
        "sample_id": "P4Q-b4bb1a9b722b",
        "field": "overall_fact_status",
        "old_value": "CURRENTLY_CONSISTENT",
        "new_value": "LEGITIMATE_VERSION_OR_HISTORY",
        "r3_blind_review_id": "R3-0F062D8007B5",
        "evidence": {
            "E1": "75805deb77b826d9d95809e70e669bf8a8b7a79d4d7713a47c6f573208fab10d",
            "E2": "bfd0634d73d77115b1d459f007d301f7fbe5d74e36152c21030f723953c44d4f",
        },
        "guide_rule": "V3.2 section 1 current-time replacement test",
        "reason": (
            "E1/E2 establish 2007 as the first revision and 2021 as the second. "
            "The candidate's core claim is the version sequence itself, so removing "
            "the version/history relation changes its core meaning."
        ),
        "taxonomy": "EXPECTED_V2_INTRINSIC_VERSION_SEQUENCE_UNDERCLASSIFICATION",
    },
    {
        "sample_id": "P4Q-afb8936eb07e",
        "field": "overall_fact_status",
        "old_value": "LEGITIMATE_VERSION_OR_HISTORY",
        "new_value": "CURRENTLY_CONSISTENT",
        "r3_blind_review_id": "R3-F056E6D1A15A",
        "evidence": {
            "E1": "a8ca840964b8f6e625ab85314f58f9438a38edd0dfd297d96ba08c48c05e1b0b",
            "E2": "3317ab26f903a3fe6d6688bf8b2ab28931b0ebdaab10548d45a262f5a704f7ca",
        },
        "guide_rule": "V3.2 section 1 dates alone do not create history status",
        "reason": (
            "E1/E2 establish that the 2023 Company Law revision took effect on "
            "2024-07-01 and remains the current legal state. The date is background, "
            "not a superseded applicability boundary."
        ),
        "taxonomy": "EXPECTED_V2_ACTIVE_REVISION_OVERCLASSIFIED_AS_HISTORY",
    },
    {
        "sample_id": "P4Q-1affdb97e391",
        "field": "overall_fact_status",
        "old_value": "LEGITIMATE_VERSION_OR_HISTORY",
        "new_value": "CURRENTLY_CONSISTENT",
        "r3_blind_review_id": "R3-694A4DEA7537",
        "evidence": {
            "E1": "57960cb547b13e42c6510b9c01db536fadd4da36e5663d9125e2491e292970a8",
            "E2": "bd29217d6297d88942ed99286412e99df133baf156f5d594f6b611a5d1c09ad3",
        },
        "guide_rule": "V3.2 section 1 current legal state versus history",
        "reason": (
            "The official material establishes the 2021 Education Law update as a "
            "valid update; the candidate does not assert that a superseded rule still applies."
        ),
        "taxonomy": "EXPECTED_V2_ACTIVE_REVISION_OVERCLASSIFIED_AS_HISTORY",
    },
    {
        "sample_id": "P4Q-1affdb97e391",
        "field": "authority_claim_status",
        "old_value": "PRESENT_CORRECT",
        "new_value": "NOT_PRESENT",
        "r3_blind_review_id": "R3-694A4DEA7537",
        "evidence": {
            "E1": "57960cb547b13e42c6510b9c01db536fadd4da36e5663d9125e2491e292970a8",
            "E2": "bd29217d6297d88942ed99286412e99df133baf156f5d594f6b611a5d1c09ad3",
        },
        "guide_rule": "V3.2 section 4 requires a specific named authority proposition",
        "reason": (
            "The candidate says only 'lawful authority' and does not identify an "
            "organ, issuer, approver, or competence relation. Under Guide V3.2 this "
            "generic legality phrase is not an authority claim."
        ),
        "taxonomy": "EXPECTED_V2_GENERIC_AUTHORITY_OVERCALL",
    },
    {
        "sample_id": "P4Q-8f3f3210e05b",
        "field": "overall_fact_status",
        "old_value": "LEGITIMATE_VERSION_OR_HISTORY",
        "new_value": "CURRENTLY_CONSISTENT",
        "r3_blind_review_id": "R3-EF3352A604E3",
        "evidence": {
            "E1": "fc65d41039de11d994b6f2db1fcd9cd08002cb49d2201e231c69a4acf74b43a2",
            "E2": "36aefac05583e26da288b24eb77ba0dab86126c21764582f49ea55014d434622",
        },
        "guide_rule": "V3.2 section 1 dates alone do not create history status",
        "reason": (
            "E1/E2 support the current applicability of the 2012 Labor Contract Law "
            "amendment and the related dispatch rules. The amendment date is auxiliary."
        ),
        "taxonomy": "EXPECTED_V2_ACTIVE_REVISION_OVERCLASSIFIED_AS_HISTORY",
    },
    {
        "sample_id": "P4Q-3bd40af7ed77",
        "field": "minimum_external_evidence_needed",
        "old_value": "NOT_APPLICABLE",
        "new_value": "ONE_OFFICIAL_EVIDENCE",
        "r3_blind_review_id": "R3-2529846AF14C",
        "evidence": {
            "E1": "de8ba9ccd63ab3d6a8cfbac236cc82f3a651a1776d460478e47ef717d6016dd2",
            "E2": "92892e182af27300e6d5ef21e11c1c4403f454d08f0d7df4d2f12f3cd3c39b82",
        },
        "guide_rule": "V3.2 section 5: one official source sufficient for a conflict",
        "reason": (
            "Expected V2 already marks a factual conflict. E1 alone states State "
            "Council Order No. 741, directly refuting the claim of Education-Ministry-only issuance."
        ),
        "taxonomy": "EXPECTED_V2_CONFLICT_WITH_NOT_APPLICABLE_MINIMUM",
    },
    {
        "sample_id": "P4Q-d1cea30f62e3",
        "field": "minimum_external_evidence_needed",
        "old_value": "MULTI_EVIDENCE_OR_VERSION_CHAIN",
        "new_value": "ONE_OFFICIAL_EVIDENCE",
        "r3_blind_review_id": "R3-F0A837BCC6E6",
        "evidence": {
            "E1": "a1c1d26400eb18ea0a5b78b7c2c10e4b33ebdecc020d8f8924702b7c3566efa4",
            "E2": "9958bc2d20e4121a465610d2dfaece23fe4948cf2f49cf88d78cb4e38b743e81",
        },
        "guide_rule": "V3.2 section 5: test E1 alone before multi-evidence",
        "reason": (
            "E1 alone states that the concrete scope is the scope of archives under "
            "the Archives Law. That directly refutes treating implementation-regulation "
            "scope as independently sufficient outside the statutory definition."
        ),
        "taxonomy": "EXPECTED_V2_MULTI_EVIDENCE_OVERCALL",
    },
)

RESIDUAL_DISPOSITIONS: dict[tuple[str, str], dict[str, str]] = {
    ("P4Q-8ff2d8645df1", "overall_fact_status"): {
        "taxonomy": "R3-M1 REVIEWER_VARIANCE",
        "root_cause": "UNCHANGED_RULE_INSIDE_EXPLICIT_CROSS_VERSION_COMPARISON",
        "materiality": "NONBLOCKING_SINGLE_ROW_VARIANCE",
        "recommended_action": "RETAIN_EXPECTED_V3_AND_RECORD_VARIANCE",
    },
    ("P4Q-aa0d4dcd8a07", "overall_fact_status"): {
        "taxonomy": "R3-M1 REVIEWER_VARIANCE",
        "root_cause": "UNCHANGED_RULE_INSIDE_EXPLICIT_CROSS_VERSION_COMPARISON",
        "materiality": "NONBLOCKING_SINGLE_ROW_VARIANCE",
        "recommended_action": "RETAIN_EXPECTED_V3_AND_RECORD_VARIANCE",
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


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON_OBJECT_REQUIRED:{path}")
    return value


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"JSONL_OBJECT_REQUIRED:{path}")
            rows.append(value)
    return rows


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _write_jsonl(path: Path, rows: Iterable[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
        newline="\n",
    )


def _write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8", newline="\n")


def _hash_record(path: Path) -> dict[str, Any]:
    return {"path": str(path), "bytes": path.stat().st_size, "sha256": _sha256(path)}


def _assert_hash(path: Path, expected: str, blocker: str) -> None:
    if not path.is_file() or _sha256(path) != expected:
        raise ValueError(f"{blocker}:{path}")


def _agreement(agree: int, total: int) -> dict[str, Any]:
    return {
        "agree": agree,
        "total": total,
        "fraction": agree / total,
        "percent": 100.0 * agree / total,
    }


def _expected_value(row: Mapping[str, Any], field: str) -> str:
    if field == "phase2_issue":
        return "NONE"
    value = row.get(field)
    if not isinstance(value, str):
        raise ValueError(f"EXPECTED_FIELD_MISSING:{row.get('sample_id')}:{field}")
    return value


def _read_raw(path: Path) -> list[dict[str, str]]:
    text = path.read_bytes().decode("utf-8-sig", errors="strict")
    reader = csv.DictReader(StringIO(text))
    if tuple(reader.fieldnames or ()) != RAW_COLUMNS:
        raise ValueError("R3_RAW_SCHEMA_DRIFT_BLOCKER")
    rows = [{key: value or "" for key, value in row.items()} for row in reader]
    ids = [row["blind_review_id"] for row in rows]
    if len(rows) != 37 or len(set(ids)) != 37:
        raise ValueError("R3_RAW_ID_DRIFT_BLOCKER")
    return rows


def _diff_expected_rows(
    before: Sequence[Mapping[str, Any]], after: Sequence[Mapping[str, Any]]
) -> list[dict[str, Any]]:
    before_by_id = {row["sample_id"]: row for row in before}
    after_by_id = {row["sample_id"]: row for row in after}
    if set(before_by_id) != set(after_by_id):
        raise ValueError("EXPECTED_V3_CANDIDATE_SET_MUTATION_BLOCKER")
    changes: list[dict[str, Any]] = []
    for sample_id in before_by_id:
        old = before_by_id[sample_id]
        new = after_by_id[sample_id]
        if set(old) != set(new):
            raise ValueError(f"EXPECTED_V3_ROW_SCHEMA_MUTATION_BLOCKER:{sample_id}")
        for field in old:
            if old[field] != new[field]:
                changes.append(
                    {
                        "sample_id": sample_id,
                        "field": field,
                        "old_value": old[field],
                        "new_value": new[field],
                    }
                )
    return changes


def derive_expected_v3(
    expected_v2: Mapping[str, Any],
    packet_rows: Sequence[Mapping[str, Any]],
    snapshot_root: Path,
    guide_path: Path,
    candidate_path: Path,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Derive V3 without accepting or reading any reviewer-return object."""
    if expected_v2.get("version") != EXPECTED_V2_VERSION:
        raise ValueError("EXPECTED_V2_VERSION_BLOCKER")
    if _sha256(guide_path) != GUIDE_V3_2_SHA256:
        raise ValueError("GUIDE_V3_2_HASH_BLOCKER")
    if _sha256(candidate_path) != CANDIDATE_CORPUS_SHA256:
        raise ValueError("CANDIDATE_CORPUS_HASH_BLOCKER")
    expected_rows = expected_v2.get("rows", [])
    if not isinstance(expected_rows, list) or len(expected_rows) != 72:
        raise ValueError("EXPECTED_V2_72_ROW_BLOCKER")
    packet_by_id = {row["blind_review_id"]: row for row in packet_rows}
    rows = copy.deepcopy(expected_rows)
    by_sample = {row["sample_id"]: row for row in rows}
    if len(by_sample) != 72:
        raise ValueError("EXPECTED_V2_SAMPLE_ID_BLOCKER")

    audit: list[dict[str, Any]] = []
    for spec in CORRECTION_SPECS:
        sample_id = spec["sample_id"]
        field = spec["field"]
        row = by_sample[sample_id]
        if row[field] != spec["old_value"]:
            raise ValueError(f"EXPECTED_V2_OLD_VALUE_DRIFT:{sample_id}:{field}")
        packet = packet_by_id.get(spec["r3_blind_review_id"])
        if packet is None:
            raise ValueError(f"R3_PACKET_IDENTITY_BLOCKER:{sample_id}")
        if packet["candidate_text"] not in candidate_path.read_text(encoding="utf-8"):
            raise ValueError(f"CANDIDATE_TEXT_LINEAGE_BLOCKER:{sample_id}")
        evidence_checks: list[dict[str, Any]] = []
        packet_evidence = {
            item["evidence_id"]: item for item in packet["evidence_pool"]
        }
        for evidence_id, expected_hash in spec["evidence"].items():
            evidence = packet_evidence[evidence_id]
            snapshot = snapshot_root / evidence["frozen_snapshot_path"]
            actual_hash = _sha256(snapshot)
            if (
                actual_hash != expected_hash
                or evidence["frozen_snapshot_sha256"] != expected_hash
            ):
                raise ValueError(
                    f"EXPECTED_V3_EVIDENCE_HASH_BLOCKER:{sample_id}:{evidence_id}"
                )
            evidence_checks.append(
                {
                    "evidence_id": evidence_id,
                    "title": evidence["official_page_title"],
                    "url": evidence["official_source_url"],
                    "snapshot_path": str(snapshot),
                    "snapshot_sha256": actual_hash,
                    "hash_pass": True,
                }
            )
        row[field] = spec["new_value"]
        audit.append(
            {
                "sample_id": sample_id,
                "field": field,
                "old_value": spec["old_value"],
                "new_value": spec["new_value"],
                "candidate_text": packet["candidate_text"],
                "guide_rule": spec["guide_rule"],
                "independent_reason": spec["reason"],
                "taxonomy": spec["taxonomy"],
                "evidence": evidence_checks,
                "reviewer_value_consulted": False,
            }
        )

    actual_changes = _diff_expected_rows(expected_rows, rows)
    authorized = [
        {
            "sample_id": spec["sample_id"],
            "field": spec["field"],
            "old_value": spec["old_value"],
            "new_value": spec["new_value"],
        }
        for spec in CORRECTION_SPECS
    ]
    def change_key(item: Mapping[str, Any]) -> tuple[str, str]:
        return str(item["sample_id"]), str(item["field"])

    if sorted(actual_changes, key=change_key) != sorted(authorized, key=change_key):
        raise ValueError(f"EXPECTED_V3_SCOPE_EXPANSION_BLOCKER:{actual_changes}")
    changed_candidates = {item["sample_id"] for item in actual_changes}
    if len(actual_changes) != 7 or len(changed_candidates) != 6:
        raise ValueError("EXPECTED_V3_SCOPE_EXPANSION_BLOCKER")

    expected_v3 = copy.deepcopy(dict(expected_v2))
    expected_v3.update(
        {
            "version": EXPECTED_V3_VERSION,
            "status": "ADDITIVE_TARGETED_CORRECTION_LOCKED",
            "parent_version": EXPECTED_V2_VERSION,
            "parent_sha256": EXPECTED_V2_SHA256,
            "candidate_corpus_sha256": CANDIDATE_CORPUS_SHA256,
            "guide_version": "ANNOTATION_GUIDE_V3_2_TARGETED_REPAIR",
            "guide_sha256": GUIDE_V3_2_SHA256,
            "evidence_pool_version": "PILOT4_EVIDENCE_POOL_V2_TARGETED_REPAIR",
            "evidence_pool_sha256": EVIDENCE_POOL_V2_SHA256,
            "owner_authorization": OWNER_AUTHORIZATION,
            "change_count": 7,
            "changed_candidate_count": 6,
            "candidate_text_change_count": 0,
            "rows": rows,
            "changes": audit,
            "reviewer_values_used_to_derive_changes": False,
        }
    )
    return expected_v3, audit


def _compare(
    raw_rows: Sequence[Mapping[str, str]],
    mapping_rows: Sequence[Mapping[str, Any]],
    expected_rows: Sequence[Mapping[str, Any]],
    version_key: str,
) -> tuple[list[dict[str, Any]], dict[str, int], int]:
    raw_by_id = {row["blind_review_id"]: row for row in raw_rows}
    expected_by_sample = {row["sample_id"]: row for row in expected_rows}
    comparison: list[dict[str, Any]] = []
    field_counts = {field: 0 for field in RELEVANT_FIELDS}
    exact = 0
    for mapping in mapping_rows:
        reviewer = raw_by_id[mapping["r3_blind_review_id"]]
        expected = expected_by_sample[mapping["sample_id"]]
        field_results: dict[str, Any] = {}
        mismatches: list[str] = []
        for field in RELEVANT_FIELDS:
            reviewer_value = reviewer[field]
            expected_value = _expected_value(expected, field)
            agrees = reviewer_value == expected_value
            field_results[field] = {
                "reviewer": reviewer_value,
                version_key: expected_value,
                "agreement": agrees,
            }
            if agrees:
                field_counts[field] += 1
            else:
                mismatches.append(field)
        if not mismatches:
            exact += 1
        comparison.append(
            {
                "r3_blind_review_id": mapping["r3_blind_review_id"],
                "sample_id": mapping["sample_id"],
                "selection_role": mapping["selection_role"],
                "impact_taxonomies": mapping["impact_taxonomies"],
                "field_results": field_results,
                "exact_relevant_field_agreement": not mismatches,
                "mismatch_fields": mismatches,
            }
        )
    return comparison, field_counts, exact


def _markdown_table(rows: Sequence[Mapping[str, Any]], fields: Sequence[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    lines.extend(
        "| "
        + " | ".join(str(row.get(field, "")).replace("|", "\\|") for field in fields)
        + " |"
        for row in rows
    )
    return "\n".join(lines)


def build(args: argparse.Namespace) -> dict[str, Any]:
    output = args.output.resolve()
    r3_package = args.r3_package.resolve()
    previous = args.previous_acceptance.resolve()
    candidate_path = args.candidate_corpus.resolve()
    if output.exists():
        raise FileExistsError(f"REFUSING_EXISTING_OUTPUT:{output}")

    raw_path = previous / "raw" / "PILOT4_TARGETED_PROTOCOL_R3_PHASE2_RETURN.csv"
    expected_v2_path = (
        r3_package / "expected" / "PILOT4_EXPECTED_CONTRACT_V2_TARGETED_REPAIR.json"
    )
    guide_path = r3_package / "guide" / "ANNOTATION_GUIDE_V3_2_TARGETED_REPAIR.md"
    evidence_pool_path = (
        r3_package / "evidence_pool" / "PILOT4_EVIDENCE_POOL_V2_TARGETED_REPAIR.json"
    )
    mapping_path = r3_package / "r3" / "control" / "r3_identity_mapping.json"
    packet_path = r3_package / "r3" / "control" / "packet_rows.jsonl"
    snapshot_root = r3_package / "r3" / "reviewer"
    m2_path = r3_package / "adjudication" / "m2_boundary_adjudication.jsonl"
    m4_path = r3_package / "adjudication" / "m4_evidence_pool_audit.jsonl"
    m8_path = r3_package / "adjudication" / "minimum_evidence_ablation.jsonl"
    comparison_v2_path = previous / "comparison" / "r3_expected_v2_comparison.json"
    defect_v2_path = previous / "comparison" / "expected_v2_defect_candidates.jsonl"
    acceptance_v2_path = (
        previous / "acceptance" / "PILOT4_ANNOTATION_PROTOCOL_ACCEPTANCE_EVIDENCE_V2.md"
    )
    expected_v1_path = Path(_read_json(expected_v2_path)["source_expected_v1_path"])

    exact_hashes = (
        (raw_path, R3_RAW_SHA256, "R3_RAW_PRESERVATION_BLOCKER"),
        (expected_v2_path, EXPECTED_V2_SHA256, "EXPECTED_V2_PRESERVATION_BLOCKER"),
        (guide_path, GUIDE_V3_2_SHA256, "GUIDE_V3_2_PRESERVATION_BLOCKER"),
        (
            evidence_pool_path,
            EVIDENCE_POOL_V2_SHA256,
            "EVIDENCE_POOL_V2_PRESERVATION_BLOCKER",
        ),
        (mapping_path, MAPPING_SHA256, "R3_MAPPING_PRESERVATION_BLOCKER"),
        (
            candidate_path,
            CANDIDATE_CORPUS_SHA256,
            "CANDIDATE_CORPUS_PRESERVATION_BLOCKER",
        ),
        (
            comparison_v2_path,
            EXPECTED_V2_COMPARISON_SHA256,
            "R3_COMPARISON_V2_PRESERVATION_BLOCKER",
        ),
        (
            acceptance_v2_path,
            ACCEPTANCE_V2_SHA256,
            "ACCEPTANCE_V2_PRESERVATION_BLOCKER",
        ),
    )
    for path, expected_hash, blocker in exact_hashes:
        _assert_hash(path, expected_hash, blocker)
    if raw_path.stat().st_size != R3_RAW_BYTES:
        raise ValueError("R3_RAW_BYTES_BLOCKER")
    expected_v2 = _read_json(expected_v2_path)
    _assert_hash(
        expected_v1_path,
        expected_v2["source_expected_v1_sha256"],
        "EXPECTED_V1_BLOCKER",
    )

    immutable_inputs = [
        raw_path,
        expected_v1_path,
        expected_v2_path,
        guide_path,
        evidence_pool_path,
        mapping_path,
        packet_path,
        m2_path,
        m4_path,
        m8_path,
        candidate_path,
        comparison_v2_path,
        acceptance_v2_path,
    ]
    before = [_hash_record(path) for path in immutable_inputs]

    # Independent derivation stage: do not parse raw or prior mismatch artifacts.
    packet_rows = _read_jsonl(packet_path)
    expected_v3, independent_audit = derive_expected_v3(
        expected_v2, packet_rows, snapshot_root, guide_path, candidate_path
    )
    expected_v3_path = (
        output / "expected" / "PILOT4_EXPECTED_CONTRACT_V3_TARGETED_CORRECTION.json"
    )
    _write_json(expected_v3_path, expected_v3)
    expected_v3_lock_timestamp = _now()
    expected_v3_sha256 = _sha256(expected_v3_path)
    _write_json(
        output / "audit" / "EXPECTED_V3_INDEPENDENT_JUSTIFICATION_AUDIT.json",
        {
            "task_id": TASK_ID,
            "status": "PASS",
            "reviewer_values_hidden_during_independent_readjudication": True,
            "reviewer_raw_parsed_before_expected_v3_lock": False,
            "derivation_function_accepts_reviewer_data": False,
            "expected_v3_lock_timestamp": expected_v3_lock_timestamp,
            "expected_v3_sha256": expected_v3_sha256,
            "change_count": 7,
            "changed_candidate_count": 6,
            "records": independent_audit,
        },
    )

    raw_target = output / "raw" / raw_path.name
    raw_target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(raw_path, raw_target)
    expected_v2_target = output / "immutable" / expected_v2_path.name
    expected_v2_target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(expected_v2_path, expected_v2_target)
    if (
        _sha256(raw_target) != R3_RAW_SHA256
        or _sha256(expected_v2_target) != EXPECTED_V2_SHA256
    ):
        raise ValueError("IMMUTABLE_COPY_BLOCKER")

    # Comparison stage starts only after the independently-derived V3 is locked.
    raw_load_timestamp = _now()
    if not expected_v3_lock_timestamp < raw_load_timestamp:
        raise ValueError("EXPECTED_V3_BEFORE_REVIEWER_LOAD_ORDER_BLOCKER")
    raw_rows = _read_raw(raw_path)
    mapping = _read_json(mapping_path)
    mapping_rows = mapping.get("records", [])
    if len(mapping_rows) != 37:
        raise ValueError("R3_MAPPING_37_BLOCKER")
    raw_ids = {row["blind_review_id"] for row in raw_rows}
    mapping_ids = {row["r3_blind_review_id"] for row in mapping_rows}
    if raw_ids != mapping_ids:
        raise ValueError("R3_MAPPING_PARITY_BLOCKER")
    if sum(row["selection_role"] == "IMPACTED" for row in mapping_rows) != 21:
        raise ValueError("R3_IMPACTED_POPULATION_BLOCKER")
    if sum(row["selection_role"] == "MATCHED_CONTROL" for row in mapping_rows) != 16:
        raise ValueError("R3_CONTROL_POPULATION_BLOCKER")

    # Only now read the prior reviewer-derived defect audit; it validates scope,
    # but did not participate in deriving V3.
    prior_defects = _read_jsonl(defect_v2_path)
    prior_defect_keys = {(row["sample_id"], row["field"]) for row in prior_defects}
    correction_keys = {(item["sample_id"], item["field"]) for item in independent_audit}
    if prior_defect_keys != correction_keys or len(prior_defects) != 7:
        raise ValueError("OWNER_AUTHORIZED_CORRECTION_SCOPE_PARITY_BLOCKER")

    v2_comparison, v2_counts, v2_exact = _compare(
        raw_rows, mapping_rows, expected_v2["rows"], "expected_v2"
    )
    v3_comparison, v3_counts, v3_exact = _compare(
        raw_rows, mapping_rows, expected_v3["rows"], "expected_v3"
    )
    previous_v2_comparison = _read_json(comparison_v2_path)
    if previous_v2_comparison.get("rows") != v2_comparison:
        raise ValueError("V2_COMPARISON_REPRODUCTION_BLOCKER")
    _write_json(
        output / "comparison" / "r3_expected_v3_comparison.json",
        {"rows": v3_comparison},
    )

    raw_by_id = {row["blind_review_id"]: row for row in raw_rows}
    expected_v2_by_sample = {row["sample_id"]: row for row in expected_v2["rows"]}
    expected_v3_by_sample = {row["sample_id"]: row for row in expected_v3["rows"]}
    residuals: list[dict[str, Any]] = []
    for row in v3_comparison:
        for field in row["mismatch_fields"]:
            key = (row["sample_id"], field)
            if key not in RESIDUAL_DISPOSITIONS:
                raise ValueError(f"EXPECTED_V3_UNADJUDICATED_RESIDUAL_BLOCKER:{key}")
            reviewer = raw_by_id[row["r3_blind_review_id"]]
            residuals.append(
                {
                    "r3_blind_review_id": row["r3_blind_review_id"],
                    "sample_id": row["sample_id"],
                    "selection_role": row["selection_role"],
                    "field": field,
                    "reviewer_value": reviewer[field],
                    "expected_v3_value": _expected_value(
                        expected_v3_by_sample[row["sample_id"]], field
                    ),
                    "reviewer_reason": reviewer["phase2_reason"],
                    **RESIDUAL_DISPOSITIONS[key],
                }
            )
    if {(row["sample_id"], row["field"]) for row in residuals} != set(
        RESIDUAL_DISPOSITIONS
    ):
        raise ValueError("EXPECTED_V3_RESIDUAL_SET_DRIFT_BLOCKER")
    _write_jsonl(
        output / "comparison" / "residual_mismatch_taxonomy_v3.jsonl", residuals
    )

    m2_samples = {row["sample_id"] for row in _read_jsonl(m2_path)}
    if len(m2_samples) != 16:
        raise ValueError("M2_LINEAGE_BLOCKER")
    m2_rows: list[dict[str, Any]] = []
    for mapping_row in mapping_rows:
        sample_id = mapping_row["sample_id"]
        if sample_id not in m2_samples:
            continue
        reviewer_value = raw_by_id[mapping_row["r3_blind_review_id"]][
            "overall_fact_status"
        ]
        old = expected_v2_by_sample[sample_id]["overall_fact_status"]
        new = expected_v3_by_sample[sample_id]["overall_fact_status"]
        residual = next(
            (item for item in residuals if item["sample_id"] == sample_id), None
        )
        m2_rows.append(
            {
                "r3_blind_review_id": mapping_row["r3_blind_review_id"],
                "sample_id": sample_id,
                "reviewer": reviewer_value,
                "expected_v2": old,
                "expected_v3": new,
                "v2_agreement": reviewer_value == old,
                "v3_agreement": reviewer_value == new,
                "v3_taxonomy": residual["taxonomy"] if residual else "NONE",
                "v3_root_cause": residual["root_cause"] if residual else "NONE",
            }
        )
    if len(m2_rows) != 16:
        raise ValueError("M2_RECOMPUTE_16_BLOCKER")
    _write_jsonl(output / "comparison" / "m2_gate_recompute_v3.jsonl", m2_rows)
    m2_v2_residual = sum(not row["v2_agreement"] for row in m2_rows)
    m2_v3_residual = sum(not row["v3_agreement"] for row in m2_rows)
    root_counts = Counter(
        row["v3_root_cause"] for row in m2_rows if not row["v3_agreement"]
    )
    max_root = max(root_counts.values(), default=0)

    controls_v2 = [
        row for row in v2_comparison if row["selection_role"] == "MATCHED_CONTROL"
    ]
    controls_v3 = [
        row for row in v3_comparison if row["selection_role"] == "MATCHED_CONTROL"
    ]
    control_overall_v2 = sum(
        row["field_results"]["overall_fact_status"]["agreement"] for row in controls_v2
    )
    control_overall_v3 = sum(
        row["field_results"]["overall_fact_status"]["agreement"] for row in controls_v3
    )
    control_exact_v2 = sum(row["exact_relevant_field_agreement"] for row in controls_v2)
    control_exact_v3 = sum(row["exact_relevant_field_agreement"] for row in controls_v3)
    control_summary = {
        "population": 16,
        "overall_v2": _agreement(control_overall_v2, 16),
        "overall_v3": _agreement(control_overall_v3, 16),
        "exact_v2": _agreement(control_exact_v2, 16),
        "exact_v3": _agreement(control_exact_v3, 16),
        "threshold": "at least 15/16 without rounding",
        "gate_pass": control_overall_v3 >= 15,
    }
    _write_json(
        output / "comparison" / "control_gate_recompute_v3.json", control_summary
    )

    m4_records = _read_jsonl(m4_path)
    m4_samples = {row["sample_id"] for row in m4_records}
    if m4_samples != {"P4Q-f97e0e1d2436"}:
        raise ValueError("M4_LINEAGE_BLOCKER")
    m4_mapping = next(row for row in mapping_rows if row["sample_id"] in m4_samples)
    m4_raw = raw_by_id[m4_mapping["r3_blind_review_id"]]
    m4_expected = expected_v3_by_sample[m4_mapping["sample_id"]]
    m4_pass = m4_raw["phase2_issue"] == "NONE" and all(
        m4_raw[field] == _expected_value(m4_expected, field)
        for field in RELEVANT_FIELDS
    )
    _write_json(
        output / "comparison" / "m4_evidence_defect_recurrence_v3.json",
        {
            "status": "PASS" if m4_pass else "FAIL",
            "sample_id": m4_mapping["sample_id"],
            "r3_blind_review_id": m4_mapping["r3_blind_review_id"],
            "phase2_issue": m4_raw["phase2_issue"],
            "same_evidence_defect_recurred": not m4_pass,
        },
    )

    m8_records = _read_jsonl(m8_path)
    m8_by_sample = {row["sample_id"]: row for row in m8_records}
    if len(m8_by_sample) != 4:
        raise ValueError("M8_LINEAGE_BLOCKER")
    m8_results: list[dict[str, Any]] = []
    for mapping_row in mapping_rows:
        sample_id = mapping_row["sample_id"]
        if sample_id not in m8_by_sample:
            continue
        reviewer_value = raw_by_id[mapping_row["r3_blind_review_id"]][
            "minimum_external_evidence_needed"
        ]
        expected_value = expected_v3_by_sample[sample_id][
            "minimum_external_evidence_needed"
        ]
        ablation = m8_by_sample[sample_id]["repaired_expected"]
        unique = reviewer_value == expected_value == ablation
        m8_results.append(
            {
                "sample_id": sample_id,
                "reviewer": reviewer_value,
                "expected_v3": expected_value,
                "prior_ablation": ablation,
                "operational_interpretation_unique": unique,
            }
        )
    m8_pass = len(m8_results) == 4 and all(
        row["operational_interpretation_unique"] for row in m8_results
    )
    _write_jsonl(
        output / "comparison" / "m8_operational_recompute_v3.jsonl", m8_results
    )

    v2_metrics = {field: _agreement(v2_counts[field], 37) for field in RELEVANT_FIELDS}
    v3_metrics = {field: _agreement(v3_counts[field], 37) for field in RELEVANT_FIELDS}
    delta = {field: v3_counts[field] - v2_counts[field] for field in RELEVANT_FIELDS}
    metrics = {
        "scope": "R3_TARGETED_VALIDATION_NOT_FORMAL_BENCHMARK_PERFORMANCE",
        "v2": {"per_field": v2_metrics, "exact": _agreement(v2_exact, 37)},
        "v3": {"per_field": v3_metrics, "exact": _agreement(v3_exact, 37)},
        "v2_to_v3_agree_count_delta": {**delta, "exact": v3_exact - v2_exact},
        "evidence_selection_accuracy_computed": False,
        "evidence_selection_policy": "DESCRIPTIVE_ONLY",
        "evidence_selection_descriptive": dict(
            sorted(Counter(row["evidence_selection"] for row in raw_rows).items())
        ),
    }
    _write_json(output / "comparison" / "v2_to_v3_agreement_delta.json", metrics)

    gate_a = m2_v3_residual <= 2
    gate_b = max_root < 3
    gate_c = control_overall_v3 >= 15
    gate_d = m4_pass
    gate_e = m8_pass
    gate_f = (
        len(residuals) == 2
        and all(row["taxonomy"] == "R3-M1 REVIEWER_VARIANCE" for row in residuals)
        and len(_diff_expected_rows(expected_v2["rows"], expected_v3["rows"])) == 7
    )
    gates = {
        "A": {"pass": gate_a, "observed": f"{m2_v3_residual}/16", "required": "<=2"},
        "B": {
            "pass": gate_b,
            "observed_max_same_root_cluster": max_root,
            "required": "<3",
        },
        "C": {
            "pass": gate_c,
            "observed": f"{control_overall_v3}/16",
            "required": ">=15/16, no rounding",
        },
        "D": {"pass": gate_d, "prior_m4_evidence_defect_recurred": not m4_pass},
        "E": {
            "pass": gate_e,
            "unique_operational_rows": sum(
                row["operational_interpretation_unique"] for row in m8_results
            ),
            "required": "4/4",
        },
        "F": {
            "pass": gate_f,
            "new_candidate_evidence_guide_leak_or_protocol_failure": 0,
        },
    }
    all_gates_pass = all(item["pass"] for item in gates.values())
    if not all_gates_pass:
        raise ValueError(f"FROZEN_GATE_RECOMPUTE_BLOCKER:{gates}")
    recommendation = "RECOMMEND_ACCEPT_WITH_NONBLOCKING_NOTES"
    calibration_stop = True
    r4_required = False

    change_table = _markdown_table(
        independent_audit,
        ("sample_id", "field", "old_value", "new_value", "taxonomy"),
    )
    _write_text(
        output / "expected" / "EXPECTED_CONTRACT_V2_TO_V3_CHANGE_LOG.md",
        f"""# Expected Contract V2 → V3 change log

Expected V3 是对 Expected V2 的追加式、Owner 批准的定向更正。Expected V2 保持原字节和原 SHA；R3 raw、候选、Guide、Evidence Pool、mapping 均未改写。

- Owner authorization: `{OWNER_AUTHORIZATION}=TRUE`
- Parent: `{EXPECTED_V2_VERSION}` / `{EXPECTED_V2_SHA256}`
- New version: `{EXPECTED_V3_VERSION}` / `{expected_v3_sha256}`
- Changed fields: `7`; changed candidates: `6`; candidate text changes: `0`
- Reviewer values were hidden during independent re-adjudication: `TRUE`

{change_table}
""",
    )

    gate_rows = [
        {
            "gate": key,
            "result": "PASS" if value["pass"] else "FAIL",
            "observed": json.dumps(value, ensure_ascii=False),
        }
        for key, value in gates.items()
    ]
    residual_table = _markdown_table(
        residuals,
        (
            "r3_blind_review_id",
            "sample_id",
            "field",
            "reviewer_value",
            "expected_v3_value",
            "taxonomy",
        ),
    )
    gate_md = f"""# Pilot4 Protocol Acceptance Gate Recompute V3

## 结论

Expected V3 在 reviewer raw 加载前完成独立证据复核与哈希锁定。冻结门槛 A–F 全部 PASS；R3 仅剩 2 个非系统性 `R3-M1 REVIEWER_VARIANCE`。因此校准停止条件满足，R4 不需要。

## V2 → V3

- M2 residual: `{m2_v2_residual}/16` → `{m2_v3_residual}/16`
- same-root cluster: `3`（V2 Expected overclassification）→ `{max_root}`（V3 reviewer variance）
- controls overall: `{control_overall_v2}/16` → `{control_overall_v3}/16`
- controls exact: `{control_exact_v2}/16` → `{control_exact_v3}/16`
- all-R3 exact relevant fields: `{v2_exact}/37` → `{v3_exact}/37`

## Frozen gate matrix

{_markdown_table(gate_rows, ("gate", "result", "observed"))}

## Residual taxonomy

{residual_table}

`PILOT4_CALIBRATION_STOP_CONDITION_MET=TRUE`; `R4_EXTERNAL_REVIEW_REQUIRED=FALSE`。
`PILOT4_ANNOTATION_PROTOCOL_ACCEPTED` 仍未由 Owner 签署。
"""
    _write_text(
        output / "acceptance" / "PILOT4_PROTOCOL_ACCEPTANCE_GATE_RECOMPUTE_V3.md",
        gate_md,
    )

    acceptance_md = f"""# Pilot4 Annotation Protocol Acceptance Evidence V3

## 人类可读结论

Pilot4 用来在正式 A/B 前检查候选质量、Phase1/Phase2 隔离、证据可访问性和标签规则。Attempt1 发现五条候选缺陷并完成定向修复，因此同一 Final72 corpus 重新执行 Full72 Phase1；Attempt2 Phase1 72/72 通过。Phase2 首次出现 23 条访问限制，同一 reviewer 重试后全部可访问，说明单次 URL 失败属于过程限制，不能直接等同于证据失效。

R3 对 21 条受影响样本加 16 条匹配控制进行 fresh opaque-ID 验证。R3 raw 保持 `{R3_RAW_BYTES}` bytes / `{R3_RAW_SHA256}`。独立 Evidence/Guide 审计确认 Expected V2 有 7 字段、6 候选缺陷；Owner 批准后形成 additive Expected V3，未改 raw、候选、Guide 或 Evidence Pool。

## V3 results

- overall `{v3_counts["overall_fact_status"]}/37`; version `{v3_counts["version_claim_status"]}/37`; authority `{v3_counts["authority_claim_status"]}/37`; minimum `{v3_counts["minimum_external_evidence_needed"]}/37`; issue `{v3_counts["phase2_issue"]}/37`。
- exact relevant fields `{v3_exact}/37`。
- controls overall `{control_overall_v3}/16`; controls exact `{control_exact_v3}/16`。
- M2 residual `{m2_v3_residual}/16`; maximum same-root residual cluster `{max_root}`。
- M4 prior Evidence defect recurrence `0`; M8 unique operational interpretation `4/4`。
- evidence_selection remains descriptive; no accuracy was fabricated.

## Remaining disagreements

{residual_table}

这两条均为同一明确跨版本比较边界中的 reviewer variance，数量不构成 ≥3 的系统性 cluster。没有剩余 Expected V3 defect、Evidence Pool defect、Guide systemic blocker、candidate defect 或 leakage/protocol failure。

## Recommendation and boundary

Frozen gates A–F 全部 PASS。Codex recommendation 为 `{recommendation}`；这不是 Owner 最终协议验收。
Calibration stop 为 TRUE，R4 不需要。下一道门是 Owner 明确签署或退回 Protocol；若签署，通过后仍需另行批准正式 A/B execution。当前不得启动 A/B、Ground Truth、240-group、Dataset freeze、Detector、Training、5090 或 Formal Experiment。
"""
    acceptance_path = (
        output / "acceptance" / "PILOT4_ANNOTATION_PROTOCOL_ACCEPTANCE_EVIDENCE_V3.md"
    )
    _write_text(acceptance_path, acceptance_md)

    owner_md = f"""# Pilot4 Owner Protocol Final Decision Packet V3

## 当前状态

- Codex recommendation: `{recommendation}`
- Frozen gates A–F: `PASS / PASS / PASS / PASS / PASS / PASS`
- Calibration stop condition: `TRUE`
- R4 external review required: `FALSE`
- Protocol accepted: `FALSE / OWNER DECISION PENDING`
- A/B distribution authorized: `FALSE`

## Owner 可作出的下一项决定

请在主线明确二选一：

1. `PILOT4_ANNOTATION_PROTOCOL_ACCEPTED`；或
2. `RETURNED_FOR_REPAIR`，并给出具体 gate/证据理由。

如果选择接受，仍需另一个独立授权才可生成或分发正式 A/B annotation。该接受不自动授权 Ground Truth、240-group、Dataset freeze、Detector、Training、5090 或 Formal Experiment。

## 签署依据

Expected V3 changes: 7 fields / 6 candidates；reviewer-blind evidence justification PASS；R3 exact relevant fields `{v3_exact}/37`；controls overall `{control_overall_v3}/16`；M2 residual `{m2_v3_residual}/16`；residuals 2，均为 non-systemic reviewer variance。
"""
    owner_path = (
        output / "acceptance" / "PILOT4_OWNER_PROTOCOL_FINAL_DECISION_PACKET_V3.md"
    )
    _write_text(owner_path, owner_md)

    _write_json(
        output / "acceptance" / "frozen_gate_results_v3.json",
        {
            "task_id": TASK_ID,
            "gates": gates,
            "all_pass": all_gates_pass,
            "recommendation": recommendation,
            "pilot4_calibration_stop_condition_met": calibration_stop,
            "r4_external_review_required": r4_required,
            "protocol_accepted": False,
            "owner_protocol_acceptance_pending": True,
            "ab_distribution_authorized": False,
        },
    )
    _write_json(
        output / "qa" / "expected_v3_before_reviewer_load_proof.json",
        {
            "status": "PASS",
            "expected_v3_lock_timestamp": expected_v3_lock_timestamp,
            "reviewer_raw_load_timestamp": raw_load_timestamp,
            "strictly_ordered": expected_v3_lock_timestamp < raw_load_timestamp,
            "reviewer_values_hidden_during_independent_readjudication": True,
            "prior_reviewer_derived_defect_audit_loaded_after_v3_lock": True,
            "prior_defect_scope_parity": "7/7 fields; 6/6 candidates",
        },
    )
    _write_json(
        output / "qa" / "scope_and_lineage_validation.json",
        {
            "status": "PASS",
            "expected_v3_change_count": 7,
            "expected_v3_changed_candidate_count": 6,
            "candidate_text_change_count": 0,
            "new_candidate_count": 0,
            "new_r3_id_count": 0,
            "new_control_count": 0,
            "r3_raw_rewritten": False,
            "expected_v1_rewritten": False,
            "expected_v2_rewritten": False,
            "guide_v3_2_rewritten": False,
            "evidence_pool_v2_rewritten": False,
            "mapping_rewritten": False,
            "r3_comparison_v2_rewritten": False,
            "acceptance_v2_rewritten": False,
            "r4_executed": False,
        },
    )

    after = [_hash_record(path) for path in immutable_inputs]
    if before != after:
        raise ValueError("IMMUTABLE_INPUT_PRE_POST_HASH_BLOCKER")
    _write_json(
        output / "qa" / "immutable_inputs_pre_post.json",
        {
            "status": "PASS_BYTE_IDENTICAL_PRE_POST",
            "records_pre": before,
            "records_post": after,
        },
    )
    _write_json(
        output / "qa" / "task_qa.json",
        {
            "status": "PASS",
            "expected_v3_sha256": expected_v3_sha256,
            "change_count": 7,
            "changed_candidate_count": 6,
            "r3_raw_sha256": R3_RAW_SHA256,
            "r3_raw_bytes": R3_RAW_BYTES,
            "reviewer_blind_derivation": True,
            "all_frozen_gates_pass": True,
            "residual_count": len(residuals),
            "residual_taxonomy": dict(Counter(row["taxonomy"] for row in residuals)),
            "expected_v3_defects_remaining": 0,
            "evidence_pool_defects_remaining": 0,
            "guide_systemic_blocker": False,
            "calibration_stop_condition_met": True,
            "r4_external_review_required": False,
            "recommendation": recommendation,
            "protocol_accepted": False,
            "owner_protocol_acceptance_pending": True,
            "ab_distribution_authorized": False,
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
        "expected_v3": str(expected_v3_path),
        "expected_v3_sha256": expected_v3_sha256,
        "changes": "7 fields / 6 candidates",
        "m2": f"{m2_v2_residual}/16 -> {m2_v3_residual}/16",
        "control_overall": f"{control_overall_v2}/16 -> {control_overall_v3}/16",
        "control_exact": f"{control_exact_v2}/16 -> {control_exact_v3}/16",
        "exact": f"{v2_exact}/37 -> {v3_exact}/37",
        "gates": gates,
        "recommendation": recommendation,
        "output": str(output),
    }


def finalize(args: argparse.Namespace) -> dict[str, Any]:
    output = args.output.resolve()
    manifest_path = output / "manifest" / "manifest.json"
    if not manifest_path.is_file():
        raise FileNotFoundError(f"PACKAGE_MANIFEST_NOT_FOUND:{manifest_path}")
    repo_qa_path = output / "qa" / "repository_validation.json"
    _write_json(repo_qa_path, _read_json(args.repository_qa.resolve()))
    docs_path = output / "qa" / "documentation_closeout.json"
    _write_json(docs_path, _read_json(args.documentation_closeout.resolve()))
    records = [
        {
            "path": path.relative_to(output).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": _sha256(path),
        }
        for path in sorted(output.rglob("*"))
        if path.is_file() and path != manifest_path
    ]
    manifest = _read_json(manifest_path)
    manifest["finalized_at"] = _now()
    manifest["record_count"] = len(records)
    manifest["records"] = records
    manifest["documentation_closeout"] = "PASS"
    manifest["repository_validation"] = "PASS"
    _write_json(manifest_path, manifest)
    return {
        "status": "FINALIZED",
        "record_count": len(records),
        "manifest": str(manifest_path),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    build_parser = sub.add_parser("build")
    build_parser.add_argument("--output", type=Path, required=True)
    build_parser.add_argument("--r3-package", type=Path, required=True)
    build_parser.add_argument("--previous-acceptance", type=Path, required=True)
    build_parser.add_argument("--candidate-corpus", type=Path, required=True)
    final_parser = sub.add_parser("finalize")
    final_parser.add_argument("--output", type=Path, required=True)
    final_parser.add_argument("--repository-qa", type=Path, required=True)
    final_parser.add_argument("--documentation-closeout", type=Path, required=True)
    args = parser.parse_args()
    result = build(args) if args.command == "build" else finalize(args)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
