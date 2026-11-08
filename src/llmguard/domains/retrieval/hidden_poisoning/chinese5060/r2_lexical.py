"""Role-blind R2 web chrome detection and length-preserving lexical views."""
from __future__ import annotations

import re

# Require the grouped navigation/download toolbar, never isolated words.
TOOLBAR = re.compile(
    r"(?<!\S)(?:首页[ \t]+首页[ \t]+>[ \t]+)?正文阅读[ \t]+"
    r"下载[ \t]*Word[ \t]+下载[ \t]*PDF[ \t]+扫码下载(?=\s|$)"
)
CUES = re.compile(r"首页|历史沿革|下载|PDF|版本|修订|网站导航|当前位置|版权所有|返回顶部", re.I)


def lexical_view(text: str) -> tuple[str, str, list[tuple[int, int]], int]:
    """Return the class, view, masked Unicode offsets, and rejected mask count."""
    matches = list(TOOLBAR.finditer(text))
    spans = [match.span() for match in matches]
    if not spans:
        return ("AMBIGUOUS" if CUES.search(text) else "NONE", text, [], 0)
    masked = list(text)
    for begin, end in spans:
        masked[begin:end] = " " * (end - begin)
    view = "".join(masked)
    if not view.strip():
        return ("AMBIGUOUS", text, [], len(spans))
    return ("WEB_CHROME_CONFIDENT", view, spans, 0)
