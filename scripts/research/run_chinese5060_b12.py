"""Run unchanged public v0.2 on fixed role-free TopK; no evaluator imports."""
from __future__ import annotations

import argparse
import importlib.metadata
import json
import random
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from llmguard.domains.retrieval.hidden_poisoning.chinese5060.b12 import validate_packets, validate_removed
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.p2_runtime import file_hash, network_denied


def write(path: Path, obj: Any) -> None:
    path.write_bytes((json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--upstream", type=Path, required=True)
    args = parser.parse_args()
    if (args.run / "PAIR_OUTPUT_SEAL.json").exists():
        raise ValueError("NO_RERUN_OVERWRITE")
    upstream = subprocess.check_output(["git", "-C", str(args.upstream), "rev-parse", "HEAD"]).decode().strip()
    if upstream != "ba2a17efba165d45409114df2d70b030ade1e1b8" or subprocess.check_output(
            ["git", "-C", str(args.upstream), "status", "--porcelain"]).strip():
        raise ValueError("PINNED_CLEAN_UPSTREAM_REQUIRED")
    packets = json.loads((args.run / "PACKETS_PRIVATE.json").read_bytes())
    validate_packets(packets)
    paths = json.loads((args.run / "PRIVATE_PATHS.json").read_bytes())
    assets = json.loads((args.run / "ASSET_MANIFEST.json").read_bytes())
    for name in ("B1", "B2"):
        for row in assets[name + "_files"]:
            if file_hash(Path(paths[name]) / row["path"]) != row["sha256"]:
                raise ValueError("MODEL_FILE_CHANGED")
    write(args.run / "PAIR_PRE_EXECUTION_LOCK.json", {"source_commit": subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip(),
        "upstream_sha": upstream, "packets_sha256": file_hash(args.run / "PACKETS_PRIVATE.json"),
        "assets_sha256": file_hash(args.run / "ASSET_MANIFEST.json"), "single_hop": True, "p": 2, "m": 5,
        "seed": 0, "CPU_threads": 2, "order": "B1_ALL_SORTED_WORLDS_THEN_B2_ALL_SORTED_WORLDS",
        "encode_kwargs": "UPSTREAM_DEFAULT_CONVERT_TO_TENSOR_TRUE_NO_NORMALIZATION_OVERRIDE",
        "wall_cap_seconds": 1800, "model_load_kwargs": {"device": "cpu", "local_files_only": True, "trust_remote_code": False},
        "timing": "PER_DEFEND_CALL_WITH_READ_ONLY_PYTHON_PROFILE_OBSERVER_NO_WARMUP_NO_RETRY",
        "dependencies": {d.metadata["Name"]: d.version for d in importlib.metadata.distributions()}})
    events: list[str] = []
    results = {name: [{"world_id": p["world_id"], "status": "NOT_RUN"} for p in packets] for name in ("B1", "B2")}
    models_info: dict[str, Any] = {}
    started = time.perf_counter()
    hard_stop: str | None = None
    with network_denied(events):
        import numpy as np
        import torch
        from sentence_transformers import SentenceTransformer
        sys.path.insert(0, str(args.upstream.resolve()))
        from ragdefender import RAGDefender
        torch.set_num_threads(2)
        for name in ("B1", "B2"):
            if hard_stop:
                break
            random.seed(0)
            np.random.seed(0)
            torch.manual_seed(0)
            index = -1
            try:
                begin_load = time.perf_counter()
                model = SentenceTransformer(paths[name], device="cpu", local_files_only=True, trust_remote_code=False)
                models_info[name] = {"load_seconds": time.perf_counter() - begin_load,
                    "max_seq_length": model.max_seq_length, "dimension": model.get_embedding_dimension(),
                    "tokenizer_class": type(model.tokenizer).__name__, "tokenizer_is_fast": model.tokenizer.is_fast,
                    "modules": [type(x).__name__ for x in model], "all_input_encoder_tokens": []}
                defender = RAGDefender(embedder=model, task_type="single_hop", device="cpu", p=2, m=5)
                for index, packet in enumerate(packets):
                    if time.perf_counter() - started > 1800:
                        raise RuntimeError("WALL_CAP_STOP")
                    texts = [c["text"] for c in packet["chunks"]]
                    token_lengths = [len(model.tokenizer(t, truncation=False)["input_ids"]) for t in texts]
                    models_info[name]["all_input_encoder_tokens"].extend(token_lengths)
                    observations: dict[str, Any] = {"encode_calls": 0, "tie_policy": "UPSTREAM_STABLE_PAIR_ORDER_AND_LOWER_INDEX_SCORE_TIE"}

                    def observe(frame: Any, event: str, value: Any, encoder: Any = model,
                                clustering: Any = defender._clustering, identifier: Any = defender._identify) -> None:
                        owner = frame.f_locals.get("self")
                        fn = frame.f_code.co_name
                        if event == "call" and fn == "encode" and owner is encoder:
                            observations["encode_calls"] += 1
                        if event == "return" and owner is clustering and value is not None:
                            if fn == "estimate_n_adv":
                                observations["n_adv"] = int(value)
                            if fn == "_n_tfidf":
                                observations["n_tfidf"] = int(value)
                        if event == "return" and owner is identifier and fn == "select":
                            scores = frame.f_locals.get("f", [])
                            observations["frequency_scores"] = scores
                            observations["equal_frequency_score_pairs"] = sum(
                                scores[i] == scores[j] for i in range(len(scores)) for j in range(i + 1, len(scores)))
                    began = time.perf_counter()
                    try:
                        sys.setprofile(observe)
                        safe, removed = defender.defend(packet["query"], texts, return_indices=True)
                    finally:
                        sys.setprofile(None)
                    del observe
                    elapsed = time.perf_counter() - began
                    validate_removed(texts, safe, removed)
                    results[name][index] = {"world_id": packet["world_id"], "status": "PASS",
                        "snapshot_hash": packet["snapshot_hash"], "removed_indices": removed,
                        "retained_chunk_ids": [c["chunk_id"] for i, c in enumerate(packet["chunks"]) if i not in removed],
                        "removed_chunk_ids": [packet["chunks"][i]["chunk_id"] for i in removed],
                        "empty_context": not safe, "latency_seconds": elapsed, "observations": observations,
                        "encoder_token_lengths": token_lengths}
                    write(args.run / (name + "_RESULTS_PRIVATE.json"), results[name])
                del defender, model
            except Exception as exc:
                hard_stop = type(exc).__name__ + ": " + str(exc)
                if 0 <= index < len(packets):
                    results[name][index] = {"world_id": packets[index]["world_id"], "status": "FAILED", "error": hard_stop}
                import traceback
                (args.run / "FAILURE_TRACE_PRIVATE.txt").write_text(traceback.format_exc(), encoding="utf-8")
    for name in results:
        write(args.run / (name + "_RESULTS_PRIVATE.json"), results[name])
    write(args.run / "LOADED_MODELS_PRIVATE.json", models_info)
    write(args.run / "PAIR_STOP_STATE.json", {"hard_stop": hard_stop, "network_attempts": events,
        "wall_seconds": time.perf_counter() - started, "new_API_calls": 0})
    names = ["PACKETS_PRIVATE.json", "ASSET_MANIFEST.json", "PAIR_PRE_EXECUTION_LOCK.json", "B1_RESULTS_PRIVATE.json",
             "B2_RESULTS_PRIVATE.json", "LOADED_MODELS_PRIVATE.json", "PAIR_STOP_STATE.json"]
    write(args.run / "PAIR_OUTPUT_SEAL.json", {"worlds": 36, "outcomes": 72, "status": "SEALED_ALL_OUTCOMES",
        "records": [{"path": p, "sha256": file_hash(args.run / p)} for p in names], "network_attempts": events})
    print(json.dumps({"status": "SEALED", "hard_stop": hard_stop,
        "success": {k: sum(r["status"] == "PASS" for r in v) for k, v in results.items()}, "new_API_calls": 0}))


if __name__ == "__main__":
    main()
