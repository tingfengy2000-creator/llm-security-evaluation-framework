"""One-shot blind Owner33 replay through the pinned Owner28 retrieval backend."""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import date
from hashlib import sha256
import json
import re
import shutil
import time
from pathlib import Path
from types import SimpleNamespace
from typing import Any
from urllib.parse import urlsplit

import run_chinese5060_owner28 as backend
from llmguard.domains.retrieval.hidden_poisoning.chinese5060 import (
    owner33_vcare as vcare,
)
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.owner28_benchmark import (
    exact_keys,
    hash_string,
    parse_json,
    write_once,
)
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.owner31_qcer import Query

BASE = Path("experiments/paper1_chinese5060")


def digest(raw: bytes) -> str:
    return sha256(raw).hexdigest()


def fail_unless(ok: object, code: str) -> None:
    if not ok:
        raise ValueError(code)


REMOTE = "11242cc6613a0ec3f53332255d0e19de941273a3"
FROZEN = "11880c5be71e22d73217c32e0c779fbf8b117741"
SOURCE_SHA = "fc8c14e14d82f97bc76849609d661ef29691a46a1855de423bd4804227d90bd2"
HANDOFF = "docs/paper1/dual_machine/repro5090/owner33_eval/"
DEV_MANIFEST = (
    "docs/paper1/dual_machine/chinese5060/OWNER33_VCARE_DEV_RUN_MANIFEST.json"
)
OWNER28_RUNNER = "scripts/research/run_chinese5060_owner28.py"
FROZEN_FILES = {
    "vcare": "src/llmguard/domains/retrieval/hidden_poisoning/chinese5060/owner33_vcare.py",
    "qcer": "src/llmguard/domains/retrieval/hidden_poisoning/chinese5060/owner31_qcer.py",
    "numeric": "src/llmguard/domains/retrieval/hidden_poisoning/chinese5060/owner30_auto_eval.py",
    "schema": "src/llmguard/domains/retrieval/hidden_poisoning/chinese5060/owner28_benchmark.py",
    "runner": OWNER28_RUNNER,
}
DATE_PREFIX = re.compile(r"^(\d{4}-\d{2}-\d{2})当天，限于")
EXCLUDED = {
    "STATUTORY_HOLIDAYS",
    "PUBLIC_HYGIENE",
    "DRIVING_LICENSE",
    "BASIC_DRUG_CATALOG",
    "POPULATION_FAMILY_PLANNING_LAW",
    "STATE_COUNCIL_WORK_TIME",
    "PATENT_LAW",
    "COMPANY_CAPITAL_PERIOD",
    "TRADEMARK_STATUTORY_DAMAGES",
    "WORK_INJURY_LUMP_SUM",
    "ACCOUNTING_LAW_FINE",
}


def read_remote(name: str) -> tuple[bytes, Any]:
    raw = backend.git("show", f"{REMOTE}:{HANDOFF}{name}")
    return raw, parse_json(raw)


