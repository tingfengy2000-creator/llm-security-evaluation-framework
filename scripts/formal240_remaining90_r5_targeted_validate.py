"""Validate the locked R5 targeted Phase1 return and compare only blind fields."""

from __future__ import annotations

import argparse
import json
import os
from collections import Counter
from pathlib import Path
from typing import Any

from formal240_remaining90_phase1_validate import (
    DEFAULTS,
    FIELDS,
    read_json,
    sha256,
)


EXPECTED_PACKET_SHA = "4ec24e2a2e432fbd7e12104f14a4d75eec3a80aea1ca68318ce24008645555b2"
EXPECTED_SCHEMA_SHA = "c53d527652fbc5d2415ec7e11b1a2654e7a8f116482f193fe736d505a53e43e9"
EXPECTED_R3_SHA = "36a14d40f530bd2f9566f18f36acdce07a11a43b0c56142b8bb41e6af84f1e14"
EXPECTED_R4_SHA = "d3aa0c1470b5dffab91217157a6b808f73531ae9fc3bbee21ef8626500759f04"


def require_sha(name: str, raw: bytes, expected: str) -> None:
    if sha256(raw) != expected:
        raise ValueError(f"{name}: frozen SHA256 mismatch")


def validate_r5(
    rows: Any,
    packet_rows: list[dict[str, Any]],
    allowed: dict[str, Any],
) -> dict[str, Any]:
    if not isinstance(rows, list) or len(rows) != 10:
        raise ValueError("r5: expected exactly 10 JSON objects")
    expected_ids = [row["blind_review_id"] for row in packet_rows]
    ids: list[str] = []
    for index, row in enumerate(rows):
        if not isinstance(row, dict) or list(row) != list(allowed):
            raise ValueError(f"r5: noncanonical keys/order at row {index}")
        ident = row["blind_review_id"]
        if not isinstance(ident, str) or not ident:
            raise ValueError(f"r5: invalid ID at row {index}")
        ids.append(ident)
        for field, legal in allowed.items():
            value = row[field]
            if not isinstance(value, str):
                raise ValueError(f"r5: nonstring {field} at row {index}")
            if isinstance(legal, list) and value not in legal:
                raise ValueError(f"r5: illegal {field}={value} at row {index}")
        flagged = any(row[field] != default for field, default in zip(FIELDS, DEFAULTS))
        if flagged != bool(row["issue_note"].strip()):
            raise ValueError(f"r5: issue_note flag mismatch at row {index} ({ident})")
    if len(set(ids)) != 10 or ids != expected_ids:
        raise ValueError("r5: ID uniqueness/set/order mismatch")
    return {
        "records": 10,
        "unique_ids": 10,
        "id_set_and_order": "PASS",
        "exact_seven_keys_and_order": "PASS",
        "canonical_enums": "PASS",
        "flag_note_rule": "PASS",
        "distributions": {
            field: dict(Counter(row[field] for row in rows)) for field in FIELDS
        },
        "flagged_notes": sum(bool(row["issue_note"].strip()) for row in rows),
    }


def validate_reference(name: str, rows: Any) -> dict[str, dict[str, Any]]:
    if not isinstance(rows, list) or len(rows) != 90:
        raise ValueError(f"{name}: expected 90 locked reference rows")
    if any(not isinstance(row, dict) for row in rows):
        raise ValueError(f"{name}: invalid reference row")
    by_id = {row.get("blind_review_id"): row for row in rows}
    if len(by_id) != 90:
        raise ValueError(f"{name}: duplicate reference ID")
    return by_id


