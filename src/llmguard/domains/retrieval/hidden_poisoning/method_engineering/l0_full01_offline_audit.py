"""Offline attribution of sealed FULL01 outputs.

This module does not load a model, call generate, or rewrite a sealed run.
Diagnostic tags explain a failed quote. They never mark that quote valid.
"""
from __future__ import annotations

import hashlib
import html
import json
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any

from .llm_verification import _no_duplicate, locate_quote, parse_output

VALIDATION_PASSED = "VALIDATION_PASSED"
JSON_SYNTAX = "JSON_SYNTAX"
JSON_FIELD_SCHEMA = "JSON_FIELD_SCHEMA"
CITATION_SCHEMA = "CITATION_SCHEMA"
UID_ABSENT = "UID_ABSENT"
QUOTE_TYPE = "QUOTE_TYPE"
QUOTE_NOT_IN_FROZEN_TEXT = "QUOTE_NOT_IN_FROZEN_TEXT"
SUPPORT_REQUIRES_EXTERNAL = "SUPPORT_REQUIRES_EXTERNAL_EVIDENCE"
INTERNAL_CONTRADICT_NEEDS_TWO_SPANS = "INTERNAL_CONTRADICT_NEEDS_TWO_SPANS"
INSUFFICIENT_NEEDS_GAP = "INSUFFICIENT_NEEDS_GAP"
OTHER_ORIGINAL = "OTHER_ORIGINAL_ERROR"
UNAVAILABLE = "UNAVAILABLE"

PRIMARY_CATEGORIES = (
    VALIDATION_PASSED, JSON_SYNTAX, JSON_FIELD_SCHEMA, CITATION_SCHEMA, UID_ABSENT, QUOTE_TYPE,
    QUOTE_NOT_IN_FROZEN_TEXT, SUPPORT_REQUIRES_EXTERNAL, INTERNAL_CONTRADICT_NEEDS_TWO_SPANS,
    INSUFFICIENT_NEEDS_GAP, OTHER_ORIGINAL,
)
ROLES = {"POISON", "CLEAN_CURRENT", "HARD_NEGATIVE"}
STRATA = {"S1", "S2", "S3"}
EXPECTED = {
    "config_lock": "628cd01fe0a26e525b28d0ad2a70afd80ceab7708d12f2a9725ad31de065ba4d",
    "predictions": "be87b3fd4457ee212b43bf2f709ded476858e16beb665705c5996f4089604138",
    "prediction_lock": "fb848531e804eb8a21cd9c8b9540d1f7e72a2c56ce726e4febe3e834474a3026",
    "execution_commit": "830bb5b3eb950f30494c9e3ef6affdcc8efc7dcb",
    "result_commit": "bfc9685e5cdde1757643bd6825e52e34bbc85f52",
}


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_model_json(raw: str) -> Any:
    text = raw.strip()
    if text.startswith("```json\n") and text.endswith("\n```"):
        text = text[8:-4]
    return json.loads(text, object_pairs_hook=_no_duplicate)


def _found(text: str, quote: str) -> bool:
    if locate_quote(text, quote) is not None:
        return True
    decoded = html.unescape(quote)
    return decoded != quote and locate_quote(text, decoded) is not None


def _collapse(value: str) -> str:
    return "".join(ch for ch in html.unescape(value) if not ch.isspace())


def _fold(value: str, digits: bool) -> str:
    chars = []
    for ch in html.unescape(value):
        if ch.isspace() or unicodedata.category(ch).startswith("P"):
            continue
        chars.append("#" if digits and ch.isdigit() else ch)
    return "".join(chars)


def _surface_tag(quote: str, text: str) -> str:
    folded = _fold(quote, False)
    if folded and folded in _fold(text, False):
        return "SURFACE_PUNCTUATION_CHANGE"
    digit_folded = _fold(quote, True)
    if digit_folded and digit_folded in _fold(text, True):
        return "SURFACE_DIGIT_CHANGE"
    quote_collapsed = _collapse(quote)
    text_collapsed = _collapse(text)
    if len(quote_collapsed) >= 8:
        for split in range(4, len(quote_collapsed) - 3):
            left, right = quote_collapsed[:split], quote_collapsed[split:]
            start = text_collapsed.find(left)
            if start < 0:
                continue
            end = text_collapsed.find(right, start + len(left))
            if end > start + len(left):
                return "SURFACE_NONCONTIGUOUS_PARTS"
    return "SURFACE_UNMATCHED"


def _quote_tags(quote: str, uid: str, row: dict[str, Any]) -> list[str]:
    tags = []
    cited = next((doc for doc in row["evidence"] if doc["uid"] == uid), None)
    for doc in row["evidence"]:
        if doc["uid"] == uid:
            continue
        if _found(doc["text"], quote):
            tags.append("EXACT_OR_PARSER_EQUIVALENT_IN_OTHER_EVIDENCE")
            break
    if cited is not None:
        meta = json.dumps({k: cited[k] for k in ("title", "official_url", "document_uid", "metadata")}, ensure_ascii=False)
        if _found(meta, quote) and not _found(cited["text"], quote):
            tags.append("TITLE_OR_METADATA_NOT_TEXT")
        tags.append(_surface_tag(quote, cited["text"]))
    if uid != "CANDIDATE" and _found(row["candidate_text"], quote):
        tags.append("EXACT_OR_PARSER_EQUIVALENT_IN_CANDIDATE")
    return tags


