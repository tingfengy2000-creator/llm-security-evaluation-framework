"""Repair pre-release neutral queries additively, preserving candidate text."""

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
        raise ValueError("Refusing to overwrite pre-release draft")
    draft = json.loads(args.draft.read_bytes())
    overlay = json.loads(args.overlay.read_bytes())["query_replacements"]
    before = [(r["fact_id"], r["C"], r["P"], r["H"]) for r in draft["triplets"]]
    actual = {r["fact_id"] for r in draft["triplets"]}
    if not overlay.keys() <= actual:
        raise ValueError("Unknown query slot")
    for row in draft["triplets"]:
        if row["fact_id"] in overlay:
            row["query"] = overlay[row["fact_id"]]
    after = [(r["fact_id"], r["C"], r["P"], r["H"]) for r in draft["triplets"]]
    if before != after:
        raise ValueError("Candidate text changed during query-only repair")
    draft["status"] = "UNRELEASED_QUERY_NEUTRALITY_REPAIRED_AWAITING_GATES"
    draft["supersedes_draft_sha256"] = hashlib.sha256(args.draft.read_bytes()).hexdigest()
    draft["repair_overlay_sha256"] = hashlib.sha256(args.overlay.read_bytes()).hexdigest()
    with args.output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(draft, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps({"repaired_queries": len(overlay), "candidate_text_parity": True}))


if __name__ == "__main__":
    main()
