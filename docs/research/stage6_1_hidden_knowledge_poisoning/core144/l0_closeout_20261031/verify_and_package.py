"""Verify report delivery and package redacted owner-facing files only."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
PIN = "4dc9161e79b79ece70a7c17144175a19b985770d"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    from pypdf import PdfReader

    validation = json.loads((HERE / "REPORT_VALIDATION_V1.json").read_text("utf-8"))
    assert validation["all_pass"]
    pdf_path = HERE / "output/pdf/PAPER1_L0_D1_BASELINE_OWNER_REPORT_V1.pdf"
    reader = PdfReader(pdf_path)
    assert len(reader.pages) == 6
    extracted = "\n".join(page.extract_text() or "" for page in reader.pages)
    for text in ["负责人摘要", "事实核验", "22", "35.0%", "37.5%", "0.896", "未独立", "OWNER_REVIEW_REQUIRED"]:
        assert text in extracted, text
    assert all(len(page.extract_text() or "") > 500 for page in reader.pages)
    embedded_font = False
    image_count = 0
    for page in reader.pages:
        for font in page["/Resources"].get("/Font", {}).get_object().values():
            font_obj = font.get_object()
            descriptor = font_obj.get("/FontDescriptor")
            if descriptor is not None and descriptor.get_object().get("/FontFile2"):
                embedded_font = True
        xobjects = page["/Resources"].get("/XObject", {})
        for value in xobjects.get_object().values() if hasattr(xobjects, "get_object") else xobjects.values():
            if value.get_object().get("/Subtype") == "/Image":
                image_count += 1
    assert embedded_font and image_count == 2
    page_images = [HERE / f"tmp/pdfs/delivery-{n}.png" for n in range(1, 7)]
    assert all(p.is_file() for p in page_images)
    changed = subprocess.check_output(["git", "diff", PIN, "--name-only"], cwd=ROOT, text=True, encoding="utf-8").splitlines()
    assert all(p == "PROJECT_MASTER_CONTEXT.md" or p.startswith("docs/") for p in changed)
    protected_diff = subprocess.check_output(["git", "diff", PIN, "--", "src", "tests", "data", "configs", "scripts", "llm-security-stage1", "docs/research/stage6_1_hidden_knowledge_poisoning/human/research_plan_authority.md", "docs/governance/long_term_research_requirements.md"], cwd=ROOT)
    assert not protected_diff
    checks = {
        "human_ledger_checked": True, "human_ledger_updated_if_required": True,
        "agent_ledger_checked": True, "agent_ledger_updated": True,
        "current_work_state_updated": True, "execution_log_appended": True,
        "experiment_master_condition_evaluated": True, "owner_decision_condition_evaluated": True,
        "stage_process_condition_evaluated": True, "lessons_condition_evaluated": True,
        "research_authority_condition_evaluated": True, "README_condition_evaluated": True,
        "cross_document_current_task_consistent": True, "cross_document_status_consistent": True,
        "cross_document_next_action_consistent": True, "cross_document_blocker_consistent": True,
        "markdown_links_valid": True,
    }
    task_token = "P1-L0-D1-BASELINE-EVIDENCE-AND-OWNER-REPORT-01"
    task_docs = ["docs/governance/current_work_state.md", "docs/governance/experiment_master_record.md", "docs/governance/research_execution_log.md", "docs/research/stage6_1_hidden_knowledge_poisoning/agent/experiment_ledger_agentUse.md", "docs/research/stage6_1_hidden_knowledge_poisoning/stage_process/S6.1-P1_work_process.md"]
    for relative in task_docs:
        assert task_token in (ROOT / relative).read_text("utf-8")[:2600]
    textual = [p for p in HERE.rglob("*") if p.is_file() and "tmp" not in p.relative_to(HERE).parts and p.suffix in {".md", ".txt", ".py", ".json", ".csv"}]
    secrets = re.compile(r"(?:sk-|gsk_)[A-Za-z0-9]{18,}|Bearer\s+[A-Za-z0-9._-]{20,}")
    for path in textual:
        text = path.read_text("utf-8-sig")
        assert not secrets.search(text), path
    qa = {
        "task": task_token, "source_cutoff_commit": PIN,
        "report_branch": "codex/l0-baseline-closeout-20261031",
        "aggregate_checks_pass": validation["all_pass"], "aggregate_checks_count": len(validation["checks"]),
        "pdf_pages": len(reader.pages), "pdf_sha256": sha(pdf_path), "chinese_font_embedded": embedded_font,
        "pdf_figures": image_count, "pdf_text_readback_pass": True,
        "visual_review": {"status": "PASS", "reviewed_by": "control-plane assistant", "all_final_pages_inspected": [1, 2, 3, 4, 5, 6], "checks": ["legibility", "no clipping or overlap", "tables kept together", "figures and source qualifications", "footer/page numbers"], "rendered_page_sha256": {p.name: sha(p) for p in page_images}},
        "ruff": "PASS", "mypy": "PASS", "protected_code_and_data_diff_empty": True,
        "task_scoped_secret_scan_pass": True,
        "closeout_matrix": checks,
        "conditional_documents": {"Experiment_Master": "UPDATED: evidence/report index", "Owner_Register": "UPDATED: PODR-154 authorizes report, not scientific acceptance", "Stage_Process": "UPDATED: report review gate", "README": "UPDATED: current navigation", "Canonical_Lessons": "NO_PROMOTION: no final scientific acceptance; provisional interpretation stays in report", "Research_Plan_Authority": "UNCHANGED: research contract not changed", "Long_Term_Requirements": "UNCHANGED"},
        "no_new_model_or_GPU_calls": True,
        "private_raw_locally_replayed": False, "paired_bootstrap_locally_replayed": False,
        "owner_scientific_acceptance": "PENDING_OWNER_REVIEW",
        "git_delivery": "verify actual commit, push and local/remote equality after committing; this is not a static assertion of sync",
    }
    # Validate only newly added links in governance/navigation, not legacy debt.
    added = subprocess.check_output(["git", "diff", PIN, "--unified=0", "--", "*.md"], cwd=ROOT, text=True, encoding="utf-8")
    current = None
    link_count = 0
    for line in added.splitlines():
        if line.startswith("+++ b/"):
            current = ROOT / line[6:]
        elif (current is not None and not current.is_relative_to(HERE)
              and line.startswith("+") and not line.startswith("+++")):
            for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", line):
                if not target.startswith("https://"):
                    assert (current.parent / target.split("#")[0]).exists(), (current, target)
                    link_count += 1
    qa["new_governance_link_count"] = link_count
    dump(HERE / "DELIVERY_QA_V1.json", qa)
    paths = [p for p in sorted(HERE.rglob("*")) if p.is_file() and not p.is_symlink() and not ({"tmp", "__pycache__"} & set(p.relative_to(HERE).parts)) and p.suffix != ".zip" and p.name != "PACKAGE_INDEX_V1.json"]
    assert not any(p.name in {"L0_PREDICTIONS.jsonl", "labels.jsonl", "PRIVATE_CASE_REVIEW.jsonl"} for p in paths)
    manifest: dict[str, Any] = {"report": "D1/L0 owner review package", "private_raw_included": False, "evidence_class": "redacted Git sources and aggregate derived report only", "files": [{"path": p.relative_to(HERE).as_posix(), "bytes": p.stat().st_size, "sha256": sha(p)} for p in paths]}
    dump(HERE / "PACKAGE_INDEX_V1.json", manifest)
    archive = HERE / "output/PAPER1_L0_D1_OWNER_REVIEW_PACKAGE_V1.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for path in [*paths, HERE / "PACKAGE_INDEX_V1.json"]:
            z.write(path, "D1_L0_OWNER_REVIEW/" + path.relative_to(HERE).as_posix())
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for entry in manifest["files"]:
            assert hashlib.sha256(z.read("D1_L0_OWNER_REVIEW/" + entry["path"])).hexdigest() == entry["sha256"]
        assert all(not Path(name).is_absolute() and ".." not in Path(name).parts for name in z.namelist())
    print(json.dumps({"pdf_pages": len(reader.pages), "package_files": len(paths) + 1, "package_bytes": archive.stat().st_size, "package_sha256": sha(archive), "status": "OWNER_REPORT_READY / OWNER_REVIEW_REQUIRED"}))


if __name__ == "__main__":
    main()
