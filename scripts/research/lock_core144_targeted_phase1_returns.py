"""Strict targeted Phase1 validation and additive, non-final evidence views.

Only candidate-visible packets are used during reviewer comparison. Immutable
old/new identity lineage is loaded afterwards solely to join historical returns.
This module never decides semantic blockers or authorizes Phase2 by agreement.
"""

from __future__ import annotations

import argparse
import json
import os
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.research.lock_core144_d2_d3_phase1_returns import (
    DEFAULTS,
    FIELDS,
    digest,
    now,
    parse,
    save_new,
)

REPAIR_ROOT = Path("experiments/core144_d2_d3_phase1_owner_triage_repair_20261003")
OLD_ROOT = Path("experiments/core144_d2_d3_phase1_raw_lock_20261003")
PACKAGE_HASHES = {
    (
        "D2",
        "R3_GPT",
    ): "613ce4c2f8baeea3fae86c5f90f6b7e8c732ac37df3387710b8d34166194d130",
    (
        "D2",
        "R4_CODEX",
    ): "ab1ac71d9eca8a7d4439ed29516b6e23ef513505494afeaf5ede73e3bfa3dedf",
    (
        "D3",
        "R3_GPT",
    ): "7d2d202996589ee15f10d0eac52d26414944b30c807cfd00183e6e0f21399d3d",
    (
        "D3",
        "R4_CODEX",
    ): "db39725a815f81bdf185a882bc93dc1388e26d0206b9c3801310248fe12a4a66",
}
OLD_RAW_HASHES = {
    (
        "D2",
        "R3_GPT",
    ): "71098c2264023408d253248c6bb8c654c08aa9c85fd5ead30a2e58aa9c9a5e55",
    (
        "D2",
        "R4_CODEX",
    ): "6fb101fd1f359397d387d225a6164812b594abfb166c79fa2942fbb43a78c06c",
    (
        "D3",
        "R3_GPT",
    ): "e0c5c95a6de770f4aee692a4c5cc4e35c79786184acc006224caa079e9fb28aa",
    (
        "D3",
        "R4_CODEX",
    ): "c2adf1b01ff25e8b2b22ac5980abf99106e07ecab5690f00681ad7d2b5c8f211",
}


