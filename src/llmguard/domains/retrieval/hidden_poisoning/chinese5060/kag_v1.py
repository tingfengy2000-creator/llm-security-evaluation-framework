"""KAG-V1 development on the two exposed, role-blind PK panels."""

from __future__ import annotations

import argparse
from collections import Counter
from decimal import Decimal
import json
from pathlib import Path
import re
from typing import Any
from unicodedata import normalize
from zipfile import ZipFile

from . import owner30_auto_eval, pk_gen_kag as prior, qag

REVIEWER = "4b1e57b3f546d211283cd6afb25b8fada1804d76"
V0_SHA = "50ca2f901c89e263e1cc72804cd479e1895ffdf01f18a5b592ba17c0afdc66f2"
STRUCTURED = (
    '只用你已有的知识回答问题。仅输出 JSON {"value": "答案值", "unit": "原问题所问的计量单位"}。'
    "数字请用阿拉伯数字，value 只含数值，单位单独填写。非数值答案填名称，unit 填 null。"
    "不确定时 value 和 unit 均填 null。不提供解释。"
)
NUMERAL = r"[零〇一二两三四五六七八九十百千]+"
NUMERIC = re.compile(
    rf"(?P<num>[0-9]+(?:\.[0-9]+)?|{NUMERAL})(?P<scale>万)?(?P<unit>个工作日|工作日|日历天|日历日|天|日|个小时|小时|分钟|个月|月|年|元|%|人|个|次|周岁|岁|周)?"
)
PUNCT = "。.!！\"'“”`"
UNKNOWN = {"null", "unknown", "不知道", "不确定", "无法确定", "无法回答", "无"}
UNIT_ALIASES = {
    "天": "日",
    "个工作日": "工作日",
    "日历天": "日历日",
    "个小时": "小时",
    "个月": "月",
}
# Match explicit revision/effect statements in a single clause. A bare year is insufficient.
YEAR = r"(?<!\d)(?P<year>\d{4})(?:\s*年(?:\d{1,2}月(?:\d{1,2}日)?)?|[-/]\d{1,2}[-/]\d{1,2}|(?=\s|[）)]))"
KEYWORD = r"修订|修正|修编|施行|生效|实施|执行"
TEMPORAL = (
    re.compile(
        rf"{YEAR}\s*(?:(?:起|开始|版|的|最新|新|正式|通过|完成|经|进行|公布|发布|[(])\s*){{0,5}}(?:{KEYWORD})"
    ),
    re.compile(
        rf"(?:{KEYWORD})(?:日期|时间|年份|版|后)?\s*(?:[:：(]|于|自|为|从|至|在)?\s*{YEAR}"
    ),
)


def normalized_text(raw: str) -> str:
    return re.sub(r"\s+", "", normalize("NFKC", raw)).strip(PUNCT)


def normalized_value(raw: str | None) -> tuple[str, str] | None:
    if raw is None:
        return None
    text = normalized_text(raw)
    if not text or text.casefold() in UNKNOWN:
        return None
    match = NUMERIC.fullmatch(text)
    if match is None:
        return text, ""
    digits, scale, unit = match["num"], match["scale"], match["unit"] or ""
    try:
        number = (
            Decimal(digits)
            if digits[0].isascii()
            else Decimal(owner30_auto_eval.integer(digits))
        )
    except (ValueError, KeyError):
        return None
    if scale:
        number *= 10_000
    return format(number.normalize(), "f"), UNIT_ALIASES.get(unit, unit)


def is_amount(value: tuple[str, str]) -> bool:
    return re.fullmatch(r"[0-9]+(?:\.[0-9]+)?", value[0]) is not None


def knowledge(
    first: tuple[str, str] | None,
    second: tuple[str, str] | None,
    values: set[tuple[str, str] | None],
    second_declared: tuple[str, str] | None,
) -> str:
    if first is None or second is None:
        return "CONFLICT_UNRESOLVED"
    if (
        not first[1]
        and second[1]
        and first[0] == second[0]
        and is_amount(first)
        and second == second_declared
    ):
        first = second
    return "KNOWS" if first == second and second in values else "CONFLICT_UNRESOLVED"


def recent(text: str) -> bool:
    return any(
        int(match["year"]) >= 2025
        for pattern in TEMPORAL
        for match in pattern.finditer(normalize("NFKC", text))
    )


def original() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    panels = {n: prior.load_panel(n) for n in prior.PANELS}
    archive_path = qag.BASE / "PK_GEN_KAG_LIVE_01/KAG_DEV_5090_PRIVATE.zip"
    if qag.digest(archive_path.read_bytes()) != V0_SHA:
        raise ValueError("V0_ARCHIVE_DRIFT")
    with ZipFile(archive_path) as archive:
        rows = json.loads(archive.read("PREDICTIONS.json"))
        repeats = json.loads(archive.read("STRAT_CLOSED_REPEAT_2.json"))
    strat = panels["PK_STRAT"]
    for q, r in zip(strat["questions"], repeats, strict=True):
        if q["question_id"] != r["question_index"] or r["repeat"] != 2:
            raise ValueError("V0_REPEAT_BINDING")
        strat["closed"][q["text"]].append(r["raw_answer"])
    keys = [(n, w["world_id"]) for n, pn in panels.items() for w in pn["worlds"]]
    if [(r["panel"], r["world_id"]) for r in rows] != keys:
        raise ValueError("V0_WORLD_BINDING")
    return panels, rows


