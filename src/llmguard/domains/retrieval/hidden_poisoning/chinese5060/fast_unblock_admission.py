"""Owner 11 V2 freeze and independent, offline admission verification."""
from __future__ import annotations

import os
import re
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .pilot_admission import (
    HISTORICAL_DELTA_CNY,
    INPUT_CAP,
    MAX_CALLS,
    MODEL,
    OUTPUT_CAP,
    RESERVE_FACTOR,
    Budget,
    BudgetInput,
    Stop,
    json_bytes,
    money,
    sha256,
    strict_json,
    token_int,
    usd_ceiling,
)
from .pilot_inputs import PINNED_INPUTS, PROPOSAL, Cell
from .pilot_live_transport import verify_host
from .pilot_offline import local_de

RUN_ROOT = "experiments/paper1_chinese5060/W1-5060-FAST-UNBLOCK-20261105-01"
V2 = "V2_SINGLE_FIELD_OUTPUT_CAP"
V2_BILLABLE_CAP = OUTPUT_CAP + 10
# A later, explicit Owner decision must bind this to independently reviewed bytes.
# A local receipt, CLI flag, credentials, or the old V1 Owner decision cannot set it.
LIVE_AUTHORITY_SHA256: str | None = None
EVIDENCE_KEYS = frozenset({"transfer", "wire", "token", "budget", "price", "fx", "ledger", "balance",
                           "transfer_basis", "wire_basis", "token_basis"})


def digest_required(value: object) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"[a-f0-9]{64}", value):
        raise Stop("ADMISSION_DIGEST_MISSING_OR_INVALID")
    return value


def refreeze(cells: list[Cell]) -> tuple[list[Cell], list[dict[str, Any]]]:
    if len(cells) != MAX_CALLS:
        raise Stop("V2_REQUIRES_108_CELLS")
    revised: list[Cell] = []
    diffs: list[dict[str, Any]] = []
    for ordinal, cell in enumerate(cells, 1):
        old = strict_json(cell.body)
        if not isinstance(old, dict) or old.get("max_tokens") != OUTPUT_CAP or "max_completion_tokens" in old:
            raise Stop("V1_FIELD_IDENTITY_DRIFT")
        new = {k: v for k, v in old.items() if k != "max_tokens"}
        new["max_completion_tokens"] = OUTPUT_CAP
        raw = json_bytes(new)
        # Compare a fresh wire parse, including exact nested message strings.
        again = strict_json(raw)
        if (set(old) - set(again), set(again) - set(old)) != ({"max_tokens"}, {"max_completion_tokens"}):
            raise Stop("V2_FIELD_SET_DRIFT")
        if any(old[k] != again[k] for k in old.keys() & again.keys()):
            raise Stop("V2_OTHER_WIRE_CONTENT_DRIFT")
        revised.append(replace(cell, body=raw))
        diffs.append({"ordinal": ordinal, "request_id": cell.request_id, "prompt_sha256": cell.prompt_hash,
                      "v1_wire_sha256": sha256(cell.body), "v2_wire_sha256": sha256(raw)})
    return revised, diffs


def path_digest(path: Path) -> str:
    return sha256(os.fsencode(path))


def grid_digest(cells: list[Cell]) -> str:
    return sha256(json_bytes([cell.index_row() for cell in cells]))


class ReservedBudget(Budget):
    def __init__(self, config: BudgetInput, input_cap: int, output_cap: int) -> None:
        super().__init__(config)
        self.cell_max = usd_ceiling(config.tariff.charge(input_cap, 0, output_cap) * RESERVE_FACTOR)


@dataclass(frozen=True)
class CheckedAdmission:
    source_commit: str
    config_sha256: str
    request_grid_sha256: str
    evidence_manifest_sha256: str
    host: str
    region: str
    output: Path
    input_bounds: tuple[int, ...]
    budget: BudgetInput


def _object(raw: bytes) -> dict[str, Any]:
    result = strict_json(raw)
    if not isinstance(result, dict):
        raise Stop("ADMISSION_OBJECT_REQUIRED")
    return result


