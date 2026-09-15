"""Deterministic, label-blind Final72 signal-feasibility extraction helpers.

The extractors in this module consume only the sanitized candidate/evidence
projection.  They deliberately do not accept Ground Truth, expected labels,
annotation values, attack classes, stealth levels, or matched-group metadata.
"""

from __future__ import annotations

import math
import re
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import asdict
from urllib.parse import urlparse

from .registry import FIVE_VIEW_SIGNAL_REGISTRY
from .schema import (
    SignalComputationStatus,
    SignalInstance,
    SignalOrientation,
    SignalView,
)

EXTRACTOR_VERSION = "PAPER1_FINAL72_DETERMINISTIC_RULES_V1"
REFERENCE_YEAR = 2026

_YEAR_RE = re.compile(r"(?<!\d)(19\d{2}|20\d{2})(?=年|[-/.]|\D|$)")
_DATE_RE = re.compile(r"(19\d{2}|20\d{2})年(\d{1,2})月(?:([0-3]?\d)日)?")
_NUMBER_RE = re.compile(r"(?<![A-Za-z0-9])\d+(?:\.\d+)?")
_BOOK_RE = re.compile(r"《([^》]{2,80})》")
_AUTHORITY_RE = re.compile(
    r"([\u4e00-\u9fff]{2,24}(?:人民代表大会常务委员会|人民代表大会|人民政府|"
    r"国务院|教育部|财政部|司法部|工业和信息化部|国家互联网信息办公室|"
    r"证监会|委员会|法院|检察院))"
)

_NEGATION = ("不", "不得", "禁止", "未", "无权", "不能", "不适用")
_CONDITION = ("如果", "若", "在", "当", "仅", "只有", "适用", "条件", "应当", "可以")
_EXCEPTION = ("除", "但是", "但", "例外", "不适用", "除外")
_HISTORICAL = ("曾", "原", "历史", "修订前", "废止前", "当时", "旧版", "前序版本")
_CURRENT = ("现行", "目前", "当前", "现已", "仍然", "仍须", "现在")
_VERSION = ("修订", "修改", "版本", "施行", "废止", "替代", "通过")


SIGNAL_ORIENTATIONS: Mapping[str, SignalOrientation] = {
    "mlm_masked_token_naturalness": SignalOrientation.LOWER_IS_RISKIER,
    "ppl_naturalness": SignalOrientation.LOWER_IS_RISKIER,
    "current_version_semantic_similarity": SignalOrientation.LOWER_IS_RISKIER,
    "historical_version_semantic_similarity": SignalOrientation.NON_MONOTONIC,
    "top_k_semantic_similarity": SignalOrientation.NON_MONOTONIC,
    "semantic_version_margin": SignalOrientation.HIGHER_IS_RISKIER,
    "subject_match": SignalOrientation.LOWER_IS_RISKIER,
    "predicate_match": SignalOrientation.LOWER_IS_RISKIER,
    "entity_conflict": SignalOrientation.HIGHER_IS_RISKIER,
    "numeric_conflict": SignalOrientation.HIGHER_IS_RISKIER,
    "date_conflict": SignalOrientation.HIGHER_IS_RISKIER,
    "condition_conflict": SignalOrientation.HIGHER_IS_RISKIER,
    "exception_conflict": SignalOrientation.HIGHER_IS_RISKIER,
    "negation_flip": SignalOrientation.HIGHER_IS_RISKIER,
    "relation_conflict": SignalOrientation.HIGHER_IS_RISKIER,
    "official_source": SignalOrientation.LOWER_IS_RISKIER,
    "host_publisher_relation": SignalOrientation.UNDEFINED,
    "publisher_issuer_match": SignalOrientation.LOWER_IS_RISKIER,
    "claimed_authority_match": SignalOrientation.LOWER_IS_RISKIER,
    "document_identity_match": SignalOrientation.LOWER_IS_RISKIER,
    "version_identity_match": SignalOrientation.LOWER_IS_RISKIER,
    "official_repost": SignalOrientation.NON_MONOTONIC,
    "provenance_consistency": SignalOrientation.LOWER_IS_RISKIER,
    "current_fact_match": SignalOrientation.LOWER_IS_RISKIER,
    "historical_fact_match": SignalOrientation.NON_MONOTONIC,
    "version_mismatch": SignalOrientation.HIGHER_IS_RISKIER,
    "superseded_version": SignalOrientation.NON_MONOTONIC,
    "effective_interval_conflict": SignalOrientation.HIGHER_IS_RISKIER,
    "current_history_binding_conflict": SignalOrientation.HIGHER_IS_RISKIER,
    "successor_exists": SignalOrientation.NON_MONOTONIC,
    "version_distance": SignalOrientation.NON_MONOTONIC,
    "present_time_substitution_signal": SignalOrientation.NON_MONOTONIC,
    "retrieval_rank": SignalOrientation.NON_MONOTONIC,
    "retrieval_score": SignalOrientation.NON_MONOTONIC,
    "historical_docs_at_k": SignalOrientation.NON_MONOTONIC,
    "current_docs_at_k": SignalOrientation.NON_MONOTONIC,
    "historical_dominance_at_k": SignalOrientation.NON_MONOTONIC,
    "historical_current_rank_gap": SignalOrientation.NON_MONOTONIC,
    "historical_current_score_gap": SignalOrientation.NON_MONOTONIC,
    "current_missing_topk": SignalOrientation.HIGHER_IS_RISKIER,
    "version_diversity": SignalOrientation.NON_MONOTONIC,
    "ranking_stability": SignalOrientation.LOWER_IS_RISKIER,
}


