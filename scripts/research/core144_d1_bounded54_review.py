"""Proposal-only bounded Human annotation review guardrails.

This module validates coverage, enum scope and exact frozen-evidence witnesses.
It does not adjudicate facts or infer an annotator's historical evidence use.
"""
from __future__ import annotations

import hashlib
from typing import Any

from scripts.research.validate_core144_d1_human_phase2_returns import ENUMS

P1_ENUMS = {
    'text_naturalness': {'NATURAL', 'MINOR_ISSUE', 'UNNATURAL'},
    'local_internal_conflict': {'YES', 'NO', 'UNCERTAIN'},
    'self_containment': {'PASS', 'FLAG', 'UNCERTAIN'},
    'ambiguous_referent': {'YES', 'NO', 'UNCERTAIN'},
    'meta_or_template_language': {'YES', 'NO', 'UNCERTAIN'},
}


def validate_coverage(queue: list[dict[str, Any]], review: list[dict[str, Any]],
                      count: int = 54) -> None:
    before = [r['comparison_id'] for r in queue]
    after = [r['comparison_id'] for r in review]
    if len(before) != count or len(set(before)) != count or after != before:
        raise ValueError('Exact bounded queue, unique IDs and original order required')


def check_proposals(proposals: dict[str, str]) -> None:
    legal = {**ENUMS, **P1_ENUMS}
    for field, value in proposals.items():
        if field == 'evidence_selection' or field not in legal or value not in legal[field]:
            raise ValueError('Invalid proposal or forbidden reading-process reconstruction')


def evidence_witness(text: str, anchor: str, before: int = 40,
                     after: int = 220) -> dict[str, Any]:
    """Locate a desk-selected anchor, preserving original bytes in the quote.

    Whitespace removal is used only for locating a passage, never for Candidate
    pairing, raw rewriting, or evidence identity. Report exact original offsets.
    """
    positions = [i for i, c in enumerate(text) if not c.isspace()]
    flat = ''.join(text[i] for i in positions)
    target = ''.join(anchor.split())
    found = flat.find(target)
    if not target or found < 0:
        raise ValueError(f'Frozen witness not found: {anchor}')
    start = max(0, positions[found] - before)
    end = min(len(text), positions[found + len(target) - 1] + after + 1)
    return {'anchor': anchor, 'start': start, 'end': end, 'quote': text[start:end],
            'text_sha256': hashlib.sha256(text.encode('utf-8')).hexdigest()}
