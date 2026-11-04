"""Capture P1 zero-paid preparation tests, static checks, D1 audit and git-show."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REMOTE_SHA = "aa85841ff83be31c86e0fa305d3a84d70f2158b5"
REMOTE_DOCS = ("handoff.json", "upstream_pin.md", "implementation_difference_audit.md",
               "environment_manifest.md", "failure_log.md", "run_manifest.json", "claim1_run_report.md")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()
    if not re.fullmatch(r"W1-5060-P1-[A-Z0-9-]+", args.run_id):
        raise ValueError("INVALID_RUN_ID")
    output = Path("experiments/paper1_chinese5060") / args.run_id
    output.mkdir(parents=True, exist_ok=False)
    env = dict(os.environ, PYTHONPATH=str(Path("src").resolve()), PYTHONIOENCODING="utf-8",
               HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1", PYTHONDONTWRITEBYTECODE="1")
    package = "src/llmguard/domains/retrieval/hidden_poisoning/chinese5060"
    scripts = ["scripts/research/prepare_chinese5060_p1.py", "scripts/research/validate_chinese5060_p1.py"]
    tests = ["tests/research/test_chinese5060.py", "tests/research/test_chinese5060_p1_access.py",
             "tests/research/test_chinese5060_p1_preparation.py"]
    design_run = args.run_id + "-DESIGN"
    jobs = [
        ("tests", [sys.executable, "-m", "pytest", "-q", "--tb=short", f"--basetemp={output / 'temp_fixtures'}", *tests]),
        ("ruff", [sys.executable, "-m", "ruff", "check", package, *scripts, *tests]),
        ("mypy", [sys.executable, "-m", "mypy", "--follow-imports=silent", package, *scripts]),
        ("D1_preparation", [sys.executable, scripts[0], "--workspace", str(args.workspace), "--run-id", design_run]),
    ]
    jobs.extend(("5090_" + name.replace(".", "_"), ["git", "show", f"{REMOTE_SHA}:docs/paper1/dual_machine/repro5090/{name}"]) for name in REMOTE_DOCS)
    records: list[dict[str, Any]] = []
    for name, command in jobs:
        started = datetime.now(timezone.utc).isoformat()
        result = subprocess.run(command, env=env, capture_output=True, check=False)
        (output / (name + ".stdout")).write_bytes(result.stdout)
        (output / (name + ".stderr")).write_bytes(result.stderr)
        records.append({"name": name, "argv": command, "cwd": str(Path.cwd()), "started_utc": started,
                        "ended_utc": datetime.now(timezone.utc).isoformat(), "exit_code": result.returncode})
        (output / "COMMANDS_PRIVATE.json").write_bytes((json.dumps(records, ensure_ascii=False, indent=2) + "\n").encode())
        print(json.dumps({"check": name, "exit_code": result.returncode}), flush=True)
        if result.returncode:
            break
    paths = [*Path(package).glob("*.py"), *(Path(s) for s in scripts), *(Path(t) for t in tests),
             Path("docs/paper1/dual_machine/chinese5060/p1/P1_PROTOCOL_CANDIDATE.json")]
    summary = {"run_id": args.run_id, "design_run_id": design_run,
               "source_sha": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
               "source_file_hashes": {p.as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
               "handoff_commit": REMOTE_SHA, "handoff_docs": list(REMOTE_DOCS),
               "checks": [{"name": r["name"], "exit_code": r["exit_code"]} for r in records],
               "status": "PASS" if len(records) == len(jobs) and all(r["exit_code"] == 0 for r in records) else "FAIL",
               "paid_calls": 0, "cost_CNY": "0", "claim_runs": 0, "retrieval_or_generation_runs": 0}
    (output / "VALIDATION_PUBLIC.json").write_bytes((json.dumps(summary, ensure_ascii=False, indent=2) + "\n").encode())
    print(json.dumps({"run_id": args.run_id, "status": summary["status"]}), flush=True)
    sys.exit(0 if summary["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
