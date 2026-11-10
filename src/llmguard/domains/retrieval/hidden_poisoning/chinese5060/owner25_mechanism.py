"""Receipt-gated selection for the Owner25 synthetic pilot."""
from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from .s1b_oneshot_adapter import project
from .s1b_rule_v2 import extract_one

ARMS = (
    "NONE", "FIXED_PARENT_PROXY", "ANCHOR_ONLY", "SCOPE_VERSION_ONLY", "JOINT_P0",
    "FORGED_RECEIPT_NEGCTRL", "JOINT_P0_HALF_RECEIPTS", "JOINT_P0_RAW_RULE_V2",
)
UNAVAILABLE = {
    "RD_B2": "Same-world neural Stage 2 embeddings not presealed; new inference outside zero-model scope",
    "RD_ZH": "Character TF-IDF changes Stage 1 only; same-world Stage 2 embeddings still required",
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


@dataclass(frozen=True)
class Claim:
    subject: str
    attribute: str
    value: str
    unit: str
    scope: str
    version: str
    start: str
    end: str

    def comparable(self, query: Mapping[str, str]) -> bool:
        return (self.subject, self.attribute, self.unit) == (query["subject"], query["attribute"], query["unit"])

    def applicable(self, query: Mapping[str, str]) -> bool:
        return self.comparable(query) and self.scope == query["scope"] and self.start <= query["at"] <= self.end


def receipt(doc: dict[str, Any], registry: dict[str, Any], ref: str | None) -> dict[str, Any] | None:
    entry = registry["receipts"].get(ref)
    if entry is None:
        return None
    issuer = registry["issuers"].get(entry["issuer"])
    if issuer is None or not issuer["enabled"] or entry["family"] != issuer["family"]:
        return None
    if (entry["document"] != doc["id"] or entry["body_sha256"] != sha(doc["text"].encode())
            or entry["parent_sha256"] != doc["parent_sha256"]
            or entry["scope"] not in issuer["authorized_scopes"]
            or not issuer["not_before"] <= entry["issued"] <= issuer["not_after"]):
        return None
    return entry


def raw_claim(query: dict[str, str], text: str) -> tuple[Claim | None, str]:
    try:
        p = project(extract_one(query["text"], text), text)
    except ValueError:
        return None, "INVALID_SPAN"
    if p["status"] != "ANSWER":
        return None, "RULE_UNKNOWN"
    scope = (p["scope"] or {}).get("jurisdiction")
    # Reject ambiguous or incomplete binding and exceptions. No fixture-assisted
    # value, date, version or scope repair is permitted in the text arm.
    if (not all((p["subject"], p["attribute"], p["value"], p["unit"], p["version"],
                 p["effective_from"], p["effective_to"], scope, p["spans"]))
            or p["condition"] or p["exception"] or p["negation"]):
        return None, "INCOMPLETE_NATIVE_BINDING"
    return Claim(str(p["subject"]), str(p["attribute"]), str(p["value"]), str(p["unit"]), str(scope),
                 str(p["version"]), str(p["effective_from"]), str(p["effective_to"])), "BOUND"


def decide(world: dict[str, Any], registry: dict[str, Any], claims: Mapping[str, Claim | None],
           arm: str) -> dict[str, Any]:
    docs = world["docs"]
    ids = [d["id"] for d in docs]
    parent = set(world["parent_keep"])
    query = world["query"]
    refs = [d["receipt_ref"] for d in docs]
    if arm == "FORGED_RECEIPT_NEGCTRL":
        issued = [ref if receipt(doc, registry, ref) else None for doc, ref in zip(docs, refs, strict=True)]
        refs = issued[1:] + issued[:1]
    entries = {
        d["id"]: verified for d, ref in zip(docs, refs, strict=True)
        if (verified := receipt(d, registry, ref)) is not None
        and (arm != "JOINT_P0_HALF_RECEIPTS" or ref in registry["half_keep"])
    }
    eligible: dict[str, Claim] = {}
    for key, entry in entries.items():
        claim = claims[key]
        if claim is None or not claim.comparable(query):
            continue
        bound = (claim.scope, claim.version, claim.start, claim.end) == (
            entry["scope"], entry["version"], entry["start"], entry["end"],
        )
        if bound and (arm == "ANCHOR_ONLY" or claim.applicable(query)):
            eligible[key] = claim
    if arm in {"NONE", "FIXED_PARENT_PROXY", "SCOPE_VERSION_ONLY"}:
        eligible = {}
    votes: dict[str, set[str]] = {}
    for key, claim in eligible.items():
        votes.setdefault(entries[key]["family"], set()).add(claim.value)
    values = set().union(*votes.values())
    status = "UNRESOLVED"
    kept = set(ids) if arm == "NONE" else parent.copy()
    if len(values) == 1:
        status = "ANCHORED"
        accepted = next(iter(values))
        for key, claim in claims.items():
            if claim is None:
                continue
            comparable = claim.comparable(query) if arm == "ANCHOR_ONLY" else claim.applicable(query)
            if comparable and claim.value != accepted:
                kept.discard(key)
        # P0 uplift requires a hash-bound receipt on the same document.
        kept.update(eligible)
    return {
        "keep": [key for key in ids if key in kept],
        "verified": sorted(entries),
        "eligible": sorted(eligible),
        "families": {key: sorted(vals) for key, vals in sorted(votes.items())},
        "restored": sorted(kept - parent) if arm != "NONE" else [],
        "anchor_status": status,
        "anchor_value": next(iter(values)) if status == "ANCHORED" else None,
        "scope_conflict_cues": sum(
            c is not None and c.comparable(query) and not c.applicable(query) for c in claims.values()
        ),
    }
