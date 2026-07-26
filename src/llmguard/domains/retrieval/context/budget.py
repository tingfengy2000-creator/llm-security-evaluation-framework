"""Exact Unicode code-point budget checks for deterministic rendered contexts."""

from __future__ import annotations


def fits_context_budget(*, rendered_context: str, max_context_characters: int) -> bool:
    """Return whether the final rendered string fits the approved code-point budget."""

    return len(rendered_context) <= max_context_characters
