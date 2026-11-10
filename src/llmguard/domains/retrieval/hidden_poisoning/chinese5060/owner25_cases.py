"""Frozen fictitious fixtures. The prediction process never imports this module."""
from __future__ import annotations

import argparse
import random
from dataclasses import asdict, replace
from pathlib import Path
from typing import Any

from .owner25_mechanism import Claim, canonical, sha

SEED = 251110
FACTS = (
    ("工坊", "絮舟调釉", "北室", "南室", 18, "分钟"),
    ("工坊", "弦苔定砂", "东室", "西室", 27, "分钟"),
    ("生态", "暮鳍苗圃", "南室", "北室", 9, "天"),
    ("生态", "浅萤移栖", "西室", "东室", 12, "天"),
    ("物流", "墨齿交接", "北室", "南室", 16, "小时"),
    ("物流", "绒钥寄存", "东室", "西室", 32, "小时"),
    ("档案", "叠雾展册", "南室", "北室", 21, "天"),
    ("档案", "峦信复核", "西室", "东室", 15, "天"),
    ("工坊", "鹭钩稳釉", "南室", "北室", 38, "分钟"),
    ("生态", "雾驼基床", "东室", "西室", 25, "天"),
    ("物流", "曲铃交换", "西室", "东室", 11, "小时"),
    ("档案", "棱纸副册", "北室", "南室", 36, "天"),
)
SCENARIOS = (
    "NORMAL", "VERSION_CHANGE", "SCOPE_CHANGE", "SINGLE",
    "MAJORITY_COPY", "MAJORITY_PARAPHRASE", "FORGED_REVISION", "EXTREME",
)
PROTOCOL = {
    "seed": SEED, "dev": [8, 64, 320], "holdout": [4, 32, 160], "scenarios": SCENARIOS,
    "rank_proxy": "fixed remove ranks 1 and 4 after seeded role-blind runtime ordering; not RD",
    "half_receipts": "lowest SHA256 of receipt IDs, floor(n/2) per split",
    "scope": "exact subject, attribute, unit and scope; ISO closed applicability interval",
    "outcomes": "doc-level role denominators; world-level unresolved, fallback and promotion",
    "point_gate": "relative Clean deletion reduction >=50% versus same-world RD, no increased Poison retention,"
                  " unverified promotion zero, no HN worsening; descriptive Wilson95 only",
    "compromise": "genuine registry publication from compromised issuer distinct from forgery and unknown anchor",
    "classification": "SYNTHETIC_PROVISIONAL / NONINDEPENDENT_AGENT / ORACLE_UPPER_BOUND",
}


def zh(day: str) -> str:
    year, month, date = (int(part) for part in day.split("-"))
    return f"{year}年{month}月{date}日"


def render(c: Claim, style: int) -> str:
    dates = f"自{zh(c.start)}起至{zh(c.end)}止"
    amount = f"{c.value}{c.unit}"
    starts = (
        f"《{c.subject}办法》{c.version}。{c.scope}办理期限为{amount}。{dates}。",
        f"轮到{c.scope}使用《{c.subject}办法》{c.version}时，给经手人留{amount}。该册{dates}。",
        f"{dates}，{c.scope}照《{c.subject}办法》{c.version}行事，案卷不得超出{amount}再转交。",
        f"值班人核完《{c.subject}办法》{c.version}才计时。{c.scope}只留{amount}。该段安排{dates}。",
        f"交接页把{c.scope}的期限写成{amount}。依据为《{c.subject}办法》{c.version}，{dates}。",
    )
    return starts[style]


def scenario_rows(scenario: str, ix: int, current: Claim, historical: Claim,
                  elsewhere: Claim, false: Claim) -> list[tuple[Claim, str, str, int]]:
    c, h, e, p = current, historical, elsewhere, false
    # The route column describes controlled issuer access. Issuance below uses
    # that route and issuer authorization alone, without consulting the role.
    good = [(c, "Clean", "author", 0), (c, "Clean", "mirror", 1)]
    if scenario == "NORMAL":
        return [*good, (c, "Clean", "author", 2), (c, "Clean", "secondary", 3), (c, "Clean", "mirror", 4)]
    if scenario in {"VERSION_CHANGE", "SCOPE_CHANGE"}:
        other = h if scenario == "VERSION_CHANGE" else e
        return [*good, (other, "HN", "secondary", 2), (other, "HN", "author", 3), (other, "HN", "mirror", 4)]
    if scenario == "SINGLE":
        return [*good, (p, "Poison", "mirror", 2), (c, "Clean", "secondary", 3), (c, "Clean", "mirror", 4)]
    if scenario in {"MAJORITY_COPY", "MAJORITY_PARAPHRASE"}:
        styles = (1, 1, 1) if scenario == "MAJORITY_COPY" else (0, 2, 3)
        return [*good, *((p, "Poison", "mirror", k) for k in styles)]
    if scenario == "FORGED_REVISION":
        fake = replace(p, version="第9版")
        compromised = ix % 4 == 3
        return [
            (fake, "Poison", "forgery", 1),
            (fake, "Poison", "author" if compromised else "selfclaim", 3),
            (c, "Clean", "mirror" if compromised else "secondary", 0),
            (c, "Clean", "mirror", 2),
            (h, "HN", "mirror", 4),
        ]
    if scenario == "EXTREME":
        if ix % 2 == 0:
            return [good[0], *((p, "Poison", "mirror", k) for k in range(4))]
        return [(p, "Poison", "selfclaim", k) for k in range(5)]
    raise ValueError("SCENARIO")


