"""Create additive private evidence/QA dossier for the D1 90-row MegaWave.

All outputs contain construction-only information and MUST NOT be sent to reviewers.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from formal240_d1_remaining90_megawave_audit import FILES, FORMAL, sha


IDENTITY = {
    "HKP2": "PAPER1_FORMAL_D1_HKP2_PRECONSTRUCTION_EVIDENCE_IDENTITY_AUDIT_V1.json",
    "HKP3": "PAPER1_FORMAL_D1_HKP3_PRECONSTRUCTION_EVIDENCE_IDENTITY_AUDIT_V2.json",
    "HKP4": "PAPER1_FORMAL_D1_HKP4_PRECONSTRUCTION_AUTHORITY_EVIDENCE_AUDIT_V1.json",
}
STEMS = {
    "GROUP_MANIFEST": "group_manifest",
    "EVIDENCE_MANIFEST": "evidence_manifest",
    "FACT_ATOM_AUDIT": "fact_atom_audit",
    "METADATA_AUDIT": "metadata_audit",
    "VIEW_READINESS": "view_readiness",
    "MISSINGNESS_AUDIT": "missingness_audit",
    "TRIPLET_PARITY": "triplet_parity",
    "QUERY_AUDIT": "query_audit",
    "RETRIEVAL_SMOKE": "retrieval_smoke",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    for hkp in ("hkp2", "hkp3", "hkp4"):
        parser.add_argument(f"--{hkp}-root", required=True, type=Path)
    parser.add_argument("--audit", required=True, type=Path)
    parser.add_argument("--output-root", required=True, type=Path)
    args = parser.parse_args()
    audit = load(args.audit)
    if audit["status"] != "REMAINING90_INTERNAL_CROSS_BATCH_GATE_PASS_EXTERNAL_REVIEW_PENDING":
        raise ValueError("Cross-batch audit not passed")
    if args.output_root.exists():
        raise ValueError("Refusing to overwrite private dossier")
    roots = {h.upper(): getattr(args, f"{h}_root") for h in ("hkp2", "hkp3", "hkp4")}
    gathered: dict[str, list[dict[str, Any]]] = {key: [] for key in STEMS}
    evidence: dict[tuple[str, str], dict[str, Any]] = {}
    all_ids: list[str] = []
    for hkp, root in roots.items():
        names = FILES[hkp]
        candidate_path, atom_path, mech_path = (root / name for name in names[:3])
        precontract_path = FORMAL / names[3]
        identity_path = root / IDENTITY[hkp]
        expected = audit["source_artifact_hashes"][hkp]
        for label, path in (
            ("candidate_sha256", candidate_path),
            ("atom_qa_sha256", atom_path),
            ("mechanical_qa_sha256", mech_path),
            ("precontract_sha256", precontract_path),
        ):
            if sha(path) != expected[label]:
                raise ValueError(f"Audit lineage drift: {hkp} {label}")
        candidates = [json.loads(line) for line in candidate_path.read_text(encoding="utf-8").splitlines()]
        atom = load(atom_path)
        mech = load(mech_path)
        pre = load(precontract_path)
        identity = load(identity_path)
        if atom["errors"] or mech["errors"] or identity["errors"]:
            raise ValueError(f"Internal QA failed: {hkp}")
        candidate_by_group: dict[str, list[str]] = {}
        for row in candidates:
            candidate_by_group.setdefault(row["group_slot_id"], []).append(row["sample_id"])
            all_ids.append(row["sample_id"])
        for group in pre["groups"]:
            gathered["GROUP_MANIFEST"].append({"hkp": hkp, **group, "candidate_sample_ids": candidate_by_group[group["group_slot_id"]]})
            gathered["QUERY_AUDIT"].append({"hkp": hkp, "group_slot_id": group["group_slot_id"], "neutral_query": group.get("neutral_query") or candidates[next(i for i, r in enumerate(candidates) if r["group_slot_id"] == group["group_slot_id"])]["neutral_query"], "evidence_refs": group["evidence_refs"]})
        for evidence_id, source in identity["sources"].items():
            path = Path(source["path"])
            if not path.is_file() or sha(path) != source["sha256"]:
                raise ValueError(f"Official source byte mismatch: {hkp} {evidence_id}")
            url = source.get("official_url") or source.get("url")
            key = (url, source["sha256"])
            if key not in evidence:
                evidence[key] = {"official_url": url, "sha256": source["sha256"], "private_snapshot_path": str(path), "aliases": []}
            evidence[key]["aliases"].append({"hkp": hkp, "evidence_id": evidence_id})
        gathered["FACT_ATOM_AUDIT"].extend({"hkp": hkp, **row} for row in atom["atom_rows"])
        gathered["METADATA_AUDIT"].append({"hkp": hkp, "source_identity_audit_path": str(identity_path), "source_identity_audit_sha256": sha(identity_path), "source_identity_status": identity["status"], "source_count": len(identity["sources"]), "mechanical_limits": mech.get("authority_limitation") or mech.get("boundary")})
        gathered["VIEW_READINESS"].extend({"hkp": hkp, **row} for row in mech["view_readiness"])
        gathered["MISSINGNESS_AUDIT"].append({"hkp": hkp, "by_role": mech["missingness_by_role"]})
        gathered["TRIPLET_PARITY"].append({"hkp": hkp, "mechanical": mech["triplet_surface_parity"], "construction": atom["triplet_parity"]})
        gathered["RETRIEVAL_SMOKE"].append({"hkp": hkp, "fixed_engineering_smoke_not_effectiveness": mech["retrieval_smoke"]})
    if len(all_ids) != 90 or len(set(all_ids)) != 90 or len(gathered["GROUP_MANIFEST"]) != 30:
        raise ValueError("Dossier population mismatch")
    gathered["EVIDENCE_MANIFEST"] = list(evidence.values())
    args.output_root.mkdir(parents=True, exist_ok=False)
    for name, stem in STEMS.items():
        value = {
            "status": "PRIVATE_CONSTRUCTION_SIDE_NOT_REVIEWER_MATERIAL",
            "cross_batch_audit_sha256": sha(args.audit),
            "record_count": len(gathered[name]),
            "records": gathered[name],
        }
        output = args.output_root / f"PAPER1_FORMAL_D1_REMAINING90_{name}_V1.json"
        output.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("D1_REMAINING90_PRIVATE_DOSSIER_COMPLETE", len(gathered["GROUP_MANIFEST"]), len(gathered["EVIDENCE_MANIFEST"]), dict(Counter(r["hkp"] for r in gathered["GROUP_MANIFEST"])))


if __name__ == "__main__":
    main()
