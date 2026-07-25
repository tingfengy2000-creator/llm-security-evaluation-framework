from __future__ import annotations

import hashlib

import pytest

from llmguard.domains.retrieval.context import (
    CorpusContentResolver,
    InMemoryCorpusSnapshotReader,
    StaticApprovedCorpusSnapshotRegistry,
    StaticLegacyContentRefAdapter,
)
from llmguard.domains.retrieval.contracts import (
    ContentRef,
    ContentResolutionIntegrityError,
    ContentResolutionLookupError,
    ContentResolutionRuntimeError,
    RetrievalInputError,
)


def _hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def _chunk(letter: str = "a") -> str:
    return "CH-" + letter * 64


def _resolver(content: str = "Synthetic content\r\nwith exact bytes.") -> tuple[
    CorpusContentResolver,
    ContentRef,
]:
    reference = ContentRef.corpus("synthetic-v1", _chunk())
    reader = InMemoryCorpusSnapshotReader(
        corpus_snapshot_id="synthetic-v1",
        snapshot_fingerprint="b" * 64,
        chunks={_chunk(): content},
    )
    registry = StaticApprovedCorpusSnapshotRegistry(
        registrations={"synthetic-v1": ("b" * 64, reader)}
    )
    return CorpusContentResolver(registry=registry), reference


def test_canonical_reference_resolves_exact_content_and_audits_only_metadata() -> None:
    content = "Synthetic content\r\nwith exact bytes."
    resolver, reference = _resolver(content)

    resolved = resolver.resolve(content_ref=reference, expected_content_hash=_hash(content))

    assert resolved.content == content
    assert resolved.canonical_content_ref == reference
    assert content not in repr(resolved)
    assert content not in str(resolved.to_audit_dict())


def test_hash_mismatch_fails_closed_without_returning_content() -> None:
    resolver, reference = _resolver()
    with pytest.raises(ContentResolutionIntegrityError) as caught:
        resolver.resolve(content_ref=reference, expected_content_hash="0" * 64)

    assert caught.value.error_code == "CONTENT_HASH_MISMATCH"
    assert "Synthetic content" not in str(caught.value)


def test_malformed_expected_hash_is_input_error_not_content_mismatch() -> None:
    resolver, reference = _resolver()
    with pytest.raises(RetrievalInputError) as caught:
        resolver.resolve(content_ref=reference, expected_content_hash="not-a-sha256")

    assert caught.value.error_code == "RETRIEVAL_INPUT_INVALID"


def test_reader_and_registry_are_immutable_and_do_not_expose_content_in_repr() -> None:
    chunks = {_chunk(): "Synthetic only"}
    reader = InMemoryCorpusSnapshotReader(
        corpus_snapshot_id="synthetic-v1",
        snapshot_fingerprint="b" * 64,
        chunks=chunks,
    )
    chunks[_chunk("c")] = "post-construction mutation"
    assert reader.read_chunk(chunk_id=_chunk()) == "Synthetic only"
    assert "Synthetic only" not in repr(reader)
    assert not hasattr(reader, "chunks")
    with pytest.raises(TypeError):
        reader._chunks[_chunk("c")] = "blocked"  # type: ignore[index]

    registry = StaticApprovedCorpusSnapshotRegistry(
        registrations={"synthetic-v1": ("b" * 64, reader)}
    )
    assert not hasattr(registry, "registrations")
    with pytest.raises(TypeError):
        registry._registrations["another"] = ("b" * 64, reader)  # type: ignore[index]


def test_unknown_snapshot_and_chunk_are_lookup_errors() -> None:
    resolver, reference = _resolver()
    unknown_snapshot = ContentRef.corpus("unknown-v1", _chunk())
    with pytest.raises(ContentResolutionLookupError) as snapshot_error:
        resolver.resolve(content_ref=unknown_snapshot, expected_content_hash="0" * 64)
    assert snapshot_error.value.error_code == "UNKNOWN_CORPUS_SNAPSHOT"

    unknown_chunk = ContentRef.corpus("synthetic-v1", _chunk("c"))
    with pytest.raises(ContentResolutionLookupError) as chunk_error:
        resolver.resolve(content_ref=unknown_chunk, expected_content_hash="0" * 64)
    assert chunk_error.value.error_code == "UNKNOWN_CORPUS_CHUNK"
    assert str(reference) not in str(chunk_error.value)


def test_registry_rejects_reader_identity_and_pinned_fingerprint_mismatch() -> None:
    reader = InMemoryCorpusSnapshotReader(
        corpus_snapshot_id="actual-v1",
        snapshot_fingerprint="b" * 64,
        chunks={_chunk(): "Synthetic"},
    )
    registry = StaticApprovedCorpusSnapshotRegistry(
        registrations={"registered-v1": ("b" * 64, reader)}
    )
    with pytest.raises(ContentResolutionIntegrityError) as identity_error:
        registry.get_reader(corpus_snapshot_id="registered-v1")
    assert identity_error.value.error_code == "CORPUS_SNAPSHOT_INTEGRITY_FAILURE"

    matching_reader = InMemoryCorpusSnapshotReader(
        corpus_snapshot_id="registered-v1",
        snapshot_fingerprint="c" * 64,
        chunks={_chunk(): "Synthetic"},
    )
    fingerprint_registry = StaticApprovedCorpusSnapshotRegistry(
        registrations={"registered-v1": ("b" * 64, matching_reader)}
    )
    with pytest.raises(ContentResolutionIntegrityError) as fingerprint_error:
        fingerprint_registry.get_reader(corpus_snapshot_id="registered-v1")
    assert fingerprint_error.value.error_code == "CORPUS_SNAPSHOT_INTEGRITY_FAILURE"


