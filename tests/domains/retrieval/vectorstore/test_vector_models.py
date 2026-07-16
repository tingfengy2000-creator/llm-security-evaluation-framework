from __future__ import annotations

import math
import unittest

from llmguard.domains.retrieval.vectorstore.models import (
    MetadataIsolationError,
    VectorDocument,
    VectorSearchHit,
)


CONTENT_HASH = "a" * 64


def allowed_metadata(doc_id: str = "doc-1") -> dict[str, object]:
    return {
        "doc_id": doc_id,
        "source_id": "source-1",
        "source_type": "policy",
        "timestamp": "2026-07-01T00:00:00Z",
        "version": "1.0",
        "content_hash": CONTENT_HASH,
        "language": "zh",
    }


class VectorModelTests(unittest.TestCase):
    def test_vector_document_freezes_allowlisted_metadata(self) -> None:
        document = VectorDocument(
            doc_id="doc-1",
            vector=(1.0, 0.0, 0.0),
            metadata=allowed_metadata(),
            content_hash=CONTENT_HASH,
            content_ref="chroma:doc-1",
        )

        self.assertEqual("doc-1", document.metadata["doc_id"])
        with self.assertRaises(TypeError):
            document.metadata["source_id"] = "changed"  # type: ignore[index]

    def test_metadata_rejects_evaluator_labels_and_unknown_fields(self) -> None:
        for forbidden in (
            "poisoned",
            "poison_label",
            "label",
            "attack_id",
            "attack_goal",
            "attack_category",
            "expected_answer",
            "expected_behavior",
            "failure_type",
            "ground_truth",
            "oracle",
            "risk_goal",
            "stealth_level",
            "unapproved",
        ):
            with self.subTest(forbidden=forbidden):
                metadata = allowed_metadata()
                metadata[forbidden] = "value"
                with self.assertRaises(MetadataIsolationError):
                    VectorDocument(
                        doc_id="doc-1",
                        vector=(1.0, 0.0, 0.0),
                        metadata=metadata,
                        content_hash=CONTENT_HASH,
                        content_ref="chroma:doc-1",
                    )

    def test_vectors_and_search_hits_reject_non_finite_values(self) -> None:
        for value in (math.nan, math.inf, -math.inf):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    VectorDocument(
                        doc_id="doc-1",
                        vector=(1.0, value),
                        metadata=allowed_metadata(),
                        content_hash=CONTENT_HASH,
                        content_ref="chroma:doc-1",
                    )

        with self.assertRaises(ValueError):
            VectorSearchHit(
                doc_id="doc-1",
                distance=math.nan,
                similarity=0.0,
                metadata=allowed_metadata(),
                rank=1,
            )


if __name__ == "__main__":
    unittest.main()
