"""Preflight, synthetic probe and bounded D1 execution. No evaluator entry."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "src")]

from llmguard.domains.retrieval.hidden_poisoning.feasibility_sprint.api import MODEL, PaidClient, gate_issues, write_new  # noqa: E402
from llmguard.domains.retrieval.hidden_poisoning.feasibility_sprint.contracts import F5_SHA, digest, loads, validate_runtime  # noqa: E402
from llmguard.domains.retrieval.hidden_poisoning.feasibility_sprint.prompts import prompt_contract  # noqa: E402
from llmguard.domains.retrieval.hidden_poisoning.feasibility_sprint.runtime import Engine, predict_all  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=["preflight", "probe", "run"])
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--runtime-f5", type=Path)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--e4", action="store_true")
    args = parser.parse_args()
    config = loads(args.config.read_text("utf-8"))
    issues = gate_issues(config, probe=args.phase == "probe")
    if args.phase == "preflight":
        print(json.dumps({"status": "PAID_EXPERIMENT_BLOCKED" if issues else "PREFLIGHT_CONFIG_READY", "issues": issues,
                          "no_requests_sent": True, "model": MODEL}, ensure_ascii=False))
        return 2 if issues else 0
    if issues:
        print(json.dumps({"status": "PAID_EXPERIMENT_BLOCKED", "issues": issues, "no_requests_sent": True}))
        return 2
    run = args.run_dir.resolve()
    task_root = ROOT / "experiments/paper1_feasibility_sprint_01"
    if not run.is_relative_to(task_root.resolve()):
        raise RuntimeError("PRIVATE_RUN_MUST_STAY_IN_TASK_BUDGET_ROOT")
    if subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT).strip():
        raise RuntimeError("COMMIT_FROZEN_SOURCE_BEFORE_PAID_EXECUTION")
    run.mkdir(parents=True, exist_ok=True)
    client = PaidClient(task_root, config)
    probe_path = task_root / "SYNTHETIC_PROBE_PASS.json"
    if args.phase == "probe":
        if probe_path.exists():
            raise RuntimeError("PROBE_ALREADY_PASSED_NO_REPEAT")
        result = client.call([{"role": "system", "content": '仅输出JSON对象{"ok":true}。'}, {"role": "user", "content": "这是纯虚构的接口探测，不含研究数据。"}], "probe", 64, probe=True)
        if loads(result["content"]) != {"ok": True}:
            raise RuntimeError("SYNTHETIC_PROBE_FAILED_NO_RETRY")
        write_new(probe_path, {"config_sha256": digest(config), "result": result})
        return 0
    probe = probe_path
    if not probe.exists() or hashlib.sha256(probe.read_bytes()).hexdigest() != config["synthetic_probe_receipt_sha256"]:
        raise RuntimeError("SYNTHETIC_PROBE_RECEIPT_IDENTITY")
    tested = loads(probe.read_text("utf-8"))["config_sha256"]
    before = {**config, "synthetic_probe_receipt_sha256": None}
    if digest(before) != tested:
        raise RuntimeError("API_CONFIG_CHANGED_AFTER_PROBE")
    if args.runtime_f5 is None:
        raise RuntimeError("RUNTIME_F5_REQUIRED")
    data = args.runtime_f5.read_bytes()
    if hashlib.sha256(data).hexdigest() != F5_SHA:
        raise RuntimeError("FROZEN_D1_F5_IDENTITY")
    rows = [loads(line) for line in data.decode("utf-8").splitlines() if line.strip()]
    if len(rows) != 120:
        raise RuntimeError("SIGNED_COHORT_NOT_120")
    for row in rows:
        validate_runtime(row)
    lock = run / "RUN_IN_FLIGHT.lock"
    fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    try:
        source_paths = sorted((ROOT / "src/llmguard/domains/retrieval/hidden_poisoning/feasibility_sprint").glob("*.py")) + [Path(__file__).resolve()]
        source_paths += [ROOT / "src/llmguard/domains/retrieval/hidden_poisoning/method_engineering/llm_verification.py",
                         ROOT / "scripts/research/evaluate_paper1_feasibility.py"]
        doc_dir = ROOT / "docs/research/stage6_1_hidden_knowledge_poisoning/core144/feasibility_sprint_01"
        source_paths += [doc_dir / name for name in ("FEASIBILITY_PROTOCOL_V1.md", "S1_INTERNAL_CONTRADICTION_SPEC_V1.md", "CLAIM_RELATION_VERIFICATION_SPEC_V1.md", "BEIJING_EXECUTION_ADDENDUM_V2.md")]
        frozen = {"git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
                  "config": config, "prompts": prompt_contract(), "input_sha256": F5_SHA, "e4": args.e4,
                  "source_hashes": {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in source_paths}}
        write_new(run / "CONFIG_LOCK.json", frozen)
        predict_all(Engine(client), rows, run, digest(frozen), e4=args.e4)
        settled, pending = client.totals()
        write_new(run / "EXECUTION_COMPLETE.json", {"status": "D1_DEV_PREDICTIONS_SEALED_NOT_SCORED", "estimated_actual_usd": str(settled), "pending_usd": str(pending)})
    finally:
        os.close(fd)
        lock.unlink()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
