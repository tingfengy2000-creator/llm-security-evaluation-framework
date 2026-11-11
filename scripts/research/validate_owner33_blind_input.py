"""Check the Owner33 public blind input. Does not read private labels."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PUB = REPO / "docs/paper1/dual_machine/repro5090/owner33_eval"
ROLE_FREE = PUB / "OWNER33_ROLE_FREE.json"
MANIFEST = PUB / "OWNER33_PRESEAL_MANIFEST.json"
SNAPSHOT = PUB / "OWNER33_SOURCE_SNAPSHOT.json"
BANNED_FIELDS = ("poison", "gold", "attack", "clean", "role", "scenario")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def banned_field(blob: str) -> str | None:
    for key in BANNED_FIELDS:
        if re.search(rf'"{key}"\s*:', blob):
            return key
    return None


def main() -> None:
    raw = ROLE_FREE.read_bytes()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    snapshot = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    payload = json.loads(raw)
    if sha(raw) != manifest["role_free_sha256"]:
        raise SystemExit("ROLE_FREE_SHA")
    if sha(SNAPSHOT.read_bytes()) != manifest["source_snapshot_sha256"]:
        raise SystemExit("SNAPSHOT_SHA")
    if payload["schema"] != "OWNER33_EVAL_ROLE_FREE_V1":
        raise SystemExit("SCHEMA")
    if payload["text_status"] != "SELF_AUTHORED_SOURCE_GROUNDED_PARAPHRASE":
        raise SystemExit("STATUS")
    if snapshot["frozen_before_fact_selection"] is not True:
        raise SystemExit("SNAPSHOT_ORDER")
    if any("world_id" in record for record in snapshot["records"]):
        raise SystemExit("SNAPSHOT_WORLD")
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
    found = banned_field(raw.decode("utf-8"))
    if found:
        raise SystemExit(f"BANNED_FIELD {found}")
    if manifest["human_gold"] != 0 or manifest["scoring"] != "NOT_RUN":
        raise SystemExit("NOT_SCORED")
    if manifest["blind_score_completed"] is not False:
        raise SystemExit("SCORED")
    if manifest["method_sealed_seen"] is not True or manifest["prediction_authorized"] is not True:
        raise SystemExit("HANDOFF")
    if manifest["frozen_before_method"] is not True:
        raise SystemExit("HANDOFF")
    if manifest["fresh_eval_prediction"] != "NOT_RECEIVED":
        raise SystemExit("PREDICTION")
    print("OWNER33_BLIND_OK")
    print(manifest["source_snapshot_sha256"])
    print(manifest["role_free_sha256"])
    print(manifest["private_label_sha256"])
    print(manifest["worlds"])


if __name__ == "__main__":
    main()
