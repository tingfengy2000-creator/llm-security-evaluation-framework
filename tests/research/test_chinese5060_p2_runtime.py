from __future__ import annotations

import hashlib
import importlib.util
import json
import socket
from pathlib import Path
from types import SimpleNamespace

import pytest

from llmguard.domains.retrieval.hidden_poisoning.chinese5060.p2_runtime import canonical_hits, chunk_world, network_denied
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.snapshots import digest


class CharTokenizer:
    def __call__(self, text, add_special_tokens=False, truncation=False, return_offsets_mapping=False):
        result = {"input_ids": list(range(len(text) + (2 if add_special_tokens else 0)))}
        if return_offsets_mapping:
            result["offset_mapping"] = [(i, i + 1) for i in range(len(text))]
        return result


def world(text="甲" * 200):
    docs = [{"document_id": "d-fixture", "source_id": "s-fixture", "text": text,
        "content_sha256": hashlib.sha256(text.encode()).hexdigest(), "trust_boundary": "UNVERIFIED",
        "authority_claim": None, "publication_time": None, "effective_time": None}]
    return {"world_id": "w-fixture", "documents": docs, "corpus_hash": digest(docs)}


def test_chunking_preserves_source_slices_and_exact_overlap():
    w = world()
    chunks = chunk_world(w, CharTokenizer())
    assert len(chunks) == 3
    assert [(c["source_token_start"], c["source_token_end"]) for c in chunks] == [(0, 96), (80, 176), (160, 200)]
    assert all(c["text"] == w["documents"][0]["text"][c["char_start"]:c["char_end"]] for c in chunks)
    assert all(c["content_tokens"] <= 96 and c["encoder_tokens"] <= 128 for c in chunks)


def test_exact_window_does_not_add_duplicate_tail():
    assert len(chunk_world(world("甲" * 96), CharTokenizer())) == 1


def test_changed_corpus_and_trusted_upgrade_are_rejected():
    w = world()
    w["documents"][0]["text"] = "改"
    with pytest.raises(ValueError, match="WORLD_CORPUS_CHANGED"):
        chunk_world(w, CharTokenizer())
    w = world()
    w["documents"][0]["trust_boundary"] = "INDEPENDENT_TRUSTED"
    w["corpus_hash"] = digest(w["documents"])
    with pytest.raises(ValueError, match="T0_UNVERIFIED_ONLY"):
        chunk_world(w, CharTokenizer())


def test_frozen_parameters_are_not_adjusted_to_pass():
    with pytest.raises(ValueError, match="FROZEN_CHUNK_PARAMETERS"):
        chunk_world(world(), CharTokenizer(), window=95)


def test_network_guard_denies_and_restores_without_real_connection():
    events = []
    original = socket.create_connection
    with network_denied(events):
        with pytest.raises(RuntimeError, match="NETWORK_FORBIDDEN"):
            socket.create_connection(("forbidden.example", 443))
    assert socket.create_connection is original and events == ["DENIED_NETWORK_ATTEMPT"]


def test_hits_use_stable_order_and_do_not_rewrite_scores():
    hits = [SimpleNamespace(doc_id=uid, similarity=0.75, distance=0.25, metadata={}) for uid in ("b", "a")]
    assert canonical_hits(hits) == [
        {"rank": 1, "chunk_id": "a", "similarity": 0.75, "distance": 0.25, "metadata": {}},
        {"rank": 2, "chunk_id": "b", "similarity": 0.75, "distance": 0.25, "metadata": {}}]


def evaluator_module():
    spec = importlib.util.spec_from_file_location("sealed_eval_test", Path("scripts/research/evaluate_chinese5060_p2.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_evaluator_rejects_unsealed_run_before_label_access(tmp_path):
    with pytest.raises(ValueError, match="OUTPUT_SEAL_REQUIRED_BEFORE_LABEL_ACCESS"):
        evaluator_module().require_sealed(tmp_path)


def test_evaluator_rejects_changed_output_before_label_access(tmp_path):
    (tmp_path / "fixture.txt").write_bytes(b"changed")
    (tmp_path / "OUTPUT_SEAL.json").write_text(json.dumps({"worlds": 36, "status": "SEALED_ALL_WORLD_OUTCOMES",
        "network_attempts": [], "records": [{"path": "fixture.txt", "sha256": "0" * 64}]}), encoding="utf-8")
    with pytest.raises(ValueError, match="SEALED_OUTPUT_CHANGED"):
        evaluator_module().require_sealed(tmp_path)
