"""Validate byte-locked R5 auxiliary Phase1 and targeted Phase1 returns."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


FIELDS = (
    "text_naturalness", "local_internal_conflict", "self_containment",
    "ambiguous_referent", "meta_or_template_language",
)
FILES = (
    "PAPER1_FORMAL_D1_CANARY_R5_CLAUDE_PHASE1_AUX_RAW_V1.json",
    "PAPER1_FORMAL_D1_CANARY_R5_CLAUDE_TARGETED_PHASE1_AUX_RAW_V1.json",
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> Any:
    return json.loads(path.read_bytes().decode("utf-8-sig"))


def write(path: Path, value: Any) -> None:
    with path.open("xb") as stream:
        stream.write((json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))


def validate(rows: Any, packet: list[dict[str, Any]], schema: dict[str, Any]) -> None:
    assert isinstance(rows, list) and len(rows) == len(packet)
    ids = [row["blind_review_id"] for row in rows]
    assert len(set(ids)) == len(ids)
    assert ids == [row["blind_review_id"] for row in packet]
    for row in rows:
        assert set(row) == set(schema)
        assert isinstance(row["issue_note"], str)
        for field in FIELDS:
            assert row[field] in schema[field]


def main() -> None:
    parser = argparse.ArgumentParser()
    for key in ("source", "previous", "locked"):
        parser.add_argument(f"--{key}", type=Path, required=True)
    args = parser.parse_args()
    roots = (args.source / "R5-claude24条.txt", args.source / "R5-claude2条.txt")
    copies = tuple(args.locked / name for name in FILES)
    assert all(root.read_bytes() == copy.read_bytes() for root, copy in zip(roots, copies, strict=True))
    schema = load(args.source / "paper1_formal240_d1_canary_20260922" / "PAPER1_FORMAL_D1_BLIND_REVIEW_IMPORT_SCHEMA_V2.json")["phase1"]
    old_packet = load(args.source / "paper1_formal240_d1_canary_20260922" / "PAPER1_FORMAL_D1_BLIND_REVIEW_PACKAGE_PHASE1_V2.json")["records"]
    new_packet = load(args.previous / "PAPER1_FORMAL_D1_CANARY_TARGETED_PHASE1_REVIEW_PACKAGE_V1.json")["records"]
    old, targeted = load(copies[0]), load(copies[1])
    validate(old, old_packet, schema)
    validate(targeted, new_packet, schema)
    primary = {
        "R3-gpt": (load(args.previous / "PAPER1_FORMAL_D1_CANARY_R3_GPT_PHASE1_RAW_V1.json"),
                   load(args.locked / "PAPER1_FORMAL_D1_CANARY_R3_GPT_TARGETED_PHASE1_RAW_V1.json")),
        "R4-codex": (load(args.previous / "PAPER1_FORMAL_D1_CANARY_R4_CODEX_PHASE1_RAW_V1.json"),
                     load(args.locked / "PAPER1_FORMAL_D1_CANARY_R4_CODEX_TARGETED_PHASE1_RAW_V1.json")),
    }
    comparisons: dict[str, Any] = {}
    for name, (full, short) in primary.items():
        comparisons[name] = {}
        for scope, left, right in (("full_24", old, full), ("targeted_2", targeted, short)):
            by_field = {field: sum(a[field] == b[field] for a, b in zip(left, right, strict=True)) for field in FIELDS}
            differences = [a["blind_review_id"] for a, b in zip(left, right, strict=True)
                           if any(a[field] != b[field] for field in FIELDS)]
            comparisons[name][scope] = {"field_agreement": by_field, "structured_disagreement_ids": differences}
    assert targeted[0]["blind_review_id"] == "D1BR-C9E69F1920D5"
    assert targeted[0]["text_naturalness"] == "UNNATURAL"
    assert targeted[0]["local_internal_conflict"] == "YES"
    assert "自相矛盾" in targeted[0]["issue_note"]
    assert targeted[1]["text_naturalness"] == "NATURAL" and targeted[1]["local_internal_conflict"] == "NO"
    manifest = {
        "locked_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_files": [{"path": str(src), "bytes": src.stat().st_size, "sha256": sha(src),
                          "immutable_copy": str(dst), "copy_sha256": sha(dst)}
                         for src, dst in zip(roots, copies, strict=True)],
        "validation": "FULL_24_AND_TARGETED_2_EXACT_ID_ORDER_SCHEMA_ENUM_PASS",
        "role": "AUXILIARY_NON_GATING_PHASE1_ONLY",
    }
    report = {
        "status": "R5_AUXILIARY_QA_RECORDED_NON_GATING",
        "full_rows": 24, "targeted_rows": 2, "raw_sha256": [sha(path) for path in copies],
        "comparisons": comparisons,
        "targeted_first_row_interpretation": "AUXILIARY_NATURALNESS_CONFLICT_COUPLING; contradiction alone is not a candidate naturalness defect",
        "candidate_repair_triggered_by_r5": False,
        "phase2_release_gating_effect": "NONE",
        "not_phase2": True,
    }
    write(args.locked / "PAPER1_FORMAL_D1_CANARY_R5_AUX_RAW_LOCK_MANIFEST_V1.json", manifest)
    write(args.locked / "PAPER1_FORMAL_D1_CANARY_R5_AUXILIARY_COMPARISON_V1.json", report)
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
