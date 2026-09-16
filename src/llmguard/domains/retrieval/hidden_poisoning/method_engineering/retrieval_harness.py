"""Label-blind retrieval harness contracts for Paper 1 method engineering.

The module deliberately separates document-level poison risk from query-time
retrieval exposure risk.  It contains no detector fitting and accepts no class,
HKP, stealth, Expected, or Ground Truth fields in retriever-visible records.
"""

from __future__ import annotations

import hashlib
import math
import re
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any, cast

from .registry import FIVE_VIEW_SIGNAL_REGISTRY


HARNESS_VERSION = "paper1_retrieval_harness_v1"
PREDECLARED_K = (1, 3, 5, 10)


class EvidenceAccessMode(str, Enum):
    CANDIDATE_ONLY = "CANDIDATE_ONLY"
    PUBLIC_METADATA_ONLY = "PUBLIC_METADATA_ONLY"
    VERSION_REGISTRY_LOOKUP = "VERSION_REGISTRY_LOOKUP"
    TRUSTED_EVIDENCE_RETRIEVAL = "TRUSTED_EVIDENCE_RETRIEVAL"
    QUERY_RETRIEVAL_TRACE = "QUERY_RETRIEVAL_TRACE"
    ORACLE_MATCHED_EVIDENCE_DIAGNOSTIC_ONLY = "ORACLE_MATCHED_EVIDENCE_DIAGNOSTIC_ONLY"
    NOT_REQUIRED = "NOT_REQUIRED"


class SignalDeployability(str, Enum):
    DIAGNOSTIC_ONLY = "DIAGNOSTIC_ONLY"
    DEPLOYABLE_NOW = "DEPLOYABLE_NOW"
    DEPLOYABLE_AFTER_VERSION_REGISTRY = "DEPLOYABLE_AFTER_VERSION_REGISTRY"
    DEPLOYABLE_AFTER_TRUSTED_RETRIEVER = "DEPLOYABLE_AFTER_TRUSTED_RETRIEVER"
    QUERY_RUNTIME_ONLY = "QUERY_RUNTIME_ONLY"
    NOT_READY = "NOT_READY"


class RiskStage(str, Enum):
    DOCUMENT_POISON_RISK = "DOCUMENT_POISON_RISK"
    RETRIEVAL_EXPOSURE_RISK = "RETRIEVAL_EXPOSURE_RISK"


class TemporalGapCause(str, Enum):
    NO_TEMPORAL_CLAIM = "NO_TEMPORAL_CLAIM"
    NO_VERSION_ROLE_METADATA = "NO_VERSION_ROLE_METADATA"
    NO_EFFECTIVE_INTERVAL = "NO_EFFECTIVE_INTERVAL"
    NO_CURRENT_VERSION_BINDING = "NO_CURRENT_VERSION_BINDING"
    NO_HISTORICAL_VERSION_BINDING = "NO_HISTORICAL_VERSION_BINDING"
    EXTRACTOR_LIMITATION = "EXTRACTOR_LIMITATION"
    OTHER = "OTHER"


@dataclass(frozen=True, slots=True, kw_only=True)
class RetrievalQuery:
    query_id: str
    independence_group: str
    query_text: str
    primary_subject: str
    temporal_intent: str = "CURRENT_STATE"
    construction_method: str = "GROUP_SUBJECT_DETERMINISTIC_TEMPLATE_V1"


@dataclass(frozen=True, slots=True, kw_only=True)
class RetrievalDocument:
    doc_id: str
    candidate_text: str
    source_title: str
    primary_subject: str


@dataclass(frozen=True, slots=True, kw_only=True)
class RetrievalTraceRow:
    query_id: str
    doc_id: str
    raw_score: float
    rank: int
    retriever_id: str
    run_id: str


@dataclass(frozen=True, slots=True, kw_only=True)
class TrustedVersionRecord:
    """Allowed registry metadata; labels and expected outcomes are absent."""

    document_id: str
    version_id: str
    version_role: str
    publication_date: str | None
    effective_from: str | None
    effective_to: str | None
    predecessor_version_id: str | None
    successor_version_id: str | None
    superseded_by_version_id: str | None
    issuer: str | None
    adopting_authority: str | None
    amending_authority: str | None
    official_url: str
    frozen_document_sha256: str