def test_legacy_adapter_is_exact_deterministic_and_uses_normal_resolution_flow() -> None:
    content = "Synthetic legacy resolution"
    resolver, canonical = _resolver(content)
    legacy = ContentRef("chroma:legacy-record")
    reversed_mapping = StaticLegacyContentRefAdapter(
        mapping_version="1.0",
        mappings={legacy: canonical, ContentRef("chroma:unused"): canonical},
    )
    ordered_mapping = StaticLegacyContentRefAdapter(
        mapping_version="1.0",
        mappings={ContentRef("chroma:unused"): canonical, legacy: canonical},
    )
    assert reversed_mapping.mapping_hash == ordered_mapping.mapping_hash

    legacy_resolver = CorpusContentResolver(
        registry=resolver.registry,
        legacy_adapter=reversed_mapping,
    )
    assert legacy_resolver.resolve(
        content_ref=legacy,
        expected_content_hash=_hash(content),
    ).canonical_content_ref == canonical

    changed = StaticLegacyContentRefAdapter(
        mapping_version="1.0",
        mappings={legacy: ContentRef.corpus("synthetic-v1", _chunk("c"))},
    )
    assert changed.mapping_hash != reversed_mapping.mapping_hash
    with pytest.raises(TypeError):
        reversed_mapping._mappings[legacy] = canonical  # type: ignore[index]


def test_canonical_reference_does_not_call_legacy_adapter() -> None:
    content = "Synthetic canonical content"
    resolver, reference = _resolver(content)

    class ExplodingAdapter:
        mapping_version = "1.0"
        mapping_hash = "f" * 64

        def to_canonical(self, *, legacy_content_ref: ContentRef) -> ContentRef:
            raise AssertionError("canonical reference must not use legacy adapter")

    guarded = CorpusContentResolver(
        registry=resolver.registry,
        legacy_adapter=ExplodingAdapter(),
    )
    assert guarded.resolve(
        content_ref=reference,
        expected_content_hash=_hash(content),
    ).content == content


def test_non_string_reader_output_and_reader_exception_are_redacted_runtime_errors() -> None:
    class NonStringReader:
        corpus_snapshot_id = "synthetic-v1"
        snapshot_fingerprint = "b" * 64

        def read_chunk(self, *, chunk_id: str) -> object:
            return 7

    class ExplodingReader:
        corpus_snapshot_id = "synthetic-v1"
        snapshot_fingerprint = "b" * 64

        def read_chunk(self, *, chunk_id: str) -> str:
            raise RuntimeError("synthetic body must not appear")

    reference = ContentRef.corpus("synthetic-v1", _chunk())
    for reader in (NonStringReader(), ExplodingReader()):
        registry = StaticApprovedCorpusSnapshotRegistry(
            registrations={"synthetic-v1": ("b" * 64, reader)}
        )
        with pytest.raises(ContentResolutionRuntimeError) as caught:
            CorpusContentResolver(registry=registry).resolve(
                content_ref=reference,
                expected_content_hash="0" * 64,
            )
        assert caught.value.error_code == "CONTENT_RESOLUTION_FAILURE"
        assert "synthetic body must not appear" not in str(caught.value)


def test_legacy_adapter_output_must_be_a_canonical_corpus_reference() -> None:
    resolver, _ = _resolver()

    class InvalidAdapter:
        mapping_version = "1.0"
        mapping_hash = "f" * 64

        def to_canonical(self, *, legacy_content_ref: ContentRef) -> ContentRef:
            return ContentRef("chroma:still-legacy")

    with pytest.raises(ContentResolutionIntegrityError) as caught:
        CorpusContentResolver(
            registry=resolver.registry,
            legacy_adapter=InvalidAdapter(),
        ).resolve(
            content_ref=ContentRef("chroma:legacy-record"),
            expected_content_hash="0" * 64,
        )
    assert caught.value.error_code == "CORPUS_SNAPSHOT_INTEGRITY_FAILURE"


def test_legacy_failures_and_unknown_dependencies_are_redacted() -> None:
    resolver, _ = _resolver()
    legacy = ContentRef("chroma:legacy-record")
    with pytest.raises(ContentResolutionLookupError) as no_adapter:
        resolver.resolve(content_ref=legacy, expected_content_hash="0" * 64)
    assert no_adapter.value.error_code == "UNKNOWN_CONTENT_REF"

    adapter = StaticLegacyContentRefAdapter(mapping_version="1.0", mappings={})
    mapped_resolver = CorpusContentResolver(registry=resolver.registry, legacy_adapter=adapter)
    with pytest.raises(ContentResolutionLookupError) as unmapped:
        mapped_resolver.resolve(content_ref=legacy, expected_content_hash="0" * 64)
    assert unmapped.value.error_code == "UNKNOWN_CONTENT_REF"

    class ExplodingRegistry:
        def get_reader(self, *, corpus_snapshot_id: str) -> object:
            raise RuntimeError("sensitive lower-level detail")

    reference = ContentRef.corpus("synthetic-v1", _chunk())
    with pytest.raises(ContentResolutionRuntimeError) as runtime_error:
        CorpusContentResolver(registry=ExplodingRegistry()).resolve(
            content_ref=reference,
            expected_content_hash="0" * 64,
        )
    assert runtime_error.value.error_code == "CONTENT_RESOLUTION_FAILURE"
    assert "sensitive lower-level detail" not in str(runtime_error.value)
