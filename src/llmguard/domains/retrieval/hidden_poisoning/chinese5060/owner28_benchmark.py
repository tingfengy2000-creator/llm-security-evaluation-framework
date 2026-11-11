"""Owner28 public schemas and immutable four-arm mask rules. No label readers."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from .owner27_version_guard import visible_date_filter

ARMS = ("NONE", "RD_B2", "RD_ZH", "DATE_ONLY")
AUTHORITY = "W1-OD-20261111-PAPER1-OWNER28-BENCHMARK-INDEPENDENT-PILOT"
EXCLUDED = {"PUBLIC_HYGIENE", "BASIC_DRUG_CATALOG", "STATUTORY_HOLIDAYS", "DRIVING_LICENSE"}
WORLD_KEYS = {"world_id", "fact_uid", "event_date", "query_text", "documents"}
DOCUMENT_KEYS = {"document_id", "source_id", "text", "content_sha256", "source_uri"}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def exact_keys(value: Any, allowed: set[str]) -> None:
    if not isinstance(value, dict) or set(value) != allowed:
        raise ValueError("ROLE_FREE_SCHEMA")


def uid(value: Any, prefix: str) -> None:
    if not isinstance(value, str) or not re.fullmatch(prefix + r"-[0-9a-f]{24}", value):
        raise ValueError("OPAQUE_UID_REQUIRED")


def hash_string(value: Any) -> None:
    if not isinstance(value, str) or not re.fullmatch("[0-9a-f]{64}", value):
        raise ValueError("SHA256_REQUIRED")


def public_uri(value: Any) -> None:
    if value is None:
        return
    if not isinstance(value, str) or len(value) > 2048:
        raise ValueError("SOURCE_URI_TYPE")
    uri = urlsplit(value)
    if uri.scheme != "https" or not uri.hostname or not uri.hostname.endswith(".gov.cn") or uri.username:
        raise ValueError("OFFICIAL_METADATA_URI_REQUIRED")


def parse_json(data: bytes) -> Any:
    def reject_duplicate(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value = {}
        for key, item in pairs:
            if key in value:
                raise ValueError("DUPLICATE_JSON_KEY")
            value[key] = item
        return value
    return json.loads(data, object_pairs_hook=reject_duplicate)


def validate_payload(value: Any, fixture: bool = False) -> list[dict[str, Any]]:
    exact_keys(value, {"schema_version", "main", "mirrors"})
    if value["schema_version"] != "OWNER28_ROLE_FREE_V1":
        raise ValueError("SCHEMA_VERSION")
    main, mirrors = value["main"], value["mirrors"]
    expected = 2 if fixture else 32
    if not isinstance(main, list) or len(main) != expected or not isinstance(mirrors, list) or len(mirrors) not in {0, 8}:
        raise ValueError("WORLD_DENOMINATOR")
    rows = main + mirrors
    seen_worlds: set[str] = set()
    seen_documents: set[str] = set()
    for world in rows:
        exact_keys(world, WORLD_KEYS)
        uid(world["world_id"], "w")
        uid(world["fact_uid"], "f")
        if world["world_id"] in seen_worlds:
            raise ValueError("WORLD_REUSED")
        seen_worlds.add(world["world_id"])
        if date.fromisoformat(world["event_date"]).isoformat() != world["event_date"]:
            raise ValueError("QUERY_DATE_FORMAT")
        if not isinstance(world["query_text"], str) or not 1 <= len(world["query_text"]) <= 2000:
            raise ValueError("QUERY_TEXT")
        if not isinstance(world["documents"], list) or len(world["documents"]) != 11:
            raise ValueError("CORPUS_DENOMINATOR")
        for doc in world["documents"]:
            exact_keys(doc, DOCUMENT_KEYS)
            uid(doc["document_id"], "d")
            uid(doc["source_id"], "s")
            if doc["document_id"] in seen_documents:
                raise ValueError("CROSS_WORLD_DOCUMENT_ID")
            seen_documents.add(doc["document_id"])
            if not isinstance(doc["text"], str) or not 1 <= len(doc["text"]) <= 8192:
                raise ValueError("DOCUMENT_TEXT")
            hash_string(doc["content_sha256"])
            if sha(doc["text"].encode()) != doc["content_sha256"]:
                raise ValueError("DOCUMENT_BYTES")
            public_uri(doc["source_uri"])
    main_groups = Counter(w["fact_uid"] for w in main)
    if not fixture and (len(main_groups) != 4 or set(main_groups.values()) != {8}):
        raise ValueError("FOUR_FACTS_EIGHT_WORLDS")
    if mirrors and Counter(w["fact_uid"] for w in mirrors) != {g: 2 for g in main_groups}:
        raise ValueError("TIME_MIRROR_GROUPS")
    return rows


def validate_curator(value: Any, payload_sha: str, mirror_worlds: int) -> None:
    exact_keys(value, {"schema_version", "authority", "producer_branch", "role_free_sha256", "private_custody_sha256",
                       "query_view_sha256", "selection_sha256", "main_worlds", "mirror_worlds", "label_status",
                       "human_gold", "dev_outputs_accessed", "source_type", "source_audits", "excluded_lineages", "attestation"})
    if (value["schema_version"], value["authority"], value["producer_branch"]) != (
        "OWNER28_CURATOR_V1", AUTHORITY, "research/paper1-ragdefender-repro-5090"
    ):
        raise ValueError("CURATOR_AUTHORITY")
    if (value["role_free_sha256"], value["main_worlds"], value["mirror_worlds"]) != (payload_sha, 32, mirror_worlds):
        raise ValueError("CURATOR_PAYLOAD_BINDING")
    if (value["label_status"], value["human_gold"], value["dev_outputs_accessed"], value["source_type"],
            value["attestation"]) != (
        "AGENT_PROVISIONAL", 0, False, "SOURCE_GROUNDED_PARAPHRASE", "INDEPENDENT_SOURCE_AND_QUERY_AUDIT_PASSED"
    ):
        raise ValueError("CURATOR_INDEPENDENCE_OR_RIGHTS")
    if value["dev_outputs_accessed"] is not False or type(value["human_gold"]) is not int:
        raise ValueError("CURATOR_TYPE_SAFETY")
    if not isinstance(value["excluded_lineages"], list) or set(value["excluded_lineages"]) != EXCLUDED:
        raise ValueError("EXCLUSION_AUDIT_REQUIRED")
    for key in ("role_free_sha256", "private_custody_sha256", "query_view_sha256", "selection_sha256"):
        hash_string(value[key])
    if not isinstance(value["source_audits"], list) or len(value["source_audits"]) != 4:
        raise ValueError("FOUR_NEW_FACT_UNITS")
    facts, lineages, issuers = set(), set(), set()
    for row in value["source_audits"]:
        exact_keys(row, {"fact_uid", "lineage_id", "issuer_class", "old_uri", "new_uri",
                         "old_effective_from", "old_effective_until", "new_effective_from", "old_locator", "new_locator",
                         "scope_check", "rights", "transition_check"})
        uid(row["fact_uid"], "f")
        if not all(isinstance(row[k], str) and row[k] for k in ("lineage_id", "issuer_class", "old_locator", "new_locator")):
            raise ValueError("SOURCE_IDENTITY")
        if row["lineage_id"].upper() in EXCLUDED or row["scope_check"] != "MATCHED_SAME_OBJECT_PREDICATE":
            raise ValueError("LINEAGE_OR_SCOPE_GATE")
        if row["rights"] != "SELF_AUTHORED_PRIVATE_LOCAL_ONLY":
            raise ValueError("RIGHTS_GATE")
        public_uri(row["old_uri"])
        public_uri(row["new_uri"])
        if not row["old_uri"] or not row["new_uri"] or row["old_uri"] == row["new_uri"]:
            raise ValueError("PAIRED_OFFICIAL_SOURCES_REQUIRED")
        if (date.fromisoformat(row["old_effective_from"]) >= date.fromisoformat(row["new_effective_from"])
                or row["old_effective_until"] != row["new_effective_from"]
                or row["transition_check"] != "NO_UNRESOLVED_TRANSITION_FOR_THIS_SCOPE"):
            raise ValueError("VERSION_DATE_ORDER")
        facts.add(row["fact_uid"])
        lineages.add(row["lineage_id"])
        issuers.add(row["issuer_class"])
    if len(facts) != 4 or len(lineages) < 2 or len(issuers) < 2:
        raise ValueError("CURATION_MINIMUM")


def assemble_masks(count: int, when: str, texts: list[str], b2_deleted: list[int], zh_deleted: list[int]) -> dict[str, Any]:
    if count != 5 or len(texts) != 5:
        raise ValueError("TOPK5_REQUIRED")
    for deleted in (b2_deleted, zh_deleted):
        if any(type(i) is not int or i not in range(count) for i in deleted) or len(set(deleted)) != len(deleted):
            raise ValueError("INVALID_RD_MASK")
    return {
        "NONE": list(range(count)),
        "RD_B2": [i for i in range(count) if i not in b2_deleted],
        "RD_ZH": [i for i in range(count) if i not in zh_deleted],
        "DATE_ONLY": list(visible_date_filter(texts, when)),
    }


def write_once(path: Path, value: Any) -> str:
    data = canonical(value)
    with path.open("xb") as handle:
        handle.write(data)
    return sha(data)
