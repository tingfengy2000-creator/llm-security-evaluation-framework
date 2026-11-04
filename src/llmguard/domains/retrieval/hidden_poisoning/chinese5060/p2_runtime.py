"""Offline T0 chunking and source identity. No evaluator/labels/QA imports."""
from __future__ import annotations

import hashlib
import socket
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from .snapshots import digest


def file_hash(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


@contextmanager
def network_denied(events: list[str]):
    """Block Python socket connection/DNS calls; not an OS sandbox claim."""
    targets = [(socket.socket, "connect"), (socket.socket, "connect_ex"),
               (socket, "create_connection"), (socket, "getaddrinfo")]
    original = [(obj, name, getattr(obj, name)) for obj, name in targets]

    def deny(*args: Any, **kwargs: Any) -> Any:
        events.append("DENIED_NETWORK_ATTEMPT")
        raise RuntimeError("NETWORK_FORBIDDEN")
    try:
        for obj, name in targets:
            setattr(obj, name, deny)
        yield
    finally:
        for obj, name, function in original:
            setattr(obj, name, function)


def chunk_world(world: dict[str, Any], tokenizer: Any, window: int = 96,
                overlap: int = 16) -> list[dict[str, Any]]:
    """Original character slices, token-offset windows, rechecked encoder lengths."""
    if window != 96 or overlap != 16:
        raise ValueError("FROZEN_CHUNK_PARAMETERS_REQUIRED")
    if digest(world["documents"]) != world["corpus_hash"]:
        raise ValueError("WORLD_CORPUS_CHANGED")
    chunks = []
    for doc in world["documents"]:
        if hashlib.sha256(doc["text"].encode()).hexdigest() != doc["content_sha256"]:
            raise ValueError("DOCUMENT_CHANGED")
        if doc["trust_boundary"] != "UNVERIFIED":
            raise ValueError("T0_UNVERIFIED_ONLY")
        encoded = tokenizer(doc["text"], add_special_tokens=False, truncation=False, return_offsets_mapping=True)
        ids, offsets = encoded["input_ids"], encoded["offset_mapping"]
        if not ids or len(ids) != len(offsets):
            raise ValueError("NO_USABLE_TOKEN_OFFSETS")
        for index, start in enumerate(range(0, len(ids), window - overlap)):
            end = min(start + window, len(ids))
            a, b = offsets[start][0], offsets[end - 1][1]
            if not 0 <= a < b <= len(doc["text"]):
                raise ValueError("INVALID_CHARACTER_OFFSETS")
            text = doc["text"][a:b]
            content_tokens = len(tokenizer(text, add_special_tokens=False, truncation=False)["input_ids"])
            encoder_tokens = len(tokenizer(text, add_special_tokens=True, truncation=False)["input_ids"])
            if content_tokens > window or encoder_tokens > 128:
                raise ValueError("TOKEN_WINDOW_REENCODING_OVERFLOW_NO_AUTO_REPAIR")
            uid = "ch-" + digest([world["world_id"], doc["document_id"], a, b, text])[:32]
            chunks.append({"chunk_id": uid, "parent_doc_id": doc["document_id"], "text": text,
                "content_hash": hashlib.sha256(text.encode()).hexdigest(), "source_id": doc["source_id"],
                "source_document_hash": doc["content_sha256"], "source_authority_claim": doc["authority_claim"],
                "publication_time": doc["publication_time"], "effective_time": doc["effective_time"],
                "trust_boundary": "UNVERIFIED", "chunk_index": index,
                "source_token_start": start, "source_token_end": end, "char_start": a, "char_end": b,
                "content_tokens": content_tokens, "encoder_tokens": encoder_tokens})
            if end == len(ids):
                break
    if len({c["chunk_id"] for c in chunks}) != len(chunks):
        raise ValueError("DUPLICATE_CHUNK")
    return chunks


def canonical_hits(hits: Any) -> list[dict[str, Any]]:
    values = sorted(hits, key=lambda h: (-h.similarity, h.distance, h.doc_id))
    return [{"rank": i + 1, "chunk_id": h.doc_id, "distance": h.distance,
             "similarity": h.similarity, "metadata": dict(h.metadata)} for i, h in enumerate(values)]
