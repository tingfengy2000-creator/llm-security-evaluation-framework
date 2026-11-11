"""PK-GEN and KAG-DEV on frozen, role-blind PK panels."""

from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from decimal import Decimal
import json
import os
from pathlib import Path
import re
from typing import Any
from unicodedata import normalize
from zipfile import ZIP_DEFLATED, ZipFile

from . import owner30_auto_eval, pk_strat, qag

REVIEWER = "ed8ffde925a5f0340d33a3acb9d08b93ce996997"
ARMS = ("NONE", "RD_B2", "QWEN_VERIFY")
LIMIT = Decimal("1")
WORKERS = 12
GRID = "a3ce06197921e086a28fee2429f6cbe2c71acfbde4cddeee3d444ebf480050c2"
PANELS = {
    "PK_STRAT": (
        "PK_STRAT_INPUT_38F0F5B",
        "PK_STRAT_LIVE_01",
        56,
        24,
        "55939a39dba36572b9fd4c6cefa1b0e9664001b5502c51b99e802dd0e8e0fda6",
        "15cdcffbe8646c470bb92239b0025d855b313dc6102f1a09dca2488ab4e18d26",
        "d9c2528a571bb73f0ca0eb7b7fc800de529309abf536e323d01bca2cd6fab7dc",
    ),
    "PK_CONFIRM": (
        "PKC_INPUT_092EFE9",
        "PKC_LIVE_01",
        80,
        36,
        "f3a3ca1b5591aaf46d5858936bc1721bd9abe7a8c26219a62107dcbea57b90e5",
        "fb5e23d0b33ccb842db581941d42d2198b683da9961e803dec5e650bc04b7e17",
        "18f59b12baf29b1085e153373af0f2910cefd358199c34490e9862d251d97e0e",
    ),
}
FULL_DATE = re.compile(
    r"(?<!\d)(\d{4})(?:年|-)(\d{1,2})(?:月|-)(\d{1,2})(?:日|(?=\D|$))"
)
AMOUNT = re.compile(
    r"(?P<number>[0-9]+(?:\.[0-9]+)?|[零〇一二两三四五六七八九十百千]+)"
    r"(?P<unit>个工作日|工作日|日历天|日历日|天|日|个小时|小时|分钟|个月|月|年|元|%|人|个|次|周)?"
)


def read(path: Path, digest: str) -> Any:
    return qag.checked(path.read_bytes(), digest)


def load_panel(name: str) -> dict[str, Any]:
    prep, live, n_world, n_q, seal_sha, ans_sha, pred_sha = PANELS[name]
    base = qag.BASE
    seal = read(base / prep / "SEAL.json", seal_sha)
    data = read(base / prep / "INPUT.json", seal["input_sha256"])
    answers = read(base / live / "CLOSED_BOOK_ANSWERS.json", ans_sha)
    preds = read(base / live / "PREDICTIONS.json", pred_sha)
    if len(preds) != n_world or len(data["worlds"]) != n_world:
        raise ValueError("PK_PANEL_DENOMINATOR")
    masks = {row["world_id"]: row["masks"] for row in preds}
    if (
        set(masks) != {row["world_id"] for row in data["worlds"]}
        or len(masks) != n_world
    ):
        raise ValueError("PK_MASK_BINDING")
    if name == "PK_STRAT":
        questions = [
            {"question_id": row["question_index"], "text": row["question"]}
            for row in answers
        ]
        if [q["text"] for q in questions] != data["closed_book"]:
            raise ValueError("PK_STRAT_CLOSED_BINDING")
        closed = {a["question"]: [a["raw_answer"]] for a in answers}
    else:
        questions = data["questions"]
        pairs = {(a["question_id"], a["repeat"]): a["raw_answer"] for a in answers}
        if len(pairs) != len(answers) or len(pairs) != n_q * 2:
            raise ValueError("PK_CONFIRM_CLOSED_BINDING")
        closed = {
            q["text"]: [pairs[q["question_id"], rep] for rep in (1, 2)]
            for q in questions
        }
    if len(closed) != n_q or len(questions) != n_q:
        raise ValueError("PK_CLOSED_COUNT")
    worlds = []
    for row in data["worlds"]:
        if name == "PK_CONFIRM":
            ids, texts = zip(
                *[(p["passage_id"], p["text"]) for p in row["passages"]], strict=True
            )
        else:
            ids, texts = tuple(range(1, 6)), row["texts"]
        keep = masks[row["world_id"]]
        if (
            len(texts) != 5
            or row["query"] not in closed
            or keep["NONE"] != list(range(5))
            or any(
                keep[a] is None
                or keep[a] != sorted(set(keep[a]))
                or not set(keep[a]) <= set(range(5))
                for a in ARMS
            )
        ):
            raise ValueError("PK_PANEL_ROW")
        worlds.append(
            {
                "world_id": row["world_id"],
                "query": row["query"],
                "ids": ids,
                "texts": texts,
                "masks": {a: keep[a] for a in ARMS},
            }
        )
    return {"questions": questions, "closed": closed, "worlds": worlds}


