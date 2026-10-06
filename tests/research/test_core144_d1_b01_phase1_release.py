"""The B01 gate is mechanical, independent and fail-closed; raw bytes survive."""

import importlib.util
import json
import stat
import sys
from pathlib import Path
from typing import Any

import pytest


ROOT = Path(__file__).resolve().parents[2]
CORE = ROOT / "docs/research/stage6_1_hidden_knowledge_poisoning/core144"
SCRIPT = ROOT / "scripts/research/lock_core144_d1_b01_phase1_return.py"
sys.path.insert(0, str(SCRIPT.parent))
SPEC = importlib.util.spec_from_file_location("b01_lock", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
LOCKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LOCKER)


def inputs(tmp_path: Path) -> tuple[Path, Path, Path, Path, Path, Path]:
    source = tmp_path / "returned.xlsx"
    original = tmp_path / "original.xlsx"
    phase2 = tmp_path / "phase2.xlsx"
    manifest1 = tmp_path / "manifest1.json"
    manifest2 = tmp_path / "manifest2.json"
    for path, value in ((source, b"raw bytes"), (original, b"original"), (phase2, b"sealed")):
        path.write_bytes(value)
    for path, phase in ((manifest1, "PHASE1"), (manifest2, "PHASE2")):
        path.write_text(json.dumps({"artifact": f"{LOCKER.PREFIX}_{phase}_V1.xlsx"}), encoding="utf-8")
    return source, original, manifest1, phase2, manifest2, tmp_path / "archive"


def test_raw_is_locked_before_validation_and_validation_failure_preserves_it(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    args = inputs(tmp_path)

    def reject(raw: Path, *unused: Any) -> dict[str, Any]:
        assert raw.read_bytes() == args[0].read_bytes()
        assert (args[-1] / LOCKER.LOCK_NAME).is_file()
        assert raw.stat().st_file_attributes & stat.FILE_ATTRIBUTE_READONLY
        raise AssertionError("fixture schema mismatch")

    monkeypatch.setattr(LOCKER, "validate_phase1", reject)
    result = LOCKER.lock_then_validate(*args)
    assert result["status"] == "FAIL_CLOSED"
    assert result["phase2_release_authorized"] is False
    assert (args[-1] / LOCKER.RAW_NAME).read_bytes() == b"raw bytes"
    assert json.loads((args[-1] / LOCKER.VALIDATION_NAME).read_text())["blocking_error"]
    assert args[0].read_bytes() == b"raw bytes"


def test_existing_evidence_cannot_be_overwritten(tmp_path: Path) -> None:
    args = inputs(tmp_path)
    args[-1].mkdir()
    raw = args[-1] / LOCKER.RAW_NAME
    raw.write_bytes(b"historical")
    with pytest.raises(FileExistsError):
        LOCKER.lock_then_validate(*args)
    assert raw.read_bytes() == b"historical"


def test_a01_manifest_is_rejected_before_copy(tmp_path: Path) -> None:
    args = inputs(tmp_path)
    args[2].write_text(json.dumps({"artifact": "PAPER1_CORE144_D1_HUMAN_A01_PHASE1_V1.xlsx"}))
    with pytest.raises(AssertionError, match="B01 manifest"):
        LOCKER.lock_then_validate(*args)
    assert not args[-1].exists()


def test_no_workbook_authoring_or_ai_annotation() -> None:
    text = SCRIPT.read_text(encoding="utf-8")
    assert ".save(" not in text
    assert "shutil.copyfile(source, raw)" in text
    assert text.index("write_new_json(lock,") < text.index("result[\"phase1\"] = validate_phase1")


def test_public_record_exact_identity_and_individual_gate() -> None:
    text = (CORE / "PAPER1_CORE144_D1_HUMAN_B01_PHASE1_RAW_LOCK_AND_PHASE2_RELEASE_V1.md").read_text(encoding="utf-8")
    assert "df423484092733066cbed628dde7ced0494dcb8a024c16bd35c0f1d9edfcbc6a" in text
    assert "bad9c6459dc163cd085517a8964deac6c950115486d15b4237d7273f8e138cdf" in text
    for value in ("37,202", "523,102", "144/144", "16/16", "B01_PHASE2_RELEASE_AUTHORIZED", "NO_GT"):
        assert value in text
    assert "not adjudication" in text


def test_send_list_includes_workbook_and_chinese_guide_only() -> None:
    text = (CORE / "PAPER1_CORE144_D1_HUMAN_B01_PHASE2_OWNER_SEND_CHECKLIST_V1.md").read_text(encoding="utf-8")
    assert "Send exactly two files" in text
    assert "PAPER1_CORE144_D1_HUMAN_B01_PHASE2_V1.xlsx" in text
    assert "PAPER1_CORE144_HUMAN_PHASE2_ANNOTATION_GUIDE_ZH_V1.md" in text
    assert "PAPER1_CORE144_D1_HUMAN_B01_PHASE2_RETURN_V1.xlsx" in text
    assert "HUMAN-B01_ONLY" in text
    assert "Do not send" in text


def test_parallel_state_preserves_d2_d3_withheld_gate() -> None:
    text = (CORE / "PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V9.md").read_text(encoding="utf-8")
    assert "B01_PHASE2_RELEASE_AUTHORIZED" in text
    assert text.count("Phase2 withheld") == 2
    assert "Not frozen / not executed / not started" in text