def validate_orientation_contract() -> None:
    names = {item.signal_name for item in FIVE_VIEW_SIGNAL_REGISTRY}
    if names != set(SIGNAL_ORIENTATIONS):
        missing = sorted(names - set(SIGNAL_ORIENTATIONS))
        extra = sorted(set(SIGNAL_ORIENTATIONS) - names)
        raise ValueError(f"orientation mismatch: missing={missing}, extra={extra}")


def _normalize(text: str) -> str:
    return re.sub(r"[^0-9A-Za-z\u4e00-\u9fff]+", "", text).lower()


def _shingles(text: str, width: int = 2) -> set[str]:
    normalized = _normalize(text)
    if not normalized:
        return set()
    if len(normalized) < width:
        return {normalized}
    return {
        normalized[index : index + width]
        for index in range(len(normalized) - width + 1)
    }


def lexical_similarity(left: str, right: str) -> float:
    """Character-bigram Jaccard similarity, deterministic and model-free."""

    lhs = _shingles(left)
    rhs = _shingles(right)
    if not lhs or not rhs:
        return 0.0
    return len(lhs & rhs) / len(lhs | rhs)


def _years(text: str) -> tuple[int, ...]:
    return tuple(sorted({int(value) for value in _YEAR_RE.findall(text)}))


def _dates(text: str) -> tuple[str, ...]:
    values: set[str] = set()
    for year, month, day in _DATE_RE.findall(text):
        values.add(f"{int(year):04d}-{int(month):02d}-{int(day or 0):02d}")
    return tuple(sorted(values))


def _numbers(text: str) -> tuple[str, ...]:
    return tuple(sorted(set(_NUMBER_RE.findall(text))))


def _books(text: str) -> tuple[str, ...]:
    return tuple(dict.fromkeys(value.strip() for value in _BOOK_RE.findall(text)))


def _authorities(text: str) -> tuple[str, ...]:
    return tuple(dict.fromkeys(value.strip() for value in _AUTHORITY_RE.findall(text)))


def _contains_any(text: str, cues: Sequence[str]) -> bool:
    return any(cue in text for cue in cues)


def _official_url(url: str) -> bool:
    host = (urlparse(url).hostname or "").lower()
    return host.endswith(".gov.cn") or host == "gov.cn"


def _combined_evidence(sample: Mapping[str, object]) -> str:
    evidence = sample.get("evidence")
    if not isinstance(evidence, list):
        return ""
    parts: list[str] = []
    for item in evidence:
        if not isinstance(item, dict):
            continue
        parts.extend(
            str(item.get(field) or "")
            for field in ("official_source_title", "snapshot_text")
        )
    return " ".join(parts)


def _evidence_items(sample: Mapping[str, object]) -> list[Mapping[str, object]]:
    raw = sample.get("evidence")
    if not isinstance(raw, list):
        return []
    return [item for item in raw if isinstance(item, dict)]


def _source_refs(sample: Mapping[str, object]) -> tuple[str, ...]:
    return tuple(
        str(item.get("source_ref") or item.get("official_source_url") or "")
        for item in _evidence_items(sample)
        if item.get("source_ref") or item.get("official_source_url")
    )


def _computed(
    sample_id: str,
    name: str,
    view: SignalView,
    value: bool | int | float | str,
    confidence: float,
    reason_code: str,
    reason: str,
    refs: tuple[str, ...],
    details: Mapping[str, bool | int | float | str | None] | None = None,
) -> SignalInstance:
    return SignalInstance(
        sample_id=sample_id,
        signal_name=name,
        view=view,
        value=value,
        applicable=True,
        confidence=confidence,
        computation_status=SignalComputationStatus.COMPUTED,
        reason_code=reason_code,
        reason=reason,
        source_refs=refs,
        extractor_version=EXTRACTOR_VERSION,
        orientation=SIGNAL_ORIENTATIONS[name],
        details=details,
    )


def _unavailable(
    sample_id: str,
    name: str,
    view: SignalView,
    status: SignalComputationStatus,
    reason_code: str,
    reason: str,
    *,
    applicable: bool = True,
    refs: tuple[str, ...] = (),
) -> SignalInstance:
    return SignalInstance(
        sample_id=sample_id,
        signal_name=name,
        view=view,
        value=None,
        applicable=applicable,
        confidence=None,
        computation_status=status,
        reason_code=reason_code,
        reason=reason,
        source_refs=refs,
        extractor_version=EXTRACTOR_VERSION,
        orientation=SIGNAL_ORIENTATIONS[name],
    )


