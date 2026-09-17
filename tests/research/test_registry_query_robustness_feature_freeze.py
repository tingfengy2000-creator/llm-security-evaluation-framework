from scripts.research.run_registry_query_robustness_feature_freeze import (
    _risk,
    _safe_date,
    build_registry_v2,
    canonical_family,
    forbidden_hits,
    query_texts,
    structured_claim,
)


def _candidate() -> dict[str, object]:
    return {
        "sample_id": "P4Q-test",
        "primary_subject": "中华人民共和国示例法",
        "phase1_view": {
            "source_title": "示例法官方页面",
            "candidate_text": "《中华人民共和国示例法》由示例委员会于2024年修订并自2025年1月1日起施行。",
        },
    }


def test_four_queries_are_label_blind_and_distinct() -> None:
    queries = query_texts(_candidate())
    assert set(queries) == {"Q_FULL", "Q_NO_TITLE", "Q_TEXT_ONLY", "Q_STRUCTURED"}
    assert "示例法官方页面" in queries["Q_FULL"]
    assert "示例法官方页面" not in queries["Q_NO_TITLE"]
    assert not forbidden_hits(queries)


def test_structured_claim_uses_only_candidate_visible_values() -> None:
    claim = structured_claim(_candidate())
    assert "中华人民共和国示例法" in claim["subject"]
    assert "修订" in claim["predicate"]
    assert "2025年1月1日" in claim["time_expression"]


def test_family_normalization_does_not_create_supersession() -> None:
    assert canonical_family("中华人民共和国示例法（2024修正）") == "示例法"
    corpus = [
        {
            "evidence_doc_id": "TED-a",
            "source_family": "中华人民共和国示例法",
            "snapshot_text": "发布日期：2020-01-01",
            "authority_role": None,
            "snapshot_id": "SNAP-a",
            "official_url": "https://example.gov.cn/a",
        },
        {
            "evidence_doc_id": "TED-b",
            "source_family": "中华人民共和国示例法（2024修正）",
            "snapshot_text": "发布日期：2024-01-01",
            "authority_role": None,
            "snapshot_id": "SNAP-b",
            "official_url": "https://example.gov.cn/b",
        },
    ]
    registry = [
        {
            "versions": [
                {
                    "evidence_doc_id": "TED-a",
                    "version_id": "V-a",
                    "document_id": "D-a",
                    "publication_date": "2020-01-01",
                    "effective_start": None,
                    "effective_end": None,
                    "current_status": "UNKNOWN",
                    "predecessor": None,
                    "successor": None,
                    "superseded_by": None,
                    "issuer": None,
                    "authority": None,
                },
                {
                    "evidence_doc_id": "TED-b",
                    "version_id": "V-b",
                    "document_id": "D-b",
                    "publication_date": "2024-01-01",
                    "effective_start": None,
                    "effective_end": None,
                    "current_status": "UNKNOWN",
                    "predecessor": None,
                    "successor": None,
                    "superseded_by": None,
                    "issuer": None,
                    "authority": None,
                },
            ]
        }
    ]
    v2, _, _ = build_registry_v2(corpus, registry)
    assert v2[0]["chronologically_precedes"] == ["V-b"]
    assert all(row["supersedes"] is None for row in v2)


def test_date_and_shortcut_thresholds_fail_closed() -> None:
    assert _safe_date("2011", "20", "01") is None
    assert _risk(0.10, 0.0) == "MATERIAL"
    assert _risk(0.03, 0.0) == "LOW"
    assert _risk(0.01, 0.0) == "NONE"
