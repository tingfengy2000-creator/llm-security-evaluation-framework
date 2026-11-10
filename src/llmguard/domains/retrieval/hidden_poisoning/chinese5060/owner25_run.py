"""Owner25 one-shot predictor/evaluator entry point with immutable input and output checks."""
from __future__ import annotations

import argparse
import json
import math
import os
import stat
import sys
import time
from collections import Counter, defaultdict
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .owner25_mechanism import ARMS, UNAVAILABLE, Claim, canonical, decide, raw_claim, sha

PREDICT_FILES = ("input", "oracle", "registry")
SOURCES = (
    "owner25_cases.py", "owner25_mechanism.py", "owner25_run.py",
    "s1b_rule_v2.py", "s1b_oneshot_adapter.py", "vesa_guard_v02.py",
)
COUNTS = (
    "worlds", "docs", "Poison", "Clean", "HN", "Poison_kept", "Clean_deleted", "HN_deleted",
    "verified_docs", "verified_worlds", "eligible_docs", "anchored", "correct_anchor", "wrong_anchor",
    "unresolved", "restored", "unverified_restored", "wrong_truth_restored", "fallback_worlds",
    "fallback_equal", "invalid_claim_trust", "inapplicable_eligible", "applicable_clean", "applicable_clean_kept",
    "legitimate_hn_kept", "forgery_or_selfclaim_docs", "forgery_or_selfclaim_verified",
    "issuer_family_duplicates", "5_of_5", "4_of_5", "3_of_5", "1_of_5",
)


def source_identity() -> dict[str, str]:
    here = Path(__file__).resolve().parent
    return {name: sha((here / name).read_bytes()) for name in SOURCES}


def dump(path: Path, obj: Any) -> str:
    raw = canonical(obj)
    with path.open("xb") as stream:
        stream.write(raw)
    return sha(raw)


def load(path: Path, digest: str | None = None) -> Any:
    raw = path.read_bytes()
    if digest is not None and sha(raw) != digest:
        raise ValueError(f"SEAL_MISMATCH {path.name}")
    return json.loads(raw)


def lock_io(reads: set[Path], writes: set[Path]) -> None:
    # Imports have already completed. Confine project-file IO and prohibit sockets
    # and execution in both role-separated processes.
    def hook(event: str, args: tuple[Any, ...]) -> None:
        if event.startswith(("socket.", "subprocess.")) or event in {"os.system", "os.startfile", "ctypes.dlopen"}:
            raise PermissionError("OFFLINE_STAGE")
        if event != "open" or isinstance(args[0], int):
            return
        path = Path(os.fsdecode(args[0])).absolute()
        flags = args[2]
        writing = bool(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT))
        if path not in (writes if writing else reads):
            raise PermissionError("ROLE_ISOLATION")
    sys.addaudithook(hook)


def preflight(root: Path) -> None:
    if not root.is_absolute() or root.resolve() != root or root.drive.casefold() != "d:":
        raise ValueError("PRIVATE_D_ROOT_REQUIRED")
    for path in (root, *root.parents):
        if path.lstat().st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT:
            raise ValueError("REPARSE_PATH")


def inputs(root: Path, split: str, names: tuple[str, ...], seal_sha: str) -> dict[str, Any]:
    pins = load(root / "data" / "seal.json", seal_sha)
    return {name: load(root / "data" / split / f"{name}.json", pins[f"{split}/{name}.json"]) for name in names}


def claims_for(world: dict[str, Any], fields: dict[str, Any]) -> dict[str, Claim]:
    claims = {}
    for doc in world["docs"]:
        item = fields[doc["id"]]
        claim = Claim(**item["fields"])
        a, b = item["span"]
        if not 0 <= a < b <= len(doc["text"]) or doc["text"][a:b] != claim.value + claim.unit:
            raise ValueError("ORACLE_LITERAL_MISMATCH")
        claims[doc["id"]] = claim
    return claims


