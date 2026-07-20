from __future__ import annotations

import hashlib
import unittest

from llmguard.domains.retrieval.chunking import (
    ChunkingIntegrityError,
    IdentityChunker,
)
from llmguard.domains.retrieval.contracts import (
    ChunkingConfig,
    ChunkingStrategy,
    DocumentRecord,
)


def make_document(content: str = "员工可在系统中提交休假申请。") -> DocumentRecord:
    return DocumentRecord(
        doc_id="DOC-leave-001",
        content=content,
        source_id="handbook",
        source_type="policy",
        timestamp="2026-07-20T00:00:00Z",
        version="v1",
        content_hash=hashlib.sha256(content.encode("utf-8")).hexdigest(),
    )


def identity_config() -> ChunkingConfig:
    return ChunkingConfig(
        strategy=ChunkingStrategy.IDENTITY,
        schema_version="1.0",
        implementation_version="s6_t5_1_v1",
    )


class IdentityChunkerTests(unittest.TestCase):
    def test_identity_chunker_emits_one_auditable_chunk_without_repr_content(self) -> None:
        chunk = IdentityChunker().chunk(
            make_document(),
            corpus_snapshot_id="stage6-baseline-20260720",
            config=identity_config(),
            public_metadata={"language": "zh-CN", "provenance": {"source": "policy"}},
        )[0]

        self.assertEqual("DOC-leave-001", chunk.parent_doc_id)
        self.assertEqual(0, chunk.chunk_index)
        self.assertEqual("identity", chunk.chunking_strategy)
        self.assertEqual("corpus:stage6-baseline-20260720:" + chunk.chunk_id, chunk.content_ref)
        self.assertEqual("员工可在系统中提交休假申请。", chunk.content)
        self.assertNotIn(chunk.content, repr(chunk))
        self.assertEqual("zh-CN", chunk.public_metadata["language"])
        with self.assertRaises(TypeError):
            chunk.public_metadata["language"] = "en"  # type: ignore[index]

    def test_chunker_detects_document_hash_integrity_failure_without_echoing_content(self) -> None:
        document = make_document()
        object.__setattr__(document, "content_hash", "0" * 64)

        with self.assertRaises(ChunkingIntegrityError) as captured:
            IdentityChunker().chunk(
                document,
                corpus_snapshot_id="stage6-baseline-20260720",
                config=identity_config(),
            )

        self.assertNotIn(document.content, str(captured.exception))

    def test_public_metadata_rejects_label_variants_and_absolute_paths(self) -> None:
        for metadata in (
            {"nested": {"Ｇｒｏｕｎｄ＿Ｔｒｕｔｈ": "secret"}},
            {"expected_clean_doc_ids": ["DOC-leave-001"]},
            {"local_path": "C:\\Users\\Admin\\secret.txt"},
        ):
            with self.subTest(metadata=metadata):
                with self.assertRaises(ValueError):
                    IdentityChunker().chunk(
                        make_document(),
                        corpus_snapshot_id="stage6-baseline-20260720",
                        config=identity_config(),
                        public_metadata=metadata,
                    )


if __name__ == "__main__":
    unittest.main()
