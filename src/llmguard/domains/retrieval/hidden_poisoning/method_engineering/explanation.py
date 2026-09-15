"""Signal- and evidence-grounded explanation interface."""

from __future__ import annotations

from typing import Protocol

from .schema import (
    DetectionPrediction,
    DetectorFeatureVector,
    SignalGroundedExplanation,
)


class ExplanationBuilder(Protocol):
    def explain(
        self,
        features: DetectorFeatureVector,
        prediction: DetectionPrediction,
    ) -> SignalGroundedExplanation: ...


EXPLANATION_CONTRACT = {
    "grounding": ("SIGNAL_GROUNDED", "EVIDENCE_GROUNDED"),
    "required_outputs": (
        "overall_risk",
        "top_contributing_views",
        "top_contributing_signals",
        "evidence_references",
        "version_or_provenance_reason_codes",
    ),
    "free_form_llm_only_allowed": False,
}


__all__ = ["EXPLANATION_CONTRACT", "ExplanationBuilder"]
