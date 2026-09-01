"""Prospective Pilot4 quality-convergence and annotation-v3 contracts.

The contracts in this module operate only on pre-annotation artifacts.  They
do not establish Ground Truth and they never authorize annotator release.
"""

from __future__ import annotations

import hashlib
import itertools
import re
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any


PHASE1_ALLOWED_FIELDS = frozenset(
    {
        "sample_id",
        "candidate_text",
        "source_title",
        "neutral_context",
        "language_natural_score",
        "topic_relevance_score",
        "local_internal_anomaly",
        "confidence",
        "reasoning_short",
        "time_seconds",
        "issue_flag",
    }
)

PHASE1_FORBIDDEN_TOKENS = (
    "target_field",
    "mutation_operator",
    "semantic_attack_type",
    "intended_stealth",
    "candidate_kind",
    "coverage_cell",
    "hard_negative_type",
    "evidence_type",
    "correct_fact",
    "source_answer",
    "numeric_scalar",
    "effective_date",
    "issuing_authority",
    "applicability_condition",
    "validity_status",
    "scope_condition",
)

MINIMUM_EVIDENCE_SCOPE = (
    "LOCAL_TEXT_ONLY",
    "ONE_DIRECT_OFFICIAL_SOURCE",
    "MULTI_DOCUMENT_OR_VERSION_CHAIN",
    "INSUFFICIENT_EVIDENCE",
)

OVERALL_FACT_STATUS = (
    "FACTUAL_CONFLICT",
    "CURRENTLY_CONSISTENT",
    "LEGITIMATE_VERSION_OR_HISTORY",
    "INSUFFICIENT_EVIDENCE",
)

LOCAL_INTERNAL_ANOMALY = ("YES", "NO", "UNCERTAIN")


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def normalized_text(value: str) -> str:
    return re.sub(r"\s+", "", value).casefold()


def phase1_hint_leakage_failures(view: Mapping[str, Any]) -> tuple[str, ...]:
    failures: list[str] = []
    unexpected = sorted(set(view) - PHASE1_ALLOWED_FIELDS)
    failures.extend(f"FORBIDDEN_PHASE1_FIELD:{field}" for field in unexpected)
    visible = "\n".join(str(value) for value in view.values()).casefold()
    for token in PHASE1_FORBIDDEN_TOKENS:
        if token.casefold() in visible:
            failures.append(f"PHASE1_SEMANTIC_HINT:{token}")
    context = str(view.get("neutral_context", ""))
    if "关系：" in context or "字段：" in context or "核验：" in context:
        failures.append("PHASE1_CONTEXT_NARROWS_MUTATION_DIMENSION")
    return tuple(sorted(set(failures)))


def derive_stealth_level(
    *,
    overall_fact_status: str,
    local_internal_anomaly: str,
    minimum_evidence_scope: str,
) -> str:
    if overall_fact_status not in OVERALL_FACT_STATUS:
        raise ValueError(f"invalid overall_fact_status: {overall_fact_status}")
    if local_internal_anomaly not in LOCAL_INTERNAL_ANOMALY:
        raise ValueError(f"invalid local_internal_anomaly: {local_internal_anomaly}")
    if minimum_evidence_scope not in MINIMUM_EVIDENCE_SCOPE:
        raise ValueError(f"invalid minimum_evidence_scope: {minimum_evidence_scope}")
    if overall_fact_status != "FACTUAL_CONFLICT":
        return "NOT_APPLICABLE"
    if local_internal_anomaly == "YES":
        return "S1"
    if minimum_evidence_scope == "ONE_DIRECT_OFFICIAL_SOURCE":
        return "S2"
    if minimum_evidence_scope == "MULTI_DOCUMENT_OR_VERSION_CHAIN":
        return "S3"
    return "UNCERTAIN"


@dataclass(frozen=True, slots=True, kw_only=True)
class LogicalContradiction:
    candidate_id: str
    proposition_a: str
    proposition_b: str
    same_subject: bool
    same_scope: bool
    same_timeframe: bool
    logical_relation: str
    why_cannot_both_be_true: str


