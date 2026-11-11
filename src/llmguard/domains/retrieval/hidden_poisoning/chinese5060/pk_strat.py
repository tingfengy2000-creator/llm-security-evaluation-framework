"""Frozen PK-STRAT prompts, request plans, and isolated prediction receipts."""

from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal
import json
import os
from pathlib import Path
from typing import Any
from zipfile import ZIP_DEFLATED, ZipFile

from . import qag

CLOSED = "请直接回答问题。只输出答案值，不输出解释、推理或引用。"
CONTEXT_ONLY = "只依据所给片段判断，不得使用你自己的知识。"
ARMS = ("NONE", "RD_B2", "QWEN_VERIFY", "QWEN_VERIFY_CONTEXT_ONLY")
LIMIT = Decimal("1")
CLOSED_N = 24
WORLD_N = 56
CALL_N = CLOSED_N + 2 * WORLD_N


def closed_packet(question: str) -> bytes:
    return qag.encoded(
        {
            "model": qag.MODEL,
            "messages": [
                {"role": "system", "content": CLOSED},
                {"role": "user", "content": question},
            ],
            "temperature": 0,
            "enable_thinking": False,
            "stream": False,
            "max_completion_tokens": 64,
        }
    )


def context_packet(numbered: bytes) -> bytes:
    body = json.loads(numbered)
    body["messages"][0]["content"] += "\n" + CONTEXT_ONLY
    return qag.encoded(body)


def validate_inputs(data: Any) -> None:
    if not isinstance(data, dict) or set(data) != {"closed_book", "worlds"}:
        raise ValueError("PK_INPUT_FIELDS")
    closed, worlds = data["closed_book"], data["worlds"]
    if not isinstance(closed, list) or len(closed) != CLOSED_N:
        raise ValueError("PK_CLOSED_COUNT")
    if (
        not all(isinstance(q, str) and q.strip() for q in closed)
        or len(set(closed)) != CLOSED_N
    ):
        raise ValueError("PK_CLOSED_QUERY")
    if not isinstance(worlds, list) or len(worlds) != WORLD_N:
        raise ValueError("PK_WORLD_COUNT")
    ids: set[str] = set()
    for row in worlds:
        if not isinstance(row, dict) or set(row) != {"world_id", "query", "texts"}:
            raise ValueError("PK_WORLD_FIELDS")
        wid, query, texts = row["world_id"], row["query"], row["texts"]
        if not isinstance(wid, str) or not wid or wid in ids or query not in closed:
            raise ValueError("PK_WORLD_ID_OR_QUERY")
        if (
            not isinstance(texts, list)
            or len(texts) != 5
            or not all(
                isinstance(t, str) and 0 < len(t) <= 1000 and t.strip() for t in texts
            )
        ):
            raise ValueError("PK_TEXT_DENOMINATOR")
        ids.add(wid)
    counts = Counter(row["query"] for row in worlds)
    if Counter(counts.values()) != {2: 16, 3: 8}:
        raise ValueError("PK_FACT_WORLD_ALLOCATION")


def make_plan(data: dict[str, Any]) -> list[tuple[str, bytes]]:
    validate_inputs(data)
    plan = [("CLOSED_BOOK", closed_packet(query)) for query in data["closed_book"]]
    for row in data["worlds"]:
        verify = qag.packets(row["query"], row["texts"])[-1]
        plan.extend(((ARMS[2], verify), (ARMS[3], context_packet(verify))))
    if len(plan) != CALL_N or any(
        len(body) + qag.TEMPLATE_RESERVE > qag.MAX_INPUT for _, body in plan
    ):
        raise ValueError("PK_WIRE_DENOMINATOR_OR_INPUT_GATE")
    return plan


def verifier_result(content: str) -> list[int] | None:
    try:
        return qag.verify_mask(content)
    except (ValueError, TypeError):
        return None


