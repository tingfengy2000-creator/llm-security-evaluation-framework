from __future__ import annotations

from scripts.research.prepare_pilot4_targeted_r3_packet import (
    BR18_NEW_E1,
    M2_RESULTS,
    M5_REPAIRS,
    M8_ABLATIONS,
    _guide_markdown,
    _matching_score,
    _stable_opaque_id,
)


def test_targeted_repair_scope_is_exactly_frozen() -> None:
    assert len(M2_RESULTS) == 16
    assert list(value for value, _ in M2_RESULTS.values()).count(
        "LEGITIMATE_VERSION_OR_HISTORY"
    ) == 6
    assert list(value for value, _ in M2_RESULTS.values()).count(
        "CURRENTLY_CONSISTENT"
    ) == 10
    assert len(M5_REPAIRS) == 6
    assert len(M8_ABLATIONS) == 4
    assert all(value["joint"] for value in M8_ABLATIONS.values())


def test_guide_v32_contains_frozen_boundary_and_ablation_rules() -> None:
    guide = _guide_markdown()
    assert "当前时点替换测试" in guide
    assert "E1 alone、E2 alone、E1+E2" in guide
    assert guide.count("LEGITIMATE_VERSION_OR_HISTORY` |") == 2
    assert "均非 Pilot4 正式候选" in guide
    assert "expected answer" not in guide.casefold()


def test_r3_ids_are_deterministic_opaque_and_not_attempt_ids() -> None:
    first = _stable_opaque_id("P4Q-example-one")
    second = _stable_opaque_id("P4Q-example-two")
    assert first == _stable_opaque_id("P4Q-example-one")
    assert first != second
    assert first.startswith("R3-")
    assert "P4Q" not in first and "BR-" not in first


def test_control_matching_rewards_all_six_frozen_dimensions() -> None:
    profile = {
        "domain": "D",
        "candidate_class": "C",
        "hkp": "H",
        "intended_stealth": "S",
        "version_claim_present": True,
        "authority_claim_present": False,
    }
    assert _matching_score(profile, profile) == 20
    changed = dict(profile, authority_claim_present=True)
    assert _matching_score(profile, changed) == 18


def test_br18_repair_uses_direct_official_2014_amendment_page() -> None:
    assert BR18_NEW_E1["evidence_id"] == "E1"
    assert "2014年修订" in BR18_NEW_E1["official_page_title"]
    assert ".miit.gov.cn/" in BR18_NEW_E1["official_source_url"]
