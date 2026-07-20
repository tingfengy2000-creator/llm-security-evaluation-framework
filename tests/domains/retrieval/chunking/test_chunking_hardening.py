from __future__ import annotations

import dataclasses
import hashlib
import inspect
import math
import subprocess
import sys
import unittest
from pathlib import Path

from llmguard.domains.retrieval.chunking import (
    ChunkingConfigurationError as LegacyChunkingConfigurationError,
    ChunkingInputError as LegacyChunkingInputError,
    ChunkingIntegrityError as LegacyChunkingIntegrityError,
    IdentityChunker,
)
from llmguard.domains.retrieval.contracts import (
    ChunkRecord,
    ChunkingConfig,
    ChunkingConfigurationError,
    ChunkingInputError,
    ChunkingIntegrityError,
    ChunkingStrategy,
    DocumentRecord,
    derive_chunk_id,
    format_corpus_content_ref,
)


FIXED_REVISION = "0123456789abcdef0123456789abcdef01234567"
ROOT = Path(__file__).resolve().parents[4]


def identity_config(**overrides: object) -> ChunkingConfig:
    values: dict[str, object] = {
        "strategy": ChunkingStrategy.IDENTITY,
        "schema_version": "1.0",
        "implementation_version": "s6_t5_1_v1",
    }
    values.update(overrides)
    return ChunkingConfig(**values)  # type: ignore[arg-type]


def document(
    *,
    doc_id: str = "DOC-safe-001",
    content: str = "公开的休假制度文本。",
) -> DocumentRecord:
    return DocumentRecord(
        doc_id=doc_id,
        content=content,
        source_id="policy-handbook",
        source_type="enterprise-policy",
        timestamp="2026-07-20T00:00:00Z",
        version="v1",
        content_hash=hashlib.sha256(content.encode("utf-8")).hexdigest(),
    )


def chunk_record(**overrides: object) -> ChunkRecord:
    config = identity_config()
    source = document()
    content_hash = hashlib.sha256(source.content.encode("utf-8")).hexdigest()
    chunking_config_hash = config.fingerprint()
    values: dict[str, object] = {
        "chunk_schema_version": config.schema_version,
        "corpus_snapshot_id": "stage6-baseline-20260720",
        "parent_doc_id": source.doc_id,
        "chunk_index": 0,
        "content": source.content,
        "content_hash": content_hash,
        "chunking_config_hash": chunking_config_hash,
        "chunking_strategy": config.strategy.value,
        "source_id": source.source_id,
        "source_type": source.source_type,
        "timestamp": source.timestamp,
        "version": source.version,
        "public_metadata": {"language": "zh-CN"},
    }
    values["chunk_id"] = derive_chunk_id(
        chunk_schema_version=values["chunk_schema_version"],  # type: ignore[arg-type]
        corpus_snapshot_id=values["corpus_snapshot_id"],  # type: ignore[arg-type]
        parent_doc_id=values["parent_doc_id"],  # type: ignore[arg-type]
        chunk_index=values["chunk_index"],  # type: ignore[arg-type]
        content_hash=values["content_hash"],  # type: ignore[arg-type]
        chunking_config_hash=values["chunking_config_hash"],  # type: ignore[arg-type]
    )
    values["content_ref"] = format_corpus_content_ref(
        values["corpus_snapshot_id"],  # type: ignore[arg-type]
        values["chunk_id"],  # type: ignore[arg-type]
    )
    values.update(overrides)
    return ChunkRecord(**values)  # type: ignore[arg-type]


