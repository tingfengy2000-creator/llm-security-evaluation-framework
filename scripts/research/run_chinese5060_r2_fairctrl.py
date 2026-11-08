"""Owner15 bounded offline R2 experiment. Run coverage, filter, then evaluate."""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
import random
import subprocess
import sys
from collections import Counter
from pathlib import Path
from types import MethodType
from typing import Any
from zipfile import ZIP_DEFLATED, ZipFile

from llmguard.domains.retrieval.hidden_poisoning.chinese5060 import vesa_guard_v02 as v02
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.b12 import validate_packets, validate_removed
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.r2_lexical import TOOLBAR, lexical_view
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.rd_zh_tfidf import adapt_clustering_source

RUN = "W1-5060-R2-FAIRCTRL-20261108-02"
OWNER = "W1-OD-20261108-5060-R2-OFFLINE-15"
AUTH = "d89e2431a5c7a84e9a66d06c758ef45f47745f43"
UPSTREAM = "ba2a17efba165d45409114df2d70b030ade1e1b8"
MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
REV = "16e5344fbfc7dfbbbe0019d30cec21e2940cb4e1"
PAIR = "W1-5060-FAST-B-20261105-PAIR01"
P2 = "W1-5060-P2-20261104-T0-01"
ARMS = {"B2_RAW": (False, False), "RD_ZH_ONLY": (True, False),
        "RD_TEMPLATE_ONLY": (False, True), "RD_ZH_TEMPLATE": (True, True)}
TIE = "PINNED_UPSTREAM_STABLE_PAIR_AND_LOW_INDEX_TIE"
NETWORK: list[str] = []
DENIED_LOCAL_HOSTNAME: list[str] = []


def guard(event: str, _args: tuple[Any, ...]) -> None:
    if event == "socket.gethostname":
        # A local lookup triggered by an imported dependency is not an outbound operation.
        DENIED_LOCAL_HOSTNAME.append(event)
        raise PermissionError("OWNER15_LOCAL_HOSTNAME_DENIED")
    if event.startswith("socket."):
        NETWORK.append(event)
        raise PermissionError("OWNER15_OFFLINE")


def deny_evaluator_labels(event: str, args: tuple[Any, ...]) -> None:
    if event == "open" and isinstance(args[0], (str, bytes)) and Path(os.fsdecode(args[0])).name.lower() == (
        "evaluator_rows_private.json"
    ):
        raise PermissionError("ROLE_FREE_LABEL_READ_DENIED")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def read(path: Path, expected: str | None = None) -> Any:
    if path.resolve() != path:
        raise ValueError("NON_CANONICAL_INPUT_PATH")
    data = path.read_bytes()
    if expected is not None and digest(data) != expected:
        raise ValueError(f"SEALED_INPUT_HASH_MISMATCH: {path.name}")
    return json.loads(data)


def write(path: Path, value: Any) -> str:
    data = canonical(value)
    with path.open("xb") as handle:
        handle.write(data)
    return digest(data)


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(root), *args], text=True,
                                   env={**os.environ, "GIT_NO_LAZY_FETCH": "1"}).strip()


def receipts(base: Path) -> tuple[dict[str, str], dict[str, str]]:
    pair = read(base / PAIR / "PAIR_OUTPUT_SEAL.json",
                "bb775ead3d330f5e83516f8dfa871a3e2581c305e5ae7baf104500f781ac79fb")
    p2 = read(base / P2 / "OUTPUT_SEAL.json",
              "4e11d89cb6f03291c124aab28f7181622b6766cc63d55be45126023147988c52")
    if (pair["worlds"], pair["outcomes"], p2["worlds"]) != (36, 72, 36):
        raise ValueError("SEALED_DENOMINATOR_MISMATCH")
    return ({x["path"]: x["sha256"] for x in pair["records"]},
            {x["path"]: x["sha256"] for x in p2["records"]})


