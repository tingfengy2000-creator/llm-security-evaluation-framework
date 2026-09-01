"""Fail-closed structural leakage checks for Pilot0 synthetic data."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Mapping, Protocol

from .groups import GroupIdentityRecord
from .schema import LeakageBlocker
from .splits import SplitAssignment, validate_group_split
from .visibility import RuntimeAudience, assert_no_label_leakage


@dataclass(frozen=True, slots=True, kw_only=True)
class LeakageDocument:
    record_id: str
    text: str
    group_identity: GroupIdentityRecord
    split: str


@dataclass(frozen=True, slots=True, kw_only=True)
class LeakageFinding:
    check_name: str
    left_record_id: str
    right_record_id: str
    detail: str


class SemanticScanStatus(str, Enum):
    NOT_IMPLEMENTED = "NOT_IMPLEMENTED"
    OPERATIONAL = "OPERATIONAL"


class SemanticNearDuplicateScanner(Protocol):
    status: SemanticScanStatus

    def scan(self, documents: tuple[LeakageDocument, ...], *, required: bool) -> tuple[LeakageFinding, ...]: ...


class UnimplementedSemanticNearDuplicateScanner:
    status = SemanticScanStatus.NOT_IMPLEMENTED

    def scan(
        self, documents: tuple[LeakageDocument, ...], *, required: bool
    ) -> tuple[LeakageFinding, ...]:
        del documents
        if required:
            raise LeakageBlocker("SEMANTIC_NEAR_DUPLICATE_NOT_IMPLEMENTED")
        return ()


def _character_ngrams(text: str, size: int = 3) -> frozenset[str]:
    compact = _normalized_text(text)
    if len(compact) < size:
        return frozenset({compact}) if compact else frozenset()
    return frozenset(compact[index : index + size] for index in range(len(compact) - size + 1))


def _template_text(text: str) -> str:
    normalized = unicodedata.normalize("NFKC", text).casefold()
    normalized = re.sub(r"《[^》]+》", "《SUBJECT》", normalized)
    normalized = re.sub(r"\d+(?:\.\d+)?", "#", normalized)
    return re.sub(r"\s+", "", normalized)


class DeterministicSemanticNearDuplicateScanner:
    """Conservative lexical-semantic scanner for future split safety.

    The implementation is dependency-free and deterministic.  It combines
    character n-gram similarity with template, entity, version-chain and source
    family overlap.  Findings within one matched triplet are expected and are
    explicitly suppressed; cross-independence-group findings are blockers.
    """

    status = SemanticScanStatus.OPERATIONAL

    def __init__(self, *, similarity_threshold: float = 0.78) -> None:
        if not 0.0 < similarity_threshold <= 1.0:
            raise ValueError("similarity_threshold must be within (0, 1]")
        self.similarity_threshold = similarity_threshold

    def scan(
        self, documents: tuple[LeakageDocument, ...], *, required: bool
    ) -> tuple[LeakageFinding, ...]:
        del required
        findings: list[LeakageFinding] = []
        ordered = sorted(documents, key=lambda item: item.record_id)
        for index, left in enumerate(ordered):
            for right in ordered[index + 1 :]:
                same_triplet = (
                    left.group_identity.version_chain_id
                    == right.group_identity.version_chain_id
                )
                if same_triplet:
                    continue
                left_grams = _character_ngrams(left.text)
                right_grams = _character_ngrams(right.text)
                union = left_grams | right_grams
                similarity = len(left_grams & right_grams) / len(union) if union else 1.0
                template_match = _template_text(left.text) == _template_text(right.text)
                identity_overlap = sum(
                    (
                        left.group_identity.entity_id == right.group_identity.entity_id,
                        left.group_identity.version_chain_id
                        == right.group_identity.version_chain_id,
                        left.group_identity.source_document_family
                        == right.group_identity.source_document_family,
                    )
                )
                if similarity >= self.similarity_threshold or identity_overlap >= 2:
                    findings.append(
                        LeakageFinding(
                            check_name="semantic_near_duplicate",
                            left_record_id=left.record_id,
                            right_record_id=right.record_id,
                            detail=(
                                f"similarity={similarity:.4f};template={template_match};"
                                f"identity_overlap={identity_overlap};cross_independence_group=true"
                            ),
                        )
                    )
        return tuple(findings)


def _normalized_text(text: str) -> str:
    normalized = unicodedata.normalize("NFKC", text).casefold()
    return re.sub(r"\W+", "", normalized)


def scan_exact_duplicates(documents: Iterable[LeakageDocument]) -> tuple[LeakageFinding, ...]:
    return _scan_text(documents, lambda text: text, "exact_duplicate")


def scan_normalized_duplicates(
    documents: Iterable[LeakageDocument],
) -> tuple[LeakageFinding, ...]:
    return _scan_text(documents, _normalized_text, "normalized_duplicate")


def _scan_text(
    documents: Iterable[LeakageDocument], normalizer, check_name: str  # type: ignore[no-untyped-def]
) -> tuple[LeakageFinding, ...]:
    owners: dict[str, LeakageDocument] = {}
    findings: list[LeakageFinding] = []
    for document in sorted(documents, key=lambda item: item.record_id):
        key = normalizer(document.text)
        previous = owners.get(key)
        if previous is not None and previous.split != document.split:
            findings.append(
                LeakageFinding(
                    check_name=check_name,
                    left_record_id=previous.record_id,
                    right_record_id=document.record_id,
                    detail="duplicate content crosses split",
                )
            )
        else:
            owners[key] = document
    return tuple(findings)


def scan_identity_leakage(
    documents: Iterable[LeakageDocument], *, attribute: str
) -> tuple[LeakageFinding, ...]:
    allowed = {
        "entity_id",
        "version_chain_id",
        "source_document_family",
        "mutation_template_family",
    }
    if attribute not in allowed:
        raise LeakageBlocker("UNSUPPORTED_LEAKAGE_SCAN")
    owners: dict[str, LeakageDocument] = {}
    findings: list[LeakageFinding] = []
    for document in sorted(documents, key=lambda item: item.record_id):
        value = getattr(document.group_identity, attribute)
        previous = owners.get(value)
        if previous is not None and previous.split != document.split:
            findings.append(
                LeakageFinding(
                    check_name=f"{attribute}_leakage",
                    left_record_id=previous.record_id,
                    right_record_id=document.record_id,
                    detail=f"{attribute} crosses split",
                )
            )
        else:
            owners[value] = document
    return tuple(findings)


def assert_no_structural_leakage(
    documents: tuple[LeakageDocument, ...], assignments: tuple[SplitAssignment, ...]
) -> None:
    validate_group_split(assignments)
    findings = [*scan_exact_duplicates(documents), *scan_normalized_duplicates(documents)]
    for attribute in (
        "entity_id",
        "mutation_template_family",
        "version_chain_id",
        "source_document_family",
    ):
        findings.extend(scan_identity_leakage(documents, attribute=attribute))
    if findings:
        raise LeakageBlocker(f"DATA_SPLIT_LEAKAGE_BLOCKER: {findings[0].check_name}")


def assert_metadata_isolated(
    metadata: Mapping[str, object], *, forbidden_values: frozenset[str] = frozenset()
) -> None:
    assert_no_label_leakage(
        metadata, audience=RuntimeAudience.RETRIEVER, forbidden_values=forbidden_values
    )


def assert_embedding_input_isolated(
    embedding_input: object, *, forbidden_values: frozenset[str] = frozenset()
) -> None:
    assert_no_label_leakage(
        embedding_input,
        audience=RuntimeAudience.EMBEDDING,
        forbidden_values=forbidden_values,
    )


__all__ = [
    "LeakageDocument",
    "LeakageFinding",
    "DeterministicSemanticNearDuplicateScanner",
    "SemanticNearDuplicateScanner",
    "SemanticScanStatus",
    "UnimplementedSemanticNearDuplicateScanner",
    "assert_embedding_input_isolated",
    "assert_metadata_isolated",
    "assert_no_structural_leakage",
    "scan_exact_duplicates",
    "scan_identity_leakage",
    "scan_normalized_duplicates",
]
