"""Validate byte-locked R3/R4 V4.2 targeted returns without rewriting raw input."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "docs/research/stage6_1_hidden_knowledge_poisoning/formal240"
PACKAGE = FORMAL / "PAPER1_FORMAL_D1_CANARY_PHASE2_15ITEM_TARGETED_REREVIEW_PACKAGE_V1.json"
OVERLAY = FORMAL / "PAPER1_FORMAL_D1_CANARY_PHASE2_OWNER_SEMANTIC_ADJUDICATION_OVERLAY_V1.json"
SCHEMA = FORMAL / "PAPER1_FORMAL_ANNOTATION_SCHEMA_V4.json"
OUTPUT = FORMAL / "PAPER1_FORMAL_D1_CANARY_V4_2_TARGETED_R3_R4_VALIDATION_V1.json"
R3_NAME = "PAPER1_FORMAL_D1_R3_GPT_PHASE2_V4_2_TARGETED_RETURN.json"
R4_NAME = "PAPER1_FORMAL_D1_R4_CODEX_PHASE2_V4_2_TARGETED_RETURN.json"
EXPECTED_SHA = {
    R3_NAME: "24bf845e98e2fae8c9193fac8c584be1e7a36130ff2b595d3a88c1ced4f9885a",
    R4_NAME: "e2eefbc4435a6cf250a3e1b67e5e337927c4d738e957bf461d9772fa14343fe8",
}
EXPECTED_BYTES = {R3_NAME: 4655, R4_NAME: 5699}
EXPECTED_PACKAGE_SHA = "92360d2415687129521c92df2cf3be0898b8e3b800f14ea48d5e82fa664ed6dc"
EXPECTED_OVERLAY_SHA = "f5c4c899de2e48c9c453a857e22bfba065fb2020aba71fc057532d994ced9b8e"
RETURN_KEYS = {"blind_review_id", "target_field", "reviewed_value", "short_reviewer_reason"}


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def no_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def strict_json(raw: bytes) -> Any:
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError("UTF-8 BOM is not part of the raw return contract")
    return json.loads(raw.decode("utf-8", errors="strict"), object_pairs_hook=no_duplicate_keys)


def read_fixed(path: Path, expected_sha: str) -> Any:
    raw = path.read_bytes()
    if sha256(raw) != expected_sha:
        raise ValueError(f"Frozen input SHA mismatch: {path.name}")
    return strict_json(raw)


def validate_return(
    name: str, source_root: Path, lock_root: Path, package_rows: list[dict[str, Any]], enums: dict[str, list[str]]
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    source = source_root / name
    locked = lock_root / name
    source_raw = source.read_bytes()
    lock_raw = locked.read_bytes()
    if source_raw != lock_raw or sha256(lock_raw) != EXPECTED_SHA[name]:
        raise ValueError(f"Source/locked-byte parity or expected SHA failed: {name}")
    if len(lock_raw) != EXPECTED_BYTES[name]:
        raise ValueError(f"Unexpected byte length: {name}")
    rows = strict_json(lock_raw)
    if not isinstance(rows, list) or len(rows) != 15:
        raise ValueError(f"Expected exactly 15 JSON-array rows: {name}")
    ids: list[str] = []
    for index, (row, expected) in enumerate(zip(rows, package_rows, strict=True)):
        if not isinstance(row, dict) or set(row) != RETURN_KEYS:
            raise ValueError(f"Exact return schema failed: {name} row {index}")
        blind_id = row["blind_review_id"]
        if not isinstance(blind_id, str) or re.fullmatch(r"D1BR-[A-F0-9]{12}", blind_id) is None:
            raise ValueError(f"Bad blind ID: {name} row {index}")
        if blind_id != expected["blind_review_id"] or row["target_field"] != expected["target_field"]:
            raise ValueError(f"Package ID/order/target-field mismatch: {name} row {index}")
        field = row["target_field"]
        if row["reviewed_value"] not in enums[field]:
            raise ValueError(f"Invalid target-field enum: {name} row {index}")
        reason = row["short_reviewer_reason"]
        if not isinstance(reason, str) or not reason.strip():
            raise ValueError(f"Blank reviewer reason: {name} row {index}")
        ids.append(blind_id)
    if len(set(ids)) != 15:
        raise ValueError(f"Duplicate blind ID: {name}")
    read_only = locked.stat().st_file_attributes & 0x01 != 0
    if not read_only:
        raise ValueError(f"Locked raw artifact is writable: {name}")
    metadata = {
        "source_filename": name,
        "locked_filename": name,
        "byte_size": len(lock_raw),
        "sha256": sha256(lock_raw),
        "source_locked_byte_parity": True,
        "locked_read_only": read_only,
        "utf8_no_bom_json_no_duplicate_keys": True,
        "exact_rows_ids_order_schema_enums_nonblank_reasons": "15/15_PASS",
    }
    return rows, metadata


def build(source_root: Path, lock_root: Path) -> dict[str, Any]:
    package = read_fixed(PACKAGE, EXPECTED_PACKAGE_SHA)
    package_rows = package["records"]
    if len(package_rows) != 15 or len({row["blind_review_id"] for row in package_rows}) != 15:
        raise ValueError("Frozen targeted package changed")
    schema = strict_json(SCHEMA.read_bytes())
    enums = schema["phase2"]
    # Validate raw bytes and both returns before any Owner-answer overlay is loaded.
    r3_rows, r3_meta = validate_return(R3_NAME, source_root, lock_root, package_rows, enums)
    r4_rows, r4_meta = validate_return(R4_NAME, source_root, lock_root, package_rows, enums)
    overlay = read_fixed(OVERLAY, EXPECTED_OVERLAY_SHA)
    owner_by_id = {case["blind_review_id"]: case for case in overlay["cases"]}
    if len(owner_by_id) != 15:
        raise ValueError("Owner semantic overlay count changed")
    comparison: list[dict[str, Any]] = []
    for package_row, r3, r4 in zip(package_rows, r3_rows, r4_rows, strict=True):
        blind_id = package_row["blind_review_id"]
        owner = owner_by_id[blind_id]
        field = package_row["target_field"]
        if owner["target_field"] != field:
            raise ValueError(f"Owner overlay target-field mismatch: {blind_id}")
        comparison.append({
            "blind_review_id": blind_id,
            "target_field": field,
            "case_category": owner["case_category"],
            "r3_value": r3["reviewed_value"],
            "r4_value": r4["reviewed_value"],
            "owner_semantic_overlay_value": owner["owner_semantic_value"],
            "r3_r4_agree": r3["reviewed_value"] == r4["reviewed_value"],
            "both_match_owner_overlay": r3["reviewed_value"] == r4["reviewed_value"] == owner["owner_semantic_value"],
            "r3_reason_sha256": sha256(r3["short_reviewer_reason"].encode("utf-8")),
            "r4_reason_sha256": sha256(r4["short_reviewer_reason"].encode("utf-8")),
        })
    agreement = sum(row["r3_r4_agree"] for row in comparison)
    overlay_alignment = sum(row["both_match_owner_overlay"] for row in comparison)
    status = "VERSION_SCOPE_RULE_STABILITY_PASS" if agreement == overlay_alignment == 15 else "TARGETED_RULE_STABILITY_BLOCKER"
    return {
        "artifact_id": "PAPER1_FORMAL_D1_CANARY_V4_2_TARGETED_R3_R4_VALIDATION_V1",
        "review_role": "SAME_ORIGINAL_SESSIONS_TARGETED_RULE_CONFIRMATION_NOT_FRESH_INDEPENDENT_ANNOTATION",
        "review_run_lineage": "OWNER_ATTESTED_ORIGINAL_R3_R4_SESSIONS_EQUAL_MATERIALS_NO_MUTUAL_OR_OVERLAY_ACCESS_NOT_MACHINE_VERIFIED",
        "raw_lock_verified_at_utc": "2026-09-26T05:07:12Z",
        "frozen_package_sha256": EXPECTED_PACKAGE_SHA,
        "owner_overlay_sha256": EXPECTED_OVERLAY_SHA,
        "raw_files": {"r3_gpt": r3_meta, "r4_codex": r4_meta},
        "target_fields": {"version_claim_status": 13, "overall_fact_status": 2},
        "case_categories": {"bare_substantive": 12, "amendment_decision": 1, "historical_comparison": 2},
        "r3_r4_target_value_agreement": f"{agreement}/15",
        "both_match_owner_semantic_overlay": f"{overlay_alignment}/15",
        "disagreement_ids": [row["blind_review_id"] for row in comparison if not row["r3_r4_agree"]],
        "overlay_mismatch_ids": [row["blind_review_id"] for row in comparison if not row["both_match_owner_overlay"]],
        "targeted_rule_status": status,
        "canary_owner_accepted": False,
        "human_ab_authorized": False,
        "comparison": comparison,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", required=True, type=Path)
    parser.add_argument("--lock-root", required=True, type=Path)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    result = build(args.source_root, args.lock_root)
    raw = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    if args.check_only:
        if OUTPUT.read_bytes() != raw:
            raise ValueError("Validated artifact drift")
    else:
        with OUTPUT.open("xb") as stream:
            stream.write(raw)
    print(f"{result['targeted_rule_status']}: {result['r3_r4_target_value_agreement']} target fields")
    print(f"validation_sha256={sha256(OUTPUT.read_bytes())}")


if __name__ == "__main__":
    main()
