"""Owner-A length accounting, immutable prefix reuse and shared budget tests."""
from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
from typing import Any

import pytest

from llmguard.domains.retrieval.hidden_poisoning.feasibility_sprint import api, continuation, contracts, runtime

FIXTURES = Path(__file__).with_name("test_paper1_feasibility_sprint.py")
spec = importlib.util.spec_from_file_location("sprint_fixtures", FIXTURES)
assert spec and spec.loader
fixtures = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixtures)


@pytest.fixture(autouse=True)
def clock(monkeypatch: Any) -> None:
    fixtures.freeze_api_clock.__wrapped__(monkeypatch)


def config_a() -> dict[str, Any]:
    return {**fixtures.beijing_config(), "owner_continuation_approval": api.OWNER_A,
            "length_policy": "INSUFFICIENT_NO_RETRY_OWNER_A", "budget_total_usd": "15.00",
            "budget_warning_usd": "14.00", "budget_hard_stop_usd": "14.50"}


def test_budget_increase_is_explicit_and_old_contract_retained() -> None:
    assert api.budget_limits(fixtures.config()) == (api.WARNING, api.STOP)
    assert tuple(map(str, api.budget_limits(config_a()))) == ("14.00", "14.50")
    bad = {**config_a(), "owner_continuation_approval": "unknown"}
    with pytest.raises(ValueError, match="NOT_OWNER_APPROVED"):
        api.budget_limits(bad)


def test_old_spend_counts_under_the_15_dollar_task_budget(tmp_path: Path, monkeypatch: Any) -> None:
    monkeypatch.setenv("DASHSCOPE_API_KEY", "fictional-test-key")
    api.write_new(tmp_path / "api_calls/old/reservation.json", {"reserved_usd": "14.499"})
    api.write_new(tmp_path / "api_calls/old/receipt.json", {"charged_estimate_usd": "14.499"})
    client = api.PaidClient(tmp_path, config_a(), lambda *args: pytest.fail("must not send"))
    with pytest.raises(RuntimeError, match="COST_HARD_STOP"):
        client.call([{"role": "user", "content": "fiction"}], "direct", 1024)


def test_length_response_returns_once_with_usage_under_owner_a(tmp_path: Path, monkeypatch: Any) -> None:
    monkeypatch.setenv("DASHSCOPE_API_KEY", "fictional-test-key")
    response = fixtures.response()
    response["choices"][0]["finish_reason"] = "length"
    count = 0
    def transport(*args: Any) -> dict[str, Any]:
        nonlocal count
        count += 1
        return response
    client = api.PaidClient(tmp_path, config_a(), transport)
    result = client.call([{"role": "user", "content": "fiction"}], "direct", 1024)
    assert count == 1 and result["output_truncated"] is True
    assert client.totals()[0] > 0 and client.totals()[1] == 0


@pytest.mark.parametrize("kind", ["internal", "direct", "structured", "followup"])
def test_all_truncated_components_are_insufficient_without_retry(kind: str) -> None:
    row = fixtures.row()
    class Truncated(fixtures.FakeClient):
        def call(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
            response = super().call(*args, **kwargs)
            response.update(output_truncated=True, finish_reason="length")
            return response
    client = Truncated(row)
    out = runtime.Engine(client).invoke(row, kind)
    assert out["final_verdict"] == "INSUFFICIENT" and out["parser_status"] == "OUTPUT_LIMIT"
    assert len(client.calls) == 1 and out["raw_output"]
    if kind == "internal":
        assert out["certificate_status"] == "NO_INTERNAL_CERTIFICATE"


def test_truncated_structured_does_not_trigger_paid_gap_repair() -> None:
    row = fixtures.row()
    class Truncated(fixtures.FakeClient):
        def call(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
            response = super().call(*args, **kwargs)
            response.update(output_truncated=True, finish_reason="length")
            return response
    client = Truncated(row, certify=False, missing=True)
    out = runtime.Engine(client).structured(row)
    assert out["parser_status"] == "OUTPUT_LIMIT" and client.calls == ["structured"]


def test_exact_cached_request_reuses_paid_length_response_without_http() -> None:
    messages = [{"role": "user", "content": "fiction"}]
    body = api.request_body(messages, 1024)
    response = fixtures.response()
    response["choices"][0]["finish_reason"] = "length"
    receipt = {"input_tokens": 100, "output_tokens": 20, "thinking_tokens": None, "latency": .2,
               "charged_estimate_usd": "0.00006", "native_estimated_cost": "0.00036", "native_currency": "CNY"}
    class NoLive:
        def call(self, *args: Any) -> Any:
            pytest.fail("cached call must not be resent")
    key = contracts.digest(body)
    cached = {key: {"kind": "direct", "call_id": "old-paid-call", "response": response, "receipt": receipt}}
    client = continuation.ReplayClient(NoLive(), cached)  # type: ignore[arg-type]
    result = client.call(messages, "direct", 1024)
    assert result["call_id"] == "old-paid-call" and result["output_truncated"] and client.used == {key}
    with pytest.raises(RuntimeError, match="DUPLICATE_USE"):
        client.call(messages, "direct", 1024)


def test_prefix_is_byte_identical_and_only_unfinished_rows_are_invoked(tmp_path: Path) -> None:
    parent, run = tmp_path / "parent", tmp_path / "continuation"
    row = fixtures.row()
    prefix = runtime.Engine(fixtures.FakeClient(row, certify=False)).predict(row, e4=True)
    api.write_new(parent / "raw/candidate-000.json", prefix)
    original = (parent / "raw/candidate-000.json").read_bytes()
    second = copy.deepcopy(row)
    second["candidate_id"] = "fiction-second"
    class UniqueCalls(fixtures.FakeClient):
        def call(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
            result = super().call(*args, **kwargs)
            result["call_id"] = "new-" + result["call_id"]
            return result
    client = UniqueCalls(second, certify=False)
    continuation.continue_predictions(runtime.Engine(client), [row, second], parent, run, "frozen", prefix_count=1)
    assert (run / "raw/candidate-000.json").read_bytes() == original
    assert client.calls == ["internal", "direct", "structured"]
    lock = json.loads((run / "PREDICTION_LOCK.json").read_text("utf-8"))
    assert len(lock["raw_files"]) == 2 and lock["parent_failed_attempt_preserved"] is True
    assert len(lock["unique_call_costs"]) == 6


def test_prefix_input_mismatch_stops_before_any_new_request(tmp_path: Path) -> None:
    row = fixtures.row()
    output = runtime.Engine(fixtures.FakeClient(row)).predict(row, e4=True)
    api.write_new(tmp_path / "parent/raw/candidate-000.json", output)
    changed = copy.deepcopy(row)
    changed["candidate_id"] = "changed"
    client = fixtures.FakeClient(row)
    with pytest.raises(RuntimeError, match="PREFIX_INPUT_BINDING"):
        continuation.continue_predictions(runtime.Engine(client), [changed], tmp_path / "parent", tmp_path / "run", "frozen", 1)
    assert client.calls == []
