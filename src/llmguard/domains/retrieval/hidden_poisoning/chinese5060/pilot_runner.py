"""Fail-stop FakeTransport lifecycle and private evidence sealing."""
from __future__ import annotations

import os
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from time import monotonic
from typing import Any

from .pilot_admission import MAX_CALLS, MODEL, Budget, Stop, json_bytes, sha256, strict_json
from .pilot_inputs import CONTROL_SHA, PINNED_INPUTS, Cell, check_input_tokens, token_audit
from .pilot_offline import require_space
from .pilot_transport import WIRE_PATH, FakeTransport, parse_answer, parse_usage

FAULTS = frozenset({
    "timeout", "http", "missing_usage", "model", "non_json", "empty", "citation",
    "length", "hidden", "tool", "usage_over", "usage_drift",
})
SYNTHETIC_INPUT_TOKENS = 128


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


class Evidence:
    """Write once per artifact. Journal intent before sending, then fsync the outcome."""

    def __init__(self, directory: Path) -> None:
        self.directory = directory
        self.files: dict[str, str] = {}
        self.journal = directory / "JOURNAL_PRIVATE.jsonl"

    def write(self, name: str, raw: bytes) -> str:
        with (self.directory / name).open("xb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        digest = sha256(raw)
        self.files[name] = digest
        return digest

    def record(self, name: str, value: Any) -> str:
        return self.write(name, json_bytes(value))

    def append(self, value: dict[str, Any]) -> None:
        with self.journal.open("ab") as stream:
            stream.write(json_bytes(value))
            stream.flush()
            os.fsync(stream.fileno())

    def seal(self, summary: dict[str, Any]) -> str:
        if self.journal.exists():
            self.files[self.journal.name] = sha256(self.journal.read_bytes())
        self.record("RUN_MANIFEST.json", summary)
        return self.record("OUTPUT_SEAL.json", {
            "schema": "W1_5060_PILOT_RUNNER_V1", "mode": "FAKE",
            "cells": MAX_CALLS, "evaluation": "DENIED_FAKE_OUTPUT",
            "files_sha256": dict(self.files),
        })


def require_evaluation_release(mode: str) -> None:
    """There is no approved evaluator in this build, even after a mock seal exists."""
    if mode == "FAKE":
        raise Stop("EVALUATION_DENIED_MOCK_OUTPUT")
    raise Stop("EVALUATION_REQUIRES_APPROVED_INDEPENDENT_LIVE_SEAL")


def _attempt(
    row: dict[str, Any], cell: Cell, evidence: Evidence, budget: Budget,
    transport: FakeTransport, input_tokens: int, ordinal: int,
) -> None:
    require_space(evidence.directory)
    count = check_input_tokens(input_tokens)
    if not cell.citations:
        budget.release_cell()
        row.update(status="MOCK_LOCAL_ABSTAIN", response_status="ABSTAIN")
        return
    warning = budget.start()
    row.update(synthetic_input_tokens=count, budget_decision=warning,
               mock_cell_reservation_usd=str(budget.cell_max))
    evidence.append({
        "event": "FAKE_SEND_INTENT", "request_id": cell.request_id, "ordinal": ordinal,
        "request_body_sha256": row["request_body_sha256"], "attempt": 1, "time_utc": now(),
        "mock_reserved_usd": str(budget.cell_max),
    })
    started = monotonic()
    try:
        reply = transport.send(cell.body, count)
    finally:
        row["mock_elapsed_ms"] = round((monotonic() - started) * 1000, 3)
    row["http_status_fake"] = reply.status_code
    row["fake_request_id"] = reply.provider_request_id
    raw_file = f"RESPONSE_{ordinal:03d}.bin"
    row["raw_response_sha256"] = sha256(reply.body)
    evidence.write(raw_file, reply.body)
    row["raw_response_file"] = raw_file
    if reply.status_code != 200:
        raise Stop("HTTP_NON_SUCCESS")
    response = strict_json(reply.body)
    usage = parse_usage(response, count)
    cost = budget.config.tariff.charge(usage.prompt, usage.cached or 0, usage.output)
    row.update(mock_usage=usage.record(), mock_charge_upper_usd=str(cost),
               missing_cache_cost_policy="UNCACHED_UPPER_BOUND" if usage.cached is None else "FAKE_RECORDED_CACHE")
    budget.settle(cost)
    row["response_status"] = parse_answer(response, cell.citations)
    row["status"] = "MOCK_SUCCESS"


def run_fake(
    cells: list[Cell], evidence: Evidence, budget: Budget, transport: FakeTransport,
    source: dict[str, str], fake_token_override: dict[str, int] | None = None,
) -> dict[str, Any]:
    if type(transport) is not FakeTransport or transport.automatic_retries != 0 or transport.attempts != 0:
        raise Stop("PRISTINE_FAKE_TRANSPORT_ONLY")
    if len(cells) != MAX_CALLS:
        raise Stop("FROZEN_108_CELLS_REQUIRED")
    rows: list[dict[str, Any]] = [
        {**cell.index_row(), "status": "NOT_RUN", "real_status": "NOT_RUN", "mock_attempts": 0,
         "raw_response_sha256": None, "mock_usage": None, "mock_charge_upper_usd": None}
        for cell in cells
    ]
    evidence.record("PLAN_INDEX_PRIVATE.json", rows)
    stop_code = None
    started = now()
    for ordinal, (row, cell) in enumerate(zip(rows, cells, strict=True), 1):
        attempts_before = transport.attempts
        token_count = (fake_token_override or {}).get(cell.request_id, SYNTHETIC_INPUT_TOKENS)
        try:
            _attempt(row, cell, evidence, budget, transport, token_count, ordinal)
        except Stop as exc:
            stop_code = str(exc)
        except TimeoutError:
            stop_code = "TRANSPORT_TIMEOUT"
        except OSError:
            stop_code = "IO_OR_PERMISSION_STOP"
        row["mock_attempts"] = transport.attempts - attempts_before
        if stop_code:
            row.update(status="MOCK_FAILURE", failure_code=stop_code)
        evidence.append({"event": "CELL_OUTCOME", **row})
        if stop_code:
            break
    evidence.record("OUTCOMES_PRIVATE.json", rows)
    summary: dict[str, Any] = {
        "run_id": evidence.directory.name, "mode": "FAKE", "status": "MOCK_STOPPED" if stop_code else "MOCK_COMPLETE",
        "started_at_utc": started, "completed_at_utc": now(), "stop_code": stop_code,
        "control_commit": CONTROL_SHA, "source_file_sha256": source, "frozen_inputs_sha256": PINNED_INPUTS,
        "worlds": 36, "cells": MAX_CALLS, "unique_prompts": len({c.prompt_hash for c in cells}),
        "outcomes": dict(Counter(row["status"] for row in rows)), "mock_calls": transport.attempts,
        "real_api_calls": 0, "real_cost_usd": "0", "real_generation": "NOT_RUN",
        "mock_usage_source": "SYNTHETIC_FIXTURE", "mock_cost_usd": str(budget.spent),
        "mock_failed_unsettled_reservation_usd": str(budget.unsettled),
        "mock_unused_reservation_released_usd": str(budget.remaining * budget.cell_max),
        "mock_whole_batch_reservation_usd": str(MAX_CALLS * budget.cell_max),
        "historical_account_mutated": False, "model": MODEL, "wire": "WIRE_UNVERIFIED",
        "wire_candidate_path": WIRE_PATH, "candidate_timeouts_seconds": {"connect": 10, "read": 60, "overall": 90},
        "concurrency": 1, "automatic_retries": 0, "manual_retries": 0, "judge": 0, "probes": 0,
        "token_audit": token_audit(cells), "evaluation": "DENIED_FAKE_OUTPUT",
        "HumanGold": 0, "targeted_ASR": "NOT_MEASURED", "formal_qa": "NOT_MEASURED",
    }
    seal = evidence.seal(summary)
    return {**summary, "output_seal_sha256": seal}
