"""Stable contracts for Paper 1 signal and detector method engineering.

These objects describe observable inputs and outputs. They do not train a model,
compute a paper result, or permit Ground Truth to enter detector-visible data.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Mapping


class SignalView(str, Enum):
    SEMANTIC = "SEMANTIC"
    ENTITY_CLAIM = "ENTITY_CLAIM"
    PROVENANCE = "PROVENANCE"
    TEMPORAL_VERSION = "TEMPORAL_VERSION"
    RETRIEVAL_BEHAVIOR = "RETRIEVAL_BEHAVIOR"


class SignalOutputType(str, Enum):
    BOOLEAN = "BOOLEAN"
    INTEGER = "INTEGER"
    CONTINUOUS = "CONTINUOUS"
    CATEGORICAL = "CATEGORICAL"


@dataclass(frozen=True, slots=True, kw_only=True)
class SignalDefinition:
    signal_name: str
    view: SignalView
    definition: str
    input_fields: tuple[str, ...]
    output_type: SignalOutputType
    value_range: tuple[float, float] | None
    applicability: str
    missing_value_semantics: str
    evidence_dependency: str
    candidate_dependency: bool
    query_dependency: bool
    version_chain_dependency: bool
    expected_attack_relevance: tuple[str, ...]
    explanation_role: str


@dataclass(frozen=True, slots=True, kw_only=True)
class SignalObservation:
    """Applicability-aware value; not-applicable never means safe or zero risk."""

    signal_name: str
    view: SignalView
    value: bool | int | float | str | None
    applicable: bool
    confidence: float | None
    evidence_quality: float | None
    missing_reason: str | None
    evidence_references: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.applicable and self.value is None:
            raise ValueError("applicable signal requires a value")
        if not self.applicable and self.value is not None:
            raise ValueError("not-applicable signal must use value=None")
        if not self.applicable and not self.missing_reason:
            raise ValueError("not-applicable signal requires a missing reason")
        for name, value in (
            ("confidence", self.confidence),
            ("evidence_quality", self.evidence_quality),
        ):
            if value is not None and not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be in [0, 1]")


@dataclass(frozen=True, slots=True, kw_only=True)
class ClaimRepresentation:
    """Structured intermediate representation produced before claim signals."""

    subject: str | None
    predicate: str | None
    object_or_value: str | None
    unit: str | None
    time_scope: str | None
    condition: str | None
    exception: str | None
    authority: str | None


@dataclass(frozen=True, slots=True, kw_only=True)
class DetectorFeatureVector:
    """Detector-visible features only; labels are intentionally absent."""

    candidate_id: str
    query_id: str | None
    observations: tuple[SignalObservation, ...]

    def feature_payload(self) -> Mapping[str, float | bool | str | None]:
        payload: dict[str, float | bool | str | None] = {}
        for observation in self.observations:
            prefix = observation.signal_name
            payload[f"{prefix}__value"] = observation.value
            payload[f"{prefix}__applicable"] = observation.applicable
            payload[f"{prefix}__confidence"] = observation.confidence
            payload[f"{prefix}__evidence_quality"] = observation.evidence_quality
        return payload


@dataclass(frozen=True, slots=True, kw_only=True)
class DetectionPrediction:
    candidate_id: str
    raw_risk: float
    threshold: float | None
    predicted_poison: bool | None

    def __post_init__(self) -> None:
        if not 0.0 <= self.raw_risk <= 1.0:
            raise ValueError("raw_risk must be in [0, 1]")
        if self.threshold is not None and not 0.0 <= self.threshold <= 1.0:
            raise ValueError("threshold must be in [0, 1]")


@dataclass(frozen=True, slots=True, kw_only=True)
class SignalGroundedExplanation:
    candidate_id: str
    overall_risk: float
    top_contributing_views: tuple[SignalView, ...]
    top_contributing_signals: tuple[str, ...]
    evidence_references: tuple[str, ...]
    reason_codes: tuple[str, ...]


__all__ = [
    "ClaimRepresentation",
    "DetectionPrediction",
    "DetectorFeatureVector",
    "SignalDefinition",
    "SignalGroundedExplanation",
    "SignalObservation",
    "SignalOutputType",
    "SignalView",
]
