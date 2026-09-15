from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

from scripts.research.ingest_pilot4_owner_adjudication_return import (
    ALL_FIELDS,
    ENUMS,
    manifest_entries,
    sha256,
    write_json,
    write_text,
)


TASK_ID = "PILOT4-A-B-OWNER-ADJUDICATION-CONSISTENCY-CLOSURE-01"
OWNER_WORKBOOK_SHA256 = (
    "a4c65a22dd3a410c7744be5f256206d7217b8fda33d63c58ac99bb386fe95b01"
)
PRIOR_PACKAGE_AGGREGATE_SHA256 = (
    "9e561b3a30308654fe4eec58250dee7d20f4474aa0ea68138bac60b45f42625b"
)
OWNER_LINEAGE = "OWNER_CONFIRMATION_2026-09-15_CONSISTENCY_VERIFICATION_ITEMS_1_TO_5"


def now_utc() -> str:
    return datetime.now(UTC).isoformat(timespec="microseconds").replace("+00:00", "Z")


def require_new_output(path: Path) -> None:
    if path.exists() and any(path.iterdir()):
        raise ValueError(f"OUTPUT_NAMESPACE_NOT_EMPTY:{path}")
    path.mkdir(parents=True, exist_ok=True)


def verify_manifest(root: Path) -> dict[str, Any]:
    manifest_path = root / "manifest/final_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest["aggregate_sha256"] != PRIOR_PACKAGE_AGGREGATE_SHA256:
        raise ValueError("PRIOR_PACKAGE_AGGREGATE_BLOCKER")
    mismatches: list[str] = []
    for entry in manifest["entries"]:
        path = root / entry["path"]
        if (
            not path.is_file()
            or path.stat().st_size != entry["bytes"]
            or sha256(path) != entry["sha256"]
        ):
            mismatches.append(entry["path"])
    if mismatches:
        raise ValueError(f"PRIOR_PACKAGE_MANIFEST_BLOCKER:{mismatches}")
    return {
        "status": "PASS",
        "manifest_path": str(manifest_path.resolve()),
        "entry_count": len(manifest["entries"]),
        "aggregate_sha256": manifest["aggregate_sha256"],
        "mismatches": mismatches,
    }


