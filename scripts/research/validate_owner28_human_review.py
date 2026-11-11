"""Validate Owner28 human-review templates. Does not score or sign Gold."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
REVIEW_DIR = REPO / "docs/paper1/dual_machine/repro5090/owner28_eval/human_review"
SCHEMA_PATH = REVIEW_DIR / "HUMAN_REVIEW_IMPORT_SCHEMA.json"
FIXTURE_PATH = REVIEW_DIR / "HUMAN_REVIEW_FIXTURE_CASES.json"
PRIV = Path(r"D:\paper1\private_5090\owner28_eval\human_review")

FORBIDDEN_KEYS = {
    "role",
    "gold_answer",
    "subtype",
    "attack_atom",
    "scenario",
    "scenario_detail",
    "keep_ranks",
    "headline_denominator",
    "planned_focal_density",
    "fact_key",
    "score",
    "poison_retained",
    "clean_false_delete",
    "hn_false_delete",
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def walk_keys(value: object, found: set[str]) -> None:
    if isinstance(value, dict):
        found.update(value)
        for item in value.values():
            walk_keys(item, found)
    elif isinstance(value, list):
        for item in value:
            walk_keys(item, found)


def assert_no_forbidden_keys(value: object) -> None:
    found: set[str] = set()
    walk_keys(value, found)
    leaked = sorted(found & FORBIDDEN_KEYS)
    if leaked:
        raise SystemExit(f"FORBIDDEN_KEY {leaked[0]}")


def validate_schema_document(document: dict) -> None:
    if document.get("schema") != "OWNER28_HUMAN_REVIEW_IMPORT_SCHEMA_V1":
        raise SystemExit("SCHEMA_ID")
    if document.get("human_gold_until_signed") != 0:
        raise SystemExit("HUMAN_GOLD")
    submission = document["submission"]
    for field in ("truth", "temporality", "same_scope", "confidence"):
        if len(submission["enums"][field]) < 2:
            raise SystemExit("ENUM")
    if "ADJUDICATOR" not in submission["reviewer_slot"]:
        raise SystemExit("ADJUDICATOR_SLOT")
    assert_no_forbidden_keys(document)


def validate_fixtures(document: dict) -> None:
    if document.get("schema") != "OWNER28_HUMAN_REVIEW_FIXTURE_V1" or document.get("human_gold") != 0:
        raise SystemExit("FIXTURE_STATUS")
    if document.get("not_real_gold") is not True or len(document["cases"]) != 10:
        raise SystemExit("FIXTURE_COUNT")
    assert_no_forbidden_keys(document)
    for case in document["cases"]:
        if case.get("citation_status") != "SOURCE_UNVERIFIED":
            raise SystemExit("FIXTURE_CITATION")
        if "示例" not in case["fact_object"]:
            raise SystemExit("FIXTURE_NOT_FICTIONAL")


def content_without_slot(packet: dict) -> dict:
    questions = []
    for question in packet["questions"]:
        item = dict(question)
        questions.append(item)
    return {
        "schema_version": packet["schema_version"],
        "human_gold": packet["human_gold"],
        "questions": questions,
    }


def validate_packet(packet: dict, slot: str) -> str:
    if packet.get("schema_version") != "OWNER28_HUMAN_REVIEW_PACKET_V1":
        raise SystemExit("PACKET_SCHEMA")
    if packet.get("reviewer_slot") != slot or packet.get("human_gold") != 0 or packet.get("status") != "NOT_REVIEWED":
        raise SystemExit("PACKET_STATUS")
    if len(packet["questions"]) != 32:
        raise SystemExit("QUESTION_COUNT")
    items = [item for question in packet["questions"] for item in question["passages"]]
    if len(items) != 160 or len({item["item_id"] for item in items}) != 160:
        raise SystemExit("PASSAGE_COUNT")
    if any(item.get("citation_status") != "SOURCE_UNVERIFIED" for item in items):
        raise SystemExit("CITATION_STATUS")
    assert_no_forbidden_keys(packet)
    encoded = (json.dumps(content_without_slot(packet), ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    digest = sha(encoded)
    if packet.get("packet_content_sha256") != digest:
        raise SystemExit("PACKET_CONTENT_SHA")
    return digest


def validate_blank(submission: dict, packet: dict) -> None:
    if submission.get("human_gold") != 0 or submission.get("reviewer_name") or submission.get("signed_at"):
        raise SystemExit("BLANK_SIGNED")
    if submission.get("reviewer_slot") != packet.get("reviewer_slot"):
        raise SystemExit("BLANK_SLOT")
    expected = [item["item_id"] for question in packet["questions"] for item in question["passages"]]
    got = [item["item_id"] for item in submission["items"]]
    if got != expected:
        raise SystemExit("BLANK_ITEMS")
    for item in submission["items"]:
        if any(item[field] for field in ("truth", "temporality", "same_scope", "source_location", "confidence", "issue")):
            raise SystemExit("BLANK_NONEMPTY")
    assert_no_forbidden_keys(submission)


def validate_private() -> None:
    packet_a = load_json(PRIV / "REVIEW_PACKET_A.json")
    packet_b = load_json(PRIV / "REVIEW_PACKET_B.json")
    digest_a = validate_packet(packet_a, "A")
    digest_b = validate_packet(packet_b, "B")
    if digest_a != digest_b:
        raise SystemExit("AB_MISMATCH")
    validate_blank(load_json(PRIV / "REVIEW_SUBMISSION_A_BLANK.json"), packet_a)
    validate_blank(load_json(PRIV / "REVIEW_SUBMISSION_B_BLANK.json"), packet_b)
    mapping = load_json(PRIV / "REVIEW_ID_MAP.json")
    if mapping.get("human_gold") != 0 or mapping.get("roles_included") is not False:
        raise SystemExit("MAP_STATUS")
    assert_no_forbidden_keys(mapping)


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else "--public"
    validate_schema_document(load_json(SCHEMA_PATH))
    validate_fixtures(load_json(FIXTURE_PATH))
    if mode == "--private":
        validate_private()
    elif mode != "--public":
        raise SystemExit("MODE")
    print("REVIEW_TEMPLATE_OK")


if __name__ == "__main__":
    main()
