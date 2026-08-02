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
