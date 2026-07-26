"""Deterministic citation instruction generation without model invocation."""

from __future__ import annotations

from llmguard.domains.retrieval.contracts import CitationInputError, CitationMode

_INSTRUCTIONS = {
    CitationMode.OFF: "Use the evidence below to answer the user.\n",
    CitationMode.AVAILABLE: (
        "Use the evidence below to answer the user. You may cite supporting evidence "
        "with [E#].\n"
    ),
    CitationMode.REQUIRED: (
        "Use the evidence below to answer the user. Cite every factual claim with [E#]. "
        "If the evidence does not support a claim, say that the evidence is insufficient; "
        "do not invent a citation.\n"
    ),
}


def render_citation_instruction(*, mode: CitationMode) -> str:
    """Return the frozen LF-terminated instruction for a closed citation mode."""

    if not isinstance(mode, CitationMode):
        raise CitationInputError("citation mode is invalid", error_code="INVALID_CITATION_MODE")
    return _INSTRUCTIONS[mode]
