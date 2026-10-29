"""R03 length-capped continuation: new directory, read-only reuse of frozen R01."""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "src"), str(ROOT)]

from llmguard.domains.retrieval.hidden_poisoning.method_engineering.l0_r03 import disjoint_prior, orchestrate_r03  # noqa: E402
from llmguard.domains.retrieval.hidden_poisoning.method_engineering.l0_worker import write_new  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--r01-dir", type=Path, required=True)
    parser.add_argument("--r02-dir", type=Path, required=True)
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    r01, r02_dir, root = args.r01_dir.resolve(), args.r02_dir.resolve(), args.work_dir.resolve()
    disjoint_prior(r01, root)
    disjoint_prior(r02_dir, root)
    try:
        orchestrate_r03(args, ROOT)
    except BaseException as exc:
        if (root / "R03_ORIGIN.json").exists() and "R03_EXISTING_LIVE_OR_FOREIGN_PROCESS" not in str(exc):
            hard = not isinstance(exc, (KeyboardInterrupt, SystemExit))
            record = {"error": repr(exc), "hard_gate": hard, "status": "R03_STOP_RETURN_TO_CONTROL_PLANE", "R01_AND_R02_HARD_STOP_NOT_REMOVED": True}
            write_new(root / ("INCIDENT_" + str(time.time_ns()) + ".json"), record)
            if hard and not (root / "HARD_STOP.json").exists():
                write_new(root / "HARD_STOP.json", record)
        raise


if __name__ == "__main__":
    main()
