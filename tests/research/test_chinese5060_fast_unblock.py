from __future__ import annotations

import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pytest

from llmguard.domains.retrieval.hidden_poisoning.chinese5060.fast_unblock_admission import (
    RUN_ROOT,
    V2,
    CheckedAdmission,
    check_admission,
    check_live_authority,
    grid_digest,
    path_digest,
    refreeze,
)
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.fast_unblock_runner import (
    LiveInputs,
    RapidRun,
    _run,
    run_live,
    run_synthetic,
)
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.pilot_admission import MODEL, Stop, json_bytes, sha256, strict_json
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.pilot_design import messages
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.pilot_inputs import PINNED_INPUTS, PROPOSAL, Cell
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.pilot_transport import FakeTransport, Reply, encode

AT = datetime(2026, 11, 5, 1, tzinfo=timezone.utc)
ROOT = Path(__file__).resolve().parents[2]


def synthetic_cells() -> list[Cell]:
    return [
        Cell(f"SYNTHETIC-{i:03d}", f"w-{i // 3:02d}", ("G0", "G1", "G2")[i % 3], f"p-{i % 80}",
             ("C1",), encode(messages(f"fixture {i % 80}", [{"id": "C1", "text": "fixture only"}])), 0)
        for i in range(108)
    ]


@pytest.fixture
def fixture(tmp_path: Path) -> LiveInputs:
    root = tmp_path
    output = root / RUN_ROOT / "runs/SYNTHETIC"
    old = synthetic_cells()
    cells, _ = refreeze(old)
    grid = grid_digest(cells)
    source_commit = "a" * 40
    cfg = json_bytes({"version": V2, "v1_proposal_sha256": PINNED_INPUTS[PROPOSAL], "v2_grid_sha256": grid})
    blobs = {key: ("SYNTHETIC " + key).encode() for key in (
        "price", "fx", "ledger", "balance", "transfer_basis", "wire_basis", "token_basis"
    )}
    host = "fixture.cn-beijing.maas.aliyuncs.com"
    region = "cn-beijing"
    sources = {"a" * 64}
    blobs["transfer"] = json_bytes({
        "request_grid_sha256": grid, "allowed_sources": sorted(sources), "processor": "ALIBABA_CLOUD_MODEL_STUDIO",
        "host": host, "region": region, "scope": "ONLY_FROZEN_SYSTEM_QUERY_AND_RETAINED_TOPK",
        "source_rights_and_sensitive_clearance_sha256": sha256(blobs["transfer_basis"]),
    })
    blobs["wire"] = json_bytes({
        "host": host, "region": region, "model": MODEL, "version": V2, "output_wire_field": "max_completion_tokens",
        "output_value": 256, "verified_billable_upper": 266, "nonthinking_json_verified": True,
        "basis_sha256": sha256(blobs["wire_basis"]),
    })
    blobs["token"] = json_bytes({
        "model": MODEL, "version": V2, "method": "VERIFIED_EXACT_CHAT_TEMPLATE", "basis_sha256": sha256(blobs["token_basis"]),
        "rows": [{"request_id": c.request_id, "request_sha256": sha256(c.body), "upper": 128, "chat_overhead": 8}
                 for c in cells],
    })
    blobs["budget"] = json_bytes({
        "region": region, "failure_inflight_usd_included": "0.10", "valid_until_utc": "2026-11-05T02:00:00Z",
        "snapshot": {"model": MODEL, "currency": "USD", "usd_per_billing_unit": "1", "historical_usd_per_cny": "0.15",
                     "uncached_input_per_million": "1", "cached_input_per_million": "0.25", "output_per_million": "3",
                     "settled_all_streams_usd": "1.3", "pending_all_streams_usd": "0.10",
                     "available_usd_before_pending": "10", "batch_ceiling_usd": "1", "includes_all_streams": True,
                     "price_version": "SYNTHETIC", "as_of_utc": "2026-11-05T00:00:00Z",
                     "evidence_sha256": {key: sha256(blobs[key]) for key in ("price", "fx", "ledger", "balance")}},
    })
    return LiveInputs(root, output, source_commit, cfg, old, cells, sources,
                      manifest(source_commit, cfg, grid, output, blobs), blobs)


def manifest(source: str, cfg: bytes, grid: str, out: Path, blobs: dict[str, bytes]) -> bytes:
    return json_bytes({"source_commit": source, "config_sha256": sha256(cfg), "request_grid_sha256": grid,
                       "output_path_sha256": path_digest(out), "version": V2,
                       "artifacts_sha256": {key: sha256(raw) for key, raw in blobs.items()}})


