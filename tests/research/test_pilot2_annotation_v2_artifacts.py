from __future__ import annotations

import csv
import hashlib
import io
import json
import os
import zipfile
from pathlib import Path

import pytest

from llmguard.domains.retrieval.hidden_poisoning.annotation_v2 import (
    PHASE1_V2_FIELDS,
    PHASE2_V2_FIELDS,
    ResponseMode,
    validate_phase1_v2_row,
    validate_phase2_v2_row,
)


ARTIFACT_ROOT = os.environ.get("PILOT2_V2_ARTIFACT_ROOT")
RAW_ROOT = os.environ.get("PILOT2_RAW_ROOT")

pytestmark = pytest.mark.skipif(
    not ARTIFACT_ROOT or not RAW_ROOT,
    reason="set PILOT2_V2_ARTIFACT_ROOT and PILOT2_RAW_ROOT for private artifact validation",
)

EXPECTED_RAW_SHA256 = {
    "annotator_A/A01_phase1_return.zip": "c5976000abdbaf2bc66b002e0d1dfca0984653b48eea2127a76658fdf12b8ed2",
    "annotator_A/A01_phase2_fact_return.zip": "bd11e6648e0657923312a3620a7eae42ef54f536d619f8a7574f50967f5a6cc0",
    "annotator_B/B01_phase1_return.zip": "e697f7d57520ed397cff6bf1f3502662f29cad3edce2ba1640fa3bdd8223224c",
    "annotator_B/B01_phase2_fact_return.zip": "2eeedcedb53bd629e67ec2faa987279059fd88ee0297001ee4738306c2aec4ae",
}
EXPECTED_PREFLIGHT_SHA256 = "adeb458629cde0e275c621de7cac4f88bff2dc0a19751ed0ff2fb220c394bae0"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _read_zip_csv(archive_path: Path, suffix: str) -> tuple[list[str], list[dict[str, str]]]:
    with zipfile.ZipFile(archive_path) as archive:
        matches = [name for name in archive.namelist() if name.endswith(suffix)]
        assert len(matches) == 1
        payload = archive.read(matches[0])
    assert payload.startswith(b"\xef\xbb\xbf")
    reader = csv.DictReader(io.StringIO(payload.decode("utf-8-sig"), newline=""))
    rows = list(reader)
    return list(reader.fieldnames or ()), rows


def _package(root: Path, annotator: str, phase: str) -> Path:
    return root / f"annotator_{annotator}" / f"{annotator}_round1_{phase}_review_v2.zip"


def test_required_output_structure_and_raw_evidence_are_immutable() -> None:
    root = Path(ARTIFACT_ROOT or "")
    raw_root = Path(RAW_ROOT or "")
    required = {
        "annotator_A/A_round1_phase1_review_v2.zip",
        "annotator_A/A_round1_phase2_review_v2.zip",
        "annotator_B/B_round1_phase1_review_v2.zip",
        "annotator_B/B_round1_phase2_review_v2.zip",
        "coordinator/00_V2复核操作说明.md",
        "coordinator/01_完整字段字典.md",
        "coordinator/02_YES_NO_UNCERTAIN_NOT_APPLICABLE说明.md",
        "coordinator/03_authority完整示例.md",
        "coordinator/04_version_relation完整示例.md",
        "coordinator/05_history_update完整示例.md",
        "coordinator/06_overall_fact_status决策树.md",
        "coordinator/07_Phase1隐蔽等级说明.md",
        "coordinator/08_复核回收登记.csv",
        "coordinator/09_owner_blindness_correction_notice.md",
        "owner_only/round1_raw_manifest.json",
        "owner_only/owner_operational_fact_correction.json",
        "owner_only/v1_to_v2_schema_mapping.json",
        "owner_only/rereview_control_manifest.json",
        "owner_only/original_preflight_blocker_snapshot.json",
    }
    actual = {path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file()}
    assert actual == required
    for relative, expected in EXPECTED_RAW_SHA256.items():
        assert _sha256(raw_root / relative) == expected
    preflight = (
        raw_root
        / "owner_only"
        / "pilot2_return_review_20260827"
        / "pilot2_return_preflight_decision_report_20260827.xlsx"
    )
    assert _sha256(preflight) == EXPECTED_PREFLIGHT_SHA256