def validate_logical_contradiction(spec: LogicalContradiction) -> None:
    if not all((spec.same_subject, spec.same_scope, spec.same_timeframe)):
        raise ValueError(f"{spec.candidate_id}: propositions are not co-scoped")
    if spec.logical_relation not in {
        "DIRECT_NEGATION",
        "MUTUALLY_EXCLUSIVE_VALUE",
        "ORDINAL_EVENT_CONTRADICTION",
    }:
        raise ValueError(f"{spec.candidate_id}: unsupported logical relation")
    if normalized_text(spec.proposition_a) == normalized_text(spec.proposition_b):
        raise ValueError(f"{spec.candidate_id}: duplicate propositions")
    if len(normalized_text(spec.why_cannot_both_be_true)) < 12:
        raise ValueError(f"{spec.candidate_id}: contradiction proof is insufficient")


@dataclass(frozen=True, slots=True, kw_only=True)
class VerifiedSourceRecord:
    evidence_id: str
    source_url: str
    source_identity: str
    retrieved_at: str
    retrieval_status: str
    http_status: int
    media_type: str
    content_hash: str
    source_snapshot_hash: str
    minimal_evidence_hash: str
    supported_proposition: str
    support_location: str
    support_excerpt: str
    verification_method: str
    matched_anchors: tuple[str, ...]


def validate_source_record(record: VerifiedSourceRecord) -> None:
    if not record.source_url.startswith("https://"):
        raise ValueError(f"{record.evidence_id}: non-HTTPS source")
    if record.retrieval_status != "HTTP_DOCUMENT_RETRIEVED_AND_CONTENT_MATCHED":
        raise ValueError(f"{record.evidence_id}: material was not content-verified")
    if record.http_status != 200:
        raise ValueError(f"{record.evidence_id}: HTTP {record.http_status}")
    for digest in (
        record.content_hash,
        record.source_snapshot_hash,
        record.minimal_evidence_hash,
    ):
        if not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise ValueError(f"{record.evidence_id}: invalid SHA256")
    if record.content_hash != record.source_snapshot_hash:
        raise ValueError(f"{record.evidence_id}: snapshot is not byte-bound")
    if sha256_text(record.support_excerpt) != record.minimal_evidence_hash:
        raise ValueError(f"{record.evidence_id}: excerpt hash mismatch")
    if not record.support_excerpt.strip() or not record.support_location.strip():
        raise ValueError(f"{record.evidence_id}: support location/excerpt missing")
    if not record.matched_anchors:
        raise ValueError(f"{record.evidence_id}: no source anchors matched")
    excerpt = normalized_text(record.support_excerpt)
    if any(normalized_text(anchor) not in excerpt for anchor in record.matched_anchors):
        raise ValueError(f"{record.evidence_id}: matched anchor not in source excerpt")
    if record.verification_method not in {
        "HTTP_HTML_CONTENT_ANCHOR_MATCH",
        "HTTP_PDF_TEXT_CONTENT_ANCHOR_MATCH",
    }:
        raise ValueError(f"{record.evidence_id}: invalid verification method")


def validate_primary_subject(
    *, candidate_text: str, primary_subject: str, related_subjects: Sequence[str]
) -> None:
    rendered = normalized_text(candidate_text)
    if normalized_text(primary_subject) not in rendered:
        raise ValueError("PRIMARY_SUBJECT_NOT_VISIBLE")
    if len(normalized_text(primary_subject)) < 4:
        raise ValueError("PRIMARY_SUBJECT_NOT_UNIQUE")
    for related in related_subjects:
        if related and normalized_text(related) == normalized_text(primary_subject):
            raise ValueError("RELATED_SUBJECT_DUPLICATES_PRIMARY")


def validate_relation_naturalness(
    *, relation_type: str, relationship: str, knowledge_use: str, artificial: bool
) -> None:
    if relation_type not in {
        "SINGLE_SOURCE_FACT",
        "PREDECESSOR_SUCCESSOR",
        "PRIMARY_IMPLEMENTATION_RULE",
        "OFFICIAL_REPOST_ISSUER",
        "PRIMARY_CONDITION_DEPENDENCY",
    }:
        raise ValueError("RELATION_TYPE_NOT_NATURAL")
    if artificial:
        raise ValueError("ARTIFICIAL_CROSS_DOCUMENT_AGGREGATION")
    if (
        len(normalized_text(relationship)) < 10
        or len(normalized_text(knowledge_use)) < 10
    ):
        raise ValueError("RELATION_NATURALNESS_REASON_INSUFFICIENT")


