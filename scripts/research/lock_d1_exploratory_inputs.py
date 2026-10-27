"""Byte-preserve AI-assisted review inputs without promoting them to GT."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

FILENAMES = (
    "D1_BOUNDED54_AI_ASSISTED_ADJUDICATION_V2.xlsx",
    "d1_bounded54_decision_records.json",
    "D1_54_ADJUDICATION_AND_PILOT_READOUT.md",
)


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def save_new(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = (
        value
        if isinstance(value, bytes)
        else (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()
    )
    with path.open("xb") as stream:
        stream.write(raw)


def lock_inputs(source_dir: Path, output: Path) -> dict[str, Any]:
    if output.exists():
        raise ValueError("Fresh raw namespace required")
    manifest = []
    for name in FILENAMES:
        source = source_dir / name
        raw = source.read_bytes()
        target = output / name
        save_new(target, raw)
        if target.read_bytes() != source.read_bytes():
            raise ValueError("Raw/source byte stability failed")
        target.chmod(0o444)
        manifest.append(
            {
                "source": str(source),
                "locked_path": name,
                "sha256": digest(raw),
                "bytes": len(raw),
                "source_stability_verified": True,
            }
        )
    result = {
        "locked_at_utc": datetime.now(timezone.utc).isoformat(),
        "files": manifest,
        "initial_readonly_preview_before_lock": True,
        "source_unchanged_at_lock": True,
        "input_kind": "OWNER_SUPPLIED_AI_ASSISTED_QA_RECOMMENDATIONS",
        "approved_GT": False,
        "no_workbook_save_or_normalization": True,
    }
    save_new(output / "RAW_LOCK_MANIFEST_V1.json", result)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = lock_inputs(args.source_dir, args.output)
    print(json.dumps({"locked": len(result["files"]), "GT_promoted": False}))
