"""Materialize 108 DESIGN_ONLY request plans from old role-free packets; never send."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from llmguard.domains.retrieval.hidden_poisoning.chinese5060.pilot_design import canonical_hash, length_plan, messages, select_contexts
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.readonly_analysis import VerifiedReader


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--allowlist", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    reader = VerifiedReader(args.root, json.loads(args.allowlist.read_bytes()))
    packet_key = next(k for k in reader.allow if k.endswith("/PACKETS_PRIVATE.json"))
    packets = reader.json(packet_key)
    results = {}
    for arm, name in (("G1", "B1"), ("G2", "B2")):
        key = next(k for k in reader.allow if k.endswith("/" + name + "_RESULTS_PRIVATE.json"))
        results[arm] = {r["world_id"]: r for r in reader.json(key)}
    if len(packets) != 36 or any(len(r) != 36 for r in results.values()):
        raise ValueError("FROZEN_36_WORLD_INPUTS_REQUIRED")
    private_rows: list[dict[str, Any]] = []
    public_rows: list[dict[str, Any]] = []
    for packet in packets:
        wid = packet["world_id"]
        whash = canonical_hash({"world_id": wid, "snapshot_hash": packet["snapshot_hash"]})
        for arm in ("G0", "G1", "G2"):
            if arm == "G0":
                removed, retained = [], [c["chunk_id"] for c in packet["chunks"]]
            else:
                result = results[arm][wid]
                if result["status"] != "PASS" or result["snapshot_hash"] != packet["snapshot_hash"]:
                    raise ValueError("ORIGINAL_FILTER_RESULT_NOT_QUALIFIED")
                removed, retained = result["removed_indices"], result["retained_chunk_ids"]
            contexts = select_contexts(packet["chunks"], removed, retained)
            msg = messages(packet["query"], contexts)
            request_id = "REQ-" + canonical_hash([whash, arm, canonical_hash(msg)])[:24]
            row = {"request_id": request_id, "world_hash": whash, "arm": arm, "status": "NOT_RUN",
                "prompt_hash": canonical_hash(msg), "query_hash": canonical_hash(packet["query"]),
                "retained_chunk_count": len(contexts), "input_length_plan": length_plan(msg),
                "actual_input_tokens": None, "actual_output_tokens": None, "latency": None, "actual_cost": None,
                "input_cap_candidate": 4096, "max_output_tokens_candidate": 256,
                "price_version": "UNKNOWN_NOT_VERIFIED", "empty_policy": "LOCAL_ABSTAIN_NO_API" if not contexts else "ONE_REQUEST_AFTER_NEW_OWNER_APPROVAL"}
            public_rows.append(row)
            private_rows.append({**row, "world_id": wid, "query": packet["query"], "messages": msg,
                "retained_chunk_ids": retained, "original_snapshot_hash": packet["snapshot_hash"]})
    if len(private_rows) != 108 or len({r["request_id"] for r in private_rows}) != 108:
        raise ValueError("EXACT_108_PLAN_CELLS_REQUIRED")
    args.output.mkdir(exist_ok=False)
    def write(name, value):
        (args.output / name).write_bytes((json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode())
    write("GENERATOR_REQUEST_PLAN_PRIVATE.json", private_rows)
    write("REQUEST_PLAN_PUBLIC.json", public_rows)
    write("GENERATOR_DESIGN_ACCESS_LOG.json", reader.events)
    write("GENERATOR_DESIGN_LOCK.json", {"status": "DESIGN_ONLY_NOT_RUN", "cells": 108,
        "private_plan_hash": canonical_hash(private_rows), "public_plan_hash": canonical_hash(public_rows),
        "new_model_calls": 0, "new_API_calls": 0})
    print(json.dumps({"cells": 108, "worlds": 36, "unique_question_hashes": len({r["query_hash"] for r in public_rows}),
        "empty_cells": sum(r["retained_chunk_count"] == 0 for r in public_rows),
        "proxy_over_4096": sum(r["input_length_plan"]["proxy_over_4096"] for r in public_rows), "new_API_calls": 0}))


if __name__ == "__main__":
    main()
