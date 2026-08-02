"""Pure deterministic Option B filtering, downweighting and abstention."""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from .schema import (
    SCHEMA_VERSION,
    AbstentionDecision,
    AbstentionReason,
    CanonicalRecord,
    EvidenceAvailability,
    EvidenceState,
    RetrievalCandidate,
    SchemaValidationError,
)
from .visibility import RuntimeAudience, assert_no_label_leakage


class InterventionMode(str, Enum):
    HARD_FILTER = "HARD_FILTER"
    SOFT_DOWNWEIGHT = "SOFT_DOWNWEIGHT"


class ScoreNormalization(str, Enum):
    IDENTITY = "IDENTITY"
    MIN_MAX = "MIN_MAX"


@dataclass(frozen=True, slots=True, kw_only=True)
class InterventionConfig(CanonicalRecord):
    mode: InterventionMode
    tau_filter: float | None
    max_filter_count: int | None
    max_filter_fraction: float | None
    min_retained_documents: int
    lambda_value: float | None
    normalization: ScoreNormalization | None
    schema_version: str = SCHEMA_VERSION

    def __post_init__(self) -> None:
        if not isinstance(self.mode, InterventionMode):
            raise SchemaValidationError("mode must be canonical")
        if self.min_retained_documents < 1:
            raise SchemaValidationError("min_retained_documents must be positive")
        if self.max_filter_count is not None and self.max_filter_count < 0:
            raise SchemaValidationError("max_filter_count must not be negative")
        if self.max_filter_fraction is not None and not 0.0 <= self.max_filter_fraction <= 1.0:
            raise SchemaValidationError("max_filter_fraction must be within [0,1]")
        if self.mode is InterventionMode.HARD_FILTER:
            if self.tau_filter is None or not 0.0 <= self.tau_filter <= 1.0:
                raise SchemaValidationError("hard filtering requires tau_filter in [0,1]")
            if self.max_filter_count is None or self.max_filter_fraction is None:
                raise SchemaValidationError("hard filtering requires both filter budgets")
        if self.mode is InterventionMode.SOFT_DOWNWEIGHT:
            if self.lambda_value is None or self.lambda_value < 0.0:
                raise SchemaValidationError("soft downweighting requires lambda_value >= 0")
            if not isinstance(self.normalization, ScoreNormalization):
                raise SchemaValidationError("score normalization must be explicit")
        if self.schema_version != SCHEMA_VERSION:
            raise SchemaValidationError("unsupported schema_version")


@dataclass(frozen=True, slots=True, kw_only=True)
class InterventionItem(CanonicalRecord):
    document_id: str
    original_score: float
    calibrated_risk: float
    normalized_score: float
    adjusted_score: float
    original_rank: int
    final_rank: int | None
    filtered: bool
    reason: str
    schema_version: str = SCHEMA_VERSION


@dataclass(frozen=True, slots=True, kw_only=True)
class InterventionResult(CanonicalRecord):
    mode: InterventionMode
    items: tuple[InterventionItem, ...]
    retained_document_ids: tuple[str, ...]
    filtered_document_ids: tuple[str, ...]
    abstention: AbstentionDecision | None
    config_hash: str
    schema_version: str = SCHEMA_VERSION


def _risk(candidate: RetrievalCandidate) -> float:
    risk = candidate.calibrated_risk
    if risk is None or not math.isfinite(risk) or not 0.0 <= risk <= 1.0:
        raise SchemaValidationError("INVALID_CALIBRATED_RISK")
    assert_no_label_leakage(candidate.metadata, audience=RuntimeAudience.INTERVENTION)
    return risk


def _original_order(
    candidates: Iterable[RetrievalCandidate],
) -> tuple[RetrievalCandidate, ...]:
    ordered = tuple(
        sorted(candidates, key=lambda item: (-item.retrieval_score, item.document_id))
    )
    if not ordered:
        raise SchemaValidationError("retrieval candidates must not be empty")
    if len({item.document_id for item in ordered}) != len(ordered):
        raise SchemaValidationError("document_id must be unique")
    return ordered


