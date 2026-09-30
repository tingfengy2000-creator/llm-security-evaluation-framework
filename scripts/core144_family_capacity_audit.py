"""Abstract family-capacity feasibility; never select or export a data split."""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def inspect(facts: list[dict[str, Any]]) -> dict[str, Any]:
    cells: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for fact in facts:
        cells["-".join(fact["fact_id"].split("-")[:2])].append(fact)
    clusters = sorted({f["family_cluster_id"] for f in facts})
    failures = []
    for cell, members in cells.items():
        if len(members) != 4 or len({m["family"] for m in members}) != 4:
            failures.append({"cell": cell, "code": "CELL_FAMILY_NOT_FOUR_DISTINCT"})
        if len({m["core"] for m in members}) != 4:
            failures.append({"cell": cell, "code": "FACTUAL_CORE_NOT_FOUR_DISTINCT"})
    # Anonymous bins are not train/dev/test. No assignment, seed or split file
    # is retained. This checks existence of future capacity only.
    feasible = 0
    for bins in itertools.product(range(3), repeat=len(clusters)):
        capacity = dict(zip(clusters, bins, strict=True))
        if all(sorted(Counter(capacity[m["family_cluster_id"]]
                              for m in members).values()) == [1, 1, 2]
               for members in cells.values()):
            feasible += 1
    if not feasible:
        failures.append({"code": "FUTURE_CAPACITY_INFEASIBLE"})
    return {"groups": len(facts), "family_count": len({f["family"] for f in facts}),
            "conservative_cluster_count": len(clusters), "cells": cells,
            "anonymous_capacity_pattern": [2, 1, 1],
            "feasible_anonymous_capacity_count": feasible, "failures": failures,
            "split_executed": False, "assignment_exported": False,
            "status": "PASS_CAPACITY_ONLY" if not failures else "FAIL"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--facts", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = inspect(json.loads(args.facts.read_bytes())["facts"])
    with args.output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps({k: result[k] for k in ("groups", "family_count",
                     "conservative_cluster_count", "feasible_anonymous_capacity_count", "failures")}))


if __name__ == "__main__":
    main()
