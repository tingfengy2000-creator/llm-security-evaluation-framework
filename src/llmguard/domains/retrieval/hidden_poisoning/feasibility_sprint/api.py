"""Official endpoint only; serial, durable reservations; no implicit retries."""
from __future__ import annotations

import hashlib
import json
import os
import re
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any, Callable

from .contracts import digest, loads

MODEL = "qwen3.7-plus-2026-05-26"
STOP = Decimal("4.50")
WARNING = Decimal("4.00")
RATES = {"Global": (Decimal("0.276"), Decimal("1.101")), "Japan": (Decimal("0.4"), Decimal("1.6"))}
CNY_PER_USD_FLOOR = Decimal("6")  # Budget bound, not a claimed spot exchange rate.
OWNER_A = "PODR-157"


def budget_limits(config: dict[str, Any]) -> tuple[Decimal, Decimal]:
    if "budget_total_usd" not in config:
        return WARNING, STOP
    if (config.get("owner_continuation_approval") == OWNER_A
            and config.get("budget_total_usd") == "15.00"
            and config.get("budget_warning_usd") == "14.00"
            and config.get("budget_hard_stop_usd") == "14.50"):
        return Decimal("14.00"), Decimal("14.50")
    raise ValueError("BUDGET_NOT_OWNER_APPROVED")


def request_body(messages: list[dict[str, str]], max_output: int) -> dict[str, Any]:
    return {"model": MODEL, "messages": messages, "enable_thinking": False,
            "temperature": 0, "stream": False, "max_completion_tokens": max_output,
            "response_format": {"type": "json_object"}, "enable_search": False}


def native_price(config: dict[str, Any], input_tokens: int, output_tokens: int) -> tuple[Decimal, str]:
    if any(type(n) is not int or n < 0 for n in (input_tokens, output_tokens)):
        raise ValueError("INVALID_USAGE")
    if input_tokens > 256000:
        raise ValueError("INPUT_TIER_NOT_FROZEN")
    if config.get("account_region") == "cn-beijing":
        return (Decimal(2) * input_tokens + Decimal(8) * output_tokens) / Decimal(1000000), "CNY"
    rate_in, rate_out = RATES[config["deployment_scope"]]
    return (rate_in * input_tokens + rate_out * output_tokens) / Decimal(1000000), "USD"


def write_new(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())


def price(config: dict[str, Any], input_tokens: int, output_tokens: int) -> Decimal:
    amount, currency = native_price(config, input_tokens, output_tokens)
    return amount / CNY_PER_USD_FLOOR if currency == "CNY" else amount


def token_bound(messages: list[dict[str, str]]) -> int:
    # UTF-8 byte count plus ample chat framing. A conservative byte-token envelope,
    # not a measured tokenizer count. Exceeding it stops subsequent requests.
    return sum(len(m["content"].encode("utf-8")) for m in messages) + 4096


def gate_issues(config: dict[str, Any], probe: bool = False) -> list[str]:
    issues = []
    try:
        budget_limits(config)
    except ValueError:
        issues.append("BUDGET_NOT_OWNER_APPROVED")
    if config.get("length_policy") not in (None, "INSUFFICIENT_NO_RETRY_OWNER_A") or (
            config.get("length_policy") is not None and config.get("owner_continuation_approval") != OWNER_A):
        issues.append("LENGTH_POLICY_NOT_OWNER_APPROVED")
    if config.get("model") != MODEL:
        issues.append("EXACT_MODEL_NOT_FROZEN")
    for key in ("owner_transfer_authorized", "license_and_confidentiality_confirmed", "official_terms_reviewed", "prices_verified"):
        if config.get(key) is not True:
            issues.append(key.upper())
    region = config.get("account_region")
    if not ((region == "ap-northeast-1" and config.get("deployment_scope") in RATES)
            or (region == "cn-beijing" and config.get("deployment_scope") == "ChinaMainland"
                and config.get("billing_currency") == "CNY" and config.get("budget_cny_per_usd_floor") == "6")):
        issues.append("ACCOUNT_REGION_OR_SCOPE_NOT_FROZEN")
    base = config.get("base_url", "")
    pattern = rf"https://(?:llm|ws)-[a-zA-Z0-9-]+\.{re.escape(str(region))}\.maas\.aliyuncs\.com/compatible-mode/v1"
    if not isinstance(base, str) or not re.fullmatch(pattern, base):
        issues.append("OFFICIAL_WORKSPACE_ENDPOINT_NOT_FROZEN")
    if not os.environ.get("DASHSCOPE_API_KEY", "").strip():
        issues.append("DASHSCOPE_API_KEY_MISSING")
    if config.get("validated_on_jst") != datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=9))).date().isoformat():
        issues.append("REVALIDATE_MODEL_PRICE_AND_TERMS_TODAY")
    if datetime.now(timezone.utc) >= datetime(2026, 11, 9, 15, tzinfo=timezone.utc):
        issues.append("SEVEN_DAY_SPRINT_WINDOW_EXPIRED")
    if not probe and config.get("synthetic_probe_receipt_sha256") is None:
        issues.append("LIVE_SYNTHETIC_NONTHINKING_PROBE_NOT_PASSED")
    return issues


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req: Any, fp: Any, code: int, msg: str, headers: Any, newurl: str) -> None:
        raise RuntimeError("REDIRECT_FORBIDDEN")


