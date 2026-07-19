from __future__ import annotations

import unittest

from llmguard.domains.retrieval.embedding.model_spec import (
    EmbeddingConfigurationError,
    EmbeddingModelSpec,
)


FIXED_REVISION = "16e5344fbfc7dfbbbe0019d30cec21e2940cb4e1"


def make_spec(**overrides: object) -> EmbeddingModelSpec:
    values: dict[str, object] = {
        "provider": "sentence_transformers",
        "model_id": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        "revision": FIXED_REVISION,
        "dimension": 384,
        "normalize_embeddings": True,
        "device": "cpu",
        "batch_size": 16,
        "trust_remote_code": False,
        "local_files_only": True,
        "implementation_version": "s6_t4_v1",
    }
    values.update(overrides)
    return EmbeddingModelSpec(**values)  # type: ignore[arg-type]


class EmbeddingModelSpecTests(unittest.TestCase):
    def test_canonical_serialization_and_hash_ignore_local_cache_reference(self) -> None:
        left = make_spec(cache_dir_ref="local-cache-a")
        right = make_spec(cache_dir_ref="local-cache-b")
        windows_prefix = "C:" + chr(92)
        unix_prefix = "/" + "home" + "/"

        self.assertEqual(left.canonical_json(), right.canonical_json())
        self.assertEqual(left.fingerprint(), right.fingerprint())
        self.assertNotIn("cache_dir_ref", left.canonical_json())
        self.assertNotIn(windows_prefix, left.canonical_json())
        self.assertNotIn(unix_prefix, left.canonical_json())
        self.assertEqual(64, len(left.fingerprint()))

    def test_document_fingerprint_excludes_query_only_prefix(self) -> None:
        baseline = make_spec(query_prefix="query: ")
        query_prefix_changed = make_spec(query_prefix="search_query: ")
        document_prefix_changed = make_spec(document_prefix="passage: ")

        self.assertNotEqual(baseline.fingerprint(), query_prefix_changed.fingerprint())
        self.assertEqual(
            baseline.fingerprint(scope="document"),
            query_prefix_changed.fingerprint(scope="document"),
        )
        self.assertNotEqual(
            baseline.fingerprint(scope="document"),
            document_prefix_changed.fingerprint(scope="document"),
        )

    def test_rejects_mutable_revision_and_unsafe_remote_code(self) -> None:
        with self.assertRaisesRegex(EmbeddingConfigurationError, "revision"):
            make_spec(revision="main")
        with self.assertRaisesRegex(EmbeddingConfigurationError, "trust_remote_code"):
            make_spec(trust_remote_code=True)

    def test_rejects_invalid_dimensions_batch_and_absolute_cache_reference(self) -> None:
        for field, value in (("dimension", 0), ("batch_size", 0)):
            with self.subTest(field=field):
                with self.assertRaises(EmbeddingConfigurationError):
                    make_spec(**{field: value})

        windows_cache_ref = "C:" + chr(92) + "model-cache"
        with self.assertRaisesRegex(EmbeddingConfigurationError, "cache_dir_ref"):
            make_spec(cache_dir_ref=windows_cache_ref)

    def test_is_immutable(self) -> None:
        spec = make_spec()
        with self.assertRaisesRegex(AttributeError, "cannot assign"):
            spec.dimension = 512  # type: ignore[misc]


if __name__ == "__main__":
    unittest.main()
