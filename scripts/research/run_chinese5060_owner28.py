"""Owner28 fixed four-arm blind runner. Fixtures never invoke a real encoder."""

from __future__ import annotations

import argparse
import ctypes
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from types import MethodType
from typing import Any

from llmguard.domains.retrieval.hidden_poisoning.chinese5060.owner28_benchmark import (
    ARMS, AUTHORITY, assemble_masks, parse_json, sha, validate_curator, validate_payload, write_once,
)
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.p2_runtime import canonical_hits, chunk_world, file_hash
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.rd_zh_tfidf import adapt_clustering_source
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.snapshots import digest

BASE_IDENTITY = {
    "model": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    "revision": "16e5344fbfc7dfbbbe0019d30cec21e2940cb4e1",
    "upstream": "ba2a17efba165d45409114df2d70b030ade1e1b8",
    "cache_identity_sha256": "53a3935d8d35d377fb90f839604f42062c944641dd15f7ad081b0ca557f638e5",
    "dependency_sha256": "25ceec7b87f616eea4295108827671e90d78ce64627c1323012e9c38cd9ccef7", "cache_files": 10,
}
SUPPORT_SHA = "9a0ed59eb79fb127ac73310ecd1f55b287415b4711c050d786f0e5ada28b9fae"
BRANCH = "research/paper1-chinese-defense-5060"
CURATOR_BRANCH = "refs/remotes/origin/research/paper1-ragdefender-repro-5090"
SOURCES = ("scripts/research/run_chinese5060_owner28.py",
           "src/llmguard/domains/retrieval/hidden_poisoning/chinese5060/owner28_benchmark.py",
           "src/llmguard/domains/retrieval/hidden_poisoning/chinese5060/owner27_version_guard.py")


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", *args], env={**os.environ, "GIT_NO_LAZY_FETCH": "1"})


def offline_guard(event: str, args: tuple[Any, ...]) -> None:
    if event == "socket.gethostname":
        return
    if event.startswith("socket."):
        raise PermissionError("OWNER28_NO_NETWORK")
    if event == "open" and isinstance(args[0], (str, bytes)):
        path = Path(os.fsdecode(args[0]))
        if path.name.casefold() in {"eval_label_custody.json", "evaluator_rows_private.json", "labels.json"} or (
            {"evaluator-only", "gt_vault", "d2", "d3", "hold8"} & {p.casefold() for p in path.parts}
        ):
            raise PermissionError("EVALUATION_CUSTODY_DENIED")


def configure(out: Path) -> None:
    if out.resolve() != out or out.drive.upper() != "D:" or not out.is_dir():
        raise ValueError("EXISTING_D_OUTPUT_REQUIRED")
    if shutil.disk_usage(out).free < 10 * 1024**3:
        raise ValueError("DISK_HEADROOM")
    for key in ("TEMP", "TMP", "HF_HOME", "XDG_CACHE_HOME", "TORCH_HOME", "NUMBA_CACHE_DIR", "MPLCONFIGDIR"):
        os.environ[key] = str(out)
    for key in ("HF_HUB_OFFLINE", "TRANSFORMERS_OFFLINE", "HF_HUB_DISABLE_TELEMETRY", "DO_NOT_TRACK"):
        os.environ[key] = "1"
    for key in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS", "RAYON_NUM_THREADS"):
        os.environ[key] = "2"
    os.environ.update(CUDA_VISIBLE_DEVICES="-1", ANONYMIZED_TELEMETRY="False", TOKENIZERS_PARALLELISM="false", GIT_NO_LAZY_FETCH="1")
    sys.addaudithook(offline_guard)


