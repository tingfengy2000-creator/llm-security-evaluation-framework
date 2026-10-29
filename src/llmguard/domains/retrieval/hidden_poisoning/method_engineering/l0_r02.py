"""PODR-153 R02: same verifier/resources/inputs; semantic accuracy diagnostic.

No download/install route. R01 is read-only and its failed records remain intact.
"""
from __future__ import annotations

import hashlib
import io
import os
import platform
import subprocess
import time
import zipfile
from pathlib import Path
from typing import Any

from . import l0_worker as worker

POLICY = worker.BASE + "/worker_policy_r02_v1.json"
RETURN = "docs/research/stage6_1_hidden_knowledge_poisoning/core144/vace_lite/L0_5090_SYNTHETIC_GATE_EVIDENCE_RETURN_V1.zip"
RETURN_SHA = "a56c8b79a0a61879629a305325a7cbf1d0188ad7c73a187e93c31e528be838e6"
R01_SOURCE = "a83437ab0a685d69114093fd4bd0e6ab22f354aa"
SOURCES = [*worker.SOURCE_FILES, POLICY, "src/llmguard/domains/retrieval/hidden_poisoning/method_engineering/l0_r02.py", "scripts/research/paper1_l0_r02_worker.py"]
EXCLUDED = {"env", "model", "cache", "temp", "wheelhouse"}


def r02_policy(repo: Path) -> dict[str, Any]:
    policy = worker.load(repo / POLICY)
    old = worker.load(repo / worker.BASE / "worker_policy_v1.json")
    additions = {"synthetic_semantic_requirement", "parent_run_id", "owner_approval", "reuse_only_no_download_or_install"}
    if {k: v for k, v in policy.items() if k not in additions | {"run_id"}} != {k: v for k, v in old.items() if k != "run_id"}:
        raise RuntimeError("R02_MUST_NOT_CHANGE_R01_PARAMETERS")
    if policy["run_id"] != "VACE-L0-D1-20261029-R02" or policy["parent_run_id"] != old["run_id"] or policy["owner_approval"] != "PODR-153" or policy["synthetic_semantic_requirement"] != "DIAGNOSTIC_ONLY" or policy["reuse_only_no_download_or_install"] is not True:
        raise RuntimeError("R02_POLICY_IDENTITY")
    return policy


def disjoint_roots(parent: Path, root: Path) -> None:
    if parent == root or root.is_relative_to(parent) or parent.is_relative_to(root):
        raise RuntimeError("R02_CANNOT_WRITE_IN_OR_CONTAIN_R01")
    if os.name == "nt" and root.drive.upper() not in {"D:", "E:"}:
        raise RuntimeError("R02_PAYLOAD_MUST_STAY_ON_D_OR_E")


def failure_reference(repo: Path) -> dict[str, bytes]:
    blob = (repo / RETURN).read_bytes()
    if hashlib.sha256(blob).hexdigest() != RETURN_SHA:
        raise RuntimeError("R01_RETURN_ZIP_SHA_CHANGED")
    lines = (repo / (RETURN + ".sha256")).read_text("utf-8").splitlines()
    expected = {line.split("  ", 1)[1]: line.split("  ", 1)[0] for line in lines if line.strip()}
    with zipfile.ZipFile(io.BytesIO(blob)) as archive:
        names = archive.namelist()
        if len(names) != 10 or len(set(names)) != 10 or set(names) != set(expected) - {Path(RETURN).name} or archive.testzip():
            raise RuntimeError("R01_RETURN_MANIFEST_INTEGRITY")
        files = {name: archive.read(name) for name in names}
    if any(hashlib.sha256(data).hexdigest() != expected[name] for name, data in files.items()):
        raise RuntimeError("R01_RETURN_ORIGINAL_HASH_CHANGED")
    return files


def parent_snapshot(parent: Path) -> dict[str, str]:
    files = {}
    for folder, directories, names in os.walk(parent):
        directories[:] = [name for name in directories if name not in EXCLUDED]
        for name in sorted(names):
            p = Path(folder) / name
            if p.is_file():
                files[p.relative_to(parent).as_posix()] = worker.sha(p)
    return files


def parent_identity(parent: Path, repo: Path) -> tuple[dict[str, Any], dict[str, str], dict[str, bytes]]:
    reference = failure_reference(repo)
    for name, data in reference.items():
        p = (parent / name).resolve()
        if not p.is_relative_to(parent) or not p.is_file() or worker.sha(p) != hashlib.sha256(data).hexdigest():
            raise RuntimeError("R01_FAILED_RECORD_CHANGED:" + name)
    old = worker.load(parent / "CONFIG_LOCK.json")
    if old["git_head"] != R01_SOURCE or old["policy"] != worker.load(repo / worker.BASE / "worker_policy_v1.json"):
        raise RuntimeError("R01_SOURCE_OR_POLICY_CHANGED")
    if any((parent / name).exists() for name in ("PREDICTION_LOCK.json", "COMPLETE.json", "L0_PREDICTIONS.jsonl")) or list((parent / "raw").glob("*.json")):
        raise RuntimeError("R01_UNEXPECTED_D1_EXECUTION_EVIDENCE")
    for field in ("runtime_python_private", "model_path_private"):
        p = Path(old[field]).resolve()
        if not p.exists() or not p.is_relative_to(parent):
            raise RuntimeError("R01_RESOURCE_PATH_IDENTITY_CHANGED")
    return old, parent_snapshot(parent), reference