def generator_template() -> dict[str, Any]:
    root = qag.BASE / "W1-5060-OWNER29-RAPID-FEASIBILITY-20261111-01"
    sample = read(root / "REQUEST_GRID_PRIVATE.json", GRID)["cells"][0]["payload"]
    if (
        sample["model"] != qag.MODEL
        or sample["temperature"] != 0
        or sample["enable_thinking"] is not False
        or sample["stream"] is not False
        or sample["response_format"] != {"type": "json_object"}
        or sample["max_completion_tokens"] != 256
        or [m["role"] for m in sample["messages"]] != ["system", "user"]
        or set(json.loads(sample["messages"][1]["content"]))
        != {"event_date", "evidence", "question"}
    ):
        raise ValueError("OWNER29_TEMPLATE")
    return {**sample, "messages": sample["messages"][:1]}


def visible_date(query: str) -> str | None:
    dates = {date(*map(int, m.groups())).isoformat() for m in FULL_DATE.finditer(query)}
    return next(iter(dates)) if len(dates) == 1 else None


def generation_packet(
    template: dict[str, Any], world: dict[str, Any], arm: str
) -> bytes:
    evidence = [
        {"id": f"E{i + 1}", "text": world["texts"][i]} for i in world["masks"][arm]
    ]
    user = {
        "event_date": visible_date(world["query"]),
        "evidence": evidence,
        "question": world["query"],
    }
    return qag.encoded(
        {
            **template,
            "messages": [
                *template["messages"],
                {"role": "user", "content": qag.encoded(user).decode()},
            ],
        }
    )


def cached_extractions(wanted: set[str]) -> dict[str, str]:
    found: dict[str, str] = {}
    for name in ("QAG_DEV_01", "QAG_DEV_FINAL", "QAG_TEST_01"):
        for file in sorted((qag.BASE / name).glob("reply-*.json")):
            if file.name.endswith("-5.json"):
                continue
            row = json.loads(file.read_bytes())
            key = row["request_sha256"]
            if (
                key in wanted
                and "error" not in row
                and row["provider"]["model"] == qag.MODEL
            ):
                content = row["provider"]["choices"][0]["message"]["content"]
                found.setdefault(key, content)
    return found


def canonical_value(raw: str | None) -> str | None:
    if raw is None:
        return None
    text = re.sub(r"\s+", "", normalize("NFKC", raw)).strip("。.!！\"'“”`")
    if not text or text.casefold() in {
        "null",
        "unknown",
        "不知道",
        "不确定",
        "无法确定",
        "无法回答",
        "无",
    }:
        return None
    matched = AMOUNT.fullmatch(text)
    if not matched:
        return text
    digits, unit = matched["number"], matched["unit"] or ""
    if re.fullmatch(r"[0-9]+(?:\.[0-9]+)?", digits):
        number = format(Decimal(digits).normalize(), "f")
    else:
        try:
            number = str(owner30_auto_eval.integer(digits))
        except (ValueError, KeyError):
            return None
    aliases = {
        "天": "日",
        "个工作日": "工作日",
        "日历天": "日历日",
        "个小时": "小时",
        "个月": "月",
    }
    return number + aliases.get(unit, unit)


def kag_decision(
    answers: list[str], values: list[str | None], verify: list[int]
) -> tuple[list[int], str]:
    first, second = map(canonical_value, answers)
    if (
        first is not None
        and first == second
        and first in {canonical_value(v) for v in values}
    ):
        return verify, "KNOWS"
    return list(range(5)), "CONFLICT_UNRESOLVED"


