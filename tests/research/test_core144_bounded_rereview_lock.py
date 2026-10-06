"""Versioned answers stay separate from raw and automatic release authority."""

from typing import Any

import pytest

from scripts.research.lock_core144_bounded_rereview import (
    merge_prior_view,
    require_source_pairs,
)
from scripts.research.lock_core144_targeted_phase1_returns import validate_targeted


def answer(ident: str, note: str = "") -> dict[str, str]:
    return dict(
        blind_review_id=ident,
        text_naturalness="NATURAL",
        local_internal_conflict="NO",
        self_containment="PASS",
        ambiguous_referent="NO",
        meta_or_template_language="NO",
        issue_note=note,
    )


def test_exact_four_domain_reviewer_pairs() -> None:
    pairs = [
        dict(domain=d, reviewer=r)
        for d in ("D2", "D3")
        for r in ("R3_GPT", "R4_CODEX")
    ]
    require_source_pairs(pairs)
    with pytest.raises(ValueError, match="four distinct"):
        require_source_pairs(pairs + [pairs[0]])
    with pytest.raises(ValueError, match="four distinct"):
        require_source_pairs(pairs[:3])


def test_merge_retains_values_order_and_nested_prior_provenance() -> None:
    prior: list[dict[str, Any]] = [
        dict(answer=answer("old"), source="TARGETED_V1", raw_values_unchanged=True),
        dict(answer=answer("other"), source="ORIGINAL_144_V1"),
    ]
    targeted = [answer("new", "visible reason")]
    merged = merge_prior_view(prior, targeted, [dict(old_id="old", new_id="new")])
    assert merged[0]["answer"] == targeted[0]
    assert merged[0]["superseded_evidence_record"] == prior[0]
    assert merged[1] == prior[1]
    assert prior[0]["answer"]["blind_review_id"] == "old"
    assert merged[0]["source"] == "TARGETED_V2"


def test_merge_fails_closed_on_missing_ancestor_and_incomplete_targets() -> None:
    prior = [dict(answer=answer("old"))]
    with pytest.raises(ValueError, match="ancestor"):
        merge_prior_view(prior, [answer("new")], [dict(old_id="missing", new_id="new")])
    with pytest.raises(ValueError, match="coverage"):
        merge_prior_view(prior, [answer("wrong")], [dict(old_id="old", new_id="new")])


def test_schema_not_overrideable_by_targeted_record_size() -> None:
    packet = [dict(blind_review_id="new", candidate_text="Synthetic teaching text.")]
    with pytest.raises(ValueError, match="count mismatch"):
        validate_targeted(b"[]", packet, dict(record_count=3))
