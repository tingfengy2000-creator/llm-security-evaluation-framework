"""Verify D1 HKP2 frozen-slot and official-snapshot provenance before candidate writing.

This is a preconstruction gate only. It does not certify factual interpretation,
candidate quality, or readiness for external reviewers.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--precontract", type=Path, required=True)
    parser.add_argument("--matrix", type=Path, required=True)
    parser.add_argument("--batch1-root", type=Path, required=True)
    parser.add_argument("--canary-root", type=Path, required=True)
    parser.add_argument("--new-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    contract = _read_json(args.precontract)
    groups = contract["groups"]
    matrix = {
        row["group_slot_id"]: row
        for line in args.matrix.read_text(encoding="utf-8").splitlines()
        if (row := json.loads(line))["domain"] == "D1"
    }
    batch1_manifest = _read_json(
        args.batch1_root
        / "preconstruction_v2"
        / "PAPER1_FORMAL_D1_HKP1_BATCH1_EVIDENCE_MANIFEST_V2.json"
    )
    canary_manifest = _read_json(
        args.canary_root / "PAPER1_FORMAL_D1_CANARY_EVIDENCE_MANIFEST_V3.json"
    )
    batch1 = {r["evidence_doc_id"]: r for r in batch1_manifest["snapshots"]}
    canary = {r["evidence_doc_id"]: r for r in canary_manifest}
    new_manifest = _read_json(
        args.new_root
        / "new_official_snapshots"
        / "ML1988_HUBEI_GAZETTE"
        / "capture_manifest.json"
    )

    errors: list[str] = []
    source_results: dict[str, dict[str, Any]] = {}
    ids = [g["group_slot_id"] for g in groups]
    if len(ids) != 10 or len(set(ids)) != 10:
        errors.append("HKP2 group count/uniqueness is not 10/10")
    if Counter(g["target_s"] for g in groups) != Counter(
        {"S1": 3, "S2": 3, "S3": 4}
    ):
        errors.append("target-S allocation mismatch")
    if len({g["family_cluster_id"] for g in groups}) != 10:
        errors.append("family-cluster reuse inside HKP2 batch")
    for g in groups:
        slot = matrix.get(g["group_slot_id"])
        if slot is None or slot["hkp"] != "HKP2":
            errors.append(f"non-frozen or non-HKP2 slot: {g['group_slot_id']}")
        elif slot["target_stealth_design"] != g["target_s"]:
            errors.append(f"target-S mismatch: {g['group_slot_id']}")
        if not g["canonical_fact"] or not g["planned_primary_corruption"]:
            errors.append(f"missing fact/corruption plan: {g['group_slot_id']}")
        for ref in g["evidence_refs"]:
            if ref in source_results:
                continue
            if ref in batch1:
                r = batch1[ref]
                path = args.batch1_root / r["raw_path"]
                expected_sha = r["raw_sha256"]
                url = r["official_url"]
            elif ref in canary:
                r = canary[ref]
                path = args.canary_root / r["snapshot_raw_html"]
                expected_sha = r["snapshot_raw_sha256"]
                url = r["official_url"]
            elif ref == "ML1988_HUBEI_GAZETTE":
                path = Path(new_manifest["raw_path"])
                expected_sha = new_manifest["raw_sha256"]
                url = new_manifest["final_url"]
            else:
                errors.append(f"unknown evidence ID: {ref}")
                continue
            actual_sha = _sha(path) if path.is_file() else None
            if actual_sha != expected_sha:
                errors.append(f"snapshot hash mismatch: {ref}")
            if not url.startswith("https://") or ".gov.cn" not in url:
                errors.append(f"not an official HTTPS URL: {ref}")
            source_results[ref] = {
                "path": str(path),
                "official_url": url,
                "sha256": actual_sha,
                "hash_pass": actual_sha == expected_sha,
                "bytes": path.stat().st_size if path.is_file() else None,
            }
    result = {
        "status": "PRECONSTRUCTION_EVIDENCE_IDENTITY_GATE_PASS"
        if not errors
        else "PRECONSTRUCTION_EVIDENCE_IDENTITY_BLOCKED",
        "does_not_certify": [
            "factual interpretation",
            "candidate quality",
            "external review release",
        ],
        "group_count": len(groups),
        "target_s": dict(Counter(g["target_s"] for g in groups)),
        "source_count": len(source_results),
        "sources": source_results,
        "errors": errors,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.output.exists():
        raise SystemExit(f"Refusing to overwrite: {args.output}")
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