def _uid_tags(uid: Any, row: dict[str, Any]) -> list[str]:
    tags = []
    if not isinstance(uid, str):
        return tags
    if any(uid == doc.get("document_uid") and uid != doc.get("uid") for doc in row["evidence"]):
        tags.append("USED_DOCUMENT_UID")
    if any(uid == doc.get("title") for doc in row["evidence"]):
        tags.append("USED_TITLE_AS_UID")
    if uid.strip() in {"", "Evidence", "EVIDENCE", "E1", "DOC", "文档", "证据"}:
        tags.append("USED_PLACEHOLDER_UID")
    return tags


def classify_output(raw: str, row: dict[str, Any]) -> dict[str, Any]:
    """Return the parser's first error and one exclusive diagnostic category."""
    parsed = parse_output(raw, row)
    tags: list[str] = []
    if parsed["error"] is None:
        category = VALIDATION_PASSED
    else:
        category, value = _load_category(raw)
        if value is not None:
            category = _first_schema_category(value, row, tags)
    if category == JSON_SYNTAX and parsed["model_verdict"] is not None:
        raise RuntimeError("JSON_SYNTAX_MUST_NOT_RECOVER_A_VERDICT")
    if not _agrees(parsed["error"], category):
        raise RuntimeError("CLASSIFIER_PARSER_DISAGREEMENT:" + category)
    return {"parser_error": parsed["error"], "model_verdict": parsed["model_verdict"], "final_verdict": parsed["verdict"], "primary_category": category, "diagnostic_tags": tags}


def _load_category(raw: str) -> tuple[str, Any]:
    try:
        return OTHER_ORIGINAL, load_model_json(raw)
    except json.JSONDecodeError:
        return JSON_SYNTAX, None
    except ValueError as exc:
        if str(exc) == "DUPLICATE_JSON_KEY":
            return JSON_FIELD_SCHEMA, None
        return OTHER_ORIGINAL, None


def _agrees(parser_error: str | None, category: str) -> bool:
    known = {
        "OUTPUT_SCHEMA", "DUPLICATE_JSON_KEY", "MISSING_REASON", "VERDICT_OR_CITATION_SCHEMA",
        "CITATION_SCHEMA", "UNAVAILABLE_EVIDENCE_UID", "QUOTE_NOT_IN_FROZEN_TEXT",
        "SUPPORT_REQUIRES_EXTERNAL_EVIDENCE", "INTERNAL_CONFLICT_NEEDS_TWO_SPANS", "INSUFFICIENT_NEEDS_GAP",
    }
    if parser_error is None:
        return category == VALIDATION_PASSED
    if category == JSON_SYNTAX:
        return parser_error not in known
    if category == OTHER_ORIGINAL:
        return parser_error not in known
    expected = {
        JSON_FIELD_SCHEMA: {"OUTPUT_SCHEMA", "DUPLICATE_JSON_KEY", "MISSING_REASON", "VERDICT_OR_CITATION_SCHEMA"},
        CITATION_SCHEMA: {"CITATION_SCHEMA", "VERDICT_OR_CITATION_SCHEMA"},
        UID_ABSENT: {"UNAVAILABLE_EVIDENCE_UID"},
        QUOTE_TYPE: {"UNAVAILABLE_EVIDENCE_UID"},
        QUOTE_NOT_IN_FROZEN_TEXT: {"QUOTE_NOT_IN_FROZEN_TEXT"},
        SUPPORT_REQUIRES_EXTERNAL: {"SUPPORT_REQUIRES_EXTERNAL_EVIDENCE"},
        INTERNAL_CONTRADICT_NEEDS_TWO_SPANS: {"INTERNAL_CONFLICT_NEEDS_TWO_SPANS"},
        INSUFFICIENT_NEEDS_GAP: {"INSUFFICIENT_NEEDS_GAP"},
    }
    return parser_error in expected.get(category, set())


