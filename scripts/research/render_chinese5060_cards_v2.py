"""Presentation-only projection: remove prior AI comparison hints from Owner cards."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    index = json.loads((args.input / "CARD_INDEX_PUBLIC.json").read_text(encoding="utf-8"))
    if index["cards"] != 12 or index["human_gold"] != 0:
        raise ValueError("EXACT_PROVISIONAL_12_REQUIRED")
    args.output.mkdir(parents=True, exist_ok=False)
    rows = []
    for row in index["index"]:
        path = args.input / (row["card_id"] + "_PRIVATE.json")
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != row["sha256"]:
            raise ValueError("CARD_SOURCE_CHANGED")
        card = json.loads(raw)
        card["answer_atoms_provisional"] = [{k: fact[k] for k in ("field", "value", "citations")}
                                            for fact in card["answer_atoms_provisional"]]
        card["presentation_version"] = "V2_NO_PRIOR_AI_COMPARISON_HINTS"
        target = args.output / path.name
        target.write_bytes((json.dumps(card, ensure_ascii=False, indent=2) + "\n").encode())
        rows.append({"card_id": row["card_id"], "sha256": hashlib.sha256(target.read_bytes()).hexdigest(), "fact_atoms": row["fact_atoms"]})
    summary = {**index, "index": rows, "presentation_version": "V2_NO_PRIOR_AI_COMPARISON_HINTS",
               "prior_index_sha256": hashlib.sha256((args.input / "CARD_INDEX_PUBLIC.json").read_bytes()).hexdigest(),
               "renderer_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               "facts_queries_citations_changed": False}
    (args.output / "CARD_INDEX_PUBLIC.json").write_bytes((json.dumps(summary, ensure_ascii=False, indent=2) + "\n").encode())
    print(json.dumps({"cards": 12, "human_gold": 0, "presentation_only": True, "new_API_calls": 0}))


if __name__ == "__main__":
    main()