def inputs(base: Path) -> tuple[list[Any], list[Any], dict[str, Any]]:
    pair, p2 = receipts(base)
    def sealed(name: str) -> Any:
        return read(base / PAIR / name, pair[name])
    packets = sealed("PACKETS_PRIVATE.json")
    validate_packets(packets)
    prior = sealed("B2_RESULTS_PRIVATE.json")
    if len(prior) != 36:
        raise ValueError("MISSING_HISTORICAL_B2")
    for packet, old in zip(packets, prior, strict=True):
        wid = packet["world_id"]
        if len(wid) != 26 or not wid.startswith("w-") or any(c not in "0123456789abcdef" for c in wid[2:]):
            raise ValueError("WORLD_ID_FORMAT")
        name = f"{wid}/TOPK_PRIVATE.json"
        if p2[name] != packet["original_TopK_file_sha256"]:
            raise ValueError("TOPK_RECEIPT_MISMATCH")
        top = read(base / P2 / name, p2[name])
        if (top["world_id"] != wid or top["snapshot_hash"] != packet["snapshot_hash"]
                or old["snapshot_hash"] != packet["snapshot_hash"] or old["world_id"] != wid
                or old["status"] != "PASS" or packet["query"] != top["query_text"]
                or [(hit["rank"], hit["chunk_id"], hit["metadata"]["content_hash"]) for hit in top["hits"]]
                != [(rank, c["chunk_id"], c["content_hash"]) for rank, c in enumerate(packet["chunks"], 1)]):
            raise ValueError("TOPK_OR_RANK_CHANGED")
    return packets, prior, {
        "packets_sha256": pair["PACKETS_PRIVATE.json"], "historical_b2_sha256": pair["B2_RESULTS_PRIVATE.json"],
        "pair_output_seal_sha256": digest((base / PAIR / "PAIR_OUTPUT_SEAL.json").read_bytes()),
        "topk_output_seal_sha256": digest((base / P2 / "OUTPUT_SEAL.json").read_bytes()),
    }


def cache_identity(base: Path, upstream: Path) -> tuple[Path, dict[str, Any]]:
    pair, _ = receipts(base)
    asset = read(base / PAIR / "ASSET_MANIFEST.json", pair["ASSET_MANIFEST.json"])
    lock = read(base / PAIR / "PAIR_PRE_EXECUTION_LOCK.json", pair["PAIR_PRE_EXECUTION_LOCK.json"])
    cache = base / "assets" / "paraphrase-multilingual-MiniLM-L12-v2" / REV
    if (asset["B2_model_id"], asset["B2_revision"], lock["upstream_sha"]) != (MODEL, REV, UPSTREAM):
        raise ValueError("B2_CACHE_IDENTITY_MISMATCH")
    for row in asset["B2_files"]:
        file = cache / row["path"]
        if not file.resolve().is_relative_to(cache) or file.resolve() != file or digest(file.read_bytes()) != row["sha256"]:
            raise ValueError("B2_CACHE_ASSET_MISMATCH")
    if set(p.relative_to(cache).as_posix() for p in cache.rglob("*") if p.is_file()) != {
        row["path"] for row in asset["B2_files"]
    }:
        raise ValueError("B2_CACHE_FILE_SET_CHANGED")
    dependencies = {d.metadata["Name"]: d.version for d in importlib.metadata.distributions()}
    if dependencies != lock["dependencies"] or git(upstream, "rev-parse", "HEAD") != UPSTREAM or git(
        upstream, "status", "--porcelain"
    ):
        raise ValueError("PINNED_ENVIRONMENT_OR_UPSTREAM_CHANGED")
    return cache, {"model": MODEL, "revision": REV, "upstream": UPSTREAM,
                   "cache_identity_sha256": digest(canonical(asset["B2_files"])),
                   "dependency_sha256": digest(canonical(dependencies)), "cache_files": len(asset["B2_files"])}


