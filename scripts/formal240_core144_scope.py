"""Create an additive three-domain Core144 view of the frozen Formal240 slots."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


FORMAL240_MATRIX_SHA = "54a98bc8d8a16dfbd90cebeffbf37743f4bcc7cf96c6b60416177274ab08ac14"
ACTIVE = ("D1", "D2", "D3")
DEFERRED = ("D4", "D5")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def build(raw: bytes) -> tuple[bytes, dict[str, Any]]:
    if sha(raw) != FORMAL240_MATRIX_SHA:
        raise ValueError("frozen Formal240 matrix SHA256 mismatch")
    lines = raw.decode("utf-8").splitlines(keepends=True)
    rows = [json.loads(line) for line in lines if line.strip()]
    if len(rows) != 240 or len(lines) != 240:
        raise ValueError("Formal240 matrix must contain 240 nonblank lines")
    counts = Counter(row["domain"] for row in rows)
    if {domain: counts[domain] for domain in (*ACTIVE, *DEFERRED)} != dict.fromkeys((*ACTIVE, *DEFERRED), 48):
        raise ValueError("Formal240 domain allocation drift")
    ids = [row["group_slot_id"] for row in rows]
    if len(set(ids)) != 240:
        raise ValueError("duplicate Formal240 group slot")
    kept_lines = [line for line, row in zip(lines, rows) if row["domain"] in ACTIVE]
    kept = [row for row in rows if row["domain"] in ACTIVE]
    if len(kept) != 144:
        raise ValueError("Core144 group count mismatch")
    for domain in ACTIVE:
        domain_rows = [row for row in kept if row["domain"] == domain]
        if len(domain_rows) != 48:
            raise ValueError(f"{domain} group count mismatch")
        hkp = Counter(row["hkp"] for row in domain_rows)
        stealth = Counter(row["target_stealth_design"] for row in domain_rows)
        if {f"HKP{i}": hkp[f"HKP{i}"] for i in range(1, 5)} != dict.fromkeys((f"HKP{i}" for i in range(1, 5)), 12):
            raise ValueError(f"{domain} HKP allocation mismatch")
        if {f"S{i}": stealth[f"S{i}"] for i in range(1, 4)} != dict.fromkeys((f"S{i}" for i in range(1, 4)), 16):
            raise ValueError(f"{domain} stealth allocation mismatch")
        for h in range(1, 5):
            for s in range(1, 4):
                chains = {row["chain_slot"] for row in domain_rows if row["hkp"] == f"HKP{h}" and row["target_stealth_design"] == f"S{s}"}
                if chains != {1, 2, 3, 4}:
                    raise ValueError(f"{domain}/HKP{h}/S{s} chain allocation mismatch")
    view = "".join(kept_lines).encode("utf-8")
    if [json.loads(line)["group_slot_id"] for line in view.decode("utf-8").splitlines()] != [row["group_slot_id"] for row in kept]:
        raise ValueError("Core144 slot identity drift")
    selection = {
        "status": "PAPER1_CORE144_SCOPE_FROZEN",
        "decision_date": "2026-09-27",
        "historical_formal240_matrix_sha256": FORMAL240_MATRIX_SHA,
        "core144_group_matrix_view_sha256": sha(view),
        "view_semantics": "EXACT_LINE_SUBSET_OF_FROZEN_FORMAL240_MATRIX; historical slot_status values are retained, not current construction state",
        "active_domains": list(ACTIVE),
        "deferred_external_extension_domains": list(DEFERRED),
        "domain_status": {**dict.fromkeys(ACTIVE, "CORE_ACTIVE"), **dict.fromkeys(DEFERRED, "DEFERRED_EXTERNAL_EXTENSION")},
        "group_count": 144,
        "candidate_count_planned": 432,
        "groups_per_domain": 48,
        "candidates_per_domain_planned": 144,
        "groups_per_domain_hkp": 12,
        "groups_per_domain_target_s": 16,
        "future_split_seed": 20260922,
        "future_group_split": {"train": 72, "dev": 36, "test": 36},
        "future_candidate_split": {"train": 216, "dev": 108, "test": 108},
        "split_executed": False,
        "ground_truth_created_by_scope_amendment": False,
        "training_started": False,
    }
    return view, selection


def write_new(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(raw)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix", required=True, type=Path)
    parser.add_argument("--view", required=True, type=Path)
    parser.add_argument("--selection", required=True, type=Path)
    args = parser.parse_args()
    view, selection = build(args.matrix.read_bytes())
    if args.view.exists() or args.selection.exists():
        raise ValueError("refusing to overwrite Core144 artifacts")
    write_new(args.view, view)
    write_new(args.selection, (json.dumps(selection, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    print(json.dumps({"view_sha256": sha(view), "selection": selection}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
