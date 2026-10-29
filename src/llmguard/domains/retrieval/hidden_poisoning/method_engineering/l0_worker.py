"""Bounded 5090 worker orchestration. No CUDA/model work occurs on import.

Normal phases auto-continue; identity/resource/integrity/synthetic failures do
not. Evaluation is a separate process after the prediction lock. Raw data stay
private. No online lookup is available to the inference process.
"""
from __future__ import annotations

import hashlib
import importlib
import json
import os
import platform
import shutil
import subprocess
import sys
import time
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .llm_verification import check_row, messages, parse_output, sha_text, synthetic_cases

INPUT_SHA = "03fae845b50d669373d3b08776caf5a1b2cf068ea7aa5b60dea89a65177e3eb2"
BASE = "configs/research/paper1_l0"
SOURCE_FILES = [
    "src/llmguard/domains/retrieval/hidden_poisoning/method_engineering/llm_verification.py",
    "src/llmguard/domains/retrieval/hidden_poisoning/method_engineering/l0_worker.py",
    "scripts/research/paper1_l0_worker.py", "scripts/research/evaluate_l0_worker.py",
    "scripts/research/evaluate_vace_f5_diagnostic.py",
    "src/llmguard/domains/retrieval/hidden_poisoning/method_engineering/development_detection.py",
    BASE + "/worker_policy_v1.json", BASE + "/qwen_official_manifest_v1.json",
]


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for data in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(data)
    return h.hexdigest()


def load(path: Path) -> Any:
    return json.loads(path.read_text("utf-8"))


def rows(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text("utf-8").splitlines()]


def write_new(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise FileExistsError(path)
    temp = path.with_name(path.name + ".pending-" + str(time.time_ns()))
    with temp.open("x", encoding="utf-8", newline="\n") as f:
        json.dump(value, f, ensure_ascii=False, indent=2, allow_nan=False)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
    temp.rename(path)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def process_is_alive(pid: int) -> bool:
    if pid <= 0:
        return True  # malformed ownership must never authorize lock recovery
    if os.name == "nt":
        import ctypes
        from ctypes import wintypes
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
        kernel.OpenProcess.restype = wintypes.HANDLE
        kernel.GetExitCodeProcess.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]
        kernel.CloseHandle.argtypes = [wintypes.HANDLE]
        handle = kernel.OpenProcess(0x1000, False, pid)
        if not handle:
            return ctypes.get_last_error() != 87  # unknown/access denied -> alive
        code = wintypes.DWORD()
        valid = kernel.GetExitCodeProcess(handle, ctypes.byref(code))
        kernel.CloseHandle(handle)
        return not valid or code.value == 259
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def size(path: Path) -> int:
    total = 0
    for p in path.rglob("*"):
        try:
            if p.is_file() and not p.is_symlink():
                total += p.stat().st_size
        except FileNotFoundError:  # atomic .pending -> final rename while monitoring
            continue
    return total


def budget(root: Path, policy: dict[str, Any], reserve: int = 0) -> None:
    if size(root) + reserve > policy["new_model_dependency_budget_bytes"]:
        raise RuntimeError("NEW_MODEL_DEPENDENCY_24GIB_BUDGET_EXCEEDED")


def environment(root: Path, repo: Path) -> dict[str, str]:
    env = dict(os.environ)
    env.update({"PYTHONPATH": str(repo / "src") + os.pathsep + str(repo), "PYTHONUTF8": "1", "PYTHONPYCACHEPREFIX": str(root / "cache/pycache"), "HF_HOME": str(root / "cache/hf"), "HUGGINGFACE_HUB_CACHE": str(root / "cache/hf/hub"), "TORCH_HOME": str(root / "cache/torch"), "TMPDIR": str(root / "temp"), "TEMP": str(root / "temp"), "TMP": str(root / "temp"), "PIP_CACHE_DIR": str(root / "cache/pip"), "PIP_NO_CACHE_DIR": "1", "PIP_CONFIG_FILE": os.devnull, "PIP_DISABLE_PIP_VERSION_CHECK": "1", "CUBLAS_WORKSPACE_CONFIG": ":4096:8", "TOKENIZERS_PARALLELISM": "false", "HF_HUB_OFFLINE": "1", "TRANSFORMERS_OFFLINE": "1"})
    env.pop("TRANSFORMERS_CACHE", None)
    for key in ("PIP_EXTRA_INDEX_URL", "PIP_FIND_LINKS", "PIP_TRUSTED_HOST", "PIP_CONSTRAINT", "PIP_REQUIREMENT"):
        env.pop(key, None)
    env.update({"PIP_INDEX_URL": "https://pypi.org/simple", "HF_XET_CACHE": str(root / "cache/xet"), "XDG_CACHE_HOME": str(root / "cache/xdg"), "TORCHINDUCTOR_CACHE_DIR": str(root / "cache/inductor"), "TRITON_CACHE_DIR": str(root / "cache/triton"), "TORCH_EXTENSIONS_DIR": str(root / "cache/extensions")})
    return env


