"""One-shot transaction engine shared by synthetic QA and a future authorized process."""
from __future__ import annotations

import os
import re
from collections import Counter
from collections.abc import Callable
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from time import monotonic
from typing import Any

from .fast_unblock_admission import (
    LIVE_AUTHORITY_SHA256,
    V2_BILLABLE_CAP,
    CheckedAdmission,
    ReservedBudget,
    check_admission,
    check_live_authority,
    grid_digest,
    utc_now,
)
from .pilot_admission import INPUT_CAP, MAX_CALLS, Stop, json_bytes, sha256, strict_json
from .pilot_inputs import Cell, load_cells
from .pilot_live_admission import verify_projection
from .pilot_live_stage import StageProgress
from .pilot_live_transport import InterruptedResponse, _exchange, _install_socket_policy
from .pilot_offline import require_space
from .pilot_runner import Evidence, now
from .pilot_transport import FakeTransport, Reply, parse_answer, parse_usage

Send = Callable[[Cell, int, Callable[[str], None]], Reply]


@dataclass(frozen=True)
class RapidRun:
    output: Path
    request_grid_sha256: str
    evidence_manifest_sha256: str
    input_bounds: tuple[int, ...] = (INPUT_CAP,) * MAX_CALLS


class WaivedBatchCosts:
    """CNY list-price accounting for the one batch with an explicit USD waiver."""

    cell_max = Decimal("7.1486784")
    initial_reserve = Decimal("8.4737664")

    def __init__(self) -> None:
        self.remaining = MAX_CALLS
        self.spent = Decimal(0)
        self.unsettled = Decimal(0)

    def check(self) -> str:
        if self.unsettled or self.spent > self.initial_reserve:
            raise Stop("RAPID_CNY_ESTIMATE_OR_INFLIGHT_ANOMALY")
        return "SCOPED_OWNER_WAIVER_USAGE_METERED"

    def release_cell(self) -> None:
        if self.remaining <= 0:
            raise Stop("MAX_CALLS_EXHAUSTED")
        self.remaining -= 1

    def start(self) -> str:
        status = self.check()
        self.release_cell()
        self.unsettled = self.cell_max
        return status

    @staticmethod
    def charge(prompt: int, output: int) -> Decimal:
        # Full input list price is conservative even when usage includes cached tokens.
        return Decimal(2 * prompt + 8 * output) / 1_000_000

    def settle(self, cost: Decimal) -> None:
        if self.unsettled != self.cell_max or not 0 < cost <= self.charge(INPUT_CAP, V2_BILLABLE_CAP):
            raise Stop("RAPID_CNY_ESTIMATE_OR_INFLIGHT_ANOMALY")
        self.spent += cost
        self.unsettled = Decimal(0)
        self.check()


def _verify_reply(reply: Reply, cell: Cell, bound: int) -> tuple[dict[str, Any], int, int, int]:
    if reply.status_code != 200:
        raise Stop("LIVE_HTTP_NOT_200")
    response = strict_json(reply.body)
    if not isinstance(response, dict):
        raise Stop("INVALID_PROVIDER_ENVELOPE")
    provider_id = response.get("id")
    if not isinstance(provider_id, str) or not re.fullmatch(r"[A-Za-z0-9._:-]{1,192}", provider_id):
        raise Stop("LIVE_RESPONSE_ID_INVALID")
    usage_obj = response.get("usage")
    actual = usage_obj.get("prompt_tokens") if isinstance(usage_obj, dict) else None
    if type(actual) is not int:
        raise Stop("USAGE_MISSING")
    if actual > bound:
        raise Stop("LIVE_INPUT_PROOF_VIOLATION")
    usage = parse_usage(response, actual, output_cap=V2_BILLABLE_CAP)
    status = parse_answer(response, cell.citations)
    result = {"provider_response_id": provider_id, "usage": usage.record(), "answer_status": status}
    return result, usage.prompt, usage.cached or 0, usage.output


