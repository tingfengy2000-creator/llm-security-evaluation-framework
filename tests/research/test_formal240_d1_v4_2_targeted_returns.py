"""V4.2 targeted-review raw lock, strict transport, and limited acceptance gate."""

from __future__ import annotations

import hashlib
import json
import os
import runpy
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "docs/research/stage6_1_hidden_knowledge_poisoning/formal240"
SCRIPT = runpy.run_path(str(ROOT / "scripts/research/validate_formal_d1_v4_2_targeted_returns.py"))
RESULT = FORMAL / "PAPER1_FORMAL_D1_CANARY_V4_2_TARGETED_R3_R4_VALIDATION_V1.json"


def test_strict_raw_parser_rejects_duplicate_keys_and_bom() -> None:
    parser = SCRIPT["strict_json"]
    with pytest.raises(ValueError, match="Duplicate JSON key"):
        parser(b'{"blind_review_id":"one","blind_review_id":"two"}')
    with pytest.raises(ValueError, match="BOM"):
        parser(b"\xef\xbb\xbf[]")


def test_validation_artifact_is_complete_and_gate_is_narrow() -> None:
    record = json.loads(RESULT.read_text(encoding="utf-8"))
    assert record["r3_r4_target_value_agreement"] == "15/15"
    assert record["both_match_owner_semantic_overlay"] == "15/15"
    assert record["disagreement_ids"] == record["overlay_mismatch_ids"] == []
    assert record["targeted_rule_status"] == "VERSION_SCOPE_RULE_STABILITY_PASS"
    assert record["case_categories"] == {"bare_substantive": 12, "amendment_decision": 1, "historical_comparison": 2}
    assert len(record["comparison"]) == 15
    assert all(row["r3_r4_agree"] and row["both_match_owner_overlay"] for row in record["comparison"])
    assert "OWNER_ATTESTED" in record["review_run_lineage"]
    assert record["canary_owner_accepted"] is False
    assert record["human_ab_authorized"] is False
    assert all(meta["locked_read_only"] is True for meta in record["raw_files"].values())


def test_source_and_locked_raw_rebuild_exactly_when_available() -> None:
    handoff_root = os.environ.get("PAPER1_HANDOFF_ROOT")
    if handoff_root is None:
        pytest.skip("Private handoff root not supplied to this test environment")
    root = Path(handoff_root)
    lock = root / "paper1_formal240_d1_canary_v4_2_targeted_raw_lock_20260926"
    rebuilt = SCRIPT["build"](root, lock)
    assert rebuilt == json.loads(RESULT.read_text(encoding="utf-8"))
    assert hashlib.sha256(RESULT.read_bytes()).hexdigest() == "b878647ef91405a1ae67b34acc8c86d083ff19de837302b2a831d0b9507a74f6"


def test_no_raw_return_was_committed() -> None:
    for name in (SCRIPT["R3_NAME"], SCRIPT["R4_NAME"]):
        assert not (FORMAL / name).exists()