def logged(command: list[str], root: Path, name: str, env: dict[str, str], policy: dict[str, Any]) -> None:
    logs = root / "logs"
    logs.mkdir(exist_ok=True)
    start = now()
    with (logs / (name + ".stdout.txt")).open("xb") as out, (logs / (name + ".stderr.txt")).open("xb") as err:
        process = subprocess.Popen(command, stdout=out, stderr=err, env=env)
        try:
            while process.poll() is None:
                budget(root, policy)
                time.sleep(2)
        except BaseException:
            process.terminate()
            process.wait(timeout=30)
            raise
    write_new(logs / (name + ".command.json"), {"command": command, "start_utc": start, "end_utc": now(), "exit_code": process.returncode})
    if process.returncode:
        raise RuntimeError(f"COMMAND_FAILED:{name}:see {logs}")


def device_gate() -> dict[str, Any]:
    command = ["nvidia-smi", "--query-gpu=index,name,memory.total,driver_version", "--format=csv,noheader"]
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    devices: list[dict[str, Any]] = []
    for line in result.stdout.splitlines():
        fields = [x.strip() for x in line.split(",")]
        devices.append({"index": fields[0], "name": fields[1], "memory_mib": int(fields[2].split()[0]), "driver": fields[3]})
    if not any("RTX 5090" in d["name"] and d["memory_mib"] >= 30000 for d in devices):
        raise RuntimeError("REQUESTED_RTX5090_32GB_NOT_PRESENT")
    return {"command": command, "stdout": result.stdout, "stderr": result.stderr, "exit_code": result.returncode, "devices": devices}


def safe_unpack(archive: Path, target: Path) -> dict[str, Any]:
    if sha(archive) != INPUT_SHA:
        raise RuntimeError("PRIVATE_INPUT_ZIP_SHA_MISMATCH")
    target.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive) as z:
        for entry in z.infolist():
            p = (target / entry.filename).resolve()
            if not p.is_relative_to(target.resolve()) or "\\" in entry.filename or entry.file_size > 100 * 1024 * 1024:
                raise RuntimeError("UNSAFE_ZIP_ENTRY")
            if entry.is_dir():
                p.mkdir(parents=True, exist_ok=True)
            elif not p.exists():
                p.parent.mkdir(parents=True, exist_ok=True)
                pending = p.with_name(p.name + ".pending-" + str(time.time_ns()))
                with pending.open("xb") as f:
                    f.write(z.read(entry))
                pending.rename(p)
    manifest = load(target / "BUNDLE_MANIFEST.json")
    if (manifest["groups"], manifest["candidates"], manifest["families"]) != (40, 120, 13):
        raise RuntimeError("WRONG_SIGNED_COHORT")
    for entry in manifest["files"]:
        p = (target / entry["path"]).resolve()
        if not p.is_relative_to(target.resolve()) or sha(p) != entry["sha256"]:
            raise RuntimeError("PRIVATE_INPUT_FILE_IDENTITY")
    return manifest


def verify_model(path: Path, manifest: dict[str, Any]) -> dict[str, str]:
    result = {}
    for entry in manifest["files"]:
        p = path / entry["name"]
        if not p.is_file() or p.stat().st_size != entry["size"]:
            raise ValueError("MODEL_FILE_MISSING_OR_SIZE")
        result[entry["name"]] = sha(p)
        if "sha256" in entry:
            if result[entry["name"]] != entry["sha256"]:
                raise ValueError("MODEL_WEIGHT_SHA")
        else:
            blob = hashlib.sha1(f"blob {p.stat().st_size}\0".encode() + p.read_bytes()).hexdigest()
            if blob != entry["git_blob_sha1"]:
                raise ValueError("OFFICIAL_TOKENIZER_CONFIG_LICENSE_BLOB_SHA")
    return result