def _not_applicable(
    sample_id: str,
    name: str,
    view: SignalView,
    reason_code: str,
    reason: str,
    refs: tuple[str, ...] = (),
) -> SignalInstance:
    return _unavailable(
        sample_id,
        name,
        view,
        SignalComputationStatus.NOT_APPLICABLE,
        reason_code,
        reason,
        applicable=False,
        refs=refs,
    )


def _version_partition(
    evidence: Sequence[Mapping[str, object]],
) -> tuple[list[Mapping[str, object]], list[Mapping[str, object]], float]:
    dated: list[tuple[int, Mapping[str, object]]] = []
    for item in evidence:
        text = (
            f"{item.get('official_source_title', '')} {item.get('snapshot_text', '')}"
        )
        years = tuple(year for year in _years(text) if year <= REFERENCE_YEAR)
        if years:
            dated.append((max(years), item))
    if not dated:
        return [], [], 0.0
    latest = max(year for year, _ in dated)
    current = [item for year, item in dated if year == latest]
    historical = [item for year, item in dated if year < latest]
    return current, historical, 0.55


def _evidence_text(items: Sequence[Mapping[str, object]]) -> str:
    return " ".join(
        f"{item.get('official_source_title', '')} {item.get('snapshot_text', '')}"
        for item in items
    )


def _semantic_signals(sample: Mapping[str, object]) -> list[SignalInstance]:
    sample_id = str(sample["sample_id"])
    candidate = str(sample["candidate_text"])
    evidence = _evidence_items(sample)
    refs = _source_refs(sample)
    result = [
        _unavailable(
            sample_id,
            "mlm_masked_token_naturalness",
            SignalView.SEMANTIC,
            SignalComputationStatus.MODEL_UNAVAILABLE,
            "NO_FROZEN_MLM_MODEL",
            "No approved frozen MLM checkpoint/tokenizer is available locally.",
        ),
        _unavailable(
            sample_id,
            "ppl_naturalness",
            SignalView.SEMANTIC,
            SignalComputationStatus.MODEL_UNAVAILABLE,
            "NO_FROZEN_PPL_MODEL",
            "No approved frozen causal-LM checkpoint/tokenizer is available locally.",
        ),
    ]
    current, historical, role_confidence = _version_partition(evidence)
    similarities: dict[str, float] = {}
    if current:
        value = max(
            lexical_similarity(candidate, _evidence_text([item])) for item in current
        )
        similarities["current"] = value
        result.append(
            _computed(
                sample_id,
                "current_version_semantic_similarity",
                SignalView.SEMANTIC,
                value,
                role_confidence,
                "DETERMINISTIC_BIGRAM_SIMILARITY_YEAR_DERIVED_ROLE",
                "Character-bigram similarity to the Evidence item(s) with the latest observable year.",
                refs,
            )
        )
    else:
        result.append(
            _unavailable(
                sample_id,
                "current_version_semantic_similarity",
                SignalView.SEMANTIC,
                SignalComputationStatus.INPUT_MISSING,
                "VERSION_ROLE_METADATA_MISSING",
                "Evidence cannot be assigned a current-version role from frozen metadata.",
                refs=refs,
            )
        )
    if historical:
        value = max(
            lexical_similarity(candidate, _evidence_text([item])) for item in historical
        )
        similarities["historical"] = value
        result.append(
            _computed(
                sample_id,
                "historical_version_semantic_similarity",
                SignalView.SEMANTIC,
                value,
                role_confidence,
                "DETERMINISTIC_BIGRAM_SIMILARITY_YEAR_DERIVED_ROLE",
                "Character-bigram similarity to Evidence item(s) with an earlier observable year.",
                refs,
            )
        )
    else:
        result.append(
            _unavailable(
                sample_id,
                "historical_version_semantic_similarity",
                SignalView.SEMANTIC,
                SignalComputationStatus.INPUT_MISSING,
                "HISTORICAL_VERSION_ROLE_MISSING",
                "No distinct historical Evidence role can be derived without label-like identifiers.",
                refs=refs,
            )
        )
    result.append(
        _unavailable(
            sample_id,
            "top_k_semantic_similarity",
            SignalView.SEMANTIC,
            SignalComputationStatus.INPUT_MISSING,
            "QUERY_AND_RETRIEVAL_TRACE_MISSING",
            "No frozen query and independent retrieval trace exist for Final72.",
            refs=refs,
        )
    )
    if set(similarities) == {"current", "historical"}:
        result.append(
            _computed(
                sample_id,
                "semantic_version_margin",
                SignalView.SEMANTIC,
                similarities["historical"] - similarities["current"],
                role_confidence,
                "HISTORICAL_MINUS_CURRENT_SIMILARITY",
                "Historical similarity minus current similarity using predeclared version roles.",
                refs,
            )
        )
    else:
        result.append(
            _unavailable(
                sample_id,
                "semantic_version_margin",
                SignalView.SEMANTIC,
                SignalComputationStatus.INPUT_MISSING,
                "CURRENT_OR_HISTORICAL_SIMILARITY_MISSING",
                "Both version-specific similarities are required.",
                refs=refs,
            )
        )
    return result


