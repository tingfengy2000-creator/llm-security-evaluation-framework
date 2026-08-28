"""Prospective self-containment gate for new Paper 1 annotation candidates.

The gate is deliberately not applied retroactively to frozen Pilot1/Pilot2
artifacts.  Every candidate created after the owner rule must carry an explicit
subject mention and a human/tool determination that the subject is uniquely
identifiable from the candidate text itself.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .schema import SchemaValidationError


class CandidateAdmissionStatus(str, Enum):
    ELIGIBLE_FOR_ANNOTATION = "ELIGIBLE_FOR_ANNOTATION"
    BROKEN_CANDIDATE = "BROKEN_CANDIDATE"
    LEGACY_PRESERVED_NOT_REEVALUATED = "LEGACY_PRESERVED_NOT_REEVALUATED"


class CandidateAdmissionReason(str, Enum):
    NONE = "NONE"
    MISSING_CONTEXT = "MISSING_CONTEXT"
    LEGACY_PRE_RULE = "LEGACY_PRE_RULE"


@dataclass(frozen=True, slots=True)
class CandidateAdmissionRecord:
    candidate_id: str
    claim_text: str
    subject_mention: str | None
    canonical_subject_identity: str | None
    subject_uniquely_identifiable: bool | None
    status: CandidateAdmissionStatus
    reason: CandidateAdmissionReason
    prospective_rule_applied: bool


def evaluate_candidate_self_containment(
    *,
    candidate_id: str,
    claim_text: str,
    subject_mention: str | None,
    canonical_subject_identity: str | None,
    subject_uniquely_identifiable: bool | None,
    prospective_rule_applied: bool = True,
) -> CandidateAdmissionRecord:
    """Classify a candidate without rewriting or inferring historical records."""

    if not candidate_id.strip() or not claim_text.strip():
        raise SchemaValidationError("candidate_id and claim_text must be non-empty")
    if not prospective_rule_applied:
        return CandidateAdmissionRecord(
            candidate_id=candidate_id,
            claim_text=claim_text,
            subject_mention=subject_mention,
            canonical_subject_identity=canonical_subject_identity,
            subject_uniquely_identifiable=subject_uniquely_identifiable,
            status=CandidateAdmissionStatus.LEGACY_PRESERVED_NOT_REEVALUATED,
            reason=CandidateAdmissionReason.LEGACY_PRE_RULE,
            prospective_rule_applied=False,
        )

    mention = subject_mention.strip() if isinstance(subject_mention, str) else ""
    identity = (
        canonical_subject_identity.strip()
        if isinstance(canonical_subject_identity, str)
        else ""
    )
    self_contained = (
        bool(mention)
        and mention in claim_text
        and bool(identity)
        and subject_uniquely_identifiable is True
    )
    if not self_contained:
        return CandidateAdmissionRecord(
            candidate_id=candidate_id,
            claim_text=claim_text,
            subject_mention=subject_mention,
            canonical_subject_identity=canonical_subject_identity,
            subject_uniquely_identifiable=subject_uniquely_identifiable,
            status=CandidateAdmissionStatus.BROKEN_CANDIDATE,
            reason=CandidateAdmissionReason.MISSING_CONTEXT,
            prospective_rule_applied=True,
        )
    return CandidateAdmissionRecord(
        candidate_id=candidate_id,
        claim_text=claim_text,
        subject_mention=mention,
        canonical_subject_identity=identity,
        subject_uniquely_identifiable=True,
        status=CandidateAdmissionStatus.ELIGIBLE_FOR_ANNOTATION,
        reason=CandidateAdmissionReason.NONE,
        prospective_rule_applied=True,
    )


def require_formal_benchmark_eligibility(record: CandidateAdmissionRecord) -> None:
    """Fail closed unless a prospective candidate passed self-containment."""

    if (
        record.status is not CandidateAdmissionStatus.ELIGIBLE_FOR_ANNOTATION
        or record.reason is not CandidateAdmissionReason.NONE
        or not record.prospective_rule_applied
    ):
        raise SchemaValidationError(
            "candidate is not eligible for formal benchmark: "
            f"{record.status.value} / {record.reason.value}"
        )


__all__ = [
    "CandidateAdmissionReason",
    "CandidateAdmissionRecord",
    "CandidateAdmissionStatus",
    "evaluate_candidate_self_containment",
    "require_formal_benchmark_eligibility",
]