def find_existing_model(explicit: Path | None, manifest: dict[str, Any]) -> Path | None:
    if explicit is not None:
        verify_model(explicit, manifest)
        return explicit.resolve()
    locations = [Path.home() / ".cache/huggingface/hub"]
    for value in (os.environ.get("HF_HOME"), os.environ.get("HUGGINGFACE_HUB_CACHE")):
        if value:
            locations.extend([Path(value), Path(value) / "hub"])
    if os.name == "nt":
        locations += [Path("E:/Caches/huggingface/hub"), Path("D:/Caches/huggingface/hub")]
    for base in locations:
        p = base / "models--Qwen--Qwen2.5-7B-Instruct/snapshots" / manifest["revision"]
        if p.is_dir():
            try:
                verify_model(p, manifest)
                return p.resolve()
            except ValueError:
                continue
    return None


def remaining_model_bytes(path: Path, manifest: dict[str, Any]) -> int:
    return sum(max(0, x["size"] - ((path / (x["name"] + ".partial")).stat().st_size if (path / (x["name"] + ".partial")).exists() else 0)) for x in manifest["files"] if not (path / x["name"]).exists())


def download_model(path: Path, manifest: dict[str, Any], root: Path, policy: dict[str, Any]) -> None:
    path.mkdir(parents=True, exist_ok=True)
    remaining = remaining_model_bytes(path, manifest)
    budget(root, policy, remaining + 128 * 1024 * 1024)
    for entry in manifest["files"]:
        dest = path / entry["name"]
        if dest.exists():
            verify_model(path, {"files": [entry]})
            continue
        part = path / (entry["name"] + ".partial")
        url = f'https://huggingface.co/{manifest["model_id"]}/resolve/{manifest["revision"]}/{entry["name"]}'
        for attempt in range(policy["download_retries_per_file"]):
            try:
                offset = part.stat().st_size if part.exists() else 0
                if offset == entry["size"]:
                    part.rename(dest)
                    break
                request = urllib.request.Request(url, headers={"Range": f"bytes={offset}-"} if offset else {})
                with urllib.request.urlopen(request, timeout=policy["network_timeout_seconds"]) as response:
                    append = offset > 0 and response.status == 206
                    if append and not response.headers.get("Content-Range", "").startswith(f"bytes {offset}-"):
                        raise RuntimeError("DOWNLOAD_RANGE_IDENTITY")
                    with part.open("ab" if append else "wb") as f:
                        while data := response.read(8 * 1024 * 1024):
                            f.write(data)
                            if f.tell() > entry["size"]:
                                raise RuntimeError("DOWNLOAD_SIZE_LIMIT")
                if part.stat().st_size != entry["size"]:
                    raise OSError("INCOMPLETE_OFFICIAL_DOWNLOAD")
                part.rename(dest)
                break
            except (OSError, TimeoutError):
                if attempt + 1 == policy["download_retries_per_file"]:
                    raise
                time.sleep(2 ** (attempt + 1))
        if not dest.exists():
            raise RuntimeError("OFFICIAL_MODEL_DOWNLOAD_FAILED")
        verify_model(path, {"files": [entry]})
        budget(root, policy)
    verify_model(path, manifest)


