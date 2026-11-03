"""CONTROL PLANE / EVALUATOR ONLY: outcome-independent sample freeze and audit."""
from __future__ import annotations

import hashlib
from collections import Counter, defaultdict
from typing import Any

TASK = "PAPER1-RAG-DEFENSE-RECONSTRUCTION-01"
SEED = 20261104
ROLES = frozenset({"CLEAN_CURRENT", "POISON", "HARD_NEGATIVE"})


def select_groups(labels: list[dict[str, Any]]) -> list[str]:
    """Four per signed S stratum, sorted by predeclared hash; no predictions input."""
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in labels:
        groups[row["group_evaluation_only"]].append(row)
    strata: dict[str, list[str]] = defaultdict(list)
    for group, members in groups.items():
        if len(members) != 3 or {m["role_evaluation_only"] for m in members} != ROLES:
            raise ValueError("SIGNED_COMPLETE_TRIPLET_REQUIRED")
        s_values = {m["derived_s_evaluation_only"] for m in members}
        if len(s_values) != 1:
            raise ValueError("INCONSISTENT_SIGNED_S")
        s = next(iter(s_values))
        if s not in {"S1", "S2", "S3"}:
            raise ValueError("UNKNOWN_SIGNED_S")
        strata[s].append(group)
    selected = []
    for s in ("S1", "S2", "S3"):
        if len(strata[s]) < 4:
            raise ValueError("INSUFFICIENT_STRATUM")
        selected.extend(sorted(strata[s], key=lambda g: hashlib.sha256(
            f"{TASK}|{SEED}|{s}|{g}".encode()).hexdigest())[:4])
    return selected


def audit_existing_packets(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Describe preparation gaps, never invent a question or a gold answer."""
    chunks = [e for row in rows for e in row["evidence"]]
    counters: Counter[str] = Counter()
    fields = ("issuer", "publisher", "publication_date", "effective_start", "effective_end")
    for e in chunks:
        metadata = e["metadata"]
        for field in fields:
            value = metadata.get(field)
            if value is None or value == "":
                counters[field + "_missing"] += 1
            if isinstance(value, str) and "\ufffd" in value:
                counters[field + "_replacement_char"] += 1
        counters["version_role_unknown"] += metadata.get("current_history_role") in (None, "UNKNOWN", "")
    return {
        "status": "NEEDS_ADJUDICATION",
        "candidates": len(rows), "evidence_occurrences": len(chunks),
        "unique_evidence_documents": len({e["document_uid"] for e in chunks}),
        "query_text_present": sum(bool(row.get("query_text")) for row in rows),
        "independent_QA_answer_adjudication_present": sum(bool(row.get("answer_adjudication_ref")) for row in rows),
        "metadata_gaps": dict(sorted(counters.items())),
        "inference": "Candidate verification inputs do not establish unique query-level QA truth; absence applies to audited bundle, not all possible source material.",
    }
