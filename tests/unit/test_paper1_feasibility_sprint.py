"""Fictional semantic boundaries, route isolation and paid-call safety gates."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any

import pytest

from llmguard.domains.retrieval.hidden_poisoning.feasibility_sprint import api, contracts, prompts, runtime


@pytest.fixture(autouse=True)
def freeze_api_clock(monkeypatch: Any) -> None:
    class FrozenDate(datetime):
        @classmethod
        def now(cls, tz: Any = None) -> datetime:
            return datetime(2026, 11, 3, 3, tzinfo=timezone.utc).astimezone(tz)
    monkeypatch.setattr(api, "datetime", FrozenDate)


def row(text: str | None = None) -> dict[str, Any]:
    candidate = text or "甲社2026年普通岗位补贴固定为5元。甲社2026年普通岗位补贴固定为7元。"
    evidence = "甲社2026年普通岗位补贴固定为5元。"
    return {"candidate_id": "opaque-001", "candidate_text": candidate,
            "evidence": [{"uid": "DOC-01", "document_uid": "DOC-01", "title": "虚构说明", "official_url": "https://fiction.invalid",
                          "text": evidence, "text_sha256": hashlib.sha256(evidence.encode()).hexdigest(), "metadata": {}}]}


def atom(id_: str, quote: str, value: str, uid: str = "CANDIDATE") -> dict[str, Any]:
    values = {"subject": "甲社", "predicate": "补贴", "value_unit": value, "scope_condition": "普通岗位", "time_version": "2026年", "source_role": ""}
    return {"id": id_, "ref": {"uid": uid, "quote": quote}, "slots": {k: {"state": "PRESENT" if v else "NOT_APPLICABLE", "value": v} for k, v in values.items()}}


def internal(r: dict[str, Any]) -> dict[str, Any]:
    quotes = [q + "。" for q in r["candidate_text"].split("。") if q]
    return {"verdict": "CONTRADICT", "atoms": [atom("a", quotes[0], "5元"), atom("b", quotes[1], "7元")],
            "relations": [], "coverage_complete": True, "missing_obligations": []}


def as_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)


def external(r: dict[str, Any], verdict: str = "SUPPORT") -> dict[str, Any]:
    a = atom("a", r["candidate_text"], "5元")
    b = atom("b", r["evidence"][0]["text"], "5元", "DOC-01")
    return {"verdict": verdict, "atoms": [a, b], "relations": [{"left": "a", "right": "b", "relation": verdict, "alignment_checked": True}],
            "coverage_complete": True, "missing_obligations": []}


def test_exact_internal_certificate_and_non_support_without_certificate() -> None:
    r = row()
    result = contracts.parse_structured(as_json(internal(r)), r, internal=True)
    assert result["certificate_status"] == "INTERNAL_CONTRADICTION_CERTIFIED"
    assert result["final_verdict"] == "CONTRADICT"
    obj = internal(r)
    obj["verdict"] = "SUPPORT"
    assert contracts.parse_structured(as_json(obj), r, internal=True)["final_verdict"] == "INSUFFICIENT"


@pytest.mark.parametrize("slot,new", [("subject", "乙社"), ("predicate", "津贴"), ("scope_condition", "特殊岗位"), ("time_version", "2025年"), ("source_role", "公布机关")])
def test_different_bindings_cannot_certify(slot: str, new: str) -> None:
    r = row()
    obj = internal(r)
    obj["atoms"][1]["slots"][slot] = {"state": "PRESENT", "value": new}
    old = {"subject": "甲社", "predicate": "补贴", "scope_condition": "普通岗位", "time_version": "2026年", "source_role": ""}[slot]
    quote = obj["atoms"][1]["ref"]["quote"]
    changed = quote.replace(old, new) if old else new + quote
    r["candidate_text"] = obj["atoms"][0]["ref"]["quote"] + changed
    obj["atoms"][1]["ref"]["quote"] = changed
    assert all(contracts.atom_valid(a, r) for a in obj["atoms"])
    assert not contracts.internal_certificate(obj, r)


@pytest.mark.parametrize("prefix", ["至少", "至多", "不低于", "不超过", "可能", "据称", "引述", "错误观点", "或者"])
def test_compatible_bounds_quoted_views_and_alternatives_not_certified(prefix: str) -> None:
    r = row(prefix + "甲社2026年普通岗位补贴固定为5元。甲社2026年普通岗位补贴固定为7元。")
    assert not contracts.internal_certificate(internal(r), r)


def test_same_keyword_without_exclusion_and_unit_change_fail_closed() -> None:
    r = row("同一甲社2026年普通岗位补贴固定为5元。同一甲社2026年普通岗位补贴固定为5元。")
    obj = internal(r)
    obj["atoms"][1]["slots"]["value_unit"]["value"] = "5元"
    assert not contracts.internal_certificate(obj, r)
    r = row("甲社2026年普通岗位补贴固定为5元。甲社2026年普通岗位补贴固定为7天。")
    obj = internal(r)
    obj["atoms"][1]["slots"]["value_unit"]["value"] = "7天"
    assert not contracts.internal_certificate(obj, r)


def test_literal_negation_is_symmetric() -> None:
    r = row("甲社2026年普通岗位补贴允许领取。甲社2026年普通岗位补贴不允许领取。")
    obj = internal(r)
    for a, value in zip(obj["atoms"], ["允许领取", "不允许领取"], strict=True):
        a["slots"]["value_unit"]["value"] = value
    assert contracts.internal_certificate(obj, r)
    obj["atoms"].reverse()
    assert contracts.internal_certificate(obj, r)


@pytest.mark.parametrize("alternative", ["5元或7元", "5元至7元", "5元到7元"])
def test_ranges_or_alternatives_do_not_become_exact_value_conflicts(alternative: str) -> None:
    r = row(f"甲社2026年普通岗位补贴固定为{alternative}。甲社2026年普通岗位补贴固定为7元。")
    assert not contracts.internal_certificate(internal(r), r)


@pytest.mark.parametrize("state", ["UNKNOWN", "INSUFFICIENT"])
def test_missing_slots_are_never_zero_or_safe(state: str) -> None:
    r = row("甲社2026年普通岗位补贴固定为5元。")
    obj = external(r)
    obj["atoms"][1]["slots"]["time_version"] = {"state": state, "value": ""}
    assert contracts.parse_structured(as_json(obj), r)["final_verdict"] == "INSUFFICIENT"


@pytest.mark.parametrize("damage", ["json", "duplicate", "uid", "quote", "slot", "nan", "coverage", "relationship"])
def test_parser_preserves_failures_and_rejects_forged_proofs(damage: str) -> None:
    r = row("甲社2026年普通岗位补贴固定为5元。")
    obj = external(r)
    if damage == "uid":
        obj["atoms"][1]["ref"]["uid"] = "DOC-MISSING"
    elif damage == "quote":
        obj["atoms"][1]["ref"]["quote"] = "甲社有另一个未提供的事实"
    elif damage == "slot":
        obj["atoms"][1]["slots"]["subject"]["value"] = "伪造主体"
    elif damage == "coverage":
        obj["coverage_complete"] = False
    elif damage == "relationship":
        obj["relations"][0]["alignment_checked"] = False
    text = as_json(obj)
    if damage == "json":
        text = "{bad"
    elif damage == "duplicate":
        text = '{"verdict":"SUPPORT","verdict":"CONTRADICT"}'
    elif damage == "nan":
        text = '{"verdict":NaN}'
    result = contracts.parse_structured(text, r)
    assert result["final_verdict"] == "INSUFFICIENT"
    if damage in {"uid", "quote", "slot", "coverage", "relationship"}:
        assert result["raw_model_verdict"] == "SUPPORT"


def test_valid_joint_evidence_and_legal_history_role_alignment() -> None:
    r = row("甲社2026年普通岗位补贴固定为5元。")
    obj = external(r)
    assert contracts.parse_structured(as_json(obj), r)["final_verdict"] == "SUPPORT"
    # Multiple evidence dependencies must all have real local anchors.
    doc = copy.deepcopy(r["evidence"][0])
    doc["uid"] = "DOC-02"
    r["evidence"].append(doc)
    obj["atoms"].append(atom("c", doc["text"], "5元", "DOC-02"))
    obj["relations"].append({"left": "a", "right": "c", "relation": "SUPPORT", "alignment_checked": True})
    assert contracts.parse_structured(as_json(obj), r)["final_verdict"] == "SUPPORT"
    obj["atoms"][1]["slots"]["time_version"] = {"state": "UNKNOWN", "value": ""}
    obj["atoms"][2]["slots"]["time_version"] = {"state": "UNKNOWN", "value": ""}
    assert contracts.parse_structured(as_json(obj), r)["final_verdict"] == "INSUFFICIENT"


@pytest.mark.parametrize("where", ["root", "metadata", "title", "url", "text"])
def test_recursive_runtime_label_isolation(where: str) -> None:
    r = row()
    if where == "root":
        r["label"] = 1
    elif where == "metadata":
        r["evidence"][0]["metadata"]["issuer"] = "S3"
    elif where == "text":
        r["candidate_text"] += " expected_answer=SUPPORT"
    else:
        r["evidence"][0]["official_url" if where == "url" else "title"] = "https://example.invalid/poison_label"
    with pytest.raises(ValueError):
        prompts.messages(r, "direct")


def test_id_permutation_does_not_change_model_messages() -> None:
    r = row()
    other = copy.deepcopy(r)
    other["candidate_id"] = "another-id"
    assert prompts.messages(r, "direct") == prompts.messages(other, "direct")
    assert prompts.project(r, internal=True)["evidence"] == []


class FakeClient:
    def __init__(self, r: dict[str, Any], certify: bool = True, missing: bool = False):
        self.r, self.certify, self.missing = r, certify, missing
        self.calls: list[str] = []

    def call(self, messages: Any, kind: str, max_output: int, probe: bool = False) -> dict[str, Any]:
        self.calls.append(kind)
        obj: dict[str, Any]
        if kind == "internal":
            obj = internal(self.r) if self.certify else {"verdict": "INSUFFICIENT", "atoms": [], "relations": [], "coverage_complete": False, "missing_obligations": []}
        elif kind == "direct":
            obj = {"verdict": "SUPPORT", "citations": [{"source_uid": "DOC-01", "quote": self.r["evidence"][0]["text"]}], "reason": "虚构测试", "insufficient_reason": ""}
        else:
            obj = {"verdict": "INSUFFICIENT", "atoms": [], "relations": [], "coverage_complete": False,
                   "missing_obligations": ["time_version"] if self.missing else []}
        return {"content": as_json(obj), "call_id": str(len(self.calls)), "input_tokens": 100,
                "output_tokens": 50, "thinking_tokens": None, "latency": .01, "estimated_cost": "0.0001"}


def test_front_end_short_circuit_e4_and_shared_direct_calls() -> None:
    r = row()
    client = FakeClient(r)
    results = runtime.Engine(client).predict(r, e4=True)
    assert client.calls == ["internal", "direct", "structured"]
    assert results["E1"]["final_verdict"] == "SUPPORT"
    assert results["E2"]["final_verdict"] == results["E3"]["final_verdict"] == "CONTRADICT"
    assert results["E4"]["final_verdict"] == "INSUFFICIENT"
    assert results["E2"]["model_calls"] == 1 and results["E4"]["model_calls"] == 1


def test_no_certificate_external_route_and_only_one_gap_check() -> None:
    r = row()
    client = FakeClient(r, certify=False, missing=True)
    results = runtime.Engine(client).predict(r, e4=True)
    assert client.calls == ["internal", "direct", "structured", "followup"]
    assert results["E2"]["final_verdict"] == "SUPPORT"
    assert results["E3"]["final_verdict"] == "INSUFFICIENT"
    assert results["E3"]["model_calls"] == 3
    assert results["E4"]["model_calls"] == 2


def config() -> dict[str, Any]:
    return {"model": api.MODEL, "owner_transfer_authorized": True, "license_and_confidentiality_confirmed": True,
            "official_terms_reviewed": True, "prices_verified": True, "account_region": "ap-northeast-1", "deployment_scope": "Global",
            "base_url": "https://llm-unit-test.ap-northeast-1.maas.aliyuncs.com/compatible-mode/v1",
            "validated_on_jst": "2026-11-03",
            "synthetic_probe_receipt_sha256": "fictional-only"}


def response(*args: Any) -> dict[str, Any]:
    return {"model": api.MODEL, "usage": {"prompt_tokens": 100, "completion_tokens": 20},
            "choices": [{"message": {"content": '{"ok":true}'}, "finish_reason": "stop"}]}


def test_paid_reservation_usage_and_safe_parameters(tmp_path: Path, monkeypatch: Any) -> None:
    monkeypatch.setenv("DASHSCOPE_API_KEY", "fictional-test-key")
    bodies = []
    def transport(base: str, body: Any, key: str) -> dict[str, Any]:
        bodies.append(body)
        return response()
    client = api.PaidClient(tmp_path, config(), transport)
    result = client.call([{"role": "user", "content": "虚构"}], "probe", 64)
    assert client.totals() == (Decimal("0.00004962"), Decimal(0))
    assert result["thinking_tokens"] is None
    assert bodies[0]["enable_thinking"] is False and bodies[0]["enable_search"] is False
    assert "tools" not in bodies[0] and bodies[0]["max_completion_tokens"] == 64


@pytest.mark.parametrize("mutation", ["key", "endpoint", "region", "scope", "model", "date", "license", "probe"])
def test_api_gates_send_nothing(tmp_path: Path, monkeypatch: Any, mutation: str) -> None:
    monkeypatch.setenv("DASHSCOPE_API_KEY", "fictional-test-key")
    cfg = config()
    key = {"endpoint": "base_url", "region": "account_region", "scope": "deployment_scope", "model": "model", "date": "validated_on_jst", "license": "license_and_confidentiality_confirmed", "probe": "synthetic_probe_receipt_sha256"}.get(mutation)
    if key:
        cfg[key] = None
    else:
        monkeypatch.delenv("DASHSCOPE_API_KEY")
    calls = []
    client = api.PaidClient(tmp_path, cfg, lambda *a: calls.append(a) or response())
    with pytest.raises(RuntimeError, match="BLOCKED"):
        client.call([{"role": "user", "content": "fiction"}], "direct", 64)
    assert calls == [] and not list(tmp_path.rglob("reservation.json"))


def test_uncertain_request_stays_reserved_without_retry(tmp_path: Path, monkeypatch: Any) -> None:
    monkeypatch.setenv("DASHSCOPE_API_KEY", "fictional-test-key")
    count = 0
    def timeout(*args: Any) -> Any:
        nonlocal count
        count += 1
        raise TimeoutError("fictional timeout")
    client = api.PaidClient(tmp_path, config(), timeout)
    with pytest.raises(TimeoutError):
        client.call([{"role": "user", "content": "fiction"}], "direct", 64)
    assert client.totals()[1] > 0
    with pytest.raises(RuntimeError, match="UNSETTLED"):
        client.call([{"role": "user", "content": "fiction"}], "direct", 64)
    assert count == 1


def test_hard_cost_gate_and_concurrency(tmp_path: Path, monkeypatch: Any) -> None:
    monkeypatch.setenv("DASHSCOPE_API_KEY", "fictional-test-key")
    api.write_new(tmp_path / "api_calls/old/reservation.json", {"reserved_usd": "4.499"})
    api.write_new(tmp_path / "api_calls/old/receipt.json", {"charged_estimate_usd": "4.499"})
    client = api.PaidClient(tmp_path, config(), lambda *a: pytest.fail("must not send"))
    with pytest.raises(RuntimeError, match="COST_HARD_STOP"):
        client.call([{"role": "user", "content": "fiction"}], "direct", 64)
    (tmp_path / "API_IN_FLIGHT.lock").touch()
    with pytest.raises(RuntimeError, match="CONCURRENT"):
        client.call([{"role": "user", "content": "fiction"}], "direct", 64)


def test_seven_day_hard_stop_cannot_extend_by_new_run(monkeypatch: Any) -> None:
    class Expired(datetime):
        @classmethod
        def now(cls, tz: Any = None) -> datetime:
            return datetime(2026, 11, 10, tzinfo=timezone.utc).astimezone(tz)
    monkeypatch.setattr(api, "datetime", Expired)
    assert "SEVEN_DAY_SPRINT_WINDOW_EXPIRED" in api.gate_issues(config())


@pytest.mark.parametrize("bad", ["thinking", "model", "usage", "length"])
def test_response_deviations_stop_without_fallback(tmp_path: Path, monkeypatch: Any, bad: str) -> None:
    monkeypatch.setenv("DASHSCOPE_API_KEY", "fictional-test-key")
    res = response()
    if bad == "thinking":
        res["choices"][0]["message"]["reasoning_content"] = "unexpected"
    elif bad == "model":
        res["model"] = "alias"
    elif bad == "usage":
        del res["usage"]
    else:
        res["choices"][0]["finish_reason"] = "length"
    client = api.PaidClient(tmp_path, config(), lambda *a: res)
    with pytest.raises(RuntimeError):
        client.call([{"role": "user", "content": "fiction"}], "direct", 64)
    settled, pending = client.totals()
    assert (pending > 0) if bad == "usage" else (settled > 0)


def evaluator_module() -> Any:
    path = Path(__file__).resolve().parents[2] / "scripts/research/evaluate_paper1_feasibility.py"
    spec = importlib.util.spec_from_file_location("sprint_evaluator", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def fictional_results() -> list[dict[str, Any]]:
    rows = []
    for index, role in enumerate(["POISON", "CLEAN_CURRENT", "HARD_NEGATIVE"]):
        rows.append({"candidate_id": str(index), "label": int(role == "POISON"), "derived_s_evaluation_only": "S1", "group_evaluation_only": "fiction-group",
                     "family_evaluation_only": "fiction-family", "role_evaluation_only": role, "final_verdict": "CONTRADICT" if index == 0 else "SUPPORT",
                     "parser_status": "OK", "latency": index + .1, "input_tokens": 1, "output_tokens": 1, "thinking_tokens": None,
                     "model_calls": 1, "estimated_cost": "0.0001"})
    return rows


def test_evaluator_denominators_abstention_and_missing_stratum() -> None:
    mod = evaluator_module()
    data = fictional_results()
    result = mod.summary(data)
    assert result["Strict_Triplet"]["numerator"] == 1
    assert result["S2_Recall"]["rate"] is None
    data[0]["final_verdict"] = "INSUFFICIENT"
    data[0]["parser_status"] = "JSON_SCHEMA"
    result = mod.summary(data)
    assert result["Recall"] == {"numerator": 0, "denominator": 1, "rate": 0, "wilson95": result["Recall"]["wilson95"]}
    assert result["Abstention"]["denominator"] == 3 and result["Precision"]["rate"] is None


def test_paired_family_bootstrap_identical_conditions_zero_difference() -> None:
    mod = evaluator_module()
    data = fictional_results()
    result = mod.paired_bootstrap({c: data for c in ["E1", "E2", "E3", "E4"]}, repetitions=10)
    assert result["differences"]["E3-E1"]["Recall"]["percentile95"] == [0, 0]
    assert result["differences"]["E3-E1"]["S2_Recall"]["valid_replicates"] == 0


def test_decision_does_not_call_backbone_success_a_method_gain() -> None:
    mod = evaluator_module()
    perfect = {key: {"rate": 1., "numerator": 40} for key in ("Recall", "S1_Recall", "S2S3_Recall")}
    perfect.update({key: {"rate": 0., "numerator": 0} for key in ("Clean_FPR", "HN_FPR", "Abstention")})
    perfect.update(Strict_Triplet={"numerator": 40}, logical_execution_cost={"estimated_usd": "1.0"})
    results = {"E1": copy.deepcopy(perfect), "E3": copy.deepcopy(perfect)}
    predictions = {"E1": fictional_results(), "E3": fictional_results()}
    assert mod.decision(results, predictions)["recommendation"] == "CONDITIONAL"
    results["E3"]["logical_execution_cost"]["estimated_usd"] = "0.90"
    assert mod.decision(results, predictions)["recommendation"] == "GO"
    assert mod.decision(results, predictions)["adaptive_independent_comparison_available"] is False


def test_unsealed_evaluator_never_reads_labels(tmp_path: Path) -> None:
    mod = evaluator_module()
    api.write_new(tmp_path / "CONFIG_LOCK.json", {})
    api.write_new(tmp_path / "PREDICTION_LOCK.json", {"config_lock_sha256": "bad"})
    api.write_new(tmp_path / "PREDICTIONS.json", [])
    with pytest.raises(RuntimeError, match="SEAL"):
        mod.evaluate(tmp_path, tmp_path / "labels-never-opened.jsonl", "bad")
    assert not (tmp_path / "EVALUATOR_OPEN.json").exists()


def test_fictional_120_end_to_end_seal_and_independent_evaluator(tmp_path: Path, monkeypatch: Any) -> None:
    """An interface integration test, not real D1 performance evidence."""
    mod = evaluator_module()
    r = row()
    rows, labels = [], []
    for group in range(40):
        for role in ("POISON", "CLEAN_CURRENT", "HARD_NEGATIVE"):
            item = copy.deepcopy(r)
            item["candidate_id"] = f"fiction-{len(rows):03d}"
            rows.append(item)
            labels.append({"candidate_id": item["candidate_id"], "role_evaluation_only": role,
                           "label": int(role == "POISON"), "derived_s_evaluation_only": "S1" if group < 12 else "S2" if group < 27 else "S3",
                           "family_evaluation_only": str(group % 13), "group_evaluation_only": str(group)})
    labels_path = tmp_path / "fictional_labels.jsonl"
    labels_path.write_text("\n".join(as_json(r) for r in labels), encoding="utf-8")
    label_sha = hashlib.sha256(labels_path.read_bytes()).hexdigest()
    frozen = {"source_hashes": {}, "config": {"signed_label_file_sha256": label_sha}}
    api.write_new(tmp_path / "CONFIG_LOCK.json", frozen)
    runtime.predict_all(runtime.Engine(FakeClient(r, certify=False)), rows, tmp_path, contracts.digest(frozen), e4=True)
    assert (tmp_path / "PREDICTION_LOCK.json").exists()
    real_bootstrap = mod.paired_bootstrap
    monkeypatch.setattr(mod, "paired_bootstrap", lambda data: real_bootstrap(data, repetitions=10))
    mod.evaluate(tmp_path, labels_path, label_sha)
    output = contracts.loads((tmp_path / "EXPERIMENT_RESULTS.json").read_text("utf-8"))
    assert set(output["conditions"]) == {"E1", "E2", "E3", "E4"}
    assert output["conditions"]["E1"]["Recall"]["denominator"] == 40
    assert output["conditions"]["E3"]["S2S3_Recall"]["denominator"] == 28
    assert output["decision"]["recommendation"] == "NO-GO"
    with pytest.raises(RuntimeError, match="ALREADY_OPENED"):
        mod.evaluate(tmp_path, labels_path, label_sha)