def _entity_claim_signals(sample: Mapping[str, object]) -> list[SignalInstance]:
    sample_id = str(sample["sample_id"])
    candidate = str(sample["candidate_text"])
    evidence = _combined_evidence(sample)
    refs = _source_refs(sample)
    primary_subject = str(sample.get("primary_subject") or "")
    subjects = _books(candidate) or ((primary_subject,) if primary_subject else ())
    candidate_numbers = set(_numbers(candidate))
    evidence_numbers = set(_numbers(evidence))
    candidate_dates = set(_dates(candidate))
    evidence_dates = set(_dates(evidence))
    candidate_negation = _contains_any(candidate, _NEGATION)
    evidence_negation = _contains_any(evidence, _NEGATION)
    subject_match = bool(subjects) and all(
        _normalize(subject) in _normalize(evidence) for subject in subjects
    )
    predicate_score = lexical_similarity(candidate, evidence)
    predicate_match = predicate_score >= 0.08
    entity_conflict = bool(subjects) and not subject_match

    result = [
        _computed(
            sample_id,
            "subject_match",
            SignalView.ENTITY_CLAIM,
            subject_match,
            0.9,
            "TITLE_BINDING",
            "Candidate document subjects are checked against frozen Evidence.",
            refs,
        ),
        _computed(
            sample_id,
            "predicate_match",
            SignalView.ENTITY_CLAIM,
            predicate_match,
            0.55,
            "LEXICAL_RELATION_PROXY",
            "Deterministic lexical overlap is used as a predicate-alignment proxy.",
            refs,
            {"lexical_similarity": predicate_score},
        ),
        _computed(
            sample_id,
            "entity_conflict",
            SignalView.ENTITY_CLAIM,
            entity_conflict,
            0.8,
            "SUBJECT_ABSENCE_CONFLICT",
            "A document-entity conflict is flagged when a recoverable subject is absent from Evidence.",
            refs,
        ),
    ]

    if candidate_numbers:
        numeric_conflict = bool(candidate_numbers - evidence_numbers)
        result.append(
            _computed(
                sample_id,
                "numeric_conflict",
                SignalView.ENTITY_CLAIM,
                numeric_conflict,
                0.65,
                "EXPLICIT_NUMBER_SET_COMPARISON",
                "Explicit candidate numbers are compared with frozen Evidence numbers.",
                refs,
                {
                    "candidate_number_count": len(candidate_numbers),
                    "unsupported_number_count": len(
                        candidate_numbers - evidence_numbers
                    ),
                },
            )
        )
    else:
        result.append(
            _not_applicable(
                sample_id,
                "numeric_conflict",
                SignalView.ENTITY_CLAIM,
                "NO_NUMERIC_CLAIM",
                "Candidate contains no explicit numeric claim.",
                refs,
            )
        )

    if candidate_dates:
        result.append(
            _computed(
                sample_id,
                "date_conflict",
                SignalView.ENTITY_CLAIM,
                bool(candidate_dates - evidence_dates),
                0.8,
                "EXPLICIT_DATE_SET_COMPARISON",
                "Explicit full dates are compared with frozen Evidence dates.",
                refs,
            )
        )
    else:
        result.append(
            _not_applicable(
                sample_id,
                "date_conflict",
                SignalView.ENTITY_CLAIM,
                "NO_FULL_DATE_CLAIM",
                "Candidate contains no complete year-month date claim.",
                refs,
            )
        )

    for name, cues in (
        ("condition_conflict", _CONDITION),
        ("exception_conflict", _EXCEPTION),
    ):
        if _contains_any(candidate, cues):
            conflict = candidate_negation != evidence_negation and _contains_any(
                evidence, cues
            )
            result.append(
                _computed(
                    sample_id,
                    name,
                    SignalView.ENTITY_CLAIM,
                    conflict,
                    0.5,
                    "CUE_AND_POLARITY_COMPARISON",
                    "Condition/exception cues and proposition polarity are compared deterministically.",
                    refs,
                )
            )
        else:
            result.append(
                _not_applicable(
                    sample_id,
                    name,
                    SignalView.ENTITY_CLAIM,
                    f"NO_{name.upper()}_CLAIM",
                    "Candidate contains no applicable cue for this comparison.",
                    refs,
                )
            )

    negation_flip = candidate_negation != evidence_negation
    result.append(
        _computed(
            sample_id,
            "negation_flip",
            SignalView.ENTITY_CLAIM,
            negation_flip,
            0.5,
            "GLOBAL_NEGATION_CUE_COMPARISON",
            "Candidate and Evidence negation cues differ.",
            refs,
        )
    )
    conflict_values = [
        entity_conflict,
        bool(candidate_numbers and candidate_numbers - evidence_numbers),
        bool(candidate_dates and candidate_dates - evidence_dates),
        negation_flip,
    ]
    result.append(
        _computed(
            sample_id,
            "relation_conflict",
            SignalView.ENTITY_CLAIM,
            any(conflict_values),
            0.55,
            "RULE_COMPOSITE_RELATION_CONFLICT",
            "Composite of predeclared entity, number, date and polarity conflicts.",
            refs,
        )
    )
    return result


