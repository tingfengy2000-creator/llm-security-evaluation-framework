from __future__ import annotations

import hashlib
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
    REQUIRED_DOCUMENT_FIELDS,
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

    def test_all_pipeline_dataclasses_are_frozen_and_have_exact_fields(self):
        expected_fields = {
            DocumentRecord: (
                "doc_id",
                "content",
                "source_id",
                "source_type",
                "timestamp",
                "version",
                "content_hash",
            ),
            QueryRecord: (
                "query_id",
                "attack_id",
                "category",
                "retrieval_query",
                "generation_question",
                "expected_clean_doc_ids",
                "metadata",
            ),
            RetrievalEvidence: (
                "query_id",
                "doc_id",
                "rank",
                "distance",
                "similarity",
                "source_id",
                "source_type",
                "timestamp",
                "version",
                "content_hash",
                "content_ref",
            ),
            EvidenceSignal: (
                "signal_type",
                "query_id",
                "doc_ids",
                "value",
                "features",
                "method_version",
                "evidence_hash",
            ),
            TrustAssessment: (
                "mode",
                "aggregate_score",
                "ranking_changed",
                "blocked_doc_ids",
                "signals",
            ),
            RAGAttemptRecord: (
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
            RAGSecurityEnvelope: (
                "query_id",
                "retrieved_doc_ids",
                "evidence_hashes",
                "trust_signal_summary",
                "retrieval_policy",
                "failure_types",
                "context_hash",
                "final_answer_hash",
                "run_id",
            ),
        }

        for model_type, expected in expected_fields.items():
            with self.subTest(model=model_type.__name__):
                self.assertTrue(model_type.__dataclass_params__.frozen)
                self.assertEqual(
                    expected,
                    tuple(field.name for field in fields(model_type)),
                )
                self.assertTrue(
                    FORBIDDEN_PIPELINE_FIELDS.isdisjoint(
                        field.name for field in fields(model_type)
                    )
                )

        document = DocumentRecord(**valid_document())
        with self.assertRaises(FrozenInstanceError):
            document.doc_id = "changed"

    def test_query_record_rejects_nested_ground_truth_metadata(self):
        safe_query = QueryRecord(
            query_id="query-1",
            attack_id=None,
            category="benign",
            retrieval_query="policy",
            generation_question="What is the policy?",
            expected_clean_doc_ids=("doc-1",),
            metadata={"source": "fixture", "tags": ["clean"]},
        )
        self.assertEqual("fixture", safe_query.metadata["source"])

        with self.assertRaisesRegex(ValueError, "forbidden field.*ground_truth"):
            QueryRecord(
                query_id="query-2",
                attack_id=None,
                category="benign",
                retrieval_query="policy",
                generation_question="What is the policy?",
                expected_clean_doc_ids=("doc-1",),
                metadata={"nested": [{"ground_truth": "clean"}]},
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

    def test_attempt_audit_fingerprints_body_aliases_and_keeps_metadata(self):
        sentinels = {
            "raw_response": "RAW RESPONSE SENTINEL",
            "text": "TEXT SENTINEL",
            "document_text": "DOCUMENT TEXT SENTINEL",
            "prompt": "PROMPT SENTINEL",
            "messages": "MESSAGES SENTINEL",
        }
        attempt = self._attempt(
            retrieval_policy={
                "model_name": "retriever-v1",
                "nested": {
                    "RAW-Response": sentinels["raw_response"],
                    "Document.Text": sentinels["document_text"],
                },
            },
            detector_results={
                "detector_source": "guard",
                "score": 0.8,
                "TeXt": sentinels["text"],
                "deeper": [
                    {"Prompt": sentinels["prompt"]},
                    {"MESSAGES": sentinels["messages"]},
                ],
            },
            evidence_signals=(signal(),),
        )

        audit = attempt.to_audit_dict()
        serialized = json.dumps(audit)

        for sentinel in sentinels.values():
            self.assertNotIn(sentinel, serialized)
        self.assertEqual("retriever-v1", audit["retrieval_policy"]["model_name"])
        self.assertEqual("guard", audit["detector_results"]["detector_source"])
        self.assertEqual(0.8, audit["detector_results"]["score"])
        self.assertEqual(
            {
                "sha256": hashlib.sha256(
                    sentinels["raw_response"].encode("utf-8")
                ).hexdigest(),
                "length": len(sentinels["raw_response"]),
            },
            audit["retrieval_policy"]["nested"]["RAW-Response"],
        )

    def test_attempt_audit_rejects_non_json_set_values(self):
        attempt = self._attempt(
            retrieval_policy={"top_k": 2},
            detector_results={"score": 0.8},
            evidence_signals=(signal(),),
            metrics={"sample_ids": {"sample-2", "sample-1"}},
        )

        with self.assertRaisesRegex(TypeError, "unsupported audit value type: set"):
            attempt.to_audit_dict()

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

    def test_security_envelope_fingerprints_nested_body_aliases(self):
        sentinels = (
            "OUTPUT SENTINEL",
            "CONTEXT SENTINEL",
            "DOCUMENT SENTINEL",
        )
        envelope = RAGSecurityEnvelope(
            query_id="query-1",
            retrieved_doc_ids=("doc-1",),
            evidence_hashes=("a" * 64,),
            trust_signal_summary={
                "detector_source": "trust-engine",
                "score": 0.6,
                "nested": {
                    "OUTPUT": sentinels[0],
                    "Con.Text": sentinels[1],
                    "documents": [{"body": sentinels[2]}],
                },
            },
            retrieval_policy={"model_name": "retriever-v1"},
            failure_types=(),
            context_hash="c" * 64,
            final_answer_hash="d" * 64,
            run_id="run-1",
        )

        audit = envelope.to_audit_dict()
        serialized = json.dumps(audit)

        for sentinel in sentinels:
            self.assertNotIn(sentinel, serialized)
        self.assertEqual(
            "trust-engine",
            audit["trust_signal_summary"]["detector_source"],
        )
        self.assertEqual(0.6, audit["trust_signal_summary"]["score"])
        self.assertEqual("retriever-v1", audit["retrieval_policy"]["model_name"])

    @staticmethod
    def _attempt(
        *,
        retrieval_policy: dict[str, object],
        detector_results: dict[str, object],
        evidence_signals: tuple[EvidenceSignal, ...],
        metrics: dict[str, object] | None = None,
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
            metrics=(
                metrics
                if metrics is not None
                else {"faithfulness": {"rate": 0.5}}
            ),
            failure_types=("T10",),
            latency={"total_ms": 12.5},
            validation_status="valid",
        )


class DocumentSchemaTests(unittest.TestCase):
    def test_schema_field_sets_are_exact(self):
        self.assertEqual(
            {
                "doc_id",
                "content",
                "source_id",
                "source_type",
                "timestamp",
                "version",
                "content_hash",
            },
            REQUIRED_DOCUMENT_FIELDS,
        )
        self.assertEqual(
            {
                "poisoned",
                "label",
                "attack_goal",
                "expected_answer",
                "failure_type",
                "ground_truth",
            },
            FORBIDDEN_PIPELINE_FIELDS,
        )

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
            "2026-07-01X00:00:00Z",
            "2026-07-01 00:00:00Z",
            "2026-07-01t00:00:00Z",
            "not-a-timestamp",
        )

        for timestamp in invalid_timestamps:
            with self.subTest(timestamp=timestamp):
                with self.assertRaisesRegex(ValueError, "timestamp"):
                    validate_document(valid_document(timestamp=timestamp))

    def test_accepts_canonical_utc_timestamp_forms(self):
        timestamps = (
            "2026-07-01T00:00:00Z",
            "2026-07-01T00:00:00.123456Z",
            "2026-07-01T00:00:00+00:00",
            "2026-07-01T00:00:00.5+00:00",
        )

        for timestamp in timestamps:
            with self.subTest(timestamp=timestamp):
                self.assertEqual(
                    timestamp,
                    validate_document(valid_document(timestamp=timestamp)).timestamp,
                )

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
