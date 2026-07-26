"""Stable, sensitive contracts for deterministic retrieved context packages."""

from __future__ import annotations

import hashlib
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field

from .errors import (
    ContextBuildConfigurationError,
    ContextConstructionIntegrityError,
)
from .evidence_envelope import CitationBinding, CitationMode, EvidenceEnvelope
from .hashing import canonical_json_sha256
from .identifiers import require_evidence_uid, require_public_identifier, require_public_query_id, require_sha256

_JSON_SAFE_MAX = 2**53 - 1
_DECISION_CODES = frozenset(
    {
        "INCLUDED",
        "MAX_EVIDENCE_COUNT_EXCLUDED",
        "NOT_ATTEMPTED_INSTRUCTION_BUDGET_EXHAUSTED",
        "BUDGET_EXCLUDED",
        "NOT_ATTEMPTED_AFTER_BUDGET_CUTOFF",
    }
)
_ABSTENTION_REASONS = frozenset(
    {
        "EMPTY_RETRIEVAL",
        "CONTEXT_BUDGET_EXHAUSTED",
        "NO_COMPLETE_EVIDENCE_BLOCK_FITS",
    }
)


def _invalid_config() -> ContextBuildConfigurationError:
    return ContextBuildConfigurationError("context build configuration is invalid")


def _invalid_package() -> ContextConstructionIntegrityError:
    return ContextConstructionIntegrityError("retrieved context package is invalid")


def _require_positive_json_int(value: object) -> int:
    if type(value) is not int or not 0 < value <= _JSON_SAFE_MAX:
        raise _invalid_config()
    return value


def _require_nonnegative_json_int(value: object) -> int:
    if type(value) is not int or not 0 <= value <= _JSON_SAFE_MAX:
        raise _invalid_package()
    return value


def _tuple_of_uids(value: object) -> tuple[str, ...]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise _invalid_package()
    items = tuple(value)
    try:
        for item in items:
            require_evidence_uid(item)
    except ValueError as error:
        raise _invalid_package() from error
    return items


def _unique_ordered_subset(values: tuple[str, ...], stable: tuple[str, ...]) -> bool:
    return len(values) == len(set(values)) and tuple(item for item in stable if item in set(values)) == values


def _canonical_trace_payload(
    *,
    trace_schema_version: str,
    request_id: str,
    query_id: str,
    corpus_snapshot_id: str,
    context_build_config_hash: str,
    input_evidence_count: int,
    deduplicated_evidence_count: int,
    count_selected_count: int,
    resolved_count: int,
    included_count: int,
    stable_candidate_uids: tuple[str, ...],
    count_selected_uids: tuple[str, ...],
    max_count_excluded_uids: tuple[str, ...],
    resolved_uids: tuple[str, ...],
    included_uids: tuple[str, ...],
    budget_excluded_uids: tuple[str, ...],
    instruction_budget_not_attempted_uids: tuple[str, ...],
    not_attempted_after_budget_cutoff_uids: tuple[str, ...],
    decision_codes: tuple[str, ...],
) -> dict[str, object]:
    return {
        "budget_excluded_uids": list(budget_excluded_uids),
        "context_build_config_hash": context_build_config_hash,
        "corpus_snapshot_id": corpus_snapshot_id,
        "count_selected_count": count_selected_count,
        "count_selected_uids": list(count_selected_uids),
        "decision_codes": list(decision_codes),
        "deduplicated_evidence_count": deduplicated_evidence_count,
        "included_count": included_count,
        "included_uids": list(included_uids),
        "input_evidence_count": input_evidence_count,
        "instruction_budget_not_attempted_uids": list(instruction_budget_not_attempted_uids),
        "max_count_excluded_uids": list(max_count_excluded_uids),
        "not_attempted_after_budget_cutoff_uids": list(not_attempted_after_budget_cutoff_uids),
        "query_id": query_id,
        "request_id": request_id,
        "resolved_count": resolved_count,
        "resolved_uids": list(resolved_uids),
        "stable_candidate_uids": list(stable_candidate_uids),
        "trace_schema_version": trace_schema_version,
    }


