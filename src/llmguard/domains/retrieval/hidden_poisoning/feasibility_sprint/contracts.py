"""Strict runtime projection and grounded relation checks. No evaluator IO."""
from __future__ import annotations

import hashlib
import json
import re
from typing import Any

from ..method_engineering.llm_verification import check_row

SLOTS = ("subject", "predicate", "value_unit", "scope_condition", "time_version", "source_role")
STATES = {"PRESENT", "NOT_APPLICABLE", "UNKNOWN", "INSUFFICIENT"}
VERDICTS = {"SUPPORT", "CONTRADICT", "INSUFFICIENT"}
F5_SHA = "c849260e2a41fa9186e6d69ed6442cbebdaa7ff272beece9dfadc22e61cf535c"
FORBIDDEN = re.compile(r"(?i)(?:\blabel\b|poison_label|poisoned|stealth_level|\bHKP[-_ ]?[1-4]?\b|human_gt|ground_truth|expected_answer|expected_behavior|attack_id|attack_goal|attack_category|risk_goal|failure_type|\boracle\b|oracle_evidence_mapping|\bS[123]\b)")


def digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def loads(text: str) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in items:
            if key in out:
                raise ValueError("DUPLICATE_JSON_KEY")
            out[key] = value
        return out
    return json.loads(text, object_pairs_hook=pairs, parse_constant=lambda _: (_ for _ in ()).throw(ValueError("NONFINITE_JSON")))


def validate_runtime(row: dict[str, Any]) -> None:
    check_row(row)
    if not isinstance(row["candidate_id"], str) or not row["candidate_id"]:
        raise ValueError("ID_SCHEMA")
    # Scan all retriever-visible strings, including titles, URLs and metadata values.
    def visit(value: Any) -> None:
        if isinstance(value, str):
            if FORBIDDEN.search(value):
                raise ValueError("RUNTIME_LABEL_MARKER")
        elif isinstance(value, dict):
            for k, v in value.items():
                if not isinstance(k, str) or isinstance(v, (list, dict)):
                    raise ValueError("NESTED_METADATA")
                visit(k)
                visit(v)
        elif value is not None and not isinstance(value, (bool, int, float)):
            raise ValueError("METADATA_TYPE")
    visit(row["candidate_text"])
    for doc in row["evidence"]:
        for key, value in doc.items():
            if key == "metadata":
                visit(value)
            else:
                visit(value)


def project(row: dict[str, Any], internal: bool = False) -> dict[str, Any]:
    validate_runtime(row)
    # Do not send even opaque trace IDs: all pairing remains local.
    return {"candidate": {"uid": "CANDIDATE", "text": row["candidate_text"]},
            "evidence": [] if internal else [{"uid": d["uid"], "text": d["text"], "metadata": d["metadata"]} for d in row["evidence"]]}


def grounded_ref(ref: Any, row: dict[str, Any]) -> bool:
    if not isinstance(ref, dict) or set(ref) != {"uid", "quote"}:
        return False
    sources = {"CANDIDATE": row["candidate_text"], **{d["uid"]: d["text"] for d in row["evidence"]}}
    return (isinstance(ref["uid"], str) and ref["uid"] in sources and isinstance(ref["quote"], str)
            and len(ref["quote"].strip()) >= 2 and ref["quote"] in sources[ref["uid"]])


def atom_valid(atom: Any, row: dict[str, Any]) -> bool:
    if not isinstance(atom, dict) or set(atom) != {"id", "ref", "slots"} or not isinstance(atom["id"], str):
        return False
    if not grounded_ref(atom["ref"], row) or not isinstance(atom["slots"], dict) or set(atom["slots"]) != set(SLOTS):
        return False
    for slot in atom["slots"].values():
        if not isinstance(slot, dict) or set(slot) != {"state", "value"}:
            return False
        if slot["state"] not in STATES or not isinstance(slot["value"], str):
            return False
        if slot["state"] == "PRESENT":
            if not slot["value"] or slot["value"] not in atom["ref"]["quote"]:
                return False
        elif slot["value"] != "":
            return False
    return True


def aligned(a: dict[str, Any], b: dict[str, Any]) -> bool:
    for name in SLOTS:
        if name == "value_unit":
            continue
        x, y = a["slots"][name], b["slots"][name]
        if x["state"] != y["state"] or x["state"] not in {"PRESENT", "NOT_APPLICABLE"}:
            return False
        if x["value"] != y["value"]:
            return False
        if name in {"subject", "predicate"} and x["state"] != "PRESENT":
            return False
    return all(z["slots"]["value_unit"]["state"] == "PRESENT" for z in (a, b))


