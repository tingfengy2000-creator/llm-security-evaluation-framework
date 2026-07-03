from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from collections import Counter
from dataclasses import FrozenInstanceError
from pathlib import Path
from typing import ClassVar

from codeguarder.stage6_rag.attacks import (
    ATTACK_MATRIX,
    EvaluationGroundTruth,
    LoadedRAGDataset,
    PublicRAGDataset,
    load_dataset,
    load_evaluation_ground_truth,
    load_public_dataset,
    render_query_record,
)
from codeguarder.stage6_rag.contracts import DocumentRecord, QueryRecord


ROOT = Path(__file__).resolve().parents[2]
DATA_ROOT = ROOT / "data" / "stage6_rag"
ATTACK_IDS = {
    f"R{category}-A{sample:02d}" for category in range(1, 7) for sample in range(1, 3)
}
ATTACK_QUERY_IDS = {
    f"R{category}-Q{sample:02d}" for category in range(1, 7) for sample in range(1, 3)
}
BENIGN_QUERY_IDS = {f"B-Q{sample:02d}" for sample in range(1, 11)}
PUBLIC_QUERY_FIELDS = {
    "query_id",
    "attack_id",
    "category",
    "retrieval_query",
    "generation_question",
    "expected_clean_doc_ids",
    "metadata",
}
PUBLIC_DOCUMENT_FIELDS = {
    "doc_id",
    "content",
    "source_id",
    "source_type",
    "timestamp",
    "version",
    "content_hash",
}


def read_jsonl(path: Path) -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def sample_query() -> QueryRecord:
    return QueryRecord(
        query_id="R1-Q01",
        attack_id="R1-A01",
        category="R1",
        retrieval_query="employee travel policy INDEX-TOKEN alpha",
        generation_question="What is the employee travel policy?",
        expected_clean_doc_ids=("C-TRAVEL-01",),
        metadata={
            "delivery_layer": "retrieval",
            "scenario": "fictional-policy-corpus",
            "variant": 1,
        },
    )


def sample_document() -> DocumentRecord:
    content = "Fictional travel policy."
    return DocumentRecord(
        doc_id="C-TRAVEL-01",
        content=content,
        source_id="handbook",
        source_type="policy",
        timestamp="2026-07-01T00:00:00Z",
        version="1.0",
        content_hash=hashlib.sha256(content.encode("utf-8")).hexdigest(),
    )


