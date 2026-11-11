"""Owner31 DEV replay, prediction, and evaluator phases with sealed file boundaries."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations
import json
import os
from pathlib import Path
import shutil
from statistics import mean
import sys
from time import perf_counter_ns
from typing import Any
from zipfile import ZipFile

import psutil  # type: ignore[import-untyped]

from llmguard.domains.retrieval.hidden_poisoning.chinese5060 import owner31_qcer as qcer

BASE = Path("experiments/paper1_chinese5060")
ARCHIVE = (
    BASE
    / "W1-5060-OWNER27-PUBLIC-VERSION-20261111-DEV-V0/OWNER27_OFFLINE_FASTTRACK_PRIVATE.zip"
)
ARCHIVE_SHA = "cc9051b64dccb5b9bcf57495ebfdf370d99c859708fe0b833707be5a65825d92"
TOPK = "c65c9e1e811a524fcafa35cec9e642aa91da8733c63c349745d53d642741f03f"
PRED = "b4cae321ef438a84f60c6239c327e8b68541a002cf298b6dbd24c688ce32cbcd"
QUERY = "705159cc4295478d257de383232517e9ce4e9b8d63687bcaa62faaaf20645544"
LABEL = "074a446425169c91ff32baee495d93b0f4185586d5701123fe14c2483cb6574f"
BASELINE = {"P_retained": 20, "C_deleted": 40, "H_deleted": 4}
ROLES = "PCHB"
ROOT = Path.cwd()


def fail_unless(ok: object, reason: str) -> None:
    if not ok:
        raise ValueError(reason)


def digest(raw: bytes) -> str:
    return sha256(raw).hexdigest()


def serialize(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()


def checked(raw: bytes, expected: str) -> Any:
    fail_unless(digest(raw) == expected, "SEALED_INPUT_SHA256_MISMATCH")
    return json.loads(raw)


def write(path: Path, value: Any) -> str:
    raw = serialize(value)
    with path.open("xb") as out:
        out.write(raw)
        out.flush()
        os.fsync(out.fileno())
    return digest(raw)


def guard(prediction_input: Path | None = None) -> None:
    archive_path = ARCHIVE.resolve()
    label_name = "evaluator-only"
    process = psutil.Process()
    process.cpu_affinity(process.cpu_affinity()[:2])
    fail_unless(len(process.cpu_affinity()) <= 2, "CPU_AFFINITY")
    fail_unless(shutil.disk_usage(BASE.resolve()).free >= 10 * 2**30, "FREE_DISK_GATE")

    def audit(event: str, args: tuple[Any, ...]) -> None:
        if event in {"socket.connect", "socket.getaddrinfo"}:
            raise PermissionError("NETWORK_DISABLED")
        if (
            prediction_input is not None
            and event == "open"
            and isinstance(args[0], (str, os.PathLike))
        ):
            path = Path(args[0]).resolve()
            if (
                path == archive_path
                or label_name in path.parts
                or path.name == "EVALUATION_PRIVATE.json"
            ):
                raise PermissionError("PREDICTION_CANNOT_READ_EVALUATION")

    sys.addaudithook(audit)


def prepare(target: Path) -> dict[str, Any]:
    fail_unless(not target.exists(), "OUTPUT_EXISTS")
    fail_unless(digest(ARCHIVE.read_bytes()) == ARCHIVE_SHA, "ARCHIVE_IDENTITY")
    with ZipFile(ARCHIVE) as z:
        topk = checked(z.read("evidence/topk-seal.json"), TOPK)
        pred_seal = checked(z.read("evidence/prediction-seal.json"), PRED)
        fail_unless(
            pred_seal["topk_sha256"] == TOPK and pred_seal["main"] == 32,
            "BASELINE_SEAL_BINDING",
        )
        preds = checked(
            z.read("evidence/predictions.json"), pred_seal["predictions_sha256"]
        )
        queries = checked(z.read("query-view/queries.json"), QUERY)
        # The split selector uses only the already frozen partition membership.
        # No evaluator labels or IDs other than the opaque world key enter prediction.
        partitions = {
            x["world_id"]: x["partition"]
            for x in checked(z.read("evaluator-only/labels.json"), LABEL)
        }
        by_pred = {x["world_id"]: x for x in preds}
        by_query = {x["world_id"]: x for x in queries}
        fail_unless(
            len(partitions)
            == len(by_pred)
            == len(by_query)
            == len(topk["packets"])
            == 40,
            "DEV_SOURCE_SIZE",
        )
        fail_unless(
            topk["metric"] == "cosine"
            and topk["top_k"] == 5
            and topk["reopen_exact"] == 40,
            "TOPK_CONFIG",
        )
        rows = []
        for member in topk["packets"]:
            world, sha = member["world_id"], member["packet_sha256"]
            if partitions[world] != "main":
                continue
            packet = checked(z.read(f"evidence/{world}.json"), sha)
            pred = by_pred[world]
            query = by_query[world]
            fail_unless(
                pred["packet_sha256"] == sha
                and packet["query"] == query["query"]
                and packet["event_date"] == query["event_date"]
                and packet["scope"] == query["scope"],
                "DEV_BINDING",
            )
            top = packet["topk"]
            fail_unless([hit["rank"] for hit in top] == list(range(1, 6)), "RANK_DRIFT")
            fail_unless(len(packet["members"]) == 11, "WORLD_MEMBER_COUNT")
            rows.append(
                {
                    "world_id": world,
                    "packet_sha256": sha,
                    "embedding_sha256": pred["embedding_sha256"],
                    "query": {
                        "text": query["query"],
                        **{
                            k: query[k]
                            for k in ("event_date", "scope", "subject", "ask")
                        },
                    },
                    "texts": [hit["chunk"]["text"] for hit in top],
                    "similarities": [hit["similarity"] for hit in top],
                    "b2": pred["arms"]["RD_B2"]["keep"],
                    "zh": pred["arms"]["RD_ZH"]["keep"],
                    "baseline_ns": {
                        arm: pred["arms"][arm]["ns"] for arm in ("RD_B2", "RD_ZH")
                    },
                    "baseline_embedding_ns": pred["embedding_ns"],
                }
            )
    fail_unless(
        len(rows) == 32 and len({r["world_id"] for r in rows}) == 32, "MAIN_PARTITION"
    )
    target.mkdir()
    seal = write(target / "DEV_INPUT_PRIVATE.json", rows)
    return {
        "input_sha256": seal,
        "worlds": len(rows),
        "owner27_archive_sha256": ARCHIVE_SHA,
        "topk_sha256": TOPK,
        "baseline_prediction_seal_sha256": PRED,
        "baseline_prediction_sha256": pred_seal["predictions_sha256"],
        "query_sha256": QUERY,
        "baseline_encoder_revision": "16e5344fbfc7dfbbbe0019d30cec21e2940cb4e1",
    }


def predict(target: Path, run: Path, freeze: Path, freeze_sha: str) -> dict[str, Any]:
    freeze_data = checked(freeze.read_bytes(), freeze_sha)
    fail_unless(
        freeze_data["module_sha256"] == digest(Path(qcer.__file__).read_bytes())
        and freeze_data["runner_sha256"] == digest(Path(__file__).read_bytes())
        and freeze_data["params"] == qcer.CONFIG,
        "CODE_OR_PARAMETER_DRIFT",
    )
    rows = checked(
        (target / "DEV_INPUT_PRIVATE.json").read_bytes(), freeze_data["input_sha256"]
    )
    fail_unless(len(rows) == 32 and not run.exists(), "ATTEMPT_EXISTS_OR_INPUT_DRIFT")
    run.mkdir()
    write(
        run / "ATTEMPT_STARTED.json",
        {"freeze_sha256": freeze_sha, "input_sha256": freeze_data["input_sha256"]},
    )
    result = []
    for row in rows:
        query = qcer.Query(**row["query"])
        texts, sim = row["texts"], row["similarities"]
        b2, zh = tuple(row["b2"]), tuple(row["zh"])
        outcomes: dict[str, Any] = {
            "NONE": {"keep": tuple(range(5)), "increment_ns": 0}
        }
        outcomes.update(
            {
                arm: {"keep": mask, "historical_ns": row["baseline_ns"][arm]}
                for arm, mask in (("RD_B2", b2), ("RD_ZH", zh))
            }
        )
        for arm, func in (
            (qcer.ARMS[3], lambda: qcer.query_control(query, texts, b2)),
            (qcer.ARMS[4], lambda: qcer.date_scope_control(query, texts, b2)),
            (qcer.ARMS[5], lambda: qcer.filter_world(query, texts, sim, b2, zh)),
            (
                qcer.ARMS[6],
                lambda: qcer.filter_world(query, texts, sim, b2, zh, preserve=False),
            ),
        ):
            start = perf_counter_ns()
            value = func()
            ns = perf_counter_ns() - start
            outcome = (
                {"keep": value, "increment_ns": ns}
                if not isinstance(value, qcer.Decision)
                else {
                    "keep": value.keep,
                    "codes": value.codes,
                    "sufficiency": value.sufficiency,
                    "increment_ns": ns,
                }
            )
            outcomes[arm] = outcome
        for outcome in outcomes.values():
            keep = outcome["keep"]
            fail_unless(
                tuple(sorted(set(keep))) == keep and set(keep) <= set(range(5)),
                "MASK_ORDER",
            )
        result.append(
            {
                "world_id": row["world_id"],
                "packet_sha256": row["packet_sha256"],
                "historical_embedding_ns": row["baseline_embedding_ns"],
                "arms": outcomes,
            }
        )
    pred_sha = write(run / "PREDICTIONS_PRIVATE.json", result)
    seal = {
        "worlds": len(result),
        "arms": list(qcer.ARMS),
        "predictions_sha256": pred_sha,
        "freeze_sha256": freeze_sha,
        "input_sha256": freeze_data["input_sha256"],
        "new_retrieval_calls": 0,
        "new_encoder_calls": 0,
        "commercial_api_calls": 0,
    }
    return {**seal, "prediction_seal_sha256": write(run / "PREDICTION_SEAL.json", seal)}


def measure(
    roles: list[str], population: Counter[str], kept: set[int], counter: Counter[str]
) -> None:
    for role in ROLES:
        ids = {i for i, r in enumerate(roles) if r == role}
        counter.update(
            {
                f"{role}_offered": population[role],
                f"{role}_retrieved": len(ids),
                f"{role}_missed": population[role] - len(ids),
                f"{role}_retained": len(ids & kept),
                f"{role}_deleted": len(ids - kept),
            }
        )
    counter["worlds"] += 1
    counter["empty"] += not kept


def evaluate(run: Path, pred_seal_sha: str) -> dict[str, Any]:
    fail_unless(not (run / "SCORES.json").exists(), "EVALUATION_EXISTS")
    seal = checked((run / "PREDICTION_SEAL.json").read_bytes(), pred_seal_sha)
    predictions = checked(
        (run / "PREDICTIONS_PRIVATE.json").read_bytes(), seal["predictions_sha256"]
    )
    fail_unless(
        seal["worlds"] == len(predictions) == 32
        and len({x["world_id"] for x in predictions}) == 32,
        "PREDICTIONS_NOT_SEALED",
    )
    fail_unless(digest(ARCHIVE.read_bytes()) == ARCHIVE_SHA, "ARCHIVE_IDENTITY")
    counts: dict[str, dict[str, Counter[str]]] = {
        a: defaultdict(Counter) for a in qcer.ARMS
    }
    paired: dict[str, Counter[str]] = defaultdict(Counter)
    changes = []
    times: dict[str, list[int]] = defaultdict(list)
    reasons: Counter[str] = Counter()
    status: Counter[str] = Counter()
    with ZipFile(ARCHIVE) as z:
        labels = {
            x["world_id"]: x
            for x in checked(z.read("evaluator-only/labels.json"), LABEL)
            if x["partition"] == "main"
        }
        fail_unless(
            set(labels) == {row["world_id"] for row in predictions}, "LABEL_JOIN"
        )
        for row in predictions:
            world = row["world_id"]
            packet = checked(z.read(f"evidence/{world}.json"), row["packet_sha256"])
            label = labels[world]
            roles = [
                label["documents"][x["chunk"]["parent_doc_id"]] for x in packet["topk"]
            ]
            pop = Counter(label["documents"].values())
            fail_unless(
                sum(pop.values()) == 11 and set(pop) <= set(ROLES), "ROLE_POPULATION"
            )
            strata = (
                "ALL",
                "FACT:" + label["group"],
                "SCENE:" + label["scene"],
                f"DENSITY:{roles.count('P')}/5",
            )
            b2 = set(row["arms"]["RD_B2"]["keep"])
            full = set(row["arms"]["Q_CER_FULL"]["keep"])
            status[row["arms"]["Q_CER_FULL"]["sufficiency"]] += 1
            for i in sorted(b2 ^ full):
                reason = row["arms"]["Q_CER_FULL"]["codes"][i]
                reasons[f"{reason}:{roles[i]}"] += 1
                changes.append(
                    {
                        "world_id": world,
                        "rank": i + 1,
                        "role": roles[i],
                        "scene": label["scene"],
                        "fact": label["group"],
                        "action": "RESTORE" if i in full else "ISOLATE",
                        "reason": reason,
                    }
                )
            for arm, value in row["arms"].items():
                times[arm].append(
                    value.get("increment_ns", value.get("historical_ns", 0))
                )
                for stratum in strata:
                    measure(roles, pop, set(value["keep"]), counts[arm][stratum])
            for a, b in combinations(qcer.ARMS, 2):
                left, right = set(row["arms"][a]["keep"]), set(row["arms"][b]["keep"])
                stats = paired[f"{a}__{b}"]
                stats["worlds_changed"] += left != right
                for i, role in enumerate(roles):
                    stats[f"{role}_added"] += i in right - left
                    stats[f"{role}_removed"] += i in left - right
    original = counts["RD_B2"]["ALL"]
    result = counts["Q_CER_FULL"]["ALL"]
    fail_unless(all(original[k] == v for k, v in BASELINE.items()), "BASELINE_MISMATCH")
    improvements = {k: original[k] - result[k] for k in BASELINE}
    gate = min(improvements.values()) >= 0 and (
        improvements["P_retained"] >= 2 or improvements["C_deleted"] >= 3
    )
    fail_unless(
        all(counts[a]["ALL"]["worlds"] == 32 for a in qcer.ARMS), "SCORE_DENOMINATOR"
    )
    private_sha = write(run / "CHANGES_PRIVATE.json", changes)
    metrics = {
        "status": "DEV_PASS" if gate else "METHOD_DEV_NO_GO",
        "gate_pass": gate,
        "improvement_counts": improvements,
        "worlds": 32,
        "fact_groups": 4,
        "slots": 160,
        "scores": counts,
        "paired": paired,
        "reason_counts": reasons,
        "sufficiency": status,
        "latency_ms": {
            a: {"mean": round(mean(t) / 1e6, 6), "p95": round(sorted(t)[30] / 1e6, 6)}
            for a, t in times.items()
        },
        "private_changes_sha256": private_sha,
        "prediction_seal_sha256": pred_seal_sha,
        "labels_sha256": LABEL,
        "human_gold": 0,
    }
    score_sha = write(run / "SCORES.json", metrics)
    return {**metrics, "scores_sha256": score_sha}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=("prepare", "predict", "score"))
    parser.add_argument("--target", required=True, type=Path)
    parser.add_argument("--run", type=Path)
    parser.add_argument("--freeze", type=Path)
    parser.add_argument("--seal-sha")
    a = parser.parse_args()
    fail_unless(
        a.target.resolve().is_relative_to(BASE.resolve())
        and BASE.resolve().drive.upper() == "D:",
        "PRIVATE_D_PATH",
    )
    fail_unless(
        a.run is None or a.run.resolve().is_relative_to(a.target.resolve()), "RUN_PATH"
    )
    guard(a.target if a.phase == "predict" else None)
    if a.phase == "prepare":
        out = prepare(a.target)
    elif a.phase == "predict":
        if a.run is None or a.freeze is None or a.seal_sha is None:
            parser.error("prediction arguments")
        out = predict(a.target, a.run, a.freeze, a.seal_sha)
    else:
        if a.run is None or a.seal_sha is None:
            parser.error("scoring arguments")
        result = evaluate(a.run, a.seal_sha)
        out = {k: v for k, v in result.items() if k != "scores"}
        out["overall"] = {
            arm: values["ALL"] for arm, values in result["scores"].items()
        }
    print(json.dumps(out, sort_keys=True))


if __name__ == "__main__":
    main()
