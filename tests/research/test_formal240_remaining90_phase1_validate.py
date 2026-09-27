"""Synthetic checks for the D1 remaining90 blind-return validator."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

from formal240_remaining90_phase1_validate import read_json, validate_return  # noqa: E402


ALLOWED = {
    "blind_review_id": "exact supplied ID",
    "text_naturalness": ["NATURAL", "MINOR_ISSUE", "UNNATURAL"],
    "local_internal_conflict": ["YES", "NO", "UNCERTAIN"],
    "self_containment": ["PASS", "FLAG", "UNCERTAIN"],
    "ambiguous_referent": ["YES", "NO", "UNCERTAIN"],
    "meta_or_template_language": ["YES", "NO", "UNCERTAIN"],
    "issue_note": "string",
}


def synthetic_rows() -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    packet = [
        {"blind_review_id": f"D1BR-{i:012X}", "candidate_text": f"句子{i}"}
        for i in range(90)
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


def test_strict_json_rejects_duplicate_keys_and_bom(tmp_path: Path) -> None:
    source = tmp_path / "bad.json"
    source.write_bytes(b'{"a":1,"a":2}')
    with pytest.raises(ValueError, match="duplicate JSON key"):
        read_json(source)
    source.write_bytes(b"\xef\xbb\xbf{}")
    with pytest.raises(ValueError, match="BOM"):
        read_json(source)


def test_return_requires_flag_note_and_exact_order(tmp_path: Path) -> None:
    packet, rows = synthetic_rows()
    source = tmp_path / "raw.json"
    source.write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")
    qa, _ = validate_return("r3", source, packet, ALLOWED)
    assert qa["records"] == 90
    assert qa["flagged_notes"] == 0

    rows[0]["local_internal_conflict"] = "YES"
    source.write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")
    with pytest.raises(ValueError, match="issue_note"):
        validate_return("r3", source, packet, ALLOWED)
    rows[0]["issue_note"] = "同一对象的两个断言不能并存。"
    rows[0], rows[1] = rows[1], rows[0]
    source.write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")
    with pytest.raises(ValueError, match="ID uniqueness/set/order"):
        validate_return("r3", source, packet, ALLOWED)


def test_return_rejects_extra_field(tmp_path: Path) -> None:
    packet, rows = synthetic_rows()
    rows[0]["hidden_label"] = "not allowed"
    source = tmp_path / "raw.json"
    source.write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")
    with pytest.raises(ValueError, match="noncanonical keys"):
        validate_return("r3", source, packet, ALLOWED)
