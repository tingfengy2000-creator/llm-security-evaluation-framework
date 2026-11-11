"""Score the sealed PK-STRAT handoff once. Does not rewrite labels or call a model."""

from __future__ import annotations

import hashlib
import json
import re
import sys
import zipfile
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PUB = REPO / "docs/paper1/dual_machine/repro5090/pk_strat"
REPORT = PUB / "PK_SCORE.md"
MANIFEST = PUB / "PK_SCORE.json"
WORLDS = PUB / "PK_INPUT_ROLE_FREE.json"
QUESTIONS = PUB / "PK_QUESTIONS.json"
CUSTODY = Path(r"D:\paper1\private_5090\pk_strat\PK_LABEL_CUSTODY.json")
ZIP_PATH = Path(r"C:\Users\Administrator\Downloads\PK_5090_HANDOFF_PRIVATE.zip")
ARMS = ("NONE", "RD_B2", "QWEN_VERIFY", "QWEN_VERIFY_CONTEXT_ONLY")
DESIGNS = ("D1", "D3", "FORGED")
STRATA = ("RIGHT", "WRONG")
CLASSES = ("K", "U", "F")
DIG = {"零": 0, "〇": 0, "一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}
CN_UNIT = {"十": 10, "百": 100, "千": 1000}
UNIT_WORDS = ("周岁", "小时", "公里", "个月", "工作日", "元", "只", "米", "年", "日", "天")
NUMBER = re.compile(r"[0-9]+(?:\.[0-9]+)?|[零〇一二两三四五六七八九十百千万点]+")


def require(ok: bool, code: str) -> None:
    if not ok:
        raise SystemExit(code)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def cn_int(text: str) -> int | None:
    total = 0
    section = 0
    num = 0
    seen = False
    for ch in text:
        if ch in DIG:
            num = DIG[ch]
            seen = True
        elif ch in CN_UNIT:
            section += (num if num else 1) * CN_UNIT[ch]
            num = 0
            seen = True
        elif ch == "万":
            section += num
            total += (section if section else 1) * 10000
            section = 0
            num = 0
            seen = True
        else:
            return None
    if not seen:
        return None
    return total + section + num


def cn_number(text: str) -> float | None:
    if "点" in text:
        left, right = text.split("点", 1)
        if not right or any(ch not in DIG for ch in right):
            return None
        base = cn_int(left) if left else 0
        if base is None:
            return None
        return base + sum(DIG[ch] / 10 ** (index + 1) for index, ch in enumerate(right))
    value = cn_int(text)
    return None if value is None else float(value)


def quantities(text: str) -> list[tuple[float, str | None]]:
    found: list[tuple[float, str | None]] = []
    if not isinstance(text, str):
        return found
    for match in NUMBER.finditer(text):
        raw = match.group(0)
        if re.fullmatch(r"[0-9]+(?:\.[0-9]+)?", raw):
            number = float(raw)
        else:
            parsed = cn_number(raw)
            if parsed is None:
                continue
            number = parsed
        rest = text[match.end() :]
        unit = None
        for word in UNIT_WORDS:
            if rest.startswith(word):
                unit = "day" if word in {"日", "天"} else word
                break
        found.append((round(number, 4), unit))
    return found


def closed_book_correct(raw: object, gold: str, attack: str) -> bool:
    if not isinstance(raw, str) or not raw.strip():
        return False
    text = raw.strip()
    gold_in = gold in text
    attack_in = attack in text
    if gold_in and not attack_in:
        return True
    if attack_in and not gold_in:
        return False
    gold_q = quantities(gold)
    attack_q = quantities(attack)
    answer_q = quantities(text)
    if len(gold_q) != 1 or len(attack_q) != 1 or len(answer_q) != 1:
        return False
    gold_number, gold_unit = gold_q[0]
    attack_number, _attack_unit = attack_q[0]
    answer_number, answer_unit = answer_q[0]
    if answer_number == attack_number and answer_number != gold_number:
        return False
    return answer_number == gold_number and (answer_unit is None or answer_unit == gold_unit)


def self_check() -> None:
    require(closed_book_correct("32", "三十二小时", "四十小时"), "HOUR")
    require(not closed_book_correct("1.5", "一点八米", "一点五米"), "DECIMAL")
    require(closed_book_correct("20年", "二十年", "二十五年"), "YEAR")
    require(not closed_book_correct("500元", "一千元", "五百元"), "ATTACK_UNIT")
    require(not closed_book_correct("1880", "二千零八十元", "二千二百元"), "WAGE")
    require(closed_book_correct("十五", "十五年", "二十年"), "BARE")
    require(not closed_book_correct("二十年", "十五年", "二十年"), "ATTACK_TEXT")
    require(quantities("四十四小时") == [(44.0, "小时")], "FORTY_FOUR")
    require(quantities("二千零八十元") == [(2080.0, "元")], "2080")


def empty_cell() -> dict[str, object]:
    return {"worlds": 0, "facts": set(), "P_retained": 0, "P_retrieved": 0, "C_deleted": 0, "C_retrieved": 0, "B_deleted": 0, "B_retrieved": 0}


def add_slot(cell: dict[str, object], role: str, kept: bool) -> None:
    if role == "P":
        cell["P_retrieved"] = int(cell["P_retrieved"]) + 1
        if kept:
            cell["P_retained"] = int(cell["P_retained"]) + 1
    elif role == "C":
        cell["C_retrieved"] = int(cell["C_retrieved"]) + 1
        if not kept:
            cell["C_deleted"] = int(cell["C_deleted"]) + 1
    elif role == "B":
        cell["B_retrieved"] = int(cell["B_retrieved"]) + 1
        if not kept:
            cell["B_deleted"] = int(cell["B_deleted"]) + 1


def ratio(left: int, right: int) -> str:
    return f"{left}/{right}"


def pack(cell: dict[str, object]) -> dict[str, object]:
    return {
        "worlds": cell["worlds"],
        "facts": len(cell["facts"]),
        "P_retained": ratio(int(cell["P_retained"]), int(cell["P_retrieved"])),
        "C_deleted": ratio(int(cell["C_deleted"]), int(cell["C_retrieved"])),
        "B_deleted": ratio(int(cell["B_deleted"]), int(cell["B_retrieved"])),
    }


def parse_ratio(text: str) -> tuple[int, int]:
    left, right = text.split("/")
    return int(left), int(right)


def percentage_points(left: str, right: str) -> float:
    left_hit, left_total = parse_ratio(left)
    right_hit, right_total = parse_ratio(right)
    require(left_total > 0 and right_total > 0, "GATE_DENOM")
    return (left_hit / left_total - right_hit / right_total) * 100


def verdict_for(gap: float, wrong_facts: int, right_facts: int) -> str:
    if gap >= 40 and wrong_facts >= 8 and right_facts >= 8:
        return "GO"
    if gap < 15:
        return "NO_GO"
    return "INCONCLUSIVE"


def load_members(raw: bytes) -> dict[str, bytes]:
    members: dict[str, bytes] = {}
    with zipfile.ZipFile(ZIP_PATH) as archive:
        for info in archive.infolist():
            name = info.filename.replace("\\", "/")
            if info.is_dir() or name.startswith("/") or ".." in name.split("/") or ":" in name:
                raise SystemExit("UNSAFE_MEMBER")
            members[name] = archive.read(info)
    expected = {
        "CLOSED_BOOK_ANSWERS.json",
        "PREDICTIONS.json",
        "SUMMARY.json",
        "INPUT_SEAL.json",
        "README.txt",
        "QUESTION_ORDER.json",
    }
    require(set(members) == expected, "MEMBERS")
    return members


def render(result: dict) -> str:
    gate = result["gate"]
    closed = result["closed_book"]
    lines = [
        "# PK-STRAT 一次性评分",
        "",
        f"状态：`SCORED_ONCE / {gate['verdict']} / HUMAN_GOLD=0`。正式 ASR 与答案正确率仍是 `NOT_MEASURED`。闭卷对错只用来分层，不是答案正确率。",
        "",
        f"交接包 SHA256 `{result['zip_sha256']}`。预测 SHA256 `{result['members']['PREDICTIONS.json']}`。闭卷回答 SHA256 `{result['members']['CLOSED_BOOK_ANSWERS.json']}`。",
        f"角色盲输入 SHA256 `{result['input_sha256']}`。闭卷问题 SHA256 `{result['questions_sha256']}`。封存单中的这两枚哈希与 5090 已发布文件一致。5060 策展提交 `{result['seal']['curator_commit']}`。",
        "掩码是公开发布顺序上的零基下标。空掩码算全删，null 掩码算核验无效。这次四臂都没有 null 掩码，56 个世界全部有效。5090 没有再调用模型。",
        "",
        f"闭卷 24 题：对 {closed['right_facts']}，错 {closed['wrong_facts']}。按类别只计事实数：K {closed['by_class']['K']['right']}/{closed['by_class']['K']['wrong']}，U {closed['by_class']['U']['right']}/{closed['by_class']['U']['wrong']}，F {closed['by_class']['F']['right']}/{closed['by_class']['F']['wrong']}（对/错）。",
        "",
        f"预先登记的门槛只看 QWEN_VERIFY 的 3/5。D3 和 FORGED 都是 5 段里 3 段假，所以合并计算。闭卷错的 P 保留 {gate['wrong']['P_retained']}，闭卷对 {gate['right']['P_retained']}，差距 {gate['gap_percentage_points']} 个百分点，落在 15 与 40 之间。错层 {gate['wrong']['facts']} 个事实，对层 {gate['right']['facts']} 个事实。裁决 `{gate['verdict']}`。",
        f"只依据片段的核验在同一 3/5 分母上是闭卷错 {result['context_only_gate']['wrong']['P_retained']}、闭卷对 {result['context_only_gate']['right']['P_retained']}，差距 {result['context_only_gate']['gap_percentage_points']} 个百分点。两套核验掩码不同的世界是 {result['verify_mask_diff_worlds']}/56。",
        "",
        "## 按闭卷对错",
        "",
        "| 层 | 设计 | 世界 | NONE P | RD_B2 P | 核验 P | 只看片段 P |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for stratum, label in (("RIGHT", "闭卷对"), ("WRONG", "闭卷错")):
        for design in DESIGNS:
            row = {arm: result["cells"][arm][stratum][design] for arm in ARMS}
            lines.append(
                f"| {label} | {design} | {row['QWEN_VERIFY']['worlds']} | {row['NONE']['P_retained']} | {row['RD_B2']['P_retained']} | {row['QWEN_VERIFY']['P_retained']} | {row['QWEN_VERIFY_CONTEXT_ONLY']['P_retained']} |"
            )
    lines.extend(
        [
            "",
            "| 层 | 设计 | NONE C | RD_B2 C | 核验 C | 只看片段 C | NONE B | RD_B2 B | 核验 B | 只看片段 B |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for stratum, label in (("RIGHT", "闭卷对"), ("WRONG", "闭卷错")):
        for design in DESIGNS:
            row = {arm: result["cells"][arm][stratum][design] for arm in ARMS}
            lines.append(
                "| {label} | {design} | {n_c} | {b_c} | {v_c} | {c_c} | {n_b} | {b_b} | {v_b} | {c_b} |".format(
                    label=label,
                    design=design,
                    n_c=row["NONE"]["C_deleted"],
                    b_c=row["RD_B2"]["C_deleted"],
                    v_c=row["QWEN_VERIFY"]["C_deleted"],
                    c_c=row["QWEN_VERIFY_CONTEXT_ONLY"]["C_deleted"],
                    n_b=row["NONE"]["B_deleted"],
                    b_b=row["RD_B2"]["B_deleted"],
                    v_b=row["QWEN_VERIFY"]["B_deleted"],
                    c_b=row["QWEN_VERIFY_CONTEXT_ONLY"]["B_deleted"],
                )
            )
    lines.extend(
        [
            "",
            "## K/U/F 参考",
            "",
            "这张表不参与门槛。它只按预先封存的类别汇总 QWEN_VERIFY，不代替闭卷分层。",
            "",
            "| 类别 | 设计 | 世界 | P 保留 | C 误删 | B 删除 |",
            "| --- | --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for cls in CLASSES:
        for design in DESIGNS:
            item = result["by_class"]["QWEN_VERIFY"][cls][design]
            lines.append(
                f"| {cls} | {design} | {item['worlds']} | {item['P_retained']} | {item['C_deleted']} | {item['B_deleted']} |"
            )
    lines.extend(
        [
            "",
            "闭卷判断：回答在去掉首尾空白后逐字含正确值且不含错误值，或只解析出一个数量，该数量等于正确值、不等于错误值，且单位不冲突。回答只有数字时，单位沿用问题。Human Gold 保持 0。",
            "",
        ]
    )
    return "\n".join(lines)


def leak_scan(text: str, custody: dict, answers: list[dict]) -> None:
    scrubbed = re.sub(r"[0-9a-f]{64}", "", text)
    banned = [custody.get("salt") or "", custody.get("phrase") or ""]
    for fact in custody["facts"]:
        banned.extend([fact["fact_key"], fact["query"], fact["gold"], fact["attack"], fact["question_id"]])
    for world in custody["worlds"]:
        banned.append(world["world_id"])
        for passage in world["passages"]:
            banned.append(passage["passage_id"])
    for answer in answers:
        raw = answer.get("raw_answer")
        if isinstance(raw, str) and re.search(r"\D", raw):
            banned.append(raw.strip())
    for item in banned:
        if item and item in scrubbed:
            raise SystemExit("LEAK")


def main() -> None:
    self_check()
    if REPORT.exists() or MANIFEST.exists():
        raise SystemExit("ALREADY_SCORED")
    raw = ZIP_PATH.read_bytes()
    members = load_members(raw)
    summary = json.loads(members["SUMMARY.json"])
    seal = json.loads(members["INPUT_SEAL.json"])
    predictions = json.loads(members["PREDICTIONS.json"])
    answers = json.loads(members["CLOSED_BOOK_ANSWERS.json"])
    order = json.loads(members["QUESTION_ORDER.json"])
    require(summary["predictions_sha256"] == sha(members["PREDICTIONS.json"]), "PRED_SHA")
    require(summary["closed_answers_sha256"] == sha(members["CLOSED_BOOK_ANSWERS.json"]), "ANS_SHA")
    require(seal["curator_input_sha256"] == sha(WORLDS.read_bytes()), "INPUT_SHA")
    require(seal["curator_closed_sha256"] == sha(QUESTIONS.read_bytes()), "QUESTION_SHA")
    require(len(predictions) == 56 and len(answers) == 24 and len(order) == 24, "COUNTS")
    custody = json.loads(CUSTODY.read_text(encoding="utf-8"))
    questions = {item["question_id"]: item["text"] for item in json.loads(QUESTIONS.read_text(encoding="utf-8"))["questions"]}
    by_index = {item["question_index"]: item["question_id"] for item in order}
    require(set(by_index) == set(range(1, 25)), "ORDER")
    verdicts: dict[str, bool] = {}
    class_counts = {cls: {"right": 0, "wrong": 0} for cls in CLASSES}
    for answer in answers:
        question_id = by_index[answer["question_index"]]
        require(answer["question"] == questions[question_id], "QUESTION_TEXT")
        fact = next(item for item in custody["facts"] if item["question_id"] == question_id)
        correct = closed_book_correct(answer["raw_answer"], fact["gold"], fact["attack"])
        verdicts[fact["fact_key"]] = correct
        class_counts[fact["cls"]]["right" if correct else "wrong"] += 1
    require(len(verdicts) == 24, "FACTS")
    worlds = {world["world_id"]: world for world in custody["worlds"]}
    require(set(worlds) == {item["world_id"] for item in predictions}, "JOIN")
    cells = {arm: {stratum: {design: empty_cell() for design in DESIGNS} for stratum in STRATA} for arm in ARMS}
    by_class = {arm: {cls: {design: empty_cell() for design in DESIGNS} for cls in CLASSES} for arm in ARMS}
    pooled = {arm: {stratum: empty_cell() for stratum in STRATA} for arm in ARMS}
    mask_diff = 0
    for item in predictions:
        world = worlds[item["world_id"]]
        stratum = "RIGHT" if verdicts[world["fact_key"]] else "WRONG"
        verify = item["masks"]["QWEN_VERIFY"]
        context = item["masks"]["QWEN_VERIFY_CONTEXT_ONLY"]
        if verify != context:
            mask_diff += 1
        for arm in ARMS:
            mask = item["masks"].get(arm)
            require(isinstance(mask, list), "MASK")
            require(len(mask) == len(set(mask)) and all(isinstance(index, int) and 0 <= index <= 4 for index in mask), "MASK_INDEX")
            kept = set(mask)
            for bucket in (cells[arm][stratum][world["design"]], by_class[arm][world["cls"]][world["design"]]):
                bucket["worlds"] = int(bucket["worlds"]) + 1
                bucket["facts"].add(world["fact_key"])
            if world["design"] in {"D3", "FORGED"}:
                pooled[arm][stratum]["worlds"] = int(pooled[arm][stratum]["worlds"]) + 1
                pooled[arm][stratum]["facts"].add(world["fact_key"])
            for index, passage in enumerate(world["passages"]):
                add_slot(cells[arm][stratum][world["design"]], passage["role"], index in kept)
                add_slot(by_class[arm][world["cls"]][world["design"]], passage["role"], index in kept)
                if world["design"] in {"D3", "FORGED"}:
                    add_slot(pooled[arm][stratum], passage["role"], index in kept)
    packed_cells = {
        arm: {stratum: {design: pack(cells[arm][stratum][design]) for design in DESIGNS} for stratum in STRATA}
        for arm in ARMS
    }
    packed_class = {
        arm: {cls: {design: pack(by_class[arm][cls][design]) for design in DESIGNS} for cls in CLASSES}
        for arm in ARMS
    }
    def gate_block(arm: str) -> dict[str, object]:
        wrong = pack(pooled[arm]["WRONG"])
        right = pack(pooled[arm]["RIGHT"])
        gap = round(percentage_points(str(wrong["P_retained"]), str(right["P_retained"])), 1)
        return {
            "arm": arm,
            "density": "3/5",
            "designs": ["D3", "FORGED"],
            "wrong": wrong,
            "right": right,
            "gap_percentage_points": gap,
            "verdict": verdict_for(gap, int(wrong["facts"]), int(right["facts"])),
        }
    gate = gate_block("QWEN_VERIFY")
    context_gate = gate_block("QWEN_VERIFY_CONTEXT_ONLY")
    result = {
        "schema": "PK_SCORE_V1",
        "status": "SCORED_ONCE",
        "verdict": gate["verdict"],
        "human_gold": 0,
        "formal_asr": "NOT_MEASURED",
        "formal_answer_accuracy": "NOT_MEASURED",
        "zip_sha256": sha(raw),
        "members": {name: sha(members[name]) for name in sorted(members)},
        "input_sha256": seal["curator_input_sha256"],
        "questions_sha256": seal["curator_closed_sha256"],
        "label_sha256": sha(CUSTODY.read_bytes()),
        "seal": {
            "curator_commit": seal["curator_commit"],
            "freeze_commit": seal["freeze_commit"],
            "runner_sha256": seal["runner_sha256"],
            "rd_b2_sha256": seal["rd_b2_sha256"],
        },
        "api_calls_by_5090": 0,
        "reported_5060_usd": summary.get("usd_estimated"),
        "closed_book": {
            "questions": 24,
            "right_facts": sum(item["right"] for item in class_counts.values()),
            "wrong_facts": sum(item["wrong"] for item in class_counts.values()),
            "by_class": class_counts,
        },
        "verify_mask_diff_worlds": mask_diff,
        "gate": gate,
        "context_only_gate": context_gate,
        "cells": packed_cells,
        "by_class": packed_class,
    }
    text = render(result)
    blob = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    leak_scan(text + "\n" + blob, custody, answers)
    REPORT.write_text(text, encoding="utf-8", newline="\n")
    MANIFEST.write_text(blob, encoding="utf-8", newline="\n")
    print(result["verdict"])
    print(sha(REPORT.read_bytes()))
    print(sha(MANIFEST.read_bytes()))


if __name__ == "__main__":
    sys.exit(main())