class ChunkingHardeningTests(unittest.TestCase):
    def test_strategy_vocabulary_is_exact_and_only_identity_has_an_implementation(self) -> None:
        self.assertEqual(
            {"identity", "fixed_token", "token_overlap", "sentence", "semantic"},
            {strategy.value for strategy in ChunkingStrategy},
        )
        self.assertEqual(
            "llmguard.domains.retrieval.chunking.identity_chunker",
            inspect.getmodule(IdentityChunker).__name__,
        )
        chunking_root = ROOT / "src" / "llmguard" / "domains" / "retrieval" / "chunking"
        source = "\n".join(path.read_text(encoding="utf-8") for path in chunking_root.glob("*.py"))
        for prohibited_name in (
            "FixedTokenChunker",
            "OverlappingTokenChunker",
            "SentenceChunker",
            "SemanticChunker",
        ):
            with self.subTest(prohibited_name=prohibited_name):
                self.assertNotIn(prohibited_name, source)
        self.assertFalse((chunking_root / "models.py").exists())

    def test_token_configs_use_max_tokens_and_no_window_size_field_exists(self) -> None:
        self.assertNotIn("window_size", {field.name for field in dataclasses.fields(ChunkingConfig)})
        fixed = ChunkingConfig(
            strategy=ChunkingStrategy.FIXED_TOKEN,
            schema_version="1.0",
            implementation_version="future_contract_v1",
            tokenizer_model_id="tokenizer/example",
            tokenizer_revision=FIXED_REVISION,
            max_tokens=128,
        )
        overlap = ChunkingConfig(
            strategy=ChunkingStrategy.TOKEN_OVERLAP,
            schema_version="1.0",
            implementation_version="future_contract_v1",
            tokenizer_model_id="tokenizer/example",
            tokenizer_revision=FIXED_REVISION,
            max_tokens=128,
            overlap_tokens=32,
        )
        self.assertEqual(128, fixed.canonical_payload()["max_tokens"])
        self.assertEqual(32, overlap.canonical_payload()["overlap_tokens"])

    def test_configuration_errors_use_contract_error_and_hash_only_active_semantics(self) -> None:
        with self.assertRaises(ChunkingConfigurationError):
            identity_config(max_tokens=128)
        with self.assertRaises(ChunkingConfigurationError):
            ChunkingConfig(
                strategy=ChunkingStrategy.TOKEN_OVERLAP,
                schema_version="1.0",
                implementation_version="future_contract_v1",
                tokenizer_model_id="tokenizer/example",
                tokenizer_revision=FIXED_REVISION,
                max_tokens=128,
                overlap_tokens=128,
            )
        kwargs = {
            "strategy": ChunkingStrategy.FIXED_TOKEN,
            "schema_version": "1.0",
            "implementation_version": "future_contract_v1",
            "tokenizer_model_id": "tokenizer/example",
            "tokenizer_revision": FIXED_REVISION,
            "max_tokens": 128,
        }
        reordered = {key: kwargs[key] for key in reversed(tuple(kwargs))}
        self.assertEqual(
            ChunkingConfig(**kwargs).fingerprint(),
            ChunkingConfig(**reordered).fingerprint(),
        )
        self.assertNotEqual(
            ChunkingConfig(**kwargs).fingerprint(),
            ChunkingConfig(**{**kwargs, "max_tokens": 256}).fingerprint(),
        )

    def test_config_hash_is_stable_in_a_separate_python_process(self) -> None:
        command = (
            "from llmguard.domains.retrieval.contracts import ChunkingConfig, ChunkingStrategy; "
            "print(ChunkingConfig(strategy=ChunkingStrategy.IDENTITY, schema_version='1.0', "
            "implementation_version='s6_t5_1_v1').fingerprint())"
        )
        output = subprocess.check_output([sys.executable, "-c", command], text=True).strip()
        self.assertEqual(identity_config().fingerprint(), output)

    def test_contract_errors_are_reexported_by_legacy_chunking_import_path(self) -> None:
        self.assertIs(ChunkingConfigurationError, LegacyChunkingConfigurationError)
        self.assertIs(ChunkingInputError, LegacyChunkingInputError)
        self.assertIs(ChunkingIntegrityError, LegacyChunkingIntegrityError)
        self.assertTrue(issubclass(ChunkingIntegrityError, ValueError))

    def test_chunk_record_validates_its_canonical_identity(self) -> None:
        record = chunk_record()
        self.assertEqual("1.0", record.chunk_schema_version)
        for field_name, value in (
            ("chunk_id", "CH-" + "f" * 64),
            ("parent_doc_id", "DOC-safe-002"),
            ("corpus_snapshot_id", "stage6-baseline-20260721"),
            ("chunking_config_hash", "a" * 64),
        ):
            with self.subTest(field_name=field_name):
                with self.assertRaises(ChunkingIntegrityError):
                    dataclasses.replace(record, **{field_name: value})
        with self.assertRaises(ChunkingIntegrityError):
            dataclasses.replace(record, content_hash="a" * 64)

    def test_chunk_record_rejects_invalid_input_without_plaintext_in_error(self) -> None:
        secret_content = "敏感正文不应出现在异常中"
        source = document(doc_id="DOC-sensitive-raw-id", content=secret_content)
        object.__setattr__(source, "content_hash", "0" * 64)
        with self.assertRaises(ChunkingIntegrityError) as captured:
            IdentityChunker().chunk(
                source,
                corpus_snapshot_id="stage6-baseline-20260720",
                config=identity_config(),
            )
        self.assertNotIn(secret_content, str(captured.exception))
        self.assertNotIn(source.doc_id, str(captured.exception))
        self.assertEqual("DOCUMENT_CONTENT_HASH_MISMATCH", captured.exception.error_code)

    def test_identity_chunker_rejects_nonidentity_config_with_configuration_error(self) -> None:
        config = ChunkingConfig(
            strategy=ChunkingStrategy.FIXED_TOKEN,
            schema_version="1.0",
            implementation_version="future_contract_v1",
            tokenizer_model_id="tokenizer/example",
            tokenizer_revision=FIXED_REVISION,
            max_tokens=128,
        )
        with self.assertRaises(ChunkingConfigurationError):
            IdentityChunker().chunk(
                document(),
                corpus_snapshot_id="stage6-baseline-20260720",
                config=config,
            )

    def test_identity_chunker_requires_an_explicit_snapshot_and_returns_contract_type(self) -> None:
        signature = inspect.signature(IdentityChunker.chunk)
        self.assertIs(signature.parameters["corpus_snapshot_id"].default, inspect.Parameter.empty)
        chunks = IdentityChunker().chunk(
            document(),
            corpus_snapshot_id="stage6-baseline-20260720",
            config=identity_config(),
        )
        self.assertEqual(1, len(chunks))
        self.assertIsInstance(chunks[0], ChunkRecord)

    def test_metadata_rejects_keys_and_values_without_python_sort_error(self) -> None:
        invalid_metadata = (
            {1: "value", "safe": True},
            {"C:\\secret": "value"},
            {"/etc/passwd": "value"},
            {"\\\\server\\share": "value"},
            {"file:///tmp/data": "value"},
            {"safe": "file:///tmp/data"},
            {"score": math.nan},
            {"score": math.inf},
            {"count": 2**53},
            {"object": object()},
        )
        for metadata in invalid_metadata:
            with self.subTest(metadata_type=type(next(iter(metadata))).__name__):
                with self.assertRaises(ChunkingInputError):
                    chunk_record(public_metadata=metadata)

    def test_metadata_rejects_mapping_and_sequence_cycles(self) -> None:
        mapping: dict[str, object] = {}
        mapping["self"] = mapping
        sequence: list[object] = []
        sequence.append(sequence)
        for metadata in ({"nested": mapping}, {"nested": sequence}):
            with self.subTest(metadata_type=type(metadata["nested"]).__name__):
                with self.assertRaises(ChunkingInputError):
                    chunk_record(public_metadata=metadata)

    def test_metadata_rejects_case_separator_and_unicode_label_variants(self) -> None:
        for key in (
            "GROUND_TRUTH",
            "ground-truth",
            "Ground Truth",
            "Ｇｒｏｕｎｄ＿Ｔｒｕｔｈ",
        ):
            with self.subTest(key=key):
                with self.assertRaises(ChunkingInputError):
                    chunk_record(public_metadata={key: "hidden"})

    def test_audit_and_repr_do_not_expose_content_and_metadata_is_deeply_immutable(self) -> None:
        metadata = {"nested": {"tags": ["public"]}}
        record = chunk_record(public_metadata=metadata)
        metadata["nested"]["tags"].append("mutated")  # type: ignore[index]
        audit = record.to_audit_dict()
        self.assertNotIn("content", audit)
        self.assertIn("content_hash", audit)
        self.assertIn("content_length", audit)
        self.assertNotIn(record.content, repr(record))
        self.assertEqual(["public"], audit["public_metadata"]["nested"]["tags"])
        with self.assertRaises(TypeError):
            record.public_metadata["nested"] = {}  # type: ignore[index]


if __name__ == "__main__":
    unittest.main()
