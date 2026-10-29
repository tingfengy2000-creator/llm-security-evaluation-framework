"""CONTROL PLANE only: construct a private runtime/evaluator-separated input ZIP.

Never publishes the bundle or raw data to Git. Oracle mapping is projected into
the explicitly approved Oracle condition; labels go in a separate evaluator file.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path
from typing import Any

from llmguard.domains.retrieval.hidden_poisoning.method_engineering.llm_verification import check_row, sha_text


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def read(p: Path) -> Any:
    return json.loads(p.read_text("utf-8"))


def lines(p: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in p.read_text("utf-8").splitlines()]


def jl(p: Path, value: list[dict[str, Any]]) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("x", encoding="utf-8", newline="\n") as f:
        for row in value:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def prepare(args: argparse.Namespace) -> None:
    root, output = args.repo.resolve(), args.output.resolve()
    assert not output.exists(), "NEW_NAMESPACE_REQUIRED"
    first = root / "experiments/core144_d1_first_detection_20261028_run01"
    engineering = root / "experiments/core144_d1_quality_sept_20261027"
    vace = root / "experiments/vace_v03_f5_20261028_run01"
    candidates_path = first / "input/CANDIDATES_ONLY_V1.jsonl"
    assert sha(candidates_path) == "6be97906cb9de7587491e84e4c13131a22f93e07b87336772c913534dc7e79e2"
    assert read(first / "qualification/OWNER_QUALIFICATION_ACCEPTANCE_V1.json")["Owner_signed"]
    candidates = lines(candidates_path)
    assert len(candidates) == 120
    docs = {d["evidence_doc_id"]: d for d in lines(vace / "RUNTIME_CORPUS_WHITELIST_V1.jsonl")}
    meta = read(vace / "RUNTIME_REGISTRY_WHITELIST_V1.json")
    retrieved = {r["candidate_id"]: r["retrieval_top5"] for r in lines(vace / "VACE_V03_D1_PREDICTIONS.jsonl") if r["condition"] == "V03-F5"}
    reference: dict[tuple[str, str], dict[str, Any]] = {(r["candidate_id"], r["slot"]): r for r in lines(engineering / "engineering/ORACLE_REFERENCE_POST_RETRIEVAL_LOCK_V1.jsonl")}
    visible = {r["candidate_id"]: r for r in read(engineering / "quality/SEMANTIC_VISIBLE_ROWS_V1.json")}

    def project(uid: str, text: str) -> dict[str, Any]:
        m = meta[uid]
        return {"uid": uid + ":" + sha_text(text)[:16], "document_uid": uid, "title": docs[uid]["title"], "official_url": docs[uid]["official_url"], "text": text, "text_sha256": sha_text(text), "metadata": {k: m.get(k) for k in ("issuer", "publisher", "publication_date", "effective_start", "effective_end", "current_history_role")} | {"version_id": docs[uid].get("version_id"), "source_host": docs[uid].get("source_host")}}

    f5: list[dict[str, Any]] = []
    oracle: list[dict[str, Any]] = []
    for c in candidates:
        sid = c["candidate_id"]
        ranked = sorted(retrieved[sid], key=lambda r: r["rank"])
        assert len(ranked) == 5
        external = [project(r["evidence_doc_id"], docs[r["evidence_doc_id"]]["snapshot_text"]) for r in ranked]
        matched: list[dict[str, Any]] = []
        for slot in ("E1", "E2"):
            if (sid, slot) not in reference:
                assert not (visible[sid]["assigned_evidence"][slot].get("text") or "").strip(), "NONEMPTY_ORACLE_SLOT_WITHOUT_FROZEN_IDENTITY"
                continue
            ref = reference[(sid, slot)]
            text = visible[sid]["assigned_evidence"][slot]["text"]
            assert sha_text(text) == ref["assigned_text_sha256"]
            item = project(ref["evidence_doc_id"], text)
            if item["uid"] not in {d["uid"] for d in matched}:
                matched.append(item)
        for target, evidence in ((f5, external), (oracle, matched)):
            row = {**c, "evidence": evidence}
            check_row(row)
            target.append(row)
    jl(output / "runtime/f5.jsonl", f5)
    jl(output / "runtime/oracle.jsonl", oracle)
    # Evaluation data are not opened by inference; target comes from signed
    # Human/Owner development vault, NOT construction role inference.
    targets = {r["candidate_id"]: r["target"] for r in lines(first / "input/TRAINING_TARGET_VAULT_V1.jsonl")}
    split = {r["candidate_id"]: r for r in lines(first / "input/SPLIT_ONLY_METADATA_V1.jsonl")}
    s = {r["group_id"]: r["derived_s"] for r in read(first / "qualification/APPROVED_S_PATHS_V1.json")}
    qa = {r["candidate_id"]: r for r in read(engineering / "quality/ALL144_PROPOSED_DEVELOPMENT_VIEW_NOT_GT_V1.json")}
    labels = []
    for c in candidates:
        sid = c["candidate_id"]
        labels.append({"candidate_id": sid, "label": targets[sid], "role_evaluation_only": qa[sid]["construction_role_control_only"], "group_evaluation_only": split[sid]["group_id"], "family_evaluation_only": split[sid]["family"], "derived_s_evaluation_only": s[split[sid]["group_id"]], "human_approved_status_evaluation_only": qa[sid]["proposed_fields_not_GT"]["overall_fact_status"]})
    jl(output / "evaluation/labels.jsonl", labels)
    historical = read(root / "experiments/vace_lite_r1_20261028_run01/SAME120_HISTORICAL_COMPARISON_V1.json")
    (output / "evaluation/history.json").write_text(json.dumps(historical, ensure_ascii=False, indent=2), "utf-8")
    prior = [{"candidate_id": p["candidate_id"], "verdict": p["verdict"]} for p in lines(vace / "VACE_V03_D1_PREDICTIONS.jsonl") if p["condition"] == "V03-F5"]
    jl(output / "evaluation/v03_predictions.jsonl", prior)
    files = [{"path": p.relative_to(output).as_posix(), "bytes": p.stat().st_size, "sha256": sha(p)} for p in sorted(output.rglob("*")) if p.is_file()]
    manifest = {"task": "P1-VACE-L0-F5-ORACLE-STRONG-BASELINE-01", "bundle_version": 2, "groups": 40, "candidates": 120, "families": 13, "holds_groups": 8, "holds_candidates": 24, "candidate_original_sha256": sha(candidates_path), "source_signed_acceptance_sha256": sha(first / "qualification/OWNER_QUALIFICATION_ACCEPTANCE_V1.json"), "source_human_owner_target_vault_sha256": sha(first / "input/TRAINING_TARGET_VAULT_V1.jsonl"), "source_approved_minimum_evidence_paths_sha256": sha(first / "qualification/APPROVED_S_PATHS_V1.json"), "source_family_mapping_sha256": sha(first / "input/SPLIT_ONLY_METADATA_V1.jsonl"), "source_vace_prediction_lock": sha(vace / "PREDICTION_LOCK_V1.json"), "source_oracle_reference_sha256": sha(engineering / "engineering/ORACLE_REFERENCE_POST_RETRIEVAL_LOCK_V1.jsonl"), "oracle_body_policy": "EXACT_FROZEN_ASSIGNED_E1_E2_TEXT_NOT_RECONSTRUCTED_FULL_DOCUMENT", "f5_body_policy": "EXACT_EXISTING_HYBRID_TOP5_FULL_SNAPSHOT", "private_data_not_for_git": True, "files": files}
    (output / "BUNDLE_MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), "utf-8")
    zip_path = output.with_suffix(".zip")
    with zipfile.ZipFile(zip_path, "x", zipfile.ZIP_DEFLATED) as archive:
        for p in sorted(output.rglob("*")):
            if p.is_file():
                archive.write(p, p.relative_to(output).as_posix())
    print(json.dumps({"bundle": str(zip_path), "sha256": sha(zip_path), "bytes": zip_path.stat().st_size, "manifest_sha256": sha(output / "BUNDLE_MANIFEST.json")}, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, required=True)
    prepare(parser.parse_args())