def old_terms(texts: list[str]) -> tuple[list[str], int]:
    import pandas as pd
    from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer

    vectorizer = TfidfVectorizer(stop_words=list(ENGLISH_STOP_WORDS))
    matrix = vectorizer.fit_transform(texts)
    df = pd.DataFrame(matrix.todense().tolist(), columns=vectorizer.get_feature_names_out())
    terms = list(df.T.sum(axis=1).sort_values(ascending=False).index[:5])
    votes = sum(sum(term in text for term in terms) > len(terms) // 2 for text in texts)
    return terms, votes


def coverage(base: Path, out: Path, upstream: Path) -> None:
    _, identity = cache_identity(base, upstream)
    packets, prior, input_id = inputs(base)
    rows = []
    totals: Counter[str] = Counter()
    by_rank: dict[int, Counter[str]] = {r: Counter() for r in range(1, 6)}
    cross: Counter[tuple[int, int, int, int]] = Counter()
    for packet, old in zip(packets, prior, strict=True):
        chunks = packet["chunks"]
        texts = [c["text"] for c in chunks]
        terms, votes = old_terms(texts)
        if votes != old["observations"]["n_tfidf"]:
            raise ValueError("COVERAGE_HISTORICAL_TFIDF_MISMATCH")
        removed = old["removed_indices"]
        parts = []
        for rank, chunk in enumerate(chunks, 1):
            text = chunk["text"]
            classification, view, spans, unsafe = lexical_view(text)
            if unsafe:
                raise ValueError("MASK_UNSAFE_EMPTY_LEXICAL_VIEW")
            totals[classification] += 1
            by_rank[rank][classification] += 1
            disposition = "deleted" if rank - 1 in removed else "retained"
            totals[f"{disposition}_chunks"] += 1
            totals[f"{disposition}_confident"] += bool(spans)
            totals["mask_spans"] += len(spans)
            parts.append({"rank": rank, "chunk_id": chunk["chunk_id"], "original_sha256": chunk["content_hash"],
                          "lexical_sha256": digest(view.encode()), "class": classification, "spans": spans,
                          "span_sha256": digest(canonical(spans)), "unsafe": unsafe})
        masked_slices = [t[a:b] for t, part in zip(texts, parts, strict=True) for a, b in part["spans"]]
        template_positions = sum(any(term in fragment for fragment in masked_slices) for term in terms)
        totals["confident_worlds"] += bool(masked_slices)
        n_adv = old["observations"]["n_adv"]
        cross[(template_positions, votes, n_adv, len(removed))] += 1
        rows.append({"world_id": packet["world_id"], "snapshot_hash": packet["snapshot_hash"], "chunks": parts,
                     "top5_terms_private": terms, "top5_template_positions": template_positions,
                     "n_tfidf": votes, "larger_cluster": votes >= 3, "n_adv": n_adv, "deleted": len(removed)})
    lock = write(out / "MASK_ROLE_FREE_PRIVATE.json", rows)
    summary = {"worlds": 36, "chunks": 180, "unsafe": 0, "totals": dict(totals), "by_rank": by_rank,
               "cross": [{"template_positions": k[0], "n_tfidf": k[1], "larger_cluster": k[1] >= 3,
                          "n_adv": k[2], "deleted": k[3], "worlds": v} for k, v in sorted(cross.items())],
               "template_detector": "R2_GROUPED_TOOLBAR_V1",
               "span_rule_sha256": digest(TOOLBAR.pattern.encode()), "mask_sha256": lock,
               "input": input_id, "identity": identity}
    write(out / "COVERAGE_AGGREGATE.json", summary)
    print(json.dumps(summary, ensure_ascii=False))


def masked_texts(packet: dict[str, Any], mask: dict[str, Any]) -> tuple[list[str], list[str]]:
    if (packet["world_id"], packet["snapshot_hash"]) != (mask["world_id"], mask["snapshot_hash"]):
        raise ValueError("MASK_WORLD_MISMATCH")
    raw, lexical = [], []
    for chunk, part in zip(packet["chunks"], mask["chunks"], strict=True):
        text = chunk["text"]
        state, view, spans, unsafe = lexical_view(text)
        if (chunk["content_hash"], chunk["chunk_id"], state, digest(view.encode()), digest(canonical(spans)), unsafe) != (
            part["original_sha256"], part["chunk_id"], part["class"], part["lexical_sha256"],
            part["span_sha256"], 0
        ):
            raise ValueError("FROZEN_MASK_CHANGED")
        raw.append(text)
        lexical.append(view)
    return raw, lexical


def model_vectors(model: Any, texts: list[str]) -> Any:
    return model.encode(texts, convert_to_tensor=True)


def execute(base: Path, out: Path, upstream: Path) -> None:
    import numpy as np
    import torch
    from sentence_transformers import SentenceTransformer

    root = Path.cwd()
    source_commit = git(root, "rev-parse", "HEAD")
    branch = git(root, "branch", "--show-current")
    if branch != "research/paper1-chinese-defense-5060" or git(root, "status", "--porcelain"):
        raise ValueError("CLEAN_FROZEN_SOURCE_REQUIRED")
    cache, identity = cache_identity(base, upstream)
    packets, prior, input_id = inputs(base)
    cover = read(out / "COVERAGE_AGGREGATE.json")
    masks = read(out / "MASK_ROLE_FREE_PRIVATE.json", cover["mask_sha256"])
    if cover["input"] != input_id or cover["identity"] != identity or len(masks) != 36:
        raise ValueError("COVERAGE_INPUT_DRIFT")
    sys.path.insert(0, str(upstream))
    from ragdefender import RAGDefender

    original_source = (upstream / "ragdefender/grouping/clustering.py").read_bytes()
    module_scope: dict[str, Any] = {"__name__": "_rd_zh_r2_isolated"}
    exec(compile(adapt_clustering_source(original_source), "<pinned R2 lexical class>", "exec"), module_scope)
    torch.set_num_threads(2)
    random.seed(0)
    np.random.seed(0)
    torch.manual_seed(0)
    arm_config = {k: {"tokenizer": "char2_none" if v[0] else "upstream_english_default",
                     "lexical_view": "frozen_web_chrome_mask" if v[1] else "raw"} for k, v in ARMS.items()}
    frozen = {"run_id": RUN, "authorization": OWNER, "authorization_commit": AUTH, "source_commit": source_commit,
              "branch": branch, "worlds": 36, "chunks": 180, "input": input_id, "identity": identity,
              "template_detector": cover["template_detector"], "mask_sha256": cover["mask_sha256"],
              "coverage_sha256": digest((out / "COVERAGE_AGGREGATE.json").read_bytes()),
              "p": 2, "m": 5, "top_k": 5, "task": "single_hop", "cpu_threads": 2, "seed": 0,
              "tie_order": TIE, "arm_config": arm_config, "arm_config_sha256": digest(canonical(arm_config))}
    write(out / "PRE_EXECUTION_LOCK.json", frozen)
    model = SentenceTransformer(str(cache), device="cpu", local_files_only=True, trust_remote_code=False)
    defender = RAGDefender(embedder=model, task_type="single_hop", device="cpu", p=2, m=5)
    clustering = defender._clustering
    original_vote = clustering._n_tfidf
    char_vote = MethodType(module_scope["ClusteringBasedGrouping"]._n_tfidf, clustering)
    worlds = []
    replay = []
    for packet, old, mask in zip(packets, prior, masks, strict=True):
        raw, lexical = masked_texts(packet, mask)
        embedding = model_vectors(model, raw)
        ehash = digest(embedding.cpu().detach().numpy().tobytes())
        worlds.append((raw, lexical, embedding, ehash))
        row = filter_one(defender, original_vote, raw, raw, embedding, ehash)
        replay.append(row)
        if (row["n_tfidf"], row["n_adv"], row["deleted_indices"]) != (
            old["observations"]["n_tfidf"], old["observations"]["n_adv"], old["removed_indices"]
        ):
            write(out / "B2_REPLAY_FAILURE_PRIVATE.json", {"passed_prefix": len(replay) - 1, "observed": row,
                  "expected_n_tfidf": old["observations"]["n_tfidf"], "expected_n_adv": old["observations"]["n_adv"],
                  "expected_indices": old["removed_indices"]})
            raise ValueError("B2_RAW_REPLAY_MISMATCH")
    write(out / "B2_REPLAY_PRIVATE.json", replay)
    rows = []
    for index, (raw, lexical, embedding, ehash) in enumerate(worlds):
        outputs = {"B2_RAW": replay[index]}
        for name, (char, masked) in list(ARMS.items())[1:]:
            try:
                outputs[name] = filter_one(defender, char_vote if char else original_vote, raw,
                                           lexical if masked else raw, embedding, ehash)
            except ValueError as exc:
                raise ValueError(f"ARM_FAILED_OR_EMPTY_VOCABULARY: {name}") from exc
        repeat = {name: filter_one(defender, char_vote if char else original_vote, raw,
                                  lexical if masked else raw, embedding, ehash)
                  for name, (char, masked) in ARMS.items()}
        if outputs != repeat:
            raise ValueError("DETERMINISTIC_REPLAY_MISMATCH")
        for output in outputs.values():
            output["b2_delete_set_flip"] = output["deleted_indices"] != replay[index]["deleted_indices"]
            output["b2_delete_set_symmetric_difference"] = sorted(
                set(output["deleted_indices"]) ^ set(replay[index]["deleted_indices"]))
        rows.append({"world_id": packets[index]["world_id"], "snapshot_hash": packets[index]["snapshot_hash"],
                     "arms": outputs})
    if NETWORK:
        raise ValueError("UNEXPECTED_NETWORK_ATTEMPT")
    output_hash = write(out / "FOUR_ARM_ROLE_FREE_PRIVATE.json", rows)
    run = {**frozen, "status": "ROLE_FREE_SEALED", "role_free_output_sha256": output_hash,
           "b2_replay_worlds": len(replay), "deterministic_repeat_outcomes": len(rows) * 4,
           "encoder_calls": len(worlds), "new_retrieval": 0, "api_calls": 0, "downloads": 0, "new_network_assets": 0,
           "cost_usd": 0, "denied_local_hostname_calls": len(DENIED_LOCAL_HOSTNAME), "human_gold": 0, "formal_asr": "NOT_MEASURED", "formal_accuracy": "NOT_MEASURED"}
    write(out / "ROLE_FREE_MANIFEST.json", run)
    names = ("FOUR_ARM_ROLE_FREE_PRIVATE.json", "ROLE_FREE_MANIFEST.json", "B2_REPLAY_PRIVATE.json",
             "PRE_EXECUTION_LOCK.json", "MASK_ROLE_FREE_PRIVATE.json", "COVERAGE_AGGREGATE.json")
    archive = out / "ROLE_FREE_EVIDENCE_PRIVATE.zip"
    with ZipFile(archive, "x", compression=ZIP_DEFLATED) as z:
        for name in names:
            z.write(out / name, name)
    with ZipFile(archive) as z:
        if z.testzip() is not None:
            raise ValueError("ROLE_FREE_ARCHIVE_CORRUPTED")
    write(out / "ROLE_FREE_SEAL.json", {"archive_sha256": digest(archive.read_bytes()), "members": {
        n: digest((out / n).read_bytes()) for n in names}})
    print(json.dumps({"b2_replay": len(replay), "outcomes": len(rows) * 4, "encoder_calls": len(worlds),
                      "role_free_archive_sha256": digest(archive.read_bytes())}))


def filter_one(defender: Any, vote: Any, raw: list[str], lexical: list[str], embedding: Any, ehash: str) -> dict[str, Any]:
    raw_hash = digest(canonical(raw))
    original = defender._clustering._n_tfidf
    votes = int(vote(lexical))
    observation: dict[str, Any] = {}

    def bind(texts: list[str]) -> int:
        if texts is not raw:
            raise ValueError("CLUSTERING_INPUT_CHANGED")
        return votes

    def trace(frame: Any, event: str, value: Any) -> None:
        owner = frame.f_locals.get("self")
        if owner is defender._identify and frame.f_code.co_name == "select":
            if frame.f_locals["R"] is not raw or frame.f_locals["embeddings"] is not embedding:
                raise ValueError("STAGE2_INPUT_CHANGED")
            if event == "return" and value is not None:
                observation["scores"] = frame.f_locals["f"]

    defender._clustering._n_tfidf = bind
    try:
        n_adv = defender._clustering.estimate_n_adv(raw, embeddings=embedding)
        sys.setprofile(trace)
        try:
            removed = sorted(defender._identify.select(raw, n_adv, embeddings=embedding))
        finally:
            sys.setprofile(None)
    finally:
        defender._clustering._n_tfidf = original
    retained = [i for i in range(len(raw)) if i not in removed]
    context = [raw[i] for i in retained]
    validate_removed(raw, context, removed)
    if len(observation["scores"]) != 5 or digest(canonical(raw)) != raw_hash or digest(
        embedding.cpu().detach().numpy().tobytes()
    ) != ehash:
        raise ValueError("RAW_OR_SHARED_EMBEDDING_CHANGED")
    scores = observation["scores"]
    return {"n_tfidf": votes, "larger_cluster": votes >= 3, "n_adv": n_adv,
            "deleted_indices": removed, "retained_indices": retained, "deleted_count": len(removed),
            "stage2_scores": scores, "stage2_tied_score_pairs": sum(
                scores[i] == scores[j] for i in range(5) for j in range(i + 1, 5)),
            "original_text_sha256": raw_hash, "stage2_embeddings_sha256": ehash,
            "lexical_sha256": digest(canonical(lexical)), "projected_generator_context_sha256": digest(canonical(context))}


def evaluate(base: Path, out: Path) -> None:
    seal = read(out / "ROLE_FREE_SEAL.json")
    archive = out / "ROLE_FREE_EVIDENCE_PRIVATE.zip"
    if digest(archive.read_bytes()) != seal["archive_sha256"]:
        raise ValueError("ROLE_FREE_ARCHIVE_CHANGED")
    with ZipFile(archive) as z:
        if set(z.namelist()) != set(seal["members"]) or any(
            digest(z.read(n)) != h or digest((out / n).read_bytes()) != h for n, h in seal["members"].items()
        ):
            raise ValueError("ROLE_FREE_SEAL_FAILED")
    packets, _, _ = inputs(base)
    rows = read(out / "FOUR_ARM_ROLE_FREE_PRIVATE.json", seal["members"]["FOUR_ARM_ROLE_FREE_PRIVATE.json"])
    _, p2 = receipts(base)
    labels_path = "EVALUATOR_ROWS_PRIVATE.json"
    labels = read(base / P2 / labels_path, p2[labels_path])
    label_by_world = {r["world_id"]: r for r in labels}
    arm_counts: dict[str, Any] = {}
    paired = {name: Counter[str]() for name in ARMS}
    masks = read(out / "MASK_ROLE_FREE_PRIVATE.json", seal["members"]["MASK_ROLE_FREE_PRIVATE.json"])
    for name in ARMS:
        roles = {r: Counter[str]() for r in ("POISON", "CLEAN_CURRENT", "HARD_NEGATIVE")}
        totals: Counter[str] = Counter()
        n_tfidf: Counter[int] = Counter()
        n_adv: Counter[int] = Counter()
        for packet, row, mask in zip(packets, rows, masks, strict=True):
            if (packet["world_id"], packet["snapshot_hash"]) != (row["world_id"], row["snapshot_hash"]):
                raise ValueError("EVALUATOR_WORLD_MISMATCH")
            label = label_by_world[row["world_id"]]
            counts = roles[label["role_evaluation_only"]]
            arm = row["arms"][name]
            ranks = {r - 1 for r in label["candidate_ranks"]}
            deleted = set(arm["deleted_indices"])
            old = set(row["arms"]["B2_RAW"]["deleted_indices"])
            scope = v02.query_scope(packet["query"])
            scoped = [{(slot, fact.unit, fact.qualifier, fact.value) for fact in v02.extract(c["text"])
                       if (slot := v02._slot(fact, scope)) is not None} for c in packet["chunks"]]
            kept = set().union(*(scoped[i] for i in arm["retained_indices"]))
            totals["unique_scope_retained_worlds"] += len(kept) == 1
            totals["scope_bound_deleted_chunks"] += sum(bool(scoped[i]) for i in deleted)
            comparable = sum(any(v[:3] == k[:3] for v in scoped[i] for k in kept) for i in ranks & deleted)
            counts["scope_comparable_deleted_candidate"] += comparable
            totals["scope_comparable_deleted_candidates"] += comparable
            counts["worlds"] += 1
            counts["hit"] += bool(ranks)
            counts["miss"] += not ranks
            counts["deleted"] += bool(ranks & deleted)
            counts["retained"] += bool(ranks - deleted)
            counts["newly_retained_vs_b2"] += bool(ranks & old and not ranks & deleted)
            counts["newly_deleted_vs_b2"] += bool(ranks & deleted and not ranks & old)
            counts["hit_with_confident_template"] += any(mask["chunks"][i]["spans"] for i in ranks)
            totals["deleted_chunks"] += len(deleted)
            totals["any_deletion_worlds"] += bool(deleted)
            totals["changed_vs_b2"] += deleted != old
            paired[name]["vs_rd_zh_only_changed_worlds"] += deleted != set(row["arms"]["RD_ZH_ONLY"]["deleted_indices"])
            paired[name]["vs_b2_chunks_restored"] += len(old - deleted)
            paired[name]["vs_b2_chunks_newly_deleted"] += len(deleted - old)
            n_adv[arm["n_adv"]] += 1
            n_tfidf[arm["n_tfidf"]] += 1
        if [roles[k]["hit"] for k in roles] != [10, 10, 9]:
            raise ValueError("EVALUATOR_DENOMINATOR_CHANGED")
        arm_counts[name] = {"roles": roles, "totals": totals, "n_adv": n_adv, "n_tfidf": n_tfidf,
                            "paired": paired[name]}
    clean = arm_counts["RD_ZH_TEMPLATE"]["roles"]["CLEAN_CURRENT"]["deleted"]
    base_totals = arm_counts["B2_RAW"]["totals"]
    joint = arm_counts["RD_ZH_TEMPLATE"]
    pool = max(base_totals["scope_comparable_deleted_candidates"], joint["totals"]["scope_comparable_deleted_candidates"])
    poison_release = joint["roles"]["POISON"]["newly_retained_vs_b2"]
    if clean <= 2 and (base_totals["unique_scope_retained_worlds"] <= 1 or base_totals["scope_bound_deleted_chunks"] == 0):
        k1 = "K1-A / D1_DIAGNOSTIC_ONLY"
    elif clean >= 3 and pool > 0 and poison_release == 0:
        k1 = "K1-B / D1_EXPLORATORY_METHOD"
    else:
        k1 = "K1-C / INSUFFICIENT_OR_MIXED"
    summary = {"status": "EVALUATED_SEALED_OUTPUTS", "run_id": RUN, "worlds": 36, "chunks": 180,
               "candidate_hit": 29, "candidate_miss": 7, "arms": arm_counts, "k1": k1,
               "role_free_archive_sha256": seal["archive_sha256"], "candidate_labels_sha256": p2[labels_path]}
    ev_sha = write(out / "EVALUATOR_AGGREGATE.json", summary)
    run = read(out / "ROLE_FREE_MANIFEST.json", seal["members"]["ROLE_FREE_MANIFEST.json"])
    write(out / "RUN_MANIFEST.json", {**run, "status": "R2_BOUNDED_OFFLINE_COMPLETE",
          "role_free_archive_sha256": seal["archive_sha256"], "evaluator_output_sha256": ev_sha,
          "K1": k1, "auto_continue": False})
    print(json.dumps(summary, ensure_ascii=False))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("coverage", "filter", "evaluate"))
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--upstream", type=Path, required=True)
    args = parser.parse_args()
    base, upstream = args.base.resolve(), args.upstream.resolve()
    out = base / RUN
    if base.drive.upper() not in {"D:", "E:"} or not out.is_dir() or out.resolve() != out:
        raise ValueError("PRIVATE_OUTPUT_LOCATION")
    sys.addaudithook(guard)
    if args.stage != "evaluate":
        sys.addaudithook(deny_evaluator_labels)
    try:
        if args.stage == "coverage":
            coverage(base, out, upstream)
        elif args.stage == "filter":
            execute(base, out, upstream)
        else:
            evaluate(base, out)
    except Exception as exc:
        write(out / f"STOP_{args.stage}.json", {"status": "HUMAN_DECISION_REQUIRED",
              "auto_continue": False, "exception_type": type(exc).__name__, "message": str(exc),
              "network_attempts": NETWORK})
        raise


if __name__ == "__main__":
    main()