def check_freeze(commit: str) -> dict[str, str]:
    if not re.fullmatch("[0-9a-f]{40}", commit):
        raise ValueError("CODE_COMMIT_REQUIRED")
    if git("rev-parse", "HEAD").decode().strip() != commit or git("branch", "--show-current").decode().strip() != BRANCH:
        raise ValueError("FROZEN_BRANCH_AND_HEAD_REQUIRED")
    git("merge-base", "--is-ancestor", commit, "refs/remotes/origin/" + BRANCH)
    if git("status", "--porcelain"):
        raise ValueError("CLEAN_FROZEN_SOURCE_REQUIRED")
    blobs = {}
    for path in SOURCES:
        file = Path(path)
        blob = git("show", f"{commit}:{path}")
        if file.read_bytes().replace(b"\r\n", b"\n") != blob:
            raise ValueError("EXECUTED_SOURCE_DIFFERS_FROM_GIT")
        blobs[path] = sha(blob)
    return blobs


def admit(args: Any) -> tuple[list[Any], dict[str, Any]]:
    code = check_freeze(args.code_commit)
    if not re.fullmatch("[0-9a-f]{40}", args.curator_commit):
        raise ValueError("CURATOR_COMMIT_REQUIRED")
    path = args.curator_git_path
    if (not path.startswith("docs/paper1/dual_machine/repro5090/") or not path.endswith(".json")
            or ".." in Path(path).parts or "label" in path.lower()):
        raise ValueError("CURATOR_GIT_METADATA_PATH")
    subprocess.run(["git", "merge-base", "--is-ancestor", args.curator_commit, CURATOR_BRANCH], check=True)
    raw_manifest = git("show", f"{args.curator_commit}:{path}")
    if sha(raw_manifest) != args.curator_sha256:
        raise ValueError("CURATOR_GIT_BLOB_SHA")
    raw = args.input.read_bytes()
    if sha(raw) != args.input_sha256:
        raise ValueError("ROLE_FREE_BYTES_CHANGED")
    payload = parse_json(raw)
    worlds = validate_payload(payload)
    curator = parse_json(raw_manifest)
    validate_curator(curator, args.input_sha256, len(payload["mirrors"]))
    if {w["fact_uid"] for w in payload["main"]} != {x["fact_uid"] for x in curator["source_audits"]}:
        raise ValueError("CURATOR_FACT_ALLOCATION")
    gate = {
        "authority": AUTHORITY, "status": "ROLE_FREE_G1_G2_ADMITTED_AGENT_PROVISIONAL",
        "role_free_sha256": args.input_sha256, "curator_manifest_sha256": args.curator_sha256,
        "curator_git_commit": args.curator_commit, "curator_git_path": path,
        "private_custody_sha256": curator["private_custody_sha256"], "custody_file_read": False,
        "code_commit": args.code_commit, "code_blobs_sha256": code, "model_identity": BASE_IDENTITY,
        "main_worlds": 32, "mirror_worlds": len(payload["mirrors"]),
        "provenance": "GIT_BOUND_5090_ATTESTATION; NOT_A_CRYPTOGRAPHIC_ISSUER_SIGNATURE",
    }
    return worlds, gate


def asset_identity(args: Any) -> tuple[Any, Any]:
    if any(getattr(args, flag) is None for flag in ("assets", "upstream", "support")):
        raise ValueError("PINNED_BACKEND_PATHS_REQUIRED")
    if file_hash(args.support) != SUPPORT_SHA:
        raise ValueError("R2_ADAPTER_HASH")
    sys.path.insert(0, str(args.support.parent))
    import run_chinese5060_r2_fairctrl as r2

    cache, identity = r2.cache_identity(args.assets, args.upstream)
    if identity != BASE_IDENTITY:
        raise ValueError("ENCODER_OR_ENV_DRIFT")
    return cache, r2