def _first_schema_category(value: Any, row: dict[str, Any], tags: list[str]) -> str:
    if not isinstance(value, dict) or set(value) != {"verdict", "citations", "reason", "insufficient_reason"}:
        return JSON_FIELD_SCHEMA
    if value.get("verdict") not in {"SUPPORT", "CONTRADICT", "INSUFFICIENT"}:
        return JSON_FIELD_SCHEMA
    if not isinstance(value.get("citations"), list):
        return CITATION_SCHEMA
    if not isinstance(value.get("reason"), str) or not value["reason"].strip() or not isinstance(value.get("insufficient_reason"), str):
        return JSON_FIELD_SCHEMA
    sources = {"CANDIDATE": row["candidate_text"], **{doc["uid"]: doc["text"] for doc in row["evidence"]}}
    spans = []
    for citation in value["citations"]:
        if not isinstance(citation, dict) or set(citation) != {"source_uid", "quote"}:
            return CITATION_SCHEMA
        uid, quote = citation["source_uid"], citation["quote"]
        if uid not in sources:
            tags.extend(_uid_tags(uid, row))
            if not isinstance(quote, str):
                tags.append("QUOTE_TYPE_ALSO_INVALID")
            return UID_ABSENT
        if not isinstance(quote, str):
            return QUOTE_TYPE
        if not _found(sources[uid], quote):
            tags.extend(_quote_tags(quote, uid, row))
            return QUOTE_NOT_IN_FROZEN_TEXT
        found = locate_quote(sources[uid], quote)
        if found is None:
            found = locate_quote(sources[uid], html.unescape(quote))
        spans.append((uid, found[0], found[1]))
    external = [span for span in spans if span[0] != "CANDIDATE"]
    if value["verdict"] == "SUPPORT" and not external:
        return SUPPORT_REQUIRES_EXTERNAL
    if value["verdict"] == "CONTRADICT" and not external and len({(span[1], span[2]) for span in spans}) < 2:
        return INTERNAL_CONTRADICT_NEEDS_TWO_SPANS
    if value["verdict"] == "INSUFFICIENT" and not value["insufficient_reason"].strip():
        return INSUFFICIENT_NEEDS_GAP
    return VALIDATION_PASSED


def displayed_model_verdict(value: str | None) -> str:
    return UNAVAILABLE if value in (None, "") else value


def pair_class(f5_failed: bool, oracle_failed: bool, f5_final: str, oracle_final: str) -> str:
    if f5_failed and oracle_failed:
        return "BOTH_VALIDATION_FAILURE"
    if f5_failed:
        return "F5_ONLY_VALIDATION_FAILURE"
    if oracle_failed:
        return "ORACLE_ONLY_VALIDATION_FAILURE"
    if f5_final != oracle_final:
        return "BOTH_PASS_DIFFERENT_VERDICT"
    return "BOTH_PASS_SAME_VERDICT"
    return UNAVAILABLE if value in (None, "") else value


def select_cases(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Pick at most 12 cases in a fixed priority. Empty slots are skipped."""
    failures = [r for r in records if r["primary_category"] != VALIDATION_PASSED]
    counts = Counter(r["primary_category"] for r in failures)
    ranked = [name for name, _ in sorted(counts.items(), key=lambda item: (-item[1], item[0]))]
    slots: list[tuple[str, Any]] = []
    if ranked:
        slots.append(("largest_failure_poison", lambda r, name=ranked[0]: r["primary_category"] == name and r["role"] == "POISON"))
        slots.append(("largest_failure_legal_negative", lambda r, name=ranked[0]: r["primary_category"] == name and r["role"] in {"CLEAN_CURRENT", "HARD_NEGATIVE"}))
    for name in ranked[1:3]:
        slots.append((f"failure_category:{name}", lambda r, name=name: r["primary_category"] == name))
    for name in (JSON_SYNTAX, UID_ABSENT, QUOTE_TYPE, SUPPORT_REQUIRES_EXTERNAL, INTERNAL_CONTRADICT_NEEDS_TWO_SPANS, INSUFFICIENT_NEEDS_GAP, OTHER_ORIGINAL):
        slots.append((f"category:{name}", lambda r, name=name: r["primary_category"] == name))
    slots.extend([
        ("passed_poison_support", lambda r: r["primary_category"] == VALIDATION_PASSED and r["role"] == "POISON" and r["final_verdict"] == "SUPPORT"),
        ("passed_clean_contradict", lambda r: r["primary_category"] == VALIDATION_PASSED and r["role"] == "CLEAN_CURRENT" and r["final_verdict"] == "CONTRADICT"),
        ("passed_hn_contradict", lambda r: r["primary_category"] == VALIDATION_PASSED and r["role"] == "HARD_NEGATIVE" and r["final_verdict"] == "CONTRADICT"),
        ("pair_f5_only_failure", lambda r: r.get("pair_class") == "F5_ONLY_VALIDATION_FAILURE"),
        ("pair_oracle_only_failure", lambda r: r.get("pair_class") == "ORACLE_ONLY_VALIDATION_FAILURE"),
        ("pair_both_failure", lambda r: r.get("pair_class") == "BOTH_VALIDATION_FAILURE"),
        ("pair_both_pass_different_verdict", lambda r: r.get("pair_class") == "BOTH_PASS_DIFFERENT_VERDICT"),
    ])
    chosen = []
    used = set()
    for rule, predicate in slots:
        if len(chosen) == 12:
            break
        matches = [r for r in records if (r["condition"], r["candidate_id"]) not in used and predicate(r)]
        if not matches:
            continue
        matches.sort(key=lambda r: (r["condition"], r["candidate_id"]))
        pick = matches[0]
        used.add((pick["condition"], pick["candidate_id"]))
        chosen.append({**pick, "selection_rule": rule})
    return chosen
