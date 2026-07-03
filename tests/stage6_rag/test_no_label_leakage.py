from __future__ import annotations

import hashlib
import json
import re
import unicodedata
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import patch

from codeguarder.stage6_rag.attacks import load_public_dataset


ROOT = Path(__file__).resolve().parents[2]
DATA_ROOT = ROOT / "data" / "stage6_rag"
PUBLIC_FILES = (
    DATA_ROOT / "queries" / "attack_queries.jsonl",
    DATA_ROOT / "queries" / "benign_queries.jsonl",
    DATA_ROOT / "documents" / "clean_docs.jsonl",
    DATA_ROOT / "documents" / "poisoned_docs.jsonl",
    DATA_ROOT / "documents" / "corpus_manifest.json",
)
FORBIDDEN = {
    "poisoned",
    "label",
    "attack_goal",
    "expected_answer",
    "failure_type",
    "ground_truth",
}


def normalize_field_name(value: str) -> str:
    return re.sub(
        r"[^a-z0-9]+",
        "",
        unicodedata.normalize("NFKC", value).casefold(),
    )


NORMALIZED_FORBIDDEN = {normalize_field_name(field) for field in FORBIDDEN}


def walk_keys(value: object, path: str = "$"):
    if isinstance(value, dict):
        for key, nested in value.items():
            yield path, key
            yield from walk_keys(nested, f"{path}.{key}")
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            yield from walk_keys(nested, f"{path}[{index}]")


def read_public_values(path: Path) -> list[object]:
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".jsonl":
        return [json.loads(line) for line in text.splitlines() if line.strip()]
    return [json.loads(text)]


class LabelIsolationTests(unittest.TestCase):
    def test_public_files_recursively_exclude_forbidden_field_variants(self):
        for public_file in PUBLIC_FILES:
            for value in read_public_values(public_file):
                for path, key in walk_keys(value):
                    with self.subTest(file=public_file.name, path=path, key=key):
                        self.assertNotIn(
                            normalize_field_name(key),
                            NORMALIZED_FORBIDDEN,
                        )

    def test_public_loader_never_opens_ground_truth_paths(self):
        original_open = Path.open
        opened_paths: list[Path] = []

        def guarded_open(path: Path, *args: Any, **kwargs: Any) -> Any:
            resolved = Path(path)
            opened_paths.append(resolved)
            if "ground_truth" in resolved.parts:
                raise AssertionError("public loader accessed evaluator data")
            return original_open(path, *args, **kwargs)

        with patch.object(Path, "open", guarded_open):
            dataset = load_public_dataset(DATA_ROOT)

        self.assertEqual(22, len(dataset.queries))
        self.assertTrue(opened_paths)
        self.assertFalse(any("ground_truth" in path.parts for path in opened_paths))

    def test_manifest_hashes_and_counts_match_physical_public_files(self):
        manifest_path = DATA_ROOT / "documents" / "corpus_manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        expected_paths = {
            "queries/attack_queries.jsonl",
            "queries/benign_queries.jsonl",
            "documents/clean_docs.jsonl",
            "documents/poisoned_docs.jsonl",
        }

        self.assertEqual("1.0.0", manifest["schema_version"])
        self.assertEqual("1.0.0", manifest["data_version"])
        self.assertEqual(expected_paths, set(manifest["files"]))
        self.assertEqual(
            {"method", "created_at", "content_scope"},
            set(manifest["provenance"]),
        )
        for relative_path, entry in manifest["files"].items():
            with self.subTest(relative_path=relative_path):
                physical_path = DATA_ROOT / relative_path
                content = physical_path.read_bytes()
                line_count = sum(
                    1 for line in content.decode("utf-8").splitlines() if line.strip()
                )
                self.assertEqual(
                    hashlib.sha256(content).hexdigest(),
                    entry["sha256"],
                )
                self.assertEqual(line_count, entry["count"])
                self.assertEqual({"sha256", "count"}, set(entry))

    def test_ground_truth_is_physically_separate_from_public_files(self):
        query_labels = DATA_ROOT / "ground_truth" / "query_labels.jsonl"
        document_labels = DATA_ROOT / "ground_truth" / "document_labels.jsonl"

        self.assertTrue(query_labels.is_file())
        self.assertTrue(document_labels.is_file())
        self.assertNotIn(query_labels, PUBLIC_FILES)
        self.assertNotIn(document_labels, PUBLIC_FILES)
        self.assertIn("risk_goal", query_labels.read_text(encoding="utf-8"))
        self.assertIn("poisoned", document_labels.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
