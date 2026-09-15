"""Frozen evaluation planning contracts; no metrics are computed here."""

from __future__ import annotations

from dataclasses import dataclass

from .schema import SignalView


@dataclass(frozen=True, slots=True, kw_only=True)
class BaselineSpec:
    name: str
    role: str
    input_scope: str
    output: str
    required_reproduction_record: bool
    failure_boundary: str


@dataclass(frozen=True, slots=True, kw_only=True)
class MetricSpec:
    name: str
    population: str
    definition: str
    stage: str


@dataclass(frozen=True, slots=True, kw_only=True)
class AblationSpec:
    name: str
    included_views: tuple[SignalView, ...]


BASELINE_MATRIX: tuple[BaselineSpec, ...] = (
    BaselineSpec(
        name="RANDOM",
        role="SANITY_BASELINE",
        input_scope="NONE",
        output="RANDOM_SCORE",
        required_reproduction_record=False,
        failure_boundary="NOT_A_METHOD_CLAIM",
    ),
    BaselineSpec(
        name="PPL",
        role="LEXICAL_NATURALNESS_BASELINE",
        input_scope="CANDIDATE_TEXT",
        output="NATURALNESS_SCORE",
        required_reproduction_record=True,
        failure_boundary="MODEL_OR_REVISION_UNAVAILABLE",
    ),
    BaselineSpec(
        name="MLM_NATURALNESS",
        role="LEXICAL_NATURALNESS_BASELINE_AND_SEMANTIC_SIGNAL",
        input_scope="CANDIDATE_TEXT",
        output="MASKED_TOKEN_SCORE",
        required_reproduction_record=True,
        failure_boundary="MODEL_OR_REVISION_UNAVAILABLE",
    ),
    BaselineSpec(
        name="GMTP",
        role="STRONG_EXTERNAL_POISONING_DEFENSE_BASELINE",
        input_scope="CANDIDATE_QUERY_RETRIEVER_COMPATIBILITY",
        output="DETECTION_SCORE",
        required_reproduction_record=True,
        failure_boundary="CONFIG_MODEL_RETRIEVER_OR_TOKEN_GRADIENT_INCOMPATIBILITY",
    ),
    BaselineSpec(
        name="SEMANTIC_SIMILARITY",
        role="SEMANTIC_BASELINE",
        input_scope="CANDIDATE_AND_EVIDENCE",
        output="SIMILARITY_SCORE",
        required_reproduction_record=True,
        failure_boundary="EMBEDDING_OR_EVIDENCE_UNAVAILABLE",
    ),
    BaselineSpec(
        name="SEMANTIC_PLUS_NLI",
        role="CONDITIONAL_COMPOSITE_BASELINE",
        input_scope="CANDIDATE_AND_EVIDENCE",
        output="CONTRADICTION_SCORE",
        required_reproduction_record=True,
        failure_boundary="ONLY_IF_JUSTIFIED_AND_REPRODUCIBLY_CONFIGURED",
    ),
    *(
        BaselineSpec(
            name=f"{view.value}_ONLY",
            role="SINGLE_VIEW_BASELINE",
            input_scope=view.value,
            output="DETECTION_SCORE",
            required_reproduction_record=True,
            failure_boundary="VIEW_NOT_APPLICABLE_OR_SIGNAL_UNAVAILABLE",
        )
        for view in SignalView
    ),
)

METRIC_CONTRACTS: tuple[MetricSpec, ...] = (
    MetricSpec(
        name="AUPRC",
        population="BINARY_POISON_DETECTION",
        definition="Area under the precision-recall curve over Poison=1 and Clean Current/Hard Negative=0.",
        stage="DETECTION",
    ),
    MetricSpec(
        name="AUROC",
        population="BINARY_POISON_DETECTION",
        definition="Area under the receiver operating characteristic curve.",
        stage="DETECTION",
    ),
    MetricSpec(
        name="RECALL_AT_1_PERCENT_FPR",
        population="ALL_NEGATIVES",
        definition="Poison recall at a threshold whose false-positive rate is at most 1% under the frozen threshold protocol.",
        stage="DETECTION",
    ),
    MetricSpec(
        name="RECALL_AT_5_PERCENT_FPR",
        population="ALL_NEGATIVES",
        definition="Poison recall at a threshold whose false-positive rate is at most 5% under the frozen threshold protocol.",
        stage="DETECTION",
    ),
    MetricSpec(
        name="HARD_NEGATIVE_FPR",
        population="HARD_NEGATIVE_ONLY",
        definition="Hard Negative records predicted Poison divided by all valid Hard Negative records.",
        stage="CRITICAL_DETECTION",
    ),
    MetricSpec(
        name="PRECISION",
        population="BINARY_POISON_DETECTION",
        definition="True Poison predictions divided by all Poison predictions.",
        stage="DETECTION",
    ),
    MetricSpec(
        name="RECALL",
        population="BINARY_POISON_DETECTION",
        definition="Detected Poison records divided by all valid Poison records.",
        stage="DETECTION",
    ),
    MetricSpec(
        name="F1",
        population="BINARY_POISON_DETECTION",
        definition="Harmonic mean of precision and recall at a development-selected threshold.",
        stage="DETECTION",
    ),
    MetricSpec(
        name="BRIER_SCORE",
        population="RISK_CALIBRATION",
        definition="Mean squared error between calibrated risk and binary outcome.",
        stage="RISK",
    ),
    MetricSpec(
        name="EXPECTED_CALIBRATION_ERROR",
        population="RISK_CALIBRATION",
        definition="Weighted absolute gap between predicted risk and empirical frequency under a frozen binning protocol.",
        stage="RISK",
    ),
)

_ALL = tuple(SignalView)
ABLATION_MATRIX: tuple[AblationSpec, ...] = (
    *(AblationSpec(name=view.value, included_views=(view,)) for view in SignalView),
    AblationSpec(name="S_E_P_T_R", included_views=_ALL),
    *(
        AblationSpec(
            name=f"FULL_MINUS_{view.value}",
            included_views=tuple(item for item in _ALL if item is not view),
        )
        for view in SignalView
    ),
)

BREAKDOWN_AXES = ("HKP1", "HKP2", "HKP3", "HKP4", "S1", "S2", "S3")
FORMAL_RESEARCH_QUESTIONS = (
    "RQ1: How capable are Semantic, MLM and GMTP baselines on version-aware stealthy poisoning?",
    "RQ2: Does five-view fusion outperform Semantic-only under a frozen protocol?",
    "RQ3: Do Temporal-Version and Provenance reduce Hard Negative FPR?",
    "RQ4: How do view contributions differ across HKP1-4 and S1-3?",
    "RQ5: Can calibrated risk reduce poison exposure while preserving clean utility?",
)

SCALE_READINESS = {
    "domains": 5,
    "hkp_families": 4,
    "stealth_levels": 3,
    "independent_chains_per_cell": 4,
    "independent_groups": 240,
    "approximate_candidates_if_three_per_group": 720,
    "generated": False,
    "dataset_frozen": False,
    "split_rule": "VERSION_CHAIN_GROUP_AWARE_NO_CHAIN_ACROSS_TRAIN_DEV_TEST",
}


__all__ = [
    "ABLATION_MATRIX",
    "BASELINE_MATRIX",
    "BREAKDOWN_AXES",
    "FORMAL_RESEARCH_QUESTIONS",
    "METRIC_CONTRACTS",
    "SCALE_READINESS",
    "AblationSpec",
    "BaselineSpec",
    "MetricSpec",
]