def _run(
    checked: CheckedAdmission | RapidRun, cells: list[Cell], send: Send, mode: str,
    *, admission_raw: bytes | None = None,
) -> dict[str, Any]:
    if len(cells) != MAX_CALLS or grid_digest(cells) != checked.request_grid_sha256:
        raise Stop("BATCH_GRID_DRIFT")
    rapid = isinstance(checked, RapidRun)
    if rapid and (admission_raw is None or sha256(admission_raw) != checked.evidence_manifest_sha256):
        raise Stop("RAPID_ADMISSION_RECEIPT_MISMATCH")
    budget = (ReservedBudget(checked.budget, max(checked.input_bounds), V2_BILLABLE_CAP)
              if isinstance(checked, CheckedAdmission) else WaivedBatchCosts())
    currency = "cny" if rapid else "usd"
    budget.check()
    require_space(Path(checked.output.anchor))
    checked.output.parent.mkdir(parents=True, exist_ok=True)
    try:
        # The future authorization binds the full absolute path. Reuse after a crash is refused.
        checked.output.mkdir(exist_ok=False)
    except FileExistsError:
        raise Stop("DUPLICATE_RUN_OR_SEND_INTENT") from None
    evidence = Evidence(checked.output)
    if admission_raw is not None:
        evidence.write("RAPID_LIVE_ADMISSION_MANIFEST.json", admission_raw)
    evidence.record("RUN_CLAIM.json", {
        "mode": mode, "admission_sha256": checked.evidence_manifest_sha256,
        "request_grid_sha256": checked.request_grid_sha256, "created_at_utc": now(),
    })
    stage = StageProgress()
    rows: list[dict[str, Any]] = [
        {**cell.index_row(), "ordinal": i, "status": "NOT_RUN", "attempted": False, "raw_response_sha256": None}
        for i, cell in enumerate(cells, 1)
    ]
    evidence.record("PLAN_INDEX_PRIVATE.json", rows)
    attempted = 0
    stop_code = None
    for ordinal, (row, cell, bound) in enumerate(zip(rows, cells, checked.input_bounds, strict=True), 1):
        if stage.begin() != ordinal:
            raise Stop("BATCH_STAGE_DRIFT")
        try:
            require_space(checked.output)
            if not cell.citations:
                budget.release_cell()
                row["answer_status"] = "ABSTAIN"
                row["local_context_empty"] = True
            else:
                row["budget_decision"] = budget.start()
                # Exclusive file plus append-only journal. A failed write prevents transmission.
                intent = {"event": "send_intent", "ordinal": ordinal, "request_id": cell.request_id,
                          "request_body_sha256": row["request_body_sha256"],
                          f"reserved_{currency}": str(budget.cell_max),
                          "mode": mode, "time_utc": now()}
                evidence.record(f"INTENT_{ordinal:03d}.json", intent)
                evidence.append(intent)
                row["attempted"] = True
                attempted += 1

                def record_post(phase: str) -> None:
                    evidence.record(f"POST_{ordinal:03d}_{phase}.json", {"ordinal": ordinal, "phase": phase})
                    row["post_phase"] = phase

                started = monotonic()
                try:
                    reply = send(cell, bound, record_post)
                finally:
                    row["elapsed_ms"] = round(1000 * (monotonic() - started), 3)
                row["http_status"] = reply.status_code
                row["provider_request_id"] = reply.provider_request_id
                row["raw_response_sha256"] = evidence.write(f"RESPONSE_{ordinal:03d}.bin", reply.body)
                result, prompt, cached, output = _verify_reply(reply, cell, bound)
                row.update(result)
                cost = (budget.charge(prompt, output) if isinstance(budget, WaivedBatchCosts)
                        else budget.config.tariff.charge(prompt, cached, output))
                budget.settle(cost)
                row[f"accounted_usage_charge_{currency}"] = str(cost)
            row["status"] = "SUCCESS"
            stage.finish(ordinal, engineering_success=True)
            evidence.append({"event": "cell_outcome", **row})
            if ordinal == 3:
                if not stage.initial3_passed:
                    raise Stop("FIRST_THREE_CHECKPOINT_FAILED")
                evidence.record("INITIAL3_CHECKPOINT.json", {"status": "ENGINEERING_PASS", "ordinal": 3, "mode": mode})
        except (Stop, OSError) as exc:
            if isinstance(exc, InterruptedResponse):
                row["raw_response_sha256"] = evidence.write(f"PARTIAL_{ordinal:03d}.bin", exc.partial)
            stop_code = str(exc) if isinstance(exc, Stop) else (
                "TRANSPORT_TIMEOUT" if isinstance(exc, TimeoutError) else "IO_OR_NETWORK_STOP"
            )
            row.update(status="FAIL", error_code=stop_code)
            evidence.append({"event": "cell_outcome", **row})
            break
    evidence.record("OUTCOMES_PRIVATE.json", rows)
    counts = Counter(row["status"] for row in rows)
    summary: dict[str, Any] = {
        "mode": mode, "status": "STOPPED" if stop_code else "COMPLETE", "stop_code": stop_code,
        "outcomes": {k: counts[k] for k in ("SUCCESS", "FAIL", "NOT_RUN")}, "slots": MAX_CALLS,
        "attempts": attempted, "real_posts_upper_by_send_intent": attempted if mode == "LIVE" else 0,
        "initial3_passed": "INITIAL3_CHECKPOINT.json" in evidence.files,
        "new_charge_usd": None if rapid else str(budget.spent) if mode == "LIVE" else "0",
        f"unsettled_reservation_{currency}": str(budget.unsettled),
        f"charge_estimate_{currency}": str(budget.spent),
        f"initial_batch_reservation_{currency}": str(
            budget.initial_reserve if isinstance(budget, WaivedBatchCosts) else budget.cell_max * MAX_CALLS
        ),
        "transport_retries": 0, "evaluation": "NOT_RUN", "completed_at_utc": now(),
    }
    if rapid and mode == "LIVE":
        summary.update(
            real_posts_sent=sum(row.get("post_phase") == "SENT" for row in rows),
            real_posts_delivery_uncertain=sum(row.get("post_phase") == "STARTED" for row in rows),
        )
    evidence.record("RUN_MANIFEST.json", summary)
    if evidence.journal.is_file():
        evidence.files[evidence.journal.name] = sha256(evidence.journal.read_bytes())
    seal = evidence.record("OUTPUT_SEAL.json", {"mode": mode, "slots": MAX_CALLS,
                                               "files_sha256": evidence.files.copy()})
    return {**summary, "output_seal_sha256": seal}


