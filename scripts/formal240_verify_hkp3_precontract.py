"""Lock HKP3 official source identities and frozen slots before text drafting.

This gate checks identity, chronology metadata presence, and the precommitted
evidence path. It does not certify the legal interpretation or any candidate.
"""

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
    parser.add_argument("--hkp2-root", type=Path, required=True)
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
    new = load(
        args.hkp2_root
        / "new_official_snapshots"
        / "ML1988_HUBEI_GAZETTE"
        / "capture_manifest.json"
    )

    groups = contract["groups"]
    errors: list[str] = []
    source_results: dict[str, dict[str, Any]] = {}
    ids = [g["group_slot_id"] for g in groups]
    if len(ids) != 10 or len(set(ids)) != 10:
        errors.append("HKP3 group count/uniqueness is not 10/10")
    if Counter(g["target_s"] for g in groups) != Counter({"S1": 4, "S2": 3, "S3": 3}):
        errors.append("HKP3 S allocation mismatch")
    for target_s in ("S1", "S2", "S3"):
        cell = [g for g in groups if g["target_s"] == target_s]
        clusters = [g["family_cluster_id"] for g in cell]
        if len(clusters) != len(set(clusters)):
            errors.append(f"repeated family within HKP3 {target_s}")
    for group in groups:
        group_id = group["group_slot_id"]
        slot = matrix.get(group_id)
        if slot is None or slot["hkp"] != "HKP3":
            errors.append(f"non-frozen HKP3 slot: {group_id}")
        elif slot["target_stealth_design"] != group["target_s"]:
            errors.append(f"target S differs from frozen matrix: {group_id}")
        for key in (
            "canonical_fact",
            "version_path",
            "planned_primary_corruption",
            "evidence_path_precommit",
            "neutral_query",
            "primary_factual_core_id",
        ):
            if not group.get(key):
                errors.append(f"missing {key}: {group_id}")
        expected_path = {
            "S1": "ZERO_EXTERNAL_EVIDENCE_REQUIRED",
            "S2": "ONE_OFFICIAL_EVIDENCE",
            "S3": "MULTI_EVIDENCE_OR_VERSION_CHAIN",
        }[group["target_s"]]
        if group["evidence_path_precommit"] != expected_path:
            errors.append(f"bad evidence path: {group_id}")
        if group["target_s"] == "S3" and len(group["evidence_refs"]) < 2:
            errors.append(f"incomplete version chain: {group_id}")
        for ref in group["evidence_refs"]:
            if ref in source_results:
                continue
            if ref in batch1:
                record = batch1[ref]
                path = args.batch1_root / record["raw_path"]
                expected_sha = record["raw_sha256"]
                url = record["official_url"]
            elif ref in canary:
                record = canary[ref]
                path = args.canary_root / record["snapshot_raw_html"]
                expected_sha = record["snapshot_raw_sha256"]
                url = record["official_url"]
            elif ref == "ML1988_HUBEI_GAZETTE":
                path = Path(new["raw_path"])
                expected_sha = new["raw_sha256"]
                url = new["final_url"]
            else:
                errors.append(f"unknown official source: {ref}")
                continue
            actual = sha(path) if path.is_file() else None
            official = urlparse(url).scheme == "https" and urlparse(url).hostname is not None
            if actual != expected_sha:
                errors.append(f"raw snapshot mismatch: {ref}")
            if not official or not str(urlparse(url).hostname).endswith("gov.cn"):
                errors.append(f"nonofficial URL: {ref}")
            source_results[ref] = {
                "path": str(path),
                "url": url,
                "sha256": expected_sha,
                "expected_raw_sha256": expected_sha,
                "actual_raw_sha256": actual,
                "byte_identity_pass": actual == expected_sha,
                "official_host_pass": official,
            }

    report = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "status": "PRECONSTRUCTION_EVIDENCE_IDENTITY_GATE_PASS"
        if not errors
        else "GROUP_CONSTRUCTION_BLOCKED",
        "batch": "D1_REMAINING40_HKP3",
        "candidate_text_created_at_gate": False,
        "group_count": len(groups),
        "target_s_counts": dict(Counter(g["target_s"] for g in groups)),
        "official_source_count": len(source_results),
        "sources": source_results,
        "errors": errors,
        "scientific_limit": "Source hashes and frozen slots only; fact atom and blind QA pending.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(report["status"], len(groups), len(source_results), len(errors))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
