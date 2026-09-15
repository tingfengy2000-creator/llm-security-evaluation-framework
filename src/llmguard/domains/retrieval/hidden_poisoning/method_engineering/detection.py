"""Detector, calibration and extraction interfaces for method engineering."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Sequence

from .schema import (
    DetectionPrediction,
    DetectorFeatureVector,
    SignalObservation,
    SignalView,
)


class SignalExtractor(Protocol):
    view: SignalView

    def extract(self, visible_input: object) -> tuple[SignalObservation, ...]: ...


class SingleViewScorer(Protocol):
    view: SignalView

    def score(self, features: DetectorFeatureVector) -> DetectionPrediction: ...


class FusionDetector(Protocol):
    def fit(
        self, features: Sequence[DetectorFeatureVector], labels: Sequence[int]
    ) -> None: ...

    def predict(
        self, features: Sequence[DetectorFeatureVector]
    ) -> tuple[DetectionPrediction, ...]: ...


class RiskCalibrator(Protocol):
    def fit(self, raw_risks: Sequence[float], labels: Sequence[int]) -> None: ...

    def calibrate(self, raw_risks: Sequence[float]) -> tuple[float, ...]: ...


@dataclass(frozen=True, slots=True, kw_only=True)
class FusionDesign:
    primary_estimator: str
    nonlinear_comparators: tuple[str, ...]
    feature_families: tuple[str, ...]
    forbidden_estimators: tuple[str, ...]
    label_isolation: str


@dataclass(frozen=True, slots=True, kw_only=True)
class RiskCalibrationDesign:
    candidates: tuple[str, ...]
    selection_population: str
    forbidden_population: str
    output_name: str


PAPER1_FUSION_DESIGN = FusionDesign(
    primary_estimator="LOGISTIC_REGRESSION",
    nonlinear_comparators=("XGBOOST", "LIGHTGBM"),
    feature_families=(
        "NORMALIZED_SIGNAL_VALUES",
        "APPLICABILITY_INDICATORS",
        "CONFIDENCE_FEATURES",
    ),
    forbidden_estimators=(
        "LARGE_TRANSFORMER_FUSION",
        "GRAPH_NEURAL_NETWORK",
        "END_TO_END_COMPLEX_TRAINING",
    ),
    label_isolation="GROUND_TRUTH_MAY_BE_USED_BY_FIT_OR_EVALUATION_ONLY_AND_NEVER_AS_AN_INFERENCE_FEATURE",
)

PAPER1_RISK_CALIBRATION_DESIGN = RiskCalibrationDesign(
    candidates=("PLATT_SCALING", "ISOTONIC_REGRESSION"),
    selection_population="DEVELOPMENT_PROTOCOL_ONLY",
    forbidden_population="UNTOUCHED_TEST_POPULATION",
    output_name="CALIBRATED_RISK",
)


__all__ = [
    "FusionDesign",
    "FusionDetector",
    "PAPER1_FUSION_DESIGN",
    "PAPER1_RISK_CALIBRATION_DESIGN",
    "RiskCalibrationDesign",
    "RiskCalibrator",
    "SignalExtractor",
    "SingleViewScorer",
]