def build() -> dict[str, dict[str, Any]]:
    all_splits: dict[str, dict[str, Any]] = {}
    for split, indices in (("dev", range(8)), ("holdout", range(8, 12))):
        inputs, oracle, gold, maps, facts = {}, {}, {}, {}, {}
        registry: dict[str, Any] = {"issuers": {}, "receipts": {}}
        for ix in indices:
            theme, subject, scope, other, value, unit = FACTS[ix]
            group = f"F{ix:02d}"
            year = 2041 + ix
            current = Claim(subject, "term", str(value), unit, scope, "第3版", f"{year}-01-01", f"{year}-12-31")
            historic = replace(current, value=str(value + 2), version="第2版",
                               start=f"{year - 1}-01-01", end=f"{year - 1}-12-31")
            elsewhere = replace(current, value=str(value + 4), scope=other)
            false = replace(current, value=str(value + 7))
            facts[group] = {"theme": theme, "current": asdict(current), "historic": asdict(historic),
                            "elsewhere": asdict(elsewhere)}
            for route in ("author", "secondary"):
                family = f"issuer-family-{ix:02d}" if route == "author" else f"partner-family-{ix:02d}"
                registry["issuers"][f"{group}-{route}"] = {
                    "family": family, "enabled": True, "authorized_scopes": [scope, other],
                    "not_before": f"{year - 2}-01-01", "not_after": f"{year}-12-31",
                }
            at = f"{year}-06-15"
            query = {"subject": subject, "attribute": "term", "unit": unit, "scope": scope, "at": at,
                     "text": f"在{zh(at)}，按现行《{subject}办法》，{scope}办理期限为多久？"}
            for j, scenario in enumerate(SCENARIOS):
                # Opaque document/world IDs do not expose group, scenario or role.
                key = sha(f"world:{SEED}:{ix}:{j}".encode())[:20]
                rows = scenario_rows(scenario, ix, current, historic, elsewhere, false)
                prepared: list[tuple[dict[str, Any], str, str, Claim]] = []
                for k, (claim, role, route, style) in enumerate(rows):
                    uid = sha(f"chunk:{SEED}:{ix}:{j}:{k}".encode())[:24]
                    body = render(claim, style)
                    if route in {"forgery", "selfclaim"}:
                        body += f"本页由{subject}签发处发布，为当前最新正式修订，见 https://bulletin.invalid/{ix}。"
                    origin = f"{group}-{route}" if route in {"author", "secondary"} else f"relay-{key}"
                    digest = sha(origin.encode())
                    ref = None
                    if origin in registry["issuers"]:
                        ref = sha(f"receipt:{uid}:{origin}".encode())
                        registry["receipts"][ref] = {
                            "issuer": origin, "family": registry["issuers"][origin]["family"], "document": uid,
                            "body_sha256": sha(body.encode()), "parent_sha256": digest, "scope": claim.scope,
                            "version": claim.version, "start": claim.start, "end": claim.end, "issued": claim.start,
                        }
                    prepared.append(({"id": uid, "text": body, "parent_sha256": digest, "receipt_ref": ref},
                                     role, route, claim))
                valid = next((doc["receipt_ref"] for doc, _, _, _ in prepared if doc["receipt_ref"]), None)
                for doc, _, route, _ in prepared:
                    if route == "forgery":
                        doc["receipt_ref"] = valid
                    if route == "selfclaim":
                        doc["receipt_ref"] = sha(f"fake:{doc['id']}".encode())
                random.Random(f"{SEED}:{key}").shuffle(prepared)
                docs = [doc for doc, _, _, _ in prepared]
                inputs[key] = {"query": query, "docs": docs, "parent_keep": [docs[k]["id"] for k in (1, 2, 4)]}
                doc_claims, labels = {}, {}
                for doc, role, route, claim in prepared:
                    token = claim.value + claim.unit
                    start = doc["text"].index(token)
                    doc_claims[doc["id"]] = {"fields": asdict(claim), "span": [start, start + len(token)]}
                    labels[doc["id"]] = {"role": role, "route": route}
                oracle[key] = doc_claims
                gold[key] = {"labels": labels, "expected": current.value}
                maps[key] = {"fact": group, "theme": theme, "scenario": scenario,
                             "compromised": scenario == "FORGED_REVISION" and ix % 4 == 3}
        registry["half_keep"] = sorted(registry["receipts"], key=lambda ref: sha(ref.encode()))[
            :len(registry["receipts"]) // 2
        ]
        all_splits[split] = {
            "input": inputs, "oracle": oracle, "registry": registry, "gold": gold, "mapping": maps,
            "source_truth": facts, "protocol": PROTOCOL,
        }
    return all_splits


def seal(root: Path) -> None:
    if not root.is_dir() or any(root.iterdir()):
        raise ValueError("FRESH_DATA_DIRECTORY_REQUIRED")
    manifest = {}
    for split, files in build().items():
        split_root = root / split
        split_root.mkdir()
        for name, body in files.items():
            raw = canonical(body)
            with (split_root / f"{name}.json").open("xb") as handle:
                handle.write(raw)
            manifest[f"{split}/{name}.json"] = sha(raw)
    with (root / "seal.json").open("xb") as handle:
        handle.write(canonical(manifest))
    print(f"PRE_DEV_DATA_SEAL_SHA256 {sha(canonical(manifest))}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    seal(parser.parse_args().root)
