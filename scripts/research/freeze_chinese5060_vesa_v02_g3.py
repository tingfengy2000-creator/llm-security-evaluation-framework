"""Freeze one role-blind Owner14 G3-v0.2 context per original world, with no network."""
# ruff: noqa: E402 -- Isolated launcher adds only the repository source and adapter directories.
from __future__ import annotations

import json
import os
import shutil
import sys
from collections import Counter
from dataclasses import asdict
from pathlib import Path
from time import perf_counter_ns
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from freeze_chinese5060_vesa_g3 import BASE, INPUTS, P2, PAIR, SYSTEM_SHA, git, require, role_blind_chunks

from llmguard.domains.retrieval.hidden_poisoning.chinese5060.pilot_admission import json_bytes
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.pilot_design import (
    SYSTEM_TEMPLATE,
    canonical_hash,
    messages,
    select_contexts,
)
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.pilot_transport import encode
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.vesa_guard_v01 import sha
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.vesa_guard_v02 import RULE_SHA, select_v02

DEST = BASE / "W1-5060-VESA-V02-OWNER14-G3-01"
OWNER = ROOT / (
    "docs/paper1/dual_machine/owner_approvals/W1_5060_VESA_GUARD_V02_FAST_REVISION_AND_G3_AUTH_20261105.md"
)
CONTROL = ROOT / "docs/paper1/dual_machine/chinese5060/W1_5060_VESA_GUARD_V02_FAST_G3_EXECUTION_PROMPT_V1.md"
CONTROL_PINS = {
    OWNER: "64a0255c8d2cc5c94e25590f2cc0c8560f981c6de5abb38bc905f136ed318dc4",
    CONTROL: "74c05e3206f2d1d7fe7d446d8a1d61829208f7d77312b159bc24a697312b6bb8",
}
SRC = ROOT / "src/llmguard/domains/retrieval/hidden_poisoning/chinese5060"
CODE = (Path(__file__).resolve(), ROOT / "scripts/research/freeze_chinese5060_vesa_g3.py",
        *(SRC / (name + ".py") for name in (
            "vesa_guard_v02", "vesa_guard_v01", "pilot_admission", "pilot_design", "pilot_transport")))
GRID = "G3_V02_OFFLINE_GRID_PRIVATE.json"
TRACE = "G3_V02_DECISIONS_PRIVATE.json"
SEAL = "G3_V02_OFFLINE_SEAL.json"


def audit_io(event: str, args: tuple[Any, ...]) -> None:
    if event.startswith(("socket.", "subprocess.")) or event in {"os.system", "os.listdir", "os.scandir"}:
        raise PermissionError("G3_V02_RUNTIME_ACCESS_DENIED")
    if event == "open":
        name, _, flags = args
        if not isinstance(name, (bytes, str)):
            raise PermissionError("G3_V02_FILE_ACCESS_DENIED")
        path = Path(os.fsdecode(name))
        writing = bool(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND))
        if (writing and path in {DEST / GRID, DEST / TRACE, DEST / SEAL}) or (not writing and path in INPUTS):
            return
        raise PermissionError("G3_V02_FILE_ACCESS_DENIED")


def write(name: str, value: Any) -> str:
    raw = json_bytes(value)
    with (DEST / name).open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    return sha(raw)


