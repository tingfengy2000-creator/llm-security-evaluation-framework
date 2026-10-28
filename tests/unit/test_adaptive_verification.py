"""Fictional boundary fixtures; none is a D1 candidate or a teaching GT row."""
from __future__ import annotations

import dataclasses

import pytest

from llmguard.domains.retrieval.hidden_poisoning.method_engineering.adaptive_verification import (
    Evidence, Proof, digest, extract, internal_proof, validate_proof, verify,
)


def doc(text: str, title: str = "甲规范", uid: str = "doc-A") -> Evidence:
    return Evidence(uid, title, text, digest(text), {"current_history_role": "CURRENT"})


def run(text: str, docs: list[Evidence] | None = None, adaptive: bool = True) -> dict:
    return verify({"candidate_id": "opaque-x", "candidate_text": text}, docs or [], adaptive)


@pytest.mark.parametrize("text", [
    "《甲规范》中，同一职工既享受年休假，也不享受年休假。",
    "甲职工享受年休假。甲职工不享受年休假。",
    "《甲规范》中，同一职工每周工作40小时，又每周工作35小时。",
])
def test_true_internal_proof(text: str) -> None:
    result = run(text)
    assert result["verdict"] == "CONTRADICT"
    assert result["internal_early_exit"]
    assert result["evidence_consumed_uids"] == []
    assert result["proofs"]


@pytest.mark.parametrize("text", [
    "《甲规范》中，同一职工享受年休假，也享受婚假。",
    "甲职工今年享受年休假。甲职工明年不享受年休假。",
    "如果参加甲活动，职工享受年休假；如果参加乙活动，职工不享受年休假。",
    "同一职工至少享有5天年休假，也享有10天年休假。",
    "《甲规范》中，旧版每周工作48小时，新版每周工作40小时。",
    "《甲规范》由甲机关通过，由乙机关公布。",
    "有人认为同一职工既享受年休假，也不享受年休假，但这是错误观点。",
    "《甲规范》中，同一单位规定管理岗位每周工作40小时，而生产岗位每周工作35小时。",
])
def test_cue_is_not_contradiction(text: str) -> None:
    assert run(text)["verdict"] == "INSUFFICIENT"


def test_no_proof_is_not_support() -> None:
    assert run("《甲规范》规定可以申请休假。")["verdict"] == "INSUFFICIENT"


def test_typed_numeric_refutation() -> None:
    result = run("《甲规范》规定职工每周工作45小时。", [doc("第三条职工每周工作40小时。")])
    assert result["verdict"] == "CONTRADICT"
    assert result["proofs"][0]["rule_id"] == "F_FUNCTIONAL_SAME_SCOPE_VALUE"


@pytest.mark.parametrize("text", [
    "《甲规范》规定任何特殊岗位职工每周工作45小时。",
    "《乙规范》规定职工每周工作45小时。",
    "《甲规范》规定职工每月工作45小时。",
])
def test_scope_document_unit_binding(text: str) -> None:
    assert run(text, [doc("第三条职工每周工作40小时。")])["verdict"] == "INSUFFICIENT"


def test_conflicting_versions_not_arbitrary_poison() -> None:
    docs = [doc("第三条职工每周工作40小时。"), doc("第三条职工每周工作48小时。", uid="doc-B")]
    assert run("《甲规范》规定职工每周工作45小时。", docs)["verdict"] == "INSUFFICIENT"


def test_exact_payload_support() -> None:
    result = run("《甲规范》第三条规定职工每周工作40小时。", [doc("第三条职工每周工作40小时。第四条另有规定。")])
    assert result["verdict"] == "SUPPORT"


def test_authority_roles_not_host() -> None:
    evidence = doc("(2020年1月1日中华人民共和国国务院令第800号公布)第一条制定本规范。")
    result = run("《甲规范》以人力资源社会保障部令第800号公布。", [evidence])
    assert result["verdict"] == "CONTRADICT"
    assert "P" in [s["module"] for s in result["route_trace"]]
    assert run("《甲规范》由国务院通过。", [evidence])["verdict"] == "INSUFFICIENT"