def official_transport(base_url: str, body: dict[str, Any], key: str) -> dict[str, Any]:
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    request = urllib.request.Request(base_url + "/chat/completions", data=json.dumps(body, ensure_ascii=False).encode(),
                                     headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"}, method="POST")
    try:
        with opener.open(request, timeout=120) as response:
            raw = response.read(16 * 1024 * 1024 + 1)
            if len(raw) > 16 * 1024 * 1024:
                raise RuntimeError("RESPONSE_SIZE_LIMIT")
            value = loads(raw.decode("utf-8"))
            if not isinstance(value, dict):
                raise RuntimeError("RESPONSE_SCHEMA")
            return value
    except urllib.error.HTTPError as exc:
        # Provider bodies may echo prompts or credentials: never print them.
        raise RuntimeError("PROVIDER_HTTP_" + str(exc.code)) from None
    except urllib.error.URLError:
        raise RuntimeError("TRANSPORT_UNCERTAIN_NO_RETRY") from None


class PaidClient:
    def __init__(self, root: Path, config: dict[str, Any], transport: Callable[..., dict[str, Any]] = official_transport):
        self.root, self.config, self.transport = root, config, transport
        self.events = root / "api_calls"
        self.events.mkdir(parents=True, exist_ok=True)

    def totals(self) -> tuple[Decimal, Decimal]:
        settled, pending = Decimal(0), Decimal(0)
        for path in self.events.glob("*/reservation.json"):
            receipt = path.with_name("receipt.json")
            if receipt.exists():
                settled += Decimal(loads(receipt.read_text("utf-8"))["charged_estimate_usd"])
            else:
                pending += Decimal(loads(path.read_text("utf-8"))["reserved_usd"])
        return settled, pending

    def call(self, messages: list[dict[str, str]], kind: str, max_output: int, probe: bool = False) -> dict[str, Any]:
        issues = gate_issues(self.config, probe=probe)
        if issues:
            raise RuntimeError("PAID_EXPERIMENT_BLOCKED:" + ",".join(issues))
        # A single run-wide lock is owned by the orchestration process; an additional
        # call lock protects direct use of this client. Crash leaves the lock intact.
        lock_path = self.root / "API_IN_FLIGHT.lock"
        try:
            lock_fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            raise RuntimeError("CONCURRENT_OR_UNRECONCILED_REQUEST") from None
        try:
            bound = token_bound(messages)
            worst = price(self.config, bound, max_output + 16)
            settled, pending = self.totals()
            if pending:
                raise RuntimeError("UNSETTLED_REQUEST_REQUIRES_OWNER_RECONCILIATION")
            warning, hard_stop = budget_limits(self.config)
            if settled + pending + worst >= hard_stop:
                raise RuntimeError("COST_HARD_STOP")
            request_id = f"{time.time_ns()}-{kind}"
            call_dir = self.events / request_id
            body = request_body(messages, max_output)
            write_new(call_dir / "reservation.json", {"kind": kind, "request_sha256": digest(body),
                       "input_token_bound": bound, "output_token_bound": max_output + 16,
                       "reserved_usd": str(worst), "warning": settled + worst >= warning})
            write_new(call_dir / "request.json", body)
            started = time.monotonic()
            try:
                response = self.transport(self.config["base_url"], body, os.environ["DASHSCOPE_API_KEY"])
                latency = time.monotonic() - started
                write_new(call_dir / "response.json", response)
                usage = response.get("usage", {})
                inputs, outputs = usage.get("prompt_tokens"), usage.get("completion_tokens")
                if type(inputs) is not int or type(outputs) is not int or inputs < 0 or outputs < 0:
                    raise RuntimeError("USAGE_MISSING_RESERVATION_RETAINED")
                if inputs > bound or outputs > max_output + 16:
                    raise RuntimeError("USAGE_BOUND_EXCEEDED_RESERVATION_RETAINED")
                cost = price(self.config, inputs, outputs)
                native_cost, currency = native_price(self.config, inputs, outputs)
                thinking = usage.get("completion_tokens_details", {}).get("reasoning_tokens")
                write_new(call_dir / "receipt.json", {"charged_estimate_usd": str(cost), "native_estimated_cost": str(native_cost),
                           "native_currency": currency, "usd_is_conservative_budget_bound": currency == "CNY", "input_tokens": inputs,
                           "output_tokens": outputs, "thinking_tokens": thinking, "latency": latency,
                           "response_sha256": hashlib.sha256((call_dir / "response.json").read_bytes()).hexdigest()})
                if response.get("model") != MODEL:
                    raise RuntimeError("RESPONSE_MODEL_IDENTITY_MISMATCH")
                choice = response["choices"][0]
                message = choice["message"]
                if message.get("reasoning_content") or thinking not in (None, 0):
                    raise RuntimeError("NONTHINKING_NOT_PROVED_NO_FALLBACK")
                truncated = choice.get("finish_reason") == "length"
                allow_length = self.config.get("length_policy") == "INSUFFICIENT_NO_RETRY_OWNER_A"
                if choice.get("finish_reason") != "stop" and not (truncated and allow_length):
                    raise RuntimeError("GENERATION_NOT_COMPLETE_NO_RETRY")
                if not isinstance(message.get("content"), str):
                    raise RuntimeError("RESPONSE_CONTENT_SCHEMA")
                return {"content": message["content"], "input_tokens": inputs, "output_tokens": outputs,
                        "thinking_tokens": thinking, "latency": latency, "estimated_cost": str(cost),
                        "native_estimated_cost": str(native_cost), "native_currency": currency,
                        "finish_reason": choice.get("finish_reason"), "output_truncated": truncated,
                        "call_id": request_id, "response_sha256": digest(response)}
            except BaseException as exc:
                write_new(call_dir / "incident.json", {"error_type": type(exc).__name__, "stop": True,
                           "no_automatic_retry": True, "reservation_retained_unless_receipt_exists": True})
                raise
        finally:
            os.close(lock_fd)
            lock_path.unlink()