def run(prep: Path, out: Path, seal_sha: str, *, check_only: bool) -> None:
    seal = qag.checked((prep / "SEAL.json").read_bytes(), seal_sha)
    if seal["runner_sha256"] != qag.digest(Path(__file__).read_bytes()):
        raise ValueError("PK_RUNNER_DRIFT")
    if seal["transport_sha256"] != qag.digest(Path(qag.__file__).read_bytes()):
        raise ValueError("PK_TRANSPORT_DRIFT")
    data = qag.checked((prep / "INPUT.json").read_bytes(), seal["input_sha256"])
    masks = qag.checked((prep / "RD_B2.json").read_bytes(), seal["rd_b2_sha256"])
    plan = make_plan(data)
    if list(masks) != [row["world_id"] for row in data["worlds"]] or any(
        mask != sorted(set(mask)) or not set(mask) <= set(range(5))
        for mask in masks.values()
    ):
        raise ValueError("PK_RD_B2_BINDING")
    wire = qag.digest(qag.encoded([[arm, qag.digest(body)] for arm, body in plan]))
    if wire != seal["wire_sha256"]:
        raise ValueError("PK_WIRE_DRIFT")
    reserve = CALL_N * qag.cost(qag.MAX_INPUT, qag.OUTPUT_RESERVE, high=True)
    if reserve > LIMIT:
        raise ValueError("PK_BUDGET_GATE")
    print(
        qag.encoded(
            {
                "requests": len(plan),
                "max_wire_bytes": max(len(body) for _, body in plan),
                "reserve_usd": str(reserve),
            }
        ).decode(),
        flush=True,
    )
    if check_only:
        return
    key = os.environ.get("DASHSCOPE_API_KEY")
    if not key:
        raise ValueError("DASHSCOPE_API_KEY_MISSING")
    out.mkdir()
    qag.write_once(out / "ATTEMPT.json", {"prep_sha256": seal_sha, "wire_sha256": wire})
    results = []
    stats: dict[str, Counter[str]] = {
        arm: Counter() for arm in ("CLOSED_BOOK", *ARMS[2:])
    }
    latency: dict[str, list[float]] = {arm: [] for arm in stats}
    seen_ids: set[str] = set()
    spent = Decimal(0)
    with ThreadPoolExecutor(max_workers=4) as pool:
        for start in range(0, len(plan), 4):
            batch = plan[start : start + 4]
            if (
                spent
                + len(batch) * qag.cost(qag.MAX_INPUT, qag.OUTPUT_RESERVE, high=True)
                > LIMIT
            ):
                raise ValueError("PK_BUDGET_STOP")
            paths = [
                out / f"reply-{index:03}.json"
                for index in range(start, start + len(batch))
            ]
            futures = [
                pool.submit(qag.call, key, body, path)
                for (_, body), path in zip(batch, paths, strict=True)
            ]
            for (arm, _), path, future in zip(batch, paths, futures, strict=True):
                content, n_in, n_out, sec = future.result()
                receipt = json.loads(path.read_bytes())
                rid = receipt["provider"]["id"]
                if rid in seen_ids:
                    raise ValueError("PK_DUPLICATE_REQUEST_ID")
                seen_ids.add(rid)
                results.append(content)
                stats[arm].update(calls=1, input_tokens=n_in, output_tokens=n_out)
                latency[arm].append(sec)
                spent += qag.cost(n_in, n_out)
    closed_answers = [
        {"question_index": index, "question": question, "raw_answer": raw}
        for index, (question, raw) in enumerate(
            zip(data["closed_book"], results[:CLOSED_N], strict=True), 1
        )
    ]
    worlds = []
    for index, row in enumerate(data["worlds"]):
        world_id = row["world_id"]
        left = CLOSED_N + 2 * index
        worlds.append(
            {
                "world_id": world_id,
                "masks": dict(
                    zip(
                        ARMS,
                        [
                            list(range(5)),
                            masks[world_id],
                            verifier_result(results[left]),
                            verifier_result(results[left + 1]),
                        ],
                        strict=True,
                    )
                ),
            }
        )
    answers_sha = qag.write_once(out / "CLOSED_BOOK_ANSWERS.json", closed_answers)
    predictions_sha = qag.write_once(out / "PREDICTIONS.json", worlds)
    summary = {
        "worlds": len(worlds),
        "closed_book": len(closed_answers),
        "closed_answers_sha256": answers_sha,
        "predictions_sha256": predictions_sha,
        "wire_sha256": wire,
        "usd_estimated": str(spent),
        "max_input_tokens": max(
            json.loads(p.read_bytes())["provider"]["usage"]["prompt_tokens"]
            for p in out.glob("reply-*.json")
        ),
        "valid_worlds": {
            arm: sum(row["masks"][arm] is not None for row in worlds) for arm in ARMS
        },
        "stats": {
            arm: dict(values)
            | {
                "usd": str(qag.cost(values["input_tokens"], values["output_tokens"])),
                "p95_seconds": sorted(latency[arm])[
                    (95 * len(latency[arm]) + 99) // 100 - 1
                ],
            }
            for arm, values in stats.items()
        },
        "verifier_mask_changes": sum(
            row["masks"][ARMS[2]] is not None
            and row["masks"][ARMS[3]] is not None
            and row["masks"][ARMS[2]] != row["masks"][ARMS[3]]
            for row in worlds
        ),
    }
    qag.write_once(out / "SUMMARY.json", summary)
    with ZipFile(
        out / "PK_5090_HANDOFF_PRIVATE.zip", "x", compression=ZIP_DEFLATED
    ) as archive:
        for name in ("CLOSED_BOOK_ANSWERS.json", "PREDICTIONS.json", "SUMMARY.json"):
            archive.write(out / name, name)
        archive.write(prep / "SEAL.json", "INPUT_SEAL.json")
        archive.writestr(
            "README.txt",
            "Masks contain zero-based positions in the original curator fragment order. "
            "Empty means all deleted. Null means no valid verifier mask. "
            "Closed-book answers are the unmodified Qwen text, indexed in curator order. "
            "Use the 5090 private label custody for independent scoring and density strata. "
            "No evaluator data was read on 5060.",
        )
    with ZipFile(out / "PK_5090_HANDOFF_PRIVATE.zip") as archive:
        if (
            archive.testzip() is not None
            or qag.digest(archive.read("PREDICTIONS.json")) != predictions_sha
        ):
            raise ValueError("PK_ARCHIVE_READBACK")
    print(qag.encoded(summary).decode(), flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prep", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--seal-sha256", required=True)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    if not all(
        path.resolve().is_relative_to(qag.BASE.resolve())
        for path in (args.prep, args.out)
    ):
        raise ValueError("PK_PRIVATE_PATH")
    run(
        args.prep.resolve(),
        args.out.resolve(),
        args.seal_sha256,
        check_only=args.check_only,
    )


if __name__ == "__main__":
    main()