FORBIDDEN_FEATURE_KEYS = frozenset(
    {
        "candidate_kind",
        "class",
        "clean_poison_hard_negative",
        "expected",
        "ground_truth",
        "gt_outcome",
        "hkp",
        "intended_stealth",
        "label",
        "labels",
        "owner_adjudication",
        "owner_only",
        "poison_label",
        "semantic_attack_type",
        "stealth_level",
        "target",
    }
)


def forbidden_key_hits(value: object) -> list[str]:
    """Return forbidden feature-plane keys found recursively."""

    hits: set[str] = set()

    def visit(item: object) -> None:
        if isinstance(item, Mapping):
            for key, child in item.items():
                lowered = str(key).lower()
                if lowered in FORBIDDEN_FEATURE_KEYS:
                    hits.add(str(key))
                visit(child)
        elif isinstance(item, Sequence) and not isinstance(
            item, (str, bytes, bytearray)
        ):
            for child in item:
                visit(child)

    visit(value)
    return sorted(hits)


def canonical_query(group_id: str, primary_subject: str) -> RetrievalQuery:
    """Build a neutral current-state query from label-blind group metadata."""

    subject = primary_subject.strip()
    if not subject:
        raise ValueError(f"{group_id}: primary_subject is blank")
    digest = hashlib.sha256(f"{group_id}\0{subject}".encode()).hexdigest()[:12]
    return RetrievalQuery(
        query_id=f"P1Q-{digest}",
        independence_group=group_id,
        query_text=f"请说明《{subject}》当前有效规定的主要内容。",
        primary_subject=subject,
    )


def query_qa(
    query: RetrievalQuery, *, candidate_texts: Sequence[str]
) -> dict[str, object]:
    """Run conservative answer/class/member-bias checks on one query."""

    forbidden_terms = (
        "CLEAN",
        "POISON",
        "HARD_NEGATIVE",
        "HKP",
        "S1",
        "S2",
        "S3",
        "EXPECTED",
        "正确答案",
        "投毒",
        "硬负样本",
    )
    upper = query.query_text.upper()
    class_leakage = [term for term in forbidden_terms if term in upper]
    numeric_answer_leakage = re.findall(r"\d+(?:\.\d+)?", query.query_text)
    exact_candidate = any(
        query.query_text.strip() == text.strip() for text in candidate_texts
    )
    member_substring = any(
        len(query.query_text) >= 12 and query.query_text in text
        for text in candidate_texts
    )
    return {
        "query_id": query.query_id,
        "group": query.independence_group,
        "subject_present": query.primary_subject in query.query_text,
        "current_state_intent": "当前" in query.query_text,
        "class_leakage_terms": class_leakage,
        "numeric_answer_leakage": numeric_answer_leakage,
        "exact_candidate_copy": exact_candidate,
        "single_member_substring_bias": member_substring,
        "natural_template": query.query_text.startswith("请说明《")
        and query.query_text.endswith("当前有效规定的主要内容。"),
        "pass": not class_leakage
        and not numeric_answer_leakage
        and not exact_candidate
        and not member_substring,
    }


_SPACE = re.compile(r"\s+")
_PUNCT = re.compile(r"[^\w\u3400-\u9fff]+", re.UNICODE)


def normalize_text(text: str) -> str:
    compact = _SPACE.sub("", text.strip().lower())
    return _PUNCT.sub("", compact)


def character_ngrams(text: str, sizes: tuple[int, ...] = (2, 3)) -> tuple[str, ...]:
    """Chinese-compatible deterministic tokenizer used by sparse BM25."""

    normalized = normalize_text(text)
    tokens: list[str] = []
    for size in sizes:
        if len(normalized) < size:
            continue
        tokens.extend(
            normalized[index : index + size]
            for index in range(len(normalized) - size + 1)
        )
    return tuple(tokens or ([normalized] if normalized else []))