def check_admission(
    root: Path, output: Path, source_commit: str, config_sha256: str, config_raw: bytes,
    original: list[Cell], candidate: list[Cell], required_sources: set[str],
    manifest_raw: bytes, expected_manifest_sha256: str, artifacts: dict[str, bytes],
    *, at: datetime,
) -> CheckedAdmission:
    """Verify a separately pinned manifest and its evidence bytes. It grants no egress."""
    if sha256(manifest_raw) != digest_required(expected_manifest_sha256):
        raise Stop("ADMISSION_MANIFEST_SHA_DRIFT")
    if not re.fullmatch(r"[a-f0-9]{40}", source_commit):
        raise Stop("ADMISSION_SOURCE_COMMIT_INVALID")
    if sha256(config_raw) != digest_required(config_sha256):
        raise Stop("ADMISSION_CONFIG_SHA_DRIFT")
    config = _object(config_raw)
    revised, _ = refreeze(original)
    if (revised != candidate or len({c.prompt_hash for c in candidate}) != 80
            or any(not cell.citations for cell in candidate[:3])):
        raise Stop("ADMISSION_FROZEN_GRID_DRIFT")
    grid = grid_digest(candidate)
    if (config.get("version"), config.get("v1_proposal_sha256"), config.get("v2_grid_sha256")) != (
        V2, PINNED_INPUTS[PROPOSAL], grid
    ):
        raise Stop("ADMISSION_CONFIG_SCOPE_DRIFT")
    root, output = local_de(root), local_de(output)
    if output.parent != local_de(root / RUN_ROOT / "runs") or output.exists():
        raise Stop("ADMISSION_OUTPUT_NOT_NEW_CONTROLLED_DIRECTORY")
    if set(artifacts) != EVIDENCE_KEYS:
        raise Stop("ADMISSION_REQUIRED_EVIDENCE_MISSING")
    hashes = {key: sha256(raw) for key, raw in artifacts.items()}
    manifest = _object(manifest_raw)
    if manifest != {"source_commit": source_commit, "config_sha256": config_sha256, "request_grid_sha256": grid,
                    "output_path_sha256": path_digest(output), "version": V2, "artifacts_sha256": hashes}:
        raise Stop("ADMISSION_BINDING_DRIFT")

    wire = _object(artifacts["wire"])
    host, region = wire.get("host"), wire.get("region")
    if not isinstance(host, str) or not isinstance(region, str):
        raise Stop("WIRE_ACCOUNT_HOST_REQUIRED")
    verify_host(region, host)
    if wire != {"host": host, "region": region, "model": MODEL, "version": V2,
                "output_wire_field": "max_completion_tokens", "output_value": OUTPUT_CAP,
                "verified_billable_upper": V2_BILLABLE_CAP, "nonthinking_json_verified": True,
                "basis_sha256": hashes["wire_basis"]}:
        raise Stop("WIRE_BILLING_OR_PROTOCOL_UNVERIFIED")

    transfer = _object(artifacts["transfer"])
    if not required_sources or transfer != {
        "request_grid_sha256": grid, "allowed_sources": sorted(required_sources),
        "processor": "ALIBABA_CLOUD_MODEL_STUDIO", "host": host, "region": region,
        "scope": "ONLY_FROZEN_SYSTEM_QUERY_AND_RETAINED_TOPK",
        "source_rights_and_sensitive_clearance_sha256": hashes["transfer_basis"],
    }:
        raise Stop("TRANSFER_COVERAGE_OR_SCOPE_UNVERIFIED")

    token = _object(artifacts["token"])
    method = token.get("method")
    if (token.get("model") != MODEL or token.get("version") != V2
            or method not in ("VERIFIED_EXACT_CHAT_TEMPLATE", "PROVEN_STRICT_CHAT_UPPER_BOUND")
            or token.get("basis_sha256") != hashes["token_basis"]):
        raise Stop("STRICT_TOKEN_BOUND_UNAVAILABLE")
    rows = token.get("rows")
    if not isinstance(rows, list) or len(rows) != MAX_CALLS:
        raise Stop("STRICT_TOKEN_PROOF_GRID_MISSING")
    bounds = []
    for cell, row in zip(candidate, rows, strict=True):
        if not isinstance(row, dict) or set(row) != {"request_id", "request_sha256", "upper", "chat_overhead"}:
            raise Stop("STRICT_TOKEN_PROOF_ROW_INVALID")
        if (row["request_id"], row["request_sha256"]) != (cell.request_id, sha256(cell.body)):
            raise Stop("STRICT_TOKEN_PROOF_IDENTITY_DRIFT")
        upper = token_int(row["upper"])
        if not 0 < upper <= INPUT_CAP or token_int(row["chat_overhead"]) >= upper:
            raise Stop("STRICT_TOKEN_LIMIT_FAILED")
        bounds.append(upper)

    ledger = _object(artifacts["budget"])
    if set(ledger) != {"region", "failure_inflight_usd_included", "valid_until_utc", "snapshot"} or ledger["region"] != region:
        raise Stop("BUDGET_REGION_OR_PENDING_SCOPE_MISSING")
    snapshot = ledger["snapshot"]
    cfg = BudgetInput.from_manifest(snapshot)
    if snapshot["evidence_sha256"] != {key: hashes[key] for key in ("price", "fx", "ledger", "balance")}:
        raise Stop("BUDGET_SUPPORTING_BYTES_DRIFT")
    if money(ledger["failure_inflight_usd_included"]) > cfg.pending:
        raise Stop("BUDGET_FAILURE_HOLD_NOT_INCLUDED")
    try:
        as_of = datetime.fromisoformat(snapshot["as_of_utc"])
        expires = datetime.fromisoformat(ledger["valid_until_utc"])
        if at.utcoffset() is None or as_of.utcoffset() is None or expires.utcoffset() is None or not as_of <= at <= expires:
            raise Stop("BUDGET_SNAPSHOT_OUTSIDE_VALIDITY")
    except (TypeError, ValueError):
        raise Stop("BUDGET_SNAPSHOT_OUTSIDE_VALIDITY") from None
    ReservedBudget(cfg, max(bounds), V2_BILLABLE_CAP).check()
    return CheckedAdmission(source_commit, config_sha256, grid, expected_manifest_sha256, host, region,
                            output, tuple(bounds), cfg)


