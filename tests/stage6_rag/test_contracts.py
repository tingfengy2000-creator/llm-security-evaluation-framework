from __future__ import annotations

import json
import unittest
from dataclasses import FrozenInstanceError, fields

from codeguarder.stage6_rag.contracts.models import (
    DocumentRecord,
    EvidenceSignal,
    QueryRecord,
    RAGAttemptRecord,
    RAGSecurityEnvelope,
    RetrievalEvidence,
    TrustAssessment,
)
from codeguarder.stage6_rag.contracts.schemas import (
    FORBIDDEN_PIPELINE_FIELDS,
    validate_document,
    validate_document_collection,
)


def valid_document(**overrides: object) -> dict[str, object]:
    document: dict[str, object] = {
        "doc_id": "doc-1",
        "content": "A clean policy document.",
        "source_id": "source-1",
        "source_type": "policy",
        "timestamp": "2026-07-01T00:00:00Z",
        "version": "1",
        "content_hash": "a" * 64,
    }
    document.update(overrides)
    return document


def evidence() -> RetrievalEvidence:
    return RetrievalEvidence(
        query_id="query-1",
        doc_id="doc-1",
        rank=1,
        distance=0.1,
        similarity=0.9,
        source_id="source-1",
        source_type="policy",
        timestamp="2026-07-01T00:00:00Z",
        version="1",
        content_hash="a" * 64,
        content_ref="chroma:doc-1",
    )


def signal(features: dict[str, object] | None = None) -> EvidenceSignal:
    return EvidenceSignal(
        signal_type="provenance_signal",
        query_id="query-1",
        doc_ids=("doc-1",),
        value=0.75,
        features=features or {"complete": True},
        method_version="1",
        evidence_hash="b" * 64,
    )


class ModelContractTests(unittest.TestCase):
    def test_retrieval_evidence_audit_excludes_content_and_includes_doc_id(self):
        audit = evidence().to_audit_dict()

        self.assertNotIn("content", audit)
        self.assertEqual("doc-1", audit["doc_id"])
        self.assertEqual("chroma:doc-1", audit["content_ref"])

    def test_trust_assessment_observe_is_pass_through(self):
        signals = [signal()]

        assessment = TrustAssessment.observe(signals)

        self.assertEqual("observe", assessment.mode)
        self.assertIsNone(assessment.aggregate_score)
        self.assertFalse(assessment.ranking_changed)
        self.assertEqual((), assessment.blocked_doc_ids)
        self.assertEqual(tuple(signals), assessment.signals)

    def test_trust_assessment_off_has_no_signals_or_enforcement(self):
        self.assertEqual(
            TrustAssessment("off", None, False, (), ()),
            TrustAssessment.off(),
        )

    def test_all_pipeline_dataclasses_are_frozen_and_have_no_ground_truth_fields(self):
        model_types = (
            DocumentRecord,
            QueryRecord,
            RetrievalEvidence,
            EvidenceSignal,
            TrustAssessment,
            RAGAttemptRecord,
            RAGSecurityEnvelope,
        )

        for model_type in model_types:
            with self.subTest(model=model_type.__name__):
                self.assertTrue(model_type.__dataclass_params__.frozen)
                self.assertTrue(
                    FORBIDDEN_PIPELINE_FIELDS.isdisjoint(
                        field.name for field in fields(model_type)
                    )
                )

        document = DocumentRecord(**valid_document())
        with self.assertRaises(FrozenInstanceError):
            document.doc_id = "changed"

    def test_attempt_record_has_exact_semantic_fields(self):
        self.assertEqual(
            (
                "attempt_id",
                "run_id",
                "query_id",
                "attack_id",
                "guard_mode",
                "retrieval_policy",
                "retrieval_evidence",
                "evidence_signals",
                "context_hash",
                "context_length",
                "generator",
                "final_answer_hash",
                "final_answer_length",
                "detector_results",
                "metrics",
                "failure_types",
                "latency",
                "validation_status",
            ),
            tuple(field.name for field in fields(RAGAttemptRecord)),
        )

    def test_attempt_audit_serialization_is_deterministic_and_safe(self):
        first = self._attempt(
            retrieval_policy={
                "z_option": 2,
                "content": "document body",
                "a_option": {"second": 2, "first": 1},
            },
            detector_results={
                "detector": {"score": 0.2, "answer": "answer body"}
            },
            evidence_signals=(
                signal({"z": 2, "document_body": "private", "a": 1}),
            ),
        )
        second = self._attempt(
            retrieval_policy={
                "a_option": {"first": 1, "second": 2},
                "content": "document body",
                "z_option": 2,
            },
            detector_results={
                "detector": {"answer": "answer body", "score": 0.2}
            },
            evidence_signals=(
                signal({"a": 1, "document_body": "private", "z": 2}),
            ),
        )

        first_json = json.dumps(first.to_audit_dict())
        second_json = json.dumps(second.to_audit_dict())

        self.assertEqual(first_json, second_json)
        self.assertNotIn("document body", first_json)
        self.assertNotIn("answer body", first_json)
        self.assertNotIn("private", first_json)
        self.assertEqual(
            "doc-1",
            first.to_audit_dict()["retrieval_evidence"][0]["doc_id"],
        )

    def test_security_envelope_audit_serialization_is_deterministic_and_safe(self):
        first = RAGSecurityEnvelope(
            query_id="query-1",
            retrieved_doc_ids=("doc-1", "doc-2"),
            evidence_hashes=("a" * 64, "b" * 64),
            trust_signal_summary={
                "z": 2,
                "content": "document body",
                "a": {"answer": "answer body", "score": 0.5},
            },
            retrieval_policy={"top_k": 2, "method": "cosine"},
            failure_types=("T10",),
            context_hash="c" * 64,
            final_answer_hash="d" * 64,
            run_id="run-1",
        )
        second = RAGSecurityEnvelope(
            query_id="query-1",
            retrieved_doc_ids=("doc-1", "doc-2"),
            evidence_hashes=("a" * 64, "b" * 64),
            trust_signal_summary={
                "a": {"score": 0.5, "answer": "answer body"},
                "content": "document body",
                "z": 2,
            },
            retrieval_policy={"method": "cosine", "top_k": 2},
            failure_types=("T10",),
            context_hash="c" * 64,
            final_answer_hash="d" * 64,
            run_id="run-1",
        )

        first_json = json.dumps(first.to_audit_dict())

        self.assertEqual(first_json, json.dumps(second.to_audit_dict()))
        self.assertNotIn("document body", first_json)
        self.assertNotIn("answer body", first_json)
        self.assertEqual(
            ["doc-1", "doc-2"],
            first.to_audit_dict()["retrieved_doc_ids"],
        )

    @staticmethod
    def _attempt(
        *,
        retrieval_policy: dict[str, object],
        detector_results: dict[str, object],
        evidence_signals: tuple[EvidenceSignal, ...],
    ) -> RAGAttemptRecord:
        return RAGAttemptRecord(
            attempt_id="attempt-1",
            run_id="run-1",
            query_id="query-1",
            attack_id=None,
            guard_mode="observe",
            retrieval_policy=retrieval_policy,
            retrieval_evidence=(evidence(),),
            evidence_signals=evidence_signals,
            context_hash="c" * 64,
            context_length=120,
            generator={"model": "mock", "temperature": 0},
            final_answer_hash="d" * 64,
            final_answer_length=42,
            detector_results=detector_results,
            metrics={"faithfulness": {"rate": 0.5}},
            failure_types=("T10",),
            latency={"total_ms": 12.5},
            validation_status="valid",
        )