class CharacterNgramBM25:
    """Small deterministic BM25 implementation for the frozen 72-doc harness."""

    retriever_id = "CHAR_NGRAM_BM25_V1"

    def __init__(
        self,
        documents: Sequence[RetrievalDocument],
        *,
        k1: float = 1.2,
        b: float = 0.75,
        ngram_sizes: tuple[int, ...] = (2, 3),
    ) -> None:
        if not documents:
            raise ValueError("documents cannot be empty")
        self.documents = tuple(documents)
        self.k1 = k1
        self.b = b
        self.ngram_sizes = ngram_sizes
        self._tokens = tuple(
            character_ngrams(
                f"{doc.source_title} {doc.primary_subject} {doc.candidate_text}",
                ngram_sizes,
            )
            for doc in self.documents
        )
        self._term_counts = tuple(Counter(tokens) for tokens in self._tokens)
        self._lengths = tuple(len(tokens) for tokens in self._tokens)
        self._avg_length = sum(self._lengths) / len(self._lengths)
        document_frequency: Counter[str] = Counter()
        for tokens in self._tokens:
            document_frequency.update(set(tokens))
        self._idf = {
            token: math.log(1.0 + (len(documents) - count + 0.5) / (count + 0.5))
            for token, count in document_frequency.items()
        }

    def score(self, query_text: str) -> tuple[float, ...]:
        query_tokens = Counter(character_ngrams(query_text, self.ngram_sizes))
        scores: list[float] = []
        for counts, length in zip(self._term_counts, self._lengths, strict=True):
            score = 0.0
            length_norm = 1.0 - self.b + self.b * length / self._avg_length
            for token, query_frequency in query_tokens.items():
                frequency = counts.get(token, 0)
                if frequency == 0:
                    continue
                numerator = frequency * (self.k1 + 1.0)
                denominator = frequency + self.k1 * length_norm
                score += (
                    self._idf.get(token, 0.0)
                    * numerator
                    / denominator
                    * query_frequency
                )
            scores.append(score)
        return tuple(scores)

    def configuration(self) -> dict[str, object]:
        return {
            "retriever_id": self.retriever_id,
            "implementation_version": HARNESS_VERSION,
            "tokenizer": "normalized Chinese-compatible character n-grams",
            "normalization": "lowercase; remove whitespace and punctuation",
            "ngram_sizes": list(self.ngram_sizes),
            "k1": self.k1,
            "b": self.b,
            "document_count": len(self.documents),
            "score_semantics": "BM25; higher is more similar",
        }


def rank_scores(
    *,
    query_id: str,
    documents: Sequence[RetrievalDocument],
    scores: Sequence[float],
    retriever_id: str,
    run_id: str,
) -> list[RetrievalTraceRow]:
    if len(documents) != len(scores):
        raise ValueError("document/score cardinality mismatch")
    order = sorted(
        range(len(documents)),
        key=lambda index: (-float(scores[index]), documents[index].doc_id),
    )
    ranks = {index: rank for rank, index in enumerate(order, start=1)}
    return [
        RetrievalTraceRow(
            query_id=query_id,
            doc_id=document.doc_id,
            raw_score=float(scores[index]),
            rank=ranks[index],
            retriever_id=retriever_id,
            run_id=run_id,
        )
        for index, document in enumerate(documents)
    ]


_RETRIEVAL_NAMES = {
    "retrieval_rank",
    "retrieval_score",
    "historical_docs_at_k",
    "current_docs_at_k",
    "historical_dominance_at_k",
    "historical_current_rank_gap",
    "historical_current_score_gap",
    "current_missing_topk",
    "version_diversity",
    "ranking_stability",
}
_VERSION_RETRIEVAL_NAMES = _RETRIEVAL_NAMES - {
    "retrieval_rank",
    "retrieval_score",
    "ranking_stability",
}


