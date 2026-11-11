"""Prepare the two curator panels using only their frozen role-free input."""

from __future__ import annotations

import argparse
from datetime import date
import re
from pathlib import Path
from typing import Any

import run_chinese5060_owner28 as backend

from llmguard.domains.retrieval.hidden_poisoning.chinese5060 import qag

CURATOR = "11242cc6613a0ec3f53332255d0e19de941273a3"
ROLE_FREE = {
    31: "745682ea9f63a659cd3aa6fd308f80c15d807da63448c00a2b4dda1f52af9bcf",
    33: "fccae2a0967b7bcefe051849c5b8d65d930e8954abe3c4ffb1b4a53daf03cf0c",
}
CURATOR_ROOT = "docs/paper1/dual_machine/repro5090"
OWNER33_DIR = qag.BASE / "W1-5060-OWNER33-VCARE-20261111-01/independent-eval-11242cc"
OWNER33_TOPK = "861cb132b70b133bda4db3e493a11cecf07be4cd75f3cf3ebcce2c70d5174205"
OWNER33_PRED = "7082eba17608c8d8ee6d93a591b4c74fdb017e295558e76f1b1867e712a8ccd8"


def curator_worlds(panel: int) -> list[dict[str, Any]]:
    name = f"{CURATOR_ROOT}/owner{panel}_eval/OWNER{panel}_ROLE_FREE.json"
    pack = qag.checked(backend.git("show", f"{CURATOR}:{name}"), ROLE_FREE[panel])
    rows = pack["worlds"]
    if len(rows) != 32 or len({row["world_id"] for row in rows}) != 32:
        raise ValueError("CURATOR_WORLD_COUNT")
    if any(
        set(row) != {"world_id", "query", "passages"}
        or not re.fullmatch(r"w-[a-f0-9]{20,64}", row["world_id"])
        or not isinstance(row["query"], str)
        or not row["query"]
        or len(row["passages"]) != 11
        or any(
            set(passage) != {"passage_id", "text"}
            or not re.fullmatch(r"p-[a-f0-9]{20,64}", passage["passage_id"])
            or not isinstance(passage["text"], str)
            or not passage["text"]
            for passage in row["passages"]
        )
        for row in rows
    ):
        raise ValueError("CURATOR_ROLE_FREE_SCHEMA")
    if len({p["passage_id"] for row in rows for p in row["passages"]}) != 352:
        raise ValueError("CURATOR_PASSAGE_COUNT")
    return rows


def backend_world(row: dict[str, Any]) -> dict[str, Any]:
    match = re.search(r"\d{4}-\d{2}-\d{2}", row["query"])
    event = date.fromisoformat(match[0]).isoformat() if match else None
    return {
        "world_id": row["world_id"],
        "query_text": row["query"],
        "event_date": event,
        "documents": [
            {
                "document_id": item["passage_id"],
                "source_id": "s-" + item["passage_id"][2:],
                "source_uri": None,
                "text": item["text"],
                "content_sha256": qag.digest(item["text"].encode()),
            }
            for item in row["passages"]
        ],
    }


def prepare(out: Path, args: argparse.Namespace) -> None:
    rows31, rows33 = curator_worlds(31), curator_worlds(33)
    if {row["world_id"] for row in rows31} & {row["world_id"] for row in rows33}:
        raise ValueError("CROSS_PANEL_DUPLICATE")
    seal = qag.checked((OWNER33_DIR / "TOPK_SEAL.json").read_bytes(), OWNER33_TOPK)
    previous = {
        row["world_id"]: row
        for row in qag.checked(
            (OWNER33_DIR / "PREDICTIONS_ROLE_FREE.json").read_bytes(), OWNER33_PRED
        )
    }
    previous_sha = {row["world_id"]: row["packet_sha256"] for row in seal["packets"]}
    out.mkdir()
    backend.configure(out)
    (model, defender, b2, zh), r2 = backend.pinned_backend(args)
    inputs, ranks = [], []
    vectors: dict[str, Any] = {}
    for panel, rows in ((31, rows31), (33, rows33)):
        for row in rows:
            wid = row["world_id"]
            if panel == 31:
                packet = backend.build_topk(backend_world(row), model, out, vectors)
                sha = qag.write_once(out / f"{wid}-TOPK.json", packet)
            else:
                sha = previous_sha[wid]
                packet = qag.checked(
                    (OWNER33_DIR / f"{wid}-TOPK.json").read_bytes(), sha
                )
            if packet["world_id"] != wid or packet["query_text"] != row["query"]:
                raise ValueError("TOPK_QUERY_BINDING")
            top = packet["topk"]
            if len(top) != 5:
                raise ValueError("TOPK_DENOMINATOR")
            passage_texts = {p["passage_id"]: p["text"] for p in row["passages"]}
            texts = [hit["chunk"]["text"] for hit in top]
            if any(hit["chunk"]["parent_doc_id"] not in passage_texts for hit in top):
                raise ValueError("CURATOR_RANK_BINDING")
            embedding = r2.model_vectors(model, texts)
            emb_sha = qag.digest(embedding.cpu().detach().numpy().tobytes())
            masks = []
            for vote in (b2, zh):
                trace = r2.filter_one(defender, vote, texts, texts, embedding, emb_sha)
                masks.append([i for i in range(5) if i not in trace["deleted_indices"]])
            if panel == 33 and masks != [
                previous[wid]["masks"][arm] for arm in ("RD_B2", "RD_ZH")
            ]:
                raise ValueError("OWNER33_FROZEN_BASELINE_MISMATCH")
            inputs.append(
                {
                    "world_id": wid,
                    "packet_sha256": sha,
                    "query": row["query"],
                    "texts": texts,
                    "b2": masks[0],
                    "zh": masks[1],
                }
            )
            ranks.append(
                {
                    "panel": panel,
                    "world_id": wid,
                    "packet_sha256": sha,
                    "passage_ids": [hit["chunk"]["parent_doc_id"] for hit in top],
                    "chunk_sha256": [hit["chunk"]["content_hash"] for hit in top],
                }
            )
    input_sha = qag.write_once(out / "TEST_INPUT.json", inputs)
    rank_sha = qag.write_once(out / "RANK_JOIN.json", ranks)
    receipt = {
        "curator_commit": CURATOR,
        "role_free_sha256": ROLE_FREE,
        "worlds": len(inputs),
        "rank_slots": 5 * len(inputs),
        "test_input_sha256": input_sha,
        "rank_join_sha256": rank_sha,
        "owner33_topk_seal_sha256": OWNER33_TOPK,
        "backend": backend.BASE_IDENTITY,
    }
    qag.write_once(out / "TEST_INPUT_SEAL.json", receipt)
    print(qag.encoded(receipt).decode(), flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    for name in ("out", "assets", "upstream", "support"):
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--freeze", required=True)
    args = parser.parse_args()
    if (
        not args.out.resolve().is_relative_to(qag.BASE.resolve())
        or backend.git("rev-parse", "HEAD").decode().strip() != args.freeze
        or backend.git("status", "--porcelain")
    ):
        raise ValueError("FROZEN_CHECKOUT_REQUIRED")
    prepare(args.out.resolve(), args)


if __name__ == "__main__":
    main()