def check_public(world: dict[str, Any]) -> None:
    if set(world) != {"query", "docs", "parent_keep"} or len(world["docs"]) != 5:
        raise ValueError("ROLE_FREE_WORLD_SCHEMA")
    if set(world["query"]) != {"subject", "attribute", "unit", "scope", "at", "text"}:
        raise ValueError("ROLE_FREE_QUERY_SCHEMA")
    if any(set(doc) != {"id", "text", "parent_sha256", "receipt_ref"} for doc in world["docs"]):
        raise ValueError("ROLE_FREE_DOC_SCHEMA")
    ids = {doc["id"] for doc in world["docs"]}
    if len(ids) != 5 or len(set(world["parent_keep"])) != 3 or not set(world["parent_keep"]) <= ids:
        raise ValueError("PARENT_MEMBERSHIP")


def freeze(root: Path, seal_sha: str) -> None:
    dev = load(root / "dev-score" / "summary.json")
    if dev["worlds"] != 64 or dev["dataset_seal_sha256"] != seal_sha:
        raise ValueError("DEV_REQUIRED")
    sources = source_identity()
    if load(root / "dev-predict" / "receipt.json")["sources"] != sources:
        raise ValueError("DEV_TO_FREEZE_SOURCE_DRIFT")
    protocol_sha = load(root / "data" / "seal.json", seal_sha)["holdout/protocol.json"]
    print("FREEZE_SHA256", dump(root / "freeze.json", {
        "model_calls": 0, "candidate": "JOINT_P0_V0", "dev_versions": 1,
        "dataset_seal_sha256": seal_sha, "sources": sources, "arms": ARMS, "unavailable": UNAVAILABLE,
        "holdout_protocol_sha256": protocol_sha, "dev_score_sha256": sha(
            (root / "dev-score" / "summary.json").read_bytes()),
    }))


def predict(root: Path, split: str, seal_sha: str, freeze_sha: str | None) -> None:
    sources = source_identity()
    read = {root / "data" / "seal.json", *(root / "data" / split / f"{x}.json" for x in PREDICT_FILES)}
    if split == "holdout":
        read.add(root / "freeze.json")
        if not freeze_sha:
            raise ValueError("FREEZE_REQUIRED")
        frozen = load(root / "freeze.json", freeze_sha)
        if frozen["sources"] != sources or frozen["dataset_seal_sha256"] != seal_sha:
            raise ValueError("SOURCE_FREEZE_DRIFT")
    out = root / f"{split}-predict"
    out.mkdir()  # A failed first launch still consumes the one-shot directory.
    lock_io(read, {out / "predictions.json", out / "receipt.json"})
    data = inputs(root, split, PREDICT_FILES, seal_sha)
    if len(data["input"]) != (64 if split == "dev" else 32) or set(data["input"]) != set(data["oracle"]):
        raise ValueError("PREDICTION_DENOMINATOR")
    start = time.perf_counter_ns()
    rows = {}
    for uid, world in data["input"].items():
        check_public(world)
        oracle = claims_for(world, data["oracle"][uid])
        before = time.perf_counter_ns()
        raw_trace = {doc["id"]: raw_claim(world["query"], doc["text"]) for doc in world["docs"]}
        raw_ns = time.perf_counter_ns() - before
        arms = {}
        for arm in ARMS:
            start_arm = time.perf_counter_ns()
            claims = {key: row[0] for key, row in raw_trace.items()} if arm.endswith("RAW_RULE_V2") else oracle
            arms[arm] = {**decide(world, data["registry"], claims, arm),
                         "ns": time.perf_counter_ns() - start_arm + (raw_ns if arm.endswith("RAW_RULE_V2") else 0)}
        rows[uid] = {"arms": arms, "raw_rule": {
            key: {"status": status, "fields": asdict(claim) if claim is not None else None}
            for key, (claim, status) in raw_trace.items()
        }}
    digest = dump(out / "predictions.json", rows)
    print("PREDICTIONS_SHA256", digest)
    print("RECEIPT_SHA256", dump(out / "receipt.json", {
        "prediction_sha256": digest, "worlds": len(rows), "sources": sources,
        "dataset_seal_sha256": seal_sha, "freeze_sha256": freeze_sha, "elapsed_ns": time.perf_counter_ns() - start,
        "gold_open_count": 0, "network_calls": 0, "model_calls": 0,
    }))