def pinned_backend(args: Any) -> tuple[Any, Any]:
    cache, r2 = asset_identity(args)
    sys.path.insert(0, str(args.upstream))
    import numpy as np
    import torch
    from ragdefender import RAGDefender
    from sentence_transformers import SentenceTransformer

    torch.set_num_threads(2)
    torch.set_num_interop_threads(2)
    np.random.seed(0)
    torch.manual_seed(0)
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.GetProcessAffinityMask.argtypes = (
        ctypes.c_void_p, ctypes.POINTER(ctypes.c_size_t), ctypes.POINTER(ctypes.c_size_t),
    )
    kernel.SetProcessAffinityMask.argtypes = (ctypes.c_void_p, ctypes.c_size_t)
    process = kernel.GetCurrentProcess()
    allowed, system = ctypes.c_size_t(), ctypes.c_size_t()
    if not kernel.GetProcessAffinityMask(process, ctypes.byref(allowed), ctypes.byref(system)):
        raise ctypes.WinError(ctypes.get_last_error())
    bits = [1 << i for i in range(allowed.value.bit_length()) if (1 << i) & allowed.value]
    if not kernel.SetProcessAffinityMask(process, sum(bits[:2])):
        raise ctypes.WinError(ctypes.get_last_error())
    model = SentenceTransformer(str(cache), device="cpu", local_files_only=True, trust_remote_code=False)
    if model.max_seq_length != 128 or model.get_embedding_dimension() != 384 or not model.tokenizer.is_fast:
        raise ValueError("ENCODER_TOKENIZER_IDENTITY")
    defender = RAGDefender(embedder=model, task_type="single_hop", device="cpu", p=2, m=5)
    source = (args.upstream / "ragdefender/grouping/clustering.py").read_bytes()
    scope: dict[str, Any] = {"__name__": "_owner28_fixed_rd_zh"}
    exec(compile(adapt_clustering_source(source), "<Owner28 fixed RD-zh>", "exec"), scope)
    return (model, defender, defender._clustering._n_tfidf,
            MethodType(scope["ClusteringBasedGrouping"]._n_tfidf, defender._clustering)), r2


