"""Read only Owner27 seals and reconstruct its counts and failure cases."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from itertools import combinations
from pathlib import Path
from typing import Any
from zipfile import ZipFile

ARCHIVE = "cc9051b64dccb5b9bcf57495ebfdf370d99c859708fe0b833707be5a65825d92"
MANIFEST = "ebca241a364c75cfe9cfaebfb6832e7a97b9a856a47638b870e0ea55d7b762f4"
HISTORICAL = {"S1": (), "S2": (1, 2), "S3": (4,), "S4": (2,), "S5": (1,), "S6": (), "S7": (2,), "S8": ()}
OTHER_SCOPE = {"S1": (), "S2": (), "S3": (1, 2), "S4": (), "S5": (), "S6": (1,), "S7": (3,), "S8": ()}
TYPES = ("CURRENT_CLEAN_OVERDELETE", "VALID_HISTORICAL_HN_OVERDELETE", "SCOPE_HN_OVERDELETE",
         "FORGED_UPDATE_SURVIVES", "PARAPHRASED_COLLUSION_SURVIVES", "5_OF_5_NOT_RETRIEVED")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write(path: Path, value: Any) -> str:
    data = (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()
    with path.open("xb") as handle:
        handle.write(data)
    return sha(data)


def latency(values: list[int]) -> dict[str, float]:
    ordered = sorted(values)
    n = len(ordered)
    return {"median_ms": round((ordered[(n - 1) // 2] + ordered[n // 2]) / 2e6, 6),
            "p95_ms": round(ordered[(95 * n + 99) // 100 - 1] / 1e6, 6)}


def recount(archive: Path, manifest: Path, out: Path) -> dict[str, Any]:
    if sha(archive.read_bytes()) != ARCHIVE or sha(manifest.read_bytes()) != MANIFEST:
        raise ValueError("OWNER27_INPUT_IDENTITY")
    original = json.loads(manifest.read_bytes())
    with ZipFile(archive) as z:
        data = z.read("MEMBER_INDEX.json")
        if sha(data) != original["private_archive"]["member_index_sha256"]:
            raise ValueError("MEMBER_INDEX")
        hashes = {r["member"]: r["sha256"] for r in json.loads(data)}
        if len(hashes) != 363 or set(z.namelist()) != set(hashes) | {"MEMBER_INDEX.json"}:
            raise ValueError("MEMBER_SET")
        if any(sha(z.read(name)) != expected for name, expected in hashes.items()):
            raise ValueError("MEMBER_CHANGED")

        def read(name: str) -> Any:
            return json.loads(z.read(name))

        labels = {r["world_id"]: r for r in read("evaluator-only/labels.json")}
        receipts = {r["document"]: r for r in read("inputs/receipts.json")}
        predictions = read("evidence/predictions.json")
        scores = read("evidence/scores.json")
        arms = tuple(read("evidence/prediction-seal.json")["arms"])
        count: dict[str, Any] = {a: {"main": Counter(), "mirror": Counter(), "scenes": {}, "groups": {}} for a in arms}
        pairs: dict[str, Any] = {f"{a} => {b}": {"all": Counter(), "groups": {}, "scenes": {}}
                                  for a, b in combinations(arms, 2)}
        types: dict[str, Any] = {k: {"events": 0, "worlds": 0, "examples": []} for k in TYPES}
        receipt_counts: dict[str, Any] = {k: Counter() for k in ("all_corpus", "main_corpus", "main_topk")}
        subtype: dict[str, Any] = {a: Counter() for a in arms}
        ns: dict[str, list[int]] = {a: [] for a in arms}
        ns_with_embedding: dict[str, list[int]] = {a: [] for a in arms}
        for row in predictions:
            wid = row["world_id"]
            lab = labels[wid]
            part, scene, group = (lab[k] for k in ("partition", "scene", "group"))
            packet = read(f"evidence/{wid}.json")
            if row["packet_sha256"] != hashes[f"evidence/{wid}.json"]:
                raise ValueError("PACKET_BINDING")
            roles = [lab["documents"][h["chunk"]["parent_doc_id"]] for h in packet["topk"]]
            all_roles = Counter(lab["documents"].values())
            kind = {}
            if part == "main":
                for indexes, label in ((HISTORICAL[scene], "HISTORICAL"), (OTHER_SCOPE[scene], "SCOPE")):
                    kind.update({"d-" + sha(f"{wid}|{i}".encode())[:24]: label for i in indexes})
                if set(kind) != {d for d, role in lab["documents"].items() if role == "H"}:
                    raise ValueError("STATIC_AUTHORING_RECIPE")
            for d, role in lab["documents"].items():
                for layer in ("all_corpus", "main_corpus") if part == "main" else ("all_corpus",):
                    receipt_counts[layer][f"{role}_offered"] += 1
                    receipt_counts[layer][f"{role}_bound"] += d in receipts
            for a, output in row["arms"].items():
                kept = set(output["keep"])
                m = Counter[str](worlds=1, slots=5, empty=int(not kept))
                for role in "PCHB":
                    ranks = {i for i, r in enumerate(roles) if role == r}
                    m.update({f"{role}_offered": all_roles[role], f"{role}_hit": len(ranks),
                              f"{role}_retained": len(ranks & kept), f"{role}_deleted": len(ranks - kept),
                              f"{role}_missed": all_roles[role] - len(ranks),
                              f"{role}_world_hit": int(bool(ranks)),
                              f"{role}_world_any_retained": int(bool(ranks & kept)),
                              f"{role}_world_any_deleted": int(bool(ranks - kept)),
                              f"{role}_world_partial": int(bool(ranks & kept and ranks - kept)),
                              f"{role}_restored": len(ranks & set(output.get("restored", ())))})
                if "reason" in output:
                    m[output["reason"]] += 1
                count[a][part].update(m)
                if part != "main":
                    continue
                ns[a].append(output["ns"])
                ns_with_embedding[a].append(output["ns"] + (row["embedding_ns"] if a.startswith("RD_") else 0))
                for partition, unit in (("scenes", scene), ("groups", group)):
                    count[a][partition].setdefault(unit, Counter()).update(m)
                for i, hit in enumerate(packet["topk"]):
                    d = hit["chunk"]["parent_doc_id"]
                    if d in kind:
                        subtype[a][f"{kind[d]}_hit"] += 1
                        subtype[a][f"{kind[d]}_deleted"] += i not in kept
            if part != "main":
                continue
            for i, hit in enumerate(packet["topk"]):
                d = hit["chunk"]["parent_doc_id"]
                receipt_counts["main_topk"][f"{roles[i]}_offered"] += 1
                receipt_counts["main_topk"][f"{roles[i]}_bound"] += d in receipts
            for a, b in combinations(arms, 2):
                left, right = (set(row["arms"][arm]["keep"]) for arm in (a, b))
                m = Counter[str](worlds=1, mask_changed=int(left != right))
                for i in left ^ right:
                    m[f"{roles[i]}_{'kept_to_deleted' if i in left else 'deleted_to_kept'}"] += 1
                p = pairs[f"{a} => {b}"]
                p["all"].update(m)
                p["groups"].setdefault(group, Counter()).update(m)
                p["scenes"].setdefault(scene, Counter()).update(m)
            kept = set(row["arms"]["RD_ZH"]["keep"])
            failure = [
                [i for i, r in enumerate(roles) if r == "C" and i not in kept],
                [i for i, h in enumerate(packet["topk"]) if i not in kept and kind.get(h["chunk"]["parent_doc_id"]) == "HISTORICAL"],
                [i for i, h in enumerate(packet["topk"]) if i not in kept and kind.get(h["chunk"]["parent_doc_id"]) == "SCOPE"],
                [i for i, r in enumerate(roles) if scene == "S7" and r == "P" and i in kept],
                [i for i, r in enumerate(roles) if scene == "S6" and r == "P" and i in kept],
                [i for i, r in enumerate(roles) if scene == "S8" and all_roles["P"] == 5 and roles.count("P") < 5 and r == "P"],
            ]
            for name, affected in zip(TYPES, failure, strict=True):
                if affected:
                    bucket = types[name]
                    bucket["events"] += len(affected)
                    bucket["worlds"] += 1
                    if len(bucket["examples"]) < 3:
                        bucket["examples"].append({
                            "world_id": wid, "scene": scene, "packet_sha256": row["packet_sha256"],
                            "prediction_file_sha256": hashes[f"evidence/{wid}-prediction.json"],
                            "topk_ranks": [i + 1 for i in affected],
                            "chunk_sha256": [packet["topk"][i]["chunk"]["content_hash"] for i in affected],
                            "basis": "SEALED_MASK_AND_AGENT_PROVISIONAL_ROLE_PLUS_STATIC_AUTHORING_RECIPE",
                            "offered_poison": all_roles["P"], "retrieved_poison": roles.count("P"),
                        })
        def published_role_counts(measured: Counter[str]) -> dict[str, list[int]]:
            return {r: [measured[f"{r}_{'retained' if k == 'kept' else k}"] for k in original["role_array_order"]]
                    for r in "PCHB"}

        measured_latency = {a: {"filter_latency": latency(ns[a]),
                                "embedding_plus_filter_latency": latency(ns_with_embedding[a])} for a in arms}
        for a, record in count.items():
            for part, role_key in (("main", "role_counts"), ("mirror", "mirror_role_counts")):
                if published_role_counts(record[part]) != original["arms"][a][role_key]:
                    raise ValueError("GIT_MANIFEST_ROLE_COUNTS")
            if any(original["arms"][a][k] != v for k, v in measured_latency[a].items()):
                raise ValueError("GIT_MANIFEST_LATENCY")
            for key in ("main", "mirror"):
                if any(scores["arms"][a][key][k] != v for k, v in record[key].items()):
                    raise ValueError("COUNT_MISMATCH")
            for our_key, old_key in (("scenes", "scenarios"), ("groups", "fact_groups")):
                for unit, measured in record[our_key].items():
                    if any(scores["arms"][a][old_key][unit][k] != v for k, v in measured.items()):
                        raise ValueError("STRATUM_MISMATCH")
        for row in original["strata"]:
            key = "scenes" if row["type"] == "scenarios" else "groups"
            if published_role_counts(count[row["arm"]][key][row["id"]]) != row["role_counts"]:
                raise ValueError("GIT_MANIFEST_STRATA")
        public_pairs = {p["pair"]: {k: p[k] for k in ("all", "groups", "scenes")} for p in original["paired"]}
        if public_pairs != pairs:
            raise ValueError("GIT_MANIFEST_PAIR")
        for name, partitions in pairs.items():
            for key, block in partitions.items():
                if key == "all":
                    valid = all(scores["comparisons"][name][key].get(k, 0) == v for k, v in block.items())
                else:
                    valid = all(scores["comparisons"][name][key][unit].get(k, 0) == v
                                for unit, measured in block.items() for k, v in measured.items())
                if not valid:
                    raise ValueError("PAIR_MISMATCH")
        report = {"status": "READ_ONLY_SEALED_DEV_ANALYSIS", "archive_sha256": ARCHIVE, "manifest_sha256": MANIFEST,
                  "arms": count, "pairs": pairs, "failure_types": types, "hn_subtypes": subtype,
                  "latency": measured_latency,
                  "receipt_correlation": receipt_counts, "authoring_sha256": hashes["support/author_dev_proxy.py"],
                  "guard_sha256": hashes["support/guard-executed.py"], "verified_members": 363,
                  "new_scientific_trials": 0, "human_gold": 0}
        write(out / "OWNER27_READONLY_RECOUNT.json", report)
        if sha(archive.read_bytes()) != ARCHIVE:
            raise ValueError("ARCHIVE_CHANGED")
        return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("archive", "manifest", "out"):
        parser.add_argument(f"--{name}", type=Path, required=True)
    args = parser.parse_args()
    r = recount(args.archive, args.manifest, args.out)
    print(json.dumps({"status": r["status"], "failures": r["failure_types"], "receipts": r["receipt_correlation"],
                      "hn": r["hn_subtypes"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
