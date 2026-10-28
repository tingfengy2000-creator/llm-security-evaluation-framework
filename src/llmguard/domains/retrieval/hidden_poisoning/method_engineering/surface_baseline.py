"""Frozen text-only surface cues; a flag is not a factual verdict or risk probability."""
from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class SurfaceRule:
    rule_id: str
    expression: str
    description: str


# Faithful lexical transcription of the three patterns in the external review.
# Its executable code was not supplied: do not claim byte-identical code reproduction.
ORIGINAL = (
    SurfaceRule("O1", r"既.*(?:又|也)", "既…又/也；ellipsis is non-newline text"),
    SurfaceRule("O2", r"同时又|又是|又享有|同时允许", "four literal alternatives, no added terms"),
    SurfaceRule("O3", r"同一", "literal 同一, not an entity/coreference check"),
)

# Written once from the stated conflict/condition definitions before new scoring.
# Both author and external reviewer have D1 exposure; these are development rules.
GENERAL = (
    SurfaceRule("G1", r"既[^\n]*(?:又|也)|同一[^\n]{0,40}(?:又|同时)", "paired/repeated-subject cue"),
    SurfaceRule("G2", r"(?:同时|又)(?:是|为|享有|允许|禁止|适用|不适用)", "simultaneous/repeated predicate cue"),
    SurfaceRule("G3", r"(?:允许|可以|应当|必须|需要|适用|享有|有效)[^。！？\n]{0,60}(?:不允许|不得|禁止|不应|不需要|不适用|不享有|无效)|(?:不允许|不得|禁止|不应|不需要|不适用|不享有|无效)[^。！？\n]{0,60}(?:允许|可以|应当|必须|需要|适用|享有|有效)", "opposite-polarity cue, without subject binding"),
    SurfaceRule("G4", r"一律|一概|任何|所有|全部|均|始终|从不|绝不|仅限|只有|唯一", "absolute/quantifier cue"),
    SurfaceRule("G5", r"只要|只有|除非|即使|无论|不论|除[^。！？\n]{0,16}外|不受[^。！？\n]{0,16}限制", "condition/exception boundary cue"),
    SurfaceRule("G6", r"无须|无需|不必|并未|不再|不得|不享有|不适用|免于", "negation/exemption cue"),
)
RULE_SETS = {"A0-original": ORIGINAL, "A0-general": GENERAL}


def predict_surface(text: str, rule_set: str) -> tuple[int, tuple[str, ...]]:
    """Deterministic OR, flags=0, no normalization, no trained score or hidden metadata."""
    hits = tuple(rule.rule_id for rule in RULE_SETS[rule_set] if re.search(rule.expression, text, flags=0))
    return int(bool(hits)), hits
