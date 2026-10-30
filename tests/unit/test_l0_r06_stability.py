"""CPU checks for the R06 stability gates. No model and no GPU measurement."""
from __future__ import annotations

import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "research" / "paper1_l0_r06_stability.py"
SPEC = importlib.util.spec_from_file_location("r06_stability", SCRIPT)
R06 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(R06)

IDENTITY = {
    "device_ok": True,
    "model_hash_ok": True,
    "adapter_sha_ok": True,
    "deterministic": True,
    "tf32_off": True,
    "backend_ok": True,
    "protocol_matches_constants": True,
}


def _call(tokens: int = 1294, peak: int = 20_000_000_000) -> dict:
    return {"input_tokens": tokens, "peak_reserved": peak, "status": "PASS", "nan_inf": False}


def _checkpoints(allocated: list[int], reserved: list[int]) -> list[dict]:
    rows = []
    for index, (used, held) in enumerate(zip(allocated, reserved, strict=True)):
        phase = "warmup" if index < 2 else "measure"
        round_index = index + 1 if index < 2 else index - 1
        rows.append({"phase": phase, "round": round_index, "allocated": used, "reserved": held})
    return rows


def test_limits_are_the_predeclared_binary_mebibytes() -> None:
    assert R06.ALLOCATED_GROWTH_MAX_BYTES == 128 * 1024 * 1024
    assert R06.RESERVED_PLATEAU_MAX_BYTES == 512 * 1024 * 1024
    assert R06.WARMUP_ROUNDS == 2
    assert R06.MEASURE_ROUNDS == 5
    assert R06.LENGTHS == (1294, 8192, 16384, 26493, 1294)
    assert R06.CAPACITY_ONLY_MIN_NEW_TOKENS == 1024


def test_flat_measurement_passes() -> None:
    calls = [_call(tokens) for _ in range(7) for tokens in R06.LENGTHS]
    checkpoints = _checkpoints([1000] * 7, [5000] * 7)
    result = R06.decide(calls, checkpoints, IDENTITY)
    assert result["status"].startswith("R06_STABILITY_PRECHECK_PASS")
    assert result["failures"] == []
    assert result["small_end_to_end_trial_basis"] is True
    assert result["active_memory_continued_growth"] is False
    assert result["reserved_formed_plateau"] is True


def test_allocated_growth_above_128mib_fails_without_changing_the_limit() -> None:
    calls = [_call() for _ in range(35)]
    allocated = [1_000] * 2 + [1_000, 1_000, 1_000, 1_000, 1_000 + 128 * 1024 * 1024 + 1]
    result = R06.decide(calls, _checkpoints(allocated, [5_000] * 7), IDENTITY)
    assert "ALLOCATED_GROWTH" in result["failures"]
    assert result["gates"]["C_active_allocated"]["limit_bytes"] == 128 * 1024 * 1024
    assert result["small_end_to_end_trial_basis"] is False


def test_strict_increase_inside_the_128mib_window_is_still_insufficient() -> None:
    calls = [_call() for _ in range(35)]
    allocated = [1_000, 1_000, 1_100, 1_200, 1_300, 1_400, 1_500]
    result = R06.decide(calls, _checkpoints(allocated, [5_000] * 7), IDENTITY)
    assert "CONTINUED_GROWTH_STABILITY_INSUFFICIENT" in result["failures"]
    assert "ALLOCATED_GROWTH" not in result["failures"]
    assert result["gates"]["C_active_allocated"]["status"] == "PASS"


def test_last_three_reserved_span_above_512mib_fails() -> None:
    calls = [_call() for _ in range(35)]
    reserved = [5_000] * 4 + [10_000, 10_000, 10_000 + 512 * 1024 * 1024 + 1]
    result = R06.decide(calls, _checkpoints([1_000] * 7, reserved), IDENTITY)
    assert "RESERVED_PLATEAU" in result["failures"]
    assert result["gates"]["D_reserved_plateau"]["status"] == "FAIL"


def test_early_oom_does_not_invent_a_measured_plateau() -> None:
    calls = [_call(), {"input_tokens": 8192, "peak_reserved": 1, "status": "OOM", "nan_inf": False}]
    result = R06.decide(calls, [], IDENTITY)
    assert result["status"].startswith("R06_STABILITY_PRECHECK_BLOCKED")
    assert result["gates"]["C_active_allocated"]["status"] == "NOT_EXECUTED"
    assert result["gates"]["D_reserved_plateau"]["status"] == "NOT_EXECUTED"
    assert "ALLOCATED_GROWTH" not in result["failures"]
    assert "RESERVED_PLATEAU" not in result["failures"]
