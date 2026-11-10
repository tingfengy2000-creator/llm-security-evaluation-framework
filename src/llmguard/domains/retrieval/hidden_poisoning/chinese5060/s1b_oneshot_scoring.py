"""Post-seal scoring for the unchanged Owner19 protocol. Never invokes a rule."""
from __future__ import annotations

import math
import re
from collections import Counter
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Any

from .s1b_oneshot_adapter import checked_span
from .s1b_feasibility_data import support_matches

CLASSES = ("CORRECT", "WRONG", "UNKNOWN", "ERROR")


def scalar(value: Any, unit: Any) -> tuple[str, str] | None:
    if not isinstance(value, str) or not isinstance(unit, str):
        return None
    try:
        if unit == "DATE":
            return (date.fromisoformat(value).isoformat(), unit) if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value) else None
        number = Decimal(value)
        return (format(number.normalize(), "f"), unit) if number.is_finite() else None
    except (ValueError, InvalidOperation):
        return None


def attribution(pred: dict[str, Any], gold: dict[str, Any], truth: dict[str, Any], evidence: str) -> list[str]:
    """Count observed unsupported decisions with identified wrong-scope/unverified sources separately."""
    identified = []
    for atom in truth["atoms"]:
        if scalar(atom["value"], atom["unit"]) != scalar(pred["value"], pred["unit"]):
            continue
        for span in pred["spans"]:
            a = evidence.rfind("\n", 0, span["start"]) + 1
            b = evidence.find("\n", span["end"])
            line = evidence[a:b if b >= 0 else len(evidence)]
            if all(cue in line for cue in atom["selector"].split("/")):
                identified.append(atom)
                break
    issues = []
    if gold["reason"] == "UNVERIFIED_REVISION" or (
        identified and all(atom["state"] == "U" for atom in identified)
    ):
        issues.append("UNVERIFIED_REVISION_DECISION")
    if identified and all(atom["selector"] != gold["selector"] for atom in identified):
        issues.append("CROSS_SCOPE_DECISION")
    return issues


def score(pred: dict[str, Any], gold: dict[str, Any], truth: dict[str, Any], evidence: str) -> dict[str, Any]:
    for support in gold["accepted_span_sets"]:
        for span in (support["window"], *support["requires"]):
            if checked_span(evidence, span) != span:
                raise ValueError("GOLD_SPAN_IDENTITY")
    answerable = gold["status"] == "ANSWER"
    status = pred["status"]
    result = {"answerable": answerable, "status": status, "value_hit": False, "issues": [],
              "failure_subtype": pred.get("reason"), "scope_proven": False, "span_supported": False}
    if status in {"UNKNOWN", "ERROR"}:
        return result
    if status != "ANSWER":
        raise ValueError("UNSEALED_PREDICTION_SCHEMA")
    observed = scalar(pred["value"], pred["unit"])
    value_hit = answerable and observed is not None and observed == scalar(gold["value"], gold["unit"])
    spans = [checked_span(evidence, span) for span in pred["spans"]]
    coords = [(s["start"], s["end"]) for s in spans]
    supports = [s for s in gold["accepted_span_sets"] if support_matches(coords, s)]
    title = gold["document_title"].removeprefix("《").removesuffix("》")
    issues = []
    if not answerable:
        issues.append("EXPECTED_UNKNOWN_ANSWERED")
    elif not value_hit:
        issues.append("VALUE_OR_UNIT")
    if answerable and title and pred["subject"] not in {None, title}:
        issues.append("SUBJECT_MISMATCH")
    if answerable and not supports:
        issues.append("MISSING_SPAN" if not spans else "SPAN_NOT_IN_ACCEPTED_SUPPORT_SET")
        issues.append("SCOPE_BINDING_UNPROVEN")
    cited = "\n".join(evidence[s["start"]:s["end"]] for s in spans)
    if pred["negation"] is True:
        issues.append("NEGATED_VALUE")
    if answerable and supports:
        for field, values in (
            ("VERSION", [pred["version"]]),
            ("CONDITION_OR_EXCEPTION", [pred["condition"], pred["exception"]]),
            ("SCOPE", list((pred["scope"] or {}).values())),
            ("EFFECTIVE_INTERVAL", [pred["effective_from"], pred["effective_to"]]),
        ):
            if any(isinstance(v, str) and v and v not in cited for v in values):
                issues.append(field + "_UNSUPPORTED")
        selector = gold["selector"]
        if (("最低" in selector and pred["qualifier"] != "MIN") or
                (any(cue in selector for cue in ("最多", "上限")) and pred["qualifier"] != "MAX")):
            # The preregistered support already contains the requested qualifier;
            # absent native qualifier is reported, contrary explicit bound fails.
            if pred["qualifier"] in {"MIN", "MAX"}:
                issues.append("QUALIFIER_MISMATCH")
    if issues:
        issues.extend(attribution(pred, gold, truth, evidence))
    return {**result, "status": "WRONG" if issues else "CORRECT", "value_hit": value_hit, "issues": issues,
            "scope_proven": bool(supports) and not any(
                k in issues for k in ("SUBJECT_MISMATCH", "VERSION_UNSUPPORTED", "CONDITION_OR_EXCEPTION_UNSUPPORTED",
                                      "SCOPE_UNSUPPORTED", "EFFECTIVE_INTERVAL_UNSUPPORTED", "QUALIFIER_MISMATCH")
            ), "span_supported": bool(supports), "failure_subtype": None}