@dataclass(frozen=True, slots=True, kw_only=True)
class ContextBuildConfig:
    """Public deterministic limits for one future context construction run."""

    context_schema_version: str
    max_evidence_count: int
    max_context_characters: int

    def __post_init__(self) -> None:
        try:
            require_public_identifier(self.context_schema_version, "context_schema_version")
        except ValueError as error:
            raise _invalid_config() from error
        _require_positive_json_int(self.max_evidence_count)
        _require_positive_json_int(self.max_context_characters)

    @property
    def context_build_config_hash(self) -> str:
        return canonical_json_sha256(self._identity_payload())

    def _identity_payload(self) -> dict[str, object]:
        return {
            "context_schema_version": self.context_schema_version,
            "max_context_characters": self.max_context_characters,
            "max_evidence_count": self.max_evidence_count,
        }

    def to_audit_dict(self) -> dict[str, object]:
        return {**self._identity_payload(), "context_build_config_hash": self.context_build_config_hash}


@dataclass(frozen=True, slots=True, kw_only=True)
class ContextBuildTrace:
    """Content-free decision trace for a single deterministic construction attempt."""

    trace_schema_version: str
    trace_id: str
    trace_hash: str
    request_id: str
    query_id: str
    corpus_snapshot_id: str
    context_build_config_hash: str
    input_evidence_count: int
    deduplicated_evidence_count: int
    count_selected_count: int
    resolved_count: int
    included_count: int
    stable_candidate_uids: tuple[str, ...]
    count_selected_uids: tuple[str, ...]
    max_count_excluded_uids: tuple[str, ...]
    resolved_uids: tuple[str, ...]
    included_uids: tuple[str, ...]
    budget_excluded_uids: tuple[str, ...]
    instruction_budget_not_attempted_uids: tuple[str, ...]
    not_attempted_after_budget_cutoff_uids: tuple[str, ...]
    decision_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        try:
            require_public_identifier(self.trace_schema_version, "trace_schema_version")
            require_public_identifier(self.request_id, "request_id")
            require_public_query_id(self.query_id)
            if self.corpus_snapshot_id:
                require_public_identifier(self.corpus_snapshot_id, "corpus_snapshot_id")
            require_sha256(self.context_build_config_hash, "context_build_config_hash")
            require_sha256(self.trace_hash, "trace_hash")
        except ValueError as error:
            raise _invalid_package() from error
        for name in (
            "input_evidence_count",
            "deduplicated_evidence_count",
            "count_selected_count",
            "resolved_count",
            "included_count",
        ):
            _require_nonnegative_json_int(getattr(self, name))
        for name in (
            "stable_candidate_uids",
            "count_selected_uids",
            "max_count_excluded_uids",
            "resolved_uids",
            "included_uids",
            "budget_excluded_uids",
            "instruction_budget_not_attempted_uids",
            "not_attempted_after_budget_cutoff_uids",
        ):
            object.__setattr__(self, name, _tuple_of_uids(getattr(self, name)))
        if isinstance(self.decision_codes, (str, bytes)) or not isinstance(self.decision_codes, Sequence):
            raise _invalid_package()
        decisions = tuple(self.decision_codes)
        if len(decisions) != len(self.stable_candidate_uids) or any(
            item not in _DECISION_CODES for item in decisions
        ):
            raise _invalid_package()
        object.__setattr__(self, "decision_codes", decisions)
        self._validate_partition()
        expected_hash = canonical_json_sha256(self._semantic_payload())
        if self.trace_hash != expected_hash or self.trace_id != "CT-" + expected_hash:
            raise _invalid_package()

    def _validate_partition(self) -> None:
        stable = self.stable_candidate_uids
        if len(stable) != len(set(stable)):
            raise _invalid_package()
        if self.input_evidence_count < self.deduplicated_evidence_count or self.deduplicated_evidence_count != len(stable):
            raise _invalid_package()
        if self.count_selected_count != len(self.count_selected_uids):
            raise _invalid_package()
        if self.included_count != len(self.included_uids) or self.resolved_count != len(self.resolved_uids):
            raise _invalid_package()
        if self.count_selected_uids + self.max_count_excluded_uids != stable:
            raise _invalid_package()
        if self.max_count_excluded_uids != stable[self.count_selected_count :]:
            raise _invalid_package()
        subsets = (
            self.count_selected_uids,
            self.max_count_excluded_uids,
            self.resolved_uids,
            self.included_uids,
            self.budget_excluded_uids,
            self.instruction_budget_not_attempted_uids,
            self.not_attempted_after_budget_cutoff_uids,
        )
        if any(not _unique_ordered_subset(item, stable) for item in subsets):
            raise _invalid_package()
        category_sets = (
            set(self.included_uids),
            set(self.max_count_excluded_uids),
            set(self.budget_excluded_uids),
            set(self.instruction_budget_not_attempted_uids),
            set(self.not_attempted_after_budget_cutoff_uids),
        )
        if sum(len(item) for item in category_sets) != len(stable) or set().union(*category_sets) != set(stable):
            raise _invalid_package()
        expected_by_code = {
            "INCLUDED": set(self.included_uids),
            "MAX_EVIDENCE_COUNT_EXCLUDED": set(self.max_count_excluded_uids),
            "BUDGET_EXCLUDED": set(self.budget_excluded_uids),
            "NOT_ATTEMPTED_INSTRUCTION_BUDGET_EXHAUSTED": set(self.instruction_budget_not_attempted_uids),
            "NOT_ATTEMPTED_AFTER_BUDGET_CUTOFF": set(self.not_attempted_after_budget_cutoff_uids),
        }
        if any(expected_by_code[code] != {uid for uid, candidate_code in zip(stable, self.decision_codes) if candidate_code == code} for code in _DECISION_CODES):
            raise _invalid_package()
        if set(self.resolved_uids) != set(self.included_uids) | set(self.budget_excluded_uids):
            raise _invalid_package()
        if self.resolved_uids != self.included_uids + self.budget_excluded_uids:
            raise _invalid_package()
        if self.included_uids != self.count_selected_uids[: self.included_count]:
            raise _invalid_package()
        if len(self.budget_excluded_uids) > 1:
            raise _invalid_package()
        if not stable:
            if (
                self.input_evidence_count != 0
                or self.count_selected_count != 0
                or self.resolved_count != 0
                or self.included_count != 0
                or self.corpus_snapshot_id != ""
                or any(
                    (
                        self.count_selected_uids,
                        self.max_count_excluded_uids,
                        self.resolved_uids,
                        self.included_uids,
                        self.budget_excluded_uids,
                        self.instruction_budget_not_attempted_uids,
                        self.not_attempted_after_budget_cutoff_uids,
                        self.decision_codes,
                    )
                )
            ):
                raise _invalid_package()
            return
        if self.corpus_snapshot_id == "":
            raise _invalid_package()
        if self.instruction_budget_not_attempted_uids:
            if (
                self.included_uids
                or self.resolved_uids
                or self.budget_excluded_uids
                or self.not_attempted_after_budget_cutoff_uids
                or self.instruction_budget_not_attempted_uids
                != self.count_selected_uids
            ):
                raise _invalid_package()
            return
        if not self.budget_excluded_uids:
            if (
                self.included_uids != self.count_selected_uids
                or self.resolved_uids != self.count_selected_uids
                or self.not_attempted_after_budget_cutoff_uids
            ):
                raise _invalid_package()
            return
        expected_budget = self.count_selected_uids[self.included_count : self.included_count + 1]
        expected_cutoff = self.count_selected_uids[self.included_count + 1 :]
        if (
            self.included_uids == self.count_selected_uids
            or self.budget_excluded_uids != expected_budget
            or self.not_attempted_after_budget_cutoff_uids != expected_cutoff
        ):
            raise _invalid_package()

    @classmethod
    def create(cls, **values: object) -> "ContextBuildTrace":
        normalized = dict(values)
        for name in (
            "stable_candidate_uids",
            "count_selected_uids",
            "max_count_excluded_uids",
            "resolved_uids",
            "included_uids",
            "budget_excluded_uids",
            "instruction_budget_not_attempted_uids",
            "not_attempted_after_budget_cutoff_uids",
            "decision_codes",
        ):
            value = normalized[name]
            if isinstance(value, (str, bytes)) or not isinstance(value, Iterable):
                raise _invalid_package()
            normalized[name] = tuple(value)
        payload = _canonical_trace_payload(**normalized)  # type: ignore[arg-type]
        trace_hash = canonical_json_sha256(payload)
        return cls(trace_id="CT-" + trace_hash, trace_hash=trace_hash, **normalized)  # type: ignore[arg-type]

    def _semantic_payload(self) -> dict[str, object]:
        return _canonical_trace_payload(
            trace_schema_version=self.trace_schema_version,
            request_id=self.request_id,
            query_id=self.query_id,
            corpus_snapshot_id=self.corpus_snapshot_id,
            context_build_config_hash=self.context_build_config_hash,
            input_evidence_count=self.input_evidence_count,
            deduplicated_evidence_count=self.deduplicated_evidence_count,
            count_selected_count=self.count_selected_count,
            resolved_count=self.resolved_count,
            included_count=self.included_count,
            stable_candidate_uids=self.stable_candidate_uids,
            count_selected_uids=self.count_selected_uids,
            max_count_excluded_uids=self.max_count_excluded_uids,
            resolved_uids=self.resolved_uids,
            included_uids=self.included_uids,
            budget_excluded_uids=self.budget_excluded_uids,
            instruction_budget_not_attempted_uids=self.instruction_budget_not_attempted_uids,
            not_attempted_after_budget_cutoff_uids=self.not_attempted_after_budget_cutoff_uids,
            decision_codes=self.decision_codes,
        )

    def to_audit_dict(self) -> dict[str, object]:
        return {
            "trace_schema_version": self.trace_schema_version,
            "trace_id": self.trace_id,
            "trace_hash": self.trace_hash,
            "request_id": self.request_id,
            "query_id": self.query_id,
            "corpus_snapshot_id": self.corpus_snapshot_id,
            "context_build_config_hash": self.context_build_config_hash,
            "input_evidence_count": self.input_evidence_count,
            "deduplicated_evidence_count": self.deduplicated_evidence_count,
            "count_selected_count": self.count_selected_count,
            "resolved_count": self.resolved_count,
            "included_count": self.included_count,
            "stable_candidate_uids": list(self.stable_candidate_uids),
            "count_selected_uids": list(self.count_selected_uids),
            "max_count_excluded_uids": list(self.max_count_excluded_uids),
            "resolved_uids": list(self.resolved_uids),
            "included_uids": list(self.included_uids),
            "budget_excluded_uids": list(self.budget_excluded_uids),
            "instruction_budget_not_attempted_uids": list(self.instruction_budget_not_attempted_uids),
            "not_attempted_after_budget_cutoff_uids": list(self.not_attempted_after_budget_cutoff_uids),
            "decision_codes": list(self.decision_codes),
        }