def build_topk(world: dict[str, Any], model: Any, out: Path, vectors: dict[str, Any]) -> dict[str, Any]:
    import chromadb
    import numpy as np
    from chromadb.config import Settings

    from llmguard.domains.retrieval.vectorstore.chroma_store import ChromaVectorStore
    from llmguard.domains.retrieval.vectorstore.models import VectorCollectionSpec, VectorDocument, VectorSearchQuery

    start = time.perf_counter_ns()
    docs = [{**{k: v for k, v in doc.items() if k != "source_uri"}, "authority_claim": None,
             "publication_time": None, "effective_time": None, "trust_boundary": "UNVERIFIED"}
            for doc in world["documents"]]
    documents = {"world_id": world["world_id"], "documents": docs, "corpus_hash": digest(docs)}
    chunks = chunk_world(documents, model.tokenizer)
    if len(model.tokenizer(world["query_text"], add_special_tokens=True, truncation=False)["input_ids"]) > 128:
        raise ValueError("QUERY_TOKEN_OVERFLOW")
    corpus = {sha(world["query_text"].encode()): world["query_text"], **{c["content_hash"]: c["text"] for c in chunks}}
    missing = [k for k in corpus if k not in vectors]
    if missing:
        values = model.encode([corpus[k] for k in missing], batch_size=16, device="cpu",
                              normalize_embeddings=False, convert_to_numpy=True, show_progress_bar=False)
        vectors.update(zip(missing, values, strict=True))

    def unit(key: str) -> list[float]:
        vector = vectors[key]
        return list(map(float, vector / np.linalg.norm(vector)))

    spec = VectorCollectionSpec(
        fingerprint=digest({"corpus": documents["corpus_hash"], "model": BASE_IDENTITY["cache_identity_sha256"],
                            "chunk": [96, 16], "metric": "cosine"}), dimension=384,
    )
    target = out / "indexes" / world["world_id"]
    search = VectorSearchQuery(vector=unit(sha(world["query_text"].encode())), top_k=5)
    store = ChromaVectorStore(target)
    try:
        store.create_or_open_collection(spec)
        store.upsert(spec, [VectorDocument(
            doc_id=c["chunk_id"], vector=unit(c["content_hash"]),
            metadata={"doc_id": c["chunk_id"], "parent_doc_id": c["parent_doc_id"], "source_id": c["source_id"],
                      "source_type": "UNVERIFIED", "content_hash": c["content_hash"],
                      "corpus_snapshot_id": world["world_id"], "chunk_index": c["chunk_index"]},
            content_hash=c["content_hash"], content_ref=f"chroma:{c['chunk_id']}",
        ) for c in sorted(chunks, key=lambda c: c["chunk_id"])])
        hits = canonical_hits(store.query(spec, search))
        if len(hits) != 5 or store.count(spec) != len(chunks):
            raise ValueError("TOPK_OR_INDEX_DENOMINATOR")
    finally:
        store.close()
    store = ChromaVectorStore(target)
    try:
        store.create_or_open_collection(spec)
        if canonical_hits(store.query(spec, search)) != hits or store.count(spec) != len(chunks):
            raise ValueError("TOPK_REOPEN_DRIFT")
    finally:
        store.close()
    client: Any = chromadb.PersistentClient(path=str(target), settings=Settings(anonymized_telemetry=False))
    try:
        col = client.get_collection(spec.collection_name, embedding_function=None)
        config = col.configuration_json
        expected = {"space": "cosine", "ef_construction": 100, "ef_search": 100, "max_neighbors": 16,
                    "resize_factor": 1.2, "sync_threshold": 1000}
        if (set(col.get(include=[])["ids"]) != {c["chunk_id"] for c in chunks}
                or any(config["hnsw"].get(k) != v for k, v in expected.items())):
            raise ValueError("INDEX_CONFIGURATION_OR_MEMBERSHIP")
    finally:
        client.close()
    by_id = {c["chunk_id"]: c for c in chunks}
    return {"world_id": world["world_id"], "query_text": world["query_text"], "event_date": world["event_date"],
            "corpus_sha256": documents["corpus_hash"], "members": chunks, "collection_config": config,
            "topk": [{**h, "chunk": by_id[h["chunk_id"]]} for h in hits],
            "index_sha256": {f.relative_to(target).as_posix(): file_hash(f) for f in target.rglob("*") if f.is_file()},
            "retrieval_ns": time.perf_counter_ns() - start}


def save_prediction(out: Path, gate_sha: str, topk_sha: str, rows: list[Any], fixture: bool = False) -> str:
    if any(tuple(row["masks"]) != ARMS for row in rows):
        raise ValueError("FOUR_FROZEN_ARMS")
    predictions = write_once(out / "PREDICTIONS_ROLE_FREE.json", rows)
    return write_once(out / "PREDICTION_SEAL.json", {
        "status": "SOFTWARE_FIXTURE_ONLY" if fixture else "PREDICTION_SEALED_AWAITING_GIT_RECEIPT",
        "prediction_sha256": predictions, "admission_receipt_sha256": gate_sha, "topk_seal_sha256": topk_sha,
        "worlds": len(rows), "arms": list(ARMS), "labels_read": False, "commercial_api_calls": 0,
        "fixture": fixture, "new_scientific_results": 0 if fixture else len(rows),
    })


