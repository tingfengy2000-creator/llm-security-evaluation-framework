"""Independent offline preflight for Owner 10. The current checker issues no live lease."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = "src/llmguard/domains/retrieval/hidden_poisoning/chinese5060/"
SOURCES = ("scripts/research/check_chinese5060_pilot12_live.py", *(SRC + name for name in (
    "pilot_live_admission.py", "pilot_live_transport.py", "pilot_live_stage.py", "pilot_inputs.py",
    "pilot_design.py", "pilot_runner.py", "pilot_admission.py", "pilot_offline.py", "pilot_transport.py", "budget.py",
)))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--live", action="store_true", help="Requires an independent, verified live lease")
    parser.add_argument("--manifest-sha256", help="Identity alone cannot release a run")
    args = parser.parse_args()
    if not (sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode):
        print("ISOLATED_INTERPRETER_REQUIRED_USE_PYTHON_-I_-S_-B", file=sys.stderr)
        return 2

    sys.path.insert(0, str(ROOT / "src"))
    from llmguard.domains.retrieval.hidden_poisoning.chinese5060.pilot_admission import (
        MAX_CALLS,
        Stop,
        json_bytes,
        sha256,
    )
    from llmguard.domains.retrieval.hidden_poisoning.chinese5060.pilot_inputs import PINNED_INPUTS
    from llmguard.domains.retrieval.hidden_poisoning.chinese5060.pilot_live_admission import (
        OWNER,
        PAIR_FILES,
        RUN_ROOT,
        preflight,
        require_live_lease,
    )
    from llmguard.domains.retrieval.hidden_poisoning.chinese5060.pilot_offline import (
        install_offline_barrier,
        local_de,
        prepare_output,
        redirect_environment,
    )
    from llmguard.domains.retrieval.hidden_poisoning.chinese5060.pilot_runner import Evidence

    if args.live:
        try:
            require_live_lease()
        except Stop as exc:
            print(str(exc), file=sys.stderr)
            return 2
        raise RuntimeError("UNREACHABLE_NO_APPROVED_LIVE_ENTRY")

    evidence = None
    try:
        local_de(ROOT)
        local_de(Path.cwd())
        local_de(Path(sys.executable))
        output = prepare_output(args.output_dir, ROOT / RUN_ROOT / "runs")
        allow = {ROOT / name for name in (*PINNED_INPUTS, *PAIR_FILES, *SOURCES, OWNER)}
        install_offline_barrier(output, allow)
        output.mkdir()
        redirect_environment(output)
        evidence = Evidence(output)
        summary, cells = preflight(ROOT)
        summary["preflight_id"] = output.name
        summary["live_run_id"] = None
        summary["source_sha256"] = {name: sha256((ROOT / name).read_bytes()) for name in SOURCES}
        rows = [{**cell.index_row(), "ordinal": i, "status": "NOT_RUN"}
                for i, cell in enumerate(cells, 1)]
        evidence.record("OUTCOMES_PRIVATE.json", rows)
        evidence.record("ADMISSION_REFUSAL.json", summary)
        print(json_bytes(summary).decode().strip())
        return 3
    except (Stop, OSError) as exc:
        code = str(exc) if isinstance(exc, Stop) else "PREFLIGHT_IO_STOP"
        if evidence is not None:
            evidence.record("PREFLIGHT_ERROR.json", {
                "status": "LIVE_GATE_BLOCKED_NO_REQUESTS", "code": code, "real_post": 0,
                "outcomes": [{"ordinal": i, "status": "NOT_RUN"} for i in range(1, MAX_CALLS + 1)],
            })
        print(code, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
