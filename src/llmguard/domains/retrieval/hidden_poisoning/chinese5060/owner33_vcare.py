"""V-CARE role-blind, version-constrained external evidence verification."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import re
from typing import Any

from llmguard.domains.retrieval.hidden_poisoning.chinese5060.owner30_auto_eval import (
    integer,
)
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.owner31_qcer import (
    DATE,
    HISTORY,
    PLACE,
    Query,
    norm,
)

ARMS = (
    "NONE",
    "RD_B2",
    "RD_ZH",
    "B2_SAME_EXTRA_RETRIEVAL",
    "B2_ALWAYS_VERIFY",
    "VCARE_FULL",
    "VCARE_NO_SCOPE",
    "VCARE_NO_RESCUE",
)
CONFIG = {
    "top_k": 5,
    "max_source_lookups": 1,
    "max_extra_evidence": 1,
    "max_total_evidence_slots": 6,
    "offline_context_utf8_cap": 4096,
    "retained_support_required": 2,
    "extra_summary_utf8_cap": 256,
}
HOLIDAY = re.compile("元旦|春节|清明节|劳动节|端午节|中秋节|国庆节")
NATURAL_DAYS = re.compile(
    r"(?P<n>[0-9]+|[零〇一二两三四五六七八九十]+)\s*(?:天|个(?:法定节日天数|依法休息的日期|法定休假日))"
)
PERMIT_OBJECT = re.compile("旅馆|宾馆|旅店|招待所")
PERMIT = re.compile("卫生许可|卫生许可证|签发许可|许可.*签发|许可.*发放|发证")
DISEASE = re.compile("疾控|疾病预防控制")
HEALTH_ADMIN = re.compile("卫生行政|卫生健康行政")
MARKET = re.compile("市场监管|市场监督管理")
MUNICIPAL = re.compile("设区.{0,3}市|市或县|市县|市级.*县级")
COUNTY = re.compile("县.{0,4}及更高|县以上|县级以上")
RISK_SCOPE = re.compile(
    "单独安排|试点|只适用|仅限|另一区域|地方另定|行业特例|仅适用|备案管理|无需许可|免予许可"
)
QUALIFIER = re.compile("并非|不是|至少|左右|不足|至多|大约|可能")
HOLIDAY_CLAIM = re.compile("法定|依法|放假|单列的假日|计入法定|全国通行")
HISTORICAL_CONTRAST = re.compile("原先|旧版|此前|以往|历史|曾经")
DATE_BOUNDARY = re.compile(r"(?:自|从).{0,20}?(?:起|施行|生效|执行)")


@dataclass(frozen=True)
class Intent:
    entity: str
    attribute: str
    scope: str
    place: str
    event: str


@dataclass(frozen=True)
class Outcome:
    keep: tuple[int, ...]
    codes: tuple[str, ...]
    evidence_id: str | None
    looked_up: int
    state: str


def intent(query: Query) -> Intent | None:
    ask = norm(query.ask)
    place = next(iter(dict.fromkeys(PLACE.findall(query.subject))), "")
    holidays = set(HOLIDAY.findall(ask))
    if len(holidays) == 1 and re.search("法定|法定假日|节日", ask):
        return Intent(
            holidays.pop(), "statutory_days", "NATIONAL_PUBLIC", place, query.event_date
        )
    if PERMIT_OBJECT.search(query.subject) and ("机关" in ask or "签发" in ask):
        # A national-rule question has national reference scope; local eligibility is still a candidate constraint.
        if "全国" in query.text:
            return Intent(
                "旅馆",
                "permit_issuer",
                "NATIONAL_HOTEL_REQUIRING_PERMIT",
                place,
                query.event_date,
            )
        if place == "上海":
            return Intent(
                "旅馆",
                "permit_issuer",
                "SHANGHAI_HOTEL_REQUIRING_PERMIT",
                place,
                query.event_date,
            )
    if (
        "大型客车" in ask
        and "年龄" in ask
        and re.search("已持有|已持证|增驾", query.text)
    ):
        return Intent(
            "大型客车",
            "application_age_max",
            "NATIONAL_ELIGIBLE_APPLICATION",
            place,
            query.event_date,
        )
    return None


def lookup(index: list[dict[str, Any]], target: Intent | None) -> dict[str, Any] | None:
    if target is None:
        return None
    valid = [
        x
        for x in index
        if (x["entity"], x["attribute"], x["scope"])
        == (target.entity, target.attribute, target.scope)
        and x["effective_from"] <= target.event
        and (
            x["effective_to_exclusive"] is None
            or target.event < x["effective_to_exclusive"]
        )
    ]
    return valid[0] if len(valid) == 1 else None


def claim(
    target: Intent, text: str, anchor: dict[str, Any] | None, *, scope: bool
) -> int | str | None:
    text = norm(text)
    if (
        HISTORY.search(text)
        or HISTORICAL_CONTRAST.search(text)
        or QUALIFIER.search(text)
    ):
        return None
    places = set(PLACE.findall(text))
    if scope and (
        RISK_SCOPE.search(text)
        or (target.place and places and places != {target.place})
    ):
        return None
    stamps: list[str] = []
    if DATE_BOUNDARY.search(text):
        try:
            stamps = [
                date(int(m["y"]), int(m["m"]), int(m["d"])).isoformat()
                for m in DATE.finditer(text)
            ]
        except ValueError:
            return None
    if len(set(stamps)) > 1:
        return None
    if stamps and (
        stamps[0] > target.event
        or (anchor is not None and stamps[0] < anchor["effective_from"])
    ):
        return None
    content = DATE.sub(" ", text)
    if (
        target.attribute == "statutory_days"
        and target.entity in content
        and HOLIDAY_CLAIM.search(content)
    ):
        if re.search("调休共|连休共|假期共计", content):
            return None
        try:
            values = {integer(m["n"]) for m in NATURAL_DAYS.finditer(content)}
        except ValueError:
            return None
        return values.pop() if len(values) == 1 else None
    if (
        target.attribute == "permit_issuer"
        and PERMIT_OBJECT.search(content)
        and PERMIT.search(content)
    ):
        if (
            DISEASE.search(content)
            and MUNICIPAL.search(content)
            and not MARKET.search(content)
        ):
            return "MUNICIPAL_OR_COUNTY_DISEASE_CONTROL"
        if DISEASE.search(content) and "区" in content and not MARKET.search(content):
            return "DISTRICT_HEALTH_OR_DISEASE_CONTROL"
        if (
            HEALTH_ADMIN.search(content)
            and COUNTY.search(content)
            and not DISEASE.search(content)
        ):
            return "COUNTY_OR_ABOVE_HEALTH_ADMIN"
        if MARKET.search(content) and "省" in content and not DISEASE.search(content):
            return "PROVINCIAL_MARKET_REGULATION"
    return None


def trigger(
    target: Intent | None, texts: list[str], b2: tuple[int, ...], zh: tuple[int, ...]
) -> str:
    if b2 != zh:
        return "MASK_DISAGREEMENT"
    if target is None:
        return "QUERY_SCOPE_UNRESOLVED"
    values = [claim(target, text, None, scope=True) for text in texts]
    if len({v for v in values if v is not None}) > 1:
        return "VISIBLE_CONFLICT"
    if sum(values[i] is not None for i in b2) < CONFIG["retained_support_required"]:
        return "INSUFFICIENT_VISIBLE_EVIDENCE"
    return "NOT_TRIGGERED"


def verify(
    target: Intent | None,
    texts: list[str],
    b2: tuple[int, ...],
    anchor: dict[str, Any] | None,
    queried: int,
    *,
    scope: bool = True,
    rescue: bool = True,
    edit: bool = True,
) -> Outcome:
    if target is None or anchor is None:
        return Outcome(
            b2,
            tuple("KEEP_B2" if i in b2 else "DROP_B2" for i in range(len(texts))),
            None,
            queried,
            "CONFLICT_UNRESOLVED" if queried else "NOT_TRIGGERED",
        )
    if not edit:
        return Outcome(
            b2,
            tuple("KEEP_B2" if i in b2 else "DROP_B2" for i in range(len(texts))),
            anchor["evidence_sha256"],
            queried,
            "EXTRA_ONLY",
        )
    keep = set(b2)
    codes = []
    for i, text in enumerate(texts):
        observed = claim(target, text, anchor, scope=scope)
        if observed is None:
            codes.append("OUTSIDE_OR_UNRESOLVED_B2")
        elif observed != anchor["value"] and i in keep:
            keep.remove(i)
            codes.append("DROP_BOUND_CONFLICT")
        elif observed == anchor["value"] and i not in keep and rescue:
            keep.add(i)
            codes.append("RESTORE_BOUND_REFERENCE_AGREEMENT")
        else:
            codes.append("UNCHANGED_B2")
    return Outcome(
        tuple(sorted(keep)),
        tuple(codes),
        anchor["evidence_sha256"],
        queried,
        "REFERENCE_BOUND",
    )


def render_anchor(anchor: dict[str, Any] | None) -> str:
    if anchor is None:
        return ""
    return "|".join(
        str(anchor[k])
        for k in ("entity", "attribute", "scope", "value", "edition")
        if k in anchor
    )


def budget(
    texts: list[str], keep: tuple[int, ...], anchor: dict[str, Any] | None
) -> int:
    extra = render_anchor(anchor).encode()
    total = sum(len(texts[i].encode()) for i in keep) + len(extra)
    if (
        len(keep) + bool(extra) > CONFIG["max_total_evidence_slots"]
        or len(extra) > CONFIG["extra_summary_utf8_cap"]
        or total > CONFIG["offline_context_utf8_cap"]
    ):
        raise ValueError("EVIDENCE_BUDGET")
    return total