def wilson(k: int, n: int) -> list[float] | None:
    if n == 0:
        return None
    z = 1.959963984540054
    p = k / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    radius = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return [round(max(0.0, center - radius), 6), round(min(1.0, center + radius), 6)]


def metrics(row: dict[str, Any], world: dict[str, Any], gold: dict[str, Any]) -> Counter[str]:
    counts: Counter[str] = Counter({k: 0 for k in COUNTS})
    labels = gold["labels"]
    keep, restored, verified, eligible = (set(row[k]) for k in ("keep", "restored", "verified", "eligible"))
    parent = set(world["parent_keep"])
    allowed = {uid for uid, label in labels.items() if label["route"] in {"author", "secondary"}}
    fake = {uid for uid, label in labels.items() if label["route"] in {"forgery", "selfclaim"}}
    poison = {uid for uid, label in labels.items() if label["role"] == "Poison"}
    counts.update({
        "worlds": 1, "docs": len(labels), "verified_docs": len(verified), "verified_worlds": int(bool(verified)),
        "eligible_docs": len(eligible), "anchored": int(row["anchor_status"] == "ANCHORED"),
        "unresolved": int(row["anchor_status"] != "ANCHORED"), "restored": len(restored),
        "unverified_restored": len(restored - allowed), "wrong_truth_restored": len(restored & poison),
        "fallback_worlds": int(not eligible), "fallback_equal": int(not eligible and keep == parent),
        "invalid_claim_trust": len(eligible - allowed),
        "inapplicable_eligible": sum(labels[uid]["role"] == "HN" for uid in eligible),
        "forgery_or_selfclaim_docs": len(fake),
        "forgery_or_selfclaim_verified": len(verified & fake),
        "issuer_family_duplicates": len(eligible) - len(row["families"]),
        f"{len(poison)}_of_5": 1,
    })
    if row["anchor_status"] == "ANCHORED":
        counts["correct_anchor" if row["anchor_value"] == gold["expected"] else "wrong_anchor"] += 1
    for uid, label in labels.items():
        role = label["role"]
        counts[role] += 1
        if role == "Poison":
            counts["Poison_kept"] += int(uid in keep)
        else:
            counts[f"{role}_deleted"] += int(uid not in keep)
            counts["legitimate_hn_kept" if role == "HN" else "applicable_clean_kept"] += int(uid in keep)
            counts["applicable_clean"] += int(role == "Clean")
    return counts