def _provenance_signals(sample: Mapping[str, object]) -> list[SignalInstance]:
    sample_id = str(sample["sample_id"])
    candidate = str(sample["candidate_text"])
    evidence_items = _evidence_items(sample)
    evidence = _combined_evidence(sample)
    refs = _source_refs(sample)
    urls = [str(item.get("official_source_url") or "") for item in evidence_items]
    official = bool(urls) and all(_official_url(url) for url in urls)
    subjects = _books(candidate)
    document_match = bool(subjects) and any(
        all(
            _normalize(subject)
            in _normalize(
                f"{item.get('official_source_title', '')} {item.get('snapshot_text', '')}"
            )
            for subject in subjects
        )
        for item in evidence_items
    )
    authorities = _authorities(candidate)
    version_claim = bool(_years(candidate)) or _contains_any(candidate, _VERSION)

    result = [
        _computed(
            sample_id,
            "official_source",
            SignalView.PROVENANCE,
            official,
            0.95,
            "OFFICIAL_HOST_POLICY",
            "All supplied Evidence URLs are checked against the frozen official-host policy.",
            refs,
        ),
        _unavailable(
            sample_id,
            "host_publisher_relation",
            SignalView.PROVENANCE,
            SignalComputationStatus.INPUT_MISSING,
            "PAGE_PUBLISHER_ROLE_NOT_STRUCTURED",
            "Frozen Evidence identifies the host but not a normalized page-publisher role.",
            refs=refs,
        ),
        _unavailable(
            sample_id,
            "publisher_issuer_match",
            SignalView.PROVENANCE,
            SignalComputationStatus.INPUT_MISSING,
            "ISSUING_AUTHORITY_ROLE_NOT_STRUCTURED",
            "Publisher and issuing-authority roles are not jointly normalized.",
            refs=refs,
        ),
    ]
    if authorities:
        match = all(
            _normalize(authority) in _normalize(evidence) for authority in authorities
        )
        result.append(
            _computed(
                sample_id,
                "claimed_authority_match",
                SignalView.PROVENANCE,
                match,
                0.7,
                "EXPLICIT_AUTHORITY_TEXT_BINDING",
                "Explicit candidate authority names are bound to frozen Evidence text.",
                refs,
                {"authority_count": len(authorities)},
            )
        )
    else:
        result.append(
            _not_applicable(
                sample_id,
                "claimed_authority_match",
                SignalView.PROVENANCE,
                "NO_AUTHORITY_CLAIM",
                "Candidate makes no explicit authority claim.",
                refs,
            )
        )
    result.append(
        _computed(
            sample_id,
            "document_identity_match",
            SignalView.PROVENANCE,
            document_match,
            0.85,
            "DOCUMENT_TITLE_BINDING",
            "Candidate document titles are bound to Evidence title/text.",
            refs,
        )
    )

    if version_claim:
        candidate_years = set(_years(candidate))
        evidence_years = set(_years(evidence))
        value = not candidate_years or bool(candidate_years & evidence_years)
        result.append(
            _computed(
                sample_id,
                "version_identity_match",
                SignalView.PROVENANCE,
                value,
                0.6,
                "VERSION_CUE_AND_YEAR_BINDING",
                "Explicit version cues and years are compared with Evidence.",
                refs,
            )
        )
    else:
        result.append(
            _not_applicable(
                sample_id,
                "version_identity_match",
                SignalView.PROVENANCE,
                "NO_VERSION_CLAIM",
                "Candidate makes no version claim.",
                refs,
            )
        )

    roles = [
        str(item.get("official_role") or "")
        for item in evidence_items
        if item.get("official_role")
    ]
    if roles:
        result.append(
            _computed(
                sample_id,
                "official_repost",
                SignalView.PROVENANCE,
                any("REPOST" in role for role in roles),
                0.75,
                "EXPLICIT_OFFICIAL_ROLE",
                "Official repost status is derived only from explicit frozen provenance roles.",
                refs,
            )
        )
    else:
        result.append(
            _unavailable(
                sample_id,
                "official_repost",
                SignalView.PROVENANCE,
                SignalComputationStatus.INPUT_MISSING,
                "OFFICIAL_ROLE_NOT_STRUCTURED",
                "No explicit issuing/reposting role is available.",
                refs=refs,
            )
        )

    components = [float(official), float(document_match)]
    if authorities:
        components.append(
            float(
                all(
                    _normalize(authority) in _normalize(evidence)
                    for authority in authorities
                )
            )
        )
    if len(components) >= 2:
        result.append(
            _computed(
                sample_id,
                "provenance_consistency",
                SignalView.PROVENANCE,
                sum(components) / len(components),
                0.6,
                "AVAILABLE_PROVENANCE_COMPONENT_MEAN",
                "Mean consistency across available official-source, document and authority bindings.",
                refs,
                {"component_count": len(components)},
            )
        )
    else:
        result.append(
            _unavailable(
                sample_id,
                "provenance_consistency",
                SignalView.PROVENANCE,
                SignalComputationStatus.INPUT_MISSING,
                "INSUFFICIENT_PROVENANCE_COMPONENTS",
                "At least two provenance components are required.",
                refs=refs,
            )
        )
    return result