def run() -> None:
    require(ROOT.drive.upper() in {"D:", "E:"} and DEST.resolve() == DEST and not DEST.exists()
            and shutil.disk_usage(ROOT).free >= 20 * 1024**3, "G3_V02_REQUIRE_NEW_LOCAL_DE_AND_20GIB")
    require(git("branch", "--show-current").strip() == b"research/paper1-chinese-defense-5060"
            and not git("status", "--porcelain=v1"), "G3_V02_REQUIRE_CLEAN_5060")
    commit = git("rev-parse", "HEAD").decode().strip()
    code_hashes = {}
    for path in (*CONTROL_PINS, *CODE):
        raw = path.read_bytes()
        relative = path.relative_to(ROOT).as_posix()
        require(git("show", f"{commit}:{relative}") == raw, "G3_V02_COMMITTED_SOURCE_BYTES_REQUIRED")
        if path in CONTROL_PINS:
            require(sha(raw) == CONTROL_PINS[path], "G3_V02_CONTROL_DRIFT")
        else:
            code_hashes[relative] = sha(raw)
    require(canonical_hash(SYSTEM_TEMPLATE) == SYSTEM_SHA, "G3_V02_SYSTEM_DRIFT")
    require(all(path.resolve() == path for path in INPUTS), "G3_V02_INPUT_REDIRECTED")
    sys.addaudithook(audit_io)
    raw_inputs = {path: path.read_bytes() for path in INPUTS}
    require(all(sha(raw) == INPUTS[path] for path, raw in raw_inputs.items()), "G3_V02_INPUT_HASH_DRIFT")
    pair = json.loads(raw_inputs[PAIR / "PAIR_OUTPUT_SEAL.json"])
    p2 = json.loads(raw_inputs[P2 / "OUTPUT_SEAL.json"])
    packets = json.loads(raw_inputs[PAIR / "PACKETS_PRIVATE.json"])
    baseline = json.loads(raw_inputs[PAIR / "B2_RESULTS_PRIVATE.json"])
    pair_pins = {Path(row["path"]).name: row["sha256"] for row in pair["records"]}
    topk_pins = {Path(row["path"]).parent.name: row["sha256"] for row in p2["records"]
                 if Path(row["path"]).name == "TOPK_PRIVATE.json"}
    require(len(packets) == len(baseline) == len(topk_pins) == len({r["world_id"] for r in packets}) == 36
            and pair["worlds"] == p2["worlds"] == 36
            and all(pair_pins[path.name] == INPUTS[path] for path in INPUTS if path.name in (
                "PACKETS_PRIVATE.json", "B2_RESULTS_PRIVATE.json")), "G3_V02_SEAL_INDEX_DRIFT")
    grid, trace, latency = [], [], []
    counts: Counter[str] = Counter()
    risk: Counter[str] = Counter()
    reasons: Counter[str] = Counter()
    for ordinal, (packet, b2) in enumerate(zip(packets, baseline, strict=True), 1):
        chunks = role_blind_chunks(packet)
        wid = packet["world_id"]
        require(b2["status"] == "PASS" and b2["world_id"] == wid and b2["snapshot_hash"] == packet["snapshot_hash"]
                and topk_pins[wid] == packet["original_TopK_file_sha256"], "G3_V02_WORLD_OR_TOPK_DRIFT")
        before = select_contexts(packet["chunks"], b2["removed_indices"], b2["retained_chunk_ids"])
        begin = perf_counter_ns()
        selected = select_v02(packet["query"], chunks, b2["retained_chunk_ids"])
        latency.append(perf_counter_ns() - begin)
        removed = [i for i, c in enumerate(chunks) if c.chunk_id in selected.removed_ids]
        context = select_contexts(packet["chunks"], removed, list(selected.retained_chunk_ids))
        msg = messages(packet["query"], context)
        body = json.loads(encode(msg))
        body["max_completion_tokens"] = body.pop("max_tokens")
        wire = json_bytes(body)
        world = canonical_hash({"world_id": wid, "snapshot_hash": packet["snapshot_hash"]})
        prompt = canonical_hash(msg)
        changed = canonical_hash(context) != canonical_hash(before)
        dropped = sorted(set(b2["retained_chunk_ids"]) - set(selected.retained_chunk_ids))
        grid.append({
            "ordinal": ordinal, "world_id": wid, "world_hash": world, "snapshot_hash": packet["snapshot_hash"],
            "arm": "G3", "query_hash": canonical_hash(packet["query"]), "prompt_hash": prompt,
            "request_id": "REQ-" + canonical_hash([world, "G3", prompt])[:24],
            "request_body_sha256": sha(wire), "wire": wire.decode(),
            "b2_context_sha256": canonical_hash(before), "g3_context_sha256": canonical_hash(context),
            "changed": changed,
        })
        trace.append({"ordinal": ordinal, "world_id": wid, "b2_retained_ids": b2["retained_chunk_ids"],
                      "newly_isolated_ids": dropped, "g3": asdict(selected)})
        counts.update({
            "parsed_query_worlds": bool(selected.query.slots and selected.query.titles),
            "parsed_chunk_count": sum(bool(t["facts"]) for t in selected.traces),
            "concrete_value_chunk_count": sum(any(f["value"] for f in t["facts"]) for t in selected.traces),
            "changed_worlds": changed, "restored_count": len(selected.restored_ids), "newly_isolated_count": len(dropped),
            "empty_contexts": not context, "covered_slots_before": len(selected.covered_before),
            "covered_slots_after": len(selected.covered_after),
        })
        risk.update(str(t["risk"]) for t in selected.traces)
        reasons.update(str(t["reason"]) for t in selected.traces if t["chunk_id"] in b2["removed_chunk_ids"])
    DEST.mkdir(exist_ok=False)
    files = {GRID: write(GRID, grid), TRACE: write(TRACE, trace)}
    record = {
        "status": "OFFLINE_GRID_FROZEN_AWAITING_INDEPENDENT_QA" if counts["changed_worlds"]
                  else "VESA_V02_NO_MEANINGFUL_DIFF",
        "source_commit": commit, "rule_sha256": RULE_SHA, "source_sha256": code_hashes,
        "worlds": 36, "topk_fragments": 180, "counts": dict(counts), "fragment_risk_counts": dict(risk),
        "b2_removed_reasons": dict(reasons), "selection_elapsed_ns": latency,
        "files_sha256": files, "role_blind_inputs": {p.name: h for p, h in INPUTS.items()},
        "owner_sha256": CONTROL_PINS[OWNER], "contract_sha256": CONTROL_PINS[CONTROL],
        "python": sys.version.split()[0], "third_party_algorithm_dependencies": [], "new_api_calls": 0,
    }
    print(json.dumps({"offline_seal_sha256": write(SEAL, record), **record}))


if __name__ == "__main__":
    run()
