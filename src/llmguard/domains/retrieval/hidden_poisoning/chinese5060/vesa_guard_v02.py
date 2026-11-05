"""Role-blind v0.2 lexical evidence selection. Text matches confer no source trust."""
from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from collections.abc import Sequence
from dataclasses import asdict, dataclass
from datetime import date
from decimal import Decimal
from itertools import combinations
from typing import Any, TypedDict

from .vesa_guard_v01 import Chunk, Modules, Span

VERSION = "VESA_GUARD_V0.2"
_TITLE = re.compile(r"《([^》\r\n]{2,70})》")
_VERSION = re.compile(r"(?P<year>[12][0-9]{3})\s*年\s*(?P<edition>原版|修订版|修正本|修订|修正|原文|版)")
_DATE = r"[12][0-9]{3}\s*年\s*[0-9]{1,2}\s*月\s*[0-9]{1,2}\s*日"
_EVENT = r"通过|公布|发布|施行|实施|生效|废止"
_EVENT_BEFORE = re.compile(rf"(?P<event>{_EVENT})\s*(?:日期|时间|日)?\s*(?:为|是|于|在|[:：])?\s*(?P<day>{_DATE})")
_EVENT_AFTER = re.compile(rf"(?P<day>{_DATE})\s*(?:起|正式)?\s*(?P<event>{_EVENT})")
_PROPERTY = {
    "monthly_wage": r"(?:全日制)?月最低工资(?:标准)?",
    "hourly_wage": r"(?:非全日制)?小时最低工资(?:标准)?",
    "minimum_wage": r"最低工资(?:标准)?",
    "daily_hours": r"(?:每日|每天)(?:标准)?(?:工作)?(?:时间|时长|工时)?",
    "weekly_hours": r"(?:每周|周)(?:标准)?(?:工作)?(?:时间|时长|工时)",
    "holiday_days": r"放假(?:日数|天数)?|假期天数",
    "ratio": r"(?:比例|比率|占比)(?:上限)?|不得超过[^，,。；;]{0,20}(?=[0-9]+\s*[%％])",
    "amount": r"(?:金额|限额|补助|费用)(?:标准|上限)?",
    "age": r"年龄(?:上限|下限)?",
    "term": r"(?:期限|时限|年限)(?:上限|下限)?",
}
_NUMBER = re.compile(
    r"(?<![0-9.])(?P<value>[0-9]{1,12}(?:\.[0-9]{1,6})?)\s*"
    r"(?P<unit>元\s*[/／]\s*(?:月|小时|日)|元每(?:月|小时|日)|万元|元|小时|工作日|天|日|个月|月|年|岁|人|[%％])"
)
_BOUNDARY = re.compile(r"[^。！？；;!?]+")
_CONDITION = re.compile(r"(?:仅限|只有|除非|例外|但不|除外|如果|若|凡|对于|不适用|未满|达到|符合|条件|且)")
_EXPLICIT_CONDITION = re.compile(r"在([^，,。；;]{1,30})条件下|(?:若|如果)([^，,。；;]{1,30})[，,]")
_INTERVAL = re.compile(rf"自(?P<start>{_DATE})起?\s*至(?P<end>{_DATE})(?:止|有效|期间)")
_NEGATION = re.compile(r"不再|不得|不能|并非|不是|没有|未能|未曾|未|不")
_ORDER = re.compile(r"不得超过|不超过|至多|上限|至少|不低于|下限")
_ARTICLE = re.compile(r"第\s*[0-9零一二三四五六七八九十百]+\s*条")
_DIRECTIVE = re.compile(
    r"(?:忽略|无视|绕过|覆盖|不要遵守).{0,20}(?:系统|上文|之前|先前|规则|指令|提示)"
    r"|(?:系统|开发者)(?:提示|指令|消息)\s*[:：]"
    r"|(?:请|必须|务必|直接|只需).{0,12}(?:泄露|泄漏|公开|输出|显示).{0,20}(?:系统提示|密钥|隐藏|内部|引用原文)"
    r"|(?:你是|你现在是).{0,10}(?:系统|管理员|开发者)"
    r"|<\|(?:system|developer|im_start)\|>", re.IGNORECASE,
)
_QUOTE = re.compile(r"“[^”]+”|「[^」]+」|\"[^\"]+\"")
_DISCUSSION = re.compile(r"例句|示例|分析|讨论|引用|警示|演示")
_QUESTION = re.compile(r"多少|几天|几小时|哪|如何|什么|是否|分别|有何|变化|对比|比较|上限|截止|截至|日期|何时")
_VALIDITY = re.compile(r"有效|效力|适用|施行|废止|失效|现行|目前|截至")
_SPANS = re.compile(rf"{_DATE}|第\s*[0-9零一二三四五六七八九十百]+\s*条|"
                    rf"《[^》\r\n]+》|{_VERSION.pattern}|{_CONDITION.pattern}|{_NEGATION.pattern}")
