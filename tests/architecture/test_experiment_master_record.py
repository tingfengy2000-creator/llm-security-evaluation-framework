from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GOVERNANCE = ROOT / "docs" / "governance"
MASTER_RECORD = GOVERNANCE / "experiment_master_record.md"
WINDOWS_ABSOLUTE_PATH = re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:[\\\\/]")
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
SECRET_SHAPES = (
    re.compile(r"\bgsk_[A-Za-z0-9_-]+"),
    re.compile(r"(?<![A-Za-z0-9])sk-[A-Za-z0-9]{8,}"),
    re.compile(r"\bBearer\s+[A-Za-z0-9._-]{8,}"),
)
RUN_LEDGER_HEADING = "### 8.1 已回填运行"
RUN_LEDGER_HEADER = (
    "Record ID",
    "Original Run ID",
    "日期",
    "Stage/Task",
    "Run Type",
    "模型/Provider",
    "状态",
    "核心指标",
    "原始证据",
    "结论边界",
)
RUN_TYPES = frozenset({"FORMAL_EXPERIMENT", "ENGINEERING_VALIDATION"})
LEDGER_COUNT_SUMMARY = re.compile(
    r"\*\*账本统计（由上表实际记录计算）\*\*："
    r"FORMAL_EXPERIMENT = (?P<formal>\d+)；"
    r"ENGINEERING_VALIDATION = (?P<engineering>\d+)。"
)


def _parse_markdown_table_row(line: str) -> tuple[str, ...]:
    """Parse one pipe-delimited Markdown row while respecting escaped pipes."""
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        raise ValueError("Markdown table rows must start and end with a pipe")

    cells: list[str] = []
    current: list[str] = []
    escaped = False
    for character in stripped[1:-1]:
        if escaped:
            current.append(character)
            escaped = False
        elif character == "\\":
            escaped = True
        elif character == "|":
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(character)
    if escaped:
        current.append("\\")
    cells.append("".join(current).strip())
    return tuple(cells)


def _extract_run_ledger(markdown: str) -> tuple[tuple[str, ...], tuple[tuple[str, ...], ...]]:
    """Return the fixed-schema ledger directly below the Stage 8.1 heading."""
    lines = markdown.splitlines()
    heading_index = lines.index(RUN_LEDGER_HEADING)
    header_index = next(
        index
        for index in range(heading_index + 1, len(lines))
        if lines[index].strip().startswith("| Record ID |")
    )
    header = _parse_markdown_table_row(lines[header_index])
    separator = _parse_markdown_table_row(lines[header_index + 1])
    if len(separator) != len(header) or not all(set(cell) <= {"-", ":"} for cell in separator):
        raise ValueError("Run ledger header must be followed by a Markdown separator")

    rows: list[tuple[str, ...]] = []
    for line in lines[header_index + 2 :]:
        if not line.strip():
            break
        if not line.strip().startswith("|"):
            break
        rows.append(_parse_markdown_table_row(line))
    return header, tuple(rows)