def run_synthetic(checked: CheckedAdmission, cells: list[Cell], transport: FakeTransport) -> dict[str, Any]:
    if type(transport) is not FakeTransport or transport.attempts != 0 or transport.automatic_retries != 0:
        raise Stop("PRISTINE_FAKE_TRANSPORT_ONLY")

    def send(cell: Cell, bound: int, _: Callable[[str], None]) -> Reply:
        reply = transport.send(cell.body, min(bound, 128))
        if reply.status_code != 200:
            return reply
        value = strict_json(reply.body)
        value["id"] = f"SYNTHETIC-{transport.attempts:03d}"
        fault = transport.faults.get(transport.attempts)
        if fault in ("billable_over", "billable_tolerance"):
            usage = value["usage"]
            usage["completion_tokens"] = V2_BILLABLE_CAP + int(fault == "billable_over")
            usage["total_tokens"] = usage["prompt_tokens"] + usage["completion_tokens"]
        return Reply(reply.status_code, json_bytes(value), reply.provider_request_id)

    return _run(checked, cells, send, "SYNTHETIC")


@dataclass(frozen=True)
class LiveInputs:
    root: Path
    output: Path
    source_commit: str
    config_raw: bytes
    original: list[Cell]
    candidate: list[Cell]
    required_sources: set[str]
    manifest_raw: bytes
    artifacts: dict[str, bytes]


def run_live(data: LiveInputs, authority_raw: bytes) -> dict[str, Any]:
    """Positive network path. The compile-time trust anchor is absent for Owner 11."""
    if LIVE_AUTHORITY_SHA256 is None:
        raise Stop("NEW_OWNER_LIVE_APPROVAL_REQUIRED")
    if sha256(authority_raw) != LIVE_AUTHORITY_SHA256:
        raise Stop("NEW_OWNER_LIVE_APPROVAL_REQUIRED")
    approval = strict_json(authority_raw)
    checked = check_admission(
        data.root, data.output, data.source_commit, approval["config_sha256"], data.config_raw,
        data.original, data.candidate, data.required_sources, data.manifest_raw,
        approval["admission_sha256"], data.artifacts, at=utc_now(),
    )
    check_live_authority(checked, authority_raw)
    frozen = load_cells(data.root)
    verify_projection(data.root, frozen)
    if frozen != data.original:
        raise Stop("LIVE_INPUTS_NOT_FROM_PINNED_PLAN")
    key = os.environ.get("DASHSCOPE_API_KEY")
    if not key:
        raise Stop("LIVE_CREDENTIAL_UNAVAILABLE")
    _install_socket_policy()

    def send(cell: Cell, _: int, _post_phase: Callable[[str], None]) -> Reply:
        return _exchange(checked.region, checked.host, cell.body, key)

    return _run(checked, data.candidate, send, "LIVE")
