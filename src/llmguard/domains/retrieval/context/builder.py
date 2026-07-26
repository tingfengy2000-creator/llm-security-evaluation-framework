"""The single deterministic, synthetic-testable ContextBuilder implementation."""

from __future__ import annotations

from collections.abc import Sequence

from llmguard.domains.retrieval.contracts import (
    CitationInputError,
    CitationIntegrityError,
    CitationBinding,
    CitationMode,
    ContentRef,
    ContentResolutionIntegrityError,
    ContentResolutionLookupError,
    ContentResolutionRuntimeError,
    ContextBuildConfig,
    ContextBuildTrace,
    ContextConstructionError,
    ContextConstructionInputError,
    ContextConstructionIntegrityError,
    ContextConstructionRuntimeError,
    ContextRenderingError,
    EvidenceEnvelope,
    EvidenceEnvelopeInputError,
    EvidenceEnvelopeIntegrityError,
    EvidenceEnvelopeRuntimeError,
    RetrievedContextPackage,
    RetrievalContractError,
    RetrievalInputError,
    RetrievalIntegrityError,
    RetrievalEvidence,
    RetrievalRequest,
)

from .budget import fits_context_budget
from .citation import render_citation_instruction
from .protocols import ContentResolver, ContextBuilder, EvidenceEnvelopeFactory
from .rendering import render_evidence_block


