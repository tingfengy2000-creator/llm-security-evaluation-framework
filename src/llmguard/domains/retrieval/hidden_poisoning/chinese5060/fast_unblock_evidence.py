"""Offline provenance audit for only the bytes scheduled for transfer."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .d1_access import D1_BINDINGS
from .fast_unblock_admission import V2
from .pilot_admission import INPUT_CAP, Stop, sha256, strict_json
from .pilot_inputs import PINNED_INPUTS, PRIVATE_PLAN, P2_SEAL, Cell, checked_bytes
from .pilot_live_admission import PATTERNS

P2 = Path(P2_SEAL).parent
CONTEXT_MARKERS = re.compile(
    r"(?:姓名|收件人|家庭住址|居住地址|身份证号码|联系电话|银行卡号|个人邮箱|验证码|登录密码)\s*[:：]"
)
LANDLINE = re.compile(r"(?<!\d)0\d{2,3}[-－ ]\d{7,8}(?!\d)")
PATTERNS_PLUS = {**PATTERNS, "context_field_marker": CONTEXT_MARKERS, "landline_shape": LANDLINE}


def sealed_chunks(root: Path) -> dict[str, str]:
    seal = strict_json(checked_bytes(root / P2_SEAL, PINNED_INPUTS[P2_SEAL]))
    chunks = {}
    for row in seal["records"]:
        name = row["path"]
        if re.fullmatch(r"w-[a-f0-9]{24}/CHUNKS_PRIVATE\.json", name):
            chunks[(P2 / name).as_posix()] = row["sha256"]
    if len(chunks) != 36:
        raise Stop("SOURCE_CHUNK_SEALS_INCOMPLETE")
    return chunks


def source_path(root: Path) -> Path:
    return root.parents[1] / D1_BINDINGS["sources"].relative_path


def transfer_matrix(root: Path, cells: list[Cell]) -> dict[str, Any]:
    src = D1_BINDINGS["sources"]
    source_raw = checked_bytes(source_path(root), src.sha256)
    known = {}
    for row in strict_json(source_raw)["sources"]:
        if sha256(row["text"].encode()) != row["snapshot_text_sha256"]:
            raise Stop("SOURCE_SNAPSHOT_TEXT_SHA_DRIFT")
        known[row["snapshot_text_sha256"]] = row
    chunks: dict[str, Any] = {}
    for path, digest in sealed_chunks(root).items():
        for row in strict_json(checked_bytes(root / path, digest)):
            if sha256(row["text"].encode()) != row["content_hash"]:
                raise Stop("SEALED_CHUNK_TEXT_SHA_DRIFT")
            previous = chunks.get(row["chunk_id"])
            if previous is not None and previous != row:
                raise Stop("CHUNK_SOURCE_IDENTITY_CONFLICT")
            chunks[row["chunk_id"]] = row
    old_rows = strict_json(checked_bytes(root / PRIVATE_PLAN, PINNED_INPUTS[PRIVATE_PLAN]))
    groups: dict[str, Any] = {}
    high_risk = []
    flagged = dict.fromkeys(PATTERNS_PLUS, 0)
    for cell, row in zip(cells, old_rows, strict=True):
        if cell.request_id != row["request_id"]:
            raise Stop("TRANSFER_CELL_BINDING_DRIFT")
        wire = strict_json(cell.body)
        user = strict_json(wire["messages"][1]["content"])
        observed = set()
        parts = [(None, message["content"]) for message in wire["messages"][:1]] + [(None, user["question"])]
        for cid, context in zip(row["retained_chunk_ids"], user["context"], strict=True):
            chunk = chunks[cid]
            if chunk["text"] != context["text"]:
                raise Stop("TRANSFER_CHUNK_PROJECTION_DRIFT")
            digest = chunk["source_document_hash"]
            origin = known.get(digest)
            if digest not in groups:
                groups[digest] = {
                    "source_hash": digest,
                    "source_authority": origin["metadata"].get("issuer") if origin else chunk["source_authority_claim"],
                    "origin": origin["official_url"] if origin else None,
                    "license_or_usage_basis": ("OFFICIAL_SNAPSHOT_TERMS_AND_PROCESSOR_SCOPE_UNVERIFIED" if origin
                                               else "D1_DEVELOPMENT_ONLY_TRANSFER_BASIS_UNVERIFIED"),
                    "intended_processing_scope": "ONLY_FROZEN_SYSTEM_QUERY_AND_RETAINED_TOPK",
                    "third_party_processor": "ALIBABA_CLOUD_MODEL_STUDIO",
                    "alibaba_region": None, "PII_and_sensitive_result": "CONTEXTUAL_CLEARANCE_REQUIRED",
                    "approval_evidence_hash": None, "decision": "OWNER_INPUT_REQUIRED",
                    "sent_chunk_occurrences": 0,
                }
            groups[digest]["sent_chunk_occurrences"] += 1
            parts.append((digest, context["text"]))
        for digest_or_none, part in parts:
            kinds = sorted(k for k, pattern in PATTERNS_PLUS.items() if pattern.search(part))
            if kinds:
                observed.update(kinds)
                high_risk.append({"request_id": cell.request_id, "source_hash": digest_or_none,
                                  "content_sha256": sha256(part.encode()), "signals": kinds})
        for name in observed:
            flagged[name] += 1
    return {"status": "BLOCKED", "rows": [groups[k] for k in sorted(groups)],
            "transfer_source_hashes": len(groups), "source_snapshots_matched": sum(k in known for k in groups),
            "scope_note": "Actual sent-document inventory is separate from the 16 independent adjudication sources",
            "marked_cells_per_pattern": flagged, "high_risk_review_queue": high_risk,
            "contextual_review_required": True, "source_index_sha256": src.sha256}


def missing_token_proof(cells: list[Cell]) -> dict[str, Any]:
    rows = []
    for cell in cells:
        data = strict_json(cell.body)
        size = sum(len(m["content"].encode()) for m in data["messages"])
        rows.append({
            "request_id": cell.request_id, "world_hash": cell.world_hash, "arm": cell.arm,
            "request_sha256": sha256(cell.body), "tokenizer_or_bound_method_sha256": None,
            "token_count_or_upper_bound": None, "chat_overhead": None, "limit": INPUT_CAP,
            "proof_status": "STRICT_TOKEN_BOUND_UNAVAILABLE", "message_utf8_bytes": size,
        })
    return {"status": "STRICT_TOKEN_BOUND_UNAVAILABLE", "version": V2, "rows": rows,
            "strict_proven_cells": 0, "total_cells": len(cells), "strict_max": None, "strict_total": None,
            "diagnostic_max_message_utf8_bytes": max(r["message_utf8_bytes"] for r in rows),
            "diagnostic_sum_message_utf8_bytes": sum(r["message_utf8_bytes"] for r in rows)}