def _temporal_signals(sample: Mapping[str, object]) -> list[SignalInstance]:
    sample_id = str(sample["sample_id"])
    candidate = str(sample["candidate_text"])
    evidence_items = _evidence_items(sample)
    refs = _source_refs(sample)
    current, historical, role_confidence = _version_partition(evidence_items)
    candidate_years = set(_years(candidate))
    evidence = _combined_evidence(sample)
    evidence_years = set(_years(evidence))
    version_claim = bool(candidate_years) or _contains_any(candidate, _VERSION)
    historical_cue = _contains_any(candidate, _HISTORICAL)
    current_cue = _contains_any(candidate, _CURRENT)
    result: list[SignalInstance] = []

    if current:
        current_text = _evidence_text(current)
        current_match = lexical_similarity(candidate, current_text) >= 0.08
        result.append(
            _computed(
                sample_id,
                "current_fact_match",
                SignalView.TEMPORAL_VERSION,
                current_match,
                role_confidence,
                "YEAR_DERIVED_CURRENT_FACT_PROXY",
                "Candidate is compared with the Evidence item(s) having the latest observable year.",
                refs,
            )
        )
    else:
        result.append(
            _unavailable(
                sample_id,
                "current_fact_match",
                SignalView.TEMPORAL_VERSION,
                SignalComputationStatus.INPUT_MISSING,
                "CURRENT_VERSION_ROLE_MISSING",
                "Current-version Evidence role cannot be derived.",
                refs=refs,
            )
        )
    if historical:
        historical_text = _evidence_text(historical)
        historical_match = lexical_similarity(candidate, historical_text) >= 0.08
        result.append(
            _computed(
                sample_id,
                "historical_fact_match",
                SignalView.TEMPORAL_VERSION,
                historical_match,
                role_confidence,
                "YEAR_DERIVED_HISTORICAL_FACT_PROXY",
                "Candidate is compared with earlier-year Evidence item(s).",
                refs,
            )
        )
    else:
        result.append(
            _unavailable(
                sample_id,
                "historical_fact_match",
                SignalView.TEMPORAL_VERSION,
                SignalComputationStatus.INPUT_MISSING,
                "HISTORICAL_VERSION_ROLE_MISSING",
                "No distinct historical Evidence role can be derived.",
                refs=refs,
            )
        )

    if version_claim:
        mismatch = bool(candidate_years) and not bool(candidate_years & evidence_years)
        result.append(
            _computed(
                sample_id,
                "version_mismatch",
                SignalView.TEMPORAL_VERSION,
                mismatch,
                0.7,
                "EXPLICIT_VERSION_YEAR_COMPARISON",
                "Candidate version years are compared with frozen Evidence years.",
                refs,
            )
        )
    else:
        result.append(
            _not_applicable(
                sample_id,
                "version_mismatch",
                SignalView.TEMPORAL_VERSION,
                "NO_VERSION_CLAIM",
                "Candidate makes no version claim.",
                refs,
            )
        )

    if candidate_years and evidence_years:
        successor = max(evidence_years) > min(candidate_years)
        distance = (
            min(abs(max(evidence_years) - year) for year in candidate_years) / 50.0
        )
        result.append(
            _computed(
                sample_id,
                "superseded_version",
                SignalView.TEMPORAL_VERSION,
                successor and historical_cue,
                0.65,
                "YEAR_ORDER_AND_HISTORICAL_CUE",
                "Later Evidence year plus an explicit historical cue indicates a superseded version.",
                refs,
            )
        )
        result.append(
            _computed(
                sample_id,
                "successor_exists",
                SignalView.TEMPORAL_VERSION,
                successor,
                0.65,
                "OBSERVABLE_YEAR_ORDER",
                "A later Evidence year is treated as an observable successor indicator.",
                refs,
            )
        )
        result.append(
            _computed(
                sample_id,
                "version_distance",
                SignalView.TEMPORAL_VERSION,
                min(1.0, distance),
                0.6,
                "NORMALIZED_YEAR_DISTANCE",
                "Absolute claimed-to-latest Evidence year distance normalized by 50 years.",
                refs,
            )
        )
    else:
        for name in ("superseded_version", "successor_exists", "version_distance"):
            result.append(
                _unavailable(
                    sample_id,
                    name,
                    SignalView.TEMPORAL_VERSION,
                    SignalComputationStatus.INPUT_MISSING,
                    "CLAIMED_OR_EVIDENCE_YEAR_MISSING",
                    "Both candidate and Evidence year identities are required.",
                    refs=refs,
                )
            )

    candidate_dates = set(_dates(candidate))
    evidence_dates = set(_dates(evidence))
    if candidate_dates and _contains_any(candidate, ("施行", "生效", "废止")):
        result.append(
            _computed(
                sample_id,
                "effective_interval_conflict",
                SignalView.TEMPORAL_VERSION,
                bool(candidate_dates - evidence_dates),
                0.8,
                "EXPLICIT_EFFECTIVE_DATE_COMPARISON",
                "Explicit candidate effective dates are compared with frozen Evidence dates.",
                refs,
            )
        )
    else:
        result.append(
            _not_applicable(
                sample_id,
                "effective_interval_conflict",
                SignalView.TEMPORAL_VERSION,
                "NO_EXPLICIT_EFFECTIVE_DATE_CLAIM",
                "Candidate has no complete effective-date claim.",
                refs,
            )
        )

    if candidate_years and evidence_years and (historical_cue or current_cue):
        binding_conflict = current_cue and max(evidence_years) > min(candidate_years)
        result.append(
            _computed(
                sample_id,
                "current_history_binding_conflict",
                SignalView.TEMPORAL_VERSION,
                binding_conflict,
                0.6,
                "CURRENT_CUE_WITH_YEAR_ORDER",
                "Current-language cues are checked against a later observable Evidence year.",
                refs,
            )
        )
    else:
        result.append(
            _not_applicable(
                sample_id,
                "current_history_binding_conflict",
                SignalView.TEMPORAL_VERSION,
                "NO_EXPLICIT_CURRENT_HISTORY_BINDING",
                "Candidate lacks enough explicit current/history binding information.",
                refs,
            )
        )

    if candidate_years and evidence_years and historical_cue:
        historical_support = bool(candidate_years & evidence_years)
        latest = max(evidence_years)
        version_sensitive = historical_support and latest > min(candidate_years)
        current_support = historical_support and min(candidate_years) == latest
        misbinding = version_sensitive and current_cue
        result.append(
            _computed(
                sample_id,
                "present_time_substitution_signal",
                SignalView.TEMPORAL_VERSION,
                misbinding,
                0.55,
                "AUDITABLE_PRESENT_TIME_SUBSTITUTION_PROXY",
                "Historical support and later Evidence year are evaluated without using class labels.",
                refs,
                {
                    "historical_support": historical_support,
                    "current_support": current_support,
                    "version_sensitive": version_sensitive,
                    "current_misbinding_indicator": misbinding,
                },
            )
        )
    else:
        result.append(
            _unavailable(
                sample_id,
                "present_time_substitution_signal",
                SignalView.TEMPORAL_VERSION,
                SignalComputationStatus.INPUT_MISSING,
                "PRESENT_TIME_SUBSTITUTION_INPUTS_INCOMPLETE",
                "Historical qualifier, candidate year and Evidence year are all required.",
                refs=refs,
            )
        )
    return result


