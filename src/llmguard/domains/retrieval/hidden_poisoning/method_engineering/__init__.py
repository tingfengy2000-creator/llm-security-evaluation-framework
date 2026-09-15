"""Paper 1 multi-view method-engineering contracts."""

from .detection import (
    PAPER1_FUSION_DESIGN,
    PAPER1_RISK_CALIBRATION_DESIGN,
    FusionDetector,
    RiskCalibrator,
    SignalExtractor,
    SingleViewScorer,
)
from .evaluation import (
    ABLATION_MATRIX,
    BASELINE_MATRIX,
    BREAKDOWN_AXES,
    FORMAL_RESEARCH_QUESTIONS,
    METRIC_CONTRACTS,
    SCALE_READINESS,
)
from .explanation import EXPLANATION_CONTRACT, ExplanationBuilder
from .registry import FIVE_VIEW_SIGNAL_REGISTRY, signals_for_view
from .schema import (
    ClaimRepresentation,
    DetectionPrediction,
    DetectorFeatureVector,
    SignalDefinition,
    SignalGroundedExplanation,
    SignalObservation,
    SignalOutputType,
    SignalView,
)

__all__ = [
    "ABLATION_MATRIX",
    "BASELINE_MATRIX",
    "BREAKDOWN_AXES",
    "EXPLANATION_CONTRACT",
    "FIVE_VIEW_SIGNAL_REGISTRY",
    "FORMAL_RESEARCH_QUESTIONS",
    "METRIC_CONTRACTS",
    "PAPER1_FUSION_DESIGN",
    "PAPER1_RISK_CALIBRATION_DESIGN",
    "SCALE_READINESS",
    "ClaimRepresentation",
    "DetectionPrediction",
    "DetectorFeatureVector",
    "ExplanationBuilder",
    "FusionDetector",
    "RiskCalibrator",
    "SignalDefinition",
    "SignalExtractor",
    "SignalGroundedExplanation",
    "SignalObservation",
    "SignalOutputType",
    "SignalView",
    "SingleViewScorer",
    "signals_for_view",
]
