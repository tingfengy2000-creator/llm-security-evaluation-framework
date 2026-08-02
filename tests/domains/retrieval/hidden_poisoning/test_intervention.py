from __future__ import annotations

import pytest

from llmguard.domains.retrieval.hidden_poisoning import (
    AbstentionReason,
    AbstentionAction,
    EvidenceAvailability,
    EvidenceState,
    InterventionConfig,
    InterventionMode,
    RetrievalCandidate,
    SchemaValidationError,
    ScoreNormalization,
    hard_filter,
    missing_evidence_abstention,
    soft_downweight,
)


def _candidate(document_id: str, score: float, risk: float | None) -> RetrievalCandidate:
    return RetrievalCandidate(
        document_id=document_id,
        retrieval_score=score,
        calibrated_risk=risk,
        metadata={"source_type": "synthetic"},
    )


def _hard_config(**overrides: object) -> InterventionConfig:
    values: dict[str, object] = {
        "mode": InterventionMode.HARD_FILTER,
        "tau_filter": 0.70,
        "max_filter_count": 2,
        "max_filter_fraction": 0.50,
        "min_retained_documents": 1,
        "lambda_value": None,
        "normalization": None,
    }
    values.update(overrides)
    return InterventionConfig(**values)  # type: ignore[arg-type]


def test_hard_filter_uses_threshold_budget_and_stable_tie_break() -> None:
    candidates = (
        _candidate("DOC-B", 0.9, 0.8),
        _candidate("DOC-A", 0.9, 0.8),
        _candidate("DOC-C", 0.7, 0.2),
    )
    result = hard_filter(candidates, config=_hard_config())
    assert result.filtered_document_ids == ("DOC-A",)
    assert result.retained_document_ids == ("DOC-B", "DOC-C")
    assert candidates[0].retrieval_score == 0.9
    assert result.items[0].reason


def test_hard_filter_abstains_when_minimum_retained_is_not_met() -> None:
    candidates = (_candidate("DOC-A", 1.0, 0.9), _candidate("DOC-B", 0.5, 0.8))
    result = hard_filter(
        candidates,
        config=_hard_config(
            max_filter_count=2,
            max_filter_fraction=1.0,
            min_retained_documents=1,
        ),
    )
    assert result.abstention is not None
    assert result.abstention.reason_code is AbstentionReason.INSUFFICIENT_RETAINED_DOCUMENTS
    assert result.abstention.action is AbstentionAction.ABSTAIN
    assert result.abstention.required_evidence
    assert result.abstention.safe_next_action


def test_soft_downweight_formula_and_rank_change_are_explicit() -> None:
    config = InterventionConfig(
        mode=InterventionMode.SOFT_DOWNWEIGHT,
        tau_filter=None,
        max_filter_count=None,
        max_filter_fraction=None,
        min_retained_documents=1,
        lambda_value=2.0,
        normalization=ScoreNormalization.MIN_MAX,
    )
    result = soft_downweight(
        (_candidate("DOC-A", 1.0, 0.9), _candidate("DOC-B", 0.5, 0.0)),
        config=config,
    )
    assert result.retained_document_ids == ("DOC-B", "DOC-A")
    by_id = {item.document_id: item for item in result.items}
    assert by_id["DOC-A"].adjusted_score == pytest.approx(-0.8)
    assert by_id["DOC-B"].adjusted_score == pytest.approx(0.0)
    assert by_id["DOC-A"].original_rank == 1
    assert by_id["DOC-A"].final_rank == 2


@pytest.mark.parametrize("risk", [None, -0.1, 1.1])
def test_invalid_calibrated_risk_is_rejected(risk: float | None) -> None:
    with pytest.raises(SchemaValidationError, match="INVALID_CALIBRATED_RISK"):
        hard_filter((_candidate("DOC-A", 1.0, risk),), config=_hard_config())


@pytest.mark.parametrize(
    ("evidence", "reason"),
    [
        (
            EvidenceAvailability(
                document_id="DOC-A",
                temporal=EvidenceState.MISSING_EVIDENCE,
                provenance=EvidenceState.AVAILABLE,
                version_chain_complete=True,
                claim_identity_consistent=True,
            ),
            AbstentionReason.MISSING_TEMPORAL_EVIDENCE,
        ),
        (
            EvidenceAvailability(
                document_id="DOC-A",
                temporal=EvidenceState.AVAILABLE,
                provenance=EvidenceState.MISSING_EVIDENCE,
                version_chain_complete=True,
                claim_identity_consistent=True,
            ),
            AbstentionReason.MISSING_PROVENANCE_EVIDENCE,
        ),
        (
            EvidenceAvailability(
                document_id="DOC-A",
                temporal=EvidenceState.AVAILABLE,
                provenance=EvidenceState.AVAILABLE,
                version_chain_complete=False,
                claim_identity_consistent=True,
            ),
            AbstentionReason.INCOMPLETE_VERSION_CHAIN,
        ),
        (
            EvidenceAvailability(
                document_id="DOC-A",
                temporal=EvidenceState.AVAILABLE,
                provenance=EvidenceState.AVAILABLE,
                version_chain_complete=True,
                claim_identity_consistent=False,
            ),
            AbstentionReason.INCONSISTENT_CLAIM_IDENTITY,
        ),
    ],
)
def test_missing_evidence_never_defaults_to_clean(
    evidence: EvidenceAvailability, reason: AbstentionReason
) -> None:
    decision = missing_evidence_abstention(evidence)
    assert decision is not None
    assert decision.reason_code is reason
    assert decision.affected_document_ids == ("DOC-A",)


def test_complete_evidence_does_not_force_abstention() -> None:
    evidence = EvidenceAvailability(
        document_id="DOC-A",
        temporal=EvidenceState.AVAILABLE,
        provenance=EvidenceState.AVAILABLE,
        version_chain_complete=True,
        claim_identity_consistent=True,
    )
    assert missing_evidence_abstention(evidence) is None
