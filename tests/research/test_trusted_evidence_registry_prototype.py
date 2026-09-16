from scripts.research.run_trusted_evidence_registry_prototype import (
    metadata,
    minmax,
    primary_family,
    scan_forbidden,
)


def test_forbidden_label_and_oracle_fields_are_detected() -> None:
    assert scan_forbidden({"overall_fact_status": "X"})
    assert scan_forbidden({"nested": {"evidence_id": "E1"}})
    assert scan_forbidden({"candidate_id": "safe", "query": "safe"}) == []


def test_family_prefers_explicit_document_title() -> None:
    assert primary_family("官方说明", "关于《示例法》的说明") == "示例法"


def test_metadata_keeps_unknowns_explicit() -> None:
    row = metadata(
        {
            "content_hash": "a" * 64,
            "official_source_title": "官方说明",
            "official_source_url": "https://example.gov.cn/a",
            "snapshot_text": "没有可独立支持的版本日期。",
            "official_role": None,
        }
    )
    assert row["issuer"] is None
    assert row["effective_start"] is None
    assert row["metadata_status"]["supersession"] == "UNKNOWN"


def test_minmax_is_deterministic_for_constant_scores() -> None:
    assert minmax([2.0, 2.0]) == [0.0, 0.0]
