from __future__ import annotations

import pytest

from llmguard.domains.retrieval.contracts import ContentRef, format_corpus_content_ref


def test_corpus_content_ref_is_canonical_and_string_compatible() -> None:
    reference = ContentRef("corpus:stage6-v1:CH-" + "a" * 64)
    assert isinstance(reference, str)
    assert reference.scheme == "corpus"
    assert reference.corpus_snapshot_id == "stage6-v1"
    assert reference.chunk_id == "CH-" + "a" * 64
    assert format_corpus_content_ref("stage6-v1", "CH-" + "a" * 64) == reference


def test_legacy_chroma_reference_is_explicitly_compatible_but_paths_are_rejected() -> None:
    assert ContentRef("chroma:fixture-doc").scheme == "chroma"
    file_reference = "file:" + "///controlled/path"
    windows_reference = "corpus:" + "C:" + "/controlled:CH-" + "a" * 64
    for value in (file_reference, windows_reference, "raw body"):
        with pytest.raises(ValueError, match="INVALID_CONTENT_REF"):
            ContentRef(value)