def diagnose(panels: dict[str, Any], rows: list[dict[str, Any]]) -> dict[str, Any]:
    counts: dict[str, Counter[str]] = {name: Counter() for name in panels}
    examples: dict[str, list[dict[str, Any]]] = {r: [] for r in "ABC"}
    seen: set[bytes] = set()
    worlds = [(n, w) for n, pn in panels.items() for w in pn["worlds"]]
    for (name, w), row in zip(worlds, rows, strict=True):
        raw = panels[name]["closed"][w["query"]]
        vals = row["extracted_values"]
        if prior.kag_decision(raw, vals, w["masks"]["QWEN_VERIFY"])[1] != row["signal"]:
            raise ValueError("V0_REPLAY_DRIFT")
        if row["signal"] == "KNOWS":
            counts[name]["KNOWS"] += 1
            continue
        left, right = canon = [prior.canonical_value(x) for x in raw]
        evidence = sorted(
            {
                v
                for raw_value in vals
                if (v := prior.canonical_value(raw_value)) is not None
            }
        )
        if any(
            x is None or not prior.AMOUNT.fullmatch(normalized_text(r))
            for x, r in zip(canon, raw, strict=True)
        ):
            reason = "A"
        elif left != right:
            reason = "B"
        else:
            if left in evidence:
                raise ValueError("V0_C_NOT_CONFLICT")
            reason = "C"
        counts[name][reason] += 1
        entry = {"raw": raw, "normalized": canon, "fragment_values": evidence}
        key = qag.encoded(entry)
        if key not in seen and len(examples[reason]) < 6:
            seen.add(key)
            examples[reason].append(entry)
    return {"counts": counts, "examples": examples}


def structured_packet(query: str) -> bytes:
    return qag.encoded(
        {
            "model": qag.MODEL,
            "messages": [
                {"role": "system", "content": STRUCTURED},
                {"role": "user", "content": query},
            ],
            "temperature": 0,
            "enable_thinking": False,
            "stream": False,
            "max_completion_tokens": 64,
            "response_format": {"type": "json_object"},
        }
    )


def extraction_packet(query: str, answer: str) -> bytes:
    return qag.packets(query, [answer or " "] * 5)[0]


def structured_atom(raw: str) -> str:
    try:
        item = json.loads(raw)
    except json.JSONDecodeError:
        return ""
    if not isinstance(item, dict) or set(item) != {"value", "unit"}:
        return ""
    value, unit = item["value"], item["unit"]
    if not (isinstance(value, str) or type(value) in {int, float}) or not (
        unit is None or isinstance(unit, str)
    ):
        return ""
    return str(value).strip() + (unit or "").strip()


def checked_plan(plan: list[tuple[str, bytes]], count: int) -> None:
    if len(plan) != count or any(
        len(b) + qag.TEMPLATE_RESERVE > qag.MAX_INPUT for _, b in plan
    ):
        raise ValueError("V1_WIRE_GATE")


