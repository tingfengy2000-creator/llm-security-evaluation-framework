"""Full D1 development entry. Does not rerun R05 or R06."""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "src"), str(ROOT)]

from llmguard.domains.retrieval.hidden_poisoning.method_engineering.l0_full01 import orchestrate_full01  # noqa: E402
from llmguard.domains.retrieval.hidden_poisoning.method_engineering.l0_worker import write_new  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--r01-dir", type=Path, required=True)
    parser.add_argument("--r02-dir", type=Path, required=True)
    parser.add_argument("--r03-dir", type=Path, required=True)
    parser.add_argument("--r05-dir", type=Path, required=True)
    parser.add_argument("--r06-dir", type=Path, required=True)
    parser.add_argument("--work-dir", type=Path, required=True)
    args = parser.parse_args()
    root = args.work_dir.resolve()
    try:
        orchestrate_full01(args, ROOT)
    except BaseException as exc:
        hard = not isinstance(exc, (KeyboardInterrupt, SystemExit))
        if root.exists() and (root / "FULL01_ORIGIN.json").exists() and hard and not (root / "HARD_STOP.json").exists():
            write_new(root / "HARD_STOP.json", {"error": repr(exc), "hard_gate": True, "status": "L0_D1_DEV_FULL_BLOCKED", "no_automatic_repair_or_next_run": True})
        if root.exists():
            write_new(root / ("INCIDENT_" + str(time.time_ns()) + ".json"), {"error": repr(exc), "hard_gate": hard})
        raise


if __name__ == "__main__":
    main()
