"""Apply an additive, exact-slot D3 text repair without touching prior drafts."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--draft", type=Path, required=True)
    parser.add_argument("--overlay", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError("Refusing to overwrite draft")
    draft = json.loads(args.draft.read_bytes())
    overlay = json.loads(args.overlay.read_bytes())
    replacements = overlay["poison_text_replacements"]
    ids = {row["fact_id"] for row in draft["triplets"]}
    if not replacements.keys() <= ids:
        raise ValueError("Replacement references unknown slot")
    for row in draft["triplets"]:
        if row["fact_id"] in replacements:
            row["P"] = [replacements[row["fact_id"]]]
    draft["status"] = "UNRELEASED_SURFACE_REPAIRED_DRAFT_AWAITING_SEMANTIC_GATES"
    draft["supersedes_draft_sha256"] = hashlib.sha256(args.draft.read_bytes()).hexdigest()
    draft["repair_overlay_sha256"] = hashlib.sha256(args.overlay.read_bytes()).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(draft, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps({"repaired": len(replacements), "total": len(draft["triplets"])}))


if __name__ == "__main__":
    main()
