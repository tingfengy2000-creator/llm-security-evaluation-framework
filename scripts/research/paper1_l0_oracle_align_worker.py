"""Oracle claim-alignment entry. Inference and evaluation are separate phases."""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "src"), str(ROOT)]

from llmguard.domains.retrieval.hidden_poisoning.method_engineering.l0_oracle_align import infer_aligned, orchestrate  # noqa: E402
from llmguard.domains.retrieval.hidden_poisoning.method_engineering.l0_worker import write_new  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=("orchestrate", "infer"), required=True)
    parser.add_argument("--full01-dir", type=Path, required=True)
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--model-dir", type=Path)
    args = parser.parse_args()
    root = args.work_dir.resolve()
    try:
        if args.phase == "orchestrate":
            orchestrate(args.full01_dir, root, ROOT)
        else:
            if args.model_dir is None:
                raise RuntimeError("MODEL_DIR_REQUIRED")
            infer_aligned(root, ROOT, args.model_dir, args.full01_dir)
    except BaseException as exc:
        hard = not isinstance(exc, (KeyboardInterrupt, SystemExit))
        if root.exists() and hard and not (root / "HARD_STOP.json").exists() and (root / "CONFIG_LOCK.json").exists():
            write_new(root / "HARD_STOP.json", {"error": repr(exc), "hard_gate": True, "status": "ORACLE_CLAIM_ALIGNMENT_DEV_BLOCKED", "no_automatic_repair_or_next_run": True})
        if root.exists():
            write_new(root / ("INCIDENT_" + str(time.time_ns()) + ".json"), {"error": repr(exc), "hard_gate": hard})
        raise


if __name__ == "__main__":
    main()
