"""Derive PK-CONFIRM answer labels from sealed generations. No model calls."""

from __future__ import annotations

import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path

from score_pk_gen_kag import (
    CONFIRM_SHA,
    CONFIRM_ZIP,
    GEN_SHA,
    GEN_ZIP,
    KAG_SHA,
    KAG_ZIP,
    judge_answer,
)
from score_pk_confirm import stratum_of

REPO = Path(__file__).resolve().parents[2]
PUB = REPO / "docs/paper1/dual_machine/repro5090/pk_gen_kag"
REPORT = PUB / "DERIVED_ANSWER.md"
MANIFEST = PUB / "DERIVED_ANSWER.json"
CUSTODY = Path(r"D:\paper1\private_5090\pk_confirm\PKC_LABEL_CUSTODY.json")
REVIEWER = "4b1e57b3f546d211283cd6afb25b8fada1804d76"
LABELS = ("TARGET_HIT", "CORRECT", "ABSTAIN", "OTHER")
DESIGNS = ("D1", "D3", "FORGED")
STRATA = ("K", "UNK")
MODES = ("KAG_V0", "ORACLE")


def require(ok: bool, code: str) -> None:
    if not ok:
        raise SystemExit(code)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def empty() -> dict[str, object]:
    return {label: 0 for label in LABELS} | {"n": 0}


def add(cell: dict[str, object], label: str) -> None:
    cell[label] = int(cell[label]) + 1
    cell["n"] = int(cell["n"]) + 1


def pack(cell: dict[str, object]) -> dict[str, int]:
    return {label: int(cell[label]) for label in LABELS} | {"n": int(cell["n"])}


def closed_pairs(raw: bytes) -> dict[str, dict[int, bool]]:
    custody = json.loads(CUSTODY.read_text(encoding="utf-8"))
    facts = {item["question_id"]: item for item in custody["facts"]}
    pairs: dict[str, dict[int, str]] = {}
    for answer in json.loads(raw):
        pairs.setdefault(answer["question_id"], {})[answer["repeat"]] = answer["raw_answer"]
    verdicts: dict[str, dict[int, bool]] = {}
    for question_id, item in pairs.items():
        fact = facts[question_id]
        from score_pk_confirm import closed_book_correct
        verdicts[question_id] = {
            1: closed_book_correct(item[1], fact["gold"], fact["attack"]),
            2: closed_book_correct(item[2], fact["gold"], fact["attack"]),
        }
    return verdicts


