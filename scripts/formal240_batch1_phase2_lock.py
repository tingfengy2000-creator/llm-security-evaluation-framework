"""Validate and byte-lock the two independent D1 HKP1 Batch-1 Phase2 returns.

This deliberately cannot read construction labels or target stealth metadata.
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
EXPECTED_HASHES = {
    "r3": "65bec342aabd38b936694299f6c97330951fd24154beea5e22f648609361cdf0",
    "r4": "561737885f0801441c0a69cbac61cbdf2388a023b19cc2bdd2b20ad44946e7eb",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def strict_json(data: bytes) -> Any:
    return json.loads(data.decode("utf-8-sig"))


def validate(
    name: str, source: Path, expected_ids: list[str], allowed: dict[str, Any]
) -> tuple[dict[str, Any], list[dict[str, Any]], bytes]:
    raw = source.read_bytes()
    digest = sha256(raw)
    if digest != EXPECTED_HASHES[name]:
        raise ValueError(f"{name}: raw SHA mismatch: {digest}")
    rows = strict_json(raw)
    if not isinstance(rows, list) or len(rows) != 30:
        raise ValueError(f"{name}: expected 30 JSON objects")
    keys = set(allowed)
    ids: list[str] = []
    for index, row in enumerate(rows):
        if not isinstance(row, dict) or set(row) != keys:
            raise ValueError(f"{name}: row {index} has noncanonical keys")
        ident = row["blind_review_id"]
        if not isinstance(ident, str) or not ident:
            raise ValueError(f"{name}: row {index} has invalid ID")
        ids.append(ident)
        for field, legal in allowed.items():
            value = row[field]
            if isinstance(legal, list) and value not in legal:
                raise ValueError(f"{name}: row {index} invalid {field}: {value}")
            if not isinstance(legal, list) and not isinstance(value, str):
                raise ValueError(f"{name}: row {index} nonstring {field}")
        if not row["phase2_reason"].strip():
            raise ValueError(f"{name}: row {index} blank reason")
    if len(set(ids)) != 30 or ids != expected_ids:
        raise ValueError(f"{name}: ID uniqueness/set/order mismatch")
    return {"source": str(source), "bytes": len(raw), "sha256": digest,
            "rows": 30, "unique_ids": 30, "schema_enum_order": "PASS"}, rows, raw


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--r3", type=Path, required=True)
    parser.add_argument("--r4", type=Path, required=True)
    parser.add_argument("--packet", type=Path, required=True)
    parser.add_argument("--schema", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    packet = strict_json(args.packet.read_bytes())
    allowed = strict_json(args.schema.read_bytes())["phase2"]
    expected_ids = [row["blind_review_id"] for row in packet["records"]]
    if len(expected_ids) != 30 or len(set(expected_ids)) != 30:
        raise ValueError("Packet population invalid")
    qa3, rows3, raw3 = validate("r3", args.r3, expected_ids, allowed)
    qa4, rows4, raw4 = validate("r4", args.r4, expected_ids, allowed)
    by3 = {row["blind_review_id"]: row for row in rows3}
    by4 = {row["blind_review_id"]: row for row in rows4}
    agreement = {
        field: {"agree": sum(by3[i][field] == by4[i][field] for i in expected_ids),
                "total": 30,
                "disagreement_ids": [i for i in expected_ids if by3[i][field] != by4[i][field]]}
        for field in FIELDS
    }
    disagreements = [
        {"blind_review_id": ident, "candidate_text": next(
            row["candidate_text"] for row in packet["records"]
            if row["blind_review_id"] == ident),
         "r3": by3[ident]["version_claim_status"],
         "r4": by4[ident]["version_claim_status"]}
        for ident in agreement["version_claim_status"]["disagreement_ids"]
    ]
    result: dict[str, Any] = {
        "status": "PHASE2_RAW_LOCKED_BEFORE_CONSTRUCTION_TARGET_LOAD",
        "locked_at_utc": datetime.now(timezone.utc).isoformat(),
        "packet_path": str(args.packet),
        "packet_sha256": sha256(args.packet.read_bytes()),
        "r3": qa3, "r4": qa4,
        "agreement": agreement,
        "version_disagreements_candidate_only": disagreements,
        "overall_distribution_r3": dict(Counter(r["overall_fact_status"] for r in rows3)),
        "overall_distribution_r4": dict(Counter(r["overall_fact_status"] for r in rows4)),
        "conflict_evidence_path_r3": dict(Counter(
            r["minimum_external_evidence_needed"] for r in rows3
            if r["overall_fact_status"] == "FACTUAL_CONFLICT")),
        "conflict_evidence_path_r4": dict(Counter(
            r["minimum_external_evidence_needed"] for r in rows4
            if r["overall_fact_status"] == "FACTUAL_CONFLICT")),
    }
    if args.output.exists():
        raise FileExistsError(args.output)
    args.output.mkdir(parents=True)
    destinations = {
        "r3": args.output / "PAPER1_FORMAL_D1_HKP1_BATCH1_R3_GPT_PHASE2_RAW_RETURN_V4.json",
        "r4": args.output / "PAPER1_FORMAL_D1_HKP1_BATCH1_R4_CODEX_PHASE2_RAW_RETURN_V4.json",
    }
    for name, data in (("r3", raw3), ("r4", raw4)):
        destinations[name].write_bytes(data)
        os.chmod(destinations[name], 0o444)
        if sha256(destinations[name].read_bytes()) != EXPECTED_HASHES[name]:
            raise AssertionError(f"{name}: immutable copy hash drift")
        result[name]["immutable_copy"] = str(destinations[name])
    report = args.output / "PAPER1_FORMAL_D1_HKP1_BATCH1_PHASE2_RAW_LOCK_AND_AGREEMENT_V1.json"
    report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.chmod(report, 0o444)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
