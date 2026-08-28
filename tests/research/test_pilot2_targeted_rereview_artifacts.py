from __future__ import annotations

import csv
import hashlib
import json
import os
import zipfile
from pathlib import Path
from xml.etree import ElementTree

import pytest


ARTIFACT_ROOT = os.environ.get("PILOT2_TARGETED_ARTIFACT_ROOT")
RAW_ROOT = os.environ.get("PILOT2_RAW_ROOT")
FULL_V2_ROOT = os.environ.get("PILOT2_FULL_V2_ROOT")

pytestmark = pytest.mark.skipif(
    not ARTIFACT_ROOT or not RAW_ROOT or not FULL_V2_ROOT,
    reason="set targeted, raw, and full V2 artifact roots",
)

EXPECTED_RAW_SHA256 = {
    "annotator_A/A01_phase1_return.zip": "c5976000abdbaf2bc66b002e0d1dfca0984653b48eea2127a76658fdf12b8ed2",
    "annotator_A/A01_phase2_fact_return.zip": "bd11e6648e0657923312a3620a7eae42ef54f536d619f8a7574f50967f5a6cc0",
    "annotator_B/B01_phase1_return.zip": "e697f7d57520ed397cff6bf1f3502662f29cad3edce2ba1640fa3bdd8223224c",
    "annotator_B/B01_phase2_fact_return.zip": "2eeedcedb53bd629e67ec2faa987279059fd88ee0297001ee4738306c2aec4ae",
}

COMPLETED_A1_SHA256 = "100cffe2b81a23f3a65ade5ba712cd7aeefcfc56c600dae68f2b0241af36737f"

FORBIDDEN = {
    "attack_type",
    "candidate_kind",
    "candidate_label",
    "candidate_intent",
    "mutation_spec",
    "expected_conclusion",
    "owner_mapping",
    "ground_truth",
    "poison_label",
    "attack_id",
    "agreement",
    "disagreement",
}


def _root() -> Path:
    return Path(ARTIFACT_ROOT or "")


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _csv(path: Path) -> list[dict[str, str]]:
    payload = path.read_bytes()
    assert payload.startswith(b"\xef\xbb\xbf")
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def _xlsx(annotator: str, phase: int) -> Path:
    return _root() / f"annotator_{annotator}" / f"{annotator}_phase{phase}_targeted_rereview.xlsx"


def _worksheet_xml(path: Path, index: int) -> ElementTree.Element:
    with zipfile.ZipFile(path) as archive:
        return ElementTree.fromstring(archive.read(f"xl/worksheets/sheet{index}.xml"))


def test_output_structure_and_immutable_inputs() -> None:
    root = _root()
    expected = {
        f"annotator_{annotator}/{annotator}_phase{phase}_targeted_rereview.{suffix}"
        for annotator in ("A", "B")
        for phase in (1, 2)
        for suffix in ("csv", "xlsx")
    }
    expected |= {
        "annotator_A/A_targeted_rereview_instructions.md",
        "annotator_B/B_targeted_rereview_instructions.md",
        "coordinator/00_发放和回收说明.md",
        "coordinator/POST_ANNOTATION_EXPERIMENT_TRANSITION.md",
        "coordinator/targeted_field_audit_summary.md",
        "coordinator/targeted_return_registration.csv",
        "owner_only/original_v2_package_manifest.json",
        "owner_only/targeted_field_audit.json",
        "owner_only/targeted_rereview_manifest.json",
    }
    actual = {path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file()}
    assert actual == expected
    raw_root = Path(RAW_ROOT or "")
    for relative, digest in EXPECTED_RAW_SHA256.items():
        assert _sha(raw_root / relative) == digest
    full_v2_root = Path(FULL_V2_ROOT or "")
    manifest = json.loads((root / "owner_only" / "original_v2_package_manifest.json").read_text(encoding="utf-8"))
    for entry in manifest["files"]:
        current = full_v2_root / entry["path"]
        assert current.stat().st_size == entry["size_bytes"]
        assert _sha(current) == entry["sha256"]


