from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CORE = ROOT / "docs/research/stage6_1_hidden_knowledge_poisoning/core144"
RAW_SHA = "d752d27451fcbae9ffba82b6bb33445452ef8b51e35f68877793687216f21b28"
PHASE2_SHA = "76d43b8b48fbab4595b4d561bc09f41046a1ca5cd2f39118fd85de3875baef8a"


def test_a01_raw_lock_record_has_exact_identity_and_boundaries() -> None:
    text = (
        CORE / "PAPER1_CORE144_D1_HUMAN_A01_PHASE1_RAW_LOCK_AND_PHASE2_RELEASE_V1.md"
    ).read_text(encoding="utf-8")
    assert RAW_SHA in text
    assert PHASE2_SHA in text
    assert "36,361" in text
    assert "527,949" in text
    assert "A01_PHASE2_RELEASE_AUTHORIZED" in text
    assert "B01_PHASE2_WITHHELD" in text
    assert "NO_GT" in text
    assert "144 rows" in text
    assert "15 rows" in text


def test_a01_owner_checklist_is_one_file_and_b01_stays_withheld() -> None:
    text = (
        CORE / "PAPER1_CORE144_D1_HUMAN_A01_PHASE2_OWNER_SEND_CHECKLIST_V1.md"
    ).read_text(encoding="utf-8")
    assert text.count(
        "E:\\LLMGuard-Handoff\\paper1_core144_d1_human_phase2_sealed_20260927"
        "\\HUMAN-A01\\PAPER1_CORE144_D1_HUMAN_A01_PHASE2_V1.xlsx"
    ) == 1
    assert PHASE2_SHA in text
    assert "PAPER1_CORE144_D1_HUMAN_A01_PHASE2_RETURN_V1.xlsx" in text
    assert "Send exactly one file" in text
    assert "B01 Phase2 remains `WITHHELD`" in text
    assert "Do not send" in text


def test_lock_script_never_saves_an_openpyxl_workbook() -> None:
    text = (ROOT / "scripts/research/lock_core144_d1_human_phase1_return.py").read_text(
        encoding="utf-8"
    )
    assert "shutil.copyfile(args.source_raw, locked_path)" in text
    assert ".save(" not in text
    assert "Refusing to overwrite existing lock artifact" in text
