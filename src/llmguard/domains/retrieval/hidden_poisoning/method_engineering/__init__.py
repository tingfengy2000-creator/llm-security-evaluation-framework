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
from .feasibility import (
    EXTRACTOR_VERSION,
    SIGNAL_ORIENTATIONS,
    extract_sample_signals,
)
from .registry import FIVE_VIEW_SIGNAL_REGISTRY, signals_for_view
from .schema import (
    ClaimRepresentation,
    DetectionPrediction,
    DetectorFeatureVector,
    SignalDefinition,
    SignalComputationStatus,
    SignalGroundedExplanation,
    SignalInstance,
    SignalObservation,
    SignalOrientation,
    SignalOutputType,
    SignalView,
)

__all__ = [
    "ABLATION_MATRIX",
    "BASELINE_MATRIX",
    "BREAKDOWN_AXES",
    "EXPLANATION_CONTRACT",
    "EXTRACTOR_VERSION",
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
    "SignalComputationStatus",
    "SignalExtractor",
    "SignalGroundedExplanation",
    "SignalInstance",
    "SignalObservation",
    "SignalOrientation",
    "SignalOutputType",
    "SignalView",
    "SingleViewScorer",
    "SIGNAL_ORIENTATIONS",
    "extract_sample_signals",
    "signals_for_view",
]
