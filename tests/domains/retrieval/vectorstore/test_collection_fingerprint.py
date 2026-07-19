from __future__ import annotations

import unittest

from llmguard.domains.retrieval.embedding.model_spec import EmbeddingModelSpec
from llmguard.domains.retrieval.vectorstore.fingerprint import CollectionFingerprint


FIXED_REVISION = "16e5344fbfc7dfbbbe0019d30cec21e2940cb4e1"


def make_embedding_spec(**overrides: object) -> EmbeddingModelSpec:
    values: dict[str, object] = {
        "provider": "llmguard_static",
        "model_id": "llmguard/static-fixture",
        "revision": FIXED_REVISION,
        "dimension": 3,
        "normalize_embeddings": True,
        "device": "cpu",
        "batch_size": 16,
        "trust_remote_code": False,
        "local_files_only": True,
        "implementation_version": "s6_t4_v1",
    }
    values.update(overrides)
    return EmbeddingModelSpec(**values)  # type: ignore[arg-type]


def make_fingerprint(**overrides: object) -> CollectionFingerprint:
    values: dict[str, object] = {
        "corpus_hash": "a" * 64,
        "corpus_manifest_version": "1.0.1",
        "chunking_config_hash": "b" * 64,
        "document_embedding_spec": make_embedding_spec(),
        "distance_metric": "cosine",
        "vector_schema_version": "1.0",
        "public_metadata_schema_version": "1.0",
    }
    values.update(overrides)
    document_embedding_spec = values.pop("document_embedding_spec")
    return CollectionFingerprint.from_document_embedding_spec(
        document_embedding_spec=document_embedding_spec,  # type: ignore[arg-type]
        **values,  # type: ignore[arg-type]
    )


class CollectionFingerprintTests(unittest.TestCase):
    def test_canonical_hash_is_stable_and_contains_no_machine_path(self) -> None:
        left = make_fingerprint()
        right = make_fingerprint()
        windows_prefix = "C:" + chr(92)
        unix_prefix = "/" + "home" + "/"

        self.assertEqual(left.value, right.value)
        self.assertEqual(left.canonical_json(), right.canonical_json())
        self.assertEqual(64, len(left.value))
        self.assertNotIn(windows_prefix, left.canonical_json())
        self.assertNotIn(unix_prefix, left.canonical_json())

    def test_each_semantic_component_changes_the_fingerprint(self) -> None:
        baseline = make_fingerprint().value
        changes = (
            {"corpus_hash": "c" * 64},
            {"document_embedding_spec": make_embedding_spec(provider="other")},
            {"document_embedding_spec": make_embedding_spec(model_id="other/model")},
            {"document_embedding_spec": make_embedding_spec(revision="f" * 40)},
            {"document_embedding_spec": make_embedding_spec(dimension=4)},
            {"document_embedding_spec": make_embedding_spec(normalize_embeddings=False)},
            {"document_embedding_spec": make_embedding_spec(document_prefix="passage: ")},
            {"document_embedding_spec": make_embedding_spec(expected_output_dtype="float16")},
            {"document_embedding_spec": make_embedding_spec(implementation_version="s6_t4_v2")},
            {"distance_metric": "l2"},
        )

        for change in changes:
            with self.subTest(change=change):
                self.assertNotEqual(baseline, make_fingerprint(**change).value)

    def test_query_prefix_does_not_change_document_collection_fingerprint(self) -> None:
        first = make_fingerprint(document_embedding_spec=make_embedding_spec(query_prefix="query: "))
        second = make_fingerprint(
            document_embedding_spec=make_embedding_spec(query_prefix="different_query: ")
        )

        self.assertEqual(first.value, second.value)


if __name__ == "__main__":
    unittest.main()
