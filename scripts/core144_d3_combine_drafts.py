"""Combine four D3 HKP drafts in frozen fact order, without semantic approval."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--hkp1", type=Path, required=True)
    parser.add_argument("--hkp2", type=Path, required=True)
    parser.add_argument("--hkp3", type=Path, required=True)
    parser.add_argument("--hkp4", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError("Refusing to overwrite D3 draft")
    expected = [row["fact_id"] for row in json.loads(
        (args.contract / "canonical_fact_records.json").read_bytes())["facts"]]
    fragments = [args.hkp1, args.hkp2, args.hkp3, args.hkp4]
    rows = []
    for index, path in enumerate(fragments, start=1):
        value = json.loads(path.read_bytes())
        if value["domain"] != "D3" or len(value["triplets"]) != 12:
            raise ValueError(f"D3 HKP{index} draft cardinality failed")
        if any(not row["fact_id"].startswith(f"HKP{index}-")
               for row in value["triplets"]):
            raise ValueError(f"Wrong HKP draft in slot {index}")
        rows.extend(value["triplets"])
    if [row["fact_id"] for row in rows] != expected:
        raise ValueError("Draft order does not match locked fact order")
    obj = {"domain": "D3", "status": "UNRELEASED_DRAFT_AWAITING_SEMANTIC_AND_ABLATION_GATES",
           "fragment_shas": {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                             for path in fragments}, "triplets": rows}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(obj, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps({"groups": len(rows), "candidate_drafts": len(rows) * 3}))


if __name__ == "__main__":
    main()