class ExperimentMasterRecordTests(unittest.TestCase):
    def test_single_master_record_exists_without_forbidden_duplicates(self) -> None:
        self.assertTrue(MASTER_RECORD.is_file())

        forbidden_duplicates = (
            GOVERNANCE / "experiment_overview.md",
            GOVERNANCE / "master_experiment_plan.md",
            GOVERNANCE / "experiment_master_plan.md",
            GOVERNANCE / "experiment_tracking.md",
            GOVERNANCE / "project_experiment_record.md",
            GOVERNANCE / "research_experiment_log.md",
        )
        for path in forbidden_duplicates:
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertFalse(path.exists())

    def test_canonical_entrypoints_reference_the_master_record(self) -> None:
        paths_and_references = (
            (ROOT / "AGENTS.md", "docs/governance/experiment_master_record.md"),
            (
                GOVERNANCE / "context_recovery_protocol.md",
                "docs/governance/experiment_master_record.md",
            ),
            (
                ROOT / "PROJECT_MASTER_CONTEXT.md",
                "docs/governance/experiment_master_record.md",
            ),
            (
                GOVERNANCE / "current_work_state.md",
                "docs/governance/experiment_master_record.md",
            ),
            (
                ROOT / "stages" / "stage6_rag_security" / "README.md",
                "../../docs/governance/experiment_master_record.md",
            ),
        )

        for path, reference in paths_and_references:
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertIn(reference, text)

    def test_master_record_has_permanent_governance_sections(self) -> None:
        text = MASTER_RECORD.read_text(encoding="utf-8")
        required_sections = (
            "五分钟项目快照",
            "文档职责矩阵",
            "项目阶段路线图",
            "实验与验证分类",
            "指标字典",
            "正式运行总账",
            "Blocker Register",
            "Approval Gate Register",
            "当前结论边界",
            "证据地图",
            "项目交接指南",
            "每次运行记录模板",
            "持续更新协议",
            "Change Log",
        )
        for section in required_sections:
            with self.subTest(section=section):
                self.assertIn(section, text)

        self.assertIn("控制面、索引和汇总入口", text)
        self.assertIn("不是原始数据仓库", text)
        self.assertIn("工程验证证明代码满足契约和边界", text)
        self.assertIn("不直接证明安全防护效果", text)

    def test_run_ledger_has_a_stable_ten_column_schema(self) -> None:
        text = MASTER_RECORD.read_text(encoding="utf-8")
        header, rows = _extract_run_ledger(text)
        self.assertEqual(RUN_LEDGER_HEADER, header)
        self.assertTrue(rows)

        record_ids: set[str] = set()
        counts = {run_type: 0 for run_type in RUN_TYPES}
        for row in rows:
            with self.subTest(record_id=row[0] if row else "<missing>"):
                self.assertEqual(len(header), len(row))
                record_id, _, _, _, run_type, model_provider, status, *_ = row
                self.assertTrue(record_id)
                self.assertNotIn(record_id, record_ids)
                record_ids.add(record_id)

                normalized_run_type = run_type.strip("`")
                self.assertIn(normalized_run_type, RUN_TYPES)
                self.assertNotRegex(
                    normalized_run_type.casefold(),
                    r"groq|mock|llama|test\.|completed|failed|invalid|excluded",
                )
                self.assertTrue(model_provider)
                self.assertTrue(status)
                self.assertNotRegex(
                    model_provider.casefold(),
                    r"^(completed|failed|invalid|excluded)$",
                )
                counts[normalized_run_type] += 1

        summary_match = LEDGER_COUNT_SUMMARY.search(text)
        self.assertIsNotNone(summary_match)
        assert summary_match is not None
        self.assertEqual(counts["FORMAL_EXPERIMENT"], int(summary_match["formal"]))
        self.assertEqual(
            counts["ENGINEERING_VALIDATION"], int(summary_match["engineering"])
        )

    def test_master_record_is_portable_and_secret_free(self) -> None:
        text = MASTER_RECORD.read_text(encoding="utf-8")
        self.assertIsNone(WINDOWS_ABSOLUTE_PATH.search(text))
        self.assertNotIn("/home/", text)
        for secret_shape in SECRET_SHAPES:
            with self.subTest(secret_shape=secret_shape.pattern):
                self.assertIsNone(secret_shape.search(text))

    def test_master_record_relative_links_resolve(self) -> None:
        text = MASTER_RECORD.read_text(encoding="utf-8")
        for target in MARKDOWN_LINK.findall(text):
            if "://" in target or target.startswith("#"):
                continue
            path_part = target.split("#", maxsplit=1)[0]
            if not path_part:
                continue
            candidate = (MASTER_RECORD.parent / path_part).resolve()
            with self.subTest(target=target):
                self.assertTrue(candidate.exists(), target)

    def test_dense_retriever_acceptance_keeps_later_work_and_experiments_closed(self) -> None:
        text = MASTER_RECORD.read_text(encoding="utf-8")

        for required in (
            "S6-T5.3 DenseRetriever 已通过人工验收",
            "HUMAN_ACCEPTED",
            "S6-T5.4 ContentResolver 尚未批准",
            "正式 RAG 安全实验：**Not started**",
            "RESOLVED_BY_VERSIONED_PUBLIC_METADATA_CONTRACT",
            "candidate_count",
            "ENGINEERING_VALIDATION",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

        self.assertNotIn("S6-T5.3 | DenseRetriever | 透明 Dense Retrieval | 已完成，待人工验收", text)


if __name__ == "__main__":
    unittest.main()
