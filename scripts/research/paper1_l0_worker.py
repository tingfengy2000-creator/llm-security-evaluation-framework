"""One 5090 Cursor entrypoint: check-only, then full bounded resumable workflow."""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "src"), str(ROOT)]

from llmguard.domains.retrieval.hidden_poisoning.method_engineering.l0_worker import infer, orchestrate, write_new  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-zip", type=Path)
    parser.add_argument("--work-dir", type=Path, default=ROOT / "experiments/vace_l0_worker_20261029_run01")
    parser.add_argument("--python", type=Path, help="Existing isolated research interpreter if available")
    parser.add_argument("--model-dir", type=Path, help="Optional existing exact official model snapshot")
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--infer-phase", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    try:
        if args.infer_phase:
            if args.model_dir is None:
                parser.error("--model-dir required for internal phase")
            infer(args.work_dir.resolve(), ROOT, args.model_dir.resolve())
        else:
            if args.input_zip is None:
                parser.error("--input-zip required; private inputs are not in Git")
            orchestrate(args, ROOT)
    except BaseException as exc:
        if args.work_dir.exists():
            hard = not isinstance(exc, (KeyboardInterrupt, SystemExit)) and (args.infer_phase or any(k in str(exc).upper() for k in ("CUDA", "VRAM", "BUDGET", "SHA", "IDENTITY", "FROZEN", "SYNTHETIC", "DEVICE", "COHORT", "INTEGRITY")))
            record = {"error": repr(exc), "status": "STOP_RETURN_TO_CONTROL_PLANE", "hard_gate": hard, "no_alternative_model_or_protocol_authorized": True}
            write_new(args.work_dir / ("INCIDENT_" + str(time.time_ns()) + ".json"), record)
            if hard and not (args.work_dir / "HARD_STOP.json").exists():
                write_new(args.work_dir / "HARD_STOP.json", record)
        raise


if __name__ == "__main__":
    main()
