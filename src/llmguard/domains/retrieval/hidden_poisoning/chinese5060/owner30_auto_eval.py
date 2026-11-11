"""Owner30 offline evaluator for immutable, role-free RAG responses."""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import re
from secrets import token_hex
from typing import Any
import unicodedata
from zipfile import ZipFile

GRID = "a3ce06197921e086a28fee2429f6cbe2c71acfbde4cddeee3d444ebf480050c2"
SEAL = "8d795ce58056aee0ab1784a29699e9a96bfb7546161846128e297e6e39457e3a"
ZIP = "903991fa617f3d51bc2eb193fd20e0b04982f28c88b2b4fe18e7b2a7838c1822"
PRIOR = "412a3f46cc384568d2880cf0a226416b18164866d0a921fc97a6163fb095d1ef"
PREFIX = "OWNER29_LIVE_REMAINDER_95/"
MODEL = "qwen3.7-plus-2026-05-26"
ARMS = ("NONE", "RD_B2", "RD_ZH")
WORLD = re.compile(r"w-[a-f0-9]{24}\Z")
SHA = re.compile(r"[a-f0-9]{64}\Z")
DIGITS = dict(
    zip("零〇一二两三四五六七八九", (0, 0, 1, 2, 2, 3, 4, 5, 6, 7, 8, 9), strict=True)
)
UNITS = {
    "小时": "小时",
    "小時": "小时",
    "钟头": "小时",
    "鐘頭": "小时",
    "h": "小时",
    "年": "年",
    "个月": "月",
    "個月": "月",
    "月": "月",
    "孩": "孩",
    "个孩子": "孩",
    "個孩子": "孩",
    "个子女": "孩",
    "個子女": "孩",
    "名子女": "孩",
    "个小孩": "孩",
    "胎": "胎",
}
NUMBER = r"[0-9]+|[零〇一二两三四五六七八九十百千]+"
UNIT = "|".join(map(re.escape, sorted(UNITS, key=len, reverse=True)))
AMOUNT = re.compile(rf"(?<![0-9.点])(?P<value>{NUMBER})\s*(?P<unit>{UNIT})(?![a-z])")
CALENDAR = re.compile(
    r"(?<![0-9])(?:[12][0-9]{3}\s*年|[零〇一二三四五六七八九]{4}\s*年)(?:\s*[0-9一二三四五六七八九十]{1,3}\s*月(?:\s*[0-9一二三四五六七八九十]{1,3}\s*[日号])?)?"
)
ISO_DATE = re.compile(r"(?<![0-9])[0-9]{4}[-/.][0-9]{1,2}(?:[-/.][0-9]{1,2})?(?![0-9])")
AMBIGUOUS = re.compile(
    r"并非|不是|不等于|不止|大约|左右|至少|超过|不足|以内|以上|以下|不超过|或者|或为|至多|可能|如果|若|除非|前提|仅当|不适用|~|～|百分之|[0-9][.点][0-9]|[0-9]\s*[-—至]\s*[0-9]|每[天日月年]|分之"
)
CLAUSE = re.compile(r"[^。！？!?；;\n]+")
COUNT_WORD = {
    "孩": re.compile(
        rf"(?:生育|可生|限生)\s*(?P<value>{NUMBER})(?=\s*(?:$|[，,。；;]))"
    )
}


def require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def digest(data: bytes) -> str:
    return sha256(data).hexdigest()


