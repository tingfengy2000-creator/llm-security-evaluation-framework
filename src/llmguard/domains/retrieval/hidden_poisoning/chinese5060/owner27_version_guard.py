"""Owner27 T1 filters. Input receipts are sealed local paraphrase bindings."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from datetime import date

DATE_CLAIM = re.compile(r"自(\d{4})年(\d{1,2})月(\d{1,2})日(?:起|施行)")
TOP_K = 5


@dataclass(frozen=True)
class Receipt:
    document: str
    content_sha256: str
    lineage: str
    scope: str
    fact: str
    version: str
    start: str
    end: str | None
    normalized_value_sha256: str
    source_uri: str


def visible_date_filter(texts: list[str], when: str) -> tuple[int, ...]:
    """Keep undated text and the latest explicitly claimed in-force date."""
    dates: dict[int, date] = {}
    for i, text in enumerate(texts):
        values: set[date] = set()
        for match in DATE_CLAIM.finditer(text):
            try:
                values.add(date(*map(int, match.groups())))
            except ValueError:
                continue
        if len(values) == 1:
            dates[i] = values.pop()
    cutoff = date.fromisoformat(when)
    current = max((d for d in dates.values() if d <= cutoff), default=None)
    return tuple(i for i in range(len(texts)) if i not in dates or dates[i] == current)


def check_binding(document: str, document_sha256: str, receipt: Receipt) -> bool:
    return (document, document_sha256) == (receipt.document, receipt.content_sha256)


def receipt_filter(
    parent: tuple[int, ...], documents: list[tuple[str, str]], register: dict[str, Receipt],
    when: str, scope: str, mode: str,
) -> tuple[tuple[int, ...], str, tuple[int, ...]]:
    """Only locally bound receipts may restore a rank.

    The simple baseline protects unambiguous, time-valid exact-scope receipts.
    The joint arm also preserves valid adjacent-scope evidence within the same
    lineage when an exact anchor exists. No-scope ignores the scope comparison.
    """
    if mode not in {"simple", "joint", "no_scope"}:
        raise ValueError("UNKNOWN_T1_ARM")
    verified = {i: register[uid] for i, (uid, sha) in enumerate(documents)
                if uid in register and check_binding(uid, sha, register[uid])}
    active = {i: r for i, r in verified.items() if r.start <= when and (r.end is None or when < r.end)}
    anchor = {i: r for i, r in active.items() if r.scope == scope or mode == "no_scope"}
    if not anchor:
        return parent, "NO_APPLICABLE_ANCHOR", ()
    roots = {(r.lineage, r.fact) for r in anchor.values()}
    if len(roots) != 1 or len({r.normalized_value_sha256 for r in anchor.values()}) != 1:
        return parent, "ANCHOR_CONFLICT", ()
    support = dict(anchor)
    if mode == "joint":
        scopes: dict[str, set[str]] = {}
        for r in active.values():
            if (r.lineage, r.fact) in roots:
                scopes.setdefault(r.scope, set()).add(r.normalized_value_sha256)
        if any(len(values) > 1 for values in scopes.values()):
            return parent, "ADJACENT_SCOPE_CONFLICT", ()
        support.update({i: r for i, r in active.items() if (r.lineage, r.fact) in roots})
    # Identity is a lineage binding. Reposts cannot be counted as extra votes.
    supported = tuple(sorted(support))
    restored = tuple(i for i in supported if i not in parent)
    return tuple(sorted(set(parent) | set(supported))), "BOUND_SCOPE_SUPPORT", restored


def sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