def validate_targeted(
    raw: bytes, packet: list[dict[str, Any]], schema: dict[str, Any]
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Validate any frozen packet size; never normalize a raw return."""
    report: dict[str, Any] = {"errors": [], "validation_pass": False}
    if schema["record_count"] != len(packet):
        raise ValueError("frozen packet/schema count mismatch")
    expected = [row["blind_review_id"] for row in packet]
    if len(set(expected)) != len(expected):
        raise ValueError("frozen packet has duplicate identities")
    if any(set(row) != {"blind_review_id", "candidate_text"} for row in packet):
        raise ValueError("packet is not candidate-only")
    try:
        rows = parse(raw)
    except (ValueError, UnicodeError) as exc:
        report["errors"].append(str(exc))
        return report, []
    if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
        report["errors"].append("return must be a JSON array of objects")
        return report, []
    ids = [row.get("blind_review_id") for row in rows]
    valid_ids = [ident for ident in ids if isinstance(ident, str)]
    keys = schema["keys"]
    report.update(
        records=len(rows),
        expected_records=len(packet),
        unique_ids=len(set(valid_ids)),
        count_exact=len(rows) == len(packet),
        id_set_exact=set(valid_ids) == set(expected),
        id_order_exact=ids == expected,
        duplicate_ids=len(valid_ids) - len(set(valid_ids)),
        missing_ids=sorted(set(expected) - set(valid_ids)),
        unexpected_ids=sorted(set(valid_ids) - set(expected)),
        key_order_exact=all(list(row) == keys for row in rows),
    )
    if not all(
        report[key] for key in ("count_exact", "id_set_exact", "id_order_exact")
    ):
        report["errors"].append("record count / exact ID set / order mismatch")
    if not report["key_order_exact"]:
        report["errors"].append("exact seven-key order mismatch")
    for index, row in enumerate(rows):
        if set(row) != set(keys):
            report["errors"].append(f"row {index + 1}: schema keys mismatch")
            continue
        if any(not isinstance(row[key], str) for key in keys):
            report["errors"].append(f"row {index + 1}: all values must be strings")
            continue
        for field in FIELDS:
            if row[field] not in schema["enums"][field]:
                report["errors"].append(f"row {index + 1}: illegal {field}")
        if any(row[field] != default for field, default in zip(FIELDS, DEFAULTS)):
            if not row["issue_note"].strip():
                report["errors"].append(f"row {index + 1}: abnormal requires note")
    if not report["errors"]:
        report.update(
            validation_pass=True,
            exact_schema_keys=True,
            legal_enums=True,
            required_notes_pass=True,
            utf8_without_bom=True,
            duplicate_json_keys=0,
            distributions={
                field: dict(Counter(row[field] for row in rows)) for field in FIELDS
            },
        )
    return report, rows


def compare_targeted(
    packet: list[dict[str, Any]],
    left: list[dict[str, Any]],
    right: list[dict[str, Any]],
) -> dict[str, Any]:
    """Join by exact identity, not row position across reviewer-specific orders."""
    a = {row["blind_review_id"]: row for row in left}
    b = {row["blind_review_id"]: row for row in right}
    ids = [row["blind_review_id"] for row in packet]
    if (
        len(a) != len(left)
        or len(b) != len(right)
        or set(a) != set(ids)
        or set(b) != set(ids)
    ):
        raise ValueError("comparison requires validated unique identities")
    disagreements = []
    flags = []
    for row in packet:
        ident = row["blind_review_id"]
        differing = [field for field in FIELDS if a[ident][field] != b[ident][field]]
        item = dict(row, r3=a[ident], r4=b[ident], different_fields=differing)
        if differing:
            disagreements.append(item)
        if any(
            result[field] != value
            for result in (a[ident], b[ident])
            for field, value in zip(FIELDS, DEFAULTS)
        ):
            flags.append(item)
    categorical = {}
    for field in FIELDS:
        differing = [ident for ident in ids if a[ident][field] != b[ident][field]]
        categorical[field] = {
            "agree": len(ids) - len(differing),
            "total": len(ids),
            "agreement_rate": (len(ids) - len(differing)) / len(ids),
            "disagreement_ids": differing,
        }
    return {
        "categorical_agreement": categorical,
        "disagreement_rows": disagreements,
        "disagreement_row_count": len(disagreements),
        "disagreement_cell_count": sum(
            len(row["different_fields"]) for row in disagreements
        ),
        "flagged_rows": flags,
        "issue_note_raw_identical_rows": sum(
            a[ident]["issue_note"] == b[ident]["issue_note"] for ident in ids
        ),
        "issue_note_semantics": "INDEPENDENT_TEXT_VISIBLE_INSPECTION_NOT_LITERAL_AGREEMENT",
        "agreement_is_not_acceptance": True,
    }


def merge_evidence_view(
    old: list[dict[str, Any]],
    targeted: list[dict[str, Any]],
    lineage: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Keep each reviewer answer verbatim, with source attribution outside answers."""
    mapping = {row["old_id"]: row["new_id"] for row in lineage}
    targets = {row["blind_review_id"]: row for row in targeted}
    if len(mapping) != len(lineage) or set(mapping.values()) != set(targets):
        raise ValueError("targeted coverage differs from frozen changed set")
    if not set(mapping) <= {row["blind_review_id"] for row in old}:
        raise ValueError("lineage has no historical raw ancestor")
    result = []
    for row in old:
        old_id = row["blind_review_id"]
        changed = old_id in mapping
        answer = dict(targets[mapping[old_id]] if changed else row)
        result.append(
            {
                "answer": answer,
                "source": "TARGETED_V1" if changed else "ORIGINAL_144_V1",
                "previous_blind_review_id": old_id,
                "raw_values_unchanged": True,
            }
        )
    if len({row["answer"]["blind_review_id"] for row in result}) != len(old):
        raise ValueError("merged evidence has duplicate current identities")
    return result


def verify_index(root: Path, expected_hash: str) -> dict[str, Any]:
    path = root / "FINAL_EVIDENCE_INDEX_V1.json"
    if digest(path.read_bytes()) != expected_hash:
        raise ValueError("prior immutable index SHA changed")
    index = parse(path.read_bytes())
    entries = index["files"]
    if isinstance(entries, dict):
        entries = [dict(value, path=key) for key, value in entries.items()]
    for row in entries:
        if digest((root / row["path"]).read_bytes()) != row["sha256"]:
            raise ValueError(f"prior immutable evidence changed: {row['path']}")
    return {
        "index_sha256": expected_hash,
        "checked_files": len(index["files"]),
        "pass": True,
    }


def run(repo: Path, output: Path, analysis: Path | None = None) -> dict[str, Any]:
    destination = analysis or output
    if analysis is not None:
        if analysis.exists():
            raise ValueError("fresh analysis namespace required")
        analysis.mkdir(parents=True)
    lock = parse((output / "RAW_LOCK_MANIFEST_V1.json").read_bytes())
    for row in lock["raw_artifacts"]:
        target = output / row["locked_path"]
        raw = target.read_bytes()
        if raw != Path(row["source_path"]).read_bytes() or digest(raw) != row["sha256"]:
            raise ValueError("immutable raw source/copy/hash mismatch")
        if len(raw) != row["bytes"] or target.stat().st_mode & 0o222:
            raise ValueError("immutable raw byte count/read-only check failed")
    # All hashes and locks above precede strict parsing and reviewer evaluation.
    os.chmod(output / "RAW_LOCK_MANIFEST_V1.json", 0o444)
    previous = repo / REPAIR_ROOT / "output_v3"
    result: dict[str, Any] = {
        "scope": "CANDIDATE_ONLY_TARGETED_PHASE1_QA_NOT_GT",
        "validation_started_utc": now(),
        "raw_locked_before_validation": True,
        "owner_isolation_status": lock["owner_attestation"]["status"],
        "candidate_labels_expected_gt_evidence_used_in_comparison": False,
        "domains": {},
    }
    packets = {}
    valid = {}
    for domain, count in (("D2", 25), ("D3", 32)):
        reports = {}
        for reviewer in ("R3_GPT", "R4_CODEX"):
            folder = previous / "reviewers" / domain / reviewer
            packet_raw = (
                folder
                / f"PAPER1_CORE144_{domain}_{reviewer}_TARGETED_PHASE1_PACKAGE_V1.json"
            ).read_bytes()
            if digest(packet_raw) != PACKAGE_HASHES[domain, reviewer]:
                raise ValueError("frozen targeted packet identity changed")
            packet = parse(packet_raw)
            schema = parse(
                (
                    folder
                    / f"PAPER1_CORE144_{domain}_TARGETED_PHASE1_IMPORT_SCHEMA_V1.json"
                ).read_bytes()
            )
            if len(packet) != count:
                raise ValueError("wrong frozen targeted count")
            raw = (
                output
                / "raw"
                / f"PAPER1_CORE144_{domain}_{reviewer}_TARGETED_PHASE1_RAW_RETURN_V1.json"
            ).read_bytes()
            reports[reviewer], valid[domain, reviewer] = validate_targeted(
                raw, packet, schema
            )
            packets[domain, reviewer] = packet
        parity = {
            row["blind_review_id"]: row["candidate_text"]
            for row in packets[domain, "R3_GPT"]
        } == {
            row["blind_review_id"]: row["candidate_text"]
            for row in packets[domain, "R4_CODEX"]
        }
        if not parity:
            raise ValueError("reviewer information parity failure")
        item: dict[str, Any] = {
            "validation": reports,
            "packet_information_parity": parity,
        }
        if all(row["validation_pass"] for row in reports.values()):
            item["comparison"] = compare_targeted(
                packets[domain, "R3_GPT"],
                valid[domain, "R3_GPT"],
                valid[domain, "R4_CODEX"],
            )
        item["phase2_release_authorized"] = False
        item["semantic_gate"] = "PENDING_INDEPENDENT_TEXT_VISIBLE_TRIAGE"
        result["domains"][domain] = item
    result["validation_completed_utc"] = now()
    save_new(destination / "TARGETED_RAW_VALIDATION_AND_COMPARISON_V1.json", result)
    if not all(
        all(row["validation_pass"] for row in item["validation"].values())
        for item in result["domains"].values()
    ):
        return result  # No evidence view is formed from an invalid targeted return.
    immutable = {
        "repair": verify_index(
            previous, "5f0dd262b0180186b3aedde7dfc115288ef2ee54ac21efaedf731544ba71ff90"
        ),
        "historical_raw": verify_index(
            repo / OLD_ROOT,
            "f7502705956fa6252de04f978a0a4b7fbc14c40538633a7d0a61f0936325818d",
        ),
    }
    # Identity-only private join AFTER candidate-visible validation/comparison.
    for domain in ("D2", "D3"):
        lineage = parse(
            (previous / "private" / domain / "OLD_TO_NEW_LINEAGE_V1.json").read_bytes()
        )
        views = {}
        packet = None
        for reviewer in ("R3_GPT", "R4_CODEX"):
            path = (
                repo
                / OLD_ROOT
                / "raw"
                / f"PAPER1_CORE144_{domain}_{reviewer}_PHASE1_RAW_RETURN_V1.json"
            )
            if digest(path.read_bytes()) != OLD_RAW_HASHES[domain, reviewer]:
                raise ValueError("historical raw identity changed")
            rows = parse(path.read_bytes())
            merged = merge_evidence_view(rows, valid[domain, reviewer], lineage)
            views[reviewer] = [row["answer"] for row in merged]
            if len(merged) != 144:
                raise ValueError("current evidence view is not 144 rows")
            corpus = [
                parse(line.encode("utf-8"))
                for line in (
                    previous / "private" / domain / "candidate_corpus_v3.jsonl"
                )
                .read_text(encoding="utf-8")
                .splitlines()
            ]
            text_by_id = {
                row["blind_review_id"]: row["candidate_text"] for row in corpus
            }
            if set(text_by_id) != {row["answer"]["blind_review_id"] for row in merged}:
                raise ValueError("current corpus identity differs from joined evidence")
            packet = [
                {
                    "blind_review_id": row["answer"]["blind_review_id"],
                    "candidate_text": text_by_id[row["answer"]["blind_review_id"]],
                }
                for row in merged
            ]
            save_new(
                destination
                / f"{domain}_{reviewer}_CURRENT_PHASE1_EVIDENCE_VIEW_V1.json",
                {
                    "status": "PROVISIONAL_NOT_FINAL_NOT_GT",
                    "phase2_release_authorized": False,
                    "records": merged,
                    "same_original_order_after_identity_substitution": True,
                    "counts": dict(Counter(row["source"] for row in merged)),
                    "created_utc": now(),
                },
            )
        assert packet is not None
        save_new(
            destination / f"{domain}_CURRENT_144_PHASE1_COMPARISON_V1.json",
            compare_targeted(packet, views["R3_GPT"], views["R4_CODEX"]),
        )
    save_new(destination / "HISTORICAL_ARTIFACT_PRESERVATION_V1.json", immutable)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--analysis-dir", type=Path)
    args = parser.parse_args()
    result = run(
        args.repo.resolve(),
        args.output.resolve(),
        args.analysis_dir.resolve() if args.analysis_dir else None,
    )
    print(
        json.dumps(
            {
                domain: {
                    "validation": row["validation"],
                    "agreement": row.get("comparison", {}).get("categorical_agreement"),
                    "disagreement_rows": row.get("comparison", {}).get(
                        "disagreement_row_count"
                    ),
                    "phase2_release_authorized": False,
                }
                for domain, row in result["domains"].items()
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
