"""Fast-Track A T0 retrieval/B0 only; no evaluator, role, answer, or paid API access."""
from __future__ import annotations

import argparse
import importlib.metadata
import json
import os
import re
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any

from llmguard.domains.retrieval.hidden_poisoning.chinese5060.p2_runtime import (
    canonical_hits, chunk_world, file_hash, network_denied,
)
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.snapshots import digest


def write(path: Path, value: Any) -> None:
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()
    if not re.fullmatch(r"W1-5060-P2-[A-Z0-9-]+", args.run_id):
        raise ValueError("NEW_BOUNDED_RUN_REQUIRED")
    output = Path("experiments/paper1_chinese5060") / args.run_id
    output.mkdir(parents=True, exist_ok=False)
    if shutil.disk_usage(output).free < 2 * 1024**3:
        raise RuntimeError("INSUFFICIENT_DISK_HEADROOM")
    overall_started = time.perf_counter()
    os.environ.update(HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1", HF_HUB_DISABLE_TELEMETRY="1",
        ANONYMIZED_TELEMETRY="False", CUDA_VISIBLE_DEVICES="", TOKENIZERS_PARALLELISM="false")
    protocol = Path("docs/paper1/dual_machine/chinese5060/p1/P1_PROTOCOL_CANDIDATE.json")
    assert file_hash(protocol) == "6691273c5269ce52cb2c99629e3155daef38ebb36ccca01ae4402bc0cb22692c"
    prior = json.loads(Path("docs/research/stage6_1_hidden_knowledge_poisoning/core144/rag_defense_reconstruction_01/PAUSED_HANDOFF.json").read_text(encoding="utf-8"))["core_audit"]
    if args.model.name != "16e5344fbfc7dfbbbe0019d30cec21e2940cb4e1" or args.model.parent.parent.name != "models--sentence-transformers--paraphrase-multilingual-MiniLM-L12-v2":
        raise ValueError("MODEL_ID_REVISION_MISMATCH")
    if any(not (args.model / name).resolve().is_relative_to(args.model.parent.parent.resolve()) for name in prior["embedding_files_sha256"]):
        raise ValueError("MODEL_FILE_ESCAPES_PINNED_CACHE")
    files = {name: file_hash(args.model / name) for name in prior["embedding_files_sha256"]}
    if files != prior["embedding_files_sha256"]:
        raise ValueError("MODEL_BYTES_CHANGED")
    from llmguard.domains.retrieval.hidden_poisoning.chinese5060.d1_access import Binding, D1Reader
    # Custody checks only. Do not parse labels/roles in the frozen selection.
    custody = D1Reader(args.workspace)
    for key in ("selection", "bundle_manifest", "f5"):
        custody.read(key)
    index_path = Path("docs/paper1/dual_machine/chinese5060/p1/evidence/PRIVATE_EVIDENCE_INDEX.json")
    if file_hash(index_path) != "4995030167c2e37c4174428bcfaa9776ab7dc55a185421e44e1dcab9067cf5d4":
        raise ValueError("P1_WORLD_PIN_INDEX_CHANGED")
    entries = json.loads(index_path.read_text(encoding="utf-8"))["records"]
    pattern = r"W1-5060-P1-20261104-02-DESIGN/w-[0-9a-f]{24}\.json"
    admitted = [r for r in entries if re.fullmatch(pattern, r["path"])]
    if len(admitted) != 36:
        raise ValueError("EXACT_36_WORLD_FILES_REQUIRED")
    world_reader = D1Reader(Path.cwd(), {r["path"]: Binding("experiments/paper1_chinese5060/" + r["path"], r["sha256"]) for r in admitted})
    worlds = []
    for entry in admitted:
        world = json.loads(world_reader.read(entry["path"]))
        if len(world["documents"]) != 19 or world["trusted_registry"]:
            raise ValueError("FROZEN_T0_CORPUS_REQUIRED")
        worlds.append(world)
    model_hash = digest(files)
    deps = {d.metadata["Name"]: d.version for d in importlib.metadata.distributions()}
    execution_config = Path("docs/paper1/dual_machine/chinese5060/p2/P2_OFFLINE_EXECUTION_CONFIG_V1.json")
    frozen_config = json.loads(execution_config.read_text(encoding="utf-8"))
    if frozen_config["files_sha256"] != files or frozen_config["full_dependency_hash"] != digest(deps):
        raise ValueError("PREFLIGHT_MODEL_OR_DEPENDENCY_PIN_DRIFT")
    if importlib.metadata.version("chromadb") != "1.5.9" or importlib.metadata.version("sentence-transformers") != "5.6.0":
        raise ValueError("DEPENDENCY_DRIFT")
    default_ref = args.model.parent.parent.parent / "models--sentence-transformers--all-MiniLM-L6-v2/refs/main"
    baseline_status = {"B1": "BLOCKED_DEFAULT_PRECISE_REVISION_CACHE_NOT_PINNED",
        "B2": "BLOCKED_B1_PRECONDITION", "default_ref_exists": default_ref.is_file(),
        "cache_search_scope": "EXACT_DEFAULT_REFS_MAIN_ONLY_NO_MODEL_DIRECTORY_DISCOVERY"}
    write(output / "BASELINE_GATES.json", baseline_status)
    records: list[dict[str, Any]] = []
    events: list[str] = []
    vector_cache: dict[str, Any] = {}
    manifest = {"run_id": args.run_id, "source_sha": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "authorization_commit": "af68d89a870647be138cf5592ccd4a058e44a8ab", "authorization_id": "W1-OD-20261104-FAST-A-03",
        "protocol_sha256": file_hash(protocol), "world_input_files": admitted, "model_id": prior["embedding_id"],
        "execution_config_sha256": file_hash(execution_config),
        "authorization_file_sha256": file_hash(Path("docs/paper1/dual_machine/owner_approvals/W1_FAST_TRACK_A_OWNER_AUTHORIZATION_20261104.md")),
        "model_revision": args.model.name, "model_files_sha256": files, "model_aggregate_hash": model_hash,
        "dependencies": deps, "TopK": 5, "chunk_window": 96, "overlap": 16, "CPU_threads": 2,
        "normalize_embeddings": True, "embedding_batch_size": 16, "candidate_worlds": 36,
        "wall_time_cap_seconds": 1800, "new_run_disk_cap_bytes": 2 * 1024**3,
        "selection_sha256": "2c16fd6915c2dee377631d311ff33fe0ad36fdc8928a86e8fcabdcbca01cf689",
        "baseline_status": baseline_status, "all_model_inputs_label_free": True,
        "embedding_cache": "PURE_TEXT_HASH_TO_VECTOR_SAME_FROZEN_MODEL_NO_CORPUS_STATISTICS",
        "ASR": "NOT_MEASURED", "Answer_Accuracy": "NOT_MEASURED", "new_API_calls": 0}
    write(output / "PRE_EXECUTION_LOCK_PRIVATE.json", manifest)
    hard_stop_reason: str | None = None
    with network_denied(events):
        import torch
        torch.set_num_threads(2)
        from sentence_transformers import SentenceTransformer
        import chromadb
        from chromadb.config import Settings
        from llmguard.domains.retrieval.vectorstore.chroma_store import ChromaVectorStore
        from llmguard.domains.retrieval.vectorstore.models import VectorCollectionSpec, VectorDocument, VectorSearchQuery
        model = SentenceTransformer(str(args.model), device="cpu", local_files_only=True, trust_remote_code=False)
        if model.max_seq_length != 128 or model.get_embedding_dimension() != 384 or not model.tokenizer.is_fast:
            raise ValueError("ENCODER_TOKENIZER_IDENTITY_DRIFT")

        def embed(text: str) -> Any:
            key = digest(text)
            if key not in vector_cache:
                vector_cache[key] = model.encode([text], batch_size=16, device="cpu", normalize_embeddings=True,
                                                convert_to_numpy=True, show_progress_bar=False)[0]
            return vector_cache[key]

        for world in worlds:
            started = time.perf_counter()
            wid = world["world_id"]
            target = output / wid
            target.mkdir()
            try:
                query_tokens = len(model.tokenizer(world["query_text"], add_special_tokens=True, truncation=False)["input_ids"])
                if query_tokens > 128:
                    raise ValueError("QUERY_OVERFLOW_NO_TRUNCATION")
                chunks = chunk_world(world, model.tokenizer)
                if len(chunks) < 5:
                    raise ValueError("FEWER_THAN_FIVE_CHUNKS")
                if {c["parent_doc_id"] for c in chunks} != {d["document_id"] for d in world["documents"]}:
                    raise ValueError("DOCUMENT_OMITTED_DURING_CHUNKING")
                write(target / "CHUNKS_PRIVATE.json", chunks)
                spec = VectorCollectionSpec(fingerprint=digest({"corpus": world["corpus_hash"], "model": model_hash,
                    "chunk": [96, 16], "metric": "cosine"}), dimension=384)
                store = ChromaVectorStore(target / "index")
                try:
                    store.create_or_open_collection(spec)
                    store.upsert(spec, [VectorDocument(doc_id=c["chunk_id"], vector=embed(c["text"]).tolist(),
                        metadata={"doc_id": c["chunk_id"], "parent_doc_id": c["parent_doc_id"],
                                  "source_id": c["source_id"], "source_type": "UNVERIFIED", "content_hash": c["content_hash"],
                                  "corpus_snapshot_id": wid, "chunk_index": c["chunk_index"]},
                        content_hash=c["content_hash"], content_ref=f"chroma:{c['chunk_id']}") for c in chunks])
                    query_vector = embed(world["query_text"])
                    hits = canonical_hits(store.query(spec, VectorSearchQuery(vector=query_vector.tolist(), top_k=5)))
                    count = store.count(spec)
                    write(target / "QUERY_VECTOR_PRIVATE.json", {"vector": query_vector.tolist(), "dtype": str(query_vector.dtype),
                        "canonical_vector_hash": digest(query_vector.tolist())})
                finally:
                    store.close()
                reopened = ChromaVectorStore(target / "index")
                try:
                    reopened.create_or_open_collection(spec)
                    persisted_query = json.loads((target / "QUERY_VECTOR_PRIVATE.json").read_text(encoding="utf-8"))
                    if digest(persisted_query["vector"]) != persisted_query["canonical_vector_hash"]:
                        raise ValueError("PERSISTED_QUERY_VECTOR_CHANGED")
                    replay = canonical_hits(reopened.query(spec, VectorSearchQuery(vector=persisted_query["vector"], top_k=5)))
                    if reopened.count(spec) != count or hits != replay:
                        raise ValueError("PERSISTED_RANK_SCORE_OR_MEMBERSHIP_DRIFT")
                finally:
                    reopened.close()
                client: Any = chromadb.PersistentClient(path=str(target / "index"), settings=Settings(anonymized_telemetry=False))
                try:
                    collection = client.get_collection(spec.collection_name, embedding_function=None)
                    config = collection.configuration_json
                    members = collection.get(include=["metadatas"])
                    if set(members["ids"]) != {c["chunk_id"] for c in chunks}:
                        raise ValueError("INDEX_MEMBERSHIP_MISMATCH")
                finally:
                    client.close()
                expected_hnsw = {"space": "cosine", "ef_construction": 100, "ef_search": 100,
                                 "max_neighbors": 16, "resize_factor": 1.2, "sync_threshold": 1000}
                if config["hnsw"] != expected_hnsw:
                    raise ValueError("HNSW_DEFAULTS_DRIFT")
                snap = {"world_id": wid, "query_id": world["query_id"], "query_text": world["query_text"],
                    "query_hash": digest(world["query_text"]), "query_tokens": query_tokens,
                    "query_vector_hash": __import__("hashlib").sha256(query_vector.tobytes()).hexdigest(),
                    "corpus_hash": world["corpus_hash"], "index_member_hash": digest(sorted(members["ids"])),
                    "collection_fingerprint": spec.fingerprint, "collection_config": config,
                    "model_hash": model_hash, "TopK": 5, "hits": hits,
                    "B0_retained_chunk_ids": [h["chunk_id"] for h in hits], "B0_removed": [],
                    "reopen_rank_score_exact_match": True}
                snap["snapshot_hash"] = digest(snap)
                write(target / "TOPK_PRIVATE.json", snap)
                record = {"world_id": wid, "status": "PASS", "chunks": count, "TopK": len(hits),
                          "snapshot_hash": snap["snapshot_hash"], "seconds": time.perf_counter() - started}
            except Exception as exc:
                record = {"world_id": wid, "status": "FAILED", "exception": type(exc).__name__, "reason": str(exc),
                          "seconds": time.perf_counter() - started}
                write(target / "FAILURE.json", record)
            records.append(record)
            print(json.dumps(record, ensure_ascii=True), flush=True)
            if events or record.get("reason") in {"HNSW_DEFAULTS_DRIFT", "WORLD_CORPUS_CHANGED", "DOCUMENT_CHANGED", "T0_UNVERIFIED_ONLY", "INDEX_MEMBERSHIP_MISMATCH"}:
                hard_stop_reason = "NETWORK_FORBIDDEN" if events else record.get("reason")
                break
            if record.get("exception") in {"MemoryError", "OSError"}:
                hard_stop_reason = "RESOURCE_OR_FILESYSTEM_EXCEPTION"
                break
            if time.perf_counter() - overall_started > 1800 or sum(p.stat().st_size for p in output.rglob("*") if p.is_file()) > 2 * 1024**3:
                hard_stop_reason = "RESOURCE_CAP"
                break
    observed = {r["world_id"] for r in records}
    records.extend({"world_id": w["world_id"], "status": "NOT_STARTED_AFTER_HARD_STOP"} for w in worlds if w["world_id"] not in observed)
    write(output / "WORLD_RESULTS.json", records)
    write(output / "STOP_STATE.json", {"hard_stop_reason": hard_stop_reason, "network_attempts": events})
    if files != {name: file_hash(args.model / name) for name in files}:
        raise ValueError("MODEL_CHANGED_DURING_RUN")
    if events:
        raise RuntimeError("NETWORK_ATTEMPT_HARD_STOP")
    seal_records = [{"path": p.relative_to(output).as_posix(), "bytes": p.stat().st_size, "sha256": file_hash(p)}
                    for p in sorted(output.rglob("*")) if p.is_file()]
    write(output / "OUTPUT_SEAL.json", {"source_sha": manifest["source_sha"], "worlds": 36, "records": seal_records,
        "network_attempts": events, "status": "SEALED_ALL_WORLD_OUTCOMES", "evaluator_opened": False})
    print(json.dumps({"run_id": args.run_id, "worlds": 36, "success": sum(r["status"] == "PASS" for r in records),
                      "failed": sum(r["status"] != "PASS" for r in records), "API_calls": 0}), flush=True)


if __name__ == "__main__":
    main()