def plan_all() -> tuple[
    dict[str, Any], list[tuple[str, bytes]], list[tuple[str, bytes]], dict[str, str]
]:
    panels = {name: load_panel(name) for name in PANELS}
    template = generator_template()
    gen = [
        ("PK_GEN", generation_packet(template, row, arm))
        for row in panels["PK_CONFIRM"]["worlds"]
        for arm in ARMS
    ]
    unique: dict[str, bytes] = {}
    for panel in panels.values():
        for row in panel["worlds"]:
            row["extract_keys"] = []
            for body in qag.packets(row["query"], row["texts"])[:5]:
                key = qag.digest(body)
                unique.setdefault(key, body)
                row["extract_keys"].append(key)
    prior = cached_extractions(set(unique))
    strat = panels["PK_STRAT"]["questions"]
    kag = [("STRAT_CLOSED", pk_strat.closed_packet(q["text"])) for q in strat]
    kag.extend(("KAG_EXTRACT", b) for key, b in unique.items() if key not in prior)
    if (
        len(gen) != 240
        or len(strat) != 24
        or any(
            len(body) + qag.TEMPLATE_RESERVE > qag.MAX_INPUT for _, body in gen + kag
        )
    ):
        raise ValueError("PK_GEN_KAG_PLAN_GATE")
    return panels, gen, kag, prior


def wire_sha(plan: list[tuple[str, bytes]]) -> str:
    return qag.digest(qag.encoded([[arm, qag.digest(body)] for arm, body in plan]))


def execute(
    out: Path, plan: list[tuple[str, bytes]], spent: Decimal
) -> tuple[list[str], dict[str, dict[str, Any]], Decimal]:
    key = os.environ["DASHSCOPE_API_KEY"]
    out.mkdir()
    qag.write_once(
        out / "ATTEMPT.json", {"wire_sha256": wire_sha(plan), "calls": len(plan)}
    )
    responses = []
    stats: dict[str, Counter[str]] = {}
    seen: set[str] = set()
    reserve = qag.cost(qag.MAX_INPUT, qag.OUTPUT_RESERVE, high=True)
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        for start in range(0, len(plan), WORKERS):
            batch = plan[start : start + WORKERS]
            if spent + len(batch) * reserve > LIMIT:
                raise ValueError("PK_GEN_KAG_BUDGET_STOP")
            files = [
                out / f"reply-{i:03}.json" for i in range(start, start + len(batch))
            ]
            futures = [
                pool.submit(qag.call, key, b, p)
                for (_, b), p in zip(batch, files, strict=True)
            ]
            for (arm, _), path, future in zip(batch, files, futures, strict=True):
                response, n_in, n_out, _ = future.result()
                receipt = json.loads(path.read_bytes())
                rid = receipt["provider"]["id"]
                if rid in seen:
                    raise ValueError("DUPLICATE_REQUEST_ID")
                seen.add(rid)
                stats.setdefault(arm, Counter()).update(
                    calls=1, input_tokens=n_in, output_tokens=n_out
                )
                spent += qag.cost(n_in, n_out)
                responses.append(response)
    usage = {
        a: dict(s) | {"usd": str(qag.cost(s["input_tokens"], s["output_tokens"]))}
        for a, s in stats.items()
    }
    qag.write_once(out / "USAGE.json", usage)
    return responses, usage, spent


def answer_status(raw: str, allowed: set[str]) -> str:
    try:
        item = json.loads(raw)
    except json.JSONDecodeError:
        return "INVALID"
    if not isinstance(item, dict) or set(item) != {"status", "answer", "citations"}:
        return "INVALID"
    status, answer, citations = item["status"], item["answer"], item["citations"]
    if (
        not isinstance(answer, str)
        or not isinstance(citations, list)
        or any(not isinstance(c, str) or c not in allowed for c in citations)
    ):
        return "INVALID"
    if status == "ANSWER" and answer.strip() and citations:
        return "ANSWER"
    if status == "ABSTAIN" and not answer.strip() and not citations:
        return "ABSTAIN"
    return "INVALID"


def make_zip(path: Path, files: dict[str, bytes]) -> str:
    with ZipFile(path, "x", compression=ZIP_DEFLATED) as archive:
        for name, data in files.items():
            archive.writestr(name, data)
    with ZipFile(path) as archive:
        if archive.testzip() or any(archive.read(n) != b for n, b in files.items()):
            raise ValueError("PK_GEN_KAG_ZIP_READBACK")
    return qag.digest(path.read_bytes())


