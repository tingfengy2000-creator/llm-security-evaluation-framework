"""Deterministic, label-isolated Pilot3 signal diagnostics.

These signals are engineering probes, not a trained detector or paper result.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Mapping

from .visibility import RuntimeAudience, assert_no_label_leakage

VIEW_NAMES = (
    "SEMANTIC",
    "ENTITY_CLAIM",
    "PROVENANCE",
    "TEMPORAL_VERSION",
    "RETRIEVAL_BEHAVIOR",
)

_NUMBER = re.compile(r"\d{4}|\d+(?:\.\d+)?")
_AUTHORITY = re.compile(r"国务院|全国人大(?:常委会)?|教育部|财政部|人力资源社会保障部|监察部")


@dataclass(frozen=True, slots=True)
class SignalRecord:
    candidate_id: str
    query_id: str
    view_name: str
    raw_signal: Mapping[str, object]
    normalized_signal: float | None
    direction: str
    evidence: tuple[str, ...]
    available: str
    missing_reason: str | None
    runtime_ms: float

    def canonical_payload(self) -> dict[str, object]:
        return asdict(self)


def _tokens(text: str) -> set[str]:
    compact = re.sub(r"\s+", "", text)
    return {compact[index : index + 2] for index in range(max(0, len(compact) - 1))}


def _jaccard(left: str, right: str) -> float:
    a, b = _tokens(left), _tokens(right)
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b) if a | b else 0.0


def extract_signals(visible: Mapping[str, object]) -> tuple[SignalRecord, ...]:
    """Extract five separable signals from detector-visible fields only."""

    assert_no_label_leakage(visible, audience=RuntimeAudience.DETECTOR)
    required = {"candidate_id", "candidate_text", "version_context", "source_title", "publisher", "query_text"}
    missing = required - set(visible)
    if missing:
        raise ValueError(f"missing visible signal fields: {sorted(missing)}")
    candidate_id = str(visible["candidate_id"])
    query_id = f"Q-{candidate_id}"
    candidate = str(visible["candidate_text"])
    context = str(visible["version_context"])
    title = str(visible["source_title"])
    publisher = str(visible["publisher"])
    query = str(visible["query_text"])
    semantic_similarity = _jaccard(candidate, context + title)
    semantic = SignalRecord(
        candidate_id, query_id, "SEMANTIC",
        {"bigram_jaccard": semantic_similarity}, 1.0 - semantic_similarity,
        "HIGHER_MEANS_GREATER_TEXT_REFERENCE_DIVERGENCE",
        ("candidate_text", "version_context", "source_title"), "AVAILABLE", None, 0.0,
    )

    candidate_numbers = set(_NUMBER.findall(candidate))
    reference_numbers = set(_NUMBER.findall(context + title))
    unmatched = sorted(candidate_numbers - reference_numbers)
    denominator = max(1, len(candidate_numbers))
    entity = SignalRecord(
        candidate_id, query_id, "ENTITY_CLAIM",
        {"candidate_numbers": sorted(candidate_numbers), "unmatched_numbers": unmatched},
        len(unmatched) / denominator,
        "HIGHER_MEANS_MORE_NUMERIC_OR_DATE_MISMATCH",
        ("candidate_text", "version_context"), "AVAILABLE", None, 0.0,
    )

    claimed = sorted(set(_AUTHORITY.findall(candidate)))
    if claimed:
        mismatched = [item for item in claimed if item not in publisher]
        provenance = SignalRecord(
            candidate_id, query_id, "PROVENANCE",
            {"claimed_authorities": claimed, "publisher": publisher, "mismatched": mismatched},
            len(mismatched) / len(claimed),
            "HIGHER_MEANS_STATED_AUTHORITY_DIFFERS_FROM_SOURCE_PUBLISHER",
            ("candidate_text", "publisher"), "AVAILABLE", None, 0.0,
        )
    else:
        provenance = SignalRecord(
            candidate_id, query_id, "PROVENANCE", {"claimed_authorities": []}, None,
            "NOT_APPLICABLE_WHEN_NO_AUTHORITY_CLAIM", ("candidate_text",),
            "NOT_APPLICABLE", "NO_STATED_AUTHORITY_CLAIM", 0.0,
        )

    candidate_years = {item for item in candidate_numbers if len(item) == 4}
    context_years = {item for item in reference_numbers if len(item) == 4}
    year_mismatch = sorted(candidate_years - context_years)
    temporal = SignalRecord(
        candidate_id, query_id, "TEMPORAL_VERSION",
        {"candidate_years": sorted(candidate_years), "reference_years": sorted(context_years), "unmatched_years": year_mismatch},
        len(year_mismatch) / max(1, len(candidate_years)),
        "HIGHER_MEANS_VERSION_TIME_NOT_SUPPORTED_BY_VISIBLE_CONTEXT",
        ("candidate_text", "version_context", "source_title"), "AVAILABLE", None, 0.0,
    )

    retrieval_overlap = _jaccard(query, candidate)
    retrieval = SignalRecord(
        candidate_id, query_id, "RETRIEVAL_BEHAVIOR",
        {"diagnostic_query_overlap": retrieval_overlap}, retrieval_overlap,
        "HIGHER_MEANS_GREATER_DIAGNOSTIC_QUERY_EXPOSURE",
        ("query_text", "candidate_text"), "AVAILABLE", None, 0.0,
    )
    return semantic, entity, provenance, temporal, retrieval


__all__ = ["SignalRecord", "VIEW_NAMES", "extract_signals"]
