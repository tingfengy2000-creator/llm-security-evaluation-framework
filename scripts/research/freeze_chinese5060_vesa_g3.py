"""Freeze one offline Owner13 G3 plan from only the pinned role-blind inputs."""
# ruff: noqa: E402 -- Isolated launcher adds the repository source directory.
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from collections import Counter
from dataclasses import asdict
from pathlib import Path
from time import perf_counter_ns
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.pilot_admission import json_bytes
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.pilot_design import (
    SYSTEM_TEMPLATE,
    canonical_hash,
    messages,
    select_contexts,
)
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.pilot_transport import encode
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.vesa_guard_v01 import (
    Chunk,
    rule_sha256,
    sha,
    vesa_select,
)

BASE = ROOT / "experiments/paper1_chinese5060"
PAIR = BASE / "W1-5060-FAST-B-20261105-PAIR01"
P2 = BASE / "W1-5060-P2-20261104-T0-01"
DEST = BASE / "W1-5060-VESA-V01-OWNER13-G3-01"
INPUTS = {
    PAIR / "PAIR_OUTPUT_SEAL.json": "bb775ead3d330f5e83516f8dfa871a3e2581c305e5ae7baf104500f781ac79fb",
    PAIR / "PACKETS_PRIVATE.json": "d0f196ab994a94bfd0804c37c08b81d41f582aaf2d74e143c26560ffa7043525",
    PAIR / "B2_RESULTS_PRIVATE.json": "9b65b5d7c412aea78a5d66f4d5402743afd029802eb0af981ebdd929376feb4f",
    P2 / "OUTPUT_SEAL.json": "4e11d89cb6f03291c124aab28f7181622b6766cc63d55be45126023147988c52",
}
OWNER_PATH = ROOT / (
    "docs/paper1/dual_machine/owner_approvals/W1_5060_VESA_GUARD_V01_FAST_METHOD_AND_G3_PILOT_AUTH_20261105.md"
)
OWNER_SHA = "59854a2a04e5799f79128e62206bad4daee1eb982c10aac877f74595ee325ee5"
CONTROL_PATH = ROOT / "docs/paper1/dual_machine/chinese5060/W1_5060_VESA_GUARD_V01_FAST_G3_EXECUTION_PROMPT_V1.md"
CONTROL_SHA = "b3b23da428f0fb574510c5fb84ca8b97d53bb58d43e6a63168cdb4e2c448033f"
SYSTEM_SHA = "b3c74613bc3700eacdce7dfedc382043013f452e321a13d8639b27817edbd1f1"
ALGORITHM = ROOT / "src/llmguard/domains/retrieval/hidden_poisoning/chinese5060/vesa_guard_v01.py"
GRID = "G3_OFFLINE_GRID_PRIVATE.json"
TRACE = "G3_DECISION_TRACE_PRIVATE.json"
SEAL = "G3_OFFLINE_SEAL.json"


def require(ok: bool, code: str) -> None:
    if not ok:
        raise ValueError(code)


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=ROOT)


def offline_io(event: str, args: tuple[Any, ...]) -> None:
    """Only four experiment inputs are reachable after entering the selection process."""
    if event.startswith(("socket.", "subprocess.")) or event in {"os.system", "os.listdir", "os.scandir"}:
        raise PermissionError("G3_RUNTIME_ACCESS_DENIED")
    if event == "open":
        name, _, flags = args
        if not isinstance(name, (bytes, str)):
            raise PermissionError("G3_FILE_ACCESS_DENIED")
        path = Path(os.fsdecode(name))
        writing = bool(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND))
        if writing and path in {DEST / GRID, DEST / TRACE, DEST / SEAL}:
            return
        if not writing and path in INPUTS:
            return
        raise PermissionError("G3_FILE_ACCESS_DENIED")


def _write(name: str, value: Any) -> str:
    raw = json_bytes(value)
    with (DEST / name).open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    return sha(raw)


def role_blind_chunks(packet: dict[str, Any]) -> list[Chunk]:
    require(set(packet) == {"world_id", "query", "original_TopK_file_sha256", "snapshot_hash", "chunks"}
            and bool(re.fullmatch(r"w-[a-f0-9]{24}", packet["world_id"]))
            and isinstance(packet["query"], str) and bool(packet["query"]) and len(packet["chunks"]) == 5,
            "G3_NON_ROLE_BLIND_PACKET")
    chunks = []
    for rank, row in enumerate(packet["chunks"], 1):
        require(set(row) == {"chunk_id", "text", "content_hash"}
                and bool(re.fullmatch(r"ch-[a-f0-9]{32}", row["chunk_id"])), "G3_NON_ROLE_BLIND_CHUNK")
        # The frozen packet supplies no verified production provenance or validity metadata.
        chunks.append(Chunk(row["chunk_id"], rank, row["text"], row["content_hash"]))
    return chunks


