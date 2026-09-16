from __future__ import annotations

from collections import Counter

from llmguard.domains.retrieval.hidden_poisoning.method_engineering import (
    FIVE_VIEW_SIGNAL_REGISTRY,
)
from llmguard.domains.retrieval.hidden_poisoning.method_engineering.retrieval_harness import (
    PREDECLARED_K,
    CharacterNgramBM25,
    RetrievalDocument,
    build_signal_deployability_matrix,
    canonical_query,
    character_ngrams,
    forbidden_key_hits,
    query_qa,
    rank_scores,
    temporal_gap_cause,
)
from scripts.research import run_final72_retrieval_harness as runner


def _documents() -> list[RetrievalDocument]:
    return [
        RetrievalDocument(
            doc_id="D1",
            candidate_text="示例规定适用于普通学校。",
            source_title="示例规定",
            primary_subject="示例规定",
        ),
        RetrievalDocument(
            doc_id="D2",
            candidate_text="另一制度涉及城市管理。",
            source_title="另一制度",
            primary_subject="另一制度",
        ),
    ]


def test_character_ngram_bm25_is_deterministic() -> None:
    documents = _documents()
    retriever = CharacterNgramBM25(documents)
    first = retriever.score("示例规定当前内容是什么？")
    second = retriever.score("示例规定当前内容是什么？")
    assert first == second
    assert first[0] > first[1]
    assert character_ngrams("中 文。") == character_ngrams("中文")
    ranked = rank_scores(
        query_id="Q1",
        documents=documents,
        scores=first,
        retriever_id=retriever.retriever_id,
        run_id="RUN1",
    )
    assert {row.doc_id: row.rank for row in ranked} == {"D1": 1, "D2": 2}


def test_query_is_subject_only_and_passes_leakage_qa() -> None:
    query = canonical_query("IG-1", "示例管理规定")
    qa = query_qa(
        query,
        candidate_texts=(
            "《示例管理规定》自2020年起施行。",
            "《示例管理规定》自2021年起施行。",
            "旧版《示例管理规定》曾经施行。",
        ),
    )
    assert qa["pass"] is True
    assert qa["numeric_answer_leakage"] == []
    assert "当前" in query.query_text


def test_feature_plane_rejects_labels_and_owner_fields() -> None:
    assert forbidden_key_hits({"doc_id": "D1", "candidate_text": "x"}) == []
    assert forbidden_key_hits({"owner_only": {"candidate_kind": "POISON"}}) == [
        "candidate_kind",
        "owner_only",
    ]


def test_all_42_signals_have_evidence_access_and_deployability() -> None:
    rows = build_signal_deployability_matrix()
    assert len(rows) == len(FIVE_VIEW_SIGNAL_REGISTRY) == 42
    assert len({row["signal_name"] for row in rows}) == 42
    modes = Counter(row["evidence_access_mode"] for row in rows)
    assert modes["ORACLE_MATCHED_EVIDENCE_DIAGNOSTIC_ONLY"] == 29
    assert modes["QUERY_RETRIEVAL_TRACE"] == 4
    assert modes["VERSION_REGISTRY_LOOKUP"] == 7
    assert modes["CANDIDATE_ONLY"] == 2
    assert (
        sum(row["current_implementation_uses_oracle_matched_evidence"] for row in rows)
        == 29
    )


def test_temporal_gap_distinguishes_not_applicable_from_missing_metadata() -> None:
    no_claim = {"candidate_text": "本规定适用于普通学校。", "evidence": []}
    temporal_claim = {
        "candidate_text": "本规定于2022年修订。",
        "evidence": [{"evidence_id": "E1"}],
    }
    assert temporal_gap_cause(no_claim).value == "NO_TEMPORAL_CLAIM"
    assert temporal_gap_cause(temporal_claim).value == "NO_VERSION_ROLE_METADATA"


def test_cli_requires_physical_lock_stages() -> None:
    parser = runner.parser()
    assert (
        parser.parse_args(
            [
                "prepare",
                "--candidate-corpus",
                "candidate.jsonl",
                "--previous-raw-matrix",
                "raw.jsonl",
                "--output",
                "out",
            ]
        ).command
        == "prepare"
    )
    assert (
        parser.parse_args(["lock-queries", "--output", "out"]).command == "lock-queries"
    )
    assert (
        parser.parse_args(["lock-corpus", "--output", "out"]).command == "lock-corpus"
    )
    assert parser.parse_args(["retrieve", "--output", "out"]).command == "retrieve"
    assert parser.parse_args(["signals", "--output", "out"]).command == "signals"
    assert (
        parser.parse_args(
            [
                "analyze",
                "--output",
                "out",
                "--ground-truth",
                "gt.json",
                "--candidate-corpus",
                "candidate.jsonl",
                "--previous-safe-projection",
                "safe.jsonl",
                "--previous-raw-matrix",
                "raw.jsonl",
            ]
        ).command
        == "analyze"
    )
    assert (
        parser.parse_args(["finalize", "--output", "out", "--repo-root", "."]).command
        == "finalize"
    )
    assert PREDECLARED_K == (1, 3, 5, 10)
