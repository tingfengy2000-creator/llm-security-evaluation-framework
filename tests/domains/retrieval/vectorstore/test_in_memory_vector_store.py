from __future__ import annotations

import unittest

from llmguard.domains.retrieval.vectorstore.fingerprint import CollectionFingerprint
from llmguard.domains.retrieval.vectorstore.in_memory_store import InMemoryVectorStore
from llmguard.domains.retrieval.vectorstore.models import (
    VectorCollectionSpec,
    VectorDimensionError,
    VectorDocument,
    VectorSearchQuery,
    VectorStoreConfigurationError,
)


CONTENT_HASH = "a" * 64


def make_fingerprint(corpus_hash: str = "a" * 64) -> CollectionFingerprint:
    return CollectionFingerprint(
        corpus_hash=corpus_hash,
        corpus_manifest_version="1.0.1",
        chunking_config_hash="b" * 64,
        embedding_model_id="llmguard/static-fixture",
        embedding_revision="16e5344fbfc7dfbbbe0019d30cec21e2940cb4e1",
        embedding_dimension=3,
        normalize_embeddings=True,
        distance_metric="cosine",
        vector_schema_version="1.0",
        public_metadata_schema_version="1.0",
    )


def make_spec(corpus_hash: str = "a" * 64) -> VectorCollectionSpec:
    return VectorCollectionSpec(fingerprint=make_fingerprint(corpus_hash).value, dimension=3)


def make_document(doc_id: str, vector: tuple[float, ...]) -> VectorDocument:
    return VectorDocument(
        doc_id=doc_id,
        vector=vector,
        metadata={
            "doc_id": doc_id,
            "source_id": "source-1",
            "source_type": "policy",
            "timestamp": "2026-07-01T00:00:00Z",
            "version": "1.0",
            "content_hash": CONTENT_HASH,
        },
        content_hash=CONTENT_HASH,
        content_ref=f"chroma:{doc_id}",
    )


class InMemoryVectorStoreTests(unittest.TestCase):
    def test_query_uses_cosine_distance_and_doc_id_tie_breaking(self) -> None:
        store = InMemoryVectorStore()
        collection = make_spec()
        store.create_or_open_collection(collection)
        store.upsert(
            collection,
            (
                make_document("doc-b", (0.0, 1.0, 0.0)),
                make_document("doc-a", (0.0, 1.0, 0.0)),
                make_document("doc-c", (-1.0, 0.0, 0.0)),
            ),
        )

        hits = store.query(
            collection,
            VectorSearchQuery(vector=(0.0, 1.0, 0.0), top_k=3),
        )

        self.assertEqual(("doc-a", "doc-b", "doc-c"), tuple(hit.doc_id for hit in hits))
        self.assertEqual((1, 2, 3), tuple(hit.rank for hit in hits))
        self.assertEqual((0.0, 0.0, 1.0), tuple(hit.distance for hit in hits))
        self.assertEqual((1.0, 1.0, 0.0), tuple(hit.similarity for hit in hits))

    def test_upsert_replaces_same_doc_id_and_collections_are_isolated(self) -> None:
        store = InMemoryVectorStore()
        first = make_spec()
        second = make_spec("c" * 64)
        store.create_or_open_collection(first)
        store.create_or_open_collection(second)
        store.upsert(first, (make_document("doc-1", (1.0, 0.0, 0.0)),))
        store.upsert(first, (make_document("doc-1", (0.0, 1.0, 0.0)),))

        self.assertEqual(1, store.count(first))
        self.assertEqual(0, store.count(second))
        self.assertEqual(
            "doc-1",
            store.query(first, VectorSearchQuery(vector=(0.0, 1.0, 0.0), top_k=1))[0].doc_id,
        )

    def test_rejects_dimension_and_collection_configuration_mismatches(self) -> None:
        store = InMemoryVectorStore()
        collection = make_spec()
        store.create_or_open_collection(collection)

        with self.assertRaises(VectorDimensionError):
            store.upsert(collection, (make_document("doc-1", (1.0, 0.0)),))
        with self.assertRaises(VectorDimensionError):
            store.query(collection, VectorSearchQuery(vector=(1.0, 0.0), top_k=1))
        with self.assertRaises(VectorStoreConfigurationError):
            store.create_or_open_collection(
                VectorCollectionSpec(fingerprint=collection.fingerprint, dimension=4)
            )


if __name__ == "__main__":
    unittest.main()
