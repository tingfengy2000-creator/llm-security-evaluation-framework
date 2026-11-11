"""Query-conditioned conflict and evidence retention on a frozen TopK."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date
import re
import unicodedata

from llmguard.domains.retrieval.hidden_poisoning.chinese5060.owner30_auto_eval import (
    integer,
)

ARMS = (
    "NONE",
    "RD_B2",
    "RD_ZH",
    "B2_QUERY_RELEVANCE_ONLY",
    "B2_VISIBLE_DATE_SCOPE_ONLY",
    "Q_CER_FULL",
    "Q_CER_NO_PRESERVATION",
)
CONFIG = {"lexical_bigram_min": 2, "max_restores": 1, "max_isolations": 1, "top_k": 5}
DATE = re.compile(r"(?P<y>\d{4})[-年](?P<m>\d{1,2})[-月](?P<d>\d{1,2})日?")
BOUNDARY = re.compile(r"^.{0,10}(?:起|生效|施行|执行|实施|适用)")
HISTORY = re.compile(r"历史|曾经|此前|旧版|以往|原先|当时|仅供回顾")
PRESENT = re.compile(r"现行|现在|目前|当前|即刻|即日|立即|已生效")
AUTHORITY_CLAIM = re.compile(r"最新|官方|官网|权威|正式发布|紧急更新|以此为准")
PLACE = re.compile(r"北京|上海|天津|重庆|广州|深圳|杭州|南京|苏州|成都|武汉|西安|长沙")
TERM = re.compile(r"大型|中型|小型|普通|残障|残疾|特种|外地|本地|特许|特例")
VALUE = re.compile(
    r"(?<![\d.负])(?P<n>[0-9]+|[零〇一二两三四五六七八九十百千]+)"
    r"(?:个)?(?P<u>周岁|岁|小时|工作日|天|日|个月|月|年|名|人|次|公里|元|吨)(?![\d.])"
)
AUTHORITY = re.compile(
    r"(?:由|向|找)([^，。；]{2,24}(?:机关|部门|机构|委员会|中心|办公室))(?:签发|办理|核发|审批)"
)
TEXT = re.compile(r"[\u4e00-\u9fff]{2,}")
ASK_FILLER = re.compile(
    r"请问|按照|按全国规定|有几天|是多少|是多少岁|是多少年|应找|哪一级|哪类|请说明|什么|多少"
)
SENTENCES = re.compile(r"[。；！？\n]")


@dataclass(frozen=True)
class Query:
    text: str
    event_date: str
    scope: str
    subject: str
    ask: str


@dataclass(frozen=True)
class Segment:
    values: frozenset[str]
    time: str
    scope: str
    bound: bool
    has_claim: bool
    present_claim: bool


@dataclass(frozen=True)
class Decision:
    keep: tuple[int, ...]
    codes: tuple[str, ...]
    sufficiency: str


def norm(text: str) -> str:
    return unicodedata.normalize("NFKC", text).lower()


def grams(text: str) -> set[str]:
    return {s[i : i + 2] for s in TEXT.findall(text) for i in range(len(s) - 1)}


def visible_date(text: str, event: date) -> str:
    dates: list[date] = []
    for match in DATE.finditer(text):
        if not BOUNDARY.search(text[match.end() :]):
            continue
        try:
            dates.append(date(int(match["y"]), int(match["m"]), int(match["d"])))
        except ValueError:
            return "UNKNOWN"
    if len(set(dates)) != 1:
        return "UNKNOWN"
    if HISTORY.search(text):
        return "HISTORICAL"
    return "FUTURE" if dates[0] > event else "APPLICABLE"


def visible_scope(query: Query, text: str) -> str:
    query_text = norm(query.text + " " + query.subject + " " + query.ask)
    q_places = set(PLACE.findall(query_text))
    p_places = set(PLACE.findall(text))
    q_terms = set(TERM.findall(query_text))
    p_terms = set(TERM.findall(text))
    if (q_places and p_places and not (q_places & p_places)) or (
        q_terms and p_terms and not (q_terms & p_terms)
    ):
        return "OTHER"
    return "MATCH" if (q_places & p_places) or (q_terms & p_terms) else "UNKNOWN"


def relevant(query: Query, text: str) -> bool:
    query_grams = grams(ASK_FILLER.sub(" ", norm(query.ask or query.text)))
    subject_grams = grams(norm(query.subject))
    passage_grams = grams(norm(text))
    overlap = query_grams & passage_grams
    return len(overlap) >= CONFIG["lexical_bigram_min"] or bool(
        overlap and subject_grams & passage_grams
    )


def values(text: str) -> frozenset[str]:
    value_text = DATE.sub(" ", text)
    result = set()
    for match in VALUE.finditer(value_text):
        try:
            count = integer(match["n"])
        except ValueError:
            continue
        unit = {"周岁": "岁", "天": "日", "个月": "月"}.get(match["u"], match["u"])
        result.add(f"{count}:{unit}")
    result.update(f"issuer:{match[1]}" for match in AUTHORITY.finditer(text))
    return frozenset(result)


def observe(query: Query, text: str, event: date) -> Segment:
    relevant_sentences = [s for s in SENTENCES.split(norm(text)) if relevant(query, s)]
    assertions = [(s, values(s)) for s in relevant_sentences]
    factual = [(s, v) for s, v in assertions if v]
    if not factual:
        return Segment(frozenset(), "UNKNOWN", "UNKNOWN", False, False, False)
    claims = "。".join(s for s, _ in factual)
    return Segment(
        frozenset().union(*(v for _, v in factual)),
        visible_date(claims, event),
        visible_scope(query, claims),
        True,
        bool(AUTHORITY_CLAIM.search(claims)),
        bool(PRESENT.search(claims)),
    )


def compare(left: frozenset[str], right: frozenset[str]) -> bool:
    """Different values on the same scalar unit or the issuer predicate."""
    return any(
        a != b
        and (
            a.startswith("issuer:")
            and b.startswith("issuer:")
            or a.split(":")[1] == b.split(":")[1]
        )
        for a in left
        for b in right
    )


def filter_world(
    query: Query,
    texts: Sequence[str],
    similarities: Sequence[float],
    b2: tuple[int, ...],
    zh: tuple[int, ...],
    *,
    preserve: bool = True,
) -> Decision:
    if len(texts) != len(similarities) or len(texts) > CONFIG["top_k"]:
        raise ValueError("TOPK_SHAPE")
    event = date.fromisoformat(query.event_date)
    observed = [observe(query, text, event) for text in texts]
    current = [
        i
        for i, x in enumerate(observed)
        if x.bound and x.scope != "OTHER" and x.time not in {"HISTORICAL", "FUTURE"}
    ]
    conflict = any(
        compare(observed[i].values, observed[j].values)
        for i in current
        for j in current
        if i < j
    )
    kept = set(b2)
    codes = ["BASE_KEEP" if i in kept else "BASE_DROP" for i in range(len(texts))]
    for i, item in enumerate(observed):
        if item.scope == "OTHER":
            codes[i] += ":OTHER_SCOPE"
        if item.time == "HISTORICAL":
            codes[i] += ":HISTORICAL"
        if not item.bound or item.scope == "UNKNOWN" or item.time == "UNKNOWN":
            codes[i] += ":UNKNOWN_BINDING"
    if current:
        risky = [
            i
            for i in b2
            if observed[i].bound
            and observed[i].time == "FUTURE"
            and observed[i].scope != "OTHER"
            and observed[i].present_claim
            and any(compare(observed[i].values, observed[j].values) for j in current)
        ]
        for i in risky[: CONFIG["max_isolations"]]:
            kept.remove(i)
            codes[i] = "ISOLATE_SELF_INCONSISTENT_CURRENT_FUTURE"
    if preserve:
        candidates = [
            i
            for i, item in enumerate(observed)
            if i not in b2
            and item.bound
            and len(item.values) == 1
            and not item.has_claim
            and (
                item.time == "HISTORICAL"
                or item.scope == "OTHER"
                and item.time == "APPLICABLE"
                or item.scope == "MATCH"
                and item.time == "APPLICABLE"
                and not conflict
                and any(j in kept and observed[j].values == item.values for j in b2)
            )
        ]
        candidates.sort(key=lambda i: (i not in zh, -similarities[i], i))
        for i in candidates[: CONFIG["max_restores"]]:
            kept.add(i)
            codes[i] = "RESTORE_BOUND_HISTORICAL_OR_QUALIFIED_EVIDENCE"
    supported = any(
        i in kept and observed[i].scope == "MATCH" and observed[i].time == "APPLICABLE"
        for i in current
    )
    return Decision(
        tuple(sorted(kept)),
        tuple(codes),
        "CONFLICT_UNRESOLVED"
        if conflict
        else ("VISIBLE_SUPPORT" if supported else "NO_SUPPORTED_EVIDENCE"),
    )


def query_control(
    query: Query, texts: Sequence[str], b2: tuple[int, ...]
) -> tuple[int, ...]:
    return tuple(i for i in b2 if relevant(query, texts[i]))


def date_scope_control(
    query: Query, texts: Sequence[str], b2: tuple[int, ...]
) -> tuple[int, ...]:
    event = date.fromisoformat(query.event_date)
    return tuple(
        i
        for i in b2
        if visible_date(norm(texts[i]), event) != "FUTURE"
        and visible_scope(query, norm(texts[i])) != "OTHER"
    )
