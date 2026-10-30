"""Build the owner report from pinned, redacted Git records; never load a model.

Use system Python for --figures, and the bundled ReportLab Python for --pdf.
No installation, network, private raw access, score rewriting, or experiment run.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import math
import os
import re
import subprocess
from pathlib import Path
from statistics import NormalDist
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
PIN = "4dc9161e79b79ece70a7c17144175a19b985770d"
STAGE = "docs/research/stage6_1_hidden_knowledge_poisoning/"
VACE = STAGE + "core144/vace_lite/"
MAIN = "PAPER1_L0_D1_BASELINE_OWNER_REPORT_V1"
SOURCES = [
    ("SRC-FULL01", VACE + "VACE_L0_FULL01_D1_EXECUTION_V1.md"),
    ("SRC-AUDIT", VACE + "VACE_L0_FULL01_OFFLINE_AUDIT_V1.md"),
    ("SRC-ALIGN-RESULT", VACE + "VACE_L0_ORACLE_CLAIM_ALIGNMENT_RESULT_V1.md"),
    ("SRC-ALIGN-PROTOCOL", VACE + "VACE_L0_ORACLE_CLAIM_ALIGNMENT_V1.md"),
    ("SRC-R05", VACE + "VACE_L0_R05_EXPLICIT_GQA_PRECHECK_V1.md"),
    ("SRC-R06", VACE + "VACE_L0_R06_ALLOCATOR_STABILITY_V1.md"),
    ("SRC-DEVICE", VACE + "VACE_L0_HARDWARE_PREFLIGHT_BLOCKER_V1.md"),
    ("SRC-R01", VACE + "VACE_L0_5090_SYNTHETIC_GATE_BLOCKER_V1.md"),
    ("SRC-PARSER", "src/llmguard/domains/retrieval/hidden_poisoning/method_engineering/llm_verification.py"),
    ("SRC-EVAL-FULL", "scripts/research/evaluate_l0_worker.py"),
    ("SRC-EVAL-ALIGN", "scripts/research/evaluate_oracle_align.py"),
    ("SRC-R02", VACE + "VACE_L0_R02_CUDA_OOM_BLOCKER_V1.md"),
    ("SRC-D1-DEV", STAGE + "core144/PAPER1_D1_FIRST_DETECTION_RESULTS_RECORD_V1.md"),
    ("SRC-RPA", STAGE + "human/research_plan_authority.md"),
    ("SRC-R03", VACE + "VACE_L0_R03_LENGTH_CAP_DISCLOSURE_V1.md"),
    ("SRC-ADAPTER", "src/llmguard/domains/retrieval/hidden_poisoning/method_engineering/explicit_gqa_efficient_sdpa.py"),
    ("SRC-POLICY-FULL", "configs/research/paper1_l0/worker_policy_full01_v1.json"),
    ("SRC-POLICY-ALIGN", "configs/research/paper1_l0/worker_policy_oracle_align01_v1.json"),
    ("SRC-MODEL", "configs/research/paper1_l0/qwen_official_manifest_v1.json"),
    ("SRC-BASELINE-MATRIX", STAGE + "method_engineering/PAPER1_BASELINE_MATRIX_V1.md"),
]


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=ROOT)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def dump(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def reviewed() -> dict:
    return json.loads((HERE / "RESULTS_REVIEWED_V1.json").read_text("utf-8"))


def wilson(k: int, n: int) -> tuple[float, float]:
    z = NormalDist().inv_cdf(0.975)
    p = k / n
    den = 1 + z * z / n
    mid = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return mid - half, mid + half


def metadata() -> None:
    data = reviewed()
    evidence = HERE / "evidence"
    evidence.mkdir(exist_ok=True)
    register: list[dict[str, Any]] = []
    source_text: dict[str, str] = {}
    for source_id, path in SOURCES:
        content = git("show", PIN + ":" + path)
        source_text[source_id] = content.decode("utf-8")
        suffix = ".md" if path.endswith(".md") else ".txt"
        target = evidence / (source_id + suffix)
        target.write_bytes(content)
        register.append({"id": source_id, "repo_path": path, "evidence_commit": PIN,
                         "git_blob_sha1": git("rev-parse", PIN + ":" + path).decode().strip(),
                         "snapshot": target.relative_to(HERE).as_posix(), "bytes": len(content),
                         "sha256": digest(content), "verification": "PINNED_GIT_BYTES_LOCALLY_HASHED",
                         "url": f"https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/{PIN}/{path}"})
    expected = data["fixed_model"]
    assert digest(git("show", PIN + ":" + SOURCES[8][1])) == expected["parser_file_sha256"]
    assert digest(git("show", PIN + ":" + SOURCES[15][1])) == expected["adapter_sha256"]
    for artifact in data["private_artifacts"]:
        assert artifact["sha256"] in source_text[artifact["source_id"]], artifact
        artifact["verification"] = "SOURCE_REPORTED_NOT_LOCALLY_REHASHED"
        artifact["custodian"] = "5090 Worker private run directory; not present on control plane"
    dump(HERE / "SOURCE_REGISTER_V1.json", {
        "as_of_commit": PIN, "sources": register,
        "private_artifacts": data["private_artifacts"],
        "private_verification_limit": data["private_artifact_verification"],
        "unavailable_primary": [{"id": "U1", "description": "User-supplied R04 Worker report and R03 completion attestation in this conversation", "original_file_not_available_here": True, "original_sha256": None}],
    })
    main_path = HERE / (MAIN + ".md")
    main_text = main_path.read_text("utf-8")
    for source in register:
        original_relative = Path(os.path.relpath(ROOT / source["repo_path"], HERE)).as_posix()
        main_text = main_text.replace("](" + original_relative + ")", "](" + source["snapshot"] + ")")
    main_path.write_text(main_text, encoding="utf-8", newline="\n")
    fields = ["method", "source_id", "S1_TP", "S1_N", "S2_TP", "S2_N", "S3_TP", "S3_N", "TP", "Poison_N", "Recall", "Recall_Wilson95_low", "Recall_Wilson95_high", "Clean_FP", "Clean_N", "Clean_FPR", "HN_FP", "HN_N", "HN_FPR", "Precision", "SUPPORT", "CONTRADICT", "INSUFFICIENT", "strict_triplets", "Poison_SUPPORT", "JSON_errors", "citation_errors", "model_own_insufficient", "input_errors"]
    with (HERE / "RESULTS_TABLE_V1.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for m in data["methods"]:
            lo, hi = wilson(m["tp"], 40)
            row = {"method": m["id"], "source_id": m["source_id"], "TP": m["tp"], "Poison_N": 40, "Recall": m["tp"] / 40, "Recall_Wilson95_low": lo, "Recall_Wilson95_high": hi,
                   "Clean_FP": m["clean_fp"], "Clean_N": 40, "Clean_FPR": m["clean_fp"] / 40,
                   "HN_FP": m["hn_fp"], "HN_N": 40, "HN_FPR": m["hn_fp"] / 40,
                   "Precision": m["tp"] / m["contradict"], "SUPPORT": m["support"], "CONTRADICT": m["contradict"], "INSUFFICIENT": m["insufficient"],
                   "strict_triplets": m["strict_triplets"], "Poison_SUPPORT": m["poison_support"], "JSON_errors": m["json_errors"], "citation_errors": m["citation_errors"], "model_own_insufficient": m["model_insufficient_without_error"], "input_errors": m["input_errors"]}
            for i, n in enumerate([12, 15, 13]):
                row[f"S{i + 1}_TP"] = m["s_tp"][i]
                row[f"S{i + 1}_N"] = n
            writer.writerow(row)
    print(f"Pinned sources: {len(register)}; no private raw files loaded.")


def figures() -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import FontProperties
    from matplotlib.ticker import PercentFormatter

    data = reviewed()
    font = FontProperties(fname="C:/Windows/Fonts/msyh.ttc")
    plt.rcParams.update({"font.family": font.get_name(), "axes.spines.top": False, "axes.spines.right": False, "axes.unicode_minus": False, "font.size": 10})
    target = HERE / "figures"
    target.mkdir(exist_ok=True)
    methods = data["methods"]
    colors = ["#46778F", "#1E4D70", "#C07535"]
    labels = ["F5\n直接核验", "Oracle\n直接核验", "Oracle\n逐断言提示"]
    fig, axes = plt.subplots(1, 3, figsize=(10.4, 4.0), sharey=True)
    for ax, field, title in zip(axes, ["tp", "clean_fp", "hn_fp"], ["Poison 检出率", "Clean 误报率", "HN 误报率"]):
        for i, m in enumerate(methods):
            p = m[field] / 40
            lo, hi = wilson(m[field], 40)
            ax.bar(i, p, color=colors[i], width=.62, zorder=2)
            ax.errorbar(i, p, yerr=[[p - lo], [hi - p]], color="#243746", capsize=4, linewidth=1.1, zorder=3)
            ax.text(i, hi + .022, f'{m[field]}/40\n{p:.1%}', ha="center", va="bottom", fontsize=9)
        ax.set_xticks(range(3), labels)
        ax.set_title(title, fontsize=12, pad=14)
        ax.set_ylim(0, .68)
        ax.yaxis.set_major_formatter(PercentFormatter(1))
        ax.grid(axis="y", alpha=.16, zorder=0)
    axes[0].set_ylabel("比例；误差线为样本级 Wilson 95%")
    fig.suptitle("逐断言提示的检出增量伴随合法知识误报增加", fontsize=14, y=.98)
    fig.text(.5, .015, "同一 D1 开发集；每类 n=40。Oracle 对照仅改变固定 system 后缀。非正式测试。", ha="center", fontsize=9, color="#526273")
    fig.tight_layout(rect=[0, .075, 1, .91])
    fig.savefig(target / "detection_and_fpr_v1.png", dpi=180, facecolor="white")
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(9.4, 3.9))
    bottom = [0, 0, 0]
    components = [("json_errors", "JSON 失败", "#A5B2BE"), ("citation_errors", "引用相关失败", "#46778F"), ("model_insufficient_without_error", "模型自身缺证（无错误）", "#C07535")]
    for field, label, color in components:
        values = [m[field] for m in methods]
        ax.barh(range(3), values, left=bottom, label=label, height=.56, color=color)
        for i, value in enumerate(values):
            if value:
                ax.text(bottom[i] + value / 2, i, str(value), ha="center", va="center", fontsize=10, color="white" if field == "citation_errors" else "#172B3A")
        bottom = [a + b for a, b in zip(bottom, values)]
    for i, m in enumerate(methods):
        ax.text(m["insufficient"] + .8, i, f'合计 {m["insufficient"]}/120', va="center", fontsize=10)
    ax.set_yticks(range(3), ["F5 直接核验", "Oracle 直接核验", "Oracle 逐断言提示"])
    ax.invert_yaxis()
    ax.set_xlim(0, 56)
    ax.set_xlabel("最终 INSUFFICIENT 条数；全部 120 条保留原分母")
    ax.set_title("未决输出主要来自校验失败，不能等同于模型主动谨慎", fontsize=13, pad=15)
    ax.legend(loc="upper center", bbox_to_anchor=(.5, -.20), ncol=3, frameon=False, fontsize=9)
    ax.grid(axis="x", alpha=.16)
    ax.set_axisbelow(True)
    fig.tight_layout(rect=[0, .08, 1, 1])
    fig.savefig(target / "insufficient_breakdown_v1.png", dpi=180, facecolor="white", bbox_inches="tight")
    plt.close(fig)
    print("Two static scientific figures exported.")


def pdf() -> None:
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_LEFT
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable, KeepTogether

    pdfmetrics.registerFont(TTFont("OwnerYaHei", "C:/Windows/Fonts/msyh.ttc", subfontIndex=0))
    output = HERE / "output/pdf"
    output.mkdir(parents=True, exist_ok=True)
    w = A4[0] - 96
    styles = {
        "body": ParagraphStyle("body", fontName="OwnerYaHei", fontSize=9.3, leading=15, spaceAfter=7, wordWrap="CJK", splitLongWords=True),
        "title": ParagraphStyle("title", fontName="OwnerYaHei", fontSize=22, leading=29, textColor=colors.HexColor("#173D58"), spaceAfter=13, wordWrap="CJK", keepWithNext=True),
        "h2": ParagraphStyle("h2", fontName="OwnerYaHei", fontSize=15, leading=21, spaceBefore=13, spaceAfter=8, textColor=colors.HexColor("#173D58"), wordWrap="CJK", keepWithNext=True),
        "h3": ParagraphStyle("h3", fontName="OwnerYaHei", fontSize=11.5, leading=17, spaceBefore=9, spaceAfter=5, textColor=colors.HexColor("#246482"), wordWrap="CJK", keepWithNext=True),
        "cell": ParagraphStyle("cell", fontName="OwnerYaHei", fontSize=7.2, leading=11, wordWrap="CJK", splitLongWords=True, alignment=TA_LEFT),
        "small": ParagraphStyle("small", fontName="OwnerYaHei", fontSize=7.5, leading=11, wordWrap="CJK", textColor=colors.HexColor("#526273"), spaceAfter=6),
    }
    pinned_sources = json.loads((HERE / "SOURCE_REGISTER_V1.json").read_text("utf-8"))["sources"]
    snapshot_urls = {source["snapshot"]: source["url"] for source in pinned_sources}
    def inline(value: str) -> str:
        value = html.escape(value)
        value = re.sub(r"\*\*(.+?)\*\*", r'<font color="#173D58">\1</font>', value)
        value = re.sub(r"`([^`]+)`", r'<font size="8">\1</font>', value)
        def link(match: re.Match) -> str:
            title, path = match.group(1), html.unescape(match.group(2))
            if path.startswith("https://"):
                url = path
            else:
                resolved = (HERE / path).resolve()
                if path in snapshot_urls:
                    url = snapshot_urls[path]
                elif resolved.is_relative_to(HERE):
                    return title
                elif resolved.is_relative_to(ROOT):
                    url = "https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/" + PIN + "/" + resolved.relative_to(ROOT).as_posix()
                else:
                    return title
            return '<link href="' + html.escape(url, quote=True) + '" color="#246482">' + title + "</link>"
        return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, value)
    def p(text: str, style: str = "body"):
        return Paragraph(inline(text), styles[style])
    lines = (HERE / (MAIN + ".md")).read_text("utf-8").splitlines()
    story = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line.startswith("!["):
            image_match = re.search(r"\]\(([^)]+)\)", line)
            if image_match is None:
                raise ValueError("INVALID_MARKDOWN_IMAGE")
            path = image_match.group(1)
            im = Image(str(HERE / path))
            im.drawHeight *= w / im.drawWidth
            im.drawWidth = w
            story.extend([Spacer(1, 5), im, Spacer(1, 8)])
        elif line.startswith("| "):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                vals = [v.strip() for v in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r"[:\- ]+", v) for v in vals):
                    rows.append([Paragraph(inline(v).replace(" = ", "<br/>").replace("Oracle-ClaimAligned", "Oracle<br/>ClaimAligned"), styles["cell"]) for v in vals])
                i += 1
            n = len(rows[0])
            if n >= 8:
                widths = [76] + [(w - 76) / (n - 1)] * (n - 1)
            elif n == 3:
                widths = [w * .23, w * .38, w * .39]
            elif n == 2:
                widths = [w * .24, w * .76]
            else:
                widths = [w / n] * n
            table = Table(rows, colWidths=widths, repeatRows=1, hAlign="LEFT")
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E7EFF4")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F5F8FA")]),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LINEBELOW", (0, 0), (-1, 0), .65, colors.HexColor("#ABC0CD")),
                ("LINEBELOW", (0, 1), (-1, -1), .25, colors.HexColor("#DFE7ED")),
                ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]))
            story.append(KeepTogether([table, Spacer(1, 9)]))
            continue
        elif line.startswith("# "):
            story.extend([p(line[2:], "title"), HRFlowable(width="100%", thickness=2, color=colors.HexColor("#C07535")), Spacer(1, 12)])
        elif line.startswith("## "):
            story.append(p(line[3:], "h2"))
        elif line.startswith("### "):
            story.append(p(line[4:], "h3"))
        elif line.startswith("- "):
            story.append(p("• " + line[2:]))
        elif line.startswith("> "):
            story.append(p(line[2:]))
        else:
            story.append(p(line))
        i += 1
    def decorate(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#D5E0E8"))
        canvas.line(48, 43, A4[0] - 48, 43)
        canvas.setFont("OwnerYaHei", 7.5)
        canvas.setFillColor(colors.HexColor("#526273"))
        canvas.drawString(48, 30, "LLMGuard / D1-L0 开发基线 / 项目负责人审阅稿")
        canvas.drawRightString(A4[0] - 48, 30, f"2026-10-31   {doc.page}")
        canvas.restoreState()
    doc = SimpleDocTemplate(str(output / (MAIN + ".pdf")), pagesize=A4, rightMargin=48, leftMargin=48, topMargin=45, bottomMargin=58,
                            title="D1核验基线阶段报告：固定提示未带来无额外误报的改善", author="LLMGuard / Control Plane", subject="D1 development evidence and owner review, not formal scientific acceptance")
    doc.build(story, onFirstPage=decorate, onLaterPages=decorate)
    print(output / (MAIN + ".pdf"))


def validate() -> None:
    data = reviewed()
    checks = []
    def check(name: str, condition: bool):
        checks.append({"check": name, "pass": bool(condition)})
    for m in data["methods"]:
        check(m["id"] + " stratum TP sum", sum(m["s_tp"]) == m["tp"])
        check(m["id"] + " verdict denominator", m["support"] + m["contradict"] + m["insufficient"] == 120)
        check(m["id"] + " confusion reconciliation", m["tp"] + m["clean_fp"] + m["hn_fp"] == m["contradict"])
        check(m["id"] + " insufficient components", m["json_errors"] + m["citation_errors"] + m["model_insufficient_without_error"] == m["insufficient"])
        check(m["id"] + " historical HN", sum(m["historical_hn"][k] for k in ["support", "contradict", "insufficient"]) == 11)
        check(m["id"] + " Wilson valid", 0 <= wilson(m["tp"], 40)[0] <= m["tp"] / 40 <= wilson(m["tp"], 40)[1] <= 1)
    old, new = data["methods"][1:]
    pair = data["paired_claim_alignment"]
    check("paired TP gain-loss", pair["gained_tp"] - pair["lost_tp"] == new["tp"] - old["tp"] == 1)
    check("paired FP gain-loss", pair["gained_fp"] - pair["removed_fp"] == new["clean_fp"] + new["hn_fp"] - old["clean_fp"] - old["hn_fp"] == 5)
    check("preregistered benefit false", not (new["tp"] > old["tp"] and new["clean_fp"] <= old["clean_fp"] and new["hn_fp"] <= old["hn_fp"]))
    check("strict triplets unchanged", old["strict_triplets"] == new["strict_triplets"] == 8)
    check("audit pair partition", sum(data["offline_audit"]["pair_partition"].values()) == 120)
    check("F5 primary error sum", sum(data["offline_audit"]["f5_first_error_counts"].values()) == 40)
    check("Oracle primary error sum", sum(data["offline_audit"]["oracle_first_error_counts"].values()) == 17)
    check("360 unique run predictions not 360 unique candidates", sum(r["model_calls"] for r in data["run_costs"]) == 360 and data["cohort"]["candidates"] == 120)
    check("FULL01 hard memory limit", data["run_costs"][0]["peak_reserved_bytes"] < 30 * 2**30)
    check("FULL01 headroom honestly below 1GiB", 0 < 30 * 2**30 - data["run_costs"][0]["peak_reserved_bytes"] < 2**30)
    check("unreported interval remains null", pair["precision_difference_family_ci"] is None and new["reported_recall_family_ci"] is None)
    for src in json.loads((HERE / "SOURCE_REGISTER_V1.json").read_text("utf-8"))["sources"]:
        check(src["id"] + " snapshot integrity", digest((HERE / src["snapshot"]).read_bytes()) == src["sha256"] == digest(git("show", PIN + ":" + src["repo_path"])))
    text = (HERE / (MAIN + ".md")).read_text("utf-8")
    dump(HERE / "REPORT_VALIDATION_V1.json", {"status": "VALIDATION_RUNNING"})
    for link in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", text):
        if not re.match(r"https?://", link):
            check("report link " + link, (HERE / link.split("#")[0]).exists())
    check("no model imports", not re.search(r"^\s*(?:from|import) (?:torch|transformers)", Path(__file__).read_text("utf-8"), re.M))
    check("original code and data diff empty", not git("diff", PIN, "--", "src", "tests", "configs", "data", "scripts/research/paper1_l0*", "scripts/research/evaluate*"))
    payload = {"report": MAIN, "as_of_commit": PIN, "source_level": data["source_class"], "checks": checks, "all_pass": all(r["pass"] for r in checks), "not_performed": ["private raw replay", "bootstrap reproduction", "new GPU/model call", "owner final scientific acceptance"], "pdf_visual_review": "RECORDED_SEPARATELY_IN_DELIVERY_QA"}
    dump(HERE / "REPORT_VALIDATION_V1.json", payload)
    print(json.dumps({"checks": len(checks), "all_pass": payload["all_pass"], "failures": [r for r in checks if not r["pass"]]}, ensure_ascii=False))
    if not payload["all_pass"]:
        raise SystemExit(1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=["metadata", "figures", "pdf", "validate"])
    args = parser.parse_args()
    {"metadata": metadata, "figures": figures, "pdf": pdf, "validate": validate}[args.phase]()


if __name__ == "__main__":
    main()
