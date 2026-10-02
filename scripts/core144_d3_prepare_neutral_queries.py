"""Freeze opaque, role-blind D3 information-need queries for IO smoke."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


def save(path: Path, value: object) -> None:
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--draft", type=Path, required=True)
    parser.add_argument("--queries", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    args = parser.parse_args()
    if args.queries.exists() or args.audit.exists():
        raise ValueError("Refusing to overwrite locked query artifact")
    draft = json.loads(args.draft.read_bytes())
    if draft["domain"] != "D3" or len(draft["triplets"]) != 48:
        raise ValueError("D3 draft identity/count mismatch")
    records = []
    mapping = []
    flags = []
    for row in draft["triplets"]:
        query = row["query"]
        if not isinstance(query, str) or len(query) < 12:
            flags.append({"fact_id": row["fact_id"], "code": "SHORT_OR_MISSING_QUERY"})
        if re.search(r"(?i)HKP[1-4]|\bS[123]\b|POISON|CLEAN|HARD_NEGATIVE|EXPECTED|GT", query):
            flags.append({"fact_id": row["fact_id"], "code": "VISIBLE_LABEL_OR_FACTOR"})
        if re.search(r"相同|不同|高于|低于|先于|后于|正确|错误|唯一|四部门|国务院令|全国人大常委会", query):
            flags.append({"fact_id": row["fact_id"], "code": "POTENTIAL_ANSWER_CUE"})
        query_id = "DQ3-" + hashlib.sha256(
            ("CORE144-D3-NEUTRAL-QUERY-V1|" + row["fact_id"]).encode()
        ).hexdigest()[:12].upper()
        records.append({"query_id": query_id, "query_text": query})
        mapping.append({"fact_id": row["fact_id"], "query_id": query_id,
                        "query_text_sha256": hashlib.sha256(query.encode()).hexdigest()})
    if len({r["query_id"] for r in records}) != 48:
        flags.append({"code": "OPAQUE_QUERY_ID_COLLISION"})
    if flags:
        raise ValueError(json.dumps(flags, ensure_ascii=False))
    save(args.queries, {"domain": "D3", "queries": records})
    save(args.audit, {"domain": "D3", "draft_sha256": hashlib.sha256(args.draft.read_bytes()).hexdigest(),
                      "query_file_sha256": hashlib.sha256(args.queries.read_bytes()).hexdigest(),
                      "private_query_to_fact_mapping": mapping,
                      "query_readable_fields": ["query_id", "query_text"],
                      "query_reads_candidate_role_or_expected": False,
                      "query_ids_hide_hkp_and_s": True, "flags": [],
                      "review_scope": "MECHANICAL_SCREEN_PLUS_CONSTRUCTION_AUTHOR_NEUTRALITY_REVIEW",
                      "retrieval_quality_not_used_for_candidate_selection": True})
    print(json.dumps({"queries": len(records), "flags": 0}))


if __name__ == "__main__":
    main()
