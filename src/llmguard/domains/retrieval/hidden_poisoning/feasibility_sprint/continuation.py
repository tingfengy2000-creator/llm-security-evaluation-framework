"""Owner-A continuation: immutable prefix and paid-response reuse, no retries."""
from __future__ import annotations

import hashlib
import shutil
from pathlib import Path
from typing import Any

from .api import MODEL, PaidClient, request_body, write_new
from .contracts import digest, loads
from .runtime import Engine

PARENT_INDEX_SHA = "9055fca39ddc455e1df7f6e6d5ff989bcc8e94e0068055c1f2c0f50f3d096ffa"
PARENT_ARCHIVE_SHA = "34680b4cdb7e4c90a46942f2cea7b1bebec23f73a680342270a43ee0d579481b"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_parent(task: Path, repo: Path) -> dict[str, Any]:
    index_path = task / "ATTEMPT01_PRIVATE_EVIDENCE_INDEX.json"
    if sha(index_path) != PARENT_INDEX_SHA or sha(task / "FEASIBILITY_BEIJING_ATTEMPT01_PRIVATE_EVIDENCE.zip") != PARENT_ARCHIVE_SHA:
        raise RuntimeError("PARENT_ARCHIVE_OR_INDEX_CHANGED")
    index = loads(index_path.read_text("utf-8"))
    for entry in index["files"]:
        p = (task / entry["path"]).resolve()
        if not p.is_relative_to(task.resolve()) or sha(p) != entry["sha256"]:
            raise RuntimeError("PARENT_EVIDENCE_CHANGED")
    parent = task / "D1-DEV-BEIJING01"
    frozen = loads((parent / "CONFIG_LOCK.json").read_text("utf-8"))
    for suffix in ("/prompts.py", "/contracts.py", "/llm_verification.py", "/evaluate_paper1_feasibility.py"):
        matches = [p for p in frozen["source_hashes"] if p.endswith(suffix)]
        if len(matches) != 1 or sha(repo / matches[0]) != frozen["source_hashes"][matches[0]]:
            raise RuntimeError("SCIENTIFIC_CONTRACT_CHANGED")
    stop = loads((parent / "HARD_STOP.json").read_text("utf-8"))
    if stop["completed_candidate_packages"] != 52 or stop["failed_kind"] != "direct" or stop["failed_finish_reason"] != "length":
        raise RuntimeError("PARENT_STOP_NOT_OWNER_A_CASE")
    return {"index_sha256": PARENT_INDEX_SHA, "archive_sha256": PARENT_ARCHIVE_SHA,
            "partial_lock_sha256": sha(parent / "PARTIAL_ARCHIVAL_LOCK.json"),
            "parent_config": frozen, "complete_prefix": 52}


class ReplayClient:
    def __init__(self, live: PaidClient, cached: dict[str, dict[str, Any]]):
        self.live, self.cached = live, cached
        self.used: set[str] = set()
        self.enabled = True

    def call(self, messages: list[dict[str, str]], kind: str, max_output: int, probe: bool = False) -> dict[str, Any]:
        key = digest(request_body(messages, max_output))
        if not self.enabled or key not in self.cached:
            return self.live.call(messages, kind, max_output, probe)
        saved = self.cached[key]
        if saved["kind"] != kind or key in self.used:
            raise RuntimeError("REPLAY_KIND_OR_DUPLICATE_USE")
        response, receipt = saved["response"], saved["receipt"]
        if (response.get("model") != MODEL or response["choices"][0]["message"].get("reasoning_content")
                or receipt["thinking_tokens"] not in (None, 0)):
            raise RuntimeError("PARENT_RESPONSE_IDENTITY")
        choice = response["choices"][0]
        if choice["finish_reason"] not in {"stop", "length"}:
            raise RuntimeError("PARENT_RESPONSE_NOT_REUSABLE")
        self.used.add(key)
        return {"content": choice["message"]["content"], "call_id": saved["call_id"],
                "input_tokens": receipt["input_tokens"], "output_tokens": receipt["output_tokens"],
                "thinking_tokens": receipt["thinking_tokens"], "latency": receipt["latency"],
                "estimated_cost": receipt["charged_estimate_usd"],
                "native_estimated_cost": receipt["native_estimated_cost"], "native_currency": receipt["native_currency"],
                "response_sha256": digest(response), "finish_reason": choice["finish_reason"],
                "output_truncated": choice["finish_reason"] == "length", "reused_from_parent": True}


