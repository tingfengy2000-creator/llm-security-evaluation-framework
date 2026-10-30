"""CPU checks for the full D1 entry. No model load and no private text."""
from __future__ import annotations

import os
from pathlib import Path

import pytest

from llmguard.domains.retrieval.hidden_poisoning.method_engineering import l0_full01, l0_worker as worker

ROOT = Path(__file__).resolve().parents[2]


def test_policy_keeps_the_baseline_generation_contract() -> None:
    policy = l0_full01.full01_policy(ROOT)
    assert policy["max_input_tokens"] == 31744
    assert policy["min_new_tokens"] is None
    assert policy["adapter_module_sha256"] == l0_full01.ADAPTER_SHA
    assert policy["attention_adapter"] == "explicit_gqa_efficient_r06"
    text = (ROOT / l0_full01.ADAPTER).read_text(encoding="utf-8")
    assert "SDPBackend.EFFICIENT_ATTENTION" in text
    assert "repeat_kv_contiguous" in text


def test_unapproved_cap_cannot_use_the_full01_diagnostic_gate() -> None:
    with pytest.raises(RuntimeError, match="FULL01_IDENTITY"):
        worker.synthetic_assessment([], {}, {"synthetic_semantic_requirement": "DIAGNOSTIC_ONLY", "run_id": "VACE-L0-D1-20261030-FULL01", "owner_approval": "P1-L0-D1-FULL-EXECUTION-01", "max_input_tokens": 7200, "attention_adapter": "explicit_gqa_efficient_r06", "overflow_policy": "INPUT_FAILURE_AS_INSUFFICIENT_FULL_DENOMINATOR_NO_TRUNCATION"})


def test_adapter_evidence_rejects_a_math_backend_and_accepts_efficient() -> None:
    before = {"signatures": []}
    good = {"signatures": [{"query_len": 8, "key_len": 8, "kv_heads": 4, "expanded_heads": 28, "enable_gqa": False, "backend": "EFFICIENT_ATTENTION", "count": 28}, {"query_len": 1, "key_len": 9, "kv_heads": 4, "expanded_heads": 28, "enable_gqa": False, "backend": "EFFICIENT_ATTENTION", "count": 28}]}
    evidence = worker.adapter_evidence(before, good)
    assert evidence["efficient_only"] is True and evidence["prefill_and_decode"] is True
    bad = {"signatures": [{"query_len": 8, "key_len": 8, "kv_heads": 4, "expanded_heads": 4, "enable_gqa": True, "backend": "MATH", "count": 1}, {"query_len": 1, "key_len": 9, "kv_heads": 4, "expanded_heads": 4, "enable_gqa": True, "backend": "MATH", "count": 1}]}
    refused = worker.adapter_evidence(before, bad)
    assert refused["efficient_only"] is False


def test_inference_cannot_open_the_evaluation_vault(tmp_path: Path) -> None:
    vault = tmp_path / "evaluation"
    runtime = tmp_path / "runtime" / "f5.jsonl"
    vault.mkdir()
    assert worker.evaluation_vault_forbidden(vault / "labels.jsonl", [vault.resolve()])
    assert worker.evaluation_vault_forbidden(runtime, [vault.resolve()]) is False


def test_resume_rejects_a_changed_input_or_config() -> None:
    assert worker.resume_identity_matches({"input_sha256": "a", "config_lock_sha256": "b"}, "a", "b")
    assert worker.resume_identity_matches({"input_sha256": "a", "config_lock_sha256": "b"}, "changed", "b") is False


def test_incomplete_seal_is_not_a_finished_run() -> None:
    with pytest.raises(RuntimeError, match="INCOMPLETE"):
        l0_full01.require_prediction_seal({"rows": 239, "raw": {}})


def test_worker_installs_the_adapter_only_behind_the_full01_flag() -> None:
    text = (ROOT / "src/llmguard/domains/retrieval/hidden_poisoning/method_engineering/l0_worker.py").read_text(encoding="utf-8")
    assert 'policy.get("attention_adapter") == "explicit_gqa_efficient_r06"' in text
    assert "install(model)" in text
    assert "empty_cache" not in text


def test_run_directories_do_not_hide_the_parent_module() -> None:
    text = Path(l0_full01.__file__).read_text(encoding="utf-8")
    assert "r02_dir = args.r02_dir.resolve()" in text
    assert "r02.parent_identity" in text
    assert "r02.copy_frozen_inputs" in text
    assert "r02.assert_parent" in text


def test_prior_directories_stay_disjoint(tmp_path: Path) -> None:
    if os.name == "nt":
        with pytest.raises(RuntimeError, match="D_OR_E"):
            l0_full01.disjoint(Path(r"C:\not-a-payload"), [])
    parent = (tmp_path / "R01").resolve()
    child = (parent / "FULL01").resolve()
    with pytest.raises(RuntimeError, match="PRIOR_RUN"):
        l0_full01.disjoint(child, [parent])