def internal_certificate(value: Any, row: dict[str, Any]) -> bool:
    if not isinstance(value, dict) or value.get("verdict") != "CONTRADICT" or value.get("missing_obligations") != []:
        return False
    atoms = value.get("atoms", [])
    if not isinstance(atoms, list) or len(atoms) != 2 or not all(atom_valid(a, row) for a in atoms):
        return False
    a, b = atoms
    if any(z["ref"]["uid"] != "CANDIDATE" for z in atoms) or a["ref"]["quote"] == b["ref"]["quote"] or not aligned(a, b):
        return False
    # No invented shared context: explicit time and applicability witnesses required.
    if any(a["slots"][s]["state"] != "PRESENT" for s in ("scope_condition", "time_version")):
        return False
    if re.search(r"声称|据称|误称|错误观点|引述|引用|有人认为|表示|[“”\"]", row["candidate_text"]):
        return False
    x, y = (z["slots"]["value_unit"]["value"] for z in atoms)
    if re.search(r"不得不|不能不|并非不|不是不|除非", a["ref"]["quote"] + b["ref"]["quote"]):
        return False
    # Closed, symmetric negation grammar; avoids treating lexical cues as proof.
    if x == "不" + y or y == "不" + x:
        return True
    # Explicit exact quantities only; lower/upper bounds, alternatives and exceptions fail closed.
    if re.search(r"至|到|不低于|不超过|以上|以下|或|例外|除外|可能", a["ref"]["quote"] + b["ref"]["quote"]):
        return False
    pattern = r"(\d+(?:\.\d+)?)(小时|分钟|天|日|年|个月|%|元|人)"
    nx, ny = re.fullmatch(pattern, x), re.fullmatch(pattern, y)
    return bool(nx and ny and nx[2] == ny[2] and float(nx[1]) != float(ny[1])
                and all(re.search(r"固定为|等于|恰为|唯一为", z["ref"]["quote"]) for z in atoms))


def empty_result(error: str | None = None) -> dict[str, Any]:
    return {"raw_model_verdict": None, "final_verdict": "INSUFFICIENT", "evidence_refs": [],
            "supporting_spans": [], "conflicting_spans": [], "missing_obligations": [error] if error else [],
            "route_trace": [], "parser_status": error or "OK"}


def parse_structured(text: str, row: dict[str, Any], internal: bool = False) -> dict[str, Any]:
    out = empty_result()
    try:
        obj = loads(text)
        if not isinstance(obj, dict):
            raise ValueError("JSON_SCHEMA")
        out["raw_model_verdict"] = obj.get("verdict")
        if set(obj) != {"verdict", "atoms", "relations", "coverage_complete", "missing_obligations"}:
            raise ValueError("JSON_SCHEMA")
        if obj["verdict"] not in VERDICTS or type(obj["coverage_complete"]) is not bool:
            raise ValueError("JSON_SCHEMA")
        if not isinstance(obj["missing_obligations"], list) or not all(isinstance(x, str) for x in obj["missing_obligations"]):
            raise ValueError("JSON_SCHEMA")
        if not isinstance(obj["atoms"], list) or not all(atom_valid(a, row) for a in obj["atoms"]):
            raise ValueError("SPAN_OR_SLOT_BINDING")
        ids = [a["id"] for a in obj["atoms"]]
        if len(set(ids)) != len(ids) or not isinstance(obj["relations"], list):
            raise ValueError("ATOM_OR_RELATION_SCHEMA")
        atoms = {a["id"]: a for a in obj["atoms"]}
        support: set[str] = set()
        conflicts: list[dict[str, Any]] = []
        for rel in obj["relations"]:
            if not isinstance(rel, dict) or set(rel) != {"left", "right", "relation", "alignment_checked"}:
                raise ValueError("RELATION_SCHEMA")
            if rel["left"] not in atoms or rel["right"] not in atoms or rel["relation"] not in {"SUPPORT", "CONTRADICT", "UNKNOWN"}:
                raise ValueError("RELATION_SCHEMA")
            if type(rel["alignment_checked"]) is not bool:
                raise ValueError("RELATION_SCHEMA")
            a, b = atoms[rel["left"]], atoms[rel["right"]]
            if a["ref"]["uid"] != "CANDIDATE" or b["ref"]["uid"] == "CANDIDATE":
                continue
            if rel["alignment_checked"] is not True or not aligned(a, b):
                continue
            if rel["relation"] == "CONTRADICT":
                conflicts.extend([a["ref"], b["ref"]])
            elif rel["relation"] == "SUPPORT":
                support.add(a["id"])
        refs = [a["ref"] for a in obj["atoms"]]
        out.update(evidence_refs=refs, missing_obligations=obj["missing_obligations"], structured=obj)
        if internal:
            certified = internal_certificate(obj, row)
            out["certificate_status"] = "INTERNAL_CONTRADICTION_CERTIFIED" if certified else "NO_INTERNAL_CERTIFICATE"
            if certified:
                out.update(final_verdict="CONTRADICT", conflicting_spans=refs)
            # NO_INTERNAL_CERTIFICATE is never SUPPORT.
        elif obj["verdict"] == "CONTRADICT" and conflicts and not obj["missing_obligations"]:
            out.update(final_verdict="CONTRADICT", conflicting_spans=conflicts)
        elif (obj["verdict"] == "SUPPORT" and obj["coverage_complete"] and not obj["missing_obligations"]
              and support and support == {a["id"] for a in obj["atoms"] if a["ref"]["uid"] == "CANDIDATE"} and not conflicts):
            out.update(final_verdict="SUPPORT", supporting_spans=refs)
        elif obj["verdict"] != "INSUFFICIENT":
            out["missing_obligations"] = sorted(set(out["missing_obligations"] + ["UNPROVED_RELATION_OR_COVERAGE"]))
    except (ValueError, TypeError, KeyError, AttributeError) as exc:
        status = "JSON_PARSE_ERROR" if isinstance(exc, json.JSONDecodeError) else str(exc) if isinstance(exc, ValueError) else "JSON_SCHEMA"
        out.update(final_verdict="INSUFFICIENT", parser_status=status)
        out["missing_obligations"] = [out["parser_status"]]
    return out
