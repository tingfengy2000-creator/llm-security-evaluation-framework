"""Freeze/test gate, then label-blind VACE F5 prediction. No evaluation entrypoint.

Only the signed candidate-text subset, official corpus, registry and the existing
local model cache are runtime inputs. All detailed artifacts remain Git-ignored.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import os
import platform
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from llmguard.domains.retrieval.hidden_poisoning.method_engineering.adaptive_verification import (
    VERSION, Evidence, digest, verify,
)

MODEL_REVISION = "16e5344fbfc7dfbbbe0019d30cec21e2940cb4e1"
MODEL_TREE = "14be5b8d047148b787bcca877c4b91722c10bc3e1a184ea3aaffe8b6fd3d1fb7"
CANDIDATE_SHA = "6be97906cb9de7587491e84e4c13131a22f93e07b87336772c913534dc7e79e2"
MODULE = "src/llmguard/domains/retrieval/hidden_poisoning/method_engineering/adaptive_verification.py"
SOURCES = [
    MODULE, "scripts/research/run_vace_f5_diagnostic.py", "tests/unit/test_adaptive_verification.py",
    "src/llmguard/domains/retrieval/hidden_poisoning/method_engineering/surface_baseline.py",
    "src/llmguard/domains/retrieval/hidden_poisoning/method_engineering/retrieval_harness.py",
    "src/llmguard/domains/retrieval/embedding/model_spec.py",
    "src/llmguard/domains/retrieval/embedding/sentence_transformer_provider.py",
    "scripts/research/run_registry_query_robustness_feature_freeze.py",
    "src/llmguard/domains/retrieval/hidden_poisoning/method_engineering/development_detection.py",
]
DOC_FIELDS = (
    "evidence_doc_id", "title", "official_url", "source_host", "snapshot_text",
    "snapshot_sha256", "snapshot_text_sha256", "document_id", "version_id", "source_family",
)
META_FIELDS = (
    "issuer", "publisher", "authority_role", "publication_date", "effective_start",
    "effective_end", "current_history_role", "supersedes", "superseded_by",
    "source_family", "metadata_confidence",
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_rows(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text("utf-8").splitlines()]


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as f:
        json.dump(value, f, ensure_ascii=False, indent=2)
        f.write("\n")


def jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def freeze(args: argparse.Namespace) -> None:
    args.output.mkdir(parents=True, exist_ok=True)
    assert not (args.output / "PROTOCOL_FREEZE_V1.json").exists()
    assert sha(args.candidates) == CANDIDATE_SHA
    paths = [*SOURCES, "scripts/research/evaluate_vace_f5_diagnostic.py"]
    # No candidate text, labels or historical per-sample predictions are opened.
    config = {
        "task": "P1-VACE-LITE-V03-F5-IMPLEMENTATION-AND-D1-DIAGNOSTIC-01",
        "run_id": args.output.name, "frozen_utc": now(), "rules_version": VERSION,
        "source_head": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "source_sha256": {p: sha(Path(p)) for p in paths},
        "inputs": {"candidates": sha(args.candidates), "corpus": sha(args.corpus), "registry": sha(args.registry)},
        "conditions": ["V03-F5", "V02-NA-F5"], "top_k": 5,
        "corpus_or_oracle_expansion": False, "learned_verifier": None,
        "retriever": {"query": "FIRST_CANDIDATE_BOOK_TITLE_ELSE_FIRST20+FULL_CANDIDATE", "bm25_ngram": [2, 3], "k1": 1.2, "b": 0.75, "hybrid": "EQUAL_WEIGHT_QUERY_MINMAX", "dense_revision": MODEL_REVISION, "dense_tree": MODEL_TREE, "l2": True, "cpu_threads": 4, "local_only": True},
        "routing": {"V03-F5": "I_CERTIFICATE_ELSE_F_THEN_T_P_J_GAPS_ONCE", "V02-NA-F5": "I_F_T_P_F_REBIND_J_ALWAYS_SAME_FINAL_LOGIC", "max_each_T_P_J": 1, "max_F": 2, "new_body_fetches": 0, "llm_calls": 0},
        "decision": {"policy": "VALID_CONTRADICT_CERTIFICATE_ONLY_FLAGS", "insufficient": "ABSTAIN_REMAINS_FULL_DENOMINATOR", "support": "ALL_ASSERTIONS_EXACT_PAYLOAD_ONLY", "no_continuous_risk_score": True, "threshold_tuning": False},
        "statistics": {"wilson_z": 1.959963984540054, "family_bootstrap_resamples": 2000, "seed": 20261028, "matched": "P_CONTRADICT_AND_C_HN_SUPPORT_STRICT"},
        "privacy": {"candidate_fields": ["candidate_id", "candidate_text"], "doc_fields": DOC_FIELDS, "registry_fields": META_FIELDS, "oracle_or_labels_or_role_paths_accepted": False},
        "risk_review": {"forward": "PASS_WITH_APPROVED_CLOSED_GRAMMAR_LIMITATIONS", "paper": "D1_DEV_ONLY_NO_L0_OR_GENERALIZATION_CLAIM", "unknown_version": "ABSTAIN_NOT_NEWEST_YEAR", "a0": "CUES_ONLY", "no_rule_tuning_after_prediction": True},
        "cost_policy": "ALL120_TOP5_SHARED_PREPARATION_COST_RECORDED_NOT_FREE; ONLINE_BODY_CONSUMPTION_SEPARATE",
        "preflight": json.loads(args.preflight.read_text("utf-8")),
    }
    assert config["preflight"]["all_gates_pass"] is True
    dump(args.output / "PROTOCOL_FREEZE_V1.json", config)
    print(json.dumps({"frozen": True, "sha256": sha(args.output / "PROTOCOL_FREEZE_V1.json"), "no_predictions_or_labels_loaded": True}))


def predict(args: argparse.Namespace) -> None:
    import re

    from llmguard.domains.retrieval.embedding.model_spec import EmbeddingModelSpec
    from llmguard.domains.retrieval.embedding.sentence_transformer_provider import SentenceTransformerEmbeddingProvider
    from llmguard.domains.retrieval.hidden_poisoning.method_engineering.retrieval_harness import CharacterNgramBM25, RetrievalDocument
    from scripts.research.run_registry_query_robustness_feature_freeze import _rank_rows, tree_hash

    protocol = json.loads((args.output / "PROTOCOL_FREEZE_V1.json").read_text("utf-8"))
    for p, expected in protocol["source_sha256"].items():
        assert sha(Path(p)) == expected, f"FROZEN_CODE_CHANGED:{p}"
    for key in ("candidates", "corpus", "registry"):
        assert sha(getattr(args, key)) == protocol["inputs"][key]
    assert args.model_cache.name == MODEL_REVISION
    assert tree_hash(args.model_cache) == MODEL_TREE
    assert not (args.output / "PREDICTION_LOCK_V1.json").exists()
    os.environ.update({"HF_HUB_OFFLINE": "1", "TRANSFORMERS_OFFLINE": "1", "TOKENIZERS_PARALLELISM": "false"})
    torch = importlib.import_module("torch")
    sentence_transformer = importlib.import_module("sentence_transformers").SentenceTransformer
    torch.set_num_threads(4)
    torch.manual_seed(0)
    candidates = read_rows(args.candidates)
    assert len(candidates) == len({c["candidate_id"] for c in candidates}) == 120
    assert all(set(c) == {"candidate_id", "candidate_text"} for c in candidates)
    registry = json.loads(args.registry.read_text("utf-8"))
    metadata = {d["evidence_doc_id"]: {k: d.get(k) for k in META_FIELDS} for d in registry["documents"]}
    # Drop construction filename aliases and unused metadata before retrieval.
    corpus = [{k: d[k] for k in DOC_FIELDS if k in d} for d in read_rows(args.corpus)]
    assert len(corpus) == len({d["evidence_doc_id"] for d in corpus}) == 33
    docs: dict[str, Evidence] = {}
    for d in corpus:
        assert digest(d["snapshot_text"]) == d["snapshot_text_sha256"]
        docs[d["evidence_doc_id"]] = Evidence(d["evidence_doc_id"], d["title"], d["snapshot_text"], d["snapshot_text_sha256"], metadata[d["evidence_doc_id"]])
    jsonl(args.output / "RUNTIME_CORPUS_WHITELIST_V1.jsonl", corpus)
    dump(args.output / "RUNTIME_REGISTRY_WHITELIST_V1.json", metadata)
    queries = []
    for c in candidates:
        names = re.findall(r"《([^》]+)》", c["candidate_text"])
        subject = names[0] if names else c["candidate_text"][:20]
        queries.append({"candidate_id": c["candidate_id"], "query_id": "VACEQ-" + digest(c["candidate_text"])[:16], "condition": "Q_NO_TITLE", "query_text": subject + "。" + c["candidate_text"]})
    jsonl(args.output / "QUERIES_TEXT_ONLY_V1.jsonl", queries)
    tick = time.perf_counter()
    model = sentence_transformer(str(args.model_cache), device="cpu", local_files_only=True, trust_remote_code=False)
    spec = EmbeddingModelSpec(provider="sentence_transformers", model_id="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2", revision=MODEL_REVISION, dimension=384, normalize_embeddings=True, device="cpu", batch_size=16, trust_remote_code=False, local_files_only=True, implementation_version="query_robustness_v1", cache_dir_ref="HF_HOME_FROZEN_CACHE")
    provider = SentenceTransformerEmbeddingProvider(spec, model_loader=lambda **_: model)
    sparse = CharacterNgramBM25([RetrievalDocument(doc_id=d["evidence_doc_id"], candidate_text=d["snapshot_text"], source_title=d["title"], primary_subject=d["source_family"]) for d in corpus], k1=1.2, b=0.75)
    rows = _rank_rows(queries, corpus, sparse, provider)
    preparation_seconds = time.perf_counter() - tick
    tick = time.perf_counter()
    repeat = _rank_rows(queries, corpus, sparse, provider)
    assert rows == repeat, "RETRIEVAL_NOT_DETERMINISTIC"
    rerun_seconds = time.perf_counter() - tick
    # Query/caching identity is content-derived, not the opaque candidate ID.
    aliases = [{**q, "candidate_id": "alias-" + str(i)} for i, q in enumerate(queries)]
    invariant = _rank_rows(aliases, corpus, sparse, provider)
    assert [{k: v for k, v in r.items() if k != "candidate_id"} for r in rows] == [{k: v for k, v in r.items() if k != "candidate_id"} for r in invariant]
    jsonl(args.output / "RETRIEVAL_ALL_RANKS_V1.jsonl", rows)
    bundles: dict[str, list[dict[str, Any]]] = {c["candidate_id"]: [] for c in candidates}
    for r in rows:
        if r["retriever"] == "HYBRID" and r["rank"] <= 5:
            bundles[r["candidate_id"]].append(r)
    predictions = []
    # Counterbalance cheap verifier timing order; shared corpus/index preparation
    # is reported separately and never credited as online adaptive savings.
    for i, c in enumerate(candidates):
        bundle = sorted(bundles[c["candidate_id"]], key=lambda r: r["rank"])
        assert len(bundle) == 5
        evidence = [docs[r["evidence_doc_id"]] for r in bundle]
        for adaptive in ((True, False) if i % 2 == 0 else (False, True)):
            result = verify(c, evidence, adaptive)
            result.update({"run_id": args.output.name, "protocol_sha256": sha(args.output / "PROTOCOL_FREEZE_V1.json"), "retrieval_top5": bundle})
            predictions.append(result)
    jsonl(args.output / "VACE_V03_D1_PREDICTIONS.jsonl", predictions)
    receipt = {"utc": now(), "python": platform.python_version(), "torch": torch.__version__, "sentence_transformers": importlib.import_module("sentence_transformers").__version__, "provider": dict(provider.runtime_metadata()), "frozen_model_tree": MODEL_TREE, "model_max_seq_length": model.max_seq_length, "dense_truncated_documents": sum(len(model.tokenizer(d["title"] + "。" + d["snapshot_text"], truncation=False)["input_ids"]) > model.max_seq_length for d in corpus), "shared_retrieval_preparation_seconds": preparation_seconds, "determinism_rerun_seconds": rerun_seconds, "id_replacement_invariance": True, "same_top5_both_methods": True, "candidates": 120, "rows": len(predictions), "labels_loaded": False, "new_source_or_download": False, "command": ["run_vace_f5_diagnostic.py", "--predict", "<frozen-inputs-and-local-cache>"]}
    dump(args.output / "RUNTIME_RECEIPT_V1.json", receipt)
    dump(args.output / "PREDICTION_LOCK_V1.json", {"locked_utc": now(), "predictions_sha256": sha(args.output / "VACE_V03_D1_PREDICTIONS.jsonl"), "retrieval_sha256": sha(args.output / "RETRIEVAL_ALL_RANKS_V1.jsonl"), "protocol_sha256": sha(args.output / "PROTOCOL_FREEZE_V1.json"), "receipt_sha256": sha(args.output / "RUNTIME_RECEIPT_V1.json"), "rows": len(predictions), "all_predictions_and_routes_before_label_load": True, "evaluator_may_now_load_labels": True})
    print(json.dumps({"prediction_lock_sha256": sha(args.output / "PREDICTION_LOCK_V1.json"), "rows": len(predictions), "no_scores_computed": True}))


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument("--freeze", action="store_true")
    mode.add_argument("--predict", action="store_true")
    for name in ("output", "candidates", "corpus", "registry", "preflight", "model-cache"):
        p.add_argument("--" + name, type=Path, required=True)
    args = p.parse_args()
    (freeze if args.freeze else predict)(args)


if __name__ == "__main__":
    main()