def run() -> None:
    require(ROOT.drive.upper() in {"D:", "E:"} and DEST.resolve() == DEST and not DEST.exists()
            and shutil.disk_usage(ROOT).free >= 20 * 1024**3, "G3_REQUIRE_NEW_LOCAL_DE_AND_20GIB")
    require(git("branch", "--show-current").strip() == b"research/paper1-chinese-defense-5060"
            and not git("status", "--porcelain=v1"), "G3_REQUIRE_CLEAN_5060")
    source_commit = git("rev-parse", "HEAD").decode().strip()
    control_pins = {OWNER_PATH: OWNER_SHA, CONTROL_PATH: CONTROL_SHA}
    code = {}
    for path in (*control_pins, ALGORITHM, Path(__file__).resolve()):
        raw = path.read_bytes()
        relative = path.relative_to(ROOT).as_posix()
        require(git("show", f"{source_commit}:{relative}") == raw, "G3_COMMITTED_SOURCE_BYTES_REQUIRED")
        if path in control_pins:
            require(sha(raw) == control_pins[path], "G3_CONTROL_DOCUMENT_DRIFT")
        else:
            code[relative] = sha(raw)
    require(canonical_hash(SYSTEM_TEMPLATE) == SYSTEM_SHA, "G3_ORIGINAL_SYSTEM_DRIFT")
    require(all(path.resolve() == path for path in INPUTS), "G3_INPUT_REDIRECTED")
    sys.addaudithook(offline_io)
    blobs = {path: path.read_bytes() for path in INPUTS}
    require(all(sha(raw) == INPUTS[path] for path, raw in blobs.items()), "G3_SEALED_INPUT_BYTES_DRIFT")
    pair = json.loads(blobs[PAIR / "PAIR_OUTPUT_SEAL.json"])
    p2 = json.loads(blobs[P2 / "OUTPUT_SEAL.json"])
    packets = json.loads(blobs[PAIR / "PACKETS_PRIVATE.json"])
    decisions = json.loads(blobs[PAIR / "B2_RESULTS_PRIVATE.json"])
    pair_pins = {Path(row["path"]).name: row["sha256"] for row in pair["records"]}
    p2_topk = {Path(row["path"]).parent.name: row["sha256"] for row in p2["records"]
               if Path(row["path"]).name == "TOPK_PRIVATE.json"}
    require(len(packets) == len(decisions) == len(p2_topk) == 36 and len({r["world_id"] for r in packets}) == 36
            and pair["worlds"] == p2["worlds"] == 36
            and all(pair_pins[path.name] == INPUTS[path] for path in INPUTS if path.name in (
                "PACKETS_PRIVATE.json", "B2_RESULTS_PRIVATE.json")), "G3_SEAL_INDEX_DRIFT")

    grid, trace = [], []
    reasons: Counter[str] = Counter()
    elapsed = []
    for ordinal, (packet, b2) in enumerate(zip(packets, decisions, strict=True), 1):
        chunks = role_blind_chunks(packet)
        wid = packet["world_id"]
        require(b2["status"] == "PASS" and b2["world_id"] == wid and b2["snapshot_hash"] == packet["snapshot_hash"]
                and p2_topk[wid] == packet["original_TopK_file_sha256"], "G3_WORLD_OR_TOPK_DRIFT")
        before = select_contexts(packet["chunks"], b2["removed_indices"], b2["retained_chunk_ids"])
        began = perf_counter_ns()
        decision = vesa_select(packet["query"], chunks, b2["retained_chunk_ids"])
        elapsed.append(perf_counter_ns() - began)
        removed = [rank for rank, chunk in enumerate(chunks) if chunk.chunk_id in decision.removed_ids]
        context = select_contexts(packet["chunks"], removed, list(decision.retained_chunk_ids))
        msg = messages(packet["query"], context)
        body = json.loads(encode(msg))
        body["max_completion_tokens"] = body.pop("max_tokens")
        wire = json_bytes(body)
        world_hash = canonical_hash({"world_id": wid, "snapshot_hash": packet["snapshot_hash"]})
        prompt = canonical_hash(msg)
        changed = canonical_hash(context) != canonical_hash(before)
        grid.append({
            "ordinal": ordinal, "world_id": wid, "world_hash": world_hash, "snapshot_hash": packet["snapshot_hash"],
            "arm": "G3", "query_hash": canonical_hash(packet["query"]), "prompt_hash": prompt,
            "request_id": "REQ-" + canonical_hash([world_hash, "G3", prompt])[:24],
            "request_body_sha256": sha(wire), "wire": wire.decode(),
            "b2_context_sha256": canonical_hash(before), "g3_context_sha256": canonical_hash(context),
            "changed_context_hash": changed,
        })
        trace.append({"ordinal": ordinal, "world_id": wid, "b2_retained_ids": b2["retained_chunk_ids"],
                      "b2_removed_ids": b2["removed_chunk_ids"], "g3": asdict(decision)})
        reasons.update(t.reason for t in decision.reasons_by_chunk if t.chunk_id in b2["removed_chunk_ids"])
    changes = sum(bool(row["changed_context_hash"]) for row in grid)
    require(not changes and not any(row["g3"]["restored_ids"] for row in trace), "G3_UNVERIFIED_CHANGE_STOP")
    DEST.mkdir(exist_ok=False)
    seals = {GRID: _write(GRID, grid), TRACE: _write(TRACE, trace)}
    result = {
        "status": "VESA_V01_OFFLINE_NO_SAFE_G3_DIFF", "source_commit": source_commit,
        "worlds": 36, "changed_worlds": changes, "restored_chunks": 0, "newly_removed_chunks": 0,
        "role_blind_packets": 36, "topk_chunks": 180, "production_source_attestations": 0,
        "reasons_for_b2_removed_chunks": dict(reasons), "guard_elapsed_ns": elapsed, "real_api_requests": 0,
        "python": sys.version.split()[0], "third_party_algorithm_dependencies": [],
        "algorithm_version_sha256": rule_sha256(), "source_sha256": code, "files_sha256": seals,
        "role_blind_input_sha256": {path.name: digest for path, digest in INPUTS.items()},
        "authority_sha256": OWNER_SHA, "contract_sha256": CONTROL_SHA,
        "next_gate": "NO_SAFE_CONTEXT_CHANGE_PAID_BRANCH_NOT_ENTERED",
    }
    print(json.dumps({"output_seal_sha256": _write(SEAL, result), **result}))


if __name__ == "__main__":
    run()
