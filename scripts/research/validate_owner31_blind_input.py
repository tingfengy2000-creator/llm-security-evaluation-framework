"""Check the Owner31 public blind input. Does not read private labels."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PUB = REPO / "docs/paper1/dual_machine/repro5090/owner31_eval"
ROLE_FREE = PUB / "OWNER31_ROLE_FREE.json"
MANIFEST = PUB / "OWNER31_BLIND_SEAL_MANIFEST.json"
BANNED_FIELDS = ("poison", "gold", "attack", "clean", "role", "scenario")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    raw = ROLE_FREE.read_bytes()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    payload = json.loads(raw)
    if sha(raw) != manifest["role_free_sha256"]:
        raise SystemExit("ROLE_FREE_SHA")
    if payload["schema"] != "OWNER31_EVAL_ROLE_FREE_V1":
        raise SystemExit("SCHEMA")
    if payload["text_status"] != "SELF_AUTHORED_FICTIONAL_PROVISIONAL":
        raise SystemExit("STATUS")
    worlds = payload["worlds"]
    if len(worlds) != 32 or manifest["worlds"] != 32:
        raise SystemExit("WORLD_COUNT")
    ids = [world["world_id"] for world in worlds]
    if ids != sorted(ids) or len(set(ids)) != 32:
        raise SystemExit("WORLD_ORDER")
    passage_ids: list[str] = []
    texts: list[str] = []
    for world in worlds:
        if set(world) != {"world_id", "query", "passages"}:
            raise SystemExit("WORLD_FIELDS")
        if not world["query"] or len(world["passages"]) != 11:
            raise SystemExit("PASSAGES")
        local = [item["passage_id"] for item in world["passages"]]
        if local != sorted(local) or len(set(local)) != 11:
            raise SystemExit("PASSAGE_ORDER")
        for item in world["passages"]:
            if set(item) != {"passage_id", "text"} or not item["text"]:
                raise SystemExit("PASSAGE_FIELDS")
            passage_ids.append(item["passage_id"])
            texts.append(item["text"])
    if len(set(passage_ids)) != 352 or len(set(texts)) != 352:
        raise SystemExit("UNIQUENESS")
    blob = raw.decode("utf-8")
    for key in BANNED_FIELDS:
        if re.search(rf'"{key}"\s*:', blob):
            raise SystemExit("BANNED_FIELD")
    if manifest["human_gold"] != 0 or manifest["scoring"] != "NOT_RUN":
        raise SystemExit("NOT_SCORED")
    if manifest["prediction_authorized"] is not False or manifest["frozen_before_method"] is not True:
        raise SystemExit("HANDOFF")
    print("OWNER31_BLIND_OK")
    print(manifest["role_free_sha256"])
    print(manifest["private_label_sha256"])
    print(manifest["worlds"])


if __name__ == "__main__":
    main()