RUNTIME_PROBE = r'''
import importlib.util,json,sys,pathlib
if any(importlib.util.find_spec(x) is None for x in ('torch','transformers','accelerate','numpy','safetensors')):
 print(json.dumps({'status':'NEEDS_ISOLATED_SETUP'}));sys.exit(0)
import torch,transformers,accelerate,numpy,safetensors
def ver(s): return tuple(int(x) for x in s.split('+')[0].split('.')[:2])
isolated=sys.prefix!=sys.base_prefix or ('envs' in pathlib.Path(sys.prefix).parts and (pathlib.Path(sys.prefix)/'conda-meta').exists())
if not isolated or ver(torch.__version__)<(2,7) or not torch.version.cuda or ver(torch.version.cuda)<(12,8) or ver(transformers.__version__)<(4,57) or ver(transformers.__version__)>=(6,0):
 print(json.dumps({'status':'NEEDS_ISOLATED_SETUP','torch':torch.__version__,'transformers':transformers.__version__}));sys.exit(0)
assert torch.cuda.is_available(),'CUDA_UNAVAILABLE_NO_CPU_FALLBACK'
choices=[i for i in range(torch.cuda.device_count()) if 'RTX 5090' in torch.cuda.get_device_name(i)]
assert choices,'CUDA_VISIBLE_DEVICE_IS_NOT_5090'
i=choices[0];torch.cuda.set_device(i)
assert torch.cuda.is_bf16_supported(),'BF16_UNSUPPORTED'
x=torch.ones((64,64),dtype=torch.bfloat16,device=f'cuda:{i}');y=x@x;torch.cuda.synchronize()
assert float(y[0,0])==64,'CUDA_KERNEL_RESULT'
print(json.dumps({'status':'CUDA_KERNEL_PASS','device_index':i,'device_name':torch.cuda.get_device_name(i),'capability':torch.cuda.get_device_capability(i),'total_memory':torch.cuda.get_device_properties(i).total_memory,'python':sys.version,'torch':torch.__version__,'torch_cuda':torch.version.cuda,'transformers':transformers.__version__,'accelerate':accelerate.__version__,'numpy':numpy.__version__,'safetensors':safetensors.__version__,'isolated':isolated}))
'''


