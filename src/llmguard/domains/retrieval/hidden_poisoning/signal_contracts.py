"""Structured Pilot4 temporal-version and provenance diagnostic contracts."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum

from .schema import SchemaValidationError


class VersionValidityStatus(str, Enum):
    CURRENT_VALID = "CURRENT_VALID"
    HISTORICAL_VALID = "HISTORICAL_VALID"
    FUTURE_NOT_EFFECTIVE = "FUTURE_NOT_EFFECTIVE"
    REPEALED = "REPEALED"
    SUPERSEDED = "SUPERSEDED"
    VERSION_CONFLICT = "VERSION_CONFLICT"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"


@dataclass(frozen=True, slots=True, kw_only=True)
class VersionFact:
    document_id: str
    subject_id: str
    version_id: str
    publication_date: str | None
    effective_date: str | None
    expiry_date: str | None
    repeal_date: str | None
    predecessor: str | None
    successor: str | None
    amends: tuple[str, ...]
    supersedes: tuple[str, ...]
    authority: str
    validity_interval: tuple[str | None, str | None]
    source_evidence: tuple[str, ...]


def classify_version_fact(
    fact: VersionFact, *, as_of: str, claimed_version_id: str | None = None
) -> VersionValidityStatus:
    """Classify validity from structured relations rather than year overlap."""

    if not fact.source_evidence or not fact.effective_date:
        return VersionValidityStatus.INSUFFICIENT_EVIDENCE
    try:
        point = date.fromisoformat(as_of)
        effective = date.fromisoformat(fact.effective_date)
        expiry = date.fromisoformat(fact.expiry_date) if fact.expiry_date else None
        repeal = date.fromisoformat(fact.repeal_date) if fact.repeal_date else None
    except ValueError as exc:
        raise SchemaValidationError("invalid ISO date in VersionFact") from exc
    if claimed_version_id is not None and claimed_version_id != fact.version_id:
        return VersionValidityStatus.VERSION_CONFLICT
    if point < effective:
        return VersionValidityStatus.FUTURE_NOT_EFFECTIVE
    if repeal is not None and point >= repeal:
        return VersionValidityStatus.REPEALED
    if expiry is not None and point > expiry:
        return VersionValidityStatus.SUPERSEDED if fact.successor else VersionValidityStatus.HISTORICAL_VALID
    if fact.successor and expiry is not None:
        return VersionValidityStatus.HISTORICAL_VALID
    return VersionValidityStatus.CURRENT_VALID


class ProvenanceApplicability(str, Enum):
    AVAILABLE = "AVAILABLE"
    PROVENANCE_NOT_APPLICABLE = "PROVENANCE_NOT_APPLICABLE"


@dataclass(frozen=True, slots=True, kw_only=True)
class StructuredProvenance:
    stated_authority: str | None
    actual_authority: str
    publisher: str
    issuing_authority: str
    source_family: str
    primary_or_repost: str
    joint_issuers: tuple[str, ...]
    authority_level: str
    source_url: str
    source_hash: str


@dataclass(frozen=True, slots=True, kw_only=True)
class ProvenanceAssessment:
    applicability: ProvenanceApplicability
    authority_matches: bool | None
    hosting_equals_issuing: bool
    risk: float | None


def assess_provenance(record: StructuredProvenance) -> ProvenanceAssessment:
    """Treat publisher/host and issuing authority as distinct evidence."""

    if len(record.source_hash) != 64 or not record.source_url.startswith("https://"):
        raise SchemaValidationError("invalid provenance source binding")
    hosting_equals_issuing = record.publisher == record.issuing_authority
    if record.stated_authority is None:
        return ProvenanceAssessment(
            applicability=ProvenanceApplicability.PROVENANCE_NOT_APPLICABLE,
            authority_matches=None,
            hosting_equals_issuing=hosting_equals_issuing,
            risk=None,
        )
    actual = {record.actual_authority, record.issuing_authority, *record.joint_issuers}
    matches = record.stated_authority in actual
    return ProvenanceAssessment(
        applicability=ProvenanceApplicability.AVAILABLE,
        authority_matches=matches,
        hosting_equals_issuing=hosting_equals_issuing,
        risk=0.0 if matches else 1.0,
    )


def hard_negative_adjustment(
    *, historical_valid: bool, legitimate_exception: bool, scope_qualified: bool
) -> float:
    """Return a diagnostic risk deduction without reading a Ground Truth label."""

    return min(1.0, 0.4 * historical_valid + 0.35 * legitimate_exception + 0.25 * scope_qualified)


__all__ = [
    "ProvenanceApplicability",
    "ProvenanceAssessment",
    "StructuredProvenance",
    "VersionFact",
    "VersionValidityStatus",
    "assess_provenance",
    "classify_version_fact",
    "hard_negative_adjustment",
]