def compare(
    r5_rows: list[dict[str, Any]],
    r3_by_id: dict[str, dict[str, Any]],
    r4_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    comparisons = []
    for row in r5_rows:
        ident = row["blind_review_id"]
        if ident not in r3_by_id or ident not in r4_by_id:
            raise ValueError(f"reference ID absent: {ident}")
        r3 = r3_by_id[ident]
        r4 = r4_by_id[ident]
        comparisons.append(
            {
                "blind_review_id": ident,
                "fields": {
                    field: {
                        "r3": r3[field],
                        "r4": r4[field],
                        "r5": row[field],
                        "r5_matches_r3": row[field] == r3[field],
                        "r5_matches_r4": row[field] == r4[field],
                    }
                    for field in FIELDS
                },
                "issue_notes": {
                    "r3": r3["issue_note"],
                    "r4": r4["issue_note"],
                    "r5": row["issue_note"],
                },
            }
        )
    disagreement_fields = ("text_naturalness", "local_internal_conflict")
    support = {
        field: {
            "r3_r4_disagreement_count": sum(
                item["fields"][field]["r3"] != item["fields"][field]["r4"]
                for item in comparisons
            ),
            "r5_matches_r3": sum(
                item["fields"][field]["r5_matches_r3"] for item in comparisons
            ),
            "r5_matches_r4": sum(
                item["fields"][field]["r5_matches_r4"] for item in comparisons
            ),
        }
        for field in disagreement_fields
    }
    return {"support_counts": support, "row_comparisons": comparisons}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--r5", required=True, type=Path)
    parser.add_argument("--packet", required=True, type=Path)
    parser.add_argument("--schema", required=True, type=Path)
    parser.add_argument("--r3", required=True, type=Path)
    parser.add_argument("--r4", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    packet, packet_raw = read_json(args.packet)
    require_sha("R5 packet", packet_raw, EXPECTED_PACKET_SHA)
    if not isinstance(packet, dict) or not isinstance(packet.get("records"), list):
        raise ValueError("invalid R5 packet")
    packet_rows = packet["records"]
    if len(packet_rows) != 10 or any(
        not isinstance(row, dict)
        or list(row) != ["blind_review_id", "candidate_text"]
        or not isinstance(row["candidate_text"], str)
        for row in packet_rows
    ):
        raise ValueError("R5 packet requires ten candidate-only records")
    if len({row["blind_review_id"] for row in packet_rows}) != 10:
        raise ValueError("R5 packet IDs duplicate")
    schema, schema_raw = read_json(args.schema)
    require_sha("R5 schema", schema_raw, EXPECTED_SCHEMA_SHA)
    if not isinstance(schema, dict) or not isinstance(schema.get("phase1"), dict):
        raise ValueError("invalid R5 Phase1 schema")
    allowed = schema["phase1"]
    if list(allowed) != ["blind_review_id", *FIELDS, "issue_note"]:
        raise ValueError("R5 schema field drift")

    r5_rows, r5_raw = read_json(args.r5)
    qa = validate_r5(r5_rows, packet_rows, allowed)
    r3_rows, r3_raw = read_json(args.r3)
    r4_rows, r4_raw = read_json(args.r4)
    require_sha("R3 reference", r3_raw, EXPECTED_R3_SHA)
    require_sha("R4 reference", r4_raw, EXPECTED_R4_SHA)
    result = {
        "scope": "R5_AUXILIARY_TARGETED_PHASE1_NOT_GT_NOT_OWNER_ADJUDICATION",
        "r5_raw": {"path": str(args.r5), "bytes": len(r5_raw), "sha256": sha256(r5_raw)},
        "r5_packet_sha256": sha256(packet_raw),
        "r5_schema_sha256": sha256(schema_raw),
        "r3_reference_sha256": sha256(r3_raw),
        "r4_reference_sha256": sha256(r4_raw),
        "r5_validation": qa,
        "categorical_comparison": compare(
            r5_rows,
            validate_reference("r3", r3_rows),
            validate_reference("r4", r4_rows),
        ),
        "issue_note_rule": "semantic/manual comparison only; no string equality required",
        "phase2_release_authorized": False,
    }
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(rendered)
        os.chmod(args.output, 0o444)
    print(rendered)


if __name__ == "__main__":
    main()
