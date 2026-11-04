"""Control-plane provenance gates. Never imported by a defense or generator."""
from __future__ import annotations

from collections.abc import Mapping, Sequence


def validate_world_membership(members: Sequence[str], *, selected: str,
                              lineage: Mapping[str, tuple[str, str]],
                              expected_manifest: Mapping[str, str]) -> None:
    """Check ALL indexed chunks, not just TopK, using independent chunk lineage.

    lineage maps chunk -> (fact group, candidate identity); expected_manifest
    maps each admitted fact group to its sole permitted candidate in this world.
    Background chunks must also be registered (under their own immutable group).
    """
    if not members or len(set(members)) != len(members):
        raise ValueError("EMPTY_OR_DUPLICATE_CORPUS")
    seen: set[str] = set()
    for member in members:
        if member not in lineage:
            raise ValueError("UNKNOWN_CHUNK_LINEAGE")
        group, candidate = lineage[member]
        if expected_manifest.get(group) != candidate:
            raise ValueError("MIXED_OR_UNAUTHORIZED_WORLD")
        seen.add(candidate)
    if selected not in seen:
        raise ValueError("SELECTED_CANDIDATE_ABSENT")
