from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


SCRIPT = Path(__file__).parents[2] / "scripts" / "build_pilot2_targeted_rereview.py"
SPEC = importlib.util.spec_from_file_location("pilot2_targeted_builder", SCRIPT)
assert SPEC and SPEC.loader
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)


def test_known_historical_header_aliases_are_canonicalized() -> None:
    source = {
        " sample_id ": "S-01",
        "locally_detectable仅靠当前文本/给定背景能否发现问题\n": "YES",
        "version_relation_correct（版本）": "NO",
        "authority_matches（发布机构）": "YES",
    }
    normalized = BUILDER.normalize_v1_row(source)
    assert normalized["sample_id"] == "S-01"
    assert normalized["locally_detectable"] == "YES"
    assert normalized["version_relation_correct"] == "NO"
    assert normalized["authority_matches"] == "YES"


def test_v1_absent_is_allowed_only_for_three_new_phase2_fields() -> None:
    assert BUILDER.v1_value_for({}, "authority_claim_present", 2) == "[V1_ABSENT]"
    with pytest.raises(RuntimeError, match="unexpected V1 absence"):
        BUILDER.v1_value_for({}, "locally_detectable", 1)
    with pytest.raises(RuntimeError, match="unexpected V1 absence"):
        BUILDER.v1_value_for({}, "authority_matches", 2)


def test_conflicting_aliases_fail_closed() -> None:
    with pytest.raises(RuntimeError, match="conflicting V1 columns"):
        BUILDER.normalize_v1_row(
            {
                "authority_matches": "YES",
                "authority_matches（发布机构）": "NO",
            }
        )