def _retrieval_signals(sample: Mapping[str, object]) -> list[SignalInstance]:
    sample_id = str(sample["sample_id"])
    refs = _source_refs(sample)
    return [
        _unavailable(
            sample_id,
            definition.signal_name,
            SignalView.RETRIEVAL_BEHAVIOR,
            SignalComputationStatus.INPUT_MISSING,
            "FROZEN_QUERY_AND_RETRIEVAL_TRACE_MISSING",
            "Final72 has no frozen query, retriever configuration, top-k trace, or comparable score run.",
            refs=refs,
        )
        for definition in FIVE_VIEW_SIGNAL_REGISTRY
        if definition.view is SignalView.RETRIEVAL_BEHAVIOR
    ]


def extract_sample_signals(sample: Mapping[str, object]) -> list[SignalInstance]:
    """Extract all 42 signals without accepting any label-bearing argument."""

    validate_orientation_contract()
    required = {"sample_id", "candidate_text", "source_title", "evidence"}
    missing = required - set(sample)
    if missing:
        raise ValueError(f"safe projection row missing fields: {sorted(missing)}")
    records = [
        *_semantic_signals(sample),
        *_entity_claim_signals(sample),
        *_provenance_signals(sample),
        *_temporal_signals(sample),
        *_retrieval_signals(sample),
    ]
    if len(records) != len(FIVE_VIEW_SIGNAL_REGISTRY):
        raise ValueError(f"expected 42 signals, got {len(records)}")
    if len({record.signal_name for record in records}) != len(records):
        raise ValueError("duplicate signal name in sample extraction")
    return records


def instance_to_dict(instance: SignalInstance) -> dict[str, object]:
    payload = asdict(instance)
    payload["view"] = instance.view.value
    payload["computation_status"] = instance.computation_status.value
    payload["orientation"] = instance.orientation.value
    payload["source_refs"] = list(instance.source_refs)
    return payload


def numeric_value(record: Mapping[str, object]) -> float | None:
    if record.get("computation_status") != SignalComputationStatus.COMPUTED.value:
        return None
    value = record.get("value")
    if isinstance(value, bool):
        return float(value)
    if isinstance(value, (int, float)) and math.isfinite(float(value)):
        return float(value)
    return None