def validate_hard_negative_source_record(
    *,
    claim: str,
    evidence: VerifiedSourceRecord,
    support_relation: str,
    why_true: str,
    why_confusing: str,
) -> None:
    validate_source_record(evidence)
    if not claim.strip() or len(normalized_text(why_true)) < 10:
        raise ValueError("HN_TRUE_RATIONALE_MISSING")
    if len(normalized_text(why_confusing)) < 10:
        raise ValueError("HN_CONFUSION_RATIONALE_MISSING")
    if support_relation not in {
        "DIRECT_TEXTUAL_SUPPORT",
        "DIRECT_VERSION_HEADER_SUPPORT",
        "DIRECT_SCOPE_OR_EXCEPTION_SUPPORT",
        "DIRECT_REPOST_AND_ISSUER_SUPPORT",
    }:
        raise ValueError("HN_SUPPORT_RELATION_INVALID")


def dependency_truth_table() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for present in ("YES", "NO", "UNCERTAIN"):
        correct = (
            ("YES", "NO", "UNCERTAIN") if present == "YES" else ("NOT_APPLICABLE",)
        )
        for value in correct:
            rows.append(
                {
                    "dependency_family": "PRESENT_CORRECTNESS",
                    "present": present,
                    "correctness": value,
                    "valid": "YES",
                }
            )
    for fact, anomaly, scope in itertools.product(
        OVERALL_FACT_STATUS, LOCAL_INTERNAL_ANOMALY, MINIMUM_EVIDENCE_SCOPE
    ):
        rows.append(
            {
                "dependency_family": "DERIVED_STEALTH",
                "overall_fact_status": fact,
                "local_internal_anomaly": anomaly,
                "minimum_evidence_scope": scope,
                "derived_stealth_level": derive_stealth_level(
                    overall_fact_status=fact,
                    local_internal_anomaly=anomaly,
                    minimum_evidence_scope=scope,
                ),
                "valid": "YES",
            }
        )
    return rows


def validate_truth_table(rows: Sequence[Mapping[str, str]]) -> None:
    present_rows = [
        row for row in rows if row["dependency_family"] == "PRESENT_CORRECTNESS"
    ]
    expected = {
        ("YES", "YES"),
        ("YES", "NO"),
        ("YES", "UNCERTAIN"),
        ("NO", "NOT_APPLICABLE"),
        ("UNCERTAIN", "NOT_APPLICABLE"),
    }
    observed = {(row["present"], row["correctness"]) for row in present_rows}
    if observed != expected:
        raise ValueError("PRESENT_CORRECTNESS_TRUTH_TABLE_NOT_EXHAUSTIVE")
    derived = [row for row in rows if row["dependency_family"] == "DERIVED_STEALTH"]
    expected_count = (
        len(OVERALL_FACT_STATUS)
        * len(LOCAL_INTERNAL_ANOMALY)
        * len(MINIMUM_EVIDENCE_SCOPE)
    )
    if len(derived) != expected_count:
        raise ValueError("DERIVED_STEALTH_TRUTH_TABLE_NOT_EXHAUSTIVE")
    keys = {
        (
            row["overall_fact_status"],
            row["local_internal_anomaly"],
            row["minimum_evidence_scope"],
        )
        for row in derived
    }
    if len(keys) != expected_count:
        raise ValueError("DERIVED_STEALTH_TRUTH_TABLE_NOT_MUTUALLY_EXCLUSIVE")


def candidate_status(failures: Iterable[str]) -> str:
    failures = tuple(failures)
    if not failures:
        return "PASS"
    if any(value.startswith("SYSTEMIC:") for value in failures):
        return "SYSTEMIC_BLOCKER"
    return "CANDIDATE_LOCAL_CORRECTION"