def correction_specs() -> list[dict[str, Any]]:
    minimum_reason = (
        "Owner confirms that minimum_external_evidence_needed applies only when "
        "overall_fact_status is FACTUAL_CONFLICT; this sample is not a factual conflict."
    )
    minimum_evidence = (
        "Accepted Guide relation: minimum_external_evidence_needed is substantive only "
        "for FACTUAL_CONFLICT; Owner confirmation item 1."
    )
    specs: list[dict[str, Any]] = []
    for index, sample_id in enumerate(
        (
            "P4Q-097a559a5f61",
            "P4Q-281af2c34dcb",
            "P4Q-3ed81a10fec6",
            "P4Q-8f3f3210e05b",
        ),
        start=1,
    ):
        specs.append(
            {
                "correction_id": f"P4-OCC-{index:03d}",
                "source_finding_ids": [index],
                "sample_id": sample_id,
                "field": "minimum_external_evidence_needed",
                "after": "NOT_APPLICABLE",
                "reason": minimum_reason,
                "evidence_basis": minimum_evidence,
                "owner_decision_lineage": OWNER_LINEAGE,
            }
        )
    specs.extend(
        [
            {
                "correction_id": "P4-OCC-005",
                "source_finding_ids": [5],
                "sample_id": "P4Q-f27d8deeb5a7",
                "field": "phase2_issue",
                "after": "NONE",
                "reason": (
                    "E2 Article 72 directly supports the personal-or-family-affairs exception; "
                    "the second sentence is a summary of that exception and does not create an "
                    "independent evidence requirement."
                ),
                "evidence_basis": (
                    "Frozen E2, Personal Information Protection Law of the People's Republic "
                    "of China, Article 72: natural-person processing for personal or family "
                    "affairs is outside the law's application. Owner confirmation item 2."
                ),
                "owner_decision_lineage": OWNER_LINEAGE,
            },
            {
                "correction_id": "P4-OCC-006",
                "source_finding_ids": [9],
                "sample_id": "P4Q-097a559a5f61",
                "field": "version_claim_status",
                "after": "PRESENT_CORRECT",
                "reason": "仅通过 E1 即可判断该版本/修订命题。",
                "evidence_basis": (
                    "Frozen E1, Securities Law of the People's Republic of China (2019 "
                    "revision), directly records adoption of the revision on 2019-12-28; "
                    "E3 in the raw Owner reason was a writing error. Owner confirmation item 3."
                ),
                "owner_decision_lineage": OWNER_LINEAGE,
            },
            {
                "correction_id": "P4-OCC-007",
                "source_finding_ids": [7],
                "sample_id": "P4Q-02a9af3fa54f",
                "field": "overall_fact_status",
                "after": "INSUFFICIENT_EVIDENCE",
                "reason": (
                    "Frozen E1/E2 do not establish the degree-count provisions of the prior "
                    "Academic Degrees Regulations, so the cross-version comparison cannot be "
                    "resolved within the frozen packet."
                ),
                "evidence_basis": (
                    "FROZEN_PACKET_ONLY / EXPECTED_BLIND; E1 is the Academic Degrees Law and "
                    "E2 is What is a degree? No new E3 is introduced. Owner confirmation item 4."
                ),
                "owner_decision_lineage": OWNER_LINEAGE,
            },
            {
                "correction_id": "P4-OCC-008",
                "source_finding_ids": [8],
                "sample_id": "P4Q-02a9af3fa54f",
                "field": "version_claim_status",
                "after": "PRESENT_EVIDENCE_INSUFFICIENT",
                "reason": (
                    "The candidate makes a version/history comparison, but frozen E1/E2 do not "
                    "establish the prior Regulations' degree-count provision."
                ),
                "evidence_basis": (
                    "FROZEN_PACKET_ONLY / EXPECTED_BLIND; no post-hoc E3 expansion. Owner "
                    "confirmation item 4."
                ),
                "owner_decision_lineage": OWNER_LINEAGE,
            },
            {
                "correction_id": "P4-OCC-009",
                "source_finding_ids": [6],
                "sample_id": "P4Q-02a9af3fa54f",
                "field": "minimum_external_evidence_needed",
                "after": "NOT_APPLICABLE",
                "reason": (
                    "Minimum external evidence is not applicable because the frozen-packet "
                    "overall status is INSUFFICIENT_EVIDENCE, not FACTUAL_CONFLICT."
                ),
                "evidence_basis": (
                    "Accepted Guide relation plus Owner confirmation item 4; no E3 is used."
                ),
                "owner_decision_lineage": OWNER_LINEAGE,
            },
            {
                "correction_id": "P4-OCC-010",
                "source_finding_ids": [],
                "sample_id": "P4Q-02a9af3fa54f",
                "field": "phase2_issue",
                "after": "EVIDENCE_MISSING",
                "reason": (
                    "The frozen Evidence Pool omits evidence sufficient to establish the prior "
                    "Academic Degrees Regulations' degree-count provision."
                ),
                "evidence_basis": (
                    "FROZEN_PACKET_ONLY / EXPECTED_BLIND; E1/E2 are insufficient and no E3/E4 "
                    "is introduced. Owner confirmation item 4."
                ),
                "owner_decision_lineage": OWNER_LINEAGE,
                "note": "Additional field-reason normalization needed to remove the raw E4 reference while preserving the Owner-confirmed value.",
            },
        ]
    )
    return specs


