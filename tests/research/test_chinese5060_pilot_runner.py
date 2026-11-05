from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import replace
from decimal import Decimal
from pathlib import Path

import pytest

from llmguard.domains.retrieval.hidden_poisoning.chinese5060.pilot_admission import (
    HISTORICAL_DELTA_CNY,
    MAX_CALLS,
    MODEL,
    Budget,
    BudgetInput,
    Stop,
    fake_budget,
    sha256,
)
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.pilot_design import canonical_hash, messages
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.pilot_inputs import (
    checked_bytes,
    token_audit,
    validate_grid,
)
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.pilot_runner import (
    Evidence,
    require_evaluation_release,
    run_fake,
)
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.pilot_transport import FakeTransport, LiveTransport

ROOT = Path(__file__).resolve().parents[2]


def synthetic_grid() -> tuple[list[dict], list[dict]]:
    private, public = [], []
    for index in range(MAX_CALLS):
        arm = ("G0", "G1", "G2")[index % 3]
        question = f"Synthetic prompt {index % 80}"
        chunks = [{"id": f"C{i}", "text": f"Mock context {i}"} for i in range(1, 6)]
        msg = messages(question, chunks)
        world, snap = f"W{index // 3:02d}", f"S{index // 3:02d}"
        whash = canonical_hash({"world_id": world, "snapshot_hash": snap})
        phash = canonical_hash(msg)
        row = {
            "request_id": "REQ-" + canonical_hash([whash, arm, phash])[:24], "arm": arm,
            "world_hash": whash, "prompt_hash": phash, "query_hash": canonical_hash(question),
            "retained_chunk_count": 5,
        }
        public.append(row)
        private.append({
            **row, "world_id": world, "query": question, "messages": msg, "original_snapshot_hash": snap,
            "retained_chunk_ids": ["fake"] * 5,
        })
    return private, public


def test_frozen_grid_and_raw_sha(tmp_path: Path) -> None:
    private, public = synthetic_grid()
    plan = tmp_path / "plan.json"
    frozen = json.dumps(private).encode()
    plan.write_bytes(frozen)
    assert checked_bytes(plan, sha256(frozen)) == frozen
    plan.write_bytes(frozen + b" ")
    with pytest.raises(Stop, match="SHA_DRIFT"):
        checked_bytes(plan, sha256(frozen))
    cells = validate_grid(private, public)
    assert len(cells) == 108 and len({c.world_hash for c in cells}) == 36
    assert len({c.prompt_hash for c in cells}) == 80
    assert token_audit(cells)["exact_input_tokens"] is None
    assert token_audit(cells)["status"] == "TOKEN_GATE_BLOCKED"
    with pytest.raises(Stop, match="108_CELLS"):
        validate_grid(private[:-1], public)


def test_generator_rejects_evaluator_shape() -> None:
    private, public = synthetic_grid()
    private[0]["expected_answer"] = "PRIVATE_SENTINEL"
    with pytest.raises(Stop, match="PUBLIC_PROJECTION_DRIFT"):
        validate_grid(private, public)
    del private[0]["expected_answer"]
    private[0]["messages"][1]["content"] = '{"question":"Synthetic prompt 0","context":[],"target":"secret"}'
    with pytest.raises(Stop, match="USER_ENVELOPE_DRIFT"):
        validate_grid(private, public)


def test_full_fake_grid_preserves_duplicates_and_seals(tmp_path: Path) -> None:
    cells = validate_grid(*synthetic_grid())
    transport = FakeTransport()
    summary = run_fake(cells, Evidence(tmp_path), Budget(fake_budget()), transport, {})
    assert summary["outcomes"] == {"MOCK_SUCCESS": 108}
    assert summary["mock_calls"] == transport.attempts == 108
    assert summary["real_api_calls"] == 0 and summary["real_cost_usd"] == "0"
    assert summary["mock_cost_usd"] == "0.018360000"
    seal_raw = (tmp_path / "OUTPUT_SEAL.json").read_bytes()
    assert sha256(seal_raw) == summary["output_seal_sha256"]
    for name, digest in json.loads(seal_raw)["files_sha256"].items():
        assert sha256((tmp_path / name).read_bytes()) == digest
    outcomes = json.loads((tmp_path / "OUTCOMES_PRIVATE.json").read_bytes())
    assert {row["real_status"] for row in outcomes} == {"NOT_RUN"}
    assert all(row["mock_attempts"] == 1 and row["mock_usage"]["cached_input_tokens"] == 16 for row in outcomes)
    assert outcomes[0]["prompt_hash"] == outcomes[80]["prompt_hash"]
    assert outcomes[0]["fake_request_id"] != outcomes[80]["fake_request_id"]
    body = json.loads(cells[0].body)
    assert body["model"] == MODEL and body["max_tokens"] == 256
    assert body["temperature"] == 0 and body["top_p"] == 1
    assert body["enable_search"] is body["enable_thinking"] is body["stream"] is False
    assert set(body["messages"][1]) == {"role", "content"}
    assert set(json.loads(body["messages"][1]["content"])) == {"question", "context"}
    with pytest.raises(Stop, match="DENIED_MOCK_OUTPUT"):
        require_evaluation_release("FAKE")
    with pytest.raises(FileExistsError):
        run_fake(cells, Evidence(tmp_path), Budget(fake_budget()), FakeTransport(), {})