def test_targeted_counts_and_process_only_scope() -> None:
    expected = {("A", 1): 108, ("A", 2): 252, ("B", 1): 108, ("B", 2): 274}
    for key, count in expected.items():
        annotator, phase = key
        rows = _csv(_root() / f"annotator_{annotator}" / f"{annotator}_phase{phase}_targeted_rereview.csv")
        assert len(rows) == count
        process = [row for row in rows if row["task_type"] == "PROCESS_FIX_ONLY"]
        if key == ("B", 2):
            assert sum(row["field_name"] == "professional_lookup_used" for row in process) == 21
            assert sum(row["field_name"] == "lookup_source_type" for row in process) == 1
            lookup = next(row for row in process if row["field_name"] == "lookup_source_type")
            assert "google.com/search" in lookup["source_or_evidence"].lower()
            assert lookup["v1_value"] == "OFFICIAL_GOVERNMENT"
        else:
            assert not process


def test_no_peer_disagreement_or_candidate_intent_leakage() -> None:
    for annotator in ("A", "B"):
        peer = "B" if annotator == "A" else "A"
        for path in (_root() / f"annotator_{annotator}").iterdir():
            payload = path.read_bytes()
            if path.suffix == ".xlsx":
                with zipfile.ZipFile(path) as archive:
                    text = "\n".join(
                        archive.read(name).decode("utf-8", errors="ignore")
                        for name in archive.namelist()
                        if name.endswith(".xml")
                    ).lower()
            else:
                text = payload.decode("utf-8-sig").lower()
            assert f"annotator_{peer.lower()}" not in text
            assert not any(token in text for token in FORBIDDEN)


def test_xlsx_sheets_dropdowns_formulas_and_read_only_guards() -> None:
    namespace = {"x": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    for annotator in ("A", "B"):
        for phase in (1, 2):
            path = _xlsx(annotator, phase)
            with zipfile.ZipFile(path) as archive:
                workbook = ElementTree.fromstring(archive.read("xl/workbook.xml"))
                names = [node.attrib["name"] for node in workbook.findall(".//x:sheet", namespace)]
            assert names == ["先看这里", "需要你复核", "原结果只读", "回溯声明"]
            tasks = _worksheet_xml(path, 2)
            formulas = tasks.findall(".//x:f", namespace)
            validations = tasks.findall(".//x:dataValidation", namespace)
            assert formulas
            assert any(node.attrib.get("type") == "list" for node in validations)
            assert any(node.attrib.get("type") == "custom" for node in validations)
            # The owner-completed A1 workbook was saved by the human spreadsheet
            # application, which preserved values/formulas/validations but removed
            # OOXML errorStyle metadata.  Do not rewrite that returned evidence.
            if _sha(path) != COMPLETED_A1_SHA256:
                assert any(node.attrib.get("errorStyle") == "stop" for node in validations)
            original = _worksheet_xml(path, 3)
            original_validations = original.findall(".//x:dataValidation", namespace)
            assert any(node.attrib.get("type") == "custom" for node in original_validations)


def test_manifest_keeps_follow_on_gates_closed() -> None:
    manifest = json.loads((_root() / "owner_only" / "targeted_rereview_manifest.json").read_text(encoding="utf-8"))
    assert manifest["targeted_rereview_kit"] == "READY_FOR_HUMAN_EXECUTION"
    assert manifest["formal_agreement"] == "NOT_STARTED"
    assert manifest["adjudication"] == "NOT_STARTED"
    assert manifest["dataset"] == "NOT_FROZEN"
    assert manifest["detector"] == "NOT_STARTED"
    assert manifest["training"] == "NOT_STARTED"
    assert manifest["formal_experiment"] == "NOT_STARTED"
    assert manifest["auto_continue"] == "NO"