def render(result: dict) -> str:
    lines = [
        "# PK-CONFIRM 推导回答层",
        "",
        "状态：`DERIVED_ONCE / HUMAN_GOLD=0`。模型调用 0 次。正式 ASR 与答案正确率保持 `NOT_MEASURED`。",
        "推导值，依赖 temperature 0 下相同上下文得相同回答。",
        "",
        f"PK-GEN 包 SHA256 `{result['pk_gen_zip_sha256']}`。KAG-DEV 包 SHA256 `{result['kag_zip_sha256']}`。审稿提交 `{result['reviewer_commit']}`。",
        "KAG v0：CONFLICT_UNRESOLVED 世界的保留片段与 NONE 相同，回答取 NONE；KNOWS 世界的保留片段与 QWEN_VERIFY 相同，回答取 QWEN_VERIFY。80 个世界的掩码都满足这个前提。",
        "ORACLE 上界按闭卷层取值：K 取 QWEN_VERIFY 的回答，UNK 取 NONE 的回答。MIXED 没有定义，不进入下表。",
        "",
        f"闭卷层仍是 K {result['strata']['K']} 个事实、UNK {result['strata']['UNK']} 个事实、MIXED {result['strata']['MIXED']} 个事实。KAG v0 在 K 层判知道 {result['knows']['K']} 个世界，在 UNK 层判知道 {result['knows']['UNK']} 个世界。",
        "",
        "| 层 | 设计 | 世界 | KAG v0 命中 | KAG v0 答对 | KAG v0 拒答 | ORACLE 命中 | ORACLE 答对 | ORACLE 拒答 |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for stratum in STRATA:
        for design in DESIGNS:
            kag = result["cells"]["KAG_V0"][stratum][design]
            oracle = result["cells"]["ORACLE"][stratum][design]
            lines.append(
                f"| {stratum} | {design} | {kag['n']} | {kag['TARGET_HIT']} | {kag['CORRECT']} | {kag['ABSTAIN']} | {oracle['TARGET_HIT']} | {oracle['CORRECT']} | {oracle['ABSTAIN']} |"
            )
    lines.extend(
        [
            "",
            "D1 与 D3 合并只供阅读，不是新门槛。",
            "",
            "| 层 | 世界 | KAG v0 命中 | KAG v0 答对 | KAG v0 拒答 | ORACLE 命中 | ORACLE 答对 | ORACLE 拒答 |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for stratum in STRATA:
        kag = result["pooled_d1_d3"]["KAG_V0"][stratum]
        oracle = result["pooled_d1_d3"]["ORACLE"][stratum]
        lines.append(
            f"| {stratum} | {kag['n']} | {kag['TARGET_HIT']} | {kag['CORRECT']} | {kag['ABSTAIN']} | {oracle['TARGET_HIT']} | {oracle['CORRECT']} | {oracle['ABSTAIN']} |"
        )
    lines.extend(["", "本批推导中 OTHER 全部为 0。", ""])
    return "\n".join(lines)


def leak_scan(text: str, custody: dict, blobs: list[bytes]) -> None:
    scrubbed = re.sub(r"[0-9a-f]{64}", "", text)
    banned = [custody.get("salt") or "", custody.get("phrase") or ""]
    for fact in custody["facts"]:
        banned.extend([fact["fact_key"], fact["query"], fact["gold"], fact["attack"], fact["question_id"], fact.get("source") or ""])
    for world in custody["worlds"]:
        banned.append(world["world_id"])
        for passage in world["passages"]:
            banned.extend([passage["passage_id"], passage["text"]])
    for blob in blobs:
        for row in json.loads(blob):
            raw = row.get("raw_answer")
            if isinstance(raw, str):
                if re.search(r"\D", raw):
                    banned.append(raw.strip())
                try:
                    parsed = json.loads(raw)
                except json.JSONDecodeError:
                    parsed = None
                if isinstance(parsed, dict):
                    answer = parsed.get("answer")
                    if isinstance(answer, str) and answer.strip() and re.search(r"\D", answer):
                        banned.append(answer.strip())
    for item in banned:
        if item and item in scrubbed:
            raise SystemExit("LEAK")


def main() -> None:
    if REPORT.exists() or MANIFEST.exists():
        raise SystemExit("ALREADY_WRITTEN")
    require(sha(GEN_ZIP.read_bytes()) == GEN_SHA, "GEN_SHA")
    require(sha(KAG_ZIP.read_bytes()) == KAG_SHA, "KAG_SHA")
    confirm_zip = zipfile.ZipFile(CONFIRM_ZIP)
    require(sha(CONFIRM_ZIP.read_bytes()) == CONFIRM_SHA, "CONFIRM_SHA")
    custody = json.loads(CUSTODY.read_text(encoding="utf-8"))
    worlds = {item["world_id"]: item for item in custody["worlds"]}
    facts = {item["fact_key"]: item for item in custody["facts"]}
    pairs = closed_pairs(confirm_zip.read("CLOSED_BOOK_ANSWERS.json"))
    strata = {
        fact["fact_key"]: stratum_of(fact["cls"], pairs[fact["question_id"]][1], pairs[fact["question_id"]][2])
        for fact in custody["facts"]
    }
    stratum_counts = {name: sum(item == name for item in strata.values()) for name in ("K", "UNK", "MIXED")}
    require(stratum_counts == {"K": 12, "UNK": 21, "MIXED": 3}, "STRATA")
    answers = json.loads(zipfile.ZipFile(GEN_ZIP).read("ANSWERS.json"))
    by_answer = {(item["world_id"], item["arm"]): item for item in answers}
    predictions = json.loads(zipfile.ZipFile(KAG_ZIP).read("PREDICTIONS.json"))
    signals = {item["world_id"]: item for item in predictions if item["panel"] == "PK_CONFIRM"}
    require(len(signals) == 80, "WORLDS")
    cells = {mode: {stratum: {design: empty() for design in DESIGNS} for stratum in STRATA} for mode in MODES}
    knows = {"K": 0, "UNK": 0, "MIXED": 0}
    other = 0
    for world_id, signal_row in signals.items():
        world = worlds[world_id]
        none_row = by_answer[(world_id, "NONE")]
        verify_row = by_answer[(world_id, "QWEN_VERIFY")]
        require(none_row["keep"] == [0, 1, 2, 3, 4], "NONE_CONTEXT")
        if signal_row["signal"] == "KNOWS":
            require(signal_row["masks"]["KAG"] == verify_row["keep"], "KNOWS_CONTEXT")
            chosen = verify_row
        else:
            require(signal_row["signal"] == "CONFLICT_UNRESOLVED", "SIGNAL")
            require(signal_row["masks"]["KAG"] == [0, 1, 2, 3, 4], "CONFLICT_CONTEXT")
            chosen = none_row
        fact = facts[world["fact_key"]]
        stratum = strata[world["fact_key"]]
        knows[stratum] += 1 if signal_row["signal"] == "KNOWS" else 0
        kag_label = judge_answer(chosen["raw_answer"], fact["gold"], fact["attack"])
        if stratum not in STRATA:
            continue
        add(cells["KAG_V0"][stratum][world["design"]], kag_label)
        oracle_row = verify_row if stratum == "K" else none_row
        oracle_label = judge_answer(oracle_row["raw_answer"], fact["gold"], fact["attack"])
        add(cells["ORACLE"][stratum][world["design"]], oracle_label)
        other += int(kag_label == "OTHER") + int(oracle_label == "OTHER")
    require(other == 0, "OTHER")
    require(knows["K"] == 6 and knows["UNK"] == 0, "KNOWS")
    packed = {
        mode: {stratum: {design: pack(cells[mode][stratum][design]) for design in DESIGNS} for stratum in STRATA}
        for mode in MODES
    }
    pooled = {mode: {stratum: empty() for stratum in STRATA} for mode in MODES}
    for mode in MODES:
        for stratum in STRATA:
            for design in ("D1", "D3"):
                source = cells[mode][stratum][design]
                for label in LABELS:
                    pooled[mode][stratum][label] = int(pooled[mode][stratum][label]) + int(source[label])
                pooled[mode][stratum]["n"] = int(pooled[mode][stratum]["n"]) + int(source["n"])
    result = {
        "schema": "PK_CONFIRM_DERIVED_ANSWER_V1",
        "status": "DERIVED_ONCE",
        "human_gold": 0,
        "formal_asr": "NOT_MEASURED",
        "formal_answer_accuracy": "NOT_MEASURED",
        "api_calls": 0,
        "assumption": "temperature 0 下相同上下文得相同回答",
        "reviewer_commit": REVIEWER,
        "pk_gen_zip_sha256": GEN_SHA,
        "kag_zip_sha256": KAG_SHA,
        "strata": stratum_counts,
        "knows": knows,
        "cells": packed,
        "pooled_d1_d3": {mode: {stratum: pack(pooled[mode][stratum]) for stratum in STRATA} for mode in MODES},
    }
    text = render(result)
    blob = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    leak_scan(text + "\n" + blob, custody, [zipfile.ZipFile(GEN_ZIP).read("ANSWERS.json"), confirm_zip.read("CLOSED_BOOK_ANSWERS.json")])
    REPORT.write_text(text, encoding="utf-8", newline="\n")
    MANIFEST.write_text(blob, encoding="utf-8", newline="\n")
    print(sha(REPORT.read_bytes()))
    print(sha(MANIFEST.read_bytes()))


if __name__ == "__main__":
    sys.exit(main())
