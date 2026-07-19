"""Explicit-network integration coverage for the pinned Stage 6 embedding baseline."""

from __future__ import annotations

import hashlib
import math
import os
import tempfile
import unittest
from pathlib import Path


RUN_REAL_EMBEDDING_TESTS = os.getenv("LLMGUARD_RUN_REAL_EMBEDDING_TESTS") == "1"
FIXED_REVISION = "16e5344fbfc7dfbbbe0019d30cec21e2940cb4e1"
MODEL_ID = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


@unittest.skipUnless(
    RUN_REAL_EMBEDDING_TESTS,
    "set LLMGUARD_RUN_REAL_EMBEDDING_TESTS=1 to run the pinned real-model integration test",
)
class RealEmbeddingChromaIntegrationTests(unittest.TestCase):
    def test_multilingual_top_one_is_leave_policy_after_chroma_reopen(self) -> None:
        from llmguard.domains.retrieval.embedding.model_spec import EmbeddingModelSpec
        from llmguard.domains.retrieval.embedding.sentence_transformer_provider import (
            SentenceTransformerEmbeddingProvider,
        )
        from llmguard.domains.retrieval.vectorstore.chroma_store import ChromaVectorStore
        from llmguard.domains.retrieval.vectorstore.fingerprint import CollectionFingerprint
        from llmguard.domains.retrieval.vectorstore.models import (
            FORBIDDEN_METADATA_FIELDS,
            VectorCollectionSpec,
            VectorDocument,
            VectorSearchQuery,
        )

        model_spec = EmbeddingModelSpec(
            provider="sentence_transformers",
            model_id=MODEL_ID,
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
        document_texts = {
            "doc-leave": "员工请假、休假、年假或病假（leave）流程：应登录人事服务门户提交 leave request，填写请假开始日期、结束日期和休假原因，由直属主管审批。",
            "doc-travel": "员工完成出差后，应提交行程单、交通住宿发票和费用明细，发起差旅报销申请。",
            "doc-password": "员工忘记系统密码时，可在账户中心验证身份后重置密码，并重新登录企业服务。",
            "doc-archive": "项目结项后，项目负责人应整理源代码、设计文档和验收材料，提交项目归档库。",
            "doc-procurement": "采购办公设备前，申请人应填写采购申请，说明预算和用途，并等待采购审批。",
        }
        document_vectors = provider.embed_documents(tuple(document_texts.values()))
        self.assertEqual(5, len(document_vectors))
        self.assertEqual((384,) * 5, tuple(len(vector) for vector in document_vectors))
        self.assertTrue(
            all(math.isfinite(value) for vector in document_vectors for value in vector)
        )

        fingerprint = CollectionFingerprint.from_document_embedding_spec(
            corpus_hash=hashlib.sha256("integration-fixture-v2".encode("utf-8")).hexdigest(),
            corpus_manifest_version="integration-fixture-v2",
            chunking_config_hash=hashlib.sha256("no-chunking".encode("utf-8")).hexdigest(),
            document_embedding_spec=model_spec,
            distance_metric="cosine",
            vector_schema_version="1.0",
            public_metadata_schema_version="1.0",
        )
        collection = VectorCollectionSpec(fingerprint=fingerprint.value, dimension=384)
        documents = tuple(
            VectorDocument(
                doc_id=doc_id,
                vector=vector,
                metadata={
                    "doc_id": doc_id,
                    "source_id": "employee-policy-fixture",
                    "source_type": "policy",
                    "timestamp": "2026-07-01T00:00:00Z",
                    "version": "1.0",
                    "content_hash": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                    "language": "zh",
                },
                content_hash=hashlib.sha256(text.encode("utf-8")).hexdigest(),
                content_ref=f"chroma:{doc_id}",
            )
            for (doc_id, text), vector in zip(
                document_texts.items(), document_vectors, strict=True
            )
        )

        with tempfile.TemporaryDirectory() as temporary_directory:
            directory = Path(temporary_directory)
            writer = ChromaVectorStore(directory)
            try:
                writer.create_or_open_collection(collection)
                writer.upsert(collection, documents)
            finally:
                writer.close()

            reader = ChromaVectorStore(directory)
            try:
                info = reader.create_or_open_collection(collection)
                for question in (
                    "员工如何申请休假？",
                    "How should employees request leave?",
                ):
                    top_one = reader.query(
                        collection,
                        VectorSearchQuery(vector=provider.embed_query(question), top_k=1),
                    )
                    top_three = reader.query(
                        collection,
                        VectorSearchQuery(vector=provider.embed_query(question), top_k=3),
                    )

                    self.assertEqual(1, len(top_one))
                    self.assertEqual("doc-leave", top_one[0].doc_id)
                    self.assertEqual("doc-leave", top_three[0].doc_id)
                    self.assertEqual((1, 2, 3), tuple(hit.rank for hit in top_three))
                    self.assertTrue(
                        all(math.isfinite(hit.distance) for hit in top_three)
                    )
                    self.assertTrue(
                        all(math.isfinite(hit.similarity) for hit in top_three)
                    )
                    self.assertTrue(
                        all(-1.0 <= hit.similarity <= 1.0 for hit in top_three)
                    )
                    self.assertTrue(
                        all(
                            math.isclose(
                                hit.similarity,
                                max(-1.0, min(1.0, 1.0 - hit.distance)),
                                abs_tol=1e-6,
                            )
                            for hit in top_three
                        )
                    )
                    self.assertTrue(
                        all(
                            not (set(hit.metadata) & FORBIDDEN_METADATA_FIELDS)
                            for hit in top_three
                        )
                    )

                self.assertEqual(fingerprint.value, info.fingerprint)
                self.assertEqual(5, info.count)
            finally:
                reader.close()


if __name__ == "__main__":
    unittest.main()
