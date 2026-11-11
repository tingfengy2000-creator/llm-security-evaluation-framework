"""Prepare PK-STRAT offline with the historical RAGDefender B2 implementation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
from typing import Any

import run_chinese5060_owner28 as backend

from llmguard.domains.retrieval.hidden_poisoning.chinese5060 import pk_strat, qag

PUBLIC_ROOT = "docs/paper1/dual_machine/repro5090/pk_strat/"
PUBLIC_NAMES = {
    "PK_INPUT_ROLE_FREE.json",
    "PK_ROLE_FREE.json",
    "PK_CLOSED_BOOK_QUESTIONS.json",
}


def public_blob(commit: str, filename: str) -> bytes:
    if filename not in PUBLIC_NAMES or not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("PK_CURATOR_PUBLIC_PATH")
    backend.git("merge-base", "--is-ancestor", commit, backend.CURATOR_BRANCH)
    return backend.git("show", f"{commit}:{PUBLIC_ROOT}{filename}")


def normalize(raw: bytes, closed_raw: bytes | None) -> dict[str, Any]:
    data = json.loads(raw)
    if (
        not isinstance(data, dict)
        or not set(data)
        <= {
            "schema",
            "worlds",
            "closed_book",
            "closed_book_questions",
            "labels_included",
            "human_gold",
            "world_count",
            "closed_book_count",
        }
        or data.get("labels_included", False) is not False
    ):
        raise ValueError("PK_CURATOR_INPUT_SCHEMA")
    closed = data.get("closed_book", data.get("closed_book_questions"))
    if closed_raw is not None:
        if closed is not None:
            raise ValueError("PK_CLOSED_DUPLICATE_INPUT")
        closed = json.loads(closed_raw)
    worlds = []
    for row in data["worlds"]:
        keys = set(row)
        text_key = next(
            (
                key
                for key in ("texts", "passages", "fragments", "documents")
                if key in keys
            ),
            "",
        )
        if keys != {"world_id", "query", text_key}:
            raise ValueError("PK_CURATOR_WORLD_SCHEMA")
        worlds.append(
            {"world_id": row["world_id"], "query": row["query"], "texts": row[text_key]}
        )
    result = {"closed_book": closed, "worlds": worlds}
    pk_strat.validate_inputs(result)
    return result


def prepare(args: argparse.Namespace) -> dict[str, Any]:
    out = args.out.resolve()
    if (
        not out.is_relative_to(qag.BASE.resolve())
        or backend.git("rev-parse", "HEAD").decode().strip() != args.freeze
        or backend.git("status", "--porcelain")
    ):
        raise ValueError("PK_FROZEN_CHECKOUT")
    raw = public_blob(args.curator, args.filename)
    closed_raw = (
        public_blob(args.curator, args.closed_filename)
        if args.closed_filename
        else None
    )
    data = normalize(raw, closed_raw)
    plan = pk_strat.make_plan(data)
    out.mkdir()
    backend.configure(out)
    (model, defender, baseline, _), r2 = backend.pinned_backend(args)
    masks: dict[str, list[int]] = {}
    for row in data["worlds"]:
        texts = row["texts"]
        embedding = r2.model_vectors(model, texts)
        emb_sha = qag.digest(embedding.cpu().detach().numpy().tobytes())
        trace = r2.filter_one(defender, baseline, texts, texts, embedding, emb_sha)
        masks[row["world_id"]] = [
            i for i in range(5) if i not in trace["deleted_indices"]
        ]
    receipt = {
        "curator_commit": args.curator,
        "curator_input_sha256": qag.digest(raw),
        "curator_closed_sha256": qag.digest(closed_raw)
        if closed_raw is not None
        else None,
        "freeze_commit": args.freeze,
        "runner_sha256": qag.digest(Path(pk_strat.__file__).read_bytes()),
        "transport_sha256": qag.digest(Path(qag.__file__).read_bytes()),
        "input_sha256": qag.write_once(out / "INPUT.json", data),
        "rd_b2_sha256": qag.write_once(out / "RD_B2.json", masks),
        "wire_sha256": qag.digest(
            qag.encoded([[arm, qag.digest(body)] for arm, body in plan])
        ),
        "rd_b2_backend": backend.BASE_IDENTITY,
    }
    return receipt | {"seal_sha256": qag.write_once(out / "SEAL.json", receipt)}


def main() -> None:
    parser = argparse.ArgumentParser()
    for name in ("out", "assets", "upstream", "support"):
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--freeze", required=True)
    parser.add_argument("--curator", required=True)
    parser.add_argument("--filename", required=True)
    parser.add_argument("--closed-filename")
    args = parser.parse_args()
    print(qag.encoded(prepare(args)).decode(), flush=True)


if __name__ == "__main__":
    main()
