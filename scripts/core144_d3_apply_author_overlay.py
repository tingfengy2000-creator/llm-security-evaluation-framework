"""Apply exact atom-note expansions additively without rewriting V1 evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--overlay", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError("Refusing to overwrite author interpretation")
    data = json.loads(args.source.read_bytes())
    overlay = json.loads(args.overlay.read_bytes())
    groups = {row["fact_id"]: row for row in data["groups"]}
    for replacement in overlay["replacements"]:
        atoms = groups[replacement["fact_id"]][replacement["key"]]
        if atoms.count(replacement["old"]) != 1:
            raise ValueError("Replacement not uniquely found")
        atoms[atoms.index(replacement["old"])] = replacement["new"]
    data["status"] = "AUTHOR_NOTE_SPECIFICITY_REPAIRED_UNRELEASED"
    data["source_sha256"] = hashlib.sha256(args.source.read_bytes()).hexdigest()
    data["overlay_sha256"] = hashlib.sha256(args.overlay.read_bytes()).hexdigest()
    with args.output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps({"groups": len(groups), "replacements": len(overlay["replacements"])}))


if __name__ == "__main__":
    main()