def test_version_not_in_registry_is_not_false() -> None:
    result = run("《甲规范》2025年版规定每周工作45小时。", [doc("第三条职工每周工作40小时。")])
    assert result["verdict"] == "INSUFFICIENT"


def test_joint_two_premises() -> None:
    evidence = [doc("第三条七级伤残为12个月的本人工资。", "甲规范（2003原版）"), doc("第三条七级伤残为13个月的本人工资。", "甲规范（2010修订）", "doc-B")]
    text = "《甲规范》2003年版至2010年修订版，七级伤残一次性伤残补助金标准有所降低。"
    assert run(text, evidence)["verdict"] == "CONTRADICT"
    assert run(text, evidence[:1])["verdict"] == "INSUFFICIENT"


def test_evidence_order_invariance() -> None:
    docs = [doc("第三条每周工作40小时。"), doc("与休假无关。", "乙规范", "doc-B")]
    a = run("《甲规范》职工每周工作45小时。", docs)
    b = run("《甲规范》职工每周工作45小时。", docs[::-1])
    assert (a["verdict"], a["proofs"]) == (b["verdict"], b["proofs"])


def test_id_and_cache_invariance() -> None:
    text = "甲职工享受年休假。甲职工不享受年休假。"
    a = run(text)
    b = verify({"candidate_id": "arbitrary-other-id", "candidate_text": text}, [], True)
    for key in ("verdict", "proofs", "slots", "internal_early_exit"):
        assert a[key] == b[key]
    assert run("甲职工享受年休假。")["verdict"] == "INSUFFICIENT"


def test_forbidden_metadata_rejected() -> None:
    with pytest.raises(ValueError, match="FORBIDDEN_RUNTIME_FIELDS"):
        verify({"candidate_id": "x", "candidate_text": "text", "label": "poison"}, [], True)


def test_hash_budget_and_certificate_validation() -> None:
    with pytest.raises(ValueError, match="HASH"):
        run("测试", [Evidence("a", "甲", "正文", "wrong")])
    with pytest.raises(ValueError, match="BUDGET"):
        run("测试", [doc("正文", uid=f"d-{i}") for i in range(6)])
    text = "甲职工享受年休假。甲职工不享受年休假。"
    p = internal_proof(extract(text))
    assert isinstance(p, Proof)
    assert validate_proof(p, text, {"candidate": text})
    damaged = dataclasses.replace(p, witnesses=(dataclasses.replace(p.witnesses[0], text="伪造span"),))
    assert not validate_proof(damaged, text, {"candidate": text})


def test_shared_logic_and_nonadaptive_cost_path() -> None:
    text = "甲职工享受年休假。甲职工不享受年休假。"
    a = run(text, [doc("正文")])
    b = run(text, [doc("正文")], False)
    assert a["verdict"] == b["verdict"]
    assert a["proofs"] == b["proofs"]
    assert {"F", "T", "P", "J"} <= {s["module"] for s in b["route_trace"]}
    assert len(b["evidence_consumed_uids"]) == 1


def test_no_a0_required() -> None:
    r = run("甲职工享受年休假。甲职工不享受年休假。")
    assert r["verdict"] == "CONTRADICT"
    assert not any(h["rule_id"].startswith("O") for h in r["a0_cues_only"])


def test_weaker_upper_bound_and_metadata_poison() -> None:
    text = "《甲规范》规定被派遣劳动者数量不得超过其用工总量的20%。"
    assert run(text, [doc("第四条被派遣劳动者数量不得超过其用工总量的10%。")])["verdict"] == "INSUFFICIENT"
    with pytest.raises(ValueError, match="FORBIDDEN_EVIDENCE_METADATA"):
        run("《甲规范》规定职工每周工作45小时。", [Evidence("d", "甲规范", "每周工作40小时。", digest("每周工作40小时。"), {"label": "safe"})])


def test_unknown_currentness_is_not_latest_year() -> None:
    d = Evidence("d", "甲规范", "第三条每周工作40小时。", digest("第三条每周工作40小时。"), {"current_history_role": "UNKNOWN"})
    assert run("《甲规范》规定职工每周工作45小时。", [d])["verdict"] == "INSUFFICIENT"
