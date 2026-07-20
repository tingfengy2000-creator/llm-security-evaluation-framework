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


if __name__ == "__main__":
    unittest.main()