def check_live_authority(checked: CheckedAdmission, authority_raw: bytes) -> None:
    if LIVE_AUTHORITY_SHA256 is None or sha256(authority_raw) != LIVE_AUTHORITY_SHA256:
        raise Stop("NEW_OWNER_LIVE_APPROVAL_REQUIRED")
    approval = _object(authority_raw)
    owner_id = approval.pop("owner_id", "")
    if not isinstance(owner_id, str) or not re.fullmatch(r"W1-OD-[0-9]{8}-5060-[A-Z0-9-]+", owner_id):
        raise Stop("NEW_OWNER_LIVE_APPROVAL_REQUIRED")
    if owner_id.endswith(("-LIVE-10", "-UNBLOCK-11")) or approval != {
        "scope": "REAL_PILOT12_3PLUS105", "source_commit": checked.source_commit, "config_sha256": checked.config_sha256,
        "request_grid_sha256": checked.request_grid_sha256, "admission_sha256": checked.evidence_manifest_sha256,
        "output_path_sha256": path_digest(checked.output),
    }:
        raise Stop("LIVE_OWNER_BINDING_DRIFT")


def blocked_budget_template() -> dict[str, Any]:
    return {
        "status": "OWNER_INPUT_REQUIRED", "owner_account": "OWNER_ATTESTED",
        "region": None, "failure_inflight_usd_included": None, "valid_until_utc": None,
        "historical_difference_cny": str(HISTORICAL_DELTA_CNY),
        "snapshot": {"model": MODEL, "currency": None, "usd_per_billing_unit": None, "historical_usd_per_cny": None,
                     "uncached_input_per_million": None, "cached_input_per_million": None, "output_per_million": None,
                     "settled_all_streams_usd": None, "pending_all_streams_usd": None,
                     "available_usd_before_pending": None, "batch_ceiling_usd": None, "includes_all_streams": None,
                     "price_version": None, "as_of_utc": None,
                     "evidence_sha256": dict.fromkeys(("price", "fx", "ledger", "balance"))},
        "candidate_input_tokens": INPUT_CAP * MAX_CALLS, "candidate_output_tokens": V2_BILLABLE_CAP * MAX_CALLS,
        "whole_batch_reservation_usd": None, "warn_usd": 25, "stop_new_usd": 28, "total_cap_usd": 30,
    }


def utc_now() -> datetime:
    return datetime.now(timezone.utc)