def rate(num: int, den: int) -> dict[str, Any]:
    if not den:
        return {"n": num, "d": den, "point": None, "wilson95": None}
    z = 1.959963984540054
    p = num / den
    scale = 1 + z * z / den
    mid = (p + z * z / (2 * den)) / scale
    half = z * math.sqrt(p * (1 - p) / den + z * z / (4 * den * den)) / scale
    return {"n": num, "d": den, "point": p, "wilson95": [max(0.0, mid - half), min(1.0, mid + half)]}


def metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    counts = Counter(row["status"] for row in rows)
    n = len(rows)
    a = sum(row["answerable"] for row in rows)
    decided = counts["CORRECT"] + counts["WRONG"]
    return {"total": n, "answerable": a, "counts": {key: counts[key] for key in CLASSES},
            "value_hit": rate(sum(row["value_hit"] for row in rows), a),
            "wrong_decided": rate(counts["WRONG"], decided), "wrong_total": rate(counts["WRONG"], n),
            "strict_correct": rate(counts["CORRECT"], n), "coverage": rate(decided, n),
            "abstention": rate(counts["UNKNOWN"], n), "span_supported": rate(sum(r["span_supported"] for r in rows), n),
            "scope_proven": rate(sum(r["scope_proven"] for r in rows), n),
            "missed_answerable": rate(sum(r["answerable"] and r["status"] == "UNKNOWN" for r in rows), a),
            "expected_unknown_wrong": rate(sum(not r["answerable"] and r["status"] == "WRONG" for r in rows), n-a),
            "failure_types": dict(Counter(issue for r in rows for issue in r["issues"])),
            "refusal_and_error_reasons": dict(Counter(r["failure_subtype"] for r in rows if r["failure_subtype"]))}


def summarize(rows: list[dict[str, Any]], pairs: list[dict[str, Any]]) -> dict[str, Any]:
    main = [r for r in rows if r["form"] == "primary"]
    extra = [r for r in rows if r["form"] == "companion"]
    ids = {r["id"]: r for r in rows}
    paired = [(ids[g["primary"]], ids[g["companion"]]) for g in pairs if g["companion"]]
    stats = metrics(main)
    gate = {"value_gate": stats["value_hit"]["n"] >= 63,
            "wrong_gate": stats["wrong_decided"]["d"] > 0 and stats["wrong_decided"]["n"] * 50 <=
                          stats["wrong_decided"]["d"], "no_technical_failure": not any(r["status"] == "ERROR" for r in rows)}
    strata = {}
    for k in ("category", "title", "domain", "family"):
        strata[k] = {value: metrics([r for r in main if r[k] == value]) for value in sorted({r[k] for r in main})}
    worst = min(m["value_hit"]["n"] for m in strata["category"].values())
    return {"main": stats, "companion": metrics(extra), "primary_with_companion": metrics([x for x, _ in paired]),
            "paired_status": dict(Counter(x["status"] + "->" + y["status"] for x, y in paired)),
            "paired_value": dict(Counter(str(x["value_hit"]) + "->" + str(y["value_hit"]) for x, y in paired)),
            "strata": strata, "gate": gate,
            "worst_categories_by_value_hit": [k for k, m in strata["category"].items() if m["value_hit"]["n"] == worst]}