def assert_parent(parent: Path, snapshot: dict[str, str]) -> None:
    if parent_snapshot(parent) != snapshot:
        raise RuntimeError("R01_IMMUTABILITY_BREACH_STOP_R02")


def copy_frozen_inputs(parent: Path, root: Path, old: dict[str, Any]) -> dict[str, Any]:
    source = parent / "input"
    if worker.sha(source / "BUNDLE_MANIFEST.json") != old["bundle_manifest_sha256"]:
        raise RuntimeError("R01_INPUT_MANIFEST_SHA_CHANGED")
    manifest = worker.load(source / "BUNDLE_MANIFEST.json")
    if manifest["files"] != old["bundle_files"] or (manifest["groups"], manifest["candidates"], manifest["families"]) != (40, 120, 13):
        raise RuntimeError("R02_COHORT_OR_INPUT_LINEAGE_CHANGED")
    entries = [*manifest["files"], {"path": "BUNDLE_MANIFEST.json", "sha256": old["bundle_manifest_sha256"]}]
    for entry in entries:
        src = (source / entry["path"]).resolve()
        dst = (root / "input" / entry["path"]).resolve()
        if not src.is_relative_to(source.resolve()) or not dst.is_relative_to((root / "input").resolve()) or worker.sha(src) != entry["sha256"]:
            raise RuntimeError("R02_INPUT_COPY_IDENTITY")
        if not dst.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            tmp = dst.with_name(dst.name + ".pending-" + str(time.time_ns()))
            with tmp.open("xb") as file:
                file.write(src.read_bytes())
            tmp.rename(dst)
        if worker.sha(dst) != entry["sha256"]:
            raise RuntimeError("R02_EXISTING_INPUT_CHANGED")
    return manifest


