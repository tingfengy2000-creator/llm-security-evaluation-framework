from __future__ import annotations

import pytest

from llmguard.domains.retrieval.contracts import CitationBinding, CitationInputError

from conftest import chunk_id


def _binding(*, citation_id: object = "E1", **overrides: object) -> CitationBinding:
    values: dict[str, object] = {
        "citation_id": citation_id,
        "evidence_uid": "EV-" + "a" * 64,
        "chunk_id": chunk_id(),
        "parent_doc_id": "parent-1",
        "content_hash": "b" * 64,
        "source_id": "source-1",
        "version": "v1",
        "rank": 1,
    }
    values.update(overrides)
    return CitationBinding(**values)  # type: ignore[arg-type]


@pytest.mark.parametrize("citation_id", ["E1", "E2", "E10"])
def test_valid_citation_ids(citation_id: str) -> None:
    assert _binding(citation_id=citation_id).citation_id == citation_id


@pytest.mark.parametrize("citation_id", ["E0", "E01", "E-1", "e1", "[E1]", "", None])
def test_invalid_citation_ids_fail_closed(citation_id: object) -> None:
    with pytest.raises(CitationInputError) as caught:
        _binding(citation_id=citation_id)
    assert caught.value.error_code == "INVALID_CITATION_ID"
    assert str(caught.value) == "citation id is invalid [INVALID_CITATION_ID]"


def test_citation_id_obeys_the_public_identifier_length_limit() -> None:
    with pytest.raises(CitationInputError) as caught:
        _binding(citation_id="E" + "1" * 128)

    assert caught.value.error_code == "INVALID_CITATION_ID"
    assert str(caught.value) == "citation id is invalid [INVALID_CITATION_ID]"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("evidence_uid", "evidence-1"),
        ("evidence_uid", "EV-" + "A" * 64),
        ("chunk_id", "chunk-1"),
        ("parent_doc_id", ""),
        ("content_hash", "0" * 63),
        ("source_id", "source\n1"),
        ("version", ""),
        ("rank", 0),
    ],
)
def test_invalid_binding_fields_have_their_own_fixed_error(field: str, value: object) -> None:
    with pytest.raises(CitationInputError) as caught:
        _binding(**{field: value})

    assert caught.value.error_code == "INVALID_CITATION_BINDING"
    assert str(caught.value) == "citation binding is invalid [INVALID_CITATION_BINDING]"


def test_binding_audit_has_no_plaintext_or_metadata() -> None:
    binding = _binding()
    audit = binding.to_audit_dict()
    assert audit["citation_id"] == "E1"
    assert "content" not in audit
    assert "metadata" not in audit
    with pytest.raises(CitationInputError):
        _binding(rank=0)
