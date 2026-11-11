"""Collect short public statutory facts from a fixed official DEV document list."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha256
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import ssl
import time
from typing import Any
import unicodedata
from urllib.error import URLError
from urllib.request import HTTPSHandler, HTTPRedirectHandler, Request, build_opener

# Fixed source document roster, with known version bounds from the official publications.
# No world IDs, answer labels, or per-question entries are used by the extractor.
SOURCES = (
    (
        "H795",
        "holiday",
        "国务院",
        "国务院令第795号",
        "2025-01-01",
        None,
        "https://app.www.gov.cn/govdata/gov/202411/12/521605/article.html",
    ),
    (
        "H644",
        "holiday",
        "国务院",
        "国务院令第644号",
        "2014-01-01",
        "2025-01-01",
        "https://www.ln.gov.cn/web/zwgkx/lnsrmzfgb/2014n/qk/2014n_dyq/gwywj/C02298C830654E08B8CDFC5E6A46E0D8/index.shtml",
    ),
    (
        "S797",
        "health",
        "国务院",
        "国务院令第797号",
        "2025-01-20",
        None,
        "https://app.www.gov.cn/govdata/gov/202412/13/522682/articleNew.html",
    ),
    (
        "S2019",
        "health",
        "国务院",
        "公共场所卫生管理条例2019年修订",
        "2019-04-23",
        "2025-01-20",
        "https://xzfg.moj.gov.cn/mobile/law/detail?LawID=120",
    ),
    (
        "S2023",
        "health",
        "上海市卫生健康委员会",
        "沪卫规〔2023〕3号",
        "2023-09-01",
        "2028-09-01",
        "https://www.shanghai.gov.cn/gwk/search/content/52b4e0bc29a7436b95c83aacc5ac6358",
    ),
    (
        "D172",
        "driving",
        "公安部",
        "公安部令第172号",
        "2025-01-01",
        None,
        "https://www.beijing.gov.cn/zhengce/zhengcefagui/qtwj/202412/t20241231_3978134.html",
    ),
    (
        "D162",
        "driving",
        "公安部",
        "公安部令第162号",
        "2022-04-01",
        "2025-01-01",
        "https://www.beijing.gov.cn/zhengce/zhengcefagui/202206/t20220607_2731272.html",
    ),
)
HOLIDAYS = ("元旦", "新年", "春节", "清明节", "劳动节", "端午节", "中秋节", "国庆节")
VEHICLES = (
    "大型客车",
    "中型客车",
    "重型牵引挂车",
    "城市公交车",
    "大型货车",
    "低速载货汽车",
    "普通三轮摩托车",
)


class NoRedirect(HTTPRedirectHandler):
    def http_error_302(
        self, req: Any, fp: Any, code: int, msg: str, headers: Any
    ) -> Any:
        return None

    http_error_301 = http_error_303 = http_error_307 = http_error_308 = http_error_302


class TextView(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.ignored = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in ("script", "style"):
            self.ignored += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style") and self.ignored:
            self.ignored -= 1

    def handle_data(self, data: str) -> None:
        if not self.ignored:
            self.parts.append(data)


def wire(x: object) -> bytes:
    return json.dumps(
        x, sort_keys=True, ensure_ascii=False, separators=(",", ":")
    ).encode()


def digest(data: bytes) -> str:
    return sha256(data).hexdigest()


def view(raw: bytes, charset: str | None) -> str:
    try:
        decoded = raw.decode(charset or "utf-8")
    except (UnicodeError, LookupError):
        decoded = raw.decode("gb18030", errors="strict")
    parser = TextView()
    parser.feed(decoded)
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", "".join(parser.parts)))


def atom(
    entity: str, attribute: str, value: int | str, scope: str, locator: str
) -> dict[str, Any]:
    return {
        "entity": entity,
        "attribute": attribute,
        "value": value,
        "scope": scope,
        "locator": locator,
    }


def extract(source_id: str, text: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if source_id.startswith("H"):
        for h in HOLIDAYS:
            match = set(re.findall(rf"{h}[,，]放假([0-9]+)天", text))
            if len(match) == 1:
                rows.append(
                    atom(
                        h,
                        "statutory_days",
                        int(match.pop()),
                        "NATIONAL_PUBLIC",
                        "全国年节及纪念日放假办法第二条",
                    )
                )
        return rows
    if source_id == "S797":
        amendment = re.search(
            r"十七、将《公共场所卫生管理条例》(.{1,1800}?)(?=十八、)", text
        )
        if not amendment:
            return []
        provision = amendment[1]
        if (
            "宾馆、旅店、招待所" in provision
            and "设区的市级、县级人民政府疾病预防控制部门" in provision
        ):
            rows.append(
                atom(
                    "旅馆",
                    "permit_issuer",
                    "MUNICIPAL_OR_COUNTY_DISEASE_CONTROL",
                    "NATIONAL_HOTEL_REQUIRING_PERMIT",
                    "附件1第十七项修订第二、四、八条",
                )
            )
        for name in (
            "书店",
            "美术馆",
            "展览馆",
            "博物馆",
            "图书馆",
            "录像厅",
            "音乐厅",
        ):
            if name in provision and "办理卫生备案" in provision:
                rows.append(
                    atom(
                        name,
                        "administrative_procedure",
                        "HYGIENE_FILING",
                        "NATIONAL_PUBLIC_VENUES",
                        "附件1第十七项第八条",
                    )
                )
        for name in ("公园", "体育场", "公共交通工具"):
            if "除公园、体育场(馆)、公共交通工具" in provision:
                rows.append(
                    atom(
                        name,
                        "administrative_procedure",
                        "PERMIT_EXCEPTION",
                        "NATIONAL_PUBLIC_VENUES",
                        "附件1第十七项第八条",
                    )
                )
        return rows
    if source_id == "S2019":
        if "宾馆、饭馆、旅店、招待所" in text and "由县以上卫生行政部门签发" in text:
            rows.append(
                atom(
                    "旅馆",
                    "permit_issuer",
                    "COUNTY_OR_ABOVE_HEALTH_ADMIN",
                    "NATIONAL_HOTEL_REQUIRING_PERMIT",
                    "公共场所卫生管理条例第二、四、八条",
                )
            )
        return rows
    if source_id == "S2023":
        if (
            "宾馆、旅店、招待所" in text
            and "区卫生健康行政部门(疾控行政部门)负责辖区内" in text
        ):
            rows.append(
                atom(
                    "旅馆",
                    "permit_issuer",
                    "DISTRICT_HEALTH_OR_DISEASE_CONTROL",
                    "SHANGHAI_HOTEL_REQUIRING_PERMIT",
                    "上海市公共场所卫生行政许可管理办法第三、四、六条",
                )
            )
        duration = re.search(
            r"卫生许可证有效期限为([一二三四五六七八九十0-9]+)年", text
        )
        if duration:
            rows.append(
                atom(
                    "公共场所",
                    "permit_years",
                    duration[1],
                    "SHANGHAI_PUBLIC_VENUES",
                    "第十三条",
                )
            )
        return rows
    if source_id.startswith("D"):
        section = re.search(
            r"第十四条.*?年龄条件[：:](.{30,1100}?)(?:身体条件|二、将第六十五条)", text
        )
        if section:
            for vehicle in VEHICLES:
                matches = {
                    int(hi)
                    for obj, hi in re.findall(
                        r"申请([^;。]{2,95})准驾车型的[,，]在\d+周岁以上[,，](\d+)周岁以下",
                        section[1],
                    )
                    if vehicle in obj
                }
                if len(matches) == 1:
                    rows.append(
                        atom(
                            vehicle,
                            "application_age_max",
                            matches.pop(),
                            "NATIONAL_ELIGIBLE_APPLICATION",
                            "第十四条第一项",
                        )
                    )
        if re.search(
            r"初次申领机动车驾驶证的.{1,160}已持有机动车驾驶证.{1,140}大型客车", text
        ):
            rows.append(
                atom(
                    "大型客车",
                    "license_path",
                    "ADD_ON_EXISTING_LICENSE",
                    "NATIONAL_APPLICATION_PATH",
                    "第十六至十七条",
                )
            )
        return rows
    raise ValueError("UNKNOWN_SOURCE")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", type=Path, required=True)
    args = parser.parse_args()
    if args.index.exists():
        raise FileExistsError(args.index)
    opener = build_opener(
        NoRedirect(), HTTPSHandler(context=ssl.create_default_context())
    )
    receipts, records = [], []
    for sid, family, issuer, edition, start, end, url in SOURCES:
        receipt: dict[str, Any] = {
            "source_id": sid,
            "family": family,
            "issuer": issuer,
            "edition": edition,
            "url": url,
            "effective_from": start,
            "effective_to_exclusive": end,
            "checked_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "scope_of_use": "LOCAL_DEV_PUBLIC_FACT_ATOMS_AND_METADATA_ONLY",
        }
        try:
            req = Request(
                url,
                headers={
                    "Accept": "text/html",
                    "User-Agent": "Paper1-Owner33-ReadOnly/1",
                },
            )
            with opener.open(req, timeout=12) as response:
                raw = response.read(1024 * 1024 + 1)
                if (
                    response.geturl() != url
                    or response.status != 200
                    or len(raw) > 1024 * 1024
                ):
                    raise ValueError("BODY_OR_URI_GATE")
                normalized = view(raw, response.headers.get_content_charset())
            extracted = extract(sid, normalized)
            receipt.update(
                http_status=200,
                tls="SYSTEM_CA_VERIFIED",
                raw_response_sha256=digest(raw),
                body_bytes=len(raw),
                persisted_body=False,
                extracted_atoms=len(extracted),
                status="INDEXED" if extracted else "LOCATOR_NOT_PARSED",
            )
            for row in extracted:
                row.update(
                    source_id=sid,
                    family=family,
                    effective_from=start,
                    effective_to_exclusive=end,
                    evidence_sha256=digest(
                        wire(
                            {
                                **row,
                                "source_response_sha256": receipt[
                                    "raw_response_sha256"
                                ],
                            }
                        )
                    ),
                )
                records.append(row)
        except (OSError, URLError, ValueError) as exc:
            receipt.update(
                status="UNAVAILABLE",
                error_class=type(exc).__name__,
                http_status=getattr(exc, "code", None),
            )
        receipts.append(receipt)
        time.sleep(0.5)
    data = {
        "schema": "OWNER33_DEV_OFFICIAL_FACT_INDEX_V0",
        "records": records,
        "receipts": receipts,
        "rights": "Public short factual values and metadata only. No website HTML, files, evaluator or world keys retained. No EVAL or external-model rights.",
    }
    with args.index.open("xb") as f:
        f.write(wire(data))
    print(
        json.dumps(
            {
                "index_sha256": digest(wire(data)),
                "records": len(records),
                "source_summary": [
                    [r["source_id"], r["status"], r.get("extracted_atoms", 0)]
                    for r in receipts
                ],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