def oriented_value(record: Mapping[str, object]) -> float | None:
    value = numeric_value(record)
    if value is None:
        return None
    orientation = record.get("orientation")
    if orientation == SignalOrientation.HIGHER_IS_RISKIER.value:
        return value
    if orientation == SignalOrientation.LOWER_IS_RISKIER.value:
        return -value
    return None


def cliffs_delta(left: Sequence[float], right: Sequence[float]) -> float | None:
    if not left or not right:
        return None
    greater = sum(a > b for a in left for b in right)
    lower = sum(a < b for a in left for b in right)
    return (greater - lower) / (len(left) * len(right))


def mann_whitney_u(left: Sequence[float], right: Sequence[float]) -> float | None:
    if not left or not right:
        return None
    wins = sum(a > b for a in left for b in right)
    ties = sum(a == b for a in left for b in right)
    return wins + 0.5 * ties


def diagnostic_auroc(
    positive: Sequence[float], negative: Sequence[float]
) -> float | None:
    u_value = mann_whitney_u(positive, negative)
    if u_value is None:
        return None
    return u_value / (len(positive) * len(negative))


def diagnostic_average_precision(
    positive: Sequence[float], negative: Sequence[float]
) -> float | None:
    if not positive or not negative:
        return None
    grouped: dict[float, list[int]] = {}
    for value, label in [(item, 1) for item in positive] + [
        (item, 0) for item in negative
    ]:
        grouped.setdefault(value, []).append(label)
    true_positive = 0
    seen = 0
    precision_sum = 0.0
    for value in sorted(grouped, reverse=True):
        labels = grouped[value]
        group_positive = sum(labels)
        true_positive += group_positive
        seen += len(labels)
        precision_sum += (true_positive / seen) * group_positive
    return precision_sum / len(positive)


def percentile(values: Sequence[float], probability: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    position = (len(ordered) - 1) * probability
    low = math.floor(position)
    high = math.ceil(position)
    if low == high:
        return ordered[low]
    return ordered[low] + (ordered[high] - ordered[low]) * (position - low)


def describe(values: Sequence[float]) -> dict[str, float | int | None]:
    if not values:
        return {
            "count": 0,
            "mean": None,
            "median": None,
            "std": None,
            "iqr": None,
            "min": None,
            "max": None,
        }
    mean = sum(values) / len(values)
    variance = sum((value - mean) ** 2 for value in values) / max(1, len(values) - 1)
    q1 = percentile(values, 0.25)
    q3 = percentile(values, 0.75)
    return {
        "count": len(values),
        "mean": mean,
        "median": percentile(values, 0.5),
        "std": math.sqrt(variance),
        "iqr": None if q1 is None or q3 is None else q3 - q1,
        "min": min(values),
        "max": max(values),
    }


def rankdata(values: Sequence[float]) -> list[float]:
    indexed = sorted(enumerate(values), key=lambda item: item[1])
    ranks = [0.0] * len(values)
    start = 0
    while start < len(indexed):
        end = start + 1
        while end < len(indexed) and indexed[end][1] == indexed[start][1]:
            end += 1
        rank = (start + 1 + end) / 2.0
        for original_index, _ in indexed[start:end]:
            ranks[original_index] = rank
        start = end
    return ranks


def spearman(left: Sequence[float], right: Sequence[float]) -> float | None:
    if len(left) != len(right) or len(left) < 3:
        return None
    lhs = rankdata(left)
    rhs = rankdata(right)
    lhs_mean = sum(lhs) / len(lhs)
    rhs_mean = sum(rhs) / len(rhs)
    numerator = sum(
        (a - lhs_mean) * (b - rhs_mean) for a, b in zip(lhs, rhs, strict=True)
    )
    lhs_den = math.sqrt(sum((a - lhs_mean) ** 2 for a in lhs))
    rhs_den = math.sqrt(sum((b - rhs_mean) ** 2 for b in rhs))
    if lhs_den == 0 or rhs_den == 0:
        return None
    return numerator / (lhs_den * rhs_den)


def forbidden_key_hits(value: object, forbidden: set[str]) -> list[str]:
    hits: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            if str(key).lower() in forbidden:
                hits.append(str(key))
            hits.extend(forbidden_key_hits(nested, forbidden))
    elif isinstance(value, list):
        for nested in value:
            hits.extend(forbidden_key_hits(nested, forbidden))
    return hits


def finite_or_none(values: Iterable[float | None]) -> bool:
    return all(value is None or math.isfinite(value) for value in values)


__all__ = [
    "EXTRACTOR_VERSION",
    "REFERENCE_YEAR",
    "SIGNAL_ORIENTATIONS",
    "cliffs_delta",
    "describe",
    "diagnostic_auroc",
    "diagnostic_average_precision",
    "extract_sample_signals",
    "finite_or_none",
    "forbidden_key_hits",
    "instance_to_dict",
    "lexical_similarity",
    "mann_whitney_u",
    "numeric_value",
    "oriented_value",
    "spearman",
    "validate_orientation_contract",
]