@pytest.mark.parametrize("annotator", ["A", "B"])
def test_phase1_and_phase2_templates_preserve_identity_and_frozen_columns(annotator: str) -> None:
    root = Path(ARTIFACT_ROOT or "")
    for phase, expected_fields in (("phase1", PHASE1_V2_FIELDS), ("phase2", PHASE2_V2_FIELDS)):
        archive = _package(root, annotator, phase)
        fields, rows = _read_zip_csv(archive, "01_V2复核表.csv")
        _, v1_rows = _read_zip_csv(archive, "02_V1原始答案只读参考.csv")
        assert fields == list(expected_fields)
        assert len(rows) == len(v1_rows) == 36
        visible = expected_fields[:4] if phase == "phase1" else expected_fields[:5]
        for v2, v1 in zip(rows, v1_rows, strict=True):
            assert all(v2[field] == v1[field] for field in visible)
            if phase == "phase1":
                validate_phase1_v2_row(v2, mode=ResponseMode.TEMPLATE)
            else:
                validate_phase2_v2_row(v2, mode=ResponseMode.TEMPLATE)


def test_a_and_b_share_sample_identity_but_packages_do_not_cross_leak() -> None:
    root = Path(ARTIFACT_ROOT or "")
    forbidden = {
        "candidate_kind",
        "candidate_label",
        "mutation_spec",
        "expected_conclusion",
        "owner_mapping",
        "ground_truth",
        "poison_label",
        "attack_id",
    }
    for phase in ("phase1", "phase2"):
        _, a_rows = _read_zip_csv(_package(root, "A", phase), "01_V2复核表.csv")
        _, b_rows = _read_zip_csv(_package(root, "B", phase), "01_V2复核表.csv")
        assert [row["sample_id"] for row in a_rows] == [row["sample_id"] for row in b_rows]
        assert [row["claim_text"] for row in a_rows] == [row["claim_text"] for row in b_rows]
        for annotator, peer in (("A", "B"), ("B", "A")):
            archive_path = _package(root, annotator, phase)
            with zipfile.ZipFile(archive_path) as archive:
                for name in archive.namelist():
                    assert f"annotator_{peer}" not in name.lower()
                    if name.endswith("/"):
                        continue
                    text = archive.read(name).decode("utf-8-sig").lower()
                    assert forbidden.isdisjoint(text.split())
                    assert not any(token in text for token in forbidden)


def test_owner_correction_and_blocker_history_are_additive() -> None:
    root = Path(ARTIFACT_ROOT or "")
    correction = json.loads((root / "owner_only" / "owner_operational_fact_correction.json").read_text(encoding="utf-8"))
    blocker = json.loads((root / "owner_only" / "original_preflight_blocker_snapshot.json").read_text(encoding="utf-8"))
    control = json.loads((root / "owner_only" / "rereview_control_manifest.json").read_text(encoding="utf-8"))
    assert correction["A_PHASE1_STRICT_BLINDNESS"] == "OWNER_CONFIRMED_PRESERVED"
    assert correction["REGISTRATION_TIMESTAMP_STATUS"] == "INCORRECT_RECORDING / DOCUMENTATION_DEFECT_ONLY"
    assert blocker["original_inference_status"] == "PRESERVED_AS_HISTORICAL_PREFLIGHT_INFERENCE"
    assert blocker["superseding_disposition"] == "PROTOCOL_AND_ANNOTATION_SCHEMA_BLOCKER"
    assert blocker["BLINDNESS_SUBISSUE"] == "RESOLVED_BY_OWNER_CONFIRMED_ACTUAL_DISTRIBUTION_ORDER"
    assert control["formal_agreement_v2"] == "NOT_YET_ESTABLISHED"
    assert control["disagreement_packet"] == "NOT_GENERATED"
    assert control["adjudication"] == "NOT_EXECUTED"
    assert all(check["status"] == "PASS" for check in control["validation"])
