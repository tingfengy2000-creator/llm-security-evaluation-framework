"""Validate locked D1 remaining90 Phase1 returns without construction labels."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from collections import Counter
from pathlib import Path
from typing import Any


FIELDS = (
    "text_naturalness",
    "local_internal_conflict",
    "self_containment",
    "ambiguous_referent",
    "meta_or_template_language",
)
DEFAULTS = ("NATURAL", "NO", "PASS", "NO", "NO")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise ValueError(f"non-JSON numeric constant: {value}")


def read_json(path: Path) -> tuple[Any, bytes]:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError(f"UTF-8 BOM is not permitted: {path}")
    obj = json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=unique_object,
        parse_constant=reject_constant,
    )
    return obj, raw


def packet_rows(path: Path) -> tuple[list[dict[str, Any]], str]:
    packet, raw = read_json(path)
    if not isinstance(packet, dict) or not isinstance(packet.get("records"), list):
        raise ValueError(f"invalid candidate-only packet: {path}")
    rows = packet["records"]
    if len(rows) != 90 or any(
        not isinstance(row, dict)
        or list(row) != ["blind_review_id", "candidate_text"]
        for row in rows
    ):
        raise ValueError(f"packet must have 90 two-field records: {path}")
    ids = [row["blind_review_id"] for row in rows]
    if len(set(ids)) != 90:
        raise ValueError(f"packet has duplicate IDs: {path}")
    return rows, sha256(raw)


def validate_return(
    name: str,
    path: Path,
    packet: list[dict[str, Any]],
    allowed: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    rows, raw = read_json(path)
    if not isinstance(rows, list) or len(rows) != 90:
        raise ValueError(f"{name}: expected exactly 90 JSON objects")
    expected_keys = list(allowed)
    expected_ids = [row["blind_review_id"] for row in packet]
    ids: list[str] = []
    notes_with_flags = 0
    for index, row in enumerate(rows):
        if not isinstance(row, dict) or list(row) != expected_keys:
            raise ValueError(f"{name}: noncanonical keys/order at row {index}")
        ident = row["blind_review_id"]
        if not isinstance(ident, str) or not ident:
            raise ValueError(f"{name}: invalid ID at row {index}")
        ids.append(ident)
        for field, legal in allowed.items():
            value = row[field]
            if not isinstance(value, str):
                raise ValueError(f"{name}: nonstring {field} at row {index}")
            if isinstance(legal, list) and value not in legal:
                raise ValueError(f"{name}: illegal {field}={value} at row {index}")
        flagged = any(row[field] != default for field, default in zip(FIELDS, DEFAULTS))
        note_present = bool(row["issue_note"].strip())
        if flagged != note_present:
            raise ValueError(f"{name}: issue_note flag mismatch at row {index} ({ident})")
        notes_with_flags += int(note_present)
    if len(set(ids)) != 90 or ids != expected_ids:
        raise ValueError(f"{name}: ID uniqueness/set/order mismatch")
    return {
        "path": str(path),
        "bytes": len(raw),
        "sha256": sha256(raw),
        "records": len(rows),
        "unique_ids": len(set(ids)),
        "id_order": "PASS",
        "keys_order_enums": "PASS",
        "flagged_notes": notes_with_flags,
        "distributions": {
            field: dict(Counter(row[field] for row in rows)) for field in FIELDS
        },
    }, rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--r3", required=True, type=Path)
    parser.add_argument("--r4", required=True, type=Path)
    parser.add_argument("--r3-packet", required=True, type=Path)
    parser.add_argument("--r4-packet", required=True, type=Path)
    parser.add_argument("--schema", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    r3_packet, r3_packet_sha = packet_rows(args.r3_packet)
    r4_packet, r4_packet_sha = packet_rows(args.r4_packet)
    r3_text = {row["blind_review_id"]: row["candidate_text"] for row in r3_packet}
    r4_text = {row["blind_review_id"]: row["candidate_text"] for row in r4_packet}
    if r3_text != r4_text:
        raise ValueError("R3/R4 packet ID/text parity failure")
    schema, schema_raw = read_json(args.schema)
    if not isinstance(schema, dict) or not isinstance(schema.get("phase1"), dict):
        raise ValueError("invalid Phase1 import schema")
    allowed = schema["phase1"]
    qa3, rows3 = validate_return("r3", args.r3, r3_packet, allowed)
    qa4, rows4 = validate_return("r4", args.r4, r4_packet, allowed)
    by3 = {row["blind_review_id"]: row for row in rows3}
    by4 = {row["blind_review_id"]: row for row in rows4}
    ids = [row["blind_review_id"] for row in r3_packet]
    agreement = {
        field: {
            "agree": sum(by3[ident][field] == by4[ident][field] for ident in ids),
            "total": 90,
            "disagreement_ids": [
                ident for ident in ids if by3[ident][field] != by4[ident][field]
            ],
        }
        for field in FIELDS
    }
    result = {
        "scope": "PHASE1_CANDIDATE_ONLY_PREANNOTATION_QA_NOT_GT",
        "r3_packet_sha256": r3_packet_sha,
        "r4_packet_sha256": r4_packet_sha,
        "schema_sha256": sha256(schema_raw),
        "packet_id_text_parity": "PASS",
        "r3": qa3,
        "r4": qa4,
        "categorical_agreement": agreement,
        "issue_note_comparison": "RAW_SEMANTIC_REVIEW_ONLY_NOT_EXACT_STRING_AGREEMENT",
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