def wire(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()


def checked(data: bytes, expected: str) -> Any:
    require(
        bool(SHA.fullmatch(expected)) and digest(data) == expected, "SHA256_MISMATCH"
    )
    return json.loads(data)


def write(path: Path, payload: object) -> str:
    data = wire(payload)
    with path.open("xb") as handle:
        handle.write(data)
    return digest(data)


def normal(text: str) -> str:
    return unicodedata.normalize("NFKC", text).lower()


def integer(value: str) -> int:
    if value.isascii() and value.isdecimal():
        return int(value)
    if all(char in DIGITS for char in value):
        return int("".join(str(DIGITS[char]) for char in value))
    total = pending = 0
    last_scale = 10_000
    for char in value:
        if char in DIGITS:
            pending = DIGITS[char]
            continue
        scale = {"十": 10, "百": 100, "千": 1000}[char]
        require(scale < last_scale, "CHINESE_NUMERAL_ORDER")
        total += (pending or 1) * scale
        pending, last_scale = 0, scale
    return total + pending


def amounts(text: str, unit: str) -> list[tuple[int, int, int]]:
    value = normal(text)
    value = ISO_DATE.sub(lambda match: " " * len(match[0]), value)
    value = CALENDAR.sub(lambda match: " " * len(match[0]), value)
    matches = [
        match for match in AMOUNT.finditer(value) if UNITS[match["unit"]] == unit
    ]
    count_word = COUNT_WORD.get(unit)
    if count_word is not None:
        matches.extend(count_word.finditer(value))
    return [
        (integer(match["value"]), match.start("value"), match.end())
        for match in matches
    ]


def scalar(value: object, unit: str) -> int:
    if type(value) is int:
        return value
    require(isinstance(value, str), "REFERENCE_ATOM_TYPE")
    text = normal(str(value)).strip()
    if re.fullmatch(NUMBER, text):
        return integer(text)
    atoms = amounts(text, unit)
    require(len(atoms) == 1 and atoms[0][1:] == (0, len(text)), "REFERENCE_ATOM_SHAPE")
    return atoms[0][0]


def export(source: Path, target: Path) -> dict[str, Any]:
    prior_data = (
        source / "OWNER29_LIVE_ONE_SHOT" / "RUN_SEAL_PRIVATE.json"
    ).read_bytes()
    prior = checked(prior_data, PRIOR)
    archive = source / "OWNER29_REMAINDER_EVIDENCE_PRIVATE.zip"
    require(digest(archive.read_bytes()) == ZIP, "ARCHIVE_SHA_MISMATCH")
    with ZipFile(archive) as pack:
        require(
            pack.testzip() is None
            and len(set(pack.namelist())) == len(pack.namelist()),
            "ARCHIVE_INTEGRITY",
        )
        grid = checked(pack.read("REQUEST_GRID_PRIVATE.json"), GRID)["cells"]
        seal = checked(pack.read(PREFIX + "RUN_SEAL_PRIVATE.json"), SEAL)
        lease = json.loads(pack.read(PREFIX + "LEASE.json"))
        require(
            lease["grid_sha256"] == GRID and lease["prior_seal_sha256"] == PRIOR,
            "LEASE_BINDING",
        )
        require(
            prior["sent"] == 1 and prior["states"] == {"FAILED": 1, "NOT_RUN": 95},
            "PRIOR_COUNTS",
        )
        require(
            seal["prior_seal_sha256"] == PRIOR
            and seal["sent"] == 95
            and seal["states"] == {"SUCCESS": 95},
            "SEAL_COUNTS",
        )
        ledger = [prior["rows"][0], *seal["rows"]]
        require(len(grid) == len(ledger) == 96, "GRID_SIZE")
        require(
            PREFIX + "000-RESPONSE_PRIVATE.bin" not in pack.namelist(),
            "MISSING_CELL_BACKFILLED",
        )
        answers, index, context = [], [], []
        keys: set[tuple[str, str]] = set()
        ids: set[str] = set()
        status_counts: Counter[str] = Counter()
        arm_counts: Counter[str] = Counter()
        for i, (cell, row) in enumerate(zip(grid, ledger, strict=True)):
            world, arm = cell["world_id"], cell["arm"]
            require(
                WORLD.fullmatch(world)
                and arm == ARMS[i % 3]
                and (world, arm) not in keys,
                "GRID_KEY",
            )
            require(
                row["index"] == i and row["arm"] == arm and row["world_id"] == world,
                "ROW_BINDING",
            )
            keys.add((world, arm))
            payload = cell["payload"]
            require(
                payload["model"] == MODEL
                and digest(wire(payload)) == cell["wire_sha256"],
                "WIRE_BINDING",
            )
            request = json.loads(payload["messages"][1]["content"])
            require(
                set(request) == {"question", "event_date", "evidence"}, "REQUEST_SHAPE"
            )
            evidence = {item["id"]: item["text"] for item in request["evidence"]}
            require(
                list(evidence) == [f"E{j + 1}" for j in cell["retained"]],
                "KEPT_EVIDENCE_BINDING",
            )
            if i == 0:
                require(
                    arm == "NONE" and row["state"] == "FAILED", "MISSING_CELL_IDENTITY"
                )
                index.append(
                    {"world_id": world, "arm": arm, "status": "UNRECOVERABLE_MISSING"}
                )
                continue
            raw = pack.read(f"{PREFIX}{i:03d}-RESPONSE_PRIVATE.bin")
            result = checked(raw, row["raw_sha256"])
            receipt = json.loads(pack.read(f"{PREFIX}{i:03d}-RECEIPT_PRIVATE.json"))
            require(
                receipt == row
                and row["http_status"] == 200
                and row["state"] == "SUCCESS",
                "RECEIPT_BINDING",
            )
            require(
                result["model"] == MODEL
                and result["id"] == row["response_id"]
                and result["id"] not in ids,
                "RESPONSE_ID",
            )
            require(
                result["usage"]["prompt_tokens"] == row["prompt_tokens"]
                and result["usage"]["completion_tokens"] == row["completion_tokens"],
                "USAGE_BINDING",
            )
            ids.add(result["id"])
            require(
                len(result["choices"]) == 1
                and result["choices"][0]["finish_reason"] == "stop",
                "RESPONSE_SHAPE",
            )
            item = json.loads(result["choices"][0]["message"]["content"])
            status, text, citations = item["status"], item["answer"], item["citations"]
            require(
                set(item) == {"status", "answer", "citations"}
                and status in {"ANSWER", "ABSTAIN"}
                and status == row["answer_status"]
                and isinstance(text, str)
                and isinstance(citations, list),
                "ANSWER_SHAPE",
            )
            require(
                all(isinstance(c, str) and c in evidence for c in citations)
                and len(set(citations)) == len(citations),
                "CITATION_BINDING",
            )
            require(status == "ABSTAIN" or (text.strip() and citations), "EMPTY_ANSWER")
            opaque = token_hex(16)
            answers.append(
                {
                    "response_key": opaque,
                    "world_id": world,
                    "status": status,
                    "answer": text,
                    "citations": citations,
                    "raw_sha256": digest(raw),
                    "response_id_sha256": digest(result["id"].encode()),
                }
            )
            index.append(
                {
                    "response_key": opaque,
                    "world_id": world,
                    "arm": arm,
                    "status": status,
                }
            )
            context.append(
                {
                    "response_key": opaque,
                    "question": request["question"],
                    "event_date": request["event_date"],
                    "cited_text": {
                        citation: evidence[citation] for citation in citations
                    },
                }
            )
            status_counts[status] += 1
            arm_counts[arm] += 1
    require(
        len({item["response_key"] for item in answers}) == len(ids) == 95,
        "EXPORT_BIJECTION",
    )
    require(arm_counts == {"NONE": 31, "RD_B2": 32, "RD_ZH": 32}, "ARM_DENOMINATOR")
    require(
        status_counts == {"ANSWER": 68, "ABSTAIN": 27}
        and len({key[0] for key in keys}) == 32,
        "STATUS_DENOMINATOR",
    )
    target.mkdir()
    hashes = {
        "answer_export_sha256": write(
            target / "ANSWERS_ROLE_FREE_PRIVATE.json",
            sorted(answers, key=lambda row: row["response_key"]),
        ),
        "mapping_sha256": write(target / "ARM_MAPPING_PRIVATE.json", index),
        "cited_context_sha256": write(
            target / "CITED_CONTEXT_PRIVATE.json",
            sorted(context, key=lambda row: row["response_key"]),
        ),
    }
    return {
        "owner29_grid_sha256": GRID,
        "owner29_seal_sha256": SEAL,
        "owner29_prior_seal_sha256": PRIOR,
        "owner29_archive_sha256": ZIP,
        "responses_verified": len(ids),
        "per_arm": dict(arm_counts),
        "status_counts": dict(status_counts),
        "worlds": 32,
        "grid_cells": 96,
        "complete_triples": 31,
        "extra_b2_zh_pairs": 1,
        "missing": {"arm": "NONE", "count": 1, "status": "UNRECOVERABLE_MISSING"},
        "private_export": "D_DRIVE_GIT_IGNORED",
        "fresh_generation_calls": 0,
        **hashes,
    }


def judge_rule(
    answer: dict[str, Any], ctx: dict[str, Any], ref: dict[str, Any]
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "correct": None,
        "support": "NOT_APPLICABLE",
        "value": None,
        "span": None,
    }
    if answer["status"] == "ABSTAIN":
        return {**result, "outcome": "ABSTAIN"}
    result["support"] = "UNRESOLVED"
    if ref.get("answerable") is not True or ref.get("status") == "REFERENCE_UNRESOLVED":
        return {**result, "outcome": "UNRESOLVED", "reason": "REFERENCE_UNRESOLVED"}
    unit = UNITS.get(normal(str(ref.get("unit", ""))))
    if unit is None or ctx["event_date"] != ref["event_date"]:
        return {**result, "outcome": "UNRESOLVED", "reason": "UNIT_OR_EVENT_BINDING"}
    try:
        expected = scalar(ref["normalized_gold_value"], unit)
        hits = amounts(answer["answer"], unit)
    except ValueError:
        return {**result, "outcome": "UNRESOLVED", "reason": "UNPARSED_SCALAR"}
    values = {item[0] for item in hits}
    if len(values) != 1 or AMBIGUOUS.search(normal(answer["answer"])):
        return {**result, "outcome": "UNRESOLVED", "reason": "AMBIGUOUS_OR_NO_VALUE"}
    value, start, end = hits[0]
    text = answer["answer"]
    if len(normal(text)) != len(text):
        return {**result, "outcome": "UNRESOLVED", "reason": "SPAN_NORMALIZATION_DRIFT"}
    result.update(
        value={"amount": value, "unit": unit}, span={"start": start, "end": end}
    )
    scopes = ref.get("scope_qualifiers", [])
    if isinstance(scopes, str):
        scopes = [scopes] if scopes else []
    if not isinstance(scopes, list) or any(
        not isinstance(scope, str) for scope in scopes
    ):
        return {**result, "outcome": "UNRESOLVED", "reason": "SCOPE_SCHEMA"}
    # A qualifier can be inherited only from the same frozen question, or explicitly stated.
    text_norm = normal(text)
    query_norm = normal(ctx["question"])
    if not all(
        normal(scope) in query_norm or normal(scope) in text_norm for scope in scopes
    ):
        return {
            **result,
            "outcome": "UNRESOLVED",
            "reason": "SCOPE_NOT_EXPLICITLY_BOUND",
        }
    if ISO_DATE.search(text_norm) or CALENDAR.search(text_norm):
        if ctx["event_date"] not in text_norm:
            return {
                **result,
                "outcome": "UNRESOLVED",
                "reason": "ANSWER_CONTAINS_OTHER_DATE",
            }
    # Missing lexical evidence is distinct from an otherwise equivalent answer.
    try:
        evidence_hits = [
            (normal(cited), {x[0] for x in amounts(cited, unit)})
            for cited in ctx["cited_text"].values()
        ]
    except ValueError:
        return {**result, "outcome": "UNRESOLVED", "reason": "CITATION_UNPARSED"}
    if not any(value in found for _, found in evidence_hits):
        result["support"] = "UNSUPPORTED"
    elif any(
        found == {value}
        and not AMBIGUOUS.search(cited)
        and all(normal(scope) in cited for scope in scopes)
        and not ISO_DATE.search(cited)
        and not CALENDAR.search(cited)
        for cited, found in evidence_hits
    ):
        result["support"] = "ATOM_SUPPORTED_IN_KEPT_CITATION"
    correct = value == expected
    if result["support"] == "UNRESOLVED":
        return {
            **result,
            "outcome": "UNRESOLVED",
            "reason": "CITATION_SEMANTICS",
            "value_match": correct,
        }
    outcome = (
        ("UNSUPPORTED_CORRECT" if result["support"] == "UNSUPPORTED" else "CORRECT")
        if correct
        else "OTHER_WRONG"
    )
    return {**result, "correct": correct, "outcome": outcome}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner29", required=True, type=Path)
    parser.add_argument("--private-out", required=True, type=Path)
    parser.add_argument("--rubric", required=True, type=Path)
    args = parser.parse_args()
    require(
        args.owner29.resolve().drive.upper() == "D:"
        and args.private_out.resolve().drive.upper() == "D:",
        "PRIVATE_STORAGE_NOT_D",
    )
    rubric = args.rubric.read_bytes()
    config = json.loads(rubric)
    require(
        config["status"] == "RUBRIC_FROZEN"
        and config["rule_source_sha256"] == digest(Path(__file__).read_bytes()),
        "RUBRIC_SOURCE_BINDING",
    )
    result = export(args.owner29, args.private_out)
    result.update(
        rubric_sha256=digest(rubric), rule_source_sha256=config["rule_source_sha256"]
    )
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
