"""Verify HKP4 frozen slots and official source identities before any candidate."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--precontract", type=Path, required=True)
    parser.add_argument("--matrix", type=Path, required=True)
    parser.add_argument("--batch1-root", type=Path, required=True)
    parser.add_argument("--canary-root", type=Path, required=True)
    parser.add_argument("--hkp4-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"Refusing to overwrite: {args.output}")
    contract = load(args.precontract)
    matrix = {
        row["group_slot_id"]: row
        for line in args.matrix.read_text(encoding="utf-8").splitlines()
        if (row := json.loads(line))["domain"] == "D1"
    }
    batch1 = {
        row["evidence_doc_id"]: row
        for row in load(
            args.batch1_root
            / "preconstruction_v2"
            / "PAPER1_FORMAL_D1_HKP1_BATCH1_EVIDENCE_MANIFEST_V2.json"
        )["snapshots"]
    }
    canary = {
        row["evidence_doc_id"]: row
        for row in load(
            args.canary_root / "PAPER1_FORMAL_D1_CANARY_EVIDENCE_MANIFEST_V3.json"
        )
    }
    new_manifests = {
        doc_id: load(
            args.hkp4_root / "new_official_snapshots" / doc_id / "capture_manifest.json"
        )
        for doc_id in ("SI2018_LAW_OFFICIAL_REPOST", "WI_RECOGNITION_2010_MINISTRY")
    }
    groups = contract["groups"]
    errors: list[str] = []
    ids = [group["group_slot_id"] for group in groups]
    if len(ids) != 10 or len(set(ids)) != 10:
        errors.append("HKP4 frozen group count/uniqueness != 10")
    if Counter(g["target_s"] for g in groups) != Counter({"S1": 4, "S2": 2, "S3": 4}):
        errors.append("HKP4 target-S allocation mismatch")
    for target_s in ("S1", "S2", "S3"):
        cell = [g["family_cluster_id"] for g in groups if g["target_s"] == target_s]
        if len(cell) != len(set(cell)):
            errors.append(f"family reused within HKP4 {target_s}")
    sources: dict[str, dict[str, Any]] = {}
    for group in groups:
        group_id = group["group_slot_id"]
        slot = matrix.get(group_id)
        if slot is None or slot["hkp"] != "HKP4":
            errors.append(f"non-frozen HKP4 slot: {group_id}")
        elif slot["target_stealth_design"] != group["target_s"]:
            errors.append(f"target-S mismatch: {group_id}")
        expected_path = {
            "S1": "ZERO_EXTERNAL_EVIDENCE_REQUIRED",
            "S2": "ONE_OFFICIAL_EVIDENCE",
            "S3": "MULTI_EVIDENCE_OR_VERSION_CHAIN",
        }[group["target_s"]]
        if group["evidence_path_precommit"] != expected_path:
            errors.append(f"wrong evidence path: {group_id}")
        if len(group["evidence_refs"]) != (2 if group["target_s"] == "S3" else 1):
            errors.append(f"wrong source count: {group_id}")
        for key in (
            "primary_factual_core_id",
            "family_cluster_id",
            "authority_fact",
            "host_role",
            "original_issuer",
            "planned_primary_corruption",
            "neutral_query",
        ):
            if not group.get(key):
                errors.append(f"missing authority precheck {key}: {group_id}")
        for ref in group["evidence_refs"]:
            if ref in sources:
                continue
            if ref in batch1:
                item = batch1[ref]
                path = args.batch1_root / item["raw_path"]
                expected_sha = item["raw_sha256"]
                url = item["official_url"]
            elif ref in canary:
                item = canary[ref]
                path = args.canary_root / item["snapshot_raw_html"]
                expected_sha = item["snapshot_raw_sha256"]
                url = item["official_url"]
            elif ref in new_manifests:
                item = new_manifests[ref]
                path = Path(item["raw_path"])
                expected_sha = item["raw_sha256"]
                url = item["final_url"]
            else:
                errors.append(f"unknown source: {ref}")
                continue
            actual_sha = sha(path) if path.is_file() else None
            parsed = urlparse(url)
            official = parsed.scheme == "https" and bool(parsed.hostname) and str(
                parsed.hostname
            ).endswith("gov.cn")
            if actual_sha != expected_sha:
                errors.append(f"official raw bytes mismatch: {ref}")
            if not official:
                errors.append(f"nonofficial host: {ref}")
            sources[ref] = {
                "path": str(path),
                "official_url": url,
                "sha256": expected_sha,
                "actual_sha256": actual_sha,
                "byte_identity_pass": actual_sha == expected_sha,
                "official_host_pass": official,
            }
    result = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "status": "PRECONSTRUCTION_AUTHORITY_EVIDENCE_GATE_PASS"
        if not errors
        else "GROUP_CONSTRUCTION_BLOCKED",
        "batch": "D1_REMAINING40_HKP4",
        "candidate_text_created_at_gate": False,
        "group_count": len(groups),
        "target_s_counts": dict(Counter(g["target_s"] for g in groups)),
        "official_source_count": len(sources),
        "sources": sources,
        "scientific_limit": "Snapshot identity and stated issuer locators are not independent factual adjudication.",
        "errors": errors,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(result["status"], len(groups), len(sources), len(errors))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
