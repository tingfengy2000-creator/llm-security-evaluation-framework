"""Public-source registry contracts for the Paper 1 Pilot1 feasibility audit.

The registry stores identities, hashes, relationship evidence, and release
decisions.  Source bodies remain outside Git.
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from enum import Enum
from typing import Iterable
from urllib.parse import urlparse

from .schema import SCHEMA_VERSION, CanonicalRecord, SchemaValidationError


_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2}:\d{2}Z)?$")


class SourceDomain(str, Enum):
    HUMAN_RESOURCES = "HUMAN_RESOURCES_AND_INSTITUTIONAL_MANAGEMENT"
    FINANCE_RESEARCH = "FINANCE_PROCUREMENT_AND_RESEARCH_MANAGEMENT"
    EDUCATION_RESEARCH = "EDUCATION_AND_RESEARCH"


class TermsOrLicenseStatus(str, Enum):
    NOT_EXPLICITLY_VERIFIED = "NOT_EXPLICITLY_VERIFIED"
    EXPLICIT_PUBLIC_LICENSE = "EXPLICIT_PUBLIC_LICENSE"


class RedistributionStatus(str, Enum):
    NOT_AUTHORIZED_FOR_REPUBLICATION = "NOT_AUTHORIZED_FOR_REPUBLICATION"
    REDISTRIBUTION_AUTHORIZED = "REDISTRIBUTION_AUTHORIZED"


class ReleaseClassification(str, Enum):
    PUBLIC_FULL = "PUBLIC_FULL"
    PUBLIC_REDACTED = "PUBLIC_REDACTED"
    HASH_ONLY = "HASH_ONLY"
    INTERNAL_ONLY = "INTERNAL_ONLY"


@dataclass(frozen=True, slots=True, kw_only=True)
class SourceArtifact(CanonicalRecord):
    source_chain_id: str
    domain: SourceDomain
    source_title: str
    publisher: str
    official_url: str
    retrieval_utc: str
    document_version_id: str
    publication_date: str
    effective_at: str | None
    expires_at: str | None
    repealed_at: str | None
    predecessor: str | None
    successor: str | None
    supersedes: tuple[str, ...]
    amends: tuple[str, ...]
    source_sha256: str
    local_artifact_sha256: str
    terms_or_license_status: TermsOrLicenseStatus
    redistribution_status: RedistributionStatus
    release_classification: ReleaseClassification
    evidence_notes: str
    artifact_name: str
    schema_version: str = SCHEMA_VERSION

    def __post_init__(self) -> None:
        if not self.source_chain_id or not self.document_version_id:
            raise SchemaValidationError("source and version identities are required")
        if not isinstance(self.domain, SourceDomain):
            raise SchemaValidationError("source domain must be canonical")
        if not self.source_title or not self.publisher or not self.evidence_notes:
            raise SchemaValidationError("source identity and relationship evidence are required")
        parsed = urlparse(self.official_url)
        if parsed.scheme != "https" or not parsed.netloc:
            raise SchemaValidationError("official_url must be a public HTTPS URL")
        for name in ("retrieval_utc", "publication_date"):
            if _DATE.fullmatch(getattr(self, name)) is None:
                raise SchemaValidationError(f"{name} must use an ISO date or UTC timestamp")
        for name in ("effective_at", "expires_at", "repealed_at"):
            value = getattr(self, name)
            if value is not None and _DATE.fullmatch(value) is None:
                raise SchemaValidationError(f"{name} must use an ISO date or UTC timestamp")
        for name in ("source_sha256", "local_artifact_sha256"):
            if _SHA256.fullmatch(getattr(self, name)) is None:
                raise SchemaValidationError(f"{name} must be a lowercase SHA256")
        if not isinstance(self.terms_or_license_status, TermsOrLicenseStatus):
            raise SchemaValidationError("terms_or_license_status must be canonical")
        if not isinstance(self.redistribution_status, RedistributionStatus):
            raise SchemaValidationError("redistribution_status must be canonical")
        if not isinstance(self.release_classification, ReleaseClassification):
            raise SchemaValidationError("release_classification must be canonical")
        if (
            self.terms_or_license_status is TermsOrLicenseStatus.NOT_EXPLICITLY_VERIFIED
            and self.release_classification is ReleaseClassification.PUBLIC_FULL
        ):
            raise SchemaValidationError("PUBLIC_FULL requires explicit redistribution evidence")
        if "/" in self.artifact_name or "\\" in self.artifact_name or not self.artifact_name:
            raise SchemaValidationError("artifact_name must be a private basename")
        if self.schema_version != SCHEMA_VERSION:
            raise SchemaValidationError("unsupported schema_version")


@dataclass(frozen=True, slots=True, kw_only=True)
class SourceChain(CanonicalRecord):
    source_chain_id: str
    domain: SourceDomain
    artifacts: tuple[SourceArtifact, ...]
    relationship_type: str
    relationship_evidence: str
    schema_version: str = SCHEMA_VERSION

    def __post_init__(self) -> None:
        if len(self.artifacts) < 2:
            raise SchemaValidationError("a source chain requires at least two versions")
        if any(
            artifact.source_chain_id != self.source_chain_id or artifact.domain is not self.domain
            for artifact in self.artifacts
        ):
            raise SchemaValidationError("source-chain identities must be consistent")
        version_ids = {artifact.document_version_id for artifact in self.artifacts}
        if len(version_ids) != len(self.artifacts):
            raise SchemaValidationError("document_version_id must be unique within a chain")
        if not self.relationship_type or not self.relationship_evidence:
            raise SchemaValidationError("version relationship evidence is required")
        linked = any(
            artifact.predecessor
            or artifact.successor
            or artifact.supersedes
            or artifact.amends
            or artifact.repealed_at
            for artifact in self.artifacts
        )
        if not linked:
            raise SchemaValidationError("source chain must encode a temporal or version relation")
        if self.schema_version != SCHEMA_VERSION:
            raise SchemaValidationError("unsupported schema_version")


PILOT1_A_GATE_NAMES = (
    "twelve_independent_source_chains",
    "at_least_three_domains",
    "at_least_four_chains_per_domain",
    "verifiable_version_or_temporal_relation",
    "official_url_per_source",
    "local_sha256_per_artifact",
    "relationship_evidence_per_chain",
    "terms_status_per_source",
    "release_classification_per_source",
    "raw_content_excluded_from_git",
    "schema_validation",
    "label_isolation",
    "independence_group_construction",
    "no_cross_group_identity_conflict",
    "evidence_index_complete",
)


def evaluate_pilot1_a(
    chains: Iterable[SourceChain],
    *,
    raw_content_excluded_from_git: bool,
    label_isolation_passed: bool,
    independence_groups_passed: bool,
    no_cross_group_identity_conflict: bool,
    evidence_index_complete: bool,
) -> dict[str, bool]:
    ordered = tuple(chains)
    counts = Counter(chain.domain for chain in ordered)
    artifacts = tuple(artifact for chain in ordered for artifact in chain.artifacts)
    unique_chain_ids = {chain.source_chain_id for chain in ordered}
    results = {
        "twelve_independent_source_chains": len(ordered) == 12 and len(unique_chain_ids) == 12,
        "at_least_three_domains": len(counts) >= 3,
        "at_least_four_chains_per_domain": bool(counts) and all(count >= 4 for count in counts.values()),
        "verifiable_version_or_temporal_relation": all(len(chain.artifacts) >= 2 for chain in ordered),
        "official_url_per_source": all(urlparse(item.official_url).scheme == "https" for item in artifacts),
        "local_sha256_per_artifact": all(_SHA256.fullmatch(item.local_artifact_sha256) for item in artifacts),
        "relationship_evidence_per_chain": all(bool(chain.relationship_evidence) for chain in ordered),
        "terms_status_per_source": all(isinstance(item.terms_or_license_status, TermsOrLicenseStatus) for item in artifacts),
        "release_classification_per_source": all(isinstance(item.release_classification, ReleaseClassification) for item in artifacts),
        "raw_content_excluded_from_git": raw_content_excluded_from_git,
        "schema_validation": True,
        "label_isolation": label_isolation_passed,
        "independence_group_construction": independence_groups_passed,
        "no_cross_group_identity_conflict": no_cross_group_identity_conflict,
        "evidence_index_complete": evidence_index_complete,
    }
    if tuple(results) != PILOT1_A_GATE_NAMES:
        raise AssertionError("Pilot1-A gate contract drifted")
    return results


__all__ = [
    "PILOT1_A_GATE_NAMES",
    "RedistributionStatus",
    "ReleaseClassification",
    "SourceArtifact",
    "SourceChain",
    "SourceDomain",
    "TermsOrLicenseStatus",
    "evaluate_pilot1_a",
]
