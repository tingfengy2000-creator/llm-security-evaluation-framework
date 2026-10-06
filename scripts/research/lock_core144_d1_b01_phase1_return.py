"""Byte-lock HUMAN-B01 Phase1 before read-only validation of its individual gate."""

from __future__ import annotations

import argparse
import json
import shutil
import stat
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import openpyxl  # type: ignore[import-untyped]

from lock_core144_d1_human_phase1_return import read_json, sha256, validate_phase1, validate_phase2


PREFIX = "PAPER1_CORE144_D1_HUMAN_B01"
RAW_NAME = f"{PREFIX}_PHASE1_RAW_RETURN_V1.xlsx"
LOCK_NAME = f"{PREFIX}_PHASE1_RAW_LOCK_MANIFEST_V1.json"
VALIDATION_NAME = f"{PREFIX}_PHASE1_VALIDATION_V1.json"


def write_new_json(path: Path, value: dict[str, Any]) -> None:
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def lock_then_validate(
    source: Path,
    original_phase1: Path,
    phase1_manifest: Path,
    phase2: Path,
    phase2_manifest: Path,
    output_dir: Path,
) -> dict[str, Any]:
    """No workbook save, answer correction, comparison, or actual distribution."""
    inputs = (source, original_phase1, phase1_manifest, phase2, phase2_manifest)
    for path in inputs:
        if not path.is_file():
            raise FileNotFoundError(path)
    for path, suffix in ((phase1_manifest, "PHASE1"), (phase2_manifest, "PHASE2")):
        if read_json(path)["artifact"] != f"{PREFIX}_{suffix}_V1.xlsx":
            raise AssertionError("Expected the frozen B01 manifest, not A01 or another dataset")
    output_dir.mkdir(parents=True, exist_ok=True)
    raw = output_dir / RAW_NAME
    lock = output_dir / LOCK_NAME
    receipt = output_dir / VALIDATION_NAME
    if any(path.exists() for path in (raw, lock, receipt)):
        raise FileExistsError("Refusing to overwrite existing B01 evidence")
    input_hashes = {str(path): sha256(path) for path in inputs}
    shutil.copyfile(source, raw)
    if source.read_bytes() != raw.read_bytes() or sha256(raw) != input_hashes[str(source)]:
        raise AssertionError("Source changed or raw byte-copy verification failed")
    raw.chmod(stat.S_IREAD)
    write_new_json(lock, {
        "status": "IMMUTABLE_RAW_LOCKED_BEFORE_WORKBOOK_PARSE",
        "locked_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_name": source.name,
        "source_sha256": input_hashes[str(source)],
        "source_bytes": source.stat().st_size,
        "locked_artifact": RAW_NAME,
        "locked_sha256": sha256(raw),
        "locked_bytes": raw.stat().st_size,
        "locked_file_read_only": bool(
            getattr(raw.stat(), "st_file_attributes", 0)
            & getattr(stat, "FILE_ATTRIBUTE_READONLY", 1)
        ),
        "copy_method": "BYTE_FOR_BYTE_NO_EXCEL_RESAVE",
        "validation": "PENDING_SEPARATE_ADDITIVE_RECEIPT",
        "input_hashes": input_hashes,
    })
    result: dict[str, Any] = {
        "status": "FAIL_CLOSED",
        "phase2_release_authorized": False,
        "release_scope": "HUMAN-B01_ONLY",
        "phase2_distributed": False,
        "actual_distribution_observed": False,
        "ground_truth_created": False,
        "ab_comparison_performed": False,
    }
    try:
        result["phase1"] = validate_phase1(raw, original_phase1, phase1_manifest)
        book = openpyxl.load_workbook(raw, read_only=True, data_only=False)
        for row in book["【标注表】"].iter_rows(min_row=2, min_col=8, max_col=8):
            if row[0].value is not None and not isinstance(row[0].value, str):
                raise AssertionError("issue_note must be blank or plain text")
        book.close()
        result["phase2_release_file"] = validate_phase2(phase2, phase2_manifest, result["phase1"])
        if any(sha256(path) != input_hashes[str(path)] for path in inputs):
            raise AssertionError("An input changed during validation")
        result["status"] = "PASS"
        result["phase2_release_authorized"] = True
    except (AssertionError, ValueError, TypeError, KeyError, OSError) as error:
        result["blocking_error"] = f"{type(error).__name__}: {error}"
    finally:
        result["validated_at_utc"] = datetime.now(timezone.utc).isoformat()
        write_new_json(receipt, result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in (
        "source-raw", "original-phase1", "phase1-manifest", "phase2", "phase2-manifest", "output-dir"
    ):
        parser.add_argument(f"--{name}", type=Path, required=True)
    args = parser.parse_args()
    result = lock_then_validate(
        args.source_raw, args.original_phase1, args.phase1_manifest,
        args.phase2, args.phase2_manifest, args.output_dir,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
