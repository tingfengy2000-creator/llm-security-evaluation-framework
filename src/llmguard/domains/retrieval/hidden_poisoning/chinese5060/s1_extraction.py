"""S1 single-fact projection over the frozen, rule-based v0.2 extractor."""
from __future__ import annotations

from typing import Any

from . import vesa_guard_v02 as v02

POLICY = "S1_V02_STRICT_SINGLE_SCOPE_V1"


def extract_one(query: str, evidence: str) -> dict[str, Any]:
    """Return an evidenced scalar or an explicit refusal, with no provenance promotion."""
    query_scope = v02.query_scope(query)
    if not query_scope.titles or not query_scope.slots:
        return {"status": "UNKNOWN", "reason": "QUERY_SUBJECT_OR_ATTRIBUTE_NOT_RECOGNIZED"}
    if v02.instruction_spans(evidence):
        return {"status": "UNKNOWN", "reason": "INSTRUCTION_LIKE_TEXT"}
    facts = v02.extract(evidence)
    matched = [fact for fact in facts if v02._slot(fact, query_scope) is not None]
    if not matched:
        return {"status": "UNKNOWN", "reason": (
            "NO_SCALAR_EXTRACTED" if not any(fact.value for fact in facts) else "NO_QUERY_SCOPE_MATCH"
        )}
    keys = {(f.subject, f.attribute, f.value, f.unit, f.version, f.article, f.condition, f.qualifier,
             f.validity) for f in matched}
    if len(keys) != 1:
        return {"status": "UNKNOWN", "reason": "MULTIPLE_SCOPED_FACTS"}
    fact = min(matched, key=lambda f: (f.span.start, f.span.end))
    return {"status": "DECIDED", "subject": fact.subject, "attribute": fact.attribute,
            "value": fact.value, "unit": fact.unit, "version": fact.version,
            "effective_from": fact.validity[0] if fact.validity else None,
            "effective_to": fact.validity[1] if fact.validity else None,
            "condition": fact.condition, "scope": {"article": fact.article, "jurisdiction": None},
            "negation": False, "exception": None, "qualifier": fact.qualifier,
            "source_span": {"start": fact.span.start, "end": fact.span.end},
            "provenance": "UNVERIFIED_TEXT_ONLY"}
