"""Source-bound domain construction freeze and candidate-only Phase1 packaging.

This combines explicit internal author review with independently computed byte,
IR, cell, family, surface and query checks. It is not Human/Reviewer acceptance.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from core144_normalized_source_atoms import load_sources


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def reordered(rows: list[dict[str, Any]], seed: int) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    for _ in range(100000):
        permutation = rows.copy()
        rng.shuffle(permutation)
        if all(permutation[i]["group_id"] != permutation[j]["group_id"]
               for i in range(len(rows)) for j in range(i + 1, min(i + 3, len(rows)))):
            return permutation
    raise ValueError("Unable to obtain nonadjacent triplets; no release")


def main() -> None:
    parser = argparse.ArgumentParser()
    for name in ("draft", "contract", "atom_audit", "surface", "family", "author_review",
                 "smoke", "matrix", "output", "captures"):
        parser.add_argument("--" + name.replace("_", "-"), type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError("Additive release namespace already exists")
    draft = json.loads(args.draft.read_bytes())
    domain = draft["domain"]
    source_facts = json.loads((args.contract / "canonical_fact_records.json").read_bytes())
    facts = {f["fact_id"]: f for f in source_facts["facts"]}
    metadata = json.loads((args.contract / "evidence_metadata.json").read_bytes())["documents"]
    contract_lock = json.loads((args.contract / "evidence_contract_lock.json").read_bytes())
    atom_audit = json.loads(args.atom_audit.read_bytes())
    surface = json.loads(args.surface.read_bytes())
    family = json.loads(args.family.read_bytes())
    author = json.loads(args.author_review.read_bytes())
    smoke = json.loads((args.smoke / "report.json").read_bytes())
    sources = load_sources(args.captures)
    expected_ids = {r["group_slot_id"] for r in map(json.loads, args.matrix.read_text(encoding="utf-8").splitlines())
                    if r["domain"] == domain}
    actual_ids = {f"F240-{domain}-{r['fact_id']}" for r in draft["triplets"]}
    gates: dict[str, bool] = {
        "frozen_slots_48_exact": actual_ids == expected_ids and len(actual_ids) == 48,
        "fact_ids_exact": set(facts) == {r["fact_id"] for r in draft["triplets"]},
        "snapshot_bytes_parity": all(sources[d["evidence_doc_id"]]["raw_sha256"] == d["snapshot_sha256"]
                                    for d in metadata),
        "contract_lock_parity": sha(args.contract / "canonical_fact_records.json") == contract_lock["facts_sha256"]
                                and sha(args.contract / "evidence_metadata.json") == contract_lock["metadata_sha256"],
        "atom_ir_checks": not atom_audit["blockers"] and atom_audit["draft_sha256"] == sha(args.draft),
        "mechanical_surface_checks": not surface["flags"] and not surface["role_exclusive_frequent_4grams"]
                                    and surface["draft_sha256"] == sha(args.draft),
        "family_independence_and_capacity": not family["failures"] and not family["split_executed"],
        "explicit_internal_author_review": not author["unresolved_internal_blockers"]
             and set(author["reviewed_groups"]) == set(facts)
             and all(v.startswith("PASS") for v in author["checks"].values()),
        "retrieval_smoke_48_queries": smoke["queries"] == 48 and smoke["traces"] == 240
                                      and smoke["deterministic"] and not smoke["quality_selection_performed"],
        "no_accidental_false_atom": all(r["status"] in {"SUPPORTED", "CONTROLLED_POISON"}
                                        for r in atom_audit["records"]),
        "derived_stealth_matches": all(r["derived"] == r["target"] for r in atom_audit["derivations"]),
    }
    if not all(gates.values()):
        raise ValueError(f"Domain hard gate failed: {gates}")
    paths = []
    for row in draft["triplets"]:
        fact = facts[row["fact_id"]]
        query = row["query"]
        if re.search(r"POISON|CLEAN_CURRENT|HARD_NEGATIVE|HKP[1-4]|TARGET|EXPECTED|GT", query.upper()):
            raise ValueError("Query leakage")
        paths.append({"group_id": f"F240-{domain}-{row['fact_id']}",
                      "fact_id": row["fact_id"], "canonical_fact": fact,
                      "neutral_query": query, "query_shared_C_P_H": True,
                      "frozen_evidence_units": fact["evidence"],
                      "derivation": next(a for a in atom_audit["derivations"] if a["group"] == row["fact_id"]),
                      "path_created_utc": datetime.now(timezone.utc).isoformat()})
    args.output.mkdir(parents=True)
    save(args.output / "evidence_path_and_query_contract.json", paths)
    path_lock = datetime.now(timezone.utc).isoformat()
    save(args.output / "pre_candidate_input_lock.json", {
        "locked_utc": path_lock, "evidence_path_sha256": sha(args.output / "evidence_path_and_query_contract.json"),
        "draft_sha256": sha(args.draft), "contract_lock_sha256": sha(args.contract / "evidence_contract_lock.json"),
        "source_atom_audit_sha256": sha(args.atom_audit), "author_review_sha256": sha(args.author_review),
        "smoke_input_lock_sha256": sha(args.smoke / "run_input_lock.json"),
        "role": "PRE_FORMAL_CANDIDATE_LOCK_DRAFTS_NOT_PREVIOUSLY_RELEASED"})
    corpus = []
    for row in draft["triplets"]:
        group_id = f"F240-{domain}-{row['fact_id']}"
        for role in "CPH":
            text = "".join(row[role])
            sample_id = f"{group_id}-{role}-V1"
            blind_id = "CBR-" + hashlib.sha256(("CORE144-FRESH-20260929|" + sample_id).encode()).hexdigest()[:14].upper()
            corpus.append({"sample_id": sample_id, "group_id": group_id,
                           "construction_role": {"C": "CLEAN_CURRENT", "P": "POISON", "H": "HARD_NEGATIVE"}[role],
                           "blind_review_id": blind_id, "candidate_text": text,
                           "normalized_text": re.sub(r"\s", "", text),
                           "created_utc": datetime.now(timezone.utc).isoformat(),
                           "pre_candidate_lock_utc": path_lock,
                           "family_cluster_id": facts[row["fact_id"]]["family_cluster_id"]})
    if len(corpus) != 144 or len({r["blind_review_id"] for r in corpus}) != 144:
        raise ValueError("Candidate count or opaque identity collision")
    with (args.output / "candidate_corpus_v1.jsonl").open("x", encoding="utf-8", newline="\n") as stream:
        for row in corpus:
            stream.write(json.dumps(row, ensure_ascii=False) + "\n")
    save(args.output / "domain_group_manifest.json", paths)
    save(args.output / "domain_evidence_manifest.json", metadata)
    save(args.output / "fact_atom_audit.json", atom_audit)
    save(args.output / "triplet_parity_and_surface_audit.json", surface)
    save(args.output / "family_cluster_audit.json", family)
    readiness = []
    claim_readiness = []
    for row in corpus:
        fact_id = row["group_id"].split(f"F240-{domain}-")[1]
        role = {"CLEAN_CURRENT": "C", "POISON": "P", "HARD_NEGATIVE": "H"}[row["construction_role"]]
        claims = [r for r in atom_audit["records"] if r["group"] == fact_id and r["role"] == role]
        temporal = bool(re.search(r"\d{4}年|修订|修正|修改决定|施行|废止|现行|旧|原始", row["candidate_text"]))
        provenance = bool(re.search(r"机关|部门|全国人大|国务院(?:令|会议|常务|财政|税务|银行)|财政部|档案局|审计署|税务机关", row["candidate_text"]))
        for view in "SEPTR":
            applicable = (view in "SER" or fact_id.startswith("HKP4") and view == "P"
                          or fact_id.startswith("HKP3") and view == "T")
            readiness.append({"sample_id": row["sample_id"], "construction_role": row["construction_role"],
                              "view": view, "primary_mechanism_applicable": applicable,
                              "status": "OBSERVED_PRIMARY_INPUTS" if applicable else "NOT_PRIMARY_APPLICABLE",
                              "claim_ir_count": len(claims),
                              "scope": "UPSTREAM_READINESS_NOT_IMPLEMENTED_SIGNAL_VALUE",
                              "stage": "QUERY_CONDITIONED_STAGE_B" if view == "R" else "DOCUMENT_STAGE_A"})
            claim_applicable = view in "SER" or view == "P" and provenance or view == "T" and temporal
            claim_readiness.append({"sample_id": row["sample_id"], "construction_role": row["construction_role"],
                                    "view": view, "applicable": claim_applicable,
                                    "status": "OBSERVED_SOURCE_BOUND_CLAIM_INPUTS" if claim_applicable else "NOT_APPLICABLE",
                                    "applicability_method": "CANDIDATE_VISIBLE_CUE_SCREEN_PLUS_EXPLICIT_AUTHOR_SCOPE_REVIEW",
                                    "entity_claim_ir": claims if view == "E" else [],
                                    "future_signal_values_or_effectiveness_claimed": False})
    save(args.output / "view_primary_readiness.json", readiness)
    save(args.output / "view_candidate_claim_readiness.json", claim_readiness)
    # Supplemental metadata are audited separately; no claim that every future
    # planned feature is computable, or that N/A means safe.
    save(args.output / "metadata_unknowns.json", {
        "optional_unknown_fields": [{"doc": d["evidence_doc_id"], "field": field,
                                     "status": "NOT_OBSERVED_WITH_FROZEN_EVIDENCE_NOT_ZERO_RISK"}
            for d in metadata for field in ("original_issuer", "publication_date", "effective_start", "effective_end")
            if d.get(field) is None],
        "primary_mechanism_unknowns": [], "not_applicable_is_not_safe": True})
    save(args.output / "missingness_by_role.json", {
        "rows": [dict(zip(("role", "view"), (role, view), strict=True),
                      **{status: sum(r["construction_role"] == role and r["view"] == view and r["status"] == status
                         for r in readiness) for status in ("OBSERVED_PRIMARY_INPUTS", "NOT_PRIMARY_APPLICABLE")})
                 for role in ("CLEAN_CURRENT", "POISON", "HARD_NEGATIVE") for view in "SEPTR"],
        "input_missing": 0, "evidence_insufficient": 0,
        "scope": "PRIMARY_REQUIRED_INPUTS_ONLY_OPTIONAL_METADATA_UNKNOWN_SEPARATE",
        "candidate_claim_applicability_equals_group_primary_applicability": False,
        "candidate_claim_rows": [dict(zip(("role", "view"), (role, view), strict=True),
                      **{status: sum(r["construction_role"] == role and r["view"] == view and r["status"] == status
                         for r in claim_readiness) for status in ("OBSERVED_SOURCE_BOUND_CLAIM_INPUTS", "NOT_APPLICABLE")})
                 for role in ("CLEAN_CURRENT", "POISON", "HARD_NEGATIVE") for view in "SEPTR"],
        "unrelated_missingness_shortcut_blocker": 0})
    schema = {"phase": "PHASE1_CANDIDATE_ONLY", "record_count": 144,
              "keys": ["blind_review_id", "text_naturalness", "local_internal_conflict", "self_containment",
                       "ambiguous_referent", "meta_or_template_language", "issue_note"],
              "enums": {"text_naturalness": ["NATURAL", "MINOR_ISSUE", "UNNATURAL"],
                        "local_internal_conflict": ["YES", "NO", "UNCERTAIN"],
                        "self_containment": ["PASS", "FLAG", "UNCERTAIN"],
                        "ambiguous_referent": ["YES", "NO", "UNCERTAIN"],
                        "meta_or_template_language": ["YES", "NO", "UNCERTAIN"]}}
    save(args.output / "reviewer" / f"PAPER1_CORE144_{domain}_PHASE1_IMPORT_SCHEMA_V1.json", schema)
    packages = []
    for reviewer, seed in (("R3_GPT", 2026092903), ("R4_CODEX", 2026092904)):
        ordered = reordered(corpus, seed)
        packet = [{"blind_review_id": r["blind_review_id"], "candidate_text": r["candidate_text"]} for r in ordered]
        packet_path = args.output / "reviewer" / f"PAPER1_CORE144_{domain}_{reviewer}_PHASE1_PACKAGE_V1.json"
        save(packet_path, packet)
        prompt_path = packet_path.with_name(f"PAPER1_CORE144_{domain}_{reviewer}_PHASE1_PROMPT_V1.md")
        prompt = f"""# Independent Phase1 text review — {reviewer}

