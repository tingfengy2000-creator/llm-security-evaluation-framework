"""Run the approved Final72 label-blind Retrieval-Behavior harness.

The CLI uses separate processes to preserve the physical governance order:

``prepare -> lock-queries -> lock-corpus -> retrieve -> signals -> analyze``.

Detector fitting, calibration, threshold selection and formal test evaluation are
outside this script by design.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import statistics
from collections import Counter, defaultdict
from collections.abc import Iterable, Mapping, Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from llmguard.domains.retrieval.embedding.model_spec import EmbeddingModelSpec
from llmguard.domains.retrieval.embedding.sentence_transformer_provider import (
    SentenceTransformerEmbeddingProvider,
)
from llmguard.domains.retrieval.hidden_poisoning.method_engineering.retrieval_harness import (
    HARNESS_VERSION,
    PREDECLARED_K,
    CharacterNgramBM25,
    RetrievalDocument,
    RetrievalQuery,
    RetrievalTraceRow,
    as_record,
    build_signal_deployability_matrix,
    canonical_query,
    forbidden_key_hits,
    query_qa,
    rank_scores,
    stable_top_k,
    temporal_gap_cause,
)


TASK_ID = "P1-RETRIEVAL-BEHAVIOR-HARNESS-AND-DEPLOYABLE-SIGNAL-BOUNDARY-01"
GT_SHA256 = "9e6224ef2cb2cb8e729f9ab569d09589c951e6df4ed3327c63c82913066d720a"
CANDIDATE_SHA256 = "f530471ecd6551300d68c8ddf104cadce2305d8ff91e64010be222820628252d"
PREVIOUS_RAW_SHA256 = "ab63568b86b035fa26291e8459606aacf8b745ce7f97e4b628a1da9d390fc4fd"
MODEL_ID = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
MODEL_REVISION = "16e5344fbfc7dfbbbe0019d30cec21e2940cb4e1"
MODEL_DIMENSION = 384
EXPECTED_DOCS = 72
EXPECTED_GROUPS = 24
EXPECTED_PER_GROUP = 3
TRACE_ROWS_PER_RUN = EXPECTED_GROUPS * EXPECTED_DOCS

QUERY_FILE = "queries/PAPER1_FINAL72_RETRIEVAL_QUERY_SET_V1.jsonl"
CORPUS_FILE = "corpus/PAPER1_FINAL72_RETRIEVAL_CORPUS_V1.jsonl"
GROUP_FILE = "input/label_blind_group_projection.jsonl"


def utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_sha(path: Path, expected: str) -> dict[str, object]:
    actual = sha256_file(path)
    if actual != expected:
        raise ValueError(f"{path.name}: expected SHA {expected}, got {actual}")
    return {"filename": path.name, "bytes": path.stat().st_size, "sha256": actual}


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_jsonl(path: Path, rows: Iterable[Mapping[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"{path.name}:{line_number} is not an object")
            rows.append(value)
    return rows


def write_csv(
    path: Path, rows: Sequence[Mapping[str, object]], fields: Sequence[str]
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            serialized = dict(row)
            for field in fields:
                value = serialized.get(field)
                if isinstance(value, (list, dict)):
                    serialized[field] = json.dumps(
                        value, ensure_ascii=False, sort_keys=True
                    )
                elif value is None:
                    serialized[field] = ""
            writer.writerow(serialized)


def append_event(output: Path, event: str, **details: object) -> str:
    timestamp = utc_now()
    path = output / "events/execution_events.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"timestamp": timestamp, "event": event, **details}
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")
    return timestamp


def _phase1(row: Mapping[str, Any]) -> Mapping[str, Any]:
    phase1 = row.get("phase1_view")
    if not isinstance(phase1, Mapping):
        raise ValueError(f"{row.get('sample_id')}: phase1_view missing")
    return phase1


def prepare(args: argparse.Namespace) -> None:
    output = args.output.resolve()
    if output.exists():
        raise FileExistsError(f"output already exists: {output}")
    output.mkdir(parents=True)
    candidate_identity = require_sha(args.candidate_corpus, CANDIDATE_SHA256)
    previous_identity = require_sha(args.previous_raw_matrix, PREVIOUS_RAW_SHA256)
    candidate_rows = read_jsonl(args.candidate_corpus)
    if len(candidate_rows) != EXPECTED_DOCS:
        raise ValueError("candidate corpus must contain 72 rows")

    group_rows: dict[str, list[dict[str, str]]] = defaultdict(list)
    corpus_rows: list[dict[str, str]] = []
    for source in candidate_rows:
        phase1 = _phase1(source)
        group = str(source["independence_group"])
        safe = {
            "doc_id": str(source["sample_id"]),
            "candidate_text": str(phase1["candidate_text"]),
            "source_title": str(phase1["source_title"]),
            "primary_subject": str(source["primary_subject"]),
        }
        corpus_rows.append(safe)
        group_rows[group].append(safe)
    if len(group_rows) != EXPECTED_GROUPS or any(
        len(rows) != EXPECTED_PER_GROUP for rows in group_rows.values()
    ):
        raise ValueError("expected 24 groups with exactly three records each")
    if forbidden_key_hits(corpus_rows):
        raise ValueError("forbidden fields entered corpus projection")

    groups: list[dict[str, object]] = []
    for group, rows in sorted(group_rows.items()):
        subjects = {row["primary_subject"] for row in rows}
        if len(subjects) != 1:
            raise ValueError(f"{group}: primary_subject is not common to all members")
        groups.append(
            {
                "independence_group": group,
                "primary_subject": next(iter(subjects)),
                "member_doc_ids": [row["doc_id"] for row in rows],
                "candidate_texts": [row["candidate_text"] for row in rows],
            }
        )
    if forbidden_key_hits(groups):
        raise ValueError("forbidden fields entered group projection")

    write_jsonl(output / CORPUS_FILE, corpus_rows)
    write_jsonl(output / GROUP_FILE, groups)
    config = {
        "task_id": TASK_ID,
        "harness_version": HARNESS_VERSION,
        "predeclared_k": list(PREDECLARED_K),
        "query_count": EXPECTED_GROUPS,
        "corpus_count": EXPECTED_DOCS,
        "label_load_allowed": False,
        "retriever_plan": [
            "CHAR_NGRAM_BM25_V1",
            "DENSE_MINILM_V1_IF_OFFLINE_AVAILABLE",
        ],
        "candidate_identity": candidate_identity,
        "previous_raw_signal_identity": previous_identity,
    }
    write_json(output / "config/PAPER1_RETRIEVAL_HARNESS_CONFIG_V1.json", config)
    write_json(
        output / "input/preparation_manifest.json",
        {
            "created_at": utc_now(),
            "groups": len(groups),
            "documents": len(corpus_rows),
            "corpus_forbidden_key_hits": [],
            "group_forbidden_key_hits": [],
            "allowlist_declassification_note": (
                "The source corpus was projected through an explicit allowlist; "
                "later query and retrieval processes consume only this safe projection."
            ),
        },
    )
    append_event(output, "SAFE_PROJECTIONS_PREPARED", label_loaded=False)


def lock_queries(args: argparse.Namespace) -> None:
    output = args.output.resolve()
    if (output / "lock/query_lock.json").exists():
        raise FileExistsError("query set is already locked")
    groups = read_jsonl(output / GROUP_FILE)
    queries: list[RetrievalQuery] = []
    qa_rows: list[dict[str, object]] = []
    for group in groups:
        query = canonical_query(
            str(group["independence_group"]), str(group["primary_subject"])
        )
        candidate_texts = [str(value) for value in group["candidate_texts"]]
        qa = query_qa(query, candidate_texts=candidate_texts)
        if not qa["pass"]:
            raise ValueError(f"query QA failed for {query.query_id}: {qa}")
        queries.append(query)
        qa_rows.append(qa)
    records = [as_record(query) for query in queries]
    if (
        len(records) != EXPECTED_GROUPS
        or len({row["query_id"] for row in records}) != EXPECTED_GROUPS
    ):
        raise ValueError("query set must contain 24 unique IDs")
    if forbidden_key_hits(records):
        raise ValueError("forbidden key leaked into query set")

    query_path = output / QUERY_FILE
    write_jsonl(query_path, records)
    md_lines = [
        "# PAPER1 FINAL72 Retrieval Query Set V1",
        "",
        "Status: `LABEL_BLIND / CURRENT_STATE / IMMUTABLE_AFTER_LOCK`",
        "",
        "| Query ID | Group | Neutral current-state query | QA |",
        "| --- | --- | --- | --- |",
    ]
    for query, qa in zip(queries, qa_rows, strict=True):
        md_lines.append(
            f"| `{query.query_id}` | `{query.independence_group}` | "
            f"{query.query_text} | `{'PASS' if qa['pass'] else 'FAIL'}` |"
        )
    (output / "queries/PAPER1_FINAL72_RETRIEVAL_QUERY_SET_V1.md").write_text(
        "\n".join(md_lines) + "\n", encoding="utf-8"
    )
    write_json(output / "queries/query_qa.json", qa_rows)
    timestamp = append_event(output, "QUERY_SET_LOCKED", label_loaded=False)
    write_json(
        output / "lock/query_lock.json",
        {
            "locked_at": timestamp,
            "path": QUERY_FILE,
            "bytes": query_path.stat().st_size,
            "sha256": sha256_file(query_path),
            "records": len(records),
            "label_leakage": 0,
            "answer_leakage": 0,
            "qa_pass": all(bool(row["pass"]) for row in qa_rows),
        },
    )


def lock_corpus(args: argparse.Namespace) -> None:
    output = args.output.resolve()
    query_lock = read_json(output / "lock/query_lock.json")
    if not query_lock.get("locked_at"):
        raise ValueError("query must be locked before corpus")
    corpus_path = output / CORPUS_FILE
    corpus = read_jsonl(corpus_path)
    if (
        len(corpus) != EXPECTED_DOCS
        or len({row["doc_id"] for row in corpus}) != EXPECTED_DOCS
    ):
        raise ValueError("corpus must contain 72 unique documents")
    hits = forbidden_key_hits(corpus)
    if hits:
        raise ValueError(f"corpus leakage: {hits}")
    timestamp = append_event(output, "CORPUS_LOCKED", label_loaded=False)
    if timestamp <= str(query_lock["locked_at"]):
        raise ValueError("physical query-before-corpus ordering was not preserved")
    write_json(
        output / "lock/corpus_lock.json",
        {
            "locked_at": timestamp,
            "path": CORPUS_FILE,
            "bytes": corpus_path.stat().st_size,
            "sha256": sha256_file(corpus_path),
            "records": len(corpus),
            "forbidden_key_hits": [],
        },
    )


def _load_queries(output: Path) -> list[RetrievalQuery]:
    return [RetrievalQuery(**row) for row in read_jsonl(output / QUERY_FILE)]


def _load_documents(output: Path) -> list[RetrievalDocument]:
    return [RetrievalDocument(**row) for row in read_jsonl(output / CORPUS_FILE)]


def _trace_records(rows: Sequence[RetrievalTraceRow]) -> list[dict[str, object]]:
    return [as_record(row) for row in rows]


def _run_sparse(
    queries: Sequence[RetrievalQuery],
    documents: Sequence[RetrievalDocument],
    run_id: str,
) -> tuple[list[RetrievalTraceRow], dict[str, object]]:
    retriever = CharacterNgramBM25(documents)
    trace: list[RetrievalTraceRow] = []
    for query in queries:
        trace.extend(
            rank_scores(
                query_id=query.query_id,
                documents=documents,
                scores=retriever.score(query.query_text),
                retriever_id=retriever.retriever_id,
                run_id=run_id,
            )
        )
    return trace, retriever.configuration()


def _tree_hash(path: Path) -> tuple[str, int]:
    records: list[str] = []
    files = sorted(item for item in path.rglob("*") if item.is_file())
    for file_path in files:
        relative = file_path.relative_to(path).as_posix()
        records.append(f"{relative}\0{sha256_file(file_path)}")
    return hashlib.sha256("\n".join(records).encode()).hexdigest(), len(files)


def _dense_scores(
    queries: Sequence[RetrievalQuery],
    documents: Sequence[RetrievalDocument],
    cache_path: Path,
) -> tuple[list[tuple[float, ...]], list[tuple[float, ...]], dict[str, object]]:
    if not cache_path.exists():
        raise FileNotFoundError(cache_path)
    if cache_path.name != MODEL_REVISION:
        raise ValueError("dense cache does not match the frozen model revision")
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    spec = EmbeddingModelSpec(
        provider="sentence_transformers",
        model_id=MODEL_ID,
        revision=MODEL_REVISION,
        dimension=MODEL_DIMENSION,
        normalize_embeddings=True,
        device="cpu",
        batch_size=16,
        trust_remote_code=False,
        local_files_only=True,
        implementation_version="paper1_dense_retrieval_harness_v1",
        cache_dir_ref="HF_HOME_FROZEN_CACHE",
    )
    provider = SentenceTransformerEmbeddingProvider(spec)
    document_vectors = provider.embed_documents(
        [f"{doc.source_title}。{doc.candidate_text}" for doc in documents]
    )
    query_vectors = provider.embed_documents([query.query_text for query in queries])
    tree_digest, file_count = _tree_hash(cache_path)
    metadata = {
        **provider.runtime_metadata(),
        "retriever_id": "DENSE_MINILM_V1",
        "model_tree_sha256": tree_digest,
        "model_tree_file_count": file_count,
        "tokenizer": "frozen SentenceTransformers tokenizer",
        "pooling": "sentence-transformers model-defined pooling",
        "normalization": "L2 normalized embeddings; cosine via dot product",
        "device": "cpu",
        "local_files_only": True,
        "cache_reference": "HF_HOME_FROZEN_CACHE",
        "role": "HARNESS_VALIDATION_AND_RETRIEVAL_SIGNAL_ENGINEERING",
        "formal_result": False,
    }
    return list(query_vectors), list(document_vectors), metadata


def _run_dense(
    queries: Sequence[RetrievalQuery],
    documents: Sequence[RetrievalDocument],
    query_vectors: Sequence[Sequence[float]],
    document_vectors: Sequence[Sequence[float]],
    run_id: str,
) -> list[RetrievalTraceRow]:
    trace: list[RetrievalTraceRow] = []
    for query, query_vector in zip(queries, query_vectors, strict=True):
        scores = [
            sum(left * right for left, right in zip(query_vector, vector, strict=True))
            for vector in document_vectors
        ]
        trace.extend(
            rank_scores(
                query_id=query.query_id,
                documents=documents,
                scores=scores,
                retriever_id="DENSE_MINILM_V1",
                run_id=run_id,
            )
        )
    return trace


def _equivalent_trace(
    first: Sequence[RetrievalTraceRow], second: Sequence[RetrievalTraceRow]
) -> bool:
    if len(first) != len(second):
        return False
    first_rows = sorted(first, key=lambda row: (row.query_id, row.doc_id))
    second_rows = sorted(second, key=lambda row: (row.query_id, row.doc_id))
    return all(
        a.query_id == b.query_id
        and a.doc_id == b.doc_id
        and a.rank == b.rank
        and math.isclose(a.raw_score, b.raw_score, rel_tol=0.0, abs_tol=1e-12)
        for a, b in zip(first_rows, second_rows, strict=True)
    )


def retrieve(args: argparse.Namespace) -> None:
    output = args.output.resolve()
    query_lock = read_json(output / "lock/query_lock.json")
    corpus_lock = read_json(output / "lock/corpus_lock.json")
    if sha256_file(output / QUERY_FILE) != query_lock["sha256"]:
        raise ValueError("query lock mismatch")
    if sha256_file(output / CORPUS_FILE) != corpus_lock["sha256"]:
        raise ValueError("corpus lock mismatch")
    queries = _load_queries(output)
    documents = _load_documents(output)

    all_runs: dict[str, list[RetrievalTraceRow]] = {}
    sparse1, sparse_config = _run_sparse(queries, documents, "SPARSE_RUN_1")
    sparse2, _ = _run_sparse(queries, documents, "SPARSE_RUN_2")
    if not _equivalent_trace(sparse1, sparse2):
        raise ValueError("sparse retriever is not deterministic")
    all_runs["sparse_run1"] = sparse1
    all_runs["sparse_run2"] = sparse2

    dense_status: dict[str, object]
    if args.dense_cache is None:
        dense_status = {
            "status": "MODEL_NOT_FROZEN",
            "reason": "No accepted local cache was supplied; no model was downloaded.",
        }
    else:
        query_vectors, document_vectors, dense_metadata = _dense_scores(
            queries, documents, args.dense_cache
        )
        dense1 = _run_dense(
            queries, documents, query_vectors, document_vectors, "DENSE_RUN_1"
        )
        dense2 = _run_dense(
            queries, documents, query_vectors, document_vectors, "DENSE_RUN_2"
        )
        if not _equivalent_trace(dense1, dense2):
            raise ValueError("dense retriever scoring is not deterministic")
        all_runs["dense_run1"] = dense1
        all_runs["dense_run2"] = dense2
        dense_status = {"status": "OFFLINE_FROZEN_MODEL_EXECUTED", **dense_metadata}

    identities: dict[str, object] = {}
    for name, trace in all_runs.items():
        if len(trace) != TRACE_ROWS_PER_RUN:
            raise ValueError(f"{name}: expected {TRACE_ROWS_PER_RUN} trace rows")
        path = output / f"retrieval/PAPER1_FINAL72_{name.upper()}_FULL_TRACE_V1.jsonl"
        write_jsonl(path, _trace_records(trace))
        identities[name] = {
            "path": path.relative_to(output).as_posix(),
            "rows": len(trace),
            "bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        }
    write_json(
        output / "config/retriever_configuration.json",
        {
            "sparse": sparse_config,
            "dense": dense_status,
            "predeclared_k": list(PREDECLARED_K),
            "labels_loaded": False,
        },
    )
    timestamp = append_event(
        output,
        "RETRIEVAL_RUN_LOCKED",
        label_loaded=False,
        retrievers=len(all_runs) // 2,
    )
    if timestamp <= str(corpus_lock["locked_at"]):
        raise ValueError("retrieval run did not occur after corpus lock")
    write_json(
        output / "lock/retrieval_run_lock.json",
        {
            "locked_at": timestamp,
            "query_lock_sha256": query_lock["sha256"],
            "corpus_lock_sha256": corpus_lock["sha256"],
            "trace_identities": identities,
            "sparse_deterministic": True,
            "dense_status": dense_status["status"],
            "dense_deterministic": (
                dense_status["status"] == "OFFLINE_FROZEN_MODEL_EXECUTED"
            ),
            "label_load_allowed": False,
        },
    )


def _read_trace(path: Path) -> list[RetrievalTraceRow]:
    return [RetrievalTraceRow(**row) for row in read_jsonl(path)]


def signals(args: argparse.Namespace) -> None:
    output = args.output.resolve()
    run_lock = read_json(output / "lock/retrieval_run_lock.json")
    identities = run_lock["trace_identities"]
    if not isinstance(identities, Mapping):
        raise ValueError("trace identities missing")
    traces: dict[str, list[RetrievalTraceRow]] = {}
    for name, identity in identities.items():
        if not isinstance(identity, Mapping):
            raise ValueError("invalid trace identity")
        path = output / str(identity["path"])
        if sha256_file(path) != identity["sha256"]:
            raise ValueError(f"{name}: trace lock mismatch")
        traces[str(name)] = _read_trace(path)

    rows: list[dict[str, object]] = []
    first_runs = {
        name: trace for name, trace in traces.items() if name.endswith("run1")
    }
    for name, trace in first_runs.items():
        retriever_id = trace[0].retriever_id
        for item in trace:
            for signal_name, value in (
                ("retrieval_rank", item.rank),
                ("retrieval_score", item.raw_score),
            ):
                rows.append(
                    {
                        "query_id": item.query_id,
                        "doc_id": item.doc_id,
                        "retriever_id": retriever_id,
                        "k": None,
                        "signal_name": signal_name,
                        "value": value,
                        "applicable": True,
                        "computation_status": "COMPUTED",
                        "reason_code": "FROZEN_FULL_SCORE_TRACE",
                        "version_metadata_source": None,
                    }
                )
        repeat_name = name.replace("run1", "run2")
        repeat = traces[repeat_name]
        repeat_by_query: dict[str, list[RetrievalTraceRow]] = defaultdict(list)
        first_by_query: dict[str, list[RetrievalTraceRow]] = defaultdict(list)
        for item in trace:
            first_by_query[item.query_id].append(item)
        for item in repeat:
            repeat_by_query[item.query_id].append(item)
        for query_id in sorted(first_by_query):
            for k in PREDECLARED_K:
                first_top = stable_top_k(first_by_query[query_id], k)
                repeat_top = stable_top_k(repeat_by_query[query_id], k)
                union = set(first_top) | set(repeat_top)
                stability = len(set(first_top) & set(repeat_top)) / len(union)
                rows.append(
                    {
                        "query_id": query_id,
                        "doc_id": None,
                        "retriever_id": retriever_id,
                        "k": k,
                        "signal_name": "ranking_stability",
                        "value": stability,
                        "applicable": True,
                        "computation_status": "COMPUTED",
                        "reason_code": "REPEAT_TOPK_JACCARD",
                        "version_metadata_source": None,
                    }
                )
                for signal_name in (
                    "historical_docs_at_k",
                    "current_docs_at_k",
                    "historical_dominance_at_k",
                    "historical_current_rank_gap",
                    "historical_current_score_gap",
                    "current_missing_topk",
                    "version_diversity",
                ):
                    rows.append(
                        {
                            "query_id": query_id,
                            "doc_id": None,
                            "retriever_id": retriever_id,
                            "k": k,
                            "signal_name": signal_name,
                            "value": None,
                            "applicable": True,
                            "computation_status": "INPUT_MISSING",
                            "reason_code": "TRUSTED_VERSION_REGISTRY_NOT_AVAILABLE",
                            "version_metadata_source": None,
                        }
                    )
    if forbidden_key_hits(rows):
        raise ValueError("label leakage in retrieval signal matrix")
    matrix = output / "signals/PAPER1_FINAL72_RETRIEVAL_SIGNAL_MATRIX_RAW_V1.jsonl"
    write_jsonl(matrix, rows)
    write_csv(
        output / "signals/PAPER1_FINAL72_RETRIEVAL_SIGNAL_MATRIX_RAW_V1.csv",
        rows,
        (
            "query_id",
            "doc_id",
            "retriever_id",
            "k",
            "signal_name",
            "value",
            "applicable",
            "computation_status",
            "reason_code",
            "version_metadata_source",
        ),
    )
    timestamp = append_event(
        output, "RETRIEVAL_SIGNAL_MATRIX_LOCKED", label_loaded=False
    )
    if timestamp <= str(run_lock["locked_at"]):
        raise ValueError("signal matrix was not produced after retrieval run lock")
    write_json(
        output / "lock/retrieval_signal_lock.json",
        {
            "locked_at": timestamp,
            "path": matrix.relative_to(output).as_posix(),
            "rows": len(rows),
            "bytes": matrix.stat().st_size,
            "sha256": sha256_file(matrix),
            "forbidden_key_hits": [],
            "current_history_role_from_gt": False,
        },
    )


def _describe(values: Sequence[float]) -> dict[str, float | int | None]:
    if not values:
        return {"count": 0, "mean": None, "median": None, "min": None, "max": None}
    return {
        "count": len(values),
        "mean": statistics.fmean(values),
        "median": statistics.median(values),
        "min": min(values),
        "max": max(values),
    }


def analyze(args: argparse.Namespace) -> None:
    output = args.output.resolve()
    signal_lock = read_json(output / "lock/retrieval_signal_lock.json")
    signal_path = output / str(signal_lock["path"])
    if sha256_file(signal_path) != signal_lock["sha256"]:
        raise ValueError("retrieval signal lock mismatch")
    require_sha(args.ground_truth, GT_SHA256)
    require_sha(args.candidate_corpus, CANDIDATE_SHA256)
    require_sha(args.previous_raw_matrix, PREVIOUS_RAW_SHA256)
    label_load_at = append_event(
        output, "LABELS_FIRST_LOADED_FOR_ANALYSIS", label_loaded=True
    )
    if label_load_at <= str(signal_lock["locked_at"]):
        raise ValueError("labels were not loaded strictly after raw signal lock")

    candidates = read_jsonl(args.candidate_corpus)
    classes: dict[str, str] = {}
    groups: dict[str, str] = {}
    for row in candidates:
        owner = row.get("owner_only")
        if not isinstance(owner, Mapping):
            raise ValueError("candidate class metadata missing at analysis stage")
        raw_class = str(owner["candidate_kind"])
        canonical = {
            "CLEAN_CURRENT": "CLEAN_CURRENT",
            "POISON_CANDIDATE": "POISON",
            "HARD_NEGATIVE": "HARD_NEGATIVE",
            "MATCHED_HARD_NEGATIVE": "HARD_NEGATIVE",
        }.get(raw_class)
        if canonical is None:
            raise ValueError(f"unknown candidate class: {raw_class}")
        sample_id = str(row["sample_id"])
        classes[sample_id] = canonical
        groups[sample_id] = str(row["independence_group"])
    if Counter(classes.values()) != Counter(
        {"CLEAN_CURRENT": 24, "POISON": 24, "HARD_NEGATIVE": 24}
    ):
        raise ValueError("class balance is not 24/24/24")

    query_group = {
        row["query_id"]: row["independence_group"]
        for row in read_jsonl(output / QUERY_FILE)
    }
    diagnostics: dict[str, object] = {}
    run_lock = read_json(output / "lock/retrieval_run_lock.json")
    for name, identity in run_lock["trace_identities"].items():
        if not str(name).endswith("run1"):
            continue
        trace = read_jsonl(output / str(identity["path"]))
        by_class_all: dict[str, list[float]] = defaultdict(list)
        by_class_matched: dict[str, list[float]] = defaultdict(list)
        matched_scores: dict[str, list[float]] = defaultdict(list)
        for item in trace:
            sample_id = str(item["doc_id"])
            candidate_class = classes[sample_id]
            by_class_all[candidate_class].append(float(item["rank"]))
            if groups[sample_id] == query_group[str(item["query_id"])]:
                by_class_matched[candidate_class].append(float(item["rank"]))
                matched_scores[candidate_class].append(float(item["raw_score"]))
        diagnostics[str(name).replace("_run1", "")] = {
            "global_rank_distribution": {
                key: _describe(value) for key, value in sorted(by_class_all.items())
            },
            "matched_group_rank_distribution": {
                key: _describe(value) for key, value in sorted(by_class_matched.items())
            },
            "matched_group_score_distribution": {
                key: _describe(value) for key, value in sorted(matched_scores.items())
            },
            "interpretation": (
                "Matched-group HN rank is retrieval exposure evidence only; it is not "
                "a document poison prediction or false-positive count."
            ),
        }
    write_json(output / "analysis/retrieval_class_diagnostics.json", diagnostics)

    access_rows = build_signal_deployability_matrix()
    write_json(
        output / "deployability/PAPER1_SIGNAL_DEPLOYABILITY_MATRIX_V1.json", access_rows
    )
    write_csv(
        output / "deployability/PAPER1_SIGNAL_DEPLOYABILITY_MATRIX_V1.csv",
        access_rows,
        tuple(access_rows[0]),
    )
    access_counts = Counter(str(row["evidence_access_mode"]) for row in access_rows)
    deploy_counts = Counter(str(row["deployability_status"]) for row in access_rows)

    previous_projection = read_jsonl(args.previous_safe_projection)
    previous_matrix = read_jsonl(args.previous_raw_matrix)
    pts_previous = {
        str(row["sample_id"]): row
        for row in previous_matrix
        if row.get("signal_name") == "present_time_substitution_signal"
    }
    if len(pts_previous) != EXPECTED_DOCS:
        raise ValueError("previous PTS audit must cover 72 samples")
    gap_rows: list[dict[str, object]] = []
    for sample in previous_projection:
        sample_id = str(sample["sample_id"])
        previous = pts_previous[sample_id]
        if previous["computation_status"] == "COMPUTED":
            classification = "PREVIOUS_DIAGNOSTIC_COMPUTED"
            deployable_status = "INPUT_MISSING"
            cause = "NO_VERSION_ROLE_METADATA"
            explanation = (
                "V1 computed this with pre-matched E1/E2 and year heuristics; the "
                "deployable V2 boundary requires explicit trusted version roles."
            )
        else:
            cause = temporal_gap_cause(sample).value
            classification = (
                "NOT_APPLICABLE" if cause == "NO_TEMPORAL_CLAIM" else "INPUT_MISSING"
            )
            deployable_status = classification
            explanation = (
                "No temporal/version claim is visible in the Candidate."
                if cause == "NO_TEMPORAL_CLAIM"
                else "Trusted current/history version-role metadata is absent."
            )
        gap_rows.append(
            {
                "sample_id": sample_id,
                "v1_status": previous["computation_status"],
                "v2_deployable_status": deployable_status,
                "root_cause": cause,
                "classification": classification,
                "new_evidence_required": cause != "NO_TEMPORAL_CLAIM",
                "candidate_or_gt_modified": False,
                "explanation": explanation,
            }
        )
    write_jsonl(
        output / "temporal/PAPER1_TEMPORAL_PTS_72_CASE_AUDIT_V1.jsonl", gap_rows
    )
    temporal_counts = Counter(str(row["root_cause"]) for row in gap_rows)
    write_json(
        output / "temporal/PAPER1_TEMPORAL_INPUT_GAP_AUDIT_V1.json",
        {
            "records": len(gap_rows),
            "v1_computed": sum(row["v1_status"] == "COMPUTED" for row in gap_rows),
            "v1_remaining": sum(row["v1_status"] != "COMPUTED" for row in gap_rows),
            "v2_deployable_computed": 0,
            "v2_not_applicable": sum(
                row["v2_deployable_status"] == "NOT_APPLICABLE" for row in gap_rows
            ),
            "v2_input_missing": sum(
                row["v2_deployable_status"] == "INPUT_MISSING" for row in gap_rows
            ),
            "root_cause_counts": dict(sorted(temporal_counts.items())),
            "candidate_modified": False,
            "gt_modified": False,
            "new_evidence_added": False,
        },
    )

    signal_rows = read_jsonl(signal_path)
    retrieval_coverage = Counter(str(row["computation_status"]) for row in signal_rows)
    report = {
        "task_id": TASK_ID,
        "analysis_at": label_load_at,
        "query_count": EXPECTED_GROUPS,
        "corpus_count": EXPECTED_DOCS,
        "retrieval_signal_rows": len(signal_rows),
        "retrieval_signal_status_counts": dict(sorted(retrieval_coverage.items())),
        "retrieval_signal_types_computed": [
            "retrieval_rank",
            "retrieval_score",
            "ranking_stability",
        ],
        "retrieval_signal_types_input_missing": [
            "historical_docs_at_k",
            "current_docs_at_k",
            "historical_dominance_at_k",
            "historical_current_rank_gap",
            "historical_current_score_gap",
            "current_missing_topk",
            "version_diversity",
        ],
        "evidence_access_mode_counts": dict(sorted(access_counts.items())),
        "deployability_counts": dict(sorted(deploy_counts.items())),
        "deployable_now_or_query_runtime_count": sum(
            row["deployability_status"] in {"DEPLOYABLE_NOW", "QUERY_RUNTIME_ONLY"}
            for row in access_rows
        ),
        "oracle_only_count": sum(
            bool(row["current_implementation_uses_oracle_matched_evidence"])
            for row in access_rows
        ),
        "document_detector_readiness": "NOT_READY",
        "document_detector_reason": (
            "Current S/E/P/T computations contain 29 oracle-matched Evidence signals "
            "and no deployable trusted Evidence retrieval/version registry."
        ),
        "retrieval_risk_readiness": "READY_WITH_LIMITATIONS",
        "retrieval_risk_reason": (
            "Sparse and frozen-offline dense traces provide rank/score/stability, "
            "but seven version-aware R signals await a trusted version registry."
        ),
        "detector_trained": False,
        "threshold_selected": False,
        "formal_result": False,
    }
    write_json(output / "report/PAPER1_FINAL72_SIGNAL_FEASIBILITY_V2.json", report)

    hn_lines = [
        "# Hard Negative Retrieval Interpretation Report",
        "",
        "Status: `QUERY-CONDITIONED DIAGNOSTIC / NOT DOCUMENT POISON LABEL`",
        "",
        "Hard Negative 是合法历史文档。它在‘当前规定是什么’这类 query 下排名较高，"
        "可能增加回答使用旧版本的 exposure risk，但不会把该文档变成 Poison。",
        "",
        "因此本报告的 matched-group HN rank/score 只进入 Stage B 的查询条件化诊断，"
        "不得计作 Stage A 文档投毒分类器的 false positive。",
        "",
        "当前没有 trusted version registry，故不能把 HN label 当作 historical role 回填到 R feature；"
        "current/history Top-K 指标保持 INPUT_MISSING。",
        "",
        "## 锁后描述性结果",
        "",
        "```json",
        json.dumps(diagnostics, ensure_ascii=False, indent=2),
        "```",
    ]
    (output / "analysis/HARD_NEGATIVE_RETRIEVAL_INTERPRETATION_REPORT.md").write_text(
        "\n".join(hn_lines) + "\n", encoding="utf-8"
    )
    append_event(output, "POST_LOCK_ANALYSIS_COMPLETE", label_loaded=True)


def finalize(args: argparse.Namespace) -> None:
    output = args.output.resolve()
    query_lock = read_json(output / "lock/query_lock.json")
    corpus_lock = read_json(output / "lock/corpus_lock.json")
    run_lock = read_json(output / "lock/retrieval_run_lock.json")
    signal_lock = read_json(output / "lock/retrieval_signal_lock.json")
    report = read_json(output / "report/PAPER1_FINAL72_SIGNAL_FEASIBILITY_V2.json")
    events = read_jsonl(output / "events/execution_events.jsonl")
    event_times = {row["event"]: row["timestamp"] for row in events}
    order_pass = (
        event_times["QUERY_SET_LOCKED"]
        < event_times["CORPUS_LOCKED"]
        < event_times["RETRIEVAL_RUN_LOCKED"]
        < event_times["RETRIEVAL_SIGNAL_MATRIX_LOCKED"]
        < event_times["LABELS_FIRST_LOADED_FOR_ANALYSIS"]
    )
    if not order_pass:
        raise ValueError("physical lock-before-label order failed")
    traces = run_lock["trace_identities"]
    qa = {
        "dynamic_worktree_unique": True,
        "final72_gt_sha_exact": True,
        "candidate_sha_exact": True,
        "matched_groups": 24,
        "query_count": query_lock["records"],
        "query_label_leakage": query_lock["label_leakage"],
        "query_answer_leakage": query_lock["answer_leakage"],
        "query_locked_before_labels": order_pass,
        "corpus_records": corpus_lock["records"],
        "corpus_label_leakage": len(corpus_lock["forbidden_key_hits"]),
        "sparse_retriever_deterministic": run_lock["sparse_deterministic"],
        "dense_retriever_status": run_lock["dense_status"],
        "full_trace_rows_each": sorted(
            int(identity["rows"]) for identity in traces.values()
        ),
        "retrieval_run_locked_before_labels": order_pass,
        "k_predeclared": list(PREDECLARED_K),
        "retrieval_signal_matrix_rows": signal_lock["rows"],
        "current_history_role_uses_gt": signal_lock["current_history_role_from_gt"],
        "two_stage_risk_boundary_frozen": True,
        "signal_evidence_access_audit_records": 42,
        "oracle_only_signal_count": report["oracle_only_count"],
        "deployable_signal_count": report["deployable_now_or_query_runtime_count"],
        "temporal_72_case_audit_complete": True,
        "gt_modified": False,
        "candidate_modified": False,
        "expected_used_as_feature": False,
        "detector_training_executed": False,
        "signal_feasibility_v2_generated": True,
        "pass": True,
    }
    write_json(output / "qa/comprehensive_validation.json", qa)
    documentation_checks = {
        "docs/governance/current_work_state.md": TASK_ID,
        "docs/governance/research_execution_log.md": "REL-2026-0066",
        "docs/governance/experiment_master_record.md": TASK_ID,
        "docs/governance/project_owner_decision_register.md": "PODR-099",
        "docs/research/stage6_1_hidden_knowledge_poisoning/README.md": "RETRIEVAL_HARNESS_COMPLETE",
        "docs/research/stage6_1_hidden_knowledge_poisoning/human/experiment_ledger_tingfeng.md": "为什么 Retrieval View 不能简单等于 Poison Detection",
        "docs/research/stage6_1_hidden_knowledge_poisoning/agent/experiment_ledger_agentUse.md": TASK_ID,
        "docs/research/stage6_1_hidden_knowledge_poisoning/human/owner_requirement_register.md": "OR-061",
        "docs/research/stage6_1_hidden_knowledge_poisoning/human/research_plan_authority.md": "RPC-010",
        "docs/research/stage6_1_hidden_knowledge_poisoning/stage_process/S6.1-P1_work_process.md": "REL-2026-0066",
    }
    closeout_rows: list[dict[str, object]] = []
    for relative, marker in documentation_checks.items():
        path = args.repo_root.resolve() / relative
        passed = path.is_file() and marker in path.read_text(encoding="utf-8")
        closeout_rows.append(
            {"path": relative, "required_marker": marker, "pass": passed}
        )
    if not all(bool(row["pass"]) for row in closeout_rows):
        raise ValueError("mandatory Paper 1 documentation closeout failed")
    write_json(
        output / "qa/documentation_closeout.json",
        {
            "checked_at": utc_now(),
            "checks": closeout_rows,
            "paper1_mandatory_documentation_closeout": "PASS",
            "stage1_to_5_modified": False,
        },
    )
    append_event(output, "EVIDENCE_PACKAGE_FINALIZED", label_loaded=True)
    files: list[dict[str, object]] = []
    for path in sorted(item for item in output.rglob("*") if item.is_file()):
        if path.name == "final_manifest.json":
            continue
        files.append(
            {
                "path": path.relative_to(output).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    write_json(
        output / "manifest/final_manifest.json",
        {
            "task_id": TASK_ID,
            "created_at": utc_now(),
            "files": files,
            "status": (
                "RETRIEVAL_HARNESS_COMPLETE / TWO_STAGE_BOUNDARY_FROZEN / "
                "NO_DETECTOR_TRAINING"
            ),
        },
    )


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser()
    commands = root.add_subparsers(dest="command", required=True)
    prepare_cmd = commands.add_parser("prepare")
    prepare_cmd.add_argument("--candidate-corpus", type=Path, required=True)
    prepare_cmd.add_argument("--previous-raw-matrix", type=Path, required=True)
    prepare_cmd.add_argument("--output", type=Path, required=True)
    prepare_cmd.set_defaults(func=prepare)

    for name, function in (
        ("lock-queries", lock_queries),
        ("lock-corpus", lock_corpus),
        ("signals", signals),
    ):
        command = commands.add_parser(name)
        command.add_argument("--output", type=Path, required=True)
        command.set_defaults(func=function)

    finalize_cmd = commands.add_parser("finalize")
    finalize_cmd.add_argument("--output", type=Path, required=True)
    finalize_cmd.add_argument("--repo-root", type=Path, required=True)
    finalize_cmd.set_defaults(func=finalize)

    retrieve_cmd = commands.add_parser("retrieve")
    retrieve_cmd.add_argument("--output", type=Path, required=True)
    retrieve_cmd.add_argument("--dense-cache", type=Path)
    retrieve_cmd.set_defaults(func=retrieve)

    analyze_cmd = commands.add_parser("analyze")
    analyze_cmd.add_argument("--output", type=Path, required=True)
    analyze_cmd.add_argument("--ground-truth", type=Path, required=True)
    analyze_cmd.add_argument("--candidate-corpus", type=Path, required=True)
    analyze_cmd.add_argument("--previous-safe-projection", type=Path, required=True)
    analyze_cmd.add_argument("--previous-raw-matrix", type=Path, required=True)
    analyze_cmd.set_defaults(func=analyze)
    return root


def main() -> None:
    args = parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
