from __future__ import annotations

import unittest

from llmguard.domains.retrieval.vectorstore.fingerprint import CollectionFingerprint


def make_fingerprint(**overrides: object) -> CollectionFingerprint:
    values: dict[str, object] = {
        "corpus_hash": "a" * 64,
        "corpus_manifest_version": "1.0.1",
        "chunking_config_hash": "b" * 64,
        "embedding_model_id": "llmguard/static-fixture",
        "embedding_revision": "16e5344fbfc7dfbbbe0019d30cec21e2940cb4e1",
        "embedding_dimension": 3,
        "normalize_embeddings": True,
        "distance_metric": "cosine",
        "vector_schema_version": "1.0",
        "public_metadata_schema_version": "1.0",
    }
    values.update(overrides)
    return CollectionFingerprint(**values)  # type: ignore[arg-type]


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
            {"embedding_revision": "f" * 40},
            {"embedding_dimension": 4},
            {"normalize_embeddings": False},
            {"distance_metric": "l2"},
        )

        for change in changes:
            with self.subTest(change=change):
                self.assertNotEqual(baseline, make_fingerprint(**change).value)


if __name__ == "__main__":
    unittest.main()
