"""R02 approved continuation: new directory, read-only reuse of frozen R01."""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "src"), str(ROOT)]

from llmguard.domains.retrieval.hidden_poisoning.method_engineering.l0_r02 import disjoint_roots, orchestrate_r02  # noqa: E402
from llmguard.domains.retrieval.hidden_poisoning.method_engineering.l0_worker import write_new  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--r01-dir", type=Path, required=True)
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    disjoint_roots(args.r01_dir.resolve(), args.work_dir.resolve())
    try:
        orchestrate_r02(args, ROOT)
    except BaseException as exc:
        root = args.work_dir.resolve()
        if (root / "R02_ORIGIN.json").exists() and "R02_EXISTING_LIVE_OR_FOREIGN_PROCESS" not in str(exc):
            hard = not isinstance(exc, (KeyboardInterrupt, SystemExit))
            record = {"error": repr(exc), "hard_gate": hard, "status": "R02_STOP_RETURN_TO_CONTROL_PLANE", "R01_HARD_STOP_NOT_REMOVED": True}
            write_new(root / ("INCIDENT_" + str(time.time_ns()) + ".json"), record)
            if hard and not (root / "HARD_STOP.json").exists():
                write_new(root / "HARD_STOP.json", record)
        raise


if __name__ == "__main__":
    main()
