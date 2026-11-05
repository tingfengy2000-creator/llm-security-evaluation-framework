"""Owner 11 offline evidence generator. It has no executable live command."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OWNER_COMMIT = "82dcd7c77854dc7b85eac5074db5669cd04ad0e0"
CONTROL = "ea7e7d6a585ac96dddf3d1c2dcc37113ee460612"
OWNER = "docs/paper1/dual_machine/owner_approvals/W1_5060_PILOT12_FAST_UNBLOCK_OWNER_AUTHORIZATION_20261105.md"
OWNER_SHA = "0891ae9db6563ee86f41501d5d3ff98608a3ac33e0e7ea0ea4a240af2837b603"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--live", action="store_true")
    args = parser.parse_args()
    if args.live:
        print("NEW_OWNER_LIVE_APPROVAL_REQUIRED", file=sys.stderr)
        return 2
    if not (sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode):
        print("ISOLATED_INTERPRETER_REQUIRED", file=sys.stderr)
        return 2

    sys.path.insert(0, str(ROOT / "src"))
    from llmguard.domains.retrieval.hidden_poisoning.chinese5060.fast_unblock_admission import (
        RUN_ROOT,
        V2,
        V2_BILLABLE_CAP,
        blocked_budget_template,
        grid_digest,
        refreeze,
    )
    from llmguard.domains.retrieval.hidden_poisoning.chinese5060.fast_unblock_evidence import (
        missing_token_proof,
        sealed_chunks,
        source_path,
        transfer_matrix,
    )
    from llmguard.domains.retrieval.hidden_poisoning.chinese5060.pilot_admission import (
        INPUT_CAP,
        MAX_CALLS,
        MODEL,
        Stop,
        json_bytes,
    )
    from llmguard.domains.retrieval.hidden_poisoning.chinese5060.pilot_inputs import (
        PINNED_INPUTS,
        PROPOSAL,
        SYSTEM_SHA,
        checked_bytes,
        load_cells,
    )
    from llmguard.domains.retrieval.hidden_poisoning.chinese5060.pilot_live_admission import (
        ADMISSION_INPUTS,
        PAIR_FILES,
        verify_projection,
    )
    from llmguard.domains.retrieval.hidden_poisoning.chinese5060.pilot_offline import (
        install_offline_barrier,
        local_de,
        prepare_output,
        redirect_environment,
    )
    from llmguard.domains.retrieval.hidden_poisoning.chinese5060.pilot_runner import Evidence

    try:
        local_de(ROOT)
        local_de(Path.cwd())
        local_de(Path(sys.executable))
        output = prepare_output(args.output_dir, ROOT / RUN_ROOT / "runs")
        chunk_reads = sealed_chunks(ROOT)
        install_offline_barrier(output, {ROOT / name for name in (*PINNED_INPUTS, *PAIR_FILES, *chunk_reads, OWNER)}
                                | {source_path(ROOT)})
        output.mkdir()
        redirect_environment(output)
        evidence = Evidence(output)
        checked_bytes(ROOT / OWNER, OWNER_SHA)
        old = load_cells(ROOT)
        verify_projection(ROOT, old)
        cells, diff = refreeze(old)
        plan_sha = evidence.record("V2_REQUEST_PLAN_PRIVATE.json", [
            {**cell.index_row(), "ordinal": i, "wire": cell.body.decode()}
            for i, cell in enumerate(cells, 1)
        ])
        config_sha = evidence.record("V2_SINGLE_FIELD_OUTPUT_CAP_PROPOSAL.json", {
            "version": V2, "v1_proposal_sha256": PINNED_INPUTS[PROPOSAL], "v1_grid_sha256": grid_digest(old),
            "v2_grid_sha256": grid_digest(cells), "v2_request_plan_sha256": plan_sha, "system_sha256": SYSTEM_SHA,
            "model": MODEL, "worlds": 36, "cells": MAX_CALLS, "unique_prompts": 80, "input_limit": INPUT_CAP,
            "removed_field": "max_tokens", "added_field": "max_completion_tokens", "field_value": 256,
            "documented_output_tolerance_candidate": 10, "billable_upper_candidate": V2_BILLABLE_CAP,
            "single_concurrency": True, "retries": 0, "send_order": "FIRST3_THEN_UP_TO_105",
            "real_release": "NEW_OWNER_LIVE_APPROVAL_REQUIRED",
        })
        diff_sha = evidence.record("FIELD_DIFF_PRIVATE.json", diff)
        transfer = transfer_matrix(ROOT, cells)
        token = missing_token_proof(cells)
        evidence.record("SOURCE_TRANSFER_RIGHTS_MATRIX.json", transfer)
        evidence.record("TOKEN_GRID_PRIVATE.json", token)
        evidence.record("BUDGET_PRIVATE.json", blocked_budget_template())
        evidence.record("REAL_OUTCOMES_PRIVATE.json", [
            {**cell.index_row(), "ordinal": i, "status": "NOT_RUN"} for i, cell in enumerate(cells, 1)
        ])
        evidence.record("ENDPOINT_PRIVATE.json", {"status": "OWNER_INPUT_REQUIRED", "region": None, "host": None,
                        "workspace": None, "account_status": "OWNER_ATTESTED"})
        result = {
            "status": "FAST_UNBLOCK_PARTIAL_BLOCKED", "owner_commit": OWNER_COMMIT,
            "owner_document_sha256": OWNER_SHA, "control_commit": CONTROL, "proposal_version": V2,
            "v1_wire_grid_sha256": grid_digest(old), "v2_wire_grid_sha256": grid_digest(cells),
            "v2_proposal_sha256": config_sha, "v2_private_plan_sha256": plan_sha, "field_diff_sha256": diff_sha,
            "immutable_input_sha256": {**PINNED_INPUTS, **PAIR_FILES}, "sealed_p2_chunk_files_read": len(chunk_reads),
            "cells": len(cells), "unique_prompts": len({c.prompt_hash for c in cells}),
            "transfer_sources": transfer["transfer_source_hashes"], "matching_source_snapshots": transfer["source_snapshots_matched"],
            "pii_screen_counts": transfer["marked_cells_per_pattern"],
            "context_review_pointer_count": len(transfer["high_risk_review_queue"]),
            "token": {k: v for k, v in token.items() if k != "rows"},
            "known_private_artifacts_present": {k: (ROOT / v).is_file() for k, v in ADMISSION_INPUTS.items()},
            "new_real_api_requests": 0, "new_real_cost_usd": "0", "real_not_run": MAX_CALLS,
            "private_files_sha256": evidence.files.copy(),
        }
        evidence.record("OFFLINE_EVIDENCE_SEAL.json", result)
        print(json_bytes(result).decode().strip())
        return 0
    except (Stop, OSError) as exc:
        print(str(exc) if isinstance(exc, Stop) else "OFFLINE_EVIDENCE_IO_STOP", file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