def apply_corrections(
    records: list[dict[str, Any]], specs: Sequence[Mapping[str, Any]]
) -> list[dict[str, Any]]:
    by_id = {str(record["sample_id"]): record for record in records}
    if len(by_id) != len(records):
        raise ValueError("CANDIDATE_SAMPLE_ID_DUPLICATE_BLOCKER")
    applied: list[dict[str, Any]] = []
    for spec in specs:
        sample_id = str(spec["sample_id"])
        field = str(spec["field"])
        record = by_id[sample_id]
        cell = record["fields"][field]
        before = str(cell["value"])
        before_reason = str(cell.get("owner_reason", ""))
        before_source = str(cell["source"])
        after = str(spec["after"])
        if after not in ENUMS[field]:
            raise ValueError(f"CORRECTION_ENUM_BLOCKER:{sample_id}:{field}:{after}")
        cell["pre_consistency_correction_value"] = before
        cell["pre_consistency_correction_reason"] = before_reason
        cell["pre_consistency_correction_source"] = before_source
        cell["value"] = after
        cell["owner_reason"] = str(spec["reason"])
        cell["source"] = "OWNER_CONSISTENCY_CORRECTION_OVERLAY"
        cell["consistency_correction_id"] = str(spec["correction_id"])
        applied.append(
            {
                **dict(spec),
                "before": before,
                "after": after,
                "value_changed": before != after,
                "before_reason": before_reason,
                "after_reason": str(spec["reason"]),
                "reason_changed": before_reason != str(spec["reason"]),
                "before_source": before_source,
                "after_source": "OWNER_CONSISTENCY_CORRECTION_OVERLAY",
            }
        )
    return applied


