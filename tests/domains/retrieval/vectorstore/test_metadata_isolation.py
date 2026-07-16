from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from llmguard.domains.retrieval.vectorstore.chroma_store import ChromaVectorStore
from llmguard.domains.retrieval.vectorstore.fingerprint import CollectionFingerprint
from llmguard.domains.retrieval.vectorstore.models import (
    PUBLIC_METADATA_FIELDS,
    MetadataIsolationError,
    VectorCollectionSpec,
    VectorDocument,
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


def make_document(metadata: dict[str, object]) -> VectorDocument:
    return VectorDocument(
        doc_id="doc-1",
        vector=(1.0, 0.0, 0.0),
        metadata=metadata,
        content_hash=CONTENT_HASH,
        content_ref="chroma:doc-1",
    )


def allowed_metadata() -> dict[str, object]:
    return {
        "doc_id": "doc-1",
        "source_id": "source-1",
        "source_type": "policy",
        "timestamp": "2026-07-01T00:00:00Z",
        "version": "1.0",
        "content_hash": CONTENT_HASH,
    }


class MetadataIsolationTests(unittest.TestCase):
    def test_forbidden_metadata_is_rejected_before_chroma_write(self) -> None:
        metadata = allowed_metadata()
        metadata["ground_truth"] = "not-allowed"

        with self.assertRaises(MetadataIsolationError):
            make_document(metadata)

    def test_chroma_receives_only_allowlisted_document_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            store = ChromaVectorStore(Path(temporary_directory))
            collection_spec = make_spec()
            store.create_or_open_collection(collection_spec)
            store.upsert(collection_spec, (make_document(allowed_metadata()),))

            raw_collection = store._client.get_collection(collection_spec.collection_name)
            stored = raw_collection.get(include=["metadatas"])
            metadata = stored["metadatas"][0]

            self.assertIsNotNone(metadata)
            assert metadata is not None
            self.assertTrue(set(metadata).issubset(PUBLIC_METADATA_FIELDS))
            self.assertNotIn("ground_truth", metadata)
            self.assertNotIn("attack_id", metadata)
            store.close()


if __name__ == "__main__":
    unittest.main()
