"""Role-free projection of the evidence and fields supplied by each frozen rule."""
from __future__ import annotations

import hashlib
from collections.abc import Callable
from typing import Any

FIELDS = ("subject", "attribute", "value", "unit", "version", "effective_from", "effective_to",
          "condition", "scope", "qualifier", "negation", "exception", "provenance")
SCHEMA = "owner20-rule-projection-v1"
INPUT_FIELDS = {"id", "query", "evidence"}
Extract = Callable[[str, str], dict[str, Any]]


def checked_span(evidence: str, span: Any) -> dict[str, Any]:
    if not isinstance(span, dict):
        raise ValueError("INVALID_SPAN_SCHEMA")
    a, b = span.get("start"), span.get("end")
    if type(a) is not int or type(b) is not int or not 0 <= a < b <= len(evidence):
        raise ValueError("INVALID_SPAN_COORDINATES")
    lo, hi = len(evidence[:a].encode()), len(evidence[:b].encode())
    payload = evidence.encode()[lo:hi]
    result = {"start": a, "end": b, "byte_start": lo, "byte_end": hi,
              "sha256": hashlib.sha256(payload).hexdigest()}
    if payload.decode() != evidence[a:b] or any(k in span and span[k] != v for k, v in result.items()):
        raise ValueError("INVALID_SPAN_BYTES")
    return result


def project(raw: dict[str, Any], evidence: str) -> dict[str, Any]:
    status = raw.get("status")
    if status == "UNKNOWN" and isinstance(raw.get("reason"), str):
        return {"status": "UNKNOWN", "reason": raw["reason"]}
    if status != "DECIDED":
        raise ValueError("INVALID_RULE_STATUS")
    chosen = raw.get("source_span")
    primary = checked_span(evidence, chosen) if chosen is not None else None
    spans = [primary] if primary is not None else []
    # Scope spans are included only when the raw trace identifies exactly one
    # selected, nonrejected candidate with the same native fields and scalar span.
    matched = [c for c in raw.get("candidates", [])
               if primary is not None and c["source_span"] == chosen and not c["rejections"]
               and all(c.get(k) == raw.get(k) for k in FIELDS)]
    if len(matched) == 1:
        spans.extend(checked_span(evidence, s) for s in matched[0].get("scope_spans", {}).values())
    # Discard duplicate or nested intervals, retaining only actual reported
    # intervals. Never join touching ranges, expand, relocalize or repair evidence.
    ordered = sorted(spans, key=lambda s: (s["start"], -s["end"]))
    output: list[dict[str, Any]] = []
    for part in ordered:
        if not output or part["end"] > output[-1]["end"]:
            if output and part["start"] < output[-1]["end"]:
                raise ValueError("OVERLAPPING_NATIVE_SPANS")
            output.append(part)
    return {"status": "ANSWER", **{k: raw.get(k) for k in FIELDS}, "spans": output,
            "missing": [k for k in FIELDS if raw.get(k) is None],
            "span_basis": "SELECTED_NATIVE_TRACE" if len(matched) == 1 else "TOP_LEVEL_ONLY"}


def invoke(extractor: Extract, row: dict[str, Any]) -> dict[str, Any]:
    raw = None
    try:
        raw = extractor(row["query"], row["evidence"])
        projected = project(raw, row["evidence"])
    except PermissionError:
        raise
    except Exception as exc:
        projected = {"status": "ERROR", "reason": type(exc).__name__, "detail": str(exc)}
    return {"id": row["id"], "raw": raw, "projection": projected}