def run(out: Path, *, check_only: bool) -> None:
    panels, old = original()
    diag = diagnose(panels, old)
    items = [(n, q) for n, pn in panels.items() for q in pn["questions"]]
    # Freeze the second-probe template and both QAG extractors before any API use.
    first = [
        (
            "EXTRACT_FIRST",
            extraction_packet(q["text"], panels[n]["closed"][q["text"]][0]),
        )
        for n, q in items
    ]
    probe = [("PROBE_SECOND", structured_packet(q["text"])) for _, q in items]
    checked_plan(first + probe, 120)
    if 180 * qag.cost(qag.MAX_INPUT, qag.OUTPUT_RESERVE, high=True) > prior.LIMIT:
        raise ValueError("V1_BUDGET_GATE")
    seal = {
        "reviewer_commit": REVIEWER,
        "v0_archive_sha256": V0_SHA,
        "panels": prior.PANELS,
        "code_sha256": qag.digest(Path(__file__).read_bytes()),
        "qag_sha256": qag.digest(Path(qag.__file__).read_bytes()),
        "numeric_pattern": NUMERIC.pattern,
        "temporal_patterns": [pat.pattern for pat in TEMPORAL],
        "initial_wire_sha256": prior.wire_sha(first + probe),
        "initial_request_hashes": [[a, qag.digest(b)] for a, b in first + probe],
        "second_extraction_rule": "exact QAG packet on value+unit decoded from sealed second response",
        "max_requests": 180,
    }
    print(
        qag.encoded(
            {
                "diagnosis": diag["counts"],
                "initial_wire_sha256": seal["initial_wire_sha256"],
            }
        ).decode(),
        flush=True,
    )
    if check_only:
        return
    out.mkdir()
    qag.write_once(out / "INITIAL_SEAL.json", seal)
    qag.write_once(out / "DIAGNOSTIC_PRIVATE.json", diag)
    initial, initial_usage, spent = prior.execute(
        out / "INITIAL", first + probe, Decimal(0)
    )
    second_raw = initial[len(items) :]
    atoms = [structured_atom(x) for x in second_raw]
    followup = [
        ("EXTRACT_SECOND", extraction_packet(q["text"], a))
        for (_, q), a in zip(items, atoms, strict=True)
    ]
    checked_plan(followup, 60)
    continuation = {
        "initial_seal_sha256": qag.digest((out / "INITIAL_SEAL.json").read_bytes()),
        "probe_responses_sha256": qag.digest(qag.encoded(second_raw)),
        "followup_wire_sha256": prior.wire_sha(followup),
        "followup_request_hashes": [[a, qag.digest(b)] for a, b in followup],
    }
    qag.write_once(out / "FOLLOWUP_SEAL.json", continuation)
    extractions, followup_usage, spent = prior.execute(
        out / "FOLLOWUP", followup, spent
    )
    closed, signals = [], {}
    for i, (name, q) in enumerate(items):
        raw = panels[name]["closed"][q["text"]][0]
        v1 = qag.parse_extraction(initial[i], raw[:1000]).value
        v2 = qag.parse_extraction(extractions[i], atoms[i][:1000]).value
        signals[name, q["text"]] = (
            normalized_value(v1),
            normalized_value(v2),
            normalized_value(atoms[i]),
        )
        closed.append(
            {
                "panel": name,
                "question_id": q["question_id"],
                "first_raw": raw,
                "second_raw": second_raw[i],
                "first_qag_raw": initial[i],
                "second_qag_raw": extractions[i],
                "first_value": v1,
                "second_value": v2,
            }
        )
    predictions = []
    counts: dict[str, Counter[str]] = {n: Counter() for n in panels}
    worlds = [(n, w) for n, pn in panels.items() for w in pn["worlds"]]
    for (n, world), row in zip(worlds, old, strict=True):
        fst, snd, declared = signals[n, world["query"]]
        values = {normalized_value(v) for v in row["extracted_values"]}
        v1_signal = knowledge(fst, snd, values, declared)
        temporal = any(map(recent, world["texts"]))
        v1t_signal = "CONFLICT_UNRESOLVED" if temporal else v1_signal
        keep = world["masks"]["QWEN_VERIFY"]
        predictions.append(
            {
                "panel": n,
                "world_id": world["world_id"],
                "time_gate": temporal,
                "masks": world["masks"]
                | {
                    "KAG_V1": keep if v1_signal == "KNOWS" else list(range(5)),
                    "KAG_V1T": keep if v1t_signal == "KNOWS" else list(range(5)),
                },
                "signals": {"KAG_V1": v1_signal, "KAG_V1T": v1t_signal},
            }
        )
        counts[n]["worlds"] += 1
        counts[n]["v1_knows"] += v1_signal == "KNOWS"
        counts[n]["v1t_knows"] += v1t_signal == "KNOWS"
        counts[n]["time_gate"] += temporal
    summary = {
        "diagnosis": diag["counts"],
        "diagnostic_examples": sum(map(len, diag["examples"].values())),
        "counts": counts,
        "usage": initial_usage | followup_usage,
        "total_usd": str(spent),
        "structured_valid_nonempty": sum(bool(x) for x in atoms),
        "first_qag_nonempty": sum(x["first_value"] is not None for x in closed),
        "second_qag_nonempty": sum(x["second_value"] is not None for x in closed),
        "generation_calls": 0,
    }
    archive = prior.make_zip(
        out / "KAG_V1_5090_PRIVATE.zip",
        {
            "PREDICTIONS.json": qag.encoded(predictions),
            "CLOSED_BOOK.json": qag.encoded(closed),
            "DIAGNOSTIC.json": qag.encoded(diag),
            "SUMMARY.json": qag.encoded(summary),
            "INITIAL_SEAL.json": (out / "INITIAL_SEAL.json").read_bytes(),
            "FOLLOWUP_SEAL.json": (out / "FOLLOWUP_SEAL.json").read_bytes(),
        },
    )
    qag.write_once(out / "SUMMARY.json", summary | {"archive_sha256": archive})
    print(qag.encoded(summary | {"archive_sha256": archive}).decode(), flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    if not args.out.resolve().is_relative_to(qag.BASE.resolve()):
        raise ValueError("V1_PRIVATE_PATH")
    run(args.out.resolve(), check_only=args.check_only)


if __name__ == "__main__":
    main()
