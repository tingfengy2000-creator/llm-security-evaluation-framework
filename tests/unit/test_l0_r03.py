"""R03 length-cap tests. No model, network, GPU, or real D1 evaluation."""
from __future__ import annotations

import copy
import hashlib
import os
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from llmguard.domains.retrieval.hidden_poisoning.method_engineering import l0_r02 as r02
from llmguard.domains.retrieval.hidden_poisoning.method_engineering import l0_r03 as r03
from llmguard.domains.retrieval.hidden_poisoning.method_engineering import l0_worker as worker

ROOT = Path(__file__).resolve().parents[2]


def test_r03_changes_only_the_input_cap() -> None:
    policy = r03.r03_policy(ROOT)
    old = r02.r02_policy(ROOT)
    assert policy["max_input_tokens"] == 7200
    assert old["max_input_tokens"] == 31744
    assert policy["overflow_policy"] == "INPUT_FAILURE_AS_INSUFFICIENT_FULL_DENOMINATOR_NO_TRUNCATION"
    assert policy["dtype"] == "bfloat16" and policy["attention"] == "sdpa"
    assert policy["no_quantization_cpu_offload_or_alternative_model"] is True
    kept = {k: v for k, v in policy.items() if k not in r03.DELTA}
    assert kept == {k: v for k, v in old.items() if k not in r03.DELTA}


def test_r03_diagnostic_keeps_the_known_semantic_miss() -> None:
    records, repeat = json_cases()
    before = copy.deepcopy(records)
    assessment = worker.synthetic_assessment(records, repeat, r03.r03_policy(ROOT))
    assert assessment["semantic_correct"] == 4 and not assessment["semantic_all_pass"]
    assert not assessment["all_pass"] and assessment["execution_gate_passed"] and assessment["engineering_all_pass"]
    assert records == before and records[2]["verdict"] == "CONTRADICT"


def test_r03_rejects_a_raised_cap_or_other_parameter(tmp_path: Path) -> None:
    base = tmp_path / worker.BASE
    base.mkdir(parents=True)
    loosened = r03.r03_policy(ROOT)
    loosened["max_input_tokens"] = 8000
    worker.write_new(base / "worker_policy_v1.json", worker.load(ROOT / worker.BASE / "worker_policy_v1.json"))
    worker.write_new(base / "worker_policy_r02_v1.json", r02.r02_policy(ROOT))
    worker.write_new(base / "worker_policy_r03_v1.json", loosened)
    with pytest.raises(RuntimeError, match="R03_POLICY_IDENTITY"):
        r03.r03_policy(tmp_path)


def test_unapproved_diagnostic_still_refuses() -> None:
    records, repeat = json_cases()
    with pytest.raises(RuntimeError, match="NOT_AUTHORIZED"):
        worker.synthetic_assessment(records, repeat, {"synthetic_semantic_requirement": "DIAGNOSTIC_ONLY", "run_id": "VACE-L0-D1-20261029-R03", "owner_approval": "PODR-153", "max_input_tokens": 7200, "overflow_policy": "INPUT_FAILURE_AS_INSUFFICIENT_FULL_DENOMINATOR_NO_TRUNCATION"})


def test_payload_drive_and_prior_directories(tmp_path: Path) -> None:
    if os.name == "nt":
        with pytest.raises(RuntimeError, match="D_OR_E"):
            r03.assert_payload_drive(Path(r"C:\not-a-payload"))
    parent, root = (tmp_path / "R01").resolve(), (tmp_path / "R01" / "R03").resolve()
    with pytest.raises(RuntimeError, match="CANNOT_WRITE"):
        r03.disjoint_prior(parent, root)


def test_r03_module_has_no_install_download_or_generate() -> None:
    text = (ROOT / "src/llmguard/domains/retrieval/hidden_poisoning/method_engineering/l0_r03.py").read_text("utf-8")
    assert "worker.setup_runtime(" not in text and "worker.download_model(" not in text
    assert '"pip", "install"' not in text and "model.generate(" not in text
    assert "INPUT_TOO_LONG_NO_SILENT_TRUNCATION" in text


def json_cases() -> tuple[list[dict], dict]:
    import json
    gate = json.loads(r02.failure_reference(ROOT)["SYNTHETIC_GATE.json"])
    return gate["records"], gate["greedy_repeat"]


