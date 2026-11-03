"""PODR-157 continuation; exact immutable prefix and paid-response reuse."""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from llmguard.domains.retrieval.hidden_poisoning.feasibility_sprint.api import OWNER_A, PaidClient, gate_issues, request_body, write_new  # noqa: E402
from llmguard.domains.retrieval.hidden_poisoning.feasibility_sprint.continuation import ReplayClient, continue_predictions, pending_cache, sha, verify_parent  # noqa: E402
from llmguard.domains.retrieval.hidden_poisoning.feasibility_sprint.contracts import F5_SHA, digest, loads, validate_runtime  # noqa: E402
from llmguard.domains.retrieval.hidden_poisoning.feasibility_sprint.prompts import messages, prompt_contract  # noqa: E402
from llmguard.domains.retrieval.hidden_poisoning.feasibility_sprint.runtime import Engine  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--runtime-f5", type=Path, required=True)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    task = ROOT / "experiments/paper1_feasibility_sprint_01"
    parent = task / "D1-DEV-BEIJING01"
    run = task / "D1-DEV-BEIJING-CONT-A01"
    config = loads(args.config.read_text("utf-8"))
    if config.get("owner_continuation_approval") != OWNER_A or config.get("length_policy") != "INSUFFICIENT_NO_RETRY_OWNER_A":
        raise RuntimeError("OWNER_A_APPROVAL_REQUIRED")
    issues = gate_issues(config)
    if issues:
        raise RuntimeError("CONTINUATION_PREFLIGHT:" + ",".join(issues))
    provenance = verify_parent(task, ROOT)
    old = provenance["parent_config"]["config"]
    changed = {k for k in set(old) | set(config) if old.get(k) != config.get(k)}
    if changed - {"owner_continuation_approval", "length_policy", "budget_total_usd", "budget_warning_usd", "budget_hard_stop_usd"}:
        raise RuntimeError("API_CONFIG_CHANGED_BEYOND_OWNER_A")
    if sha(task / "SYNTHETIC_PROBE_PASS.json") != config["synthetic_probe_receipt_sha256"]:
        raise RuntimeError("PROBE_IDENTITY_CHANGED")
    if sha(args.runtime_f5) != F5_SHA:
        raise RuntimeError("FROZEN_F5_CHANGED")
    rows = [loads(line) for line in args.runtime_f5.read_text("utf-8").splitlines() if line.strip()]
    if len(rows) != 120:
        raise RuntimeError("NOT_SIGNED_120")
    for row in rows:
        validate_runtime(row)
    partial = rows[52]
    bodies = {digest(request_body(messages(partial, kind), cap)): request_body(messages(partial, kind), cap)
              for kind, cap in (("internal", 2048), ("direct", 1024))}
    cached = pending_cache(task, bodies)
    if args.check_only:
        print({"status": "CONT_A_CHECK_PASS_NO_REQUEST", "prefix": 52, "cached_partial_calls": len(cached), "labels_opened": False})
        return
    if subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT).strip():
        raise RuntimeError("FROZEN_COMMIT_MUST_BE_CLEAN")
    if run.exists():
        raise RuntimeError("CONTINUATION_NAMESPACE_ALREADY_EXISTS")
    run.mkdir()
    fd = os.open(task / "CONTINUATION_IN_FLIGHT.lock", os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    try:
        source_paths = list((ROOT / "src/llmguard/domains/retrieval/hidden_poisoning/feasibility_sprint").glob("*.py"))
        source_paths += [Path(__file__).resolve(), ROOT / "scripts/research/evaluate_paper1_feasibility.py", ROOT / "src/llmguard/domains/retrieval/hidden_poisoning/method_engineering/llm_verification.py"]
        doc_dir = ROOT / "docs/research/stage6_1_hidden_knowledge_poisoning/core144/feasibility_sprint_01"
        source_paths += [doc_dir / p for p in ("FEASIBILITY_PROTOCOL_V1.md", "S1_INTERNAL_CONTRADICTION_SPEC_V1.md", "CLAIM_RELATION_VERIFICATION_SPEC_V1.md", "BEIJING_EXECUTION_ADDENDUM_V2.md", "CONTINUATION_A_PROTOCOL_V3.md")]
        frozen = {"git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
                  "config": config, "prompts": prompt_contract(), "input_sha256": F5_SHA,
                  "parent_provenance": provenance, "e4": True,
                  "source_hashes": {p.relative_to(ROOT).as_posix(): sha(p) for p in source_paths}}
        write_new(run / "CONFIG_LOCK.json", frozen)
        client = ReplayClient(PaidClient(task, config), cached)
        continue_predictions(Engine(client), rows, parent, run, digest(frozen))
        if client.used != set(cached):
            raise RuntimeError("EXPECTED_PARENT_CALLS_NOT_REUSED")
        verify_parent(task, ROOT)
        write_new(run / "EXECUTION_COMPLETE.json", {"status": "D1_DEV_PREDICTIONS_SEALED_NOT_SCORED", "copied_prefix": 52, "reused_partial_calls": 2, "owner_approval": OWNER_A})
    finally:
        os.close(fd)
        (task / "CONTINUATION_IN_FLIGHT.lock").unlink()


if __name__ == "__main__":
    main()
