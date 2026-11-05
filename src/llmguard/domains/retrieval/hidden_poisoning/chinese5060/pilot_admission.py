"""Offline admission arithmetic for the frozen 5060 Pilot."""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from decimal import ROUND_CEILING, Decimal, localcontext
from typing import Any

from .budget import admit_paid_batch

MODEL = "qwen3.7-plus-2026-05-26"
MAX_CALLS = 108
INPUT_CAP = 4096
OUTPUT_CAP = 256
HISTORICAL_USAGE_CNY = Decimal("7.611826")
HISTORICAL_OWNER_CNY = Decimal("7.528095914")
HISTORICAL_DELTA_CNY = HISTORICAL_USAGE_CNY - HISTORICAL_OWNER_CNY
RESERVE_FACTOR = Decimal("1.20")


class Stop(ValueError):
    """Sanitized stop code. Never pass provider text or credentials as a code."""


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, allow_nan=False, sort_keys=True) + "\n").encode()


def strict_json(raw: str | bytes) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            if key in result:
                raise Stop("JSON_DUPLICATE_FIELD")
            result[key] = value
        return result

    def reject_constant(_: str) -> None:
        raise Stop("JSON_NON_FINITE")

    try:
        return json.loads(raw, object_pairs_hook=pairs, parse_constant=reject_constant)
    except (ValueError, RecursionError) as exc:
        if isinstance(exc, Stop):
            raise
        raise Stop("INVALID_JSON") from None


def money(value: object) -> Decimal:
    if not isinstance(value, str) or not re.fullmatch(r"(?:0|[1-9][0-9]{0,8})(?:\.[0-9]{1,12})?", value):
        raise Stop("BUDGET_INVALID_DECIMAL")
    return Decimal(value)


def token_int(value: object) -> int:
    if type(value) is not int or value < 0:
        raise Stop("INVALID_TOKEN_COUNT")
    return value