def hard_filter(
    candidates: Iterable[RetrievalCandidate], *, config: InterventionConfig
) -> InterventionResult:
    if config.mode is not InterventionMode.HARD_FILTER:
        raise SchemaValidationError("hard_filter requires HARD_FILTER mode")
    ordered = _original_order(candidates)
    risks = {item.document_id: _risk(item) for item in ordered}
    count_budget = config.max_filter_count or 0
    fraction_budget = math.floor(len(ordered) * (config.max_filter_fraction or 0.0))
    budget = min(count_budget, fraction_budget)
    eligible = sorted(
        (
            item
            for item in ordered
            if risks[item.document_id] >= (config.tau_filter or 0.0)
        ),
        key=lambda item: (-risks[item.document_id], item.document_id),
    )
    filtered_ids = frozenset(item.document_id for item in eligible[:budget])
    retained = tuple(item for item in ordered if item.document_id not in filtered_ids)
    abstention = None
    if len(retained) < config.min_retained_documents:
        abstention = AbstentionDecision(
            reason_code=AbstentionReason.INSUFFICIENT_RETAINED_DOCUMENTS,
            affected_document_ids=tuple(item.document_id for item in ordered),
            required_evidence=("additional low-risk retrieval candidates",),
            safe_next_action="abstain and request a larger audited retrieval set",
        )
    final_ranks = {item.document_id: index for index, item in enumerate(retained, start=1)}
    original_ranks = {item.document_id: index for index, item in enumerate(ordered, start=1)}
    items = tuple(
        InterventionItem(
            document_id=item.document_id,
            original_score=item.retrieval_score,
            calibrated_risk=risks[item.document_id],
            normalized_score=item.retrieval_score,
            adjusted_score=item.retrieval_score,
            original_rank=original_ranks[item.document_id],
            final_rank=final_ranks.get(item.document_id),
            filtered=item.document_id in filtered_ids,
            reason=(
                "risk_at_or_above_threshold_within_budget"
                if item.document_id in filtered_ids
                else "retained_by_threshold_or_budget"
            ),
        )
        for item in ordered
    )
    return InterventionResult(
        mode=config.mode,
        items=items,
        retained_document_ids=tuple(item.document_id for item in retained),
        filtered_document_ids=tuple(sorted(filtered_ids)),
        abstention=abstention,
        config_hash=config.sha256(),
    )


def _normalize(
    ordered: tuple[RetrievalCandidate, ...], normalization: ScoreNormalization
) -> dict[str, float]:
    if normalization is ScoreNormalization.IDENTITY:
        return {item.document_id: item.retrieval_score for item in ordered}
    scores = [item.retrieval_score for item in ordered]
    low, high = min(scores), max(scores)
    if high == low:
        return {item.document_id: 0.5 for item in ordered}
    return {
        item.document_id: (item.retrieval_score - low) / (high - low)
        for item in ordered
    }


def soft_downweight(
    candidates: Iterable[RetrievalCandidate], *, config: InterventionConfig
) -> InterventionResult:
    if config.mode is not InterventionMode.SOFT_DOWNWEIGHT:
        raise SchemaValidationError("soft_downweight requires SOFT_DOWNWEIGHT mode")
    ordered = _original_order(candidates)
    risks = {item.document_id: _risk(item) for item in ordered}
    if config.normalization is None or config.lambda_value is None:  # guarded by config.
        raise SchemaValidationError("soft downweighting configuration is incomplete")
    normalized = _normalize(ordered, config.normalization)
    adjusted = {
        item.document_id: normalized[item.document_id]
        - config.lambda_value * risks[item.document_id]
        for item in ordered
    }
    final = tuple(
        sorted(ordered, key=lambda item: (-adjusted[item.document_id], item.document_id))
    )
    original_ranks = {item.document_id: index for index, item in enumerate(ordered, start=1)}
    final_ranks = {item.document_id: index for index, item in enumerate(final, start=1)}
    items = tuple(
        InterventionItem(
            document_id=item.document_id,
            original_score=item.retrieval_score,
            calibrated_risk=risks[item.document_id],
            normalized_score=normalized[item.document_id],
            adjusted_score=adjusted[item.document_id],
            original_rank=original_ranks[item.document_id],
            final_rank=final_ranks[item.document_id],
            filtered=False,
            reason=(
                "rank_changed_by_explicit_risk_penalty"
                if original_ranks[item.document_id] != final_ranks[item.document_id]
                else "rank_stable_after_explicit_risk_penalty"
            ),
        )
        for item in final
    )
    return InterventionResult(
        mode=config.mode,
        items=items,
        retained_document_ids=tuple(item.document_id for item in final),
        filtered_document_ids=(),
        abstention=None,
        config_hash=config.sha256(),
    )


def missing_evidence_abstention(
    evidence: EvidenceAvailability,
) -> AbstentionDecision | None:
    reason: AbstentionReason | None = None
    required: tuple[str, ...] = ()
    if evidence.temporal is not EvidenceState.AVAILABLE:
        reason = AbstentionReason.MISSING_TEMPORAL_EVIDENCE
        required = ("effective, expiry, repeal and version-relation evidence",)
    elif evidence.provenance is not EvidenceState.AVAILABLE:
        reason = AbstentionReason.MISSING_PROVENANCE_EVIDENCE
        required = ("source and authority evidence",)
    elif not evidence.version_chain_complete:
        reason = AbstentionReason.INCOMPLETE_VERSION_CHAIN
        required = ("complete predecessor and successor chain",)
    elif not evidence.claim_identity_consistent:
        reason = AbstentionReason.INCONSISTENT_CLAIM_IDENTITY
        required = ("consistent entity and claim-family identity",)
    if reason is None:
        return None
    return AbstentionDecision(
        reason_code=reason,
        affected_document_ids=(evidence.document_id,),
        required_evidence=required,
        safe_next_action="abstain and request human-reviewed evidence completion",
    )


__all__ = [
    "InterventionConfig",
    "InterventionItem",
    "InterventionMode",
    "InterventionResult",
    "ScoreNormalization",
    "hard_filter",
    "missing_evidence_abstention",
    "soft_downweight",
]
