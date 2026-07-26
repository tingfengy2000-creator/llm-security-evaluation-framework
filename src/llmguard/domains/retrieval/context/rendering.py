"""Deterministic structural rendering for exactly one bound evidence envelope."""

from __future__ import annotations

import math

from llmguard.domains.retrieval.contracts import (
    CitationBinding,
    CitationIntegrityError,
    ContextRenderingError,
    EvidenceEnvelope,
)


def _require_text(value: object) -> str:
    if not isinstance(value, str):
        raise ContextRenderingError("context rendering failed")
    return value


def escape_xml_text(value: str) -> str:
    """Escape raw text once without interpreting existing entities as safe."""

    text = _require_text(value)
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def escape_xml_attribute(value: str) -> str:
    """Escape raw XML attribute text once, including both quote kinds."""

    text = _require_text(value)
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def _format_metric(value: object) -> str:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ContextRenderingError("context rendering failed")
    number = float(value)
    if not math.isfinite(number):
        raise ContextRenderingError("context rendering failed")
    if number == 0.0:
        number = 0.0
    return format(number, ".17g")


def _verify_binding(*, envelope: EvidenceEnvelope, binding: CitationBinding) -> None:
    if not isinstance(envelope, EvidenceEnvelope) or not isinstance(binding, CitationBinding):
        raise ContextRenderingError("context rendering failed")
    fields = (
        "evidence_uid",
        "chunk_id",
        "parent_doc_id",
        "content_hash",
        "source_id",
        "version",
        "rank",
    )
    if any(getattr(binding, name) != getattr(envelope, name) for name in fields):
        raise CitationIntegrityError("citation binding does not match evidence")


def render_evidence_block(*, envelope: EvidenceEnvelope, binding: CitationBinding) -> str:
    """Render exactly one fully bound evidence block or fail closed."""

    _verify_binding(envelope=envelope, binding=binding)
    try:
        attributes = (
            ("citation_id", binding.citation_id),
            ("evidence_uid", envelope.evidence_uid),
            ("doc_id", envelope.doc_id),
            ("chunk_id", envelope.chunk_id),
            ("parent_doc_id", envelope.parent_doc_id),
            ("source_id", envelope.source_id),
            ("source_type", envelope.source_type),
            ("version", envelope.version),
            ("timestamp", envelope.timestamp),
            ("content_hash", envelope.content_hash),
            ("rank", str(envelope.rank)),
            ("distance", _format_metric(envelope.distance)),
            ("similarity", _format_metric(envelope.similarity)),
        )
        rendered_attributes = " ".join(
            f'{name}="{escape_xml_attribute(value)}"' for name, value in attributes
        )
        rendered_content = escape_xml_text(
            envelope.content.replace("\r\n", "\n").replace("\r", "\n")
        )
        separator = "" if rendered_content.endswith("\n") else "\n"
        return (
            f"<EVIDENCE {rendered_attributes}>\n<CONTENT>\n"
            f"{rendered_content}{separator}</CONTENT>\n</EVIDENCE>\n"
        )
    except (CitationIntegrityError, ContextRenderingError):
        raise
    except Exception as error:
        raise ContextRenderingError("context rendering failed") from error
