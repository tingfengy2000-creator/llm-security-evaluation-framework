from __future__ import annotations

import pytest

from llmguard.domains.retrieval.context.citation import render_citation_instruction
from llmguard.domains.retrieval.contracts import CitationInputError, CitationMode


@pytest.mark.parametrize(
    ("mode", "expected"),
    [
        (CitationMode.OFF, "Use the evidence below to answer the user.\n"),
        (CitationMode.AVAILABLE, "Use the evidence below to answer the user. You may cite supporting evidence with [E#].\n"),
        (CitationMode.REQUIRED, "Use the evidence below to answer the user. Cite every factual claim with [E#]. If the evidence does not support a claim, say that the evidence is insufficient; do not invent a citation.\n"),
    ],
)
def test_citation_instruction_is_exact_and_has_one_lf(mode: CitationMode, expected: str) -> None:
    assert render_citation_instruction(mode=mode) == expected
    assert expected.count("\n") == 1


def test_citation_instruction_rejects_raw_string_mode() -> None:
    with pytest.raises(CitationInputError) as caught:
        render_citation_instruction(mode="required")  # type: ignore[arg-type]
    assert caught.value.error_code == "INVALID_CITATION_MODE"
