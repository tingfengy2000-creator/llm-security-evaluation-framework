"""Full D1 development run with the R06 explicit-GQA adapter.

R05 stays blocked and R06 stays passed. This module does not rerun either precheck.
"""
from __future__ import annotations

import hashlib
import os
import platform
import subprocess
import time
from pathlib import Path
from typing import Any

from . import l0_r02 as r02
from . import l0_worker as worker

POLICY = worker.BASE + "/worker_policy_full01_v1.json"
ADAPTER = "src/llmguard/domains/retrieval/hidden_poisoning/method_engineering/explicit_gqa_efficient_sdpa.py"
ADAPTER_SHA = "0cb1d1854ba90d94efa859e03a54f18b25999c4bcaf4c84ac9e43073128eb2d4"
BASELINE = "fdf77cff25158c731a3fdb2dde70a5ad27b0c77d"
RUN_ID = "VACE-L0-D1-20261030-FULL01"
STATUS = "L0_D1_DEV_FULL_COMPLETE / OWNER_REVIEW_REQUIRED"
SOURCES = [*worker.SOURCE_FILES, POLICY, ADAPTER,
           "src/llmguard/domains/retrieval/hidden_poisoning/method_engineering/l0_full01.py",
           "scripts/research/paper1_l0_full01_worker.py"]
PARENT_HASHES = {
    "r01_hard_stop": "67152d26f9708b98e4ff7870897c0fe4f84a2675ff8a355e1813c1ef983d0629",
    "r01_config_lock": "b8eddcaef02b50dbab201a2ceb8d39caa6c57a9136e273c6a79f8e72be01da58",
    "r01_generation": "2e667e6e68c069bac62b13dfb7359b6b8f0e6c96c3664f9af7db27b68521d542",
    "r02_hard_stop": "88c2f00fc70a81d54e72774833ac985afcd3c4c296d7987e5fd59422d4c83b71",
    "r03_complete": "8864389aab8dbc01f57268e8e8a26aada0243d0608c6e9785c9337cd4dc19e0c",
    "r05_report": "6c329dc9a93ce27aae8d60c6bd323cac79a1371152f06545a0989c7e5f88c90c",
    "r05_failure": "7fc88eef47f6ca417f98238d9c766625b92453e7642cea6f2a8f6d11c01da999",
    "r06_report": "54143163556d3fbbc3ad3d487b1601967e8c83531f39c466bc75df9d0cbaa66a",
    "r06_protocol": "55c9d4aacc7f7571c11f31b32c64d911a3c2bc22c8cdca86a5d4fa8ff95b1db7",
}


def full01_policy(repo: Path) -> dict[str, Any]:
    policy = worker.load(repo / POLICY)
    identity = (
        policy["task"] == "P1-L0-D1-FULL-EXECUTION-01"
        and policy["run_id"] == RUN_ID
        and policy["owner_approval"] == "P1-L0-D1-FULL-EXECUTION-01"
        and policy["baseline_commit"] == BASELINE
        and policy["max_input_tokens"] == 31744
        and policy["max_new_tokens"] == 1024
        and policy["max_context_tokens"] == 32768
        and policy["max_torch_reserved_bytes"] == 32212254720
        and policy["seed"] == 20261029
        and policy["do_sample"] is False
        and policy["num_beams"] == 1
        and policy["attention_adapter"] == "explicit_gqa_efficient_r06"
        and policy["adapter_module_sha256"] == ADAPTER_SHA
        and policy["min_new_tokens"] is None
        and policy["capacity_probe_min_new_tokens_not_used"] is True
        and policy["synthetic_semantic_requirement"] == "DIAGNOSTIC_ONLY"
        and policy["overflow_policy"] == "INPUT_FAILURE_AS_INSUFFICIENT_FULL_DENOMINATOR_NO_TRUNCATION"
        and policy["no_empty_cache"] is True
        and policy["no_allocator_change"] is True
        and policy["reuse_only_no_download_or_install"] is True
    )
    if not identity:
        raise RuntimeError("FULL01_POLICY_IDENTITY")
    return policy


def parent_files(r01: Path, r02: Path, r03: Path, r05: Path, r06: Path) -> dict[str, Path]:
    return {
        "r01_hard_stop": r01 / "HARD_STOP.json",
        "r01_config_lock": r01 / "CONFIG_LOCK.json",
        "r01_generation": r01 / "ACTUAL_GENERATION_CONFIG.json",
        "r02_hard_stop": r02 / "HARD_STOP.json",
        "r03_complete": r03 / "COMPLETE.json",
        "r05_report": r05 / "PRECHECK_REPORT.md",
        "r05_failure": r05 / "FAILURE.json",
        "r06_report": r06 / "PRECHECK_REPORT.md",
        "r06_protocol": r06 / "R06_STABILITY_PROTOCOL.json",
    }