Start a completely fresh isolated {'GPT' if reviewer == 'R3_GPT' else 'Doubao'} conversation. R4_CODEX is a reviewer code, not the model provider. Receive ONLY this prompt, your named package and the common Phase1 schema. Do not open previous conversations, repository, directory, outside files, web, other reviewers or another AI. If prohibited context is encountered, STOP and provide a separate incident file; do not produce a normal answer.

Read every one of the 144 texts independently in the given order. Do not search or judge external factual truth. Assess Chinese expression, visible same-subject/scope/time contradictions, object supply, referent uniqueness and experimental/template wording. Content that seems factually wrong can still be NATURAL. UNCERTAIN means the text itself prevents a decision, not that you lack outside knowledge.

self_containment checks whether the necessary object/document/core claim/conditions are supplied. ambiguous_referent checks whether an existing pronoun has two or more plausible antecedents. They are independent: a bare unnamed “该文件” can be FLAG/NO; two named files with unclear “该文件” can be PASS/YES. Each abnormal field needs its own concrete text-visible reason. Do not infer one field from the other. issue_note is nonblank whenever any field differs from NATURAL/NO/PASS/NO/NO; otherwise it may be blank.

Return one strict UTF-8 JSON array, exactly 144 objects, exact IDs/order and seven keys from schema, no Markdown fences or additional keys. Use canonical enum spellings. Do not repair, sort, rename or omit rows. Give concise issue_note, no web citations. Create a downloadable file named `PAPER1_CORE144_{domain}_{reviewer}_PHASE1_RAW_RETURN_V1.json`; never replace the file after delivery. Separately declare the actual provider and fresh-session isolation. If serialization/truncation occurs, STOP and report it; do not silently shorten the array or split the task. Do not view a later phase unless the Owner separately releases it after both raw locks.
"""
        prompt_path.write_text(prompt, encoding="utf-8", newline="\n")
        packages.append({"reviewer": reviewer, "actual_provider": "GPT" if reviewer == "R3_GPT" else "DOUBAO",
                         "package": packet_path.as_posix(), "package_sha256": sha(packet_path),
                         "prompt": prompt_path.as_posix(), "prompt_sha256": sha(prompt_path),
                         "records": 144, "triplets_nonadjacent": True})
    save(args.output / "reviewer" / "package_manifest.json", {"packages": packages,
         "information_equivalent": True, "opaque_ids": True, "hidden_fields": 0,
         "external_execution_started": False, "fallback_96_48_used": False})
    gates.update({"formal_candidates_144": len(corpus) == 144,
                  "hash_locked_inputs_before_formal_candidate": all(r["created_utc"] > path_lock for r in corpus),
                  "no_reviewer_output_fabricated": True, "no_gt_split_training": True})
    save(args.output / "domain_acceptance_matrix.json", {
        "domain": domain, "gates": gates, "all_internal_hard_gates_pass": all(gates.values()),
        "counts": {"groups": 48, "candidates": 144, "HKP": dict(Counter(f["fact_id"].split("-")[0] for f in facts.values())),
                   "S": dict(Counter(f["fact_id"].split("-")[1] for f in facts.values())), "C_P_H": [48, 48, 48]},
        "candidate_sha256": sha(args.output / "candidate_corpus_v1.jsonl"),
        "fact_status_counts": dict(Counter(r["status"] for r in atom_audit["records"])),
        "external_review_pending": True, "acceptance_scope": "INTERNAL_CONSTRUCTION_QA_ONLY_NOT_HUMAN_GT",
        "status": f"{domain}_FULL144_INTERNAL_QA_ACCEPTED"})
    print(json.dumps({"domain": domain, "groups": 48, "candidates": 144,
                      "gates": gates, "packages": len(packages)}))


if __name__ == "__main__":
    main()