def build_signal_deployability_matrix() -> list[dict[str, object]]:
    """Audit all 42 signals against the current inference-time threat model."""

    rows: list[dict[str, object]] = []
    for signal in FIVE_VIEW_SIGNAL_REGISTRY:
        name = signal.signal_name
        if name in {"mlm_masked_token_naturalness", "ppl_naturalness"}:
            mode = EvidenceAccessMode.CANDIDATE_ONLY
            status = SignalDeployability.NOT_READY
            requirement = "Freeze the exact language-model checkpoint and policy."
        elif name in _VERSION_RETRIEVAL_NAMES:
            mode = EvidenceAccessMode.VERSION_REGISTRY_LOOKUP
            status = SignalDeployability.DEPLOYABLE_AFTER_VERSION_REGISTRY
            requirement = "Join trace to a trusted label-free version registry."
        elif name in _RETRIEVAL_NAMES or name == "top_k_semantic_similarity":
            mode = EvidenceAccessMode.QUERY_RETRIEVAL_TRACE
            status = SignalDeployability.QUERY_RUNTIME_ONLY
            requirement = "Use a prelocked query/corpus/retrieval trace at runtime."
        else:
            mode = EvidenceAccessMode.ORACLE_MATCHED_EVIDENCE_DIAGNOSTIC_ONLY
            status = SignalDeployability.DIAGNOSTIC_ONLY
            requirement = (
                "Replace pre-matched E1/E2 with an independently retrieved trusted "
                "Evidence set or trusted version-registry lookup."
            )
        stage = (
            RiskStage.RETRIEVAL_EXPOSURE_RISK
            if signal.query_dependency
            else RiskStage.DOCUMENT_POISON_RISK
        )
        rows.append(
            {
                "signal_name": name,
                "view": signal.view.value,
                "risk_stage": stage.value,
                "evidence_access_mode": mode.value,
                "deployability_status": status.value,
                "current_implementation_uses_oracle_matched_evidence": (
                    mode is EvidenceAccessMode.ORACLE_MATCHED_EVIDENCE_DIAGNOSTIC_ONLY
                ),
                "deployment_requirement": requirement,
                "decision_basis": "LEGAL_INFERENCE_INPUT_AVAILABILITY_NOT_AUROC",
            }
        )
    if len(rows) != 42:
        raise AssertionError("deployability audit must cover exactly 42 signals")
    return rows


_TEMPORAL_CUE = re.compile(
    r"(?:19|20)\d{2}|修订|修正|废止|施行|实施|现行|当前|原《|旧版|新版|版本|历史|替代|同时废止"
)


def temporal_gap_cause(sample: Mapping[str, Any]) -> TemporalGapCause:
    """Classify why the deployable present-time substitution test is unavailable."""

    text = str(sample.get("candidate_text") or "")
    if _TEMPORAL_CUE.search(text) is None:
        return TemporalGapCause.NO_TEMPORAL_CLAIM
    evidence = sample.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        return TemporalGapCause.NO_VERSION_ROLE_METADATA
    if any(
        not isinstance(item, Mapping) or not item.get("version_role")
        for item in evidence
    ):
        return TemporalGapCause.NO_VERSION_ROLE_METADATA
    if any(
        not item.get("effective_from") and not item.get("effective_to")
        for item in evidence
        if isinstance(item, Mapping)
    ):
        return TemporalGapCause.NO_EFFECTIVE_INTERVAL
    roles = {
        str(item.get("version_role")) for item in evidence if isinstance(item, Mapping)
    }
    if "CURRENT" not in roles:
        return TemporalGapCause.NO_CURRENT_VERSION_BINDING
    if "HISTORICAL" not in roles:
        return TemporalGapCause.NO_HISTORICAL_VERSION_BINDING
    return TemporalGapCause.EXTRACTOR_LIMITATION


def as_record(value: object) -> dict[str, object]:
    if not hasattr(value, "__dataclass_fields__"):
        raise TypeError("value is not a dataclass record")
    return cast(dict[str, object], asdict(cast(Any, value)))


def stable_top_k(trace: Iterable[RetrievalTraceRow], k: int) -> tuple[str, ...]:
    return tuple(row.doc_id for row in sorted(trace, key=lambda row: row.rank)[:k])


__all__ = [
    "FORBIDDEN_FEATURE_KEYS",
    "HARNESS_VERSION",
    "PREDECLARED_K",
    "CharacterNgramBM25",
    "EvidenceAccessMode",
    "RetrievalDocument",
    "RetrievalQuery",
    "RetrievalTraceRow",
    "RiskStage",
    "SignalDeployability",
    "TemporalGapCause",
    "TrustedVersionRecord",
    "as_record",
    "build_signal_deployability_matrix",
    "canonical_query",
    "character_ngrams",
    "forbidden_key_hits",
    "normalize_text",
    "query_qa",
    "rank_scores",
    "stable_top_k",
    "temporal_gap_cause",
]