def assert_parents(r01: Path, r02: Path, r03: Path, r05: Path, r06: Path) -> None:
    for key, path in parent_files(r01, r02, r03, r05, r06).items():
        if worker.sha(path) != PARENT_HASHES[key]:
            raise RuntimeError("FULL01_PARENT_EVIDENCE_CHANGED:" + key)


def disjoint(root: Path, priors: list[Path]) -> None:
    for prior in priors:
        if prior == root or root.is_relative_to(prior) or prior.is_relative_to(root):
            raise RuntimeError("FULL01_CANNOT_WRITE_INSIDE_PRIOR_RUN")
    if os.name == "nt" and root.drive.upper() not in {"D:", "E:"}:
        raise RuntimeError("FULL01_PAYLOAD_MUST_STAY_ON_D_OR_E")


def require_prediction_seal(lock: dict[str, Any]) -> None:
    if lock.get("rows") != 240 or len(lock.get("raw") or {}) != 240:
        raise RuntimeError("INCOMPLETE_PREDICTION_SEAL")


def orchestrate_full01(args: Any, repo: Path) -> None:
    r01 = args.r01_dir.resolve()
    r02_dir = args.r02_dir.resolve()
    r03 = args.r03_dir.resolve()
    r05 = args.r05_dir.resolve()
    r06 = args.r06_dir.resolve()
    root = args.work_dir.resolve()
    priors = [r01, r02_dir, r03, r05, r06]
    disjoint(root, priors)
    policy = full01_policy(repo)
    if worker.sha(repo / ADAPTER) != ADAPTER_SHA:
        raise RuntimeError("ADAPTER_SHA_MISMATCH")
    assert_parents(r01, r02_dir, r03, r05, r06)
    old, snapshot, reference = r02.parent_identity(r01, repo)
    if root.exists() and not (root / "FULL01_ORIGIN.json").exists():
        if any(p.name not in {"cache", "temp"} or not p.is_dir() or p.is_symlink() or not p.resolve().is_relative_to(root) for p in root.iterdir()):
            raise RuntimeError("FULL01_REQUIRES_EMPTY_NEW_RUN_DIRECTORY")
    root.mkdir(parents=True, exist_ok=True)
    (root / "temp").mkdir(exist_ok=True)
    origin = {"owner_approval": policy["owner_approval"], "run_id": RUN_ID, "baseline_commit": BASELINE, "adapter_sha256": ADAPTER_SHA, "r01_private": str(r01)}
    if not (root / "FULL01_ORIGIN.json").exists():
        worker.write_new(root / "FULL01_ORIGIN.json", origin)
    elif worker.load(root / "FULL01_ORIGIN.json") != origin:
        raise RuntimeError("FULL01_ORIGIN_CHANGED")
    if (root / "HARD_STOP.json").exists():
        raise RuntimeError("FULL01_PRIOR_HARD_STOP_REQUIRES_OWNER")
    if (root / "COMPLETE.json").exists():
        complete = worker.load(root / "COMPLETE.json")
        if complete.get("status") != STATUS or worker.sha(root / "L0_PREDICTIONS.jsonl") != complete["prediction_sha256"]:
            raise RuntimeError("FULL01_COMPLETED_RESULT_INTEGRITY")
        print("FULL01_ALREADY_COMPLETE_NO_RETRY", flush=True)
        return
    lock = root / "ORCHESTRATOR_LOCK.json"
    if lock.exists():
        prior = worker.load(lock)
        if prior["host"] != platform.node() or worker.process_is_alive(prior["pid"]):
            raise RuntimeError("FULL01_EXISTING_LIVE_OR_FOREIGN_PROCESS")
        lock.rename(root / ("RECOVERED_DEAD_PROCESS_LOCK_" + str(time.time_ns()) + ".json"))
    worker.write_new(lock, {"pid": os.getpid(), "host": platform.node(), "utc": worker.now()})
    try:
        device = worker.device_gate()
        if device["devices"] != old["device_enumeration"]["devices"]:
            raise RuntimeError("FULL01_DEVICE_DIFFERS_FROM_R01")
        env = worker.environment(root, repo)
        env.pop("PYTORCH_CUDA_ALLOC_CONF", None)
        runtime = Path(old["runtime_python_private"])
        model = Path(old["model_path_private"])
        actual = worker.runtime_probe(runtime, env)
        if actual != old["runtime"] or actual["status"] != "CUDA_KERNEL_PASS":
            raise RuntimeError("FULL01_RUNTIME_DIFFERS_FROM_R01")
        official = worker.load(repo / worker.BASE / "qwen_official_manifest_v1.json")
        model_hashes = worker.verify_model(model, official)
        if model_hashes != old["model_file_sha256"]:
            raise RuntimeError("FULL01_MODEL_DIFFERS_FROM_R01")
        dependency = subprocess.run([str(runtime), "-m", "pip", "freeze", "--all"], env=env, capture_output=True, check=True).stdout
        if hashlib.sha256(dependency).hexdigest() != old["dependency_freeze_sha256"] or dependency != reference["DEPENDENCIES_FROZEN.txt"]:
            raise RuntimeError("FULL01_DEPENDENCIES_DIFFERS_FROM_R01")
        bundle = r02.copy_frozen_inputs(r01, root, old)
        remaining = policy["new_model_dependency_budget_bytes"] - worker.size(r01)
        if remaining <= 0:
            raise RuntimeError("NEW_MODEL_DEPENDENCY_24GIB_BUDGET_EXCEEDED")
        monitoring = {**policy, "new_model_dependency_budget_bytes": remaining}
        worker.budget(root, monitoring)
        if not (root / "DEPENDENCIES_FROZEN.txt").exists():
            with (root / "DEPENDENCIES_FROZEN.txt").open("xb") as file:
                file.write(dependency)
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()
        if subprocess.call(["git", "merge-base", "--is-ancestor", BASELINE, head], cwd=repo) != 0:
            raise RuntimeError("FULL01_BASELINE_NOT_ANCESTOR")
        config = {"task": policy["task"], "utc": worker.now(), "git_head": head, "code_sha256": {p: worker.sha(repo / p) for p in SOURCES},
                  "policy": policy, "official_manifest": official, "model_path_private": str(model), "model_file_sha256": model_hashes,
                  "runtime_python_private": str(runtime), "runtime": actual, "bundle_manifest_sha256": old["bundle_manifest_sha256"],
                  "bundle_files": bundle["files"], "dependency_freeze_sha256": old["dependency_freeze_sha256"], "device_enumeration": device,
                  "parent_r01_config_sha256": worker.sha(r01 / "CONFIG_LOCK.json"), "parent_r01_generation_sha256": worker.sha(r01 / "ACTUAL_GENERATION_CONFIG.json"),
                  "additional_evaluator_vaults_private": [str(r01 / "input/evaluation")], "model_runtime_frozen_before_synthetic_and_D1": True,
                  "adapter_sha256": ADAPTER_SHA, "r05_not_rewritten": "R05_PRECHECK_BLOCKED", "r06_not_rewritten": "R06_STABILITY_PRECHECK_PASS"}
        if not (root / "CONFIG_LOCK.json").exists():
            worker.write_new(root / "CONFIG_LOCK.json", config)
        else:
            previous = worker.load(root / "CONFIG_LOCK.json")
            for key in ("code_sha256", "policy", "model_file_sha256", "runtime", "bundle_manifest_sha256", "bundle_files", "dependency_freeze_sha256", "parent_r01_generation_sha256", "adapter_sha256"):
                if previous[key] != config[key]:
                    raise RuntimeError("FULL01_FROZEN_IDENTITY_CHANGED:" + key)
        if not (root / "PREDICTION_LOCK.json").exists():
            worker.logged([str(runtime), str(repo / "scripts/research/paper1_l0_worker.py"), "--infer-phase", "--work-dir", str(root), "--model-dir", str(model)], root, "infer-" + str(time.time_ns()), env, monitoring)
        require_prediction_seal(worker.load(root / "PREDICTION_LOCK.json"))
        assert_parents(r01, r02_dir, r03, r05, r06)
        r02.assert_parent(r01, snapshot)
        worker.logged([str(runtime), str(repo / "scripts/research/evaluate_l0_worker.py"), "--work-dir", str(root)], root, "evaluate-" + str(time.time_ns()), env, monitoring)
        assert_parents(r01, r02_dir, r03, r05, r06)
        r02.assert_parent(r01, snapshot)
        worker.return_archive(root, STATUS)
        worker.budget(root, monitoring)
        print(STATUS, flush=True)
    finally:
        lock.unlink(missing_ok=True)
