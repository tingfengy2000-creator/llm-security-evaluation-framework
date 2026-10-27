"""Re-execute a frozen, label-blind evidence trace without query/model tuning.

Only sanitized queries/corpus and the locked trace are inputs. This command does
not open Human returns, Oracle identities, QA decisions or construction roles.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import os
from pathlib import Path
from typing import Any


def _read(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("prelock", "corpus", "queries", "trace", "model-cache"):
        parser.add_argument(f"--{name}", type=Path, required=True)
    args = parser.parse_args()
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    sentence_transformer = importlib.import_module("sentence_transformers").SentenceTransformer
    torch = importlib.import_module("torch")

    from llmguard.domains.retrieval.embedding.model_spec import EmbeddingModelSpec
    from llmguard.domains.retrieval.embedding.sentence_transformer_provider import (
        SentenceTransformerEmbeddingProvider,
    )
    from llmguard.domains.retrieval.hidden_poisoning.method_engineering.retrieval_harness import (
        CharacterNgramBM25,
        RetrievalDocument,
    )
    from scripts.research.run_registry_query_robustness_feature_freeze import (
        _rank_rows,
        tree_hash,
    )

    prelock = json.loads(args.prelock.read_text(encoding="utf-8"))
    assert _sha(args.corpus) == prelock["corpus_sha256"]
    assert _sha(args.queries) == prelock["queries_sha256"]
    assert tree_hash(args.model_cache) == prelock["model_tree_sha256"]
    assert args.model_cache.name == "16e5344fbfc7dfbbbe0019d30cec21e2940cb4e1"
    assert prelock["Oracle_or_human_mapping_read_by_this_process"] is False
    corpus, queries, expected = _read(args.corpus), _read(args.queries), _read(args.trace)
    allowed = {"candidate_id", "query_id", "condition", "query_text"}
    assert all(set(query) == allowed for query in queries)
    torch.set_num_threads(4)
    torch.manual_seed(0)
    model = sentence_transformer(
        str(args.model_cache), device="cpu", local_files_only=True, trust_remote_code=False
    )
    spec = EmbeddingModelSpec(
        provider="sentence_transformers",
        model_id="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        revision=args.model_cache.name,
        dimension=384,
        normalize_embeddings=True,
        device="cpu",
        batch_size=16,
        trust_remote_code=False,
        local_files_only=True,
        implementation_version="query_robustness_v1",
        cache_dir_ref="HF_HOME_FROZEN_CACHE",
    )
    provider = SentenceTransformerEmbeddingProvider(spec, model_loader=lambda **_: model)
    sparse = CharacterNgramBM25(
        [
            RetrievalDocument(
                doc_id=doc["evidence_doc_id"], candidate_text=doc["snapshot_text"],
                source_title=doc["title"], primary_subject=doc["source_family"],
            ) for doc in corpus
        ],
        k1=1.2, b=0.75,
    )
    actual = _rank_rows(queries, corpus, sparse, provider)
    assert len({row["run_id"] for row in expected}) == 1
    for row in actual:
        row["run_id"] = expected[0]["run_id"]
    assert actual == expected, "locked scores/ranks changed"
    print(json.dumps({
        "exact_trace_replay": True, "rows": len(actual),
        "trace_sha256": _sha(args.trace), "model_max_seq_length": model.max_seq_length,
        "Oracle_or_labels_loaded": False, "no_fit_or_detector_metrics": True,
    }))


if __name__ == "__main__":
    main()