@pytest.mark.parametrize(("fault", "code"), [
    ("timeout", "TRANSPORT_TIMEOUT"), ("http", "HTTP_NON_SUCCESS"), ("non_json", "INVALID_JSON"),
    ("missing_usage", "USAGE_MISSING"), ("model", "RETURNED_MODEL_MISMATCH"),
    ("citation", "ANSWER_INVALID_CITATIONS"), ("empty", "RESPONSE_EMPTY"),
    ("hidden", "USAGE_CACHE_OR_REASONING_VIOLATION"), ("length", "RESPONSE_NOT_COMPLETE"),
    ("tool", "RESPONSE_UNAPPROVED_REASONING_TOOL_OR_REFUSAL"),
    ("usage_over", "USAGE_TOKEN_CAP_EXCEEDED"), ("usage_drift", "USAGE_TOKEN_DRIFT"),
])
def test_first_error_preserves_denominator(tmp_path: Path, fault: str, code: str) -> None:
    summary = run_fake(validate_grid(*synthetic_grid()), Evidence(tmp_path), Budget(fake_budget()),
                       FakeTransport({2: fault}), {})
    assert summary["stop_code"] == code and summary["mock_calls"] == 2
    assert summary["outcomes"] == {"MOCK_SUCCESS": 1, "MOCK_FAILURE": 1, "NOT_RUN": 106}
    outcomes = json.loads((tmp_path / "OUTCOMES_PRIVATE.json").read_bytes())
    assert outcomes[2]["mock_attempts"] == 0
    assert bool(outcomes[1]["raw_response_sha256"]) == (fault != "timeout")
    if fault in {"timeout", "http", "missing_usage", "model", "hidden", "usage_over", "usage_drift"}:
        assert Decimal(summary["mock_failed_unsettled_reservation_usd"]) > 0
    else:
        assert outcomes[1]["mock_usage"]["output_tokens"] == 18


def test_token_cap_and_empty_policy(tmp_path: Path) -> None:
    cells = validate_grid(*synthetic_grid())
    cells[0] = replace(cells[0], citations=())
    summary = run_fake(cells, Evidence(tmp_path), Budget(fake_budget()), FakeTransport(), {},
                       {cells[1].request_id: 4097})
    assert summary["outcomes"] == {"MOCK_LOCAL_ABSTAIN": 1, "MOCK_FAILURE": 1, "NOT_RUN": 106}
    assert summary["stop_code"] == "INPUT_TOKEN_GATE_EXCEEDED" and summary["mock_calls"] == 0


def budget_manifest() -> dict:
    return {
        "model": MODEL, "currency": "CNY", "usd_per_billing_unit": "0.15", "historical_usd_per_cny": "0.15",
        "uncached_input_per_million": "7", "cached_input_per_million": "2", "output_per_million": "20",
        "settled_all_streams_usd": "1.20", "pending_all_streams_usd": "0", "available_usd_before_pending": "10",
        "batch_ceiling_usd": "1", "includes_all_streams": True, "price_version": "SYNTHETIC",
        "as_of_utc": "2026-11-05T00:00:00Z", "evidence_sha256": {k: "1" * 64 for k in (
            "price", "fx", "ledger", "balance",
        )},
    }