def orchestrate_r02(args: Any, repo: Path) -> None:
    parent, root = args.r01_dir.resolve(), args.work_dir.resolve()
    disjoint_roots(parent, root)  # before ANY creation or incident write
    policy = r02_policy(repo)
    old, snapshot, reference = parent_identity(parent, repo)
    if root.exists() and not (root / "R02_ORIGIN.json").exists():
        # Python startup may create the explicitly redirected task cache before
        # this entrypoint runs. Never accept prior raw/results/config here.
        if any(p.name not in {"cache", "temp"} or not p.is_dir() or p.is_symlink() or not p.resolve().is_relative_to(root) for p in root.iterdir()):
            raise RuntimeError("R02_REQUIRES_EMPTY_NEW_RUN_DIRECTORY")
    root.mkdir(parents=True, exist_ok=True)
    (root / "temp").mkdir(exist_ok=True)
    origin = {"owner_approval": "PODR-153", "run_id": policy["run_id"], "parent_private": str(parent), "parent_snapshot": snapshot, "parent_reference_zip_sha256": RETURN_SHA}
    if not (root / "R02_ORIGIN.json").exists():
        worker.write_new(root / "R02_ORIGIN.json", origin)
    elif worker.load(root / "R02_ORIGIN.json") != origin:
        raise RuntimeError("R02_PARENT_ORIGIN_CHANGED")
    if (root / "HARD_STOP.json").exists():
        raise RuntimeError("R02_PRIOR_ENGINEERING_HARD_STOP_REQUIRES_OWNER")
    lock = root / "ORCHESTRATOR_LOCK.json"
    if lock.exists():
        prior = worker.load(lock)
        if prior["host"] != platform.node() or worker.process_is_alive(prior["pid"]):
            raise RuntimeError("R02_EXISTING_LIVE_OR_FOREIGN_PROCESS")
        lock.rename(root / ("RECOVERED_DEAD_PROCESS_LOCK_" + str(time.time_ns()) + ".json"))
    worker.write_new(lock, {"pid": os.getpid(), "host": platform.node(), "utc": worker.now()})
    try:
        device = worker.device_gate()
        if device["devices"] != old["device_enumeration"]["devices"]:
            raise RuntimeError("R02_DEVICE_OR_DRIVER_DIFFERS_FROM_R01")
        env = worker.environment(root, repo)
        runtime = Path(old["runtime_python_private"])
        model = Path(old["model_path_private"])
        actual = worker.runtime_probe(runtime, env)
        if actual != old["runtime"] or actual["status"] != "CUDA_KERNEL_PASS":
            raise RuntimeError("R02_RUNTIME_DIFFERS_FROM_R01")
        official = worker.load(repo / worker.BASE / "qwen_official_manifest_v1.json")
        model_hashes = worker.verify_model(model, official)
        if model_hashes != old["model_file_sha256"]:
            raise RuntimeError("R02_MODEL_DIFFERS_FROM_R01")
        dependency = subprocess.run([str(runtime), "-m", "pip", "freeze", "--all"], env=env, capture_output=True, check=True).stdout
        if hashlib.sha256(dependency).hexdigest() != old["dependency_freeze_sha256"] or dependency != reference["DEPENDENCIES_FROZEN.txt"]:
            raise RuntimeError("R02_DEPENDENCIES_DIFFERS_FROM_R01")
        bundle = copy_frozen_inputs(parent, root, old)
        remaining = policy["new_model_dependency_budget_bytes"] - worker.size(parent)
        monitoring = {**policy, "new_model_dependency_budget_bytes": remaining}
        worker.budget(root, monitoring)
        assert_parent(parent, snapshot)
        if args.check_only:
            worker.write_new(root / ("CHECK_ONLY_" + str(time.time_ns()) + ".json"), {"utc": worker.now(), "device": device, "runtime": actual, "input_files_exact": True, "same_r01_model_dependencies": True, "no_download_install_or_parent_write": True, "parent_unchanged": True})
            print("R02_CHECK_ONLY_PASS_NO_NEW_MODEL_OR_DEPENDENCY", flush=True)
            return
        if (root / "COMPLETE.json").exists():
            complete = worker.load(root / "COMPLETE.json")
            if worker.sha(root / "L0_PREDICTIONS.jsonl") != complete["prediction_sha256"] or worker.sha(root / "L0_RETURN_NO_WEIGHTS.zip") != complete["return_archive_sha256"]:
                raise RuntimeError("R02_COMPLETED_RESULT_INTEGRITY")
            print("R02_ALREADY_COMPLETE_NO_RETRY", flush=True)
            return
        if not (root / "DEPENDENCIES_FROZEN.txt").exists():
            with (root / "DEPENDENCIES_FROZEN.txt").open("xb") as file:
                file.write(dependency)
        config = {"task": policy["task"], "utc": worker.now(), "git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip(),
                  "code_sha256": {p: worker.sha(repo / p) for p in SOURCES}, "policy": policy, "official_manifest": official,
                  "model_path_private": str(model), "model_file_sha256": model_hashes, "runtime_python_private": str(runtime), "runtime": actual,
                  "bundle_manifest_sha256": old["bundle_manifest_sha256"], "bundle_files": bundle["files"], "dependency_freeze_sha256": old["dependency_freeze_sha256"],
                  "device_enumeration": device, "parent_r01_config_sha256": worker.sha(parent / "CONFIG_LOCK.json"),
                  "additional_evaluator_vaults_private": [str(parent / "input/evaluation")],
                  "parent_r01_generation_sha256": worker.sha(parent / "ACTUAL_GENERATION_CONFIG.json"), "model_runtime_frozen_before_synthetic_and_D1": True}
        if not (root / "CONFIG_LOCK.json").exists():
            worker.write_new(root / "CONFIG_LOCK.json", config)
        else:
            previous = worker.load(root / "CONFIG_LOCK.json")
            for key in ("code_sha256", "policy", "model_file_sha256", "runtime", "bundle_manifest_sha256", "bundle_files", "dependency_freeze_sha256", "parent_r01_config_sha256", "parent_r01_generation_sha256", "additional_evaluator_vaults_private"):
                if previous[key] != config[key]:
                    raise RuntimeError("R02_FROZEN_IDENTITY_CHANGED:" + key)
        if not (root / "R02_PROTOCOL_DISCLOSURE.json").exists():
            worker.write_new(root / "R02_PROTOCOL_DISCLOSURE.json", {"run_id": policy["run_id"], "parent_run_id": policy["parent_run_id"],
                             "owner_approval": "PODR-153", "semantic_accuracy_is_diagnostic_not_execution_gate": True,
                             "R01_remains_failed_not_relabelled": True, "model_prompt_parser_inputs_parameters_unchanged": True,
                             "new_protocol_after_R01_synthetic_error_before_any_D1_prediction": True,
                             "no_verdict_repair_from_reason_and_no_synthetic_expected_change": True})
        if not (root / "PREDICTION_LOCK.json").exists():
            worker.logged([str(runtime), str(repo / "scripts/research/paper1_l0_worker.py"), "--infer-phase", "--work-dir", str(root), "--model-dir", str(model)], root, "infer-" + str(time.time_ns()), env, monitoring)
        assert_parent(parent, snapshot)
        worker.logged([str(runtime), str(repo / "scripts/research/evaluate_l0_worker.py"), "--work-dir", str(root)], root, "evaluate-" + str(time.time_ns()), env, monitoring)
        assert_parent(parent, snapshot)
        if not (root / "R01_UNCHANGED_FINAL.json").exists():
            worker.write_new(root / "R01_UNCHANGED_FINAL.json", {"utc": worker.now(), "all_parent_records_and_HARD_STOP_unchanged": True, "parent_snapshot": snapshot})
        worker.return_archive(root)
        worker.budget(root, monitoring)
        print("R02_L0_STRONG_BASELINE_D1_DEV_COMPLETE / OWNER_REVIEW_REQUIRED", flush=True)
    finally:
        lock.unlink(missing_ok=True)
        assert_parent(parent, snapshot)
