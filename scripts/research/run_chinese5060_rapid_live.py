"""Run or independently check the fixed Owner12 Pilot12 V2 batch."""
# ruff: noqa: E402 -- The isolated launcher must add the frozen src directory first.
from __future__ import annotations

import argparse
import os
import re
import sys
from collections.abc import Callable
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from llmguard.domains.retrieval.hidden_poisoning.chinese5060.fast_unblock_runner import RapidRun, _run
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.pilot_admission import Stop, json_bytes, sha256
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.pilot_inputs import Cell
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.pilot_live_transport import (
    _exchange,
    _install_socket_policy,
)
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.pilot_transport import Reply
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.rapid_live_admission import (
    CHECKER_MANIFEST,
    RUN_ROOT,
    verify_rapid_admission,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    operation = parser.add_mutually_exclusive_group(required=True)
    operation.add_argument("--check-only", action="store_true")
    operation.add_argument("--live", action="store_true")
    args = parser.parse_args()
    try:
        manifest, cells, host = verify_rapid_admission(ROOT)
        raw = json_bytes(manifest)
        receipt = ROOT / RUN_ROOT / CHECKER_MANIFEST
        if args.check_only:
            with receipt.open("xb") as file:
                file.write(raw)
                file.flush()
                os.fsync(file.fileno())
            print(json_bytes({"status": manifest["status"], "admission_sha256": sha256(raw)}).decode(), end="")
            return 0
        if receipt.resolve() != receipt or not receipt.is_file() or receipt.read_bytes() != raw:
            raise Stop("RAPID_INDEPENDENT_CHECKER_RECEIPT_MISSING_OR_DRIFT")
        key = os.environ.get("DASHSCOPE_API_KEY")
        if not key:
            raise Stop("LIVE_CREDENTIAL_UNAVAILABLE")
        _install_socket_policy()

        def send(cell: Cell, _: int, record_post: Callable[[str], None]) -> Reply:
            return _exchange("cn-beijing", host, cell.body, key, post_phase=record_post)

        result = _run(
            RapidRun(Path(manifest["output_path"]), manifest["request_grid_sha256"], sha256(raw)),
            cells, send, "LIVE", admission_raw=raw,
        )
        print(json_bytes(result).decode(), end="")
        return 0 if result["status"] == "COMPLETE" else 3
    except Stop as exc:
        code = str(exc)
        print(code if re.fullmatch(r"[A-Z0-9_]{1,120}", code) else "RAPID_CONTROLLED_STOP", file=sys.stderr)
        return 2
    except (KeyError, OSError, ValueError, TypeError, RuntimeError):
        print("RAPID_CONTROLLED_IO_OR_SCHEMA_STOP", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