def usd_ceiling(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.000000001"), rounding=ROUND_CEILING)


@dataclass(frozen=True)
class Tariff:
    input_rate: Decimal
    cached_rate: Decimal
    output_rate: Decimal
    usd_per_unit: Decimal

    def charge(self, prompt: int, cached: int, output: int) -> Decimal:
        with localcontext() as ctx:
            ctx.prec = 80
            native = self.input_rate * (prompt - cached) + self.cached_rate * cached + self.output_rate * output
            return usd_ceiling(native * self.usd_per_unit / Decimal(1_000_000))

    def max_cell(self) -> Decimal:
        return usd_ceiling(self.charge(INPUT_CAP, 0, OUTPUT_CAP) * RESERVE_FACTOR)


@dataclass(frozen=True)
class BudgetInput:
    tariff: Tariff
    settled: Decimal
    pending: Decimal
    available: Decimal
    batch_cap: Decimal

    @classmethod
    def from_manifest(cls, value: Any) -> BudgetInput:
        """Check a private Owner-bound numeric snapshot. Source authenticity is a separate gate."""
        required = {
            "model", "currency", "usd_per_billing_unit", "historical_usd_per_cny",
            "uncached_input_per_million", "cached_input_per_million", "output_per_million",
            "settled_all_streams_usd", "pending_all_streams_usd", "available_usd_before_pending",
            "batch_ceiling_usd", "includes_all_streams", "price_version", "as_of_utc", "evidence_sha256",
        }
        if not isinstance(value, dict) or set(value) != required:
            raise Stop("BUDGET_GATE_BLOCKED_MISSING_OR_UNRECOGNIZED_FIELDS")
        if value["model"] != MODEL or value["includes_all_streams"] is not True:
            raise Stop("BUDGET_MODEL_OR_ALL_STREAM_SCOPE_INVALID")
        if value["currency"] not in ("USD", "CNY"):
            raise Stop("BUDGET_CURRENCY_UNVERIFIED")
        if not isinstance(value["as_of_utc"], str) or not re.fullmatch(
            r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", value["as_of_utc"]
        ) or not isinstance(value["price_version"], str) or not value["price_version"].strip():
            raise Stop("BUDGET_VERSION_OR_TIME_MISSING")
        evidence = value["evidence_sha256"]
        if not isinstance(evidence, dict) or set(evidence) != {"price", "fx", "ledger", "balance"} or any(
            not isinstance(digest, str) or not re.fullmatch(r"[a-f0-9]{64}", digest) for digest in evidence.values()
        ):
            raise Stop("BUDGET_EVIDENCE_DIGESTS_REQUIRED")
        tariff = Tariff(*(money(value[key]) for key in (
            "uncached_input_per_million", "cached_input_per_million", "output_per_million", "usd_per_billing_unit"
        )))
        historical_fx = money(value["historical_usd_per_cny"])
        if (tariff.cached_rate > tariff.input_rate or not tariff.usd_per_unit or not historical_fx
                or not tariff.input_rate or not tariff.output_rate
                or (value["currency"] == "USD" and tariff.usd_per_unit != 1)):
            raise Stop("BUDGET_INVALID_RATE_OR_FX")
        settled, pending, available, cap = (money(value[key]) for key in (
            "settled_all_streams_usd", "pending_all_streams_usd", "available_usd_before_pending", "batch_ceiling_usd"
        ))
        if settled + pending < usd_ceiling(HISTORICAL_USAGE_CNY * historical_fx):
            raise Stop("BUDGET_HISTORICAL_FLOOR_OR_DELTA_MISSING")
        if not 0 < cap <= 30:
            raise Stop("BUDGET_INVALID_APPROVAL_CEILING")
        return cls(tariff, settled, pending, available, cap)


class Budget:
    """Serial reservations for one run, shared between mock and offline numeric admission."""
    def __init__(self, config: BudgetInput) -> None:
        self.config = config
        self.cell_max = config.tariff.max_cell()
        self.remaining = MAX_CALLS
        self.spent = Decimal(0)
        self.unsettled = Decimal(0)

    def check(self) -> str:
        reserved = self.cell_max * self.remaining
        cumulative = self.config.settled + self.spent
        pending = self.config.pending + self.unsettled
        if cumulative + pending >= 30:
            raise Stop("STOP_CUMULATIVE_30_USD")
        if cumulative + pending + reserved >= 28:
            raise Stop("STOP_NEW_BATCH_28_USD")
        if self.spent + self.unsettled + reserved > self.config.batch_cap:
            raise Stop("STOP_OWNER_BATCH_CEILING")
        if reserved == 0:
            return "NO_FURTHER_REQUESTS"
        status = admit_paid_batch(
            cumulative_usd=cumulative, pending_usd=pending,
            account_remaining_usd=self.config.available - self.spent,
            next_upper_usd=reserved, billing_verified=True,
        )
        if not status.startswith("ADMIT_"):
            raise Stop(status)
        return status

    def release_cell(self) -> None:
        if self.remaining <= 0:
            raise Stop("MAX_CALLS_EXHAUSTED")
        self.remaining -= 1

    def start(self) -> str:
        status = self.check()
        self.release_cell()
        self.unsettled += self.cell_max
        return status

    def settle(self, cost: Decimal) -> None:
        if self.unsettled < self.cell_max or not 0 <= cost <= self.cell_max:
            raise Stop("STOP_CELL_RESERVATION_EXCEEDED")
        self.spent += cost
        self.unsettled -= self.cell_max
        self.check()


def fake_budget() -> BudgetInput:
    """Deliberately synthetic. No account snapshot is needed for the fake run."""
    return BudgetInput(
        Tariff(Decimal("1"), Decimal("0.25"), Decimal("3"), Decimal("1")),
        Decimal("1.30"), Decimal("0.10"), Decimal("10"), Decimal("1"),
    )