def run(out: Path, *, check_only: bool) -> None:
    panels, gen, kag, previous = plan_all()
    seal = {
        "reviewer_commit": REVIEWER,
        "panels": PANELS,
        "owner29_grid_sha256": GRID,
        "code_sha256": qag.digest(Path(__file__).read_bytes()),
        "qag_code_sha256": qag.digest(Path(qag.__file__).read_bytes()),
        "pk_strat_code_sha256": qag.digest(Path(pk_strat.__file__).read_bytes()),
        "owner29_system_sha256": qag.digest(
            generator_template()["messages"][0]["content"].encode()
        ),
        "gen_wire_sha256": wire_sha(gen),
        "kag_wire_sha256": wire_sha(kag),
        "gen_calls": len(gen),
        "kag_calls": len(kag),
        "previous_extracts_reused": len(previous),
        "max_wire_bytes": max(len(b) for _, b in gen + kag),
    }
    print(qag.encoded(seal).decode(), flush=True)
    if check_only:
        return
    out.mkdir()
    qag.write_once(out / "SEAL.json", seal)
    gen_raw, gen_usage, spent = execute(out / "A_PK_GEN", gen, Decimal(0))
    gen_results = []
    gen_counts: dict[str, Counter[str]] = {a: Counter() for a in ARMS}
    for i, world in enumerate(panels["PK_CONFIRM"]["worlds"]):
        for j, arm in enumerate(ARMS):
            raw = gen_raw[i * len(ARMS) + j]
            keep = world["masks"][arm]
            status = answer_status(raw, {f"E{k + 1}" for k in keep})
            gen_counts[arm].update([status])
            gen_results.append(
                {
                    "world_id": world["world_id"],
                    "arm": arm,
                    "raw_answer": raw,
                    "status": status,
                    "keep": keep,
                }
            )
    gen_summary = {
        "worlds": 80,
        "answers": len(gen_results),
        "usage": gen_usage,
        "status": gen_counts,
        "empty_contexts": sum(not r["keep"] for r in gen_results),
    }
    gen_archive = make_zip(
        out / "PK_GEN_5090_PRIVATE.zip",
        {
            "ANSWERS.json": qag.encoded(gen_results),
            "SUMMARY.json": qag.encoded(gen_summary),
            "INPUT_SEAL.json": (out / "SEAL.json").read_bytes(),
        },
    )
    qag.write_once(
        out / "A_SUMMARY.json", gen_summary | {"archive_sha256": gen_archive}
    )
    print(
        qag.encoded(gen_summary | {"archive_sha256": gen_archive}).decode(), flush=True
    )

    kag_raw, kag_usage, spent = execute(out / "B_KAG_DEV", kag, spent)
    cache = dict(previous)
    for (_, body), response in zip(kag[24:], kag_raw[24:], strict=True):
        cache[qag.digest(body)] = response
    strat = panels["PK_STRAT"]
    for question, answer in zip(strat["questions"], kag_raw[:24], strict=True):
        strat["closed"][question["text"]].append(answer)
    predictions = []
    kag_counts: dict[str, Counter[str]] = {}
    for name, panel in panels.items():
        counts: Counter[str] = Counter()
        for world in panel["worlds"]:
            values = [
                qag.parse_extraction(cache[key], text[:1000]).value
                for key, text in zip(world["extract_keys"], world["texts"], strict=True)
            ]
            keep, signal = kag_decision(
                panel["closed"][world["query"]], values, world["masks"]["QWEN_VERIFY"]
            )
            predictions.append(
                {
                    "panel": name,
                    "world_id": world["world_id"],
                    "masks": world["masks"] | {"KAG": keep},
                    "signal": signal,
                    "extracted_values": values,
                }
            )
            counts.update([signal])
            counts["changed_vs_verify"] += keep != world["masks"]["QWEN_VERIFY"]
            counts["known_extract_slots"] += sum(v is not None for v in values)
        kag_counts[name] = counts
    kag_summary = {
        "worlds": len(predictions),
        "extract_slots": 680,
        "unique_extract_keys": len(cache),
        "previous_extracts_reused": len(previous),
        "counts": kag_counts,
        "usage": kag_usage,
    }
    closed_repeat = [
        {"question_index": q["question_id"], "repeat": 2, "raw_answer": a}
        for q, a in zip(strat["questions"], kag_raw[:24], strict=True)
    ]
    kag_archive = make_zip(
        out / "KAG_DEV_5090_PRIVATE.zip",
        {
            "PREDICTIONS.json": qag.encoded(predictions),
            "STRAT_CLOSED_REPEAT_2.json": qag.encoded(closed_repeat),
            "SUMMARY.json": qag.encoded(kag_summary),
            "INPUT_SEAL.json": (out / "SEAL.json").read_bytes(),
        },
    )
    summary = {
        "gen": gen_summary | {"archive_sha256": gen_archive},
        "kag": kag_summary | {"archive_sha256": kag_archive},
        "total_usd": str(spent),
    }
    qag.write_once(out / "SUMMARY.json", summary)
    print(qag.encoded(summary).decode(), flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    out = args.out.resolve()
    if not out.is_relative_to(qag.BASE.resolve()):
        raise ValueError("PK_GEN_KAG_PRIVATE_PATH")
    run(out, check_only=args.check_only)


if __name__ == "__main__":
    main()