def test_budget_history_warning_stop_and_reservation(tmp_path: Path) -> None:
    assert HISTORICAL_DELTA_CNY == Decimal("0.083730086")
    value = budget_manifest()
    config = BudgetInput.from_manifest(value)
    assert Budget(config).check() == "ADMIT_BUDGET_ONLY"
    with pytest.raises(Stop, match="HISTORICAL_FLOOR"):
        BudgetInput.from_manifest({**value, "settled_all_streams_usd": "1.129214387"})
    with pytest.raises(Stop, match="EVIDENCE_DIGESTS"):
        BudgetInput.from_manifest({**value, "evidence_sha256": {}})
    assert Budget(replace(config, settled=Decimal("25"))).check() == "ADMIT_WITH_25_USD_WARNING"
    with pytest.raises(Stop, match="CEILING"):
        Budget(replace(config, batch_cap=Decimal("0.1"))).check()
    with pytest.raises(Stop, match="INSUFFICIENT_ACCOUNT"):
        Budget(replace(config, available=Decimal("0.1"))).check()
    with pytest.raises(Stop, match="CUMULATIVE_30"):
        Budget(replace(config, settled=Decimal("30"))).check()
    exhausted = Budget(replace(config, settled=Decimal("27.99")))
    summary = run_fake(validate_grid(*synthetic_grid()), Evidence(tmp_path), exhausted, FakeTransport(), {})
    assert summary["stop_code"] == "STOP_NEW_BATCH_28_USD" and summary["mock_calls"] == 0
    assert summary["outcomes"] == {"MOCK_FAILURE": 1, "NOT_RUN": 107}
    per_cell = Budget(config)
    per_cell.start()
    with pytest.raises(Stop, match="CELL_RESERVATION"):
        per_cell.settle(per_cell.cell_max + Decimal("0.01"))
    assert per_cell.unsettled == per_cell.cell_max


def test_live_constructor_and_cli_refuse_even_with_approval(tmp_path: Path) -> None:
    with pytest.raises(Stop, match="LIVE_NOT_AUTHORIZED"):
        LiveTransport(approval={"signature": "synthetic", "budget": 1})
    out = tmp_path / "must_not_create"
    result = subprocess.run([
        sys.executable, "-I", "-S", "-B", str(ROOT / "scripts/research/run_chinese5060_minimal_rag_pilot.py"),
        "--live", "--owner-execution-approval", "synthetic", "--output-dir", str(out),
    ], capture_output=True, check=False, env={**os.environ, "PILOT_LIVE": "1"})
    assert result.returncode == 2 and result.stderr.strip() == b"LIVE_NOT_AUTHORIZED" and not out.exists()


def test_offline_process_blocks_socket_subprocess_private_reads_and_c_writes(tmp_path: Path) -> None:
    out = tmp_path / "fake-out"
    # A synthetic stand-in proves denied evaluator reads without opening any research file.
    private = tmp_path / "private-evaluator-fixture.json"
    private.write_text("SYNTHETIC_SENTINEL")
    script = """
import os, socket, subprocess, sys, tempfile
from pathlib import Path
sys.path.insert(0, sys.argv[1])
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.pilot_admission import Stop
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.pilot_offline import (
    CACHE_VARS, install_offline_barrier, local_de, redirect_environment,
)
output, private = Path(sys.argv[2]), Path(sys.argv[3])
install_offline_barrier(output, set())
output.mkdir()
redirect_environment(output)
for key in CACHE_VARS:
    assert Path(os.environ[key]) == output / "local_scratch"
assert Path(tempfile.gettempdir()) == output / "local_scratch"
for action in (
    lambda: socket.socket(),
    lambda: socket.getaddrinfo("blocked.invalid", 443),
    lambda: subprocess.Popen([sys.executable, "-V"]),
    lambda: private.read_bytes(),
    lambda: sys.audit("open", r"C:\\offlimits\\pilot-test.bin", "wb", os.O_WRONLY | os.O_CREAT),
):
    try:
        action()
    except PermissionError as exc:
        assert "OFFLINE_" in str(exc)
    else:
        raise AssertionError("offline barrier allowed a prohibited operation")
try:
    local_de(Path(r"C:\\offlimits\\pilot-test.bin"))
except Stop as exc:
    assert str(exc) == "CONTROLLED_PATH_MUST_BE_LOCAL_D_OR_E"
else:
    raise AssertionError("C was accepted")
assert not any(m in sys.modules for m in ("openai", "dashscope"))
print("OFFLINE_AND_EVALUATOR_ISOLATION_PASS")
"""
    result = subprocess.run([sys.executable, "-I", "-S", "-B", "-c", script,
                             str(ROOT / "src"), str(out), str(private)], capture_output=True, check=False)
    assert result.returncode == 0, result.stderr.decode()
    assert result.stdout.strip() == b"OFFLINE_AND_EVALUATOR_ISOLATION_PASS"
