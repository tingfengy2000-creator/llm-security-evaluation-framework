from __future__ import annotations

import json
import re
from dataclasses import dataclass

from .hash_utils import sha256_text


TURN_MARKER = re.compile(r"\[\[TURN:([A-Za-z_-]+)\]\]")
ALLOWED_ROLES = {"user", "assistant"}


class PromptRenderError(ValueError):
    """Raised when the constrained multi-turn DSL is invalid."""


@dataclass(frozen=True)
class RenderedPrompt:
    messages: tuple[dict[str, str], ...]
    rendered_text: str
    prompt_hash: str


def render_prompt(prompt: str) -> RenderedPrompt:
    markers = list(TURN_MARKER.finditer(prompt))
    if not markers:
        if "[[TURN:" in prompt:
            raise PromptRenderError("invalid turn marker")
        messages = ({"role": "user", "content": prompt},)
    else:
        if prompt[: markers[0].start()].strip():
            raise PromptRenderError("text before first turn marker is not allowed")
        parsed = []
        for index, marker in enumerate(markers):
            role = marker.group(1).lower()
            if role not in ALLOWED_ROLES:
                raise PromptRenderError(f"unsupported turn role: {role}")
            end = markers[index + 1].start() if index + 1 < len(markers) else len(prompt)
            content = prompt[marker.end() : end]
            if not content.strip():
                raise PromptRenderError("turn content cannot be empty")
            parsed.append({"role": role, "content": content})
        messages = tuple(parsed)
    rendered_text = json.dumps(
        messages,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return RenderedPrompt(
        messages=messages,
        rendered_text=rendered_text,
        prompt_hash=sha256_text(rendered_text),
    )
