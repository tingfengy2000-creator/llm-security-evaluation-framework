"""PODR-153 gate/origin tests; no model, network, GPU or real D1 evaluation."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from llmguard.domains.retrieval.hidden_poisoning.method_engineering import l0_r02 as r02
from llmguard.domains.retrieval.hidden_poisoning.method_engineering import l0_worker as worker
from llmguard.domains.retrieval.hidden_poisoning.method_engineering.llm_verification import parse_output, sha_text, synthetic_cases

ROOT = Path(__file__).resolve().parents[2]


def recorded_cases() -> tuple[list[dict], dict]:
    gate = json.loads(r02.failure_reference(ROOT)["SYNTHETIC_GATE.json"])
    return gate["records"], gate["greedy_repeat"]


def test_r01_real_synthetic_outputs_reparse_exact_without_model() -> None:
    records, _ = recorded_cases()
    for (row, expected), actual in zip(synthetic_cases(), records, strict=True):
        assert actual["input_sha256"] == sha_text(json.dumps(row, ensure_ascii=False, sort_keys=True))
        parsed = parse_output(actual["raw_output"], row)
        for key, value in parsed.items():
            assert actual[key] == value
        assert expected == actual["expected_fictional"]


def test_r01_strict_semantics_remains_blocked() -> None:
    records, repeat = recorded_cases()
    assessment = worker.synthetic_assessment(records, repeat, worker.load(ROOT / worker.BASE / "worker_policy_v1.json"))
    assert assessment["semantic_correct"] == 4
    assert not assessment["all_pass"] and not assessment["execution_gate_passed"]
    assert assessment["engineering_all_pass"]


def test_r02_preserves_error_but_authorizes_after_engineering() -> None:
    records, repeat = recorded_cases()
    before = copy.deepcopy(records)
    assessment = worker.synthetic_assessment(records, repeat, r02.r02_policy(ROOT))
    assert assessment["semantic_correct"] == 4 and not assessment["semantic_all_pass"]
    assert not assessment["all_pass"]  # never relabel 4/5 as all-correct
    assert assessment["execution_gate_passed"] and assessment["engineering_all_pass"]
    assert assessment["nonempty_gap_on_nonabstention_diagnostic"] == 4
    assert records == before and records[2]["verdict"] == "CONTRADICT"


@pytest.mark.parametrize("defect", ["parse", "quote", "repeat", "count", "order", "empty"])
def test_r02_engineering_defects_still_stop(defect: str) -> None:
    records, repeat = recorded_cases()
    if defect == "parse":
        records[0]["error"] = "OUTPUT_SCHEMA"
    elif defect == "quote":
        records[0]["error"] = "QUOTE_NOT_IN_FROZEN_TEXT"
    elif defect == "repeat":
        repeat["raw_output"] += "changed"
    elif defect == "count":
        records.pop()
    elif defect == "order":
        records.reverse()
    elif defect == "empty":
        records[0]["raw_output"] = ""
    assert not worker.synthetic_assessment(records, repeat, r02.r02_policy(ROOT))["execution_gate_passed"]


def test_unapproved_gate_policy_cannot_relax() -> None:
    records, repeat = recorded_cases()
    with pytest.raises(RuntimeError, match="NOT_AUTHORIZED"):
        worker.synthetic_assessment(records, repeat, {"synthetic_semantic_requirement": "DIAGNOSTIC_ONLY", "run_id": "R01"})


def test_synthetic_expected_and_input_cannot_be_changed() -> None:
    records, repeat = recorded_cases()
    records[2]["expected_fictional"] = "CONTRADICT"
    assert not worker.synthetic_assessment(records, repeat, r02.r02_policy(ROOT))["execution_gate_passed"]


def test_model_verdict_cannot_be_repaired_using_reason() -> None:
    records, repeat = recorded_cases()
    records[2]["verdict"] = "SUPPORT"
    assert not worker.synthetic_assessment(records, repeat, r02.r02_policy(ROOT))["execution_gate_passed"]


def test_model_prompt_parser_evaluator_and_r01_config_exact() -> None:
    old = json.loads(r02.failure_reference(ROOT)["CONFIG_LOCK.json"])
    for path in (
        "src/llmguard/domains/retrieval/hidden_poisoning/method_engineering/llm_verification.py",
        "scripts/research/evaluate_l0_worker.py",
        "scripts/research/prepare_l0_worker_input.py",
        worker.BASE + "/worker_policy_v1.json",
        worker.BASE + "/qwen_official_manifest_v1.json",
    ):
        if path in old["code_sha256"]:
            assert worker.sha(ROOT / path) == old["code_sha256"][path]
    assert old["policy"]["seed"] == r02.r02_policy(ROOT)["seed"]


def test_fixed_policy_disallows_changed_model_parameter(tmp_path: Path) -> None:
    base = tmp_path / worker.BASE
    base.mkdir(parents=True)
    old = worker.load(ROOT / worker.BASE / "worker_policy_v1.json")
    changed = r02.r02_policy(ROOT)
    changed["seed"] += 1
    worker.write_new(base / "worker_policy_v1.json", old)
    worker.write_new(base / "worker_policy_r02_v1.json", changed)
    with pytest.raises(RuntimeError, match="MUST_NOT_CHANGE"):
        r02.r02_policy(tmp_path)


@pytest.mark.parametrize("relation", ["same", "nested", "contains"])
def test_parent_directory_cannot_be_reused_or_written(tmp_path: Path, relation: str) -> None:
    parent = (tmp_path / "R01").resolve()
    root = parent if relation == "same" else parent / "R02" if relation == "nested" else tmp_path
    with pytest.raises(RuntimeError, match="CANNOT_WRITE"):
        r02.disjoint_roots(parent, root)
    assert not parent.exists()


def test_parent_snapshot_detects_HARD_STOP_change(tmp_path: Path) -> None:
    parent = tmp_path / "R01"
    worker.write_new(parent / "HARD_STOP.json", {"immutable": "failed"})
    snapshot = r02.parent_snapshot(parent)
    r02.assert_parent(parent, snapshot)
    (parent / "HARD_STOP.json").write_text("changed", "utf-8")
    with pytest.raises(RuntimeError, match="IMMUTABILITY"):
        r02.assert_parent(parent, snapshot)


def test_exact_input_byte_copy_no_label_parse(tmp_path: Path) -> None:
    parent, root = tmp_path / "R01", tmp_path / "R02"
    content = b'{"synthetic": "NOT_REAL_D1"}\n'
    source = parent / "input/runtime/f5.jsonl"
    source.parent.mkdir(parents=True)
    source.write_bytes(content)
    files = [{"path": "runtime/f5.jsonl", "sha256": hashlib.sha256(content).hexdigest()}]
    worker.write_new(parent / "input/BUNDLE_MANIFEST.json", {"groups": 40, "candidates": 120, "families": 13, "files": files})
    old = {"bundle_manifest_sha256": worker.sha(parent / "input/BUNDLE_MANIFEST.json"), "bundle_files": files}
    r02.copy_frozen_inputs(parent, root, old)
    assert (root / "input/runtime/f5.jsonl").read_bytes() == content
    assert source.read_bytes() == content
    (root / "input/runtime/f5.jsonl").write_bytes(b"bad")
    with pytest.raises(RuntimeError, match="EXISTING_INPUT"):
        r02.copy_frozen_inputs(parent, root, old)


def test_r02_module_has_no_install_download_or_parser_override() -> None:
    text = (ROOT / "src/llmguard/domains/retrieval/hidden_poisoning/method_engineering/l0_r02.py").read_text("utf-8")
    assert "worker.setup_runtime(" not in text and "worker.download_model(" not in text
    assert '"pip", "install"' not in text and '"pip", "download"' not in text
    assert "parse_output(" not in text and "model.generate(" not in text


def test_fictional_r02_check_execute_and_idempotence_preserve_parent(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    parent, root = (tmp_path / "R01").resolve(), (tmp_path / "R02").resolve()
    parent.mkdir()
    runtime, model = parent / "env/python", parent / "model/exact"
    runtime.parent.mkdir()
    runtime.write_bytes(b"NOT_EXECUTABLE_FICTIONAL_TEST")
    model.mkdir(parents=True)
    dependency = b"FICTIONAL_NOT_ACTUAL_ENV\n"
    worker.write_new(parent / "input/BUNDLE_MANIFEST.json", {"groups": 40, "candidates": 120, "families": 13, "files": []})
    old = {"git_head": r02.R01_SOURCE, "policy": worker.load(ROOT / worker.BASE / "worker_policy_v1.json"),
           "device_enumeration": {"devices": [{"fixture_no_device": True}]},
           "runtime_python_private": str(runtime), "model_path_private": str(model),
           "runtime": {"status": "CUDA_KERNEL_PASS", "fixture_only": True}, "model_file_sha256": {"test": "NOT_MODEL"},
           "bundle_manifest_sha256": worker.sha(parent / "input/BUNDLE_MANIFEST.json"), "bundle_files": [],
           "dependency_freeze_sha256": hashlib.sha256(dependency).hexdigest()}
    worker.write_new(parent / "CONFIG_LOCK.json", old)
    worker.write_new(parent / "ACTUAL_GENERATION_CONFIG.json", {"fictional": True})
    worker.write_new(parent / "HARD_STOP.json", {"original_failure": True})
    with (parent / "DEPENDENCIES_FROZEN.txt").open("xb") as file:
        file.write(dependency)
    reference = {p.name: p.read_bytes() for p in parent.iterdir() if p.is_file()}
    monkeypatch.setattr(r02, "failure_reference", lambda repo: reference)
    monkeypatch.setattr(worker, "device_gate", lambda: old["device_enumeration"])
    monkeypatch.setattr(worker, "runtime_probe", lambda *args: old["runtime"])
    monkeypatch.setattr(worker, "verify_model", lambda *args: old["model_file_sha256"])
    real_run = r02.subprocess.run

    def frozen_dependency_only(command: list[str], *args: Any, **kwargs: Any) -> Any:
        if command[1:] == ["-m", "pip", "freeze", "--all"]:
            return SimpleNamespace(stdout=dependency)
        return real_run(command, *args, **kwargs)

    monkeypatch.setattr(r02.subprocess, "run", frozen_dependency_only)
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
    before = r02.parent_snapshot(parent)
    (root / "cache/pycache").mkdir(parents=True)  # allowed startup redirection only
    args = SimpleNamespace(r01_dir=parent, work_dir=root, check_only=True)
    r02.orchestrate_r02(args, ROOT)
    assert not calls and r02.parent_snapshot(parent) == before
    args.check_only = False
    r02.orchestrate_r02(args, ROOT)
    assert calls == ["infer", "evaluate"] and (root / "COMPLETE.json").exists()
    assert r02.parent_snapshot(parent) == before
    r02.orchestrate_r02(args, ROOT)
    assert calls == ["infer", "evaluate"] and r02.parent_snapshot(parent) == before
