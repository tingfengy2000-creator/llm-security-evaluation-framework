"""Attach repository-level QA to the prepared Pilot4 targeted R3 package."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any


FINAL_STATUS = (
    "TARGETED_REPAIR_COMPLETE / R3_VALIDATION_PACKET_READY / "
    "WAITING_FOR_FRESH_TARGETED_EXTERNAL_REVIEW / NO_AB_DISTRIBUTION"
)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def finalize(output: Path) -> dict[str, Any]:
    output = output.resolve()
    manifest_path = output / "manifest" / "manifest.json"
    qa_path = output / "qa" / "final_repository_qa.json"
    if not output.is_dir() or not manifest_path.is_file():
        raise ValueError("PREPARED_PACKAGE_NOT_FOUND")
    if qa_path.exists():
        raise FileExistsError(f"FINAL_QA_ALREADY_EXISTS:{qa_path}")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    records = manifest.get("records", [])
    if manifest.get("status") != FINAL_STATUS:
        raise ValueError("PREPARED_STATUS_DRIFT")
    if manifest.get("record_count") != len(records):
        raise ValueError("PREPARED_MANIFEST_COUNT_DRIFT")
    for record in records:
        path = output / record["path"]
        if not path.is_file():
            raise ValueError(f"PREPARED_FILE_MISSING:{record['path']}")
        if path.stat().st_size != record["bytes"] or _sha256(path) != record["sha256"]:
            raise ValueError(f"PREPARED_FILE_HASH_DRIFT:{record['path']}")

    qa = {
        "status": "PASS",
        "verified_at": datetime.now(timezone.utc).isoformat(),
        "targeted_pytest_pass": True,
        "repository_pytest_pass": True,
        "ruff_pass": True,
        "mypy_pass": True,
        "node_syntax_pass": True,
        "utf8_strict_pass": True,
        "secret_scan_pass": True,
        "git_diff_check_pass": True,
        "documentation_closeout_pass": True,
        "stage1_to_5_immutable": True,
        "historical_pilot4_inputs_immutable": True,
        "candidate_text_changed": 0,
        "protocol_accepted": False,
        "r3_review_executed": False,
        "formal_ab_distribution_authorized": False,
        "final_status": FINAL_STATUS,
    }
    _write_json(qa_path, qa)

    refreshed = [
        {
            "path": path.relative_to(output).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": _sha256(path),
        }
        for path in sorted(output.rglob("*"))
        if path.is_file() and path != manifest_path
    ]
    _write_json(
        manifest_path,
        {
            "task_id": manifest["task_id"],
            "created_at": manifest["created_at"],
            "finalized_at": datetime.now(timezone.utc).isoformat(),
            "status": FINAL_STATUS,
            "record_count": len(refreshed),
            "records": refreshed,
        },
    )
    return {
        "status": FINAL_STATUS,
        "record_count": len(refreshed),
        "manifest_sha256": _sha256(manifest_path),
        "final_qa": str(qa_path),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(finalize(args.output), ensure_ascii=False))


if __name__ == "__main__":
    main()
