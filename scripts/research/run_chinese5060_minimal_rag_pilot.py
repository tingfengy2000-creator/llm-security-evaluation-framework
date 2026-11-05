"""5060 Pilot12 Runner. Run only with python -I -S -B and --dry-run or --preflight."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# The isolated interpreter deliberately ignores PYTHONPATH and site packages.
ROOT = Path(__file__).resolve().parents[2]
SCRIPT = "scripts/research/run_chinese5060_minimal_rag_pilot.py"
SOURCE_ROOT = "src/llmguard/domains/retrieval/hidden_poisoning/chinese5060/"
SOURCE_FILES = (SCRIPT, *(SOURCE_ROOT + name for name in (
    "budget.py", "pilot_design.py", "pilot_admission.py", "pilot_inputs.py",
    "pilot_offline.py", "pilot_runner.py", "pilot_transport.py",
)))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--preflight", action="store_true")
    mode.add_argument("--live", action="store_true", help="Always blocked by Owner 09")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--owner-execution-approval", help="Future gate placeholder; cannot unlock this build")
    parser.add_argument("--budget-sha256", help="Only preflight. Hash of the fixed private budget manifest")
    parser.add_argument("--fake-failure", help="Only dry run. One synthetic failure as ORDINAL:CODE")
    args = parser.parse_args()
    if args.live:
        print("LIVE_NOT_AUTHORIZED", file=sys.stderr)
        return 2
    if not (sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode):
        print("ISOLATED_INTERPRETER_REQUIRED_USE_PYTHON_-I_-S_-B", file=sys.stderr)
        return 2

    sys.path.insert(0, str(ROOT / "src"))
    from llmguard.domains.retrieval.hidden_poisoning.chinese5060.pilot_admission import (
        MAX_CALLS,
        Budget,
        BudgetInput,
        Stop,
        fake_budget,
        json_bytes,
        sha256,
        strict_json,
    )
    from llmguard.domains.retrieval.hidden_poisoning.chinese5060.pilot_inputs import (
        BUDGET_FILE,
        PINNED_INPUTS,
        RUN_ROOT,
        checked_bytes,
        load_cells,
        token_audit,
    )
    from llmguard.domains.retrieval.hidden_poisoning.chinese5060.pilot_offline import (
        install_offline_barrier,
        local_de,
        prepare_output,
        redirect_environment,
    )
    from llmguard.domains.retrieval.hidden_poisoning.chinese5060.pilot_runner import FAULTS, Evidence, run_fake
    from llmguard.domains.retrieval.hidden_poisoning.chinese5060.pilot_transport import FakeTransport

    faults: dict[int, str] = {}
    evidence = None
    try:
        if args.owner_execution_approval is not None:
            raise Stop("LIVE_NOT_AUTHORIZED")
        if args.fake_failure:
            if not args.dry_run:
                raise Stop("FAKE_FAILURE_REQUIRES_DRY_RUN")
            match = re.fullmatch(r"([1-9][0-9]{0,2}):([a-z_]+)", args.fake_failure)
            if not match or int(match[1]) > MAX_CALLS or match[2] not in FAULTS:
                raise Stop("INVALID_FAKE_FAILURE")
            faults[int(match[1])] = match[2]
        if args.budget_sha256 and (not args.preflight or not re.fullmatch(r"[a-f0-9]{64}", args.budget_sha256)):
            raise Stop("BUDGET_DIGEST_REQUIRES_PREFLIGHT")
        local_de(ROOT)
        if Path(sys.executable).drive.upper() not in {"D:", "E:"}:
            raise Stop("PYTHON_EXECUTABLE_MUST_BE_ON_D_OR_E")
        output = prepare_output(args.output_dir, ROOT / RUN_ROOT / "runs")
        reads = {ROOT / name for name in (*PINNED_INPUTS, *SOURCE_FILES)}
        if args.budget_sha256:
            reads.add(ROOT / BUDGET_FILE)
        install_offline_barrier(output, reads)
        output.mkdir()
        redirect_environment(output)
        evidence = Evidence(output)
        source = {name: sha256((ROOT / name).read_bytes()) for name in SOURCE_FILES}
        cells = load_cells(ROOT)
        if args.preflight:
            gates = {
                "owner_account_model_region_rates_balance": "OWNER_ATTESTED",
                "live": "LIVE_NOT_AUTHORIZED",
                "wire": "WIRE_UNVERIFIED",
                "token": token_audit(cells),
                "budget": "BUDGET_GATE_BLOCKED",
                "budget_numeric_result": None,
                "budget_config_sha256": args.budget_sha256,
                "real_api_calls": 0,
                "real_cost_usd": "0",
                "cells": len(cells),
                "source_file_sha256": source,
                "process_socket_barrier": "DENIED_BEFORE_SOCKET_CREATION",
            }
            if args.budget_sha256:
                try:
                    raw = checked_bytes(ROOT / BUDGET_FILE, args.budget_sha256)
                    budget = Budget(BudgetInput.from_manifest(strict_json(raw)))
                    decision = budget.check()
                    gates["budget_numeric_result"] = {
                        "decision": decision, "per_cell_reserved_usd": str(budget.cell_max),
                        "whole_batch_reserved_usd": str(budget.remaining * budget.cell_max),
                        "evidence_authenticity": "REQUIRES_FUTURE_OWNER_BINDING",
                    }
                except (Stop, OSError) as exc:
                    gates["budget_numeric_result"] = {"decision": str(exc) if isinstance(exc, Stop) else "BUDGET_IO_DENIED"}
            evidence.record("PREFLIGHT.json", gates)
            print(json_bytes(gates).decode().strip())
            return 0
        summary = run_fake(cells, evidence, Budget(fake_budget()), FakeTransport(faults), source)
        print(json_bytes(summary).decode().strip())
        return 0 if summary["status"] == "MOCK_COMPLETE" else 3
    except (Stop, OSError) as exc:
        code = str(exc) if isinstance(exc, Stop) else "IO_OR_PERMISSION_STOP"
        if evidence is not None:
            try:
                evidence.record("ABORT_PRIVATE.json", {
                    "stop_code": code, "real_generation": "NOT_RUN", "registered_real_cells": MAX_CALLS,
                    "real_api_calls": 0, "real_cost_usd": "0",
                    "real_outcomes": [{"ordinal": n, "status": "NOT_RUN"} for n in range(1, MAX_CALLS + 1)],
                    "recovery": "Preserve original plan index and durable journal if present. Never resume automatically.",
                })
            except OSError:
                # A failing disk/permission boundary can leave only the durable prefix.
                pass
        print(code, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
