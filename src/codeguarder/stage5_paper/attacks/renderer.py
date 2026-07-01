from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass


TURN_MARKER = re.compile(r"\[\[TURN:([A-Za-z_-]+)\]\]")


class PromptRenderError(ValueError):
    """Raised when the constrained multi-turn DSL is invalid."""


@dataclass(frozen=True)
class RenderedPrompt:
    messages: tuple[dict[str, str], ...]
    canonical_prompt_json: str
    prompt_hash: str
    turn_count: int


def render_prompt(prompt: str) -> RenderedPrompt:
    markers = list(TURN_MARKER.finditer(prompt))
    if not markers:
        if "[[TURN:" in prompt:
            raise PromptRenderError("invalid turn marker")
        messages = ({"role": "user", "content": prompt},)
    else:
        if prompt[: markers[0].start()].strip():
            raise PromptRenderError("text before first turn is not allowed")
        turns = []
        for index, marker in enumerate(markers):
            role = marker.group(1).lower()
            if role not in {"user", "assistant"}:
                raise PromptRenderError(f"unsupported role: {role}")
            end = markers[index + 1].start() if index + 1 < len(markers) else len(prompt)
            content = prompt[marker.end() : end]
            if not content.strip():
                raise PromptRenderError("turn cannot be empty")
            turns.append({"role": role, "content": content})
        messages = tuple(turns)
    canonical = json.dumps(
        messages, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )
    return RenderedPrompt(
        messages=messages,
        canonical_prompt_json=canonical,
        prompt_hash=hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
        turn_count=len(messages),
    )
