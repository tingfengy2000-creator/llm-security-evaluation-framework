"""Run the sealed PK-CONFIRM request plan once and preserve scoring inputs."""

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

from . import pk_strat, qag

CURATOR = "092efe9e8626d68a7172b0b3ade6b9f888cbf398"
REVIEWER = "87864727a5130ec14822852671aebdbc25af429d"
INPUT_SHA = {
    "PKC_INPUT_ROLE_FREE.json": "1f204b647fff82d25990146f941d07ea47692487fd65297ea7ea36c19bcc9ce4",
    "PKC_INPUT_QUESTIONS.json": "d93ad1984fe36db46667cf9c62ca5593c4fb166088af9ec5b03d037c01db2795",
    "PKC_INPUT_MANIFEST.json": "8ea6753d7a408266e3208119b7fced2c8d11d4360bff8db4d20b08bd45e0630a",
}
QUESTIONS, REPEATS, WORLDS = 36, 2, 80
CLOSED = QUESTIONS * REPEATS
CALLS = CLOSED + WORLDS
ARMS = ("NONE", "RD_B2", "QWEN_VERIFY")
LIMIT = Decimal("1")


def validated_inputs(blobs: dict[str, bytes]) -> dict[str, Any]:
    if blobs.keys() != INPUT_SHA.keys():
        raise ValueError("PKC_BLOB_SET")
    data, closed, manifest = (
        qag.checked(blobs[name], expected) for name, expected in INPUT_SHA.items()
    )
    for key, expected_value in {
        "schema": "PKC_INPUT_MANIFEST_V1",
        "status": "INPUT_SEALED",
        "scoring": "NOT_RECEIVED",
        "reviewer_commit": REVIEWER,
        "labels_included": False,
        "human_gold": 0,
        "questions": QUESTIONS,
        "closed_book_repeats": REPEATS,
        "worlds": WORLDS,
        "passages_per_world": 5,
        "questions_sha256": INPUT_SHA["PKC_INPUT_QUESTIONS.json"],
        "worlds_sha256": INPUT_SHA["PKC_INPUT_ROLE_FREE.json"],
    }.items():
        if manifest.get(key) != expected_value:
            raise ValueError(f"PKC_MANIFEST:{key}")
    if (
        set(data) != {"schema", "labels_included", "human_gold", "worlds"}
        or data["schema"] != "PKC_ROLE_FREE_V1"
        or set(closed)
        != {"schema", "labels_included", "human_gold", "questions", "repeats"}
        or closed["schema"] != "PKC_CLOSED_BOOK_V1"
        or closed["repeats"] != REPEATS
        or any(
            x["labels_included"] is not False or x["human_gold"] != 0
            for x in (data, closed)
        )
    ):
        raise ValueError("PKC_PUBLIC_SCHEMA")
    questions, worlds = closed["questions"], data["worlds"]
    if len(questions) != QUESTIONS or len(worlds) != WORLDS:
        raise ValueError("PKC_DENOMINATOR")
    question_ids, queries = set(), set()
    for q in questions:
        if (
            set(q) != {"question_id", "text"}
            or not all(isinstance(x, str) and x.strip() for x in q.values())
            or q["question_id"] in question_ids
            or q["text"] in queries
        ):
            raise ValueError("PKC_QUESTION_SHAPE")
        question_ids.add(q["question_id"])
        queries.add(q["text"])
    world_ids, passage_ids = set(), set()
    allocation: Counter[str] = Counter()
    for row in worlds:
        if (
            set(row) != {"world_id", "query", "passages"}
            or not isinstance(row["world_id"], str)
            or not row["world_id"]
            or row["world_id"] in world_ids
            or row["query"] not in queries
            or len(row["passages"]) != 5
        ):
            raise ValueError("PKC_WORLD_SHAPE")
        world_ids.add(row["world_id"])
        allocation[row["query"]] += 1
        for passage in row["passages"]:
            if (
                set(passage) != {"passage_id", "text"}
                or not isinstance(passage["passage_id"], str)
                or not passage["passage_id"]
                or passage["passage_id"] in passage_ids
                or not isinstance(passage["text"], str)
                or not passage["text"].strip()
                or len(passage["text"]) > 1000
            ):
                raise ValueError("PKC_PASSAGE_SHAPE")
            passage_ids.add(passage["passage_id"])
    if Counter(allocation.values()) != {2: 28, 3: 8}:
        raise ValueError("PKC_FACT_ALLOCATION")
    return {"questions": questions, "worlds": worlds}


