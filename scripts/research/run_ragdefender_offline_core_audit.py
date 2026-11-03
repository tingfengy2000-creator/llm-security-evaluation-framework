"""Run unchanged upstream core with an explicit cached embedder; not paper reproduction."""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

UPSTREAM_SHA = "ba2a17efba165d45409114df2d70b030ade1e1b8"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--upstream", type=Path, required=True)
    parser.add_argument("--cached-embedding", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists() or not args.cached_embedding.is_dir():
        raise RuntimeError("NEW_OUTPUT_AND_LOCAL_MODEL_REQUIRED")
    sha = subprocess.check_output(["git", "-C", str(args.upstream), "rev-parse", "HEAD"], text=True).strip()
    if sha != UPSTREAM_SHA or subprocess.check_output(["git", "-C", str(args.upstream), "diff", "--name-only"], text=True).strip():
        raise RuntimeError("PINNED_UNMODIFIED_UPSTREAM_REQUIRED")
    os.environ.update({"HF_HUB_OFFLINE": "1", "TRANSFORMERS_OFFLINE": "1", "CUDA_VISIBLE_DEVICES": "",
                       "TOKENIZERS_PARALLELISM": "false", "PYTHONDONTWRITEBYTECODE": "1"})
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(args.upstream.resolve()))
    import torch
    from sentence_transformers import SentenceTransformer
    from ragdefender import RAGDefender

    torch.set_num_threads(2)
    model = SentenceTransformer(str(args.cached_embedding.resolve()), device="cpu", local_files_only=True, trust_remote_code=False)
    defender = RAGDefender(embedder=model, task_type="single_hop", device="cpu", p=2, m=5)
    results: dict[str, Any] = {}
    for kind, task_type in (("singlehop", "single_hop"), ("multihop", "multi_hop")):
        fixture = json.loads((args.upstream / f"tests/fixtures/legacy_v011_{kind}.json").read_text("utf-8"))
        safe, removed = defender.defend(fixture["query"], fixture["docs"], task_type=task_type, return_indices=True)
        if safe != [text for i, text in enumerate(fixture["docs"]) if i not in removed]:
            raise RuntimeError("INDEX_PRESERVATION_FAILED")
        results[kind] = {"input_count": len(fixture["docs"]), "removed_indices": removed,
                         "retained_count": len(safe), "interpretation": "cached multilingual embedding; not upstream fixture equivalence"}
    # Fictional engineering probe: changing query time must not be represented as
    # a demonstrated weakness of E1 or an independently adjudicated D1 result.
    passages = [
        "甲市2022年管理办法规定，许可证有效期为三年。",
        "甲市2024年管理办法规定，许可证有效期调整为五年。",
        "甲市2022年办法适用于当年受理的许可证申请。",
        "甲市2024年修订办法适用于新受理的许可证申请。",
        "甲市许可管理机构负责受理申请并公开办理流程。",
        "甲市政务服务中心公布许可申请材料清单。",
    ]
    _, old = defender.defend("根据2022年办法，许可证有效期多久？", passages, return_indices=True)
    _, new = defender.defend("根据2024年办法，许可证有效期多久？", passages, return_indices=True)
    results["fictional_query_time_probe"] = {"removed_2022": old, "removed_2024": new,
        "same_removed_indices": old == new, "not_D1_or_security_effectiveness": True}
    try:
        defender.defend("单文档问题", [passages[0]])
    except ValueError as exc:
        results["single_hop_singleton"] = {"status": "UPSTREAM_VALUE_ERROR", "exception": str(exc)}
    else:
        results["single_hop_singleton"] = {"status": "SUPPORTED"}
    files = {p.relative_to(args.cached_embedding).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
             for p in sorted(args.cached_embedding.rglob("*")) if p.is_file()}
    report = {"status": "CORE_ALGORITHM_VERIFIED_WITH_CACHED_NONPAPER_EMBEDDING", "upstream_sha": sha,
        "upstream_version": "0.2.0", "paper_reproduction": False, "author_default_example_verified": False,
        "migration_ready": False, "embedding_id": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        "embedding_revision": args.cached_embedding.name, "embedding_files_sha256": files,
        "embedding_max_seq_length": model.max_seq_length,
        "environment_versions": {name: importlib.metadata.version(name) for name in ("torch", "transformers", "sentence-transformers", "numpy", "scikit-learn", "pandas")},
        "results": results, "paid_calls": 0, "model_downloads": 0, "GPU_used": False}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2)
    print(json.dumps(report, ensure_ascii=True))


if __name__ == "__main__":
    main()