def test_fictional_r03_preserves_both_priors(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(r03, "assert_payload_drive", lambda root: None)
    r01, failed, root = (tmp_path / "R01").resolve(), (tmp_path / "R02").resolve(), (tmp_path / "R03").resolve()
    r01.mkdir()
    runtime, model = r01 / "env/python", r01 / "model/exact"
    runtime.parent.mkdir()
    runtime.write_bytes(b"NOT_EXECUTABLE_FICTIONAL_TEST")
    model.mkdir(parents=True)
    dependency = b"FICTIONAL_NOT_ACTUAL_ENV\n"
    worker.write_new(r01 / "input/BUNDLE_MANIFEST.json", {"groups": 40, "candidates": 120, "families": 13, "files": []})
    old = {"git_head": r02.R01_SOURCE, "policy": worker.load(ROOT / worker.BASE / "worker_policy_v1.json"),
           "device_enumeration": {"devices": [{"fixture_no_device": True}]},
           "runtime_python_private": str(runtime), "model_path_private": str(model),
           "runtime": {"status": "CUDA_KERNEL_PASS", "fixture_only": True}, "model_file_sha256": {"test": "NOT_MODEL"},
           "bundle_manifest_sha256": worker.sha(r01 / "input/BUNDLE_MANIFEST.json"), "bundle_files": [],
           "dependency_freeze_sha256": hashlib.sha256(dependency).hexdigest()}
    worker.write_new(r01 / "CONFIG_LOCK.json", old)
    worker.write_new(r01 / "ACTUAL_GENERATION_CONFIG.json", {"fictional": True})
    worker.write_new(r01 / "HARD_STOP.json", {"original_failure": True})
    with (r01 / "DEPENDENCIES_FROZEN.txt").open("xb") as file:
        file.write(dependency)
    reference = {p.name: p.read_bytes() for p in r01.iterdir() if p.is_file()}
    monkeypatch.setattr(r02, "failure_reference", lambda repo: reference)
    failed.mkdir()
    r02_policy = r02.r02_policy(ROOT)
    r02_config = {"git_head": r03.R02_SOURCE, "policy": r02_policy, "model_path_private": str(model), "runtime_python_private": str(runtime)}
    worker.write_new(failed / "CONFIG_LOCK.json", r02_config)
    worker.write_new(failed / "HARD_STOP.json", {"oom": True})
    worker.write_new(failed / "SYNTHETIC_GATE.json", {"diagnostic": True})
    for name in r03.R02_RAW:
        worker.write_new(failed / "raw" / name, {"fixture_raw": name})
    monkeypatch.setattr(r03, "R02_HARD_STOP_SHA", worker.sha(failed / "HARD_STOP.json"))
    monkeypatch.setattr(r03, "R02_SYNTHETIC_GATE_SHA", worker.sha(failed / "SYNTHETIC_GATE.json"))
    monkeypatch.setattr(r03, "R02_CONFIG_LOCK_SHA", worker.sha(failed / "CONFIG_LOCK.json"))
    monkeypatch.setattr(worker, "device_gate", lambda: old["device_enumeration"])
    monkeypatch.setattr(worker, "runtime_probe", lambda *args: old["runtime"])
    monkeypatch.setattr(worker, "verify_model", lambda *args: old["model_file_sha256"])
    real_run = subprocess_run()

    def frozen_dependency_only(command: list[str], *args: Any, **kwargs: Any) -> Any:
        if command[1:] == ["-m", "pip", "freeze", "--all"]:
            return SimpleNamespace(stdout=dependency)
        return real_run(command, *args, **kwargs)

    monkeypatch.setattr(r03.subprocess, "run", frozen_dependency_only)
    calls = []

    def fictional_logged(command: list[str], output: Path, name: str, *args: object) -> None:
        calls.append(name.split("-")[0])
        if name.startswith("infer-"):
            worker.write_new(output / "SYNTHETIC_GATE.json", {"fixture_only": True})
            (output / "L0_PREDICTIONS.jsonl").write_bytes(b"FICTIONAL_NOT_D1_OR_LLM_PREDICTIONS\n")
            worker.write_new(output / "PREDICTION_LOCK.json", {"fixture_only": True})
        else:
            worker.write_new(output / "L0_RUN_MANIFEST.json", {"fixture_only": True})

    monkeypatch.setattr(worker, "logged", fictional_logged)
    before_r01, before_r02 = r02.parent_snapshot(r01), r02.parent_snapshot(failed)
    args = SimpleNamespace(r01_dir=r01, r02_dir=failed, work_dir=root, check_only=True)
    r03.orchestrate_r03(args, ROOT)
    assert not calls and r02.parent_snapshot(r01) == before_r01 and r02.parent_snapshot(failed) == before_r02
    args.check_only = False
    r03.orchestrate_r03(args, ROOT)
    assert calls == ["infer", "evaluate"] and (root / "COMPLETE.json").exists()
    assert (root / "CONFIG_LOCK.json").exists() and (root / "R03_PROTOCOL_DISCLOSURE.json").exists()
    assert worker.load(root / "CONFIG_LOCK.json")["policy"]["max_input_tokens"] == 7200
    assert r02.parent_snapshot(r01) == before_r01 and r02.parent_snapshot(failed) == before_r02


def subprocess_run():
    return r03.subprocess.run
