from __future__ import annotations

import hashlib
import unittest

from llmguard.domains.retrieval.chunking import IdentityChunker
from llmguard.domains.retrieval.contracts import (
    ChunkingConfig,
    ChunkingStrategy,
    DocumentRecord,
    format_corpus_content_ref,
)


def make_document(*, content: str = "采购审批需要部门负责人确认。") -> DocumentRecord:
    return DocumentRecord(
        doc_id="DOC-procurement-001",
        content=content,
        source_id="handbook",
        source_type="policy",
        timestamp="2026-07-20T00:00:00Z",
        version="v1",
        content_hash=hashlib.sha256(content.encode("utf-8")).hexdigest(),
    )


def config(*, implementation_version: str = "s6_t5_1_v1") -> ChunkingConfig:
    return ChunkingConfig(
        strategy=ChunkingStrategy.IDENTITY,
        schema_version="1.0",
        implementation_version=implementation_version,
    )


class ChunkIdStabilityTests(unittest.TestCase):
    def test_same_inputs_produce_identical_chunk_id_and_reference(self) -> None:
        first = IdentityChunker().chunk(
            make_document(),
            corpus_snapshot_id="stage6-baseline-20260720",
            config=config(),
        )[0]
        second = IdentityChunker().chunk(
            make_document(),
            corpus_snapshot_id="stage6-baseline-20260720",
            config=config(),
        )[0]

        self.assertEqual(first.chunk_id, second.chunk_id)
        self.assertEqual(first.content_ref, second.content_ref)

    def test_semantic_identity_changes_change_the_chunk_id(self) -> None:
        baseline = IdentityChunker().chunk(
            make_document(),
            corpus_snapshot_id="stage6-baseline-20260720",
            config=config(),
        )[0]
        variants = (
            IdentityChunker().chunk(
                make_document(content="采购审批需要财务负责人确认。"),
                corpus_snapshot_id="stage6-baseline-20260720",
                config=config(),
            )[0],
            IdentityChunker().chunk(
                make_document(),
                corpus_snapshot_id="stage6-baseline-20260721",
                config=config(),
            )[0],
            IdentityChunker().chunk(
                make_document(),
                corpus_snapshot_id="stage6-baseline-20260720",
                config=config(implementation_version="s6_t5_1_v2"),
            )[0],
        )

        for variant in variants:
            with self.subTest(variant=variant.chunk_id):
                self.assertNotEqual(baseline.chunk_id, variant.chunk_id)

    def test_content_reference_rejects_unsafe_snapshot_or_chunk_id(self) -> None:
        with self.assertRaises(ValueError):
            format_corpus_content_ref("C:\\unsafe", "CH-" + "a" * 64)
        with self.assertRaises(ValueError):
            format_corpus_content_ref("snapshot", "CH-not-a-digest")


if __name__ == "__main__":
    unittest.main()
