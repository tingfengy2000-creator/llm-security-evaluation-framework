"""Immutable role-blind input binding for the Runner."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .pilot_admission import INPUT_CAP, MAX_CALLS, Stop, sha256, strict_json, token_int
from .pilot_design import SYSTEM_TEMPLATE, canonical_hash, length_plan, messages
from .pilot_transport import encode

CONTROL_SHA = "e378f04835709a0753ab27f913638642714351bb"
PROPOSAL = "docs/paper1/dual_machine/chinese5060/pilot_design/PILOT_EXECUTION_PROPOSAL.json"
PRIVATE_ROOT = "experiments/paper1_chinese5060"
RUN_ROOT = PRIVATE_ROOT + "/W1-5060-RUNNER-20261105-01"
PRIVATE_PLAN = PRIVATE_ROOT + (
    "/W1-5060-PILOTDESIGN-20261105-01/runtime_plan/GENERATOR_REQUEST_PLAN_PRIVATE.json"
)
P2_SEAL = PRIVATE_ROOT + "/W1-5060-P2-20261104-T0-01/OUTPUT_SEAL.json"
PAIR_SEAL = PRIVATE_ROOT + "/W1-5060-FAST-B-20261105-PAIR01/PAIR_OUTPUT_SEAL.json"
BUDGET_FILE = RUN_ROOT + "/admission/BUDGET_PRIVATE.json"
SYSTEM_SHA = "b3c74613bc3700eacdce7dfedc382043013f452e321a13d8639b27817edbd1f1"
PINNED_INPUTS = {
    PROPOSAL: "0aaf4cfb28dc1e7d9fea8fcdc8f7143afd56857fa300f8b6e3f8f9d0ff081cb6",
    PRIVATE_PLAN: "7db82812f893fc0384b2896c98bb5c779504e19a5c45a097945962e840999c96",
    P2_SEAL: "4e11d89cb6f03291c124aab28f7181622b6766cc63d55be45126023147988c52",
    PAIR_SEAL: "bb775ead3d330f5e83516f8dfa871a3e2581c305e5ae7baf104500f781ac79fb",
}


@dataclass(frozen=True)
class Cell:
    request_id: str
    world_hash: str
    arm: str
    prompt_hash: str
    citations: tuple[str, ...]
    body: bytes
    planning_units: int

    def index_row(self) -> dict[str, str]:
        return {"request_id": self.request_id, "world_hash": self.world_hash, "arm": self.arm,
                "prompt_hash": self.prompt_hash, "request_body_sha256": sha256(self.body)}


def checked_bytes(path: Path, digest: str) -> bytes:
    if path != path.resolve():
        raise Stop("INPUT_PATH_REDIRECTED")
    with path.open("rb") as stream:
        raw = stream.read(2 * 1024 * 1024 + 1)
    if len(raw) > 2 * 1024 * 1024 or sha256(raw) != digest:
        raise Stop("FROZEN_BYTES_SHA_DRIFT")
    return raw


def load_cells(root: Path) -> list[Cell]:
    inputs = {name: checked_bytes(root / name, digest) for name, digest in PINNED_INPUTS.items()}
    proposal = strict_json(inputs[PROPOSAL])
    rows = strict_json(inputs[PRIVATE_PLAN])
    if canonical_hash(SYSTEM_TEMPLATE) != SYSTEM_SHA or proposal["system_prompt_hash"] != SYSTEM_SHA:
        raise Stop("SYSTEM_PROMPT_DRIFT")
    return validate_grid(rows, proposal["request_plan"])


def validate_grid(rows: Any, public: Any) -> list[Cell]:
    if not isinstance(rows, list) or not isinstance(public, list) or len(rows) != MAX_CALLS or len(public) != MAX_CALLS:
        raise Stop("FROZEN_108_CELLS_REQUIRED")
    cells: list[Cell] = []
    for index, (row, projected) in enumerate(zip(rows, public, strict=True)):
        if not isinstance(projected, dict) or not isinstance(row, dict):
            raise Stop("PLAN_ROW_SCHEMA")
        private_keys = {"world_id", "query", "messages", "retained_chunk_ids", "original_snapshot_hash"}
        if set(row) != set(projected) | private_keys or any(row[k] != v for k, v in projected.items()):
            raise Stop("PLAN_PUBLIC_PROJECTION_DRIFT")
        msg = row["messages"]
        if not isinstance(msg, list) or len(msg) != 2 or any(
            not isinstance(m, dict) or set(m) != {"role", "content"} or not isinstance(m["content"], str)
            for m in msg
        ):
            raise Stop("PLAN_MESSAGES_SCHEMA")
        user = strict_json(msg[1]["content"])
        if not isinstance(user, dict) or set(user) != {"question", "context"} or user["question"] != row["query"]:
            raise Stop("PLAN_USER_ENVELOPE_DRIFT")
        contexts = user["context"]
        if not isinstance(contexts, list) or any(
            not isinstance(c, dict) or set(c) != {"id", "text"} or not isinstance(c["id"], str)
            or not isinstance(c["text"], str) for c in contexts
        ):
            raise Stop("PLAN_CONTEXT_SCHEMA")
        citations = tuple(c["id"] for c in contexts)
        if any(c not in ("C1", "C2", "C3", "C4", "C5") for c in citations) or citations != tuple(sorted(set(citations))):
            raise Stop("PLAN_ORIGINAL_RANK_DRIFT")
        if (msg != messages(row["query"], contexts) or len(citations) != row["retained_chunk_count"]
                or len(citations) != len(row["retained_chunk_ids"])
                or row["query_hash"] != canonical_hash(row["query"])):
            raise Stop("PLAN_EXACT_MESSAGE_DRIFT")
        whash = canonical_hash({"world_id": row["world_id"], "snapshot_hash": row["original_snapshot_hash"]})
        arm = ("G0", "G1", "G2")[index % 3]
        phash = canonical_hash(msg)
        rid = "REQ-" + canonical_hash([whash, arm, phash])[:24]
        if (row["arm"], row["world_hash"], row["prompt_hash"], row["request_id"]) != (arm, whash, phash, rid):
            raise Stop("PLAN_CELL_ID_OR_HASH_DRIFT")
        if arm != "G0" and cells[-(index % 3)].world_hash != whash:
            raise Stop("PLAN_WORLD_ORDER_DRIFT")
        if arm == "G0" and citations != ("C1", "C2", "C3", "C4", "C5"):
            raise Stop("PLAN_G0_MUST_RETAIN_TOPK5")
        proxy = length_plan(msg)["planning_units_utf8_plus_chat_reserve"]
        cells.append(Cell(rid, whash, arm, phash, citations, encode(msg), proxy))
    if (len({c.world_hash for c in cells}) != 36 or len({c.request_id for c in cells}) != MAX_CALLS
            or len({c.prompt_hash for c in cells}) != 80):
        raise Stop("PLAN_36_WORLDS_80_UNIQUE_PROMPTS_REQUIRED")
    return cells


def token_audit(cells: list[Cell]) -> dict[str, Any]:
    proxy = [cell.planning_units for cell in cells]
    return {
        "status": "TOKEN_GATE_BLOCKED",
        "method": "INEXACT_UTF8_CONTENT_BYTES_PLUS_512_NOT_A_CERTIFIED_UPPER_BOUND",
        "cells": len(cells), "exact_input_tokens": None, "max_proxy": max(proxy),
        "proxy_over_4096": sum(value > INPUT_CAP for value in proxy), "sum_proxy": sum(proxy),
        "tokenizer": "NO_VERIFIED_MODEL_AND_CHAT_TEMPLATE_IDENTITY",
    }


def check_input_tokens(value: object) -> int:
    count = token_int(value)
    if not 0 < count <= INPUT_CAP:
        raise Stop("INPUT_TOKEN_GATE_EXCEEDED")
    return count
