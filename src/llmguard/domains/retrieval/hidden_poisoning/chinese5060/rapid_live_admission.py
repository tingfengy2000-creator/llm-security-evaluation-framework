"""Verify the single Owner12 V2 live admission against the frozen local inputs."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from .fast_unblock_admission import grid_digest, refreeze
from .pilot_admission import MODEL, Stop, sha256, strict_json
from .pilot_inputs import Cell, checked_bytes, load_cells
from .pilot_live_admission import scan_payloads, verify_projection
from .pilot_live_transport import verify_host
from .pilot_offline import local_de, require_space

DOCS = "docs/paper1/dual_machine/owner_approvals/"
OWNER = DOCS + "W1_5060_PILOT12_RAPID_LIVE_OWNER_AUTHORIZATION_20261105.md"
WAIVER = DOCS + "W1_5060_PILOT12_RAPID_LIVE_BUDGET_WAIVER.md"
OWNER_SHA = "dcdd24fc93229c3f6f2d3f6eb46f45345222251ea918da2dc34fe4ee43b96602"
WAIVER_SHA = "f85070e6b71c4a82f2e5af215e160a743a9a888685806f949ca0981cde9f8525"
BASE = "experiments/paper1_chinese5060/"
RUN_ROOT = BASE + "W1-5060-RAPID-LIVE-20261105-01"
RUN_ID = "OWNER12_LIVE_108"
CHECKER_MANIFEST = "RAPID_LIVE_ADMISSION_MANIFEST.json"
RECOVERY = BASE + "W1-5060-EVIDENCE-RECOVERY-20261105-01/"
V2 = BASE + "W1-5060-FAST-UNBLOCK-20261105-01/runs/QA_EVIDENCE_FINAL01/"
PLAN = V2 + "V2_REQUEST_PLAN_PRIVATE.json"
PLAN_SHA = "0920add3e5b5383a9b685207cabeb539bb3d414ee1db30c6f7a313d37469bbcc"
GRID_SHA = "78708759e0965e816d9d5b7aaa0bca92d2a6b92562930cd028dc87875d09468c"
HISTORICAL_LOCK = (
    ".worktrees/paper1-feasibility-sprint-01/experiments/paper1_feasibility_sprint_01/"
    "D1-DEV-BEIJING-CONT-A01/CONFIG_LOCK.json"
)
ASSETS = {
    "proposal": (V2 + "V2_SINGLE_FIELD_OUTPUT_CAP_PROPOSAL.json",
                 "e5bd219b7812b8ef97ef916226ac221e177f227808cd0dbc0bbe280920d1b70e"),
    "plan": (PLAN, PLAN_SHA),
    "sources": (RECOVERY + "SOURCE_ORIGIN_RECONCILIATION_PRIVATE.json",
                "21db4e4feebf39df6410ae4b2954542b5c2e30d3bf176f9b8c8e105122e05a26"),
    "outbound_scope": (RUN_ROOT + "/OUTBOUND_SCOPE_PRIVATE.json",
                       "d3ed97f90d227816849c4d0b5122f3dd64105d4eb4260afbdbf434d459236f8c"),
    "endpoint": (RECOVERY + "ENDPOINT_PRIVATE.json",
                 "3e84064dbfdcbb13e4d3d5213c3d85158898073bc01e8b41b8067370ddb31882"),
    "historical_ledger": (RECOVERY + "ACCOUNT_AND_LEDGER_RECOVERY_PRIVATE.json",
                          "63511193ce83635db8a53fb3b5d98361db793969de4aed29a8217a206f57c9b1"),
}
SOURCE = "src/llmguard/domains/retrieval/hidden_poisoning/chinese5060/"
SCRIPT = "scripts/research/run_chinese5060_rapid_live.py"
BOUND_CODE = (
    SCRIPT, *(SOURCE + f"{name}.py" for name in (
        "rapid_live_admission", "fast_unblock_runner", "fast_unblock_admission", "pilot_inputs",
        "pilot_runner", "pilot_admission", "pilot_live_admission", "pilot_live_transport",
        "pilot_transport", "pilot_live_stage", "pilot_offline", "pilot_design",
    )),
)


def _git(root: Path, *args: str) -> bytes:
    proc = subprocess.run(["git", *args], cwd=root, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=False)
    if proc.returncode:
        raise Stop("LIVE_GIT_PREFLIGHT_FAILED")
    return proc.stdout


def _check_authority(root: Path) -> tuple[str, dict[str, str]]:
    branch = _git(root, "branch", "--show-current").strip()
    head = _git(root, "rev-parse", "HEAD").decode("ascii").strip()
    if (branch != b"research/paper1-chinese-defense-5060" or not re.fullmatch(r"[0-9a-f]{40}", head)
            or _git(root, "status", "--porcelain=v1")):
        raise Stop("LIVE_GIT_NOT_CLEAN_5060")
    for name, digest in ((OWNER, OWNER_SHA), (WAIVER, WAIVER_SHA)):
        raw = checked_bytes(root / name, digest)
        if _git(root, "show", f"HEAD:{name}") != raw:
            raise Stop("LIVE_GIT_OWNER_BYTES_DRIFT")
    if _git(root, "show", f"d0737d3e6f43b322586df9ead88f9e8faecd5969:{OWNER}") != (root / OWNER).read_bytes():
        raise Stop("LIVE_GIT_ORIGINAL_OWNER_DRIFT")
    hashes = {}
    for name in BOUND_CODE:
        raw = _git(root, "show", f"{head}:{name}")
        hashes[name] = sha256(raw)
        checked_bytes(root / name, hashes[name])
    return head, hashes


def _check_wire(cells: list[Cell], plan: Any, sources: Any, scope: Any) -> None:
    if (grid_digest(cells) != GRID_SHA or len(plan) != 108 or not all(cell.citations for cell in cells)
            or any(scan_payloads(cells).values())):
        raise Stop("LIVE_V2_GRID_OR_PAYLOAD_DRIFT")
    observed = {}
    unique: set[str] = set()
    for ordinal, (cell, row) in enumerate(zip(cells, plan, strict=True), 1):
        if row != {"ordinal": ordinal, **cell.index_row(), "wire": cell.body.decode("utf-8")}:
            raise Stop("LIVE_V2_FROZEN_WIRE_DRIFT")
        system, user = strict_json(cell.body)["messages"]
        envelope = strict_json(user["content"])
        unique.update((system["content"], envelope["question"]))
        for chunk in envelope["context"]:
            text = chunk["text"]
            unique.add(text)
            observed[(ordinal, int(chunk["id"][1:]))] = (cell.request_id, cell.arm, sha256(text.encode()))
    roots = {"SIGNED_D1_CONSTRUCTION_BODY": 0, "OFFICIAL_SNAPSHOT": 0}
    hashes = set()
    for record in sources["records"]:
        hashes.add(record["source_hash"])
        roots[record["root"]] += 1
        for loc in record["locations"]:
            value = observed.pop((loc["ordinal"], loc["rank"]), None)
            if value != (loc["request_id"], loc["arm"], loc["chunk_sha256"]):
                raise Stop("LIVE_OUTBOUND_SOURCE_MAPPING_DRIFT")
    if (observed or len(hashes) != 46 or roots != {"SIGNED_D1_CONSTRUCTION_BODY": 29, "OFFICIAL_SNAPSHOT": 17}
            or scope["unique_outbound_texts_context_reviewed"] != len(unique)
            or scope["occurrences"] != sum(len(record["locations"]) for record in sources["records"])
            or scope["plan_sha256"] != PLAN_SHA or scope["source_index_sha256"] != ASSETS["sources"][1]
            or scope["processor"] != "ALIBABA_CLOUD_MODEL_STUDIO" or scope["region"] != "cn-beijing"
            or scope["scope"] != "ONLY_FROZEN_SYSTEM_QUERY_AND_RETAINED_TOPK"):
        raise Stop("LIVE_OUTBOUND_CLEARANCE_NOT_BOUND")


def _check_endpoint(root: Path, endpoint: Any) -> str:
    historical_raw = checked_bytes(
        local_de(root.parents[1] / HISTORICAL_LOCK),
        "c5cc22414245107ff9d321a0290952e3e3fe478146e02c8cb5099aa9f7f05239",
    )
    historical = strict_json(historical_raw)["config"]
    base = urlsplit(endpoint["base_url"])
    host = endpoint["host"]
    verify_host("cn-beijing", host)
    if (base.scheme != "https" or base.netloc != host or base.path != "/compatible-mode/v1"
            or base.query or base.fragment or not host.endswith(".cn-beijing.maas.aliyuncs.com")
            or endpoint["workspace"] != host.split(".")[0] or endpoint["exact_model"] != MODEL
            or endpoint["region"] != "cn-beijing" or historical["account_region"] != "cn-beijing"
            or historical["base_url"].rstrip("/") != endpoint["base_url"]
            or historical["model"] != MODEL or historical["owner_transfer_authorized"] is not True
            or historical["license_and_confidentiality_confirmed"] is not True):
        raise Stop("LIVE_BEIJING_WORKSPACE_BINDING_DRIFT")
    return str(host)


def verify_rapid_admission(root: Path) -> tuple[dict[str, Any], list[Cell], str]:
    root = local_de(root)
    head, source = _check_authority(root)
    output = local_de(root / RUN_ROOT / RUN_ID)
    if output.exists():
        raise Stop("DUPLICATE_RUN_OR_SEND_INTENT")
    require_space(Path(output.anchor))
    inputs = {key: strict_json(checked_bytes(root / name, digest)) for key, (name, digest) in ASSETS.items()}
    original = load_cells(root)
    verify_projection(root, original)
    cells, _ = refreeze(original)
    _check_wire(cells, inputs["plan"], inputs["sources"], inputs["outbound_scope"])
    host = _check_endpoint(root, inputs["endpoint"])
    return {
        "status": "OWNER12_RAPID_ADMISSION_VERIFIED",
        "source_commit": head, "source_file_sha256": source,
        "authority_sha256": OWNER_SHA, "scoped_waiver_sha256": WAIVER_SHA,
        "artifact_sha256": {key: digest for key, (_, digest) in ASSETS.items()},
        "output_path": str(output), "run_id": RUN_ID,
        "region": "cn-beijing", "model": MODEL, "request_grid_sha256": GRID_SHA,
        "slots": 108, "initial_checkpoint_slots": 3, "transport_retries": 0,
        "gates": {
            "A": "46_SOURCE_AND_EXACT_OUTBOUND_SCOPE_VERIFIED",
            "B": "SEALED_BEIJING_WORKSPACE_REUSED_OWNER_ATTESTED_ACCOUNT",
            "C": "C_RISK_ACCEPTED_OWNER12",
            "D": "OWNER_WAIVER_28_30_THIS_BATCH_ONLY_USAGE_AND_COST_TRACKED",
        },
        "current_all_streams_and_funding_verified": False,
        "usd_25_warning_status": "UNKNOWN_WITHOUT_CURRENT_UNIFIED_LEDGER",
        "public_price_basis": "https://help.aliyun.com/zh/model-studio/qwen3-7-plus",
        "single_overrun_reserve_cny_estimate": "8.4737664",
    }, cells, host
