"""Build the QAG role-blind input from already public texts."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "docs/paper1/dual_machine/repro5090/qag_eval/QAG_INPUT_ROLE_FREE.json"
PIN = "108b35c9239ad113c50f7d84daf9b84f361b37d6"
PRED = "docs/paper1/dual_machine/chinese5060/owner33_eval/OWNER33_EVAL_PREDICTIONS_ROLE_FREE.json"
BANNED_KEYS = {"role", "gold", "attack", "poison", "scenario", "scope", "clean"}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def check(value: object) -> None:
    if isinstance(value, dict):
        found = BANNED_KEYS.intersection(value)
        if found:
            raise SystemExit("LEAK " + ",".join(sorted(found)))
        for item in value.values():
            check(item)
    elif isinstance(value, list):
        for item in value:
            check(item)


def main() -> None:
    if OUT.exists():
        raise SystemExit("ALREADY_WRITTEN")
    predictions = json.loads(subprocess.check_output(["git", "cat-file", "blob", f"{PIN}:{PRED}"], cwd=REPO))
    role33 = load(REPO / "docs/paper1/dual_machine/repro5090/owner33_eval/OWNER33_ROLE_FREE.json")
    role31 = load(REPO / "docs/paper1/dual_machine/repro5090/owner31_eval/OWNER31_ROLE_FREE.json")
    text33 = {world["world_id"]: {item["passage_id"]: item["text"] for item in world["passages"]} for world in role33["worlds"]}
    query33 = {world["world_id"]: world["query"] for world in role33["worlds"]}
    worlds = []
    for item in predictions:
        world_id = item["world_id"]
        topk = []
        for row in item["ranks"]:
            topk.append({"passage_id": row["passage_id"], "rank": row["rank"], "text": text33[world_id][row["passage_id"]]})
        if [row["rank"] for row in topk] != [1, 2, 3, 4, 5]:
            raise SystemExit("RANK")
        worlds.append(
            {
                "batch": "OWNER33",
                "order_source": "SEALED_MINILM_TOPK",
                "query": query33[world_id],
                "topk": topk,
                "world_id": world_id,
            }
        )
    for world in role31["worlds"]:
        worlds.append(
            {
                "batch": "OWNER31",
                "order_source": "NOT_RETRIEVED",
                "passages": [{"passage_id": item["passage_id"], "text": item["text"]} for item in world["passages"]],
                "query": world["query"],
                "topk": None,
                "world_id": world["world_id"],
            }
        )
    worlds.sort(key=lambda world: (world["batch"], world["world_id"]))
    payload = {
        "human_gold": 0,
        "labels_included": False,
        "owner31_order_source": "NOT_RETRIEVED_ENCODER_ABSENT_ON_5090",
        "owner31_passages_per_world": 11,
        "owner31_worlds": 32,
        "owner33_order_source": "SEALED_MINILM_TOPK",
        "owner33_passages_per_world": 5,
        "owner33_prediction_commit": PIN,
        "owner33_predictions_sha256": "7082eba17608c8d8ee6d93a591b4c74fdb017e295558e76f1b1867e712a8ccd8",
        "owner33_worlds": 32,
        "schema": "QAG_ROLE_FREE_INPUT_V1",
        "worlds": worlds,
    }
    check(payload)
    if sum(world["batch"] == "OWNER33" for world in worlds) != 32:
        raise SystemExit("COUNT33")
    if sum(world["batch"] == "OWNER31" and world["topk"] is None and len(world["passages"]) == 11 for world in worlds) != 32:
        raise SystemExit("COUNT31")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    OUT.write_bytes(raw)
    print(sha(raw))


if __name__ == "__main__":
    main()
