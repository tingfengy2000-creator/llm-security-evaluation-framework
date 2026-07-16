"""Explicit-network integration coverage for the pinned Stage 6 embedding baseline."""

from __future__ import annotations

import hashlib
import os
import tempfile
import unittest
from pathlib import Path


RUN_REAL_EMBEDDING_TESTS = os.getenv("LLMGUARD_RUN_REAL_EMBEDDING_TESTS") == "1"
FIXED_REVISION = "16e5344fbfc7dfbbbe0019d30cec21e2940cb4e1"


@unittest.skipUnless(
    RUN_REAL_EMBEDDING_TESTS,
    "set LLMGUARD_RUN_REAL_EMBEDDING_TESTS=1 to run the pinned real-model integration test",
)
class RealEmbeddingChromaIntegrationTests(unittest.TestCase):
    def test_multilingual_embeddings_persist_and_reopen_without_public_label_metadata(self) -> None:
        from llmguard.domains.retrieval.embedding.model_spec import EmbeddingModelSpec
        from llmguard.domains.retrieval.embedding.sentence_transformer_provider import (
            SentenceTransformerEmbeddingProvider,
        )
        from llmguard.domains.retrieval.vectorstore.chroma_store import ChromaVectorStore
        from llmguard.domains.retrieval.vectorstore.fingerprint import CollectionFingerprint
        from llmguard.domains.retrieval.vectorstore.models import (
            VectorCollectionSpec,
            VectorDocument,
            VectorSearchQuery,
        )

        model_spec = EmbeddingModelSpec(
            provider="sentence_transformers",
            model_id="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
            revision=FIXED_REVISION,
            dimension=384,
            normalize_embeddings=True,
            device="cpu",
            batch_size=2,
            trust_remote_code=False,
            local_files_only=False,
            implementation_version="s6_t4_sentence_transformers_v1",
        )
        provider = SentenceTransformerEmbeddingProvider(model_spec)
        texts = (
            "员工应通过人事门户提交休假申请。",
            "差旅报销需要行程单和收据。",
        )
        document_vectors = provider.embed_documents(texts)
        self.assertEqual((384, 384), tuple(len(vector) for vector in document_vectors))

        fingerprint = CollectionFingerprint(
            corpus_hash=hashlib.sha256("fixture-corpus".encode("utf-8")).hexdigest(),
            corpus_manifest_version="integration-fixture-v1",
            chunking_config_hash=hashlib.sha256("no-chunking".encode("utf-8")).hexdigest(),
            embedding_model_id=model_spec.model_id,
            embedding_revision=model_spec.revision,
            embedding_dimension=model_spec.dimension,
            normalize_embeddings=model_spec.normalize_embeddings,
            distance_metric="cosine",
            vector_schema_version="1.0",
            public_metadata_schema_version="1.0",
        )
        collection = VectorCollectionSpec(fingerprint=fingerprint.value, dimension=384)
        metadata = (
            {
                "doc_id": "doc-leave",
                "source_id": "fixture-policy",
                "source_type": "policy",
                "timestamp": "2026-07-01T00:00:00Z",
                "version": "1.0",
                "content_hash": hashlib.sha256(texts[0].encode("utf-8")).hexdigest(),
                "language": "zh",
            },
            {
                "doc_id": "doc-travel",
                "source_id": "fixture-policy",
                "source_type": "policy",
                "timestamp": "2026-07-01T00:00:00Z",
                "version": "1.0",
                "content_hash": hashlib.sha256(texts[1].encode("utf-8")).hexdigest(),
                "language": "zh",
            },
        )
        documents = tuple(
            VectorDocument(
                doc_id=item["doc_id"],
                vector=vector,
                metadata=item,
                content_hash=item["content_hash"],
                content_ref=f"chroma:{item['doc_id']}",
            )
            for item, vector in zip(metadata, document_vectors, strict=True)
        )

        with tempfile.TemporaryDirectory() as temporary_directory:
            directory = Path(temporary_directory)
            writer = ChromaVectorStore(directory)
            writer.create_or_open_collection(collection)
            writer.upsert(collection, documents)
            writer.close()

            reader = ChromaVectorStore(directory)
            info = reader.create_or_open_collection(collection)
            for question in ("员工如何申请休假？", "How should employees request leave?"):
                hits = reader.query(
                    collection,
                    VectorSearchQuery(vector=provider.embed_query(question), top_k=2),
                )
                self.assertIn("doc-leave", {hit.doc_id for hit in hits})
                self.assertTrue(
                    all("ground_truth" not in hit.metadata for hit in hits)
                )
            self.assertEqual(fingerprint.value, info.fingerprint)
            reader.close()


if __name__ == "__main__":
    unittest.main()
