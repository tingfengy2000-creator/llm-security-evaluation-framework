"""Model-facing replay and filter interface, without evaluator or filesystem access."""
from __future__ import annotations

import copy
import hashlib
import json
from collections.abc import Callable, Mapping, Sequence
from typing import Any

from ..rag_defense_reconstruction.contracts import validate_packet


def digest(value: Any) -> str:
    """Canonical JSON identity: UTF-8, sorted keys, no NaN, no whitespace."""
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def freeze(packet: dict[str, Any], *, corpus_hash: str, retriever: str,
           requested_top_k: int, trusted_sources: Mapping[str, str]) -> dict[str, Any]:
    """Freeze an ordered retrieval result; authority requires an external text-hash pin.

    The caller obtains trusted_sources from a separately audited registry, never
    from candidate source claims. No assignment of trust occurs in this function.
    """
    validate_packet(packet)
    if (len(corpus_hash) != 64 or any(c not in "0123456789abcdef" for c in corpus_hash)
            or not retriever.strip() or type(requested_top_k) is not int or requested_top_k < 1):
        raise ValueError("RETRIEVAL_IDENTITY_REQUIRED")
    if len(packet["retrieved_chunks"]) > requested_top_k:
        raise ValueError("TOPK_EXCEEDED")
    for chunk in packet["retrieved_chunks"]:
        if chunk["trust_boundary"] == "INDEPENDENT_TRUSTED":
            text_hash = hashlib.sha256(chunk["text"].encode()).hexdigest()
            if trusted_sources.get(chunk["source_id"]) != text_hash:
                raise ValueError("TRUST_REQUIRES_INDEPENDENT_SOURCE_HASH")
    body = {"schema": "chinese5060.snapshot.v1", "packet": copy.deepcopy(packet),
            "corpus_hash": corpus_hash, "retriever": retriever,
            "requested_top_k": requested_top_k,
            "trusted_registry_hash": digest(dict(trusted_sources))}
    return {**body, "topK_snapshot_hash": digest(body)}


def replay(snapshot: dict[str, Any]) -> dict[str, Any]:
    expected = {"schema", "packet", "corpus_hash", "retriever", "requested_top_k",
                "trusted_registry_hash", "topK_snapshot_hash"}
    if set(snapshot) != expected or snapshot["schema"] != "chinese5060.snapshot.v1":
        raise ValueError("SNAPSHOT_SCHEMA")
    body = {k: v for k, v in snapshot.items() if k != "topK_snapshot_hash"}
    if digest(body) != snapshot["topK_snapshot_hash"]:
        raise ValueError("SNAPSHOT_CHANGED")
    validate_packet(snapshot["packet"])
    return copy.deepcopy(snapshot["packet"])


def filtered_context(snapshot: dict[str, Any], retained_indices: Sequence[int]) -> dict[str, Any]:
    """Only deletion is permitted. Preserve surviving text and original TopK order."""
    packet = replay(snapshot)
    chunks = packet["retrieved_chunks"]
    indices = list(retained_indices)
    if (any(type(i) is not int or i < 0 or i >= len(chunks) for i in indices)
            or indices != sorted(set(indices))):
        raise ValueError("FILTER_MUST_PRESERVE_INDICES_AND_ORDER")
    # Operational IDs stay outside the model view. Chunk IDs are citation handles.
    return {"query_text": packet["query_text"], "chunks": [chunks[i] for i in indices]}


def invoke_generator(snapshot: dict[str, Any], retained_indices: Sequence[int], *,
                     generator: Callable[[dict[str, Any]], str]) -> dict[str, str]:
    """Injection seam only; no provider, retry, paid fallback, or answer judge here."""
    context = filtered_context(snapshot, retained_indices)
    if not context["chunks"]:
        return {"status": "ABSTAIN_NO_CONTEXT", "output_hash": digest("ABSTAIN_NO_CONTEXT")}
    answer = generator(context)
    if not isinstance(answer, str) or not answer.strip():
        raise ValueError("GENERATOR_OUTPUT_INVALID")
    return {"status": "GENERATED_UNJUDGED", "output_hash": digest(answer)}
