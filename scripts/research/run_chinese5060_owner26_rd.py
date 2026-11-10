"""Replay both Owner26 Pilot12 RD baselines offline, then independently score."""
from __future__ import annotations

import argparse
import json
import random
import sys
import time
from collections import Counter
from pathlib import Path
from types import MethodType
from typing import Any

import run_chinese5060_r2_fairctrl as r2

from llmguard.domains.retrieval.hidden_poisoning.chinese5060.rd_zh_tfidf import adapt_clustering_source

RUN = "W1-5060-OWNER26-D1-RD7-DEV-20261110-01"
R2_RUN = "W1-5060-R2-FAIRCTRL-20261108-02"
R2_ROLE_FREE = "7240a44a6a8b5acbbc4628b48b49d69df80905567a6147128eaf9923d852177a"
LABELS_SHA = "0b75212782f4495037e27d56a2e480b01839e44b2143a8fe5845a1688c8a8ca3"
ARMS = ("RD_B2", "RD_ZH")


def run(base: Path, out: Path, upstream: Path) -> None:
    import numpy as np
    import torch
    from sentence_transformers import SentenceTransformer

    cache, identity = r2.cache_identity(base, upstream)
    packets, prior, input_id = r2.inputs(base)
    previous = r2.read(base / R2_RUN / "FOUR_ARM_ROLE_FREE_PRIVATE.json", R2_ROLE_FREE)
    sys.path.insert(0, str(upstream))
    from ragdefender import RAGDefender

    source = (upstream / "ragdefender/grouping/clustering.py").read_bytes()
    patch = adapt_clustering_source(source)
    scope: dict[str, Any] = {"__name__": "_owner26_rd_zh"}
    exec(compile(patch, "<pinned RD-zh Stage 1>", "exec"), scope)
    torch.set_num_threads(2)
    random.seed(0)
    np.random.seed(0)
    torch.manual_seed(0)
    lock = {
        "run_id": RUN, "source_sha256": r2.digest(Path(__file__).read_bytes()),
        "reuse_source_sha256": r2.digest(Path(r2.__file__).read_bytes()), "identity": identity, "inputs": input_id,
        "worlds": 36, "chunks": 180, "p": 2, "m": 5, "seed": 0, "cpu_threads": 2, "top_k": 5,
        "stage1_original_sha256": r2.digest(source), "stage1_rd_zh_sha256": r2.digest(patch),
    }
    lock_sha = r2.write(out / "RD_PRE_EXECUTION_LOCK.json", lock)
    model = SentenceTransformer(str(cache), device="cpu", local_files_only=True, trust_remote_code=False)
    defender = RAGDefender(embedder=model, task_type="single_hop", device="cpu", p=2, m=5)
    original = defender._clustering._n_tfidf
    char2 = MethodType(scope["ClusteringBasedGrouping"]._n_tfidf, defender._clustering)
    results: list[dict[str, Any]] = []
    for packet, old, old_r2 in zip(packets, prior, previous, strict=True):
        if (packet["world_id"], packet["snapshot_hash"]) != (old_r2["world_id"], old_r2["snapshot_hash"]):
            raise ValueError("R2_WORLD_ORDER_CHANGED")
        texts = [c["text"] for c in packet["chunks"]]
        start = time.perf_counter_ns()
        embedding = r2.model_vectors(model, texts)
        elapsed = time.perf_counter_ns() - start
        ehash = r2.digest(embedding.cpu().detach().numpy().tobytes())
        arms = {}
        for name, vote in zip(ARMS, (original, char2), strict=True):
            start = time.perf_counter_ns()
            arms[name] = {**r2.filter_one(defender, vote, texts, texts, embedding, ehash),
                          "filter_ns": time.perf_counter_ns() - start}
        row = {"world_id": packet["world_id"], "snapshot_hash": packet["snapshot_hash"], "arms": arms,
               "ordered_content_sha256": [c["content_hash"] for c in packet["chunks"]], "embedding_ns": elapsed}
        if (arms["RD_B2"]["deleted_indices"] != old["removed_indices"]
                or arms["RD_ZH"]["deleted_indices"] != old_r2["arms"]["RD_ZH_ONLY"]["deleted_indices"]):
            r2.write(out / "RD_REPLAY_FAILURE_PRIVATE.json", {"prefix": results, "failure": row})
            raise ValueError("HISTORICAL_RD_FILTER_DRIFT")
        results.append(row)
    if len(results) != 36 or r2.NETWORK:
        raise ValueError("DENOMINATOR_OR_NETWORK")
    result_sha = r2.write(out / "RD_ROLE_FREE_PRIVATE.json", results)
    seal_sha = r2.write(out / "RD_ROLE_FREE_SEAL.json", {
        "lock_sha256": lock_sha, "predictions_sha256": result_sha, "worlds": 36, "outcomes": 72,
        "encoder_calls": 36, "api_calls": 0, "denied_local_hostname_calls": len(r2.DENIED_LOCAL_HOSTNAME),
    })
    print(json.dumps({"worlds": 36, "predictions_sha256": result_sha, "seal_sha256": seal_sha}))