def pending_cache(task: Path, expected_bodies: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Bind only the partial candidate's two calls, never cache arbitrary rows."""
    cache: dict[str, dict[str, Any]] = {}
    for p in sorted((task / "api_calls").glob("*/request.json")):
        body = loads(p.read_text("utf-8"))
        key = digest(body)
        if key not in expected_bodies:
            continue
        reservation = loads(p.with_name("reservation.json").read_text("utf-8"))
        if reservation["request_sha256"] != key or key in cache:
            raise RuntimeError("PARENT_DUPLICATE_OR_REQUEST_HASH")
        receipt = loads(p.with_name("receipt.json").read_text("utf-8"))
        if sha(p.with_name("response.json")) != receipt["response_sha256"]:
            raise RuntimeError("PARENT_RESPONSE_HASH")
        cache[key] = {"call_id": p.parent.name, "kind": reservation["kind"], "receipt": receipt,
                      "response": loads(p.with_name("response.json").read_text("utf-8"))}
    if set(cache) != set(expected_bodies):
        raise RuntimeError("PARTIAL_CANDIDATE_CACHE_INCOMPLETE")
    return cache


def continue_predictions(engine: Engine, rows: list[dict[str, Any]], parent: Path, run: Path,
                         config_sha: str, prefix_count: int = 52) -> None:
    ids = [r["candidate_id"] for r in rows]
    if len(ids) != len(set(ids)):
        raise RuntimeError("DUPLICATE_INPUT_IDS")
    predictions: list[dict[str, Any]] = []
    prefix_hashes: dict[str, str] = {}
    for index, row in enumerate(rows):
        name = f"candidate-{index:03d}.json"
        dest = run / "raw" / name
        if index < prefix_count:
            original = parent / "raw" / name
            outputs = loads(original.read_text("utf-8"))
            if set(outputs) != {"E1", "E2", "E3", "E4"} or any(p["candidate_id"] != row["candidate_id"] or p["input_sha256"] != digest(row) for p in outputs.values()):
                raise RuntimeError("PREFIX_INPUT_BINDING")
            dest.parent.mkdir(parents=True, exist_ok=True)
            if dest.exists():
                raise RuntimeError("NO_OVERWRITE_CONTINUATION")
            shutil.copyfile(original, dest)
            if sha(original) != sha(dest):
                raise RuntimeError("PREFIX_NOT_BYTE_IDENTICAL")
            prefix_hashes[name] = sha(original)
        else:
            outputs = engine.predict(row, e4=True)
            write_new(dest, outputs)
            if index == prefix_count and isinstance(engine.client, ReplayClient):
                # The recovery cache belongs only to this input identity.
                if engine.client.used != set(engine.client.cached):
                    raise RuntimeError("PARTIAL_CACHE_NOT_FULLY_CONSUMED")
                engine.client.enabled = False
        predictions.extend(outputs.values())
    # Physical costs are deduplicated by immutable provider call ID, not by condition.
    calls: dict[str, dict[str, Any]] = {}
    for p in predictions:
        for record in p["call_records"]:
            if record["call_id"] in calls:
                for key in ("input_tokens", "output_tokens", "estimated_cost", "latency"):
                    if calls[record["call_id"]][key] != record[key]:
                        raise RuntimeError("SHARED_CALL_COST_CONFLICT")
            else:
                calls[record["call_id"]] = record
    write_new(run / "PREDICTIONS.json", predictions)
    write_new(run / "PREDICTION_LOCK.json", {"prediction_sha256": digest(predictions), "runtime_sha256": digest(rows),
               "config_lock_sha256": config_sha, "candidates": len(rows), "conditions": ["E1", "E2", "E3", "E4"],
               "ids_sha256": digest(ids), "unique_call_costs": list(calls.values()),
               "raw_files": {p.name: sha(p) for p in sorted((run / "raw").glob("*.json"))},
               "parent_prefix_byte_identical": prefix_hashes, "parent_failed_attempt_preserved": True,
               "owner_length_policy_revision": "PODR-157", "not_formal_test": True, "sealed_before_labels": True})