def runtime_probe(python: Path, env: dict[str, str]) -> dict[str, Any]:
    result = subprocess.run([str(python), "-c", RUNTIME_PROBE], env=env, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError("CUDA_RUNTIME_PREFLIGHT_FAILED:" + result.stderr[-1500:])
    return json.loads(result.stdout.strip().splitlines()[-1])


def setup_runtime(root: Path, repo: Path, python: Path, policy: dict[str, Any], model_reserve: int) -> Path:
    env = environment(root, repo)
    probe = runtime_probe(python, env)
    if probe["status"] == "CUDA_KERNEL_PASS":
        return python
    target = root / "env"
    exe = target / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    if not exe.exists():
        logged([str(python), "-m", "venv", str(target)], root, "create-env-" + str(time.time_ns()), env, policy)
    stage = root / "wheelhouse"
    stage.mkdir(exist_ok=True)
    if not (root / "WHEEL_LOCK.json").exists():
        logged([str(exe), "-m", "pip", "download", "--only-binary=:all:", "--no-cache-dir", "--index-url", policy["package_index"], "--extra-index-url", policy["torch_index"], "--dest", str(stage), *policy["requirements_when_new_environment_needed"]], root, "download-wheels-" + str(time.time_ns()), env, policy)
        wheels = list(stage.glob("*.whl"))
        expanded = sum(sum(x.file_size for x in zipfile.ZipFile(p).infolist()) for p in wheels)
        staged = sum(p.stat().st_size for p in wheels)
        current = size(root)
        cap = policy["new_model_dependency_budget_bytes"]
        # Conservative install/temp/bytecode allowance and final model reserve.
        if max(current + int(expanded * 1.25) + max(p.stat().st_size for p in wheels), current - staged + int(expanded * 1.25) + model_reserve + 512 * 1024 * 1024) > cap:
            raise RuntimeError("WHEEL_INSTALL_AND_MODEL_PROJECTED_24GIB_EXCEEDED")
        write_new(root / "WHEEL_LOCK.json", {"expanded_bytes": expanded, "files": [{"name": p.name, "sha256": sha(p), "bytes": p.stat().st_size} for p in wheels]})
    lock = load(root / "WHEEL_LOCK.json")
    if not (root / "ENV_READY.json").exists():
        for entry in lock["files"]:
            if sha(stage / entry["name"]) != entry["sha256"]:
                raise RuntimeError("WHEEL_IDENTITY_CHANGED")
        logged([str(exe), "-m", "pip", "install", "--no-index", "--no-cache-dir", "--find-links", str(stage), *policy["requirements_when_new_environment_needed"]], root, "install-isolated-" + str(time.time_ns()), env, policy)
        probe = runtime_probe(exe, env)
        if probe["status"] != "CUDA_KERNEL_PASS":
            raise RuntimeError("NEW_ENV_CUDA_NOT_READY")
        write_new(root / "ENV_READY.json", probe)
        # Delete only this task's hash-locked, newly downloaded wheels; never a
        # user's existing environment/cache. No recursive filesystem removal.
        for entry in lock["files"]:
            p = (stage / entry["name"]).resolve()
            if not p.is_relative_to(root.resolve()) or sha(p) != entry["sha256"]:
                raise RuntimeError("UNSAFE_WHEEL_CLEANUP_TARGET")
            p.unlink()
    budget(root, policy, model_reserve)
    return exe


def infer(root: Path, repo: Path, model_path: Path) -> None:
    policy = load(repo / BASE / "worker_policy_v1.json")
    model_manifest = load(repo / BASE / "qwen_official_manifest_v1.json")
    freeze = load(root / "CONFIG_LOCK.json")
    for p, h in freeze["code_sha256"].items():
        if sha(repo / p) != h:
            raise RuntimeError("FROZEN_CODE_CHANGED")
    for entry in freeze["bundle_files"]:
        if entry["path"].startswith("runtime/") and sha(root / "input" / entry["path"]) != entry["sha256"]:
            raise RuntimeError("RUNTIME_INPUT_CHANGED_AFTER_FREEZE")
    if verify_model(model_path, model_manifest) != freeze["model_file_sha256"]:
        raise RuntimeError("FROZEN_MODEL_CHANGED")
    # Deny evaluator-label file access in the inference process, even if an
    # accidental new helper attempts it. Not a substitute for OS sandboxing.
    evaluation = (root / "input/evaluation").resolve()

    def deny_labels(event: str, args: tuple[Any, ...]) -> None:
        if event == "open" and isinstance(args[0], (str, bytes, os.PathLike)):
            p = Path(os.fsdecode(args[0])).resolve()
            if p.is_relative_to(evaluation):
                raise PermissionError("EVALUATOR_VAULT_ACCESS_FORBIDDEN_DURING_INFERENCE")

    sys.addaudithook(deny_labels)
    torch = importlib.import_module("torch")
    transformers = importlib.import_module("transformers")
    index = freeze["runtime"]["device_index"]
    torch.cuda.set_device(index)
    if torch.cuda.mem_get_info(index)[0] < policy["min_device_free_bytes_before_load"]:
        raise RuntimeError("INSUFFICIENT_FREE_VRAM_DO_NOT_KILL_OTHER_PROCESSES")
    torch.cuda.set_per_process_memory_fraction(policy["max_torch_reserved_bytes"] / torch.cuda.get_device_properties(index).total_memory, index)
    torch.manual_seed(policy["seed"])
    torch.use_deterministic_algorithms(True)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    torch.backends.cudnn.deterministic = True
    tokenizer = transformers.AutoTokenizer.from_pretrained(str(model_path), local_files_only=True, trust_remote_code=False)
    model = transformers.AutoModelForCausalLM.from_pretrained(str(model_path), torch_dtype=torch.bfloat16, device_map={"": index}, attn_implementation="sdpa", local_files_only=True, trust_remote_code=False)
    model.eval()
    if any(p.device.type != "cuda" or p.dtype != torch.bfloat16 for p in model.parameters()):
        raise RuntimeError("MODEL_DTYPE_OR_CPU_OFFLOAD_NOT_AUTHORIZED")
    if model.config.max_position_embeddings < policy["max_context_tokens"] or model.config._attn_implementation != "sdpa":
        raise RuntimeError("ACTUAL_CONTEXT_OR_ATTENTION_DOES_NOT_MATCH_POLICY")
    generation = transformers.GenerationConfig.from_model_config(model.config)
    generation.do_sample = False
    generation.num_beams = 1
    generation.max_new_tokens = policy["max_new_tokens"]
    generation.use_cache = True
    generation.pad_token_id = tokenizer.pad_token_id or tokenizer.eos_token_id
    if not (root / "ACTUAL_GENERATION_CONFIG.json").exists():
        write_new(root / "ACTUAL_GENERATION_CONFIG.json", generation.to_dict())
    elif load(root / "ACTUAL_GENERATION_CONFIG.json") != generation.to_dict():
        raise RuntimeError("ACTUAL_GENERATION_CONFIG_CHANGED_ON_RESUME")
    if not (root / "GPU_LOAD_RECEIPT.json").exists():
        write_new(root / "GPU_LOAD_RECEIPT.json", {"device": torch.cuda.get_device_name(index), "device_index": index, "dtype": "bfloat16", "attention": model.config._attn_implementation, "device_map": getattr(model, "hf_device_map", None), "max_position_embeddings": model.config.max_position_embeddings, "free_total_after_load": torch.cuda.mem_get_info(index), "deterministic_algorithms": torch.are_deterministic_algorithms_enabled(), "actual_generation_config_sha256": sha(root / "ACTUAL_GENERATION_CONFIG.json"), "inference_network": "OFFLINE_LOCAL_FILES_ONLY"})
    raw_dir = root / "raw"
    raw_dir.mkdir(exist_ok=True)
    started = time.monotonic()

    def generate(row: dict[str, Any]) -> dict[str, Any]:
        check_row(row)
        prompt = tokenizer.apply_chat_template(messages(row), tokenize=False, add_generation_prompt=True)
        encoded = tokenizer(prompt, return_tensors="pt", truncation=False)
        count = int(encoded["input_ids"].shape[-1])
        base = {"candidate_id": row["candidate_id"], "input_sha256": sha_text(json.dumps(row, ensure_ascii=False, sort_keys=True)), "prompt_sha256": sha_text(prompt), "generation_config_sha256": sha(root / "ACTUAL_GENERATION_CONFIG.json"), "evidence_uids": [d["uid"] for d in row["evidence"]], "evidence_document_uids": [d["document_uid"] for d in row["evidence"]], "input_tokens": count, "output_tokens": 0, "model_called": False}
        if count > policy["max_input_tokens"]:
            return {**base, "raw_output": None, "verdict": "INSUFFICIENT", "citations": [], "reason": "", "insufficient_reason": "INPUT_TOO_LONG_NO_SILENT_TRUNCATION", "error": "INPUT_TOO_LONG", "elapsed_seconds": 0.0, "peak_allocated_bytes": 0, "peak_reserved_bytes": 0}
        inputs = {k: v.to(index) for k, v in encoded.items()}
        torch.cuda.reset_peak_memory_stats(index)
        torch.cuda.synchronize(index)
        tick = time.perf_counter()
        with torch.inference_mode():
            output = model.generate(**inputs, generation_config=generation)
        torch.cuda.synchronize(index)
        seconds = time.perf_counter() - tick
        generated = output[0, count:]
        raw = tokenizer.decode(generated, skip_special_tokens=True)
        peak = torch.cuda.max_memory_reserved(index)
        if peak > policy["max_torch_reserved_bytes"]:
            raise RuntimeError("VRAM_BUDGET_EXCEEDED")
        result = {**base, "raw_output": raw, **parse_output(raw, row), "output_tokens": len(generated), "model_called": True, "elapsed_seconds": seconds, "peak_allocated_bytes": torch.cuda.max_memory_allocated(index), "peak_reserved_bytes": peak, "generation_stop": "MAX_NEW_TOKENS" if len(generated) == policy["max_new_tokens"] else "EOS"}
        del inputs, output, generated
        return result

    if not (root / "SYNTHETIC_GATE.json").exists():
        records = []
        for row, expected in synthetic_cases():
            p = generate(row)
            records.append({**p, "expected_fictional": expected})
        repeat = generate(synthetic_cases()[0][0])
        passed = all(r["verdict"] == r["expected_fictional"] and not r["error"] for r in records) and repeat["raw_output"] == records[0]["raw_output"]
        write_new(root / "SYNTHETIC_GATE.json", {"records": records, "greedy_repeat": repeat, "all_pass": passed, "D1_not_loaded_yet": True})
        if not passed:
            raise RuntimeError("SYNTHETIC_GATE_FAIL_NO_PROMPT_TUNING")
    elif not load(root / "SYNTHETIC_GATE.json")["all_pass"]:
        raise RuntimeError("PRIOR_SYNTHETIC_GATE_FAILED_DO_NOT_RERUN_TO_CHASE_PASS")
    predictions = []
    for condition, filename in (("L0-F5", "f5.jsonl"), ("L0-Oracle", "oracle.jsonl")):
        data = rows(root / "input/runtime" / filename)
        if len(data) != 120:
            raise RuntimeError("COHORT_SIZE_CHANGED")
        for i, row in enumerate(data):
            if time.monotonic() - started > policy["run_timeout_hours"] * 3600:
                raise RuntimeError("RUN_TIME_BUDGET_EXCEEDED")
            p = raw_dir / f"{condition}-{i:03d}.json"
            if p.exists():
                result = load(p)
                if result["input_sha256"] != sha_text(json.dumps(row, ensure_ascii=False, sort_keys=True)) or result["config_lock_sha256"] != sha(root / "CONFIG_LOCK.json"):
                    raise RuntimeError("RESUME_INPUT_OR_CONFIG_CHANGED")
            else:
                result = {**generate(row), "condition": condition, "run_id": policy["run_id"], "config_lock_sha256": sha(root / "CONFIG_LOCK.json")}
                write_new(p, result)
            predictions.append(result)
            print(json.dumps({"phase": "prediction", "condition": condition, "complete": i + 1, "total": 120, "verdict": result["verdict"]}), flush=True)
            budget(root, policy)
    output = root / "L0_PREDICTIONS.jsonl"
    if not output.exists():
        with output.open("x", encoding="utf-8", newline="\n") as f:
            for p in predictions:
                f.write(json.dumps(p, ensure_ascii=False) + "\n")
    if not (root / "PREDICTION_LOCK.json").exists():
        write_new(root / "PREDICTION_LOCK.json", {"utc": now(), "rows": len(predictions), "prediction_sha256": sha(output), "raw": {p.name: sha(p) for p in sorted(raw_dir.glob("*.json"))}, "all_predictions_before_evaluator_label_join": True})


def return_archive(root: Path) -> None:
    archive = root / "L0_RETURN_NO_WEIGHTS.zip"
    excluded = {"env", "model", "cache", "temp", "wheelhouse"}
    paths = [p for p in sorted(root.rglob("*")) if p.is_file() and not (set(p.relative_to(root).parts) & excluded) and p.name not in {"ORCHESTRATOR_LOCK.json", archive.name, "RETURN_INDEX.json", "COMPLETE.json"} and ".pending-" not in p.name]
    if not (root / "RETURN_INDEX.json").exists():
        write_new(root / "RETURN_INDEX.json", {"files": [{"path": p.relative_to(root).as_posix(), "sha256": sha(p), "bytes": p.stat().st_size} for p in paths], "exclusions": [*sorted(excluded), "self index", "archive", "live orchestrator lock", "later COMPLETE receipt"]})
    if not archive.exists():
        with zipfile.ZipFile(archive, "x", zipfile.ZIP_DEFLATED) as z:
            for p in paths:
                z.write(p, p.relative_to(root).as_posix())
            z.write(root / "RETURN_INDEX.json", "RETURN_INDEX.json")
    with zipfile.ZipFile(archive) as z:
        if z.testzip() is not None:
            raise RuntimeError("RETURN_ARCHIVE_INTEGRITY")
    write_new(root / "COMPLETE.json", {"utc": now(), "status": "L0_STRONG_BASELINE_D1_DEV_COMPLETE / OWNER_REVIEW_REQUIRED", "prediction_sha256": sha(root / "L0_PREDICTIONS.jsonl"), "return_archive_sha256": sha(archive), "return_index_sha256": sha(root / "RETURN_INDEX.json"), "run_manifest_sha256": sha(root / "L0_RUN_MANIFEST.json"), "no_formal_test_GT_training_or_VACE_LM": True})


def orchestrate(args: Any, repo: Path) -> None:
    root = args.work_dir.resolve()
    if os.name == "nt" and root.drive.upper() not in {"D:", "E:"}:
        raise RuntimeError("LARGE_PAYLOADS_MUST_BE_ON_D_OR_E_NOT_C")
    root.mkdir(parents=True, exist_ok=True)
    (root / "temp").mkdir(exist_ok=True)
    policy = load(repo / BASE / "worker_policy_v1.json")
    official = load(repo / BASE / "qwen_official_manifest_v1.json")
    device = device_gate()
    bundle = safe_unpack(args.input_zip, root / "input")
    env = environment(root, repo)
    selected = Path(args.python).resolve() if args.python else Path(sys.executable)
    if args.check_only:
        record = {"utc": now(), "device": device, "private_zip_sha256": sha(args.input_zip), "bundle_manifest_sha256": sha(root / "input/BUNDLE_MANIFEST.json"), "runtime": runtime_probe(selected, env), "new_install_or_model_download": False}
        name = "CHECK_ONLY_" + str(time.time_ns()) + ".json"
        write_new(root / name, record)
        print(json.dumps(record, ensure_ascii=False))
        return
    if (root / "COMPLETE.json").exists():
        complete = load(root / "COMPLETE.json")
        if complete["prediction_sha256"] != sha(root / "L0_PREDICTIONS.jsonl"):
            raise RuntimeError("COMPLETED_RESULT_INTEGRITY_CHANGED")
        print("ALREADY_COMPLETE_NO_RETRY")
        return
    if (root / "HARD_STOP.json").exists():
        raise RuntimeError("PRIOR_HARD_GATE_FAILURE_REQUIRES_OWNER_DECISION_NO_AUTORETRY")
    lock = root / "ORCHESTRATOR_LOCK.json"
    if lock.exists():
        old = load(lock)
        if old["host"] != platform.node():
            raise RuntimeError("LOCK_FROM_ANOTHER_HOST")
        if not process_is_alive(old["pid"]):
            lock.rename(root / ("RECOVERED_DEAD_PROCESS_LOCK_" + str(time.time_ns()) + ".json"))
        else:
            raise RuntimeError("EXISTING_LIVE_ORCHESTRATOR_DO_NOT_DOUBLE_LAUNCH")
    with lock.open("x", encoding="utf-8") as f:
        json.dump({"pid": os.getpid(), "host": platform.node(), "utc": now()}, f)
    try:
        existing = find_existing_model(args.model_dir, official)
        own_model = root / "model" / official["revision"]
        if existing is None and own_model.exists():
            try:
                verify_model(own_model, official)
                existing = own_model
            except ValueError:
                pass
        reserve = 0 if existing else remaining_model_bytes(own_model, official)
        if shutil.disk_usage(root).free < reserve + 512 * 1024 * 1024:
            raise RuntimeError("INSUFFICIENT_DISK_HEADROOM")
        runtime = setup_runtime(root, repo, selected, policy, reserve)
        model_path = existing or root / "model" / official["revision"]
        if existing is None:
            download_model(model_path, official, root, policy)
        actual = runtime_probe(runtime, env)
        pip_result = subprocess.run([str(runtime), "-m", "pip", "freeze", "--all"], env=env, capture_output=True, check=True)
        dependency_sha = hashlib.sha256(pip_result.stdout).hexdigest()
        if not (root / "DEPENDENCIES_FROZEN.txt").exists():
            with (root / "DEPENDENCIES_FROZEN.txt").open("xb") as f:
                f.write(pip_result.stdout)
        config = {"task": policy["task"], "utc": now(), "git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip(), "code_sha256": {p: sha(repo / p) for p in SOURCE_FILES}, "policy": policy, "official_manifest": official, "model_path_private": str(model_path), "model_file_sha256": verify_model(model_path, official), "runtime_python_private": str(runtime), "runtime": actual, "bundle_manifest_sha256": sha(root / "input/BUNDLE_MANIFEST.json"), "bundle_files": bundle["files"], "model_runtime_frozen_before_synthetic_and_D1": True}
        config["dependency_freeze_sha256"] = dependency_sha
        config["device_enumeration"] = device
        if not (root / "CONFIG_LOCK.json").exists():
            write_new(root / "CONFIG_LOCK.json", config)
        else:
            previous = load(root / "CONFIG_LOCK.json")
            for key in ("code_sha256", "policy", "model_file_sha256", "bundle_manifest_sha256", "runtime", "dependency_freeze_sha256"):
                if previous[key] != config[key]:
                    raise RuntimeError("RESUME_FROZEN_IDENTITY_CHANGED:" + key)
        if not (root / "PREDICTION_LOCK.json").exists():
            logged([str(runtime), str(repo / "scripts/research/paper1_l0_worker.py"), "--infer-phase", "--work-dir", str(root), "--model-dir", str(model_path)], root, "infer-" + str(time.time_ns()), env, policy)
        if not (root / "COMPLETE.json").exists():
            logged([str(runtime), str(repo / "scripts/research/evaluate_l0_worker.py"), "--work-dir", str(root)], root, "evaluate-" + str(time.time_ns()), env, policy)
        return_archive(root)
        budget(root, policy)
        print("L0_STRONG_BASELINE_D1_DEV_COMPLETE / OWNER_REVIEW_REQUIRED", flush=True)
    finally:
        lock.unlink(missing_ok=True)