def admit() -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    fail_unless(
        backend.git("branch", "--show-current").decode().strip()
        == "research/paper1-chinese-defense-5060",
        "BRANCH",
    )
    dev_raw = backend.git("show", f"{FROZEN}:{DEV_MANIFEST}")
    dev = parse_json(dev_raw)
    fail_unless(all(dev["dev"]["gates"].values()), "DEV_NOT_GO")
    for key, path in FROZEN_FILES.items():
        local = Path(path).read_bytes()
        pinned = backend.git("show", f"{FROZEN}:{path}")
        if key == "schema":
            local, pinned = (b.replace(b"\r\n", b"\n") for b in (local, pinned))
        fail_unless(local == pinned, "FROZEN_RUNTIME_BYTES")
    fail_unless(
        digest(Path(vcare.__file__).read_bytes())
        == SOURCE_SHA
        == dev["freeze"]["model_sha256"],
        "FROZEN_METHOD_DRIFT",
    )
    fail_unless(vcare.CONFIG == dev["freeze"]["config"], "FROZEN_PARAMETER_DRIFT")
    raw_m, m = read_remote("OWNER33_PRESEAL_MANIFEST.json")
    raw_s, source = read_remote("OWNER33_SOURCE_SNAPSHOT.json")
    raw_l, selection = read_remote("OWNER33_SELECTION_LOG.json")
    raw_w, pack = read_remote("OWNER33_ROLE_FREE.json")
    fail_unless(
        m["method_freeze_commit"] == FROZEN
        and m["vcare_source_sha256"] == SOURCE_SHA
        and m["dev_run_manifest_sha256"] == digest(dev_raw)
        and m["parameter_freeze_sha256"] == dev["dev"]["freeze_sha256"]
        and m["dev_index_sha256"] == dev["freeze"]["index_sha256"]
        and m["status"] == "FRESH_SOURCE_PRESEALED"
        and m["prediction_authorized"] is True
        and m["frozen_before_fact_selection"] is True
        and m["human_gold"] == 0
        and m["worlds"] == 32
        and m["fact_units"] == 4
        and m["passage_count"] == 352,
        "PRESEAL",
    )
    for key, raw in (
        ("source_snapshot_sha256", raw_s),
        ("selection_log_sha256", raw_l),
        ("role_free_sha256", raw_w),
    ):
        fail_unless(digest(raw) == m[key], "HANDOFF_SHA_DRIFT")
    fail_unless(
        source["frozen_before_fact_selection"] is True
        and source["full_body_retained"] is False
        and selection["source_snapshot_sha256"] == digest(raw_s),
        "SOURCE_ORDER",
    )
    ranked = sorted(
        selection["qualified_fact_keys"],
        key=lambda k: digest(raw_s + b"\n" + k.encode()),
    )
    fail_unless(
        ranked == selection["ranked_fact_keys"]
        and ranked[:4] == selection["selected_fact_keys"]
        and len(ranked) == 4,
        "SELECTION_REPLAY",
    )
    records = source["records"]
    verified = [
        r
        for r in records
        if r.get("http_status") == 200 and r["selection_status"] != "EXCLUDED"
    ]
    new_catalog = [r for r in records if r["lineage_id"] not in EXCLUDED]
    qualified = [r for r in verified if r["selection_status"] == "QUALIFIED_FACT_INPUT"]
    fail_unless(
        len({r["lineage_id"] for r in new_catalog}) == m["new_lineages_in_catalog"] >= 6
        and len({r["issuer_family"] for r in new_catalog}) >= 3
        and len({r["lineage_id"] for r in qualified}) == 4
        and not {r["lineage_id"] for r in verified} & EXCLUDED,
        "LINEAGE_ISOLATION",
    )
    for r in verified:
        hash_string(r["access_sha256"])
        u = urlsplit(r["final_url"])
        fail_unless(
            u.scheme == "https"
            and u.hostname is not None
            and u.hostname.endswith(".gov.cn")
            and u.username is None
            and r["tls"] == "DEFAULT_CONTEXT_VERIFIED"
            and r["body_retained"] is False,
            "SOURCE_RIGHTS_OR_TLS",
        )
    exact_keys(pack, {"schema", "human_gold", "text_status", "worlds"})
    fail_unless(
        pack["schema"] == "OWNER33_EVAL_ROLE_FREE_V1"
        and pack["human_gold"] == 0
        and pack["text_status"] == "SELF_AUTHORED_SOURCE_GROUNDED_PARAPHRASE"
        and len(pack["worlds"]) == 32,
        "ROLE_FREE_SHAPE",
    )
    worlds, seen_worlds, seen_passages = [], set(), set()
    for row in pack["worlds"]:
        exact_keys(row, {"world_id", "query", "passages"})
        fail_unless(re.fullmatch(r"w-[a-f0-9]{20}", row["world_id"]), "WORLD_UID")
        fail_unless(
            row["world_id"] not in seen_worlds and len(row["passages"]) == 11,
            "WORLD_DUPLICATE_OR_DENOMINATOR",
        )
        seen_worlds.add(row["world_id"])
        match = DATE_PREFIX.match(row["query"])
        if not match or date.fromisoformat(match[1]).isoformat() != match[1]:
            raise ValueError("EVENT_DATE_NOT_EXPLICIT")
        # No semantic scope extraction is added after freeze. The exact question is
        # supplied as the visible subject and ask; no hidden IDs enter the detector.
        q = Query(row["query"], match[1], "", row["query"], row["query"])
        docs = []
        for passage in row["passages"]:
            exact_keys(passage, {"passage_id", "text"})
            fail_unless(
                re.fullmatch(r"p-[a-f0-9]{20}", passage["passage_id"]), "PASSAGE_UID"
            )
            fail_unless(
                passage["passage_id"] not in seen_passages
                and isinstance(passage["text"], str)
                and 1 <= len(passage["text"]) <= 8192,
                "PASSAGE_SHAPE",
            )
            seen_passages.add(passage["passage_id"])
            # The role-free passage ID is the original parent ID. Only the opaque
            # source alias is generated for the existing vectorstore metadata schema.
            docs.append(
                {
                    "document_id": passage["passage_id"],
                    "source_id": "s-" + passage["passage_id"][2:],
                    "source_uri": None,
                    "text": passage["text"],
                    "content_sha256": digest(passage["text"].encode()),
                }
            )
        worlds.append(
            {
                "world_id": row["world_id"],
                "event_date": q.event_date,
                "query_text": q.text,
                "query": q,
                "documents": docs,
            }
        )
    fail_unless(
        len(seen_passages) == 352 and len(seen_worlds) == 32, "TOTAL_DENOMINATOR"
    )
    query_groups = Counter(DATE_PREFIX.sub("", w["query_text"]) for w in worlds)
    fail_unless(
        len(query_groups) == 4 and set(query_groups.values()) == {8}, "FOUR_FACT_GROUPS"
    )
    typed_keys = {
        "entity",
        "attribute",
        "scope",
        "value",
        "effective_from",
        "effective_to_exclusive",
        "evidence_sha256",
    }
    recognized = sum(vcare.intent(w["query"]) is not None for w in worlds)
    fail_unless(
        recognized == 0 or all(typed_keys <= set(x) for x in verified),
        "FROZEN_INDEX_SCHEMA_UNSUPPORTED",
    )
    receipt = {
        "worlds": 32,
        "passages": 352,
        "curator_commit": REMOTE,
        "method_freeze_commit": FROZEN,
        "source_sha256": SOURCE_SHA,
        "preseal_sha256": digest(raw_m),
        "role_free_sha256": digest(raw_w),
        "source_snapshot_sha256": digest(raw_s),
        "selection_log_sha256": digest(raw_l),
        "source_records": len(records),
        "verified_catalog_records": len(verified),
        "recognized_frozen_intents": recognized,
        "labels_read": False,
    }
    return worlds, verified, receipt


