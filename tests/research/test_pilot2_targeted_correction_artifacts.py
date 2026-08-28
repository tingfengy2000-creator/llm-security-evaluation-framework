from __future__ import annotations

import csv
import hashlib
import json
import os
import zipfile
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree

import pytest


ARTIFACT_ROOT = os.environ.get("PILOT2_TARGETED_CORRECTION_ROOT")
pytestmark = pytest.mark.skipif(not ARTIFACT_ROOT, reason="set PILOT2_TARGETED_CORRECTION_ROOT")

EXPECTED_ABSENT = {
    ("A", 2): {"version_relation_present", "history_or_update_claim_present", "authority_claim_present"},
    ("B", 1): set(),
    ("B", 2): {"version_relation_present", "history_or_update_claim_present", "authority_claim_present"},
}


def _root() -> Path:
    return Path(ARTIFACT_ROOT or "")


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _csv(annotator: str, phase: int) -> list[dict[str, str]]:
    path = _root() / f"annotator_{annotator}" / f"{annotator}_phase{phase}_targeted_rereview.csv"
    assert path.read_bytes().startswith(b"\xef\xbb\xbf")
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def _xlsx_text(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        return "\n".join(
            archive.read(name).decode("utf-8", errors="ignore")
            for name in archive.namelist()
            if name.endswith(".xml")
        )


def test_correction_is_additive_and_contains_only_three_open_workbooks() -> None:
    expected = {
        f"annotator_{annotator}/{annotator}_phase{phase}_targeted_rereview.{suffix}"
        for annotator, phase in (("A", 2), ("B", 1), ("B", 2))
        for suffix in ("csv", "xlsx")
    }
    expected |= {"coordinator/00_更正与填写顺序.md", "owner_only/correction_manifest.json"}
    actual = {path.relative_to(_root()).as_posix() for path in _root().rglob("*") if path.is_file()}
    assert actual == expected
    manifest = json.loads((_root() / "owner_only" / "correction_manifest.json").read_text(encoding="utf-8"))
    completed_a1 = Path(manifest["completed_a1"]["path"])
    assert manifest["completed_a1"]["included"] is False
    assert manifest["completed_a1"]["mutation"] == "NONE"
    assert _sha(completed_a1) == manifest["completed_a1"]["sha256"]


def test_v1_header_mapping_and_absence_contract() -> None:
    for key, expected_absent in EXPECTED_ABSENT.items():
        rows = _csv(*key)
        actual_absent = {row["field_name"] for row in rows if row["v1_value"] == "[V1_ABSENT]"}
        assert actual_absent == expected_absent
        assert all(not row["new_value"] for row in rows)

    b1 = _csv("B", 1)
    assert Counter(row["v1_value"] for row in b1 if row["field_name"] == "locally_detectable") == Counter(YES=26, NO=8, UNCERTAIN=2)
    assert Counter(row["v1_value"] for row in b1 if row["field_name"] == "cross_document_evidence_needed") == Counter(YES=14, NO=21, UNCERTAIN=1)
    assert Counter(row["v1_value"] for row in b1 if row["field_name"] == "assigned_stealth_level") == Counter(S1=19, S2=3, S3=1, NOT_APPLICABLE=8, UNCERTAIN=5)

    b2 = _csv("B", 2)
    assert Counter(row["v1_value"] for row in b2 if row["field_name"] == "version_relation_correct") == Counter(YES=24, NO=12)
    assert Counter(row["v1_value"] for row in b2 if row["field_name"] == "authority_matches") == Counter(YES=35, NO=1)


def test_workbooks_preserve_guards_and_freeze_owner_rules() -> None:
    namespace = {"x": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    for annotator, phase in (("A", 2), ("B", 1), ("B", 2)):
        path = _root() / f"annotator_{annotator}" / f"{annotator}_phase{phase}_targeted_rereview.xlsx"
        text = _xlsx_text(path)
        assert "version_context / 版本背景在本轮视为已知正确" in text
        assert "[V1_ABSENT] 只能出现在 Phase2 新增" in text
        if phase == 1:
            assert "S2/S3 衡量已存在的事实错误多难发现" in text
            assert "单独打开一个官方页面不算 cross-document" in text
        with zipfile.ZipFile(path) as archive:
            workbook = ElementTree.fromstring(archive.read("xl/workbook.xml"))
            names = [node.attrib["name"] for node in workbook.findall(".//x:sheet", namespace)]
            tasks = ElementTree.fromstring(archive.read("xl/worksheets/sheet2.xml"))
        assert names == ["先看这里", "需要你复核", "原结果只读", "回溯声明"]
        validations = tasks.findall(".//x:dataValidation", namespace)
        assert any(node.attrib.get("type") == "list" for node in validations)
        assert any(node.attrib.get("type") == "custom" for node in validations)
        assert any(node.attrib.get("errorStyle") == "stop" for node in validations)


def test_follow_on_gates_remain_closed() -> None:
    manifest = json.loads((_root() / "owner_only" / "correction_manifest.json").read_text(encoding="utf-8"))
    assert manifest["status"] == "THREE_CORRECTED_WORKBOOKS_READY_FOR_INDEPENDENT_HUMAN_COMPLETION"
    assert manifest["formal_agreement"] == "NOT_STARTED"
    assert manifest["adjudication"] == "NOT_STARTED"
    assert manifest["dataset"] == "NOT_FROZEN"
    assert manifest["detector"] == "NOT_STARTED"
    assert manifest["training"] == "NOT_STARTED"
    assert manifest["formal_experiment"] == "NOT_STARTED"
    assert manifest["auto_continue"] == "NO"