class DocumentSchemaTests(unittest.TestCase):
    def test_valid_document_is_converted_to_record(self):
        self.assertEqual(
            DocumentRecord(**valid_document()),
            validate_document(valid_document()),
        )
        self.assertEqual(
            "2026-07-01T00:00:00+00:00",
            validate_document(
                valid_document(timestamp="2026-07-01T00:00:00+00:00")
            ).timestamp,
        )

    def test_rejects_missing_required_field(self):
        document = valid_document()
        del document["source_id"]

        with self.assertRaisesRegex(ValueError, "missing required fields.*source_id"):
            validate_document(document)

    def test_rejects_forbidden_field(self):
        with self.assertRaisesRegex(ValueError, "forbidden field.*poisoned"):
            validate_document(valid_document(poisoned=True))

    def test_rejects_forbidden_nested_field(self):
        with self.assertRaisesRegex(ValueError, "forbidden field.*ground_truth"):
            validate_document(
                valid_document(metadata=[{"ground_truth": "poisoned"}])
            )

    def test_rejects_non_utc_or_invalid_timestamp(self):
        invalid_timestamps = (
            "2026-07-01T00:00:00",
            "2026-07-01T08:00:00+08:00",
            "not-a-timestamp",
        )

        for timestamp in invalid_timestamps:
            with self.subTest(timestamp=timestamp):
                with self.assertRaisesRegex(ValueError, "timestamp"):
                    validate_document(valid_document(timestamp=timestamp))

    def test_rejects_invalid_or_non_lowercase_sha256_hash(self):
        invalid_hashes = ("a" * 63, "A" * 64, "g" * 64)

        for content_hash in invalid_hashes:
            with self.subTest(content_hash=content_hash):
                with self.assertRaisesRegex(ValueError, "content_hash"):
                    validate_document(valid_document(content_hash=content_hash))

    def test_rejects_blank_id_and_required_string(self):
        for field_name in ("doc_id", "content", "source_id", "source_type", "version"):
            with self.subTest(field=field_name):
                with self.assertRaisesRegex(ValueError, field_name):
                    validate_document(valid_document(**{field_name: " \t"}))

    def test_rejects_extra_field(self):
        with self.assertRaisesRegex(ValueError, "unexpected fields.*metadata"):
            validate_document(valid_document(metadata={"owner": "security"}))

    def test_rejects_duplicate_document_ids(self):
        documents = (
            valid_document(),
            valid_document(content="Different content.", content_hash="b" * 64),
        )

        with self.assertRaisesRegex(ValueError, "duplicate doc_id.*doc-1"):
            validate_document_collection(documents)

    def test_document_collection_returns_records(self):
        documents = (
            valid_document(),
            valid_document(doc_id="doc-2", content_hash="b" * 64),
        )

        records = validate_document_collection(documents)

        self.assertIsInstance(records, tuple)
        self.assertEqual(("doc-1", "doc-2"), tuple(record.doc_id for record in records))


if __name__ == "__main__":
    unittest.main()
