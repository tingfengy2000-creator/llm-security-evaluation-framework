"""Rule-V2 for evidence-bound Chinese scalar extraction on exposed development fixtures."""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from datetime import date
from decimal import Decimal
from typing import Any

from . import vesa_guard_v02 as v02

SCHEMA = "chinese_scalar_candidates_v1"
POLICY = "S1B_RULE_V2_CLAUSE_SCOPE_03"
_DIGITS = "零〇一二两三四五六七八九"
_CN = _DIGITS + "十百千万"
_NUM = rf"(?:[0-9]+(?:\.[0-9]+)?|[{_CN}]+|半)"
_DAY = re.compile(
    rf"(?P<y>{_NUM})年(?P<m>{_NUM})月(?:(?P<d>{_NUM})日|(?P<period>上旬|中旬|下旬)的第(?P<ordinal>{_NUM})天)"
)
_SCALAR = re.compile(
    rf"百分之(?P<pct>{_NUM})|(?P<value>{_NUM})\s*(?P<unit>个工作日|个昼夜|工作日|昼夜|小时|分钟|秒|个月|万元|元|天|日|"
    r"月|年|岁|%|成|枚|个|卷|件|台|套|人|升)"
)
_PART = re.compile(
    rf"每(?P<base>{_NUM})(?P<unit>个|件|台|枚|人)(?P<object>[^，。；]{{1,12}}?)"
    rf"(?:里|中)(?:留|取|抽取)(?P<part>{_NUM})(?P=unit)"
)
_CLAUSE = re.compile(r"[^，,。；;！？!?\r\n]+")
_FIELD = {
    "daily_hours": r"(?:每日|每天)(?:标准)?(?:工作)?(?:时间|时长|工时)",
    "weekly_hours": r"(?:每周|每星期|周)(?:标准)?(?:工作)?(?:时间|时长|工时)",
    "ratio": r"比例|比率|占比|覆盖率|占(?:多少|几成)",
    "amount": r"金额|费用|租金|押金|补助|多少钱",
    "term": r"期限|时限|年限|时长|多久|几天|几日|几小时|几分钟",
    "quantity": r"(?:多少|几)(?:个|枚|件|台|套|人|卷)",
}
_EVENTS = {
    "施行": r"施行|实施|生效|开始执行",
    "公布": r"发布|公布|公示",
    "通过": r"通过",
    "废止": r"废止|失效",
}
_UNITS = {
    "daily_hours": {"小时"}, "weekly_hours": {"小时"}, "ratio": {"%"}, "amount": {"元", "万元"},
    "term": {"天", "日", "工作日", "小时", "分钟", "秒", "个月", "月", "年"},
    "quantity": {"枚", "个", "卷", "件", "台", "套", "人"},
}
_VERSION = re.compile(rf"{v02._VERSION.pattern}|新册|旧册|换册后")
_REQUESTED_EDITION = re.compile(r"现行|目前|最新版|新版|修订版|修正版|原版|新册|旧册")
_SCOPE = re.compile(r"[\u4e00-\u9fff]{1,6}?(?:分点|分区|分室|分站|分部)|[东南西北中][室馆区]|(?:成人|青少年|儿童|老年)组")
_CONDITION = re.compile(r"在([^，。；]{1,24})条件下|(?:若|如果|遇)([^，。；]{1,24}?)(?:则|$)")
_IMPLICIT = {
    "ratio": re.compile(r"占|百分之"),
    "term": re.compile(r"提前|历时|耗时|需要|等待|允许|晾|时段|只有|倒数|限定"),
    "quantity": re.compile(r"装|放|配|备|有|含|分配"),
}
_INTERVAL = re.compile(r"自(?P<start>[^，。；至]{1,32}?)起?至(?P<end>[^，。；]{1,32}?)(?:止|有效|期间)$")
_UNVERIFIED = re.compile(r"转载|自称|非官方|未附|无(?:任何)?正式|没有(?:任何)?正式|未经证实|据传")
_NEGATION = re.compile(r"不再|不是|并非|未采用|取消|不适用|无效|尚未|没有")
_BOUND = re.compile(r"上限|不超过|不得超过|至多|最高|下限|不低于|至少|最低")
_EXCEPTION = re.compile(r"^(?:但(.+)|(.+时另议))$")
_METADATA = re.compile(r"页脚|页尾|网页(?:时间|更新时间)|历史沿革")
_EDGE = re.compile(r"^(?:(?:里|的|在|中|规定|记载|说明|要求|写明|把|将|注明|载明|明确)\s*)+")
_FORMER = re.compile(r"从(?:过去|此前|先前|原先|原来)的?$")
_REPLACEMENT = re.compile(r"^(?:改为|调整为|变更为)(?:现在|目前|现行)?的?$")
_NAMED_ROLE = re.compile(r"([\u4e00-\u9fff]{0,12}?(?:主持|人员|访客|者|人))(?=的|最低|最高|至少|至多)")
_QUANTITY_OBJECT = re.compile(r"(?:多少|几)(?:个|枚|件|台|套|人|卷)([\u4e00-\u9fff]{1,12})$")
_NAME = re.compile(r"[\u4e00-\u9fff]{2,}")
_UNIT_ALIASES = {"昼夜": "天", "个昼夜": "天", "个工作日": "工作日", "％": "%"}
_CONFIG = {
    "schema": SCHEMA, "policy": POLICY, "fields": _FIELD, "events": _EVENTS,
    "units": {field: sorted(units) for field, units in _UNITS.items()},
    "unit_aliases": _UNIT_ALIASES, "digits": _DIGITS,
    "patterns": {name: pattern.pattern for name, pattern in sorted(globals().copy().items())
                 if isinstance(pattern, re.Pattern)},
    "provenance": "UNVERIFIED_TEXT_ONLY",
    "span": "raw Unicode code points and UTF-8 bytes, half-open",
}
CONFIG_SHA256 = hashlib.sha256(json.dumps(_CONFIG, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def _numeral(text: str) -> Decimal:
    if text == "半":
        return Decimal("0.5")
    if text[0].isascii():
        return Decimal(text)
    digits = {symbol: value for symbol, value in zip(_DIGITS, (0, 0, 1, 2, 2, 3, 4, 5, 6, 7, 8, 9), strict=True)}
    if all(symbol in digits for symbol in text):
        return Decimal("".join(str(digits[symbol]) for symbol in text))
    if "万" in text:
        prefix, _, suffix = text.partition("万")
        if not prefix or "万" in suffix:
            raise ValueError("AMBIGUOUS_NUMERAL")
        return _numeral(prefix) * 10000 + (_numeral(suffix) if suffix else 0)
    total, pending, previous_scale = 0, None, 10000
    for symbol in text:
        if symbol in digits:
            if pending is not None and pending != 0:
                raise ValueError("AMBIGUOUS_NUMERAL")
            pending = digits[symbol]
            continue
        scale = {"十": 10, "百": 100, "千": 1000}[symbol]
        if scale >= previous_scale or pending == 0:
            raise ValueError("AMBIGUOUS_NUMERAL")
        total += (1 if pending is None else pending) * scale
        pending, previous_scale = None, scale
    if pending and previous_scale > 10 and not text.endswith(("零" + text[-1], "〇" + text[-1])):
        raise ValueError("AMBIGUOUS_NUMERAL")
    return Decimal(total + (pending or 0))


def _calendar(match: re.Match[str]) -> str:
    numbers = [_numeral(match[key]) for key in ("y", "m", "d" if match["d"] else "ordinal")]
    if any(number != number.to_integral_value() for number in numbers):
        raise ValueError("FRACTIONAL_CALENDAR_FIELD")
    year, month, ordinal = map(int, numbers)
    if match["d"] is not None:
        return date(year, month, ordinal).isoformat()
    if not 1 <= ordinal <= 10:
        raise ValueError("INVALID_MONTH_SEGMENT")
    day = {"上旬": 0, "中旬": 10, "下旬": 20}[match["period"]] + ordinal
    return date(year, month, day).isoformat()


def _span(raw: str, start: int, end: int) -> dict[str, Any]:
    if not 0 <= start < end <= len(raw):
        raise ValueError("INVALID_EVIDENCE_SPAN")
    value = raw[start:end]
    byte_start = len(raw[:start].encode())
    byte_end = byte_start + len(value.encode())
    if raw.encode()[byte_start:byte_end].decode() != value:
        raise ValueError("INVALID_UTF8_SPAN")
    return {"start": start, "end": end, "byte_start": byte_start, "byte_end": byte_end,
            "sha256": hashlib.sha256(value.encode()).hexdigest()}


def _view(text: str) -> str:
    # Per-code-point normalization is allowed only when it preserves offsets.
    return "".join(norm if len(norm := unicodedata.normalize("NFKC", c)) == 1 else c for c in text)


def _edition(text: str) -> str:
    if text in {"新册", "旧册", "换册后"}:
        return "新册" if text == "换册后" else text
    return v02._version(text) or text


def _place(text: str) -> set[str]:
    return {match[0] for match in _SCOPE.finditer(_EDGE.sub("", text))}


def _condition(text: str) -> str:
    match = _CONDITION.search(text)
    return (match[1] or match[2]) if match else ""


def _bound(text: str) -> str:
    markers = {"MIN" if m[0] in {"下限", "不低于", "至少", "最低"} else "MAX" for m in _BOUND.finditer(text)}
    return next(iter(markers)) if len(markers) == 1 else "CONFLICT" if markers else "ASSERTED"


def _attributes(text: str) -> set[str]:
    found = {key for key, pattern in _FIELD.items() if re.search(pattern, text)}
    if found & {"daily_hours", "weekly_hours"}:
        found.discard("term")
    return found


def _names(text: str) -> set[str]:
    return {m[0] for m in _NAME.finditer(text)}


def _scalar_candidates(text: str) -> list[tuple[int, int, str | None, str]]:
    """Keep invalid and nonmatching numeric observations in the trace, never as decided facts."""
    found: list[tuple[int, int, str | None, str]] = []
    covered: list[tuple[int, int]] = []
    for kind, pattern in (("DATE", _DAY), ("%", _PART), ("", _SCALAR)):
        for match in pattern.finditer(text):
            start, end = match.span()
            if any(start < right and left < end for left, right in covered):
                continue
            covered.append((start, end))
            unit = kind or ("%" if match["pct"] else _UNIT_ALIASES.get(match["unit"], match["unit"]))
            try:
                if kind == "DATE":
                    value = _calendar(match)
                elif pattern is _PART:
                    denominator = _numeral(match["base"])
                    numerator = _numeral(match["part"])
                    if not 0 <= numerator <= denominator or denominator == 0:
                        raise ValueError("INVALID_PART_RATIO")
                    ratio = numerator * 100 / denominator
                    if ratio * denominator != numerator * 100:
                        raise ValueError("INEXACT_PART_RATIO")
                    value = format(ratio.normalize(), "f")
                else:
                    numeric = _numeral(match["pct"] or match["value"])
                    if unit == "成":
                        numeric *= 10
                    value = format(numeric.normalize(), "f")
            except (ArithmeticError, ValueError):
                value = None
            found.append((start, end, value, "%" if unit == "成" else unit))
    return sorted(found)


def _specificity(query: str, context: str, field: str) -> int:
    # Match only complete source cues, or a suffix of one before a field marker.
    # A common numeral or field name alone never resolves a conflict.
    marker = _FIELD.get(field)
    if marker:
        context = re.sub(marker, " ", context)
        query = re.sub(marker, " ", query)
    context = re.sub(r"另(?:收|列)|定在|列为|记为|期限定为|为|是|其|由|明确|写明", " ", _EDGE.sub("", context))
    return max((size for word in _names(context) for size in range(2, len(word) + 1)
                if word[-size:] in query or word[:size] in query), default=0)


def extract_one(query: str, source_original: str, public_schema: str = SCHEMA) -> dict[str, Any]:
    """Return scoped hypotheses with raw spans. No text can establish source authority."""
    evidence = _view(source_original)
    query = _view(query)
    candidates: list[dict[str, Any]] = []
    observations: list[dict[str, Any]] = []
    result = {"candidates": candidates, "observations": observations, "schema": SCHEMA}

    def unknown(reason: str) -> dict[str, Any]:
        return {**result, "status": "UNKNOWN", "reason": reason}

    if public_schema != SCHEMA:
        return unknown("UNKNOWN_PUBLIC_SCHEMA")
    titles = set(v02._titles(query))
    outside = v02._TITLE.sub("", query)
    fields = _attributes(outside)
    if re.search(r"日期|时间|何时|何日|哪天|哪一天|什么时候", outside):
        fields = {"date:" + event for event, pattern in _EVENTS.items() if re.search(pattern, outside)} or fields
    if len(titles) != 1 or len(fields) != 1:
        return unknown("QUERY_SUBJECT_OR_ATTRIBUTE_AMBIGUOUS")
    title, field = next(iter(titles)), next(iter(fields))
    requested = [_edition(m[0]) for m in _VERSION.finditer(outside)]
    versions = set(requested[-1:] if "不同" in outside and requested[-1:] in (["新册"], ["旧册"]) else requested)
    as_of = _DAY.search(outside) if "截至" in outside else None
    try:
        day = _calendar(as_of) if as_of else None
    except ValueError:
        return unknown("INVALID_QUERY_DATE")
    places = _place(outside)
    query_condition = _condition(outside)
    requested_context = _NAMED_ROLE.search(_EDGE.sub("", outside))
    object_match = _QUANTITY_OBJECT.search(outside.rstrip("？?"))
    requested_object = object_match[1] if object_match else None
    if requested_context and not query_condition:
        query_condition = requested_context[1]
    article = v02._ARTICLE.search(outside)
    bound = _bound(outside)
    if len(versions) > 1 or len(places) > 1 or bound == "CONFLICT":
        return unknown("QUERY_SCOPE_AMBIGUOUS")
    if v02.instruction_spans(evidence):
        return unknown("INSTRUCTION_LIKE_TEXT")
    version_sensitive = bool(versions or day or _REQUESTED_EDITION.search(outside))
    if version_sensitive and _UNVERIFIED.search(evidence):
        return unknown("UNVERIFIED_REVISION")
    if not versions and not day and _REQUESTED_EDITION.search(outside):
        return unknown("VERSION_APPLICABILITY_UNBOUND")

    subject: str | None = None
    version: str | None = None
    section: str | None = None
    validity: tuple[str, str] | None = None
    pending_condition = ""
    revision_unverified = False
    eligible: list[dict[str, Any]] = []
    for part in _CLAUSE.finditer(evidence):
        clause = part[0]
        base = part.start()
        names = set(v02._titles(clause))
        editions = {_edition(m[0]) for m in _VERSION.finditer(v02._TITLE.sub("", clause))}
        heading = v02._ARTICLE.search(clause)
        if names or editions:
            validity = None
            section = None
            pending_condition = ""
        if names:
            subject = next(iter(names)) if len(names) == 1 else None
            version = None
            revision_unverified = False
        if editions:
            version = next(iter(editions)) if len(editions) == 1 else None
        if _UNVERIFIED.search(clause):
            revision_unverified = True
        if heading:
            section = v02._compact(heading[0])
        local_condition = _condition(clause)
        interval = _INTERVAL.search(clause)
        if interval:
            start_day, end_day = (_DAY.fullmatch(interval[name]) for name in ("start", "end"))
            try:
                if start_day and end_day:
                    first, last = _calendar(start_day), _calendar(end_day)
                    validity = (first, last) if first <= last else None
            except ValueError:
                validity = None
        exception = _EXCEPTION.match(clause.lstrip())
        if exception and candidates and candidates[-1]["clause_end"] + 1 == base:
            candidates[-1]["exception"] = exception[1] or exception[2]
            candidates[-1]["scope_spans"]["exception"] = _span(source_original, base, part.end())
        tokens = _scalar_candidates(clause)
        if not tokens and local_condition:
            pending_condition = local_condition
            continue
        previous_end = 0
        previous_fields: set[str] = set()
        for start, end, value, unit in tokens:
            span = _span(source_original, base + start, base + end)
            observations.append({"kind": "scalar", "value": value, "unit": unit, "span": span})
            if v02._TITLE.search(clause, previous_end, end) and any(
                m.start() <= start < m.end() for m in v02._TITLE.finditer(clause)
            ):
                previous_end = end
                continue
            prefix = v02._TITLE.sub("", clause[previous_end:start])
            previous_end = end
            stated_fields = _attributes(prefix)
            local_text = re.sub(r"[()（）]|答案是", "", prefix).strip()
            if _REPLACEMENT.fullmatch(local_text):
                stated_fields = previous_fields
            previous_fields = stated_fields
            own_places = _place(prefix)
            own_place = next(iter(own_places)) if len(own_places) == 1 else None
            condition = local_condition or pending_condition
            cue = _EDGE.sub("", prefix)
            group = re.match(r"(.{1,14}?)(?:组|主持|人员|者|人)(?=应|可|必须|需|的)", cue)
            if group:
                condition = group[0]
            specificity = _specificity(outside, prefix, field)
            if field.startswith("date:"):
                event = _EVENTS[field.removeprefix("date:")]
                relevant = bool(re.search(event, prefix + clause[end:]))
                date_count = sum(token[3] == "DATE" for token in tokens)
                compatible = unit == "DATE" and relevant and interval is None and date_count == 1
            else:
                implicit = _IMPLICIT.get(field)
                observed_field = (field in stated_fields or
                                  (not stated_fields and (
                                      (field == "ratio" and unit == "%")
                                      or (implicit is not None and implicit.search(prefix))
                                      or (field == "term" and bool(local_condition or pending_condition))
                                  )))
                compatible = bool(unit in _UNITS[field] and observed_field)
            qualifier = _bound(prefix)
            reasons = []
            if subject != title or not compatible or _METADATA.search(prefix):
                reasons.append("SUBJECT_OR_ATTRIBUTE_MISMATCH")
            if value is None:
                reasons.append("INVALID_SCALAR")
            if _FORMER.search(local_text):
                reasons.append("SUPERSEDED_VALUE")
            if field == "quantity" and requested_object and not clause[end:].lstrip(" )）").startswith(requested_object):
                reasons.append("OBJECT_MISMATCH")
            if _NEGATION.search(prefix):
                reasons.append("NEGATED")
            if qualifier == "CONFLICT" or (bound != "ASSERTED" and qualifier != bound):
                reasons.append("BOUND_MISMATCH")
            if (version_sensitive and (revision_unverified or len(editions) > 1)) or (versions and version not in versions):
                reasons.append("VERSION_MISMATCH")
            if day and (validity is None or not validity[0] <= day <= validity[1]):
                reasons.append("DATE_OUTSIDE_EVIDENCED_INTERVAL")
            if (places and own_place not in places) or len(own_places) > 1:
                reasons.append("JURISDICTION_MISMATCH")
            if article and section != v02._compact(article[0]):
                reasons.append("ARTICLE_MISMATCH")
            if condition and condition not in outside:
                reasons.append("CONDITION_MISMATCH")
            if query_condition and condition != query_condition:
                reasons.append("CONDITION_MISMATCH")
            if field == "term" and re.search(r"雨天|降雨|下雨", outside) and not condition:
                reasons.append("CONDITION_MISMATCH")
            candidate = {
                "subject": subject, "attribute": field if compatible else None, "value": value, "unit": unit,
                "version": version, "effective_from": validity[0] if validity else None,
                "effective_to": validity[1] if validity else None, "condition": condition,
                "scope": {"article": section, "jurisdiction": own_place}, "qualifier": qualifier,
                "negation": "NEGATED" in reasons, "exception": None, "source_span": span,
                "scope_spans": {"clause": _span(source_original, base, part.end())},
                "provenance": "UNVERIFIED_TEXT_ONLY", "rejections": reasons,
                "clause_end": part.end(), "specificity": specificity,
            }
            candidates.append(candidate)
            if not reasons:
                eligible.append(candidate)
        if tokens:
            pending_condition = ""
        for pattern, kind in ((_VERSION, "edition"), (v02._TITLE, "title"), (_NAME, "lexical")):
            observations.extend({"kind": kind, "span": _span(source_original, base + m.start(), base + m.end())}
                                for m in pattern.finditer(clause))

    # A conditional match supersedes a general statement for that explicit condition.
    # Incomparable or conflicting candidates remain visible and cause abstention.
    scoped = [candidate for candidate in eligible if candidate["condition"]]
    if scoped:
        eligible = scoped
    if not eligible:
        return unknown("NO_BOUND_VALID_CANDIDATE")
    # A positive lexical anchor may disambiguate an unrelated field sibling, but
    # differing positive candidates are left unresolved.
    if any(c["specificity"] for c in eligible):
        eligible = [c for c in eligible if c["specificity"]]
    fields_to_bind = ("subject", "attribute", "value", "unit", "version", "effective_from", "effective_to",
                      "condition", "scope", "qualifier", "negation", "exception")
    keys = {json.dumps({key: c[key] for key in fields_to_bind}, sort_keys=True) for c in eligible}
    if len(keys) != 1:
        return unknown("MULTIPLE_INCOMPARABLE_CANDIDATES")
    chosen = eligible[0]
    return {**result, **{key: chosen[key] for key in fields_to_bind}, "status": "DECIDED",
            "source_span": chosen["source_span"], "provenance": chosen["provenance"]}
