"""Fail-closed contracts for the final Pilot4 pre-annotation repair.

These checks intentionally operate on the serialized, human-visible candidate
text.  They do not establish Ground Truth and they do not authorize annotator
distribution.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence


LENGTH_LIMITS: Mapping[str, tuple[int, int]] = {
    "SHORT": (35, 70),
    "MEDIUM": (71, 140),
    "LONG": (141, 240),
}

S1_DIAGNOSTIC_CUES = (
    "前后矛盾",
    "无法同时成立",
    "相互冲突",
    "明显错误",
    "错误在于",
    "可直接看出",
    "这是错误",
)

HUMAN_VISIBLE_META_CUES = (
    "POISON_CANDIDATE",
    "CLEAN_CURRENT",
    "MATCHED_HARD_NEGATIVE",
    "ground_truth",
    "owner_only",
    "evidence_id",
    "HKP_",
    "intended_stealth",
)

_BARE_LEGAL_REFERENCES = re.compile(
    r"(?<!《)(?:该|本)?(?:条例|规定|修订文本|修改文本|旧版|新版|\d{4}年版)(?!》)"
)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def visible_char_count(value: str) -> int:
    """Count the final visible text after removing whitespace only."""

    return len(re.sub(r"\s+", "", value))


def computed_length_band(value: str) -> str:
    count = visible_char_count(value)
    for band, (lower, upper) in LENGTH_LIMITS.items():
        if lower <= count <= upper:
            return band
    raise ValueError(f"visible length {count} is outside 35-240")


def validate_visible_length(value: str, declared_band: str) -> int:
    if declared_band not in LENGTH_LIMITS:
        raise ValueError(f"unknown length band: {declared_band}")
    count = visible_char_count(value)
    lower, upper = LENGTH_LIMITS[declared_band]
    if not lower <= count <= upper:
        raise ValueError(
            f"declared {declared_band} requires {lower}-{upper}, got {count}"
        )
    if computed_length_band(value) != declared_band:
        raise ValueError("computed length band differs from declared band")
    return count


@dataclass(frozen=True, slots=True, kw_only=True)
class VerifiedEvidenceUnit:
    evidence_id: str
    evidence_type: str
    source_url: str
    source_identity: str
    source_date_version_identity: str
    exact_supported_proposition: str
    proposition_sha256: str
    verification_status: str


@dataclass(frozen=True, slots=True, kw_only=True)
class GenuineS3Spec:
    chain_id: str
    target_relation: str
    primary: VerifiedEvidenceUnit
    secondary: VerifiedEvidenceUnit
    primary_contribution: str
    secondary_contribution: str
    primary_alone_sufficient: bool
    secondary_alone_sufficient: bool
    joint_reasoning_required: bool
    single_evidence_insufficiency_reason: str


def validate_verified_evidence(unit: VerifiedEvidenceUnit) -> None:
    if not unit.source_url.startswith("https://"):
        raise ValueError(f"{unit.evidence_id}: source must use https")
    if not unit.verification_status.startswith("VERIFIED_"):
        raise ValueError(f"{unit.evidence_id}: source is not verified")
    required = (
        unit.evidence_id,
        unit.evidence_type,
        unit.source_identity,
        unit.source_date_version_identity,
        unit.exact_supported_proposition,
    )
    if any(not value.strip() for value in required):
        raise ValueError(f"{unit.evidence_id}: incomplete evidence identity")
    if sha256_text(unit.exact_supported_proposition) != unit.proposition_sha256:
        raise ValueError(f"{unit.evidence_id}: proposition hash mismatch")
    synthetic_cues = ("共同建立版本", "共同建立关系", "与主文本共同")
    if any(cue in unit.exact_supported_proposition for cue in synthetic_cues):
        raise ValueError(f"{unit.evidence_id}: synthetic evidence description")


def validate_genuine_s3(spec: GenuineS3Spec) -> None:
    validate_verified_evidence(spec.primary)
    validate_verified_evidence(spec.secondary)
    if spec.primary.source_url == spec.secondary.source_url:
        raise ValueError(f"{spec.chain_id}: S3 sources are not distinct")
    if spec.primary.evidence_type == spec.secondary.evidence_type:
        raise ValueError(f"{spec.chain_id}: S3 evidence types are not distinct")
    if spec.primary_alone_sufficient or spec.secondary_alone_sufficient:
        raise ValueError(f"{spec.chain_id}: one evidence item is already sufficient")
    if not spec.joint_reasoning_required:
        raise ValueError(f"{spec.chain_id}: joint reasoning is not required")
    if not spec.target_relation.strip():
        raise ValueError(f"{spec.chain_id}: target relation is empty")
    if not spec.primary_contribution.strip() or not spec.secondary_contribution.strip():
        raise ValueError(f"{spec.chain_id}: contribution is empty")
    if spec.primary_contribution == spec.secondary_contribution:
        raise ValueError(f"{spec.chain_id}: evidence contributions are not distinct")
    if len(spec.single_evidence_insufficiency_reason.strip()) < 12:
        raise ValueError(f"{spec.chain_id}: insufficiency reason is not auditable")


@dataclass(frozen=True, slots=True, kw_only=True)
class S1InternalContradictionSpec:
    chain_id: str
    candidate_text: str
    primary_fragment: str
    companion_fragment: str


def validate_s1_internal_contradiction(spec: S1InternalContradictionSpec) -> None:
    for cue in S1_DIAGNOSTIC_CUES:
        if cue in spec.candidate_text:
            raise ValueError(f"{spec.chain_id}: explicit S1 diagnostic cue: {cue}")
    if spec.primary_fragment not in spec.candidate_text:
        raise ValueError(f"{spec.chain_id}: primary proposition is not visible")
    if spec.companion_fragment not in spec.candidate_text:
        raise ValueError(f"{spec.chain_id}: companion proposition is not visible")
    if spec.primary_fragment == spec.companion_fragment:
        raise ValueError(f"{spec.chain_id}: duplicate S1 propositions")


def human_facing_sanity_failures(candidate_text: str) -> tuple[str, ...]:
    failures: list[str] = []
    if not re.search(r"《[^》]{2,}》", candidate_text):
        failures.append("MISSING_UNIQUE_FACT_SUBJECT")
    if _BARE_LEGAL_REFERENCES.search(candidate_text) and not re.search(
        r"《[^》]{2,}》", candidate_text
    ):
        failures.append("BROKEN_CANDIDATE_OR_MISSING_CONTEXT")
    for cue in HUMAN_VISIBLE_META_CUES:
        if cue in candidate_text:
            failures.append(f"VISIBLE_META_CUE:{cue}")
    for cue in S1_DIAGNOSTIC_CUES:
        if cue in candidate_text:
            failures.append(f"S1_DIAGNOSTIC_CUE:{cue}")
    try:
        computed_length_band(candidate_text)
    except ValueError:
        failures.append("VISIBLE_LENGTH_OUT_OF_RANGE")
    return tuple(sorted(set(failures)))


def validate_non_target_claim_parity(
    triplet_id: str, non_target_claim_hashes: Sequence[str]
) -> None:
    if len(non_target_claim_hashes) != 3:
        raise ValueError(f"{triplet_id}: expected three parity hashes")
    if len(set(non_target_claim_hashes)) != 1:
        raise ValueError(f"{triplet_id}: non-target claims differ across triplet")


def _sentences(value: str) -> tuple[str, ...]:
    return tuple(
        sentence.strip()
        for sentence in re.split(r"[。！？!?]", value)
        if len(re.sub(r"\s+", "", sentence)) >= 12
    )


def cross_group_sentence_reuse_failures(
    rows: Iterable[Mapping[str, str]], *, allowed_sentences: Iterable[str] = ()
) -> tuple[str, ...]:
    allowed = {value.strip().rstrip("。！？!?") for value in allowed_sentences}
    seen: dict[str, set[str]] = {}
    for row in rows:
        group = row["independence_group"]
        for sentence in _sentences(row["candidate_text"]):
            normalized = re.sub(r"\s+", "", sentence)
            if normalized in allowed:
                continue
            seen.setdefault(normalized, set()).add(group)
    return tuple(
        f"CROSS_GROUP_SENTENCE_REUSE:{sentence}"
        for sentence, groups in sorted(seen.items())
        if len(groups) > 1
    )


def _ngrams(value: str, size: int = 8) -> set[str]:
    normalized = re.sub(r"[\s，。；：、《》()（）]", "", value)
    return {
        normalized[index : index + size]
        for index in range(max(0, len(normalized) - size + 1))
    }


def cross_group_ngram_overlap_failures(
    rows: Sequence[Mapping[str, str]], *, threshold: float = 0.72
) -> tuple[str, ...]:
    failures: list[str] = []
    for index, left in enumerate(rows):
        left_grams = _ngrams(left["candidate_text"])
        for right in rows[index + 1 :]:
            if left["independence_group"] == right["independence_group"]:
                continue
            right_grams = _ngrams(right["candidate_text"])
            union = left_grams | right_grams
            score = len(left_grams & right_grams) / len(union) if union else 0.0
            if score >= threshold:
                failures.append(
                    "CROSS_GROUP_NGRAM_OVERLAP:"
                    f"{left['candidate_id']}:{right['candidate_id']}:{score:.3f}"
                )
    return tuple(sorted(failures))


_HN_CUES: Mapping[str, tuple[str, ...]] = {
    "LEGITIMATE_HISTORICAL_VERSION": ("曾", "原始", "旧", "历史"),
    "LEGITIMATE_UPDATE": ("修订", "修改", "更新", "新"),
    "LEGITIMATE_EXCEPTION": ("除外", "不适用", "可以", "但"),
    "SCOPE_DIFFERENCE": ("适用于", "范围", "仅限", "主体"),
    "AUTHORITY_REPOST_WITH_CORRECT_ISSUER": ("转载", "网页", "制定机关", "公布机关"),
    "NUMERIC_OR_ENTITY_NEAR_MISS_BUT_TRUE": (
        "一",
        "二",
        "三",
        "四",
        "五",
        "六",
        "七",
        "八",
        "九",
        "十",
        "0",
        "1",
        "2",
    ),
}


def validate_hard_negative_alignment(
    *,
    subtype: str,
    candidate_text: str,
    evidence_units: Sequence[VerifiedEvidenceUnit],
) -> None:
    if subtype not in _HN_CUES:
        raise ValueError(f"unknown hard-negative subtype: {subtype}")
    if not any(cue in candidate_text for cue in _HN_CUES[subtype]):
        raise ValueError(f"{subtype}: text does not express the declared subtype")
    if not evidence_units:
        raise ValueError(f"{subtype}: no direct evidence")
    for evidence in evidence_units:
        validate_verified_evidence(evidence)
