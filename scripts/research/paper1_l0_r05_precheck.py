"""R05 explicit-GQA efficient-SDPA precheck. No D1 scoring and no label reads."""
from __future__ import annotations

import argparse
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
    NUMERICAL_ACCEPTANCE,
    cache_head_counts,
    call_summary,
    install,
    kernel_correspondence,
    synthetic_parity,
    uninstall,
)
from llmguard.domains.retrieval.hidden_poisoning.method_engineering.llm_verification import messages  # noqa: E402

R01 = Path(r"D:\paper1\VACE-L0-D1-20261029-R01")
R02 = Path(r"D:\paper1\VACE-L0-D1-20261029-R02")
R03 = Path(r"D:\paper1\VACE-L0-D1-20261029-R03")
R04 = Path(r"D:\paper1\VACE-L0-D1-20261029-R04-PRECHECK")
MODEL = R01 / "model" / "a09a35458c702b33eeacc393d103063234e8bc28"
PARSER = "src/llmguard/domains/retrieval/hidden_poisoning/method_engineering/llm_verification.py"
ADAPTER = "src/llmguard/domains/retrieval/hidden_poisoning/method_engineering/explicit_gqa_efficient_sdpa.py"
THIS = "scripts/research/paper1_l0_r05_precheck.py"
TEST = "tests/unit/test_explicit_gqa_efficient_sdpa.py"
SOURCE_FILES = [PARSER, ADAPTER, THIS, TEST]


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".pending")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def parent_hashes() -> dict[str, str | None]:
    files = {
        "r01_hard_stop": R01 / "HARD_STOP.json",
        "r01_config_lock": R01 / "CONFIG_LOCK.json",
        "r02_hard_stop": R02 / "HARD_STOP.json",
        "r02_config_lock": R02 / "CONFIG_LOCK.json",
        "r03_complete": R03 / "COMPLETE.json",
        "r03_config_lock": R03 / "CONFIG_LOCK.json",
        "r04_report": R04 / "PRECHECK_REPORT.md",
        "r04_kernel_receipt": R04 / "SDPA_KERNEL_RECEIPT.json",
        "r04_capacity": R04 / "CAPACITY_PRECHECK.json",
    }
    return {key: sha(path) if path.is_file() else None for key, path in files.items()}


def not_executed(reason: str) -> dict[str, str]:
    return {"status": "NOT_EXECUTED", "reason": reason}


