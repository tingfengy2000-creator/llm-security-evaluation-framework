from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from llmguard.domains.retrieval.vectorstore.chroma_store import ChromaVectorStore
from llmguard.domains.retrieval.vectorstore.fingerprint import CollectionFingerprint
from llmguard.domains.retrieval.vectorstore.models import (
    VectorCollectionSpec,
    VectorDocument,
    VectorSearchQuery,
)


CONTENT_HASH = "a" * 64


def make_spec() -> VectorCollectionSpec:
    fingerprint = CollectionFingerprint(
        corpus_hash="a" * 64,
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
    return VectorCollectionSpec(fingerprint=fingerprint.value, dimension=3)


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


class ChromaVectorStoreContractTests(unittest.TestCase):
    def test_query_returns_stable_domain_hits_with_doc_id_tie_breaking(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            store = ChromaVectorStore(Path(temporary_directory))
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
            self.assertEqual((0.0, 0.0, 1.0), tuple(round(hit.distance, 6) for hit in hits))
            self.assertEqual((1.0, 1.0, 0.0), tuple(round(hit.similarity, 6) for hit in hits))
            self.assertEqual(3, store.count(collection))
            self.assertEqual(collection.fingerprint, store.get_collection_info(collection).fingerprint)
            store.close()


if __name__ == "__main__":
    unittest.main()