def validate_candidate_view(records: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    violations: list[dict[str, str]] = []
    nonfrozen_reference_pattern = re.compile(
        r"(?:(?<![A-Za-z0-9_])E[3-9](?![A-Za-z0-9_])|证据\s*[3-9])",
        re.IGNORECASE,
    )
    current_source_counts: Counter[str] = Counter()
    value_count = 0
    for record in records:
        sample_id = str(record["sample_id"])
        fields = record["fields"]
        if set(fields) != set(ALL_FIELDS):
            violations.append(
                {"sample_id": sample_id, "rule": "EXACT_EIGHT_FIELD_CONTRACT"}
            )
            continue
        for field in ALL_FIELDS:
            value = str(fields[field]["value"])
            value_count += 1
            current_source_counts[str(fields[field]["source"])] += 1
            if value not in ENUMS[field]:
                violations.append(
                    {
                        "sample_id": sample_id,
                        "field": field,
                        "rule": "CANONICAL_ENUM",
                        "value": value,
                    }
                )
            reason = str(fields[field].get("owner_reason", ""))
            if nonfrozen_reference_pattern.search(reason):
                violations.append(
                    {
                        "sample_id": sample_id,
                        "field": field,
                        "rule": "NO_UNBOUND_E3_OR_HIGHER_IN_EFFECTIVE_REASON",
                        "value": reason,
                    }
                )
        local = str(fields["local_internal_conflict"]["value"])
        overall = str(fields["overall_fact_status"]["value"])
        minimum = str(fields["minimum_external_evidence_needed"]["value"])
        issue = str(fields["phase2_issue"]["value"])
        if overall != "FACTUAL_CONFLICT" and minimum != "NOT_APPLICABLE":
            violations.append(
                {
                    "sample_id": sample_id,
                    "rule": "NON_CONFLICT_MINIMUM_MUST_BE_NOT_APPLICABLE",
                    "value": minimum,
                }
            )
        if overall == "FACTUAL_CONFLICT" and local == "YES":
            if minimum != "NOT_APPLICABLE" or issue != "NONE":
                violations.append(
                    {
                        "sample_id": sample_id,
                        "rule": "INTERNAL_CONTRADICTION_OWNER_RULE",
                        "value": f"minimum={minimum};issue={issue}",
                    }
                )
        if (
            overall == "FACTUAL_CONFLICT"
            and local != "YES"
            and minimum == "NOT_APPLICABLE"
        ):
            violations.append(
                {
                    "sample_id": sample_id,
                    "rule": "EXTERNAL_CONFLICT_MINIMUM_REQUIRED",
                    "value": minimum,
                }
            )
        if issue == "EVIDENCE_MISSING" and overall != "INSUFFICIENT_EVIDENCE":
            violations.append(
                {
                    "sample_id": sample_id,
                    "rule": "EVIDENCE_MISSING_REQUIRES_INSUFFICIENT_EVIDENCE",
                    "value": overall,
                }
            )
    return {
        "status": "PASS" if not violations else "FAIL",
        "record_count": len(records),
        "field_count": value_count,
        "current_source_counts": dict(sorted(current_source_counts.items())),
        "violations": violations,
        "unresolved_consistency_blocker": len(violations),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prior-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--git-head", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    require_new_output(args.output)
    timestamp = now_utc()
    prior_integrity = verify_manifest(args.prior_root)
    prior_workbook = (
        args.prior_root
        / "raw/PILOT4_AB_OWNER_EXPECTED_BLIND_ADJUDICATION_WORKBOOK_V1_RETURNED.xlsx"
    )
    if sha256(prior_workbook) != OWNER_WORKBOOK_SHA256:
        raise ValueError("OWNER_WORKBOOK_SHA_BLOCKER")

    prior_view = json.loads(
        (args.prior_root / "control/resolved_label_candidate_pre_gt.json").read_text(
            encoding="utf-8"
        )
    )
    if prior_view["record_count"] != 72 or prior_view["field_count"] != 576:
        raise ValueError("PRIOR_CANDIDATE_VIEW_CONTRACT_BLOCKER")
    records = list(prior_view["records"])
    specs = correction_specs()
    applied = apply_corrections(records, specs)
    validation = validate_candidate_view(records)
    if validation["status"] != "PASS":
        raise ValueError(f"CONSISTENCY_CLOSURE_BLOCKER:{validation['violations']}")

    resolved_finding_ids = sorted(
        {int(item) for row in applied for item in row["source_finding_ids"]}
    )
    if resolved_finding_ids != list(range(1, 10)):
        raise ValueError(f"PRIOR_FINDING_RESOLUTION_BLOCKER:{resolved_finding_ids}")
    correction_summary = {
        "task_id": TASK_ID,
        "recorded_at": timestamp,
        "classification": "ADDITIVE_OWNER_CONSISTENCY_CORRECTION_OVERLAY",
        "owner_attribution": "PROJECT_REQUIREMENT_OWNER_HUMAN_DECISION",
        "owner_decision_lineage": OWNER_LINEAGE,
        "source_workbook": {
            "path": str(prior_workbook.resolve()),
            "bytes": prior_workbook.stat().st_size,
            "sha256": sha256(prior_workbook),
            "modified": False,
        },
        "source_consistency_findings": 9,
        "resolved_consistency_findings": 9,
        "unresolved_consistency_findings": 0,
        "field_overlay_count": len(applied),
        "field_value_change_count": sum(bool(row["value_changed"]) for row in applied),
        "field_value_confirmation_count": sum(
            not bool(row["value_changed"]) for row in applied
        ),
        "corrections": applied,
        "raw_a_b_returns_modified": False,
        "raw_owner_workbook_modified": False,
        "expected_v3_loaded": False,
        "ground_truth_generated": False,
    }
    write_json(
        args.output / "control/owner_consistency_correction_overlay.json",
        correction_summary,
    )
    write_json(
        args.output / "control/resolved_label_candidate_pre_gt_consistency_closed.json",
        {
            "task_id": TASK_ID,
            "classification": "OWNER_PRIORITIZED_PRE_GROUND_TRUTH_CANDIDATE",
            "status": "OWNER_ADJUDICATION_CONSISTENCY_CLOSED_NOT_GROUND_TRUTH",
            "record_count": 72,
            "field_count": 576,
            "prior_resolution_source_counts": prior_view["source_counts"],
            "current_resolution_source_counts": validation["current_source_counts"],
            "owner_consistency_overlay_count": len(applied),
            "expected_v3_loaded": False,
            "ground_truth": False,
            "records": records,
        },
    )
    write_json(
        args.output / "qa/candidate_view_consistency_validation.json",
        {
            "task_id": TASK_ID,
            "validated_at": timestamp,
            **validation,
            "source_findings": 9,
            "resolved_findings": 9,
            "unresolved_findings": 0,
            "expected_v3_loaded": False,
            "ground_truth_generation_allowed_by_this_task": False,
        },
    )
    write_json(
        args.output / "qa/source_evidence_integrity.json",
        {
            "task_id": TASK_ID,
            "status": "PASS",
            "prior_package": prior_integrity,
            "owner_workbook": {
                "path": str(prior_workbook.resolve()),
                "bytes": prior_workbook.stat().st_size,
                "sha256": sha256(prior_workbook),
                "expected_sha256": OWNER_WORKBOOK_SHA256,
                "identity_match": True,
            },
            "raw_a_b_returns_modified": False,
            "raw_owner_workbook_modified": False,
        },
    )
    write_text(
        args.output
        / "acceptance/PILOT4_OWNER_ADJUDICATION_CONSISTENCY_CLOSURE_EVIDENCE.md",
        f"""# Pilot4 Owner Adjudication Consistency Closure Evidence

- Task: `{TASK_ID}`
- Owner workbook SHA256: `{OWNER_WORKBOOK_SHA256}` (unchanged).
- Prior consistency findings: `9`; resolved: `9`; unresolved: `0`.
- Field-level overlays: `{len(applied)}`; value changes: `{sum(bool(row["value_changed"]) for row in applied)}`; value confirmations with reason/provenance normalization: `{sum(not bool(row["value_changed"]) for row in applied)}`.
- Candidate view: `72 samples / 576 fields`; canonical enum and relational validation: `PASS`.
- Unbound E3/E4-or-higher references in effective reasons: `0`.
- A/B raw returns modified: `false`; Owner raw workbook modified: `false`.
- Expected V3 loaded: `false`; Ground Truth generated: `false`.
- Final status: `OWNER_ADJUDICATION_CONSISTENCY_CLOSED / WAITING_FOR_OWNER_NEXT_APPROVAL`.
""",
    )
    write_text(
        args.output / "README.md",
        """# Pilot4 Owner adjudication consistency closure

This additive package applies the Owner's 2026-09-15 confirmation to the already locked adjudication candidate. It preserves the A/B returns and Owner workbook unchanged, records every before/after value, prior/effective reason, evidence basis and Owner lineage, and resolves all nine previously reported consistency findings.

The resulting 72-sample / 576-field view passed canonical enum, minimum-evidence, internal-contradiction, evidence-missing and effective-evidence-reference validation. It remains a pre-Ground-Truth candidate. Expected V3 was not loaded and no Ground Truth or downstream experiment was created.
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
            "generated_at": timestamp,
            "git_head": args.git_head,
            "entry_count_excluding_manifest": len(entries),
            "aggregate_sha256": aggregate,
            "entries": entries,
            "final_status": [
                "OWNER_ADJUDICATION_CONSISTENCY_CLOSED",
                "UNRESOLVED_CONSISTENCY_BLOCKER_0",
                "OWNER_WORKBOOK_SHA_UNCHANGED",
                "RAW_A_B_RETURNS_UNCHANGED",
                "EXPECTED_V3_NOT_LOADED",
                "NO_GROUND_TRUTH_YET",
                "WAITING_FOR_OWNER_NEXT_APPROVAL",
            ],
        },
    )
    print(
        json.dumps(
            {
                "status": "OWNER_ADJUDICATION_CONSISTENCY_CLOSED",
                "source_findings": 9,
                "resolved_findings": 9,
                "unresolved_findings": 0,
                "field_overlays": len(applied),
                "value_changes": sum(bool(row["value_changed"]) for row in applied),
                "value_confirmations": sum(
                    not bool(row["value_changed"]) for row in applied
                ),
                "workbook_sha256": OWNER_WORKBOOK_SHA256,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
