"""Label-free validation and complete-outcome sealing for the approved B1/B2 run."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .p2_runtime import file_hash


def validate_packets(packets: list[dict[str, Any]]) -> None:
    if len(packets) != 36 or len({p["world_id"] for p in packets}) != 36:
        raise ValueError("EXACT_36_UNIQUE_WORLDS_REQUIRED")
    for packet in packets:
        if set(packet) != {"world_id", "query", "original_TopK_file_sha256", "snapshot_hash", "chunks"}:
            raise ValueError("UNEXPECTED_PACKET_METADATA")
        if len(packet["chunks"]) != 5:
            raise ValueError("FROZEN_TOPK5_REQUIRED")
        for chunk in packet["chunks"]:
            if set(chunk) != {"chunk_id", "text", "content_hash"}:
                raise ValueError("UNEXPECTED_CHUNK_METADATA")
            if hashlib.sha256(chunk["text"].encode()).hexdigest() != chunk["content_hash"]:
                raise ValueError("CHUNK_TEXT_CHANGED")


def validate_removed(texts: list[str], safe: list[str], removed: list[int]) -> None:
    if (len(set(removed)) != len(removed) or any(type(i) is not int or not 0 <= i < len(texts) for i in removed)
            or removed != sorted(removed)):
        raise ValueError("INVALID_REMOVED_INDICES")
    if safe != [text for i, text in enumerate(texts) if i not in removed]:
        raise ValueError("TEXT_OR_ORDER_CHANGED")


def require_pair_seal(run: Path) -> dict[str, Any]:
    seal = json.loads((run / "PAIR_OUTPUT_SEAL.json").read_bytes())
    if seal["worlds"] != 36 or seal["outcomes"] != 72 or seal["status"] != "SEALED_ALL_OUTCOMES":
        raise ValueError("COMPLETE_PAIR_SEAL_REQUIRED")
    for row in seal["records"]:
        p = run / row["path"]
        if not p.resolve().is_relative_to(run.resolve()) or file_hash(p) != row["sha256"]:
            raise ValueError("SEALED_PAIR_OUTPUT_CHANGED")
    return seal