def predict(args: Any, worlds: list[Any], gate: dict[str, Any]) -> str:
    out = args.out
    gate_sha = write_once(out / "ADMISSION_RECEIPT.json", gate)
    registry = Path.cwd() / "experiments/paper1_chinese5060/OWNER28_ONESHOT_REGISTRY"
    registry.mkdir(parents=True, exist_ok=True)
    write_once(registry / "OWNER28-EVAL-01.json", {"input_sha256": args.input_sha256,
                  "code_commit": args.code_commit, "receipt_sha256": gate_sha})
    write_once(out / "ATTEMPT_STARTED.json", {"input_sha256": args.input_sha256})
    begin = time.monotonic()
    backend, r2 = pinned_backend(args)
    model, defender, b2, zh = backend
    vector_cache: dict[str, Any] = {}

    def resource_gate() -> None:
        if time.monotonic() - begin > 5300 or shutil.disk_usage(out).free < 10 * 1024**3:
            raise ValueError("RESOURCE_LIMIT")
        if sum(p.stat().st_size for p in out.rglob("*") if p.is_file()) > 5 * 1024**3:
            raise ValueError("PRIVATE_DISK_LIMIT")

    receipt = []
    packets = []
    for world in worlds:
        resource_gate()
        packet = build_topk(world, model, out, vector_cache)
        packet_sha = write_once(out / f"{world['world_id']}-TOPK.json", packet)
        receipt.append({"world_id": world["world_id"], "sha256": packet_sha})
        packets.append(packet)
    topk_sha = write_once(out / "TOPK_SEAL.json", {"input_sha256": args.input_sha256, "members": receipt,
                                                "worlds": len(packets), "top_k": 5, "exact_reopens": len(packets)})
    rows = []
    for packet, receipt_row in zip(packets, receipt, strict=True):
        resource_gate()
        texts = [h["chunk"]["text"] for h in packet["topk"]]
        tick = time.perf_counter_ns()
        embedding = r2.model_vectors(model, texts)
        embedding_ns = time.perf_counter_ns() - tick
        ehash = sha(embedding.cpu().detach().numpy().tobytes())
        traces = {}
        latency = {}
        for name, vote in (("RD_B2", b2), ("RD_ZH", zh)):
            tick = time.perf_counter_ns()
            traces[name] = r2.filter_one(defender, vote, texts, texts, embedding, ehash)
            latency[name] = time.perf_counter_ns() - tick
        tick = time.perf_counter_ns()
        masks = assemble_masks(5, packet["event_date"], texts,
                               traces["RD_B2"]["deleted_indices"], traces["RD_ZH"]["deleted_indices"])
        latency["DATE_ONLY"] = time.perf_counter_ns() - tick
        row = {"world_id": packet["world_id"], "packet_sha256": receipt_row["sha256"], "masks": masks,
               "traces": traces, "filter_ns": latency, "embedding_ns": embedding_ns,
               "embedding_sha256": ehash}
        write_once(out / f"{packet['world_id']}-PREDICTION.json", row)
        rows.append(row)
    result = save_prediction(out, gate_sha, topk_sha, rows)
    write_once(out / "RESOURCE_USAGE.json", {"seconds": time.monotonic() - begin, "threads": 2,
                                           "private_bytes": sum(p.stat().st_size for p in out.rglob("*") if p.is_file()),
                                           "commercial_usd": 0})
    return result


def fixture(args: Any) -> str:
    payload = parse_json(args.input.read_bytes())
    worlds = validate_payload(payload, fixture=True)
    topks, rows = [], []
    for world in worlds:
        # This software integration stub is never reachable from the scientific entry point.
        docs = world["documents"][:5]
        texts = [d["text"] for d in docs]
        packet_sha = write_once(args.out / f"{world['world_id']}-FIXTURE_TOPK.json", {
            "world_id": world["world_id"], "documents": docs, "backend": "MOCK_FIRST_FIVE",
        })
        topks.append(packet_sha)
        rows.append({"world_id": world["world_id"], "packet_sha256": packet_sha,
                     "masks": assemble_masks(5, world["event_date"], texts, [1], [1, 3])})
    receipt = write_once(args.out / "FIXTURE_RECEIPT.json", {
        "status": "SOFTWARE_FIXTURE_ONLY", "input_sha256": sha(args.input.read_bytes()),
        "model_calls": 0, "backend": "MOCK_FIXED_DELETIONS",
    })
    topk_sha = write_once(args.out / "FIXTURE_TOPK_SEAL.json", topks)
    return save_prediction(args.out, receipt, topk_sha, rows, fixture=True)


