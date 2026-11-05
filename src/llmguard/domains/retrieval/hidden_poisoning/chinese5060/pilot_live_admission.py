"""Owner 10 offline admission checker. A refusal cannot issue a network lease."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .pilot_admission import MAX_CALLS, MODEL, Stop, sha256, strict_json
from .pilot_design import canonical_hash, messages, select_contexts
from .pilot_inputs import PINNED_INPUTS, PROPOSAL, Cell, checked_bytes, load_cells, token_audit
from .pilot_transport import encode

CONTROL = "312f9b17dba2a20c142507ce7df5ec7ae203642d"
OWNER_COMMIT = "74c816e264a94a7ec2013d0d5127ac4df3720944"
OWNER_SHA = "8710e0a797b0d3b24ba3adc4d6453a26b630620fce4d57552ab2bb5873f90b4c"
OWNER_ID = "W1-OD-20261105-5060-PILOT12-CONDITIONAL-LIVE-10"
OWNER = "docs/paper1/dual_machine/owner_approvals/W1_5060_PILOT12_CONDITIONAL_LIVE_RUN_AUTHORIZATION_20261105.md"
BASE = "experiments/paper1_chinese5060/"
RUN_ROOT = BASE + "W1-5060-PILOTLIVE-20261105-01"
PAIR = BASE + "W1-5060-FAST-B-20261105-PAIR01/"
FAST_C_ARCHIVE = BASE + "archives/W1-5060-FAST-C-ATTRIB01-20261105.zip"
PAIR_FILES = {
    PAIR + "PACKETS_PRIVATE.json": "d0f196ab994a94bfd0804c37c08b81d41f582aaf2d74e143c26560ffa7043525",
    PAIR + "B1_RESULTS_PRIVATE.json": "5831dcacb3132c4e6a65344f45dc18f1b85e1b9605815f5d9adb87897239fb74",
    PAIR + "B2_RESULTS_PRIVATE.json": "9b65b5d7c412aea78a5d66f4d5402743afd029802eb0af981ebdd929376feb4f",
    FAST_C_ARCHIVE: "73b3f66a5b410e61cc8b9772885c77e026de502b3b9d78b295fa2e52b4a9fdb4",
}
ADMISSION_INPUTS = {
    "transfer": RUN_ROOT + "/admission/TRANSFER_SCOPE_PRIVATE.json",
    "wire": RUN_ROOT + "/admission/WIRE_PRIVATE.json",
    "token": RUN_ROOT + "/admission/TOKEN_PROOF_PRIVATE.json",
    "budget": BASE + "W1-5060-RUNNER-20261105-01/admission/BUDGET_PRIVATE.json",
    "manifest": RUN_ROOT + "/admission/RUN_ADMISSION_MANIFEST.json",
}


def verify_projection(root: Path, cells: list[Cell]) -> None:
    """Rebuild bytes from the three old role-blind inputs without a retriever or filter."""
    checked = {name: checked_bytes(root / name, digest) for name, digest in PAIR_FILES.items()}
    packets = strict_json(checked[PAIR + "PACKETS_PRIVATE.json"])
    arms = {
        name: {row["world_id"]: row for row in strict_json(checked[PAIR + f"B{index}_RESULTS_PRIVATE.json"])}
        for index, name in ((1, "G1"), (2, "G2"))
    }
    if len(packets) != 36 or any(len(rows) != 36 for rows in arms.values()):
        raise Stop("SOURCE_WORLD_COUNT_DRIFT")
    for i, packet in enumerate(packets):
        whash = canonical_hash({"world_id": packet["world_id"], "snapshot_hash": packet["snapshot_hash"]})
        ids = [chunk["chunk_id"] for chunk in packet["chunks"]]
        for offset, arm in enumerate(("G0", "G1", "G2")):
            retained, removed = ids, []
            if arm != "G0":
                row = arms[arm][packet["world_id"]]
                if row["status"] != "PASS" or row["snapshot_hash"] != packet["snapshot_hash"]:
                    raise Stop("SOURCE_PAIR_FILTER_IDENTITY_DRIFT")
                retained, removed = row["retained_chunk_ids"], row["removed_indices"]
            context = select_contexts(packet["chunks"], removed, retained)
            msg = messages(packet["query"], context)
            cell = cells[3 * i + offset]
            if (cell.world_hash, cell.arm, cell.prompt_hash, cell.body) != (
                whash, arm, canonical_hash(msg), encode(msg)
            ):
                raise Stop("SOURCE_PROJECTION_DRIFT")


# A lexical warning triggers local review only. A clean scan does not prove rights/PII clearance.
PATTERNS = {
    "email": re.compile(r"(?i)\b[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}\b"),
    "mobile_cn": re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)"),
    "citizen_id_shape": re.compile(r"(?<!\d)\d{17}[\dXx](?!\d)"),
    "credential_shape": re.compile(r"(?i)\b(?:sk-[a-z0-9]{16,}|AKIA[A-Z0-9]{16})\b|-----BEGIN .*PRIVATE KEY-----"),
}


def scan_payloads(cells: list[Cell]) -> dict[str, int]:
    counts = dict.fromkeys(PATTERNS, 0)
    for cell in cells:
        wire = strict_json(cell.body)
        envelope = strict_json(wire["messages"][1]["content"])
        parts = [envelope["question"], *(chunk["text"] for chunk in envelope["context"])]
        for name, pattern in PATTERNS.items():
            counts[name] += int(any(pattern.search(part) for part in parts))
    return counts


def preflight(root: Path) -> tuple[dict[str, Any], list[Cell]]:
    cells = load_cells(root)
    verify_projection(root, cells)
    owner_hash = sha256(checked_bytes(root / OWNER, OWNER_SHA))
    present = {key: (root / path).is_file() for key, path in ADMISSION_INPUTS.items()}
    proposal = strict_json(checked_bytes(root / PROPOSAL, PINNED_INPUTS[PROPOSAL]))
    denominators = proposal["independent_evaluation"]["denominators"]
    # Missing evidence cannot be replaced by a digest supplied in argv or a self-authored PASS receipt.
    # This build ships the negative checker only. A positive verifier needs independently anchored sources.
    gates = {
        "A": {"status": "BLOCKED", "local_projection": "PASS_108", "patterns_flagged_cells": scan_payloads(cells),
              "reason": "NO_VERIFIED_PER_SOURCE_PROCESSOR_TRANSFER_RIGHTS_AND_SENSITIVITY_CLEARANCE"},
        "B": {"status": "BLOCKED", "reason": "NO_BOUND_ACCOUNT_REGION_HOST_OR_256_TOTAL_BILLABLE_TOKEN_PROOF"},
        "C": {"status": "BLOCKED", "reason": "NO_VERIFIABLE_MODEL_CHAT_TOKENIZER_OR_STRICT_BOUND"},
        "D": {"status": "BLOCKED", "reason": "NO_VERIFIED_ALL_STREAM_BUDGET_FX_BALANCE_AND_WIRE_BOUND"},
        "E": {"status": "BLOCKED", "reason": "NO_INDEPENDENTLY_VERIFIED_ALL_PASS_IMMUTABLE_ADMISSION"},
    }
    return {
        "status": "LIVE_GATE_BLOCKED_NO_REQUESTS", "gates": gates,
        "authority": {"id": OWNER_ID, "git_commit": OWNER_COMMIT, "document_sha256": owner_hash,
                      "control_commit": CONTROL},
        "source_evidence_sha256": {**PINNED_INPUTS, **PAIR_FILES},
        "admission_artifacts_present": present, "model": MODEL, "owner_account": "OWNER_ATTESTED",
        "worlds": 36, "cells": MAX_CALLS, "unique_prompts": len({cell.prompt_hash for cell in cells}),
        "context_empty": sum(not cell.citations for cell in cells),
        "single_chunk": sum(len(cell.citations) == 1 for cell in cells),
        "candidate_hit_worlds": denominators["retrieved_conditional"], "candidate_miss_worlds": 7,
        "token_audit": token_audit(cells),
        "initial3": "NOT_RUN", "real_post": 0, "real_success": 0, "real_fail": 0,
        "real_not_run": MAX_CALLS, "real_input_tokens": 0, "real_output_tokens": 0,
        "new_cost_usd": "0", "new_pending_usd": "0", "evaluation": "NOT_RUN",
    }, cells


def require_live_lease() -> None:
    """Until positive machine evidence is supported, this checker never releases a socket."""
    raise Stop("LIVE_DENIAL_WHEN_GATE_FAILED")
