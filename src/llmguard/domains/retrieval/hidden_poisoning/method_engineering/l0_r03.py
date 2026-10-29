"""R03 length cap: same verifier, model, and inputs; shorter max_input_tokens only.

No download/install. R01 and R02 stay read-only, including both HARD_STOP files.
Over-long rows are INSUFFICIENT with INPUT_TOO_LONG_NO_SILENT_TRUNCATION.
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

POLICY = worker.BASE + "/worker_policy_r03_v1.json"
R02_SOURCE = "a31ade51c2e6923991b81895163060b80db6da4f"
R02_HARD_STOP_SHA = "88c2f00fc70a81d54e72774833ac985afcd3c4c296d7987e5fd59422d4c83b71"
R02_SYNTHETIC_GATE_SHA = "c970884b79927b08d7310f74cf574260755f9efa47a30630db9bff70a7f5d627"
R02_CONFIG_LOCK_SHA = "60c604e4af99d6b59767e73ecf6d53603fe138968706107959ec18503068aa73"
R02_RAW = [f"L0-F5-00{i}.json" for i in range(5)]
DELTA = {"run_id", "parent_run_id", "owner_approval", "max_input_tokens", "r01_run_id", "length_cap_tokens", "rejected_probe_tokens", "oom_input_tokens"}
SOURCES = [*worker.SOURCE_FILES, POLICY, "configs/research/paper1_l0/worker_policy_r02_v1.json",
           "src/llmguard/domains/retrieval/hidden_poisoning/method_engineering/l0_r02.py",
           "src/llmguard/domains/retrieval/hidden_poisoning/method_engineering/l0_r03.py",
           "scripts/research/paper1_l0_r03_worker.py"]


def r03_policy(repo: Path) -> dict[str, Any]:
    policy = worker.load(repo / POLICY)
    old = r02.r02_policy(repo)
    if {k: v for k, v in policy.items() if k not in DELTA} != {k: v for k, v in old.items() if k not in DELTA}:
        raise RuntimeError("R03_MUST_NOT_CHANGE_OTHER_FROZEN_PARAMETERS")
    identity = (
        policy["run_id"] == "VACE-L0-D1-20261029-R03"
        and policy["parent_run_id"] == "VACE-L0-D1-20261029-R02"
        and policy["r01_run_id"] == old["parent_run_id"] == "VACE-L0-D1-20261029-R01"
        and policy["owner_approval"] == "R03_LENGTH_CAP_CONTINUATION"
        and policy["max_input_tokens"] == policy["length_cap_tokens"] == 7200
        and policy["rejected_probe_tokens"] == 7400
        and policy["oom_input_tokens"] == 10820
        and policy["synthetic_semantic_requirement"] == "DIAGNOSTIC_ONLY"
        and policy["reuse_only_no_download_or_install"] is True
        and policy["overflow_policy"] == "INPUT_FAILURE_AS_INSUFFICIENT_FULL_DENOMINATOR_NO_TRUNCATION"
    )
    if not identity or policy["max_input_tokens"] >= old["max_input_tokens"]:
        raise RuntimeError("R03_POLICY_IDENTITY")
    return policy


def assert_payload_drive(root: Path) -> None:
    if os.name == "nt" and root.drive.upper() not in {"D:", "E:"}:
        raise RuntimeError("R03_PAYLOAD_MUST_STAY_ON_D_OR_E")


def disjoint_prior(prior: Path, root: Path) -> None:
    if prior == root or root.is_relative_to(prior) or prior.is_relative_to(root):
        raise RuntimeError("R03_CANNOT_WRITE_IN_OR_CONTAIN_R01_OR_R02")
    assert_payload_drive(root)


def verify_r02(path: Path, r01_config: dict[str, Any]) -> dict[str, str]:
    pinned = {
        "HARD_STOP.json": R02_HARD_STOP_SHA,
        "SYNTHETIC_GATE.json": R02_SYNTHETIC_GATE_SHA,
        "CONFIG_LOCK.json": R02_CONFIG_LOCK_SHA,
    }
    for name, digest in pinned.items():
        file = (path / name).resolve()
        if not file.is_relative_to(path) or not file.is_file() or worker.sha(file) != digest:
            raise RuntimeError("R02_FAILED_RECORD_CHANGED:" + name)
    cfg = worker.load(path / "CONFIG_LOCK.json")
    if cfg["git_head"] != R02_SOURCE or cfg["policy"]["run_id"] != "VACE-L0-D1-20261029-R02" or cfg["policy"]["max_input_tokens"] != 31744:
        raise RuntimeError("R02_SOURCE_OR_POLICY_CHANGED")
    if cfg["model_path_private"] != r01_config["model_path_private"] or cfg["runtime_python_private"] != r01_config["runtime_python_private"]:
        raise RuntimeError("R02_RESOURCE_PATH_DIFFERS_FROM_R01")
    if any((path / name).exists() for name in ("COMPLETE.json", "PREDICTION_LOCK.json", "L0_PREDICTIONS.jsonl")):
        raise RuntimeError("R02_UNEXPECTED_COMPLETION_EVIDENCE")
    names = sorted(p.name for p in (path / "raw").glob("*.json"))
    if names != R02_RAW:
        raise RuntimeError("R02_RAW_EVIDENCE_COUNT_CHANGED")
    return r02.parent_snapshot(path)


def disclosure(policy: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": policy["run_id"],
        "parent_run_id": policy["parent_run_id"],
        "r01_run_id": policy["r01_run_id"],
        "owner_approval": policy["owner_approval"],
        "origin_had_no_r03_podr_at_b22a118": True,
        "only_protocol_parameter_changed": "max_input_tokens",
        "max_input_tokens_r01_r02": 31744,
        "max_input_tokens_r03": 7200,
        "dtype": "bfloat16",
        "attention": "sdpa",
        "deterministic_algorithms": True,
        "quantization_cpu_offload_alternative_model_or_allocator_change": False,
        "silent_truncation": False,
        "overlong_record": "INSUFFICIENT INPUT_TOO_LONG_NO_SILENT_TRUNCATION model_called false full denominator",
        "semantic_gate": "DIAGNOSTIC_ONLY continued from PODR-153; not a new verdict relaxation",
        "R01_remains_failed_not_relabelled": True,
        "R02_remains_cuda_oom_failed_not_relabelled": True,
        "r02_completed_6707_peak_reserved_bytes": 29196550144,
        "r02_oom_input_tokens": 10820,
        "attention_matrix_bytes_at_10820": 28 * 4 * 10820 * 10820,
        "max_torch_reserved_bytes": 32212254720,
        "selected_probe_headroom_bytes": 32212254720 - 30935089152,
        "rejected_7400_headroom_bytes": 32212254720 - 31784435712,
        "probes": [
            {"tokens": 6707, "new_tokens": 1, "status": "PASS", "peak_reserved_bytes": 28858908672, "peak_allocated_bytes": 27779841536},
            {"tokens": 7200, "new_tokens": 1, "status": "PASS", "peak_reserved_bytes": 30930894848, "peak_allocated_bytes": 29609686528},
            {"tokens": 7200, "new_tokens": 256, "status": "PASS", "peak_reserved_bytes": 30935089152, "peak_allocated_bytes": 29609686528},
            {"tokens": 7400, "new_tokens": 1, "status": "REJECTED_HEADROOM", "peak_reserved_bytes": 31784435712, "peak_allocated_bytes": 30387698688},
        ],
        "tokenizer_coverage_not_a_score": {"f5_at_or_below_cap": 33, "f5_total": 120, "oracle_at_or_below_cap": 102, "oracle_total": 120, "overlong_kept_in_denominator": 105},
        "no_private_candidate_or_label_text": True,
    }


def orchestrate_r03(args: Any, repo: Path) -> None:
    r01, r02_dir, root = args.r01_dir.resolve(), args.r02_dir.resolve(), args.work_dir.resolve()
    disjoint_prior(r01, root)
    disjoint_prior(r02_dir, root)
    if r01 == r02_dir:
        raise RuntimeError("R03_CANNOT_WRITE_IN_OR_CONTAIN_R01_OR_R02")
    policy = r03_policy(repo)
    old, r01_snapshot, reference = r02.parent_identity(r01, repo)
    r02_snapshot = verify_r02(r02_dir, old)
    if root.exists() and not (root / "R03_ORIGIN.json").exists():
        if any(p.name not in {"cache", "temp"} or not p.is_dir() or p.is_symlink() or not p.resolve().is_relative_to(root) for p in root.iterdir()):
            raise RuntimeError("R03_REQUIRES_EMPTY_NEW_RUN_DIRECTORY")
    root.mkdir(parents=True, exist_ok=True)
    (root / "temp").mkdir(exist_ok=True)
    origin = {"owner_approval": policy["owner_approval"], "run_id": policy["run_id"], "r01_private": str(r01), "r02_private": str(r02_dir),
              "r01_snapshot": r01_snapshot, "r02_snapshot": r02_snapshot, "r01_reference_zip_sha256": r02.RETURN_SHA, "r02_hard_stop_sha256": R02_HARD_STOP_SHA}
    if not (root / "R03_ORIGIN.json").exists():
        worker.write_new(root / "R03_ORIGIN.json", origin)
    elif worker.load(root / "R03_ORIGIN.json") != origin:
        raise RuntimeError("R03_PARENT_ORIGIN_CHANGED")
    if (root / "HARD_STOP.json").exists():
        raise RuntimeError("R03_PRIOR_ENGINEERING_HARD_STOP_REQUIRES_OWNER")
    lock = root / "ORCHESTRATOR_LOCK.json"
    if lock.exists():
        prior = worker.load(lock)
        if prior["host"] != platform.node() or worker.process_is_alive(prior["pid"]):
            raise RuntimeError("R03_EXISTING_LIVE_OR_FOREIGN_PROCESS")
        lock.rename(root / ("RECOVERED_DEAD_PROCESS_LOCK_" + str(time.time_ns()) + ".json"))
    worker.write_new(lock, {"pid": os.getpid(), "host": platform.node(), "utc": worker.now()})
    try:
        device = worker.device_gate()
        if device["devices"] != old["device_enumeration"]["devices"]:
            raise RuntimeError("R03_DEVICE_OR_DRIVER_DIFFERS_FROM_R01")
        env = worker.environment(root, repo)
        runtime = Path(old["runtime_python_private"])
        model = Path(old["model_path_private"])
        actual = worker.runtime_probe(runtime, env)
        if actual != old["runtime"] or actual["status"] != "CUDA_KERNEL_PASS":
            raise RuntimeError("R03_RUNTIME_DIFFERS_FROM_R01")
        official = worker.load(repo / worker.BASE / "qwen_official_manifest_v1.json")
        model_hashes = worker.verify_model(model, official)
        if model_hashes != old["model_file_sha256"]:
            raise RuntimeError("R03_MODEL_DIFFERS_FROM_R01")
        dependency = subprocess.run([str(runtime), "-m", "pip", "freeze", "--all"], env=env, capture_output=True, check=True).stdout
        if hashlib.sha256(dependency).hexdigest() != old["dependency_freeze_sha256"] or dependency != reference["DEPENDENCIES_FROZEN.txt"]:
            raise RuntimeError("R03_DEPENDENCIES_DIFFERS_FROM_R01")
        bundle = r02.copy_frozen_inputs(r01, root, old)
        remaining = policy["new_model_dependency_budget_bytes"] - worker.size(r01) - worker.size(r02_dir)
        if remaining <= 0:
            raise RuntimeError("NEW_MODEL_DEPENDENCY_24GIB_BUDGET_EXCEEDED")
        monitoring = {**policy, "new_model_dependency_budget_bytes": remaining}
        worker.budget(root, monitoring)
        r02.assert_parent(r01, r01_snapshot)
        r02.assert_parent(r02_dir, r02_snapshot)
        if args.check_only:
            worker.write_new(root / ("CHECK_ONLY_" + str(time.time_ns()) + ".json"), {"utc": worker.now(), "device": device, "runtime": actual, "input_files_exact": True, "same_r01_model_dependencies": True, "no_download_install_or_parent_write": True, "r01_and_r02_unchanged": True, "max_input_tokens": 7200})
            print("R03_CHECK_ONLY_PASS_NO_NEW_MODEL_OR_DEPENDENCY", flush=True)
            return
        if (root / "COMPLETE.json").exists():
            complete = worker.load(root / "COMPLETE.json")
            if worker.sha(root / "L0_PREDICTIONS.jsonl") != complete["prediction_sha256"] or worker.sha(root / "L0_RETURN_NO_WEIGHTS.zip") != complete["return_archive_sha256"]:
                raise RuntimeError("R03_COMPLETED_RESULT_INTEGRITY")
            print("R03_ALREADY_COMPLETE_NO_RETRY", flush=True)
            return
        if not (root / "DEPENDENCIES_FROZEN.txt").exists():
            with (root / "DEPENDENCIES_FROZEN.txt").open("xb") as file:
                file.write(dependency)
        config = {"task": policy["task"], "utc": worker.now(), "git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip(),
                  "code_sha256": {p: worker.sha(repo / p) for p in SOURCES}, "policy": policy, "official_manifest": official,
                  "model_path_private": str(model), "model_file_sha256": model_hashes, "runtime_python_private": str(runtime), "runtime": actual,
                  "bundle_manifest_sha256": old["bundle_manifest_sha256"], "bundle_files": bundle["files"], "dependency_freeze_sha256": old["dependency_freeze_sha256"],
                  "device_enumeration": device, "parent_r01_config_sha256": worker.sha(r01 / "CONFIG_LOCK.json"),
                  "additional_evaluator_vaults_private": [str(r01 / "input/evaluation"), str(r02_dir / "input/evaluation")],
                  "parent_r01_generation_sha256": worker.sha(r01 / "ACTUAL_GENERATION_CONFIG.json"), "model_runtime_frozen_before_synthetic_and_D1": True}
        if not (root / "CONFIG_LOCK.json").exists():
            worker.write_new(root / "CONFIG_LOCK.json", config)
        else:
            previous = worker.load(root / "CONFIG_LOCK.json")
            for key in ("code_sha256", "policy", "model_file_sha256", "runtime", "bundle_manifest_sha256", "bundle_files", "dependency_freeze_sha256", "parent_r01_config_sha256", "parent_r01_generation_sha256", "additional_evaluator_vaults_private"):
                if previous[key] != config[key]:
                    raise RuntimeError("R03_FROZEN_IDENTITY_CHANGED:" + key)
        if not (root / "R03_PROTOCOL_DISCLOSURE.json").exists():
            worker.write_new(root / "R03_PROTOCOL_DISCLOSURE.json", disclosure(policy))
        if not (root / "PREDICTION_LOCK.json").exists():
            worker.logged([str(runtime), str(repo / "scripts/research/paper1_l0_worker.py"), "--infer-phase", "--work-dir", str(root), "--model-dir", str(model)], root, "infer-" + str(time.time_ns()), env, monitoring)
        r02.assert_parent(r01, r01_snapshot)
        r02.assert_parent(r02_dir, r02_snapshot)
        worker.logged([str(runtime), str(repo / "scripts/research/evaluate_l0_worker.py"), "--work-dir", str(root)], root, "evaluate-" + str(time.time_ns()), env, monitoring)
        r02.assert_parent(r01, r01_snapshot)
        r02.assert_parent(r02_dir, r02_snapshot)
        if not (root / "R01_R02_UNCHANGED_FINAL.json").exists():
            worker.write_new(root / "R01_R02_UNCHANGED_FINAL.json", {"utc": worker.now(), "r01_and_r02_records_and_HARD_STOP_unchanged": True, "r01_snapshot": r01_snapshot, "r02_snapshot": r02_snapshot})
        worker.return_archive(root)
        worker.budget(root, monitoring)
        print("R03_L0_STRONG_BASELINE_D1_DEV_COMPLETE / OWNER_REVIEW_REQUIRED", flush=True)
    finally:
        lock.unlink(missing_ok=True)
        r02.assert_parent(r01, r01_snapshot)
        r02.assert_parent(r02_dir, r02_snapshot)