def export_receipt(out: Path, expected: str) -> str:
    """Prepare a hash-only Git receipt. 5090 must verify its publication before scoring."""
    path = out / "PREDICTION_SEAL.json"
    if file_hash(path) != expected:
        raise ValueError("PREDICTION_SEAL_SHA")
    seal = parse_json(path.read_bytes())
    if seal["fixture"] or seal["status"] != "PREDICTION_SEALED_AWAITING_GIT_RECEIPT":
        raise ValueError("SCIENTIFIC_PREDICTION_SEAL_REQUIRED")
    for name, key in (("PREDICTIONS_ROLE_FREE.json", "prediction_sha256"),
                      ("ADMISSION_RECEIPT.json", "admission_receipt_sha256"), ("TOPK_SEAL.json", "topk_seal_sha256")):
        if file_hash(out / name) != seal[key]:
            raise ValueError("PREDICTION_RECEIPT_CHAIN")
    if not (out / "RESOURCE_USAGE.json").is_file() or (out / "STOP.json").exists():
        raise ValueError("SUCCESSFUL_COMPLETION_REQUIRED")
    gate = parse_json((out / "ADMISSION_RECEIPT.json").read_bytes())
    if seal["worlds"] != gate["main_worlds"] + gate["mirror_worlds"] or seal["arms"] != list(ARMS):
        raise ValueError("SEALED_DENOMINATOR_OR_ARMS")
    result = {
        "status_after_git_publication": "PREDICTION_READY_FOR_INDEPENDENT_5090_EVAL",
        "authority": AUTHORITY, "main_worlds": gate["main_worlds"], "mirror_worlds": gate["mirror_worlds"],
        "role_free_sha256": gate["role_free_sha256"], "curator_git_commit": gate["curator_git_commit"],
        "curator_manifest_sha256": gate["curator_manifest_sha256"],
        "code_commit": gate["code_commit"], "prediction_seal_sha256": expected,
        "prediction_sha256": seal["prediction_sha256"], "topk_seal_sha256": seal["topk_seal_sha256"],
        "admission_receipt_sha256": seal["admission_receipt_sha256"],
    }
    return write_once(out / "PREDICTION_PUBLIC_RECEIPT.json", result)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("fixture", "check", "predict", "export-receipt"))
    parser.add_argument("--input", type=Path)
    parser.add_argument("--prediction-seal-sha256")
    parser.add_argument("--out", type=Path, required=True)
    for flag in ("input-sha256", "curator-sha256", "curator-commit", "curator-git-path", "code-commit"):
        parser.add_argument(f"--{flag}")
    for flag in ("assets", "upstream", "support"):
        parser.add_argument(f"--{flag}", type=Path)
    args = parser.parse_args()
    args.out = args.out.resolve()
    configure(args.out)
    if args.stage == "export-receipt":
        print(export_receipt(args.out, args.prediction_seal_sha256))
        return
    if args.input is None:
        raise ValueError("ROLE_FREE_INPUT_REQUIRED")
    if args.stage == "fixture":
        print(fixture(args))
        return
    if any(getattr(args, flag) is None for flag in (
        "input_sha256", "curator_sha256", "curator_commit", "curator_git_path", "code_commit",
    )):
        raise ValueError("SIGNED_HANDOFF_AND_FROZEN_CODE_REQUIRED")
    worlds, gate = admit(args)
    asset_identity(args)
    gate["identity_verified"] = True
    if args.stage == "check":
        print(write_once(args.out / "CHECK_ONLY_RECEIPT.json", gate))
        return
    try:
        print(predict(args, worlds, gate))
    except Exception as exc:
        write_once(args.out / "STOP.json", {"exception": type(exc).__name__, "reason": str(exc),
                                           "retry_authorized": False})
        raise


if __name__ == "__main__":
    main()