def checked(data: LiveInputs, *, rebind_fixture: bool = False, at: datetime = AT) -> CheckedAdmission:
    raw = data.manifest_raw
    if rebind_fixture:
        raw = manifest(data.source_commit, data.config_raw, grid_digest(data.candidate), data.output, data.artifacts)
    return check_admission(data.root, data.output, data.source_commit, sha256(data.config_raw), data.config_raw,
                           data.original, data.candidate, data.required_sources, raw, sha256(raw), data.artifacts, at=at)


def test_v2_only_rename_all_108(fixture: LiveInputs) -> None:
    assert len(fixture.candidate) == 108
    for old, new in zip(fixture.original, fixture.candidate, strict=True):
        before, after = strict_json(old.body), strict_json(new.body)
        assert before.pop("max_tokens") == after.pop("max_completion_tokens") == 256
        assert before == after
        assert old.request_id == new.request_id and old.prompt_hash == new.prompt_hash


def test_all_pass_engine_then_real_authority_stays_locked(
    fixture: LiveInputs, monkeypatch: pytest.MonkeyPatch,
) -> None:
    gate = checked(fixture)
    monkeypatch.setenv("DASHSCOPE_API_KEY", "SYNTHETIC")
    monkeypatch.setenv("PILOT_LIVE", "1")
    with pytest.raises(Stop, match="NEW_OWNER_LIVE_APPROVAL_REQUIRED"):
        check_live_authority(gate, json_bytes({"owner_id": "W1-OD-20261105-5060-PILOT12-CONDITIONAL-LIVE-10"}))
    with pytest.raises(Stop, match="NEW_OWNER_LIVE_APPROVAL_REQUIRED"):
        run_live(fixture, fixture.manifest_raw)
    assert not fixture.output.exists()

    base_send = FakeTransport.send

    def check_intent(self: FakeTransport, raw: bytes, count: int) -> Reply:
        i = self.attempts + 1
        assert (fixture.output / f"INTENT_{i:03d}.json").is_file()
        assert (fixture.output / "INITIAL3_CHECKPOINT.json").is_file() == (i > 3)
        return base_send(self, raw, count)

    monkeypatch.setattr(FakeTransport, "send", check_intent)
    fake = FakeTransport({3: "billable_tolerance"})
    summary = run_synthetic(gate, fixture.candidate, fake)
    assert summary["outcomes"] == {"SUCCESS": 108, "FAIL": 0, "NOT_RUN": 0}
    assert summary["real_posts_upper_by_send_intent"] == 0 and summary["new_charge_usd"] == "0"
    assert summary["initial3_passed"] and fake.attempts == 108
    seal = strict_json((fixture.output / "OUTPUT_SEAL.json").read_bytes())
    assert all(sha256((fixture.output / name).read_bytes()) == digest for name, digest in seal["files_sha256"].items())
    with pytest.raises(Stop, match="DUPLICATE_RUN_OR_SEND_INTENT"):
        run_synthetic(gate, fixture.candidate, FakeTransport())


@pytest.mark.parametrize(("field", "code"), [
    ("transfer", "TRANSFER_COVERAGE"), ("wire", "WIRE_ACCOUNT_HOST"), ("token", "STRICT_TOKEN"),
    ("budget", "BUDGET_REGION"),
])
def test_any_gate_failure_blocks_before_sending(fixture: LiveInputs, field: str, code: str) -> None:
    fixture.artifacts[field] = b"{}"
    with pytest.raises(Stop, match=code):
        checked(fixture, rebind_fixture=True)
    assert not fixture.output.exists()


@pytest.mark.parametrize(("position", "fault", "reason"), [
    (1, "timeout", "TRANSPORT_TIMEOUT"), (3, "http", "LIVE_HTTP_NOT_200"),
    (4, "missing_usage", "USAGE_MISSING"), (5, "billable_over", "USAGE_TOKEN_CAP_EXCEEDED"),
])
def test_failure_preserves_all_slots_and_pending(
    fixture: LiveInputs, position: int, fault: str, reason: str,
) -> None:
    gate = checked(fixture)
    fake = FakeTransport({position: fault})
    summary = run_synthetic(gate, fixture.candidate, fake)
    assert summary["stop_code"] == reason and summary["initial3_passed"] == (position > 3)
    assert summary["outcomes"] == {"SUCCESS": position - 1, "FAIL": 1, "NOT_RUN": 108 - position}
    assert fake.attempts == position and float(summary["unsettled_reservation_usd"]) > 0
    assert len(strict_json((fixture.output / "OUTCOMES_PRIVATE.json").read_bytes())) == 108