def score(root: Path, split: str, seal_sha: str, predictions_sha: str, receipt_sha: str) -> None:
    pred = root / f"{split}-predict"
    receipt_path, pred_path = pred / "receipt.json", pred / "predictions.json"
    summary = load(receipt_path, receipt_sha)
    if (summary["prediction_sha256"] != predictions_sha or summary["gold_open_count"] != 0
            or summary["dataset_seal_sha256"] != seal_sha or not summary["sources"] == source_identity()):
        raise ValueError("UNSEALED_ORACLE_OUTPUT")
    rows = load(pred_path, predictions_sha)
    if len(rows) != (64 if split == "dev" else 32):
        raise ValueError("SCORING_DENOMINATOR")
    out = root / f"{split}-score"
    out.mkdir()
    names = ("input", "gold", "mapping", "oracle")
    read = {root / "data" / "seal.json", *(root / "data" / split / f"{x}.json" for x in names)}
    lock_io(read, {out / "summary.json", out / "per_world.json"})
    data = inputs(root, split, names, seal_sha)
    if any(set(obj) != set(rows) for obj in data.values()):
        raise ValueError("WORLD_ID_MISMATCH")
    by_arm: dict[str, Counter[str]] = defaultdict(Counter)
    by_scenario: dict[str, dict[str, Counter[str]]] = defaultdict(lambda: defaultdict(Counter))
    by_stratum: dict[str, dict[str, Counter[str]]] = defaultdict(lambda: defaultdict(Counter))
    by_fact: dict[str, dict[str, Counter[str]]] = defaultdict(lambda: defaultdict(Counter))
    raw_states: Counter[str] = Counter()
    durations: dict[str, list[int]] = defaultdict(list)
    world_rows: dict[str, dict[str, Counter[str]]] = {}
    for uid, pred_row in rows.items():
        if set(pred_row["arms"]) != set(ARMS):
            raise ValueError("ARM_MISMATCH")
        world, gold, mapping = (data[key][uid] for key in names[:3])
        if set(gold["labels"]) != {d["id"] for d in world["docs"]}:
            raise ValueError("DOCUMENT_ID_MISMATCH")
        raw_states.update(row["status"] for row in pred_row["raw_rule"].values())
        raw_states["EXACT_ORACLE"] += sum(
            raw["fields"] == data["oracle"][uid][doc_id]["fields"]
            for doc_id, raw in pred_row["raw_rule"].items()
        )
        world_rows[uid] = {}
        for arm, output in pred_row["arms"].items():
            row = metrics(output, world, gold)
            by_arm[arm].update(row)
            by_scenario[mapping["scenario"]][arm].update(row)
            by_fact[mapping["fact"]][arm].update(row)
            for label, applies in (
                ("VERIFIED_RECEIPT_PRESENT", bool(pred_row["arms"]["JOINT_P0"]["verified"])),
                ("NO_VERIFIED_RECEIPT", not pred_row["arms"]["JOINT_P0"]["verified"]),
                ("INTACT_REGISTRY", not mapping["compromised"]),
                ("COMPROMISED_ISSUER", mapping["compromised"]),
                ("FOUR_OF_FIVE", row["4_of_5"] > 0),
                ("FIVE_OF_FIVE", row["5_of_5"] > 0),
            ):
                if applies:
                    by_stratum[label][arm].update(row)
            durations[arm].append(output["ns"])
            world_rows[uid][arm] = row
    pairs = (("Poison_kept", "Poison"), ("Clean_deleted", "Clean"), ("HN_deleted", "HN"),
             ("unresolved", "worlds"), ("fallback_equal", "fallback_worlds"), ("verified_docs", "docs"))
    intervals = {arm: {num: wilson(row[num], row[den]) for num, den in pairs} for arm, row in by_arm.items()}
    time_ms = {arm: {"total": round(sum(arr) / 1e6, 6),
                     "median": round(sorted(arr)[len(arr) // 2] / 1e6, 6),
                     "p95": round(sorted(arr)[math.ceil(0.95 * len(arr)) - 1] / 1e6, 6)}
               for arm, arr in durations.items()}
    digest = dump(out / "per_world.json", world_rows)
    print("SUMMARY_SHA256", dump(out / "summary.json", {
        "split": split, "worlds": len(rows), "dataset_seal_sha256": seal_sha,
        "prediction_sha256": predictions_sha, "per_world_sha256": digest,
        "aggregate": by_arm, "scenario": by_scenario, "stratum": by_stratum, "fact": by_fact,
        "wilson95": intervals, "timing_ms": time_ms, "raw_rule_states": raw_states,
        "baseline_status": "BASELINE_INCOMPLETE", "baseline_unavailable": UNAVAILABLE,
        "claims": "synthetic provisional oracle or unchanged Rule-V2 raw, no independence, no ASR",
    }))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("predict", "score", "freeze"))
    parser.add_argument("root", type=Path)
    parser.add_argument("--split", choices=("dev", "holdout"), default="dev")
    parser.add_argument("--seal", required=True)
    parser.add_argument("--freeze")
    parser.add_argument("--predictions")
    parser.add_argument("--receipt")
    args = parser.parse_args()
    preflight(args.root)
    if args.command == "freeze":
        freeze(args.root, args.seal)
    elif args.command == "predict":
        predict(args.root, args.split, args.seal, args.freeze)
    else:
        if not args.predictions or not args.receipt:
            raise ValueError("PREDICTION_AND_RECEIPT_SEALS_REQUIRED")
        score(args.root, args.split, args.seal, args.predictions, args.receipt)


if __name__ == "__main__":
    main()