@dataclass(frozen=True, slots=True, kw_only=True)
class RetrievedContextPackage:
    """Sensitive rendered context plus content-free deterministic construction trace."""

    package_id: str
    request_id: str
    query_id: str
    citation_mode: CitationMode
    evidence_envelopes: tuple[EvidenceEnvelope, ...]
    citation_bindings: tuple[CitationBinding, ...]
    rendered_context: str = field(repr=False)
    rendered_context_hash: str
    evidence_count: int
    abstention_required: bool
    abstention_reason_codes: tuple[str, ...]
    context_schema_version: str
    context_build_config_hash: str
    max_evidence_count: int
    max_context_characters: int
    build_trace: ContextBuildTrace

    def __post_init__(self) -> None:
        try:
            require_public_identifier(self.package_id, "package_id")
            require_public_identifier(self.request_id, "request_id")
            require_public_query_id(self.query_id)
            require_sha256(self.rendered_context_hash, "rendered_context_hash")
            require_public_identifier(self.context_schema_version, "context_schema_version")
            require_sha256(self.context_build_config_hash, "context_build_config_hash")
        except ValueError as error:
            raise _invalid_package() from error
        if not isinstance(self.citation_mode, CitationMode) or not isinstance(self.rendered_context, str):
            raise _invalid_package()
        if type(self.abstention_required) is not bool:
            raise _invalid_package()
        _require_positive_json_int(self.max_evidence_count)
        _require_positive_json_int(self.max_context_characters)
        envelopes = tuple(self.evidence_envelopes)
        bindings = tuple(self.citation_bindings)
        reasons = tuple(self.abstention_reason_codes)
        if not all(isinstance(item, EvidenceEnvelope) for item in envelopes) or not all(isinstance(item, CitationBinding) for item in bindings):
            raise _invalid_package()
        if not isinstance(self.build_trace, ContextBuildTrace) or type(self.evidence_count) is not int:
            raise _invalid_package()
        if self.evidence_count != len(envelopes) or len(envelopes) != len(bindings):
            raise _invalid_package()
        if hashlib.sha256(self.rendered_context.encode("utf-8")).hexdigest() != self.rendered_context_hash:
            raise _invalid_package()
        if any(reason not in _ABSTENTION_REASONS for reason in reasons):
            raise _invalid_package()
        object.__setattr__(self, "evidence_envelopes", envelopes)
        object.__setattr__(self, "citation_bindings", bindings)
        object.__setattr__(self, "abstention_reason_codes", reasons)
        self._validate_identity()

    def _validate_identity(self) -> None:
        try:
            expected_config_hash = ContextBuildConfig(
                context_schema_version=self.context_schema_version,
                max_evidence_count=self.max_evidence_count,
                max_context_characters=self.max_context_characters,
            ).context_build_config_hash
        except ContextBuildConfigurationError as error:
            raise _invalid_package() from error
        if (
            expected_config_hash != self.context_build_config_hash
            or self.build_trace.request_id != self.request_id
            or self.build_trace.query_id != self.query_id
            or self.build_trace.context_build_config_hash != self.context_build_config_hash
        ):
            raise _invalid_package()
        envelope_uids = tuple(item.evidence_uid for item in self.evidence_envelopes)
        if self.build_trace.included_uids != envelope_uids:
            raise _invalid_package()
        for index, (envelope, binding) in enumerate(zip(self.evidence_envelopes, self.citation_bindings), start=1):
            if binding.citation_id != f"E{index}" or any(
                getattr(binding, field) != getattr(envelope, field)
                for field in ("evidence_uid", "chunk_id", "parent_doc_id", "content_hash", "source_id", "version", "rank")
            ):
                raise _invalid_package()
        if self.abstention_required:
            if len(self.abstention_reason_codes) != 1 or self.evidence_envelopes or self.citation_bindings or self.evidence_count != 0 or self.rendered_context != "":
                raise _invalid_package()
            self._validate_abstention_reason()
        elif self.abstention_reason_codes or not self.evidence_envelopes:
            raise _invalid_package()
        elif self.build_trace.included_count == 0 or self.build_trace.instruction_budget_not_attempted_uids:
            raise _invalid_package()
        expected_id = "PK-" + canonical_json_sha256(self._identity_payload())
        if self.package_id != expected_id:
            raise _invalid_package()

    def _validate_abstention_reason(self) -> None:
        trace = self.build_trace
        reason = self.abstention_reason_codes[0]
        if reason == "EMPTY_RETRIEVAL":
            if trace.stable_candidate_uids or trace.input_evidence_count != 0:
                raise _invalid_package()
            return
        if reason == "CONTEXT_BUDGET_EXHAUSTED":
            if (
                not trace.count_selected_uids
                or trace.resolved_count != 0
                or trace.included_count != 0
                or trace.instruction_budget_not_attempted_uids != trace.count_selected_uids
                or trace.budget_excluded_uids
                or trace.not_attempted_after_budget_cutoff_uids
            ):
                raise _invalid_package()
            return
        if reason == "NO_COMPLETE_EVIDENCE_BLOCK_FITS":
            if (
                trace.included_count != 0
                or len(trace.budget_excluded_uids) != 1
                or trace.budget_excluded_uids != trace.count_selected_uids[:1]
                or trace.not_attempted_after_budget_cutoff_uids
                != trace.count_selected_uids[1:]
                or trace.instruction_budget_not_attempted_uids
            ):
                raise _invalid_package()
            return
        raise _invalid_package()

    @classmethod
    def create(
        cls,
        *,
        request_id: str,
        query_id: str,
        citation_mode: CitationMode,
        evidence_envelopes: Sequence[EvidenceEnvelope],
        citation_bindings: Sequence[CitationBinding],
        rendered_context: str,
        abstention_required: bool,
        abstention_reason_codes: Sequence[str],
        context_schema_version: str,
        context_build_config_hash: str,
        max_evidence_count: int,
        max_context_characters: int,
        build_trace: ContextBuildTrace,
    ) -> "RetrievedContextPackage":
        envelopes = tuple(evidence_envelopes)
        bindings = tuple(citation_bindings)
        reasons = tuple(abstention_reason_codes)
        rendered_hash = hashlib.sha256(rendered_context.encode("utf-8")).hexdigest()
        payload = cls._identity_payload_from(
            context_schema_version=context_schema_version,
            request_id=request_id,
            query_id=query_id,
            citation_mode=citation_mode,
            rendered_context_hash=rendered_hash,
            evidence_uids=tuple(item.evidence_uid for item in envelopes),
            context_build_config_hash=context_build_config_hash,
            context_build_trace_hash=build_trace.trace_hash,
        )
        return cls(
            package_id="PK-" + canonical_json_sha256(payload),
            request_id=request_id,
            query_id=query_id,
            citation_mode=citation_mode,
            evidence_envelopes=envelopes,
            citation_bindings=bindings,
            rendered_context=rendered_context,
            rendered_context_hash=rendered_hash,
            evidence_count=len(envelopes),
            abstention_required=abstention_required,
            abstention_reason_codes=reasons,
            context_schema_version=context_schema_version,
            context_build_config_hash=context_build_config_hash,
            max_evidence_count=max_evidence_count,
            max_context_characters=max_context_characters,
            build_trace=build_trace,
        )

    @staticmethod
    def _identity_payload_from(
        *,
        context_schema_version: str,
        request_id: str,
        query_id: str,
        citation_mode: CitationMode,
        rendered_context_hash: str,
        evidence_uids: Sequence[str],
        context_build_config_hash: str,
        context_build_trace_hash: str,
    ) -> dict[str, object]:
        return {
            "citation_mode": citation_mode.value,
            "context_build_config_hash": context_build_config_hash,
            "context_build_trace_hash": context_build_trace_hash,
            "context_schema_version": context_schema_version,
            "evidence_uids": list(evidence_uids),
            "query_id": query_id,
            "rendered_context_hash": rendered_context_hash,
            "request_id": request_id,
        }

    def _identity_payload(self) -> dict[str, object]:
        return self._identity_payload_from(
            context_schema_version=self.context_schema_version,
            request_id=self.request_id,
            query_id=self.query_id,
            citation_mode=self.citation_mode,
            rendered_context_hash=self.rendered_context_hash,
            evidence_uids=tuple(item.evidence_uid for item in self.evidence_envelopes),
            context_build_config_hash=self.context_build_config_hash,
            context_build_trace_hash=self.build_trace.trace_hash,
        )

    def to_audit_dict(self) -> dict[str, object]:
        """Return a content-free audit form; ``asdict`` remains sensitive by design."""

        return {
            "package_id": self.package_id,
            "request_id": self.request_id,
            "query_id": self.query_id,
            "citation_mode": self.citation_mode.value,
            "evidence_uids": [item.evidence_uid for item in self.evidence_envelopes],
            "citation_ids": [item.citation_id for item in self.citation_bindings],
            "rendered_context_hash": self.rendered_context_hash,
            "rendered_context_length": len(self.rendered_context),
            "evidence_count": self.evidence_count,
            "abstention_required": self.abstention_required,
            "abstention_reason_codes": list(self.abstention_reason_codes),
            "context_schema_version": self.context_schema_version,
            "context_build_config_hash": self.context_build_config_hash,
            "max_evidence_count": self.max_evidence_count,
            "max_context_characters": self.max_context_characters,
            "context_build_trace_hash": self.build_trace.trace_hash,
        }