@pytest.mark.parametrize(("key", "val", "reason"), [
    ("settled_all_streams_usd", "28", "STOP_NEW_BATCH_28_USD"),
    ("settled_all_streams_usd", "30", "STOP_CUMULATIVE_30_USD"),
    ("available_usd_before_pending", "0", "BLOCKED_INSUFFICIENT_ACCOUNT_BALANCE"),
    ("pending_all_streams_usd", "0", "BUDGET_FAILURE_HOLD_NOT_INCLUDED"),
    ("settled_all_streams_usd", "0", "BUDGET_HISTORICAL_FLOOR"),
])
def test_budget_failure_cases(fixture: LiveInputs, key: str, val: str, reason: str) -> None:
    budget = strict_json(fixture.artifacts["budget"])
    budget["snapshot"][key] = val
    fixture.artifacts["budget"] = json_bytes(budget)
    with pytest.raises(Stop, match=reason):
        checked(fixture, rebind_fixture=True)


def test_budget_warn_and_exact_v2_tolerance(fixture: LiveInputs) -> None:
    budget: dict[str, Any] = strict_json(fixture.artifacts["budget"])
    budget["snapshot"]["settled_all_streams_usd"] = "25"
    fixture.artifacts["budget"] = json_bytes(budget)
    result = run_synthetic(checked(fixture, rebind_fixture=True), fixture.candidate, FakeTransport({1: "billable_tolerance"}))
    assert result["initial_batch_reservation_usd"] == "0.120009600"
    rows = strict_json((fixture.output / "OUTCOMES_PRIVATE.json").read_bytes())
    assert rows[0]["budget_decision"] == "ADMIT_WITH_25_USD_WARNING"
    assert rows[0]["usage"]["output_tokens"] == 266


def test_proof_staleness_and_tamper(fixture: LiveInputs) -> None:
    with pytest.raises(Stop, match="BUDGET_SNAPSHOT_OUTSIDE_VALIDITY"):
        checked(fixture, at=datetime(2026, 11, 6, tzinfo=timezone.utc))
    fixture.artifacts["wire"] += b"\n"
    with pytest.raises(Stop, match="ADMISSION_BINDING_DRIFT"):
        checked(fixture)
    proof = strict_json(fixture.artifacts["token"])
    proof["rows"][-1]["upper"] = 4097
    fixture.artifacts["token"] = json_bytes(proof)
    with pytest.raises(Stop, match="STRICT_TOKEN_LIMIT_FAILED"):
        checked(fixture, rebind_fixture=True)


def test_cli_live_flag_denied(tmp_path: Path) -> None:
    out = tmp_path / "must-not-exist"
    result = subprocess.run([
        sys.executable, "-I", "-S", "-B", "scripts/research/prepare_chinese5060_fast_unblock.py",
        "--live", "--output-dir", str(out),
    ], cwd=ROOT, capture_output=True, check=False)
    assert result.returncode == 2 and result.stderr.strip() == b"NEW_OWNER_LIVE_APPROVAL_REQUIRED"
    assert not out.exists()


@pytest.mark.parametrize("oversize_at", [None, 2, 4])
def test_owner12_post_usage_and_initial_checkpoint(fixture: LiveInputs, oversize_at: int | None) -> None:
    raw = b"independent synthetic test admission"
    checked = RapidRun(fixture.output, grid_digest(fixture.candidate), sha256(raw))
    fake = FakeTransport({})

    def send(cell: Cell, bound: int, record_post: Any) -> Reply:
        ordinal = fake.attempts + 1
        assert bound == 4096
        assert (fixture.output / f"INTENT_{ordinal:03d}.json").is_file()
        assert (fixture.output / "INITIAL3_CHECKPOINT.json").is_file() == (ordinal > 3)
        record_post("STARTED")
        record_post("SENT")
        reply = fake.send(cell.body, 128)
        response = strict_json(reply.body)
        response["id"] = f"FAKE-{ordinal}"
        if ordinal == oversize_at:
            response["usage"]["prompt_tokens"] = 4097
        return Reply(200, json_bytes(response), None)

    with pytest.raises(Stop, match="RAPID_ADMISSION_RECEIPT_MISMATCH"):
        _run(checked, fixture.candidate, send, "SYNTHETIC", admission_raw=b"wrong")
    assert not fixture.output.exists()
    result = _run(checked, fixture.candidate, send, "SYNTHETIC", admission_raw=raw)
    if oversize_at is None:
        assert result["outcomes"] == {"SUCCESS": 108, "FAIL": 0, "NOT_RUN": 0}
        assert result["stop_code"] is None and result["initial3_passed"]
    else:
        assert result["outcomes"] == {"SUCCESS": oversize_at - 1, "FAIL": 1, "NOT_RUN": 108 - oversize_at}
        assert result["stop_code"] == "LIVE_INPUT_PROOF_VIOLATION"
        assert result["initial3_passed"] == (oversize_at > 3)
        assert result["unsettled_reservation_cny"] == "7.1486784"
    assert fake.attempts == (oversize_at or 108)
    assert (fixture.output / "OUTPUT_SEAL.json").is_file()
    assert (fixture.output / "RAPID_LIVE_ADMISSION_MANIFEST.json").read_bytes() == raw
