"""Byte-lock and validate D1 remaining90 Phase2 reviewer returns before mapping load.

This module intentionally reads only reviewer-visible packets and the import
schema. Construction roles/targets are loaded by a separate, later audit.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


EXPECTED = {
    "r3": (55153, "d667c3136fea2f302b1130388d142109a53b66bfa0d86eab7fe2a60147dc8b5a"),
    "r4": (60907, "9f18bd2e27491f849764f8bb9807fc8a794a5a50134fa7c091735c15a83e9691"),
}
FIELDS = (
    "overall_fact_status",
    "version_claim_status",
    "authority_claim_status",
    "minimum_external_evidence_needed",
    "evidence_selection",
    "phase2_issue",
    "possible_accidental_secondary_error",
    "evidence_sufficiency",
)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def strict_json(raw: bytes) -> Any:
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError("UTF-8 BOM is prohibited")
    return json.loads(raw.decode("utf-8", errors="strict"), object_pairs_hook=unique_pairs)


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def validate(
    name: str, source: Path, packet_path: Path, schema: dict[str, Any]
) -> tuple[dict[str, Any], list[dict[str, Any]], bytes]:
    raw = source.read_bytes()
    size, digest = EXPECTED[name]
    require(len(raw) == size and sha(raw) == digest, f"{name}: source byte/hash mismatch")
    rows = strict_json(raw)
    packet = strict_json(packet_path.read_bytes())
    expected_ids = [row["blind_review_id"] for row in packet["records"]]
    require(isinstance(rows, list) and len(rows) == 90, f"{name}: expected 90 objects")
    require(len(expected_ids) == len(set(expected_ids)) == 90, f"{name}: packet IDs invalid")
    expected_fields = list(schema["phase2"])
    actual_ids: list[str] = []
    for index, row in enumerate(rows):
        require(isinstance(row, dict), f"{name}: row {index} not an object")
        require(list(row) == expected_fields, f"{name}: row {index} keys/order invalid")
        for field, rule in schema["phase2"].items():
            value = row[field]
            require(isinstance(value, str), f"{name}: row {index} {field} non-string")
            if isinstance(rule, list):
                require(value in rule, f"{name}: row {index} invalid {field}={value}")
        require(row["phase2_reason"].strip() != "", f"{name}: row {index} blank reason")
        actual_ids.append(row["blind_review_id"])
    require(actual_ids == expected_ids and len(set(actual_ids)) == 90,
            f"{name}: ID set/order/uniqueness mismatch")
    return {
        "source_path": str(source),
        "source_bytes": len(raw),
        "source_sha256": sha(raw),
        "packet_sha256": sha(packet_path.read_bytes()),
        "records": 90,
        "unique_ids": 90,
        "strict_utf8_json": "PASS",
        "exact_keys_and_order": "PASS",
        "legal_enums": "PASS",
        "reviewer_packet_id_order": "PASS",
        "nonblank_reasons": "PASS",
    }, rows, raw


def main() -> None:
    parser = argparse.ArgumentParser()
    for name in ("r3", "r4", "r3-packet", "r4-packet", "schema", "out"):
        parser.add_argument(f"--{name}", type=Path, required=True)
    args = parser.parse_args()
    require(not args.out.exists(), "refusing to overwrite an existing raw-lock namespace")
    schema_raw = args.schema.read_bytes()
    schema = strict_json(schema_raw)
    require(list(schema["phase2"]) == ["blind_review_id", *FIELDS[:6],
            "phase2_reason", *FIELDS[6:], "reviewer_note"], "schema field order drift")
    qa3, rows3, raw3 = validate("r3", args.r3, args.r3_packet, schema)
    qa4, rows4, raw4 = validate("r4", args.r4, args.r4_packet, schema)
    by3 = {row["blind_review_id"]: row for row in rows3}
    by4 = {row["blind_review_id"]: row for row in rows4}
    require(set(by3) == set(by4), "reviewer ID sets differ")
    id_order = [row["blind_review_id"] for row in rows3]
    agreement = {
        field: {
            "agree": sum(by3[ident][field] == by4[ident][field] for ident in id_order),
            "total": 90,
            "disagreement_ids": [
                ident for ident in id_order if by3[ident][field] != by4[ident][field]
            ],
        }
        for field in FIELDS
    }
    def distribution(rows: list[dict[str, Any]], field: str) -> dict[str, int]:
        return dict(sorted(Counter(row[field] for row in rows).items()))

    for rows in (rows3, rows4):
        require(distribution(rows, "phase2_issue") == {"NONE": 90}, "Phase2 issue gate failed")
        require(distribution(rows, "possible_accidental_secondary_error") == {"NO": 90},
                "secondary error gate failed")
        require(distribution(rows, "evidence_sufficiency") == {"SUFFICIENT": 90},
                "Evidence sufficiency gate failed")
        require(distribution(rows, "minimum_external_evidence_needed") == {
            "MULTI_EVIDENCE_OR_VERSION_CHAIN": 11,
            "NOT_APPLICABLE": 60,
            "ONE_OFFICIAL_EVIDENCE": 8,
            "ZERO_EXTERNAL_EVIDENCE_REQUIRED": 11,
        }, "minimum Evidence distribution changed")
        require(distribution(rows, "overall_fact_status")["FACTUAL_CONFLICT"] == 30,
                "factual conflict count changed")
    packet = strict_json(args.r3_packet.read_bytes())
    text_by = {row["blind_review_id"]: row["candidate_text"] for row in packet["records"]}
    disagreements = [
        {
            "blind_review_id": ident,
            "candidate_text": text_by[ident],
            "fields": {
                field: {"r3": by3[ident][field], "r4": by4[ident][field]}
                for field in FIELDS if by3[ident][field] != by4[ident][field]
            },
            "r3_reason": by3[ident]["phase2_reason"],
            "r4_reason": by4[ident]["phase2_reason"],
        }
        for ident in id_order if any(by3[ident][f] != by4[ident][f] for f in FIELDS)
    ]
    result: dict[str, Any] = {
        "status": "REVIEWER_RAW_LOCKED_BEFORE_CONSTRUCTION_TARGET_LOAD",
        "locked_at_utc": datetime.now(timezone.utc).isoformat(),
        "schema_sha256": sha(schema_raw),
        "r3": qa3,
        "r4": qa4,
        "agreement": agreement,
        "distributions": {
            "r3": {field: distribution(rows3, field) for field in FIELDS},
            "r4": {field: distribution(rows4, field) for field in FIELDS},
        },
        "disagreements": disagreements,
        "process_field": "evidence_selection",
        "construction_target_loaded": False,
        "not_ground_truth": True,
    }
    args.out.mkdir(parents=True)
    for name, raw in (("r3", raw3), ("r4", raw4)):
        destination = args.out / (
            "PAPER1_FORMAL_D1_REMAINING90_" + name.upper() + "_PHASE2_RAW_RETURN_V5.json"
        )
        destination.write_bytes(raw)
        os.chmod(destination, 0o444)
        require(destination.read_bytes() == raw, f"{name}: locked copy differs")
        result[name]["immutable_copy"] = str(destination)
    report = args.out / "PAPER1_CORE144_D1_REMAINING90_PHASE2_RAW_LOCK_AND_COMPARISON_V1.json"
    report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.chmod(report, 0o444)
    print(json.dumps({
        "locked_at_utc": result["locked_at_utc"],
        "r3_sha256": qa3["source_sha256"],
        "r4_sha256": qa4["source_sha256"],
        "agreement": {key: value["agree"] for key, value in agreement.items()},
        "disagreement_records": len(disagreements),
        "output": str(args.out),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
