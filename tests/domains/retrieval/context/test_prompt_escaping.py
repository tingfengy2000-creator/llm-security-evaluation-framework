from __future__ import annotations

import pytest

from llmguard.domains.retrieval.context.rendering import escape_xml_attribute, escape_xml_text
from llmguard.domains.retrieval.contracts import ContextRenderingError


def test_text_and_attribute_escaping_are_structural_and_repeatable() -> None:
    assert escape_xml_text("<&>&lt;") == "&lt;&amp;&gt;&amp;lt;"
    assert escape_xml_attribute("<&>\"'&lt;") == "&lt;&amp;&gt;&quot;&apos;&amp;lt;"


def test_escaping_preserves_unicode_and_line_endings() -> None:
    value = "Cafe\u0301\r\n<"
    assert escape_xml_text(value) == "Cafe\u0301\r\n&lt;"


@pytest.mark.parametrize("func", [escape_xml_text, escape_xml_attribute])
def test_escaping_rejects_non_strings_without_echoing_input(func: object) -> None:
    with pytest.raises(ContextRenderingError) as caught:
        func(42)  # type: ignore[operator]
    assert caught.value.error_code == "CONTEXT_RENDERING_FAILURE"
    assert "42" not in str(caught.value)
