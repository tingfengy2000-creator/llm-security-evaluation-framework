"""Byte-lock the two Owner-pasted targeted Phase1 JSON arrays.

The source is a composite instruction attachment, not separately uploaded
reviewer files. Exact UTF-8 byte ranges are extracted without JSON rewriting.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


NAMES = {
    "R3-gpt": "PAPER1_FORMAL_D1_CANARY_R3_GPT_TARGETED_PHASE1_RAW_V1.json",
    "R4-codex": "PAPER1_FORMAL_D1_CANARY_R4_CODEX_TARGETED_PHASE1_RAW_V1.json",
}
MARKERS = {
    "R3-gpt": "原始返回：",
    "R4-codex": "Reviewer ID = R4-codex",
}
FIELDS = (
    "text_naturalness",
    "local_internal_conflict",
    "self_containment",
    "ambiguous_referent",
    "meta_or_template_language",
)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def extract(source: bytes, marker: str) -> tuple[bytes, int, int, Any]:
    content = source.decode("utf-8")
    anchor = content.index(marker)
    begin = content.index("[", anchor + len(marker))
    data, consumed = json.JSONDecoder().raw_decode(content[begin:])
    end = begin + consumed
    byte_start = len(content[:begin].encode("utf-8"))
    byte_end = len(content[:end].encode("utf-8"))
    raw = source[byte_start:byte_end]
    assert json.loads(raw) == data
    return raw, byte_start, byte_end, data


def check(rows: Any, packet: list[dict[str, Any]], schema: dict[str, Any]) -> None:
    assert isinstance(rows, list) and len(rows) == len(packet) == 2
    ids = [row["blind_review_id"] for row in rows]
    assert len(set(ids)) == 2
    assert ids == [row["blind_review_id"] for row in packet]
    for row in rows:
        assert set(row) == set(schema)
        assert isinstance(row["issue_note"], str)
        for field in FIELDS:
            assert row[field] in schema[field]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--attachment", type=Path, required=True)
    parser.add_argument("--packet", type=Path, required=True)
    parser.add_argument("--schema", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    assert args.output.is_dir()
    attachment = args.attachment.read_bytes()
    packet = json.loads(args.packet.read_bytes())["records"]
    schema = json.loads(args.schema.read_bytes())["phase1"]
    results: dict[str, Any] = {}
    for reviewer in NAMES:
        raw, start, end, rows = extract(attachment, MARKERS[reviewer])
        check(rows, packet, schema)
        results[reviewer] = {
            "source": str(args.attachment),
            "source_sha256": digest(attachment),
            "source_byte_range_start_inclusive": start,
            "source_byte_range_end_exclusive": end,
            "raw_filename": NAMES[reviewer],
            "bytes": len(raw),
            "sha256": digest(raw),
            "records": len(rows),
            "schema_id_order_enum": "PASS",
            "provenance_level": "OWNER_PASTED_COMPOSITE_ATTACHMENT_BYTE_SLICE",
        }
    target_paths = [args.output / NAMES[reviewer] for reviewer in NAMES]
    manifest_path = args.output / "PAPER1_FORMAL_D1_CANARY_TARGETED_PHASE1_RAW_LOCK_MANIFEST_V1.json"
    assert all(not path.exists() for path in [*target_paths, manifest_path])
    for reviewer in NAMES:
        raw, _, _, _ = extract(attachment, MARKERS[reviewer])
        with (args.output / NAMES[reviewer]).open("xb") as stream:
            stream.write(raw)
    manifest = {
        "task": "P1-FORMAL240-D1-CANARY-PHASE1-FINAL-CLOSEOUT-AND-PHASE2-RELEASE-PREP-01",
        "locked_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_attachment_sha256": digest(attachment),
        "reviewers": results,
        "raw_lock_before_private_mapping_load": True,
    }
    with manifest_path.open("xb") as stream:
        stream.write((json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
