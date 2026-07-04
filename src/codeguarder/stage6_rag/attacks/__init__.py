"""Retrieval attack fixtures and physically separated dataset loaders."""

from codeguarder.stage6_rag.attacks.attack_matrix import (
    ATTACK_MATRIX,
    AttackDefinition,
    EvaluationGroundTruth,
    LoadedRAGDataset,
    PublicRAGDataset,
    load_dataset,
    load_evaluation_ground_truth,
    load_public_dataset,
)
from codeguarder.stage6_rag.attacks.attack_renderer import (
    GENERATION_QUESTION_INJECTION_PATTERNS,
    PUBLIC_QUERY_FIELDS,
    render_query_record,
)

__all__ = [
    "ATTACK_MATRIX",
    "GENERATION_QUESTION_INJECTION_PATTERNS",
    "PUBLIC_QUERY_FIELDS",
    "AttackDefinition",
    "EvaluationGroundTruth",
    "LoadedRAGDataset",
    "PublicRAGDataset",
    "load_dataset",
    "load_evaluation_ground_truth",
    "load_public_dataset",
    "render_query_record",
]
