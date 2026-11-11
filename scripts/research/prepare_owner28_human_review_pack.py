"""Export the Owner28 double-review pack once. Does not score or sign Gold."""

from __future__ import annotations

import hashlib
import json
import random
import secrets
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PUB = REPO / "docs/paper1/dual_machine/repro5090/owner28_eval"
REVIEW_DIR = PUB / "human_review"
PRIV_SRC = Path(r"D:\paper1\private_5090\owner28_eval")
PRIV = PRIV_SRC / "human_review"
PRED_COMMIT = "ad413ea639c950faea2106a52fa4352735384ef1"
PRED_PATH = "docs/paper1/dual_machine/chinese5060/owner28_eval/EVAL_PREDICTIONS_5060_ROLE_FREE.json"
PROJECTION_SHA = "5c9874bd6bb3252a2685e8481b92ea979dc1e842b5f3250a798e2bb7f03d21bb"
ROLE_FREE_SHA = "059a859c8e1296d6a09d1cf7aa4e6124275c8a85af96d85b20749108e6ba56c8"
CURATOR_SHA = "2d5e11e6a2a98e5f1ebd3d2aa16b3b80b6d92f4e6f223f6616df05219fdbe235"
MAP_SHA = "119e7f5242c86a3fd74d10df9ad3d402a41b5cfe4037a1f6a6f4f46f3fe5c0a0"
BRIEF_SHA = "78b888fbcc5192327e357efcc079d4fcee228acf3ff21b3689eb24ee6a6e753e"
CUSTODY_SHA = "c4244e86fb2ecf1177cc3d2bb39b8791e1b789713fc3522bbfaa46b35b055595"
INSTRUMENTS = {
    "POPULATION_FAMILY_PLANNING_LAW": "人口与计划生育法",
    "STATE_COUNCIL_WORK_TIME": "国务院关于职工工作时间的规定",
    "PATENT_LAW": "专利法",
}
CITATION_NOTE = "本段是自写释义，尚未逐句核对到官方原句，标记为 SOURCE_UNVERIFIED。请对照本题列出的公开出处独立判断。"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def dumps(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def require(condition: bool, code: str) -> None:
    if not condition:
        raise SystemExit(code)


def git_bytes(commit: str, path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=REPO)


def review_id(seed: str, kind: str, prefix: str, *parts: str) -> str:
    digest = sha(f"OWNER28_HUMAN_REVIEW_V1|{seed}|{kind}|{'|'.join(parts)}".encode("utf-8"))[:24]
    return f"{prefix}-{digest}"


def content_digest(packet: dict) -> str:
    body = {"schema_version": packet["schema_version"], "human_gold": packet["human_gold"], "questions": packet["questions"]}
    return sha((json.dumps(body, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8"))


def metadata_leak_scan(packets: list[dict], custody: dict) -> None:
    tokens = [custody["salt_hex"]]
    for fact in custody["facts"]:
        tokens.extend(fact[field] for field in ("old_value", "new_value", "selection_preimage", "fact_key"))
        tokens.append(fact["fact_key"])
    for world in custody["worlds"]:
        tokens.append(world["gold_answer"])
    blobs = []
    for packet in packets:
        for question in packet["questions"]:
            scope = question["asked_scope"]
            blobs.extend((scope["object"], scope["condition"], scope["predicate"], question["instrument"], question["query_text"], CITATION_NOTE))
            for version in question["official_versions"]:
                blobs.append(version["locator"])
    text = "\n".join(blobs)
    for token in tokens:
        if isinstance(token, str) and token and token in text:
            raise SystemExit("REVIEW_CONTEXT_LEAK")


def load_inputs() -> tuple[dict, dict, dict, dict, dict]:
    projection = git_bytes(PRED_COMMIT, PRED_PATH)
    require(sha(projection) == PROJECTION_SHA, "PROJECTION_SHA")
    prediction = json.loads(projection)
    for world in prediction["worlds"]:
        world.pop("keep_ranks", None)
    compat_bytes = (PUB / "EVAL_ROLE_FREE_5060_COMPAT.json").read_bytes()
    curator_bytes = (PUB / "EVAL_CURATOR_5060_COMPAT.json").read_bytes()
    map_bytes = (PRIV_SRC / "EVAL_COMPAT_ID_MAP.json").read_bytes()
    brief_bytes = (PRIV_SRC / "query_briefs.json").read_bytes()
    custody_bytes = (PRIV_SRC / "EVAL_LABEL_CUSTODY.json").read_bytes()
    require(sha(compat_bytes) == ROLE_FREE_SHA, "ROLE_FREE_SHA")
    require(sha(curator_bytes) == CURATOR_SHA, "CURATOR_SHA")
    require(sha(map_bytes) == MAP_SHA, "MAP_SHA")
    require(sha(brief_bytes) == BRIEF_SHA, "BRIEF_SHA")
    require(sha(custody_bytes) == CUSTODY_SHA, "CUSTODY_SHA")
    return prediction, json.loads(compat_bytes), json.loads(curator_bytes), json.loads(map_bytes), json.loads(custody_bytes)


def build(seed: str, prediction: dict, compat: dict, curator: dict, id_map: dict) -> tuple[dict, dict, dict]:
    audits = {item["fact_uid"]: item for item in curator["source_audits"]}
    compat_worlds = {item["world_id"]: item for item in compat["main"]}
    mapped = {item["new_world_id"]: item for item in id_map["worlds"]}
    briefs = {item["brief_id"]: item for item in json.loads((PRIV_SRC / "query_briefs.json").read_bytes())["briefs"]}
    questions = []
    private_questions = []
    for predicted in prediction["worlds"]:
        world_id = predicted["world_id"]
        public = compat_worlds[world_id]
        private = mapped[world_id]
        brief = briefs[private["brief_id"]]
        audit = audits[public["fact_uid"]]
        require(audit["lineage_id"] in INSTRUMENTS, "LINEAGE")
        documents = {item["document_id"]: item["text"] for item in public["documents"]}
        passage_ids = {item["document_id"]: item["old_passage_id"] for item in private["documents"]}
        passages = []
        private_items = []
        for hit in predicted["topk"]:
            document_id = hit["document_id"]
            item_id = review_id(seed, "item", "r", world_id, document_id)
            passages.append({
                "item_id": item_id,
                "text": documents[document_id],
                "citation_status": "SOURCE_UNVERIFIED",
                "citation_note": CITATION_NOTE,
            })
            private_items.append({
                "item_id": item_id,
                "document_id": document_id,
                "old_passage_id": passage_ids[document_id],
                "retrieved_rank": hit["rank"],
            })
        question_id = review_id(seed, "question", "q", world_id)
        questions.append({
            "question_id": question_id,
            "instrument": INSTRUMENTS[audit["lineage_id"]],
            "query_text": public["query_text"],
            "asked_scope": {
                "object": brief["object"],
                "time_point": brief["time_point"],
                "condition": brief["condition"],
                "predicate": brief["predicate"],
            },
            "official_versions": [
                {
                    "label": "较早文本",
                    "locator": audit["old_locator"],
                    "uri": audit["old_uri"],
                    "effective_from": audit["old_effective_from"],
                    "effective_until": audit["old_effective_until"],
                },
                {
                    "label": "较晚文本",
                    "locator": audit["new_locator"],
                    "uri": audit["new_uri"],
                    "effective_from": audit["new_effective_from"],
                },
            ],
            "passages": passages,
        })
        private_questions.append({
            "question_id": question_id,
            "new_world_id": world_id,
            "old_world_id": private["old_world_id"],
            "fact_uid": public["fact_uid"],
            "brief_id": private["brief_id"],
            "items": private_items,
        })
    require(len(questions) == 32, "QUESTION_COUNT")
    require(sum(len(item["passages"]) for item in questions) == 160, "PASSAGE_COUNT")
    rng = random.Random(seed)
    order = list(range(len(questions)))
    rng.shuffle(order)
    shuffled_questions = []
    shuffled_private = []
    for position, index in enumerate(order, start=1):
        question = questions[index]
        private_question = private_questions[index]
        passage_order = list(range(len(question["passages"])))
        rng.shuffle(passage_order)
        question["passages"] = [question["passages"][item] for item in passage_order]
        private_question["items"] = [private_question["items"][item] for item in passage_order]
        question["display_index"] = position
        private_question["display_index"] = position
        for passage_position, passage in enumerate(question["passages"], start=1):
            passage["display_index"] = passage_position
        for passage_position, item in enumerate(private_question["items"], start=1):
            item["display_index"] = passage_position
        shuffled_questions.append(question)
        shuffled_private.append(private_question)
    packet = {
        "schema_version": "OWNER28_HUMAN_REVIEW_PACKET_V1",
        "human_gold": 0,
        "status": "NOT_REVIEWED",
        "agent_labels_included": False,
        "model_predictions_included": False,
        "scores_included": False,
        "questions": shuffled_questions,
    }
    packet["packet_content_sha256"] = content_digest(packet)
    mapping = {
        "schema": "OWNER28_HUMAN_REVIEW_ID_MAP_V1",
        "human_gold": 0,
        "roles_included": False,
        "predictions_included": False,
        "scores_included": False,
        "shuffle_seed_hex": seed,
        "shuffle_seed_sha256": sha(seed.encode("utf-8")),
        "packet_content_sha256": packet["packet_content_sha256"],
        "questions": shuffled_private,
    }
    return packet, mapping


def blank_submission(packet: dict, slot: str) -> dict:
    return {
        "schema_version": "OWNER28_HUMAN_REVIEW_SUBMISSION_V1",
        "reviewer_slot": slot,
        "packet_content_sha256": packet["packet_content_sha256"],
        "human_gold": 0,
        "reviewer_name": "",
        "signed_at": "",
        "items": [
            {
                "item_id": item["item_id"],
                "truth": "",
                "temporality": "",
                "same_scope": "",
                "source_location": "",
                "confidence": "",
                "issue": "",
            }
            for question in packet["questions"]
            for item in question["passages"]
        ],
    }


def main() -> None:
    if any((PRIV / name).exists() for name in (
        "REVIEW_ID_MAP.json", "REVIEW_PACKET_A.json", "REVIEW_PACKET_B.json",
        "REVIEW_SUBMISSION_A_BLANK.json", "REVIEW_SUBMISSION_B_BLANK.json",
    )):
        raise SystemExit("REVIEW_PACK_ALREADY_EXPORTED")
    prediction, compat, curator, id_map, custody = load_inputs()
    seed = secrets.token_hex(32)
    packet, mapping = build(seed, prediction, compat, curator, id_map)
    packet_a = dict(packet, reviewer_slot="A")
    packet_b = dict(packet, reviewer_slot="B")
    metadata_leak_scan([packet_a, packet_b], custody)
    PRIV.mkdir(parents=True, exist_ok=True)
    map_bytes = dumps(mapping)
    packet_a_bytes = dumps(packet_a)
    packet_b_bytes = dumps(packet_b)
    blank_a = dumps(blank_submission(packet_a, "A"))
    blank_b = dumps(blank_submission(packet_b, "B"))
    counts = {
        "schema": "OWNER28_HUMAN_REVIEW_PACK_COUNTS_V1",
        "human_gold": 0,
        "status": "PACK_PREPARED_NOT_REVIEWED",
        "main_questions": 32,
        "retrieved_passages": 160,
        "official_lineages": sorted(INSTRUMENTS),
        "official_lineage_count": len(INSTRUMENTS),
        "fact_units": 4,
        "independent_fact_samples": False,
        "sentence_citation_status": "SOURCE_UNVERIFIED",
        "unverified_sentence_count": 160,
        "reviewer_slots_prepared": ["A", "B"],
        "submissions_received": 0,
        "adjudications_received": 0,
        "agent_labels_in_packet": False,
        "model_predictions_in_packet": False,
        "scores_in_packet": False,
        "packet_content_sha256": packet["packet_content_sha256"],
        "packet_a_sha256": sha(packet_a_bytes),
        "packet_b_sha256": sha(packet_b_bytes),
        "blank_a_sha256": sha(blank_a),
        "blank_b_sha256": sha(blank_b),
        "private_id_map_sha256": sha(map_bytes),
        "shuffle_seed_sha256": mapping["shuffle_seed_sha256"],
        "private_location": "LOCAL_PRIVATE_OUTSIDE_GIT",
        "labels_in_git": False,
    }
    (PRIV / "REVIEW_ID_MAP.json").write_bytes(map_bytes)
    (PRIV / "REVIEW_PACKET_A.json").write_bytes(packet_a_bytes)
    (PRIV / "REVIEW_PACKET_B.json").write_bytes(packet_b_bytes)
    (PRIV / "REVIEW_SUBMISSION_A_BLANK.json").write_bytes(blank_a)
    (PRIV / "REVIEW_SUBMISSION_B_BLANK.json").write_bytes(blank_b)
    (REVIEW_DIR / "HUMAN_REVIEW_PACK_COUNTS.json").write_bytes(dumps(counts))
    if sha((PRIV_SRC / "EVAL_LABEL_CUSTODY.json").read_bytes()) != CUSTODY_SHA:
        raise SystemExit("CUSTODY_CHANGED")
    print(sha(Path(__file__).read_bytes()))
    print(counts["packet_content_sha256"])
    print(counts["private_id_map_sha256"])
    print(sha((REVIEW_DIR / "HUMAN_REVIEW_PACK_COUNTS.json").read_bytes()))


if __name__ == "__main__":
    sys.exit(main())