def inventory(lock: dict[str, Any]) -> dict[str, Any]:
    from transformers import AutoTokenizer

    if lock["code_sha256"][PARSER] != sha(ROOT / PARSER):
        raise RuntimeError("ORIGINAL_PARSER_HASH_MISMATCH")
    tokenizer = AutoTokenizer.from_pretrained(MODEL, local_files_only=True, trust_remote_code=False)
    items = []
    for name in ("f5.jsonl", "oracle.jsonl"):
        path = R01 / "input" / "runtime" / name
        expected = next(item["sha256"] for item in lock["bundle_files"] if item["path"] == f"runtime/{name}")
        if sha(path) != expected:
            raise RuntimeError("RUNTIME_INPUT_HASH_MISMATCH:" + name)
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            prompt = tokenizer.apply_chat_template(messages(row), tokenize=False, add_generation_prompt=True)
            count = int(tokenizer(prompt, return_tensors="pt", truncation=False)["input_ids"].shape[-1])
            items.append({"condition": name[:-6], "candidate_id": row["candidate_id"], "input_tokens": count})
    if len(items) != 240 or any(item["input_tokens"] > 31744 for item in items):
        raise RuntimeError("INPUT_PACK_IDENTITY")
    summary = {}
    for condition in ("f5", "oracle"):
        values = sorted(item["input_tokens"] for item in items if item["condition"] == condition)
        summary[condition] = {"n": len(values), "min": values[0], "p50": values[len(values) // 2], "p90": values[int(len(values) * 0.9)], "max": values[-1]}
    counts = [item["input_tokens"] for item in items]
    return {"n": 240, "global_min": min(counts), "global_max": max(counts), "summary": summary, "items": items, "candidate_text_omitted": True}


def load_model():
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig

    index = 0
    free, _ = torch.cuda.mem_get_info(index)
    if free < 27917287424:
        raise RuntimeError("INSUFFICIENT_FREE_VRAM_DO_NOT_KILL_OTHER_PROCESSES")
    torch.cuda.set_per_process_memory_fraction(CONTRACT_RESERVED_BYTES / torch.cuda.get_device_properties(index).total_memory, index)
    torch.manual_seed(20261029)
    torch.use_deterministic_algorithms(True, warn_only=False)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    torch.backends.cudnn.deterministic = True
    tokenizer = AutoTokenizer.from_pretrained(MODEL, local_files_only=True, trust_remote_code=False)
    model = AutoModelForCausalLM.from_pretrained(MODEL, dtype=torch.bfloat16, device_map={"": index}, attn_implementation="sdpa", local_files_only=True, trust_remote_code=False)
    model.eval()
    if any(parameter.device.type != "cuda" or parameter.dtype != torch.bfloat16 for parameter in model.parameters()):
        raise RuntimeError("MODEL_DTYPE_OR_CPU_OFFLOAD_NOT_AUTHORIZED")
    generation = GenerationConfig.from_model_config(model.config)
    generation.do_sample = False
    generation.num_beams = 1
    generation.max_new_tokens = 1024
    generation.use_cache = True
    generation.pad_token_id = tokenizer.pad_token_id or tokenizer.eos_token_id
    return tokenizer, model, generation


def classify_profile(prof: Any) -> dict[str, Any]:
    named = []
    for event in prof.events():
        kernels = [kernel.name for kernel in getattr(event, "kernels", [])]
        named.append((event.name or "", kernels))
    return kernel_correspondence(named)


def phase_capacity(work: Path, tokens: int) -> None:
    import torch

    started = time.perf_counter()
    _, model, generation = load_model()
    previous = install(model)
    generator = torch.Generator(device="cpu")
    generator.manual_seed(20261029 + tokens)
    ids = torch.randint(1, int(model.config.vocab_size), (1, tokens), generator=generator)
    free_before = torch.cuda.mem_get_info(0)
    allocated_before = int(torch.cuda.memory_allocated(0))
    reserved_before = int(torch.cuda.memory_reserved(0))
    torch.cuda.reset_peak_memory_stats(0)
    record: dict[str, Any] = {
        "tokens": tokens,
        "capacity_only_min_new_tokens": 1024,
        "generation_config_max_new_tokens": 1024,
        "min_new_tokens_not_written_to_generation_config": True,
        "cold_start": True,
    }
    try:
        with torch.inference_mode():
            output = model.generate(ids.to(0), generation_config=generation, min_new_tokens=1024, attention_mask=torch.ones_like(ids).to(0))
        torch.cuda.synchronize()
        record.update({
            "status": "PASS",
            "output_tokens": int(output.shape[-1] - tokens),
            "elapsed_seconds": time.perf_counter() - started,
            "allocated_before": allocated_before,
            "reserved_before": reserved_before,
            "allocated_after": int(torch.cuda.memory_allocated(0)),
            "reserved_after": int(torch.cuda.memory_reserved(0)),
            "peak_allocated_bytes": int(torch.cuda.max_memory_allocated(0)),
            "peak_reserved_bytes": int(torch.cuda.max_memory_reserved(0)),
            "free_before": list(free_before),
            "free_after": list(torch.cuda.mem_get_info(0)),
        })
        record["contract_headroom_bytes"] = CONTRACT_RESERVED_BYTES - record["peak_reserved_bytes"]
        record["within_contract"] = record["output_tokens"] == 1024 and record["peak_reserved_bytes"] <= CONTRACT_RESERVED_BYTES and record["contract_headroom_bytes"] >= CONTRACT_HEADROOM_BYTES
        if not record["within_contract"]:
            record["status"] = "HEADROOM_OR_CAP_FAIL"
    except torch.OutOfMemoryError as exc:
        record.update({"status": "OOM", "error": str(exc), "within_contract": False})
    except Exception as exc:  # noqa: BLE001 — preserve the original failure and stop
        record.update({"status": type(exc).__name__, "error": "".join(traceback.format_exception_only(type(exc), exc)).strip()[:4000], "within_contract": False})
    finally:
        uninstall(model, previous)
    write_json(work / f"CAPACITY_{tokens}.json", record)
    print(json.dumps({"tokens": tokens, "status": record["status"]}, ensure_ascii=False), flush=True)
    if record["status"] != "PASS":
        raise SystemExit(2)


def phase_alternate(work: Path) -> None:
    import torch

    _, model, generation = load_model()
    previous = install(model)
    rows = []
    try:
        for tokens in (512, 8192, 512):
            generator = torch.Generator(device="cpu")
            generator.manual_seed(20261029 + tokens)
            ids = torch.randint(1, int(model.config.vocab_size), (1, tokens), generator=generator)
            torch.cuda.reset_peak_memory_stats(0)
            with torch.inference_mode():
                model.generate(ids.to(0), generation_config=generation, max_new_tokens=8, attention_mask=torch.ones_like(ids).to(0))
            torch.cuda.synchronize()
            rows.append({"tokens": tokens, "max_new_tokens": 8, "peak_reserved_bytes": int(torch.cuda.max_memory_reserved(0)), "reserved_after": int(torch.cuda.memory_reserved(0)), "free_after": list(torch.cuda.mem_get_info(0))})
        peaks = [row["peak_reserved_bytes"] for row in rows]
        grew = rows[-1]["reserved_after"] > rows[0]["reserved_after"] + 512 * 1024 * 1024
        status = "PASS" if max(peaks) <= CONTRACT_RESERVED_BYTES - CONTRACT_HEADROOM_BYTES and not grew else "ACCUMULATION_OR_CAP_FAIL"
    except Exception as exc:  # noqa: BLE001
        status = type(exc).__name__
        rows.append({"error": "".join(traceback.format_exception_only(type(exc), exc)).strip()[:2000]})
    finally:
        uninstall(model, previous)
    write_json(work / "CAPACITY_ALTERNATE.json", {"status": status, "steps": rows, "empty_cache_not_called": True})
    print(json.dumps({"alternate": status}, ensure_ascii=False), flush=True)
    if status != "PASS":
        raise SystemExit(2)


def run_all(work: Path) -> None:
    import torch
    from transformers import __version__ as transformers_version

    if (work / "PRECHECK_REPORT.md").exists():
        raise SystemExit("R05_PRECHECK_ALREADY_PRESENT_NOT_RERUN")
    work.mkdir(parents=True, exist_ok=True)
    before = parent_hashes()
    write_json(work / "PARENT_HASHES_BEFORE.json", before)
    lock = json.loads((R01 / "CONFIG_LOCK.json").read_text(encoding="utf-8"))
    import os
    device = {
        "name": torch.cuda.get_device_name(0),
        "capability": list(torch.cuda.get_device_capability(0)),
        "torch": torch.__version__,
        "cuda": torch.version.cuda,
        "transformers": transformers_version,
        "host": platform.node(),
    }
    if device["name"] != "NVIDIA GeForce RTX 5090" or tuple(device["capability"]) != (12, 0) or device["torch"] != "2.8.0+cu128" or device["transformers"] != "4.57.1":
        raise RuntimeError("IDENTITY_MISMATCH:" + json.dumps(device))
    from llmguard.domains.retrieval.hidden_poisoning.method_engineering import l0_worker as worker

    if worker.verify_model(MODEL, lock["official_manifest"]) != lock["model_file_sha256"]:
        raise RuntimeError("MODEL_HASH_MISMATCH")
    counted = inventory(lock)
    write_json(work / "LENGTH_INVENTORY.json", counted)
    config = {
        "task": "P1-L0-R05-EXPLICIT-GQA-EFFICIENT-SDPA-PRECHECK-01",
        "base_git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "code_sha256": {path: sha(ROOT / path) for path in SOURCE_FILES},
        "acceptance": NUMERICAL_ACCEPTANCE,
        "device": device,
        "model_file_sha256": lock["model_file_sha256"],
        "parser_sha256": sha(ROOT / PARSER),
        "runtime_input_sha256": {name: sha(R01 / "input" / "runtime" / name) for name in ("f5.jsonl", "oracle.jsonl")},
        "length_summary": {key: counted[key] for key in ("n", "global_min", "global_max", "summary")},
        "adapter": "explicit contiguous KV repeat then SDPBackend.EFFICIENT_ATTENTION only",
        "generation_contract": {"dtype": "bfloat16", "do_sample": False, "num_beams": 1, "seed": 20261029, "max_new_tokens": 1024, "deterministic_algorithms": True, "warn_only": False, "tf32": False, "max_context_tokens": 32768},
        "no_d1_prediction_or_scoring": True,
        "pyTorch_alloc_conf": os.environ.get("PYTORCH_CUDA_ALLOC_CONF"),
    }
    write_json(work / "CONFIG_LOCK.json", config)
    print("PHASE_A_PASS", flush=True)

    numerical: dict[str, Any]
    backend: dict[str, Any] = not_executed("waiting")
    determinism: dict[str, Any] = not_executed("waiting")
    capacity: dict[str, Any] = not_executed("waiting")
    status = "R05_PRECHECK_BLOCKED"
    failure = None
    try:
        torch.use_deterministic_algorithms(True, warn_only=False)
        torch.backends.cuda.matmul.allow_tf32 = False
        torch.backends.cudnn.allow_tf32 = False
        numerical = synthetic_parity("cuda")
        write_json(work / "NUMERICAL_PARITY_REPORT.json", numerical)
        if not numerical["pass"]:
            failure = "NUMERICAL_ACCEPTANCE_FAILED"
            raise RuntimeError(failure)
        print("PHASE_B_PASS", flush=True)
        tokenizer, model, generation = load_model()
        previous = install(model)
        try:
            from torch.profiler import ProfilerActivity, profile

            fictional = tokenizer.apply_chat_template([{"role": "user", "content": "Fictional 2099 protocol: the blue widget clause does not amend the red annex."}], add_generation_prompt=True, return_tensors="pt").to(0)
            with profile(activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA]) as prof:
                with torch.inference_mode():
                    model.generate(fictional, generation_config=generation, max_new_tokens=2, attention_mask=torch.ones_like(fictional))
            kernel = classify_profile(prof)
            summary = call_summary()
            probe = model(fictional, use_cache=True, attention_mask=torch.ones_like(fictional))
            prefill_heads = cache_head_counts(probe.past_key_values)
            follow = torch.randint(1, int(model.config.vocab_size), (1, 1))
            probe2 = model(follow.to(0), past_key_values=probe.past_key_values, use_cache=True, cache_position=torch.tensor([fictional.shape[-1]], device=0))
            decode_heads = cache_head_counts(probe2.past_key_values)
            backend = {"kernel": kernel, "calls": summary, "prefill_cache_kv_heads": prefill_heads, "decode_cache_kv_heads": decode_heads, "cache_stayed_at_4_heads": set(prefill_heads + decode_heads) == {4}}
            write_json(work / "BACKEND_AND_KERNEL_REPORT.json", backend)
            if not kernel["efficient_kernel_proved"] or not backend["cache_stayed_at_4_heads"] or summary["first_decode"] is None:
                failure = "EFFICIENT_BACKEND_OR_CACHE_NOT_PROVED"
                raise RuntimeError(failure)
            print("PHASE_C_BACKEND_PASS", flush=True)
            left = model.generate(fictional, generation_config=generation, max_new_tokens=32, attention_mask=torch.ones_like(fictional))
            right = model.generate(fictional, generation_config=generation, max_new_tokens=32, attention_mask=torch.ones_like(fictional))
            same = torch.equal(left, right)
            determinism = {"status": "PASS" if same else "FAIL", "max_new_tokens": 32, "left_tokens": int(left.shape[-1]), "right_tokens": int(right.shape[-1]), "token_ids_equal": bool(same), "deterministic_algorithms": bool(torch.are_deterministic_algorithms_enabled()), "warn_only": False}
            write_json(work / "DETERMINISM_REPORT.json", determinism)
            if not same:
                failure = "DETERMINISM_TOKEN_MISMATCH"
                raise RuntimeError(failure)
            print("PHASE_C_DETERMINISM_PASS", flush=True)
        finally:
            uninstall(model, previous)
            del model
            torch.cuda.empty_cache()
        capacity_rows = []
        for tokens in (8192, 16384, 26493):
            completed = subprocess.run([sys.executable, str(ROOT / THIS), "--work-dir", str(work), "--phase", "capacity", "--tokens", str(tokens)], cwd=ROOT, text=True, capture_output=True)
            (work / f"CAPACITY_{tokens}.stdout.txt").write_text(completed.stdout, encoding="utf-8")
            (work / f"CAPACITY_{tokens}.stderr.txt").write_text(completed.stderr, encoding="utf-8")
            row = {"tokens": tokens, "exit_code": completed.returncode}
            path = work / f"CAPACITY_{tokens}.json"
            if path.exists():
                row["result"] = json.loads(path.read_text(encoding="utf-8"))
            capacity_rows.append(row)
            if completed.returncode != 0 or not row.get("result", {}).get("within_contract"):
                failure = "CAPACITY_GATE_FAILED"
                capacity = {"status": "FAIL", "rows": capacity_rows, "alternate": not_executed(failure)}
                raise RuntimeError(failure)
        alternate = subprocess.run([sys.executable, str(ROOT / THIS), "--work-dir", str(work), "--phase", "alternate"], cwd=ROOT, text=True, capture_output=True)
        (work / "CAPACITY_ALTERNATE.stdout.txt").write_text(alternate.stdout, encoding="utf-8")
        (work / "CAPACITY_ALTERNATE.stderr.txt").write_text(alternate.stderr, encoding="utf-8")
        alternate_result = json.loads((work / "CAPACITY_ALTERNATE.json").read_text(encoding="utf-8")) if (work / "CAPACITY_ALTERNATE.json").exists() else not_executed("no file")
        if alternate.returncode != 0 or alternate_result.get("status") != "PASS":
            failure = "ALTERNATE_CAPACITY_FAILED"
            capacity = {"status": "FAIL", "rows": capacity_rows, "alternate": alternate_result}
            raise RuntimeError(failure)
        capacity = {"status": "PASS", "rows": capacity_rows, "alternate": alternate_result, "per_pack_prediction": "NOT_EXECUTED"}
        lengths = [item["input_tokens"] for item in counted["items"]]
        capacity["all_240_lengths_within_verified_max"] = max(lengths) <= 26493 and min(lengths) >= 1 and all(item <= 26493 for item in lengths)
        status = "R05_PRECHECK_PASS / OWNER_REVIEW_REQUIRED"
    except Exception as exc:  # noqa: BLE001
        failure = failure or type(exc).__name__
        if "numerical" not in locals():
            numerical = {"pass": False, "error": "".join(traceback.format_exception_only(type(exc), exc)).strip()[:4000]}
        if not (work / "NUMERICAL_PARITY_REPORT.json").exists():
            write_json(work / "NUMERICAL_PARITY_REPORT.json", numerical if isinstance(numerical, dict) else not_executed(failure))
        if not (work / "BACKEND_AND_KERNEL_REPORT.json").exists():
            write_json(work / "BACKEND_AND_KERNEL_REPORT.json", backend if isinstance(backend, dict) and backend.get("kernel") else not_executed(failure))
        if not (work / "DETERMINISM_REPORT.json").exists():
            write_json(work / "DETERMINISM_REPORT.json", determinism if determinism.get("status") in {"PASS", "FAIL"} else not_executed(failure))
        if not (work / "CAPACITY_REPORT.json").exists():
            capacity = capacity if capacity.get("status") in {"PASS", "FAIL"} else not_executed(failure)
        status = "R05_PRECHECK_BLOCKED"
        write_json(work / "FAILURE.json", {"error": failure, "detail": "".join(traceback.format_exception_only(type(exc), exc)).strip()[:4000]})
    write_json(work / "CAPACITY_REPORT.json", capacity)
    after = parent_hashes()
    integrity = {"before": before, "after": after, "unchanged": before == after}
    write_json(work / "PRIOR_RUN_INTEGRITY_REPORT.json", integrity)
    if not integrity["unchanged"]:
        status = "R05_PRECHECK_BLOCKED"
        failure = "PARENT_HASH_CHANGED"
    answers = answers_from(work, numerical if isinstance(numerical, dict) else {}, capacity, status)
    write_report(work, answers, status, failure)
    index = []
    for path in sorted(work.glob("*")):
        if path.is_file() and path.name != "EVIDENCE_INDEX.json" and ".pending" not in path.name:
            index.append({"path": path.name, "sha256": sha(path), "bytes": path.stat().st_size})
    write_json(work / "EVIDENCE_INDEX.json", {"status": status, "files": index})
    print(status, flush=True)


def answers_from(work: Path, numerical: dict[str, Any], capacity: dict[str, Any], status: str) -> dict[str, Any]:
    backend_path = work / "BACKEND_AND_KERNEL_REPORT.json"
    determinism_path = work / "DETERMINISM_REPORT.json"
    backend = json.loads(backend_path.read_text(encoding="utf-8")) if backend_path.exists() else {}
    determinism = json.loads(determinism_path.read_text(encoding="utf-8")) if determinism_path.exists() else {}
    kernel_ok = bool(backend.get("kernel", {}).get("efficient_kernel_proved")) and bool(backend.get("cache_stayed_at_4_heads"))
    long_ok = False
    if capacity.get("status") == "PASS":
        long_ok = any(row.get("tokens") == 26493 and row.get("result", {}).get("within_contract") for row in capacity.get("rows", []))
    return {
        "head_mapping_and_efficient_numeric_pass": bool(numerical.get("pass")),
        "model_ran_efficient_attention": kernel_ok,
        "determinism_pass": determinism.get("status") == "PASS" and determinism.get("token_ids_equal") is True,
        "longest_plus_1024_within_contract": long_ok,
        "all_240_lengths_inside_verified_envelope": bool(capacity.get("all_240_lengths_within_verified_max")),
        "per_pack_d1_prediction": "NOT_EXECUTED",
        "ready_to_request_full_d1_dev": status.startswith("R05_PRECHECK_PASS"),
        "status": status,
    }


def write_report(work: Path, answers: dict[str, Any], status: str, failure: str | None) -> None:
    inventory_path = work / "LENGTH_INVENTORY.json"
    summary = json.loads(inventory_path.read_text(encoding="utf-8")) if inventory_path.exists() else {}
    lines = [
        "# R05 explicit GQA efficient SDPA precheck",
        "",
        f"状态：{status}",
        "",
        f"1. 显式 GQA 展开是否通过正确性检查：{'是' if answers['head_mapping_and_efficient_numeric_pass'] else '否'}",
        f"2. 模型实际是否执行 efficient attention：{'是' if answers['model_ran_efficient_attention'] else '否'}",
        f"3. 确定性是否通过：{'是' if answers['determinism_pass'] else '否'}",
        f"4. 26493 输入加 1024 输出是否在资源门内通过：{'是' if answers['longest_plus_1024_within_contract'] else '否'}",
        f"5. 全部 240 包是否落在已验证的执行范围：{'是' if answers['all_240_lengths_inside_verified_envelope'] else '否'}。这是长度包络，不是逐包预测完成。",
        f"6. 是否具备申请完整 D1 开发实验的工程条件：{'是' if answers['ready_to_request_full_d1_dev'] else '否'}",
        "",
        "没有启动 D1 预测、评分、R06、VACE-LM 或 D2/D3。",
        f"失败原因：{failure or '无'}",
        "",
        f"长度盘点 n={summary.get('n')} min={summary.get('global_min')} max={summary.get('global_max')}。候选正文未写入本报告。",
        "数值门在第一次比较前固定：float32 头映射 max_abs/relative_L2 <= 1e-5；bf16 efficient 对展开 math 的 max_abs <= 2e-2、mean_abs <= 5e-3、relative_L2 <= 2e-2。",
        "持久 KV cache 必须保持 4 头。容量门是峰值预留不超过 30 GiB，且合同内余量至少 1 GiB。",
    ]
    (work / "PRECHECK_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work-dir", type=Path, default=Path(r"D:\paper1\VACE-L0-D1-20261030-R05-PRECHECK"))
    parser.add_argument("--phase", choices=("all", "capacity", "alternate"), default="all")
    parser.add_argument("--tokens", type=int)
    args = parser.parse_args()
    work = args.work_dir.resolve()
    if work.drive.upper() not in {"D:", "E:"}:
        raise SystemExit("R05_PAYLOAD_MUST_STAY_ON_D_OR_E")
    if args.phase == "capacity":
        phase_capacity(work, int(args.tokens))
    elif args.phase == "alternate":
        phase_alternate(work)
    else:
        run_all(work)


if __name__ == "__main__":
    main()
