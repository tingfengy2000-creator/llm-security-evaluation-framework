from __future__ import annotations

import pytest

from llmguard.domains.retrieval.hidden_poisoning import (
    CandidateAdmissionReason,
    CandidateAdmissionStatus,
    SchemaValidationError,
    evaluate_candidate_self_containment,
    require_formal_benchmark_eligibility,
)


def test_future_candidate_with_unique_subject_is_eligible() -> None:
    record = evaluate_candidate_self_containment(
        candidate_id="NEW-001",
        claim_text="修订后的《中华人民共和国职业教育法》自2022年5月1日起施行。",
        subject_mention="《中华人民共和国职业教育法》",
        canonical_subject_identity="中华人民共和国职业教育法",
        subject_uniquely_identifiable=True,
    )
    assert record.status is CandidateAdmissionStatus.ELIGIBLE_FOR_ANNOTATION
    assert record.reason is CandidateAdmissionReason.NONE
    require_formal_benchmark_eligibility(record)


@pytest.mark.parametrize(
    ("claim_text", "subject_mention", "identity", "unique"),
    [
        ("该条例自2024年7月1日起施行。", "条例", None, False),
        ("2017年版已经废止。", "2017年版", None, False),
        ("修订文本于次日生效。", "制度", "某制度", True),
        ("该规定继续有效。", "该规定", "多个可能主体", None),
    ],
)
def test_future_bare_reference_is_broken_candidate(
    claim_text: str,
    subject_mention: str,
    identity: str | None,
    unique: bool | None,
) -> None:
    record = evaluate_candidate_self_containment(
        candidate_id="NEW-BROKEN",
        claim_text=claim_text,
        subject_mention=subject_mention,
        canonical_subject_identity=identity,
        subject_uniquely_identifiable=unique,
    )
    assert record.status is CandidateAdmissionStatus.BROKEN_CANDIDATE
    assert record.reason is CandidateAdmissionReason.MISSING_CONTEXT
    with pytest.raises(SchemaValidationError, match="BROKEN_CANDIDATE / MISSING_CONTEXT"):
        require_formal_benchmark_eligibility(record)


def test_legacy_candidate_is_preserved_but_not_re_admitted() -> None:
    record = evaluate_candidate_self_containment(
        candidate_id="PILOT2-LEGACY",
        claim_text="修订文本已经生效。",
        subject_mention=None,
        canonical_subject_identity=None,
        subject_uniquely_identifiable=None,
        prospective_rule_applied=False,
    )
    assert record.status is CandidateAdmissionStatus.LEGACY_PRESERVED_NOT_REEVALUATED
    assert record.reason is CandidateAdmissionReason.LEGACY_PRE_RULE
    with pytest.raises(SchemaValidationError, match="LEGACY_PRESERVED_NOT_REEVALUATED"):
        require_formal_benchmark_eligibility(record)
