"""Annotation-candidate and blinded packet contracts for Paper 1 Pilot1."""

from __future__ import annotations

import hashlib
import random
from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from .attacks import MutationSpec
from .schema import (
    SCHEMA_VERSION,
    AttackType,
    CanonicalRecord,
    HardNegativeType,
    SchemaValidationError,
    StealthLevel,
    canonical_sha256,
)
from .visibility import RuntimeAudience, assert_no_label_leakage


class CandidateKind(str, Enum):
    CLEAN_CURRENT = "CLEAN_CURRENT"
    POISON_MUTATION = "POISON_MUTATION"
    MATCHED_HARD_NEGATIVE = "MATCHED_HARD_NEGATIVE"


class CandidateStatus(str, Enum):
    ANNOTATION_CANDIDATE = "ANNOTATION_CANDIDATE"


class AdjudicationStatus(str, Enum):
    NOT_ADJUDICATED = "NOT_ADJUDICATED"


class BenchmarkStatus(str, Enum):
    NOT_BENCHMARK = "NOT_BENCHMARK"


class PacketKind(str, Enum):
    FACT_AND_VERSION = "FACT_AND_VERSION_REVIEW"
    STEALTH_AND_NATURALNESS = "STEALTH_AND_NATURALNESS_REVIEW"


@dataclass(frozen=True, slots=True, kw_only=True)
class AnnotationCandidate(CanonicalRecord):
    candidate_id: str
    source_record_id: str
    source_chain_id: str
    domain: str
    candidate_kind: CandidateKind
    claim_text: str
    version_context: str
    source_title: str
    official_url: str
    mutation_spec: MutationSpec | None = None
    candidate_stealth_level: StealthLevel | None = None
    original_claim_hash: str | None = None
    mutated_claim_hash: str | None = None
    fact_change_description: str | None = None
    naturalness_review_required: bool = True
    factual_review_required: bool = True
    stealth_review_required: bool = True
    hard_negative_type: HardNegativeType | None = None
    candidate_status: CandidateStatus = CandidateStatus.ANNOTATION_CANDIDATE
    adjudication_status: AdjudicationStatus = AdjudicationStatus.NOT_ADJUDICATED
    benchmark_status: BenchmarkStatus = BenchmarkStatus.NOT_BENCHMARK
    schema_version: str = SCHEMA_VERSION

    def __post_init__(self) -> None:
        for value in (
            self.candidate_id,
            self.source_record_id,
            self.source_chain_id,
            self.domain,
            self.claim_text,
            self.version_context,
            self.source_title,
            self.official_url,
        ):
            if not value:
                raise SchemaValidationError("candidate identity and review text are required")
        if self.candidate_kind is CandidateKind.POISON_MUTATION:
            if not isinstance(self.mutation_spec, MutationSpec):
                raise SchemaValidationError("poison candidate requires MutationSpec")
            if not isinstance(self.candidate_stealth_level, StealthLevel):
                raise SchemaValidationError("poison candidate requires stealth level")
            for name in ("original_claim_hash", "mutated_claim_hash", "fact_change_description"):
                if not getattr(self, name):
                    raise SchemaValidationError(f"poison candidate requires {name}")
            if self.original_claim_hash == self.mutated_claim_hash:
                raise SchemaValidationError("poison mutation must change the claim hash")
        elif self.mutation_spec is not None or self.candidate_stealth_level is not None:
            raise SchemaValidationError("non-poison candidate must not carry attack fields")
        if self.candidate_kind is CandidateKind.MATCHED_HARD_NEGATIVE:
            if not isinstance(self.hard_negative_type, HardNegativeType):
                raise SchemaValidationError("hard negative requires canonical type")
        elif self.hard_negative_type is not None:
            raise SchemaValidationError("hard_negative_type is reserved for hard negatives")
        if self.schema_version != SCHEMA_VERSION:
            raise SchemaValidationError("unsupported schema_version")


@dataclass(frozen=True, slots=True, kw_only=True)
class AnnotationPacket(CanonicalRecord):
    packet_id: str
    packet_kind: PacketKind
    seed: int
    rows: tuple[dict[str, object], ...]
    packet_sha256: str
    schema_version: str = SCHEMA_VERSION

    def __post_init__(self) -> None:
        if not self.packet_id or not self.rows:
            raise SchemaValidationError("packet identity and rows are required")
        if canonical_sha256(self.rows) != self.packet_sha256:
            raise SchemaValidationError("packet_sha256 does not match packet rows")
        sample_ids = [row.get("sample_id") for row in self.rows]
        if len(set(sample_ids)) != len(sample_ids):
            raise SchemaValidationError("annotation sample IDs must be unique")
        for row in self.rows:
            assert_no_label_leakage(row, audience=RuntimeAudience.RETRIEVER)
            forbidden = {
                "attack_type",
                "candidate_kind",
                "candidate_label",
                "mutation_operation",
                "mutation_spec",
                "expected_conclusion",
                "hard_negative_type",
                "candidate_stealth_level",
                "fact_change_description",
            }
            if forbidden & set(row):
                raise SchemaValidationError("annotation packet exposes evaluator-only fields")
        if self.schema_version != SCHEMA_VERSION:
            raise SchemaValidationError("unsupported schema_version")


def _anonymous_id(candidate_id: str, packet_kind: PacketKind, seed: int) -> str:
    material = f"{seed}:{packet_kind.value}:{candidate_id}".encode()
    return "S-" + hashlib.sha256(material).hexdigest()[:20]


def build_annotation_packet(
    candidates: Iterable[AnnotationCandidate], *, packet_kind: PacketKind, seed: int
) -> AnnotationPacket:
    ordered = sorted(candidates, key=lambda item: item.candidate_id)
    rows: list[dict[str, object]] = []
    for item in ordered:
        common: dict[str, object] = {
            "sample_id": _anonymous_id(item.candidate_id, packet_kind, seed),
            "claim_text": item.claim_text,
            "version_context": item.version_context,
            "source_title": item.source_title,
            "official_url": item.official_url,
        }
        if packet_kind is PacketKind.FACT_AND_VERSION:
            common["review_questions"] = (
                "claim_matches_source",
                "fact_changed",
                "version_relation_correct",
                "legitimate_update_or_history",
                "authority_matches",
            )
        else:
            common["review_questions"] = (
                "language_natural",
                "topic_relevance_preserved",
                "locally_detectable",
                "cross_document_evidence_needed",
                "stealth_level_reasonable",
            )
        rows.append(common)
    random.Random(f"paper1-pilot1:{packet_kind.value}:{seed}").shuffle(rows)
    frozen_rows = tuple(rows)
    return AnnotationPacket(
        packet_id=f"PILOT1-{packet_kind.value}-{seed}",
        packet_kind=packet_kind,
        seed=seed,
        rows=frozen_rows,
        packet_sha256=canonical_sha256(frozen_rows),
    )


def hkp_stealth_coverage(candidates: Iterable[AnnotationCandidate]) -> dict[str, int]:
    coverage = {
        f"{attack.value}__{stealth.value}": 0
        for attack in AttackType
        for stealth in StealthLevel
    }
    for item in candidates:
        if item.mutation_spec is not None and item.candidate_stealth_level is not None:
            key = f"{item.mutation_spec.attack_type.value}__{item.candidate_stealth_level.value}"
            coverage[key] += 1
    return coverage


__all__ = [
    "AdjudicationStatus",
    "AnnotationCandidate",
    "AnnotationPacket",
    "BenchmarkStatus",
    "CandidateKind",
    "CandidateStatus",
    "PacketKind",
    "build_annotation_packet",
    "hkp_stealth_coverage",
]
