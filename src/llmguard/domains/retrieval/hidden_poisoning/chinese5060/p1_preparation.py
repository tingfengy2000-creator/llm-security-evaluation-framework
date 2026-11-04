"""D1 development preparation only. No retrieval, defense, generation or judging."""
from __future__ import annotations

import hashlib
import unicodedata
from typing import Any

from .control_plane import validate_world_membership
from .snapshots import digest


def assert_no_sibling_bodies(documents: list[dict[str, Any]], forbidden_bodies: list[str]) -> None:
    """Check corpus bodies as well as lineage; does not equate shared facts to copies."""
    def normalize(text: str) -> str:
        return "".join(unicodedata.normalize("NFKC", text).split())
    for body in forbidden_bodies:
        needle = normalize(body)
        if not needle:
            raise ValueError("EMPTY_SIBLING_BODY")
        if any(needle in normalize(d["text"]) for d in documents):
            raise ValueError("SIBLING_BODY_IN_INDEX_DESIGN")


def audit_proposal(query: dict[str, Any], proposal: dict[str, Any],
                   sources: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Locate source spans without promoting AI proposals into a human answer key."""
    if query["query_id"] != proposal["query_id"] or query["query_text"] != proposal["question_draft"]:
        raise ValueError("QUERY_VERSION_MISMATCH")
    if proposal.get("human_approved") or proposal.get("pilot_execution_approved"):
        raise ValueError("UNEXPECTED_APPROVAL_REQUIRES_REVIEW")
    required: set[str] = set()
    bad_spans = 0
    quotes = 0
    for fact in proposal["facts"]:
        if not fact["citations"]:
            bad_spans += 1
        for citation in fact["citations"]:
            quotes += 1
            sid = citation["source_id"]
            required.add(sid)
            source = sources.get(sid)
            if source is None:
                bad_spans += 1
                continue
            start, end = citation["start"], citation["end"]
            if (type(start) is not int or type(end) is not int or start < 0 or end <= start
                    or end > len(source["text"]) or source["text"][start:end] != citation["quote"]):
                bad_spans += 1
    source_rows = [sources[sid] for sid in sorted(required) if sid in sources]
    return {
        "query_id": query["query_id"], "query_sha256": digest(query["query_text"]),
        "query_text": query["query_text"], "time_scope": proposal["time_scope"],
        "answer_boundary_proposal": proposal["answer_proposal"], "conditions_and_caveats": proposal["caveats"],
        "facts_evaluator_only": proposal["facts"], "required_source_ids_evaluator_only": sorted(required),
        "citation_count": quotes, "invalid_citation_spans": bad_spans,
        "source_snapshot_hashes": {s["source_id"]: s["snapshot_text_sha256"] for s in source_rows},
        "publication_metadata_missing": sum(s["metadata"].get("publication_date") is None for s in source_rows),
        "effective_start_metadata_missing": sum(s["metadata"].get("effective_start") is None for s in source_rows),
        "source_text_and_span_status": "PASS" if not bad_spans else "FAIL",
        "evaluation_freeze_status": "NEEDS_ADJUDICATION", "human_gold": False,
        "trusted_provenance_root_verified": False,
        "attack_target": None, "attack_intent_inferred_from_label": False,
        "missing_adjudications": ["ANSWER_EQUIVALENCE_AND_SCOPE_RUBRIC", "PER_WORLD_SUFFICIENCY",
                                  "INDEPENDENT_OFFICIAL_PROVENANCE_ROOT", "EXPLICIT_ATTACK_TARGET"],
    }


def verify_source_texts(sources: list[dict[str, Any]]) -> None:
    if len({s["source_id"] for s in sources}) != len(sources):
        raise ValueError("DUPLICATE_SOURCE")
    for source in sources:
        if hashlib.sha256(source["text"].encode()).hexdigest() != source["snapshot_text_sha256"]:
            raise ValueError("SOURCE_TEXT_HASH_MISMATCH")


def design_world(query: dict[str, Any], *, candidate_id: str, candidate_text: str,
                 all_sibling_ids: list[str], sources: list[dict[str, Any]]) -> dict[str, Any]:
    """Build a role-free index PLAN. One candidate, all fixed background copies.

    Official-looking copies stay UNVERIFIED. The trusted registry is separate and
    blocked until independent provenance is verified. No answer citations select
    background documents or retrieval ranks. No index is built by this function.
    """
    if candidate_id not in all_sibling_ids or len(set(all_sibling_ids)) != 3:
        raise ValueError("COMPLETE_COUNTERFACTUAL_MEMBERSHIP_REQUIRED")
    world_id = "w-" + digest(["p1-world-v1", query["query_id"], candidate_id])[:24]
    candidate_doc = "d-" + digest(["candidate-doc", candidate_id])[:24]
    documents: list[dict[str, Any]] = [{"document_id": candidate_doc, "text": candidate_text,
                  "content_sha256": hashlib.sha256(candidate_text.encode()).hexdigest(),
                  "source_id": "s-" + digest(candidate_id)[:24], "authority_claim": "UNVERIFIED",
                  "publication_time": None, "effective_time": None, "trust_boundary": "UNVERIFIED"}]
    lineage = {candidate_doc: ("candidate-group", candidate_id)}
    expected = {"candidate-group": candidate_id}
    for source in sources:
        uid = "d-" + digest(["background-copy", source["source_id"], source["snapshot_text_sha256"]])[:24]
        documents.append({"document_id": uid, "text": source["text"], "content_sha256": source["snapshot_text_sha256"],
                          "source_id": source["source_id"], "authority_claim": source["metadata"].get("issuer"),
                          "publication_time": source["metadata"].get("publication_date"),
                          "effective_time": source["metadata"].get("effective_start"), "trust_boundary": "UNVERIFIED"})
        lineage[uid] = (uid, uid)
        expected[uid] = uid
    validate_world_membership([d["document_id"] for d in documents], selected=candidate_id,
                              lineage=lineage, expected_manifest=expected)
    return {"world_id": world_id, "query_id": query["query_id"], "query_text": query["query_text"],
            "documents": documents, "corpus_hash": digest(documents),
            "index_namespace": world_id, "index_status": "DESIGN_ONLY_NOT_BUILT",
            "topK_snapshot_hash": None, "trusted_registry": [],
            "trusted_provenance_status": "BLOCKED_PENDING_INDEPENDENT_ROOT",
            "variant_or_group_or_label_in_runtime": False}