def request_plan(data: dict[str, Any]) -> list[tuple[str, bytes]]:
    plan = [
        ("CLOSED_BOOK", pk_strat.closed_packet(question["text"]))
        for _ in range(REPEATS)
        for question in data["questions"]
    ] + [
        (
            "QWEN_VERIFY",
            qag.packets(row["query"], [p["text"] for p in row["passages"]])[-1],
        )
        for row in data["worlds"]
    ]
    if len(plan) != CALLS or any(
        len(b) + qag.TEMPLATE_RESERVE > qag.MAX_INPUT for _, b in plan
    ):
        raise ValueError("PKC_WIRE_GATE")
    return plan


def plan_hash(plan: list[tuple[str, bytes]]) -> str:
    return qag.digest(qag.encoded([[arm, qag.digest(body)] for arm, body in plan]))


def code_hashes() -> dict[str, str]:
    return {
        "pk_confirm": qag.digest(Path(__file__).read_bytes()),
        "pk_strat": qag.digest(Path(pk_strat.__file__).read_bytes()),
        "qag": qag.digest(Path(qag.__file__).read_bytes()),
    }


def run(prep: Path, out: Path, seal_sha: str, *, check_only: bool) -> None:
    seal = qag.checked((prep / "SEAL.json").read_bytes(), seal_sha)
    data = qag.checked((prep / "INPUT.json").read_bytes(), seal["input_sha256"])
    rd = qag.checked((prep / "RD_B2.json").read_bytes(), seal["rd_b2_sha256"])
    plan = request_plan(data)
    if (
        seal["code_sha256"] != code_hashes()
        or seal["wire_sha256"] != plan_hash(plan)
        or list(rd) != [row["world_id"] for row in data["worlds"]]
        or any(
            mask != sorted(set(mask)) or not set(mask) <= set(range(5))
            for mask in rd.values()
        )
    ):
        raise ValueError("PKC_FREEZE_DRIFT")
    per_request = qag.cost(qag.MAX_INPUT, qag.OUTPUT_RESERVE, high=True)
    reserve = CALLS * per_request
    if reserve > LIMIT:
        raise ValueError("PKC_BUDGET_GATE")
    print(
        qag.encoded(
            {
                "requests": CALLS,
                "max_wire_bytes": max(len(b) for _, b in plan),
                "reserved_usd": str(reserve),
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
    qag.write_once(
        out / "ATTEMPT.json", {"seal_sha256": seal_sha, "wire_sha256": plan_hash(plan)}
    )
    responses: list[str] = []
    stats: dict[str, Counter[str]] = {
        arm: Counter() for arm in ("CLOSED_BOOK", "QWEN_VERIFY")
    }
    seen: set[str] = set()
    spent = Decimal(0)
    max_input, max_output = 0, 0
    with ThreadPoolExecutor(max_workers=4) as pool:
        for start in range(0, len(plan), 4):
            batch = plan[start : start + 4]
            if spent + len(batch) * per_request > LIMIT:
                raise ValueError("PKC_BUDGET_STOP")
            paths = [
                out / f"reply-{i:03}.json" for i in range(start, start + len(batch))
            ]
            futures = [
                pool.submit(qag.call, key, body, path)
                for (_, body), path in zip(batch, paths, strict=True)
            ]
            for (arm, _), path, future in zip(batch, paths, futures, strict=True):
                content, n_in, n_out, _ = future.result()
                receipt = json.loads(path.read_bytes())
                rid = receipt["provider"]["id"]
                if rid in seen:
                    raise ValueError("PKC_DUPLICATE_REQUEST_ID")
                seen.add(rid)
                responses.append(content)
                stats[arm].update(calls=1, input_tokens=n_in, output_tokens=n_out)
                max_input, max_output = max(max_input, n_in), max(max_output, n_out)
                spent += qag.cost(n_in, n_out)
    answers = [
        {
            "question_id": q["question_id"],
            "repeat": repeat,
            "raw_answer": responses[(repeat - 1) * QUESTIONS + i],
        }
        for repeat in range(1, REPEATS + 1)
        for i, q in enumerate(data["questions"])
    ]
    predictions = [
        {
            "world_id": row["world_id"],
            "masks": {
                "NONE": list(range(5)),
                "RD_B2": rd[row["world_id"]],
                "QWEN_VERIFY": pk_strat.verifier_result(responses[CLOSED + i]),
            },
        }
        for i, row in enumerate(data["worlds"])
    ]
    answer_sha = qag.write_once(out / "CLOSED_BOOK_ANSWERS.json", answers)
    prediction_sha = qag.write_once(out / "PREDICTIONS.json", predictions)
    summary = {
        "closed_answers_sha256": answer_sha,
        "predictions_sha256": prediction_sha,
        "wire_sha256": seal["wire_sha256"],
        "usd_estimated": str(spent),
        "max_input_tokens": max_input,
        "max_output_tokens": max_output,
        "closed_answers": len(answers),
        "worlds": len(predictions),
        "repeat_text_exact_matches": sum(
            responses[i] == responses[QUESTIONS + i] for i in range(QUESTIONS)
        ),
        "valid_worlds": {
            a: sum(row["masks"][a] is not None for row in predictions) for a in ARMS
        },
        "stats": {
            a: dict(s) | {"usd": str(qag.cost(s["input_tokens"], s["output_tokens"]))}
            for a, s in stats.items()
        },
    }
    qag.write_once(out / "SUMMARY.json", summary)
    archive_path = out / "PKC_5090_HANDOFF_PRIVATE.zip"
    with ZipFile(archive_path, "x", compression=ZIP_DEFLATED) as archive:
        for name in ("CLOSED_BOOK_ANSWERS.json", "PREDICTIONS.json", "SUMMARY.json"):
            archive.write(out / name, name)
        archive.write(prep / "SEAL.json", "INPUT_SEAL.json")
        archive.writestr(
            "README.txt",
            "Closed-book answers are unmodified provider text. Join by question_id and repeat (1 or 2). "
            "Masks contain zero-based positions in the original curator fragment order. "
            "Empty means all removed; null means invalid verifier output. "
            "Score privately on 5090 using the presealed labels and the registered strata. "
            "No labels were accessed on 5060.",
        )
    with ZipFile(archive_path) as archive:
        if archive.testzip() or any(
            qag.digest(archive.read(name)) != expected
            for name, expected in (
                ("CLOSED_BOOK_ANSWERS.json", answer_sha),
                ("PREDICTIONS.json", prediction_sha),
            )
        ):
            raise ValueError("PKC_ARCHIVE_READBACK")
    print(
        qag.encoded(
            summary | {"handoff_sha256": qag.digest(archive_path.read_bytes())}
        ).decode(),
        flush=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prep", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--seal-sha256", required=True)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    if not all(
        p.resolve().is_relative_to(qag.BASE.resolve()) for p in (args.prep, args.out)
    ):
        raise ValueError("PKC_PRIVATE_PATH")
    run(
        args.prep.resolve(),
        args.out.resolve(),
        args.seal_sha256,
        check_only=args.check_only,
    )


if __name__ == "__main__":
    main()
