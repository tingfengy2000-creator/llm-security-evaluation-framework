"""Synthetic checks for the R5 auxiliary targeted Phase1 lock validator."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

from formal240_remaining90_r5_targeted_validate import (  # noqa: E402
    compare,
    validate_r5,
)


ALLOWED = {
    "blind_review_id": "exact supplied ID",
    "text_naturalness": ["NATURAL", "MINOR_ISSUE", "UNNATURAL"],
    "local_internal_conflict": ["YES", "NO", "UNCERTAIN"],
    "self_containment": ["PASS", "FLAG", "UNCERTAIN"],
    "ambiguous_referent": ["YES", "NO", "UNCERTAIN"],
    "meta_or_template_language": ["YES", "NO", "UNCERTAIN"],
    "issue_note": "string",
}


def fixtures() -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    packet = [
        {"blind_review_id": f"D1BR-{i:012X}", "candidate_text": f"句子{i}"}
        for i in range(10)
    ]
    rows = [
        {
            "blind_review_id": item["blind_review_id"],
            "text_naturalness": "NATURAL",
            "local_internal_conflict": "NO",
            "self_containment": "PASS",
            "ambiguous_referent": "NO",
            "meta_or_template_language": "NO",
            "issue_note": "",
        }
        for item in packet
    ]
    return packet, rows


def test_r5_validates_ten_rows_and_notes() -> None:
    packet, rows = fixtures()
    qa = validate_r5(rows, packet, ALLOWED)
    assert qa["records"] == 10
    assert qa["flagged_notes"] == 0
    rows[0]["local_internal_conflict"] = "YES"
    with pytest.raises(ValueError, match="issue_note"):
        validate_r5(rows, packet, ALLOWED)
    rows[0]["issue_note"] = "同一对象有两个冲突断言。"
    assert validate_r5(rows, packet, ALLOWED)["flagged_notes"] == 1


def test_r5_rejects_id_order_and_extra_field() -> None:
    packet, rows = fixtures()
    rows[0], rows[1] = rows[1], rows[0]
    with pytest.raises(ValueError, match="ID uniqueness/set/order"):
        validate_r5(rows, packet, ALLOWED)
    rows[0], rows[1] = rows[1], rows[0]
    rows[0]["hidden_label"] = "Poison"
    with pytest.raises(ValueError, match="noncanonical keys"):
        validate_r5(rows, packet, ALLOWED)


def test_r5_comparison_is_descriptive_not_adjudication() -> None:
    _, rows = fixtures()
    r3 = {row["blind_review_id"]: dict(row) for row in rows}
    r4 = {row["blind_review_id"]: dict(row) for row in rows}
    r3[rows[0]["blind_review_id"]]["local_internal_conflict"] = "NO"
    r4[rows[0]["blind_review_id"]]["local_internal_conflict"] = "YES"
    rows[0]["local_internal_conflict"] = "YES"
    output = compare(rows, r3, r4)
    assert output["support_counts"]["local_internal_conflict"] == {
        "r3_r4_disagreement_count": 1,
        "r5_matches_r3": 9,
        "r5_matches_r4": 10,
    }
