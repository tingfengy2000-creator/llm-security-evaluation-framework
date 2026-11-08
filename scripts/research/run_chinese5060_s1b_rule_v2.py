"""Owner18 developer-only Rule-V2 replay of exactly the sealed, exposed S1 rows."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any
from zipfile import ZIP_DEFLATED, ZipFile

from llmguard.domains.retrieval.hidden_poisoning.chinese5060 import s1b_rule_v2 as rule

BRANCH = "research/paper1-chinese-defense-5060"
OWNER = "W1-OD-20261108-5060-S1B-RULEV2-DEV-18"
OWNER_COMMIT = "6561568584c05d12a7c9000933a46282ed0a565c"
RUN = "W1-5060-S1B-RULEV2-DEV-20261109-03"
OLD_RUN = "W1-5060-S1-CHINESE-EXTRACTION-20261108-01"
OLD_SOURCE = "68d34a5d877206f4e6d7d9e2bdda16784145a76a"
OLD_FILES = {
    "INFERENCE_PRIVATE.json": "8245af9a1241fe966f0dbc05e52ed7744b041e13685a743a81aebd818b9a8481",
    "ANNOTATION_PRIVATE.json": "2dcf3009d18b3cb09e1962b1517132cafe8fb992b25734923c58b57ea0e4dd24",
    "PREDICTIONS_PRIVATE.json": "2a2dda408a0ae914dc619c81f7bd738f11e9e7f1c427dd6493a677302ed1bbd7",
    "EVALUATION_PRIVATE.json": "b67b66398d8674c81664d3d160ea66889f3ce1c30f8960ee7b2405168b9be789",
    "RUN_MANIFEST.json": "9ba6097f448950c31ccdf4dbcf757d41c560c185033f7ea0b3e290cc5962249d",
    "S1_COMPLETE_AUDIT_PRIVATE.zip": "708c06264fdc2dd3678ad6ad5535d10c9e341646d335d646bfcb399d28d12d49",
}
OLD_SCORER = "scripts/research/run_chinese5060_s1_extraction.py"
OLD_SCORER_SHA = "5cedc9f3d11fba87d292961e37370439f6c3c58f78265b0ee2a515665e1d3fe1"
CLASS = ["EXPOSED_DEV_FIXTURES", "DEVELOPMENT_REUSE", "NOT_INDEPENDENT", "NOT_HUMAN_GOLD"]
NETWORK_EVENTS: list[str] = []


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read(path: Path, expected: str | None = None) -> bytes:
    if path.resolve(strict=True) != path:
        raise ValueError("NON_CANONICAL_PATH")
    raw = path.read_bytes()
    if expected is not None and sha(raw) != expected:
        raise ValueError("SEALED_INPUT_CHANGED")
    return raw


def write(path: Path, data: Any) -> str:
    content = (json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()
    with path.open("xb") as out:
        out.write(content)
    return sha(content)


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", *args], env={**os.environ, "GIT_NO_LAZY_FETCH": "1"})


def code() -> dict[str, Any]:
    if git("branch", "--show-current").decode().strip() != BRANCH or git("status", "--porcelain"):
        raise ValueError("FIXED_CLEAN_BRANCH_REQUIRED")
    base = Path(__file__).resolve().parents[2]
    impl = Path(rule.__file__).resolve()
    paths = (Path(__file__).resolve(), impl, impl.with_name("s1_extraction.py"),
             impl.with_name("vesa_guard_v02.py"), impl.with_name("vesa_guard_v01.py"))
    local = {p.relative_to(base).as_posix(): read(p) for p in paths}
    # Git text checkout on Windows may expand LF to CRLF. Verify canonical
    # source bytes against the committed blob and record raw worktree hashes too.
    files = {name: sha(raw.replace(b"\r\n", b"\n")) for name, raw in local.items()}
    for name in files:
        if files[name] != sha(git("show", f"HEAD:{name}")):
            raise ValueError("WORKTREE_BYTES_MISMATCH")
    for name in files:
        if name.endswith(("s1_extraction.py", "vesa_guard_v02.py", "vesa_guard_v01.py")):
            if files[name] != sha(git("show", f"{OLD_SOURCE}:{name}")):
                raise ValueError("HISTORICAL_RULE_CHANGED")
    if sha(git("show", f"HEAD:{OLD_SCORER}")) != OLD_SCORER_SHA:
        raise ValueError("HISTORICAL_SCORER_CHANGED")
    return {"source_commit": git("rev-parse", "HEAD").decode().strip(), "sources": files,
            "worktree_sources": {name: sha(raw) for name, raw in local.items()},
            "rule_config_sha256": rule.CONFIG_SHA256, "scorer_sha256": OLD_SCORER_SHA,
            "rule_policy": rule.POLICY, "schema": rule.SCHEMA}


def audit(stage: str, old: Path, out: Path) -> None:
    def guard(event: str, args: tuple[Any, ...]) -> None:
        if event.startswith("socket."):
            NETWORK_EVENTS.append(event)
            raise PermissionError("OWNER18_OFFLINE")
        if event == "open" and isinstance(args[0], (bytes, str)):
            path = Path(os.fsdecode(args[0])).resolve()
            if path.is_relative_to(old):
                allowed = {"INFERENCE_PRIVATE.json"} if stage == "predict" else OLD_FILES.keys()
                if path.parent != old or path.name not in allowed or args[2] & (os.O_WRONLY | os.O_RDWR):
                    raise PermissionError("OWNER18_HISTORICAL_READ_ALLOWLIST")
            if stage == "predict" and path.is_relative_to(out.parent) and path.parent != out and path.parent != old:
                raise PermissionError("OWNER18_OTHER_EVIDENCE_DENIED")
    sys.addaudithook(guard)


def inputs(old: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = json.loads(read(old / "INFERENCE_PRIVATE.json", OLD_FILES["INFERENCE_PRIVATE.json"]))
    if len(rows) != 73 or any(set(row) != {"id", "query", "evidence"} for row in rows):
        raise ValueError("OLD73_INPUT_SCHEMA")
    if len({row["id"] for row in rows}) != 73 or len({(row["query"], row["evidence"]) for row in rows}) != 73:
        raise ValueError("OLD73_DUPLICATE")
    return rows


def predict(old: Path, out: Path) -> None:
    frozen = write(out / "INPUT_LOCK.json", {
        "run_id": RUN, "owner": OWNER, "owner_commit": OWNER_COMMIT, "branch": BRANCH,
        "code": code(), "old_run_id": OLD_RUN, "inputs_sha256": OLD_FILES["INFERENCE_PRIVATE.json"],
        "class": CLASS, "total": 73, "network_denied": True, "input_fields": ["query", "evidence"],
    })
    predictions = []
    for case in inputs(old):
        result = rule.extract_one(case["query"], case["evidence"], rule.SCHEMA)
        if result != rule.extract_one(case["query"], case["evidence"], rule.SCHEMA):
            raise ValueError("NONDETERMINISTIC_RESULT")
        predictions.append({"id": case["id"], "prediction": result})
    checksum = write(out / "PREDICTIONS_PRIVATE.json", predictions)
    write(out / "PREDICTION_SEAL.json", {
        "run_id": RUN, "input_lock_sha256": frozen, "predictions_sha256": checksum,
        "deterministic_replay": len(predictions), "label_reads": 0, "network_events": NETWORK_EVENTS,
    })


def evaluate(old: Path, out: Path) -> None:
    seal = json.loads(read(out / "PREDICTION_SEAL.json"))
    lock = json.loads(read(out / "INPUT_LOCK.json", seal["input_lock_sha256"]))
    if lock["code"] != code() or lock["run_id"] != RUN or seal["deterministic_replay"] != 73:
        raise ValueError("EVALUATOR_IDENTITY_MISMATCH")
    predictions = json.loads(read(out / "PREDICTIONS_PRIVATE.json", seal["predictions_sha256"]))
    for name, checksum in OLD_FILES.items():
        read(old / name, checksum)
    cases = inputs(old)
    labels = json.loads(read(old / "ANNOTATION_PRIVATE.json", OLD_FILES["ANNOTATION_PRIVATE.json"]))
    old_predictions = json.loads(read(old / "PREDICTIONS_PRIVATE.json", OLD_FILES["PREDICTIONS_PRIVATE.json"]))
    historical = json.loads(read(old / "EVALUATION_PRIVATE.json", OLD_FILES["EVALUATION_PRIVATE.json"]))
    scorer = git("show", f"{OLD_SOURCE}:{OLD_SCORER}")
    if sha(scorer) != OLD_SCORER_SHA:
        raise ValueError("UNVERIFIED_SCORER")
    scoring: dict[str, Any] = {"__name__": "owner16_frozen_scoring"}
    exec(compile(scorer, OLD_SCORER, "exec"), scoring)
    compare, metrics = scoring["compare"], scoring["metrics"]
    rows = []
    for case, label, pred, prior, prior_row in zip(cases, labels, predictions, old_predictions, historical, strict=True):
        if len({row["id"] for row in (case, label, pred, prior, prior_row)}) != 1:
            raise ValueError("UNPAIRED_ROW")
        if compare(case, label, prior["prediction"]) != prior_row:
            raise ValueError("HISTORICAL_RECOMPUTATION_MISMATCH")
        rows.append(compare(case, label, pred["prediction"]))
    previous = metrics(historical)
    current = metrics(rows)
    if (previous["correct"], previous["wrong"], previous["unknown"], current["total"]) != (30, 4, 39, 73):
        raise ValueError("HISTORICAL_DENOMINATOR_MISMATCH")

    def by(field: str) -> dict[str, Any]:
        return {value: {"v1": metrics([r for r in historical if r[field] == value]),
                        "v2": metrics([r for r in rows if r[field] == value])}
                for value in sorted({r[field] for r in rows})}

    def status_counts(selected: list[dict[str, Any]]) -> dict[str, int]:
        return dict(Counter(r["status"] for r in selected))

    def pairs(observations: list[dict[str, Any]]) -> dict[str, int]:
        grouped: dict[str, dict[str, str]] = {}
        for row in observations:
            if row["pair"] is not None:
                grouped.setdefault(row["pair"], {})[row["form"]] = row["status"]
        if len(grouped) != 12:
            raise ValueError("HISTORICAL_PAIR_COUNT")
        return dict(Counter(p["explicit"] + "->" + p["natural"] for p in grouped.values()))

    checks: dict[str, list[dict[str, Any]]] = {}
    for before, after in zip(historical, rows, strict=True):
        if before["answerable"] and before["status"] == "UNKNOWN":
            checks.setdefault(before["unknown_reason"], []).append(after)
    cross_tab = dict(Counter(
        before["status"] + "->" + after["status"] for before, after in zip(historical, rows, strict=True)
    ))
    failures = Counter(
        error for before, after in zip(historical, rows, strict=True)
        if before["status"] != "INCORRECT" and after["status"] == "INCORRECT" for error in after["errors"]
    )
    evaluation_sha = write(out / "EVALUATION_PRIVATE.json", rows)
    summary = {
        **lock, "status": "RULE_V2_DEV_COMPLETED", "v1": previous, "v2": current, "paired_transitions": cross_tab,
        "semantic_cases": 61, "paired_views": 12, "by_form": by("form"), "by_category": by("category"),
        "v1_explicit_to_natural": pairs(historical), "v2_explicit_to_natural": pairs(rows),
        "old_answerable_unknown": {key: status_counts(value) for key, value in checks.items()},
        "old_wrong_followup": status_counts(
            [after for before, after in zip(historical, rows, strict=True) if before["status"] == "INCORRECT"]
        ),
        "new_wrong_types": dict(failures),
        "expected_unknown_by_category": {
            category: {"v1": status_counts([r for r in historical if r["category"] == category and not r["answerable"]]),
                       "v2": status_counts([r for r in rows if r["category"] == category and not r["answerable"]])}
            for category in sorted({r["category"] for r in rows if not r["answerable"]})
        },
        "old_artifacts_verified_sha256": OLD_FILES, "prediction_seal_sha256": sha(read(out / "PREDICTION_SEAL.json")),
        "predictions_sha256": seal["predictions_sha256"], "evaluation_sha256": evaluation_sha,
        "human_gold": 0, "independent_validation": "NOT_RUN", "formal_asr": "NOT_MEASURED",
        "formal_accuracy": "NOT_MEASURED", "model_downloads": 0, "wheel_downloads": 0, "installs": 0,
        "model_loads": 0, "model_calls": 0, "api_calls": 0, "cost_usd": 0,
        "network_events": NETWORK_EVENTS, "auto_continue": False,
    }
    write(out / "EVALUATION_AGGREGATE.json", summary)
    names = ("INPUT_LOCK.json", "PREDICTION_SEAL.json", "PREDICTIONS_PRIVATE.json", "EVALUATION_PRIVATE.json",
             "EVALUATION_AGGREGATE.json")
    members = {name: sha(read(out / name)) for name in names}
    archive = out / "OLD73_DEV_PRIVATE.zip"
    with ZipFile(archive, "x", compression=ZIP_DEFLATED) as bundle:
        for name in names:
            bundle.write(out / name, name)
    with ZipFile(archive) as bundle:
        if bundle.testzip() is not None or any(sha(bundle.read(n)) != digest for n, digest in members.items()):
            raise ValueError("PRIVATE_ARCHIVE_MISMATCH")
    for name, checksum in OLD_FILES.items():
        read(old / name, checksum)
    write(out / "RUN_MANIFEST.json", {**summary, "archive_sha256": sha(read(archive)), "members_sha256": members})
    print(json.dumps({"status": summary["status"], "total": len(rows), "v2": {
        key: current[key] for key in ("correct", "wrong", "unknown", "decided", "value_accuracy_answerable")}}))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("predict", "evaluate"))
    args = parser.parse_args()
    worktree = Path(__file__).resolve().parents[2]
    base = worktree.parent / "paper1-chinese-defense-5060" / "experiments" / "paper1_chinese5060"
    old, out = base / OLD_RUN, base / RUN
    if old.resolve(strict=True) != old or base.drive.upper() not in {"D:", "E:"}:
        raise ValueError("INVALID_D_E_EXPOSED_DATA_ROOT")
    audit(args.stage, old, out)
    if args.stage == "predict":
        out.mkdir(exist_ok=False)
    try:
        {"predict": predict, "evaluate": evaluate}[args.stage](old, out)
    except Exception as exc:
        write(out / f"STOP_{args.stage}.json", {"exception_type": type(exc).__name__,
              "status": "HUMAN_DECISION_REQUIRED", "auto_continue": False, "network_events": NETWORK_EVENTS})
        raise


if __name__ == "__main__":
    main()
