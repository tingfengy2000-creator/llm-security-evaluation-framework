"""Owner16 S1 staged synthetic evaluation. Prediction and evaluation are separate processes."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any
from zipfile import ZIP_DEFLATED, ZipFile

from llmguard.domains.retrieval.hidden_poisoning.chinese5060 import s1_extraction as s1

RUN = "W1-5060-S1-CHINESE-EXTRACTION-20261108-01"
OWNER = "W1-OD-20261108-5060-S1-OFFLINE-16"
OWNER_COMMIT = "7186762"
BRANCH = "research/paper1-chinese-defense-5060"
CLASS = ["AI_AUTHORED", "NOT_HUMAN_INDEPENDENT", "SEALED_SYNTHETIC_DEVELOPMENT", "PROVISIONAL"]
MIN_TOTAL = 60
MIN_VALUE_ACCURACY = 0.90
MAX_WRONG_DECIDED = 0.02
POLICY = {"min_total": MIN_TOTAL, "answerable_value_accuracy": MIN_VALUE_ACCURACY,
          "max_wrong_decided": MAX_WRONG_DECIDED,
          "unknown_counts_as_value_correct": False, "offset": "zero-based Unicode code points, end exclusive"}
FIELDS = {
    "VALUE_UNIT": ("value", "unit"),
    "SUBJECT_ATTRIBUTE": ("subject", "attribute"),
    "TIME_VERSION_SCOPE": ("version", "effective_from", "effective_to", "condition", "scope",
                           "negation", "exception", "qualifier"),
}
NETWORK: list[str] = []


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read(path: Path, expected: str | None = None) -> Any:
    if path.resolve() != path:
        raise ValueError("NON_CANONICAL_PATH")
    raw = path.read_bytes()
    if expected is not None and sha(raw) != expected:
        raise ValueError("SEALED_INPUT_MISMATCH")
    return json.loads(raw)


def write(path: Path, value: Any) -> str:
    raw = canonical(value)
    with path.open("xb") as out:
        out.write(raw)
    return sha(raw)


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True,
                                   env={**os.environ, "GIT_NO_LAZY_FETCH": "1"}).strip()


def guard(event: str, _args: tuple[Any, ...]) -> None:
    if event.startswith("socket."):
        NETWORK.append(event)
        raise PermissionError("OWNER16_OFFLINE")


def label_guard(root: Path) -> Any:
    def audit(event: str, args: tuple[Any, ...]) -> None:
        if event == "open" and isinstance(args[0], (str, bytes)):
            path = Path(os.fsdecode(args[0])).resolve()
            if path.is_relative_to(root) and path not in {
                root / "INFERENCE_PRIVATE.json", root / "INPUT_LOCK.json", root / "PREDICTIONS_PRIVATE.json",
                root / "PREDICTION_SEAL.json", root / "STOP_predict.json",
            }:
                raise PermissionError("S1_PREDICTOR_PRIVATE_PATH_DENIED")
    return audit


def code_id() -> dict[str, Any]:
    if git("branch", "--show-current") != BRANCH or git("status", "--porcelain"):
        raise ValueError("CLEAN_FIXED_SOURCE_REQUIRED")
    tracked = [Path(__file__), Path(s1.__file__), Path(s1.v02.__file__)]
    return {"source_commit": git("rev-parse", "HEAD"),
            "owner_commit": git("rev-parse", OWNER_COMMIT),
            "sources": {p.name: sha(p.read_bytes()) for p in tracked},
            "extractor_policy": s1.POLICY, "underlying_rule_sha256": s1.v02.RULE_SHA}


def lock(root: Path) -> None:
    inf = root / "INFERENCE_PRIVATE.json"
    ann = root / "ANNOTATION_PRIVATE.json"
    cases, labels = read(inf), read(ann)
    if len(cases) < MIN_TOTAL or len(cases) != len(labels):
        raise ValueError("INSUFFICIENT_SYNTHETIC_SAMPLES")
    if len({(c["query"], c["evidence"]) for c in cases}) != len(cases):
        raise ValueError("DUPLICATE_QUERY_EVIDENCE")
    if len({c["id"] for c in cases}) != len(cases):
        raise ValueError("DUPLICATE_ID")
    pairs: dict[str, list[Any]] = {}
    for case, label in zip(cases, labels, strict=True):
        if set(case) != {"id", "query", "evidence"} or case["id"] != label["id"]:
            raise ValueError("INFERENCE_SCHEMA_OR_MAPPING")
        gold = label["fact"]
        anchor = label["anchor"]
        begin, end = label["span"]
        if case["evidence"][begin:end] != anchor or not 0 <= begin < end <= len(case["evidence"]):
            raise ValueError("LABEL_SOURCE_SPAN_INVALID")
        if gold is not None and set(gold) != {k for group in FIELDS.values() for k in group}:
            raise ValueError("LABEL_SCHEMA")
        if label["pair"] is not None:
            pairs.setdefault(label["pair"], []).append((case, label))
    for pair in pairs.values():
        if len(pair) != 2:
            raise ValueError("PAIR_COUNT")
        (a, x), (b, y) = pair
        if a["query"] != b["query"] or x["fact"] != y["fact"] or {x["form"], y["form"]} != {"natural", "explicit"}:
            raise ValueError("PAIR_CHANGED_MEANING")
    write(root / "INPUT_LOCK.json", {"run_id": RUN, "owner": OWNER, "branch": BRANCH,
          "code": code_id(), "policy": POLICY, "policy_sha256": sha(canonical(POLICY)),
          "inference_sha256": sha(inf.read_bytes()), "annotation_sha256": sha(ann.read_bytes()),
          "total": len(cases), "pairs": len(pairs), "data_class": CLASS, "source": "LOCALLY_FICTIONAL",
          "risk_review": {"forward": "role-free view, isolated labels, fail-closed, prior assets untouched",
                          "paper": "synthetic development only; abstention separate; pair dependence explicit"}})


def predict(root: Path) -> None:
    # The lock carries label identity only, and the audit hook denies opening other private files.
    sys.addaudithook(label_guard(root))
    frozen = read(root / "INPUT_LOCK.json")
    if frozen["code"] != code_id():
        raise ValueError("FROZEN_CODE_CHANGED")
    cases = read(root / "INFERENCE_PRIVATE.json", frozen["inference_sha256"])
    rows = []
    for case in cases:
        if set(case) != {"id", "query", "evidence"}:
            raise ValueError("PREDICTOR_INPUT_SCHEMA")
        result = s1.extract_one(case["query"], case["evidence"])
        if result != s1.extract_one(case["query"], case["evidence"]):
            raise ValueError("NONDETERMINISTIC_EXTRACTION")
        rows.append({"id": case["id"], "prediction": result})
    if NETWORK:
        raise ValueError("NETWORK_EVENT")
    checksum = write(root / "PREDICTIONS_PRIVATE.json", rows)
    write(root / "PREDICTION_SEAL.json", {"run_id": RUN, "total": len(rows), "predictions_sha256": checksum,
          "input_lock_sha256": sha((root / "INPUT_LOCK.json").read_bytes()), "deterministic_replay": len(rows),
          "label_reads": 0, "model_calls": 0, "api_calls": 0, "network_events": []})


def wilson(num: int, den: int) -> dict[str, Any]:
    if not den:
        return {"n": num, "d": den, "estimate": None, "wilson95": None}
    z = 1.959963984540054
    p = num / den
    scale = 1 + z*z / den
    mid = (p + z*z / (2*den)) / scale
    delta = z * math.sqrt(p*(1-p)/den + z*z/(4*den*den)) / scale
    return {"n": num, "d": den, "estimate": p, "wilson95": [max(0.0, mid-delta), min(1.0, mid+delta)]}


def compare(case: dict[str, Any], label: dict[str, Any], pred: dict[str, Any]) -> dict[str, Any]:
    gold = label["fact"]
    errors = []
    decided = pred["status"] == "DECIDED"
    value_exact = gold is not None and decided and pred["value"] == gold["value"]
    if decided and gold is None:
        errors.append("UNSUPPORTED_ANSWER")
    if decided and gold is not None:
        errors.extend(kind for kind, fields in FIELDS.items() if any(pred[k] != gold[k] for k in fields))
        begin, end = label["span"]
        span = pred["source_span"]
        if not 0 <= span["start"] <= begin < end <= span["end"] <= len(case["evidence"]):
            errors.append("SOURCE_SPAN")
    return {"id": case["id"], "category": label["category"], "form": label["form"], "pair": label["pair"],
            "answerable": gold is not None, "value_exact": value_exact, "status": (
                "UNKNOWN" if not decided else "INCORRECT" if errors else "CORRECT"),
            "errors": errors, "unknown_reason": pred.get("reason"), "annotation_reason": label.get("reason")}


def metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    n = len(rows)
    states = Counter(r["status"] for r in rows)
    errors = Counter(e for r in rows for e in r["errors"])
    unknown = states["UNKNOWN"]
    decided = n - unknown
    correct, wrong = states["CORRECT"], states["INCORRECT"]
    answerable = sum(r["answerable"] for r in rows)
    decided_answerable = sum(r["answerable"] and r["status"] != "UNKNOWN" for r in rows)
    value_exact = sum(r["value_exact"] for r in rows)
    return {"total": n, "answerable": answerable, "decided": decided, "correct": correct, "wrong": wrong,
            "unknown": unknown, "expected_unknown": n-answerable,
            "appropriate_unknown": sum(not r["answerable"] and r["status"] == "UNKNOWN" for r in rows),
            "missed_answerable": sum(r["answerable"] and r["status"] == "UNKNOWN" for r in rows),
            "wrong_total": wilson(wrong, n), "wrong_decided": wilson(wrong, decided),
            "coverage": wilson(decided, n), "abstention": wilson(unknown, n),
            "strict_correct_total": wilson(correct, n), "strict_correct_decided": wilson(correct, decided),
            "value_accuracy_answerable": wilson(value_exact, answerable),
            "value_accuracy_decided_answerable": wilson(value_exact, decided_answerable),
            "value_accuracy_total": wilson(value_exact, n),
            "error_types": {k: {"per_total": wilson(errors[k], n), "per_decided": wilson(errors[k], decided)}
                            for k in (*FIELDS, "SOURCE_SPAN", "UNSUPPORTED_ANSWER")},
            "unknown_reasons": dict(Counter(r["unknown_reason"] for r in rows if r["status"] == "UNKNOWN"))}


def evaluate(root: Path) -> None:
    seal = read(root / "PREDICTION_SEAL.json")
    frozen = read(root / "INPUT_LOCK.json", seal["input_lock_sha256"])
    if frozen["code"] != code_id():
        raise ValueError("EVALUATION_CODE_DRIFT")
    cases = read(root / "INFERENCE_PRIVATE.json", frozen["inference_sha256"])
    preds = read(root / "PREDICTIONS_PRIVATE.json", seal["predictions_sha256"])
    labels = read(root / "ANNOTATION_PRIVATE.json", frozen["annotation_sha256"])
    rows = []
    pairs: dict[str, dict[str, Any]] = {}
    for case, label, pred in zip(cases, labels, preds, strict=True):
        if case["id"] != label["id"] or case["id"] != pred["id"]:
            raise ValueError("EVALUATOR_ID_MISMATCH")
        row = compare(case, label, pred["prediction"])
        rows.append(row)
        if row["pair"] is not None:
            pairs.setdefault(row["pair"], {})[row["form"]] = row
    overall = metrics(rows)
    passing = (overall["total"] >= MIN_TOTAL and overall["decided"] > 0
               and overall["value_accuracy_answerable"]["estimate"] >= MIN_VALUE_ACCURACY
               and overall["wrong_decided"]["estimate"] <= MAX_WRONG_DECIDED)
    report = {"run_id": RUN, "status": "S1_DEV_OFFLINE_GATE_PASS" if passing else "S1_FAIL_STOP",
              "overall": overall, "by_category": {k: metrics([r for r in rows if r["category"] == k])
                  for k in sorted({r["category"] for r in rows})},
              "by_form": {k: metrics([r for r in rows if r["form"] == k]) for k in ("explicit", "natural")},
              "paired_forms": {k: metrics([p[k] for p in pairs.values()]) for k in ("explicit", "natural")},
              "paired_transitions": dict(Counter(p["explicit"]["status"] + "->" + p["natural"]["status"]
                                               for p in pairs.values())),
              "data_class": CLASS, "human_gold": 0, "api_calls": 0, "model_calls": 0, "downloads": 0,
              "cost_usd": 0, "formal_asr": "NOT_MEASURED", "formal_accuracy": "NOT_MEASURED", "auto_continue": False}
    score = write(root / "EVALUATION_PRIVATE.json", rows)
    public = write(root / "EVALUATION_AGGREGATE.json", report)
    write(root / "EVALUATOR_SEAL.json", {"prediction_seal_sha256": sha((root / "PREDICTION_SEAL.json").read_bytes()),
          "evaluation_sha256": score, "aggregate_sha256": public, "labels_sha256": frozen["annotation_sha256"]})
    names = ("INFERENCE_PRIVATE.json", "ANNOTATION_PRIVATE.json", "INPUT_LOCK.json", "PREDICTIONS_PRIVATE.json",
             "PREDICTION_SEAL.json", "EVALUATION_PRIVATE.json", "EVALUATION_AGGREGATE.json", "EVALUATOR_SEAL.json")
    archive = root / "S1_PRIVATE_EVIDENCE.zip"
    with ZipFile(archive, "x", compression=ZIP_DEFLATED) as zip_file:
        for name in names:
            zip_file.write(root / name, name)
    with ZipFile(archive) as zip_file:
        if zip_file.testzip() is not None or any(zip_file.read(n) != (root / n).read_bytes() for n in names):
            raise ValueError("EVIDENCE_ARCHIVE_CORRUPTION")
    write(root / "RUN_MANIFEST.json", {**frozen, **report, "members_sha256": {
          n: sha((root / n).read_bytes()) for n in names}, "archive_sha256": sha(archive.read_bytes())})
    print(json.dumps({"status": report["status"], "total": len(rows), "decided": overall["decided"],
                      "archive_sha256": sha(archive.read_bytes())}))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("lock", "predict", "evaluate"))
    parser.add_argument("--run", type=Path, required=True)
    args = parser.parse_args()
    root = args.run.resolve(strict=True)
    if root.drive.upper() not in {"D:", "E:"} or root.name != RUN:
        raise ValueError("S1_PRIVATE_ROOT")
    sys.addaudithook(guard)
    try:
        {"lock": lock, "predict": predict, "evaluate": evaluate}[args.stage](root)
    except Exception as exc:
        write(root / f"STOP_{args.stage}.json", {"status": "HUMAN_DECISION_REQUIRED", "auto_continue": False,
              "exception_type": type(exc).__name__, "network_events": NETWORK})
        raise


if __name__ == "__main__":
    main()