def percentile(values: list[int], num: int, den: int) -> float:
    return round(sorted(values)[(len(values) * num + den - 1) // den - 1] / 1e6, 6)


def evaluate(base: Path, out: Path, expected_seal: str) -> None:
    seal = r2.read(out / "RD_ROLE_FREE_SEAL.json", expected_seal)
    if (seal["worlds"], seal["outcomes"]) != (36, 72):
        raise ValueError("COMPLETE_PREDICTION_SEAL_REQUIRED")
    rows = r2.read(out / "RD_ROLE_FREE_PRIVATE.json", seal["predictions_sha256"])
    r2.read(out / "RD_PRE_EXECUTION_LOCK.json", seal["lock_sha256"])
    labels = {r["world_id"]: r for r in r2.read(base / r2.P2 / "EVALUATOR_ROWS_PRIVATE.json", LABELS_SHA)}
    if len(rows) != 36 or len(labels) != 36 or {r["world_id"] for r in rows} != set(labels):
        raise ValueError("PREDICTION_LABEL_WORLD_IDENTITY")
    report = {}
    for arm in ARMS:
        roles = {role: Counter[str]() for role in ("POISON", "CLEAN_CURRENT", "HARD_NEGATIVE")}
        other_removed, other = 0, 0
        for row in rows:
            label = labels[row["world_id"]]
            ranks = {r - 1 for r in label["candidate_ranks"]}
            deleted = set(row["arms"][arm]["deleted_indices"])
            roles[label["role_evaluation_only"]].update({
                "worlds": 1, "hit": int(bool(ranks)), "miss": int(not ranks), "retained": int(bool(ranks - deleted)),
                "removed_any": int(bool(ranks & deleted)), "removed_all": int(bool(ranks and ranks <= deleted)),
            })
            other_removed += len(deleted - ranks)
            other += 5 - len(ranks)
        if [c["hit"] for c in roles.values()] != [10, 10, 9]:
            raise ValueError("CANDIDATE_RECALL_DENOMINATOR_CHANGED")
        local_ns = [r["embedding_ns"] + r["arms"][arm]["filter_ns"] for r in rows]
        report[arm] = {"roles": roles, "worlds": 36, "chunks": 180, "other_chunks_deleted": other_removed,
                       "other_chunks": other, "median_ms": percentile(local_ns, 1, 2),
                       "p95_ms": percentile(local_ns, 95, 100)}
    aggregate = {"run_id": RUN, "pilot_only": True, "label_sha256": LABELS_SHA,
                 "role_free_seal_sha256": expected_seal, "prediction_sha256": seal["predictions_sha256"],
                 "arms": report, "changed_worlds_b2_to_zh": sum(
                     r["arms"]["RD_B2"]["deleted_indices"] != r["arms"]["RD_ZH"]["deleted_indices"] for r in rows
                 )}
    r2.write(out / "RD_EVALUATOR_AGGREGATE.json", aggregate)
    print(json.dumps(aggregate, ensure_ascii=False))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("predict", "evaluate"))
    for name in ("base", "out", "upstream"):
        parser.add_argument(f"--{name}", type=Path, required=True)
    parser.add_argument("--seal")
    args = parser.parse_args()
    if args.out.drive.upper() != "D:" or args.out.resolve() != args.out or not args.out.is_dir():
        raise ValueError("PRIVATE_OUTPUT_LOCATION")
    sys.addaudithook(r2.guard)
    if args.stage == "predict":
        sys.addaudithook(r2.deny_evaluator_labels)
        run(args.base, args.out, args.upstream)
    elif args.seal:
        evaluate(args.base, args.out, args.seal)
    else:
        raise ValueError("EVALUATOR_REQUIRES_PREDICTION_SEAL")


if __name__ == "__main__":
    main()
