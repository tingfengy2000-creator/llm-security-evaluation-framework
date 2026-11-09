"""Owner19 authoring, schema checks and sealing only. No extraction or evaluation runner."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from datetime import date
from decimal import Decimal
from pathlib import Path
from typing import Any
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

RUN = "W1-5060-S1B-FEAS-DATA-PREP-20261109-01"
SEED = "owner19-preallocated-20261109-v1"
OLD = "W1-5060-S1-CHINESE-EXTRACTION-20261108-01"
OLD_SHA = "8245af9a1241fe966f0dbc05e52ed7744b041e13685a743a81aebd818b9a8481"
CATEGORIES = (
    "scalar", "as_of", "scope", "negation_exception", "equivalent_spans",
    "cross_scope_same_value", "linked_passages", "unverified_revision", "navigation", "repeat_conflict",
)
PARTS = ("01-03.txt", "04-06.txt", "07-08.txt", "09-10.txt")
FIELDS = {"id", "query", "evidence"}
PRIVATE_KEYS = re.compile(r"accepted_span_sets|ground_truth|expected_answer|oracle|poison_label", re.I)
MARKER = re.compile(r"〔([^〔〕]+)〕")
WORD = re.compile(r"[\u4e00-\u9fff]+")
RISK = {
    "N": r"不是|不能|不收|划掉|不再|废止|撤|不采用",
    "U": r"转述|匿名|草案|传闻|转录|摘录|抄签|自称|群聊|转载|另印",
    "X": r"导航|首页|页眉|页脚|页顶|侧栏|筛选项|链接|站内搜索",
    "D": r"收费|单位",
    "M": r"未|没|空栏|无法|脱落|待",
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(data: Any) -> bytes:
    return (json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def need(condition: bool, reason: str) -> None:
    if not condition:
        raise ValueError(reason)


def read(path: Path) -> bytes:
    need(path.resolve(strict=True) == path, "NONCANONICAL_INPUT_PATH")
    return path.read_bytes()


def span(text: str, start: int, end: int) -> dict[str, Any]:
    need(0 <= start < end <= len(text), "INVALID_CHARACTER_SPAN")
    b0, b1 = len(text[:start].encode()), len(text[:end].encode())
    payload = text.encode()[b0:b1]
    need(payload.decode() == text[start:end], "UTF8_BOUNDARY")
    return {"start": start, "end": end, "byte_start": b0, "byte_end": b1, "sha256": sha(payload)}


def support_matches(candidate: list[tuple[int, int]], support: dict[str, Any]) -> bool:
    """Pure interval rule, available to a future authorized scorer. Uses no labels itself."""
    outer = support["window"]
    if not candidate or any(not outer["start"] <= lo < hi <= outer["end"] for lo, hi in candidate):
        return False
    ordered = sorted(candidate)
    if any(left[1] > right[0] for left, right in zip(ordered, ordered[1:], strict=False)):
        return False
    return all(any(lo <= part["start"] < part["end"] <= hi for lo, hi in ordered)
               for part in support["requires"])


def parse_atom(raw: str) -> tuple[dict[str, Any], str]:
    state, key, interval, value, unit, clause = raw.split("~")
    need(state in {"A", *RISK}, "ATOM_STATE")
    if state in RISK:
        need(bool(re.search(RISK[state], clause)), f"NO_VISIBLE_{state}_CUE")
    valid = [] if interval == "-" else interval.split(":")
    if valid:
        need(len(valid) == 2 and date.fromisoformat(valid[0]) <= date.fromisoformat(valid[1]), "BAD_INTERVAL")
    if state == "M":
        need(value == unit == "-", "MISSING_SLOT_CONTAINS_VALUE")
    elif unit == "DATE":
        need(date.fromisoformat(value).isoformat() == value, "BAD_DATE")
    else:
        number = Decimal(value)
        need(number.is_finite() and number >= 0 and (unit != "%" or number <= 100) and unit != "-", "BAD_SCALAR")
    return {"state": state, "selector": key, "valid": valid, "value": value, "unit": unit}, clause.strip()


def minimal_support(text: str, atom: dict[str, Any], raw: str, offset: int) -> tuple[str, dict[str, Any]]:
    block = raw.replace("^", "\n")
    expected = "" if atom["state"] == "M" else (
        atom["value"] if atom["unit"] == "DATE" else atom["value"] + atom["unit"]
    )
    found = list(MARKER.finditer(block))
    need([match[1] for match in found] == ([expected] if expected else []), "VALUE_MARKER_MISMATCH")
    clean = MARKER.sub(lambda m: m[1], block)
    cues = atom["selector"].split("/") + atom["valid"]
    need(all(cue and cue in clean for cue in cues), "MISSING_VISIBLE_SCOPE_OR_INTERVAL")
    ranges = [(clean.index(cue), clean.index(cue) + len(cue)) for cue in cues]
    if found:
        # The marker identifies the exact scalar occurrence before it is stripped from the input.
        at = found[0].start()
        ranges.append((at, at + len(expected)))
        need(clean[at:at + len(expected)] == expected, "VALUE_AT_WRONG_OFFSET")
    if "\n" in clean:
        left, right = clean.split("\n")
        # The shared bridge must be explicit in both paragraphs. Use the longest shared phrase.
        candidates = {word[i:j] for word in WORD.findall(left) for i in range(len(word))
                      for j in range(i + 2, len(word) + 1) if word[i:j] in right}
        need(bool(candidates), "MISSING_PARAGRAPH_BRIDGE")
        bridge = min(candidates, key=lambda token: (-len(token), token))
        a, b = left.index(bridge), len(left) + 1 + right.index(bridge)
        ranges.extend([(a, a + len(bridge)), (b, b + len(bridge))])
    full = text + clean
    return clean, {
        "window": span(full, offset, offset + len(clean)),
        "requires": [span(full, offset + a, offset + b) for a, b in sorted(set(ranges))],
    }


def applicable(atom: dict[str, Any], key: str, as_of: str | None) -> bool:
    if atom["state"] != "A" or atom["selector"] != key:
        return False
    valid = atom["valid"]
    return not valid if as_of is None else bool(valid and valid[0] <= as_of <= valid[1])


def profile(text: str) -> set[str]:
    content = re.sub(r"【虚构来源[^】]+】|《[^》]+》|[0-9]+|[\W_]+", "", text)
    return {content[i:i + 3] for i in range(len(content) - 2)}


def similarity(a: set[str], b: set[str]) -> float:
    return len(a & b) / len(a | b) if a or b else 0.0


def build(root: Path, old: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    plans = json.loads(read(root / "control" / "GENERATION_PLAN.json"))
    need(plans["seed"] == SEED and tuple(plans["categories"]) == CATEGORIES
         and plans["quota_per_category"] == [7, 3, 2], "PLAN_CHANGED")
    sources = json.loads(read(root / "control" / "SOURCE_LICENSE.json"))
    families = sources["synthetic"]["families"]
    need(len({f["name"] for f in families}) == 10 and len({f["domain"] for f in families}) >= 4, "FAMILIES")
    old_raw = read(old)
    need(sha(old_raw) == OLD_SHA, "OLD73_IDENTITY_CHANGED")
    prior = json.loads(old_raw)
    need(len(prior) == 73 and all(set(row) == FIELDS for row in prior), "OLD73_SCHEMA")
    views: list[dict[str, Any]] = []
    labels: list[dict[str, Any]] = []
    truth: list[dict[str, Any]] = []
    groups: list[dict[str, Any]] = []
    counts: dict[str, Counter[str]] = {}
    cases: list[dict[str, Any]] = []
    subjects: set[str] = set()
    category = ""
    seen: list[str] = []
    for line in "\n".join(read(root / "authoring" / f).decode() for f in PARTS).splitlines():
        if not line.strip():
            continue
        if line.startswith("@"):
            category = line[1:]
            need(category in CATEGORIES and category not in counts, "CATEGORY_ORDER")
            counts[category] = Counter()
            seen.append(category)
            continue
        stat = counts[category]
        index = stat["primary"]
        try:
            query, rewrite, key, when, authored, joined = line.split(" | ")
            family = families[index]
            subject = key.split("/")[0]
            need(subject not in subjects, "REUSED_SEMANTIC_SUBJECT")
            subjects.add(subject)
            as_of = None if when == "-" else date.fromisoformat(when).isoformat()
            parsed = [parse_atom(piece) for piece in joined.split(" // ")]
            resolved = [atom for atom, _ in parsed if applicable(atom, key, as_of)]
            values = {(atom["value"], atom["unit"]) for atom in resolved}
            decision = "ANSWER" if len(values) == 1 else "UNKNOWN"
            need(decision == authored == ("ANSWER" if index < 7 else "UNKNOWN"), "ORACLE_DISAGREES_WITH_SOURCE_TRUTH")
            has_pair = rewrite != "-"
            need(has_pair == (index < 2), "PAIR_QUOTA_OR_SELECTION")
            title = "《" + subject + "工作札》" if (index + len(seen) - 1) % 10 < 7 else ""
            evidence = "【虚构来源·" + family["name"] + "】\n" + (title + "\n" if title else "")
            facts = [atom for atom, _ in parsed]
            group = sha(f"{SEED}:{category}:{index}".encode())[:18]
            truth.append({"group": group, "category": category, "family": family["name"], "selector": key,
                          "as_of": as_of, "document_title": title, "atoms": facts})
            supports = []
            for atom, clause in parsed:
                if not evidence.endswith("\n"):
                    evidence += "\n"
                block, support = minimal_support(evidence, atom, clause, len(evidence))
                evidence += block
                if decision == "ANSWER" and applicable(atom, key, as_of):
                    outer = support["window"]
                    need(support_matches([(outer["start"], outer["end"])], support), "SUPPORT_SELF_CHECK")
                    supports.append(support)
            if category == "equivalent_spans" and decision == "ANSWER":
                need(len(supports) >= 2, "MISSING_EQUIVALENT_SUPPORT")
            if category == "cross_scope_same_value" and decision == "ANSWER":
                need(len(supports) == 1 and any(
                    (a["value"], a["unit"]) in values and a["selector"] != key for a in facts
                ), "NO_WRONG_SCOPE_EQUAL_VALUE")
            need(not PRIVATE_KEYS.search(evidence + query + rewrite) and not any(
                marker in evidence for marker in ("〔", "〕", "^", " // ")
            ), "AUTHOR_METADATA_IN_INPUT")
            if decision == "UNKNOWN":
                relevant = [a for a in facts if a["selector"] == key]
                reason = ("SAME_SCOPE_CONFLICT" if values else "UNVERIFIED_REVISION" if any(
                    a["state"] == "U" for a in relevant
                ) else "TEMPORAL_SCOPE_UNBOUND" if as_of else "NO_SUPPORTED_VALUE")
            else:
                reason = None
            value, unit = next(iter(values)) if decision == "ANSWER" else (None, None)
            view_ids = []
            for form, prompt in (("primary", query), ("companion", rewrite)) if has_pair else (("primary", query),):
                need(all(cue in prompt for cue in key.split("/")) and (as_of is None or as_of in prompt),
                     "QUERY_SELECTOR_OR_TIME_NOT_VISIBLE")
                uid = sha(f"{SEED}:{group}:{form}".encode())[:24]
                visible_query = (title + "｜" if title else "") + prompt
                views.append({"id": uid, "query": visible_query, "evidence": evidence})
                labels.append({"id": uid, "status": decision, "value": value, "unit": unit, "selector": key,
                               "as_of": as_of, "document_title": title, "accepted_span_sets": supports,
                               "reason": reason, "evidence_sha256": sha(evidence.encode())})
                view_ids.append(uid)
            need(not has_pair or profile(query) != profile(rewrite), "REWRITE_NOT_DISTINCT")
            groups.append({"group": group, "primary": view_ids[0], "companion": view_ids[1] if has_pair else None})
            cases.append({"query": query, "evidence": evidence, "id": view_ids[0]})
            stat.update({"primary": 1, decision: 1, "paired": int(has_pair), "titled": int(bool(title))})
        except (IndexError, ValueError) as exc:
            raise ValueError(f"QA {category} slot {index + 1}: {exc}") from exc
    need(tuple(seen) == CATEGORIES and all(
        c["primary"] == 10 and c["ANSWER"] == 7 and c["UNKNOWN"] == 3 and c["paired"] == 2
        and c["titled"] == 7 for c in counts.values()
    ), "COVERAGE_QUOTAS")
    need(len(views) == len({r["id"] for r in views}) == 120 and len(subjects) == 100, "COUNT_OR_ID")
    need(len({(r["query"], r["evidence"]) for r in views}) == 120, "EXACT_VIEW_DUPLICATE")
    profiles = [(profile(c["query"]), profile(c["evidence"])) for c in cases]
    old_profiles = [(profile(c["query"]), profile(c["evidence"])) for c in prior]

    def distances(comparisons: list[tuple[tuple[set[str], set[str]], tuple[set[str], set[str]]]]) -> dict[str, Any]:
        max_query, max_evidence, flags = 0.0, 0.0, 0
        for (aq, ae), (bq, be) in comparisons:
            q, e = similarity(aq, bq), similarity(ae, be)
            max_query, max_evidence = max(q, max_query), max(e, max_evidence)
            flags += int(e >= 0.84 or (q >= 0.72 and e >= 0.72))
        need(flags == 0, "NEAR_DUPLICATE_REQUIRES_ADJUDICATION")
        return {"pairs": len(comparisons), "max_query": max_query, "max_evidence": max_evidence, "flags": flags}

    intra = distances([(a, b) for i, a in enumerate(profiles) for b in profiles[:i]])
    legacy = distances([(a, b) for a in profiles for b in old_profiles])
    need(all(set(row) == FIELDS for row in views), "ROLE_FREE_SCHEMA")
    ids = {row["id"]: row for row in labels}
    for view in views:
        label = ids[view["id"]]
        evidence = view["evidence"]
        need(sha(evidence.encode()) == label["evidence_sha256"], "EVIDENCE_BINDING")
        for support in label["accepted_span_sets"]:
            for proof in (support["window"], *support["requires"]):
                need(span(evidence, proof["start"], proof["end"]) == proof, "SEALED_SPAN_REPLAY")
    for pair in groups:
        if pair["companion"]:
            primary, alternate = (ids[pair[key]] for key in ("primary", "companion"))
            need({k: v for k, v in primary.items() if k != "id"} ==
                 {k: v for k, v in alternate.items() if k != "id"}, "PARAPHRASE_ORACLE_DRIFT")
    items = {"runtime/INPUT.json": sorted(views, key=lambda r: r["id"]),
             "custodian/SOURCE_TRUTH.json": sorted(truth, key=lambda r: r["group"]),
             "evaluation/PROVISIONAL_GOLD.json": sorted(labels, key=lambda r: r["id"]),
             "custodian/PAIRS.json": sorted(groups, key=lambda r: r["group"])}
    summary = {
        "semantic_cases": len(subjects), "views": len(views), "families": len(families),
        "domains": len({f["domain"] for f in families}), "categories": counts,
        "intra_dedup": intra, "old73_dedup": legacy, "old73_input_sha256": OLD_SHA,
        "reason_counts_primary": Counter(ids[g["primary"]]["reason"] for g in groups if ids[g["primary"]]["reason"]),
        "accepted_support_sets": sum(len(r["accepted_span_sets"]) for r in labels),
        "span_checks": sum(1 + len(s["requires"]) for r in labels for s in r["accepted_span_sets"]),
        "role_free_schema": sorted(FIELDS), "human_gold": 0, "new_predictions": 0, "new_scores": 0,
    }
    return items, summary


def archive(root: Path, directory: str, names: tuple[str, ...], verify: bool) -> str:
    target = root / "seals" / (directory + ".zip")
    if not verify:
        with ZipFile(target, "x", compression=ZIP_DEFLATED) as bundle:
            for name in names:
                info = ZipInfo(name, (2026, 11, 9, 0, 0, 0))
                bundle.writestr(info, read(root / directory / name), compress_type=ZIP_DEFLATED)
    with ZipFile(target) as bundle:
        need(bundle.namelist() == list(names) and bundle.testzip() is None, "ZIP_INVALID")
        need(all(bundle.read(n) == read(root / directory / n) for n in names), "ZIP_MEMBER_DRIFT")
    return sha(read(target))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("seal", "verify"))
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--seal-sha256", help="required expected receipt hash for verify")
    args = parser.parse_args()
    root = args.root.resolve(strict=True)
    need(root == args.root and root.name == RUN and root.drive.upper() in {"D:", "E:"}
         and root.parent.name == "paper1_chinese5060" and root.parent.parent.name == "experiments",
         "EXACT_PRIVATE_ROOT_REQUIRED")
    old = root.parent / OLD / "INFERENCE_PRIVATE.json"
    verify = args.stage == "verify"
    sealed = root / "seals"
    destination = sealed / "DATA_SEAL.json"
    recorded = None
    if verify:
        receipt = read(destination)
        need(sha(receipt) == args.seal_sha256, "EXPECTED_RECEIPT_HASH_REQUIRED_OR_MISMATCH")
        recorded = json.loads(receipt)
    else:
        need(args.seal_sha256 is None, "SEAL_DOES_NOT_TAKE_A_RECEIPT_HASH")
    items, summary = build(root, old)
    if not verify:
        sealed.mkdir(exist_ok=False)
    members = {}
    for name, value in items.items():
        blob = canonical(value)
        path = root / name
        if verify:
            need(read(path) == blob, "MEMBER_REPLAY_DRIFT")
        else:
            path.parent.mkdir(exist_ok=True)
            with path.open("xb") as out:
                out.write(blob)
        members[name] = sha(blob)
    docs = ("GENERATION_PLAN.json", "SOURCE_LICENSE.json", "SCORING_PROTOCOL.md")
    members.update({"control/" + name: sha(read(root / "control" / name)) for name in docs})
    members.update({"authoring/" + name: sha(read(root / "authoring" / name)) for name in PARTS})
    bundles = {"runtime": ("INPUT.json",), "evaluation": ("PROVISIONAL_GOLD.json",),
               "custodian": ("SOURCE_TRUTH.json", "PAIRS.json"), "control": docs, "authoring": PARTS}
    archives = {name: archive(root, name, files, verify) for name, files in bundles.items()}
    manifest = {"run_id": RUN, "status": "FEAS_DATA_READY", "members": members, "archives": archives,
                "validator_sha256": sha(Path(__file__).read_bytes().replace(b"\r\n", b"\n")),
                "counts": summary, "data_class": "AGENT_GENERATED_PROVISIONAL_FEASIBILITY",
                "authorship": "NOT_INDEPENDENT_AUTHOR", "human_gold": 0, "evaluation": "NOT_RUN",
                "stage": "DATA_PREP_NOT_SCIENTIFIC_TRIAL", "auto_continue": False}
    if recorded is not None:
        # Preserve the authenticated sealing program identity during cross-version read-only replay.
        manifest["validator_sha256"] = recorded["validator_sha256"]
    payload = canonical(manifest)
    if verify:
        need(read(destination) == payload, "DATA_SEAL_DRIFT")
    else:
        with destination.open("xb") as out:
            out.write(payload)
    print(json.dumps({"status": manifest["status"], "stage": args.stage, "seal_sha256": sha(payload),
                      "semantic_cases": summary["semantic_cases"], "views": summary["views"]}))


if __name__ == "__main__":
    main()
