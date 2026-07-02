from __future__ import annotations

import json
import unittest
from dataclasses import FrozenInstanceError, fields

from codeguarder.stage6_rag.contracts import models as contract_models
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


def signal(
    features: dict[str, object] | None = None,
    *,
    signal_type: str = "provenance_signal",
) -> EvidenceSignal:
    return EvidenceSignal(
        signal_type=signal_type,
        query_id="query-1",
        doc_ids=("doc-1",),
        value=0.75,
        features=features if features is not None else {"source_count": 1},
        method_version="1",
        evidence_hash="b" * 64,
    )


class ModelContractTests(unittest.TestCase):
    def test_retrieval_evidence_audit_excludes_content_and_includes_doc_id(self):
        audit = evidence().to_audit_dict()

        self.assertNotIn("content", audit)
        self.assertEqual("doc-1", audit["doc_id"])
        self.assertEqual("chroma:doc-1", audit["content_ref"])

    def test_retrieval_evidence_accepts_planned_chroma_references(self):
        references = (
            "chroma:d1",
            "chroma:policies:doc-1",
            "chroma:collection_1:doc.v2",
        )

        for content_ref in references:
            with self.subTest(content_ref=content_ref):
                item = RetrievalEvidence(
                    **{
                        **evidence().__dict__,
                        "content_ref": content_ref,
                    }
                )
                self.assertEqual(content_ref, item.content_ref)

    def test_retrieval_evidence_rejects_body_text_and_invalid_references(self):
        invalid_references = (
            "RAW_DOCUMENT_BODY_DO_NOT_AUDIT",
            "chroma:document body",
            "chroma:collection:doc:extra",
            "chroma:集合:doc-1",
            f"chroma:{'a' * 250}",
        )

        for content_ref in invalid_references:
            with self.subTest(content_ref=content_ref):
                with self.assertRaisesRegex(ValueError, "content_ref"):
                    RetrievalEvidence(
                        **{
                            **evidence().__dict__,
                            "content_ref": content_ref,
                        }
                    )

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

    def test_trust_assessment_direct_observe_allows_signals(self):
        item = signal()

        assessment = TrustAssessment(
            "observe",
            None,
            False,
            [],
            [item],
        )

        self.assertEqual((), assessment.blocked_doc_ids)
        self.assertEqual((item,), assessment.signals)

    def test_trust_assessment_rejects_non_stage6_modes(self):
        for mode in ("enforce", "audit", ""):
            with self.subTest(mode=mode):
                with self.assertRaisesRegex(ValueError, "mode"):
                    TrustAssessment(mode, None, False, (), ())

    def test_trust_assessment_rejects_pass_through_invariant_violations(self):
        violations = (
            ("off", 0.5, False, (), ()),
            ("off", None, True, (), ()),
            ("off", None, False, ("doc-1",), ()),
            ("off", None, False, (), (signal(),)),
            ("observe", 0.5, False, (), ()),
            ("observe", None, True, (), ()),
            ("observe", None, False, ("doc-1",), ()),
        )

        for violation in violations:
            with self.subTest(assessment=violation):
                with self.assertRaises(ValueError):
                    TrustAssessment(*violation)

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

    def test_field_specific_audit_allowlists_are_exact_and_immutable(self):
        expected_allowlists = {
            "generator": (
                "GENERATOR_AUDIT_KEYS",
                {
                    "provider",
                    "model",
                    "model_name",
                    "seed",
                    "temperature",
                    "max_tokens",
                    "revision",
                },
            ),
            "detector_results": (
                "DETECTOR_RESULT_AUDIT_KEYS",
                {
                    "detector_id",
                    "detector_name",
                    "detector_source",
                    "passed",
                    "score",
                    "matched",
                    "rule_ids",
                    "output_hash",
                    "output_length",
                    "method_version",
                },
            ),
            "metrics": (
                "METRICS_AUDIT_KEYS",
                {
                    "rpr",
                    "cir",
                    "rmsr",
                    "faithfulness",
                    "cross_layer_leakage",
                    "retrieval_poison_rate",
                    "context_injection_rate",
                    "retrieval_manipulation_success_rate",
                    "cross_layer_leakage_rate",
                },
            ),
            "latency": (
                "LATENCY_AUDIT_KEYS",
                {
                    "retrieval_ms",
                    "evidence_ms",
                    "trust_ms",
                    "context_ms",
                    "generation_ms",
                    "evaluation_ms",
                    "total_ms",
                },
            ),
            "validation_status": (
                "VALIDATION_STATUS_AUDIT_KEYS",
                {
                    "status",
                    "valid",
                    "issue_codes",
                    "method_version",
                },
            ),
            "trust_signal_summary": (
                "TRUST_SIGNAL_SUMMARY_AUDIT_KEYS",
                {
                    "signal_count",
                    "signal_types",
                    "method_versions",
                    "evidence_hashes",
                    "aggregate_score",
                    "ranking_changed",
                    "blocked_doc_ids",
                },
            ),
        }

        for field_name, (constant_name, expected) in expected_allowlists.items():
            with self.subTest(field_name=field_name):
                actual = getattr(contract_models, constant_name, None)
                self.assertEqual(expected, actual)
                with self.assertRaises(AttributeError):
                    actual.add("document_text")

    def test_evidence_feature_allowlists_are_exact_and_immutable(self):
        self.assertEqual(
            {
                "provenance_signal": frozenset(
                    {
                        "source_id",
                        "source_type",
                        "timestamp",
                        "version",
                        "content_hash",
                        "source_count",
                        "document_count",
                        "age_days",
                    }
                ),
                "embedding_anomaly_signal": frozenset(
                    {
                        "rank",
                        "distance",
                        "similarity",
                        "mean_distance",
                        "std_distance",
                        "z_score",
                        "top_k",
                    }
                ),
                "semantic_conflict_signal": frozenset(
                    {
                        "pair_count",
                        "conflict_count",
                        "max_conflict_score",
                        "mean_conflict_score",
                        "compared_doc_ids",
                    }
                ),
                "source_diversity_signal": frozenset(
                    {
                        "source_count",
                        "document_count",
                        "diversity_ratio",
                        "source_types",
                    }
                ),
            },
            contract_models.EVIDENCE_FEATURE_ALLOWLISTS,
        )
        with self.assertRaises(TypeError):
            contract_models.EVIDENCE_FEATURE_ALLOWLISTS[
                "provenance_signal"
            ] = frozenset(
                {"document_text"}
            )
        with self.assertRaises(AttributeError):
            contract_models.EVIDENCE_FEATURE_ALLOWLISTS[
                "provenance_signal"
            ].add(
                "unexpected_feature"
            )

    def test_query_record_deep_freezes_caller_metadata(self):
        tags = ["clean"]
        labels = {"public"}
        nested = {"tags": tags, "labels": labels}
        metadata = {"source": "fixture", "nested": nested}
        query = QueryRecord(
            query_id="query-1",
            attack_id=None,
            category="benign",
            retrieval_query="policy",
            generation_question="What is the policy?",
            expected_clean_doc_ids=("doc-1",),
            metadata=metadata,
        )

        metadata["source"] = "mutated"
        nested["added"] = True
        tags.append("mutated")
        labels.add("private")

        self.assertEqual("fixture", query.metadata["source"])
        self.assertEqual(
            {"labels": ("public",), "tags": ("clean",)},
            dict(query.metadata["nested"]),
        )
        with self.assertRaises(TypeError):
            query.metadata["source"] = "blocked"

    def test_query_record_rejects_normalized_forbidden_metadata_keys(self):
        forbidden_variants = (
            "Ground_Truth",
            "ground-truth",
            "GROUND TRUTH",
            "Poisoned",
            "LABEL",
            "attack-goal",
            "expected answer",
            "failure.type",
        )

        for key in forbidden_variants:
            with self.subTest(key=key):
                with self.assertRaisesRegex(ValueError, "forbidden field"):
                    QueryRecord(
                        query_id="query-1",
                        attack_id=None,
                        category="benign",
                        retrieval_query="policy",
                        generation_question="What is the policy?",
                        expected_clean_doc_ids=("doc-1",),
                        metadata={"nested": [{key: "label"}]},
                    )

    def test_evidence_signal_deep_freezes_features(self):
        source_types = ["policy"]
        features = {"source_count": 1, "source_types": source_types}
        item = signal(features, signal_type="source_diversity_signal")

        features["source_count"] = 0
        source_types.append("mutated")

        self.assertEqual(1, item.features["source_count"])
        self.assertEqual(("policy",), item.features["source_types"])
        with self.assertRaises(TypeError):
            item.features["new"] = True

    def test_evidence_signal_rejects_unknown_signal_type(self):
        with self.assertRaisesRegex(ValueError, "unknown signal_type"):
            signal({"source_count": 1}, signal_type="future_signal")

    def test_evidence_signal_rejects_body_aliases_and_ground_truth_variants(self):
        forbidden_feature_keys = (
            "Completion",
            "assistant_reply",
            "result",
            "payload",
            "raw_response",
            "text",
            "document_text",
            "Ground_Truth",
            "ground-truth",
            "GROUND TRUTH",
        )

        for key in forbidden_feature_keys:
            with self.subTest(key=key):
                with self.assertRaisesRegex(
                    ValueError,
                    "unknown keys|forbidden field",
                ):
                    signal({key: "secret"})

    def test_evidence_signal_rejects_nested_body_aliases_at_construction(self):
        signal_features = {
            "provenance_signal": "source_id",
            "embedding_anomaly_signal": "rank",
            "semantic_conflict_signal": "pair_count",
            "source_diversity_signal": "source_count",
        }

        for signal_type, feature_name in signal_features.items():
            with self.subTest(signal_type=signal_type):
                with self.assertRaisesRegex(ValueError, "nested mappings"):
                    signal(
                        {
                            feature_name: {
                                "document_text": "secret",
                            }
                        },
                        signal_type=signal_type,
                    )

    def test_evidence_signal_supports_exact_features_for_all_signal_types(self):
        feature_contracts = {
            "provenance_signal": {
                "source_id": "source-1",
                "source_type": "policy",
                "timestamp": "2026-07-01T00:00:00Z",
                "version": "1",
                "content_hash": "a" * 64,
                "source_count": 2,
                "document_count": 3,
                "age_days": 0.5,
            },
            "embedding_anomaly_signal": {
                "rank": 1,
                "distance": 0.1,
                "similarity": 0.9,
                "mean_distance": 0.2,
                "std_distance": 0.05,
                "z_score": -2.0,
                "top_k": 5,
            },
            "semantic_conflict_signal": {
                "pair_count": 3,
                "conflict_count": 1,
                "max_conflict_score": 0.8,
                "mean_conflict_score": 0.4,
                "compared_doc_ids": ("doc-1", "doc-2"),
            },
            "source_diversity_signal": {
                "source_count": 2,
                "document_count": 3,
                "diversity_ratio": 2 / 3,
                "source_types": ("policy", "wiki"),
            },
        }

        for signal_type, features in feature_contracts.items():
            with self.subTest(signal_type=signal_type):
                first = signal(features, signal_type=signal_type)
                second = signal(
                    dict(reversed(tuple(features.items()))),
                    signal_type=signal_type,
                )

                first_audit = first.to_audit_dict()
                second_audit = second.to_audit_dict()

                self.assertEqual(
                    json.dumps(first_audit),
                    json.dumps(second_audit),
                )
                self.assertEqual(
                    sorted(features),
                    list(first_audit["features"]),
                )
                expected_features = {
                    key: (
                        list(value)
                        if isinstance(value, tuple)
                        else value
                    )
                    for key, value in features.items()
                }
                self.assertEqual(expected_features, first_audit["features"])

    def test_attempt_audit_rejects_transitive_unknown_signal_features(self):
        forbidden_feature_keys = (
            "Completion",
            "assistant_reply",
            "result",
            "payload",
            "raw_response",
            "text",
            "document_text",
            "Ground_Truth",
            "ground-truth",
            "GROUND TRUTH",
        )

        for key in forbidden_feature_keys:
            with self.subTest(key=key):
                malformed_signal = signal()
                object.__setattr__(
                    malformed_signal,
                    "features",
                    {"source_count": 1, key: "secret"},
                )
                attempt = self._attempt(evidence_signals=(malformed_signal,))

                with self.assertRaisesRegex(
                    ValueError,
                    "unknown keys|forbidden field",
                ):
                    attempt.to_audit_dict()

    def test_attempt_audit_serialization_is_deterministic_and_safe(self):
        first = self._attempt(
            generator={"temperature": 0, "model": "mock", "provider": "local"},
            detector_results=(
                {
                    "score": 0.2,
                    "output_length": 12,
                    "output_hash": "a" * 64,
                    "detector_id": "detector-1",
                },
            ),
            metrics={"faithfulness": 0.5, "rpr": 0.1},
            latency={"total_ms": 12.5, "context_ms": 1.5},
            validation_status={
                "valid": True,
                "status": "valid",
                "issue_codes": (),
            },
        )
        second = self._attempt(
            generator={"provider": "local", "model": "mock", "temperature": 0},
            detector_results=(
                {
                    "detector_id": "detector-1",
                    "output_hash": "a" * 64,
                    "output_length": 12,
                    "score": 0.2,
                },
            ),
            metrics={"rpr": 0.1, "faithfulness": 0.5},
            latency={"context_ms": 1.5, "total_ms": 12.5},
            validation_status={
                "issue_codes": (),
                "status": "valid",
                "valid": True,
            },
        )

        first_json = json.dumps(first.to_audit_dict())
        second_json = json.dumps(second.to_audit_dict())

        self.assertEqual(first_json, second_json)
        audit = first.to_audit_dict()
        self.assertEqual("mock", audit["generator"]["model"])
        self.assertEqual(1.5, audit["latency"]["context_ms"])
        self.assertEqual(
            "a" * 64,
            audit["detector_results"][0]["output_hash"],
        )
        self.assertEqual(12, audit["detector_results"][0]["output_length"])
        self.assertEqual(
            "doc-1",
            audit["retrieval_evidence"][0]["doc_id"],
        )

    def test_attempt_construction_rejects_unknown_keys_in_every_mapping(self):
        builders = {
            "generator": lambda payload: self._attempt(generator=payload),
            "detector_results": lambda payload: self._attempt(
                detector_results=(payload,)
            ),
            "metrics": lambda payload: self._attempt(metrics=payload),
            "latency": lambda payload: self._attempt(latency=payload),
            "validation_status": lambda payload: self._attempt(
                validation_status=payload
            ),
        }
        unknown_keys = (
            "Completion",
            "assistant_reply",
            "content",
            "answer",
            "output",
            "response",
            "result",
            "payload",
            "raw_response",
            "text",
            "document_text",
            "prompt",
            "context",
            "messages",
            "document",
            "documents",
            "body",
            "unexpected_feature",
        )

        for field_name, builder in builders.items():
            for key in unknown_keys:
                with self.subTest(field_name=field_name, key=key):
                    with self.assertRaisesRegex(ValueError, "unknown keys"):
                        builder({key: "secret"})

    def test_attempt_construction_rejects_ground_truth_variants_in_every_mapping(
        self,
    ):
        builders = {
            "generator": lambda payload: self._attempt(generator=payload),
            "detector_results": lambda payload: self._attempt(
                detector_results=(payload,)
            ),
            "metrics": lambda payload: self._attempt(metrics=payload),
            "latency": lambda payload: self._attempt(latency=payload),
            "validation_status": lambda payload: self._attempt(
                validation_status=payload
            ),
        }
        ground_truth_variants = (
            "Ground_Truth",
            "ground-truth",
            "GROUND TRUTH",
        )

        for field_name, builder in builders.items():
            for key in ground_truth_variants:
                with self.subTest(field_name=field_name, key=key):
                    with self.assertRaisesRegex(ValueError, "forbidden field"):
                        builder({key: "secret"})

    def test_attempt_construction_rejects_nested_ground_truth_variants(self):
        builders = {
            "generator": lambda key: self._attempt(
                generator={"model": {key: "secret"}}
            ),
            "detector_results": lambda key: self._attempt(
                detector_results=(
                    {"detector_id": {key: "secret"}},
                )
            ),
            "metrics": lambda key: self._attempt(
                metrics={"faithfulness": {key: "secret"}}
            ),
            "latency": lambda key: self._attempt(
                latency={"total_ms": {key: "secret"}}
            ),
            "validation_status": lambda key: self._attempt(
                validation_status={"status": {key: "secret"}}
            ),
        }

        for field_name, builder in builders.items():
            for key in ("Ground_Truth", "ground-truth", "GROUND TRUTH"):
                with self.subTest(field_name=field_name, key=key):
                    with self.assertRaisesRegex(ValueError, "forbidden field"):
                        builder(key)

    def test_attempt_construction_rejects_nested_mapping_values(self):
        builders = {
            "generator": lambda: self._attempt(
                generator={"model": {"payload": "secret"}}
            ),
            "detector_results": lambda: self._attempt(
                detector_results=(
                    {"detector_id": {"payload": "secret"}},
                )
            ),
            "metrics": lambda: self._attempt(
                metrics={"faithfulness": {"payload": "secret"}}
            ),
            "latency": lambda: self._attempt(
                latency={"total_ms": {"payload": "secret"}}
            ),
            "validation_status": lambda: self._attempt(
                validation_status={"status": {"payload": "secret"}}
            ),
        }

        for field_name, builder in builders.items():
            with self.subTest(field_name=field_name):
                with self.assertRaisesRegex(ValueError, "nested mappings"):
                    builder()

    def test_attempt_metadata_is_deeply_immutable(self):
        generator = {"model": "mock"}
        detector = {"detector_id": "d1", "rule_ids": ["R1"]}
        metrics = {"faithfulness": 0.5}
        attempt = self._attempt(
            generator=generator,
            detector_results=(detector,),
            metrics=metrics,
        )

        generator["model"] = "mutated"
        detector["rule_ids"].append("R2")
        metrics["faithfulness"] = 0.0

        audit = attempt.to_audit_dict()
        self.assertEqual("mock", audit["generator"]["model"])
        self.assertEqual(["R1"], audit["detector_results"][0]["rule_ids"])
        self.assertEqual(0.5, audit["metrics"]["faithfulness"])
        with self.assertRaises(TypeError):
            attempt.generator["model"] = "blocked"

    def test_security_envelope_audit_is_allowlisted_and_deterministic(self):
        first = RAGSecurityEnvelope(
            query_id="query-1",
            retrieved_doc_ids=("doc-1", "doc-2"),
            evidence_hashes=("a" * 64, "b" * 64),
            trust_signal_summary={
                "signal_types": ("provenance_signal",),
                "signal_count": 1,
                "aggregate_score": None,
            },
            retrieval_policy="observe",
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
                "aggregate_score": None,
                "signal_count": 1,
                "signal_types": ("provenance_signal",),
            },
            retrieval_policy="observe",
            failure_types=("T10",),
            context_hash="c" * 64,
            final_answer_hash="d" * 64,
            run_id="run-1",
        )

        first_json = json.dumps(first.to_audit_dict())

        self.assertEqual(first_json, json.dumps(second.to_audit_dict()))
        self.assertEqual(
            ["doc-1", "doc-2"],
            first.to_audit_dict()["retrieved_doc_ids"],
        )
        self.assertEqual(
            ["provenance_signal"],
            first.to_audit_dict()["trust_signal_summary"]["signal_types"],
        )

    def test_security_envelope_construction_rejects_unknown_summary_keys(self):
        unknown_keys = (
            "Completion",
            "assistant_reply",
            "content",
            "answer",
            "output",
            "response",
            "result",
            "payload",
            "raw_response",
            "text",
            "document_text",
            "prompt",
            "context",
            "messages",
            "document",
            "documents",
            "body",
            "unexpected_feature",
        )

        for key in unknown_keys:
            with self.subTest(key=key):
                with self.assertRaisesRegex(ValueError, "unknown keys"):
                    self._envelope({key: "secret"})

    def test_security_envelope_construction_rejects_ground_truth_variants(self):
        for key in ("Ground_Truth", "ground-truth", "GROUND TRUTH"):
            with self.subTest(key=key):
                with self.assertRaisesRegex(ValueError, "forbidden field"):
                    self._envelope({key: "secret"})

    def test_security_envelope_rejects_nested_ground_truth_variants(self):
        for key in ("Ground_Truth", "ground-truth", "GROUND TRUTH"):
            with self.subTest(key=key):
                with self.assertRaisesRegex(ValueError, "forbidden field"):
                    self._envelope({"signal_count": {key: "secret"}})

    def test_security_envelope_rejects_nested_mapping_values_at_construction(
        self,
    ):
        with self.assertRaisesRegex(ValueError, "nested mappings"):
            self._envelope({"signal_count": {"payload": "secret"}})

    def test_security_envelope_deep_freezes_trust_summary(self):
        signal_types = ["provenance_signal"]
        summary = {"signal_count": 1, "signal_types": signal_types}
        envelope = self._envelope(summary)

        signal_types.append("mutated")
        summary["signal_count"] = 0

        audit = envelope.to_audit_dict()
        self.assertEqual(1, audit["trust_signal_summary"]["signal_count"])
        self.assertEqual(
            ["provenance_signal"],
            audit["trust_signal_summary"]["signal_types"],
        )
        with self.assertRaises(TypeError):
            envelope.trust_signal_summary["signal_count"] = 0

    @staticmethod
    def _envelope(
        trust_signal_summary: dict[str, object],
    ) -> RAGSecurityEnvelope:
        envelope = RAGSecurityEnvelope(
            query_id="query-1",
            retrieved_doc_ids=("doc-1",),
            evidence_hashes=("a" * 64,),
            trust_signal_summary=trust_signal_summary,
            retrieval_policy="observe",
            failure_types=(),
            context_hash="c" * 64,
            final_answer_hash="d" * 64,
            run_id="run-1",
        )
        return envelope

    @staticmethod
    def _attempt(
        *,
        generator: dict[str, object] | None = None,
        detector_results: tuple[dict[str, object], ...] | None = None,
        evidence_signals: tuple[EvidenceSignal, ...] = (),
        metrics: dict[str, object] | None = None,
        latency: dict[str, object] | None = None,
        validation_status: dict[str, object] | None = None,
    ) -> RAGAttemptRecord:
        return RAGAttemptRecord(
            attempt_id="attempt-1",
            run_id="run-1",
            query_id="query-1",
            attack_id=None,
            guard_mode="observe",
            retrieval_policy="observe",
            retrieval_evidence=(evidence(),),
            evidence_signals=evidence_signals,
            context_hash="c" * 64,
            context_length=120,
            generator=generator if generator is not None else {"model": "mock"},
            final_answer_hash="d" * 64,
            final_answer_length=42,
            detector_results=(
                detector_results
                if detector_results is not None
                else ({"detector_id": "detector-1", "score": 0.8},)
            ),
            metrics=(
                metrics
                if metrics is not None
                else {"faithfulness": 0.5}
            ),
            failure_types=("T10",),
            latency=latency if latency is not None else {"total_ms": 12.5},
            validation_status=(
                validation_status
                if validation_status is not None
                else {"status": "valid", "valid": True}
            ),
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
