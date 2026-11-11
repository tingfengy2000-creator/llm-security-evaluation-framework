"""One-shot Owner33 DEV on frozen Owner27 TopK, using the existing replay helpers."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from itertools import combinations
import json
from pathlib import Path
from statistics import mean
from time import perf_counter_ns
from typing import Any
from zipfile import ZipFile

from llmguard.domains.retrieval.hidden_poisoning.chinese5060 import owner33_vcare as v
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.owner31_qcer import Query
from run_chinese5060_owner31_dev import (
    ARCHIVE,
    ARCHIVE_SHA,
    BASE,
    BASELINE,
    LABEL,
    checked,
    digest,
    fail_unless,
    guard,
    measure,
    write,
)

OLD_PROJECTION = BASE / "W1-5060-OWNER31-QCER-20261111-01" / "DEV_INPUT_PRIVATE.json"
PROJECTION_SHA = "f7e06c6b9c6b00df990e375bd8d2a67517f9447e6e40b87ca79bc45570d0125d"


def admitted(
    source: Path, expected: str
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    p = checked(OLD_PROJECTION.read_bytes(), PROJECTION_SHA)
    s = checked(source.read_bytes(), expected)
    fail_unless(
        s["schema"] == "OWNER33_DEV_OFFICIAL_FACT_INDEX_V0" and len(p) == 32, "SCHEMA"
    )
    rec = s["records"]
    active: Counter[str] = Counter()
    for row in p:
        match = v.lookup(rec, v.intent(Query(**row["query"])))
        if match:
            active[match["family"]] += 1
    fail_unless(len(active) >= 2, "SOURCE_INDEX_BLOCKED_STOP")
    return p, rec


def predict(
    run: Path, index: Path, freeze_path: Path, freeze_sha: str
) -> dict[str, Any]:
    f = checked(freeze_path.read_bytes(), freeze_sha)
    fail_unless(
        f["model_sha256"] == digest(Path(v.__file__).read_bytes())
        and f["runner_sha256"] == digest(Path(__file__).read_bytes())
        and f["config"] == v.CONFIG
        and f["input_sha256"] == PROJECTION_SHA,
        "CODE_OR_INPUT_DRIFT",
    )
    rows, records = admitted(index, f["index_sha256"])
    fail_unless(not run.exists(), "ATTEMPT_EXISTS")
    run.mkdir()
    write(run / "ATTEMPT_STARTED.json", {"freeze_sha256": freeze_sha})
    predictions = []
    for r in rows:
        b2, zh = tuple(r["b2"]), tuple(r["zh"])
        text = r["texts"]
        start = perf_counter_ns()
        intent = v.intent(Query(**r["query"]))
        state = v.trigger(intent, text, b2, zh)
        trigger_ns = perf_counter_ns() - start
        tick = perf_counter_ns()
        # Physically share one lookup. Charge each arm its full logical lookup cost.
        anchor = v.lookup(records, intent)
        lookup_ns = perf_counter_ns() - tick
        adaptive = int(state != "NOT_TRIGGERED")
        acts: dict[str, Any] = {}
        for arm, mask in zip(v.ARMS[:3], (tuple(range(5)), b2, zh), strict=True):
            acts[arm] = {
                "keep": mask,
                "ns": r["baseline_ns"].get(arm, 0),
                "lookups": 0,
                "evidence_id": None,
                "evidence_slots": len(mask),
                "context_bytes": v.budget(text, mask, None),
                "state": "HISTORICAL_MASK",
            }
        for arm, should_query, edit, preserve_scope, rescue in (
            (v.ARMS[3], adaptive, False, True, False),
            (v.ARMS[4], 1, True, True, False),
            (v.ARMS[5], adaptive, True, True, True),
            (v.ARMS[6], adaptive, True, False, True),
            (v.ARMS[7], adaptive, True, True, False),
        ):
            local_anchor = anchor if should_query else None
            tick = perf_counter_ns()
            out = v.verify(
                intent,
                text,
                b2,
                local_anchor,
                should_query,
                scope=preserve_scope,
                rescue=rescue,
                edit=edit,
            )
            context_bytes = v.budget(text, out.keep, local_anchor)
            local_ns = perf_counter_ns() - tick
            fail_unless(
                tuple(sorted(set(out.keep))) == out.keep
                and set(out.keep) <= set(range(5)),
                "INVALID_MASK",
            )
            acts[arm] = {
                "keep": out.keep,
                "codes": out.codes,
                "state": out.state,
                "evidence_id": out.evidence_id,
                "lookups": out.looked_up,
                "context_bytes": context_bytes,
                "extra_bytes": len(v.render_anchor(local_anchor).encode()),
                "evidence_slots": len(out.keep) + bool(local_anchor),
                "ns": local_ns
                + (lookup_ns if should_query else 0)
                + (trigger_ns if arm != v.ARMS[4] else 0),
            }
        matched, full = acts[v.ARMS[3]], acts[v.ARMS[5]]
        fail_unless(
            (matched["lookups"], matched["evidence_id"], matched["extra_bytes"])
            == (full["lookups"], full["evidence_id"], full["extra_bytes"]),
            "MATCHED_BUDGET_DRIFT",
        )
        predictions.append(
            {
                "world_id": r["world_id"],
                "packet_sha256": r["packet_sha256"],
                "trigger": state,
                "source_family": anchor["family"] if adaptive and anchor else None,
                "arms": acts,
            }
        )
    psha = write(run / "PREDICTIONS_PRIVATE.json", predictions)
    seal = {
        "worlds": 32,
        "predictions_sha256": psha,
        "freeze_sha256": freeze_sha,
        "index_sha256": f["index_sha256"],
        "original_topk_input_sha256": PROJECTION_SHA,
        "physical_lookup_calls_shared": len(rows),
        "new_embedding_calls": 0,
        "new_topk_queries": 0,
        "api_calls": 0,
    }
    return {**seal, "seal_sha256": write(run / "PREDICTION_SEAL.json", seal)}


def evaluate(run: Path, expected: str) -> dict[str, Any]:
    seal = checked((run / "PREDICTION_SEAL.json").read_bytes(), expected)
    pred = checked(
        (run / "PREDICTIONS_PRIVATE.json").read_bytes(), seal["predictions_sha256"]
    )
    fail_unless(
        seal["worlds"] == len(pred) == 32 and len({r["world_id"] for r in pred}) == 32,
        "DENOMINATOR",
    )
    fail_unless(digest(ARCHIVE.read_bytes()) == ARCHIVE_SHA, "ARCHIVE_DRIFT")
    scores: dict[str, dict[str, Counter[str]]] = {
        arm: defaultdict(Counter) for arm in v.ARMS
    }
    stats: dict[str, Counter[str]] = defaultdict(Counter)
    time: dict[str, list[int]] = defaultdict(list)
    paired: dict[str, Counter[str]] = defaultdict(Counter)
    outcomes: Counter[str] = Counter()
    actions: Counter[str] = Counter()
    failures = []
    with ZipFile(ARCHIVE) as z:
        gold = {
            r["world_id"]: r
            for r in checked(z.read("evaluator-only/labels.json"), LABEL)
            if r["partition"] == "main"
        }
        fail_unless(set(gold) == {r["world_id"] for r in pred}, "LABEL_ALIGNMENT")
        for row in pred:
            world = row["world_id"]
            label = gold[world]
            p = checked(z.read(f"evidence/{world}.json"), row["packet_sha256"])
            roles = [label["documents"][h["chunk"]["parent_doc_id"]] for h in p["topk"]]
            population = Counter(label["documents"].values())
            strata = (
                "ALL",
                "FACT:" + label["group"],
                "SCENE:" + label["scene"],
                f"DENSITY:{roles.count('P')}/5",
            )
            if row["source_family"]:
                outcomes["SOURCE_HIT:" + row["source_family"]] += 1
            outcomes[row["trigger"]] += 1
            for arm, a in row["arms"].items():
                for k in strata:
                    measure(roles, population, set(a["keep"]), scores[arm][k])
                time[arm].append(a["ns"])
                stats[arm].update(
                    {
                        "lookups": a["lookups"],
                        "evidence_hits": bool(a["evidence_id"]),
                        "extra_bytes": a.get("extra_bytes", 0),
                        "context_bytes": a["context_bytes"],
                        "slots": a["evidence_slots"],
                    }
                )
            b2 = set(row["arms"]["RD_B2"]["keep"])
            full = set(row["arms"]["VCARE_FULL"]["keep"])
            for i in b2 ^ full:
                action = "RESTORE" if i in full else "DROP"
                actions[f"{action}:{roles[i]}"] += 1
                if (action == "RESTORE" and roles[i] == "P") or (
                    action == "DROP" and roles[i] in "CH"
                ):
                    failures.append(
                        {
                            "world_id": world,
                            "rank": i + 1,
                            "action": action,
                            "role": roles[i],
                            "stratum": label["scene"],
                        }
                    )
            for a, b in combinations(v.ARMS, 2):
                before, after = (set(row["arms"][k]["keep"]) for k in (a, b))
                c = paired[f"{a}__{b}"]
                c["worlds_changed"] += before != after
                for i, role in enumerate(roles):
                    c[f"{role}_add"] += i in after - before
                    c[f"{role}_remove"] += i in before - after
    all_counts = {k: v0["ALL"] for k, v0 in scores.items()}
    baseline_counts = all_counts["RD_B2"]
    full_counts = all_counts["VCARE_FULL"]
    ctrl = all_counts["B2_SAME_EXTRA_RETRIEVAL"]
    fail_unless(
        all(baseline_counts[k] == BASELINE[k] for k in BASELINE), "BASELINE_DRIFT"
    )
    dev_delta = {k: baseline_counts[k] - full_counts[k] for k in BASELINE}
    matched_delta = {k: ctrl[k] - full_counts[k] for k in BASELINE}
    gates = {
        "non_inferior_P_C_HN": min(dev_delta.values()) >= 0,
        "minimum_vs_b2": dev_delta["P_retained"] >= 3 or dev_delta["C_deleted"] >= 5,
        "minimum_vs_matched": matched_delta["P_retained"] >= 2
        or matched_delta["C_deleted"] >= 3,
    }
    result = {
        "status": "DEV_GO" if all(gates.values()) else "METHOD_DEV_NO_GO",
        "gates": gates,
        "b2_delta": dev_delta,
        "matched_delta": matched_delta,
        "overall": all_counts,
        "scores": scores,
        "paired": paired,
        "actions": actions,
        "trigger_and_source": outcomes,
        "budgets": stats,
        "latency_ms": {
            k: {"mean": round(mean(t) / 1e6, 6), "p95": round(sorted(t)[30] / 1e6, 6)}
            for k, t in time.items()
        },
        "safety_failures": len(failures),
        "failures_sha256": write(run / "FAILURES_PRIVATE.json", failures),
        "prediction_seal_sha256": expected,
        "human_gold": 0,
    }
    score_sha = write(run / "SCORES.json", result)
    return {
        **{k: v0 for k, v0 in result.items() if k not in ("scores", "paired")},
        "scores_sha256": score_sha,
        "paired_b2_full": paired["RD_B2__VCARE_FULL"],
        "paired_full_no_scope": paired["VCARE_FULL__VCARE_NO_SCOPE"],
        "paired_full_no_rescue": paired["VCARE_FULL__VCARE_NO_RESCUE"],
    }


def main() -> None:
    a = argparse.ArgumentParser()
    a.add_argument("stage", choices=("check", "predict", "score"))
    a.add_argument("--root", type=Path, required=True)
    a.add_argument("--seal")
    a.add_argument("--version", choices=("v0", "v1"), default="v0")
    cfg = a.parse_args()
    root = cfg.root.resolve()
    fail_unless(
        root.drive.upper() == "D:" and root.is_relative_to(BASE.resolve()),
        "ROOT_NOT_PRIVATE",
    )
    guard(root if cfg.stage == "predict" else None)
    index = root / "SOURCE_INDEX_V0.json"
    run = root / cfg.version
    if cfg.stage == "check":
        p, records = admitted(index, digest(index.read_bytes()))
        valid = Counter(
            r["family"]
            for row in p
            if (r := v.lookup(records, v.intent(Query(**row["query"])))) is not None
        )
        report = {
            "status": "SOURCE_INDEX_ADMITTED_DEV",
            "worlds": len(p),
            "source_hits_by_family": valid,
            "records": len(records),
        }
    else:
        if cfg.seal is None:
            a.error("--seal required")
        report = (
            predict(run, index, root / f"FREEZE_{cfg.version.upper()}.json", cfg.seal)
            if cfg.stage == "predict"
            else evaluate(run, cfg.seal)
        )
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