_COMPACT = re.compile(r"[\s，,。；;：:！？!?]+")
_NOUNS = {name: re.compile(pattern) for name, pattern in _PROPERTY.items()}
_UNITS = {
    "monthly_wage": {"元", "元/月"}, "hourly_wage": {"元", "元/小时"},
    "minimum_wage": {"元", "元/月", "元/小时"}, "daily_hours": {"小时"}, "weekly_hours": {"小时"},
    "holiday_days": {"日", "天", "工作日"}, "ratio": {"%"}, "amount": {"元", "万元"},
    "age": {"岁"}, "term": {"小时", "工作日", "天", "日", "个月", "月", "年"},
}
_EVENTS = {"发布": "公布", "实施": "施行", "生效": "施行"}
_MAX_GAP = 36
_MAX_RESTORES = 1
# Rule data and the source are pinned separately by the offline adapter.
RULE_SHA = hashlib.sha256(json.dumps({
    "version": VERSION, "property": _PROPERTY, "event_alias": _EVENTS, "gap": _MAX_GAP,
    "max_restore": _MAX_RESTORES, "priority": "original_rank_then_id",
    "patterns": [p.pattern for p in (_TITLE, _VERSION, _EVENT_BEFORE, _EVENT_AFTER, _NUMBER, _BOUNDARY,
        _CONDITION, _EXPLICIT_CONDITION, _INTERVAL, _NEGATION, _ORDER, _ARTICLE,
        _DIRECTIVE, _QUOTE, _DISCUSSION, _QUESTION, _VALIDITY, _SPANS, _COMPACT)],
    "trust": "NO_TRUST_CLAIM", "risk": "BLOCK_EXPLICIT_AND_UNRESOLVED_SLOT_CONFLICT",
    "units": {key: sorted(units) for key, units in _UNITS.items()}, "modules": asdict(Modules()),
}, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def _span(text: str, start: int, end: int) -> Span:
    return Span(start, end, hashlib.sha256(text[start:end].encode()).hexdigest())


def _compact(text: str) -> str:
    return _COMPACT.sub("", unicodedata.normalize("NFKC", text))


def _titles(text: str) -> tuple[str, ...]:
    return tuple(dict.fromkeys(_compact(m[1]).replace("〈", "").replace("〉", "") for m in _TITLE.finditer(text)))


def _version(text: str) -> str | None:
    found = {
        m["year"] + ({"修订": "修订版", "修正": "修订版", "修正本": "修订版", "原文": "原版"}.get(m["edition"], m["edition"]))
        for m in _VERSION.finditer(text)
    }
    return next(iter(found)) if len(found) == 1 else None


def _calendar(text: str) -> str | None:
    try:
        return date(*(int(s) for s in re.findall(r"\d+", text))).isoformat()
    except ValueError:
        return None


def _condition(text: str) -> str | None:
    explicit = list(_EXPLICIT_CONDITION.finditer(text))
    if len(explicit) == 1 and not _CONDITION.search(_EXPLICIT_CONDITION.sub("", text)):
        return _compact(explicit[0][1] or explicit[0][2])
    return None if _CONDITION.search(text) else ""


@dataclass(frozen=True)
class Fact:
    attribute: str
    value: str
    unit: str
    subject: str | None
    version: str | None
    article: str | None
    condition: str | None
    qualifier: str
    span: Span
    validity: tuple[str, str] | None


@dataclass(frozen=True)
class QueryScope:
    titles: tuple[str, ...]
    slots: tuple[str, ...]
    versions: tuple[str, ...]
    article: str | None
    condition: str | None
    date_sensitive: bool
    as_of: str | None
    bound: str | None
    spans: tuple[Span, ...]


class ChunkTrace(TypedDict):
    chunk_id: str
    facts: list[dict[str, Any]]
    instruction_spans: tuple[Span, ...]
    query_slots: list[str]
    coverage_gain_against_b2: list[str]
    risk: str
    reason: str
    provenance: str
    trust: str


@dataclass(frozen=True)
class Decision:
    retained_chunk_ids: tuple[str, ...]
    removed_ids: tuple[str, ...]
    restored_ids: tuple[str, ...]
    query: QueryScope
    covered_before: tuple[str, ...]
    covered_after: tuple[str, ...]
    traces: tuple[ChunkTrace, ...]
    relations: tuple[tuple[str, str, str, str], ...]
    algorithm_version_hash: str = RULE_SHA
    trust: str = "NO_TRUST_CLAIM"


def query_scope(query: str) -> QueryScope:
    titles = _titles(query)
    # A document name is an entity anchor. Its embedded "修改" etc. are not questions.
    outside = _TITLE.sub(" ", query)
    slots: set[str] = set()
    if _QUESTION.search(outside):
        slots.update(name for name, pattern in _NOUNS.items() if pattern.search(outside))
    if re.search(r"日期|时间|何时|何日|哪天|什么时候", outside):
        slots.update("date:" + _EVENTS.get(m[0], m[0]) for m in re.finditer(_EVENT, outside))
    if re.search(r"效力|是否.*(?:有效|废止)|如何.*(?:有效|废止)", outside):
        slots.add("validity")
    if re.search(r"哪些条件|什么条件|例外|是否足以", outside):
        slots.add("condition")
    versions = tuple(dict.fromkeys(v for m in _VERSION.finditer(outside) if (v := _version(m[0])) is not None))
    if len(versions) > 1:
        slots = {slot + "@" + v for slot in slots for v in versions}
    article = _ARTICLE.search(outside)
    as_of = re.search(rf"截至\s*(?P<day>{_DATE})", outside)
    bound = "MAX" if "上限" in outside else "MIN" if "下限" in outside else None
    return QueryScope(titles, tuple(sorted(slots)), versions, _compact(article[0]) if article else None,
                      _condition(outside), bool(re.search(r"截至|现行|目前", outside)),
                      _calendar(as_of["day"]) if as_of else None,
                      bound,
                      tuple(_span(query, *m.span()) for m in _SPANS.finditer(query)))


def instruction_spans(text: str) -> tuple[Span, ...]:
    return tuple(
        _span(text, *match.span()) for match in _DIRECTIVE.finditer(text)
        if not any(q.start() < match.start() and match.end() < q.end()
                   and _DISCUSSION.search(text[max(0, q.start() - 20):q.start()])
                   for q in _QUOTE.finditer(text))
    )


def extract(text: str) -> tuple[Fact, ...]:
    facts = []
    intervals = list(_INTERVAL.finditer(text))
    validity: tuple[str, str] | None = None
    if len(intervals) == 1 and len(_titles(text)) == 1 and len(tuple(_VERSION.finditer(text))) <= 1:
        start_day, end_day = (_calendar(intervals[0][field]) for field in ("start", "end"))
        if start_day is not None and end_day is not None and start_day <= end_day:
            validity = (start_day, end_day)
    inherited_subject: str | None = None
    inherited_version: str | None = None
    inherited_article: str | None = None
    for boundary in _BOUNDARY.finditer(text):
        clause = boundary[0]
        titles = _titles(clause)
        articles = {_compact(m[0]) for m in _ARTICLE.finditer(clause)}
        article = next(iter(articles)) if len(articles) == 1 else inherited_article if not articles else None
        has_version = bool(_VERSION.search(clause))
        explicit_version = _version(clause)
        subject = titles[0] if len(titles) == 1 else inherited_subject if not titles else None
        if titles and subject != inherited_subject:
            inherited_version = inherited_article = None
            if not articles:
                article = None
        version = explicit_version if has_version else inherited_version
        inherited_subject = subject
        inherited_version, inherited_article = version, article
        condition = _condition(clause)
        offset = boundary.start()
        for pattern in (_EVENT_BEFORE, _EVENT_AFTER):
            for m in pattern.finditer(clause):
                value = _calendar(m["day"])
                if value is None:
                    continue
                prefix = clause[max(0, m.start() - 8):m.start()]
                qualifier = "NEGATED" if _NEGATION.search(prefix) else "ASSERTED"
                event = _EVENTS.get(m["event"], m["event"])
                facts.append(Fact("date:" + event, value, "DATE", subject, version, article, condition,
                                  qualifier, _span(text, offset + m.start(), offset + m.end()), validity))
        for n in _NUMBER.finditer(clause):
            if n["unit"] in ("年", "月", "日") and any(m.start() <= n.start() < m.end()
                                                     for m in re.finditer(_DATE, clause)):
                continue
            unit = unicodedata.normalize("NFKC", n["unit"]).replace(" ", "").replace("每", "/")
            anchors = [
                (name, m.start(), m.end()) for name, pattern in _NOUNS.items()
                if unit in _UNITS[name]
                for m in pattern.finditer(clause, max(0, n.start() - _MAX_GAP), n.start())
            ]
            if not anchors and unit == "%" and _ORDER.search(clause[:n.start()]):
                anchors = [("ratio", n.start(), n.start())]
            if not anchors:
                continue
            attribute, start, end = max(anchors, key=lambda a: (a[2], a[2] - a[1], a[0]))
            prefix = clause[max(0, min(start, n.start()) - 6):n.start()]
            bound = _ORDER.search(prefix)
            without_bound = prefix if bound is None else prefix[:bound.start()] + prefix[bound.end():]
            if _NEGATION.search(without_bound):
                qualifier = "NEGATED"
            elif bound is not None:
                qualifier = "MIN" if bound[0] in ("至少", "不低于", "下限") else "MAX"
            else:
                qualifier = "ASSERTED"
            value = format(Decimal(n["value"]).normalize(), "f")
            facts.append(Fact(attribute, value, unit, subject, version, article, condition, qualifier,
                              _span(text, offset + start, offset + n.end()), validity))
        # Conditions and validity are observable, but prose alone cannot fill a scalar query slot.
        if _CONDITION.search(clause) or _VALIDITY.search(clause):
            facts.append(Fact("condition" if _CONDITION.search(clause) else "validity", "", "", subject,
                              version, article, condition, "OBSERVED_ONLY",
                              _span(text, boundary.start(), boundary.end()), validity))
    return tuple(dict.fromkeys(facts))


def _subject_match(subject: str | None, titles: tuple[str, ...]) -> bool:
    return bool(subject is not None and any(
        subject == title or re.fullmatch(r".{0,24}关于修改" + re.escape(title) + "的决定", subject)
        for title in titles
    ))


def _slot(fact: Fact, query: QueryScope) -> str | None:
    if (not fact.value or not _subject_match(fact.subject, query.titles)
            or (query.article is not None and query.article != fact.article)
            or query.condition is None or query.condition != fact.condition
            or (query.date_sensitive and (query.as_of is None or fact.validity is None
                                          or not fact.validity[0] <= query.as_of <= fact.validity[1]))
            or fact.qualifier == "NEGATED" or (query.bound is not None and query.bound != fact.qualifier)):
        return None
    if query.versions and fact.version not in query.versions:
        return None
    name = fact.attribute if len(query.versions) < 2 else fact.attribute + "@" + str(fact.version)
    return name if name in query.slots else None


def _relation(a: Fact, b: Fact) -> str | None:
    if (a.attribute != b.attribute or not a.value or not b.value
            or (a.subject is not None and b.subject is not None and a.subject != b.subject)
            or (a.article is not None and b.article is not None and a.article != b.article)
            or (a.version is not None and b.version is not None and a.version != b.version)):
        return None
    if a.unit != b.unit or a.condition is None or a.condition != b.condition:
        return "UNRESOLVED_SCOPE_OR_UNIT"
    if a.validity is not None and b.validity is not None and (
        a.validity[1] < b.validity[0] or b.validity[1] < a.validity[0]
    ):
        return None
    if a.value == b.value and a.qualifier == b.qualifier:
        return "CORRELATED_OR_UNVERIFIED"
    # Different bounds (e.g. maximum vs observed value) are not the same assertion.
    comparable = (a.subject is not None and a.subject == b.subject and a.version is not None
                  and a.version == b.version and a.article == b.article)
    polarity_conflict = a.value == b.value and {a.qualifier, b.qualifier} == {"ASSERTED", "NEGATED"}
    value_conflict = a.value != b.value and a.qualifier == b.qualifier != "NEGATED"
    return "EXPLICIT_CONFLICT" if comparable and (polarity_conflict or value_conflict) else "UNRESOLVED_SCOPE_OR_UNIT"


def select_v02(
    query: str, topk: Sequence[Chunk], b2_retained: Sequence[str], *, modules: Modules = Modules(),
) -> Decision:
    ids: dict[str, Chunk] = {}
    for rank, c in enumerate(topk, 1):
        if (type(c) is not Chunk or not c.chunk_id or c.chunk_id in ids or c.rank != rank
                or hashlib.sha256(c.text.encode()).hexdigest() != c.content_sha256):
            raise ValueError("V02_INVALID_TOPK")
        ids[c.chunk_id] = c
    if len(ids) > 5 or tuple(b2_retained) != tuple(cid for cid in ids if cid in b2_retained):
        raise ValueError("V02_INVALID_B2_SUBSET")
    scope = query_scope(query)
    facts = {cid: extract(c.text) if modules.scope else () for cid, c in ids.items()}
    instructions = {cid: instruction_spans(c.text) if modules.graph else () for cid, c in ids.items()}
    slots = {cid: {name for f in fs if (name := _slot(f, scope)) is not None} for cid, fs in facts.items()}
    relations = []
    risks: dict[str, set[str]] = {cid: set() for cid in ids}
    asked = {name.split("@")[0] for name in scope.slots}
    for cid, claims in facts.items() if modules.graph else ():
        for a, b in combinations(claims, 2):
            relation = _relation(a, b)
            if a.attribute in asked and (_slot(a, scope) or _slot(b, scope)) and relation in (
                "EXPLICIT_CONFLICT", "UNRESOLVED_SCOPE_OR_UNIT"
            ):
                risks[cid].add(relation)
    for left, right in combinations(ids, 2) if modules.graph else ():
        for a in facts[left]:
            for b in facts[right]:
                relation = _relation(a, b)
                if relation is None:
                    continue
                relations.append((left, right, a.attribute, relation))
                if (a.attribute in asked and (_slot(a, scope) or _slot(b, scope))
                        and relation != "CORRELATED_OR_UNVERIFIED"):
                    risks[left].add(relation)
                    risks[right].add(relation)
    before = set(b2_retained)
    kept = {cid for cid in before if not instructions[cid]}
    covered = set().union(*(slots[cid] for cid in kept))
    restored: list[str] = []
    trace: list[ChunkTrace] = []
    for cid in ids:
        gains = slots[cid] - covered
        outside_version = bool(scope.versions and not slots[cid] and any(
            f.attribute in asked and f.version is not None and f.version not in scope.versions
            and _subject_match(f.subject, scope.titles) for f in facts[cid]
        ))
        if instructions[cid]:
            risk, reason = "HARD_BLOCK", "EXPLICIT_INSTRUCTION_RISK"
        elif "EXPLICIT_CONFLICT" in risks[cid]:
            risk, reason = "HARD_BLOCK", "EXPLICIT_COMPARABLE_CONFLICT"
        elif outside_version:
            risk, reason = "HARD_BLOCK", "EXPLICIT_VERSION_OUTSIDE_QUERY"
        elif risks[cid]:
            risk, reason = "INSUFFICIENT_OR_AMBIGUOUS", "UNRESOLVED_COMPARISON"
        elif not slots[cid]:
            risk, reason = "INSUFFICIENT_OR_AMBIGUOUS", "NO_SCOPED_CONCRETE_QUERY_VALUE"
        elif not gains:
            risk, reason = "CAUTIOUS_RESCUE_CANDIDATE", "NO_INCREMENTAL_COVERAGE"
        elif cid in before:
            risk, reason = "CAUTIOUS_RESCUE_CANDIDATE", "INHERITED_B2"
        elif not (modules.scope and modules.graph and modules.rescue):
            risk, reason = "CAUTIOUS_RESCUE_CANDIDATE", "MODULE_DISABLED"
        elif len(restored) >= _MAX_RESTORES:
            risk, reason = "CAUTIOUS_RESCUE_CANDIDATE", "WORLD_RESCUE_CAP"
        else:
            risk, reason = "CAUTIOUS_RESCUE_CANDIDATE", "RISK_ACCEPTED_NOT_PROVEN_TRUSTED"
            restored.append(cid)
        trace.append({
            "chunk_id": cid, "facts": [asdict(f) for f in facts[cid]], "instruction_spans": instructions[cid],
            "query_slots": sorted(slots[cid]), "coverage_gain_against_b2": sorted(gains),
            "risk": risk, "reason": reason, "provenance": "PROVENANCE_UNVERIFIED", "trust": "NO_TRUST_CLAIM",
        })
    final = kept | set(restored)
    return Decision(tuple(cid for cid in ids if cid in final), tuple(cid for cid in ids if cid not in final),
                    tuple(restored), scope, tuple(sorted(covered)),
                    tuple(sorted(covered | set().union(*(slots[cid] for cid in restored)))),
                    tuple(trace), tuple(relations), RULE_SHA if modules == Modules() else hashlib.sha256(
                        (RULE_SHA + json.dumps(asdict(modules), sort_keys=True)).encode()
                    ).hexdigest())