def run(
    out: Path,
    worlds: list[dict[str, Any]],
    records: list[dict[str, Any]],
    receipt: dict[str, Any],
    args: SimpleNamespace,
) -> dict[str, Any]:
    base = out.parent
    if out.exists() or (base / "OWNER33_EVAL_ATTEMPT_STARTED.json").exists():
        raise ValueError("SCIENTIFIC_ATTEMPT_ALREADY_USED")
    out.mkdir()
    backend.configure(out)
    # Asset identity is read-only and must pass before consuming the attempt.
    backend.asset_identity(args)
    receipt_sha = write_once(out / "ADMISSION_RECEIPT.json", receipt)
    write_once(
        base / "OWNER33_EVAL_ATTEMPT_STARTED.json",
        {
            "input_sha256": receipt["role_free_sha256"],
            "freeze_commit": FROZEN,
            "receipt_sha256": receipt_sha,
        },
    )
    start = time.monotonic()
    (model, defender, baseline, zh_vote), r2 = backend.pinned_backend(args)
    rows, members = [], []
    counters: Counter[str] = Counter()
    cache: dict[str, Any] = {}
    for w in worlds:
        if (
            time.monotonic() - start > 2700
            or shutil.disk_usage(out).free < 10 * 2**30
            or sum(p.stat().st_size for p in out.rglob("*") if p.is_file()) > 2 * 2**30
        ):
            raise ValueError("RESOURCE_LIMIT")
        packet = backend.build_topk(w, model, out, cache)
        wid = w["world_id"]
        sha = write_once(out / f"{wid}-TOPK.json", packet)
        members.append({"world_id": wid, "packet_sha256": sha})
        hits = packet["topk"]
        texts = [h["chunk"]["text"] for h in hits]
        embedding = r2.model_vectors(model, texts)
        ehash = digest(embedding.cpu().detach().numpy().tobytes())
        masks: dict[str, Any] = {"NONE": list(range(5))}
        latency: dict[str, Any] = {"NONE": 0}
        for arm, vote in (("RD_B2", baseline), ("RD_ZH", zh_vote)):
            tick = time.perf_counter_ns()
            trace = r2.filter_one(defender, vote, texts, texts, embedding, ehash)
            masks[arm] = [i for i in range(5) if i not in trace["deleted_indices"]]
            latency[arm] = time.perf_counter_ns() - tick
        b2, zh = tuple(masks["RD_B2"]), tuple(masks["RD_ZH"])
        target = vcare.intent(w["query"])
        trigger = vcare.trigger(target, texts, b2, zh)
        anchor = vcare.lookup(records, target)
        adaptive = int(trigger != "NOT_TRIGGERED")
        detail: dict[str, Any] = {}
        for arm, lookups, edit, scope, rescue in (
            (vcare.ARMS[3], adaptive, False, True, False),
            (vcare.ARMS[4], 1, True, True, False),
            (vcare.ARMS[5], adaptive, True, True, True),
            (vcare.ARMS[6], adaptive, True, False, True),
            (vcare.ARMS[7], adaptive, True, True, False),
        ):
            tick = time.perf_counter_ns()
            evidence = anchor if lookups else None
            a = vcare.verify(
                target,
                texts,
                b2,
                evidence,
                lookups,
                scope=scope,
                rescue=rescue,
                edit=edit,
            )
            masks[arm] = list(a.keep)
            latency[arm] = time.perf_counter_ns() - tick
            detail[arm] = {
                "logical_lookups": lookups,
                "source_evidence_id": a.evidence_id,
                "state": a.state,
                "codes": a.codes,
                "context_bytes": vcare.budget(texts, a.keep, evidence),
                "context_slots": len(a.keep) + bool(evidence),
            }
        fail_unless(
            detail[vcare.ARMS[3]]["logical_lookups"]
            == detail[vcare.ARMS[5]]["logical_lookups"]
            and detail[vcare.ARMS[3]]["source_evidence_id"]
            == detail[vcare.ARMS[5]]["source_evidence_id"],
            "EQUAL_BUDGET_DRIFT",
        )
        for mask in masks.values():
            fail_unless(
                mask == sorted(set(mask)) and set(mask) <= set(range(5)), "MASK_ORDER"
            )
        counters.update(
            {
                "matched_lookups": adaptive,
                "full_lookups": adaptive,
                "full_source_hits": bool(detail[vcare.ARMS[5]]["source_evidence_id"]),
                "full_changed_vs_b2": masks[vcare.ARMS[5]] != masks["RD_B2"],
                "full_changed_vs_matched": masks[vcare.ARMS[5]] != masks[vcare.ARMS[3]],
                "full_changed_vs_no_scope": masks[vcare.ARMS[5]]
                != masks[vcare.ARMS[6]],
                "full_changed_vs_no_rescue": masks[vcare.ARMS[5]]
                != masks[vcare.ARMS[7]],
            }
        )
        ranks = [
            {
                "rank": h["rank"],
                "passage_id": h["chunk"]["parent_doc_id"],
                "chunk_sha256": h["chunk"]["content_hash"],
                "score": h["similarity"],
            }
            for h in hits
        ]
        rows.append(
            {
                "world_id": wid,
                "packet_sha256": sha,
                "ranks": ranks,
                "masks": masks,
                "trigger": trigger,
                "verification": detail,
                "filter_ns": latency,
            }
        )
    topk_sha = write_once(
        out / "TOPK_SEAL.json", {"worlds": 32, "top_k": 5, "members": members}
    )
    pred_sha = write_once(out / "PREDICTIONS_ROLE_FREE.json", rows)
    seal = {
        "worlds": 32,
        "arms": list(vcare.ARMS),
        "topk_seal_sha256": topk_sha,
        "predictions_sha256": pred_sha,
        "receipt_sha256": receipt_sha,
        "source_snapshot_sha256": receipt["source_snapshot_sha256"],
        "role_free_sha256": receipt["role_free_sha256"],
        "freeze_commit": FROZEN,
        "labels_read": False,
        "commercial_api_calls": 0,
        "new_model_downloads": 0,
        "measurements": dict(counters),
    }
    return {
        **seal,
        "prediction_seal_sha256": write_once(out / "PREDICTION_SEAL.json", seal),
        "seconds": round(time.monotonic() - start, 3),
        "private_bytes": sum(p.stat().st_size for p in out.rglob("*") if p.is_file()),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("check", "predict"))
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--assets", type=Path, required=True)
    parser.add_argument("--upstream", type=Path, required=True)
    parser.add_argument("--support", type=Path, required=True)
    a = parser.parse_args()
    out = a.out.resolve()
    fail_unless(
        out.drive.upper() == "D:"
        and out.is_relative_to(BASE.resolve())
        and out.parent.is_dir(),
        "PRIVATE_OUT",
    )
    worlds, records, receipt = admit()
    args = SimpleNamespace(
        assets=a.assets.resolve(),
        upstream=a.upstream.resolve(),
        support=a.support.resolve(),
    )
    if a.stage == "check":
        backend.asset_identity(args)
        print(json.dumps(receipt, sort_keys=True))
        return
    print(json.dumps(run(out, worlds, records, receipt, args), sort_keys=True))


if __name__ == "__main__":
    main()