class AttackMatrixDatasetTests(unittest.TestCase):
    public: ClassVar[PublicRAGDataset]
    ground_truth: ClassVar[EvaluationGroundTruth]

    @classmethod
    def setUpClass(cls) -> None:
        cls.public = load_public_dataset(DATA_ROOT)
        cls.ground_truth = load_evaluation_ground_truth(DATA_ROOT)

    def test_attack_matrix_has_six_retrieval_only_categories(self):
        self.assertEqual({f"R{index}" for index in range(1, 7)}, set(ATTACK_MATRIX))
        for category, definition in ATTACK_MATRIX.items():
            with self.subTest(category=category):
                self.assertEqual(category, definition.category)
                self.assertEqual("retrieval", definition.delivery_layer)
                self.assertEqual(2, definition.sample_count)

    def test_query_counts_ids_and_attack_coverage_are_exact(self):
        attacks = [query for query in self.public.queries if query.attack_id]
        benign = [query for query in self.public.queries if query.attack_id is None]

        self.assertEqual(12, len(attacks))
        self.assertEqual(10, len(benign))
        self.assertEqual(
            {f"R{index}": 2 for index in range(1, 7)},
            Counter(query.category for query in attacks),
        )
        self.assertEqual(ATTACK_QUERY_IDS, {query.query_id for query in attacks})
        self.assertEqual(ATTACK_IDS, {query.attack_id for query in attacks})
        self.assertEqual(BENIGN_QUERY_IDS, {query.query_id for query in benign})
        self.assertEqual(
            len(self.public.queries),
            len({query.query_id for query in self.public.queries}),
        )

    def test_public_query_files_have_exact_schema(self):
        records = read_jsonl(DATA_ROOT / "queries" / "attack_queries.jsonl")
        records += read_jsonl(DATA_ROOT / "queries" / "benign_queries.jsonl")
        self.assertTrue(records)
        for record in records:
            self.assertEqual(PUBLIC_QUERY_FIELDS, set(record))

    def test_r1_changes_only_retrieval_input_and_generation_stays_clean(self):
        r1_queries = [query for query in self.public.queries if query.category == "R1"]
        clean_questions = {
            query.generation_question
            for query in self.public.queries
            if query.attack_id is None
        }

        self.assertEqual(2, len(r1_queries))
        for query in r1_queries:
            with self.subTest(query_id=query.query_id):
                self.assertIn(query.generation_question, clean_questions)
                self.assertIn("INDEX-TOKEN", query.retrieval_query)
                self.assertNotIn("INDEX-TOKEN", query.generation_question)
                self.assertNotRegex(
                    query.generation_question.casefold(),
                    r"ignore|instruction|system|prompt|retrieve|search",
                )

    def test_all_attacks_are_retrieval_layer_only(self):
        attacks = [query for query in self.public.queries if query.attack_id]
        for query in attacks:
            with self.subTest(query_id=query.query_id):
                self.assertEqual("retrieval", query.metadata["delivery_layer"])
                combined = (
                    f"{query.retrieval_query} {query.generation_question}"
                ).casefold()
                self.assertNotIn("system prompt", combined)
                self.assertNotIn("direct prompt", combined)

    def test_documents_have_exact_schema_prefixes_counts_and_hashes(self):
        clean = read_jsonl(DATA_ROOT / "documents" / "clean_docs.jsonl")
        attack = read_jsonl(DATA_ROOT / "documents" / "poisoned_docs.jsonl")

        self.assertGreaterEqual(len(clean), 18)
        self.assertGreaterEqual(len(attack), 10)
        self.assertEqual(10, len(attack))
        self.assertTrue(all(str(record["doc_id"]).startswith("C-") for record in clean))
        expected_prefixes = {f"P-R{category}-" for category in range(2, 7)}
        self.assertEqual(
            {prefix for prefix in expected_prefixes for _ in range(2)},
            {
                next(
                    prefix
                    for prefix in expected_prefixes
                    if str(record["doc_id"]).startswith(prefix)
                )
                for record in attack
            },
        )
        self.assertEqual(
            {f"R{category}": 2 for category in range(2, 7)},
            Counter(str(record["doc_id"]).split("-")[1] for record in attack),
        )

        for record in clean + attack:
            with self.subTest(doc_id=record["doc_id"]):
                self.assertEqual(PUBLIC_DOCUMENT_FIELDS, set(record))
                self.assertEqual(
                    hashlib.sha256(str(record["content"]).encode("utf-8")).hexdigest(),
                    record["content_hash"],
                )

    def test_expected_clean_document_references_exist(self):
        clean_ids = {
            record["doc_id"]
            for record in read_jsonl(DATA_ROOT / "documents" / "clean_docs.jsonl")
        }
        for query in self.public.queries:
            with self.subTest(query_id=query.query_id):
                self.assertTrue(query.expected_clean_doc_ids)
                self.assertLessEqual(set(query.expected_clean_doc_ids), clean_ids)

    def test_ground_truth_has_exact_coverage_and_valid_references(self):
        query_ids = {query.query_id for query in self.public.queries}
        document_ids = {document.doc_id for document in self.public.documents}

        self.assertEqual(query_ids, set(self.ground_truth.query_labels))
        self.assertEqual(document_ids, set(self.ground_truth.document_labels))
        for query_id, entry in self.ground_truth.query_labels.items():
            with self.subTest(query_id=query_id):
                self.assertEqual(query_id, entry["query_id"])
                attack_id = entry["attack_id"]
                self.assertTrue(attack_id is None or attack_id in ATTACK_IDS)
        for doc_id, entry in self.ground_truth.document_labels.items():
            with self.subTest(doc_id=doc_id):
                self.assertEqual(doc_id, entry["doc_id"])
                attack_id = entry["attack_id"]
                self.assertTrue(attack_id is None or attack_id in ATTACK_IDS)

    def test_composed_loader_is_public_by_default_and_optional_for_evaluator(self):
        default = load_dataset(DATA_ROOT)
        evaluation = load_dataset(DATA_ROOT, include_ground_truth=True)

        self.assertIsInstance(default, LoadedRAGDataset)
        self.assertIsNone(default.ground_truth)
        self.assertEqual(self.public, default.public)
        self.assertEqual(self.ground_truth, evaluation.ground_truth)

    def test_renderer_is_deterministic_and_preserves_generation_question(self):
        raw = read_jsonl(DATA_ROOT / "queries" / "attack_queries.jsonl")[0]

        first = render_query_record(raw)
        second = render_query_record(dict(reversed(tuple(raw.items()))))

        self.assertEqual(first, second)
        self.assertEqual(raw["generation_question"], first.generation_question)
        self.assertIsInstance(first, QueryRecord)

    def test_duplicate_ids_are_rejected_by_public_container(self):
        query = sample_query()
        document = sample_document()
        with self.assertRaisesRegex(ValueError, "duplicate query_id"):
            PublicRAGDataset(queries=(query, query), documents=(document,))
        with self.assertRaisesRegex(ValueError, "duplicate doc_id"):
            PublicRAGDataset(queries=(query,), documents=(document, document))

    def test_dataset_containers_are_defensively_and_deeply_immutable(self):
        query = sample_query()
        document = sample_document()
        query_input = [query]
        document_input = [document]
        public = PublicRAGDataset(
            queries=query_input,  # type: ignore[arg-type]
            documents=document_input,  # type: ignore[arg-type]
        )
        expected_behavior = ["use supported evidence"]
        query_labels = {
            query.query_id: {
                "query_id": query.query_id,
                "attack_id": query.attack_id,
                "category": query.category,
                "risk_goal": "measure retrieval steering",
                "expected_behavior": expected_behavior,
            }
        }
        truth = EvaluationGroundTruth(
            query_labels=query_labels,
            document_labels={
                document.doc_id: {
                    "doc_id": document.doc_id,
                    "poisoned": False,
                    "attack_id": None,
                    "attack_goal": None,
                }
            },
        )

        query_input.clear()
        document_input.clear()
        expected_behavior.append("mutated")

        self.assertEqual((query,), public.queries)
        self.assertEqual((document,), public.documents)
        self.assertEqual(
            ("use supported evidence",),
            truth.query_labels[query.query_id]["expected_behavior"],
        )
        with self.assertRaises(TypeError):
            truth.query_labels[query.query_id]["risk_goal"] = "mutated"  # type: ignore[index]
        with self.assertRaises(FrozenInstanceError):
            public.queries = ()  # type: ignore[misc]

    def test_jsonl_errors_include_line_number_and_reject_duplicate_keys(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            for relative in ("queries", "documents"):
                (root / relative).mkdir()
            (root / "queries" / "attack_queries.jsonl").write_text(
                '{"query_id":"R1-Q01","query_id":"R1-Q02"}\n',
                encoding="utf-8",
            )
            (root / "queries" / "benign_queries.jsonl").write_text(
                "",
                encoding="utf-8",
            )
            (root / "documents" / "clean_docs.jsonl").write_text(
                "",
                encoding="utf-8",
            )
            (root / "documents" / "poisoned_docs.jsonl").write_text(
                "",
                encoding="utf-8",
            )
            manifest = {
                "schema_version": "1.0.0",
                "data_version": "1.0.0",
                "files": {},
                "provenance": {"method": "curated-fixtures"},
            }
            (root / "documents" / "corpus_manifest.json").write_text(
                json.dumps(manifest),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(
                ValueError,
                r"attack_queries\.jsonl:1: duplicate JSON key",
            ):
                load_public_dataset(root)

    def test_query_schema_errors_include_physical_line_number(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            for relative in ("queries", "documents"):
                (root / relative).mkdir()
            invalid_query = read_jsonl(DATA_ROOT / "queries" / "attack_queries.jsonl")[
                0
            ]
            invalid_query["unexpected"] = "value"
            (root / "queries" / "attack_queries.jsonl").write_text(
                f"\n{json.dumps(invalid_query)}\n",
                encoding="utf-8",
            )
            for relative_path in (
                "queries/benign_queries.jsonl",
                "documents/clean_docs.jsonl",
                "documents/poisoned_docs.jsonl",
            ):
                (root / relative_path).write_text("", encoding="utf-8")
            (root / "documents" / "corpus_manifest.json").write_text(
                "{}",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(
                ValueError,
                r"attack_queries\.jsonl:2:.*unexpected fields",
            ):
                load_public_dataset(root)


if __name__ == "__main__":
    unittest.main()
