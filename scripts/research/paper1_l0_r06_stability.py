"""R06 allocator stability precheck. Does not rescore R05 and does not start D1."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import platform
import subprocess
import sys
import time
import traceback
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "src"), str(ROOT)]

from llmguard.domains.retrieval.hidden_poisoning.method_engineering.explicit_gqa_efficient_sdpa import (  # noqa: E402
    CONTRACT_HEADROOM_BYTES,
    CONTRACT_RESERVED_BYTES,
    call_summary,
    install,
    uninstall,
)

R01 = Path(r"D:\paper1\VACE-L0-D1-20261029-R01")
R02 = Path(r"D:\paper1\VACE-L0-D1-20261029-R02")
R03 = Path(r"D:\paper1\VACE-L0-D1-20261029-R03")
R04 = Path(r"D:\paper1\VACE-L0-D1-20261029-R04-PRECHECK")
R05 = Path(r"D:\paper1\VACE-L0-D1-20261030-R05-PRECHECK")
MODEL = R01 / "model" / "a09a35458c702b33eeacc393d103063234e8bc28"
THIS = "scripts/research/paper1_l0_r06_stability.py"
ADAPTER = "src/llmguard/domains/retrieval/hidden_poisoning/method_engineering/explicit_gqa_efficient_sdpa.py"
TEST = "tests/unit/test_l0_r06_stability.py"
R05_COMMIT = "b5ff81d5dd58493fc20d796ac9806f4678fb0928"
SEED = 20261029
WARMUP_ROUNDS = 2
MEASURE_ROUNDS = 5
LENGTHS = (1294, 8192, 16384, 26493, 1294)
CAPACITY_ONLY_MIN_NEW_TOKENS = 1024
ALLOCATED_GROWTH_MAX_BYTES = 128 * 1024 * 1024
RESERVED_PLATEAU_MAX_BYTES = 512 * 1024 * 1024
BASELINE_PHASE = "warmup"
BASELINE_ROUND = 2
CSV_FIELDS = (
    "sequence", "phase", "round", "step", "input_tokens", "output_tokens", "status",
    "allocated_before", "reserved_before", "free_before", "total_before",
    "peak_allocated", "peak_reserved", "allocated_after", "reserved_after", "free_after", "total_after",
    "elapsed_seconds", "backend", "nan_inf", "checkpoint", "error",
)


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def parent_files() -> dict[str, Path]:
    return {
        "r01_hard_stop": R01 / "HARD_STOP.json",
        "r01_config_lock": R01 / "CONFIG_LOCK.json",
        "r02_hard_stop": R02 / "HARD_STOP.json",
        "r02_config_lock": R02 / "CONFIG_LOCK.json",
        "r03_complete": R03 / "COMPLETE.json",
        "r03_config_lock": R03 / "CONFIG_LOCK.json",
        "r04_report": R04 / "PRECHECK_REPORT.md",
        "r04_kernel_receipt": R04 / "SDPA_KERNEL_RECEIPT.json",
        "r04_capacity": R04 / "CAPACITY_PRECHECK.json",
        "r05_report": R05 / "PRECHECK_REPORT.md",
        "r05_failure": R05 / "FAILURE.json",
        "r05_config_lock": R05 / "CONFIG_LOCK.json",
        "r05_numerical": R05 / "NUMERICAL_PARITY_REPORT.json",
        "r05_backend": R05 / "BACKEND_AND_KERNEL_REPORT.json",
        "r05_determinism": R05 / "DETERMINISM_REPORT.json",
        "r05_capacity": R05 / "CAPACITY_REPORT.json",
        "r05_evidence_index": R05 / "EVIDENCE_INDEX.json",
    }


def parent_hashes() -> dict[str, str | None]:
    return {key: sha(path) if path.exists() else None for key, path in parent_files().items()}


def source_hashes() -> dict[str, str]:
    return {name: sha(ROOT / name) for name in (THIS, ADAPTER, TEST)}


def build_protocol(hashes: dict[str, str], git_head: str) -> dict[str, Any]:
    r05_lock = json.loads((R05 / "CONFIG_LOCK.json").read_text(encoding="utf-8"))
    return {
        "task": "P1-L0-R06-ALLOCATOR-STABILITY-REVIEW-01",
        "locked_before_gpu": True,
        "r05_status_unchanged": "R05_PRECHECK_BLOCKED / OWNER_REVIEW_REQUIRED",
        "r05_not_rewritten": True,
        "git_head": git_head,
        "r05_result_commit": R05_COMMIT,
        "source_sha256": hashes,
        "r05_config_lock_code_sha256": r05_lock["code_sha256"],
        "r05_source_difference": {
            "executed_adapter_sha256": r05_lock["code_sha256"][ADAPTER],
            "committed_adapter_sha256": hashes[ADAPTER],
            "recorded_reason": "After the R05 GPU measurement and before commit b5ff81d, kernel_correspondence was added and the profiler predicate stopped treating the dispatcher wrapper as a missing kernel. Numerical windows and the attention forward contract were not changed. R06 uses the committed adapter and does not roll the worktree back.",
        },
        "runtime": {
            "python": r"D:\paper1\VACE-L0-D1-20261029-R01\env\Scripts\python.exe",
            "model": str(MODEL),
            "dtype": "bfloat16",
            "device_map": {"": 0},
            "attn_implementation_before_adapter": "sdpa",
            "adapter": "explicit contiguous KV repeat, then SDPBackend.EFFICIENT_ATTENTION only",
            "persistent_kv_heads": 4,
            "deterministic_algorithms": True,
            "warn_only": False,
            "tf32": False,
            "seed": SEED,
            "max_reserved_bytes": CONTRACT_RESERVED_BYTES,
            "minimum_headroom_bytes": CONTRACT_HEADROOM_BYTES,
            "no_empty_cache": True,
            "no_allocator_env_change": True,
            "no_process_restart_to_clear_accumulation": True,
        },
        "synthetic_input": {
            "method": "torch.Generator(device='cpu'); manual_seed(seed + token_length); torch.randint(1, vocab_size, (1, token_length))",
            "seed": SEED,
            "same_as_r05_capacity_probe": True,
            "real_d1_text": False,
        },
        "lengths": list(LENGTHS),
        "warmup_rounds": WARMUP_ROUNDS,
        "measure_rounds": MEASURE_ROUNDS,
        "generation": {
            "generation_config_max_new_tokens": 1024,
            "capacity_only_min_new_tokens": CAPACITY_ONLY_MIN_NEW_TOKENS,
            "min_new_tokens_written_to_generation_config": False,
            "do_sample": False,
            "num_beams": 1,
            "reuse_previous_request_cache": False,
        },
        "measurement_points": [
            "before each generate, after the previous request's tensors were deleted",
            "peak allocated and peak reserved during that generate",
            "after deleting that request's output and input and calling torch.cuda.synchronize",
            "the same-condition checkpoint is only the after-release measurement of the final 1294-token step in each round",
        ],
        "release_steps": [
            "read the output token count into a Python int",
            "delete the generate output",
            "delete the CPU input ids",
            "do not store GPU tensors in the timeline, a closure, or a result list",
            "torch.cuda.synchronize()",
            "then read allocated, reserved, and device free memory",
        ],
        "baseline": "allocated and reserved at the checkpoint after warmup round 2; the five measurement rounds all compare with this one checkpoint",
        "acceptance": {
            "A_backend_and_identity": "efficient attention only, frozen model and environment, no NaN/Inf, parent evidence hashes unchanged",
            "B_peak_reserved_max_bytes": CONTRACT_RESERVED_BYTES,
            "B_minimum_headroom_bytes": CONTRACT_HEADROOM_BYTES,
            "B_no_oom": True,
            "C_allocated_growth_max_bytes": ALLOCATED_GROWTH_MAX_BYTES,
            "C_comparison": "each measurement checkpoint allocated minus the warmup-2 checkpoint allocated",
            "D_reserved_plateau_max_bytes": RESERVED_PLATEAU_MAX_BYTES,
            "D_comparison": "max minus min of reserved at the last three measurement checkpoints",
            "continued_growth": "if every adjacent allocated delta among the five measurement checkpoints is strictly positive, or every adjacent reserved delta among them is strictly positive, report insufficient stability even when C and D pass",
            "reserved_growth_from_cold_start_is_not_by_itself_a_leak": True,
            "allocated_growth_is_not_explained_as_normal_cache": True,
        },
        "stop_conditions": [
            "OOM",
            "peak reserved above 30 GiB or headroom under 1 GiB",
            "backend other than efficient attention",
            "identity or parent-hash mismatch",
            "NaN or Inf",
            "warmup failure",
            "output length other than 1024",
        ],
    }


def decide(calls: list[dict[str, Any]], checkpoints: list[dict[str, Any]], identity: dict[str, bool]) -> dict[str, Any]:
    """Apply the protocol gates. Thresholds are the module constants, not fitted values."""
    failures: list[str] = []
    peaks = [int(row["peak_reserved"]) for row in calls if row.get("peak_reserved") is not None]
    longest = [int(row["peak_reserved"]) for row in calls if row.get("input_tokens") == 26493 and row.get("peak_reserved") is not None]
    headrooms = [CONTRACT_RESERVED_BYTES - int(row["peak_reserved"]) for row in calls if row.get("peak_reserved") is not None]
    oom = any(row.get("status") == "OOM" for row in calls)
    bad_call = any(row.get("status") != "PASS" for row in calls)
    identity_ok = all(identity.values()) and not any(row.get("nan_inf") for row in calls)
    peak_ok = bool(peaks) and max(peaks) <= CONTRACT_RESERVED_BYTES and min(headrooms) >= CONTRACT_HEADROOM_BYTES and not oom
    if not identity_ok:
        failures.append("IDENTITY_OR_BACKEND")
    if not peak_ok or bad_call:
        failures.append("PEAK_OR_CALL_FAILED")
    baseline = next((row for row in checkpoints if row["phase"] == BASELINE_PHASE and row["round"] == BASELINE_ROUND), None)
    measured = [row for row in checkpoints if row["phase"] == "measure"]
    allocated_deltas = None if baseline is None or len(measured) != MEASURE_ROUNDS else [int(row["allocated"]) - int(baseline["allocated"]) for row in measured]
    allocated_ok = allocated_deltas is not None and all(delta <= ALLOCATED_GROWTH_MAX_BYTES for delta in allocated_deltas)
    if allocated_deltas is not None and not allocated_ok:
        failures.append("ALLOCATED_GROWTH")
    last3 = measured[-3:] if len(measured) == MEASURE_ROUNDS else []
    plateau_span = None if len(last3) != 3 else max(int(row["reserved"]) for row in last3) - min(int(row["reserved"]) for row in last3)
    plateau_ok = plateau_span is not None and plateau_span <= RESERVED_PLATEAU_MAX_BYTES
    if plateau_span is not None and not plateau_ok:
        failures.append("RESERVED_PLATEAU")
    allocated_steps = None if allocated_deltas is None else [int(measured[index]["allocated"]) - int(measured[index - 1]["allocated"]) for index in range(1, len(measured))]
    reserved_steps = None if len(measured) != MEASURE_ROUNDS else [int(measured[index]["reserved"]) - int(measured[index - 1]["reserved"]) for index in range(1, len(measured))]
    allocated_continued = allocated_steps is not None and all(step > 0 for step in allocated_steps)
    reserved_continued = reserved_steps is not None and all(step > 0 for step in reserved_steps)
    if allocated_continued or reserved_continued:
        failures.append("CONTINUED_GROWTH_STABILITY_INSUFFICIENT")
    curve = []
    previous = None
    for row in checkpoints:
        item = {"phase": row["phase"], "round": row["round"], "allocated": int(row["allocated"]), "reserved": int(row["reserved"])}
        if previous is not None:
            item["allocated_delta_from_previous_checkpoint"] = item["allocated"] - previous["allocated"]
            item["reserved_delta_from_previous_checkpoint"] = item["reserved"] - previous["reserved"]
        curve.append(item)
        previous = item
    status = "R06_STABILITY_PRECHECK_PASS / OWNER_REVIEW_REQUIRED" if not failures else "R06_STABILITY_PRECHECK_BLOCKED / OWNER_REVIEW_REQUIRED"
    return {
        "status": status,
        "failures": failures,
        "gates": {
            "A_backend_and_identity": {"status": "PASS" if identity_ok else "FAIL", "measured": identity},
            "B_peak_and_headroom": {
                "status": "PASS" if peak_ok and not bad_call else "FAIL",
                "max_peak_reserved_bytes": max(peaks) if peaks else None,
                "longest_input_peak_reserved_bytes": max(longest) if longest else None,
                "minimum_contract_headroom_bytes": min(headrooms) if headrooms else None,
                "oom": oom,
            },
            "C_active_allocated": {
                "status": "PASS" if allocated_ok else ("NOT_EXECUTED" if allocated_deltas is None else "FAIL"),
                "baseline_allocated_bytes": None if baseline is None else int(baseline["allocated"]),
                "deltas_bytes": allocated_deltas,
                "limit_bytes": ALLOCATED_GROWTH_MAX_BYTES,
            },
            "D_reserved_plateau": {
                "status": "PASS" if plateau_ok else ("NOT_EXECUTED" if plateau_span is None else "FAIL"),
                "last3_span_bytes": plateau_span,
                "limit_bytes": RESERVED_PLATEAU_MAX_BYTES,
            },
            "continued_growth": {
                "status": "FAIL" if (allocated_continued or reserved_continued) else ("NOT_EXECUTED" if allocated_steps is None else "PASS"),
                "measurement_allocated_adjacent_deltas": allocated_steps,
                "measurement_reserved_adjacent_deltas": reserved_steps,
            },
        },
        "checkpoint_curve": curve,
        "active_memory_continued_growth": allocated_continued,
        "reserved_formed_plateau": plateau_ok,
        "small_end_to_end_trial_basis": not failures,
        "not_verified": [
            "not 240 predictions",
            "not a proof of no leak",
            "not arbitrary input lengths",
            "not unbounded runtime",
            "R05 512 MiB alternate gate was not revised",
        ],
    }


def git_head() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


def lock_protocol(work: Path) -> None:
    work.mkdir(parents=True, exist_ok=True)
    protocol_path = work / "R06_STABILITY_PROTOCOL.json"
    if protocol_path.exists() or (work / "CONFIG_LOCK.json").exists():
        raise SystemExit("R06_PROTOCOL_ALREADY_LOCKED_NOT_REWRITTEN")
    protocol = build_protocol(source_hashes(), git_head())
    write_json(protocol_path, protocol)
    config = {
        "task": protocol["task"],
        "locked_before_gpu": True,
        "protocol_sha256": sha(protocol_path),
        "source_sha256": protocol["source_sha256"],
        "git_head": protocol["git_head"],
        "r05_result_commit": R05_COMMIT,
        "pyTorch_alloc_conf": os.environ.get("PYTORCH_CUDA_ALLOC_CONF"),
        "parent_hashes_at_lock": parent_hashes(),
    }
    write_json(work / "CONFIG_LOCK.json", config)
    print(config["protocol_sha256"], flush=True)


def assert_locked(work: Path) -> dict[str, Any]:
    protocol_path = work / "R06_STABILITY_PROTOCOL.json"
    config = json.loads((work / "CONFIG_LOCK.json").read_text(encoding="utf-8"))
    if sha(protocol_path) != config["protocol_sha256"]:
        raise RuntimeError("PROTOCOL_HASH_MISMATCH")
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    if source_hashes() != protocol["source_sha256"]:
        raise RuntimeError("SOURCE_CHANGED_AFTER_LOCK")
    if git_head() != protocol["git_head"]:
        raise RuntimeError("GIT_HEAD_CHANGED_AFTER_LOCK")
    return protocol


def append_row(path: Path, row: dict[str, Any]) -> None:
    new_file = not path.exists()
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        if new_file:
            writer.writeheader()
        writer.writerow({key: row.get(key) for key in CSV_FIELDS})


def snapshot_backend() -> dict[tuple[Any, ...], int]:
    summary = call_summary()
    return {
        (item["query_len"], item["key_len"], item["kv_heads"], item["expanded_heads"], item["enable_gqa"], item["backend"]): item["count"]
        for item in summary["signatures"]
    }


def backend_of_delta(before: dict[tuple[Any, ...], int], after: dict[tuple[Any, ...], int]) -> str:
    changed = [key for key, count in after.items() if count > before.get(key, 0)]
    if not changed:
        return "ADAPTER_NOT_CALLED"
    if any(key[2] != 4 or key[3] != 28 or key[4] or key[5] != "EFFICIENT_ATTENTION" for key in changed):
        return "BACKEND_MISMATCH"
    return "EFFICIENT_ATTENTION"


def one_call(model: Any, generation: Any, sequence: int, phase: str, round_index: int, step: int, tokens: int) -> dict[str, Any]:
    import torch

    generator = torch.Generator(device="cpu")
    generator.manual_seed(SEED + tokens)
    ids = torch.randint(1, int(model.config.vocab_size), (1, tokens), generator=generator)
    row: dict[str, Any] = {
        "sequence": sequence, "phase": phase, "round": round_index, "step": step, "input_tokens": tokens,
        "output_tokens": None, "status": "PASS", "nan_inf": False, "checkpoint": step == len(LENGTHS), "error": "",
        "allocated_before": int(torch.cuda.memory_allocated(0)),
        "reserved_before": int(torch.cuda.memory_reserved(0)),
    }
    free_before, total = torch.cuda.mem_get_info(0)
    row["free_before"] = int(free_before)
    row["total_before"] = int(total)
    before_backend = snapshot_backend()
    output = None
    started = time.perf_counter()
    torch.cuda.reset_peak_memory_stats(0)
    try:
        with torch.inference_mode():
            output = model.generate(
                ids.to(0),
                generation_config=generation,
                min_new_tokens=CAPACITY_ONLY_MIN_NEW_TOKENS,
                attention_mask=torch.ones((1, tokens), dtype=torch.long).to(0),
            )
        torch.cuda.synchronize()
        row["output_tokens"] = int(output.shape[-1] - tokens)
        if torch.is_floating_point(output) and not bool(torch.isfinite(output).all()):
            row["nan_inf"] = True
            row["status"] = "NAN_INF"
        elif row["output_tokens"] != CAPACITY_ONLY_MIN_NEW_TOKENS:
            row["status"] = "OUTPUT_BUDGET_NOT_REACHED"
    except torch.OutOfMemoryError as exc:
        row["status"] = "OOM"
        row["error"] = str(exc)[:2000]
    except Exception as exc:  # noqa: BLE001 — keep the original failure and stop
        row["status"] = type(exc).__name__
        row["error"] = "".join(traceback.format_exception_only(type(exc), exc)).strip()[:2000]
    finally:
        del output
        del ids
        torch.cuda.synchronize()
    row["elapsed_seconds"] = round(time.perf_counter() - started, 6)
    row["peak_allocated"] = int(torch.cuda.max_memory_allocated(0))
    row["peak_reserved"] = int(torch.cuda.max_memory_reserved(0))
    free_after, total_after = torch.cuda.mem_get_info(0)
    row["allocated_after"] = int(torch.cuda.memory_allocated(0))
    row["reserved_after"] = int(torch.cuda.memory_reserved(0))
    row["free_after"] = int(free_after)
    row["total_after"] = int(total_after)
    row["backend"] = backend_of_delta(before_backend, snapshot_backend())
    if row["status"] == "PASS":
        headroom = CONTRACT_RESERVED_BYTES - int(row["peak_reserved"])
        if int(row["peak_reserved"]) > CONTRACT_RESERVED_BYTES or headroom < CONTRACT_HEADROOM_BYTES:
            row["status"] = "HEADROOM_OR_CAP_FAIL"
        elif row["backend"] != "EFFICIENT_ATTENTION":
            row["status"] = "BACKEND_FAIL"
    return row


def load_model() -> tuple[Any, Any, Any]:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig

    free, _ = torch.cuda.mem_get_info(0)
    if free < 27917287424:
        raise RuntimeError("INSUFFICIENT_FREE_VRAM_DO_NOT_KILL_OTHER_PROCESSES")
    torch.cuda.set_per_process_memory_fraction(CONTRACT_RESERVED_BYTES / torch.cuda.get_device_properties(0).total_memory, 0)
    torch.manual_seed(SEED)
    torch.use_deterministic_algorithms(True, warn_only=False)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    tokenizer = AutoTokenizer.from_pretrained(MODEL, local_files_only=True, trust_remote_code=False)
    model = AutoModelForCausalLM.from_pretrained(MODEL, dtype=torch.bfloat16, device_map={"": 0}, attn_implementation="sdpa", local_files_only=True, trust_remote_code=False)
    model.eval()
    if any(parameter.device.type != "cuda" or parameter.dtype != torch.bfloat16 for parameter in model.parameters()):
        raise RuntimeError("MODEL_DTYPE_OR_CPU_OFFLOAD_NOT_AUTHORIZED")
    generation = GenerationConfig.from_model_config(model.config)
    generation.do_sample = False
    generation.num_beams = 1
    generation.max_new_tokens = 1024
    generation.use_cache = True
    generation.pad_token_id = tokenizer.pad_token_id or tokenizer.eos_token_id
    if getattr(generation, "min_new_tokens", None) not in (None, 0):
        raise RuntimeError("GENERATION_CONFIG_MIN_NEW_TOKENS_NOT_ALLOWED")
    return tokenizer, model, generation


def write_reports(work: Path, calls: list[dict[str, Any]], checkpoints: list[dict[str, Any]], identity: dict[str, bool], before: dict[str, str | None], failure: str | None) -> None:
    decision = decide(calls, checkpoints, identity)
    if failure and failure not in decision["failures"]:
        decision["failures"].append(failure)
        decision["status"] = "R06_STABILITY_PRECHECK_BLOCKED / OWNER_REVIEW_REQUIRED"
        decision["small_end_to_end_trial_basis"] = False
    after = parent_hashes()
    integrity = {"before": before, "after": after, "unchanged": before == after}
    write_json(work / "PRIOR_RUN_INTEGRITY_REPORT.json", integrity)
    if not integrity["unchanged"]:
        decision["failures"].append("PARENT_HASH_CHANGED")
        decision["status"] = "R06_STABILITY_PRECHECK_BLOCKED / OWNER_REVIEW_REQUIRED"
        decision["gates"]["A_backend_and_identity"]["status"] = "FAIL"
        decision["small_end_to_end_trial_basis"] = False
    decision["per_call"] = [{key: row.get(key) for key in CSV_FIELDS} for row in calls]
    decision["r05_reused_not_rewritten"] = True
    write_json(work / "STABILITY_REPORT.json", decision)
    lines = [
        "# R06 allocator stability precheck",
        "",
        f"状态：{decision['status']}",
        "",
        "1. 本轮复用已提交的显式 GQA 适配器。R05 结果提交是 b5ff81d5dd58493fc20d796ac9806f4678fb0928。R05 保持 R05_PRECHECK_BLOCKED，512 MiB 旧门和 FAILURE.json 没有改写。",
        "2. 同工况检查点曲线见 STABILITY_REPORT.json 的 checkpoint_curve，含相邻增量。",
        f"3. 最长输入峰值预留：{decision['gates']['B_peak_and_headroom']['longest_input_peak_reserved_bytes']}。合同内最小余量：{decision['gates']['B_peak_and_headroom']['minimum_contract_headroom_bytes']}。",
        "4. 验收门实测见 STABILITY_REPORT.json 的 gates。",
        f"5. 正式测量轮活跃显存是否持续增长：{decision['active_memory_continued_growth']}。",
        f"6. 最后三个正式测量轮的 reserved 是否形成平台：{decision['reserved_formed_plateau']}。",
        f"7. 是否具备进入少量端到端试运行的工程依据：{decision['small_end_to_end_trial_basis']}。这不是启动该试运行的批准。",
        "8. 未验证范围：不是 240 条预测完成，不是无泄漏证明，不是任意长度，也不是无限运行稳定性。",
        "",
        "没有启动 D1 预测、评分、VACE-LM 或 D2/D3。",
        f"失败项：{decision['failures'] or '无'}。",
    ]
    (work / "PRECHECK_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    index = []
    for path in sorted(work.glob("*")):
        if path.is_file() and path.name != "EVIDENCE_INDEX.json":
            index.append({"path": path.name, "sha256": sha(path), "bytes": path.stat().st_size})
    write_json(work / "EVIDENCE_INDEX.json", {"status": decision["status"], "files": index})
    print(decision["status"], flush=True)


def run_measurement(work: Path) -> None:
    import torch

    if (work / "PRECHECK_REPORT.md").exists() or (work / "MEMORY_TIMELINE.csv").exists():
        raise SystemExit("R06_ALREADY_PRESENT_NOT_RERUN")
    before = parent_hashes()
    protocol = assert_locked(work)
    if protocol["warmup_rounds"] != WARMUP_ROUNDS or protocol["measure_rounds"] != MEASURE_ROUNDS or tuple(protocol["lengths"]) != LENGTHS:
        raise RuntimeError("PROTOCOL_CONSTANTS_MISMATCH")
    device_ok = torch.cuda.get_device_name(0) == "NVIDIA GeForce RTX 5090" and torch.cuda.get_device_capability(0) == (12, 0) and torch.__version__ == "2.8.0+cu128"
    from transformers import __version__ as transformers_version

    device_ok = device_ok and transformers_version == "4.57.1"
    from llmguard.domains.retrieval.hidden_poisoning.method_engineering import l0_worker as worker

    r01_lock = json.loads((R01 / "CONFIG_LOCK.json").read_text(encoding="utf-8"))
    model_ok = worker.verify_model(MODEL, r01_lock["official_manifest"]) == r01_lock["model_file_sha256"]
    _, model, generation = load_model()
    deterministic = bool(torch.are_deterministic_algorithms_enabled())
    warn_only = bool(getattr(torch, "are_deterministic_algorithms_warn_only_enabled", lambda: False)())
    tf32_off = not torch.backends.cuda.matmul.allow_tf32 and not torch.backends.cudnn.allow_tf32
    previous = install(model)
    calls: list[dict[str, Any]] = []
    checkpoints: list[dict[str, Any]] = []
    failure = None
    sequence = 0
    try:
        for phase, count in (("warmup", WARMUP_ROUNDS), ("measure", MEASURE_ROUNDS)):
            for round_index in range(1, count + 1):
                for step, tokens in enumerate(LENGTHS, start=1):
                    sequence += 1
                    row = one_call(model, generation, sequence, phase, round_index, step, tokens)
                    calls.append(row)
                    append_row(work / "MEMORY_TIMELINE.csv", row)
                    print(json.dumps({"sequence": sequence, "phase": phase, "round": round_index, "tokens": tokens, "status": row["status"], "reserved_after": row["reserved_after"]}, ensure_ascii=False), flush=True)
                    if row["status"] != "PASS":
                        failure = row["status"]
                        raise RuntimeError(failure)
                last = calls[-1]
                checkpoints.append({"phase": phase, "round": round_index, "allocated": last["allocated_after"], "reserved": last["reserved_after"]})
    except RuntimeError:
        pass
    finally:
        uninstall(model, previous)
    summary = call_summary()
    backend_ok = bool(summary["signatures"]) and all(
        item["backend"] == "EFFICIENT_ATTENTION" and item["kv_heads"] == 4 and item["expanded_heads"] == 28 and item["enable_gqa"] is False
        for item in summary["signatures"]
    )
    backend_ok = backend_ok and summary["first_prefill"] is not None and summary["first_decode"] is not None
    identity = {
        "device_ok": device_ok,
        "model_hash_ok": model_ok,
        "adapter_sha_ok": sha(ROOT / ADAPTER) == protocol["source_sha256"][ADAPTER],
        "deterministic": deterministic and not warn_only,
        "tf32_off": tf32_off,
        "backend_ok": backend_ok,
        "protocol_matches_constants": True,
    }
    write_json(work / "BACKEND_CALL_SUMMARY.json", summary)
    write_reports(work, calls, checkpoints, identity, before, failure)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--work-dir", type=Path, default=Path(r"D:\paper1\VACE-L0-D1-20261030-R06-STABILITY-PRECHECK"))
    parser.add_argument("--phase", choices=("lock", "run"), required=True)
    args = parser.parse_args()
    if args.work_dir.drive.upper() not in {"D:", "E:"}:
        raise SystemExit("R06_PAYLOAD_MUST_STAY_ON_D_OR_E")
    if args.phase == "lock":
        lock_protocol(args.work_dir)
        return
    run_measurement(args.work_dir)


if __name__ == "__main__":
    main()
