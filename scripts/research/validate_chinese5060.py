"""Capture exact local validation commands, outputs and exits in a NEW private run."""
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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--selection", type=Path, required=True)
    args = parser.parse_args()
    if re.fullmatch(r"W1-5060-[A-Z0-9-]+", args.run_id) is None:
        raise ValueError("INVALID_RUN_ID")
    root = Path("experiments/paper1_chinese5060") / args.run_id
    root.mkdir(parents=True, exist_ok=False)
    env = dict(os.environ, PYTHONPATH=str(Path("src").resolve()), HF_HUB_OFFLINE="1",
               TRANSFORMERS_OFFLINE="1", ANONYMIZED_TELEMETRY="False", PYTHONDONTWRITEBYTECODE="1")
    package = "src/llmguard/domains/retrieval/hidden_poisoning/chinese5060"
    scripts = ["scripts/research/audit_chinese5060_inputs.py", "scripts/research/smoke_chinese5060.py",
               "scripts/research/validate_chinese5060.py"]
    jobs = [
        ("tests", ["-m", "pytest", "-q", "tests/research/test_chinese5060.py"]),
        ("ruff", ["-m", "ruff", "check", package, *scripts, "tests/research/test_chinese5060.py"]),
        ("mypy", ["-m", "mypy", "--follow-imports=silent", package, *scripts]),
        ("D1_identity_audit", [scripts[0], "--bundle", str(args.bundle), "--selection", str(args.selection),
                               "--output", str(root / "D1_IDENTITY_AUDIT.json")]),
        ("fictional_chroma_smoke", [scripts[1], "--output-dir", str(root / "FICTIONAL_SMOKE")]),
    ]
    records: list[dict[str, Any]] = []
    for name, arguments in jobs:
        started = datetime.now(timezone.utc).isoformat()
        command = [sys.executable, *arguments]
        result = subprocess.run(command, env=env, capture_output=True, check=False)
        (root / f"{name}.stdout").write_bytes(result.stdout)
        (root / f"{name}.stderr").write_bytes(result.stderr)
        record = {"name": name, "argv": command, "cwd": str(Path.cwd()), "started_utc": started,
                  "ended_utc": datetime.now(timezone.utc).isoformat(), "exit_code": result.returncode}
        records.append(record)
        with (root / "COMMANDS_PRIVATE.json").open("w", encoding="utf-8") as stream:
            json.dump(records, stream, ensure_ascii=False, indent=2)
        print(json.dumps({"check": name, "exit_code": result.returncode}), flush=True)
        if result.returncode:
            break
    index = [{"path": path.relative_to(root).as_posix(), "bytes": path.stat().st_size,
              "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
             for path in sorted(root.rglob("*")) if path.is_file()]
    source_paths = [*Path(package).glob("*.py"), *(Path(s) for s in scripts), Path("tests/research/test_chinese5060.py")]
    summary = {"run_id": args.run_id, "classification": "ENGINEERING_VALIDATION_NOT_RESEARCH_EFFECT",
               "source_sha": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
               "source_file_hashes": {p.as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in source_paths},
               "checks": [{"name": r["name"], "exit_code": r["exit_code"]} for r in records],
               "status": "PASS" if len(records) == len(jobs) and all(r["exit_code"] == 0 for r in records) else "FAIL",
               "paid_calls": 0, "public_index_of_private_evidence": index}
    with (root / "VALIDATION_INDEX.json").open("x", encoding="utf-8") as stream:
        json.dump(summary, stream, ensure_ascii=False, indent=2)
    print(json.dumps({"run_id": args.run_id, "status": summary["status"]}), flush=True)
    sys.exit(0 if summary["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
