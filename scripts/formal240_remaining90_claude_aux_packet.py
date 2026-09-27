"""Build a candidate-only auxiliary Phase1 packet from locked R3/R4 disagreements."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from formal240_remaining90_phase1_validate import FIELDS, packet_rows, read_json


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_new(path: Path, data: bytes) -> dict[str, Any]:
    with path.open("xb") as stream:
        stream.write(data)
    os.chmod(path, 0o444)
    actual = path.read_bytes()
    if actual != data:
        raise AssertionError(f"written bytes differ: {path}")
    return {"path": str(path), "bytes": len(data), "sha256": digest(data)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--r3", required=True, type=Path)
    parser.add_argument("--r4", required=True, type=Path)
    parser.add_argument("--packet", required=True, type=Path)
    parser.add_argument("--schema", required=True, type=Path)
    parser.add_argument("--prompt", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    packet, packet_sha = packet_rows(args.packet)
    r3, r3_raw = read_json(args.r3)
    r4, r4_raw = read_json(args.r4)
    schema, schema_raw = read_json(args.schema)
    if not isinstance(r3, list) or not isinstance(r4, list) or not isinstance(schema, dict):
        raise ValueError("invalid inputs")
    expected_ids = {row["blind_review_id"] for row in packet}
    by3 = {row["blind_review_id"]: row for row in r3}
    by4 = {row["blind_review_id"]: row for row in r4}
    if len(r3) != 90 or len(r4) != 90 or set(by3) != expected_ids or set(by4) != expected_ids:
        raise ValueError("return ID set mismatch")
    selected = [
        row for row in packet
        if any(by3[row["blind_review_id"]][field] != by4[row["blind_review_id"]][field]
               for field in FIELDS)
    ]
    if len(selected) != 10:
        raise ValueError(f"expected ten unique disagreements, found {len(selected)}")
    reviewer_packet = {
        "status": "TARGETED_PHASE1_CANDIDATE_ONLY_AUXILIARY_NOT_GT",
        "records": selected,
    }
    reviewer_schema = dict(schema)
    reviewer_schema["status"] = "TARGETED_PHASE1_ONLY_NOT_GROUND_TRUTH"
    reviewer_schema["each_return"] = (
        "JSON array of exactly 10 objects; exact seven keys, ID set and packet order"
    )
    prompt_raw = args.prompt.read_bytes()
    output = args.output
    output.mkdir(parents=True, exist_ok=False)
    reviewer_dir = output / "reviewer_release"
    control_dir = output / "control_only_do_not_send"
    reviewer_dir.mkdir()
    control_dir.mkdir()
    files = [
        write_new(
            reviewer_dir / "PAPER1_FORMAL_D1_REMAINING90_R5_CLAUDE_TARGETED_PHASE1_PACKET_V1.json",
            (json.dumps(reviewer_packet, ensure_ascii=False, indent=2) + "\n").encode("utf-8"),
        ),
        write_new(
            reviewer_dir / "PAPER1_FORMAL_D1_REMAINING90_R5_CLAUDE_TARGETED_PHASE1_IMPORT_SCHEMA_V1.json",
            (json.dumps(reviewer_schema, ensure_ascii=False, indent=2) + "\n").encode("utf-8"),
        ),
        write_new(
            reviewer_dir / args.prompt.name,
            prompt_raw,
        ),
    ]
    manifest = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "purpose": "R5_CLAUDE_AUXILIARY_BLIND_PHASE1_NOT_FINAL_ADJUDICATION",
        "r3_raw_sha256": digest(r3_raw),
        "r4_raw_sha256": digest(r4_raw),
        "r3_packet_sha256": packet_sha,
        "schema_source_sha256": digest(schema_raw),
        "selected_count": len(selected),
        "selected_ids_packet_order": [row["blind_review_id"] for row in selected],
        "reviewer_release_files": files,
        "hidden_labels_loaded": False,
        "previous_reviewer_values_in_release": False,
    }
    control = write_new(
        control_dir / "PAPER1_FORMAL_D1_REMAINING90_R5_CLAUDE_TARGETED_PHASE1_MANIFEST_V1.json",
        (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8"),
    )
    print(json.dumps({"manifest": control, "release": files, "selected_ids": manifest["selected_ids_packet_order"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