class DeterministicContextBuilder(ContextBuilder):
    """Construct context packages through the frozen sequential-resolution protocol."""

    _TRACE_SCHEMA_VERSION = "1.0"

    def __init__(
        self,
        *,
        resolver: ContentResolver,
        envelope_factory: EvidenceEnvelopeFactory,
    ) -> None:
        self._resolver = resolver
        self._envelope_factory = envelope_factory

    def build(
        self,
        *,
        request: RetrievalRequest,
        evidence: Sequence[RetrievalEvidence],
        citation_mode: CitationMode,
        config: ContextBuildConfig,
    ) -> RetrievedContextPackage:
        try:
            return self._build(
                request=request,
                evidence=evidence,
                citation_mode=citation_mode,
                config=config,
            )
        except ContextConstructionError:
            raise
        except RetrievalContractError as error:
            raise self._redact_dependency_error(error) from error
        except Exception as error:
            raise ContextConstructionRuntimeError(
                "context construction failed"
            ) from error

    @staticmethod
    def _redact_dependency_error(error: RetrievalContractError) -> RetrievalContractError:
        """Keep legal error type/code while discarding injected dependency text."""

        code = getattr(error, "error_code", None)
        if isinstance(error, ContentResolutionLookupError):
            return ContentResolutionLookupError("context content lookup failed", error_code=code)
        if isinstance(error, ContentResolutionIntegrityError):
            return ContentResolutionIntegrityError("context content integrity check failed", error_code=code)
        if isinstance(error, ContentResolutionRuntimeError):
            return ContentResolutionRuntimeError("context content resolution failed", error_code=code)
        if isinstance(error, EvidenceEnvelopeInputError):
            return EvidenceEnvelopeInputError("evidence envelope is invalid", error_code=code)
        if isinstance(error, EvidenceEnvelopeIntegrityError):
            return EvidenceEnvelopeIntegrityError("evidence envelope integrity check failed", error_code=code)
        if isinstance(error, EvidenceEnvelopeRuntimeError):
            return EvidenceEnvelopeRuntimeError("evidence envelope construction failed", error_code=code)
        if isinstance(error, CitationInputError):
            return CitationInputError("citation binding is invalid", error_code=code)
        if isinstance(error, CitationIntegrityError):
            return CitationIntegrityError("citation binding does not match evidence", error_code=code)
        if isinstance(error, ContextRenderingError):
            return ContextRenderingError("context rendering failed", error_code=code)
        if isinstance(error, RetrievalInputError):
            return RetrievalInputError("context construction input is invalid", error_code=code)
        if isinstance(error, RetrievalIntegrityError):
            return RetrievalIntegrityError("context construction integrity check failed", error_code=code)
        return ContextConstructionRuntimeError("context construction failed")

    def _build(
        self,
        *,
        request: RetrievalRequest,
        evidence: Sequence[RetrievalEvidence],
        citation_mode: CitationMode,
        config: ContextBuildConfig,
    ) -> RetrievedContextPackage:
        self._validate_inputs(
            request=request,
            evidence=evidence,
            citation_mode=citation_mode,
            config=config,
        )
        source = tuple(evidence)
        self._validate_provenance(request=request, evidence=source)
        stable = self._deduplicate_stable(source)
        count_selected = stable[: config.max_evidence_count]
        max_count_excluded = stable[config.max_evidence_count :]
        instruction = render_citation_instruction(mode=citation_mode)

        if not stable:
            return self._abstention(
                request=request,
                citation_mode=citation_mode,
                config=config,
                corpus_snapshot_id="",
                input_evidence_count=0,
                stable=(),
                count_selected=(),
                max_count_excluded=(),
                reason="EMPTY_RETRIEVAL",
                instruction_not_attempted=(),
                budget_excluded=(),
                cutoff_not_attempted=(),
                resolved=(),
            )
        snapshot_id = stable[0].corpus_snapshot_id
        if not fits_context_budget(
            rendered_context=instruction,
            max_context_characters=config.max_context_characters,
        ):
            return self._abstention(
                request=request,
                citation_mode=citation_mode,
                config=config,
                corpus_snapshot_id=snapshot_id,
                input_evidence_count=len(source),
                stable=stable,
                count_selected=count_selected,
                max_count_excluded=max_count_excluded,
                reason="CONTEXT_BUDGET_EXHAUSTED",
                instruction_not_attempted=count_selected,
                budget_excluded=(),
                cutoff_not_attempted=(),
                resolved=(),
            )

        included_envelopes: list[EvidenceEnvelope] = []
        included_bindings: list[CitationBinding] = []
        rendered_blocks: list[str] = []
        resolved: list[RetrievalEvidence] = []
        budget_excluded: tuple[RetrievalEvidence, ...] = ()
        cutoff_not_attempted: tuple[RetrievalEvidence, ...] = ()
        for index, candidate in enumerate(count_selected):
            resolved_content = self._resolver.resolve(
                content_ref=ContentRef(candidate.content_ref),
                expected_content_hash=candidate.content_hash,
            )
            envelope = self._envelope_factory.create(
                evidence=candidate,
                resolved_content=resolved_content,
            )
            temporary_binding = CitationBinding(
                citation_id=f"E{len(included_bindings) + 1}",
                evidence_uid=envelope.evidence_uid,
                chunk_id=envelope.chunk_id,
                parent_doc_id=envelope.parent_doc_id,
                content_hash=envelope.content_hash,
                source_id=envelope.source_id,
                version=envelope.version,
                rank=envelope.rank,
            )
            block = render_evidence_block(
                envelope=envelope,
                binding=temporary_binding,
            )
            resolved.append(candidate)
            candidate_context = instruction + "".join(rendered_blocks) + block
            if fits_context_budget(
                rendered_context=candidate_context,
                max_context_characters=config.max_context_characters,
            ):
                included_envelopes.append(envelope)
                included_bindings.append(temporary_binding)
                rendered_blocks.append(block)
                continue
            budget_excluded = (candidate,)
            cutoff_not_attempted = count_selected[index + 1 :]
            break

        if not included_envelopes:
            return self._abstention(
                request=request,
                citation_mode=citation_mode,
                config=config,
                corpus_snapshot_id=snapshot_id,
                input_evidence_count=len(source),
                stable=stable,
                count_selected=count_selected,
                max_count_excluded=max_count_excluded,
                reason="NO_COMPLETE_EVIDENCE_BLOCK_FITS",
                instruction_not_attempted=(),
                budget_excluded=budget_excluded,
                cutoff_not_attempted=cutoff_not_attempted,
                resolved=tuple(resolved),
            )

        trace = self._trace(
            request=request,
            config=config,
            corpus_snapshot_id=snapshot_id,
            input_evidence_count=len(source),
            stable=stable,
            count_selected=count_selected,
            max_count_excluded=max_count_excluded,
            resolved=tuple(resolved),
            included=tuple(item.evidence_uid for item in included_envelopes),
            budget_excluded=budget_excluded,
            instruction_not_attempted=(),
            cutoff_not_attempted=cutoff_not_attempted,
        )
        return RetrievedContextPackage.create(
            request_id=request.request_id,
            query_id=request.query_id,
            citation_mode=citation_mode,
            evidence_envelopes=tuple(included_envelopes),
            citation_bindings=tuple(included_bindings),
            rendered_context=instruction + "".join(rendered_blocks),
            abstention_required=False,
            abstention_reason_codes=(),
            context_schema_version=config.context_schema_version,
            context_build_config_hash=config.context_build_config_hash,
            max_evidence_count=config.max_evidence_count,
            max_context_characters=config.max_context_characters,
            build_trace=trace,
        )

    @staticmethod
    def _validate_inputs(
        *,
        request: object,
        evidence: object,
        citation_mode: object,
        config: object,
    ) -> None:
        if (
            not isinstance(request, RetrievalRequest)
            or isinstance(evidence, (str, bytes))
            or not isinstance(evidence, Sequence)
            or not all(isinstance(item, RetrievalEvidence) for item in evidence)
            or not isinstance(citation_mode, CitationMode)
            or not isinstance(config, ContextBuildConfig)
        ):
            raise ContextConstructionInputError("context construction input is invalid")

    @staticmethod
    def _validate_provenance(
        *, request: RetrievalRequest,
        evidence: tuple[RetrievalEvidence, ...],
    ) -> None:
        snapshots = {item.corpus_snapshot_id for item in evidence}
        if len(snapshots) > 1 or any(
            item.query_id != request.query_id
            or item.retrieval_request_id != request.request_id
            or item.collection_fingerprint != request.collection_fingerprint
            or not 1 <= item.rank <= request.top_k
            for item in evidence
        ):
            raise ContextConstructionIntegrityError("request and evidence do not match", error_code="REQUEST_EVIDENCE_MISMATCH")

    @staticmethod
    def _semantic_projection(item: RetrievalEvidence) -> tuple[object, ...]:
        return (
            item.evidence_schema_version,
            item.evidence_uid,
            item.query_id,
            item.retrieval_request_id,
            item.corpus_snapshot_id,
            item.doc_id,
            item.chunk_id,
            item.parent_doc_id,
            str(item.content_ref),
            item.content_hash,
            item.source_id,
            item.source_type,
            item.version,
            item.timestamp,
            item.rank,
            item.distance,
            item.similarity,
            item.collection_fingerprint,
            tuple(sorted(item.public_metadata.items())),
        )

    @classmethod
    def _deduplicate_stable(
        cls, evidence: tuple[RetrievalEvidence, ...]
    ) -> tuple[RetrievalEvidence, ...]:
        stable = tuple(sorted(evidence, key=lambda item: (item.rank, item.evidence_uid)))
        seen: dict[str, RetrievalEvidence] = {}
        result: list[RetrievalEvidence] = []
        for item in stable:
            existing = seen.get(item.evidence_uid)
            if existing is None:
                seen[item.evidence_uid] = item
                result.append(item)
            elif cls._semantic_projection(existing) != cls._semantic_projection(item):
                raise ContextConstructionIntegrityError(
                    "duplicate evidence conflict", error_code="DUPLICATE_EVIDENCE_CONFLICT"
                )
        return tuple(result)

    def _abstention(
        self,
        *,
        request: RetrievalRequest,
        citation_mode: CitationMode,
        config: ContextBuildConfig,
        corpus_snapshot_id: str,
        input_evidence_count: int,
        stable: tuple[RetrievalEvidence, ...],
        count_selected: tuple[RetrievalEvidence, ...],
        max_count_excluded: tuple[RetrievalEvidence, ...],
        reason: str,
        instruction_not_attempted: tuple[RetrievalEvidence, ...],
        budget_excluded: tuple[RetrievalEvidence, ...],
        cutoff_not_attempted: tuple[RetrievalEvidence, ...],
        resolved: tuple[RetrievalEvidence, ...],
    ) -> RetrievedContextPackage:
        trace = self._trace(
            request=request,
            config=config,
            corpus_snapshot_id=corpus_snapshot_id,
            input_evidence_count=input_evidence_count,
            stable=stable,
            count_selected=count_selected,
            max_count_excluded=max_count_excluded,
            resolved=resolved,
            included=(),
            budget_excluded=budget_excluded,
            instruction_not_attempted=instruction_not_attempted,
            cutoff_not_attempted=cutoff_not_attempted,
        )
        return RetrievedContextPackage.create(
            request_id=request.request_id,
            query_id=request.query_id,
            citation_mode=citation_mode,
            evidence_envelopes=(),
            citation_bindings=(),
            rendered_context="",
            abstention_required=True,
            abstention_reason_codes=(reason,),
            context_schema_version=config.context_schema_version,
            context_build_config_hash=config.context_build_config_hash,
            max_evidence_count=config.max_evidence_count,
            max_context_characters=config.max_context_characters,
            build_trace=trace,
        )

    def _trace(
        self,
        *,
        request: RetrievalRequest,
        config: ContextBuildConfig,
        corpus_snapshot_id: str,
        input_evidence_count: int,
        stable: tuple[RetrievalEvidence, ...],
        count_selected: tuple[RetrievalEvidence, ...],
        max_count_excluded: tuple[RetrievalEvidence, ...],
        resolved: tuple[RetrievalEvidence, ...],
        included: tuple[str, ...],
        budget_excluded: tuple[RetrievalEvidence, ...],
        instruction_not_attempted: tuple[RetrievalEvidence, ...],
        cutoff_not_attempted: tuple[RetrievalEvidence, ...],
    ) -> ContextBuildTrace:
        def uid(items: tuple[RetrievalEvidence, ...]) -> tuple[str, ...]:
            return tuple(item.evidence_uid for item in items)
        stable_uids = uid(stable)
        included_uids = tuple(included)
        max_uids = uid(max_count_excluded)
        budget_uids = uid(budget_excluded)
        instruction_uids = uid(instruction_not_attempted)
        cutoff_uids = uid(cutoff_not_attempted)
        categories = {
            "INCLUDED": set(included_uids),
            "MAX_EVIDENCE_COUNT_EXCLUDED": set(max_uids),
            "BUDGET_EXCLUDED": set(budget_uids),
            "NOT_ATTEMPTED_INSTRUCTION_BUDGET_EXHAUSTED": set(instruction_uids),
            "NOT_ATTEMPTED_AFTER_BUDGET_CUTOFF": set(cutoff_uids),
        }
        decisions = tuple(
            next(code for code, uids in categories.items() if item_uid in uids)
            for item_uid in stable_uids
        )
        return ContextBuildTrace.create(
            trace_schema_version=self._TRACE_SCHEMA_VERSION,
            request_id=request.request_id,
            query_id=request.query_id,
            corpus_snapshot_id=corpus_snapshot_id,
            context_build_config_hash=config.context_build_config_hash,
            input_evidence_count=input_evidence_count,
            deduplicated_evidence_count=len(stable),
            count_selected_count=len(count_selected),
            resolved_count=len(resolved),
            included_count=len(included_uids),
            stable_candidate_uids=stable_uids,
            count_selected_uids=uid(count_selected),
            max_count_excluded_uids=max_uids,
            resolved_uids=uid(resolved),
            included_uids=included_uids,
            budget_excluded_uids=budget_uids,
            instruction_budget_not_attempted_uids=instruction_uids,
            not_attempted_after_budget_cutoff_uids=cutoff_uids,
            decision_codes=decisions,
        )
