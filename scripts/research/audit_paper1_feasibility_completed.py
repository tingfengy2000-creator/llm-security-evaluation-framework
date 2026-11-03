"""Post-seal diagnostics and independent aggregate verification; no inference."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from decimal import Decimal
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from llmguard.domains.retrieval.hidden_poisoning.feasibility_sprint.api import write_new  # noqa: E402
from llmguard.domains.retrieval.hidden_poisoning.feasibility_sprint.contracts import F5_SHA, SLOTS, STATES, digest, grounded_ref, loads  # noqa: E402


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atom_issue(atom: Any, row: dict[str, Any]) -> str | None:
    if not isinstance(atom, dict) or set(atom) != {"id", "ref", "slots"} or not isinstance(atom["id"], str):
        return "ATOM_SCHEMA"
    if not grounded_ref(atom["ref"], row):
        return "UID_OR_EXACT_QUOTE_BINDING"
    if not isinstance(atom["slots"], dict) or set(atom["slots"]) != set(SLOTS):
        return "SLOT_SET_SCHEMA"
    for name, slot in atom["slots"].items():
        if not isinstance(slot, dict) or set(slot) != {"state", "value"}:
            return "SLOT_SCHEMA:" + name
        if slot["state"] not in STATES or not isinstance(slot["value"], str):
            return "SLOT_STATE_OR_TYPE:" + name
        if slot["state"] == "PRESENT" and (not slot["value"] or slot["value"] not in atom["ref"]["quote"]):
            return "PRESENT_VALUE_NOT_IN_ATOM_QUOTE:" + name
        if slot["state"] != "PRESENT" and slot["value"] != "":
            return "NON_PRESENT_VALUE_NOT_EMPTY:" + name
    return None


def audit(run: Path, runtime_path: Path, labels_path: Path) -> dict[str, Any]:
    predictions = loads((run / "PREDICTIONS.json").read_text("utf-8"))
    lock = loads((run / "PREDICTION_LOCK.json").read_text("utf-8"))
    if digest(predictions) != lock["prediction_sha256"] or len(predictions) != 480 or len(lock["raw_files"]) != 120:
        raise RuntimeError("FULL_SEAL_REQUIRED")
    for name, expected in lock["raw_files"].items():
        if Path(name).name != name or sha(run / "raw" / name) != expected:
            raise RuntimeError("RAW_SEAL_CHANGED")
    original_metrics_sha = sha(run / "EXPERIMENT_RESULTS.json")
    config = loads((run / "CONFIG_LOCK.json").read_text("utf-8"))
    if sha(runtime_path) != F5_SHA or sha(labels_path) != config["config"]["signed_label_file_sha256"]:
        raise RuntimeError("SIGNED_INPUT_OR_LABEL_IDENTITY")
    rows = {r["candidate_id"]: r for r in (loads(line) for line in runtime_path.read_text("utf-8").splitlines())}
    labels = {r["candidate_id"]: r for r in (loads(line) for line in labels_path.read_text("utf-8").splitlines())}
    metrics = loads((run / "EXPERIMENT_RESULTS.json").read_text("utf-8"))
    by_condition = {c: [p for p in predictions if p["condition"] == c] for c in ("E1", "E2", "E3", "E4")}
    independently_checked: dict[str, Any] = {}
    for condition, data in by_condition.items():
        assert len(data) == len({p["candidate_id"] for p in data}) == 120
        counts: dict[str, Any] = {}
        for name, selected in [("Recall", [p for p in data if labels[p["candidate_id"]]["label"] == 1]),
                               ("Clean_FPR", [p for p in data if labels[p["candidate_id"]]["role_evaluation_only"] == "CLEAN_CURRENT"]),
                               ("HN_FPR", [p for p in data if labels[p["candidate_id"]]["role_evaluation_only"] == "HARD_NEGATIVE"])]:
            n = sum(p["final_verdict"] == "CONTRADICT" for p in selected)
            assert n == metrics["conditions"][condition][name]["numerator"] and len(selected) == 40
            counts[name] = n
        assert sum(p["final_verdict"] == "INSUFFICIENT" for p in data) == metrics["conditions"][condition]["Abstention"]["numerator"]
        raw = Counter(labels[p["candidate_id"]]["role_evaluation_only"] + "_raw_CONTRADICT" for p in data if p["raw_model_verdict"] == "CONTRADICT")
        independently_checked[condition] = {"verified_main_counts": counts, "raw_verdict_diagnostic_only": dict(raw),
            "logical_CNY": str(sum(Decimal(rec["native_estimated_cost"]) for p in data for rec in p["call_records"])),
            "routes": dict(Counter(step for p in data for step in p["route_trace"]))}
    failures: dict[str, Any] = {}
    for kind, condition in (("internal", "E2"), ("structured", "E4")):
        primary: Counter[str] = Counter()
        overlaps: Counter[str] = Counter()
        raw_verdicts: Counter[str] = Counter()
        for p in by_condition[condition]:
            result = p["front_output"] if kind == "internal" else p
            obj = loads(result["raw_output"])
            raw_verdicts[str(obj.get("verdict"))] += 1
            bad = [issue for atom in obj.get("atoms", []) if (issue := atom_issue(atom, rows[p["candidate_id"]]))]
            primary[bad[0] if bad else "ATOMS_PASS_CONTRACT"] += 1
            overlaps.update(set(bad))
        failures[kind] = {"first_failure_partition": dict(primary), "overlapping_row_diagnostics": dict(overlaps), "raw_verdicts_diagnostic_only": dict(raw_verdicts)}
    assert original_metrics_sha == sha(run / "EXPERIMENT_RESULTS.json")
    return {"status": "POST_SEAL_AUDIT_PASS_NO_RESCORE", "main_metrics_sha256_unchanged": original_metrics_sha,
            "prediction_file_sha256": sha(run / "PREDICTIONS.json"), "independent_counts_and_logical_costs": independently_checked,
            "failure_partition": failures, "raw_diagnostics_are_not_repaired_scores": True}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--runtime-f5", type=Path, required=True)
    parser.add_argument("--labels", type=Path, required=True)
    args = parser.parse_args()
    value = audit(args.run_dir, args.runtime_f5, args.labels)
    write_new(args.run_dir / "POST_SEAL_AUDIT.json", value)
    print(json.dumps({"status": value["status"], "main_metrics_sha256": value["main_metrics_sha256_unchanged"]}))
