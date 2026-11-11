"""Render Paper 1 aggregate-only DEV/EVAL tables and fact-group figure."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

DEV = "7b4e4cad00df38b724fdeb1c2edd63f06b7be9fd"
EVAL = "670d9ab0e546d46117bf5c48ebb2b0043689f453"
DEV_PATH = "docs/paper1/dual_machine/chinese5060/OWNER27_OFFLINE_FASTTRACK_RUN_MANIFEST.json"
EVAL_ROOT = "docs/paper1/dual_machine/repro5090/owner28_eval"
ARMS = ("NONE", "RD_B2", "RD_ZH", "DATE_ONLY")
ROLES = "PCHB"
FIELDS = ("offered", "retrieved", "missed", "kept", "deleted")
DEV_LINEAGE = {"HOL-SPRING": "STATUTORY_HOLIDAYS", "HOL-LABOR": "STATUTORY_HOLIDAYS",
               "HY-ISSUER": "PUBLIC_HYGIENE", "DRV-HEAVY-AGE": "DRIVING_LICENSE"}


def blob(commit: str, path: str, expected: str) -> Any:
    data = subprocess.check_output(["git", "show", f"{commit}:{path}"])
    if hashlib.sha256(data).hexdigest() != expected:
        raise ValueError(f"Aggregate SHA mismatch for {path}")
    return json.loads(data) if path.endswith(".json") else data


def count_rows() -> list[dict[str, Any]]:
    dev = blob(DEV, DEV_PATH, "ebca241a364c75cfe9cfaebfb6832e7a97b9a856a47638b870e0ea55d7b762f4")
    receipt = blob(EVAL, f"{EVAL_ROOT}/OWNER28_EVAL_SCORE_MANIFEST.json",
                   "2ff71d24dad2904f04d0912393f80bfce563855ea9c73ff5c7ebb6c760027378")
    blob(EVAL, f"{EVAL_ROOT}/OWNER28_EVAL_INDEPENDENT_SCORE_REPORT.md", receipt["report_sha256"])
    aggregate = blob(EVAL, f"{EVAL_ROOT}/OWNER28_EVAL_SCORE_AGGREGATES.json", receipt["aggregates_sha256"])
    evaluation = aggregate["summary"]
    rows: list[dict[str, Any]] = []

    def add(batch: str, layer: str, group: str, arm: str, role: str, counts: list[int]) -> None:
        offered, hit, miss, kept, deleted = counts
        assert offered == hit + miss and hit == kept + deleted and min(counts) >= 0
        lineage = (DEV_LINEAGE[group] if batch == "Owner27_DEV" else group.split(" | ", 1)[0]) if layer == "fact" else ""
        rows.append({"batch": batch, "layer": layer, "unit": group, "lineage": lineage, "arm": arm, "role": role,
                     **dict(zip(FIELDS, counts, strict=True))})

    positions = [dev["role_array_order"].index(k) for k in ("offered", "hit", "missed", "kept", "deleted")]
    for arm in ARMS:
        buckets = [("main", "ALL", dev["arms"][arm]["role_counts"])]
        buckets += [("fact" if r["type"] == "fact_groups" else "scenario", r["id"], r["role_counts"])
                    for r in dev["strata"] if r["arm"] == arm]
        for layer, group, roles in buckets:
            for role in ROLES:
                add("Owner27_DEV", layer, group, arm, role, [roles[role][i] for i in positions])
    for layer, buckets_by_id in (("main", {"ALL": evaluation}), ("fact", evaluation["facts"]),
                                 ("scenario", evaluation["scenarios"])):
        for group, bucket in buckets_by_id.items():
            for arm in ARMS:
                for role in ROLES:
                    counts = [bucket[k][role] for k in ("offered", "retrieved", "missed")]
                    counts += [bucket["arms"][arm][k][role] for k in ("kept", "deleted")]
                    add("Owner28_EVAL", layer, group, arm, role, counts)

    for batch in ("Owner27_DEV", "Owner28_EVAL"):
        for arm in ARMS:
            selected = [r for r in rows if r["batch"] == batch and r["arm"] == arm]
            assert sum(r["retrieved"] for r in selected if r["layer"] == "main") == 160
            for overall in (r for r in selected if r["layer"] == "main"):
                for layer in ("fact", "scenario"):
                    for key in FIELDS:
                        assert overall[key] == sum(r[key] for r in selected
                                                   if r["layer"] == layer and r["role"] == overall["role"])
    assert len(rows) == 416
    assert evaluation["worlds"] == 32 and evaluation["fact_groups"] == 4
    assert aggregate["date_audit"]["corpus_date_hits"] == aggregate["date_audit"]["retrieved_date_hits"] == 0
    for role, pair in evaluation["pair_by_role"].items():
        assert sum(pair.values()) == evaluation["retrieved"][role] and pair["ZH_ONLY"] == 0
        assert pair["BOTH_KEEP"] == evaluation["arms"]["RD_ZH"]["kept"][role]
        assert pair["BOTH_KEEP"] + pair["B2_ONLY"] == evaluation["arms"]["RD_B2"]["kept"][role]
    return rows


def figure(rows: list[dict[str, Any]], out: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    labels = ["Holiday: spring", "Holiday: labor", "Public hygiene", "Driving license",
              "Patent law", "Population law (2016)", "Population law (2021)", "Work-time regulation"]
    groups = ["HOL-SPRING", "HOL-LABOR", "HY-ISSUER", "DRV-HEAVY-AGE", "PATENT_LAW | new_effective 2021-06-01",
              "POPULATION_FAMILY_PLANNING_LAW | new_effective 2016-01-01",
              "POPULATION_FAMILY_PLANNING_LAW | new_effective 2021-08-20",
              "STATE_COUNCIL_WORK_TIME | new_effective 1995-05-01"]
    lookup = {(r["unit"], r["arm"], r["role"]): r for r in rows if r["layer"] == "fact"}
    fig, axes = plt.subplots(1, 3, sharey=True, figsize=(11.2, 4.6))
    for ax, role, metric, title in zip(axes, "PCH", ("kept", "deleted", "deleted"),
                                      ("Poison retained", "Clean false deletion", "HN false deletion"), strict=True):
        for y, group in enumerate(groups):
            a, b = (lookup[group, arm, role] for arm in ("RD_B2", "RD_ZH"))
            assert a["retrieved"] == b["retrieved"] and a["retrieved"]
            left, right = (100 * r[metric] / r["retrieved"] for r in (a, b))
            ax.plot([left, right], [y, y], color="#AEB8C4", lw=1.5, zorder=1)
            ax.scatter(left, y, s=42, c="#215386", marker="o", zorder=2)
            ax.scatter(right, y, s=37, c="#B44D24", marker="D", zorder=3, edgecolor="white", linewidth=.5)
        ax.axhline(3.5, color="#6E7781", lw=1, ls="--")
        ax.set_title(title, loc="left", fontweight="bold", fontsize=11)
        ax.set_xlim(-4, 104)
        ax.set_xticks([0, 25, 50, 75, 100])
        ax.set_xlabel("% of retrieved role")
        ax.grid(axis="x", color="#E5E9EF", lw=.8)
        ax.spines[["top", "right", "left"]].set_visible(False)
        ax.tick_params(axis="y", length=0)
    axes[0].set_yticks(range(8), labels)
    axes[0].invert_yaxis()
    fig.suptitle("RAGDefender Chinese adaptation on shared TopK5", x=.2, ha="left", fontsize=15, fontweight="bold")
    fig.text(.2, .885, "Above divider: Owner27 DEV   |   Below divider: Owner28 independent provisional EVAL", fontsize=9)
    fig.legend(handles=[Line2D([], [], marker="o", color="#215386", ls="", label="RD_B2"),
                        Line2D([], [], marker="D", color="#B44D24", ls="", label="RD_ZH")],
               loc="lower center", bbox_to_anchor=(.58, .008), ncol=2, frameon=False)
    fig.subplots_adjust(left=.20, right=.985, bottom=.19, top=.78, wspace=.25)
    fig.savefig(out / "BENCHMARK_V01_FACT_GROUPS.png", dpi=300)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    rows = count_rows()
    with (args.out / "BENCHMARK_V01_COUNTS.csv").open("x", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    figure(rows, args.out)
    print("Verified 416 aggregate rows, 8 fact groups and 3 metric panels.")


if __name__ == "__main__":
    main()
