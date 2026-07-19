from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from llmguard.domains.retrieval.embedding.model_spec import EmbeddingModelSpec
from llmguard.domains.retrieval.vectorstore.chroma_store import ChromaVectorStore
from llmguard.domains.retrieval.vectorstore.fingerprint import CollectionFingerprint
from llmguard.domains.retrieval.vectorstore.models import (
    CollectionFingerprintMismatchError,
    VectorCollectionSpec,
    VectorDocument,
    VectorSearchQuery,
)


CONTENT_HASH = "a" * 64


def make_spec(corpus_hash: str = "a" * 64) -> VectorCollectionSpec:
    document_embedding_spec = EmbeddingModelSpec(
        provider="llmguard_static",
        model_id="llmguard/static-fixture",
        revision="16e5344fbfc7dfbbbe0019d30cec21e2940cb4e1",
        dimension=3,
        normalize_embeddings=True,
        device="cpu",
        batch_size=16,
        trust_remote_code=False,
        local_files_only=True,
        implementation_version="s6_t4_v1",
    )
    fingerprint = CollectionFingerprint.from_document_embedding_spec(
        corpus_hash=corpus_hash,
        corpus_manifest_version="1.0.1",
        chunking_config_hash="b" * 64,
        document_embedding_spec=document_embedding_spec,
        distance_metric="cosine",
        vector_schema_version="1.0",
        public_metadata_schema_version="1.0",
    )
    return VectorCollectionSpec(fingerprint=fingerprint.value, dimension=3)


def make_document() -> VectorDocument:
    return VectorDocument(
        doc_id="doc-1",
        vector=(1.0, 0.0, 0.0),
        metadata={
            "doc_id": "doc-1",
            "source_id": "source-1",
            "source_type": "policy",
            "timestamp": "2026-07-01T00:00:00Z",
            "version": "1.0",
            "content_hash": CONTENT_HASH,
        },
        content_hash=CONTENT_HASH,
        content_ref="chroma:doc-1",
    )


class ChromaPersistenceTests(unittest.TestCase):
    def test_close_and_reopen_preserves_exact_fingerprint_and_hits(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            directory = Path(temporary_directory)
            collection = make_spec()
            writer = ChromaVectorStore(directory)
            writer.create_or_open_collection(collection)
            writer.upsert(collection, (make_document(),))
            writer.close()

            reader = ChromaVectorStore(directory)
            info = reader.create_or_open_collection(collection)
            hits = reader.query(
                collection,
                VectorSearchQuery(vector=(1.0, 0.0, 0.0), top_k=1),
            )

            self.assertEqual(collection.fingerprint, info.fingerprint)
            self.assertEqual(1, info.count)
            self.assertEqual("doc-1", hits[0].doc_id)
            reader.close()

    def test_different_fingerprints_use_isolated_collections(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            store = ChromaVectorStore(Path(temporary_directory))
            first = make_spec()
            second = make_spec("c" * 64)
            first_info = store.create_or_open_collection(first)
            second_info = store.create_or_open_collection(second)

            self.assertNotEqual(first_info.collection_name, second_info.collection_name)
            self.assertEqual(0, store.count(first))
            self.assertEqual(0, store.count(second))
            store.close()

    def test_collection_metadata_mismatch_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            store = ChromaVectorStore(Path(temporary_directory))
            collection = make_spec()
            store.create_or_open_collection(collection)

            # The collection name deliberately stays stable while this field differs.
            incompatible = VectorCollectionSpec(
                fingerprint=collection.fingerprint,
                dimension=3,
                vector_schema_version="2.0",
            )
            with self.assertRaises(CollectionFingerprintMismatchError):
                store.create_or_open_collection(incompatible)
            store.close()


if __name__ == "__main__":
    unittest.main()
